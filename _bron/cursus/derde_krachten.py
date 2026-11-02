# Cursus fysica 3de jaar (3NW) · Thema 2 Krachten · Hoofdstuk 2 Krachten (+ traagheid en beweging)
import sys, math
sys.argv = ['x']
from bouw import blok, denk, oef, tool, kader, figuur, bouw

# oude delen traagheid en beweging hergebruiken
ns = {}
exec(open('/tmp/oud_krachten.py').read().split("k_oef = f'''")[0].replace('k_cornell = d_cornell', ''), {**globals(), 'figuur': figuur, 'kader': kader, 'tool': tool, 'denk': denk}, ns)
k_traag = ns['k3'].replace("denk('denk_3'", "denk('denk_6'")
k_beweg_basis = ns['k4'].replace("denk('denk_4'", "denk('denk_7'").replace("denk('denk_5'", "denk('denk_8'")

k_beweg = k_beweg_basis.replace("denk('denk_4'", "denk('denk_7'").replace("denk('denk_5'", "denk('denk_8'") + kader('Traagheid en resulterende kracht in het dagelijks leven', '<p><b>Gordel en hoofdsteun.</b> Remt de auto plots, dan wil je lichaam even snel verder: de gordel houdt je tegen. Wordt de auto van achter aangereden, dan schiet de auto vooruit en blijft je hoofd achter: daarvoor dient de hoofdsteun.</p><p><b>Ketchup uit de fles.</b> Je beweegt de fles snel naar beneden en stopt plots. De fles stopt, maar de ketchup wil verder bewegen en schiet eruit.</p><p><b>Fietsen aan constante snelheid.</b> De trapkracht is even groot als de wrijving: F<sub>r</sub> = 0, de snelheid blijft gelijk.</p><p><b>Een ruimtesonde.</b> Met de motor uit vliegt ze jaren lang even snel rechtdoor: geen kracht nodig om te blijven bewegen.</p><p><b>Een auto in een bocht.</b> De wrijving tussen banden en weg wijst naar de binnenkant van de bocht (F<sub>r</sub> loodrecht op v). Op ijs is die te klein: de auto gaat rechtdoor.</p>') + tool('krachten-beweging.html#s6', 'Bekijk de voorbeelden met tekening in de tool')
B, G, R, INK, GRIJS = '#2563eb', '#059669', '#dc2626', '#1D2A36', '#64748b'
F = 'font-family="Inter,sans-serif"'
def svg(inner, w=600, h=200):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def t(x, y, s, kleur=INK, anker='middle', size=14, w=700):
    return f'<text x="{x}" y="{y}" fill="{kleur}" font-size="{size}" font-weight="{w}" text-anchor="{anker}" {F}>{s}</text>'
def pijl(x1, y1, x2, y2, kleur, b=4, dash=''):
    a = math.atan2(y2 - y1, x2 - x1); s = 13
    xa, ya = x2 - s * 0.8 * math.cos(a), y2 - s * 0.8 * math.sin(a)
    d = f' stroke-dasharray="{dash}"' if dash else ''
    kop = f'<path d="M{x2:.1f},{y2:.1f} L{x2 - s*math.cos(a-0.42):.1f},{y2 - s*math.sin(a-0.42):.1f} L{x2 - s*math.cos(a+0.42):.1f},{y2 - s*math.sin(a+0.42):.1f}Z" fill="{kleur}"/>'
    return f'<line x1="{x1}" y1="{y1}" x2="{xa:.1f}" y2="{ya:.1f}" stroke="{kleur}" stroke-width="{b}" stroke-linecap="round"{d}/>' + kop
def lijn(x1, y1, x2, y2, kleur='#94a3b8', b=1.6, dash='6 5'):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{kleur}" stroke-width="{b}" stroke-dasharray="{dash}"/>'
def punt(x, y, kleur=INK, r=5):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{kleur}"/>'
def sub(x):
    return f'<tspan baseline-shift="sub" font-size="10">{x}</tspan>'
CM = 24  # px per cm op de tekening (1 cm ≙ 10 N)

# ---------- figuren ----------
fig_effect = svg(
    '<rect width="600" height="200" fill="#fff"/>'
    # statisch: veer
    + t(150, 22, 'statisch effect: vorm verandert') +
    '<rect x="60" y="45" width="180" height="10" fill="#94a3b8"/>'
    '<path d="M150,55 l0,10 l-14,6 l28,8 l-28,8 l28,8 l-28,8 l28,8 l-14,6 l0,10" fill="none" stroke="#475569" stroke-width="3"/>'
    '<rect x="130" y="127" width="40" height="28" fill="#e7c9a9" stroke="#7c2d12" stroke-width="2"/>'
    + pijl(150, 141, 150, 190, R) + punt(150, 141, INK, 3.5) + t(165, 184, 'F', R, 'start') + t(150, 198, '', INK) +
    # dynamisch: bal
    t(450, 22, 'dynamisch effect: beweging verandert') +
    '<line x1="330" y1="150" x2="580" y2="150" stroke="#94a3b8" stroke-width="2"/>'
    '<circle cx="390" cy="132" r="18" fill="#f1f5f9" stroke="#475569" stroke-width="2"/>'
    + pijl(390, 132, 460, 132, R) + t(440, 122, 'F', R) +
    '<circle cx="520" cy="132" r="18" fill="none" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4 3"/>'
    + pijl(480, 175, 560, 175, B, 3) + t(520, 196, 'de bal begint te bewegen', B, 'middle', 12, 600), 600, 200)

