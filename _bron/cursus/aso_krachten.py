# Cursus fysica 3de jaar · andere richtingen (leerplan II-Nat'-d) · Thema 1 Krachten (hoofdstuk 1 tot 5)
# Hergebruikt de delen 'effect', 'vector', 'traagheid' en 'beweging' uit de 3NW-cursus (derde_krachten.py).
# Bouwen: cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/aso_krachten.py
import sys, re
sys.argv = ['x']
sys.path.insert(0, '/home/claude/toolswetenschappen/_bron/cursus')
from bouw import blok, denk, oef, tool, kader, figuur, bouw

_ns = {}
exec(open('/home/claude/toolswetenschappen/_bron/cursus/derde_krachten.py', encoding='utf-8').read().split('delen = [')[0], _ns)
svg, t, pijl, lijn, punt, sub = (_ns[k] for k in ('svg', 't', 'pijl', 'lijn', 'punt', 'sub'))
B, G, R, INK, GRIJS = '#2563eb', '#059669', '#dc2626', '#1D2A36', '#64748b'
PAARS, ORANJE = '#7c3aed', '#d97706'
def vec(x, y, kleur):  # vectorpijltje boven een letter (x = midden van de letter, y = basislijn)
    return f'<path d="M{x-5},{y-15} H{x+5} M{x+2},{y-18} L{x+5},{y-15} L{x+2},{y-12}" stroke="{kleur}" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'

LET = '<div style="background:#FFF7ED;border-left:4px solid #D97706;border-radius:0 8px 8px 0;padding:8px 12px;margin:12px 0"><b style="color:#B45309">Let op.</b> '
TAB = '<table style="border-collapse:collapse;margin:8px 0 12px;font-size:15px" cellpadding="5" border="1" bordercolor="#cbd5e1">'
# tools van 3ASO in plaats van 3NW
def aso(s):
    s = (s.replace('<div class="kop">Traagheid en resulterende kracht in het dagelijks leven', '<div class="kop">Voorbeelden uit het dagelijks leven')
          .replace('<div class="kader"><div class="kop">', '<div class="kader"><div class="kop">Ken dit · ')
          .replace('Ken dit · Voorbeelden uit het dagelijks leven', 'Voorbeelden uit het dagelijks leven'))
    return (s.replace('krachten-beweging.html', 'krachten-beweging-3aso.html')
             .replace('krachten.html', 'krachten-3aso.html'))

# ---------- lesdoelen (leerstofoverzicht 3ASO) ----------
lesdoelen = '''<p>Na dit thema kan je:</p><ul class="doelen">
<li>meetresultaten weergeven in de <b>SI-eenheid</b> en in een <b>afgeleide eenheid</b>;</li>
<li>meetresultaten weergeven met het juiste aantal <b>beduidende cijfers</b>;</li>
<li>de <b>wetenschappelijke notatie</b> gebruiken;</li>
<li>het <b>statisch</b> en <b>dynamisch effect</b> van een kracht aantonen in concrete situaties;</li>
<li>een kracht voorstellen als <b>vector</b> en krachten <b>tekenen op schaal</b>;</li>
<li>aantonen hoe de <b>bewegingstoestand</b> van een voorwerp verandert;</li>
<li>het <b>traagheidsbeginsel</b> uitleggen en de <b>snelheidsvector</b> tekenen;</li>
<li>uitleggen dat de <b>zwaartekracht</b> werkt in het <b>zwaarteveld</b> van een hemellichaam, en het verschil tussen beide geven;</li>
<li>de formule <b>F<sub>z</sub> = m · g</b> gebruiken en omvormen;</li>
<li>het verschil geven tussen <b>massa</b>, <b>zwaartekracht</b>, <b>gewicht</b> en <b>normaalkracht</b>;</li>
<li>uitleggen wat <b>veerkracht</b> is en de formule <b>F<sub>v</sub> = k · Δl</b> gebruiken en omvormen.</li></ul>'''

voorkennis = '''<p>Dit moet je al kennen. Twijfel je? Herhaal het dan eerst.</p><ul>
<li>Met een <b>lat</b> een lengte meten in cm en mm.</li>
<li>Rekenen met <b>kommagetallen</b> en een <b>rekenmachine</b> gebruiken.</li>
<li>Een formule invullen: in v = s / t vul je de getallen in plaats van de letters in.</li></ul>'''

