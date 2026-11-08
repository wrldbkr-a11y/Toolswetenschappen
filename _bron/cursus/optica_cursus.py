# Cursus fysica 3de jaar (3NW) · Thema 1 Optische fenomenen · H1-H4
import sys, math
sys.argv = ['x']
from bouw import blok, denk, oef, tool, kader, figuur, bouw, STAP

INK, GRIJS, LICHT, BLAUW, ROOD, GROEN = '#1D2A36', '#64748b', '#f59e0b', '#2563eb', '#dc2626', '#059669'
WATER, GLAS = '#dbeafe', '#e0f2fe'
F = 'font-family="Inter,sans-serif"'

# ---------------------------------------------------------------- helpers
def svg(inner, w=640, h=260):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg"><rect width="{w}" height="{h}" fill="#fff"/>{inner}</svg>'
def t(x, y, s, kleur=INK, anker='middle', size=14, w=700):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{kleur}" font-size="{size}" font-weight="{w}" text-anchor="{anker}" {F}>{s}</text>'
def lijn(x1, y1, x2, y2, kleur=INK, b=2, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{kleur}" stroke-width="{b}"{d} stroke-linecap="round"/>'
def kop(x, y, a, kleur, s=10):
    return f'<path d="M{x + s*0.55*math.cos(a):.1f},{y + s*0.55*math.sin(a):.1f} L{x - s*math.cos(a-0.45):.1f},{y - s*math.sin(a-0.45):.1f} L{x - s*math.cos(a+0.45):.1f},{y - s*math.sin(a+0.45):.1f}Z" fill="{kleur}"/>'
def straal(x1, y1, x2, y2, kleur=LICHT, b=2.5, pijl=True, dash='', pos=0.5):
    s = lijn(x1, y1, x2, y2, kleur, b, dash)
    if pijl:
        a = math.atan2(y2 - y1, x2 - x1)
        s += kop(x1 + (x2 - x1) * pos, y1 + (y2 - y1) * pos, a, kleur)
    return s
def punt(x, y, kleur=INK, r=4):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{kleur}"/>'
def ruit(w, h, stap=20):
    s = ''.join(lijn(x, 0, x, h, '#e5e7eb', 1) for x in range(0, w + 1, stap))
    return s + ''.join(lijn(0, y, w, y, '#e5e7eb', 1) for y in range(0, h + 1, stap))
def oog(x, y, kijk=0):
    a = math.radians(kijk)
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({kijk})"><path d="M-14,0 Q0,-10 14,0 Q0,10 -14,0Z" fill="#fff" stroke="{INK}" stroke-width="1.8"/>'
            f'<circle cx="5" cy="0" r="4.5" fill="#2F6FB0"/><circle cx="6" cy="0" r="2" fill="#111"/></g>')
def boog(cx, cy, r, a1, a2, kleur=INK):  # hoeken in graden, wiskundig (y naar boven)
    x1, y1 = cx + r*math.cos(math.radians(a1)), cy - r*math.sin(math.radians(a1))
    x2, y2 = cx + r*math.cos(math.radians(a2)), cy - r*math.sin(math.radians(a2))
    groot = 1 if abs(a2 - a1) > 180 else 0
    zin = 0 if a2 > a1 else 1
    return f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 {groot},{zin} {x2:.1f},{y2:.1f}" fill="none" stroke="{kleur}" stroke-width="1.5"/>'
def spiegel_v(x, y1, y2):  # verticale spiegel, achterkant rechts gearceerd
    s = lijn(x, y1, x, y2, '#334155', 4)
    s += ''.join(lijn(x + 2, y, x + 10, y - 8, '#94a3b8', 1.2) for y in range(int(y1) + 10, int(y2) + 1, 10))
    return s
def spiegel_h(x1, x2, y):  # horizontale spiegel, achterkant onder
    s = lijn(x1, y, x2, y, '#334155', 4)
    return s + ''.join(lijn(x, y + 2, x - 8, y + 10, '#94a3b8', 1.2) for x in range(int(x1) + 10, int(x2) + 1, 10))
def potlood(ax, ay, bx, by, kleur='#a16207', dash=''):
    # B = achterkant, A = punt
    s = lijn(bx, by, ax, ay, kleur, 7, dash)
    a = math.atan2(ay - by, ax - bx)
    s += kop(ax + 6*math.cos(a), ay + 6*math.sin(a), a, '#1D2A36' if not dash else '#94a3b8', 12)
    return s
def vk(*punten):
    return '<p>Dit moet je al kennen. Twijfel je? Herhaal het dan eerst.</p><ul>' + ''.join(f'<li>{x}</li>' for x in punten) + '</ul>'
def oplfig(svgcode, onderschrift=''):
    return f'<figure class="oplfig">{svgcode}<figcaption>{onderschrift}</figcaption></figure>'
def oef_fig(id, nr, titel, tekst, opgavefig, stappen, besluit, oplossingsfig):
    """oefening met een opgavefiguur (in de tekst) en een oplossingsfiguur (in de redenering)"""
    html = oef(id, nr, titel, tekst + figuur(opgavefig, ''), stappen, besluit)
    return html.replace('<div class="besluit">', oplfig(oplossingsfig) + '<div class="besluit">', 1)
def oefblok(inhoud, toolref=None):
    s = f'''<p>Maak deze oefeningen <b>op papier</b>. Tekenoefeningen maak je op de afgedrukte figuur of je neemt ze over op ruitjespapier; gebruik een lat, een geodriehoek en een potlood. De oplossingen verschijnen hier nadat we de oefeningen in de les besproken hebben.</p>
<p><button class="knop licht" data-print="oef">🖨 Druk de oefeningen af</button></p>
{inhoud}'''
    return s + (tool(*toolref) if toolref else '')
import re as _re
def hernummer(html):
    teller = [0]
    def f(m):
        teller[0] += 1; k = teller[0]
        return f'<div class="oef" data-vrij="opl_{k}">\n  <div class="titel"><span class="nr">{k}</span>'
    return _re.sub(r'<div class="oef" data-vrij="opl_\d+">\s*<div class="titel"><span class="nr">\d+</span>', f, html)
def maak(bestand, eyebrow, titel, intro, doelen, voorkennis, delen, oefeningen, samenvatting, toolref=None):
    oefeningen = hernummer(oefeningen)
    blokken = [blok('lesdoelen', '', 'Lesdoelen', '<p>Na dit hoofdstuk kan je:</p><ul class="doelen">' + ''.join(f'<li>{d}</li>' for d in doelen) + '</ul>'),
               blok('voorkennis', '', 'Voorkennis', voorkennis)]
    vrij = []
    for i, (k, inh) in enumerate(delen, start=1):
        blokken.append(blok(f'deel{i}', i, k, inh, f'deel{i}')); vrij.append((f'deel{i}', i == 1, k))
    blokken += [blok('oefeningen', '', 'Oefeningen op papier', oefblok(oefeningen, toolref), 'oefeningen'),
                blok('samenvatting', '', 'Samenvatting', kader('Samenvatting', samenvatting), 'samenvatting')]
    nd = sum(inh.count('class="denk"') for _, inh in delen)
    no = oefeningen.count('class="oef"')
    vrij += [(f'denk_{i}', False, f'redenering denkvraag {i}') for i in range(1, nd + 1)]
    vrij += [('oefeningen', False, 'de oefeningen zelf (opgaven)')] + [(f'opl_{i}', False, f'oplossing oefening {i}') for i in range(1, no + 1)] + [('samenvatting', False, 'samenvatting')]
    bouw(bestand, eyebrow, titel, intro, blokken, vrij, [])

# ================================================================ H1 ZIEN DOOR LICHT
def bundels():
    o = ''
    for k, (naam, soort) in enumerate([('divergerend', 'div'), ('convergerend', 'con'), ('evenwijdig', 'evw')]):
        x0 = 20 + k * 210
        for d in (-30, -15, 0, 15, 30):
            if soort == 'div': o += straal(x0 + 10, 100, x0 + 180, 100 + d * 2.2)
            elif soort == 'con': o += straal(x0 + 10, 100 + d * 2.2, x0 + 170, 100)
            else: o += straal(x0 + 10, 100 + d * 1.6, x0 + 180, 100 + d * 1.6)
        if soort == 'div': o += punt(x0 + 10, 100, '#f59e0b', 6)
        o += t(x0 + 95, 190, naam + 'e bundel')
    return svg(o, 640, 205)
fig_bundels = bundels()

def schaduw_fig(lampen, ox=270, oy=130, r=32, sx=520, oplossing=True, titel=''):
    o = lijn(sx, 20, sx, 240, '#475569', 5) + t(sx - 10, 30, 'scherm', GRIJS, 'end', 12)
    bereik = []
    for lx, ly in lampen:
        boven = ly + (oy - r - ly) * (sx - lx) / (ox - lx)
        onder = ly + (oy + r - ly) * (sx - lx) / (ox - lx)
        bereik.append((boven, onder))
        if oplossing:
            o += lijn(lx, ly, sx, boven, LICHT, 1.6) + lijn(lx, ly, sx, onder, LICHT, 1.6)
    if oplossing:
        if len(lampen) == 1:
            b, n = bereik[0]
            o += f'<rect x="{sx-4}" y="{b:.1f}" width="8" height="{n-b:.1f}" fill="#111"/>' + t(sx + 12, (b + n) / 2 + 4, 'schaduw', INK, 'start', 13)
        else:
            (b1, n1), (b2, n2) = bereik
            kb, kn = max(b1, b2), min(n1, n2)
            tb, tn = min(b1, b2), max(n1, n2)
            o += f'<rect x="{sx-4}" y="{tb:.1f}" width="8" height="{tn-tb:.1f}" fill="#94a3b8"/>'
            if kn > kb: o += f'<rect x="{sx-4}" y="{kb:.1f}" width="8" height="{kn-kb:.1f}" fill="#111"/>'
            o += t(sx + 12, (kb + kn) / 2 + 4, 'kernschaduw', INK, 'start', 13) + t(sx + 12, tb + 12, 'bijschaduw', GRIJS, 'start', 12) + t(sx + 12, tn - 4, 'bijschaduw', GRIJS, 'start', 12)
    o += f'<circle cx="{ox}" cy="{oy}" r="{r}" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>'
    for i, (lx, ly) in enumerate(lampen):
        o += f'<circle cx="{lx}" cy="{ly}" r="9" fill="#fde047" stroke="#ca8a04" stroke-width="2"/>' + t(lx - 14, ly + 4, f'L{i+1}' if len(lampen) > 1 else 'lamp', INK, 'end', 12)
    if titel: o += t(320, 252, titel, GRIJS, 'middle', 12, 600)
    return svg(o, 640, 260)
fig_schaduw1 = schaduw_fig([(70, 130)], titel='één kleine lichtbron: een scherpe schaduw')
fig_schaduw2 = schaduw_fig([(70, 105), (70, 155)], sx=500, titel='twee lichtbronnen: kernschaduw en bijschaduw')

def verduistering(soort):
    """4 randstralen vanuit de rand van de zon langs de rand van het lichaam ervoor; kernschaduw enkel tot de top van de kegel"""
    W_, H_, Y = 640, 270, 135
    Sx, Sr = 60, 55
    if soort == 'zon':
        B = (330, 20, 'maan', '#9ca3af', '#4b5563'); A = (525, 55, 'aarde', '#93c5fd', '#1d4ed8')
    else:
        B = (330, 40, 'aarde', '#93c5fd', '#1d4ed8'); A = (560, 14, 'maan', '#9ca3af', '#4b5563')
    Bx, Br = B[0], B[1]
    def lijn_y(x0, y0, x1, y1, x):  # y op de rechte door (x0,y0),(x1,y1) bij x
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    XE = W_
    # buitenste randstralen (zon boven -> lichaam boven, zon onder -> lichaam onder): grens kernschaduw
    top_b, bot_b = Y - Br, Y + Br
    apex = Bx + (Bx - Sx) * Br / (Sr - Br)
    xe_k = min(apex, XE)
    kb, ko = lijn_y(Sx, Y - Sr, Bx, top_b, xe_k), lijn_y(Sx, Y + Sr, Bx, bot_b, xe_k)
    # binnenste (gekruiste) randstralen: grens bijschaduw
    bb, bo = lijn_y(Sx, Y + Sr, Bx, top_b, XE), lijn_y(Sx, Y - Sr, Bx, bot_b, XE)
    o = f'<rect width="{W_}" height="{H_}" fill="#0f172a"/>'
    o += f'<path d="M{Bx},{top_b} L{XE},{bb:.1f} L{XE},{bo:.1f} L{Bx},{bot_b}Z" fill="#64748b" opacity="0.55"/>'
    o += f'<path d="M{Bx},{top_b} L{xe_k:.1f},{kb:.1f} L{xe_k:.1f},{ko:.1f} L{Bx},{bot_b}Z" fill="#000" opacity="0.85"/>'
    # de vier randstralen
    for (y0, y1) in [(Y - Sr, top_b), (Y + Sr, bot_b)]:
        o += lijn(Sx, y0, XE, lijn_y(Sx, y0, Bx, y1, XE), '#fbbf24', 1.6)
    for (y0, y1) in [(Y + Sr, top_b), (Y - Sr, bot_b)]:
        o += lijn(Sx, y0, XE, lijn_y(Sx, y0, Bx, y1, XE), '#fde68a', 1.6, '6 4')
    o += f'<circle cx="{Sx}" cy="{Y}" r="{Sr}" fill="#fde047" stroke="#f59e0b" stroke-width="2"/>' + t(Sx, Y + 4, 'zon', '#78350f', 'middle', 14)
    o += f'<circle cx="{A[0]}" cy="{Y}" r="{A[1]}" fill="{A[3]}" stroke="{A[4]}" stroke-width="2"/>' + t(A[0], Y + A[1] + 20, A[2], '#e2e8f0', 'middle', 13)
    o += f'<circle cx="{Bx}" cy="{Y}" r="{Br}" fill="{B[3]}" stroke="{B[4]}" stroke-width="2"/>' + t(Bx, Y - Br - 10, B[2], '#e2e8f0', 'middle', 13)
    if soort == 'zon':
        o += t(450, 30, 'bijschaduw: gedeeltelijke zonsverduistering', '#cbd5e1', 'middle', 12) + lijn(450, 36, 470, 95, '#cbd5e1', 1)
        o += t(430, 238, 'kernschaduw: totale zonsverduistering (enkel in een klein gebied)', '#fef3c7', 'middle', 12) + lijn(450, 226, 472, 138, '#fef3c7', 1)
    else:
        o += t(470, 30, 'bijschaduw van de aarde', '#cbd5e1', 'middle', 12) + t(470, 238, 'maan in de kernschaduw: totale maansverduistering', '#fef3c7', 'middle', 12)
    o += t(320, 262, 'volle lijn: randstralen van de kernschaduw · stippellijn: randstralen van de bijschaduw', '#94a3b8', 'middle', 11, 600)
    return svg(o, W_, H_)
