# Cursussen fysica 5Wet in het nieuwe formaat: Thema 1 Elektrostatica (H1-H4) en Thema 2 Gemengde schakelingen (H3).
# Gebruik:  cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/nw5_nieuw.py
# Bestaande inhoud en figuren uit ladingen_cursus.py, coulomb_cursus.py, veld_cursus.py, potentiaal_cursus.py en schakel_cursus.py
# (de oude bouw-aanroepen worden opgevangen); nieuwe inhoud in nw5_inhoud.py. Elektrostatica houdt het eigen sjabloon (sjabloon_ac.html, met nummering).
import re, sys
B_ = '/home/claude/toolswetenschappen/_bron/cursus/'
sys.path.insert(0, '/home/claude/cursus')
import bouw as BM

a = {'__name__': 'aso'}
exec(open(B_ + 'aso_krachten.py', encoding='utf-8').read().split("exec(open('/home/claude/toolswetenschappen/_bron/cursus/aso_extra.py'")[0], a)
blok, oef, kader, tool, denk, figuur = a['blok'], a['oef'], a['kader'], a['tool'], a['denk'], a['figuur']
EDI_CSS, edi, W = a['EDI_CSS'], a['edi'], a['wisbord']
svg, t, pijl, punt, label, rooster = a['svg'], a['t'], a['pijl'], a['punt'], a['label'], a['rooster']
INK, PAARS, G, ORANJE, B, R, HK, oef_fig, oplfig = a['INK'], a['PAARS'], a['G'], a['ORANJE'], a['B'], a['R'], a['HK'], a['oef_fig'], a['oplfig']
AANPAK_SCHEMA = 'maak een schets: teken de ladingen, de krachten of het veld, of het schakelschema. Kies dan de juiste formule en reken in SI-eenheden (C, m, N/C, V, Ω, A).'
AANPAK_LEES = 'de gegevens met hun eenheid en hun teken'
exec(open(B_ + 'nieuw_formaat.py', encoding='utf-8').read())
exec(open(B_ + 'nw5_inhoud.py', encoding='utf-8').read())
def fsub(x):
    if isinstance(x, str): return re.sub(r'(?<![A-Za-z])([FpVEWρURI])_((?:pot,)?[a-zA-Z]+)', r'\1<sub>\2</sub>', x)
    if isinstance(x, (list, tuple)): return type(x)(fsub(y) for y in x)
    if isinstance(x, dict): return {k: fsub(v) for k, v in x.items()}
    return x
C = fsub(C)

SJ_AC = open('/home/claude/cursus/sjabloon_ac.html', encoding='utf-8').read()
SJ_STD = BM.SJABLOON
INTRO_EXTRA = ' De oplossingen staan online, zodra ze in de les besproken zijn.'

def laad(bestand, marker='\nbouw('):
    ns = {'_BOUW': lambda *x, **k: None, '_MAAK': lambda *x, **k: ns.setdefault('_maak', x)}
    src = open(B_ + bestand, encoding='utf-8').read().replace(marker, '\n' + ('_BOUW(' if 'bouw' in marker else '_MAAK('))
    exec(src, ns)
    return ns

def hernummer(html):
    n = [0]
    def f(m):
        n[0] += 1
        return f'<div class="oef" data-vrij="opl_{n[0]}">\n  <div class="titel"><span class="nr">{n[0]}</span>'
    return re.sub(r'<div class="oef" data-vrij="opl_\w+">\s*<div class="titel"><span class="nr">\w+</span>', f, html)

def oef_opl(titel, tekst, stappen, besluit, oplossing):
    return oef('opl_x', 0, titel, tekst, stappen, besluit).replace('<div class="besluit">', oplfig(oplossing) + '<div class="besluit">', 1)

def oefintro(oud):
    m = re.search(r'Maak ook de oefeningen[^<]*', oud)
    ook = (' ' + m.group(0)) if m else ''
    return ('<p>Maak deze oefeningen <b>op papier</b>. Gebruik bij rekenoefeningen: gegeven, gevraagd, formule, oplossing, antwoord met eenheid. '
            'Tekenoefeningen maak je op de figuur, met een lat en een potlood.' + ook + ' De oplossingen verschijnen hier nadat we de oefeningen in de les besproken hebben.</p>'
            '<p><button class="knop licht" data-print="oef">🖨 Druk de oefeningen af</button></p>')

def begrippen_uit(html):
    return re.findall(r'<p><b>(.*?)</b> — (.*?)</p>', html)