fig_vector = svg(
    '<rect width="600" height="150" fill="#fff"/>' + lijn(30, 80, 580, 80) +
    punt(90, 80) + pijl(90, 80, 90 + 3.5 * CM * 3, 80, B, 5) +
    t(90, 108, 'aangrijpingspunt') + t(250, 64, 'lengte = grootte (1 cm ≙ 10 N)', B) +
    t(355, 108, 'zin: naar rechts') + t(510, 108, 'richting: horizontaal', GRIJS, 'middle', 13), 600, 150)

def kopstaart(F1, F2, titel, gegeven_tekst, res_tekst):
    # F1 naar rechts, F2 naar rechts (>0) of naar links (<0), zelfde aangrijpingspunt
    x0, s = 70, 0.08 * CM * 10 / 10  # 1 N -> 2,4 px (1 cm ≙ 10 N)
    s = CM / 10
    o = t(300, 20, titel)
    # gegeven
    o += t(130, 50, 'gegeven', GRIJS, 'middle', 12, 600)
    ox = 150 if F2 < 0 else 60
    dy = 0 if F2 < 0 else 5
    o += pijl(ox, 85 - dy, ox + F1 * s, 85 - dy, B) + t(ox + F1 * s / 2, 72, f'F₁ = {F1} N', B, 'middle', 13)
    o += pijl(ox, 85 + dy, ox + F2 * s, 85 + dy, G) + t(ox + F2 * s / 2, 112, f'F₂ = {abs(F2)} N', G, 'middle', 13) + f'<line x1="{ox}" y1="{85-dy-6}" x2="{ox}" y2="{85+dy+6}" stroke="{INK}" stroke-width="3"/>' + punt(ox, 85, INK, 4)
    # constructie
    cx = 350
    o += t(470, 50, 'kop-staart', GRIJS, 'middle', 12, 600)
    o += pijl(cx, 75, cx + F1 * s, 75, B) + pijl(cx + F1 * s, 92, cx + F1 * s + F2 * s, 92, G) + punt(cx, 75) + t(cx + F1 * s / 2, 66, 'F₁', B, 'middle', 13) + t(cx + F1 * s + F2 * s / 2, 110, 'F₂', G, 'middle', 13)
    o += lijn(cx + F1 * s, 70, cx + F1 * s, 98, '#94a3b8', 1.2, '3 3')
    Fr = F1 + F2
    o += pijl(cx, 130, cx + Fr * s, 130, R, 5) + punt(cx, 130) + t(cx + Fr * s / 2, 156, res_tekst, R, 'middle', 13)
    o += t(130, 156, gegeven_tekst, GRIJS, 'middle', 12, 600)
    return svg('<rect width="600" height="170" fill="#fff"/>' + o, 600, 170)

fig_zelfde = kopstaart(40, 30, 'Zelfde richting, zelfde zin', 'beide naar rechts', 'Fr = 40 N + 30 N = 70 N')
fig_tegen = kopstaart(60, -25, 'Zelfde richting, tegengestelde zin', 'F₁ naar rechts, F₂ naar links', 'Fr = 60 N − 25 N = 35 N, naar rechts')

fig_evenwicht = svg(
    '<rect width="600" height="150" fill="#fff"/>' + t(300, 20, 'Even grote, tegengestelde krachten: evenwicht') +
    '<line x1="120" y1="85" x2="480" y2="85" stroke="#a16207" stroke-width="4"/>'
    + punt(300, 85) + pijl(300, 85, 300 + 50 * CM / 10, 85, B) + pijl(300, 85, 300 - 50 * CM / 10, 85, G) +
    t(300 + 25 * CM / 10, 72, 'F₁ = 50 N', B, 'middle', 13) + t(300 - 25 * CM / 10, 72, 'F₂ = 50 N', G, 'middle', 13) +
    t(300, 125, 'Fr = 50 N − 50 N = 0 N', R), 600, 150)

def parall(F1, F2, hoek, titel, uitleg):
    s = CM / 10; ox, oy = 110, 170
    a = math.radians(hoek)
    p1 = (ox + F1 * s, oy); p2 = (ox + F2 * s * math.cos(a), oy - F2 * s * math.sin(a))
    pr = (p1[0] + p2[0] - ox, p1[1] + p2[1] - oy)
    o = t(300, 20, titel)
    o += lijn(*p1, *pr) + lijn(*p2, *pr)
    o += pijl(ox, oy, *p1, B) + pijl(ox, oy, *p2, G) + pijl(ox, oy, *pr, R, 5) + punt(ox, oy)
    o += t(p1[0] / 2 + ox / 2, oy + 22, 'F₁', B) + t(p2[0] / 2 + ox / 2 - 16, (p2[1] + oy) / 2, 'F₂', G, 'end')
    o += t((pr[0] + ox) / 2 - 14, (pr[1] + oy) / 2 - 10, 'Fr', R, 'end')
    o += t(ox - 8, oy + 20, 'O', INK, 'end', 13)
    if hoek == 90: o += f'<rect x="{ox}" y="{oy-12}" width="12" height="12" fill="none" stroke="{INK}"/>'
    for k, regel in enumerate(uitleg):
        o += t(400, 70 + 22 * k, regel, INK, 'start', 13, 500)
    return svg('<rect width="600" height="200" fill="#fff"/>' + o, 600, 200)

