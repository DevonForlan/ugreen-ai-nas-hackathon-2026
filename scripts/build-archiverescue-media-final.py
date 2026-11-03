"""ArchiveRescue Devpost media FINAL renderer (ARCHIVERESCUE-DEVPOST-MEDIA-FINALIZATION).

Editable source for the two final gallery images selected by the User:
workflow  <- style-pilot workflow B,  concept <- style-pilot concept A.
Concept / planned-behavior diagrams only; nothing here is NAS runtime evidence.
Palette and font follow Proposal Visual V3. Requires Pillow + Windows Arial/Consolas.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'submission/round1/archiverescue/devpost-media/final'
FONTS = Path('C:/Windows/Fonts')
W, H, S, M = 1800, 1200, 2, 72  # 3:2, drawn at 2x, 72 px outer margin

C = {k: '#' + v for k, v in {
    'ink': '243A3F', 'accent': '4A7575', 'line': 'ABBDBB', 'cool': 'EAF1F0',
    'warm': 'F3EDE4', 'human': 'E6D8C0', 'gray': 'F1F3F3', 'white': 'FFFFFF',
    'muted': '5F7174', 'humanline': 'A8844C'}.items()}
STROKE = 2.5  # one stroke weight for nodes, icons and connectors


def font(size, bold=False, mono=False):
    name = ('consolab.ttf' if bold else 'consola.ttf') if mono else ('arialbd.ttf' if bold else 'arial.ttf')
    return ImageFont.truetype(str(FONTS / name), int(size * S))


class Canvas:
    def __init__(self):
        self.im = Image.new('RGB', (W * S, H * S), C['white'])
        self.d = ImageDraw.Draw(self.im)

    def p(self, *xy):
        return [v * S for v in xy]

    def rect(self, x, y, w, h, fill=None, outline=None, width=1.5, r=10):
        self.d.rounded_rectangle(self.p(x, y, x + w, y + h), radius=r * S, fill=fill,
                                 outline=outline, width=int(width * S) if outline else 0)

    def dashed_rect(self, x, y, w, h, color, width=2):
        for a, b in (((x, y), (x + w, y)), ((x, y + h), (x + w, y + h)),
                     ((x, y), (x, y + h)), ((x + w, y), (x + w, y + h))):
            self.line(*a, *b, color=color, width=width, dash=True)

    def line(self, x1, y1, x2, y2, color=None, width=STROKE, dash=False):
        color = color or C['accent']
        if not dash:
            self.d.line(self.p(x1, y1, x2, y2), fill=color, width=int(width * S))
            return
        L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        seg, n = 12, max(1, round(L / 12))
        if n % 2 == 0:
            n += 1  # odd count -> dash at both ends, clean corners
        for i in range(0, n, 2):
            a, b = i / n, (i + 1) / n
            self.d.line(self.p(x1 + (x2 - x1) * a, y1 + (y2 - y1) * a,
                               x1 + (x2 - x1) * b, y1 + (y2 - y1) * b), fill=color, width=int(width * S))

    def arrow(self, x1, y1, x2, y2, color=None, width=STROKE, head=14):
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

    def width(self, s, f):
        return f.getlength(s) / S

    def wrap(self, x, y, s, f, maxw, color=None, lh=1.3):
        words, line, yy = s.split(), '', y
        step = f.size / S * lh
        for w_ in words:
            t = (line + ' ' + w_).strip()
            if self.width(t, f) <= maxw:
                line = t
            else:
                self.text(x, yy, line, f, color); yy += step; line = w_
        if line:
            self.text(x, yy, line, f, color); yy += step
        return yy

    def pill(self, cx, cy, s, f, fill, color, outline=None, pad=16):
        w = self.width(s, f) + pad * 2
        h = f.size / S + 16
        self.rect(cx - w / 2, cy - h / 2, w, h, fill=fill, outline=outline, r=h / 2, width=2)
        self.text(cx, cy, s, f, color, anchor='mm')
        return w

    def header(self, title, subtitle, status):
        self.text(M, 56, 'ARCHIVERESCUE · COMPANION-AWARE NAS INTAKE', font(19, True), C['accent'])
        fs = font(18, True)
        sw = self.width(status, fs) + 32
        self.pill(W - M - sw / 2, 66, status, fs, C['white'], C['accent'], outline=C['accent'])
        self.text(M, 88, title, font(54, True))
        self.text(M, 158, subtitle, font(27), C['muted'])
        self.line(M, 206, W - M, 206, C['line'], 1.5)

    def footer(self, note):
        self.line(M, 1104, W - M, 1104, C['line'], 1.5)
        self.text(M, 1124, note, font(19), C['muted'])
        self.text(W - M, 1124, 'ArchiveRescue · Round 1', font(19, True), C['muted'], anchor='ra')

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        self.im.resize((W, H), Image.LANCZOS).save(OUT / name, optimize=True)


# (title, description, chip, chip_is_native_action)
STEPS = [
    ('Select', 'Authorize staging and archive paths; at most 20 files.', 'user input', False),
    ('Inspect', 'Inventory, metadata and native SHA-256 values.', 'ls · stat · sha256sum', True),
    ('Compare', 'Equal bytes vs. same name with different bytes.', 'uses step 02 evidence', False),
    ('Review companion evidence', 'Readable notes / XMP only; unread stays opaque.', 'cat', True),
    ('Human approval', 'Exact paths, source hashes, complete units, fresh destination.', 'human decision', False),
    ('Fresh copy', 'Non-overwriting copy into a reserved, empty destination.', 'mkdir · cpmv overwrite=false', True),
    ('Verify hashes', 'Destination = reviewed source = post-copy source.', 'sha256sum', True),
    ('Save + read back', 'Separately approved intake record, compared on readback.', 'save-text · cat', True),
]


def workflow():
    c = Canvas()
    c.header('Planned intake flow',
             'Read-only evidence first, one human gate, then approved and verified writes',
             'PLANNED WORKFLOW — NAS RUNTIME NOT TESTED')
    span = W - 2 * M
    col = span / 4
    bands = [(228, 'READ-ONLY EVIDENCE', 'no writes', C['cool']),
             (618, 'APPROVED WRITES', 'each write needs approval; hashes verified', C['warm'])]
    ftag, fsub = font(19, True), font(19)
    for r, (y, tag, sub, fill) in enumerate(bands):
        c.rect(M, y, span, 372, fill=fill, r=12)
        c.text(M + 24, y + 20, tag, ftag, C['accent'])
        c.text(M + 24 + c.width(tag, ftag) + 10, y + 20, '· ' + sub, fsub, C['muted'])
        ry = y + 118
        chips = []
        for i in range(4):
            n = r * 4 + i
            title, desc, chip, native = STEPS[n]
            cx = M + col * i + col / 2
            tx, tw = cx - col / 2 + 24, col - 48
            if i < 3:
                c.arrow(cx + 50, ry, cx + col - 50, ry)
            if n == 4:
                d = 46
                c.d.polygon(c.p(cx, ry - d, cx + d, ry, cx, ry + d, cx - d, ry), fill=C['human'],
                            outline=C['humanline'], width=int(3 * S))
            else:
                c.d.ellipse(c.p(cx - 36, ry - 36, cx + 36, ry + 36), fill=C['white'],
                            outline=C['accent'], width=int(STROKE * S))
            c.text(cx, ry, f'{n + 1:02d}', font(25, True), C['ink'], anchor='mm')
            ty = c.wrap(tx, ry + 62, title, font(31, True), tw, lh=1.12)
            ty = c.wrap(tx, ty + 6, desc, font(22), tw)
            chips.append((tx, ty, chip, native))
        cy = max(t for _, t, _, _ in chips) + 28  # one chip baseline per row
        for tx, _, chip, native in chips:
            if native:
                fm = font(20, mono=True)
                c.rect(tx, cy - 18, c.width(chip, fm) + 22, 36, fill=C['white'], outline=C['line'], r=5, width=1.5)
                c.text(tx + 11, cy, chip, fm, C['accent'], anchor='lm')
            else:
                c.text(tx, cy, chip, font(20), C['muted'], anchor='lm')
        if r == 0:  # off-row connector, row 1 exit
            ex = M + span - col / 2
            c.arrow(ex + 44, ry, M + span - 20, ry)
            c.pill(M + span - 98, ry - 54, 'continues → 05', font(18, True), C['white'], C['accent'],
                   outline=C['accent'])
        else:       # off-row connector, row 2 entry
            c.pill(M + 86, ry - 54, 'from 04 →', font(18, True), C['white'], C['accent'], outline=C['accent'])
            c.arrow(M + 20, ry, M + col / 2 - 52, ry)
    y = 1008
    c.rect(M, y, span, 60, fill=C['gray'], r=8)
    c.text(M + 24, y + 30, 'Boundary', font(22, True), C['ink'], anchor='lm')
    c.text(M + 140, y + 30, 'Cancel at 05 → no directory, no copy, no record.  ·  Incomplete verification stays '
           'unverified.  ·  No automatic rollback.', font(22), C['ink'], anchor='lm')
    c.footer('Technical diagram of planned behavior — not a NAS runtime screenshot.  '
             'Monospace = registered native action.')
    c.save('ArchiveRescue_Workflow_Final.png')


def file_icon(c, x, y, w, h, kind, fill):
    f = 24
    c.d.polygon(c.p(x, y, x + w - f, y, x + w, y + f, x + w, y + h, x, y + h), fill=fill,
                outline=C['accent'], width=int(STROKE * S))
    c.d.polygon(c.p(x + w - f, y, x + w - f, y + f, x + w, y + f), fill=C['line'])
    if kind == 'image':
        c.d.polygon(c.p(x + 15, y + h - 17, x + w * 0.42, y + h * 0.42, x + w * 0.62, y + h * 0.66,
                        x + w * 0.74, y + h * 0.54, x + w - 15, y + h - 17), fill=C['accent'])
        c.d.ellipse(c.p(x + w * 0.60, y + h * 0.22, x + w * 0.60 + 15, y + h * 0.22 + 15), fill=C['accent'])
    else:
        for k in range(4):
            yy = y + 34 + k * 18
            c.line(x + 15, yy, x + w - (32 if k == 3 else 17), yy, C['accent'], 3)


def concept():
    c = Canvas()
    c.header('Byte duplicate ≠ redundant creative bundle',
             'Same source bytes do not make the companion context safe to discard or overwrite.',
             'CONCEPT — PLANNED BEHAVIOR')
    pw, ph, py = 660, 480, 236
    lx, rx = M, W - M - pw
    ftag = font(20, True)
    for x, tag, sub, comp in ((lx, 'ARCHIVE', 'already present', 'Companion A'),
                              (rx, 'STAGED', 'arriving for intake', 'Companion B')):
        c.rect(x, py, pw, ph, fill=C['cool'], outline=C['line'], r=12, width=1.5)
        c.text(x + 30, py + 26, tag, ftag, C['accent'])
        c.text(x + 30 + c.width(tag, ftag) + 10, py + 26, '· ' + sub, font(20), C['muted'])
        for k, (kind, label, note) in enumerate((('image', 'Source image', 'original'),
                                                 ('sidecar', comp, 'editing sidecar / notes'))):
            yy = py + 100 + k * 190
            fill = C['warm'] if comp.endswith('B') and k == 1 else C['white']
            file_icon(c, x + 44, yy, 98, 126, kind, fill)
            c.text(x + 176, yy + 36, label, font(32, True))
            c.text(x + 176, yy + 80, note, font(23), C['muted'])
    mx = W / 2
    for k, (sym, label, fill, col) in enumerate((('=', 'source bytes equal', C['white'], C['accent']),
                                                ('≠', 'companion differs', C['human'], C['humanline']))):
        yy = py + 163 + k * 190
        c.line(lx + pw + 10, yy, rx - 10, yy, C['line'], 2, dash=True)
        c.d.ellipse(c.p(mx - 34, yy - 34, mx + 34, yy + 34), fill=fill, outline=col, width=int(STROKE * S))
        c.text(mx, yy - 2, sym, font(38, True), C['ink'], anchor='mm')
        c.text(mx, yy + 58, label, font(21, True), C['ink'], anchor='mm')
    # human decision, fed by both panels with vertical arrows
    dw, dh = 800, 210
    dx, dy = mx - dw / 2, py + ph + 70
    c.arrow(dx + 120, py + ph + 6, dx + 120, dy - 6, C['line'])
    c.arrow(dx + dw - 120, py + ph + 6, dx + dw - 120, dy - 6, C['line'])
    c.rect(dx, dy, dw, dh, fill=C['human'], outline=C['humanline'], width=3, r=12)
    c.text(dx + 34, dy + 34, 'HUMAN DECISION', font(19, True), C['ink'])
    c.text(dx + 34, dy + 74, 'Preserve the approved pair — or defer', font(34, True))
    c.text(dx + 34, dy + 136, 'Byte equality does not decide creative intent.', font(23), C['ink'])
    # planned outcome (right) and boundaries (left), equal side boxes
    sw = dx - M - 56
    ox = dx + dw + 56
    c.arrow(dx + dw + 8, dy + dh / 2, ox - 8, dy + dh / 2)
    c.dashed_rect(ox, dy + 10, sw, dh - 20, C['accent'])
    c.text(ox + 24, dy + 38, 'PLANNED OUTCOME', font(18, True), C['accent'])
    c.wrap(ox + 24, dy + 76, 'Fresh non-overwriting copy + native hash verification', font(22), sw - 48)
    c.rect(M, dy + 10, sw, dh - 20, fill=C['gray'], r=10)
    c.text(M + 24, dy + 38, 'NEVER IMPLIED', font(18, True), C['muted'])
    for k, s in enumerate(('Matching names prove association', 'A sidecar guarantees working edits',
                           'A duplicate source permits deletion')):
        c.text(M + 24, dy + 80 + k * 34, '× ' + s, font(20), C['ink'])
    c.footer('Concept diagram of planned behavior — not a NAS runtime screenshot. NAS runtime not tested.')
    c.save('ArchiveRescue_Concept_Final.png')


if __name__ == '__main__':
    workflow(); concept()
    for p in sorted(OUT.glob('*.png')):
        print(p.relative_to(ROOT), p.stat().st_size)
