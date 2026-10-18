"""Cover and hero art for each app, built from its icon (python3 tools/make_covers.py).
Covers are 600x800 portrait (game-cover style); heroes are 1600x900 for the front-page carousel."""
import json, os
from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
BRAIN = os.path.abspath(os.path.join(ROOT, '..'))
APPS = json.load(open(os.path.join(HERE, 'apps.json')))
BG = (11, 13, 18)


def rounded(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    out = im.convert('RGBA'); out.putalpha(m); return out


def shadowed(base, icon, cx, cy, blur=36, off=26, alpha=150):
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0)); a = icon.getchannel('A').point(lambda v: alpha if v > 8 else 0)
    sh.paste((0, 0, 0, 255), (cx - icon.width // 2, cy - icon.height // 2 + off), a)
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    base.alpha_composite(icon, (cx - icon.width // 2, cy - icon.height // 2))


def backdrop(icon, w, h, dark):
    s = max(w, h) * 1.15
    bg = icon.resize((round(s), round(s)), Image.LANCZOS).crop((round((s - w) / 2), round((s - h) / 2), round((s + w) / 2), round((s + h) / 2)))
    bg = bg.filter(ImageFilter.GaussianBlur(46)).convert('RGBA')
    bg.alpha_composite(Image.new('RGBA', (w, h), (BG[0], BG[1], BG[2], round(255 * dark))))
    return bg


def fade(img, y0, y1):
    """Vertical fade into the page colour between y0 and y1."""
    g = Image.new('L', img.size, 0); px = g.load()
    for y in range(img.height):
        v = 0 if y < y0 else 255 if y > y1 else round(255 * (y - y0) / (y1 - y0))
        for x in range(img.width): px[x, y] = v
    img.alpha_composite(Image.merge('RGBA', (Image.new('L', img.size, BG[0]), Image.new('L', img.size, BG[1]), Image.new('L', img.size, BG[2]), g)))


for a in APPS:
    src = Image.open(os.path.join(BRAIN, a['icon'])).convert('RGB')
    src.resize((512, 512), Image.LANCZOS).save(os.path.join(ROOT, 'img/icons', a['slug'] + '.png'))
    # cover
    cv = backdrop(src, 600, 800, 0.55)
    shadowed(cv, rounded(src.resize((440, 440), Image.LANCZOS), 98), 300, 330)
    fade(cv, 560, 800)
    cv.convert('RGB').save(os.path.join(ROOT, 'img/covers', a['slug'] + '.jpg'), quality=88)
    # hero
    hr = backdrop(src, 1600, 900, 0.5)
    shadowed(hr, rounded(src.resize((520, 520), Image.LANCZOS), 118), 1230, 450, blur=50, off=34)
    # darken the left side for text
    ov = Image.new('RGBA', (1600, 900)); d = ImageDraw.Draw(ov)
    for x in range(1000):
        d.line((x, 0, x, 900), fill=(BG[0], BG[1], BG[2], round(235 * (1 - x / 1000))))
    hr.alpha_composite(ov); fade(hr, 700, 900)
    hr.convert('RGB').save(os.path.join(ROOT, 'img/hero', a['slug'] + '.jpg'), quality=84)
    print('built', a['slug'])
