import math
ns = {}
src = open('/home/claude/cursus/bouw.py', encoding='utf-8').read()
exec(src.split('STAP = ')[0], ns)
def zet_hfst(n):
    ns['SJABLOON'] = open('/home/claude/cursus/sjabloon_ac.html', encoding='utf-8').read().replace('{{HFST}}', str(n))
ns['FOOTER'] = 'Cursus fysica 5de jaar — gemaakt voor klasgebruik, bij de tools op Oefentools wetenschappen.'
denk, oef, blok, tool, kader, figuur, bouw = (ns[k] for k in ['denk', 'oef', 'blok', 'tool', 'kader', 'figuur', 'bouw'])
F = 'font-family="Inter,sans-serif"'
POS, NEG, INK, DIM = '#d64550', '#2a6f97', '#1D2A36', '#51606E'
METAAL, RAND, ISO = '#e2e8f0', '#475569', '#fffdf5'

# ---------------- hulpstukken ----------------
def defi(kop, tekst, wet=False):
    return f'<div class="def{" wet" if wet else ""}"><div class="kop">{kop}</div>{tekst}</div>'
def vgl(f):
    return f'<div class="vgl"><span class="f">{f}</span></div>'
def vb(kop, tekst):
    return f'<div class="voorbeeld"><div class="kop">{kop}</div>{tekst}</div>'
def verd(kop, tekst):
    return f'<div class="verdieping"><div class="kop">Verdieping · {kop}</div>{tekst}</div>'
def svg(inner, w, h):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg" {F}><defs><marker id="pijl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs>{inner}</svg>'
def q(x, y, s, r=9):
    k = POS if s > 0 else NEG
    t = f'<path d="M{x-5},{y} H{x+5}" stroke="#fff" stroke-width="2.4"/>' + (f'<path d="M{x},{y-5} V{y+5}" stroke="#fff" stroke-width="2.4"/>' if s > 0 else '')
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{k}"/>{t}'
def tx(x, y, t, size=14, kleur=INK, anker='middle', w=600):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{kleur}" text-anchor="{anker}" font-weight="{w}">{t}</text>'
def pijl(x1, y1, x2, y2, k=INK, w=2.5, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{k}" stroke-width="{w}" marker-end="url(#pijl)"{d}/>'
def aarde(x, y):
    return ''.join(f'<line x1="{x-18+i*6}" y1="{y+i*6}" x2="{x+18-i*6}" y2="{y+i*6}" stroke="{INK}" stroke-width="2.5"/>' for i in range(3))
def bol(x, y, r, ladingen, fill=METAAL):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{RAND}" stroke-width="2"/>' + ''.join(q(x + dx, y + dy, s, 7) for dx, dy, s in ladingen)
def plus(x, y, size=17):
    return f'<text x="{x}" y="{y+6}" font-size="{size}" font-weight="700" fill="{POS}" text-anchor="middle">+</text>'
def kracht(x1, y, L, label='F'):
    return pijl(x1, y, x1 - L, y, '#1D4ED8', 4) + tx(x1 - L / 2, y - 10, label, 15, '#1D4ED8', 'middle', 700)
def staaf(x, y, w, h, kleur, lad=[], label=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{kleur}" stroke="{RAND}" stroke-width="2"/>' + ''.join(q(x + dx, y + h / 2, s, 7) for dx, s in lad) + (tx(x + w / 2, y - 8, label, 13, DIM) if label else '')
def ring(n, R, s, cx, cy, start=0):
    return [(cx + R * math.cos(start + 2 * math.pi * i / n), cy + R * math.sin(start + 2 * math.pi * i / n), s) for i in range(n)]