# ------------------------------------------------------------------ tekenhulpjes
POSK, NEGK = '#d64550', '#2a6f97'
def lad(x, y, s, r=9):
    k = POSK if s > 0 else NEGK
    o = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{k}"/><path d="M{x-5},{y} H{x+5}" stroke="#fff" stroke-width="2.4"/>'
    return o + (f'<path d="M{x},{y-5} V{y+5}" stroke="#fff" stroke-width="2.4"/>' if s > 0 else '')
def metaalbol(x, y, r=62):
    return (f'<rect x="{x-5}" y="{y+r}" width="10" height="46" fill="#fde68a" stroke="#92400e"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e2e8f0" stroke="#475569" stroke-width="2"/>')
def aarde(x, y):
    return ''.join(f'<line x1="{x-18+i*6}" y1="{y+i*6}" x2="{x+18-i*6}" y2="{y+i*6}" stroke="{INK}" stroke-width="2.5"/>' for i in range(3))
PLUS4 = [(-24, -22), (24, -22), (-24, 22), (24, 22)]

def f_aarding(opl):
    o = '<rect width="600" height="270" fill="#fff"/>' + metaalbol(150, 110) + metaalbol(450, 110)
    o += t(150, 24, 'vóór het aarden', INK, 'middle', 13) + t(450, 24, 'na het aarden', INK, 'middle', 13)
    for dx, dy in PLUS4: o += lad(150 + dx - 9, 110 + dy, 1) + lad(450 + dx - 9, 110 + dy, 1)
    for dx, dy in PLUS4 + [(0, -44), (-44, 0), (44, 0)]: o += lad(150 + dx + 9, 110 + dy, -1)
    o += f'<path d="M512 110 H560 V236" fill="none" stroke="{INK}" stroke-width="2"/>' + aarde(560, 236)
    if opl:
        for dx, dy in PLUS4: o += lad(450 + dx + 9, 110 + dy, -1)
        o += pijl(572, 140, 572, 210, B, 3) + t(540, 260, '3 elektronen naar de aarde', B, 'end', 12)
    return svg(o, 600, 270)
def f_influentie(opl):
    o = '<rect width="600" height="240" fill="#fff"/>' + '<rect x="40" y="90" width="150" height="40" rx="10" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>'
    o += ''.join(lad(62 + i * 21, 110, -1, 7) for i in range(6)) + t(115, 78, 'negatieve staaf', INK, 'middle', 12) + metaalbol(380, 110)
    plus = [(-40, -18), (-40, 18), (-8, -36), (-8, -12), (-8, 12), (-8, 36)]
    for dx, dy in plus: o += lad(380 + dx, 110 + dy, 1)
    if opl:
        for dx, dy in plus[2:]: o += lad(380 + dx + 18, 110 + dy, -1)
        o += lad(426, 92, -1) + lad(426, 128, -1)
        o += f'<ellipse cx="426" cy="110" rx="17" ry="34" fill="none" stroke="{B}" stroke-width="1.5" stroke-dasharray="5 4"/>'
        o += pijl(310, 200, 250, 200, R, 3) + t(320, 205, 'de bol wordt aangetrokken', R, 'start', 12)
    return svg(o, 600, 240)
def lijnQ(opl):
    w, h = 600, 200
    o = rooster(w, h) + lad(160, 100, 1, 11) + lad(460, 100, 1, 11) + t(160, 140, 'Q₁ = +2,0 μC', INK, 'middle', 13) + t(460, 140, 'Q₂ = +4,0 μC', INK, 'middle', 13)
    o += f'<line x1="160" y1="170" x2="460" y2="170" stroke="{INK}" stroke-width="1.2"/>' + t(310, 188, '30 cm', INK, 'middle', 12, 600)
    if opl: o += pijl(160, 100, 160 - 4 * HK, 100, B) + label(80, 86, 'F', '21', B, 'end') + pijl(460, 100, 460 + 4 * HK, 100, R) + label(546, 86, 'F', '12', R)
    return svg(o, w, h)