fig_zons = verduistering('zon')
fig_maans = verduistering('maan')

h1_doelen = ['<b>lichtbronnen</b> en <b>donkere lichamen</b> van elkaar onderscheiden;',
             'uitleggen wat een <b>optische middenstof</b> is en er 4 voorbeelden van noteren;',
             'weergeven hoe licht zich <b>voortplant</b> in een optische middenstof, en aangeven dat de stralengang <b>omkeerbaar</b> is;',
             'de drie soorten <b>lichtbundels</b> (divergerend, convergerend en evenwijdig) herkennen en tekenen;',
             'noteren van welke eigenschap van licht <b>schaduwvorming</b> het gevolg is;',
             'uit een tekening van zon, maan en aarde afleiden of er een (gedeeltelijke) <b>zons- of maansverduistering</b> is;',
             'uitleggen waarom er een (gedeeltelijke) zonsverduistering plaatsvindt.']
h1_vk = vk('Je ziet iets als er <b>licht</b> in je <b>oog</b> komt.', 'De <b>zon</b> geeft licht; de <b>maan</b> draait rond de aarde en de aarde rond de zon.', 'Met een <b>lat</b> rechte lijnen tekenen.')

h1_1 = f'''<p>Je ziet iets als er licht van dat voorwerp in je oog komt. Sommige voorwerpen maken zelf licht, andere niet.</p>
<table class="vb"><tr><td>Lichtbron</td><td>een voorwerp dat <b>zelf licht uitstraalt</b></td><td>de zon, een lamp, een kaars, een scherm van een gsm, de sterren</td></tr>
<tr><td>Donker lichaam</td><td>een voorwerp dat <b>zelf geen licht uitstraalt</b></td><td>een boek, een tafel, de maan, je hand, een spiegel</td></tr></table>
<p>Let op: de <b>maan</b> lijkt te schijnen, maar is een donker lichaam. Ze weerkaatst het licht van de zon. Ook een spiegel is een donker lichaam.</p>
{tool('optica.html#z1', 'Sorteer lichtbronnen en donkere lichamen in de tool')}
{denk('denk_1', 'Is het verkeerslicht aan het Rogierplein een lichtbron? En een fietsreflector?', [
  ('Verkeerslicht', 'De lampjes geven zelf licht: een lichtbron (zolang het licht aan is).'),
  ('Fietsreflector', 'Een reflector geeft geen licht van zichzelf. Hij weerkaatst het licht van de koplampen van een auto.'),
], 'Het verkeerslicht is een lichtbron, de reflector is een donker lichaam.')}'''

h1_2 = f'''{kader('Definitie', '<p>Een <b>optische middenstof</b> is een stof waar licht door kan gaan. Voorbeelden: lucht, water, glas, vacuüm (lege ruimte), plexiglas.</p>')}
<p>In een optische middenstof plant licht zich voort in <b>rechte lijnen</b>. Je stelt dat voor met een <b>lichtstraal</b>: een rechte lijn met een pijl die de zin van het licht aangeeft.</p>
<p>De <b>stralengang is omkeerbaar</b>: licht kan dezelfde weg ook in de andere zin afleggen. Zie jij iemand via een spiegel, dan ziet die persoon jou ook.</p>
<h3>Soorten lichtbundels</h3>
{figuur(fig_bundels, 'Een lichtbundel bestaat uit veel lichtstralen.')}
<table class="vb"><tr><td>Divergerend</td><td>de stralen gaan <b>uit elkaar</b></td><td>een lamp, een kaars</td></tr>
<tr><td>Convergerend</td><td>de stralen komen <b>samen</b> in één punt</td><td>licht na een vergrootglas</td></tr>
<tr><td>Evenwijdig</td><td>de stralen blijven even ver van elkaar</td><td>zonlicht op aarde, een laser</td></tr></table>
{kader('Kan je een lichtstraal zien?', '<p>Een lichtstraal zelf zie je <b>niet</b>: je ziet licht pas als het <b>in je oog</b> komt. Een laserstraal door zuivere lucht is van opzij onzichtbaar.</p><p>Zitten er kleine deeltjes in de lucht, zoals <b>mist</b>, <b>waterdruppels</b>, <b>rook</b> of <b>stof</b>, dan weerkaatsen die deeltjes een beetje licht in alle richtingen, ook naar jouw oog. Dan zie je de bundel wel: zonnestralen tussen de bomen van het Zoniënwoud op een mistige ochtend, de koplampen van een auto in de mist, een laserstraal in rook op een concert.</p>')}
{tool('optica.html#z2', 'Bekijk de lichtbundels in de tool')}
{denk('denk_2', 'In een donkere zaal zie je de lichtbundel van een projector als een rechte "kegel" in de lucht hangen. Waarom zie je die bundel, en wat zegt de vorm over hoe licht zich voortplant?', [
  ('Waarom zie je de bundel?', 'Stofdeeltjes in de lucht weerkaatsen een beetje licht naar je oog.'),
  ('Vorm', 'De randen van de bundel zijn rechte lijnen.'),
  ('Soort bundel', 'De bundel wordt breder naar het scherm toe: een divergerende bundel.'),
], 'Licht plant zich rechtlijnig voort; de bundel van de projector is divergerend.')}'''

h1_3 = f'''<p>Licht plant zich voort in rechte lijnen. Staat er een donker lichaam in de weg, dan kan het licht er niet omheen buigen. Achter het voorwerp ontstaat een gebied zonder licht: de <b>schaduw</b>.</p>
{kader('Schaduw', '<p><b>Schaduwvorming</b> is het gevolg van de <b>rechtlijnige voortplanting</b> van licht.</p><p><b>Kernschaduw</b>: het gebied dat van <b>geen enkele</b> lichtbron licht krijgt.<br><b>Bijschaduw</b>: het gebied dat van <b>een deel</b> van de lichtbron(nen) licht krijgt.</p>')}
{figuur(fig_schaduw1, 'Met één kleine lichtbron teken je twee randstralen langs het voorwerp: daartussen ligt de schaduw.')}
{figuur(fig_schaduw2, 'Twee lichtbronnen (of één grote): waar geen licht komt, is kernschaduw; waar licht van één bron komt, bijschaduw.')}
<h3>Zons- en maansverduistering</h3>
{figuur(fig_zons, 'Zonsverduistering: de maan staat tussen zon en aarde. In de kernschaduw van de maan is de zon helemaal bedekt, in de bijschaduw gedeeltelijk.')}
{figuur(fig_maans, 'Maansverduistering: de aarde staat tussen zon en maan. De maan krijgt geen rechtstreeks zonlicht meer.')}
<p><b>Zo teken je de schaduw met vier randstralen</b>: teken vanuit de bovenrand en de onderrand van de zon een rechte langs de rand van de maan (of de aarde) aan <b>dezelfde kant</b>: die twee stralen begrenzen de <b>kernschaduw</b>. Ze komen achter het lichaam samen: de kernschaduw is een kegel die maar tot dat punt reikt. Teken daarna twee <b>gekruiste</b> stralen (bovenrand zon langs de onderkant, onderrand zon langs de bovenkant): tussen de volle en de gekruiste stralen ligt de <b>bijschaduw</b>.</p>
<table class="vb"><tr><td>Zonsverduistering</td><td>volgorde <b>zon – maan – aarde</b></td><td>de maan werpt schaduw op de aarde; totaal in de kernschaduw, gedeeltelijk in de bijschaduw</td></tr>
<tr><td>Maansverduistering</td><td>volgorde <b>zon – aarde – maan</b></td><td>de maan zit in de schaduw van de aarde; totaal als de hele maan in de kernschaduw zit, gedeeltelijk als maar een deel erin zit</td></tr></table>
<p>De zon is een <b>grote</b> lichtbron. Daarom maakt de maan een kleine kernschaduw en een grote bijschaduw op aarde. Wie in de bijschaduw staat, bv. in Brussel als de totale zonsverduistering in Spanje is, ziet maar een deel van de zon verdwijnen: een <b>gedeeltelijke zonsverduistering</b>.</p>
{tool('optica.html#z3', 'Maak schaduwen in de tool')} {tool('optica.html#z4', 'Zons- en maansverduistering in de tool')}
{denk('denk_3', 'Onder een tl-lamp is je schaduw op tafel vaag aan de randen. Onder een klein ledlampje is ze scherp. Hoe komt dat?', [
  ('Kleine lichtbron', 'Licht komt uit bijna één punt: elk punt op tafel krijgt ofwel licht, ofwel geen licht. Scherpe rand.'),
  ('Grote lichtbron', 'Een tl-lamp is lang. Aan de rand van je schaduw krijgt de tafel licht van een deel van de lamp: bijschaduw.'),
], 'Een grote lichtbron geeft naast kernschaduw ook bijschaduw: daardoor is de rand vaag.')}
{denk('denk_4', 'Waarom is er niet elke maand een zonsverduistering, al draait de maan elke maand rond de aarde?', [
  ('Wat is nodig?', 'Zon, maan en aarde moeten precies op één rechte liggen, met de maan in het midden.'),
  ('Wat gebeurt er meestal?', 'De baan van de maan ligt een beetje schuin. Meestal valt de schaduw van de maan boven of onder de aarde.'),
], 'Zon, maan en aarde staan maar zelden precies op één lijn.')}'''

op_schaduw = schaduw_fig([(70, 110)], ox=280, oy=140, r=28, oplossing=False)
opl_schaduw = schaduw_fig([(70, 110)], ox=280, oy=140, r=28, oplossing=True)
op_schaduw2 = schaduw_fig([(70, 90), (70, 170)], ox=280, oy=130, r=28, oplossing=False)
opl_schaduw2 = schaduw_fig([(70, 90), (70, 170)], ox=280, oy=130, r=28, oplossing=True)

h1_oef = f'''{oef('opl_1', 1, 'Lichtbron of donker lichaam?', 'Lichtbron of donker lichaam?<ol class="deelvragen" type="a"><li>een brandende kaars</li><li>de maan</li><li>een fietsreflector</li><li>het scherm van je gsm (aan)</li><li>een spiegel</li><li>een bliksemflits</li></ol>', [
  ('a', 'lichtbron'), ('b', 'donker lichaam: weerkaatst zonlicht'), ('c', 'donker lichaam: weerkaatst licht'), ('d', 'lichtbron'), ('e', 'donker lichaam'), ('f', 'lichtbron')], 'Een lichtbron straalt zelf licht uit.')}
{oef('opl_2', 2, 'Optische middenstoffen', 'Noteer vier optische middenstoffen. Is hout een optische middenstof? Leg uit.', [
  ('Voorbeelden', 'lucht, water, glas, vacuüm (ook plexiglas, olie …)'), ('Hout', 'Nee: licht kan niet door hout.')], 'Een optische middenstof laat licht door.')}
{oef('opl_3', 3, 'Lichtbundels herkennen', 'Welke soort lichtbundel is het?<ol class="deelvragen" type="a"><li>het licht van een straatlamp</li><li>zonlicht dat op de speelplaats valt</li><li>licht dat door een vergrootglas in één punt samenkomt</li><li>de straal van een laserpointer</li></ol>', [
  ('a', 'divergerend'), ('b', 'evenwijdig'), ('c', 'convergerend'), ('d', 'evenwijdig')], 'Uit elkaar: divergerend · samen: convergerend · even ver: evenwijdig.')}
{oef_fig('opl_4', 4, 'Schaduw tekenen', 'Teken met twee randstralen de schaduw van de bal op het scherm. Kleur de schaduw.', op_schaduw, [
  ('Randstralen', 'Teken vanuit de lamp een rechte langs de bovenkant en een langs de onderkant van de bal, tot op het scherm.'),
  ('Schaduw', 'Tussen de twee randstralen komt geen licht op het scherm.')], 'De schaduw ligt op het scherm tussen de twee randstralen.', opl_schaduw)}
{oef_fig('opl_5', 5, 'Kernschaduw en bijschaduw tekenen', 'Twee lampen L1 en L2 schijnen op een bal. Teken de randstralen van elke lamp. Duid de kernschaduw en de bijschaduw aan op het scherm.', op_schaduw2, [
  ('Per lamp', 'Teken voor L1 en voor L2 telkens twee randstralen langs de bal.'),
  ('Kernschaduw', 'Waar geen licht van L1 én geen licht van L2 komt.'), ('Bijschaduw', 'Waar licht van maar één lamp komt.')], 'Kernschaduw in het midden, bijschaduw erboven en eronder.', opl_schaduw2)}
{oef('opl_6', 6, 'Verduistering of niet?', 'Welke verduistering is het, of is er geen?<ol class="deelvragen" type="a"><li>zon – maan – aarde op één lijn</li><li>zon – aarde – maan op één lijn</li><li>de maan staat naast de lijn zon – aarde</li><li>je staat in de bijschaduw van de maan</li></ol>', [
  ('a', 'zonsverduistering'), ('b', 'maansverduistering'), ('c', 'geen verduistering'), ('d', 'gedeeltelijke zonsverduistering')], 'Het middelste hemellichaam werpt de schaduw.')}
{oef('opl_7', 7, 'Redeneren: verduistering', 'Bij een zonsverduistering is het maar op een smalle strook van de aarde volledig donker. Bij een maansverduistering kan iedereen aan de nachtkant van de aarde de verduistering zien. Leg uit.', [
  ('Zonsverduistering', 'De maan is klein: haar kernschaduw op aarde is maar een kleine vlek. Alleen daar is het totaal.'),
  ('Maansverduistering', 'De maan zit zelf in de schaduw van de aarde. Iedereen die de maan ziet, ziet ze donker worden.')], 'Het verschil zit in wie in de schaduw staat: een stukje aarde of de hele maan.')}
{oef('opl_8', 8, 'Een laserstraal zichtbaar maken', 'In de klas schijnt een laserpointer op het bord. Van opzij zie je de straal in de lucht niet. De leerkracht klopt met een krijtwisser of spuit wat water met een plantenspuit: nu zie je de straal wel. Leg uit.', [
  ('Zonder krijtstof', 'Het licht gaat rechtdoor naar het bord. Er komt geen licht van opzij in je oog, dus je ziet de straal niet.'),
  ('Met krijtstof of druppels', 'De kleine deeltjes weerkaatsen een beetje licht in alle richtingen, ook naar je oog.')], 'Je ziet een lichtstraal pas als deeltjes (stof, rook, mist, druppels) licht naar je oog weerkaatsen.')}
{oef('opl_9', 9, 'Juist of fout?', 'Juist of fout? Verbeter de foute uitspraken.<ol class="deelvragen" type="a"><li>De maan is een lichtbron.</li><li>Licht plant zich in een optische middenstof rechtlijnig voort.</li><li>Een grote lichtbron geeft een scherpere schaduw dan een kleine.</li><li>Als jij iemand ziet in een spiegel, kan die jou ook zien.</li></ol>', [
  ('a', 'Fout: de maan is een donker lichaam.'), ('b', 'Juist.'), ('c', 'Fout: een kleine lichtbron geeft een scherpere schaduw (geen bijschaduw).'), ('d', 'Juist: de stralengang is omkeerbaar.')], 'b en d zijn juist.')}'''

