import math
ns = {}
src = open('/home/claude/cursus/bouw.py', encoding='utf-8').read()
exec(src.split('STAP = ')[0], ns)
ns['SJABLOON'] = open('/home/claude/cursus/sjabloon_ac.html', encoding='utf-8').read().replace('{{HFST}}', '1')
ns['FOOTER'] = 'Cursus fysica 5de jaar — gemaakt voor klasgebruik, bij de tools op Oefentools wetenschappen.'
denk, oef, blok, tool, kader, figuur, bouw = (ns[k] for k in ['denk', 'oef', 'blok', 'tool', 'kader', 'figuur', 'bouw'])
TOOL = 'ladingen.html'
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

# ---------------- figuren ----------------
def fig_atoom():
    s = f'<circle cx="160" cy="130" r="95" fill="none" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="5 4"/>'
    s += f'<circle cx="160" cy="130" r="26" fill="#F1F5F9" stroke="#64748B"/>'
    for i, (dx, dy) in enumerate([(-9, -8), (9, -8), (0, 8), (-10, 10), (10, 9), (0, -15)]):
        s += q(160 + dx, 130 + dy, 1, 7) if i % 2 == 0 else f'<circle cx="{160+dx}" cy="{130+dy}" r="7" fill="#9CA3AF"/>'
    for x, y, _ in ring(3, 95, -1, 160, 130, -0.6):
        s += q(x, y, -1, 9)
    s += f'<line x1="186" y1="124" x2="330" y2="70" stroke="{DIM}"/>' + tx(336, 74, 'kern: protonen (+) en neutronen', 14, INK, 'start')
    s += f'<line x1="{160+95*math.cos(-0.6)}" y1="{130+95*math.sin(-0.6)}" x2="330" y2="150" stroke="{DIM}"/>' + tx(336, 154, 'elektronen (−) rond de kern', 14, INK, 'start')
    s += tx(336, 196, 'neutraal atoom: evenveel p⁺ als e⁻', 14, DIM, 'start', 400)
    return svg(s, 640, 260)

def fig_voorwerpen():
    s = ''
    # 6 paren (+ met − ernaast), plus extra of ontbrekende elektronen verspreid
    cel = [(40, 65), (100, 65), (160, 65), (40, 120), (100, 120), (160, 120)]
    for i, (titel, ontbreekt, extra, sub) in enumerate([('neutraal', [], [], '6 + en 6 −'), ('positief geladen', [0, 2, 4], [], '6 + en 3 −: elektronentekort'),
                                                        ('negatief geladen', [], [(70, 92), (130, 92), (190, 92)], '6 + en 9 −: elektronenoverschot')]):
        x0 = 10 + i * 215
        s += f'<rect x="{x0}" y="40" width="200" height="120" rx="8" fill="#F8FAFC" stroke="#64748B" stroke-width="2"/>'
        for k, (cx, cy) in enumerate(cel):
            s += q(x0 + cx - 10, cy, 1, 9)
            if k not in ontbreekt: s += q(x0 + cx + 11, cy, -1, 9)
        for (ex, ey) in extra: s += q(x0 + ex, ey, -1, 9)
        s += tx(x0 + 100, 28, titel, 15) + tx(x0 + 100, 182, sub, 13, DIM, 'middle', 400)
    return svg(s, 660, 200)

TRIBO = ['glas', 'menselijk haar', 'nylon', 'wol', 'zijde', 'papier', 'katoen', 'hout', 'barnsteen', 'rubber (ballon)', 'polyester', 'PVC (plastic)']
def fig_tribo():
    s = tx(120, 22, 'geeft gemakkelijk elektronen af (+)', 13, POS)
    for i, m in enumerate(TRIBO):
        y = 34 + i * 25; hl = m in ('wol', 'PVC (plastic)')
        s += f'<rect x="40" y="{y}" width="160" height="21" rx="4" fill="{"#EAEFF5" if hl else "#F8FAFC"}" stroke="{"#1F3A5F" if hl else "#D9D6CC"}" stroke-width="{2 if hl else 1}"/>' + tx(52, y + 15, m, 13, INK, 'start', 700 if hl else 400)
    s += tx(120, 34 + 12 * 25 + 16, 'neemt gemakkelijk elektronen op (−)', 13, NEG)
    s += f'<path d="M205,{34+3*25+10} C300,{34+3*25+10} 300,{34+11*25+10} 205,{34+11*25+10}" fill="none" stroke="{NEG}" stroke-width="2.5" marker-end="url(#pijl)"/>'
    s += tx(300, 200, 'elektronen gaan', 13, NEG, 'start', 600) + tx(300, 218, 'van wol naar PVC', 13, NEG, 'start', 600)
    s += tx(440, 120, 'wol wordt', 14, INK, 'start', 400) + tx(518, 120, 'positief', 14, POS, 'start') + tx(440, 300, 'PVC wordt', 14, INK, 'start', 400) + tx(518, 300, 'negatief', 14, NEG, 'start')
    return svg(s, 640, 370)

def fig_geleider():
    s = tx(170, 24, 'geleider (metaal)', 15) + staaf(30, 50, 280, 40, '#e5e7eb', [(28 + i * 32, -1) for i in range(8)])
    s += tx(170, 118, 'de lading verspreidt zich over het hele voorwerp', 13, DIM, 'middle', 400)
    s += tx(480, 24, 'isolator (kunststof)', 15) + staaf(340, 50, 280, 40, ISO, [(20 + i * 14, -1) for i in range(5)])
    s += tx(480, 118, 'de lading blijft waar ze is', 13, DIM, 'middle', 400)
    return svg(s, 650, 135)

