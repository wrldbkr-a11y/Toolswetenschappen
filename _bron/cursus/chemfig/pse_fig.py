# volledig PSE als SVG (liggend)
import sys
sys.path.insert(0, '/home/claude/cursus/chemfig')
from pse_data import ALLE
GROEP = {1: 'Ia', 2: 'IIa', 3: 'IIIb', 4: 'IVb', 5: 'Vb', 6: 'VIb', 7: 'VIIb', 8: 'VIIIb', 11: 'Ib', 12: 'IIb', 13: 'IIIa', 14: 'IVa', 15: 'Va', 16: 'VIa', 17: 'VIIa', 18: 'VIIIa'}
KLEUR = {'m': '#bfdbfe', 'nm': '#bbf7d0', 'eg': '#fde68a'}
INK, GRIJS, ROOD = '#1D2A36', '#64748b', '#dc2626'
FF = 'font-family="Inter,sans-serif"'
def tx(x, y, s, size=10, kleur=INK, anker='middle', w=700, extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{w}" fill="{kleur}" text-anchor="{anker}" {FF} {extra}>{s}</text>'

def pse_svg(soort='kat'):
    """soort: 'kat' (categorieën + trap), 'en' (zelfde, EN in rood + pijlen), 'leeg' (wit, enkel Z en symbool, om in te kleuren)"""
    cw, ch, x0, y0 = 62, 64, 46, 58
    fy0 = y0 + 7 * ch + 26
    W = x0 + 18 * cw + (70 if soort == 'en' else 14)
    H = fy0 + 2 * ch + (46 if soort == 'en' else 12)
    o = f'<rect width="{W}" height="{H}" fill="#fff"/>'
    # groepsnummers
    for g, n in GROEP.items():
        if g == 8:
            xm = x0 + 8.5 * cw
            o += tx(xm, y0 - 22, 'VIIIb', 14) + f'<path d="M{x0+7*cw+6},{y0-12} v-5 h{3*cw-12} v5" fill="none" stroke="{GRIJS}" stroke-width="1.4"/>'
        else:
            yy = y0 - 10 if g in (1, 18) else (y0 + ch - 10 if g in (2, 13, 14, 15, 16, 17) else y0 + 3 * ch - 10)
            o += tx(x0 + (g - .5) * cw, yy, n, 14)
    for p in range(1, 8):
        o += tx(x0 - 16, y0 + (p - .5) * ch + 5, str(p), 15, GRIJS)
    o += tx(x0 - 30, y0 - 22, 'groep', 11, GRIJS, 'start', 600) + tx(4, y0 + 7 * ch + 16, 'periode', 11, GRIJS, 'start', 600)
    o += tx(x0 + 2.5 * cw - 4, fy0 + ch / 2 + 4, 'lanthaniden', 11, GRIJS, 'end', 700) + tx(x0 + 2.5 * cw - 4, fy0 + 1.5 * ch + 4, 'actiniden', 11, GRIJS, 'end', 700)
    cel = {}
    for e in ALLE:
        pos = e['pos']
        if pos[0] == 'f': x, y = x0 + (3 + pos[2]) * cw, fy0 + pos[1] * ch
        else: x, y = x0 + (pos[1] - 1) * cw, y0 + (pos[0] - 1) * ch; cel[(pos[0], pos[1])] = e['cat']
        f = '#fff' if soort in ('leeg', 'symbolen') else KLEUR[e['cat']]
        o += f'<rect x="{x+1.5}" y="{y+1.5}" width="{cw-3}" height="{ch-3}" rx="4" fill="{f}" stroke="#64748b" stroke-width="1"/>'
        o += tx(x + 5, y + 13, str(e['Z']), 9.5, GRIJS, 'start', 700)
        if soort == 'leeg':
            o += tx(x + cw / 2, y + 42, e['s'], 20, INK, w=800); continue
        if soort == 'symbolen':
            o = o[:o.rfind(tx(x + 5, y + 13, str(e['Z']), 9.5, GRIJS, 'start', 700))]
            o += tx(x + cw / 2, y + 40, e['s'], 22, INK, w=800); continue
        if soort == 'zonder':
            if e['en']: o += tx(x + cw - 5, y + 13, f"{e['en']:.1f}".replace('.', ','), 9.5, GRIJS, 'end', 700)
            o += tx(x + cw / 2, y + 39, e['s'], 21, INK, w=800)
            ar = e['ar'] if e['ar'].startswith('(') else e['ar'].replace('.', ',')
            o += tx(x + cw / 2, y + 57, ar, 9, GRIJS, w=600); continue
        if e['en']: o += tx(x + cw - 5, y + 13, f"{e['en']:.1f}".replace('.', ','), 9.5, ROOD if soort == 'en' else GRIJS, 'end', 700)
        o += tx(x + cw / 2, y + 34, e['s'], 18, INK, w=800)
        lang = len(e['naam']) > 10
        o += tx(x + cw / 2, y + 47, e['naam'], 7.6, INK, w=600, extra=f'textLength="{cw-8}" lengthAdjust="spacingAndGlyphs"' if lang else '')
        ar = e['ar'] if e['ar'].startswith('(') else e['ar'].replace('.', ',')
        o += tx(x + cw / 2, y + 58, ar, 8.5, GRIJS, w=600)
    # verwijzing La/Ac naar de f-rijen
    for p, z in ((6, 'lanthaniden'), (7, 'actiniden')):
        x, y = x0 + 2 * cw, y0 + (p - 1) * ch
        o += f'<circle cx="{x+cw-7}" cy="{y+ch-8}" r="2.6" fill="{GRIJS}"/>'
    if soort != 'leeg':
        # trap: rand van elk niet-metaal in groep 13-17 dat grenst aan een metaal of een lege plaats links/onder
        seg = ''
        for (p, g), c in cel.items():
            if c != 'nm' or g < 13: continue
            x, y = x0 + (g - 1) * cw, y0 + (p - 1) * ch
            if cel.get((p, g - 1), 'm') == 'm': seg += f'M{x},{y} V{y+ch} '
            if cel.get((p + 1, g)) == 'm': seg += f'M{x},{y+ch} H{x+cw} '
        o += f'<path d="{seg}" stroke="{ROOD}" stroke-width="4.5" stroke-linecap="round" fill="none"/>'
        # legende + uitlegvakje in de lege ruimte boven de b-groepen
        lx, ly = x0 + 2 * cw + 14, y0 + 6
        if soort == 'symbolen':
            o += f'<line x1="{lx}" y1="{ly+10}" x2="{lx+22}" y2="{ly+10}" stroke="{ROOD}" stroke-width="4.5"/>' + tx(lx + 30, ly + 15, 'trap: metalen links, niet-metalen rechts', 13, INK, 'start')
            return f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg">{o}</svg>'
        for i, (k, n) in enumerate((('m', 'metalen'), ('nm', 'niet-metalen'), ('eg', 'edelgassen'))):
            o += f'<rect x="{lx}" y="{ly + i*24}" width="22" height="17" rx="3" fill="{KLEUR[k]}" stroke="#64748b"/>' + tx(lx + 30, ly + 13 + i * 24, n, 13, INK, 'start')
        o += f'<line x1="{lx}" y1="{ly+80}" x2="{lx+22}" y2="{ly+80}" stroke="{ROOD}" stroke-width="4.5"/>' + tx(lx + 30, ly + 85, 'trap', 13, INK, 'start')
        vx, vy = x0 + 7 * cw, y0 + 4
        o += f'<rect x="{vx}" y="{vy}" width="{cw*1.6}" height="{ch*1.6}" rx="5" fill="#f8fafc" stroke="#64748b"/>'
        o += tx(vx + 6, vy + 17, 'Z', 12, GRIJS, 'start') + tx(vx + cw * 1.6 - 6, vy + 17, 'EN', 12, ROOD if soort == 'en' else GRIJS, 'end')
        o += tx(vx + cw * .8, vy + 56, 'symbool', 14, INK) + (tx(vx + cw * .8, vy + 72, 'naam', 11, INK, w=600) if soort != 'zonder' else '') + tx(vx + cw * .8, vy + 92, 'Ar', 12, GRIJS)
        o += tx(vx + cw * 1.6 + 10, vy + 17, 'atoomnummer · elektronegativiteit', 11, GRIJS, 'start', 600)
        o += tx(vx + cw * 1.6 + 10, vy + 92, 'relatieve atoommassa', 11, GRIJS, 'start', 600)
        o += tx(vx + cw * 1.6 + 10, vy + 110, '(…) = radioactief: massagetal', 10, GRIJS, 'start', 600)
    if soort == 'en':
        ya = fy0 + 2 * ch + 26
        o += f'<line x1="{x0}" y1="{ya}" x2="{x0+17*cw}" y2="{ya}" stroke="{ROOD}" stroke-width="3"/><path d="M{x0+17*cw+12},{ya} l-14,-7 v14z" fill="{ROOD}"/>'
        o += tx(x0 + 8.5 * cw, ya + 18, 'de EN stijgt naar rechts in een periode', 13, ROOD)
        xa = x0 + 18 * cw + 30
        o += f'<line x1="{xa}" y1="{y0+7*ch}" x2="{xa}" y2="{y0+12}" stroke="{ROOD}" stroke-width="3"/><path d="M{xa},{y0} l-7,14 h14z" fill="{ROOD}"/>'
        o += tx(xa + 6, y0 + 3.5 * ch, 'de EN stijgt naar boven in een groep', 13, ROOD, extra=f'transform="rotate(90 {xa+6} {y0+3.5*ch})"')
    return f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg">{o}</svg>'

if __name__ == '__main__':
    open('/tmp/pse.html', 'w').write('<body style="margin:0">' + pse_svg('zonder') + pse_svg('symbolen') + '</body>')
