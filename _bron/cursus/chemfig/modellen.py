# deeltjesmodellen bij adsorberen en extraheren
import math, random
INK, GRIJS = '#1D2A36', '#64748b'
FF = 'font-family="Inter,sans-serif"'
def tx(x, y, s, size=13, kleur=INK, anker='middle', w=700):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{w}" fill="{kleur}" text-anchor="{anker}" {FF}>{s}</text>'
WATER, KLEUR, GEUR = '#7dd3fc', '#a21caf', '#16a34a'
def water(x, y): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{WATER}" stroke="#0284c7" stroke-width=".8"/>'
def kleurmol(x, y, a=0):  # grotere molecule: drie bolletjes
    return f'<g transform="translate({x:.1f},{y:.1f}) rotate({a:.0f})"><circle cx="-7" cy="0" r="5" fill="{KLEUR}"/><circle cx="0" cy="0" r="5.5" fill="{KLEUR}"/><circle cx="7" cy="0" r="5" fill="{KLEUR}"/></g>'
def geurmol(x, y, a=0):
    return f'<g transform="translate({x:.1f},{y:.1f}) rotate({a:.0f})"><circle cx="-5" cy="0" r="5" fill="{GEUR}"/><circle cx="5" cy="0" r="5" fill="{GEUR}"/></g>'
def vrije_punten(r, n, x0, y0, x1, y1, weg=lambda x, y: False, afst=13):
    pts = []; tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        if weg(x, y): continue
        if all((x - a) ** 2 + (y - b) ** 2 > afst ** 2 for a, b in pts): pts.append((x, y))
    return pts
def kool(cx, cy, R, r):
    # onregelmatige, poreuze korrel actieve kool
    pts = []
    for i in range(28):
        a = i / 28 * 2 * math.pi
        rr = R * (0.82 + 0.18 * r.random())
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    o = '<path d="M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + f'Z" fill="#374151" stroke="#111827" stroke-width="1.5"/>'
    for i in range(9):  # poriën
        a, d = r.uniform(0, 2 * math.pi), r.uniform(0, R * .6)
        o += f'<ellipse cx="{cx + d*math.cos(a):.1f}" cy="{cy + d*math.sin(a):.1f}" rx="{r.uniform(3,6):.1f}" ry="{r.uniform(2,4):.1f}" fill="#6b7280"/>'
    return o, pts
def bol(cx, cy, R):
    return f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>'
def fig_adsorberen():
    r = random.Random(4)
    o = '<rect width="640" height="290" fill="#fff"/>'
    # paneel 1: mengsel + losse bolletjes adsorptiemiddel
    o += '<rect x="20" y="30" width="200" height="200" rx="12" fill="#f0f9ff" stroke="#94a3b8" stroke-width="2"/>'
    for x, y in vrije_punten(r, 34, 30, 40, 210, 220): o += water(x, y)
    for x, y in vrije_punten(r, 6, 40, 50, 200, 210, afst=30): o += kleurmol(x, y, r.uniform(0, 180))
    for x, y in vrije_punten(r, 6, 40, 50, 200, 210, afst=28): o += geurmol(x, y, r.uniform(0, 180))
    o += tx(120, 20, 'mengsel', 14)
    for cx, cy in ((258, 110), (292, 104), (262, 146), (296, 140)): o += bol(cx, cy, 15)
    o += tx(277, 186, 'actieve kool', 13) + tx(277, 202, '(adsorptiemiddel)', 11, GRIJS, w=600)
    o += f'<line x1="322" y1="125" x2="358" y2="125" stroke="{INK}" stroke-width="2.5"/><path d="M366,125 l-12,-6 v12z" fill="{INK}"/>'
    # paneel 2: bolletjes in het mengsel; kleur- en geurstoffen verdeeld over hun oppervlak
    o += '<rect x="380" y="30" width="240" height="200" rx="12" fill="#f0f9ff" stroke="#94a3b8" stroke-width="2"/>'
    bollen = [(445, 85, 24), (550, 80, 24), (445, 180, 24), (550, 178, 24)]
    weg = lambda x, y: any((x - a) ** 2 + (y - b) ** 2 < (R + 20) ** 2 for a, b, R in bollen)
    for x, y in vrije_punten(r, 30, 390, 40, 610, 220, weg=weg, afst=14): o += water(x, y)
    k = 0
    for bi, (cx, cy, R) in enumerate(bollen):
        o += bol(cx, cy, R)
        for m in range(3):
            a = math.radians(bi * 40 + m * 120 + 15)
            x, y = cx + (R + 6) * math.cos(a), cy + (R + 6) * math.sin(a)
            o += (kleurmol if k % 2 == 0 else geurmol)(x, y, math.degrees(a) + 90); k += 1
    o += tx(500, 20, 'na het adsorberen', 14)
    ly = 262
    o += water(40, ly) + tx(50, ly + 4, 'watermolecule', 12, INK, 'start', 600)
    o += kleurmol(180, ly) + tx(196, ly + 4, 'kleurstof', 12, INK, 'start', 600)
    o += geurmol(290, ly) + tx(303, ly + 4, 'geurstof', 12, INK, 'start', 600)
    o += tx(410, ly - 4, 'kleur- en geurstoffen kleven aan', 12, INK, 'start', 600) + tx(410, ly + 12, 'het oppervlak van de kool; water niet', 12, INK, 'start', 600)
    return f'<svg viewBox="0 0 640 290" width="640" xmlns="http://www.w3.org/2000/svg">{o}</svg>'