def fig_aarding():
    s = ''
    for i, (titel, ne, pijlop, tekst) in enumerate([('negatief voorwerp', 9, False, '3 e⁻ naar de aarde'), ('positief voorwerp', 3, True, '3 e⁻ van de aarde')]):
        cx = 160 + i * 320
        s += tx(cx, 22, titel, 15) + f'<circle cx="{cx}" cy="85" r="48" fill="{METAAL}" stroke="{RAND}" stroke-width="2"/>'
        for k in range(6):
            a_ = k * math.pi / 3 + 0.5; s += plus(cx + 22 * math.cos(a_), 85 + 22 * math.sin(a_), 15)
        for k in range(ne):
            a_ = k * 2 * math.pi / ne; s += q(cx + 38 * math.cos(a_), 85 + 38 * math.sin(a_), -1, 6)
        s += tx(cx, 152, f'6 + en {ne} −', 13, DIM, 'middle', 400)
        s += f'<line x1="{cx}" y1="133" x2="{cx}" y2="140" stroke="{INK}" stroke-width="2.5"/><line x1="{cx-60}" y1="160" x2="{cx-60}" y2="214" stroke="{INK}" stroke-width="2.5"/>' if False else ''
        s += f'<line x1="{cx+48}" y1="85" x2="{cx+70}" y2="85" stroke="{INK}" stroke-width="2.5"/><line x1="{cx+70}" y1="85" x2="{cx+70}" y2="210" stroke="{INK}" stroke-width="2.5"/>' + aarde(cx + 70, 212)
        s += (pijl(cx + 92, 200, cx + 92, 150, NEG) if pijlop else pijl(cx + 92, 150, cx + 92, 200, NEG)) + tx(cx + 100, 180, tekst, 13, NEG, 'start')
        s += tx(cx, 250, 'daarna: 6 + en 6 − → neutraal', 13, INK, 'middle', 600)
    return svg(s, 720, 265)

def fig_contact():
    a = [(dx, dy, -1) for dx, dy, _ in ring(6, 22, -1, 0, 0)]
    s = tx(140, 22, 'vóór het contact', 14) + bol(90, 80, 38, a) + bol(190, 80, 38, [])
    s += tx(90, 138, 'A: 6 e⁻ te veel', 13, DIM, 'middle', 400) + tx(190, 138, 'B: neutraal', 13, DIM, 'middle', 400)
    s += pijl(260, 80, 330, 80, DIM)
    b = [(dx, dy, -1) for dx, dy, _ in ring(3, 20, -1, 0, 0, 0.5)]
    s += tx(470, 22, 'na het contact', 14) + bol(430, 80, 38, b) + bol(506, 80, 38, b)
    s += tx(470, 138, 'elk 3 e⁻ te veel', 13, DIM, 'middle', 400)
    return svg(s, 640, 155)

def fig_polarisatie():
    s = staaf(10, 112, 250, 36, '#e5e7eb', [(28 + i * 38, -1) for i in range(6)]) + tx(135, 100, 'negatief geladen staaf', 13)
    ox, cy = 470, 130
    s += f'<rect x="{ox-110}" y="{cy-80}" width="220" height="160" rx="6" fill="{ISO}" stroke="#94a3b8" stroke-width="1.5"/>'
    for r in range(3):
        for c in range(4):
            mx, my = ox - 75 + c * 50, cy - 48 + r * 48
            s += f'<ellipse cx="{mx}" cy="{my}" rx="19" ry="12" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.2"/>'
            s += tx(mx - 8, my + 5, '+', 14, POS, 'middle', 700) + tx(mx + 8, my + 5, '−', 14, NEG, 'middle', 700)
    s += tx(ox, cy + 104, 'papiersnipper (vergroot: moleculen)', 13)
    s += kracht(ox - 122, cy + 62, 70)
    return svg(s, 640, 250)

def fig_influentie_bol():
    s = staaf(10, 112, 250, 36, '#e5e7eb', [(28 + i * 38, -1) for i in range(6)]) + tx(135, 100, 'negatief geladen staaf', 13)
    ox, cy, R = 470, 130, 85
    s += f'<circle cx="{ox}" cy="{cy}" r="{R}" fill="{METAAL}" stroke="{RAND}" stroke-width="2"/>'
    for i in range(8):
        a_ = i * math.pi / 4 + math.pi / 8
        s += plus(ox + 0.55 * R * math.cos(a_), cy + 0.55 * R * math.sin(a_))
        t = -1.1 + (i / 7) * 2.2
        s += q(ox + 0.74 * R * math.cos(t), cy + 0.74 * R * math.sin(t), -1, 8)
    s += tx(ox, cy + R + 26, 'metalen bol op isolerende voet', 13) + kracht(ox - 98, cy + 60, 70)
    return svg(s, 640, 250)