def driehoekQ(opl):
    w, h = 600, 260
    x0, y0 = 360, 180
    o = rooster(w, h) + lad(x0, y0, -1, 11) + t(x0 + 16, y0 + 26, 'Q₃', INK, 'start', 13)
    o += pijl(x0, y0, x0, y0 - 4 * HK, G) + label(x0 + 8, y0 - 4 * HK + 6, 'F', '13', G) + pijl(x0, y0, x0 - 3 * HK, y0, B) + label(x0 - 3 * HK - 4, y0 + 22, 'F', '23', B, 'end')
    if opl:
        o += f'<line x1="{x0-3*HK}" y1="{y0}" x2="{x0-3*HK}" y2="{y0-4*HK}" stroke="#94a3b8" stroke-dasharray="5 4"/><line x1="{x0}" y1="{y0-4*HK}" x2="{x0-3*HK}" y2="{y0-4*HK}" stroke="#94a3b8" stroke-dasharray="5 4"/>'
        o += pijl(x0, y0, x0 - 3 * HK, y0 - 4 * HK, R) + label(x0 - 3 * HK - 6, y0 - 4 * HK - 4, 'F', 'r', R, 'end')
    return svg(o, w, h)
def platen(xp, xn, w, h, plus_links=True):
    o = rooster(w, h) + f'<rect x="{xp-8}" y="20" width="8" height="{h-40}" fill="{POSK}"/><rect x="{xn}" y="20" width="8" height="{h-40}" fill="{NEGK}"/>'
    o += t(xp - 14, 36, '+', POSK, 'end', 18) + t(xn + 22, 36, '−', NEGK, 'start', 18)
    return o
def f_homogeen(opl):
    w, h = 600, 260
    o = platen(100, 500, w, h)
    for x, y, n in ((200, 70, 'R'), (240, 140, 'P'), (300, 210, 'Q')): o += punt(x, y, INK, 4) + t(x - 8, y - 8, n, INK, 'end', 13)
    o += lad(240, 140, 1, 7) + lad(300, 210, -1, 7)
    if opl:
        o += pijl(200, 70, 200 + 5 * HK, 70, ORANJE) + label(306, 60, 'E', '', ORANJE)
        o += pijl(240, 140, 240 + 4 * HK, 140, R) + label(326, 130, 'F', 'p', R)
        o += pijl(300, 210, 300 - 4 * HK, 210, B) + label(214, 200, 'F', 'e', B, 'end')
    return svg(o, w, h)
def f_radiaal(opl):
    w, h = 600, 320
    o = rooster(w, h) + lad(200, 100, 1, 11) + t(186, 80, '+Q', INK, 'end', 13)
    o += punt(280, 100, INK, 4) + t(280, 92, 'P₁', INK, 'middle', 13) + punt(200, 220, INK, 4) + t(190, 226, 'P₂', INK, 'end', 13)
    if opl: o += pijl(280, 100, 280 + 9 * HK, 100, ORANJE) + label(466, 90, 'E', '1', ORANJE) + pijl(200, 220, 200, 220 + 4 * HK, ORANJE) + label(208, 300, 'E', '2', ORANJE)
    return svg(o, w, h)
def f_equi(opl):
    w, h = 600, 260
    o = rooster(w, h) + f'<rect x="132" y="20" width="8" height="220" fill="{NEGK}"/><rect x="460" y="20" width="8" height="220" fill="{POSK}"/>' + t(126, 36, '−', NEGK, 'end', 18) + t(476, 36, '+', POSK, 'start', 18)
    o += t(300, 254, 'afstand tussen de platen: 4,0 cm · spanning: 2000 V', INK, 'middle', 12, 600)
    if opl:
        for i, v in enumerate((500, 1000, 1500), start=1):
            x = 140 + i * 80
            o += f'<line x1="{x}" y1="30" x2="{x}" y2="226" stroke="{PAARS}" stroke-width="1.6" stroke-dasharray="6 4"/>' + t(x, 18, f'{v} V', PAARS, 'middle', 11, 700)
        o += pijl(440, 130, 160, 130, ORANJE) + label(300, 120, 'E', '', ORANJE)
    return svg(o, w, h)
def f_eldeeltjes(opl):
    w, h = 600, 240
    o = rooster(w, h) + f'<rect x="92" y="20" width="8" height="200" fill="{NEGK}"/><rect x="500" y="20" width="8" height="200" fill="{POSK}"/>' + t(86, 36, '−', NEGK, 'end', 18) + t(516, 36, '+', POSK, 'start', 18)
    o += lad(260, 80, -1, 8) + t(260, 62, 'elektron', INK, 'middle', 12) + lad(340, 170, 1, 8) + t(340, 200, 'proton', INK, 'middle', 12)
    if opl: o += pijl(260, 80, 260 + 4 * HK, 80, B) + label(346, 70, 'F', 'e', B) + pijl(340, 170, 340 - 4 * HK, 170, R) + label(254, 160, 'F', 'p', R, 'end')
    return svg(o, w, h)