fig_lood = parall(40, 30, 90, 'Loodrechte krachten: parallellogram (hier een rechthoek)',
                  ['1. teken F₁ en F₂ vanuit O', '2. hulplijnen evenwijdig', '   met F₁ en F₂', '3. diagonaal vanuit O = Fr', '4. Fr = √(40² + 30²) = 50 N'])
fig_schuin = parall(50, 50, 60, 'Schuine krachten: parallellogrammethode',
                    ['F₁ = F₂ = 50 N, hoek 60°', 'diagonaal meten: 8,7 cm', 'Fr ≈ 87 N', '(schaal 1 cm ≙ 10 N)'])

def fig_ontbind():
    s = CM / 10; ox, oy = 120, 170; Fv = 50; a = math.radians(30)
    px, py = ox + Fv * s * math.cos(a), oy - Fv * s * math.sin(a)
    o = t(300, 20, 'Een koffer trekken: de kracht ontbinden in Fx en Fy')
    o += lijn(ox - 20, oy, ox + 200, oy, '#cbd5e1', 1.2, '') + lijn(ox, oy + 15, ox, oy - 120, '#cbd5e1', 1.2, '')
    o += lijn(px, py, px, oy) + lijn(px, py, ox, py)
    o += pijl(ox, oy, px, py, R, 5) + pijl(ox, oy, px, oy, B) + pijl(ox, oy, ox, py, G) + punt(ox, oy)
    o += t(px + 8, py - 4, 'F = 50 N', R, 'start') + t((ox + px) / 2, oy + 22, 'Fx ≈ 43 N', B) + t(ox - 10, (oy + py) / 2 + 4, 'Fy ≈ 25 N', G, 'end')
    for k, regel in enumerate(['1. teken de twee richtingen door O', '2. trek vanuit de kop van F', '   hulplijnen evenwijdig', '   met die richtingen', '3. de componenten lopen van O', '   tot de snijpunten', '4. meet en zet om met de schaal']):
        o += t(370, 62 + 21 * k, regel, INK, 'start', 13, 500)
    return svg('<rect width="600" height="200" fill="#fff"/>' + o, 600, 200)
fig_ontb = fig_ontbind()

# ---------- tekst ----------
lesdoelen = '''<p>Na dit hoofdstuk kan je:</p><ul class="doelen">
<li>het <b>statisch</b> en <b>dynamisch effect</b> van een kracht herkennen en noteren in concrete situaties;</li>
<li>een kracht definiëren als mogelijke oorzaak van <b>vormverandering</b> of van verandering in <b>bewegingstoestand</b>;</li>
<li>een kracht voorstellen als <b>vector</b> en de 4 kenmerken benoemen;</li>
<li>krachten tekenen als vectoren met een <b>schaal</b>, en met de schaal de <b>grootte</b> van een vector bepalen;</li>
<li>met een tekening of berekening de <b>resulterende kracht</b> bepalen van krachten met hetzelfde aangrijpingspunt, met dezelfde en/of verschillende richting en zin;</li>
<li>een kracht <b>ontbinden</b> volgens zijn componenten;</li>
<li>uitleggen wat <b>traagheid</b> is en de <b>traagheidswet</b> toepassen;</li>
<li>uit de resulterende kracht afleiden of de snelheid van een voorwerp <b>toeneemt, afneemt, gelijk blijft of van richting verandert</b>.</li></ul>'''

voorkennis = '<p>Dit moet je al kennen. Twijfel je? Herhaal het dan eerst.</p><ul><li><b>Grootheden en eenheden</b>: elke grootheid heeft een symbool en een SI-eenheid, bv. massa m in kg, kracht F in N (hoofdstuk Rekenen in de fysica).</li><li><b>Zwaartekracht</b>: F<sub>z</sub> = m · g met g = 9,81 N/kg.</li><li>Met een <b>lat</b> lengtes meten en met een <b>geodriehoek</b> hoeken meten en evenwijdige lijnen tekenen.</li><li><b>Stelling van Pythagoras</b> (wiskunde): in een rechthoekige driehoek is c² = a² + b².</li></ul>'

d1 = f'''<p>Je ziet een kracht niet. Je ziet wel wat ze doet: haar <b>effect</b>.</p>
{figuur(fig_effect, 'Links: een kracht rekt een veer uit (statisch effect). Rechts: een kracht zet een bal in beweging (dynamisch effect).')}
<table class="vb"><tr><td>Statisch effect</td><td>de <b>vorm</b> van het voorwerp verandert: uitrekken, indrukken, buigen</td></tr>
<tr><td>Dynamisch effect</td><td>de <b>bewegingstoestand</b> verandert: het voorwerp vertrekt, gaat sneller of trager, stopt of verandert van richting</td></tr></table>
<table class="vb"><tr><td>gewicht aan een veer</td><td>statisch</td><td>de zwaartekracht op het gewicht rekt de veer uit</td></tr>
<tr><td>spons indrukken</td><td>statisch</td><td>je hand drukt de spons in</td></tr>
<tr><td>plank buigt door</td><td>statisch</td><td>het gewicht van een persoon buigt de plank</td></tr>
<tr><td>bal wegtrappen</td><td>dynamisch</td><td>de bal lag stil en beweegt daarna: de snelheid wordt groter</td></tr>
<tr><td>fietser remt</td><td>dynamisch</td><td>de remkracht maakt de fiets trager</td></tr>
<tr><td>magneet en knikker</td><td>dynamisch</td><td>de magneet trekt een rollende stalen knikker opzij: de richting verandert</td></tr></table>
{kader('Definitie', '<p>Een <b>kracht</b> is de oorzaak van een <b>vormverandering</b> (statisch effect) of van een verandering in <b>bewegingstoestand</b> (dynamisch effect) van een voorwerp.</p>')}
<p>Soms zie je beide effecten tegelijk: een tennisbal die tegen het racket botst, wordt even platgedrukt (statisch) en vliegt terug (dynamisch).</p>
{tool('krachten-beweging.html#s0', 'Bekijk effecten van krachten in de tool')}
{denk('denk_1', 'Je duwt met al je kracht tegen de muur van de klas. De muur beweegt niet en je ziet niets veranderen. Werkt er dan wel een kracht?', [
  ('Is er een dynamisch effect?', 'Nee: de muur verandert niet van bewegingstoestand.'),
  ('Is er een statisch effect?', 'Ja, maar heel klein: de muur wordt een heel klein beetje ingedrukt. Je voelt het effect ook in je eigen handen, die platgedrukt worden.'),
  ('Besluit', 'Een kracht werkt ook als je het effect niet goed ziet.'),
], 'Ja, er werkt een kracht. Het effect is statisch en heel klein.')}'''