ROOD_, ORANJE, GROEN_ = '#dc2626', '#f59e0b', '#16a34a'
def boon(cx, cy, rx, ry, a=-25):
    return (f'<g transform="rotate({a} {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#e7c9a0" stroke="#7c4a1e" stroke-width="3"/>'
            f'<path d="M{cx-rx*0.85},{cy} C{cx-rx*0.4},{cy-ry*0.35} {cx+rx*0.4},{cy+ry*0.35} {cx+rx*0.85},{cy}" fill="none" stroke="#7c4a1e" stroke-width="3"/></g>')
def stofje(x, y, k): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{k}" stroke="#fff" stroke-width="1"/>'
def in_ellips(x, y, cx, cy, rx, ry, a):
    c, s = math.cos(math.radians(-a)), math.sin(math.radians(-a))
    dx, dy = x - cx, y - cy
    u, v = dx * c - dy * s, dx * s + dy * c
    return (u / rx) ** 2 + (v / ry) ** 2 < 1
def fig_extraheren():
    r = random.Random(3)
    o = '<rect width="640" height="300" fill="#fff"/>'
    # tekening 1: boon met drie soorten stoffen
    cx, cy, rx, ry, a = 130, 120, 95, 66, -25
    o += boon(cx, cy, rx, ry, a)
    pts = vrije_punten(r, 27, cx - rx, cy - ry - 30, cx + rx, cy + ry + 30, weg=lambda x, y: not in_ellips(x, y, cx, cy, rx - 12, ry - 12, a), afst=15)
    for i, (x, y) in enumerate(pts): o += stofje(x, y, (ROOD_, ORANJE, GROEN_)[i % 3])
    o += tx(130, 22, 'koffieboon', 14)
    o += f'<line x1="250" y1="120" x2="300" y2="120" stroke="{INK}" stroke-width="2.5"/><path d="M308,120 l-12,-6 v12z" fill="{INK}"/>' + tx(279, 108, 'malen +', 11, GRIJS, w=600) + tx(279, 142, 'heet water', 11, GRIJS, w=600)
    # tekening 2: bekerglas met water; stofjes opgelost, gemalen koffie onderaan (residu)
    bx0, bx1, by0, by1 = 330, 610, 40, 230
    o += f'<path d="M{bx0},{by0} V{by1} H{bx1} V{by0}" fill="none" stroke="{INK}" stroke-width="3"/>'
    o += f'<rect x="{bx0+2}" y="{by0+28}" width="{bx1-bx0-4}" height="{by1-by0-30}" fill="#fde7c8" opacity=".55"/>'
    # residu: korrels gemalen koffie
    for x, y in vrije_punten(r, 30, bx0 + 10, by1 - 26, bx1 - 10, by1 - 6, afst=9):
        o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.uniform(4,6):.1f}" fill="#e7c9a0" stroke="#7c4a1e" stroke-width="1.5"/>'
    for i, (x, y) in enumerate(vrije_punten(r, 24, bx0 + 14, by0 + 40, bx1 - 14, by1 - 38, afst=20)): o += stofje(x, y, (ROOD_, ORANJE, GROEN_)[i % 3])
    o += tx(470, 22, 'koffie zetten', 14)
    o += tx(bx1 + 6, by0 + 70, 'extract', 12, INK, 'start') + tx(bx1 + 6, by1 - 12, 'residu', 12, INK, 'start')
    # legende
    ly = 270
    for i, (k, n) in enumerate(((ROOD_, 'kleurstoffen'), (ORANJE, 'smaakstoffen'), (GROEN_, 'geurstoffen'))):
        o += stofje(40 + i * 120, ly, k) + tx(52 + i * 120, ly + 4, n, 12, INK, 'start', 600)
    o += tx(410, ly + 4, 'Ze lossen op in het hete water.', 12, INK, 'start', 600)
    return f'<svg viewBox="0 0 670 290" width="640" xmlns="http://www.w3.org/2000/svg">{o}</svg>'
if __name__ == '__main__':
    open('/tmp/mod.html', 'w').write('<body style="margin:0">' + fig_adsorberen() + '<br>' + fig_extraheren() + '</body>')