# ------------------------------------------------------------------ tekenoefeningen per pagina
T = {}
T['ladingen'] = [
 oef_fig('opl_x', 0, 'Tekenen: aarding', 'Een metalen bol op een isolerend voetje is negatief geladen (links). Je verbindt hem met de aarde. Rechts staan de + ladingen al getekend.<ol class="deelvragen" type="a"><li>Teken de elektronen in de bol na het aarden.</li><li>Teken met een pijl langs de draad in welke zin de elektronen bewegen. Hoeveel elektronen zijn het?</li></ol>', f_aarding(False),
   [('a', 'Na het aarden is de bol neutraal: evenveel − als +. Teken 4 elektronen, elk bij een +.'), ('b', 'De 3 overtollige elektronen stromen van de bol naar de aarde. De + ladingen bewegen niet.')],
   'Na het aarden: 4 + en 4 −. Er stromen 3 elektronen naar de aarde.', f_aarding(True)),
 oef_fig('opl_x', 0, 'Tekenen: influentie', 'Je brengt een negatieve staaf dicht bij een neutrale metalen bol (niet aanraken). De + ladingen van de bol staan al getekend. De staaf duwt 2 elektronen naar de verre kant.<ol class="deelvragen" type="a"><li>Teken alle elektronen van de bol.</li><li>Wordt de bol aangetrokken of afgestoten? Verklaar.</li></ol>', f_influentie(False),
   [('a', 'De bol is neutraal: 6 elektronen. 4 blijven bij hun +; 2 worden naar de rechterkant geduwd. Links blijven 2 + zonder partner.'),
    ('b', 'Aangetrokken: de + kant zonder partner ligt dichter bij de staaf dan de 2 weggeduwde elektronen. De aantrekking is groter dan de afstoting.')],
   'Influentie: de elektronen verschuiven naar de verre kant; de bol wordt aangetrokken.', f_influentie(True))]
T['coulomb'] = [
 oef_fig('opl_x', 0, 'Tekenen: twee ladingen', 'Q₁ = +2,0 μC en Q₂ = +4,0 μC liggen 30 cm uit elkaar.<ol class="deelvragen" type="a"><li>Bereken de coulombkracht.</li><li>Teken de kracht op elke lading. Schaal: 1 hokje ≙ 0,20 N.</li></ol>', lijnQ(False),
   [('a', 'F = 8,99 · 10⁹ · 2,0 · 10⁻⁶ · 4,0 · 10⁻⁶ / 0,30² = 0,80 N'), ('b', 'gelijke ladingen stoten af: op Q₁ 4 hokjes naar links, op Q₂ 4 hokjes naar rechts, elk vanuit de lading')],
   'Twee even lange pijlen van 4 hokjes, weg van elkaar.', lijnQ(True)),
 oef_fig('opl_x', 0, 'Tekenen: de resulterende kracht', 'Op Q₃ werken twee coulombkrachten (getekend). Schaal: 1 hokje ≙ 0,10 N.<ol class="deelvragen" type="a"><li>Lees de grootte van beide krachten af.</li><li>Teken de resulterende kracht met de parallellogrammethode.</li><li>Bereken de grootte van de resulterende kracht.</li></ol>', driehoekQ(False),
   [('a', 'F₁₃ = 4 hokjes = 0,40 N · F₂₃ = 3 hokjes = 0,30 N'), ('b', 'Vul het parallellogram aan met twee stippellijnen; de diagonaal vanuit Q₃ is F<sub>r</sub>.'), ('c', 'F<sub>r</sub> = √(0,40² + 0,30²) = 0,50 N (5 hokjes)')],
   'F<sub>r</sub> = 0,50 N, schuin naar linksboven.', driehoekQ(True))]