d2 = f'''<p>Een kracht heeft niet alleen een <b>grootte</b>, maar ook een <b>richting</b> en een <b>zin</b>. Daarom stellen we een kracht voor met een pijl: een <b>vector</b>. Het symbool is <b>F</b> met een pijltje erboven; de eenheid is de <b>newton (N)</b>.</p>
{figuur(fig_vector, 'De vier kenmerken van een krachtvector.')}
{kader('Kenmerken van een kracht', '<p><b>Aangrijpingspunt</b>: het punt waar de kracht op het voorwerp werkt. Daar begint de pijl.<br><b>Richting</b>: de rechte waarop de pijl ligt (horizontaal, verticaal, schuin onder een hoek …).<br><b>Zin</b>: naar welke kant de pijl wijst (naar links, naar boven …).<br><b>Grootte</b>: hoe groot de kracht is, in N. Op de tekening is dat de lengte van de pijl, op schaal.</p>')}
<h3>Een kracht tekenen op schaal</h3>
<ol><li>Kies een <b>schaal</b>, bv. 1 cm ≙ 10 N (lees: 1 cm stelt 10 N voor).</li>
<li>Bereken de <b>lengte</b>: grootte gedeeld door de schaalwaarde. 35 N : 10 N = 3,5 → 3,5 cm.</li>
<li>Duid het <b>aangrijpingspunt</b> aan met een stip.</li>
<li>Teken vanuit dat punt de pijl in de juiste <b>richting</b> en <b>zin</b>, met de berekende lengte.</li>
<li>Schrijf het symbool en de grootte bij de pijl: F = 35 N.</li></ol>
<p>De <b>zwaartekracht</b> teken je altijd vanuit het midden (zwaartepunt) van het voorwerp, verticaal naar beneden.</p>
<h3>De grootte aflezen</h3>
<p>Omgekeerd kan je uit een tekening de grootte bepalen: <b>meet de lengte</b> van de pijl en <b>vermenigvuldig</b> met de schaal. Een pijl van 4,2 cm met de schaal 1 cm ≙ 20 N stelt 4,2 · 20 N = 84 N voor.</p>
{tool('krachten-beweging.html#s0b', 'Oefen: een kracht tekenen op schaal')}
{denk('denk_2', 'Je tekent een kracht van 35 N met de schaal 1 cm ≙ 10 N. Je buur kiest 1 cm ≙ 5 N. Wie tekent de langste pijl? Hoe lang zijn beide pijlen?', [
  ('Schaal 1 cm ≙ 10 N', '35 N : 10 N = 3,5 → 3,5 cm'), ('Schaal 1 cm ≙ 5 N', '35 N : 5 N = 7 → 7,0 cm'),
  ('Vergelijk', 'Met een kleinere schaalwaarde wordt de pijl langer. De kracht zelf blijft even groot.')], 'De buur tekent een pijl van 7,0 cm, jij een pijl van 3,5 cm. Het is dezelfde kracht.')}'''