def fig_influentie():
    s = ''
    R = 50
    GRID = [(-20, -17), (12, -17), (-20, 17), (12, 17)]
    def bol_(cx, cy, zonder, losse_min, oranje=False):
        o = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{METAAL}" stroke="{RAND}" stroke-width="2"/>'
        for k, (dx, dy) in enumerate(GRID):
            o += q(cx + dx - 7, cy + dy, 1, 7)
            if k not in zonder: o += q(cx + dx + 7, cy + dy, -1, 7)
        for k in range(losse_min):
            ly, lx = cy + (-17 if k == 0 else 17), cx + 37
            o += q(lx, ly, -1, 7) + (f'<circle cx="{lx}" cy="{ly}" r="10.5" fill="none" stroke="#F59E0B" stroke-width="2"/>' if oranje else '')
        return o
    panelen = [('0. Neutraal', False, None, [], 0, '4 + en 4 −', 'neutraal'),
               ('1. Staaf erbij', True, None, [0, 2], 2, '4 + en 4 −', 'neutraal'),
               ('2. Aarden', True, 'aan', [0, 2], 0, '4 + en 2 −', 'netto +2'),
               ('3. Draad weg', True, 'los', [0, 2], 0, '4 + en 2 −', 'netto +2'),
               ('4. Staaf weg', False, None, [1, 2], 0, '4 + en 2 −', 'netto +2')]
    for i, (t, st, gr, zonder, lm, tel, net) in enumerate(panelen):
        x0 = 4 + i * 134
        s += f'<rect x="{x0}" y="8" width="128" height="236" rx="6" fill="#FCFCFA" stroke="#D9D6CC"/>' + tx(x0 + 64, 28, t, 12) + tx(x0 + 64, 46, tel, 11, DIM, 'middle', 400)
        cx, cy = x0 + 70, 115
        if st: s += staaf(x0 + 3, 101, 14, 28, '#e5e7eb', [(7, -1)])
        s += bol_(cx, cy, zonder, lm, oranje=(i == 1))
        if gr:
            s += f'<line x1="{cx+R}" y1="{cy}" x2="{cx+54}" y2="{cy}" stroke="{INK}" stroke-width="2.5"/>'
            if gr == 'aan':
                s += f'<line x1="{cx+54}" y1="{cy}" x2="{cx+54}" y2="196" stroke="{INK}" stroke-width="2.5"/>' + aarde(cx + 54, 198) + tx(cx + 24, 188, '2 e⁻ ↓', 11, NEG, 'middle', 700)
            else:
                s += f'<line x1="{cx+54}" y1="{cy}" x2="{cx+54}" y2="152" stroke="{INK}" stroke-width="2.5"/><line x1="{cx+54}" y1="170" x2="{cx+54}" y2="196" stroke="{INK}" stroke-width="2.5"/>' + aarde(cx + 54, 198)
        s += tx(x0 + 64, 234, net, 12, POS if net != 'neutraal' else DIM, 'middle', 700 if net != 'neutraal' else 400)
    return svg(s, 676, 250)

def fig_bliksem():
    s = f'<path d="M120,70 C120,30 190,20 220,45 C250,15 330,20 340,55 C390,50 420,90 390,115 C400,140 340,150 320,135 C290,155 220,150 200,135 C150,150 100,130 120,100 C90,95 95,72 120,70Z" fill="#CBD5E1" stroke="#64748B" stroke-width="2"/>'
    for i in range(6): s += q(175 + i * 35, 55, 1, 8)
    for i in range(7): s += q(155 + i * 35, 120, -1, 8)
    s += f'<rect x="0" y="240" width="640" height="40" fill="#D9CBAA"/>' + ''.join(q(150 + i * 40, 252, 1, 8) for i in range(7))
    s += f'<path d="M300,140 L285,180 L305,182 L282,238" fill="none" stroke="#F59E0B" stroke-width="5" stroke-linejoin="round"/>'
    s += tx(440, 50, 'bovenkant wolk: +', 13, POS, 'start') + tx(440, 120, 'onderkant wolk: −', 13, NEG, 'start')
    s += tx(440, 200, 'aardoppervlak: +', 13, POS, 'start') + tx(440, 218, '(door influentie)', 13, POS, 'start')
    return svg(s, 640, 285)

# ---------------- inhoud ----------------
lesdoelen = '''<p>De lesdoelen volgen het leerstofoverzicht. Na dit hoofdstuk kan je:</p>
<ul class="doelen">
<li>verklaren waarom een voorwerp positief of negatief geladen is;</li>
<li>het principe van de tribo-elektrische reeks uitleggen aan de hand van een voorbeeld;</li>
<li>de grootte van de elementaire lading noteren en zeggen waar ze voorkomt in het atoom;</li>
<li>het verschil uitleggen tussen geleiders en isolatoren;</li>
<li>uitleggen wat aarding is en dit toepassen op positief en negatief geladen voorwerpen;</li>
<li>uitleggen wat er gebeurt bij een bliksemontlading;</li>
<li>uitleggen hoe je neutrale voorwerpen kunt laden door wrijving, contact en influentie;</li>
<li>het begrip polarisatie uitleggen met een tekening;</li>
<li>de bewegingen van ladingen bij laden door wrijving, contact en influentie illustreren met een tekening;</li>
<li>het principe van een fotokopieertoestel uitleggen met de correcte terminologie;</li>
<li>met de correcte terminologie uitleggen hoe swifferstofdoekjes werken.</li></ul>
<p>Leerboek p. 13–26. Oefeningen in het leerboek: 1, 6, 7, 8, 9, 10 (p. 25–26).</p>'''

voorkennis = '''<p>Voor dit hoofdstuk heb je deze leerstof uit vorige jaren nodig.</p>
<ul class="doelen">
<li>Een atoom bestaat uit een <b>kern</b> met <b>protonen</b> en <b>neutronen</b>, en <b>elektronen</b> rond de kern.</li>
<li>Gelijke ladingen <b>stoten elkaar af</b>, tegengestelde ladingen <b>trekken elkaar aan</b>.</li>
<li>Machten van tien: 10⁻⁹ = 0,000 000 001 en het voorvoegsel <b>nano</b> (n) betekent 10⁻⁹.</li></ul>'''