T['veld'] = [
 oef_fig('opl_x', 0, 'Tekenen: een homogeen veld', 'Tussen de platen is het veld 2,5 · 10⁴ N/C. In P ligt een proton, in Q een elektron.<ol class="deelvragen" type="a"><li>Teken het veld in R. Schaal: 1 hokje ≙ 5,0 · 10³ N/C.</li><li>Bereken de kracht op het proton en op het elektron.</li><li>Teken beide krachten. Schaal: 1 hokje ≙ 1,0 · 10⁻¹⁵ N.</li></ol>', f_homogeen(False),
   [('a', 'Van de + plaat naar de − plaat: 5 hokjes naar rechts, vanuit R'), ('b', 'F = 1,602 · 10⁻¹⁹ · 2,5 · 10⁴ = 4,0 · 10⁻¹⁵ N, voor beide even groot'),
    ('c', 'proton: 4 hokjes mee met het veld (naar rechts) · elektron: 4 hokjes tegen het veld in (naar links)')], 'Even grote krachten, tegengestelde zin.', f_homogeen(True)),
 oef_fig('opl_x', 0, 'Tekenen: een radiaal veld', 'Een lading van +4,0 nC ligt in de stip. Eén hokje is 2,5 cm. P₁ ligt 10 cm rechts, P₂ 15 cm onder de lading.<ol class="deelvragen" type="a"><li>Bereken het veld in P₁ en in P₂.</li><li>Teken beide veldvectoren. Schaal: 1 hokje ≙ 400 N/C.</li></ol>', f_radiaal(False),
   [('a', 'P₁: E = 8,99 · 10⁹ · 4,0 · 10⁻⁹ / 0,10² = 3,6 · 10³ N/C · P₂: E = 8,99 · 10⁹ · 4,0 · 10⁻⁹ / 0,15² = 1,6 · 10³ N/C'),
    ('b', 'P₁: 9 hokjes naar rechts · P₂: 4 hokjes naar beneden. Beide weg van de positieve lading, vanuit het punt.')],
   'Het veld wijst weg van de positieve lading en wordt snel kleiner met de afstand.', f_radiaal(True))]
T['potentiaal'] = [
 oef_fig('opl_x', 0, 'Tekenen: equipotentiaalvlakken', 'Tussen twee platen op 4,0 cm staat een spanning van 2000 V.<ol class="deelvragen" type="a"><li>Teken de equipotentiaalvlakken van 500 V, 1000 V en 1500 V. Schrijf de potentiaal erbij.</li><li>Teken een veldlijn met de zin van het veld.</li><li>Bereken de veldsterkte.</li></ol>', f_equi(False),
   [('a', 'V = E · d stijgt gelijkmatig van 0 V (− plaat) tot 2000 V (+ plaat): elke 500 V is 1,0 cm verder, dus om de 4 hokjes een vlak evenwijdig aan de platen.'),
    ('b', 'loodrecht op de vlakken, van de + plaat naar de − plaat'), ('c', 'E = U / D = 2000 / 0,040 = 5,0 · 10⁴ N/C')],
   'Equipotentiaalvlakken op gelijke afstanden, loodrecht op de veldlijnen.', f_equi(True)),
 oef_fig('opl_x', 0, 'Tekenen: een elektron en een proton tussen de platen', 'Tussen de platen is het veld 5,0 · 10⁴ N/C. Een elektron en een proton liggen eerst stil.<ol class="deelvragen" type="a"><li>Bereken de kracht op elk deeltje.</li><li>Teken beide krachten. Schaal: 1 hokje ≙ 2,0 · 10⁻¹⁵ N.</li><li>Neemt de potentiële energie van elk deeltje toe of af als je ze loslaat?</li></ol>', f_eldeeltjes(False),
   [('a', 'F = 1,602 · 10⁻¹⁹ · 5,0 · 10⁴ = 8,0 · 10⁻¹⁵ N'), ('b', 'elektron: 4 hokjes naar de + plaat · proton: 4 hokjes naar de − plaat'),
    ('c', 'Bij beide neemt de potentiële energie af: het veld verricht positieve arbeid en ze winnen kinetische energie.')], 'Een vrije lading beweegt altijd zo dat haar potentiële energie daalt.', f_eldeeltjes(True))]

# ------------------------------------------------------------------ elektrostatica (H1-H4)
PAG = [('ladingen_cursus.py', 'ladingen', 1, 'cursus-ladingen.html', 'Fysica 5de jaar · Thema 1 Elektrostatica · Hoofdstuk 1', 'Ladingen',
        'Deze cursus hoort bij de tool <a href="ladingen.html">Ladingen</a>. Oefeningen maak je op papier.'),
       ('coulomb_cursus.py', 'coulomb', 2, 'cursus-coulomb.html', 'Fysica 5de jaar · Thema 1 Elektrostatica · Hoofdstuk 2', 'Krachten tussen ladingen',
        'Deze cursus hoort bij de tool <a href="krachten-op-ladingen.html">Krachten op ladingen</a>. Oefeningen maak je op papier.'),
       ('veld_cursus.py', 'veld', 3, 'cursus-elektrisch-veld.html', 'Fysica 5de jaar · Thema 1 Elektrostatica · Hoofdstuk 3', 'Elektrisch veld',
        'Deze cursus hoort bij de tool <a href="elektrisch-veld.html">Elektrisch veld</a>. Oefeningen maak je op papier.'),
       ('potentiaal_cursus.py', 'potentiaal', 4, 'cursus-potentiaal.html', 'Fysica 5de jaar · Thema 1 Elektrostatica · Hoofdstuk 4', 'Potentiaal',
        'Deze cursus hoort bij de tool <a href="elektrisch-veld.html">Elektrisch veld</a> (tabblad Energie en potentiaal). Oefeningen maak je op papier.')]
