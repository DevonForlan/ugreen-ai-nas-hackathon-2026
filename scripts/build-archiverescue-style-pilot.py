"""ArchiveRescue Devpost media STYLE PILOT renderer (ARCHIVERESCUE-IMAGE-STYLE-PILOT-001).

Pilot only: four style candidates, not the final media package. Concept diagrams of
planned behavior; nothing here is NAS runtime evidence. Palette and font follow
Proposal Visual V3 (scripts/build-archiverescue-visual-v3.py) without modifying it.
Requires Pillow and the Windows Arial / Consolas fonts.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'submission/round1/archiverescue/devpost-media/style-pilot'
FONTS = Path('C:/Windows/Fonts')
W, H, S = 1800, 1200, 2  # 3:2 output; drawn at 2x then downsampled

C = {k: '#' + v for k, v in {
    'ink': '243A3F', 'accent': '4A7575', 'line': 'ABBDBB', 'cool': 'EAF1F0',
    'warm': 'F3EDE4', 'human': 'E6D8C0', 'gray': 'F1F3F3', 'white': 'FFFFFF',
    'muted': '6E7F82', 'humanline': 'B08F5A'}.items()}
FOOT = 'Concept diagram of planned behavior · not a NAS runtime screenshot · device validation pending'


def font(size, bold=False, mono=False):
    name = ('consolab.ttf' if bold else 'consola.ttf') if mono else ('arialbd.ttf' if bold else 'arial.ttf')
    return ImageFont.truetype(str(FONTS / name), int(size * S))


class Canvas:
    def __init__(self):
        self.im = Image.new('RGB', (W * S, H * S), C['white'])
        self.d = ImageDraw.Draw(self.im)

    def p(self, *xy):
        return [v * S for v in xy]

    def rect(self, x, y, w, h, fill=None, outline=None, width=1.5, r=10, dash=False):
        if dash:
            self.rect(x, y, w, h, fill=fill, r=r)
            for a, b in (((x + r, y), (x + w - r, y)), ((x + r, y + h), (x + w - r, y + h)),
                         ((x, y + r), (x, y + h - r)), ((x + w, y + r), (x + w, y + h - r))):
                self.line(*a, *b, color=outline, width=width, dash=True)
            return
        self.d.rounded_rectangle(self.p(x, y, x + w, y + h), radius=r * S, fill=fill,
                                 outline=outline, width=max(1, int(width * S)) if outline else 0)

    def line(self, x1, y1, x2, y2, color=None, width=2, dash=False):
        color = color or C['accent']
        if not dash:
            self.d.line(self.p(x1, y1, x2, y2), fill=color, width=int(width * S))
            return
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        n = max(1, int(length // 14))
        for i in range(n):
            if i % 2 == 0:
                a, b = i / n, min(1, (i + 1) / n)
                self.d.line(self.p(x1 + (x2 - x1) * a, y1 + (y2 - y1) * a,
                                   x1 + (x2 - x1) * b, y1 + (y2 - y1) * b), fill=color, width=int(width * S))

    def arrow(self, x1, y1, x2, y2, color=None, width=2.5, head=13):
        color = color or C['accent']
        dx, dy = x2 - x1, y2 - y1
        L = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / L, dy / L
        bx, by = x2 - ux * head, y2 - uy * head
        self.line(x1, y1, bx, by, color, width)
        self.d.polygon(self.p(x2, y2, bx - uy * head * 0.55, by + ux * head * 0.55,
                              bx + uy * head * 0.55, by - ux * head * 0.55), fill=color)

    def text(self, x, y, s, f, color=None, anchor='la'):
        self.d.text((x * S, y * S), s, font=f, fill=color or C['ink'], anchor=anchor)

    def wrap(self, x, y, s, f, maxw, color=None, lh=1.32):
        words, line, yy = s.split(), '', y
        step = f.size / S * lh
        for w_ in words:
            t = (line + ' ' + w_).strip()
            if f.getlength(t) / S <= maxw:
                line = t
            else:
                self.text(x, yy, line, f, color); yy += step; line = w_
        if line:
            self.text(x, yy, line, f, color); yy += step
        return yy

    def width(self, s, f):
        return f.getlength(s) / S

    def pill(self, cx, cy, s, f, fill, color, pad=14, outline=None):
        w = self.width(s, f) + pad * 2
        h = f.size / S + pad * 0.9
        self.rect(cx - w / 2, cy - h / 2, w, h, fill=fill, outline=outline, r=h / 2, width=1.5)
        self.text(cx, cy, s, f, color, anchor='mm')
        return w

    def header(self, title, subtitle, kicker='ArchiveRescue · Companion-aware NAS intake'):
        self.text(90, 70, kicker.upper(), font(17, True), C['accent'])
        self.text(90, 100, title, font(46, True))
        self.text(90, 166, subtitle, font(23), C['muted'])
        self.line(90, 212, W - 90, 212, C['line'], 1.5)

    def footer(self, note=FOOT):
        self.line(90, H - 78, W - 90, H - 78, C['line'], 1.5)
        self.text(90, H - 56, note, font(17), C['muted'])
        self.text(W - 90, H - 56, 'STYLE PILOT', font(17, True), C['muted'], anchor='ra')

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        self.im.resize((W, H), Image.LANCZOS).save(OUT / name, optimize=True)


STEPS = [
    ('Select', 'Authorize staging and archive paths; at most 20 files.', 'path authorization'),
    ('Inspect', 'Inventory, metadata and native SHA-256 values.', 'ls · stat · sha256sum'),
    ('Compare', 'Equal bytes vs. same name with different bytes.', 'hash + name comparison'),
    ('Review companion evidence', 'Readable notes / XMP only; unread stays opaque.', 'cat (readable only)'),
    ('Human approval', 'Exact paths, source hashes, complete units, fresh destination.', 'decision gate'),
    ('Fresh copy', 'Non-overwriting copy into a reserved, empty destination.', 'mkdir · cpmv overwrite=false'),
    ('Verify hashes', 'Destination = reviewed source = post-copy source.', 'sha256sum'),
    ('Save + read back', 'Separately approved intake record, compared on readback.', 'save-text · cat'),
]


def workflow_a():
    """Editorial cards: V3 card language, elbow 4 -> 5 continuation."""
    c = Canvas()
    c.header('Planned intake flow', 'Eight bounded steps · human approval before any write · byte verification after')
    x0, cw, gap, ch = 90, 360, 60, 262
    rows = [(282, 'READ-ONLY EVIDENCE · NO WRITES'), (690, 'APPROVED WRITES · HASH-VERIFIED')]
    for r, (y, label) in enumerate(rows):
        c.text(x0, y - 36, label, font(16, True), C['accent'])
        for i in range(4):
            n = r * 4 + i
            title, desc, _ = STEPS[n]
            x = x0 + i * (cw + gap)
            gate = n == 4
            fill = C['human'] if gate else (C['cool'] if r == 0 else C['warm'])
            c.rect(x, y, cw, ch, fill=fill, outline=C['humanline'] if gate else C['line'],
                   width=3 if gate else 1.5, r=10)
            c.text(x + 26, y + 26, f'{n + 1:02d}', font(26, True), C['accent'])
            if gate:
                c.pill(x + cw - 100, y + 41, 'DECISION GATE', font(15, True), C['white'], C['ink'],
                       outline=C['humanline'])
            yy = c.wrap(x + 26, y + 78, title, font(29, True), cw - 52, lh=1.18)
            c.wrap(x + 26, yy + 10, desc, font(21), cw - 52)
            if i < 3:
                c.arrow(x + cw + 10, y + ch / 2, x + cw + gap - 10, y + ch / 2)
    # 4 -> 5 continuation (elbow, single arrowhead, numbered)
    ex = x0 + 3 * (cw + gap) + cw / 2
    sx = x0 + cw - 34
    yb, ymid, yt = 282 + ch + 8, 600, 690 - 8
    c.line(ex, yb, ex, ymid, C['accent'], 2.5)
    c.line(ex, ymid, sx, ymid, C['accent'], 2.5)
    c.arrow(sx, ymid, sx, yt)
    c.pill((ex + sx) / 2, ymid, '04 → 05  continues', font(18, True), C['white'], C['accent'],
           outline=C['accent'])
    # boundary note
    y = 690 + ch + 34
    c.rect(x0, y, W - 180, 62, fill=C['gray'], r=8)
    c.text(x0 + 24, y + 31, 'Boundary', font(20, True), C['ink'], anchor='lm')
    c.text(x0 + 140, y + 31, 'Cancel before writes → no directory, no copy, no record.   '
           'Missing evidence, changed sources or partial copies stop dependent work.', font(20), C['ink'], anchor='lm')
    c.footer()
    c.save('workflow_style_pilot_A.png')


def workflow_b():
    """Technical rail: numbered nodes on a line, native action labels in mono, phase bands."""
    c = Canvas()
    c.header('Planned intake flow', 'Read-only evidence first, one human gate, then approved and verified writes')
    x0, span = 90, W - 180
    col = span / 4
    bands = [(250, 'READ-ONLY', 'no writes', C['cool']), (660, 'APPROVED WRITES', 'each write needs approval', C['warm'])]
    for r, (y, tag, sub, fill) in enumerate(bands):
        c.rect(x0, y, span, 370, fill=fill, r=12)
        c.text(x0 + 24, y + 22, tag, font(17, True), C['accent'])
        c.text(x0 + 24 + c.width(tag, font(17, True)) + 12, y + 22, '· ' + sub, font(17), C['muted'])
        ry = y + 120
        c.line(x0 + col / 2, ry, x0 + span - col / 2, ry, C['accent'], 3)
        for i in range(4):
            n = r * 4 + i
            title, desc, act = STEPS[n]
            cx = x0 + col * i + col / 2
            if i < 3:
                c.arrow(cx + 60, ry, cx + col - 52, ry, width=3)
            if n == 4:
                d = 50
                c.d.polygon(c.p(cx, ry - d, cx + d, ry, cx, ry + d, cx - d, ry), fill=C['human'],
                            outline=C['humanline'], width=3 * S)
            else:
                c.d.ellipse(c.p(cx - 34, ry - 34, cx + 34, ry + 34), fill=C['white'],
                            outline=C['accent'], width=3 * S)
            c.text(cx, ry, f'{n + 1:02d}', font(24, True), C['ink'], anchor='mm')
            ty = ry + 70
            ty = c.wrap(cx - col / 2 + 22, ty, title, font(26, True), col - 44, lh=1.15)
            ty = c.wrap(cx - col / 2 + 22, ty + 6, desc, font(19), col - 44, C['ink'])
            fm = font(17, mono=True)
            c.rect(cx - col / 2 + 22, ty + 8, c.width(act, fm) + 20, 32, fill=C['white'],
                   outline=C['line'], r=5, width=1)
            c.text(cx - col / 2 + 32, ty + 24, act, fm, C['accent'], anchor='lm')
        # off-row connectors for 4 -> 5
        if r == 0:
            ex = x0 + span - col / 2
            c.arrow(ex + 36, ry, x0 + span - 22, ry, width=3)
            c.pill(x0 + span - 90, ry - 52, 'continues → 05', font(16, True), C['white'], C['accent'],
                   outline=C['accent'])
        else:
            c.pill(x0 + 80, ry - 52, 'from 04 →', font(16, True), C['white'], C['accent'], outline=C['accent'])
            c.arrow(x0 + 22, ry, x0 + col / 2 - 52, ry, width=3)
    c.text(x0, 1052, 'Cancel at 05 → no directory, no copy, no record.   Two copies are not a transaction: '
           'no automatic rollback.', font(19), C['ink'])
    c.footer()
    c.save('workflow_style_pilot_B.png')


def file_icon(c, x, y, w, h, kind, fill, outline):
    f = 22
    c.d.polygon(c.p(x, y, x + w - f, y, x + w, y + f, x + w, y + h, x, y + h), fill=fill,
                outline=outline, width=2 * S)
    c.d.polygon(c.p(x + w - f, y, x + w - f, y + f, x + w, y + f), fill=C['line'])
    if kind == 'image':
        c.d.polygon(c.p(x + 14, y + h - 16, x + w * 0.42, y + h * 0.42, x + w * 0.62, y + h * 0.66,
                        x + w * 0.74, y + h * 0.54, x + w - 14, y + h - 16), fill=C['accent'])
        c.d.ellipse(c.p(x + w * 0.62, y + h * 0.22, x + w * 0.62 + 14, y + h * 0.22 + 14), fill=C['accent'])
    else:
        for k in range(4):
            yy = y + 30 + k * 16
            c.line(x + 14, yy, x + w - (28 if k == 3 else 16), yy, C['accent'], 3)


def concept_a():
    """Two equal panels, equality / difference markers, human decision, planned outcome."""
    c = Canvas()
    c.header('Byte duplicate ≠ redundant creative bundle',
             'Same source bytes, different companion: the pair can still matter')
    pw, ph, py = 640, 440, 268
    lx, rx = 90, W - 90 - 640
    for x, tag, sub, comp in ((lx, 'ARCHIVE', 'already present', 'Companion A'),
                              (rx, 'STAGED', 'arriving for intake', 'Companion B')):
        c.rect(x, py, pw, ph, fill=C['cool'], outline=C['line'], r=12)
        c.text(x + 28, py + 26, tag, font(18, True), C['accent'])
        c.text(x + 28 + c.width(tag, font(18, True)) + 12, py + 26, '· ' + sub, font(18), C['muted'])
        for k, (kind, label, note) in enumerate((('image', 'Source image', 'original'),
                                                 ('sidecar', comp, 'editing sidecar / notes'))):
            yy = py + 100 + k * 165
            fill = C['white'] if k == 0 else (C['warm'] if comp.endswith('B') else C['white'])
            file_icon(c, x + 40, yy, 92, 116, kind, fill, C['accent'])
            c.text(x + 160, yy + 34, label, font(28, True))
            c.text(x + 160, yy + 74, note, font(20), C['muted'])
    mx = W / 2
    for k, (sym, label, fill, col) in enumerate((('=', 'source bytes equal', C['white'], C['accent']),
                                                ('≠', 'companion differs', C['human'], C['ink']))):
        yy = py + 158 + k * 165
        c.line(lx + pw + 8, yy, rx - 8, yy, C['line'], 2, dash=True)
        c.d.ellipse(c.p(mx - 30, yy - 30, mx + 30, yy + 30), fill=fill, outline=col, width=2 * S)
        c.text(mx, yy - 2, sym, font(34, True), col, anchor='mm')
        c.text(mx, yy + 52, label, font(18, True), col, anchor='mm')
    # decision
    dy = py + ph + 90
    c.arrow(lx + pw / 2, py + ph + 8, lx + pw / 2 + 140, dy - 6, C['line'], 2.5)
    c.arrow(rx + pw / 2, py + ph + 8, rx + pw / 2 - 140, dy - 6, C['line'], 2.5)
    dw, dh = 760, 160
    dx = mx - dw / 2
    c.rect(dx, dy, dw, dh, fill=C['human'], outline=C['humanline'], width=3, r=12)
    c.text(dx + 30, dy + 26, 'HUMAN DECISION', font(17, True), C['ink'])
    c.text(dx + 30, dy + 58, 'Preserve the approved pair — or defer', font(31, True))
    c.text(dx + 30, dy + 104, 'Byte equality does not decide creative intent.', font(20), C['ink'])
    ox = dx + dw + 60
    c.arrow(dx + dw + 6, dy + dh / 2, ox - 6, dy + dh / 2)
    c.rect(ox, dy + 20, W - 90 - ox, dh - 40, fill=C['white'], outline=C['accent'], r=10, dash=True)
    c.text(ox + 20, dy + 44, 'PLANNED', font(15, True), C['accent'])
    c.wrap(ox + 20, dy + 68, 'Fresh copy + native hash verification', font(19), W - 90 - ox - 40)
    c.text(90, dy + dh + 70, 'Matching names do not prove association · a sidecar does not guarantee '
           'working edits · a duplicate source never permits deletion', font(18), C['muted'])
    c.footer()
    c.save('concept_style_pilot_A.png')


def concept_b():
    """Evidence ledger: one table, two questions, two answers."""
    c = Canvas()
    c.header('Byte duplicate ≠ redundant creative bundle',
             'Two checks answer two different questions')
    x0, y0 = 90, 262
    cols = [('', 330), ('ARCHIVE', 330), ('STAGED', 330), ('EVIDENCE', 630)]
    rh, hh = 185, 54
    xs = [x0]
    for _, w in cols:
        xs.append(xs[-1] + w)
    c.rect(x0, y0, xs[-1] - x0, hh, fill=C['gray'], r=8)
    for i, (t, _) in enumerate(cols):
        c.text(xs[i] + 26, y0 + hh / 2, t, font(17, True), C['accent'], anchor='lm')
    rows = [('Source image', 'image', 'same', 'same', 'Bytes equal', 'native SHA-256 match', C['white']),
            ('Companion', 'sidecar', 'A', 'B', 'Content differs', 'readable notes / XMP compared', C['human'])]
    for r, (label, kind, a, b, ev, evsub, evfill) in enumerate(rows):
        y = y0 + hh + r * rh
        c.line(x0, y + rh, xs[-1], y + rh, C['line'], 1.5)
        c.text(xs[0] + 26, y + rh / 2, label, font(27, True), anchor='lm')
        for j, v in ((1, a), (2, b)):
            fill = C['warm'] if (kind == 'sidecar' and v == 'B') else C['white']
            file_icon(c, xs[j] + 30, y + 38, 84, 108, kind, fill, C['accent'])
            c.text(xs[j] + 140, y + rh / 2, 'Companion ' + v if kind == 'sidecar' else 'source',
                   font(22), C['ink'] if kind == 'sidecar' else C['muted'], anchor='lm')
        sym = '=' if r == 0 else '≠'
        c.d.ellipse(c.p(xs[3] + 26, y + rh / 2 - 26, xs[3] + 78, y + rh / 2 + 26), fill=evfill,
                    outline=C['accent'] if r == 0 else C['humanline'], width=2 * S)
        c.text(xs[3] + 52, y + rh / 2 - 2, sym, font(30, True), C['ink'], anchor='mm')
        c.text(xs[3] + 100, y + rh / 2 - 16, ev, font(25, True), anchor='lm')
        c.text(xs[3] + 100, y + rh / 2 + 20, evsub, font(19), C['muted'], anchor='lm')
    # two questions
    y = y0 + hh + 2 * rh + 60
    bw = (xs[-1] - x0 - 40) / 2
    c.rect(x0, y, bw, 240, fill=C['gray'], r=12)
    c.text(x0 + 30, y + 28, 'BYTE CHECK ASKS', font(17, True), C['muted'])
    c.text(x0 + 30, y + 62, 'Is this source already archived?', font(28, True), C['muted'])
    c.wrap(x0 + 30, y + 112, 'Answer: yes. Skipping on that basis alone can strand companion B '
           'without its source context.', font(21), bw - 60, C['muted'])
    bx = x0 + bw + 40
    c.rect(bx, y, bw, 240, fill=C['human'], outline=C['humanline'], width=3, r=12)
    c.text(bx + 30, y + 28, 'ARCHIVERESCUE ASKS', font(17, True), C['ink'])
    c.text(bx + 30, y + 62, 'Does companion B belong with this source?', font(28, True))
    c.wrap(bx + 30, y + 112, 'A person decides: preserve the approved pair or defer. '
           'Planned outcome: fresh copy + native hash verification.', font(21), bw - 60)
    c.footer()
    c.save('concept_style_pilot_B.png')


if __name__ == '__main__':
    workflow_a(); workflow_b(); concept_a(); concept_b()
    for p in sorted(OUT.glob('*.png')):
        print(p.relative_to(ROOT), p.stat().st_size)