d3 = f'''<p>Werken er twee of meer krachten in hetzelfde aangrijpingspunt, dan kan je ze vervangen door <b>één kracht</b> die hetzelfde effect heeft: de <b>resulterende kracht F<sub>r</sub></b> (of krachtensom). Dat noem je krachten <b>samenstellen</b>.</p>
<h3>Zelfde richting, zelfde zin</h3>
{figuur(fig_zelfde, 'Kop-staartmethode: teken F₂ verder vanaf de kop van F₁. F<sub>r</sub> loopt van het begin van F₁ tot de kop van F₂.')}
<p>Tel de groottes op: <b>F<sub>r</sub> = F₁ + F₂</b>. F<sub>r</sub> heeft dezelfde richting en zin als de twee krachten.</p>
<p><b>Voorbeeld.</b> Twee leerlingen duwen een kast naar rechts, met 40 N en 30 N. F<sub>r</sub> = 40 N + 30 N = <b>70 N naar rechts</b>.</p>
{tool('krachten-construeren.html#1.1', 'Stap voor stap: zelfde zin')}
<h3>Zelfde richting, tegengestelde zin</h3>
{figuur(fig_tegen, 'Ook hier kop-staart: F₂ begint aan de kop van F₁ en wijst terug. F<sub>r</sub> loopt van het begin van F₁ tot de kop van F₂.')}
<p>Trek de kleinste grootte af van de grootste: <b>F<sub>r</sub> = F₁ − F₂</b> (F₁ is de grootste). F<sub>r</sub> heeft dezelfde richting en de <b>zin van de grootste kracht</b>.</p>
<p><b>Voorbeeld.</b> Een fietser trapt met een kracht van 60 N naar voor. Wind en wrijving werken samen met 25 N naar achter. F<sub>r</sub> = 60 N − 25 N = <b>35 N naar voor</b>.</p>
<p><b>Voorbeeld.</b> Een sleepboot op het kanaal in Brussel trekt een schip met 8000 N naar het noorden. De stroming en het water werken met 3000 N naar het zuiden. F<sub>r</sub> = 8000 N − 3000 N = <b>5000 N naar het noorden</b>.</p>
{figuur(fig_evenwicht, 'Zijn de twee tegengestelde krachten even groot, dan is de resulterende kracht nul.')}
<p>Zijn de tegengestelde krachten <b>even groot</b>, dan is <b>F<sub>r</sub> = 0</b>. De krachten zijn in <b>evenwicht</b>: bv. een boek op tafel (de zwaartekracht naar beneden en de kracht van de tafel naar boven) of twee even sterke teams bij touwtrekken.</p>
{tool('krachten-construeren.html#1.2', 'Stap voor stap: tegengestelde zin')}
<h3>Verschillende richting</h3>
{figuur(fig_lood, 'Twee loodrechte krachten: het parallellogram is een rechthoek. Bereken F<sub>r</sub> met Pythagoras.')}
<p>Gebruik de <b>parallellogrammethode</b>: teken beide krachten vanuit hetzelfde punt O. Teken met je geodriehoek door de kop van elke kracht een hulplijn evenwijdig met de andere kracht. De <b>diagonaal vanuit O</b> is F<sub>r</sub>. Meet de lengte en zet om met de schaal. Meet ook de hoek als je de richting moet geven.</p>
<p>Staan de krachten <b>loodrecht</b> op elkaar, dan kan je F<sub>r</sub> ook berekenen met de <b>stelling van Pythagoras</b>: <b>F<sub>r</sub> = √(F₁² + F₂²)</b>. Bv. 40 N en 30 N: F<sub>r</sub> = √(1600 + 900) = √2500 = 50 N.</p>
{figuur(fig_schuin, 'Twee schuine krachten van 50 N met een hoek van 60°: F<sub>r</sub> meet je op de tekening.')}
<p>Staan de krachten <b>niet loodrecht</b>, dan bepaal je F<sub>r</sub> met de tekening. F<sub>r</sub> is dan kleiner dan F₁ + F₂: de krachten werken maar voor een deel samen.</p>
{tool('krachten-construeren.html#2.1', 'Stap voor stap: loodrechte krachten')} {tool('krachten-construeren.html#2.2', 'Stap voor stap: schuine krachten')}
{kader('Overzicht: krachten samenstellen', '<p><b>Zelfde richting, zelfde zin</b>: F<sub>r</sub> = F₁ + F₂, zelfde zin.<br><b>Zelfde richting, tegengestelde zin</b>: F<sub>r</sub> = F₁ − F₂, zin van de grootste. Even groot: F<sub>r</sub> = 0 (evenwicht).<br><b>Loodrecht</b>: parallellogram, F<sub>r</sub> = √(F₁² + F₂²).<br><b>Schuin</b>: parallellogram, F<sub>r</sub> meten op de tekening.</p>')}
{denk('denk_3', 'Nora en Ilias trekken aan hetzelfde touw, elk met 100 N, maar in tegengestelde zin. Hoe groot is de resulterende kracht? Gebeurt er dan niets met het touw?', [
  ('Bereken F<sub>r</sub>', '100 N − 100 N = 0 N: de krachten zijn in evenwicht.'),
  ('Dynamisch effect?', 'Nee: het touw beweegt niet, want F<sub>r</sub> = 0.'),
  ('Statisch effect?', 'Ja: het touw staat strak gespannen en rekt een beetje uit. Elke kracht apart heeft een effect op de vorm.'),
], 'F<sub>r</sub> = 0: geen verandering van beweging, maar het touw wordt wel uitgerekt.')}
{denk('denk_4', 'Twee krachten van 30 N en 40 N werken op hetzelfde voorwerp. Hoe groot kan de resulterende kracht zijn? Wat is de kleinste en de grootste waarde?', [
  ('Grootste', 'Zelfde richting en zin: 30 N + 40 N = 70 N.'), ('Kleinste', 'Zelfde richting, tegengestelde zin: 40 N − 30 N = 10 N.'), ('Daartussen', 'Bij elke andere hoek ligt F<sub>r</sub> tussen 10 N en 70 N. Loodrecht: √(30² + 40²) = 50 N.')], 'F<sub>r</sub> ligt tussen 10 N en 70 N, afhankelijk van de hoek tussen de krachten.')}'''