h1_samenv = '''<p><b>Lichtbron</b>: straalt zelf licht uit. <b>Donker lichaam</b>: straalt zelf geen licht uit (de maan!).</p>
<p><b>Optische middenstof</b>: laat licht door (lucht, water, glas, vacuüm). Licht plant zich er <b>rechtlijnig</b> voort; de stralengang is <b>omkeerbaar</b>.</p>
<p>Lichtbundels: <b>divergerend</b>, <b>convergerend</b>, <b>evenwijdig</b>.</p>
<p>Een lichtstraal zie je pas als <b>deeltjes</b> (mist, rook, stof, waterdruppels) licht naar je oog weerkaatsen.</p>
<p><b>Schaduw</b> is het gevolg van de rechtlijnige voortplanting. <b>Kernschaduw</b>: geen licht. <b>Bijschaduw</b>: licht van een deel van de bron(nen).</p>
<p><b>Zonsverduistering</b>: zon – maan – aarde. <b>Maansverduistering</b>: zon – aarde – maan.</p>'''

maak('cursus-zien-door-licht.html', 'Fysica 3de jaar · Thema 1 Optische fenomenen · Hoofdstuk 1', 'Zien door licht',
     'Werk dit hoofdstuk samen met de tool <a href="optica.html">Optica</a>. Oefeningen maak je op papier.',
     h1_doelen, h1_vk, [('Lichtbronnen en donkere lichamen', h1_1), ('Voortplanting van licht en lichtbundels', h1_2), ('Schaduwvorming', h1_3)],
     h1_oef, h1_samenv, ('optica.html#z1', 'Oefen verder in de tool Optica'))

# ================================================================ H2 ZIEN DOOR WEERKAATSING
def weerk_fig(i_graden=40, x0=320, y0=180, L=150, labels=True, opl=True, titel=True):
    a = math.radians(i_graden)
    sx, sy = x0 - L*math.sin(a), y0 - L*math.cos(a)
    ex, ey = x0 + L*math.sin(a), y0 - L*math.cos(a)
    o = spiegel_h(x0 - 220, x0 + 220, y0) + lijn(x0, y0 + 20, x0, y0 - 170, GRIJS, 1.5, '6 5')
    o += straal(sx, sy, x0, y0, LICHT, 3)
    if opl:
        o += straal(x0, y0, ex, ey, LICHT, 3)
    o += punt(x0, y0, INK, 4)
    if labels:
        o += t(x0 + 6, y0 - 162, 'normaal', GRIJS, 'start', 12, 600) + t(x0, y0 + 36, 'invalspunt', INK, 'middle', 12, 600)
        o += boog(x0, y0, 45, 90, 90 + i_graden) + t(x0 - 26, y0 - 56, 'i', INK, 'middle', 15)
        o += t(sx - 6, sy - 8, 'invallende straal', '#b45309', 'end', 12, 600)
        if opl:
            o += boog(x0, y0, 45, 90 - i_graden, 90) + t(x0 + 26, y0 - 56, 'r', INK, 'middle', 15)
            o += t(ex + 6, ey - 8, 'weerkaatste straal', '#b45309', 'start', 12, 600)
    return svg(o, 640, 230)
fig_weerk = weerk_fig()

def regdif():
    o = t(160, 22, 'regelmatige weerkaatsing') + t(480, 22, 'diffuse weerkaatsing')
    o += spiegel_h(30, 290, 180)
    for k in range(4):
        x = 90 + k * 40
        o += straal(x - 70, 60, x, 180, LICHT, 2) + straal(x, 180, x + 70, 60, LICHT, 2)
    pts = [(350 + k * 10, 180 + (6 if k % 2 else -4)) for k in range(27)]
    o += '<polyline points="' + ' '.join(f'{x},{y}' for x, y in pts) + '" fill="none" stroke="#334155" stroke-width="3"/>'
    for k, uit in enumerate([(-60, -100), (40, -110), (-10, -120), (90, -70)]):
        x = 410 + k * 40
        o += straal(x - 70, 60, x, 180, LICHT, 2) + straal(x, 180, x + uit[0], 180 + uit[1], LICHT, 2)
    o += t(160, 210, 'glad oppervlak: weerkaatste stralen evenwijdig', GRIJS, 'middle', 12, 600) + t(480, 210, 'ruw oppervlak: weerkaatste stralen alle kanten op', GRIJS, 'middle', 12, 600)
    return svg(o, 640, 225)
fig_regdif = regdif()

def zien_fig():
    o = f'<circle cx="80" cy="60" r="16" fill="#fde047" stroke="#ca8a04" stroke-width="2"/>' + t(80, 30, 'lamp')
    o += '<circle cx="320" cy="170" r="26" fill="#ef4444"/><path d="M320,144 q4,-10 12,-12" stroke="#166534" stroke-width="3" fill="none"/>' + t(320, 215, 'appel (donker lichaam)')
    o += straal(96, 66, 300, 155, LICHT, 3) + straal(340, 155, 540, 80, LICHT, 3) + oog(560, 75, 200)
    o += t(560, 110, 'oog') + t(180, 140, '1. licht van de lamp', '#b45309', 'middle', 12, 600) + t(450, 150, '2. weerkaatst naar je oog', '#b45309', 'middle', 12, 600)
    return svg(o, 640, 230)
fig_zien = zien_fig()

def potlood_fig(A, B, E, mx=340, y1=30, y2=250, opl=True, ruitjes=True, w=640, h=270):
    o = ruit(w, h) if ruitjes else ''
    o += spiegel_v(mx, y1, y2) + potlood(*A, *B) + t(A[0] - 10, A[1] - 6, 'A', INK, 'end', 13) + t(B[0] - 10, B[1] + 14, 'B', INK, 'end', 13) + oog(*E, 0) + t(E[0], E[1] + 26, 'oog', INK, 'middle', 12)
    if opl:
        Ab, Bb = (2*mx - A[0], A[1]), (2*mx - B[0], B[1])
        o += lijn(A[0], A[1], Ab[0], Ab[1], '#94a3b8', 1, '2 4') + lijn(B[0], B[1], Bb[0], Bb[1], '#94a3b8', 1, '2 4')
        o += potlood(*Ab, *Bb, '#d6b98a', '6 4') + t(Ab[0] + 10, Ab[1] - 6, "A'", INK, 'start', 13) + t(Bb[0] + 10, Bb[1] + 14, "B'", INK, 'start', 13)
        for P, Pb in [(A, Ab), (B, Bb)]:
            tt = (mx - Pb[0]) / (E[0] - Pb[0]); Iy = Pb[1] + tt * (E[1] - Pb[1])
            o += straal(P[0], P[1], mx, Iy, LICHT, 2) + straal(mx, Iy, E[0] + 12, E[1], LICHT, 2) + lijn(mx, Iy, Pb[0], Pb[1], LICHT, 1.5, '5 4')
    return svg(o, w, h)
fig_potlood = potlood_fig((240, 90), (180, 190), (120, 230))

def gezicht_fig(O, mx=420, y1=90, y2=170, punten=(), opl=True, w=640, h=260):
    o = ruit(w, h) + spiegel_v(mx, y1, y2)
    if opl:
        Ob = (2*mx - O[0], O[1])
        ext = []
        for my in (y1, y2):
            tt = (mx - 0) / (Ob[0] - mx)  # tot x = 0
            ye = my + (my - Ob[1]) * (mx - 0) / (Ob[0] - mx)
            ext.append(ye)
            o += lijn(Ob[0], Ob[1], mx, my, GRIJS, 1.2, '5 4') + lijn(mx, my, 0, ye, '#16a34a', 1.8)
            o += straal(mx, my, O[0] + 10, O[1], LICHT, 2)
        o += f'<path d="M{mx},{y1} L0,{ext[0]:.1f} L0,{ext[1]:.1f} L{mx},{y2}Z" fill="#16a34a" opacity="0.12"/>'
        o += punt(*Ob, GRIJS, 4) + t(Ob[0] + 8, Ob[1] - 8, "O'", GRIJS, 'start', 13)
    o += oog(*O, 0) + t(O[0], O[1] + 26, 'O', INK, 'middle', 13)
    for naam, (x, y) in punten:
        o += f'<path d="M{x-5},{y-5} L{x+5},{y+5} M{x-5},{y+5} L{x+5},{y-5}" stroke="{ROOD}" stroke-width="2.5"/>' + t(x + 8, y - 6, naam, ROOD, 'start', 13)
    return svg(o, w, h)
fig_gezicht = gezicht_fig((300, 200))

h2_doelen = ['aantonen wanneer je <b>lichtbronnen</b> en wanneer je <b>donkere lichamen</b> kan zien (absorptie en/of weerkaatsing);',
             'de begrippen <b>invalshoek</b>, <b>weerkaatsingshoek</b>, <b>invalspunt</b> en <b>normaal</b> omschrijven en aanduiden op een tekening;',
             'omschrijven aan welke <b>wetten</b> de weerkaatsing van licht voldoet;',
             'de <b>stralengang</b> tekenen bij weerkaatsing op een vlakke spiegel;',
             'het verschil tussen <b>regelmatige</b> en <b>diffuse weerkaatsing</b> in woorden noteren en tekenen ("weerkaatste stralen");',
             'aan een voorwerp uitleggen hoe je ziet dat het een regelmatig of een onregelmatig oppervlak heeft;',
             'de vijf <b>kenmerken van het beeld</b> bij een vlakke spiegel weergeven;',
             'het <b>beeld van een voorwerp</b> (een potlood) door een spiegel <b>construeren</b>;',
             'het <b>gezichtsveld</b> van een spiegel tekenen met het stappenplan, en het belang ervan met voorbeelden aangeven.']
h2_vk = vk('Licht plant zich <b>rechtlijnig</b> voort en de stralengang is <b>omkeerbaar</b> (hoofdstuk 1).', '<b>Lichtbron</b> en <b>donker lichaam</b> (hoofdstuk 1).', 'Met een <b>geodriehoek</b> een loodlijn tekenen en een hoek meten en tekenen.')

h2_1 = f'''{figuur(fig_zien, 'Je ziet een donker lichaam doordat het licht van een lichtbron erop weerkaatst naar je oog.')}
<table class="vb"><tr><td>Lichtbron zien</td><td>het licht gaat van de lichtbron <b>rechtstreeks</b> naar je oog</td></tr>
<tr><td>Donker lichaam zien</td><td>het licht gaat van een lichtbron naar het voorwerp, wordt daar <b>weerkaatst</b> en komt zo in je oog</td></tr></table>
<p>Een voorwerp <b>absorbeert</b> een deel van het licht (neemt het op) en <b>weerkaatst</b> de rest. Een zwart voorwerp absorbeert bijna al het licht: daarom zie je het als zwart. Een wit voorwerp weerkaatst bijna al het licht. In een kamer zonder licht zie je geen donkere lichamen.</p>
{tool('optica.html#w0', 'Bekijk in de tool hoe je lichamen ziet')}
{denk('denk_1', 'Hamza zegt: "Ik zie de stoel omdat er licht uit mijn ogen naar de stoel gaat." Klopt dat?', [
  ('Waar komt het licht vandaan?', 'Uit een lichtbron: de lamp of de zon. Je ogen geven geen licht.'),
  ('Wat doet de stoel?', 'De stoel weerkaatst een deel van dat licht.'),
  ('Wat doet je oog?', 'Je oog vangt het weerkaatste licht op.'),
], 'Nee: licht gaat van de lichtbron naar de stoel en wordt weerkaatst naar je oog.')}'''

h2_2 = f'''{figuur(fig_weerk, 'Weerkaatsing op een vlakke spiegel: de invalshoek i is even groot als de weerkaatsingshoek r.')}
<table class="vb"><tr><td>Invalspunt</td><td>het punt waar de invallende straal de spiegel raakt</td></tr>
<tr><td>Normaal</td><td>de loodlijn op de spiegel in het invalspunt (stippellijn)</td></tr>
<tr><td>Invalshoek i</td><td>de hoek tussen de <b>invallende straal</b> en de <b>normaal</b></td></tr>
<tr><td>Weerkaatsingshoek r</td><td>de hoek tussen de <b>weerkaatste straal</b> en de <b>normaal</b></td></tr></table>
{kader('Wetten van de weerkaatsing', '<p>1. De <b>invalshoek</b> is even groot als de <b>weerkaatsingshoek</b>: i = r.<br>2. De invallende straal, de normaal en de weerkaatste straal liggen in <b>één vlak</b>.</p>')}
<p>Let op: je meet de hoeken altijd ten opzichte van de <b>normaal</b>, niet ten opzichte van de spiegel. Maakt een straal 30° met de spiegel, dan is de invalshoek 90° − 30° = 60°.</p>
<h3>Stappenplan: de weerkaatste straal tekenen</h3>
<ol><li>Duid het <b>invalspunt</b> aan.</li><li>Teken met je geodriehoek de <b>normaal</b> (stippellijn).</li><li>Meet de <b>invalshoek</b> i.</li><li>Teken aan de andere kant van de normaal de <b>weerkaatste straal</b> met r = i. Vergeet de pijl niet.</li></ol>
{tool('optica.html#s1', 'Oefen weerkaatsing in de tool')} {tool('optica.html#s9', 'Het vlak van inval in 3D')}
{denk('denk_2', 'Een lichtstraal valt loodrecht op een spiegel. Hoe groot zijn de invalshoek en de weerkaatsingshoek? Waar gaat de straal naartoe?', [
  ('Invalshoek', 'De straal valt langs de normaal: i = 0°.'), ('Weerkaatsingshoek', 'r = i = 0°.'), ('Richting', 'De straal gaat langs dezelfde weg terug.')], 'i = r = 0°: de straal keert op zichzelf terug.')}'''