# ---------- hoofdstuk 1: rekenen ----------
h1 = kader('Ken dit · SI-eenheden', '''<p>Elke <b>grootheid</b> heeft een symbool en een <b>SI-eenheid</b>:</p>
<table style="border-collapse:collapse;margin:8px 0 12px;font-size:15px" cellpadding="5" border="1" bordercolor="#cbd5e1"><tr><th>grootheid</th><th>symbool</th><th>SI-eenheid</th></tr>
<tr><td>lengte</td><td>l</td><td>meter (m)</td></tr><tr><td>massa</td><td>m</td><td>kilogram (kg)</td></tr>
<tr><td>tijd</td><td>t</td><td>seconde (s)</td></tr><tr><td>kracht</td><td>F</td><td>newton (N)</td></tr></table>
<p>Met een <b>voorvoegsel</b> maak je een <b>afgeleide eenheid</b>: k (kilo) = 1000, c (centi) = 0,01, m (milli) = 0,001.<br>
2,5 km = 2500 m · 350 g = 0,350 kg · 45 min = 45 · 60 s = 2700 s</p>''') + \
'''<p>Is een getal heel groot of heel klein, dan schrijf je het in <b>wetenschappelijke notatie</b>: een getal tussen 1 en 10, maal een macht van 10.</p>''' + \
kader('Ken dit · Wetenschappelijke notatie', '''<p>a · 10<sup>n</sup> met 1 ≤ a &lt; 10.<br>
384 000 km = 3,84 · 10<sup>5</sup> km (komma 5 plaatsen naar links → +5)<br>
0,00052 m = 5,2 · 10<sup>−4</sup> m (komma 4 plaatsen naar rechts → −4)</p>''') + \
'''<p>Een meting is nooit perfect. Met de <b>beduidende cijfers</b> (BC) toon je hoe nauwkeurig je gemeten hebt.</p>''' + \
kader('Ken dit · Beduidende cijfers', '''<p>Alle cijfers tellen mee, behalve de nullen vooraan: 0,0450 heeft <b>3 BC</b> (4, 5 en de laatste 0). 12,0 heeft 3 BC.</p>
<p>Bij <b>vermenigvuldigen en delen</b> krijgt de uitkomst evenveel BC als het gegeven met de minste BC: 2,5 m · 3,14 m = 7,85 m² → <b>7,9 m²</b> (2 BC).</p>''') + \
LET + 'Je rekenmachine weet niet hoe nauwkeurig je gemeten hebt. Neem nooit alle cijfers over: rond af op het juiste aantal BC.</div>' + \
tool('rekenen-fysica-3aso.html', 'Oefen omzetten, notatie en beduidende cijfers in de tool')

# ---------- hoofdstuk 2: krachten (uit 3NW) ----------
h2a = aso(_ns['d1'])
h2b = aso(_ns['d2'])

# ---------- hoofdstuk 3: kracht en beweging ----------
fig_v = svg(
    '<rect width="600" height="170" fill="#fff"/><line x1="20" y1="130" x2="580" y2="130" stroke="#94a3b8" stroke-width="2"/>'
    + ''.join(f'<rect x="{x-24}" y="104" width="48" height="20" rx="6" fill="#cbd5e1" stroke="#475569"/><circle cx="{x-13}" cy="126" r="6" fill="#334155"/><circle cx="{x+13}" cy="126" r="6" fill="#334155"/>' for x in (80, 300, 500))
    + pijl(80, 96, 130, 96, ORANJE) + t(105, 84, 'v' + sub('1'), ORANJE) + vec(101, 84, ORANJE)
    + pijl(300, 96, 390, 96, ORANJE) + t(345, 84, 'v' + sub('2'), ORANJE) + vec(341, 84, ORANJE)
    + pijl(500, 96, 560, 96, ORANJE) + t(530, 84, 'v' + sub('3'), ORANJE) + vec(526, 84, ORANJE)
    + t(80, 158, 't₁', INK, size=13) + t(300, 158, 't₂: sneller', INK, size=13) + t(500, 158, 't₃: trager', INK, size=13), 600, 170)

h3a = '''<p>De <b>bewegingstoestand</b> van een voorwerp is hoe snel het gaat en in welke richting. Die verandert als het voorwerp <b>vertrekt</b>, <b>sneller</b> of <b>trager</b> gaat, <b>stopt</b> of <b>van richting verandert</b>. Daarvoor is altijd een kracht nodig.</p>''' + \
kader('Ken dit · De snelheidsvector', '''<p>De snelheid is ook een <b>vector</b>: een pijl vanaf het voorwerp, in de zin van de beweging.</p>
<p>Hoe <b>sneller</b>, hoe <b>langer</b> de pijl. Staat het voorwerp stil, dan is v = 0: <b>geen pijl</b>.</p>''') + \
figuur(fig_v, 'Dezelfde auto op drie tijdstippen. Op t₂ rijdt hij sneller (langere pijl), op t₃ trager (kortere pijl).') + \
tool('krachten-beweging-3aso.html#sv', 'Teken zelf de snelheidsvector in de tool')

h3b = aso(_ns['k_traag'])
h3c = '''<p>De <b>resulterende kracht F<sub>r</sub></b> is de ene kracht die hetzelfde effect heeft als alle krachten samen. Trekken twee kinderen met even grote krachten in tegengestelde zin aan een slee, dan is F<sub>r</sub> = 0.</p>''' + aso(_ns['k_beweg']) + \
LET + '<b>Wrijving</b> werkt de beweging tegen. Toch heb je ze nodig: zonder wrijving glij je uit, en schuift een fiets in een bocht rechtdoor.</div>'

