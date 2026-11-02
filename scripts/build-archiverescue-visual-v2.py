"""Vector-only candidate authoring; never overwrites the baseline or Skill ZIP."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re

import pymupdf as pdf

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'submission/round1/archiverescue'
SOURCE = BASE / 'ArchiveRescue_Proposal_VISUAL_V2.md'
OUTPUT = BASE / 'ArchiveRescue_Proposal_VISUAL_V2.pdf'
EVIDENCE = ROOT / 'collaboration/test-results/ARCHIVERESCUE-PROPOSAL-VISUAL-REDESIGN-001.json'
PREVIEW = ROOT / 'tmp/archiverescue-visual-v2'
PROTECTED = {
    'ArchiveRescue_Proposal.pdf': '360a372dc79459bb81cd744a8acc2f622e79893ffeb4b9ca2e1fdc7887b3c1fc',
    'ArchiveRescue_Proposal.md': None,
    'ArchiveRescue_Pretest_Skill.zip': '732abef29c100b44d49e3cc0bb2ace4e7bc829d40c596bf5deb8b14851117d77',
    'skill/SKILL.md': '3819b43d6dae1e3c9fc84df14843c7a93f3a7955f169305e35f7474aa3d634f5',
}
INK = (0.13, 0.20, 0.22)
TEAL = (0.29, 0.46, 0.46)
PALE = (0.91, 0.95, 0.94)
WARM = (0.93, 0.89, 0.82)
LINE = (0.68, 0.75, 0.74)
MUTED = (0.33, 0.39, 0.40)
PAGE = (595.28, 841.89)
LEFT, RIGHT = 45, 550.28


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(text):
    return ' '.join(text.translate(str.maketrans({'“': '"', '”': '"', '’': "'", '—': '-'})).split())


def answers(text):
    return re.findall(r'^## Q(\d+)\. (.*?)\n\n(.*?)(?=\n## |\Z)', text, re.M | re.S)


def settings():
    baseline = (BASE / 'ArchiveRescue_Proposal.md').read_text(encoding='utf-8')
    source = SOURCE.read_text(encoding='utf-8')
    qa = answers(source)
    assert qa == answers(baseline), 'Questions/answers must remain exactly canonical'
    assert [int(n) for n, q, a in qa] == list(range(1, 11))
    design = json.loads(re.search(r'```json\n(.*?)\n```', source, re.S).group(1))
    disclosure = source.split('## Component and AI disclosure\n\n')[1].split('\n## Visual layout source')[0].strip()
    assert disclosure == baseline.split('## Component and AI disclosure\n\n')[1].strip()
    return qa, design, disclosure


def wrapped(text, font, size, width):
    rows, line = [], ''
    for word in normalized(text).split():
        assert pdf.get_text_length(word, fontname=font, fontsize=size) <= width, ('word exceeds text box', word)
        candidate = (line + ' ' + word).strip()
        if pdf.get_text_length(candidate, fontname=font, fontsize=size) > width:
            assert line
            rows.append(line)
            line = word
        else:
            line = candidate
    return rows + ([line] if line else [])


def text(page, value, x, y, width, size=11.2, bold=False, color=INK, leading=None):
    font = 'hebo' if bold else 'helv'
    leading = leading or size * 1.45
    for row in wrapped(value, font, size, width):
        page.insert_text((x, y), row, fontsize=size, fontname=font, color=color)
        y += leading
    return y


def header(doc, number):
    page = doc.new_page(width=PAGE[0], height=PAGE[1])
    page.draw_rect(pdf.Rect(LEFT, 36, LEFT + 5, 90), color=None, fill=TEAL)
    text(page, 'ArchiveRescue', LEFT + 17, 59, 470, 28, True)
    text(page, 'Companion-Aware NAS Intake', LEFT + 18, 81, 470, 12, color=MUTED)
    text(page, 'Unleash Your Creativity / Round 1 Proposal / Visual V2 candidate', LEFT, 105, 505, 9.5, color=MUTED)
    page.draw_line((LEFT, 117), (RIGHT, 117), color=LINE, width=0.6)
    text(page, 'ArchiveRescue / Proposal candidate', LEFT, 815, 400, 9, color=MUTED)
    text(page, f'{number} / 3', RIGHT - 27, 815, 28, 9, color=MUTED)
    return page


def question(page, qa, number, y, body=True, x=LEFT, width=RIGHT - LEFT):
    n, q, answer = qa[number - 1]
    y = text(page, f'Q{n}. {q}', x, y, width, 11.2, True) + 5
    if body:
        y = text(page, answer, x, y, width, 11.2) + 15
    return y


def arrow(page, points, color=TEAL):
    shape = page.new_shape()
    shape.draw_polyline([pdf.Point(*p) for p in points])
    x, y = points[-1]
    px, py = points[-2]
    dx, dy = x - px, y - py
    length = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / length, dy / length
    shape.draw_polyline([pdf.Point(x - 4 * ux + 2.5 * uy, y - 4 * uy - 2.5 * ux),
                         pdf.Point(x, y), pdf.Point(x - 4 * ux - 2.5 * uy, y - 4 * uy + 2.5 * ux)])
    shape.finish(color=color, width=0.75)
    shape.commit()


def plane(page, x, y, width, height, fill=PALE, offset=5):
    shape = page.new_shape()
    shape.draw_polyline([pdf.Point(x + offset, y), pdf.Point(x + width, y),
                         pdf.Point(x + width - offset, y + height), pdf.Point(x, y + height),
                         pdf.Point(x + offset, y)])
    shape.finish(color=LINE, fill=fill, width=0.6, closePath=True)
    shape.commit()


def workflow(page, y, design):
    labels = design['workflow_labels']
    pieces = design['workflow_answer_fragments']
    width, height, gap = (RIGHT - LEFT - 3 * 13) / 4, 127, 38
    boxes = []
    for i in range(8):
        col = i if i < 4 else 7 - i
        top = y if i < 4 else y + height + gap
        rect = pdf.Rect(LEFT + col * (width + 13), top, LEFT + col * (width + 13) + width, top + height)
        boxes.append(rect)
    for i, rect in enumerate(boxes):
        fill = PALE if i < 4 else WARM
        if i in (0, 7):
            plane(page, rect.x0 + 3, rect.y0 - 6, rect.width - 1, 12, fill)
        if i == 4:
            plane(page, rect.x0, rect.y0, rect.width, rect.height, WARM, 9)
        else:
            page.draw_rect(rect, color=LINE, fill=fill, width=0.6)
        x, top = rect.x0 + 10, rect.y0 + 21
        label = labels[i]
        top = text(page, label, x, top, rect.width - 20, 10.5, True, color=INK) + 6
        if pieces[i]:
            top = text(page, pieces[i], x, top, rect.width - 20, 10.5, color=MUTED)
        assert top < rect.y1 - 2, ('workflow overflow', i, top, rect.y1)
    for i in range(7):
        a, b = boxes[i], boxes[i + 1]
        if i == 3:
            arrow(page, [(a.x0 + a.width / 2, a.y1 + 2), (b.x0 + b.width / 2, b.y0 - 4)])
        elif i < 3:
            arrow(page, [(a.x1 + 1, a.y0 + 64), (b.x0 - 2, b.y0 + 64)])
        else:
            arrow(page, [(a.x0 - 1, a.y0 + 64), (b.x1 + 2, b.y0 + 64)])
    return text(page, design['workflow_cancellation'], LEFT, y + height * 2 + gap + 24,
                RIGHT - LEFT, 11.2, color=MUTED) + 10


def exceptions(page, y, design):
    width = (RIGHT - LEFT - 24) / 3
    for i, case in enumerate(design['cases']):
        x = LEFT + i * (width + 12)
        r = pdf.Rect(x, y, x + width, y + 235)
        page.draw_rect(r, color=LINE, fill=PALE if i == 0 else ((0.96, 0.95, 0.92) if i == 1 else (0.95, 0.95, 0.95)), width=0.6)
        top = text(page, case['title'], x + 11, y + 22, width - 22, 11.5, True)
        top = text(page, case['condition'], x + 11, top + 5, width - 22, 10.7)
        shape_y = y + 94
        if i < 2:
            plane(page, x + 18, shape_y + 9, 48, 13, PALE)
            plane(page, x + 20, shape_y, 48, 13, TEAL)
            plane(page, x + width - 66, shape_y + 9, 48, 13, WARM)
            plane(page, x + width - 64, shape_y, 48, 13, TEAL if i == 0 else WARM)
            page.draw_line((x + width / 2 - 5, shape_y + 5), (x + width / 2 + 5, shape_y + 5), color=TEAL, width=1)
            page.draw_line((x + width / 2 - 5, shape_y + 9), (x + width / 2 + 5, shape_y + 9), color=TEAL, width=1)
            if i == 1:
                page.draw_line((x + width / 2 - 4, shape_y + 13), (x + width / 2 + 4, shape_y + 1), color=INK, width=1)
        else:
            plane(page, x + 55, shape_y, 48, 22, PALE)
            page.draw_line((x + 55, shape_y), (x + 103, shape_y + 22), color=MUTED, width=0.9)
        top = text(page, case['outcome'], x + 11, y + 140, width - 22, 10.7)
        if case.get('extra'):
            top = text(page, case['extra'], x + 11, top + 7, width - 22, 10.7, True)
        assert top < r.y1 - 3, ('case overflow', i, top, r.y1)
    return y + 235 + 26


def make_pdf(qa, design, disclosure):
    doc = pdf.open()
    page = header(doc, 1)
    y = 145
    for number in (1, 2, 3):
        y = question(page, qa, number, y)
    y = question(page, qa, 4, y + 4, False)
    y = workflow(page, y + 5, design)
    assert y < 790, ('page 1 overflow', y)

    page = header(doc, 2)
    plane(page, LEFT, 144, RIGHT - LEFT, 80, PALE, 14)
    text(page, design['takeaway'], LEFT + 20, 174, RIGHT - LEFT - 42, 22, True, color=TEAL, leading=32)
    y = question(page, qa, 5, 260)
    y = question(page, qa, 6, y + 20, False)
    for paragraph in design['capability_answer_fragments']:
        page.draw_line((LEFT + 4, y - 9), (LEFT + 4, y + 13), color=TEAL, width=2)
        y = text(page, paragraph, LEFT + 18, y, RIGHT - LEFT - 18, 11.2) + 10
    y = question(page, qa, 7, y + 18, False)
    for paragraph in design['technical_answer_fragments']:
        y = text(page, paragraph, LEFT, y, RIGHT - LEFT, 11.2) + 8
    assert y < 790, ('page 2 overflow', y)

    page = header(doc, 3)
    y = question(page, qa, 8, 145)
    y = question(page, qa, 9, y + 8, False)
    y = exceptions(page, y + 5, design)
    y = question(page, qa, 10, y)
    y = text(page, 'Component and AI disclosure', LEFT, y + 5, RIGHT - LEFT, 9.5, True)
    y = text(page, disclosure, LEFT, y + 3, RIGHT - LEFT, 9.0, color=MUTED)
    assert y < 795, ('page 3 overflow', y)
    doc.set_metadata({'title': 'ArchiveRescue - Companion-Aware NAS Intake - Visual V2',
                      'subject': 'Round 1 proposal candidate; custom layout', 'author': '',
                      'creator': 'ArchiveRescue vector proposal authoring'})
    doc.save(OUTPUT, garbage=4, deflate=True, no_new_id=True)
    doc.close()


def validate(qa, design, disclosure):
    alpha = lambda s: len(re.findall(r'[A-Za-z0-9]+', s))
    assert ' '.join(design['workflow_answer_fragments'][:1]).startswith('and archive')
    reconstructed_q4 = 'Select staged files ' + ' '.join(design['workflow_answer_fragments'][:5])
    # The sixth node's title contains an original answer clause, not extra prose.
    reconstructed_q4 += ' ' + design['workflow_labels'][5] + ' ' + design['workflow_answer_fragments'][5]
    reconstructed_q4 += ' ' + ' '.join(design['workflow_labels'][6:]) + ' ' + design['workflow_cancellation']
    assert normalized(reconstructed_q4) == normalized(qa[3][2])
    assert normalized(' '.join(design['capability_answer_fragments'])) == normalized(qa[5][2])
    assert normalized(' '.join(design['technical_answer_fragments'])) == normalized(qa[6][2])
    reconstructed_q9 = ' '.join(' '.join(c[k] for k in ('title', 'condition', 'outcome')) for c in design['cases'])
    assert normalized(reconstructed_q9) == normalized(qa[8][2])
    extra = [design['workflow_labels'][i] for i in (1, 2, 3, 4)]
    extra += [design['takeaway']] + [c['extra'] for c in design['cases'] if c.get('extra')]
    canonical = ' '.join(a for n, q, a in qa)
    diagram_canonical = qa[3][2] + ' ' + qa[8][2]
    counts = {'qa_whitespace': len(canonical.split()), 'qa_alphanumeric': alpha(canonical),
              'added_diagram_whitespace': sum(len(s.split()) for s in extra),
              'added_diagram_alphanumeric': sum(alpha(s) for s in extra)}
    counts['all_substantive_whitespace'] = counts['qa_whitespace'] + counts['added_diagram_whitespace']
    counts['all_substantive_alphanumeric'] = counts['qa_alphanumeric'] + counts['added_diagram_alphanumeric']
    declaration = disclosure.split('Codex:', 1)[1].split('Sources:', 1)[0]
    declaration = 'Codex:' + declaration
    counts['nonlicense_disclosure_whitespace'] = len(declaration.split())
    counts['nonlicense_disclosure_alphanumeric'] = alpha(declaration)
    counts['secondary_with_nonlicense_disclosure_whitespace'] = counts['all_substantive_whitespace'] + len(declaration.split())
    counts['secondary_with_nonlicense_disclosure_alphanumeric'] = counts['all_substantive_alphanumeric'] + alpha(declaration)
    counts['diagram_whitespace_including_reused_answers'] = len(diagram_canonical.split()) + counts['added_diagram_whitespace']
    counts['diagram_alphanumeric_including_reused_answers'] = alpha(diagram_canonical) + counts['added_diagram_alphanumeric']
    assert counts['secondary_with_nonlicense_disclosure_alphanumeric'] <= 500
    assert counts['secondary_with_nonlicense_disclosure_whitespace'] <= 500
    assert OUTPUT.stat().st_size <= 1_000_000
    with pdf.open(OUTPUT) as doc:
        assert len(doc) == 3
        extracted = '\n'.join(p.get_text() for p in doc)
        flat = normalized(extracted)
        for n, q, answer in qa:
            assert normalized(f'Q{n}. {q}') in flat, n
            if int(n) not in (4, 6, 7, 9):
                assert normalized(answer) in flat, ('answer missing', n)
        for fragment in [*design['workflow_labels'], *design['workflow_answer_fragments'],
                         *design['capability_answer_fragments'], *design['technical_answer_fragments'],
                         design['workflow_cancellation'], *extra, disclosure]:
            if fragment:
                assert normalized(fragment) in flat, ('fragment missing', fragment)
        for c in design['cases']:
            for field in ('title', 'condition', 'outcome'):
                assert normalized(c[field]) in flat
        assert not re.search(r'(?i)devon|C:\\|[a-f0-9]{40}\b|session log|/Users/', extracted)
        assert doc.embfile_count() == 0 and not doc.is_form_pdf and not doc.is_encrypted
        assert not doc.get_ocgs()
        size_floor = 100
        for page in doc:
            assert not page.get_images() and not page.get_links() and not list(page.annots() or [])
            lines = []
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    rect = pdf.Rect(line['bbox'])
                    assert rect.x0 >= 30 and rect.y0 >= 20 and rect.x1 <= PAGE[0] - 20 and rect.y1 <= PAGE[1] - 15
                    lines.append(rect)
                    size_floor = min(size_floor, *(s['size'] for s in line['spans']))
            for i, a in enumerate(lines):
                for b in lines[i + 1:]:
                    intersection = a & b
                    assert intersection.is_empty or intersection.get_area() <= 1.0, ('text overlap', page.number + 1, a, b)
            page.get_pixmap(matrix=pdf.Matrix(1.5, 1.5)).save(PREVIEW / f'page-{page.number + 1}.png')
    spec = importlib.util.spec_from_file_location('baseline_builder', ROOT / 'scripts/build-archiverescue-round1.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Parse the exact candidate format; generic binary scanner remains unchanged.
    findings = module.scan_artifact('ArchiveRescue_Proposal.pdf', OUTPUT.read_bytes())
    for path in [SOURCE, Path(__file__)]:
        findings += module.scan_artifact(path.relative_to(ROOT).as_posix(), path.read_bytes())
    module.scan_module().show(3, findings)
    assert not findings
    result = {'verdict': 'VISUAL_V2_READY_FOR_USER_REVIEW', 'pages': 3,
              'pdf_bytes': OUTPUT.stat().st_size, 'pdf_sha256': digest(OUTPUT), 'counts': counts,
              'qa_content_unchanged': True, 'candidate_source': SOURCE.relative_to(ROOT).as_posix(),
              'minimum_font_points': size_floor, 'overlapping_text_lines': 0,
              'off_page_text_lines': 0, 'vector_only': True, 'secret_findings': 0,
              'protected_sha256': {name: digest(BASE / name) for name in PROTECTED},
              'render_previews': [f'tmp/archiverescue-visual-v2/page-{i}.png' for i in (1, 2, 3)]}
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    for name, expected in PROTECTED.items():
        if expected:
            assert digest(BASE / name) == expected, ('protected file changed', name)
    before = {name: digest(BASE / name) for name in PROTECTED}
    qa, design, disclosure = settings()
    PREVIEW.mkdir(parents=True, exist_ok=True)
    if not args.verify_only:
        make_pdf(qa, design, disclosure)
    validate(qa, design, disclosure)
    assert before == {name: digest(BASE / name) for name in PROTECTED}


if __name__ == '__main__':
    main()