h2_3 = f'''{figuur(fig_regdif, 'Links een glad oppervlak, rechts een ruw oppervlak. Elke straal volgt i = r, maar de normaal staat overal anders.')}
<table class="vb"><tr><td>Regelmatige weerkaatsing</td><td>op een <b>glad</b> oppervlak: evenwijdige invallende stralen geven <b>evenwijdige weerkaatste stralen</b></td><td>spiegel, rustig water, glanzende metalen deur</td></tr>
<tr><td>Diffuse weerkaatsing</td><td>op een <b>ruw</b> oppervlak: evenwijdige invallende stralen geven <b>weerkaatste stralen in alle richtingen</b></td><td>papier, muur, kleding, de maan</td></tr></table>
<p>Schijn je met een laserpointer op een <b>spiegel</b>, dan zie je op de spiegel zelf <b>geen lichtvlek</b>: al het licht wordt in één richting weerkaatst en komt alleen in je oog als je precies in die weerkaatste bundel kijkt. Schijn je op een <b>wit blad</b>, dan zie je de lichtvlek <b>vanuit elke plaats</b> in de klas: het blad weerkaatst het licht diffuus, in alle richtingen. Een heel glad, effen oppervlak zie je dus zelf bijna niet; je ziet er vooral de voorwerpen in die erin weerspiegelen.</p>
<p>Hoe zie je het verschil? In een <b>regelmatig</b> oppervlak zie je een <b>spiegelbeeld</b> van andere voorwerpen. Een <b>diffuus</b> oppervlak zie je zelf, vanuit elke richting, maar je ziet er geen spiegelbeeld in. Dankzij diffuse weerkaatsing kan iedereen in de klas het bord lezen.</p>
{tool('optica.html#s2', 'Regelmatige weerkaatsing in de tool')} {tool('optica.html#s3', 'Diffuse weerkaatsing in de tool')}
{denk('denk_3', 'Een nat wegdek ’s nachts blinkt en verblindt je, een droog wegdek niet. Leg uit met regelmatige en diffuse weerkaatsing.', [
  ('Droog wegdek', 'Het asfalt is ruw: diffuse weerkaatsing. De weerkaatste stralen gaan alle kanten op, dus maar weinig licht van de koplampen komt in je oog.'),
  ('Nat wegdek', 'Een laagje water maakt het oppervlak glad: regelmatige weerkaatsing. De weerkaatste stralen van tegenliggers gaan samen in één richting, soms recht in je oog.'),
], 'Nat: regelmatige weerkaatsing, alle weerkaatste stralen evenwijdig. Droog: diffuse weerkaatsing.')}'''

h2_4 = f'''<p>Kijk je in een spiegel, dan lijkt het alsof er een voorwerp <b>achter</b> de spiegel staat. Dat noem je het <b>beeld</b>. De weerkaatste stralen komen niet echt van achter de spiegel: je hersenen verlengen ze in een rechte lijn naar achter.</p>
{kader('Kenmerken van het beeld bij een vlakke spiegel', '<p>1. Het beeld is <b>virtueel</b> (schijnbaar): je kan het niet opvangen op een scherm.<br>2. Het beeld staat <b>rechtop</b>.<br>3. Het beeld is <b>even groot</b> als het voorwerp.<br>4. Het beeld staat <b>even ver achter</b> de spiegel als het voorwerp ervoor staat.<br>5. Het beeld is <b>spiegelbeeldig</b>: links en rechts zijn omgewisseld.</p>')}
<h3>Stappenplan: het beeld van een potlood construeren</h3>
{figuur(fig_potlood, "Beeld A'B' van het potlood AB. De weerkaatste stralen lijken uit het beeld te komen (stippellijnen achter de spiegel).")}
<ol><li>Teken vanuit de punt <b>A</b> een loodlijn op de spiegel en verleng ze achter de spiegel. Zet <b>A'</b> even ver achter de spiegel als A ervoor staat (tel de hokjes).</li>
<li>Doe hetzelfde voor het einde <b>B</b>: zo vind je <b>B'</b>.</li>
<li>Verbind A' en B' met een <b>stippellijn</b>: dat is het beeld (virtueel).</li>
<li>Teken nu de lichtstralen naar het oog: trek een rechte van A' naar het oog. Waar ze de spiegel snijdt, ligt het invalspunt. Teken de straal van A naar dat invalspunt en van daar naar het oog. Achter de spiegel teken je het verlengde in stippellijn.</li>
<li>Herhaal stap 4 voor B.</li></ol>
{tool('optica.html#s12', 'Construeer het beeld van het potlood in de tool')}
{denk('denk_4', 'Op een ambulance staat AMBULANCE in spiegelschrift. Waarom?', [
  ('Wie leest het?', 'Een chauffeur vóór de ambulance, in zijn binnenspiegel.'), ('Kenmerk 5', 'Een spiegel wisselt links en rechts om.'), ('Gevolg', 'Het spiegelschrift wordt in de spiegel weer gewoon leesbaar.')], 'In de achteruitkijkspiegel lees je AMBULANCE gewoon.')}'''

h2_5 = f'''<p>In een spiegel zie je maar een deel van de ruimte. Dat deel noem je het <b>gezichtsveld</b> van de spiegel. Het hangt af van <b>waar je oog staat</b> en van <b>hoe groot</b> de spiegel is.</p>
{figuur(fig_gezicht, "Gezichtsveld (groen) vanuit oogpunt O. O' is het spiegelbeeld van het oog.")}
<h3>Stappenplan: het gezichtsveld tekenen</h3>
<ol><li>Zoek het <b>spiegelbeeld O'</b> van het oog: loodlijn op de spiegel, even ver erachter.</li>
<li>Teken vanuit O' twee rechten door de <b>twee uiteinden</b> van de spiegel.</li>
<li>Verleng die rechten vóór de spiegel. Het gebied tussen die twee rechten (vóór de spiegel) is het <b>gezichtsveld</b>: kleur het.</li>
<li>De echte weerkaatste stralen lopen van de uiteinden van de spiegel naar het oog O.</li></ol>
<p>Een voorwerp in het gezichtsveld zie je in de spiegel; een voorwerp erbuiten niet. Hoe <b>dichter</b> je bij de spiegel staat of hoe <b>groter</b> de spiegel, hoe <b>groter</b> het gezichtsveld.</p>
<p><b>Belang in het dagelijks leven</b>: de binnenspiegel en de zijspiegels van een auto of een bus van de MIVB moeten de weg achter je tonen. Wat buiten het gezichtsveld valt, is de <b>dode hoek</b>: daarom moet je als fietser oppassen naast een vrachtwagen. Ook de spiegel bij de kapper, in een winkel of aan een uitrit werkt zo.</p>
{tool('optica.html#s13', 'Teken het gezichtsveld in de tool')}
{denk('denk_5', 'Je wil je volledig zien in een spiegel aan de muur. Moet de spiegel even groot zijn als jij?', [
  ('Kruin', 'Licht van je kruin moet via de spiegel in je oog komen. Het invalspunt ligt halverwege tussen je kruin en je oog (in hoogte).'),
  ('Voeten', 'Licht van je voeten komt in je oog via een punt halverwege tussen je oog en je voeten.'),
  ('Samen', 'De spiegel moet dus van halverwege kruin–oog tot halverwege oog–voeten lopen: de helft van je lengte.'),
], 'Nee: een spiegel van de helft van je lengte is genoeg, als hij op de juiste hoogte hangt.')}'''

op_w1, opl_w1 = weerk_fig(35, labels=False, opl=False), weerk_fig(35, labels=True, opl=True)
op_p1, opl_p1 = potlood_fig((240, 80), (240, 190), (110, 230), opl=False), potlood_fig((240, 80), (240, 190), (110, 230))
op_p2, opl_p2 = potlood_fig((260, 120), (160, 180), (140, 60), opl=False), potlood_fig((260, 120), (160, 180), (140, 60))
op_p3, opl_p3 = potlood_fig((200, 70), (280, 170), (100, 200), opl=False), potlood_fig((200, 70), (280, 170), (100, 200))
PTS = (('P', (100, 60)), ('Q', (160, 220)), ('R', (60, 140)))
op_g1, opl_g1 = gezicht_fig((300, 200), punten=PTS, opl=False), gezicht_fig((300, 200), punten=PTS)
PTS2 = (('P', (120, 80)), ('Q', (220, 230)), ('R', (80, 200)))
op_g2, opl_g2 = gezicht_fig((360, 130), y1=100, y2=160, punten=PTS2, opl=False), gezicht_fig((360, 130), y1=100, y2=160, punten=PTS2)

def zichtbaar(O, mx, y1, y2, P):
    Ob = (2*mx - O[0], O[1]); tt = (mx - P[0]) / (Ob[0] - P[0]); Iy = P[1] + tt * (Ob[1] - P[1])
    return y1 <= Iy <= y2
def zin_pts(O, mx, y1, y2, pts):
    z = [n for n, P in pts if zichtbaar(O, mx, y1, y2, P)]; nz = [n for n, P in pts if not zichtbaar(O, mx, y1, y2, P)]
    return f"zichtbaar in de spiegel: {', '.join(z) or 'geen'} · niet zichtbaar: {', '.join(nz) or 'geen'}"

h2_oef = f'''{oef_fig('opl_1', 1, 'Weerkaatste straal tekenen', 'Teken de normaal in het invalspunt, meet de invalshoek en teken de weerkaatste straal. Duid i en r aan.', op_w1, [
  ('Normaal', 'loodlijn op de spiegel in het invalspunt'), ('Invalshoek', 'i = 35°'), ('Weerkaatste straal', 'aan de andere kant van de normaal, r = 35°')], 'i = r = 35°', opl_w1)}
{oef('opl_2', 2, 'Hoeken berekenen', 'Bereken telkens de invalshoek en de weerkaatsingshoek.<ol class="deelvragen" type="a"><li>De invallende straal maakt 25° met de spiegel.</li><li>De invallende en de weerkaatste straal maken samen een hoek van 80°.</li><li>De weerkaatste straal maakt 50° met de spiegel.</li></ol>', [
  ('a', 'i = 90° − 25° = 65°, r = 65°'), ('b', 'i + r = 80° en i = r, dus i = r = 40°'), ('c', 'r = 90° − 50° = 40°, i = 40°')], 'Meet altijd t.o.v. de normaal.')}
{oef('opl_3', 3, 'Regelmatig of diffuus?', 'Regelmatige of diffuse weerkaatsing? Leg uit met het woord "weerkaatste stralen".<ol class="deelvragen" type="a"><li>een blad papier</li><li>het water van de vijver in het Warandepark als het niet waait</li><li>een glanzende metalen lift in het Atomium</li><li>een witte muur</li></ol>', [
  ('a', 'diffuus: ruw oppervlak, weerkaatste stralen in alle richtingen'), ('b', 'regelmatig: glad oppervlak, weerkaatste stralen evenwijdig; je ziet een spiegelbeeld'),
  ('c', 'regelmatig: je ziet er je spiegelbeeld in'), ('d', 'diffuus: geen spiegelbeeld')], 'Zie je een spiegelbeeld? Dan is het regelmatig.')}
{oef('opl_4', 4, 'Laser op spiegel of papier', 'Je schijnt met een laserpointer op een spiegel en daarna op een wit blad papier. Je klasgenoten zitten verspreid in de klas. Wie ziet de lichtvlek? Leg uit met regelmatige en diffuse weerkaatsing.', [
  ('Spiegel', 'Regelmatige weerkaatsing: de weerkaatste stralen gaan samen in één richting. Alleen wie precies in die richting zit, krijgt licht in zijn oog (pas op: nooit een laser in je oog!). De anderen zien op de spiegel geen vlek.'),
  ('Wit blad', 'Diffuse weerkaatsing: de weerkaatste stralen gaan in alle richtingen. Iedereen ziet de vlek.')], 'Op een glad oppervlak zie je de lichtvlek niet, op een ruw oppervlak zie je ze vanuit elke richting.')}
{oef('opl_4', 4, 'Kenmerken van het beeld', 'Sara staat 1,5 m voor een vlakke spiegel. Ze heft haar rechterhand op.<ol class="deelvragen" type="a"><li>Hoe ver staat haar beeld van de spiegel? En van Sara?</li><li>Welke hand heft het beeld op?</li><li>Sara stapt 0,5 m naar de spiegel toe. Hoe ver staat ze nu van haar beeld?</li><li>Kan je het beeld opvangen op een scherm? Waarom niet?</li></ol>', [
  ('a', '1,5 m achter de spiegel; 3,0 m van Sara'), ('b', 'de linkerhand (spiegelbeeldig)'), ('c', 'Sara staat 1,0 m van de spiegel, het beeld 1,0 m erachter: 2,0 m'), ('d', 'Nee: het beeld is virtueel, er komt geen licht van achter de spiegel.')], 'Even ver achter de spiegel, even groot, rechtop, virtueel, spiegelbeeldig.')}
{oef_fig('opl_5', 5, 'Beeld van een potlood (rechtop)', "Construeer het beeld A'B' van het potlood. Teken vanuit A en vanuit B de lichtstraal die via de spiegel in het oog komt.", op_p1, [
  ("A' en B'", 'loodlijn op de spiegel, even veel hokjes erachter'), ('Beeld', "A'B' in stippellijn: even groot, rechtop"), ('Stralen', "rechte van A' (en B') naar het oog: invalspunt op de spiegel; straal van A naar het invalspunt en verder naar het oog")], 'Het beeld staat even ver achter de spiegel als het potlood ervoor.', opl_p1)}
{oef_fig('opl_6', 6, 'Beeld van een schuin potlood', "Construeer het beeld A'B' van het schuine potlood en teken de stralen vanuit A en B naar het oog.", op_p2, [
  ("A'", 'loodlijn vanuit A, even ver achter de spiegel'), ("B'", 'loodlijn vanuit B, even ver achter de spiegel'), ('Stand', 'het beeld helt de andere kant op: spiegelbeeldig')], "A'B' is even lang als AB en helt in spiegelbeeld.", opl_p2)}
{oef_fig('opl_7', 7, 'Nog een potlood', "Construeer het beeld A'B'. Teken de stralen vanuit A en B naar het oog.", op_p3, [
  ('Werkwijze', 'zoals oefening 5: eerst de beeldpunten, dan de stralen via het beeld naar het oog')], 'Elke straal naar het oog lijkt te komen uit het beeldpunt.', opl_p3)}
{oef_fig('opl_8', 8, 'Gezichtsveld tekenen', 'Teken het gezichtsveld van de spiegel vanuit oogpunt O. Welke punten (P, Q, R) ziet het oog in de spiegel?', op_g1, [
  ("O'", 'spiegelbeeld van O, even ver achter de spiegel'), ('Randen', "rechten van O' door de uiteinden van de spiegel, verlengd vóór de spiegel"), ('Punten', zin_pts((300, 200), 420, 90, 170, PTS))], 'Alleen punten in het gezichtsveld zie je in de spiegel.', opl_g1)}
{oef_fig('opl_9', 9, 'Gezichtsveld bij een kleinere spiegel', 'Teken het gezichtsveld vanuit O. Welke punten ziet het oog in de spiegel?', op_g2, [
  ("O'", 'spiegelbeeld van O'), ('Randen', "rechten van O' door de uiteinden"), ('Punten', zin_pts((360, 130), 420, 100, 160, PTS2))], 'Een kleinere spiegel geeft een kleiner gezichtsveld.', opl_g2)}
{oef('opl_10', 10, 'Redeneren: gezichtsveld', 'Leg uit.<ol class="deelvragen" type="a"><li>Wat gebeurt er met het gezichtsveld als je dichter bij de spiegel gaat staan?</li><li>Een chauffeur van een vrachtwagen ziet een fietser naast zich niet. Waarom?</li><li>Waarom hangt er aan een uitrit van een parking soms een spiegel?</li></ol>', [
  ('a', "Het gezichtsveld wordt groter: O' komt dichter bij de spiegel, de randen gaan verder open."), ('b', 'De fietser zit in de dode hoek: buiten het gezichtsveld van de spiegels.'), ('c', 'Met de spiegel komt de straat (die je zelf niet ziet) in je gezichtsveld.')], 'Wat buiten het gezichtsveld ligt, zie je niet in de spiegel.')}
{oef('opl_11', 11, 'Twee spiegels', 'Twee vlakke spiegels staan loodrecht op elkaar (een hoek van 90°). Een lichtstraal valt in op de eerste spiegel met een invalshoek van 30°. Bereken de invalshoek op de tweede spiegel. Wat merk je op over de richting van de straal die terugkomt?', [
  ('Spiegel 1', 'i = r = 30°: de weerkaatste straal maakt 60° met spiegel 1.'), ('Spiegel 2', 'In de driehoek met de hoek van 90°: de straal maakt 30° met spiegel 2, dus i = 60° en r = 60°.'), ('Richting', 'De straal gaat evenwijdig terug met de invallende straal, in tegengestelde zin.')], 'Twee spiegels onder 90° sturen licht terug naar waar het vandaan kwam (zoals een fietsreflector).')}'''