# ---------- hoofdstuk 4: zwaartekracht ----------
fig_aarde = svg(
    '<rect width="600" height="260" fill="#fff"/><circle cx="300" cy="135" r="120" fill="none" stroke="#94a3b8" stroke-dasharray="5 5"/>'
    '<circle cx="300" cy="135" r="62" fill="#4f86c6"/><path d="M268 112 C280 98 300 104 296 122 C290 138 270 134 268 112Z" fill="#6aa84f"/><path d="M312 150 C326 142 342 150 334 166 C326 178 312 170 312 150Z" fill="#6aa84f"/>'
    + punt(300, 64, PAARS) + pijl(300, 64, 300, 92, PAARS) + t(326, 64, 'Brussel', INK, 'start', 12, 500)
    + punt(236, 168, PAARS) + pijl(236, 168, 260, 156, PAARS)
    + punt(390, 60, PAARS) + pijl(390, 60, 378, 72, PAARS, 3)
    + t(300, 252, 'zwaarteveld van de aarde', GRIJS, size=13, w=600), 600, 260)

fig_boek = svg(
    '<rect width="600" height="230" fill="#fff"/><rect x="170" y="120" width="260" height="14" fill="#b08968"/><rect x="186" y="134" width="12" height="90" fill="#9c7656"/><rect x="402" y="134" width="12" height="90" fill="#9c7656"/>'
    '<rect x="240" y="88" width="120" height="32" rx="3" fill="#60a5fa" stroke="#1e3a8a"/>'
    + punt(300, 104, PAARS, 4) + pijl(300, 104, 300, 168, PAARS) + t(282, 160, 'F' + sub('z'), PAARS, 'end') + vec(272, 160, PAARS)
    + punt(288, 120, G, 4) + pijl(288, 120, 288, 56, G) + t(272, 64, 'F' + sub('N'), G, 'end') + vec(261, 64, G)
    + punt(312, 122, ORANJE, 4) + pijl(312, 122, 312, 186, ORANJE) + t(326, 184, 'F' + sub('G'), ORANJE, 'start') + vec(331, 184, ORANJE), 600, 230)

h4a = '''<p>Laat je een appel los, dan valt hij naar beneden. De aarde trekt aan de appel: dat is de <b>zwaartekracht</b>. Ook de maan en andere hemellichamen trekken aan voorwerpen in hun buurt.</p>''' + \
kader('Ken dit · Definities', '''<p><b>Zwaartekracht F<sub>z</sub>:</b> de aantrekkingskracht die een hemellichaam uitoefent op alle voorwerpen in zijn omgeving.</p>
<p><b>Zwaarteveld:</b> het gebied rond een hemellichaam waar de zwaartekracht werkt.</p>
<p><b>Kenmerken van F<sub>z</sub>:</b> aangrijpingspunt in het zwaartepunt (het midden) · richting verticaal · zin naar het middelpunt van de aarde · grootte F<sub>z</sub> = m · g.</p>''') + \
figuur(fig_aarde, 'Overal wijst de zwaartekracht naar het middelpunt van de aarde. Verder weg is ze kleiner.') + \
LET + 'Zwaarteveld ≠ zwaartekracht. Het zwaarteveld is het <i>gebied</i>. De zwaartekracht is de <i>kracht</i> op een voorwerp in dat gebied.</div>' + \
tool('krachten-3aso.html#zw1', 'Sleep de bal rond de aarde in de tool')

h4b = kader('Ken dit · Zwaartekracht berekenen', '''<p class="formule">F<sub>z</sub> = m · g</p>
<p>F<sub>z</sub> = zwaartekracht (N) · m = massa (kg) · g = <b>zwaarteveldsterkte</b> (N/kg). Op aarde is g = 9,81 N/kg, op de maan 1,62 N/kg.</p>
<p>Omvormen: <b>m = F<sub>z</sub> / g</b> en <b>g = F<sub>z</sub> / m</b>.</p>
<p>In woorden: hoe groter de massa, hoe groter de zwaartekracht (recht evenredig). Hoe sterker het zwaarteveld (grotere g), hoe groter de zwaartekracht.</p>''') + \
'''<p><b>Voorbeeld.</b> Een leerling heeft een massa van 55 kg. F<sub>z</sub> = m · g = 55 kg · 9,81 N/kg = <b>540 N</b>. Op de maan: 55 kg · 1,62 N/kg = 89 N.</p>''' + \
tool('krachten-3aso.html#zw2', 'Vergelijk de zwaartekracht op andere hemellichamen')

h4c = kader('Ken dit · Massa en gewicht', '''<p><b>Massa m</b> (kg): hoeveel stof een voorwerp bevat. Ze is overal even groot, ook op de maan.</p>
<p><b>Gewicht F<sub>G</sub></b> (N): de kracht waarmee een voorwerp op zijn steun drukt of aan zijn ophangpunt trekt. Een voorwerp zonder steun (een duiker in de lucht, een astronaut in het ISS) is <b>gewichtloos</b>.</p>''') + \
'''<p>Een <b>normaalkracht F<sub>N</sub></b> is de kracht die een steun loodrecht uitoefent op een voorwerp. Een boek op een tafel: de tafel duwt het boek omhoog.</p>''' + \
figuur(fig_boek, 'Een boek op een tafel: drie even grote, maar verschillende krachten.') + \
'''<table style="border-collapse:collapse;margin:8px 0 12px;font-size:15px" cellpadding="5" border="1" bordercolor="#cbd5e1"><tr><th>kracht</th><th>uitgeoefend door</th><th>werkt op</th><th>aangrijpingspunt</th></tr>
<tr><td>F<sub>z</sub></td><td>de aarde</td><td>het boek</td><td>zwaartepunt van het boek</td></tr>
<tr><td>F<sub>N</sub></td><td>de tafel</td><td>het boek</td><td>contactvlak, op het boek</td></tr>
<tr><td>F<sub>G</sub></td><td>het boek</td><td>de tafel</td><td>contactvlak, op de tafel</td></tr></table>''' + \
LET + 'Op een weegschaal lees je je massa in kg af, maar de weegschaal meet eigenlijk je gewicht: hoe hard je erop drukt.</div>' + \
tool('krachten-3aso.html#zw4', 'Bekijk de drie krachten in drie situaties')