d11 = f'''<h3>1.1.1 De elementaire lading</h3>
<p>Alle materie bestaat uit atomen. Een atoom heeft een positief geladen kern met protonen en neutronen. Rond de kern bewegen negatief geladen elektronen (figuur 1.1).</p>
{figuur(fig_atoom(), 'Vereenvoudigd model van een atoom. De protonen zitten vast in de kern; alleen de elektronen kunnen van het ene voorwerp naar het andere gaan.')}
<p>Een proton en een elektron hebben een even grote lading, met een tegengesteld teken. Die kleinste lading noemen we de <b>elementaire lading</b> <i>e</i>.</p>
{defi('Elementaire lading', '<p>De <b>elementaire lading</b> <i>e</i> is de lading van één proton. Een elektron heeft lading −<i>e</i>.</p>')}
{vgl('<i>e</i> = 1,602 · 10⁻¹⁹ C')}
<p>Lading meet je in <b>coulomb</b> (C). Eén coulomb is dus een enorme hoeveelheid lading: daarvoor heb je ongeveer 6,2 · 10¹⁸ elektronen nodig.</p>
<h3>Positief en negatief geladen voorwerpen</h3>
<p>Een voorwerp is <b>neutraal</b> als het evenveel protonen als elektronen bevat. Het wordt geladen door elektronen te <b>krijgen</b> of te <b>verliezen</b> (figuur 1.2).</p>
{figuur(fig_voorwerpen(), 'Een voorwerp met een elektronentekort is positief geladen, een voorwerp met een elektronenoverschot is negatief geladen.')}
{defi('Geladen voorwerp', '<p>Een voorwerp is <b>positief geladen</b> als het een <b>tekort</b> aan elektronen heeft. Het is <b>negatief geladen</b> als het een <b>overschot</b> aan elektronen heeft.</p>')}
<p>Omdat alleen hele elektronen kunnen overgaan, is de lading van een voorwerp altijd een geheel veelvoud van <i>e</i>:</p>
{vgl('<i>Q</i> = ± <i>n</i> · <i>e</i>')}
<table class="vb"><tr><td><i>Q</i></td><td>lading van het voorwerp, in C</td></tr><tr><td><i>n</i></td><td>aantal elektronen te veel (−) of te weinig (+)</td></tr><tr><td><i>e</i></td><td>elementaire lading, 1,602 · 10⁻¹⁹ C</td></tr></table>
{vb('Elektronen tellen', '<p>Een ballon heeft na het wrijven een lading van −4,8 nC. Hoeveel elektronen heeft hij te veel?</p><p>Gegeven: <i>Q</i> = −4,8 · 10⁻⁹ C. Gevraagd: <i>n</i>.<br>Oplossing: <i>n</i> = |<i>Q</i>| / <i>e</i> = 4,8 · 10⁻⁹ C / 1,602 · 10⁻¹⁹ C = 3,0 · 10¹⁰.<br>Antwoord: de ballon heeft 3,0 · 10¹⁰ elektronen te veel.</p>')}
<h3>1.1.2 De tribo-elektrische reeks</h3>
<p>Wrijf je twee verschillende stoffen over elkaar, dan gaan er elektronen over van de ene stof naar de andere. De <b>tribo-elektrische reeks</b> rangschikt stoffen volgens hoe gemakkelijk ze elektronen afgeven (figuur 1.3).</p>
{figuur(fig_tribo(), 'Tribo-elektrische reeks. Bij wrijven wordt de stof die hoger staat positief, de stof die lager staat negatief.')}
{defi('Tribo-elektrische reeks', '<p>Bij het wrijven van twee stoffen <b>verliest</b> de stof die <b>hoger</b> in de reeks staat elektronen en wordt <b>positief</b>. De stof die <b>lager</b> staat, <b>krijgt</b> elektronen en wordt <b>negatief</b>.</p>')}
<p>Er ontstaat geen nieuwe lading: elektronen verhuizen alleen. Beide voorwerpen krijgen daarom een even grote lading met een tegengesteld teken. Hoe verder de stoffen in de reeks uit elkaar staan, hoe meer lading er overgaat.</p>
{tool(TOOL + '#l1', 'Tool: elementaire lading')} {tool(TOOL + '#l4', 'Tool: tribo-elektrische reeks')}
{denk('denk_1', 'Je wrijft een glazen staaf met een zijden doek. Daarna wrijf je een ballon over je haar. Welke voorwerpen worden positief, welke negatief? Trekken de glazen staaf en de ballon elkaar aan of stoten ze af?', [
  ('Glas en zijde', 'Glas staat hoger dan zijde: glas verliest elektronen en wordt positief, zijde wordt negatief.'),
  ('Ballon en haar', 'Haar staat hoger dan rubber: haar wordt positief, de ballon wordt negatief.'),
  ('Glas en ballon', 'Een positieve en een negatieve lading trekken elkaar aan.')],
  'Glas en haar worden positief, zijde en ballon negatief. De glazen staaf en de ballon trekken elkaar aan.')}

<h3>1.1.3 Geleiders en isolatoren</h3>
<p>In een <b>metaal</b> zitten sommige elektronen niet vast aan één atoom. Die <b>vrije elektronen</b> kunnen door het hele metaal bewegen. In kunststof, glas of droog hout zitten alle elektronen vast bij hun atoom (figuur 1.4).</p>
{figuur(fig_geleider(), 'In een geleider verspreidt de lading zich, in een isolator blijft ze op de plaats waar ze terechtkwam.')}
{defi('Geleider en isolator', '<p>Een <b>geleider</b> is een stof met vrije ladingdragers: lading kan zich erin verplaatsen. Een <b>isolator</b> heeft geen vrije ladingdragers: lading blijft op haar plaats.</p>')}
<p>Voorbeelden van geleiders: metalen, grafiet, het menselijk lichaam, de aarde, zout water. Voorbeelden van isolatoren: kunststof, glas, rubber, droge lucht, porselein.</p>
<p>In Brussel zie je het verschil bij de <b>bollen van het Atomium</b>: hun buitenhuid is van roestvrij staal, een metaal en dus een geleider. De glazen ramen erin zijn isolatoren.</p>
{tool(TOOL + '#l2', 'Tool: geleiders en isolatoren')}

<h3>1.1.4 Aarding</h3>
<p>De aarde is een zeer grote geleider. Ze kan zonder merkbare verandering elektronen opnemen of afgeven. Verbind je een geladen geleider met de aarde, dan stromen er elektronen tot het voorwerp neutraal is (figuur 1.5).</p>
{figuur(fig_aarding(), 'Aarding van een negatief en een positief geladen voorwerp. Er stromen precies zoveel elektronen tot er evenveel + als − zijn. Het symbool met de drie lijnen stelt de aarde voor.')}
{defi('Aarding', '<p><b>Aarden</b> is een geladen voorwerp geleidend verbinden met de aarde, zodat het neutraal wordt. Bij een <b>negatief</b> voorwerp stromen elektronen <b>naar</b> de aarde, bij een <b>positief</b> voorwerp stromen elektronen <b>van</b> de aarde naar het voorwerp.</p>')}
<p>Let op: bij een positief voorwerp stromen er dus geen protonen weg. Protonen zitten vast in de kern.</p>
{kader('Tekentip: tel de ladingen', '<p>Teken de vaste + ladingen en de elektronen apart. Een neutraal voorwerp heeft evenveel + als −. Bij aarden (zonder geladen voorwerp in de buurt) stromen er precies zoveel elektronen weg of bij <b>tot er weer evenveel + als − zijn</b>. Tel na: het aantal + verandert nooit.</p>')}
{tool(TOOL + '#l3', 'Tool: aarding')}'''