h2_samenv = '''<p>Een <b>lichtbron</b> zie je rechtstreeks; een <b>donker lichaam</b> zie je door weerkaatst licht.</p>
<p><b>Normaal</b>: loodlijn in het invalspunt. <b>Wetten</b>: i = r; invallende straal, normaal en weerkaatste straal in één vlak.</p>
<p><b>Regelmatig</b>: glad oppervlak, weerkaatste stralen evenwijdig; een lichtvlek op een spiegel zie je niet. <b>Diffuus</b>: ruw oppervlak, weerkaatste stralen in alle richtingen; de lichtvlek zie je overal.</p>
<p><b>Beeld bij een vlakke spiegel</b>: virtueel, rechtop, even groot, even ver achter de spiegel, spiegelbeeldig. Construeren: loodlijn, even ver erachter.</p>
<p><b>Gezichtsveld</b>: spiegelbeeld O' van het oog, rechten door de uiteinden van de spiegel.</p>'''

maak('cursus-weerkaatsing.html', 'Fysica 3de jaar · Thema 1 Optische fenomenen · Hoofdstuk 2', 'Zien door weerkaatsing',
     'Werk dit hoofdstuk samen met de tool <a href="optica.html">Optica</a>. Oefeningen maak je op papier.',
     h2_doelen, h2_vk, [('Lichamen zien', h2_1), ('Weerkaatsing op een vlakke spiegel', h2_2), ('Regelmatige en diffuse weerkaatsing', h2_3), ('Het beeld bij een vlakke spiegel', h2_4), ('Gezichtsveld', h2_5)],
     h2_oef, h2_samenv, ('optica.html#s12', 'Oefen verder: potlood en gezichtsveld in de tool'))

# ================================================================ H3 LICHTBREKING
N_WATER, N_GLAS = 1.33, 1.5
def breking_fig(i_graden, van='lucht', naar='water', n1=1.0, n2=N_WATER, opl=True, labels=True, w=640, h=240, x0=None):
    x0 = x0 or w / 2; y0 = h / 2
    boven_dicht = n1 > n2  # licht komt van boven
    kleur_b = WATER if n1 > 1 else '#ffffff'; kleur_o = WATER if n2 > 1 else '#ffffff'
    if n1 > 1.4: kleur_b = GLAS
    if n2 > 1.4: kleur_o = '#bae6fd'
    o = f'<rect x="0" y="0" width="{w}" height="{y0}" fill="{kleur_b}"/><rect x="0" y="{y0}" width="{w}" height="{h-y0}" fill="{kleur_o}"/>'
    o += lijn(0, y0, w, y0, '#334155', 2) + lijn(x0, 8, x0, h - 8, GRIJS, 1.5, '6 5')
    o += t(12, 22, van, GRIJS, 'start', 13) + t(12, h - 12, naar, GRIJS, 'start', 13)
    a = math.radians(i_graden); L = 105
    sx, sy = x0 - L*math.sin(a), y0 - L*math.cos(a)
    o += straal(sx, sy, x0, y0, LICHT, 3)
    sr = n1 * math.sin(a) / n2
    if opl:
        if sr < 1:
            r = math.asin(sr); ex, ey = x0 + L*math.sin(r), y0 + L*math.cos(r)
            o += straal(x0, y0, ex, ey, LICHT, 3)
            if labels:
                o += boog(x0, y0, 40, 90, 90 + i_graden) + t(x0 - 22, y0 - 48, 'i', INK, 'middle', 15)
                o += boog(x0, y0, 40, 270, 270 + math.degrees(r)) + t(x0 + 16, y0 + 56, 'r', INK, 'middle', 15)
        else:
            ex, ey = x0 + L*math.sin(a), y0 - L*math.cos(a)
            o += straal(x0, y0, ex, ey, LICHT, 3)
    elif labels:
        o += boog(x0, y0, 40, 90, 90 + i_graden) + t(x0 - 22, y0 - 48, 'i', INK, 'middle', 15)
    o += punt(x0, y0, INK, 3.5)
    return svg(o, w, h)
def twee_breking():
    a = breking_fig(50, 'lucht (optisch ijl)', 'water (optisch dicht)', 1.0, N_WATER, w=310, h=240)
    b = breking_fig(35, 'water (optisch dicht)', 'lucht (optisch ijl)', N_WATER, 1.0, w=310, h=240)
    a = a.replace('<svg viewBox="0 0 310 240" width="310" xmlns="http://www.w3.org/2000/svg">', '<g>').replace('</svg>', '</g>')
    b = b.replace('<svg viewBox="0 0 310 240" width="310" xmlns="http://www.w3.org/2000/svg">', '<g transform="translate(330,0)">').replace('</svg>', '</g>')
    return svg(a + b + t(155, 258, 'naar de normaal toe: r &lt; i', INK, 'middle', 13) + t(485, 258, 'van de normaal weg: r &gt; i', INK, 'middle', 13), 640, 268)
fig_breking = twee_breking()

def verhoging_fig(depth=120, xe=200, stap=4, ruitjes=False, W=640, H=385, pupil=44, oog=3.2):
    """tekening zoals in de tool: voorwerp met punt V, twee stralen, normalen, gebroken stralen, verlengden, V'"""
    n, waterY, ox, eyeH, BW, BH = 1.33, 192, 140, 150, 110, 22   # pupil klein: beide stralen gaan echt het oog in
    C1, C2 = '#2233dd', '#dd1a1a'
    crit = math.asin(1 / n)
    def solve(xe_):
        lo, hi = 1e-4, depth * math.tan(crit) - 1e-4
        for _ in range(70):
            mid = (lo + hi) / 2; i = math.atan(mid / depth); r = math.asin(min(n * math.sin(i), 1 - 1e-9))
            if mid + eyeH * math.tan(r) - xe_ < 0: lo = mid
            else: hi = mid
        return (lo + hi) / 2
    def hoek(x):
        i = math.atan(x / depth); return i, math.asin(min(n * math.sin(i), 1 - 1e-9))
    x1, x2 = solve(xe - pupil / 2), solve(xe + pupil / 2)
    (i1, r1), (i2, r2) = hoek(x1), hoek(x2)
    delta = (x2 - x1) / (math.tan(r1) - math.tan(r2))
    ax, ay = ox + x1 + math.tan(r1) * delta, waterY - delta
    o = f'<rect x="0" y="0" width="{W}" height="{waterY}" fill="#e6eff9"/><rect x="0" y="{waterY}" width="{W}" height="{H-waterY}" fill="#cfe3f6"/>'
    if ruitjes: o += ruit(W, H)
    o += lijn(0, waterY, W, waterY, '#8bbeff', 2.5) + t(W - 12, waterY - 10, 'lucht', GRIJS, 'end', 13) + t(W - 12, waterY + 22, 'water', GRIJS, 'end', 13)
    Vx, Vy = ox, waterY + depth
    def blokje(x, y, geest=False, label=''):
        st = 'fill="#2ea3c0" fill-opacity="0.3" stroke="#1d6e86" stroke-dasharray="6 4" stroke-width="1.6"' if geest else 'fill="#2ea3c0" stroke="#1d6e86" stroke-width="1.2"'
        r = f'<rect x="{x:.1f}" y="{y+3:.1f}" width="{BW}" height="{BH}" {st}/>' + punt(x, y, '#1a2430', 3.6) + t(x - 7, y + 5, "V'" if geest else 'V', '#1a2430', 'end', 15)
        if label: r += t(x + BW / 2, y + BH + (18 if geest else 40), label, '#1d4f61' if geest else INK, 'middle', 11, 600)
        return r
    o += blokje(Vx, Vy, False, 'echt voorwerp' if stap >= 4 else '')
    o += lijn(Vx, waterY, Vx, Vy, '#1a2430', 1, '3 4')
    X1, X2 = (ox + x1, waterY), (ox + x2, waterY)
    o += straal(Vx, Vy, *X1, C1, 2.3) + straal(Vx, Vy, *X2, C2, 2.3)
    if stap >= 1:
        for X in (X1, X2): o += lijn(X[0], waterY - 60, X[0], waterY + 60, GRIJS, 1.3, '6 5')
    L = eyeH - 6   # de gebroken stralen eindigen in het oog
    o1 = (X1[0] + math.tan(r1) * L, waterY - L); o2 = (X2[0] + math.tan(r2) * L, waterY - L)
    if stap >= 2: o += straal(*X1, *o1, C1, 2.3) + straal(*X2, *o2, C2, 2.3)
    if stap >= 3: o += lijn(*X1, ax, ay, C1, 1.8, '6 5') + lijn(*X2, ax, ay, C2, 1.8, '6 5')
    if stap >= 4: o += blokje(ax, ay, True, 'schijnbaar voorwerp')
    elif stap == 3: o += punt(ax, ay, '#1a2430', 3.6) + t(ax - 7, ay + 5, "V'", '#1a2430', 'end', 15)
    Ex, Ey = ox + xe, waterY - eyeH
    hoekoog = math.degrees(math.atan2(Ey - (o1[1] + o2[1]) / 2, Ex - (o1[0] + o2[0]) / 2)) + 180
    o += f'<g transform="translate({Ex:.1f},{Ey:.1f}) scale({oog}) rotate({hoekoog:.1f})"><path d="M-14,0 Q0,-10 14,0 Q0,10 -14,0Z" fill="#0c1119" stroke="#e9eef5" stroke-width="1.5"/><circle cx="4" cy="0" r="4" fill="#00d9b0"/></g>' + t(Ex + 46, Ey + 8, 'oog', GRIJS, 'middle', 11)
    return svg(o, W, H)
fig_munt = verhoging_fig()

def totaal_fig():
    w, h, yo = 640, 250, 110
    o = f'<rect x="0" y="{yo}" width="{w}" height="{h-yo}" fill="{WATER}"/>' + lijn(0, yo, w, yo, '#334155', 2)
    o += t(12, 24, 'lucht (ijl)', GRIJS, 'start', 13) + t(12, h - 10, 'water (dicht)', GRIJS, 'start', 13)
    g = math.degrees(math.asin(1 / N_WATER))
    for x0, i, kleur, label in [(150, 30, '#f59e0b', 'i < g: breking'), (340, g, '#a855f7', f'i = g ≈ {g:.0f}°'), (520, 62, ROOD, 'i > g: totale weerkaatsing')]:
        a = math.radians(i); L = 110
        sx, sy = x0 - L*math.sin(a), yo + L*math.cos(a)
        o += lijn(x0, yo - 70, x0, yo + 120, GRIJS, 1.2, '5 4') + straal(sx, sy, x0, yo, kleur, 2.5)
        sr = N_WATER * math.sin(a)
        if sr < 0.999:
            r = math.asin(sr); o += straal(x0, yo, x0 + 90*math.sin(r), yo - 90*math.cos(r), kleur, 2.5)
            o += straal(x0, yo, x0 + 60*math.sin(a), yo + 60*math.cos(a), kleur, 1, dash='3 3')
        elif sr < 1.001:
            o += straal(x0, yo, x0 + 95, yo - 2, kleur, 2.5)
        else:
            o += straal(x0, yo, x0 + L*math.sin(a), yo + L*math.cos(a), kleur, 2.5)
        o += t(x0, yo - 80, label, kleur, 'middle', 12)
    return svg(o, w, h)
fig_totaal = totaal_fig()

def glasvezel_fig():
    o = '<rect x="20" y="90" width="600" height="70" rx="35" fill="#e0f2fe" stroke="#0369a1" stroke-width="2"/>'
    pts = [(30, 125)] + [(80 + 90 * k, 92 if k % 2 == 0 else 158) for k in range(6)] + [(610, 125)]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]): o += straal(x1, y1, x2, y2, ROOD, 2.5)
    o += t(320, 190, 'het licht weerkaatst telkens volledig op de wand (i > grenshoek)', GRIJS, 'middle', 12, 600) + t(320, 70, 'glasvezel', INK)
    return svg(o, 640, 205)
fig_glasvezel = glasvezel_fig()

def fata_fig():
    o = '<rect x="0" y="0" width="640" height="200" fill="#eff6ff"/><rect x="0" y="200" width="640" height="40" fill="#9ca3af"/>'
    o += '<rect x="0" y="180" width="640" height="20" fill="#fde68a" opacity="0.6"/>' + t(630, 194, 'hete, ijle lucht boven de weg', '#92400e', 'end', 11, 600)
    o += f'<path d="M60,60 Q380,250 560,120" fill="none" stroke="{LICHT}" stroke-width="3"/>' + kop(300, 158, 0.15, LICHT)
    o += oog(570, 116, 205) + lijn(560, 120, 330, 215, LICHT, 1.6, '5 4')
    o += '<ellipse cx="320" cy="214" rx="40" ry="5" fill="#93c5fd" opacity="0.8"/>' + t(320, 232, '"plas water" = beeld van de lucht', INK, 'middle', 12)
    o += t(60, 45, 'licht van de lucht', '#b45309', 'start', 12)
    return svg(o, 640, 240)
fig_fata = fata_fig()

h3_doelen = ['uitleggen wat <b>lichtbreking</b> is en wanneer ze optreedt;',
             'de stralengang tekenen bij de overgang van een optisch <b>ijle</b> naar een optisch <b>dichte</b> middenstof en omgekeerd;',
             'met de juiste termen verwoorden wat er met een lichtstraal gebeurt bij breking (bv. "breekt naar de normaal toe");',
             'het verband tussen <b>invalshoek</b> en <b>brekingshoek</b> noteren;',
             'de <b>schijnbare verhoging</b> van een voorwerp in water verklaren met een tekening;',
             'de voorwaarden voor <b>totale weerkaatsing</b> noteren en toepassen, en de stralengang tekenen;',
             'een <b>fata morgana</b> verklaren met een tekening;',
             'de werking van een <b>glasvezelkabel</b> uitleggen.']
