#!/usr/bin/env python3
"""Manually launched, finite GitHub -> Codex -> GitHub -> CC controller."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

from agent_workflow import (ROOT, CONTROL_ROOT, STATES, Engine, Gate, GitHub, LiveTools, Locked, RemoteError,
                            clean_text, digest, git, local_lock, parse_task, relative, state_label, trusted, trusted_author, review_prompt,
                            bind_lease,recover_locks,trusted_lease_path)


def preview(hub, policy, issues, required_agent=None, inventory=None):
    output = []
    blockers = []
    for item in inventory if inventory is not None else issues:
        labels = [x for x in item['labels'] if x in STATES]
        if trusted_author(item, policy) and (not trusted(item, policy) or len(labels) != 1 or labels[0] in {'USER_DECISION_REQUIRED', 'FAILED', 'CODEX_RUNNING', 'CC_REVIEWING'}):
            blockers.append(item['number'])
    for issue in issues:
        current = [x for x in issue['labels'] if x in STATES]
        row = {'detected_issue': issue['number'], 'current_state': current[0] if len(current) == 1 else 'INVALID',
               'intended_agent': None, 'intended_action': 'STOP', 'next_state': None}
        if not trusted(issue, policy):
            row['intended_action'] = 'REJECT_UNAUTHORIZED_SOURCE'
            output.append(row)
            continue
        try:
            fields, state, _ = Engine(hub, None, policy).context(issue)
            task, current = fields['Task ID'], state['state']
            row['task_id'] = task
            actor = 'codex' if current in {'READY_FOR_CODEX', 'CHANGES_REQUESTED'} else 'cc' if current == 'READY_FOR_CC_REVIEW' else None
            row['intended_agent'] = actor
            if actor:
                plan = policy['plans'].get(task, {})
                if required_agent and actor != required_agent:
                    row['intended_action'] = 'WRONG_AGENT_FOR_STATE'
                elif not plan or plan.get('issue_number') != issue['number'] or plan.get('body_sha256') != digest(issue['body']) or not plan.get(actor + '_enabled'):
                    row.update(intended_action='OWNER_PLAN_REQUIRED', next_state='USER_DECISION_REQUIRED')
                elif state['codex_attempts'] >= min(3, policy['max_codex_attempts'], fields['limits'][0]) and actor == 'codex' or state['cc_rounds'] >= min(3, policy['max_cc_review_rounds'], fields['limits'][1]):
                    row.update(intended_action='ITERATION_LIMIT', next_state='USER_DECISION_REQUIRED')
                else:
                    row.update(intended_action='RUN_' + actor.upper(), next_state='CODEX_RUNNING' if actor == 'codex' else 'CC_REVIEWING')
            elif current == 'DONE':
                row['intended_action'] = 'SKIP_DONE'
            else:
                row['intended_action'] = 'STOP_OR_RECONCILE'
        except Gate:
            row.update(intended_action='OWNER_RECONCILIATION_REQUIRED', next_state='USER_DECISION_REQUIRED')
        output.append(row)
    if blockers:
        for row in output:
            if row['intended_action'].startswith('RUN_'):
                row.update(intended_action='GLOBAL_STOP', next_state=row['current_state'])
    print(json.dumps({'dry_run': True, 'blocked_by_issues': blockers, 'issues': output}, indent=2))
    return output


def setup_labels(hub):
    existing = {x['name'] for x in hub.api(hub.prefix + '/labels?per_page=100')}
    for state in STATES:
        if state not in existing:
            color = 'B60205' if state in {'FAILED', 'USER_DECISION_REQUIRED'} else '0E8A16' if state == 'DONE' else '1D76DB'
            hub.api(hub.prefix + '/labels', 'POST', {'name': state, 'color': color, 'description': 'Agent workflow state; exactly one per task'})
    print('Workflow labels ready: ' + ', '.join(STATES))


def manual_handoff(hub, tools, policy, issue, task_id, report, base):
    """Register already tested/pushed manual Codex work; never performs a review."""
    fields = parse_task(issue['body'])
    plan = policy['plans'].get(task_id, {})
    if not trusted(issue, policy) or fields['Task ID'] != task_id or not plan.get('manual_handoff'):
        raise Gate('Manual handoff is not approved for this issue.')
    if plan.get('issue_number') != issue['number'] or plan.get('body_sha256') != digest(issue['body']):
        raise Gate('Manual handoff source does not match the pinned plan.')
    head = tools.preflight(policy['repository'])
    if hub.head() != head:
        raise Gate('Manual handoff must already be pushed to the default branch.')
    report = relative(report)
    if not report.startswith('collaboration/codex-reports/') or not report.endswith('_' + task_id + '.md'):
        raise Gate('Unexpected report path.')
    text = hub.artifact(report, head)
    import re
    match = re.search(r'(?m)^# (?:Git Commit|Commit SHA)\s+([0-9a-f]{40,64})\b', text)
    if not match:
        raise Gate('Report has no completed task commit SHA.')
    git('merge-base', '--is-ancestor', base, head)
    tests = tools.tests(plan['required_tests'])
    packet_bytes = len(review_prompt(fields, text, tools.diff(base, head), tests, policy['max_review_bytes']).encode('utf-8'))
    state, version = hub.ledger(issue['number'])
    if state and state['state'] == 'READY_FOR_CC_REVIEW' and state.get('handoff', {}).get('head') == head:
        print('Manual handoff already registered; no review was run.')
        return
    if state_label(issue) != 'CODEX_RUNNING' or state is not None:
        raise Gate('Manual bootstrap requires an unregistered CODEX_RUNNING issue.')
    state = {'state': 'CODEX_RUNNING', 'body_sha256': digest(issue['body']), 'codex_attempts': 1, 'cc_rounds': 0,
             'history': [{'agent': 'codex', 'task_id': task_id, 'iteration': 1, 'duration_seconds': None,
                          'usage': 'UNKNOWN', 'mode': 'manual implementation; no headless agent invoked'}],
             'handoff': {'base': base, 'head': head, 'task_sha': match[1], 'report': report, 'tests': tests, 'review_context_bytes': packet_bytes}}
    engine = Engine(hub, tools, policy)
    version = hub.save(issue['number'], state, None)
    hub.comment(issue['number'], '## Codex handoff\n```json\n' + json.dumps(state['handoff'], ensure_ascii=False) + '\n```\nIndependent Claude review is pending. Codex has not approved DONE.')
    engine.save(issue, state, version, 'READY_FOR_CC_REVIEW', 'codex')
    engine.notification('WARNING', 'Ready for Claude review', task_id + ': implementation synced; independent review pending.')
    print('READY_FOR_CC_REVIEW; no Claude invocation and no DONE transition.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository')
    parser.add_argument('--issue', type=int)
    parser.add_argument('--task-id')
    parser.add_argument('--agent', choices=['codex', 'cc'])
    parser.add_argument('--one-step', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--setup-labels', action='store_true')
    parser.add_argument('--smoke-lock', action='store_true')
    parser.add_argument('--manual-handoff', action='store_true')
    parser.add_argument('--report')
    parser.add_argument('--base')
    parser.add_argument('--poll-seconds',type=float,default=30)
    parser.add_argument('--max-polls',type=int,default=60)
    parser.add_argument('--max-runtime',type=int,default=7200)
    parser.add_argument('--resume',action='store_true',help='Recover only verified durable handoff/review, never uncertain running work')
    parser.add_argument('--recover-locks',action='store_true',help='Operator-only: verified dead local owner, matching trusted identity and remote markers; no state/counter reset')
    args = parser.parse_args()
    if not 1<=args.poll_seconds<=300 or not 1<=args.max_polls<=120 or not 30<=args.max_runtime<=21600:
        raise Gate('Polling/runtime budget outside approved bounds.')
    policy = json.loads((CONTROL_ROOT / 'automation/policy.json').read_text(encoding='utf-8'))
    if (CONTROL_ROOT/'runtime/AUTO_STOP.json').exists() and not args.dry_run:
        raise Gate('Trusted controller emergency stop exists; owner reconciliation required.')
    repo = args.repository or policy['repository']
    if repo != policy['repository']:
        raise Gate('Repository must match the checked-in owner policy.')
    hub, tools = GitHub(repo), LiveTools()
    if args.recover_locks:
        if not args.issue or args.dry_run:raise Gate('Recovery requires an explicit approved Issue; no implicit dry-run mutation.')
        recover_locks(hub,policy,hub.issue(args.issue),ROOT/git('rev-parse','--git-path','agent-workflow.lock'))
        print('Owned dead-controller leases recovered; task state/counters untouched. Use --resume to validate durable evidence.')
        return 0
    stop = ROOT / git('rev-parse', '--git-path', 'AUTO_STOP.json')
    tools.stop_file = stop
    if args.setup_labels:
        if args.dry_run:
            print(json.dumps({'dry_run': True, 'labels_to_ensure': STATES}))
        else:
            setup_labels(hub)
        return 0
    all_inventory = hub.issues()
    # Only explicitly enabled owner-pinned plans drive work. Unrelated Issues,
    # comments/commits and the disabled historical AUTO-001 plan grant no authority.
    approved_numbers={p['issue_number'] for p in policy['plans'].values() if p.get('codex_enabled') or (p.get('cc_enabled') and not p.get('manual_handoff'))}
    inventory=[item for item in all_inventory if item['number'] in approved_numbers]
    issues = [hub.issue(args.issue)] if args.issue else inventory
    if args.dry_run:
        preview(hub, policy, issues, args.agent, inventory)
        if stop.exists():
            print('LOCAL STOP exists: reconcile before any live execution.')
        return 0
    if args.issue and args.issue not in approved_numbers and not (args.manual_handoff or args.smoke_lock):
        print('No enabled pinned plan for this Issue; unrelated activity ignored. No mutation/model call.')
        return 0
    if stop.exists():
        raise Gate('Persistent local emergency stop exists; User must reconcile it.')
    authorized = [x for x in issues if trusted(x, policy)]
    if len(authorized) != len(issues):
        print('Unauthorized sources rejected; no comments or state mutations on them.')
    for issue in [x for x in inventory if trusted_author(x, policy)]:
        if not trusted(issue, policy):
            tools.notify('WARNING', 'User decision required', 'An owner task has an unapproved editor. Inspect GitHub before continuing.')
            print('STOP: owner task source/editor requires reconciliation.')
            return 2
        target_manual = args.manual_handoff and issue['number'] == args.issue and state_label(issue) == 'CODEX_RUNNING'
        if state_label(issue) in {'USER_DECISION_REQUIRED', 'FAILED', 'CODEX_RUNNING', 'CC_REVIEWING'} and not (target_manual or args.smoke_lock or (args.resume and args.issue==issue['number'] and state_label(issue) in {'CODEX_RUNNING','CC_REVIEWING'})):
            tools.notify('WARNING', 'Agent automation stopped', f'Issue #{issue["number"]} requires User reconciliation.')
            print('STOP: issue requires decision/reconciliation; no agent launched.')
            return 2
    candidates = [x for x in authorized if x.get('open') and state_label(x) != 'DONE']
    if not candidates:
        print('No eligible task. DONE and unauthorized issues are not executed.')
        return 0
    issue = candidates[0]  # one issue per invocation; follow-ups wait for the next invocation
    pending_gate = None
    try:
        fields = parse_task(issue['body'])
    except Gate as exc:
        pending_gate, fields = exc, {}
    if args.task_id and fields and fields['Task ID'] != args.task_id:
        raise Gate('Task ID differs from GitHub issue.')
    if args.agent:
        expected = 'cc' if state_label(issue) == 'READY_FOR_CC_REVIEW' else 'codex'
        if args.agent != expected:
            raise Gate('Runner role is not eligible for current state.')
    lock = ROOT / git('rev-parse', '--git-path', 'agent-workflow.lock')
    with local_lock(lock) as record, hub.lock(issue['number']) as marker:
        bind_lease(record,lock,hub,issue,marker,policy)
        try:
            if pending_gate:
                raise pending_gate
            if args.smoke_lock:
                print('Local + atomic remote lock acquired; no model invoked.')
                try:
                    with hub.lock(issue['number']):
                        raise RuntimeError('Mutual exclusion test unexpectedly acquired twice.')
                except Locked:
                    print('Second acquisition rejected: PASS. Owned lock refs will be released.')
                return 0
            if args.manual_handoff:
                if not all((args.task_id, args.report, args.base)):
                    raise Gate('Manual handoff requires task ID, report and base.')
                manual_handoff(hub, tools, policy, hub.issue(issue['number']), args.task_id, args.report, args.base)
                return 0
            engine = Engine(hub, tools, policy)
            limit = 1 if args.one_step or args.agent else min(6, max(1, policy['max_steps']))
            deadline=time.monotonic()+args.max_runtime
            steps=0
            for poll in range(args.max_polls):
                if time.monotonic()>=deadline or steps>=limit:
                    break
                issue = hub.issue(issue['number'])
                with tools.execution_lease():
                    if args.resume and state_label(issue) in {'CODEX_RUNNING','CC_REVIEWING'}:
                        state=engine.recover(issue)
                    else:
                        state=engine.step(issue)
                steps+=1
                print(json.dumps({'issue': issue['number'], 'state': state}))
                if state in {'DONE', 'USER_DECISION_REQUIRED', 'FAILED', 'CODEX_RUNNING', 'CC_REVIEWING'}:
                    return 0 if state == 'DONE' else 2
                if steps<limit and poll+1<args.max_polls:
                    time.sleep(min(args.poll_seconds,max(0,deadline-time.monotonic())))
            # A bounded invocation ends; persistent counters protect the next invocation too.
            print('Bounded step budget exhausted; no background continuation.')
            return 0
        except Gate as exc:
            state, version = hub.ledger(issue['number'])
            if state is None:
                state = {'state': state_label(issue), 'body_sha256': digest(issue['body']), 'codex_attempts': 0, 'cc_rounds': 0, 'history': []}
            Engine(hub, tools, policy).gate(issue, state, version, clean_text(str(exc), 8000))
            return 2
        except BaseException as exc:
            stop.write_text(json.dumps({'issue': issue['number'], 'status': 'LOCAL ONLY — NOT SYNCED',
                                        'error_type': type(exc).__name__, 'at': datetime.now(timezone.utc).isoformat()}), encoding='utf-8')
            tools.notify('FAILED', 'Agent automation stopped', 'Remote state may be incomplete. Reconcile before restarting.')
            raise


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (Gate, Locked, RemoteError) as exc:
        print('STOP: ' + str(exc))
        raise SystemExit(2)
    except KeyboardInterrupt:
        print('User stopped workflow. Reconcile running state before resuming.')
        raise SystemExit(130)
    except Exception as exc:
        print('FAILED / LOCAL ONLY — NOT SYNCED: ' + type(exc).__name__)
        raise SystemExit(1)
