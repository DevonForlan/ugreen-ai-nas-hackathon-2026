"""ArchiveRescue Devpost HERO final (ARCHIVERESCUE-DEVPOST-MEDIA-PACKAGE).

Input: the User-supplied hero concept (devpost-media/source/hero_source_user_supplied.png,
1536x1024, generic unbranded NAS). Edits, all deterministic:
  1. Replace the invented app UI on the laptop (incl. green success checkmarks, which imply
     verified runtime success and a GUI ArchiveRescue does not have) with a neutral
     source + companion "creative bundle" illustration.
  2. Remove the two glowing arrows.
  3. Upscale to 1800x1200 (3:2) and add a concept-illustration label.
Concept illustration only; not a NAS runtime screenshot. Requires Pillow + Windows Arial.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / 'submission/round1/archiverescue/devpost-media'
SRC = MEDIA / 'source/hero_source_user_supplied.png'
OUT = MEDIA / 'final/ArchiveRescue_Hero_Final.png'
FONTS = Path('C:/Windows/Fonts')
INK, ACCENT, LINE, WARM = (36, 58, 63), (74, 117, 117), (171, 189, 187), (243, 237, 228)

# Laptop display quad in source pixels (TL, TR, BR, BL), measured from gridded crops.
QUAD = [(465, 384), (970, 383), (994, 678), (482, 691)]
ARROWS = [(300, 546, 462, 626), (1001, 542, 1150, 594)]  # boxes around the two arrows


def font(size, bold=False):
    return ImageFont.truetype(str(FONTS / ('arialbd.ttf' if bold else 'arial.ttf')), size)


def solve(a, b):
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def perspective_coeffs(dst, src):
    """Coefficients mapping output (dst) pixels back to input (src) pixels for Image.transform."""
    a, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        a.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        a.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    return solve(a, b)


def file_icon(d, x, y, w, h, kind, fill):
    f = int(w * 0.26)
    d.polygon([(x, y), (x + w - f, y), (x + w, y + f), (x + w, y + h), (x, y + h)], fill=fill,
              outline=ACCENT, width=6)
    d.polygon([(x + w - f, y), (x + w - f, y + f), (x + w, y + f)], fill=LINE)
    if kind == 'image':
        d.polygon([(x + 16, y + h - 18), (x + w * .42, y + h * .42), (x + w * .62, y + h * .66),
                   (x + w * .74, y + h * .54), (x + w - 16, y + h - 18)], fill=ACCENT)
        d.ellipse([x + w * .60, y + h * .2, x + w * .60 + 18, y + h * .2 + 18], fill=ACCENT)
    else:
        for k in range(4):
            yy = y + h * .3 + k * h * .14
            d.line([(x + 16, yy), (x + w - (40 if k == 3 else 18), yy)], fill=ACCENT, width=6)


def screen_art():
    w, h = 1010, 600
    im = Image.new('RGB', (w, h), (244, 246, 245))
    d = ImageDraw.Draw(im)
    bx, by, bw, bh = 255, 92, 500, 300  # bundle bracket
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=26, fill=(234, 241, 240), outline=ACCENT, width=5)
    file_icon(d, bx + 70, by + 58, 130, 168, 'image', (255, 255, 255))
    d.text((bx + bw / 2, by + 142), '+', font=font(64, True), fill=INK, anchor='mm')
    file_icon(d, bx + bw - 200, by + 58, 130, 168, 'sidecar', WARM)
    d.text((bx + 135, by + 262), 'source', font=font(30), fill=INK, anchor='mm')
    d.text((bx + bw - 135, by + 262), 'companion', font=font(30), fill=INK, anchor='mm')
    d.text((w / 2, by + bh + 64), 'one creative bundle', font=font(44, True), fill=INK, anchor='mm')
    return im


def replace_screen(base):
    art = screen_art()
    coeffs = perspective_coeffs(QUAD, [(0, 0), (art.width, 0), (art.width, art.height), (0, art.height)])
    warped = art.transform(base.size, Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    mask = Image.new('L', base.size, 0)
    ImageDraw.Draw(mask).polygon(QUAD, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.8))
    warped = warped.filter(ImageFilter.GaussianBlur(0.5))
    warped = Image.blend(warped, Image.new('RGB', base.size, (226, 222, 214)), 0.08)  # match ambient light
    base.paste(warped, (0, 0), mask)


def remove_arrows(base):
    px = base.load()
    for x0, y0, x1, y1 in ARROWS:
        for x in range(x0, x1):
            top, bot = px[x, y0], px[x, y1]
            for y in range(y0 + 1, y1):
                t = (y - y0) / (y1 - y0)
                bg = tuple(top[i] * (1 - t) + bot[i] * t for i in range(3))
                cur = px[x, y]
                dist = sum((cur[i] - bg[i]) ** 2 for i in range(3)) ** 0.5
                a = max(0.0, min(1.0, (dist - 1.5) / 6))  # colour distance catches the tinted glow
                if a:
                    px[x, y] = tuple(int(cur[i] * (1 - a) + bg[i] * a) for i in range(3))
        region = (x0, y0, x1, y1)
        base.paste(base.crop(region).filter(ImageFilter.GaussianBlur(1.2)), region[:2])


def label(img):
    d = ImageDraw.Draw(img, 'RGBA')
    f = font(21, True)
    s = 'CONCEPT ILLUSTRATION — NOT A NAS RUNTIME SCREENSHOT'
    w = d.textlength(s, font=f) + 36
    x1, y1 = img.width - 56, img.height - 48
    d.rounded_rectangle([x1 - w, y1 - 40, x1, y1], radius=20, fill=(255, 255, 255, 225),
                        outline=ACCENT + (255,), width=2)
    d.text((x1 - w / 2, y1 - 20), s, font=f, fill=ACCENT, anchor='mm')


def main():
    base = Image.open(SRC).convert('RGB')
    assert base.size == (1536, 1024), base.size
    remove_arrows(base)
    replace_screen(base)
    out = base.resize((1800, 1200), Image.LANCZOS)
    label(out)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT, optimize=True)
    print(OUT.relative_to(ROOT), OUT.stat().st_size)


if __name__ == '__main__':
    main()
