"""Render a pptx's vector shapes to SVG so geometry can actually be checked.
Handles the primitives the graphics deck uses: line (with flips), rect,
roundRect, ellipse, triangle (with rotation), and text runs."""
import re, sys, html, zipfile, os

E = 914400.0
SW, SH = 10.0, 5.625
SCALE = 128  # px per inch


def esc(t):
    return html.escape(t)


def parse_shape(b):
    d = {}
    xf = re.search(r'<a:xfrm([^>]*)>\s*<a:off x="(-?\d+)"\s*y="(-?\d+)"\s*/>\s*'
                   r'<a:ext cx="(\d+)"\s*cy="(\d+)"', b)
    if not xf:
        return None
    attrs = xf.group(1)
    d['x'] = int(xf.group(2)) / E
    d['y'] = int(xf.group(3)) / E
    d['w'] = int(xf.group(4)) / E
    d['h'] = int(xf.group(5)) / E
    rot = re.search(r'rot="(-?\d+)"', attrs)
    d['rot'] = int(rot.group(1)) / 60000 if rot else 0
    d['flipV'] = 'flipV="1"' in attrs
    d['flipH'] = 'flipH="1"' in attrs
    g = re.search(r'<a:prstGeom prst="(\w+)"', b)
    d['geom'] = g.group(1) if g else 'rect'
    sp = re.search(r'<p:spPr>(.*?)</p:spPr>', b, re.S)
    d['fill'] = None
    d['line'] = None
    if sp:
        body = sp.group(1)
        head = body.split('<a:ln')[0]
        f = re.search(r'<a:solidFill><a:srgbClr val="([0-9A-Fa-f]{6})"(?:>\s*<a:alpha val="(\d+)")?',
                      head)
        if f:
            alpha = int(f.group(2)) / 100000 if f.group(2) else 1.0
            d['fill'] = ('#' + f.group(1), alpha)
        lm = re.search(r'<a:ln[^>]*w="(\d+)"[^>]*>(.*?)</a:ln>', body, re.S)
        if lm:
            lc = re.search(r'srgbClr val="([0-9A-Fa-f]{6})"', lm.group(2))
            if lc:
                d['line'] = ('#' + lc.group(1), int(lm.group(1)) / 12700)
    runs = []
    for r in re.finditer(r'<a:r>(.*?)</a:r>', b, re.S):
        rb = r.group(1)
        t = html.unescape(''.join(re.findall(r'<a:t>(.*?)</a:t>', rb, re.S)))
        if not t.strip():
            continue
        sz = re.search(r'sz="(\d+)"', rb)
        col = re.search(r'<a:solidFill><a:srgbClr val="([0-9A-Fa-f]{6})"', rb)
        runs.append((t, int(sz.group(1)) / 100 if sz else 18,
                     '#' + col.group(1) if col else '#0A0A0A'))
    d['runs'] = runs
    al = re.search(r'algn="(\w+)"', b)
    d['align'] = al.group(1) if al else 'l'
    return d


def shape_svg(d):
    x, y, w, h = (d[k] * SCALE for k in ('x', 'y', 'w', 'h'))
    fill = 'none'
    op = 1.0
    if d['fill']:
        fill, op = d['fill']
    stroke = ''
    if d['line']:
        c, wd = d['line']
        stroke = f' stroke="{c}" stroke-width="{max(wd,0.6)*SCALE/72}"'
    g = d['geom']
    out = []
    if g == 'line':
        if d['flipV']:
            x1, y1, x2, y2 = x, y + h, x + w, y
        else:
            x1, y1, x2, y2 = x, y, x + w, y + h
        c, wd = d['line'] if d['line'] else ('#000', 1)
        out.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                   f'stroke="{c}" stroke-width="{max(wd,0.6)*SCALE/72:.2f}" stroke-linecap="round"/>')
    elif g == 'ellipse':
        out.append(f'<ellipse cx="{x+w/2:.2f}" cy="{y+h/2:.2f}" rx="{w/2:.2f}" ry="{h/2:.2f}" '
                   f'fill="{fill}" fill-opacity="{op:.2f}"{stroke}/>')
    elif g == 'trapezoid':
        ins = w * 0.22
        pts = f'{x+ins:.2f},{y:.2f} {x+w-ins:.2f},{y:.2f} {x+w:.2f},{y+h:.2f} {x:.2f},{y+h:.2f}'
        tr = (f' transform="rotate({d["rot"]:.1f} {x+w/2:.2f} {y+h/2:.2f})"'
              if d['rot'] else '')
        out.append(f'<polygon points="{pts}" fill="{fill}" fill-opacity="{op:.2f}"{stroke}{tr}/>')
    elif g == 'triangle':
        pts = f'{x+w/2:.2f},{y:.2f} {x+w:.2f},{y+h:.2f} {x:.2f},{y+h:.2f}'
        tr = (f' transform="rotate({d["rot"]:.1f} {x+w/2:.2f} {y+h/2:.2f})"'
              if d['rot'] else '')
        out.append(f'<polygon points="{pts}" fill="{fill}" fill-opacity="{op:.2f}"{stroke}{tr}/>')
    else:
        rx = ' rx="7"' if g == 'roundRect' else ''
        out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"{rx} '
                   f'fill="{fill}" fill-opacity="{op:.2f}"{stroke}/>')
    if d['runs']:
        anchor = {'ctr': 'middle', 'r': 'end'}.get(d['align'], 'start')
        tx = x + (w / 2 if anchor == 'middle' else (w if anchor == 'end' else 0))
        sz = d['runs'][0][1] * SCALE / 72
        ty = y + h / 2 + sz * 0.34
        spans = ''.join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, _, c in d['runs'])
        out.append(f'<text x="{tx:.2f}" y="{ty:.2f}" text-anchor="{anchor}" '
                   f'font-family="Poppins" font-weight="700" font-size="{sz:.1f}">{spans}</text>')
    return '\n'.join(out)


def render(pptx, out_html, want=None):
    z = zipfile.ZipFile(pptx)
    names = sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)],
                   key=lambda p: int(re.search(r'(\d+)', p.split('/')[-1]).group()))
    parts = ['<meta charset="utf-8">'
             '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap" rel="stylesheet">'
             '<style>body{margin:0;background:#777;font-family:Poppins}'
             '.s{margin:0 0 6px 0;display:block;position:relative}'
             '.n{position:absolute;left:2px;top:2px;font:11px monospace;background:#000;color:#0f0;'
             'padding:1px 4px;z-index:9}</style>']
    for i, nm in enumerate(names, 1):
        if want and i not in want:
            continue
        x = z.read(nm).decode()
        bgm = re.search(r'<p:bg>.*?srgbClr val="([0-9A-Fa-f]{6})"', x, re.S)
        bg = '#' + bgm.group(1) if bgm else '#FFFFFF'
        body = []
        tree = x.split('</p:nvGrpSpPr>', 1)[-1]
        for m in re.finditer(r'<p:(sp|pic|cxnSp)>(.*?)</p:\1>', tree, re.S):
            d = parse_shape(m.group(2))
            if d:
                body.append(shape_svg(d))
        parts.append(f'<div class="s"><div class="n">graphic {i}</div>'
                     f'<svg width="{SW*SCALE}" height="{SH*SCALE}" '
                     f'style="background:{bg}">' + '\n'.join(body) + '</svg></div>')
    open(out_html, 'w').write('\n'.join(parts))
    print('wrote', out_html, len(names), 'slides')


if __name__ == '__main__':
    want = set(int(a) for a in sys.argv[3:]) or None
    render(sys.argv[1], sys.argv[2], want)