d4 = f'''<p><b>Ontbinden</b> is het omgekeerde van samenstellen: je vervangt één kracht door <b>twee krachten</b> (de <b>componenten</b>) die samen hetzelfde effect hebben. Meestal ontbind je volgens twee loodrechte richtingen, bv. horizontaal en verticaal.</p>
{figuur(fig_ontb, 'Ontbinden: de kracht F is de diagonaal; de componenten zijn de zijden van het parallellogram.')}
<p>Je trekt een koffer met wieltjes met een kracht van 50 N, schuin omhoog onder 30° met de grond. Alleen de <b>horizontale component</b> F<sub>x</sub> ≈ 43 N trekt de koffer <b>vooruit</b>. De <b>verticale component</b> F<sub>y</sub> ≈ 25 N tilt de koffer een beetje <b>op</b>. Controle met Pythagoras: √(43² + 25²) ≈ 50 N. Hoe schuiner je trekt, hoe kleiner F<sub>x</sub>.</p>
<h3>Ontbinden in het dagelijks leven</h3>
<p>Vaak werkt maar één component van een kracht mee. Kijk welk deel van de kracht nuttig is.</p>
<table class="vb"><tr><td>Een grasmaaier duwen</td><td>Je duwt schuin naar beneden langs de stang. F<sub>x</sub> duwt de maaier vooruit. F<sub>y</sub> drukt hem tegen de grond: dat helpt niet om vooruit te gaan.</td></tr>
<tr><td>Een slee op een helling</td><td>De zwaartekracht wijst recht naar beneden. Je ontbindt ze langs de helling (de slee glijdt naar beneden) en loodrecht op de helling (de slee drukt tegen de helling). Hoe steiler de helling, hoe groter de component langs de helling.</td></tr>
<tr><td>Een lamp aan twee kabels</td><td>Je ontbindt de zwaartekracht op de lamp in de richting van elke kabel. De kabel die het steilst hangt, moet het meest dragen.</td></tr>
<tr><td>Natte was aan een waslijn</td><td>Hangt de waslijn bijna horizontaal, dan zijn de krachten in de lijn veel groter dan het gewicht van de was. Daarom kan een strak gespannen waslijn knappen.</td></tr></table>
<p>De gegeven richtingen hoeven dus niet loodrecht te zijn (de lamp, de waslijn): je kan een kracht volgens elke twee richtingen ontbinden met dezelfde methode.</p>
{tool('krachten-construeren.html#3.1', 'Stap voor stap: loodrechte componenten')} {tool('krachten-construeren.html#3.2', 'Stap voor stap: schuine componenten')}
{denk('denk_5', 'Je trekt een slee met een touw. Eerst hou je het touw bijna horizontaal, daarna trek je het touw steil omhoog, telkens met 50 N. Wanneer gaat de slee het best vooruit?', [
  ('Ontbind de kracht', 'Ontbind je trekkracht in een horizontale en een verticale component.'),
  ('Bijna horizontaal', 'Bijna de hele kracht is horizontaal: een grote component vooruit.'),
  ('Steil omhoog', 'Een groot deel van de kracht is verticaal. De horizontale component is klein.'),
], 'Met het touw bijna horizontaal is de horizontale component het grootst: de slee gaat dan het best vooruit.')}'''