d12 = f'''<h3>1.2.1 Laden door wrijving en door contact</h3>
<p>Bij <b>laden door wrijving</b> gaan elektronen over van de ene stof naar de andere, zoals de tribo-elektrische reeks voorspelt (§ 1.1.2).</p>
<p>Bij <b>laden door contact</b> raak je een neutrale geleider aan met een geladen voorwerp. Een deel van de lading gaat over, tot de lading over beide voorwerpen verdeeld is (figuur 1.6). Zijn de voorwerpen twee <b>identieke</b> metalen bollen, dan krijgen ze elk de helft van de totale lading.</p>
{figuur(fig_contact(), 'Laden door contact. De elektronen verdelen zich over beide geleiders. Na het contact hebben ze lading met hetzelfde teken.')}
{defi('Behoud van lading', '<p>Lading kan niet ontstaan of verdwijnen. Bij laden verplaatst er alleen lading: de totale lading van alle voorwerpen samen blijft gelijk.</p>', True)}
{vb('Twee identieke bollen', '<p>Bol A heeft een lading van +6,0 nC, bol B van −2,0 nC. De bollen zijn identiek en raken elkaar even. Welke lading heeft elke bol daarna?</p><p>Totale lading: +6,0 nC + (−2,0 nC) = +4,0 nC. Die verdeelt zich gelijk over beide bollen: elk +2,0 nC.</p>')}
<h3>Ontladen en de bliksem</h3>
<p>Een geladen voorwerp kan zijn lading verliezen door aarding, maar ook door een <b>vonk</b>: als het ladingsverschil groot genoeg is, wordt de lucht even geleidend. De <b>bliksem</b> is een reusachtige vonk (figuur 1.7).</p>
{figuur(fig_bliksem(), 'Ladingsverdeling bij een onweerswolk. De negatieve onderkant van de wolk maakt het aardoppervlak eronder positief door influentie.')}
<ol>
<li>In een onweerswolk botsen ijskristallen en hagelkorrels. Daarbij gaan elektronen over. De <b>onderkant</b> van de wolk wordt <b>negatief</b>, de bovenkant positief.</li>
<li>De negatieve onderkant stoot elektronen in de grond eronder af. Het aardoppervlak onder de wolk wordt <b>positief</b>: dat is <b>influentie</b> (§ 1.2.2).</li>
<li>Wordt het ladingsverschil groot genoeg, dan wordt de lucht geleidend. Elektronen springen van de wolk naar de aarde: de <b>bliksem</b>. De lucht wordt zo heet dat ze ontploffend uitzet: de <b>donder</b>.</li>
<li>Een <b>bliksemafleider</b> is een metalen spits die met een dikke geleider met de aarde verbonden is. De lading wordt veilig naar de aarde afgevoerd.</li></ol>
{kader('Brussel · het KMI in Ukkel', '<p>Het Koninklijk Meteorologisch Instituut (KMI) in Ukkel volgt de bliksem boven België met het meetnet <b>BELLS</b>. Een bliksemontlading zendt elektromagnetische golven uit, zoals een radiozender. Sensoren verspreid over het land vangen die op. Zo ziet het KMI meer dan 95 % van de ontladingen, tot op 100 à 200 m nauwkeurig.</p>')}
{tool(TOOL + '#l6', 'Tool: bliksem')}

<h3>1.2.2 Influentie en polarisatie</h3>
<p>Je kan een neutraal voorwerp ook beïnvloeden <b>zonder</b> het aan te raken. Wat er gebeurt, hangt af van het soort stof.</p>
{defi('Influentie', '<p><b>Influentie</b> is het verschuiven van de vrije elektronen in een <b>geleider</b> onder invloed van een geladen voorwerp in de buurt. Aan de kant van het geladen voorwerp ontstaat een tegengestelde lading, aan de andere kant een gelijke lading.</p>')}
{defi('Polarisatie', '<p><b>Polarisatie</b> is het verschuiven van de elektronen <b>binnen elk atoom of molecule</b> van een <b>isolator</b> onder invloed van een geladen voorwerp. Elk molecule wordt een kleine dipool, met een positieve en een negatieve kant.</p>')}
{figuur(fig_influentie_bol(), 'Influentie in een metalen bol. De + ladingen (vaste ionen) bewegen niet; de vrije elektronen worden naar de verre kant geduwd. De bol wordt aangetrokken (kracht F).')}
{figuur(fig_polarisatie(), 'Polarisatie in een papiersnipper (isolator), sterk vergroot. Er zijn geen vrije elektronen: elk molecule wordt een kleine dipool. Ook hier is er een netto aantrekking (kracht F).')}
<p>In beide gevallen wordt het neutrale voorwerp <b>aangetrokken</b>. De lading die tegengesteld is aan die van de staaf, ligt namelijk het dichtst bij de staaf. De aantrekking is daardoor groter dan de afstoting. Zo trekt een geladen ballon papiersnippers aan.</p>
<h3>Laden door influentie</h3>
<p>Met influentie kan je een geleider ook blijvend laden, zonder hem aan te raken (figuur 1.10).</p>
{figuur(fig_influentie(), 'Laden door influentie. Elke + heeft zijn eigen −. De staaf duwt 2 elektronen naar de verre kant (omcirkeld): links blijven 2 + zonder partner over. Via de aarding kunnen juist die 2 elektronen nog verder weg. Na stap 4 verdeelt het tekort zich over de bol: netto +2.')}
<ol>
<li>Breng de negatieve staaf in de buurt van een neutrale geleidende bol. Enkele vrije elektronen worden naar de verre kant geduwd. Aan de kant van de staaf blijven + ladingen zonder partner over.</li>
<li>Verbind de bol met de aarde. De weggeduwde elektronen stromen naar de aarde: zo komen ze nog verder van de staaf. De + ladingen aan de kant van de staaf blijven zonder partner: er komen geen elektronen van de aarde bij, want de negatieve staaf stoot elektronen af.</li>
<li>Verbreek de verbinding met de aarde, terwijl de staaf er nog is.</li>
<li>Haal de staaf weg. De bol heeft nu een elektronentekort: hij is <b>positief</b> geladen.</li></ol>
{kader('Tekentip bij influentie', '<p>Staat er een geladen staaf in de buurt, dan wordt de bol bij het aarden <b>niet</b> neutraal. Teken elke + met zijn eigen −. De staaf duwt een paar elektronen naar de verre kant: zij hebben geen partner meer. Juist die elektronen vertrekken via de aarding, want de staaf duwt ze weg en de aarde biedt een weg om nog verder weg te gaan. Hoeveel het er zijn, hangt af van hoe sterk de staaf geladen is; in de tekening kies je zelf een klein aantal, bv. 2.</p>')}
{kader('Let op de volgorde', '<p>Haal je de staaf weg <b>vóór</b> je de aarding verbreekt, dan komen de elektronen terug van de aarde en is de bol weer neutraal. Bij laden door influentie krijgt de geleider altijd een lading die <b>tegengesteld</b> is aan die van het geladen voorwerp.</p>')}
{tool(TOOL + '#l5', 'Tool: influentie en polarisatie')}
{denk('denk_2', 'Je laadt een metalen bol door contact met een negatieve staaf, en een tweede bol door influentie met dezelfde staaf. Welk teken heeft elke bol? Verklaar met de beweging van de elektronen.', [
  ('Contact', 'Bij het contact gaan elektronen van de staaf naar de bol. De bol krijgt een elektronenoverschot: negatief.'),
  ('Influentie', 'De staaf duwt elektronen van de bol weg naar de aarde. Na het verbreken van de aarding heeft de bol een elektronentekort: positief.')],
  'Contact geeft hetzelfde teken als de staaf (−), influentie het tegengestelde teken (+).')}

<h3>1.2.3 Toepassingen</h3>
<h4>Het fotokopieertoestel</h4>
<p>Een kopieertoestel en een laserprinter gebruiken een <b>trommel</b> met een <b>fotogeleidende laag</b>. In het donker is die laag een isolator; waar er licht op valt, wordt ze een geleider. De trommel is geaard.</p>
<ol>
<li>De trommel wordt in het donker overal <b>positief</b> geladen. De laag is een isolator, dus de lading blijft zitten.</li>
<li>Een lamp verlicht het origineel. De <b>witte</b> delen weerkaatsen licht naar de trommel. Daar wordt de laag geleidend en vloeit de lading weg via de aarding. Alleen waar de <b>letters</b> staan, blijft de trommel positief.</li>
<li>De <b>toner</b> is <b>negatief</b> geladen. Hij wordt aangetrokken door de positieve delen van de trommel: er ontstaat een tonerbeeld.</li>
<li>Het papier wordt <b>sterker positief</b> geladen dan de trommel en trekt de toner van de trommel naar zich toe.</li>
<li>In de <b>fixeereenheid</b> smelten warmte en druk de toner vast in het papier. De trommel wordt ontladen en gereinigd.</li></ol>
{tool(TOOL + '#l7', 'Tool: fotokopieertoestel')}
<h4>Het swifferdoekje</h4>
<ol>
<li><b>Wrijving</b>: de kunststofvezels wrijven over het oppervlak en worden negatief geladen.</li>
<li><b>Polarisatie</b>: een neutraal stofdeeltje in de buurt van het doekje wordt gepolariseerd. De positieve kant komt naar het doekje toe.</li>
<li><b>Aantrekking</b>: de positieve kant ligt dichter bij het doekje dan de negatieve kant. De aantrekking wint: het stof kleeft aan het doekje.</li></ol>
{tool(TOOL + '#l8', 'Tool: swifferdoekje')}
{verd('Waarom vonkt het in de winter?', '<p>Droge lucht is een goede isolator: lading die je opbouwt door over een tapijt te lopen of over een stoel in de metro te schuiven, kan niet weglekken. Raak je dan een metalen deurklink of een metalen paal aan, dan ontlaad je met een kleine vonk. Vochtige lucht geleidt een beetje en voert de lading geleidelijk af.</p>')}
{denk('denk_3', 'Een swifferdoekje trekt stof aan, ook al is het stof neutraal. Een leerling zegt: "Het stof moet dus positief geladen zijn." Klopt dat?', [
  ('Is het stof geladen?', 'Nee, het stof is neutraal.'),
  ('Wat gebeurt er dan?', 'Het negatieve doekje polariseert het stofdeeltje: de positieve kant komt naar het doekje toe.'),
  ('Waarom netto aantrekking?', 'De positieve kant ligt dichter bij het doekje dan de negatieve kant; de aantrekking is dus groter dan de afstoting.')],
  'De leerling heeft geen gelijk. Ook neutrale deeltjes worden aangetrokken, door polarisatie.')}'''