BM.FOOTER = 'Cursus fysica 5de jaar — gemaakt voor klasgebruik, bij de tools op Oefentools wetenschappen.'
for i, (bron, k, hfst, bestand, eyebrow, titel, intro) in enumerate(PAG):
    ns = laad(bron)
    oefs = ns['oefs'].split('</button></p>', 1)[1]
    oefs = oefintro(ns['oefs']) + hernummer(oefs + ''.join(T[k]))
    c = dict(C[k]); c['begrip'] = sorted(begrippen_uit(ns['begrippen']) + c['extra'], key=lambda x: re.sub('<[^>]+>', '', x[0]).lower())
    BM.SJABLOON = SJ_AC.replace('{{HFST}}', str(hfst))
    pagina(bestand, eyebrow, titel, intro + INTRO_EXTRA, ns['lesdoelen'], ns['voorkennis'], [(tt, inh) for _, _, tt, inh in ns['delen']],
           oefs, ns['samenv'], c, eerste=(i == 0), cornell=ns['cvr'], nrs=[n for _, n, _, _ in ns['delen']])

# ------------------------------------------------------------------ gemengde schakelingen (thema 2, H3)
ns = laad('schakel_cursus.py', '\nmaak(')
bestand, eyebrow, titel, intro, doelen, voork, delen, oefs, samenv, toolref = ns['_maak']
schema, S_, P_, R_ = ns['schema'], ns['S'], ns['P'], ns['R']
T5 = [oef_opl('Tekenen: een schakelschema', 'Teken het schakelschema: een bron van 12 V, een weerstand R₁ in serie met een paralleldeel van R₂ en R₃. Duid aan waar je een ampèremeter zet om de totale stroom te meten, en waar een voltmeter de spanning over R₁ meet.',
              [('Schema', 'R₁ na de bron, daarna twee takken naast elkaar met R₂ en R₃, terug naar de bron.'), ('Ampèremeter', 'in serie, in de hoofdleiding (bv. vlak na de bron): daar loopt de totale stroom.'),
               ('Voltmeter', 'parallel over R₁: de twee aansluitingen links en rechts van R₁.')], 'Ampèremeter in serie, voltmeter parallel.', schema(S_(R_('R1'), P_(R_('R2'), R_('R3'))), '12 V')),
      oef_opl('Tekenen: twee takken met elk twee weerstanden', 'Teken het schakelschema van (R₁ + R₂) // (R₃ + R₄) op 6,0 V. Neem R₁ = R₂ = 10 Ω en R₃ = R₄ = 5,0 Ω, en bereken de substitutieweerstand en de totale stroom.',
              [('Schema', 'twee takken parallel; in de eerste tak R₁ en R₂ na elkaar, in de tweede R₃ en R₄ na elkaar.'), ('Takken', 'R<sub>12</sub> = 20 Ω · R<sub>34</sub> = 10 Ω'),
               ('R<sub>s</sub>', '20 · 10 / 30 = 6,7 Ω'), ('I', '6,0 / 6,7 = 0,90 A')], 'R<sub>s</sub> = 6,7 Ω en I = 0,90 A.', schema(P_(S_(R_('R1', '10 Ω'), R_('R2', '10 Ω')), S_(R_('R3', '5 Ω'), R_('R4', '5 Ω'))), '6 V'))]
oefs = oefintro('') + hernummer(oefs + ''.join(T5)) + tool(*toolref)
c = dict(C['schakelingen']); c['begrip'] = c['extra']
BM.SJABLOON = SJ_STD
LD = '<p>Na dit hoofdstuk kan je:</p><ul class="doelen">' + ''.join(f'<li>{d}</li>' for d in doelen) + '</ul>'
pagina(bestand, eyebrow, titel, intro + INTRO_EXTRA, LD, voork, delen, oefs, kader('Samenvatting', samenv), c)