oefs = f'''<p>Maak deze oefeningen <b>op papier</b>. Bij constructies gebruik je een lat en een geodriehoek. De oplossingen verschijnen hier nadat we de oefeningen in de les besproken hebben.</p>
<p><button class="knop licht" data-print="oef">🖨 Druk de oefeningen af</button></p>
{oef('opl_1', 1, 'Statisch of dynamisch?', 'Is het effect van de kracht statisch, dynamisch of allebei? Leg kort uit.<ol class="deelvragen" type="a"><li>Je knijpt in een stressbal.</li><li>Een doelman vangt een bal.</li><li>Een tram van de MIVB remt voor een halte.</li><li>Een pijl wordt afgeschoten met een boog.</li><li>Een auto botst tegen een paal.</li><li>Een fietser neemt een bocht.</li></ol>', [
  ('a', 'statisch: de vorm verandert'), ('b', 'dynamisch: de bal stopt'), ('c', 'dynamisch: de tram vertraagt'), ('d', 'allebei: de boog vervormt en de pijl begint te bewegen'), ('e', 'allebei: de auto krijgt een deuk en stopt'), ('f', 'dynamisch: de richting verandert')], 'Vorm verandert: statisch. Bewegingstoestand verandert: dynamisch.')}
{oef('opl_2', 2, 'Kenmerken', 'Je trekt aan een touw dat vastzit aan een kar, met een kracht van 80 N horizontaal naar rechts. Noteer de vier kenmerken van die kracht.', [
  ('Aangrijpingspunt', 'het punt waar het touw aan de kar vastzit'), ('Richting', 'horizontaal'), ('Zin', 'naar rechts'), ('Grootte', '80 N')], 'Aangrijpingspunt, richting, zin en grootte.')}
{oef('opl_3', 3, 'Tekenen op schaal', 'Teken op schaal.<ol class="deelvragen" type="a"><li>Een kracht van 250 N horizontaal naar links. Schaal: 1 cm ≙ 50 N.</li><li>De zwaartekracht op een boekentas van 6,0 kg. Schaal: 1 cm ≙ 20 N.</li></ol>', [
  ('a', '250 N : 50 N = 5 → een pijl van 5,0 cm naar links'), ('b', 'F<sub>z</sub> = 6,0 · 9,81 = 58,9 N; 58,9 : 20 = 2,9 → een pijl van 2,9 cm verticaal naar beneden, vanuit het midden van de boekentas')], 'Lengte = grootte : schaalwaarde.')}
{oef('opl_4', 4, 'Grootte aflezen', 'Bepaal de grootte van de kracht.<ol class="deelvragen" type="a"><li>Een pijl van 4,5 cm. Schaal: 1 cm ≙ 50 N.</li><li>Een pijl van 3,2 cm. Schaal: 1 cm ≙ 5 N.</li><li>Een pijl van 6,0 cm. Schaal: 1 cm ≙ 0,5 N.</li></ol>', [
  ('a', '4,5 · 50 N = 225 N'), ('b', '3,2 · 5 N = 16 N'), ('c', '6,0 · 0,5 N = 3,0 N')], 'Grootte = lengte · schaalwaarde.')}
{oef('opl_5', 5, 'Zelfde zin', 'Twee krachten van 30 N en 50 N werken op hetzelfde punt, in dezelfde richting en zin. Construeer F<sub>r</sub> met de schaal 1 cm ≙ 10 N en bereken F<sub>r</sub>.', [
  ('Constructie', 'F₁ = 3,0 cm, F₂ = 5,0 cm kop aan staart: F<sub>r</sub> = 8,0 cm.'), ('Berekening', 'F<sub>r</sub> = 30 N + 50 N = 80 N')], 'F<sub>r</sub> = 80 N, in dezelfde zin als beide krachten.')}
{oef('opl_6', 6, 'Tegengestelde zin', 'Op een kar werkt een kracht van 70 N naar rechts en een kracht van 25 N naar links, in hetzelfde punt. Construeer F<sub>r</sub> (1 cm ≙ 10 N) en bereken F<sub>r</sub>. Welke zin heeft F<sub>r</sub>?', [
  ('Constructie', 'F₁ = 7,0 cm naar rechts; vanaf de kop F₂ = 2,5 cm terug naar links. F<sub>r</sub> loopt van het begin van F₁ tot de kop van F₂: 4,5 cm.'),
  ('Berekening', 'F<sub>r</sub> = 70 N − 25 N = 45 N'), ('Zin', 'de zin van de grootste kracht: naar rechts')], 'F<sub>r</sub> = 45 N naar rechts.')}
{oef('opl_7', 7, 'Tegengestelde zin in het dagelijks leven', 'Bepaal telkens F<sub>r</sub> (grootte en zin).<ol class="deelvragen" type="a"><li>Een lift wordt met 12 000 N omhoog getrokken. De zwaartekracht op de lift is 10 000 N.</li><li>Een parachutist: zwaartekracht 800 N naar beneden, luchtweerstand 800 N naar boven.</li><li>Een duwbak op het kanaal: de motor duwt met 6000 N vooruit, het water remt met 7500 N.</li></ol>', [
  ('a', 'F<sub>r</sub> = 12 000 N − 10 000 N = 2000 N omhoog'), ('b', 'F<sub>r</sub> = 800 N − 800 N = 0 N: evenwicht'), ('c', 'F<sub>r</sub> = 7500 N − 6000 N = 1500 N naar achter')], 'Trek af en neem de zin van de grootste kracht.')}
{oef('opl_8', 8, 'Touwtrekken', 'Team A trekt met 4 kinderen van elk 150 N naar links. Team B trekt met 3 kinderen van elk 180 N naar rechts. Bereken F<sub>r</sub> op het touw. Welk team wint?', [
  ('Team A', '4 · 150 N = 600 N naar links'), ('Team B', '3 · 180 N = 540 N naar rechts'), ('F<sub>r</sub>', '600 N − 540 N = 60 N naar links')], 'F<sub>r</sub> = 60 N naar links: team A wint.')}
{oef('opl_9', 9, 'Loodrechte krachten', 'F₁ = 40 N werkt horizontaal naar rechts, F₂ = 30 N verticaal naar boven, in hetzelfde punt. Construeer F<sub>r</sub> met de parallellogrammethode (1 cm ≙ 10 N). Meet F<sub>r</sub> en controleer met de stelling van Pythagoras.', [
  ('Constructie', 'De diagonaal van de rechthoek (4,0 cm × 3,0 cm) is 5,0 cm lang.'), ('Pythagoras', 'F<sub>r</sub> = √(40² + 30²) = √2500 = 50 N')], 'F<sub>r</sub> = 50 N, schuin naar rechtsboven.')}
{oef('opl_10', 10, 'Schuine krachten', 'Twee krachten van elk 50 N werken in hetzelfde punt. De hoek tussen beide is 60°. Construeer F<sub>r</sub> met de parallellogrammethode (1 cm ≙ 10 N) en meet de grootte.', [
  ('Constructie', 'Het parallellogram is een ruit. De diagonaal meet ongeveer 8,7 cm.'), ('Controle', 'F<sub>r</sub> ligt tussen 0 N en 100 N en precies in het midden tussen beide krachten (30° met elk).')], 'F<sub>r</sub> ≈ 87 N')}
{oef('opl_11', 11, 'Ontbinden', 'Een kracht van 60 N werkt schuin naar rechtsboven, onder 45° met de horizontale. Ontbind de kracht in een horizontale en een verticale component (1 cm ≙ 10 N). Meet beide componenten en controleer met Pythagoras.', [
  ('Constructie', 'F = 6,0 cm onder 45°. Hulplijnen vanuit de kop: beide componenten meten ongeveer 4,2 cm.'), ('Grootte', 'F<sub>x</sub> ≈ F<sub>y</sub> ≈ 42 N'), ('Controle', '√(42² + 42²) ≈ 59 N ≈ 60 N')], 'F<sub>x</sub> ≈ 42 N en F<sub>y</sub> ≈ 42 N: onder 45° zijn beide componenten even groot.')}
{oef('opl_12', 12, 'Traagheid uitleggen', 'Leg telkens uit met het begrip traagheid.<ol class="deelvragen" type="a"><li>Waarom draag je een gordel in de auto?</li><li>Waarom kan je een tafelkleed snel wegtrekken zonder dat de borden vallen?</li><li>Waarom is een volle winkelkar moeilijker te stoppen dan een lege?</li></ol>', [
  ('a', 'Remt de auto plots, dan wil je lichaam even snel verder bewegen. De gordel houdt je tegen.'), ('b', 'De borden willen blijven stilstaan. Trek je snel, dan hebben ze geen tijd om mee te bewegen.'), ('c', 'De volle kar heeft een grotere massa, dus een grotere traagheid.')], 'Traagheid: een voorwerp wil blijven doen wat het deed.')}
{oef('opl_13', 13, 'Wat gebeurt er met de snelheid?', 'Bepaal telkens F<sub>r</sub> (grootte en zin). Zeg dan of de snelheid toeneemt, afneemt of gelijk blijft.<ol class="deelvragen" type="a"><li>Een auto rijdt rechtdoor. De motorkracht is 2000 N naar voor, de wrijving 2000 N naar achter.</li><li>Een fietser stopt met trappen. Alleen de wrijving van 30 N naar achter werkt nog.</li><li>Een slee staat stil. Een kind trekt met 40 N naar voor, de wrijving is 15 N.</li><li>Een ruimtesonde vliegt ver in de ruimte met uitgeschakelde motor.</li></ol>', [
  ('a', 'F<sub>r</sub> = 0 → snelheid blijft gelijk (ERB).'), ('b', 'F<sub>r</sub> = 30 N naar achter, tegen de beweging → snelheid neemt af.'), ('c', 'F<sub>r</sub> = 40 N − 15 N = 25 N naar voor → de slee begint te bewegen, de snelheid neemt toe.'), ('d', 'F<sub>r</sub> ≈ 0 → de sonde vliegt even snel rechtdoor.')], 'Vergelijk altijd de zin van F<sub>r</sub> met de zin van de beweging.')}
{oef('opl_14', 14, 'Juist of fout?', 'Juist of fout? Verbeter de foute uitspraken.<ol class="deelvragen" type="a"><li>Een voorwerp dat beweegt, heeft altijd een kracht nodig om te blijven bewegen.</li><li>Als F<sub>r</sub> = 0, dan staat het voorwerp zeker stil.</li><li>Een bal die je weggooit, krijgt een kracht mee van je hand.</li><li>Hoe groter de massa, hoe groter de traagheid.</li></ol>', [
  ('a', 'Fout: om te blijven bewegen is geen kracht nodig. Een kracht is nodig om de snelheid te veranderen.'), ('b', 'Fout: het voorwerp staat stil óf beweegt even snel rechtdoor.'), ('c', 'Fout: de kracht van je hand bestaat alleen zolang je de bal raakt.'), ('d', 'Juist.')], 'Alleen d is juist.')}
{tool('krachten-beweging.html#s7', 'Extra oefenen in de tool')}'''