oefs = f'''<p>Maak deze oefeningen op papier. Gebruik bij rekenoefeningen: gegeven, gevraagd, formule, oplossing, antwoord met eenheid. De oplossingen verschijnen hier nadat we de oefeningen in de les besproken hebben. Maak ook de oefeningen 1, 6, 7, 8, 9 en 10 in het leerboek (p. 25–26).</p>
<p><button class="knop licht" data-print="oef">Oefeningen afdrukken</button></p>
{oef('opl_1', 1, 'Elementaire lading', 'Een voorwerp heeft 5,0 · 10¹¹ elektronen te weinig.<ol class="deelvragen" type="a"><li>Is het voorwerp positief of negatief geladen?</li><li>Bereken de lading in C en in nC.</li></ol>', [
  ('a', 'Elektronentekort: positief geladen.'), ('b', '<i>Q</i> = <i>n</i> · <i>e</i> = 5,0 · 10¹¹ · 1,602 · 10⁻¹⁹ C = 8,0 · 10⁻⁸ C = 80 nC')], '<i>Q</i> = +8,0 · 10⁻⁸ C = +80 nC')}
{oef('opl_2', 2, 'Kan dit?', 'Een leerling meet een lading van 2,4 · 10⁻¹⁹ C op een stofdeeltje. Is dat mogelijk? Verklaar.', [
  ('Hoeveel keer e?', '2,4 · 10⁻¹⁹ / 1,602 · 10⁻¹⁹ = 1,5'), ('Besluit', 'Lading is altijd een geheel veelvoud van <i>e</i>. 1,5 is geen geheel getal.')], 'Neen: er kan geen half elektron overgaan. De meting is fout.')}
{oef('opl_3', 3, 'Tribo-elektrische reeks', 'Gebruik de reeks in figuur 1.3.<ol class="deelvragen" type="a"><li>Je wrijft wol over een PVC-buis. Welk voorwerp wordt negatief?</li><li>Je wrijft nylon over zijde. In welke zin bewegen de elektronen?</li><li>Bij welk paar gaat er meer lading over: glas en PVC, of wol en zijde? Verklaar.</li></ol>', [
  ('a', 'PVC staat lager dan wol: PVC wordt negatief.'), ('b', 'Nylon staat hoger: elektronen gaan van het nylon naar de zijde.'), ('c', 'Glas en PVC staan het verst uit elkaar: daar gaat de meeste lading over.')], 'Hoger in de reeks → positief; verder uit elkaar → meer lading.')}
{oef('opl_4', 4, 'Contact', 'Drie identieke metalen bollen hebben de ladingen <i>Q</i><sub>A</sub> = +9,0 nC, <i>Q</i><sub>B</sub> = −3,0 nC en <i>Q</i><sub>C</sub> = 0. Eerst raakt A B. Daarna raakt B C. Bereken de lading van elke bol op het einde.', [
  ('A en B', '(+9,0 − 3,0) / 2 = +3,0 nC elk'), ('B en C', '(+3,0 + 0) / 2 = +1,5 nC elk'), ('Controle', '3,0 + 1,5 + 1,5 = 6,0 nC = 9,0 − 3,0 nC: de lading is behouden.')], '<i>Q</i><sub>A</sub> = +3,0 nC, <i>Q</i><sub>B</sub> = <i>Q</i><sub>C</sub> = +1,5 nC')}
{oef('opl_5', 5, 'Aarding', 'Een metalen bol op een isolerend voetje is positief geladen. Je raakt hem aan met je hand.<ol class="deelvragen" type="a"><li>Welke deeltjes bewegen, en in welke zin?</li><li>Wat is de lading van de bol daarna?</li><li>Waarom gebeurt dit niet als je een geladen kunststof staaf aanraakt?</li></ol>', [
  ('a', 'Elektronen bewegen van de aarde, via je lichaam, naar de bol. Protonen bewegen niet.'), ('b', 'De bol is neutraal.'), ('c', 'Kunststof is een isolator: alleen de lading op de plaats van je hand kan wegvloeien.')], 'Aarden van een positief voorwerp: elektronen komen van de aarde.')}
{oef('opl_6', 6, 'Laden door influentie', 'Je wilt een metalen bol negatief laden door influentie. Welk geladen voorwerp gebruik je? Beschrijf de vier stappen en teken bij elke stap de ladingen.', [
  ('Voorwerp', 'Een positief geladen staaf, want influentie geeft een tegengestelde lading.'), ('1', 'Staaf bij de bol: vrije elektronen worden aangetrokken naar de kant van de staaf.'), ('2', 'Bol aarden: elektronen stromen van de aarde naar de bol.'), ('3–4', 'Aarding verbreken, daarna de staaf weghalen: de bol heeft een elektronenoverschot.')], 'Met een positieve staaf wordt de bol negatief.')}
{oef('opl_7', 7, 'Polarisatie', 'Een negatief geladen ballon blijft aan een (neutrale) muur kleven.<ol class="deelvragen" type="a"><li>Maak een tekening van de ballon en de moleculen in de muur.</li><li>Leg uit waarom de ballon aangetrokken wordt.</li></ol>', [
  ('a', 'Moleculen in de muur als kleine dipolen, met de + kant naar de ballon.'), ('b', 'De + kanten liggen dichter bij de ballon dan de − kanten. De aantrekking is groter dan de afstoting.')], 'Polarisatie zorgt voor netto aantrekking.')}
{oef('opl_8', 8, 'Toepassingen', 'Leg met de correcte terminologie uit:<ol class="deelvragen" type="a"><li>waarom bij een kopieertoestel de toner alleen op de plaats van de letters terechtkomt;</li><li>waarom de grond onder een onweerswolk positief geladen wordt;</li><li>waarom een bliksemafleider met een dikke geleider met de aarde verbonden is.</li></ol>', [
  ('a', 'Waar licht valt (witte delen) wordt de fotogeleidende laag geleidend en vloeit de positieve lading weg. Alleen de plaatsen van de letters blijven positief en trekken de negatieve toner aan.'),
  ('b', 'Influentie: de negatieve onderkant van de wolk stoot elektronen in de grond af.'), ('c', 'Zo kan de lading via een geleider veilig naar de aarde: aarding.')], 'Gebruik de begrippen: fotogeleidend, influentie, aarding.')}
{oef('opl_9', 9, 'Onweer boven Brussel', 'Op een zomeravond hangt een onweerswolk boven het Jubelpark. De onderkant van de wolk is negatief geladen.<ol class="deelvragen" type="a"><li>Welke lading krijgt het grasveld onder de wolk? Hoe heet dit verschijnsel?</li><li>De bliksem slaat in. Bewegen de elektronen van de wolk naar de grond of omgekeerd?</li><li>Het KMI in Ukkel registreert de inslag, kilometers verder. Wat vangen de sensoren op?</li></ol>', [
  ('a', 'Positief: de negatieve wolk stoot elektronen in de grond weg. Dat is influentie.'), ('b', 'Van de wolk (elektronenoverschot) naar de grond.'), ('c', 'De elektromagnetische golven die de bliksemontlading uitzendt.')], 'Influentie maakt de grond positief; de bliksem is een ontlading van wolk naar aarde.')}'''

