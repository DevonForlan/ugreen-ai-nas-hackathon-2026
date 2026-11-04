"""ArchiveRescue Devpost STATIC PROOF final (ARCHIVERESCUE-DEVPOST-MEDIA-PACKAGE).

Designed rendering of RECORDED data only; not a terminal screenshot, not NAS runtime.
Values come from collaboration/test-results/ARCHIVERESCUE-ROUND1-BUILD-001/extracted-checker.json
and validation.json; excerpts are verbatim from submission/round1/archiverescue/skill/SKILL.md.
The script re-verifies those sources before drawing and refuses to render on mismatch.
Shares the canvas/palette of build-archiverescue-media-final.py.
"""
import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('mf', ROOT / 'scripts/build-archiverescue-media-final.py')
mf = importlib.util.module_from_spec(spec); spec.loader.exec_module(mf)
C, M, W, font, Canvas = mf.C, mf.M, mf.W, mf.font, mf.Canvas

BASE = ROOT / 'submission/round1/archiverescue'
EVID = ROOT / 'collaboration/test-results/ARCHIVERESCUE-ROUND1-BUILD-001'
EVIDENCE_DATE = '2026-11-02'  # date of the recorded check (commit e80f1f5)
EXCERPTS = [  # (exact SKILL.md section heading, delegated agent or None for prose, verbatim text)
    ('1. Inventory and genuine hashes', 'file-agent',
     'Return genuine complete SHA-256 values associated with actual paths; '
     'do not estimate hashes or invent missing results.'),
    ('4. Fresh destination and individual copies', 'file-agent',
     'For each approved regular file individually use cpmv with the exact src, approved destination '
     'directory as dst, type copy and overwrite false, retaining the basename. '
     'Obtain gateway approval for each write.'),
    ('5. Verify actual destination bytes', None,
     'Each file is verified only when destination, reviewed source and post-copy source '
     'SHA-256 all match, with the final source recheck unchanged.'),
]


def load_and_verify():
    chk = json.loads((EVID / 'extracted-checker.json').read_text(encoding='utf-8'))
    val = json.loads((EVID / 'validation.json').read_text(encoding='utf-8'))
    assert chk['status'] == 'static-pass' and chk['diagnostics'] == []
    assert val['nas_runtime'] == 'NOT_TESTED'
    skill = (BASE / 'skill/SKILL.md').read_text(encoding='utf-8')
    flat = ' '.join(skill.split())
    for sec, _, text in EXCERPTS:
        assert ('## ' + sec) in skill.splitlines(), 'heading not found: ' + sec
        assert text in flat, 'excerpt not verbatim: ' + text[:40]
    z = zipfile.ZipFile(BASE / 'ArchiveRescue_Pretest_Skill.zip')
    members = {i.filename: (i.file_size, hashlib.sha256(z.read(i)).hexdigest()) for i in z.infolist()}
    for f in chk['files']:
        assert members[f['path']][1] == f['sha256'], f['path']
    return chk, members


def main():
    chk, members = load_and_verify()
    s = chk['summary']
    c = Canvas()
    c.header('What is built and checked',
             'An authored Skill package passed the official static checker. Real NAS execution remains untested.',
             'STATIC VALIDATION ONLY — NOT NAS RUNTIME')
    top, h = 236, 636
    lw, gap = 884, 32
    rx, rw = M + lw + gap, W - 2 * M - lw - gap

    # left: verbatim Skill excerpts
    c.rect(M, top, lw, h, fill=C['white'], outline=C['line'], r=12, width=1.5)
    c.text(M + 32, top + 30, 'SKILL EXCERPT — INSTRUCTIONS, NOT EXECUTION', font(19, True), C['accent'])
    c.text(M + 32, top + 64, 'Verbatim from SKILL.md in the Round 1 package', font(20), C['muted'])
    y = top + 112
    for sec, agent, text in EXCERPTS:
        c.text(M + 32, y, 'SKILL.md · ' + sec, font(19, True), C['ink'])
        if agent:
            c.text(M + 32, y + 32, 'delegate --target ' + agent, font(19, mono=True), C['accent'])
            qy = y + 70
        else:
            qy = y + 38
        y2 = c.wrap(M + 56, qy, '“' + text + '”', font(22), lw - 100, C['ink'], lh=1.34)
        c.line(M + 34, qy - 4, M + 34, y2 - 6, C['accent'], 4)
        y = y2 + 28

    # right: recorded checker result
    c.rect(rx, top, rw, h, fill=C['cool'], outline=C['line'], r=12, width=1.5)
    c.text(rx + 32, top + 30, 'RECORDED OFFICIAL STATIC CHECK', font(19, True), C['accent'])
    c.text(rx + 32, top + 64, f'Extracted Round 1 Skill ZIP · {EVIDENCE_DATE} · catalog '
           f'{chk["catalog"]["checkedVersion"]}', font(20), C['muted'])
    c.text(rx + 32, top + 140, 'status', font(22), C['muted'], anchor='lm')
    fp = font(34, True)
    pw = c.width(chk['status'], fp) + 48
    c.rect(rx + 120, top + 112, pw, 56, fill=C['accent'], r=28)
    c.text(rx + 120 + pw / 2, top + 140, chk['status'], fp, C['white'], anchor='mm')
    tw = (rw - 64 - 32) / 3
    for i, key in enumerate(('errors', 'warnings', 'info')):
        tx = rx + 32 + i * (tw + 16)
        c.rect(tx, top + 200, tw, 128, fill=C['white'], outline=C['line'], r=10, width=1.5)
        c.text(tx + tw / 2, top + 252, str(s[key]), font(56, True), C['ink'], anchor='mm')
        c.text(tx + tw / 2, top + 302, key, font(21), C['muted'], anchor='mm')
    c.text(rx + 32, top + 376, 'PACKAGE CHECKED · MARKDOWN ONLY, NO SCRIPTS', font(18, True), C['accent'])
    fm, fmb = font(19, mono=True), font(19, True, mono=True)
    c.text(rx + 32, top + 418, 'ArchiveRescue_Pretest_Skill.zip', fmb, C['ink'])
    rows = [('├─ ', 'SKILL.md'), ('└─ ', 'references/usage-notes.md')]
    for k, (branch, name) in enumerate(rows):
        size, digest = members[name]
        yy = top + 458 + k * 70
        c.text(rx + 32, yy, branch + name, fm, C['ink'])
        c.text(rx + 32 + c.width('├─ ', fm), yy + 30, f'{size:,} B · sha256 {digest[:12]}…', fm, C['muted'])

    # bottom: what is not yet tested
    y = top + h + 24
    c.rect(M, y, W - 2 * M, 152, fill=C['gray'], r=12)
    c.text(M + 32, y + 28, 'NOT YET TESTED ON A NAS', font(19, True), C['muted'])
    x, cy = M + 32, y + 100
    for item in ('native hash attribution', 'copy / collision semantics', 'gateway approvals',
                 'save + readback', 'practical latency'):
        f = font(22)
        w = c.width(item, f) + 40
        c.rect(x, cy - 24, w, 48, fill=C['white'], outline=C['line'], r=24, width=1.5)
        c.text(x + w / 2, cy, item, f, C['ink'], anchor='mm')
        x += w + 16
    c.footer('Designed rendering of recorded data — not a terminal screenshot.  Static validation only — not NAS runtime.')
    c.save('ArchiveRescue_StaticProof_Final.png')
    print('ArchiveRescue_StaticProof_Final.png rendered')


if __name__ == '__main__':
    main()
