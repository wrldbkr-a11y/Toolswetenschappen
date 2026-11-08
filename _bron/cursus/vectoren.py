"""Vectorteken (pijltje) boven elk krachtsymbool (F…) en veldsymbool (E…) bij een pijl in een figuur.
Een label krijgt een pijltje als het alleen uit het symbool bestaat (F, Fz, F₁₂, F<tspan>A</tspan> …) en er nog geen pijltje boven staat.
Niet in grafieken (daar staat een grootte, geen vector) en niet in de optica (F = brandpunt).
Wordt aangeroepen door bouw.py.
"""
import re, html as H

ZONDER = ('cursus-lenzen', 'cursus-weerkaatsing', 'cursus-lichtbreking', 'cursus-zien-door-licht', 'cursus-oog', 'cursus-chemie', 'cursus-homeostase',
          'cursus-receptoren', 'cursus-reageren', 'cursus-spieren', 'cursus-waterhuishouding')
SYMBOOL = re.compile(r'^([FE])([A-Za-z0-9₀-₉,∥⊥]{0,8})$')
TEXT = re.compile(r'<text\b([^>]*)>(.*?)</text>', re.S)

def _attr(a, naam, std=None):
    m = re.search(r'\b' + naam + r'="([^"]*)"', a)
    return m.group(1) if m else std

def _pijltje(cx, y, fs, kleur):
    yt = y - 0.92 * fs; h = 0.28 * fs
    return (f'<path d="M{cx - h:.1f},{yt:.1f} H{cx + h:.1f} M{cx + h - 3:.1f},{yt - 3:.1f} L{cx + h:.1f},{yt:.1f} L{cx + h - 3:.1f},{yt + 3:.1f}" '
            f'stroke="{kleur}" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')

def _heeft_pijltje(svg, cx, y, fs):
    for m in re.finditer(r'd="M\s*([\d.]+)[ ,]([\d.]+)\s*H', svg):
        x0, y0 = float(m.group(1)), float(m.group(2))
        if abs(y0 - (y - fs)) < 0.45 * fs + 3 and -fs - 6 < x0 - cx < fs * 0.5 + 4: return True
    return False

def _svg(svg):
    if '<polyline' in svg: return svg
    extra = []
    for m in TEXT.finditer(svg):
        a, inhoud = m.group(1), m.group(2)
        plat = H.unescape(re.sub(r'<[^>]+>', '', inhoud)).strip()
        if not SYMBOOL.match(plat): continue
        try:
            x, y = float(_attr(a, 'x')), float(_attr(a, 'y'))
        except (TypeError, ValueError):
            continue
        fs = float(_attr(a, 'font-size', '14') or 14)
        anker = _attr(a, 'text-anchor', 'start')
        kleur = _attr(a, 'fill', '#1D2A36')
        sub = len(plat) - 1
        w = 0.62 * fs + sub * 0.5 * fs * 0.72
        cx = {'start': x + 0.31 * fs, 'middle': x - w / 2 + 0.31 * fs, 'end': x - w + 0.31 * fs}.get(anker, x + 0.31 * fs)
        if _heeft_pijltje(svg, cx, y, fs): continue
        extra.append(_pijltje(cx, y, fs, kleur))
    # vectoren met een dunne lijn
    svg = re.sub(r'(<line\b[^>]*?stroke-width=")([\d.]+)("[^>]*marker-end)', lambda m: m.group(1) + (m.group(2) if float(m.group(2)) <= 2.5 else '2.2') + m.group(3), svg)
    if not extra: return svg
    return svg[:svg.rfind('</svg>')] + ''.join(extra) + '</svg>'

def vectortekens(html, bestand):
    if bestand.startswith(ZONDER): return html
    def fig(m):
        svg, cap = m.group(1), m.group(2) or ''
        if re.search(r'functie|grafiek|grootte van', cap): return m.group(0)
        return _svg(svg) + cap
    return re.sub(r'(<svg\b.*?</svg>)(\s*<figcaption>.*?</figcaption>)?', fig, html, flags=re.S)