# ---------- hoofdstuk 5: veerkracht ----------
# hoofdstuk 5: zie aso_veer.py (wordt hieronder uitgevoerd, na de tekenhulpjes)

# ---------- tekenoefeningen (op ruitjes: werk met hokjes, niet met cm) ----------
HK = 20  # px per hokje
def oplfig(code, onder=''):
    return f'<figure class="oplfig">{code}<figcaption>{onder}</figcaption></figure>'
def oef_fig(id, nr, titel, tekst, opgave, stappen, besluit, oplossing):
    h = oef(id, nr, titel, tekst + figuur(opgave, ''), stappen, besluit)
    return h.replace('<div class="besluit">', oplfig(oplossing) + '<div class="besluit">', 1)
def rooster(w, h):
    r = ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="#dbe4ee" stroke-width="1"/>' for x in range(0, w + 1, HK))
    r += ''.join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#dbe4ee" stroke-width="1"/>' for y in range(0, h + 1, HK))
    return f'<rect width="{w}" height="{h}" fill="#fff"/>' + r
def label(x, y, letter, s_, kleur, anker='start'):
    dx = {'start': 6, 'end': -10, 'middle': -len(s_) * 3.3}[anker]
    return t(x, y, letter + sub(s_), kleur, anker) + vec(x + dx, y, kleur)
