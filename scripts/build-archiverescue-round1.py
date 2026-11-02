"""Author/validate Round 1 artifacts on the development host, never on NAS.

Requires the already-installed PyMuPDF and the unmodified official UGREEN kit.
Nothing from this script is placed in the submitted Skill ZIP.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
import zipfile

import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'submission/round1/archiverescue'
KIT = ROOT / 'tmp/ARCHIVERESCUE-TECHNICAL-PROOF-001/uliya-skill-kit'
EVIDENCE = ROOT / 'collaboration/test-results/ARCHIVERESCUE-ROUND1-BUILD-001'
ALLOWED = ['SKILL.md', 'references/usage-notes.md']
CHECKER_HASHES = {
    'check-skill.mjs': '6a9e8ad164862ab787f45e577c2e2bc98cfb31cea10f5ec291cb6550eb51fb52',
    'check-lib.mjs': 'a4020044c1138f1937777d8a600df9d304ea00bf4f3bd20ae5e00883ad6542a7',
}
QUESTIONS = [
    'What does your Skill do? (one sentence)',
    'Who is your target user, and what is their problem?',
    'What is your solution?',
    'What is the main user flow?',
    'How is your idea different from existing tools or common AI solutions?',
    'Which UGREEN AI NAS features does your Skill use, and at which step?',
    'What is your technical approach? (Describe the planned Skill workflow, supported NAS CLI capabilities, expert agent orchestration, required inputs, permissions, AI model choices, and data handling, as applicable)',
    'What have you built so far? What is not built yet? What still needs testing on a NAS?',
    'How will you test your Skill if you become a Finalist? Name two core test cases and one edge case.',
    'What are the known limits, risks, or outside dependencies of your Skill?',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def normalize(text):
    return ' '.join(text.translate(str.maketrans({'“': '"', '”': '"', '’': "'", '—': '-'})).split())


def proposal():
    text = (BASE / 'ArchiveRescue_Proposal.md').read_text(encoding='utf-8')
    parts = re.findall(r'^## Q(\d+)\. (.*?)\n\n(.*?)(?=\n## |\Z)', text, re.M | re.S)
    assert [int(n) for n, q, a in parts] == list(range(1, 11)), 'Ten numbered answers required'
    assert [q for n, q, a in parts] == QUESTIONS
    disclosure = text.split('## Component and AI disclosure\n\n', 1)[1].strip()
    return text, parts, disclosure


def lines(text, font, size, width):
    result, current = [], ''
    for word in normalize(text).split():
        candidate = (current + ' ' + word).strip()
        if fitz.get_text_length(candidate, fontname=font, fontsize=size) > width:
            assert current, 'Unbreakable text too wide'
            result.append(current)
            current = word
        else:
            current = candidate
    return result + ([current] if current else [])


def make_pdf(parts, disclosure):
    doc = fitz.open()
    for page_number, group in enumerate((parts[:5], parts[5:]), 1):
        page = doc.new_page(width=595.28, height=841.89)
        page.insert_text((46, 48), 'ARCHIVERESCUE', fontsize=20, fontname='hebo', color=(0.08, 0.24, 0.25))
        page.insert_text((46, 68), 'Companion-Aware NAS Intake | Round 1 Proposal', fontsize=11)
        page.insert_text((46, 85), 'Track: Unleash Your Creativity | Pre-test Skill; NAS runtime untested', fontsize=9)
        page.draw_line((46, 97), (549, 97), color=(0.2, 0.55, 0.5), width=1)
        y = 118
        for number, question, answer in group:
            for line in lines(f'Q{number}. {question}', 'hebo', 10, 503):
                page.insert_text((46, y), line, fontname='hebo', fontsize=10)
                y += 13
            y += 3
            for line in lines(answer, 'helv', 10.5, 503):
                page.insert_text((46, y), line, fontsize=10.5)
                y += 14
            y += 14
        if page_number == 2:
            page.insert_text((46, y), 'Component and AI disclosure', fontsize=9, fontname='hebo')
            y += 13
            for line in lines(disclosure, 'helv', 8, 503):
                page.insert_text((46, y), line, fontsize=8)
                y += 10
        assert y < 793, f'PDF page {page_number} overflow: {y}'
        page.insert_text((46, 817), f'ArchiveRescue | {page_number}/2', fontsize=8, color=(0.4, 0.4, 0.4))
    doc.set_metadata({'title': 'ArchiveRescue - Companion-Aware NAS Intake',
                      'subject': 'Round 1 Proposal', 'author': '', 'creator': 'ArchiveRescue proposal authoring'})
    doc.save(BASE / 'ArchiveRescue_Proposal.pdf', garbage=4, deflate=True, no_new_id=True)
    doc.close()


def make_zip():
    source = BASE / 'skill'
    assert sorted(p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()) == ALLOWED
    with zipfile.ZipFile(BASE / 'ArchiveRescue_Pretest_Skill.zip', 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name in ALLOWED:
            item = zipfile.ZipInfo(name, date_time=(2026, 11, 2, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.create_system = 3
            item.external_attr = 0o100644 << 16
            z.writestr(item, (source / name).read_bytes())


def checker(target, label):
    for name, expected in CHECKER_HASHES.items():
        assert sha((KIT / 'scripts' / name).read_bytes()) == expected, 'Official checker changed'
    command = ['node', str((KIT / 'scripts/check-skill.mjs').relative_to(ROOT)), str(target.relative_to(ROOT))]
    p = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', timeout=60)
    assert not p.stderr.strip(), 'Checker stderr requires investigation'
    result = json.loads(p.stdout)
    (EVIDENCE / f'{label}-checker.json').write_text(p.stdout, encoding='utf-8', newline='\n')
    assert p.returncode == 0 and result['status'] == 'static-pass', result
    assert result['summary']['errors'] == result['summary']['warnings'] == 0
    return {'command': command, 'exit_code': p.returncode, 'result': result}


def scan_module():
    spec = importlib.util.spec_from_file_location('round1_scan', ROOT / 'scripts/scan-codex-secrets.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scan_artifact(name, data):
    """Inspect the two exact-format binary deliverables via decoded content.

    General scanner remains fail-closed for arbitrary binary files. No wildcard
    exclusion or scanner policy change is used. This function also accepts index
    bytes so publication can validate the staged artifact, not just a disk path.
    """
    scanner = scan_module()
    if name == 'ArchiveRescue_Pretest_Skill.zip':
        import io
        findings = []
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            assert z.namelist() == ALLOWED
            for item in z.infolist():
                assert item.file_size <= 1_000_000 and not item.flag_bits & 1
                findings.extend(scanner.scan_blob(f'{name}/{item.filename}', z.read(item)))
        return findings
    if name == 'ArchiveRescue_Proposal.pdf':
        findings = []
        with fitz.open(stream=data, filetype='pdf') as doc:
            assert not doc.is_encrypted and doc.embfile_count() == 0
            assert not doc.get_toc() and not doc.is_form_pdf
            for page in doc:
                assert not page.get_images() and not page.get_links() and not list(page.annots() or [])
                findings.extend(scanner.scan_blob(f'{name}/page-{page.number + 1}', page.get_text().encode()))
            findings.extend(scanner.scan_blob(f'{name}/metadata', json.dumps(doc.metadata).encode()))
            for number in range(1, doc.xref_length()):
                obj = doc.xref_object(number)
                assert not re.search(r'/(?:JavaScript|JS|Launch|OpenAction|AA|EmbeddedFiles|XFA)\b', obj)
                findings.extend((name, line, rule) for line, rule in scanner.scan_text(obj))
                if doc.xref_is_stream(number):
                    stream = doc.xref_stream(number).decode('latin-1')
                    findings.extend((name, line, rule) for line, rule in scanner.scan_text(stream))
        return findings
    return scanner.scan_blob(name, data)


def validate(parts, disclosure):
    pdf = BASE / 'ArchiveRescue_Proposal.pdf'
    archive = BASE / 'ArchiveRescue_Pretest_Skill.zip'
    counts = [len(answer.split()) for n, q, answer in parts]
    total = sum(counts)
    conservative = sum(len(re.findall(r'[A-Za-z0-9]+', a)) for n, q, a in parts)
    assert 430 <= total <= 470 and total <= 480 and conservative <= 500
    assert 0 < pdf.stat().st_size <= 1_000_000
    with fitz.open(pdf) as doc:
        assert len(doc) == 2
        extracted = '\n'.join(p.get_text() for p in doc)
        flat = normalize(extracted)
        for number, question, answer in parts:
            assert normalize(f'Q{number}. {question}') in flat
            assert normalize(answer) in flat, f'Answer {number} differs from Markdown'
        assert normalize(disclosure) in flat
        assert not re.search(r'(?i)devon|C:\\|commit|[a-f0-9]{40}\b|session log', extracted)
        for page in doc:
            page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).save(EVIDENCE.parent.parent.parent / 'tmp' / f'archiverescue-proposal-page-{page.number + 1}.png')
    source_result = checker(BASE / 'skill', 'source')
    tmp_parent = ROOT / 'tmp/ARCHIVERESCUE-ROUND1-BUILD-001'
    tmp_parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix='extracted-', dir=tmp_parent))
    extracted_skill = temporary / 'skill'
    extracted_skill.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.namelist() == ALLOWED and z.testzip() is None
        entries = z.infolist()
        assert len(entries) <= 100 and archive.stat().st_size <= 10_000_000
        assert sum(x.file_size for x in entries) <= 10_000_000
        for x in entries:
            p = PurePosixPath(x.filename)
            assert not p.is_absolute() and '..' not in p.parts and not x.is_dir()
            assert (x.external_attr >> 16) & 0o170000 == 0o100000
            assert x.file_size <= 1_000_000 and p.suffix == '.md'
            data = z.read(x)
            assert data == (BASE / 'skill' / x.filename).read_bytes()
            target = extracted_skill / x.filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    exact_result = checker(extracted_skill, 'extracted')
    assert source_result['result']['files'] == exact_result['result']['files']
    findings = []
    for p in BASE.rglob('*'):
        if p.is_file():
            findings.extend(scan_artifact(p.name if p.suffix in {'.pdf', '.zip'} else p.relative_to(ROOT).as_posix(), p.read_bytes()))
    scanner = scan_module()
    scanner.show(len([p for p in BASE.rglob('*') if p.is_file()]), findings)
    assert not findings, 'Secret scan failed; only redacted findings displayed'
    result = {
        'verdict': 'ROUND1_PACKAGE_READY', 'nas_runtime': 'NOT_TESTED',
        'answer_words_by_question': counts, 'answer_word_count': total,
        'count_method': 'Python str.split() on the ten answer bodies only',
        'conservative_alphanumeric_word_count': conservative,
        'pdf': {'bytes': pdf.stat().st_size, 'sha256': sha(pdf.read_bytes()), 'pages': 2,
                'all_questions_and_answers_match': True, 'selectable_text': True},
        'zip': {'bytes': archive.stat().st_size, 'sha256': sha(archive.read_bytes()),
                'files': len(entries), 'extracted_bytes': sum(x.file_size for x in entries),
                'largest_file_bytes': max(x.file_size for x in entries), 'root_tree': ALLOWED},
        'source_checker': source_result, 'exact_extracted_zip_checker': exact_result,
        'secret_findings': len(findings), 'checker_sha256': CHECKER_HASHES,
    }
    (EVIDENCE / 'validation.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: result[k] for k in ('verdict', 'answer_word_count', 'conservative_alphanumeric_word_count', 'pdf', 'zip')}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true', help='Validate existing outputs without rebuilding')
    args = parser.parse_args()
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    text, parts, disclosure = proposal()
    if not args.verify_only:
        make_pdf(parts, disclosure)
        make_zip()
    validate(parts, disclosure)


if __name__ == '__main__':
    main()