cornell = '''<p>Op het bord bouwen we samen een Cornellschema op. Links staan de vragen, rechts noteer je de antwoorden die we samen opbouwen. Onderaan vat je alles samen in je eigen woorden. Dek thuis de rechterkolom af en overhoor jezelf.</p>
<p><button class="knop licht" data-print="cornell">Cornellblad afdrukken</button></p>'''

begrippen = '''<div class="begrippen">
<p><b>aarding</b> — geleidende verbinding met de aarde, waardoor een voorwerp neutraal wordt</p>
<p><b>elementaire lading</b> — lading van één proton, <i>e</i> = 1,602 · 10⁻¹⁹ C</p>
<p><b>elektronenoverschot</b> — meer elektronen dan protonen: negatief geladen</p>
<p><b>elektronentekort</b> — minder elektronen dan protonen: positief geladen</p>
<p><b>fotogeleidend</b> — isolator in het donker, geleider in het licht</p>
<p><b>geleider</b> — stof met vrije ladingdragers</p>
<p><b>influentie</b> — verschuiving van vrije elektronen in een geleider door een geladen voorwerp in de buurt</p>
<p><b>isolator</b> — stof zonder vrije ladingdragers</p>
<p><b>polarisatie</b> — verschuiving van elektronen binnen elk molecule van een isolator</p>
<p><b>tribo-elektrische reeks</b> — rangschikking van stoffen volgens hoe gemakkelijk ze elektronen afgeven</p>
</div>'''