def doos(x, y, w, h, kleur='#e7c9a9', rand='#7c2d12'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{kleur}" stroke="{rand}" stroke-width="2"/>'

def sc_doos(opl):
    w, h = 600, 240
    o = rooster(w, h) + f'<rect x="0" y="160" width="{w}" height="80" fill="#d6d3d1" opacity=".55"/>' + doos(260, 100, 80, 60) + punt(300, 130, INK, 4)
    if opl: o += pijl(300, 130, 300, 130 + 3 * HK, PAARS) + label(306, 190, 'F', 'z', PAARS)
    return svg(o, w, h)
def sc_boek(opl):
    w, h = 600, 240
    o = rooster(w, h) + '<rect x="160" y="140" width="280" height="14" fill="#b08968"/><rect x="176" y="154" width="12" height="86" fill="#9c7656"/><rect x="412" y="154" width="12" height="86" fill="#9c7656"/>' + doos(240, 100, 120, 40, '#60a5fa', '#1e3a8a') + punt(300, 120, INK, 4)
    if opl:
        o += pijl(300, 120, 300, 120 + 4 * HK, PAARS) + label(306, 196, 'F', 'z', PAARS)
        o += pijl(280, 140, 280, 140 - 4 * HK, G) + label(270, 70, 'F', 'N', G, 'end')
        o += pijl(320, 142, 320, 142 + 4 * HK, ORANJE) + label(330, 226, 'F', 'G', ORANJE)
    return svg(o, w, h)
def sc_lamp(opl, n=3):
    w, h = 600, 260
    o = rooster(w, h) + f'<rect x="0" y="0" width="{w}" height="20" fill="#cbd5e1"/><line x1="300" y1="20" x2="300" y2="140" stroke="{INK}" stroke-width="2"/>' + '<path d="M270 180 L330 180 L318 140 L282 140 Z" fill="#fcd34d" stroke="#92400e" stroke-width="2"/>' + punt(300, 160, INK, 4) + punt(300, 20, INK, 4)
    if opl:
        o += pijl(300, 160, 300, 160 + n * HK, PAARS) + label(306, 166 + n * HK, 'F', 'z', PAARS)
        o += pijl(300, 20, 300, 20 + n * HK, ORANJE) + label(310, 30 + n * HK, 'F', 'G', ORANJE)
    return svg(o, w, h)
def sc_slee(opl):
    w, h = 600, 220
    o = rooster(w, h) + f'<rect x="0" y="160" width="{w}" height="60" fill="#e0f2fe"/>' + doos(260, 120, 80, 34, '#c08457', '#7c2d12') + '<path d="M250 160 H350 Q362 160 362 148" fill="none" stroke="#5b3a1e" stroke-width="3"/>' + punt(300, 137, INK, 4)
    o += pijl(300, 137, 300 + 8 * HK, 137, B) + label(466, 124, 'F', '1', B)
    o += pijl(300, 137, 300 - 4 * HK, 137, R) + label(216, 124, 'F', '2', R, 'end')
    if opl:
        o += punt(300, 80, INK, 4) + pijl(300, 80, 300 + 4 * HK, 80, '#111827') + label(386, 68, 'F', 'r', '#111827')
    return svg(o, w, h)
def sc_veer(opl):
    w, h = 600, 280
    o = rooster(w, h) + f'<rect x="220" y="0" width="160" height="16" fill="#94a3b8"/>' + '<path d="M300,16 v10 l-14,6 l28,8 l-28,8 l28,8 l-28,8 l28,8 l-28,8 l28,8 l-14,6 v10" fill="none" stroke="#475569" stroke-width="3"/>' + doos(270, 120, 60, 50, '#cbd5e1', '#334155') + punt(300, 120, INK, 4) + punt(300, 145, INK, 4)
    if opl:
        o += pijl(300, 120, 300, 120 - 4 * HK, G) + label(310, 60, 'F', 'v', G)
        o += pijl(300, 145, 300, 145 + 4 * HK, PAARS) + label(306, 230, 'F', 'z', PAARS)
    return svg(o, w, h)
def sc_lees():
    w, h = 600, 140
    return svg(rooster(w, h) + doos(380, 40, 80, 60) + punt(380, 70, INK, 4) + pijl(380, 70, 380 - 5 * HK, 70, B) + label(330, 58, 'F', '', B), w, h)
def sc_bal(opl):
    w, h = 600, 280
    o = rooster(w, h) + f'<line x1="0" y1="270" x2="{w}" y2="270" stroke="#64748b" stroke-width="2"/>'
    for x, y, lab in ((140, 230, 't₁: net losgelaten'), (300, 140, 't₂: halfweg'), (460, 40, 't₃: hoogste punt')):
        o += f'<circle cx="{x}" cy="{y}" r="11" fill="#60a5fa" stroke="#1e3a8a" stroke-width="2"/>' + t(x, min(y + 30, 266), lab, INK, size=12, w=600)
    if opl:
        o += pijl(140, 219, 140, 219 - 5 * HK, ORANJE) + label(148, 150, 'v', '1', ORANJE) + pijl(300, 129, 300, 129 - 2 * HK, ORANJE) + label(308, 104, 'v', '2', ORANJE) + t(490, 44, 'v₃ = 0', ORANJE, 'start', 13)
    return svg(o, w, h)

exec(open('/home/claude/toolswetenschappen/_bron/cursus/aso_veer.py', encoding='utf-8').read())

# ---------- oefeningen ----------
oefs = STAP_ = ''
from bouw import STAP

TEKEN = 'Teken op de figuur. Begin elke pijl in het aangrijpingspunt (de stip) en zet het symbool erbij.'
t_lees = oef_fig('opl_x', 0, 'Een kracht aflezen', 'Schaal: 1 hokje ≙ 25 N. Noteer de vier kenmerken van F.', sc_lees(),
    [('Aangrijpingspunt', 'de stip op de linkerkant van de doos'), ('Richting', 'horizontaal'), ('Zin', 'naar links'), ('Grootte', '5 hokjes · 25 N = 125 N')], 'F = 125 N, horizontaal naar links.', sc_lees())
t_doos = oef_fig('opl_x', 0, 'Zwaartekracht tekenen', 'Een doos van 3,0 kg staat op de vloer. Bereken F<sub>z</sub> (neem g ≈ 10 N/kg) en teken F<sub>z</sub>. Schaal: 1 hokje ≙ 10 N. ' + TEKEN, sc_doos(False),
    [('Berekening', 'F<sub>z</sub> = m · g = 3,0 kg · 10 N/kg = 30 N'), ('Lengte', '30 N : 10 N = 3 hokjes'), ('Tekening', 'vanuit het zwaartepunt (midden), verticaal naar beneden')], 'Een pijl van 3 hokjes vanuit het midden naar beneden.', sc_doos(True))
t_slee = oef_fig('opl_x', 0, 'De resulterende kracht op een slee', 'Sara trekt de slee met F<sub>1</sub> = 40 N naar rechts, haar broer met F<sub>2</sub> = 20 N naar links (schaal: 1 hokje ≙ 5 N). Teken de resulterende kracht F<sub>r</sub> boven de slee. Gaat de slee sneller naar rechts of naar links?', sc_slee(False),
    [('Zelfde richting, tegengestelde zin', 'F<sub>r</sub> = 40 N − 20 N = 20 N'), ('Zin', 'die van de grootste kracht: naar rechts'), ('Tekening', '20 N : 5 N = 4 hokjes naar rechts')], 'F<sub>r</sub> = 20 N naar rechts: de slee gaat sneller naar rechts.', sc_slee(True))
t_bal = oef_fig('opl_x', 0, 'De snelheidsvector van een bal', 'Je gooit een bal recht omhoog. Teken de snelheidsvector op de drie tijdstippen. Op t<sub>1</sub> gaat de bal snel, op t<sub>2</sub> al trager.', sc_bal(False),
    [('t₁', 'een lange pijl naar boven'), ('t₂', 'een kortere pijl naar boven'), ('t₃', 'de bal staat even stil: v = 0, geen pijl')], 'De pijl wordt korter en verdwijnt op het hoogste punt.', sc_bal(True))
t_boek = oef_fig('opl_x', 0, 'Boek op tafel: drie krachten', 'Een boek van 2,0 kg ligt op een tafel (g ≈ 10 N/kg). Teken F<sub>z</sub>, F<sub>N</sub> en F<sub>G</sub>. Schaal: 1 hokje ≙ 5 N. ' + TEKEN, sc_boek(False),
    [('Grootte', 'F<sub>z</sub> = 2,0 · 10 = 20 N; F<sub>N</sub> = F<sub>G</sub> = 20 N → 4 hokjes'), ('F<sub>z</sub>', 'vanuit het midden van het boek, naar beneden'), ('F<sub>N</sub>', 'vanuit het contactvlak, op het boek, naar boven'), ('F<sub>G</sub>', 'vanuit het contactvlak, op de tafel, naar beneden')], 'Drie pijlen van 4 hokjes, dicht bij elkaar.', sc_boek(True))
t_lamp = oef_fig('opl_x', 0, 'Een lamp aan het plafond', 'Een lamp van 0,80 kg hangt aan een snoer (g ≈ 10 N/kg). Teken F<sub>z</sub> en F<sub>G</sub>. Schaal: 1 hokje ≙ 2 N. Waarom is er hier geen normaalkracht?', sc_lamp(False),
    [('Grootte', 'F<sub>z</sub> = F<sub>G</sub> = 0,80 · 10 = 8,0 N → 4 hokjes'), ('F<sub>z</sub>', 'vanuit het midden van de lamp, naar beneden'), ('F<sub>G</sub>', 'vanuit het ophangpunt aan het plafond, naar beneden'), ('Geen F<sub>N</sub>', 'de lamp ligt niet op een steun')], 'F<sub>z</sub> werkt op de lamp, F<sub>G</sub> op het plafond.', sc_lamp(True, 4))
t_veer = oef_fig('opl_x', 0, 'Veerkracht tekenen', 'Aan een veer hangt een massa van 200 g. Ze hangt stil (g ≈ 10 N/kg). Teken F<sub>z</sub> en F<sub>v</sub> op de massa. Schaal: 1 hokje ≙ 0,5 N. ' + TEKEN, sc_veer(False),
    [('F<sub>z</sub>', '0,200 kg · 10 N/kg = 2,0 N → 4 hokjes, vanuit het midden naar beneden'), ('F<sub>v</sub>', 'de massa hangt stil: F<sub>v</sub> = F<sub>z</sub> = 2,0 N → 4 hokjes, vanuit het ophangpunt naar boven')], 'Twee even lange pijlen in tegengestelde zin.', sc_veer(True))
_O = [
 oef('opl_1', 1, 'Eenheden omzetten', 'Zet om naar de SI-eenheid.<ol class="deelvragen" type="a"><li>3,2 km</li><li>750 g</li><li>2 min 30 s</li><li>45 cm</li></ol>',
     [('a', '3,2 · 1000 m = 3200 m'), ('b', '750 : 1000 kg = 0,750 kg'), ('c', '2 · 60 s + 30 s = 150 s'), ('d', '45 · 0,01 m = 0,45 m')], 'SI-eenheden: m, kg, s.'),
 oef('opl_2', 2, 'Wetenschappelijke notatie', 'Schrijf in wetenschappelijke notatie.<ol class="deelvragen" type="a"><li>150 000 000 km (afstand aarde–zon)</li><li>0,0035 m</li><li>7 800 000 inwoners</li></ol>',
     [('a', '1,5 · 10<sup>8</sup> km'), ('b', '3,5 · 10<sup>−3</sup> m'), ('c', '7,8 · 10<sup>6</sup>')], 'Eén cijfer (niet 0) voor de komma.'),
 oef('opl_3', 3, 'Beduidende cijfers', 'Hoeveel BC hebben 0,0072 en 3,50? Bereken daarna de oppervlakte van een blad van 21,0 cm op 29,7 cm met het juiste aantal BC.',
     [('BC', '0,0072: 2 BC · 3,50: 3 BC'), ('Berekening', '21,0 cm · 29,7 cm = 623,7 cm²'), ('Afronden', 'beide 3 BC → 624 cm²')], 'A = 624 cm²'),
 oef('opl_4', 4, 'Statisch of dynamisch?', 'Statisch of dynamisch effect?<ol class="deelvragen" type="a"><li>Je kneedt deeg.</li><li>Een keeper houdt de bal tegen.</li><li>Een fietser draait de hoek om.</li><li>Een plank buigt door onder een persoon.</li></ol>',
     [('a', 'statisch: de vorm verandert'), ('b', 'dynamisch: de bal stopt'), ('c', 'dynamisch: de richting verandert'), ('d', 'statisch')], 'Vorm → statisch, beweging → dynamisch.'),
 oef('opl_5', 5, 'Kracht op schaal', 'a) Teken een kracht van 60 N horizontaal naar rechts met de schaal 1 cm ≙ 20 N. b) Een pijl is 3,5 cm lang bij de schaal 1 cm ≙ 50 N. Hoe groot is de kracht?',
     [('a', '60 N : 20 N = 3 → een pijl van 3,0 cm naar rechts'), ('b', '3,5 · 50 N = 175 N')], 'a) 3,0 cm · b) 175 N'),
 t_lees, t_doos, t_slee,
 oef('opl_6', 6, 'Traagheid uitleggen', 'Leg uit met het woord traagheid.<ol class="deelvragen" type="a"><li>Waarom draag je een gordel?</li><li>Waarom is een volle winkelkar moeilijker te stoppen dan een lege?</li></ol>',
     [('a', 'Remt de auto, dan wil je lichaam even snel verder. De gordel houdt je tegen.'), ('b', 'Grotere massa → grotere traagheid.')], 'Traagheid: een voorwerp wil blijven doen wat het deed.'),
 oef('opl_7', 7, 'Snelheidsvector', 'Een fietser rijdt naar rechts en remt voor een rood licht. Teken de snelheidsvector op drie tijdstippen: net voor het remmen, tijdens het remmen en als hij stilstaat.',
     [('Voor het remmen', 'een lange pijl naar rechts'), ('Tijdens het remmen', 'een kortere pijl naar rechts'), ('Stilstand', 'v = 0: geen pijl')], 'De zin blijft dezelfde, de pijl wordt korter tot hij verdwijnt.'),
 t_bal,
 oef('opl_8', 8, 'Zwaartekracht berekenen', 'Een rugzak heeft een massa van 6,5 kg. Bereken de zwaartekracht op aarde en op de maan.',
     [('Gegeven', 'm = 6,5 kg · g<sub>aarde</sub> = 9,81 N/kg · g<sub>maan</sub> = 1,62 N/kg'), ('Formule', 'F<sub>z</sub> = m · g'), ('Aarde', '6,5 · 9,81 = 64 N'), ('Maan', '6,5 · 1,62 = 11 N')], 'F<sub>z</sub> = 64 N op aarde en 11 N op de maan.'),
 oef('opl_9', 9, 'Omvormen', 'a) Op aarde werkt een zwaartekracht van 196 N op een kind. Bereken zijn massa. b) Op Mars werkt op een massa van 10 kg een zwaartekracht van 37 N. Bereken g op Mars.',
     [('a', 'm = F<sub>z</sub> / g = 196 N / 9,81 N/kg = 20 kg'), ('b', 'g = F<sub>z</sub> / m = 37 N / 10 kg = 3,7 N/kg')], 'a) 20 kg · b) 3,7 N/kg'),
 oef('opl_10', 10, 'Massa, zwaartekracht of gewicht?', 'Juist of fout? Verbeter de foute uitspraken.<ol class="deelvragen" type="a"><li>Op de maan is je massa kleiner.</li><li>Een astronaut in het ISS is gewichtloos.</li><li>Gewicht meet je in kg.</li><li>Het gewicht van een boek werkt op de tafel.</li></ol>',
     [('a', 'Fout: je massa blijft gelijk, de zwaartekracht is kleiner.'), ('b', 'Juist: hij drukt op geen steun.'), ('c', 'Fout: gewicht is een kracht, in N.'), ('d', 'Juist.')], 'b en d zijn juist.'),
 oef('opl_11', 11, 'Drie krachten', 'Een fles water (1,5 kg) staat op een tafel. Geef voor F<sub>z</sub>, F<sub>N</sub> en F<sub>G</sub>: door wie, op wat, en de grootte.',
     [('F<sub>z</sub>', 'door de aarde, op de fles: 1,5 · 9,81 = 15 N'), ('F<sub>N</sub>', 'door de tafel, op de fles: 15 N omhoog'), ('F<sub>G</sub>', 'door de fles, op de tafel: 15 N omlaag')], 'Alle drie 15 N, maar drie verschillende krachten.'),
 t_boek, t_lamp,
 oef('opl_12', 12, 'Veerkracht', 'a) Een veer met k = 40 N/m wordt 15 cm uitgerekt. Bereken de veerkracht. b) Een kracht van 3,0 N rekt een veer 6,0 cm uit. Bereken k. c) Welke veer is stijver: die van a of die van b?',
     [('a', 'F<sub>v</sub> = k · Δl = 40 N/m · 0,15 m = 6,0 N'), ('b', 'k = F<sub>v</sub> / Δl = 3,0 N / 0,060 m = 50 N/m'), ('c', 'de veer van b: grotere k')], 'a) 6,0 N · b) 50 N/m · c) de veer van b'),
   o_balpen, o_twee, t_veer,
]
exec(open('/home/claude/toolswetenschappen/_bron/cursus/aso_extra.py', encoding='utf-8').read())
exec(open('/home/claude/toolswetenschappen/_bron/cursus/aso_begrip.py', encoding='utf-8').read())
def _groep(kop, items):
    return f'<h3>{kop}</h3>' + ''.join(items)
oefs = STAP + ''.join([
    _groep('Hoofdstuk 1 · Rekenen in de fysica', [_O[0], _O[1], n1a, _O[2], n1b]),
    _groep('Hoofdstuk 2 · Krachten', [_O[3], _O[5], _O[4], n2]),
    _groep('Hoofdstuk 3 · Kracht en beweging', [_O[8], _O[9], _O[10], n3, _O[7], n3b]),
    _groep('Hoofdstuk 4 · Zwaartekracht, massa en gewicht', [_O[11], _O[12], _O[13], _O[6], _O[14], _O[15], _O[16]]),
    _groep('Hoofdstuk 5 · Veerkracht', [_O[17], _O[18], _O[19], _O[20]]),
    _groep('Gemengd', [g1, g2, g3]),
    _groep('Uitdaging', [AANPAK, u1, u2, u3, u4, u5]),
]) + tool('krachten-3aso.html#oef', 'Extra oefenen in de tool')
# hernummeren in volgorde
_n = [0]
def _nr(m):
    _n[0] += 1
    return f'<div class="oef" data-vrij="opl_{_n[0]}">' + m.group(1) + f'<span class="nr">{_n[0]}</span>'
oefs = re.sub(r'<div class="oef" data-vrij="opl_\w+">(\s*<div class="titel">)<span class="nr">\d+</span>', _nr, oefs)
N_OEF = _n[0]

samenv = kader('Samenvatting', '''<p><b>SI-eenheden</b>: m, kg, s, N. Wetenschappelijke notatie: a · 10<sup>n</sup> met 1 ≤ a &lt; 10. Rond af op het juiste aantal <b>beduidende cijfers</b>.</p>
<p>Een <b>kracht</b> veroorzaakt een vormverandering (<b>statisch</b>) of een verandering van beweging (<b>dynamisch</b>). Een kracht is een <b>vector</b>: aangrijpingspunt, richting, zin, grootte. Teken op schaal.</p>
<p><b>Traagheid</b>: een voorwerp wil zijn snelheid behouden. F<sub>r</sub> = 0 → rust of ERB. F<sub>r</sub> mee met v → sneller, tegen v → trager, loodrecht → bocht. De <b>snelheidsvector</b>: langere pijl = sneller.</p>
<p><b>Zwaartekracht</b> F<sub>z</sub> = m · g werkt in het <b>zwaarteveld</b>. <b>Massa</b> (kg) is overal gelijk. <b>Gewicht</b> F<sub>G</sub> werkt op de steun. <b>Normaalkracht</b> F<sub>N</sub> werkt op het voorwerp.</p>
<p><b>Veerkracht</b> F<sub>v</sub> = k · Δl. Grote k: stijve veer, kleine k: slappe veer.</p>''')

exec(open('/home/claude/toolswetenschappen/_bron/cursus/aso_wisbord.py', encoding='utf-8').read())
h1 = EDI_CSS + WB['h1'] + h1; h2a = WB['h2a'] + h2a; h2b = WB['h2b'] + h2b; h3a = WB['h3a'] + h3a; h3b = WB['h3b'] + h3b; h3c = WB['h3c'] + h3c
h4a = WB['h4a'] + h4a; h4b = WB['h4b'] + h4b; h4c = WB['h4c'] + h4c
delen = [('Rekenen in de fysica', h1), ('Effect van een kracht', h2a), ('Een kracht is een vector', h2b),
         ('De bewegingstoestand en de snelheidsvector', h3a), ('Traagheid', h3b), ('Resulterende kracht en beweging', h3c),
         ('Zwaartekracht en zwaarteveld', h4a), ('Zwaartekracht berekenen', h4b), ('Massa, gewicht en normaalkracht', h4c), ('Veerkracht', h5)]
blokken = [blok('lesdoelen', '', 'Lesdoelen', lesdoelen), blok('voorkennis', '', 'Voorkennis', voorkennis)]
NRS = ['1', '2.1', '2.2', '3.1', '3.2', '3.2', '4.1', '4.2', '4.3–4.4', '5']  # hoofdstuknummers van het leerboek
blokken += [blok(f'deel{i}', NRS[i - 1], kop, inh, f'deel{i}') for i, (kop, inh) in enumerate(delen, start=1)]
blokken += [blok('oefeningen', '', 'Oefeningen op papier', oefs, 'oefeningen'), blok('begrippen', '', 'Begrippenlijst', begrippen), blok('samenvatting', '', 'Samenvatting', samenv, 'samenvatting')]
alle = ''.join(blokken)
denks = sorted(set(re.findall(r'data-vrij="(denk_\d+)"', alle)), key=lambda x: int(x.split('_')[1]))
vrij = [(f'deel{i}', i == 1, kop) for i, (kop, _) in enumerate(delen, start=1)]
vrij += [(d, False, ('antwoorden Test jezelf, deel ' + str(int(d.split('_')[1]) - 100)) if int(d.split('_')[1]) > 100 else 'redenering ' + d.replace('_', 'vraag ')) for d in denks]
vrij += [(x, False, 'oplossing oefening ' + x.replace('opl_v', '5.')) for x in sorted(set(re.findall(r'data-vrij="(opl_v\d+)"', alle)))]
vrij += [('oefeningen', False, 'de oefeningen zelf (opgaven)')] + [(f'opl_{i}', False, f'oplossing oefening {i}') for i in range(1, N_OEF + 1)] + [('samenvatting', False, 'samenvatting')]
bouw('cursus-krachten-3aso.html', "Fysica 3de jaar · andere richtingen · Thema 1 Krachten · Hoofdstuk 1 tot 5", 'Krachten',
     'Werk dit thema samen met de tools <a href="rekenen-fysica-3aso.html">Rekenen in de fysica</a>, <a href="krachten-beweging-3aso.html">Traagheid, resulterende kracht en beweging</a> en <a href="krachten-3aso.html">Zwaartekracht en veerkracht</a>. Oefeningen maak je op papier.',
     blokken, vrij, [])
print('ok')