h3_vk = vk('<b>Optische middenstof</b> en rechtlijnige voortplanting (hoofdstuk 1).', '<b>Normaal</b>, <b>invalspunt</b> en <b>invalshoek</b> (hoofdstuk 2).', 'Het beeld ontstaat waar de <b>verlengden</b> van stralen samenkomen (hoofdstuk 2).')

h3_1 = f'''<p>Een rietje in een glas water lijkt geknikt. Dat komt doordat licht van richting verandert als het van water naar lucht gaat.</p>
{kader('Definitie', '<p><b>Lichtbreking</b> is de richtingsverandering van licht wanneer het <b>schuin</b> invalt op het grensvlak tussen twee verschillende optische middenstoffen.</p>')}
<p>Valt het licht <b>loodrecht</b> in (i = 0°), dan gaat het rechtdoor: geen breking. Het licht gaat in een optisch <b>dichte</b> middenstof (glas, water) trager dan in een optisch <b>ijle</b> middenstof (lucht).</p>
{figuur(fig_breking, 'Links: van ijl naar dicht breekt de straal naar de normaal toe. Rechts: van dicht naar ijl breekt de straal van de normaal weg.')}
<table class="vb"><tr><td>Van ijl naar dicht</td><td>de straal breekt <b>naar de normaal toe</b></td><td>brekingshoek <b>kleiner</b> dan invalshoek: r &lt; i</td></tr>
<tr><td>Van dicht naar ijl</td><td>de straal breekt <b>van de normaal weg</b></td><td>brekingshoek <b>groter</b> dan invalshoek: r &gt; i</td></tr></table>
<p>De <b>brekingshoek r</b> is de hoek tussen de <b>gebroken straal</b> en de <b>normaal</b>. Hoe groter de invalshoek, hoe groter de brekingshoek. Ook hier is de stralengang omkeerbaar.</p>
<p>Formuleer zo: "Bij de overgang van een optisch ijle naar een optisch dichte middenstof breekt de lichtstraal <b>naar de normaal toe</b>."</p>
{tool('optica.html#s5', 'Breking van ijl naar dicht in de tool')} {tool('optica.html#s4', 'Breking van dicht naar ijl in de tool')}
{denk('denk_1', 'Een lichtstraal gaat van lucht naar glas met een invalshoek van 40°. Kan de brekingshoek 50° zijn? En 25°?', [
  ('Welke overgang?', 'Van lucht (ijl) naar glas (dicht).'), ('Regel', 'Van ijl naar dicht breekt de straal naar de normaal toe: r &lt; i.'), ('Toepassen', '50° is groter dan 40°: kan niet. 25° is kleiner: kan wel.')], 'Alleen 25° is mogelijk.')}'''

h3_2 = f'''<p>Een munt op de bodem van een glas water of een steen in een vijver lijkt <b>hoger</b> te liggen dan in werkelijkheid. Dat noem je <b>schijnbare verhoging</b>.</p>
{figuur(fig_munt, "Twee lichtstralen uit punt V breken aan het wateroppervlak van de normaal weg. Hun verlengden snijden in V': het voorwerp lijkt hoger te liggen.")}
<h3>Stappenplan: de schijnbare verhoging tekenen</h3>
<ol><li>Teken <b>twee lichtstralen</b> die uit hetzelfde punt V van het voorwerp naar het wateroppervlak gaan.</li>
<li>Teken in elk invalspunt de <b>normaal</b> (stippellijn).</li>
<li>Van water naar lucht is van <b>dicht naar ijl</b>: teken de gebroken stralen <b>van de normaal weg</b>. Ze waaieren uit en komen in het oog.</li>
<li>Je oog denkt dat licht rechtdoor gaat: <b>verleng</b> de gebroken stralen naar achter (stippellijn) tot ze snijden. Dat snijpunt is <b>V'</b>.</li>
<li>Teken in V' het <b>schijnbaar voorwerp</b>: het ligt hoger dan het echte voorwerp.</li></ol>
<p>Daarom lijkt een zwembad minder diep dan het is, en moet een visser met een speer <b>lager</b> mikken dan waar hij de vis ziet.</p>
{tool('optica.html#s11', 'Bouw de tekening stap voor stap op in de tool')}
{denk('denk_2', 'In een zwembad lijkt het diepe deel maar 1,5 m diep, maar het bord zegt 2 m. Wie heeft gelijk? Leg uit.', [
  ('Welke overgang?', 'Licht van de bodem gaat van water naar lucht: van dicht naar ijl.'), ('Breking', 'Het breekt van de normaal weg.'), ('Wat ziet je oog?', 'Je oog verlengt de gebroken stralen: de bodem lijkt hoger te liggen.')], 'Het bord heeft gelijk: door schijnbare verhoging lijkt het zwembad minder diep.')}'''

h3_3 = f'''<p>Gaat licht van een <b>dichte</b> naar een <b>ijle</b> middenstof, dan breekt het van de normaal weg. Maak je de invalshoek groter, dan wordt de brekingshoek nog sneller groter. Bij een bepaalde invalshoek, de <b>grenshoek g</b>, scheert de gebroken straal langs het grensvlak (r = 90°). Is de invalshoek nog groter, dan kan het licht niet meer naar buiten: het wordt <b>volledig weerkaatst</b>.</p>
{figuur(fig_totaal, 'Drie stralen in water met een steeds grotere invalshoek. Bij i > g is er totale weerkaatsing.')}
{kader('Voorwaarden voor totale weerkaatsing', '<p>1. Het licht gaat van een optisch <b>dichte</b> naar een optisch <b>ijle</b> middenstof.<br>2. De invalshoek is <b>groter dan de grenshoek</b>: i &gt; g.</p><p>Grenshoek water–lucht: ongeveer 49°. Grenshoek glas–lucht: ongeveer 42°.</p>')}
<p>Bij totale weerkaatsing gelden de wetten van de weerkaatsing: i = r.</p>
<h3>Glasvezel</h3>
{figuur(fig_glasvezel, 'In een glasvezel wordt het licht telkens totaal weerkaatst.')}
<p>Een <b>glasvezelkabel</b> (fiber) is een heel dunne draad van glas. Het licht valt telkens onder een grote hoek (groter dan de grenshoek) op de wand en wordt <b>totaal weerkaatst</b>. Zo blijft het licht in de vezel, ook in een bocht. Via glasvezel gaan internet en tv als lichtsignalen naar je huis; artsen gebruiken glasvezel om in het lichaam te kijken (endoscoop).</p>
<h3>Fata morgana</h3>
{figuur(fig_fata, 'Luchtspiegeling boven een hete weg: je ziet een beeld van de lucht op de weg, dat lijkt op een plas water.')}
<p>Op een warme dag is de lucht vlak boven het asfalt heel warm en dus optisch <b>ijler</b> dan de lucht erboven. Licht van de lucht dat schuin naar de weg gaat, gaat steeds van dichter naar ijler en breekt steeds verder van de normaal weg. Vlak boven de weg wordt het <b>totaal weerkaatst</b> en buigt het weer omhoog naar je oog. Je oog verlengt de straal: je ziet de blauwe lucht op de weg, als een "plas water". Dat is een <b>fata morgana</b> of luchtspiegeling.</p>
{tool('optica.html#s6', 'Totale weerkaatsing in de tool')} {tool('optica.html#s7', 'Glasvezel in de tool')} {tool('optica.html#s8', 'Luchtspiegeling in de tool')}
{denk('denk_3', 'Kan er totale weerkaatsing optreden als licht van lucht naar water gaat?', [
  ('Voorwaarde 1', 'Het licht moet van dicht naar ijl gaan.'), ('Hier', 'Van lucht naar water is van ijl naar dicht: de straal breekt naar de normaal toe en kan altijd het water in.')], 'Nee: totale weerkaatsing kan alleen van dicht naar ijl.')}'''

op_b1, opl_b1 = breking_fig(45, 'lucht', 'glas', 1.0, N_GLAS, opl=False), breking_fig(45, 'lucht', 'glas', 1.0, N_GLAS)
op_b2, opl_b2 = breking_fig(30, 'water', 'lucht', N_WATER, 1.0, opl=False), breking_fig(30, 'water', 'lucht', N_WATER, 1.0)
op_b3, opl_b3 = breking_fig(60, 'glas', 'lucht', N_GLAS, 1.0, opl=False), breking_fig(60, 'glas', 'lucht', N_GLAS, 1.0)
VH = [(120, 200), (80, 260), (150, 150)]
op_vh = [verhoging_fig(d, x, stap=0, ruitjes=True, pupil=150, oog=1.6) for d, x in VH]
opl_vh = [verhoging_fig(d, x, stap=4, ruitjes=True, pupil=150, oog=1.6) for d, x in VH]

h3_oef = f'''{oef('opl_1', 1, 'Ijl of dicht?', 'Welke middenstof is optisch het dichtst? Breekt de straal naar de normaal toe of van de normaal weg?<ol class="deelvragen" type="a"><li>van lucht naar water</li><li>van glas naar lucht</li><li>van water naar glas</li><li>van water naar lucht</li></ol>', [
  ('a', 'water is dichter: naar de normaal toe'), ('b', 'glas is dichter: van de normaal weg'), ('c', 'glas is dichter: naar de normaal toe'), ('d', 'water is dichter: van de normaal weg')], 'Naar dichter: naar de normaal toe. Naar ijler: van de normaal weg.')}
{oef_fig('opl_2', 2, 'Breking tekenen: lucht naar glas', 'Teken de gebroken straal. Duid de invalshoek i en de brekingshoek r aan. Is r groter of kleiner dan i?', op_b1, [
  ('Overgang', 'ijl naar dicht'), ('Gebroken straal', 'naar de normaal toe'), ('Hoeken', 'r &lt; i (hier ongeveer 28° tegenover 45°)')], 'De straal breekt naar de normaal toe.', opl_b1)}
{oef_fig('opl_3', 3, 'Breking tekenen: water naar lucht', 'Teken de gebroken straal en duid i en r aan.', op_b2, [
  ('Overgang', 'dicht naar ijl'), ('Gebroken straal', 'van de normaal weg'), ('Hoeken', 'r &gt; i (hier ongeveer 42° tegenover 30°)')], 'De straal breekt van de normaal weg.', opl_b2)}
{oef_fig('opl_4', 4, 'Breking of totale weerkaatsing?', 'De straal gaat van glas naar lucht met i = 60°. De grenshoek van glas is 42°. Teken wat er met de straal gebeurt.', op_b3, [
  ('Voorwaarde 1', 'van dicht naar ijl: ja'), ('Voorwaarde 2', 'i = 60° &gt; g = 42°: ja'), ('Gevolg', 'totale weerkaatsing: de straal weerkaatst met r = 60°')], 'Totale weerkaatsing: geen gebroken straal in de lucht.', opl_b3)}
{oef_fig('opl_5', 5, 'Schijnbare verhoging tekenen', "Twee lichtstralen vertrekken uit punt V. Teken de normalen, de gebroken stralen naar het oog, de verlengden en het schijnbare punt V'. Teken het schijnbaar voorwerp.", op_vh[0], [('Normalen', 'teken de normaal in elk invalspunt'), ('Breking', 'water naar lucht = dicht naar ijl: beide stralen breken van de normaal weg, naar het oog'), ('Verlengden', "verleng de gebroken stralen naar achter tot ze snijden in V'"), ('Schijnbaar voorwerp', "teken het voorwerp opnieuw vanuit V': het ligt hoger")], "Het voorwerp lijkt hoger te liggen dan het echte voorwerp.", opl_vh[0])}
{oef_fig('opl_5', 5, 'Schijnbare verhoging: ondiep water', "Het voorwerp ligt minder diep en het oog staat verder opzij. Teken de schijnbare verhoging volgens het stappenplan.", op_vh[1], [('Normalen', 'teken de normaal in elk invalspunt'), ('Breking', 'water naar lucht = dicht naar ijl: beide stralen breken van de normaal weg, naar het oog'), ('Verlengden', "verleng de gebroken stralen naar achter tot ze snijden in V'"), ('Schijnbaar voorwerp', "teken het voorwerp opnieuw vanuit V': het ligt hoger")], "Ook hier lijkt het voorwerp hoger te liggen.", opl_vh[1])}
{oef_fig('opl_5', 5, 'Schijnbare verhoging: diep water', "Het voorwerp ligt dieper en het oog kijkt bijna recht naar beneden. Teken de schijnbare verhoging en vergelijk met de vorige oefeningen.", op_vh[2], [('Normalen', 'teken de normaal in elk invalspunt'), ('Breking', 'water naar lucht = dicht naar ijl: beide stralen breken van de normaal weg, naar het oog'), ('Verlengden', "verleng de gebroken stralen naar achter tot ze snijden in V'"), ('Schijnbaar voorwerp', "teken het voorwerp opnieuw vanuit V': het ligt hoger")], "Hoe dieper het voorwerp, hoe groter de verhoging in cm.", opl_vh[2])}
{oef('opl_6', 6, 'Totale weerkaatsing: ja of nee?', 'Is er totale weerkaatsing? Leg uit met de twee voorwaarden.<ol class="deelvragen" type="a"><li>van water naar lucht, i = 30°</li><li>van water naar lucht, i = 60°</li><li>van lucht naar glas, i = 80°</li><li>van glas naar lucht, i = 50°</li></ol>', [
  ('a', 'nee: i = 30° &lt; g = 49°'), ('b', 'ja: dicht naar ijl en 60° &gt; 49°'), ('c', 'nee: van ijl naar dicht'), ('d', 'ja: dicht naar ijl en 50° &gt; 42°')], 'Beide voorwaarden moeten kloppen.')}
{oef('opl_7', 7, 'Speervissen', 'Een visser ziet een vis in het water en wil hem met een speer raken. Moet hij richten op de plaats waar hij de vis ziet, hoger of lager? Leg uit met breking.', [
  ('Overgang', 'Licht van de vis gaat van water naar lucht: van de normaal weg.'), ('Wat ziet de visser?', 'Hij verlengt de gebroken straal: de vis lijkt hoger te zitten.'), ('Besluit', 'De echte vis zit lager.')], 'Lager richten dan waar hij de vis ziet.')}
{oef('opl_8', 8, 'Glasvezel en fata morgana', 'Leg uit.<ol class="deelvragen" type="a"><li>Waarom blijft het licht in een glasvezelkabel, ook in een bocht?</li><li>Waarom zie je op een hete dag "water" op de weg dat verdwijnt als je dichterbij komt?</li></ol>', [
  ('a', 'Het licht valt onder een invalshoek groter dan de grenshoek op de wand, van glas (dicht) naar buiten (ijl): totale weerkaatsing.'),
  ('b', 'Hete lucht boven de weg is ijler. Licht van de lucht wordt vlak boven de weg totaal weerkaatst naar je oog. Je ziet een beeld van de blauwe lucht: een fata morgana.')], 'Allebei toepassingen van totale weerkaatsing.')}
{oef('opl_9', 9, 'Juist of fout?', 'Juist of fout? Verbeter.<ol class="deelvragen" type="a"><li>Licht dat loodrecht op water valt, breekt naar de normaal toe.</li><li>Van ijl naar dicht is de brekingshoek kleiner dan de invalshoek.</li><li>Totale weerkaatsing kan bij elke overgang optreden.</li><li>Door breking lijkt een zwembad dieper dan het is.</li></ol>', [
  ('a', 'Fout: loodrecht invallend licht breekt niet.'), ('b', 'Juist.'), ('c', 'Fout: alleen van dicht naar ijl en als i &gt; g.'), ('d', 'Fout: het lijkt minder diep (schijnbare verhoging).')], 'Alleen b is juist.')}'''