samenv = kader('Samenvatting', '''<p>Een voorwerp is geladen door een <b>tekort</b> (+) of een <b>overschot</b> (−) aan elektronen. De lading is een veelvoud van de elementaire lading: <i>Q</i> = ±<i>n</i> · <i>e</i>, met <i>e</i> = 1,602 · 10⁻¹⁹ C.</p>
<p><b>Wrijving</b>: de stof die hoger in de tribo-elektrische reeks staat, wordt positief. <b>Contact</b>: de lading verdeelt zich, met hetzelfde teken. <b>Influentie</b>: een geleider wordt blijvend geladen met het tegengestelde teken (staaf erbij, aarden, aarding verbreken, staaf weg).</p>
<p><b>Geleiders</b> hebben vrije ladingdragers, <b>isolatoren</b> niet. In een isolator treedt <b>polarisatie</b> op. <b>Aarden</b> maakt een geleider neutraal. Lading blijft altijd <b>behouden</b>.</p>
<p>Toepassingen: bliksem en bliksemafleider, fotokopieertoestel, swifferdoekje.</p>''')

delen = [('deel11', '1.1', 'Lading in materie', d11), ('deel12', '1.2', 'Laden van voorwerpen', d12)]
blokken = [blok('lesdoelen', '', 'Lesdoelen', lesdoelen), blok('voorkennis', '', 'Voorkennis', voorkennis)] + \
          [blok(i, n, t, c, i) for i, n, t, c in delen] + \
          [blok('oefeningen', '', 'Oefeningen', oefs, 'oefeningen'), blok('begrippen', '', 'Begrippenlijst', begrippen), blok('samenvatting', '', 'Samenvatting', samenv, 'samenvatting')]
vrij = [('deel11', True, '1.1 Lading in materie'), ('deel12', False, '1.2 Laden van voorwerpen'),
        ('denk_1', False, 'redenering denkvraag 1'), ('denk_2', False, 'redenering denkvraag 2'), ('denk_3', False, 'redenering denkvraag 3'),
        ('oefeningen', False, 'de oefeningen zelf (opgaven)')] + [(f'opl_{i}', False, f'oplossing oefening {i}') for i in range(1, 10)] + [('samenvatting', False, 'samenvatting')]
cvr = [['Wat is de elementaire lading? Waar komt ze voor?', 22], ['Wanneer is een voorwerp positief of negatief geladen?', 24], ['Wat zegt de tribo-elektrische reeks? Voorbeeld?', 28],
       ['Verschil tussen geleider en isolator?', 22], ['Wat is aarding? Bij + en bij −?', 26], ['Hoe laad je door wrijving, contact en influentie?', 36],
       ['Wat is polarisatie? Tekening.', 28], ['Hoe ontstaat bliksem?', 24], ['Hoe werken een kopieertoestel en een swifferdoekje?', 34]]
bouw('cursus-ladingen.html', 'Fysica 5de jaar · Thema 1 Elektrostatica · Hoofdstuk 1', 'Ladingen',
     'Deze cursus hoort bij de tool <a href="ladingen.html">Elektrische ladingen</a>. De nummering van definities, vergelijkingen en figuren loopt per hoofdstuk. Oefeningen maak je op papier.',
     blokken, vrij, cvr)
print('ok')