samenv = kader('Samenvatting', '''<p>Een <b>kracht</b> veroorzaakt een vormverandering (<b>statisch effect</b>) of een verandering in bewegingstoestand (<b>dynamisch effect</b>).</p>
<p>Een kracht is een <b>vector</b>: aangrijpingspunt, richting, zin en grootte (N). Lengte op de tekening = grootte : schaalwaarde.</p>
<p><b>Samenstellen</b>: zelfde zin → F<sub>r</sub> = F₁ + F₂; tegengestelde zin → F<sub>r</sub> = F₁ − F₂, zin van de grootste (even groot: evenwicht); verschillende richting → parallellogrammethode (loodrecht: Pythagoras).</p>
<p><b>Ontbinden</b>: één kracht vervangen door twee componenten; de kracht is de diagonaal van het parallellogram.</p>
<p><b>Traagheid</b>: een voorwerp wil zijn snelheid behouden. Meer massa → meer traagheid.</p>
<p><b>Traagheidswet</b>: F<sub>r</sub> = 0 → rust of ERB. F<sub>r</sub> mee met v → sneller; tegen v → trager; loodrecht → bocht.</p>''')

delen = [('Effect van een kracht', d1), ('Een kracht is een vector', d2), ('Krachten samenstellen', d3), ('Krachten ontbinden', d4), ('Traagheid', k_traag), ('Resulterende kracht en beweging', k_beweg)]
blokken = [blok('lesdoelen', '', 'Lesdoelen', lesdoelen), blok('voorkennis', '', 'Voorkennis', voorkennis)]
blokken += [blok(f'deel{i}', i, kop, inh, f'deel{i}') for i, (kop, inh) in enumerate(delen, start=1)]
blokken += [blok('oefeningen', '', 'Oefeningen op papier', oefs, 'oefeningen'), blok('samenvatting', '', 'Samenvatting', samenv, 'samenvatting')]
vrij = [(f'deel{i}', i == 1, kop) for i, (kop, _) in enumerate(delen, start=1)]
vrij += [(f'denk_{i}', False, f'redenering denkvraag {i}') for i in range(1, 9)]
vrij += [('oefeningen', False, 'de oefeningen zelf (opgaven)')] + [(f'opl_{i}', False, f'oplossing oefening {i}') for i in range(1, 15)] + [('samenvatting', False, 'samenvatting')]
bouw('cursus-krachten-beweging.html', 'Fysica 3de jaar · Thema 2 Krachten · Hoofdstuk 2', 'Krachten',
     'Werk dit hoofdstuk samen met de tools <a href="krachten-beweging.html">Krachten en beweging</a> en <a href="krachten-construeren.html">Krachten samenstellen en ontbinden</a>. Oefeningen maak je op papier.',
     blokken, vrij, [])
print('ok')