h3_samenv = '''<p><b>Lichtbreking</b>: richtingsverandering van licht dat schuin invalt op het grensvlak van twee optische middenstoffen. Loodrecht: geen breking.</p>
<p><b>Ijl → dicht</b>: naar de normaal toe, r &lt; i. <b>Dicht → ijl</b>: van de normaal weg, r &gt; i.</p>
<p><b>Schijnbare verhoging</b>: licht van een voorwerp in water breekt van de normaal weg; je oog verlengt de straal; het voorwerp lijkt hoger.</p>
<p><b>Totale weerkaatsing</b>: van dicht naar ijl én i &gt; grenshoek. Toepassingen: <b>glasvezel</b>, <b>fata morgana</b>.</p>'''

maak('cursus-lichtbreking.html', 'Fysica 3de jaar · Thema 1 Optische fenomenen · Hoofdstuk 3', 'Lichtbreking',
     'Werk dit hoofdstuk samen met de tool <a href="optica.html">Optica</a>. Oefeningen maak je op papier.',
     h3_doelen, h3_vk, [('Wat is lichtbreking?', h3_1), ('Schijnbare verhoging', h3_2), ('Totale weerkaatsing', h3_3)],
     h3_oef, h3_samenv, ('optica.html#s6', 'Oefen verder in de tool Optica'))

# ================================================================ H4 LENZEN
S, FH = 20, 3       # 20 px per hokje, brandpuntsafstand 3 hokjes
XL, YA = 320, 130   # lens en hoofdas
def lens_fig(v, h=2.0, opl=True, ruitjes=True, labels=True, w=640, H=260, nummers=False):
    o = ruit(w, H) if ruitjes else ''
    o += lijn(0, YA, w, YA, INK, 1.5)
    o += f'<path d="M{XL},{YA-100} Q{XL+14},{YA} {XL},{YA+100} Q{XL-14},{YA} {XL},{YA-100}Z" fill="#bfdbfe" stroke="#1d4ed8" stroke-width="2" opacity="0.9"/>'
    for k, naam in [(-2, '2F'), (-1, 'F'), (1, "F'"), (2, "2F'")]:
        x = XL + k * FH * S
        o += lijn(x, YA - 5, x, YA + 5, INK, 2) + t(x, YA + 20, naam, INK, 'middle', 12)
    o += punt(XL, YA, INK, 3) + t(XL + 6, YA - 6, 'O', INK, 'start', 11)
    x0, y0 = XL - v * S, YA - h * S
    o += lijn(x0, YA, x0, y0 + 4, ROOD, 3.5) + kop(x0, y0, -math.pi / 2, ROOD, 13) + t(x0 - 6, y0 - 6, 'V', ROOD, 'end', 13)
    if not opl: return svg(o, w, H)
    f = FH * S; vp = v * S; hp = h * S
    xF1, xF2 = XL - f, XL + f
    if abs(vp - f) < 0.01:
        # geen beeld: stralen evenwijdig na de lens
        o += straal(x0, y0, XL, y0, LICHT, 2) + straal(XL, y0, w, y0 + (YA - y0) * (w - XL) / f, LICHT, 2, pos=0.3)
        o += straal(x0, y0, XL, YA, LICHT, 2) + straal(XL, YA, w, YA + (YA - y0) * (w - XL) / vp, LICHT, 2, pos=0.3)
        o += t(520, 30, 'evenwijdige stralen: geen beeld', INK, 'middle', 13)
        return svg(o, w, H)
    b = vp * f / (vp - f); hb = -hp * b / vp
    xb, yb = XL + b, YA - hb
    # straal 1: evenwijdig met de as, daarna door F'
    k1 = (YA - y0) / f
    o += straal(x0, y0, XL, y0, LICHT, 2) + straal(XL, y0, w, y0 + k1 * (w - XL), LICHT, 2, pos=0.25)
    # straal 2: door O, rechtdoor
    k2 = (YA - y0) / vp
    o += straal(x0, y0, XL, YA, LICHT, 2) + straal(XL, YA, w, YA + k2 * (w - XL), LICHT, 2, pos=0.25)
    # straal 3: door F, daarna evenwijdig
    if vp > f:
        y3 = y0 + (YA - y0) * (XL - x0) / (xF1 - x0)
        o += straal(x0, y0, XL, y3, LICHT, 2) + straal(XL, y3, w, y3, LICHT, 2, pos=0.25)
    else:
        y3 = YA + (y0 - YA) * (XL - xF1) / (x0 - xF1)
        o += lijn(xF1, YA, x0, y0, LICHT, 1.3, '4 4') + straal(x0, y0, XL, y3, LICHT, 2) + straal(XL, y3, w, y3, LICHT, 2, pos=0.25)
    if nummers:
        o += t(XL - 40, y0 - 6, '1', '#b45309', 'middle', 13) + t(XL + 40, YA + (YA - y0) * 40 / vp - 8, '2', '#b45309', 'middle', 13) + t(XL + 60, y3 + 16, '3', '#b45309', 'middle', 13)
    if b > 0:
        o += lijn(xb, YA, xb, yb + (4 if hb < 0 else -4), BLAUW, 3.5) + kop(xb, yb, math.pi / 2 if hb < 0 else -math.pi / 2, BLAUW, 13) + t(xb + 8, yb + (14 if hb < 0 else -6), 'B', BLAUW, 'start', 13)
    else:
        # virtueel beeld: verlengden naar links
        o += lijn(XL, y0, xb, yb, LICHT, 1.3, '4 4') + lijn(XL, YA, xb, yb, LICHT, 1.3, '4 4') + lijn(XL, y3, xb, yb, LICHT, 1.3, '4 4')
        o += lijn(xb, YA, xb, yb + 4, BLAUW, 3, '6 4') + kop(xb, yb, -math.pi / 2, BLAUW, 13) + t(xb - 8, yb - 4, 'B (virtueel)', BLAUW, 'end', 13)
    return svg(o, w, H)

POS = [
    ('Voorwerp voorbij 2F (v > 2f)', 7.5, 'tussen F\' en 2F\'', 'omgekeerd', 'verkleind', 'reëel', 'fototoestel, oog'),
    ('Voorwerp in 2F (v = 2f)', 6.0, 'in 2F\'', 'omgekeerd', 'even groot', 'reëel', 'kopieerapparaat'),
    ('Voorwerp tussen F en 2F (f < v < 2f)', 4.5, 'voorbij 2F\'', 'omgekeerd', 'vergroot', 'reëel', 'projector, beamer'),
    ('Voorwerp in F (v = f)', 3.0, '–', '–', '–', 'geen beeld', 'zaklamp, schijnwerper'),
    ('Voorwerp tussen F en de lens (v < f)', 1.5, 'aan dezelfde kant als het voorwerp', 'rechtop', 'vergroot', 'virtueel', 'vergrootglas (loep)'),
]
fig_hoofd = lens_fig(7.5, nummers=True, ruitjes=True)
pos_figs = ''.join(figuur(lens_fig(v, ruitjes=True, opl=False), f'{naam}. Construeer het beeld samen in de les: vertrek met de hoofdstralen vanuit de top van de pijl.')
                   for naam, v, plaats, stand, grootte, aard, toep in POS)

def vergroting_fig():
    v, h = 7.5, 2.0
    f = FH * S; vp, hp = v * S, h * S; b = vp * f / (vp - f); hb = hp * b / vp
    x0, y0, xb, yb = XL - vp, YA - hp, XL + b, YA + hb
    o = lijn(0, YA, 640, YA, INK, 1.5) + f'<path d="M{XL},{YA-100} Q{XL+14},{YA} {XL},{YA+100} Q{XL-14},{YA} {XL},{YA-100}Z" fill="#bfdbfe" stroke="#1d4ed8" stroke-width="2"/>'
    o += f'<path d="M{x0},{YA} L{x0},{y0} L{XL},{YA}Z" fill="{ROOD}" opacity="0.12"/><path d="M{xb},{YA} L{xb},{yb} L{XL},{YA}Z" fill="{BLAUW}" opacity="0.12"/>'
    o += lijn(x0, YA, x0, y0, ROOD, 3.5) + lijn(xb, YA, xb, yb, BLAUW, 3.5) + straal(x0, y0, xb, yb, LICHT, 2)
    o += t(x0 - 8, (YA + y0) / 2, 'V', ROOD, 'end', 14) + t(xb + 8, (YA + yb) / 2 + 4, 'B', BLAUW, 'start', 14)
    o += lijn(x0, YA + 70, XL, YA + 70, ROOD, 1.5) + t((x0 + XL) / 2, YA + 88, 'v', ROOD, 'middle', 14)
    o += lijn(XL, YA - 60, xb, YA - 60, BLAUW, 1.5) + t((XL + xb) / 2, YA - 66, 'b', BLAUW, 'middle', 14)
    return svg(o, 640, 240)
fig_vergr = vergroting_fig()

h4_doelen = ['in een figuur de <b>drie hoofdstralen</b> tekenen die door een bolle lens gebroken worden;',
             'de stralengang bij een bolle lens tekenen en het gevormde <b>beeld construeren</b>;',
             'de <b>kenmerken van het beeld</b> (stand, grootte, aard) en de <b>toepassing</b> noteren die bij een constructie horen;',
             'met het principe van <b>gelijkvormigheid</b> de vergrotingsfactor van een bolle lens berekenen;',
             'de formule voor de <b>vergrotingsfactor</b> gebruiken en omvormen om de grootte van beeld of voorwerp, of de beeld- en voorwerpsafstand te berekenen.']
h4_vk = vk('<b>Lichtbreking</b>: van ijl naar dicht naar de normaal toe, van dicht naar ijl van de normaal weg (hoofdstuk 3).', 'Een <b>virtueel</b> beeld ontstaat waar de <b>verlengden</b> van stralen samenkomen (hoofdstuk 2).', '<b>Convergerende</b> en <b>evenwijdige</b> lichtbundels (hoofdstuk 1).', 'Een formule met een breuk <b>omvormen</b>, bv. a = b / c → b = a · c.')

h4_1 = f'''<p>Een <b>bolle lens</b> (convergerende lens) is in het midden dikker dan aan de rand. Evenwijdige stralen worden door de lens gebroken en komen samen in één punt: het <b>brandpunt</b>.</p>
<table class="vb"><tr><td>Hoofdas</td><td>de rechte door het midden van de lens, loodrecht op de lens</td></tr>
<tr><td>Optisch middelpunt O</td><td>het midden van de lens</td></tr>
<tr><td>Brandpunt F'</td><td>het punt waar stralen evenwijdig met de hoofdas na de lens samenkomen; aan de andere kant ligt F</td></tr>
<tr><td>Brandpuntsafstand f</td><td>de afstand van O tot F (= de afstand van O tot F')</td></tr></table>
{kader('De drie hoofdstralen', '<p><b>1.</b> Een straal <b>evenwijdig met de hoofdas</b> gaat na de lens <b>door F\'</b>.<br><b>2.</b> Een straal <b>door O</b> gaat <b>rechtdoor</b>.<br><b>3.</b> Een straal <b>door F</b> gaat na de lens <b>evenwijdig met de hoofdas</b>.</p>')}
{figuur(fig_hoofd, 'De drie hoofdstralen vanuit de top van het voorwerp V. Waar ze samenkomen, ligt de top van het beeld B.')}
<p>We tekenen de breking voor het gemak in één keer op de middellijn van de lens.</p>
{tool('optica.html#s10', 'Teken de hoofdstralen in de tool')}
{denk('denk_1', 'De straal door O gaat rechtdoor. Breekt hij dan niet bij het binnengaan en buitengaan van de lens?', [
  ('In het midden', 'In het midden zijn de twee kanten van de lens evenwijdig, zoals bij een dun ruitje.'),
  ('Breking', 'De straal breekt bij het binnengaan en bij het buitengaan in tegengestelde zin. Bij een dunne lens heffen die twee knikken elkaar op.'),
], 'Bij een dunne lens gaat de straal door O (bijna) rechtdoor.')}'''

tabel_pos = '<table class="vb"><tr><td><b>Plaats voorwerp</b></td><td><b>Beeld</b></td><td><b>Toepassing</b></td></tr>' + ''.join(
    f'<tr><td>{naam.replace("Voorwerp ", "")}</td><td>{"geen beeld" if aard == "geen beeld" else f"{plaats} · {stand} · {grootte} · {aard}"}</td><td>{toep}</td></tr>' for naam, v, plaats, stand, grootte, aard, toep in POS) + '</table>'

h4_2 = f'''<p>De <b>voorwerpsafstand v</b> is de afstand van het voorwerp tot de lens. De <b>beeldafstand b</b> is de afstand van het beeld tot de lens.</p>
<h3>Stappenplan: het beeld construeren</h3>
<ol><li>Teken de <b>hoofdas</b>, de lens, O en de brandpunten F, F' (en 2F, 2F').</li>
<li>Teken het voorwerp als een <b>pijl</b> op de hoofdas.</li>
<li>Teken vanuit de <b>top</b> van de pijl minstens <b>twee hoofdstralen</b> (de derde is een controle).</li>
<li>Waar de gebroken stralen <b>snijden</b>, ligt de top van het beeld. Komen ze niet samen, verleng ze dan naar achter (stippellijn).</li>
<li>Teken het beeld als een pijl tot op de hoofdas. Noteer de <b>kenmerken</b>: stand (rechtop of omgekeerd), grootte (vergroot, verkleind of even groot) en aard (reëel of virtueel).</li></ol>
<p>Een <b>reëel</b> beeld kan je opvangen op een scherm: de stralen komen er echt samen. Een <b>virtueel</b> beeld niet: alleen de verlengden komen samen.</p>
<h3>Vijf posities van het voorwerp</h3>\n<p>Construeer bij elke positie het beeld. Vertrek telkens <b>vanuit de top van de pijl</b> met de hoofdstralen. Noteer daarna de kenmerken.</p>\n{pos_figs}
{tabel_pos}
<p>Onthoud: hoe <b>dichter</b> het voorwerp bij F komt, hoe <b>verder</b> en <b>groter</b> het beeld. Komt het voorwerp binnen F, dan krijg je een rechtopstaand, vergroot, virtueel beeld: een vergrootglas.</p>
{tool('optica.html#s10', 'Verschuif het voorwerp in de tool en bekijk het beeld')}
{denk('denk_2', 'Een beamer in de klas projecteert een klein beeldje op een groot scherm. Waar staat het beeldje tegenover de lens van de beamer? Waarom staat het beeldje in de beamer ondersteboven?', [
  ('Wat is nodig?', 'Een reëel beeld (op een scherm) dat vergroot is.'), ('Welke positie?', 'Het voorwerp staat tussen F en 2F: het beeld is reëel, vergroot en omgekeerd.'), ('Omgekeerd', 'Omdat het beeld omgekeerd is, zet men het beeldje ondersteboven in de beamer. Zo staat het beeld op het scherm rechtop.')], 'Tussen F en 2F; het beeldje staat ondersteboven omdat het beeld omgekeerd is.')}
{denk('denk_3', 'Je houdt een vergrootglas boven een krant. Je brengt het vergrootglas langzaam verder van de krant. Op een bepaald moment wordt alles wazig en daarna zie je de letters ondersteboven. Leg uit.', [
  ('Dicht bij de krant', 'De krant staat tussen F en de lens: rechtop, vergroot, virtueel beeld.'), ('In F', 'Staat de krant in F, dan gaan de stralen evenwijdig: geen beeld, alles wazig.'), ('Verder weg', 'Staat de krant voorbij F, dan wordt het beeld reëel en omgekeerd.')], 'Binnen F: rechtop en vergroot. In F: geen beeld. Voorbij F: omgekeerd.')}'''

h4_3 = f'''{kader('Vergrotingsfactor', '<p>De <b>vergrotingsfactor N</b> zegt hoeveel keer het beeld groter is dan het voorwerp:</p><p style="font-size:18px"><b>N = B / V</b> &nbsp;&nbsp; en &nbsp;&nbsp; <b>N = b / v</b></p><p>B = grootte van het beeld, V = grootte van het voorwerp · b = beeldafstand, v = voorwerpsafstand. Let op: hoofdletters B en V zijn <b>groottes</b>, kleine letters b en v zijn <b>afstanden</b>.</p>')}
{figuur(fig_vergr, 'De straal door O maakt twee gelijkvormige driehoeken: B/V = b/v.')}
<p>Waarom zijn de twee formules gelijk? De straal door O vormt met het voorwerp en met het beeld twee <b>gelijkvormige driehoeken</b> (dezelfde hoeken). Dan zijn de verhoudingen van overeenkomstige zijden gelijk: B / V = b / v.</p>
<p>N &gt; 1: het beeld is vergroot. N = 1: even groot. N &lt; 1: verkleind. N heeft geen eenheid. Gebruik voor b en v dezelfde eenheid (bv. allebei cm).</p>
<h3>Omvormen</h3>
<p>B = N · V &nbsp;·&nbsp; V = B / N &nbsp;·&nbsp; b = N · v &nbsp;·&nbsp; v = b / N</p>
<h3>Uitgewerkt voorbeeld</h3>
{STAP}
<p>Een kaars van 4,0 cm staat 15 cm voor een lens. Er ontstaat een scherp beeld op een scherm op 30 cm achter de lens. Hoe groot is het beeld?</p>
<table class="vb"><tr><td>Gegeven</td><td>V = 4,0 cm · v = 15 cm · b = 30 cm</td></tr><tr><td>Gevraagd</td><td>B</td></tr>
<tr><td>Formule</td><td>N = b / v en B = N · V</td></tr><tr><td>Oplossing</td><td>N = 30 cm / 15 cm = 2,0 &nbsp;→&nbsp; B = 2,0 · 4,0 cm = 8,0 cm</td></tr>
<tr><td>Antwoord</td><td>Het beeld is 8,0 cm groot (2 keer vergroot).</td></tr></table>
{tool('optica.html#s16', 'Oefen met de vergrotingsfactor in de tool')}
{denk('denk_4', 'Bij een fototoestel is het beeld op de sensor veel kleiner dan het voorwerp. Is N dan groter of kleiner dan 1? Wat weet je dan over b en v?', [
  ('Grootte', 'B is veel kleiner dan V: N = B/V &lt; 1.'), ('Afstanden', 'N = b/v &lt; 1, dus b &lt; v: het beeld ligt dichter bij de lens dan het voorwerp.')], 'N < 1 en b < v.')}'''

op_l1, opl_l1 = lens_fig(7.5, opl=False), lens_fig(7.5)
op_l2, opl_l2 = lens_fig(4.5, opl=False), lens_fig(4.5)
op_l3, opl_l3 = lens_fig(1.5, h=1.5, opl=False), lens_fig(1.5, h=1.5)
op_l4, opl_l4 = lens_fig(6.0, opl=False), lens_fig(6.0)
EXTRA = [(9.0, 3.0), (5.0, 1.5), (3.0, 2.0), (2.0, 1.0)]
op_ex = [lens_fig(v, h=h, opl=False) for v, h in EXTRA]
opl_ex = [lens_fig(v, h=h) for v, h in EXTRA]

h4_oef = f'''{oef('opl_1', 1, 'De hoofdstralen', 'Vul aan.<ol class="deelvragen" type="a"><li>Een straal evenwijdig met de hoofdas gaat na de lens door …</li><li>Een straal door het optisch middelpunt …</li><li>Een straal door F gaat na de lens …</li></ol>', [
  ('a', "het brandpunt F'"), ('b', 'gaat rechtdoor'), ('c', 'evenwijdig met de hoofdas')], 'De drie hoofdstralen.')}
{oef_fig('opl_2', 2, 'Constructie: voorwerp voorbij 2F', 'Construeer het beeld met minstens twee hoofdstralen. Noteer stand, grootte, aard en een toepassing. (1 hokje = 1 cm, f = 3 cm)', op_l1, [
  ('Hoofdstralen', "evenwijdige straal door F'; straal door O rechtdoor; straal door F evenwijdig"), ('Beeld', "tussen F' en 2F'"), ('Kenmerken', 'omgekeerd, verkleind, reëel'), ('Toepassing', 'fototoestel, oog')], 'Omgekeerd, verkleind, reëel.', opl_l1)}
{oef_fig('opl_3', 3, 'Constructie: voorwerp tussen F en 2F', 'Construeer het beeld en noteer de kenmerken en een toepassing.', op_l2, [
  ('Beeld', "voorbij 2F'"), ('Kenmerken', 'omgekeerd, vergroot, reëel'), ('Toepassing', 'projector, beamer')], 'Omgekeerd, vergroot, reëel.', opl_l2)}
{oef_fig('opl_4', 4, 'Constructie: voorwerp tussen F en de lens', 'Construeer het beeld. De gebroken stralen komen niet samen: verleng ze. Noteer de kenmerken en een toepassing.', op_l3, [
  ('Gebroken stralen', 'lopen uit elkaar; verleng ze naar links (stippellijn)'), ('Beeld', 'aan dezelfde kant als het voorwerp, waar de verlengden snijden'), ('Kenmerken', 'rechtop, vergroot, virtueel'), ('Toepassing', 'vergrootglas')], 'Rechtop, vergroot, virtueel.', opl_l3)}
{oef_fig('opl_5', 5, 'Constructie: voorwerp in 2F', 'Construeer het beeld en meet de grootte van het beeld en de beeldafstand. Bereken N.', op_l4, [
  ('Beeld', "in 2F': b = 6 cm"), ('Grootte', 'B = 2 cm, even groot als V'), ('N', 'N = b/v = 6/6 = 1')], 'Omgekeerd, even groot, reëel; N = 1.', opl_l4)}
{oef_fig('opl_5', 5, 'Constructie: groot voorwerp ver van de lens', 'Construeer het beeld vanuit de top van de pijl. Noteer de kenmerken. Meet B en b en bereken N.', op_ex[0], [
  ('Beeld', "tussen F' en 2F': b = 4,5 cm"), ('Kenmerken', 'omgekeerd, verkleind, reëel'), ('N', 'B = 1,5 cm, V = 3 cm: N = 0,5 (controle: b/v = 4,5/9 = 0,5)')], 'Omgekeerd, verkleind, reëel; N = 0,5.', opl_ex[0])}
{oef_fig('opl_5', 5, 'Constructie: klein voorwerp tussen F en 2F', 'Construeer het beeld vanuit de top van de pijl en noteer de kenmerken.', op_ex[1], [
  ('Beeld', "voorbij 2F': b = 7,5 cm"), ('Kenmerken', 'omgekeerd, vergroot, reëel'), ('N', 'N = 7,5 / 5 = 1,5: B = 2,25 cm')], 'Omgekeerd, vergroot, reëel.', opl_ex[1])}
{oef_fig('opl_5', 5, 'Constructie: voorwerp in F', 'Teken de hoofdstralen vanuit de top van de pijl. Wat stel je vast?', op_ex[2], [
  ('Stralen', 'na de lens lopen de gebroken stralen evenwijdig'), ('Beeld', 'ze snijden niet en ook hun verlengden niet: geen beeld')], 'Voorwerp in F: geen beeld (zaklamp, schijnwerper).', opl_ex[2])}
{oef_fig('opl_5', 5, 'Constructie: vergrootglas', 'Construeer het beeld vanuit de top van de pijl. Verleng de gebroken stralen. Noteer de kenmerken.', op_ex[3], [
  ('Gebroken stralen', 'lopen uit elkaar; verleng ze naar links'), ('Beeld', 'snijpunt van de verlengden: b = 6 cm aan dezelfde kant'), ('Kenmerken', 'rechtop, vergroot (N = 3), virtueel')], 'Rechtop, vergroot, virtueel: een vergrootglas.', opl_ex[3])}
{oef('opl_6', 6, 'Vergrotingsfactor berekenen', 'Bereken telkens N. Is het beeld vergroot of verkleind?<ol class="deelvragen" type="a"><li>B = 6,0 cm en V = 2,0 cm</li><li>b = 12 cm en v = 36 cm</li><li>b = 50 cm en v = 20 cm</li></ol>', [
  ('a', 'N = 6,0 / 2,0 = 3,0: vergroot'), ('b', 'N = 12 / 36 = 0,33: verkleind'), ('c', 'N = 50 / 20 = 2,5: vergroot')], 'N > 1: vergroot. N < 1: verkleind.')}
{oef('opl_7', 7, 'Omvormen', 'Bereken.<ol class="deelvragen" type="a"><li>N = 2,5 en V = 4,0 cm. Bereken B.</li><li>N = 0,50 en v = 24 cm. Bereken b.</li><li>B = 9,0 cm en N = 3,0. Bereken V.</li><li>b = 45 cm en N = 1,5. Bereken v.</li></ol>', [
  ('a', 'B = N · V = 2,5 · 4,0 cm = 10 cm'), ('b', 'b = N · v = 0,50 · 24 cm = 12 cm'), ('c', 'V = B / N = 9,0 / 3,0 = 3,0 cm'), ('d', 'v = b / N = 45 / 1,5 = 30 cm')], 'B = N · V en b = N · v.')}
{oef('opl_8', 8, 'Beamer in de klas', 'Een beamer maakt van een beeldje van 2,0 cm hoog een beeld van 1,2 m hoog op het scherm. Het scherm staat 3,0 m van de lens.<ol class="deelvragen" type="a"><li>Bereken N.</li><li>Hoe ver staat het beeldje van de lens?</li></ol>', [
  ('Gegeven', 'V = 2,0 cm · B = 1,2 m = 120 cm · b = 3,0 m = 300 cm'),
  ('a', 'N = B / V = 120 / 2,0 = 60'), ('b', 'v = b / N = 300 cm / 60 = 5,0 cm')], 'N = 60; het beeldje staat 5,0 cm van de lens (tussen F en 2F).')}
{oef('opl_9', 9, 'Redeneren: het voorwerp verschuift', 'Een voorwerp staat ver voor een bolle lens en komt langzaam dichter, tot tegen de lens. Beschrijf wat er met het beeld gebeurt. Gebruik de vijf posities.', [
  ('Voorbij 2F', 'klein, omgekeerd, reëel beeld tussen F\' en 2F\''), ('In 2F', 'even groot, omgekeerd, in 2F\''), ('Tussen F en 2F', 'groter, omgekeerd, verder dan 2F\''), ('In F', 'geen beeld'), ('Binnen F', 'rechtop, vergroot, virtueel, aan dezelfde kant')],
  'Hoe dichter bij F, hoe groter en verder het beeld; binnen F wordt het virtueel en rechtop.')}
{oef('opl_10', 10, 'Welke toepassing?', 'Welke positie van het voorwerp hoort bij de toepassing? Noteer de kenmerken van het beeld.<ol class="deelvragen" type="a"><li>een vergrootglas</li><li>een fototoestel</li><li>een kopieerapparaat dat op ware grootte kopieert</li><li>een zaklamp met een lens</li></ol>', [
  ('a', 'v < f: rechtop, vergroot, virtueel'), ('b', 'v > 2f: omgekeerd, verkleind, reëel'), ('c', 'v = 2f: omgekeerd, even groot, reëel'), ('d', 'lampje in F: geen beeld, evenwijdige bundel')], 'Elke toepassing hoort bij een positie.')}'''

h4_samenv = '''<p><b>Hoofdstralen</b>: evenwijdig → door F' · door O → rechtdoor · door F → evenwijdig.</p>
<p><b>Constructie</b>: minstens twee hoofdstralen vanuit de top van het voorwerp; snijpunt = top van het beeld. Komen ze niet samen: verlengden (virtueel beeld).</p>
<p>v &gt; 2f: omgekeerd, verkleind, reëel (fototoestel) · v = 2f: even groot (kopieerapparaat) · f &lt; v &lt; 2f: vergroot (beamer) · v = f: geen beeld · v &lt; f: rechtop, vergroot, virtueel (vergrootglas).</p>
<p><b>Vergrotingsfactor</b>: N = B / V = b / v (gelijkvormige driehoeken). Omvormen: B = N · V, b = N · v.</p>'''

maak('cursus-lenzen.html', 'Fysica 3de jaar · Thema 1 Optische fenomenen · Hoofdstuk 4', 'Lenzen',
     'Werk dit hoofdstuk samen met de tool <a href="optica.html">Optica</a>. Oefeningen maak je op papier.',
     h4_doelen, h4_vk, [('Lichtbreking bij bolle lenzen', h4_1), ('Beeldvorming bij bolle lenzen', h4_2), ('Vergrotingsfactor', h4_3)],
     h4_oef, h4_samenv, ('optica.html#s10', 'Oefen verder met de lens in de tool'))
print('ok')
