# Cursus fysica 4de jaar (4NW): Thema 1 Druk H2-H4, Thema 2 Energie en vermogen H1-H2
import sys
sys.argv = ['x']
from bouw import blok, denk, oef, tool, kader, figuur, bouw, STAP

F = 'font-family="Inter,sans-serif"'
INK, POS, BLAUW, GROEN, GRIJS = '#1D2A36', '#d64550', '#2563eb', '#16a34a', '#64748b'

def svg(inner, w=600, h=220):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def t(x, y, s, size=14, kleur=INK, anker='middle', w=400):
    return f'<text x="{x}" y="{y}" text-anchor="{anker}" font-size="{size}" font-weight="{w}" {F} fill="{kleur}">{s}</text>'
def pijl(x1, y1, x2, y2, kleur, b=4):
    import math
    a = math.atan2(y2 - y1, x2 - x1); s = 12
    xa, ya = x2 - s * 0.8 * math.cos(a), y2 - s * 0.8 * math.sin(a)
    kop = f'M{x2:.1f},{y2:.1f} L{x2 - s*math.cos(a-0.45):.1f},{y2 - s*math.sin(a-0.45):.1f} L{x2 - s*math.cos(a+0.45):.1f},{y2 - s*math.sin(a+0.45):.1f}Z'
    return f'<line x1="{x1}" y1="{y1}" x2="{xa:.1f}" y2="{ya:.1f}" stroke="{kleur}" stroke-width="{b * 0.5}" stroke-linecap="round"/><path d="{kop}" fill="{kleur}"/>'
def punt(x, y, kleur=INK):
    return f'<circle cx="{x}" cy="{y}" r="4" fill="{kleur}"/>'

def lesdoelen(*doelen):
    return '<p>Na dit hoofdstuk kan je:</p><ul class="doelen">' + ''.join(f'<li>{d}</li>' for d in doelen) + '</ul>'

def oefblok(inhoud, toolref=None):
    s = f'''<p>Maak deze oefeningen <b>op papier</b>, in je schrift. Gebruik telkens het stappenplan. De oplossingen verschijnen hier nadat we de oefeningen in de les besproken hebben.</p>
{STAP}
<p><button class="knop licht" data-print="oef">🖨 Druk de oefeningen af</button></p>
{inhoud}'''
    if toolref: s += tool(*toolref)
    return s

def voorkennis(*punten):
    return '<p>Dit moet je al kennen. Twijfel je? Herhaal het dan eerst.</p><ul>' + ''.join(f'<li>{x}</li>' for x in punten) + '</ul>'

def maak(bestand, eyebrow, titel, intro, delen, oefeningen, samenvatting, n_oef, toolref=None, vk=None):
    blokken = [blok('lesdoelen', '', 'Lesdoelen', delen[0])]
    if vk: blokken.append(blok('voorkennis', '', 'Voorkennis', vk))
    vrij = []
    for i, (kop, inhoud) in enumerate(delen[1:], start=1):
        blokken.append(blok(f'deel{i}', i, kop, inhoud, f'deel{i}'))
        vrij.append((f'deel{i}', i == 1, kop))
    blokken.append(blok('oefeningen', '', 'Oefeningen op papier', oefblok(oefeningen, toolref), 'oefeningen'))
    blokken.append(blok('samenvatting', '', 'Samenvatting', kader('Samenvatting', samenvatting), 'samenvatting'))
    n_denk = sum(inhoud.count('class="denk"') for _, inhoud in delen[1:])
    vrij += [(f'denk_{i}', False, f'redenering denkvraag {i}') for i in range(1, n_denk + 1)]
    vrij += [('oefeningen', False, 'de oefeningen zelf (opgaven)')] + [(f'opl_{i}', False, f'oplossing oefening {i}') for i in range(1, n_oef + 1)] + [('samenvatting', False, 'samenvatting')]
    bouw(bestand, eyebrow, titel, intro, blokken, vrij, [])

# =====================================================================
#  THEMA 1 · HOOFDSTUK 2: DRUK BIJ GASSEN
# =====================================================================
fig_glas = svg(
    '<rect x="0" y="0" width="600" height="230" fill="#fff"/>'
    # glas omgekeerd, gevuld met water
    '<path d="M230,30 L370,30 L360,150 L240,150 Z" fill="#cfe5f7" stroke="#475569" stroke-width="3"/>'
    + t(300, 95, 'water', 14, '#1e5a8a') +
    '<rect x="220" y="150" width="160" height="7" fill="#f3e3b5" stroke="#8a6d2b" stroke-width="1.5"/>'
    + t(430, 158, 'kaartje', 13, INK, 'start') +
    ''.join(f'<circle cx="{x}" cy="{y}" r="3.2" fill="#94a3b8"/>' for x, y in [(240,195),(270,210),(300,190),(330,205),(360,192),(255,180),(345,178),(300,212),(390,200),(210,205)])
    + t(110, 205, 'luchtdeeltjes botsen', 13, GRIJS) + t(110, 222, 'tegen het kaartje', 13, GRIJS) +
    pijl(300, 157, 300, 112, BLAUW) + punt(300, 157, BLAUW) + t(318, 130, 'F', 16, BLAUW, 'start', 700) + t(330, 135, 'lucht', 11, BLAUW, 'start')
    + t(300, 20, 'Een omgekeerd glas vol water met een kaartje eronder', 14, INK, 'middle', 700), 600, 230)

g_doelen = lesdoelen(
    'omschrijven hoe de <b>druk in een gas</b> ontstaat;',
    'verklaren waarom een <b>kaartje</b> onder een omgekeerd glas vol water blijft hangen;',
    'verklaren hoe een <b>zuignap</b> werkt;',
    'met het <b>deeltjesmodel</b> verklaren waarom de druk van een ingesloten gas toeneemt bij een hogere temperatuur;',
    'uitleggen van welke factoren de grootte van de <b>luchtdruk</b> afhangt;',
    'de <b>kracht</b> berekenen die een gas uitoefent op een oppervlak;',
    'noteren met welke toestellen je <b>luchtdruk</b> en <b>gasdruk</b> meet;',
    'uitleggen wat <b>overdruk</b> en <b>onderdruk</b> zijn en van een toepassing zeggen om welke van de twee het gaat;',
    'de grootte van de <b>normdruk</b> noteren en gebruiken in toepassingen.')

g1 = f'''<p>Een gas bestaat uit deeltjes die kriskras door elkaar bewegen. Ze botsen voortdurend tegen elkaar en tegen de wand van het vat. Bij elke botsing oefent een deeltje een kleine <b>kracht</b> uit op de wand. Al die botsingen samen zorgen voor een kracht op elke vierkante meter wand: dat is de <b>gasdruk</b>.</p>
{kader('Definitie', '<p>De <b>druk van een gas</b> ontstaat doordat de gasdeeltjes tegen de wand botsen en er zo een kracht op uitoefenen. De gasdruk is die kracht per oppervlakte-eenheid.</p>')}
<p>Let op de woorden: het zijn de <b>deeltjes</b> (of het gas) die een kracht uitoefenen. De druk zelf duwt niet: druk vertelt hoe groot de kracht is per m².</p>
<h3>Wanneer wordt de gasdruk groter?</h3>
<p>De druk in een gesloten vat wordt groter als de deeltjes vaker of harder tegen de wand botsen:</p>
<ul><li><b>meer deeltjes</b> in hetzelfde vat (je pompt een band op) → vaker botsingen → grotere druk;</li>
<li><b>kleiner volume</b> met dezelfde deeltjes (je duwt een fietspomp in) → vaker botsingen → grotere druk;</li>
<li><b>hogere temperatuur</b> → de deeltjes bewegen sneller → ze botsen vaker én harder → grotere druk.</li></ul>
{tool('druk.html#s3', 'Bekijk de botsende deeltjes in de tool')}
{denk('denk_1', 'Een gesloten spuitbus ligt in de zon op de vensterbank. Op de bus staat: "Niet blootstellen aan temperaturen boven 50 °C." Waarom is dat gevaarlijk?', [
  ('Wat gebeurt er met de deeltjes?', 'Door de warmte stijgt de temperatuur van het gas. De deeltjes bewegen sneller.'),
  ('Wat betekent dat voor de botsingen?', 'Ze botsen vaker en harder tegen de wand van de bus.'),
  ('Wat volgt daaruit?', 'De kracht per m² op de wand, dus de druk, wordt groter. Het volume van de bus kan niet mee groter worden.'),
], 'De druk in de bus stijgt zo sterk dat de bus kan openbarsten.')}'''

g2 = f'''<p>Rond de aarde ligt een laag lucht van vele kilometers dik. De luchtdeeltjes botsen tegen alles wat ze raken: tegen jou, tegen een muur, tegen het wateroppervlak. De druk die daardoor ontstaat, noem je de <b>luchtdruk</b> of <b>atmosferische druk</b>.</p>
<h3>Waarvan hangt de luchtdruk af?</h3>
<ul><li><b>Hoogte</b>: hoe hoger je komt, hoe minder lucht er boven je is en hoe ijler de lucht. De luchtdruk daalt. Aan de top van het Atomium is de luchtdruk al ongeveer 1 % lager dan op de grond; op de top van een hoge berg is hij veel lager.</li>
<li><b>Temperatuur en weer</b>: warme lucht stijgt op en zorgt vaak voor een lagere luchtdruk (lagedrukgebied: regen en wind); koude, dalende lucht geeft een hogere luchtdruk (hogedrukgebied: droog weer).</li></ul>
<h3>Kracht door een gas berekenen</h3>
<p>Ken je de druk van een gas, dan bereken je de kracht van het gas op een oppervlak met dezelfde formule als bij vaste stoffen:</p>
<div class="formule">F = p · A</div>
<p>Bv. de lucht oefent op een tafelblad van 1,0 m² een kracht uit van 101 300 Pa · 1,0 m² ≈ 1,0 · 10⁵ N. Dat is het gewicht van een massa van 10 ton! Het tafelblad breekt niet, want de lucht oefent ook langs onder een even grote kracht uit.</p>
{tool('druk.html#s4', 'Ontdek de luchtdruk in de tool')}
<h3>Het kaartje onder het glas</h3>
{figuur(fig_glas, 'De lucht onder het kaartje oefent een kracht naar boven uit op het kaartje. In het glas zit alleen water en geen lucht.')}
<p>Vul een glas helemaal met water, leg er een kaartje op en draai het om. Het kaartje valt niet. Onder het kaartje botsen luchtdeeltjes tegen het kaartje: de lucht oefent er een kracht naar boven op uit. In het glas zit geen lucht, enkel water. De kracht van de lucht naar boven is veel groter dan het gewicht van het water, dus het kaartje blijft hangen.</p>
<h3>De zuignap</h3>
<p>Druk je een zuignap tegen een tegel, dan duw je de lucht eronder weg. Onder de zuignap zitten dan bijna geen luchtdeeltjes meer: de druk is daar veel lager. Aan de buitenkant botsen wél veel luchtdeeltjes tegen de zuignap. De lucht buiten oefent dus een veel grotere kracht uit op de zuignap dan de lucht binnen. Daardoor zit de zuignap vast.</p>
{denk('denk_2', 'Waarom kan je met een rietje drinken? Je "zuigt" het drinken toch niet echt omhoog?', [
  ('Wat doe je met je mond?', 'Je maakt je mond groter en haalt lucht uit het rietje weg. In het rietje daalt de druk.'),
  ('Wat gebeurt er boven het drinken in het glas?', 'Daar blijft de luchtdruk gewoon even groot. De lucht oefent daar een kracht uit op het oppervlak van het drinken.'),
  ('Vergelijk.', 'Buiten het rietje is de druk op het drinken groter dan in het rietje. Het drinken wordt het rietje in geduwd door de lucht buiten het rietje.'),
], 'De lucht boven het glas duwt het drinken omhoog in het rietje, omdat de druk in het rietje lager is.')}'''

g3 = f'''<h3>Toestellen</h3>
<table class="vb"><tr><td>Barometer</td><td>meet de <b>luchtdruk</b> (de druk van de atmosfeer)</td></tr>
<tr><td>Manometer</td><td>meet de <b>druk van een gas in een vat</b>, bv. in een band, een gasfles of een snelkookpan</td></tr></table>
<p>Naast pascal (Pa) en hectopascal (hPa) zie je bij een manometer vaak de eenheid <b>bar</b>: 1 bar = 100 000 Pa = 1000 hPa.</p>
{kader('Normdruk', '<p>De gemiddelde luchtdruk op zeeniveau noem je de <b>normdruk</b>:</p><p><b>p₀ = 1013 hPa = 101 300 Pa ≈ 1 bar</b></p>')}
<h3>Overdruk en onderdruk</h3>
<p>Je vergelijkt de druk van een gas met de luchtdruk buiten:</p>
<ul><li><b>Overdruk</b>: de druk van het gas is <b>groter</b> dan de luchtdruk. Bv. een opgepompte band, een spuitbus, een snelkookpan, een fles bruisend water, een opgeblazen ballon.</li>
<li><b>Onderdruk</b>: de druk van het gas is <b>kleiner</b> dan de luchtdruk. Bv. onder een zuignap, in een rietje als je drinkt, in een stofzuiger, in vacuümverpakte koffie.</li></ul>
<p>Een bandenmanometer toont meestal de <b>overdruk</b>: hoeveel de druk in de band groter is dan de luchtdruk. Staat er 2,0 bar, dan is de druk in de band 2,0 bar + 1,0 bar = 3,0 bar.</p>
{tool('druk.html#s5', 'Oefen overdruk en onderdruk in de tool')}
{denk('denk_3', 'Een Brusselse koffiebranderij verpakt haar koffie vacuüm. Waarom voelt zo’n pak keihard aan, en wordt het zacht zodra je er een gaatje in prikt?', [
  ('Hoe groot is de druk in het pak?', 'Er is bijna alle lucht uit gezogen: in het pak is er onderdruk.'),
  ('Wat doet de lucht buiten?', 'Buiten botsen veel meer luchtdeeltjes tegen het pak. De lucht buiten oefent een veel grotere kracht uit dan de lucht binnen en drukt de koffie stevig samen.'),
  ('Wat verandert er met het gaatje?', 'Er stroomt lucht binnen tot de druk binnen en buiten gelijk is. De krachten binnen en buiten zijn dan even groot.'),
], 'Door de onderdruk drukt de lucht buiten het pak samen. Met een gaatje verdwijnt de onderdruk en wordt het pak zacht.')}'''

g_oef = f'''{oef('opl_1', 1, 'Omzetten', 'Zet om.<ol class="deelvragen" type="a"><li>1013 hPa = … Pa</li><li>2,5 bar = … Pa</li><li>95 kPa = … hPa</li><li>120 000 Pa = … bar</li></ol>', [
  ('a', '1013 · 100 = 101 300 Pa'), ('b', '2,5 · 100 000 = 250 000 Pa'), ('c', '95 kPa = 95 000 Pa = 950 hPa'), ('d', '120 000 / 100 000 = 1,2 bar')], '1 hPa = 100 Pa · 1 kPa = 1000 Pa · 1 bar = 100 000 Pa')}
{oef('opl_2', 2, 'Kracht op een raam', 'Een raam van een klaslokaal is 1,2 m breed en 0,80 m hoog. De luchtdruk is 101 300 Pa.<ol class="deelvragen" type="a"><li>Bereken de kracht die de buitenlucht op het raam uitoefent.</li><li>Waarom breekt het raam niet?</li></ol>', [
  ('Gegeven', 'p = 101 300 Pa · A = 1,2 m · 0,80 m = 0,96 m²'), ('Formule', 'F = p · A'),
  ('a', 'F = 101 300 Pa · 0,96 m² = 97 248 N ≈ 9,7 · 10⁴ N'),
  ('b', 'De lucht binnen oefent een even grote kracht uit in de andere zin. De twee krachten heffen elkaar op.')], 'F ≈ 9,7 · 10⁴ N, maar de lucht aan beide kanten oefent een even grote kracht uit.')}
{oef('opl_3', 3, 'De zuignap', 'Een zuignap heeft een oppervlakte van 12 cm². Neem aan dat er onder de zuignap geen lucht meer zit. De luchtdruk is 100 000 Pa.<ol class="deelvragen" type="a"><li>Hoe groot is de kracht van de buitenlucht op de zuignap?</li><li>Hoeveel kilogram zou je er in theorie aan kunnen hangen?</li></ol>', [
  ('Gegeven', 'p = 100 000 Pa · A = 12 cm² = 0,0012 m²'),
  ('a', 'F = p · A = 100 000 Pa · 0,0012 m² = 120 N'),
  ('b', 'm = F / g = 120 N / 9,81 N/kg = 12 kg')], 'F = 120 N; in theorie 12 kg. In werkelijkheid minder, want er sluipt altijd wat lucht onder de zuignap.')}
{oef('opl_4', 4, 'Overdruk of onderdruk?', 'Is er overdruk of onderdruk? Leg telkens kort uit.<ol class="deelvragen" type="a"><li>een opgepompte fietsband</li><li>drinken met een rietje</li><li>een stofzuiger die aanstaat</li><li>een spuitbus met slagroom</li><li>vacuümverpakte kaas</li><li>een fles bruisend water die nog dicht is</li></ol>', [
  ('a', 'overdruk: er is extra lucht in de band gepompt'), ('b', 'onderdruk in het rietje'), ('c', 'onderdruk in de stofzuiger: de lucht buiten duwt stof en lucht naar binnen'),
  ('d', 'overdruk: het gas duwt de slagroom naar buiten'), ('e', 'onderdruk: de lucht is eruit gezogen'), ('f', 'overdruk: er zit extra koolstofdioxide in')], 'Groter dan de luchtdruk: overdruk. Kleiner dan de luchtdruk: onderdruk.')}
{oef('opl_5', 5, 'Chips in het vliegtuig', 'Je neemt een gesloten zak chips mee op een vliegtuig. Hoog in de lucht staat de zak bol. Verklaar met het deeltjesmodel. In de cabine is de luchtdruk lager dan op de grond.', [
  ('In de zak', 'De lucht in de zak is ingesloten op de grond: daarin zitten nog evenveel deeltjes als op de grond.'),
  ('In de cabine', 'De luchtdruk in de cabine is lager: er botsen minder luchtdeeltjes per seconde tegen de buitenkant van de zak.'),
  ('Vergelijk', 'Binnen is de kracht op de wand van de zak groter dan buiten, dus de zak zet uit.')], 'De lucht in de zak oefent een grotere kracht uit dan de lucht in de cabine: de zak staat bol.')}
{oef('opl_6', 6, 'Band in de zomer', 'Kenza pompt ’s morgens haar fietsband op. ’s Middags staat de fiets in de volle zon. Wat gebeurt er met de druk in de band? Verklaar met het deeltjesmodel.', [
  ('Temperatuur', 'De lucht in de band warmt op: de deeltjes bewegen sneller.'),
  ('Botsingen', 'Ze botsen vaker en harder tegen de binnenkant van de band.'),
  ('Druk', 'De kracht per m² op de band neemt toe.')], 'De druk in de band stijgt.')}
{oef('opl_7', 7, 'Bandenmanometer', 'De manometer van een tankstation toont 2,2 bar voor een autoband. De luchtdruk is 1,0 bar.<ol class="deelvragen" type="a"><li>Toont de manometer de overdruk of de echte druk in de band?</li><li>Hoe groot is de echte druk in de band, in bar en in Pa?</li></ol>', [
  ('a', 'De overdruk: hoeveel de druk groter is dan de luchtdruk.'), ('b', 'p = 2,2 bar + 1,0 bar = 3,2 bar = 320 000 Pa')], 'De echte druk in de band is 3,2 bar = 3,2 · 10⁵ Pa.')}
{oef('opl_8', 8, 'Snelkookpan', 'In een snelkookpan is er een overdruk van 80 kPa. Het deksel heeft een oppervlakte van 0,050 m². Hoe groot is de extra kracht van het gas in de pan op het deksel, bovenop de kracht van de buitenlucht?', [
  ('Gegeven', 'p (overdruk) = 80 kPa = 80 000 Pa · A = 0,050 m²'), ('Gevraagd', 'F'), ('Formule', 'F = p · A'), ('Oplossing', 'F = 80 000 Pa · 0,050 m² = 4000 N')], 'F = 4,0 · 10³ N. Daarom moet het deksel goed vergrendeld zijn.')}
{oef('opl_9', 9, 'Het kaartje onder het glas', 'Je vult een glas helemaal met water, legt er een kaartje op en draait het glas om. Het kaartje valt niet. Leg uit waarom. Gebruik de woorden luchtdruk, kracht en oppervlakte.', [
  ('Onderkant', 'De lucht onder het kaartje oefent een kracht naar boven uit: F = p<sub>lucht</sub> · A.'), ('Bovenkant', 'In het glas zit alleen water, geen lucht. Het water drukt minder hard op het kaartje dan de lucht eronder.'), ('Besluit', 'De kracht van de lucht naar boven is groter dan de kracht van het water naar beneden.')],
  'De luchtdruk houdt het kaartje (en het water) op zijn plaats.')}
{oef('opl_10', 10, 'Luchtdruk in de bergen', 'In Brussel is de luchtdruk ongeveer 1013 hPa. Op de top van de Mont Blanc (4800 m) is ze ongeveer 550 hPa.<ol class="deelvragen" type="a"><li>Waarom is de luchtdruk op de berg kleiner?</li><li>Van welke andere factoren hangt de luchtdruk af?</li><li>Een zak chips die je in Brussel dichtmaakt, zwelt op de berg op. Leg uit.</li></ol>', [
  ('a', 'Hoger zit er minder lucht boven je: minder gewicht van de lucht, minder deeltjes per m³.'), ('b', 'van de temperatuur en het weer (hoge- en lagedrukgebieden)'), ('c', 'De lucht in de zak heeft nog 1013 hPa; buiten is het 550 hPa. De lucht binnen oefent een grotere kracht uit dan de lucht buiten.')],
  'Hoe hoger, hoe kleiner de luchtdruk.')}'''

g_samenv = '''<p>Gasdruk ontstaat doordat <b>gasdeeltjes tegen de wand botsen</b> en er een kracht op uitoefenen. Meer deeltjes, een kleiner volume of een hogere temperatuur → grotere druk.</p>
<p>De <b>luchtdruk</b> daalt met de hoogte en hangt af van temperatuur en weer. Kracht door een gas: <b>F = p · A</b>.</p>
<p>Kaartje en zuignap: de lucht aan de kant met de grootste druk oefent de grootste kracht uit.</p>
<p><b>Barometer</b>: luchtdruk. <b>Manometer</b>: gasdruk in een vat. <b>Normdruk</b>: p₀ = 1013 hPa ≈ 1 bar.</p>
<p><b>Overdruk</b>: groter dan de luchtdruk. <b>Onderdruk</b>: kleiner dan de luchtdruk.</p>'''

maak('cursus-druk-gassen.html', 'Fysica 4de jaar · Thema 1 Druk · Hoofdstuk 2', 'Druk bij gassen',
     'Werk dit hoofdstuk samen met de tool <a href="druk.html">Druk</a>. Oefeningen maak je op papier.',
     [g_doelen, ('Hoe ontstaat gasdruk?', g1), ('Luchtdruk, kaartje en zuignap', g2), ('Gasdruk meten: overdruk en onderdruk', g3)],
     g_oef, g_samenv, 10, ('druk.html#s12', 'Extra oefenen in de tool (kies: gassen)'),
     vk=voorkennis('Het <b>deeltjesmodel</b>: alle stoffen bestaan uit deeltjes die voortdurend bewegen. In een gas liggen de deeltjes ver uit elkaar en bewegen ze snel.', 'Hoe hoger de <b>temperatuur</b>, hoe sneller de deeltjes bewegen.', '<b>p = F / A</b> en omvormen: F = p · A (hoofdstuk 1).', 'Omzetten: cm² → m² (÷ 10 000), kPa → Pa (× 1000), hPa → Pa (× 100).'))

# =====================================================================
#  THEMA 1 · HOOFDSTUK 3: DRUK BIJ VLOEISTOFFEN
# =====================================================================
def straal(x, y, d):
    return f'<path d="M{x},{y} Q{x+d*0.55},{y-6} {x+d},{196}" fill="none" stroke="#3b82c4" stroke-width="3"/>'
fig_vat = svg(
    '<rect x="0" y="0" width="600" height="230" fill="#fff"/>'
    '<rect x="0" y="196" width="600" height="34" fill="#eef2f7"/>'
    '<rect x="120" y="40" width="90" height="156" fill="#cfe5f7" stroke="#475569" stroke-width="3"/>'
    + ''.join(f'<circle cx="210" cy="{y}" r="3.5" fill="#1e5a8a"/>' + straal(212, y, d) for y, d in [(80, 40), (125, 85), (170, 140)]) +
    t(165, 30, 'water', 13, '#1e5a8a') + t(400, 70, 'Hoe dieper het gaatje,', 14) + t(400, 90, 'hoe verder het water spuit:', 14) + t(400, 110, 'de hydrostatische druk', 14) + t(400, 130, 'neemt toe met de diepte.', 14), 600, 230)

fig_pers = svg(
    '<rect x="0" y="0" width="600" height="250" fill="#fff"/>'
    '<path d="M110,90 L110,200 L470,200 L470,110 L370,110 L370,170 L150,170 L150,90 Z" fill="#fde68a" stroke="#475569" stroke-width="3"/>'
    '<rect x="108" y="78" width="44" height="14" fill="#64748b"/>'
    '<rect x="368" y="98" width="104" height="14" fill="#64748b"/>'
    + pijl(130, 85, 130, 135, POS) + punt(130, 85, POS) + t(143, 125, 'F₁', 16, POS, 'start', 700) + t(90, 150, 'A₁', 14, INK, 'middle', 700) +
    pijl(420, 105, 420, 35, POS) + punt(420, 105, POS) + t(433, 50, 'F₂', 16, POS, 'start', 700) + t(490, 150, 'A₂', 14, INK, 'start', 700) +
    t(300, 230, 'kleine zuiger: kleine kracht · grote zuiger: grote kracht · overal dezelfde druk', 13, GRIJS), 600, 250)
# F1: kracht op de kleine zuiger (naar beneden); F2: kracht van de olie op de grote zuiger (naar boven)

v_doelen = lesdoelen(
    'uitleggen hoe <b>hydrostatische druk</b> ontstaat;',
    'noteren van welke factoren de hydrostatische druk <b>wel</b> en <b>niet</b> afhangt;',
    'van een tekening van een proefopstelling afleiden welke <b>factor</b> onderzocht wordt;',
    'beredeneren wat het effect is op de hydrostatische druk als één factor verandert;',
    'de formule <b>p<sub>h</sub> = ρ · g · h</b> gebruiken en omvormen om ρ, g en h te berekenen;',
    'het <b>beginsel van Pascal</b> noteren;',
    'uitleggen waarvan de <b>totale druk</b> in een vloeistof afhangt en die druk berekenen;',
    'uitleggen wat de functie is van een <b>hydraulisch systeem</b> en er krachten en oppervlakten mee berekenen.')

v1 = f'''<p>Duik je naar de bodem van een zwembad, dan voel je de druk op je oren toenemen. Boven je ligt een steeds dikkere laag water. Het gewicht van die laag water oefent een kracht uit op alles eronder. De druk die zo ontstaat, noem je de <b>hydrostatische druk</b>.</p>
{kader('Definitie', '<p>De <b>hydrostatische druk</b> is de druk in een vloeistof die ontstaat door het gewicht van de vloeistof boven dat punt.</p>')}
{figuur(fig_vat, 'Een vat met drie gaatjes: uit het onderste gaatje spuit het water het verst.')}
<h3>Waarvan hangt de hydrostatische druk af?</h3>
<table class="vb"><tr><td>wel</td><td>de <b>diepte h</b> onder het vloeistofoppervlak · de <b>massadichtheid ρ</b> van de vloeistof · de <b>zwaarteveldsterkte g</b></td></tr>
<tr><td>niet</td><td>de <b>vorm</b> van het vat · de <b>hoeveelheid</b> vloeistof · de <b>richting</b> waarin je meet (op dezelfde diepte is de druk in alle richtingen even groot)</td></tr></table>
<div class="formule">p<sub>h</sub> = ρ · g · h</div>
<table class="vb"><tr><td>p<sub>h</sub></td><td>hydrostatische druk, in pascal (Pa)</td></tr><tr><td>ρ</td><td>massadichtheid van de vloeistof, in kg/m³ (water: 1000 kg/m³)</td></tr><tr><td>g</td><td>zwaarteveldsterkte, in N/kg (op aarde 9,81 N/kg)</td></tr><tr><td>h</td><td>diepte onder het vloeistofoppervlak, in m</td></tr></table>
<p>Omvormen: <b>ρ = p<sub>h</sub> / (g · h)</b> &nbsp;·&nbsp; <b>g = p<sub>h</sub> / (ρ · h)</b> &nbsp;·&nbsp; <b>h = p<sub>h</sub> / (ρ · g)</b></p>
<h3>Proefopstelling lezen</h3>
<p>Met een drukdoosje en een U-buis meet je de druk in een vloeistof. Wil je één factor onderzoeken, dan verander je enkel die factor en hou je de rest gelijk. Kijk dus wat er tussen de tekeningen <b>verschilt</b>: de diepte, de vloeistof of de richting van het drukdoosje.</p>
<p>Vivaqua bewaart het Brusselse drinkwater in reservoirs die hoger liggen dan de huizen. Hoe groter het hoogteverschil tussen het water in het reservoir en jouw kraan, hoe groter de hydrostatische druk aan de kraan.</p>
{tool('druk.html#s6', 'Onderzoek de hydrostatische druk in de tool')}
{denk('denk_1', 'Je meet de hydrostatische druk op 2,0 m diepte in zoet water. Daarna meet je op 4,0 m diepte in zeewater, dat een iets grotere massadichtheid heeft. Is de druk 2 keer zo groot, iets meer of iets minder?', [
  ('Factor van h', 'h wordt × 2, dus p<sub>h</sub> wordt daardoor × 2.'),
  ('Factor van ρ', 'ρ van zeewater (ongeveer 1030 kg/m³) is iets groter dan die van zoet water. Ook dat maakt p<sub>h</sub> groter.'),
  ('Combineer', 'p<sub>h</sub> wordt × 2 · 1,03 ≈ × 2,06.'),
], 'De druk wordt iets meer dan 2 keer zo groot.')}'''

v2 = f'''{kader('Beginsel van Pascal', '<p>Een druk die je uitoefent op een ingesloten vloeistof, plant zich <b>onverminderd</b> en in <b>alle richtingen</b> voort door de hele vloeistof.</p>')}
<h3>Totale druk in een vloeistof</h3>
<p>Op het oppervlak van een open vloeistof botsen luchtdeeltjes: daar heerst de luchtdruk p₀. Volgens Pascal plant die druk zich door de hele vloeistof voort. Daarbij komt nog de hydrostatische druk. De <b>totale druk</b> op diepte h is dus:</p>
<div class="formule">p<sub>tot</sub> = p₀ + ρ · g · h</div>
<p>De totale druk hangt af van de <b>luchtdruk</b> boven de vloeistof en van de <b>hydrostatische druk</b> (dus van ρ, g en h). Omvormen: p<sub>h</sub> = p<sub>tot</sub> − p₀ en p₀ = p<sub>tot</sub> − p<sub>h</sub>.</p>
<h3>Hydraulische systemen</h3>
{figuur(fig_pers, 'Hydraulische pers: een kleine kracht op de kleine zuiger zorgt voor een grote kracht van de grote zuiger.')}
<p>In een hydraulisch systeem zit een vloeistof (meestal olie) tussen twee zuigers. Duw je op de kleine zuiger, dan ontstaat er een druk in de olie. Volgens Pascal is die druk overal even groot, ook onder de grote zuiger. Omdat de grote zuiger een grotere oppervlakte heeft, is de kracht daar groter.</p>
<div class="formule">F₁ / A₁ = F₂ / A₂</div>
<p>De <b>functie</b> van een hydraulisch systeem is dus een <b>kracht vergroten</b>. Voorbeelden: een garagekrik, de remmen van een auto, de arm van een graafmachine, de hefbrug in een garage. Is A₂ 50 keer zo groot als A₁, dan is ook F₂ 50 keer zo groot als F₁.</p>
{tool('druk.html#s7', 'Probeer de hydraulische pers in de tool')}
{denk('denk_2', 'Met een hydraulische krik til je met een kleine kracht een auto op. Krijg je dan energie "gratis"? Kijk naar hoe ver de zuigers bewegen.', [
  ('Hoeveel olie verplaatst?', 'Duw je de kleine zuiger naar beneden, dan duw je een bepaalde hoeveelheid olie weg. Diezelfde hoeveelheid olie komt onder de grote zuiger.'),
  ('Hoe ver beweegt de grote zuiger?', 'De grote zuiger is breder, dus diezelfde hoeveelheid olie tilt hem maar een klein stukje op.'),
  ('Besluit', 'Kleine kracht over een lange afstand aan de ene kant, grote kracht over een korte afstand aan de andere kant.'),
], 'Je wint kracht, maar je moet de kleine zuiger veel verder duwen. Energie krijg je niet gratis.')}'''

v_oef = f'''{oef('opl_1', 1, 'Zwembad', 'Bereken de hydrostatische druk op de bodem van een zwembad van 4,0 m diep.', [
  ('Gegeven', 'ρ = 1000 kg/m³ · g = 9,81 N/kg · h = 4,0 m'), ('Gevraagd', 'p<sub>h</sub>'), ('Formule', 'p<sub>h</sub> = ρ · g · h'), ('Oplossing', 'p<sub>h</sub> = 1000 · 9,81 · 4,0 = 39 240 Pa')], 'p<sub>h</sub> = 3,9 · 10⁴ Pa')}
{oef('opl_2', 2, 'Duiken in zee', 'Een duiker zwemt 10 m diep in zee (ρ = 1030 kg/m³). De luchtdruk is 101 300 Pa.<ol class="deelvragen" type="a"><li>Bereken de hydrostatische druk.</li><li>Bereken de totale druk.</li><li>Hoeveel keer zo groot is de totale druk als de luchtdruk?</li></ol>', [
  ('a', 'p<sub>h</sub> = 1030 · 9,81 · 10 = 101 043 Pa'), ('b', 'p<sub>tot</sub> = 101 300 + 101 043 = 202 343 Pa ≈ 2,02 · 10⁵ Pa'), ('c', '202 343 / 101 300 ≈ 2,0')], 'Op 10 m diepte in zee is de totale druk ongeveer 2 keer de luchtdruk.')}
{oef('opl_3', 3, 'Hoe diep?', 'Op welke diepte in water is de hydrostatische druk 50 kPa?', [
  ('Gegeven', 'p<sub>h</sub> = 50 kPa = 50 000 Pa · ρ = 1000 kg/m³ · g = 9,81 N/kg'), ('Formule', 'h = p<sub>h</sub> / (ρ · g)'), ('Oplossing', 'h = 50 000 / (1000 · 9,81) = 5,10 m')], 'h = 5,1 m')}
{oef('opl_4', 4, 'Welke vloeistof?', 'Op 20 cm diepte in een onbekende vloeistof meet je een hydrostatische druk van 1570 Pa. Bereken de massadichtheid van de vloeistof.', [
  ('Gegeven', 'p<sub>h</sub> = 1570 Pa · h = 20 cm = 0,20 m · g = 9,81 N/kg'), ('Formule', 'ρ = p<sub>h</sub> / (g · h)'), ('Oplossing', 'ρ = 1570 / (9,81 · 0,20) = 800 kg/m³')], 'ρ = 8,0 · 10² kg/m³ (bv. alcohol)')}
{oef('opl_5', 5, 'Op de maan', 'Een astronaut meet op de maan in een vat water op 1,0 m diepte een hydrostatische druk van 1620 Pa. Bereken de zwaarteveldsterkte op de maan.', [
  ('Gegeven', 'p<sub>h</sub> = 1620 Pa · ρ = 1000 kg/m³ · h = 1,0 m'), ('Formule', 'g = p<sub>h</sub> / (ρ · h)'), ('Oplossing', 'g = 1620 / (1000 · 1,0) = 1,62 N/kg')], 'g<sub>maan</sub> = 1,62 N/kg')}
{oef('opl_6', 6, 'Proefopstelling', 'Welke factor wordt onderzocht? Wat is het besluit?<ol class="deelvragen" type="a"><li>Het drukdoosje zit telkens 10 cm diep: eerst in water, daarna in zout water.</li><li>Het drukdoosje zit in water, eerst 5 cm, dan 10 cm, dan 15 cm diep.</li><li>Het drukdoosje zit telkens 10 cm diep in water, maar de opening wijst naar boven, opzij en naar onder.</li><li>Drie vaten met een verschillende vorm zijn tot dezelfde hoogte gevuld met water. Je meet de druk op de bodem.</li></ol>', [
  ('a', 'de massadichtheid: in zout water is de druk groter'), ('b', 'de diepte: hoe dieper, hoe groter de druk'),
  ('c', 'de richting: de druk is in alle richtingen even groot'), ('d', 'de vorm van het vat: de druk op de bodem is overal even groot')], 'De hydrostatische druk hangt af van ρ, g en h, niet van de richting en niet van de vorm of de hoeveelheid.')}
{oef('opl_7', 7, 'Redeneren', 'Wat gebeurt er met de hydrostatische druk? <ol class="deelvragen" type="a"><li>De diepte wordt 3 keer zo groot.</li><li>Je meet op dezelfde diepte in een vloeistof met een 2 keer zo kleine massadichtheid.</li><li>Je giet water bij in een breed vat, maar meet op dezelfde diepte onder het oppervlak.</li></ol>', [
  ('a', 'p<sub>h</sub> × 3'), ('b', 'p<sub>h</sub> × 1/2: de druk wordt 2 keer zo klein'), ('c', 'p<sub>h</sub> blijft gelijk: de diepte onder het oppervlak verandert niet')], 'p<sub>h</sub> is recht evenredig met ρ, g en h.')}
{oef('opl_8', 8, 'Garagekrik', 'In een garage in Anderlecht tilt een hydraulische krik een auto van 1200 kg op. De grote zuiger heeft een oppervlakte van 200 cm², de kleine zuiger 4,0 cm².<ol class="deelvragen" type="a"><li>Hoe groot moet de kracht van de grote zuiger zijn?</li><li>Welke kracht moet de garagist op de kleine zuiger uitoefenen?</li></ol>', [
  ('a', 'F₂ = m · g = 1200 · 9,81 = 11 772 N'),
  ('b', 'F₁ / A₁ = F₂ / A₂ → F₁ = F₂ · A₁ / A₂ = 11 772 · 4,0 / 200 = 235 N')], 'F₂ = 1,18 · 10⁴ N en F₁ = 2,4 · 10² N: 50 keer kleiner.')}
{oef('opl_9', 9, 'Reservoir', 'Het wateroppervlak in een drinkwaterreservoir ligt 40 m hoger dan een kraan op het gelijkvloers. Hoe groot is de hydrostatische druk aan die kraan als de kraan dicht is?', [
  ('Gegeven', 'ρ = 1000 kg/m³ · g = 9,81 N/kg · h = 40 m'), ('Formule', 'p<sub>h</sub> = ρ · g · h'), ('Oplossing', 'p<sub>h</sub> = 1000 · 9,81 · 40 = 392 400 Pa')], 'p<sub>h</sub> = 3,9 · 10⁵ Pa, bijna 4 keer de luchtdruk.')}'''

v_samenv = '''<p><b>Hydrostatische druk</b> ontstaat door het gewicht van de vloeistof erboven: <b>p<sub>h</sub> = ρ · g · h</b>.</p>
<p>Hangt af van diepte, massadichtheid en zwaarteveldsterkte; <b>niet</b> van vorm, hoeveelheid of richting.</p>
<p><b>Pascal</b>: een druk op een ingesloten vloeistof plant zich onverminderd in alle richtingen voort.</p>
<p><b>Totale druk</b>: p<sub>tot</sub> = p₀ + ρ · g · h.</p>
<p><b>Hydraulisch systeem</b>: vergroot een kracht. <b>F₁ / A₁ = F₂ / A₂</b>.</p>'''

maak('cursus-druk-vloeistoffen.html', 'Fysica 4de jaar · Thema 1 Druk · Hoofdstuk 3', 'Druk bij vloeistoffen',
     'Werk dit hoofdstuk samen met de tool <a href="druk.html">Druk</a>. Oefeningen maak je op papier.',
     [v_doelen, ('Hydrostatische druk', v1), ('Beginsel van Pascal en hydraulica', v2)],
     v_oef, v_samenv, 9, ('druk.html#s12', 'Extra oefenen in de tool (kies: vloeistoffen)'),
     vk=voorkennis('<b>Massadichtheid</b>: ρ = m / V, in kg/m³. Water: ρ = 1000 kg/m³.', '<b>Zwaartekracht</b>: F<sub>z</sub> = m · g met g = 9,81 N/kg.', '<b>p = F / A</b> (hoofdstuk 1) en de <b>luchtdruk</b>: normdruk p₀ = 1013 hPa (hoofdstuk 2).', 'Een formule met drie factoren omvormen, bv. a = b · c · d → b = a / (c · d).'))

# =====================================================================
#  THEMA 1 · HOOFDSTUK 4: ARCHIMEDESKRACHT
# =====================================================================
fig_blok = svg(
    '<rect x="0" y="0" width="600" height="260" fill="#fff"/>'
    '<rect x="20" y="40" width="560" height="210" fill="#dbeafe"/>' + t(560, 60, 'water', 13, '#1e5a8a', 'end') +
    # linkerdeel: drukkrachten op boven- en ondervlak
    '<rect x="90" y="100" width="120" height="90" fill="#e7c9a9" stroke="#7c2d12" stroke-width="2"/>'
    + pijl(150, 100, 150, 124, BLAUW, 3) + punt(150, 100, BLAUW) + t(222, 108, 'F', 15, BLAUW, 'start', 700) + t(232, 112, 'boven', 10, BLAUW, 'start') +
    pijl(150, 190, 150, 140, BLAUW, 3) + punt(150, 190, BLAUW) + t(222, 186, 'F', 15, BLAUW, 'start', 700) + t(232, 190, 'onder', 10, BLAUW, 'start') +
    t(150, 228, 'onderaan dieper → grotere druk', 12, GRIJS) +
    # rechterdeel: resultante
    '<rect x="380" y="100" width="120" height="90" fill="#e7c9a9" stroke="#7c2d12" stroke-width="2"/>'
    + pijl(440, 145, 440, 95, GROEN) + t(512, 104, 'F', 16, GROEN, 'start', 700) + t(523, 108, 'A', 11, GROEN, 'start') +
    pijl(440, 145, 440, 215, POS) + t(452, 214, 'F', 16, POS, 'start', 700) + t(463, 218, 'z', 11, POS, 'start') + punt(440, 145) +
    t(150, 28, 'drukkrachten op het blok', 14, INK, 'middle', 700) + t(440, 28, 'archimedeskracht en zwaartekracht', 14, INK, 'middle', 700), 600, 260)

a_doelen = lesdoelen(
    'noteren wat de <b>archimedeskracht</b> in vloeistoffen is;',
    'de kenmerken van de <b>archimedeskrachtvector</b> noteren;',
    'de formule <b>F<sub>A</sub> = ρ<sub>vl</sub> · g · V<sub>ond</sub></b> gebruiken en omvormen om ρ, g en V te berekenen;',
    'de formule voor de archimedeskracht verklaren aan de hand van een tekening;',
    'met de archimedeskracht en een krachtenbalans, en met de <b>massadichtheden</b> van voorwerp en vloeistof, uitleggen wanneer een voorwerp <b>zinkt, zweeft, stijgt of drijft</b>;',
    'uitleggen hoe een <b>vis</b> kan zinken, zweven of stijgen;',
    'uitleggen wat de wet van Archimedes bij <b>gassen</b> inhoudt en ze in formulevorm gebruiken;',
    'uitleggen wanneer een voorwerp in een gas zal <b>dalen, zweven of opstijgen</b>.')

def paneel(x0, titel, regel, yc, LA, LZ, drijft=False):
    s = f'<rect x="{x0}" y="70" width="140" height="150" fill="#dbeafe"/>'
    if drijft:
        s += f'<rect x="{x0+45}" y="50" width="50" height="50" fill="#e7c9a9" stroke="#7c2d12" stroke-width="2"/>'
        s += f'<line x1="{x0+45}" y1="70" x2="{x0+95}" y2="70" stroke="#3b82c4" stroke-width="1.5" stroke-dasharray="4,3"/>'
        xz, yz, ya = x0 + 63, 75, 85
        s += pijl(xz, yz, xz, yz + LZ, POS) + punt(xz, yz) + pijl(x0 + 77, ya, x0 + 77, ya - LA, GROEN) + punt(x0 + 77, ya, GROEN)
    else:
        s += f'<rect x="{x0+45}" y="{yc-25}" width="50" height="50" fill="#e7c9a9" stroke="#7c2d12" stroke-width="2"/>'
        s += pijl(x0 + 70, yc, x0 + 70, yc + LZ, POS) + pijl(x0 + 70, yc, x0 + 70, yc - LA, GROEN) + punt(x0 + 70, yc)
    s += t(x0 + 70, 20, titel, 14, INK, 'middle', 700) + t(x0 + 70, 240, regel, 12, GRIJS)
    return s
fig_vier = svg(
    '<rect x="0" y="0" width="600" height="250" fill="#fff"/>'
    + paneel(5, 'zinkt', 'ρ_v &gt; ρ_vl · F_A &lt; F_z', 160, 24, 58)
    + paneel(155, 'zweeft', 'ρ_v = ρ_vl · F_A = F_z', 140, 40, 40)
    + paneel(305, 'stijgt', 'ρ_v &lt; ρ_vl · F_A &gt; F_z', 150, 58, 24)
    + paneel(455, 'drijft', 'deels onder · F_A = F_z', 0, 34, 34, True)
    + t(300, 40, '', 1)
    + f'<g {F} font-size="12"><text x="20" y="62" fill="{GROEN}" font-weight="700">groen: F_A</text><text x="100" y="62" fill="{POS}" font-weight="700">rood: F_z</text></g>', 600, 250)
fig_vier = fig_vier.replace('ρ_vl', 'ρ<tspan baseline-shift="sub" font-size="9">vl</tspan>').replace('ρ_v', 'ρ<tspan baseline-shift="sub" font-size="9">v</tspan>').replace('F_A', 'F<tspan baseline-shift="sub" font-size="9">A</tspan>').replace('F_z', 'F<tspan baseline-shift="sub" font-size="9">z</tspan>')

PHET = 'https://phet.colorado.edu/nl/simulations/buoyancy'

a1 = f"""<p>Til je iemand op in het zwembad, dan lijkt die persoon veel lichter. Het water oefent een kracht naar boven uit op alles wat erin zit. Die kracht noem je de <b>archimedeskracht</b> (of opwaartse kracht).</p>
{figuur(fig_blok, 'Links: het water oefent op het ondervlak een grotere kracht uit dan op het bovenvlak. Rechts: het resultaat is de archimedeskracht naar boven.')}
<p>Neem een blok in water. Op het <b>bovenvlak</b> oefent het water een kracht naar beneden uit. Op het <b>ondervlak</b> oefent het water een kracht naar boven uit. Het ondervlak ligt dieper, dus daar is de hydrostatische druk groter en ook de kracht. De krachten op de zijvlakken heffen elkaar op. Wat overblijft is een kracht naar boven: de archimedeskracht.</p>
{kader('Definitie', '<p>De <b>archimedeskracht</b> is de kracht naar boven die een vloeistof (of gas) uitoefent op een voorwerp dat er geheel of gedeeltelijk in ondergedompeld is.</p>')}
{kader('Kenmerken van de archimedeskrachtvector', '<p><b>Aangrijpingspunt</b>: in het midden van het ondergedompelde deel van het voorwerp<br><b>Richting</b>: verticaal<br><b>Zin</b>: naar boven<br><b>Grootte</b>: dat onderzoek je in het volgende deel</p>')}
{tool('druk.html#s8', 'Bekijk in de tool waar de archimedeskracht vandaan komt')}"""

a_onderzoek = f"""<p>Waarvan hangt de grootte van de archimedeskracht af? Dat onderzoek je zelf met de simulatie <b>Buoyancy</b> van PhET. Kies het scherm waar je zelf de vloeistof, het voorwerp en de zwaartekracht kan instellen. Zet de krachten met hun waarde aan.</p>
{tool(PHET, 'Open de PhET-simulatie Buoyancy')}
{kader('Werkvorm: expertgroepen', '<p><b>Stap 1 · Expertgroep (15 min).</b> Elke groep onderzoekt één factor. Verander telkens enkel die factor en hou de rest gelijk. Noteer de metingen in een tabel in je schrift.</p><p><b>Stap 2 · Thuisgroep (10 min).</b> In elke nieuwe groep zit één expert van A, B, C en D. Elke expert legt zijn besluit uit met zijn tabel.</p><p><b>Stap 3 · Samen.</b> Combineer de vier besluiten tot één formule.</p>')}
<table class="vb">
<tr><td>Groep A</td><td><b>massadichtheid van de vloeistof</b></td><td>Hetzelfde blok, helemaal ondergedompeld. Wissel van vloeistof (bv. benzine, olie, water, honing). Noteer ρ<sub>vl</sub> en F<sub>A</sub>.</td></tr>
<tr><td>Groep B</td><td><b>ondergedompeld volume</b></td><td>Zelfde vloeistof. Laat het blok voor een kwart, de helft, drie kwart en helemaal onderdompelen, of kies blokken met een ander volume. Noteer V<sub>ond</sub> en F<sub>A</sub>.</td></tr>
<tr><td>Groep C</td><td><b>zwaarteveldsterkte</b></td><td>Hetzelfde blok in water, helemaal ondergedompeld. Kies een andere planeet of zwaartekracht. Noteer g en F<sub>A</sub>.</td></tr>
<tr><td>Groep D</td><td><b>massa van het voorwerp en diepte</b></td><td>Blokken met hetzelfde volume maar een ander materiaal (andere massa), helemaal onder water. Duw daarna één blok dieper. Noteer m, de diepte en F<sub>A</sub>.</td></tr></table>
<p><b>Tip</b>: wordt de factor 2 keer zo groot, kijk dan of F<sub>A</sub> ook 2 keer zo groot wordt. Dan is F<sub>A</sub> <b>recht evenredig</b> met die factor.</p>
{kader('Besluit van het onderzoek', '<p>F<sub>A</sub> is recht evenredig met de <b>massadichtheid van de vloeistof</b>, met het <b>ondergedompelde volume</b> en met de <b>zwaarteveldsterkte</b>.<br>F<sub>A</sub> hangt <b>niet</b> af van de massa of het materiaal van het voorwerp, en ook niet van de diepte zodra het voorwerp helemaal ondergedompeld is.</p>')}
<div class="formule">F<sub>A</sub> = ρ<sub>vl</sub> · g · V<sub>ond</sub></div>
<table class="vb"><tr><td>F<sub>A</sub></td><td>archimedeskracht, in N</td></tr><tr><td>ρ<sub>vl</sub></td><td>massadichtheid van de <b>vloeistof</b> (niet van het voorwerp!), in kg/m³</td></tr><tr><td>g</td><td>zwaarteveldsterkte, in N/kg</td></tr><tr><td>V<sub>ond</sub></td><td>volume van het <b>ondergedompelde deel</b> van het voorwerp, in m³</td></tr></table>
<p>ρ<sub>vl</sub> · V<sub>ond</sub> is de massa van de vloeistof die het voorwerp opzij duwt. De archimedeskracht is dus <b>even groot als het gewicht van de verplaatste vloeistof</b>.</p>
<h3>De formule verklaren met de tekening</h3>
<p>Kijk terug naar de tekening van het blok met grondvlak A en hoogte h. Het bovenvlak ligt op diepte h₁, het ondervlak op diepte h₂ = h₁ + h. Met F = p · A en p = ρ · g · h:</p>
<p>F<sub>A</sub> = F<sub>onder</sub> − F<sub>boven</sub> = ρ · g · h₂ · A − ρ · g · h₁ · A = ρ · g · (h₂ − h₁) · A = ρ · g · h · A = <b>ρ · g · V</b></p>
<p>Daarom maakt de diepte niet uit: dieper worden beide krachten groter, maar hun verschil blijft gelijk.</p>
<p>Omvormen: ρ<sub>vl</sub> = F<sub>A</sub> / (g · V<sub>ond</sub>) &nbsp;·&nbsp; g = F<sub>A</sub> / (ρ<sub>vl</sub> · V<sub>ond</sub>) &nbsp;·&nbsp; V<sub>ond</sub> = F<sub>A</sub> / (ρ<sub>vl</sub> · g). Denk aan omzetten: 1 dm³ = 1 L = 0,001 m³ en 1 cm³ = 1 mL = 10⁻⁶ m³.</p>
{denk('denk_1', 'Een ijzeren en een houten blokje hebben hetzelfde volume. Je duwt ze allebei helemaal onder water. Op welk blokje is de archimedeskracht het grootst?', [
  ('Wat staat er in de formule?', 'F<sub>A</sub> = ρ<sub>vl</sub> · g · V<sub>ond</sub>: de massadichtheid van de vloeistof, g en het ondergedompelde volume.'),
  ('Wat is gelijk?', 'Zelfde vloeistof (water), zelfde g, zelfde ondergedompeld volume.'),
  ('Wat speelt geen rol?', 'Het materiaal van het voorwerp staat niet in de formule (groep D).'),
], 'De archimedeskracht is op beide blokjes even groot. Het ijzer zinkt toch, omdat zijn zwaartekracht veel groter is.')}"""

a2 = f"""<p>Op een voorwerp in een vloeistof werken twee krachten: de <b>zwaartekracht F<sub>z</sub></b> naar beneden en de <b>archimedeskracht F<sub>A</sub></b> naar boven. Wat er gebeurt, hangt af van welke kracht het grootst is.</p>
<h3>Vergelijk de massadichtheden</h3>
<p>Is het voorwerp <b>helemaal ondergedompeld</b>, dan is V<sub>ond</sub> = V. Schrijf beide krachten met de massadichtheid:</p>
<p>F<sub>z</sub> = m · g = <b>ρ<sub>v</sub></b> · V · g &nbsp;&nbsp;en&nbsp;&nbsp; F<sub>A</sub> = <b>ρ<sub>vl</sub></b> · V · g</p>
<p>V en g zijn in beide formules gelijk. Welke kracht het grootst is, hangt dus enkel af van de <b>massadichtheid van het voorwerp ρ<sub>v</sub></b> en die van de <b>vloeistof ρ<sub>vl</sub></b>.</p>
{figuur(fig_vier, 'Krachten op een blok in een vloeistof. De zwaartekracht grijpt aan in het midden van het blok, de archimedeskracht in het midden van het ondergedompelde deel. Bij een drijvend blok zijn dat twee verschillende punten.')}
<table class="vb"><tr><td>ρ<sub>v</sub> &gt; ρ<sub>vl</sub></td><td>F<sub>A</sub> &lt; F<sub>z</sub></td><td>het voorwerp <b>zinkt</b></td></tr>
<tr><td>ρ<sub>v</sub> = ρ<sub>vl</sub></td><td>F<sub>A</sub> = F<sub>z</sub></td><td>het voorwerp <b>zweeft</b></td></tr>
<tr><td>ρ<sub>v</sub> &lt; ρ<sub>vl</sub></td><td>F<sub>A</sub> &gt; F<sub>z</sub></td><td>het voorwerp <b>stijgt</b></td></tr></table>
<p>Een voorwerp dat stijgt, komt aan het oppervlak en steekt er gedeeltelijk boven uit. Dan wordt V<sub>ond</sub> kleiner en dus ook F<sub>A</sub>, tot F<sub>A</sub> = F<sub>z</sub>. Het voorwerp <b>drijft</b>.</p>
<table class="vb"><tr><td>kurk</td><td>240 kg/m³</td><td>water</td><td>1000 kg/m³</td></tr>
<tr><td>eikenhout</td><td>ongeveer 700 kg/m³</td><td>zeewater</td><td>1030 kg/m³</td></tr>
<tr><td>ijs</td><td>917 kg/m³</td><td>spiritus</td><td>800 kg/m³</td></tr>
<tr><td>aluminium</td><td>2700 kg/m³</td><td>olijfolie</td><td>920 kg/m³</td></tr>
<tr><td>ijzer</td><td>7870 kg/m³</td><td>kwik</td><td>13 600 kg/m³</td></tr></table>
{kader('Drijven', '<p>Een drijvend voorwerp is in evenwicht: <b>F<sub>A</sub> = F<sub>z</sub></b>, dus ρ<sub>vl</sub> · g · V<sub>ond</sub> = ρ<sub>v</sub> · g · V. Daaruit volgt:</p><p><b>V<sub>ond</sub> / V = ρ<sub>v</sub> / ρ<sub>vl</sub></b></p><p>Het deel dat onder het oppervlak zit, is gelijk aan de verhouding van de massadichtheden. Hout van 700 kg/m³ zit voor 700/1000 = 70 % onder water.</p>')}
<p>Een binnenvaartschip in de haven van Brussel is van staal, en staal zinkt. Toch drijft het schip: het schip is hol, dus de <b>gemiddelde</b> massadichtheid van staal plus lucht in de romp is kleiner dan die van water. Laad je het schip vol, dan wordt F<sub>z</sub> groter. Het schip zakt dieper tot het genoeg extra water verplaatst.</p>
{tool('druk.html#s9', 'Laat voorwerpen zinken, zweven en drijven in de tool')}
{denk('denk_2', 'Een ijzeren bout zinkt in water. Gooi je dezelfde bout in een bak kwik, dan drijft hij. Hoe kan dat?', [
  ('Vergelijk met water', 'ρ<sub>ijzer</sub> = 7870 kg/m³ &gt; ρ<sub>water</sub> = 1000 kg/m³: F<sub>A</sub> &lt; F<sub>z</sub>, de bout zinkt.'),
  ('Vergelijk met kwik', 'ρ<sub>ijzer</sub> = 7870 kg/m³ &lt; ρ<sub>kwik</sub> = 13 600 kg/m³: helemaal ondergedompeld zou F<sub>A</sub> &gt; F<sub>z</sub>.'),
  ('Hoe diep zakt hij?', 'V<sub>ond</sub> / V = 7870 / 13 600 ≈ 0,58: iets meer dan de helft zit onder het kwikoppervlak.'),
], 'Of iets zinkt of drijft, hangt niet af van het voorwerp alleen, maar van ρ<sub>v</sub> tegenover ρ<sub>vl</sub>.')}
<h3>De vis en zijn zwemblaas</h3>
<p>Een vis heeft een <b>zwemblaas</b>: een zakje met gas in zijn buik. De massa van de vis verandert niet, dus F<sub>z</sub> blijft gelijk. Wel kan de vis het volume van de zwemblaas veranderen. Daarmee verandert hij zijn volume en dus zijn gemiddelde massadichtheid:</p>
<ul><li>zwemblaas groter → V<sub>ond</sub> groter → F<sub>A</sub> groter (ρ<sub>vis</sub> kleiner dan ρ<sub>water</sub>) → de vis <b>stijgt</b>;</li>
<li>zwemblaas kleiner → V<sub>ond</sub> kleiner → F<sub>A</sub> kleiner (ρ<sub>vis</sub> groter dan ρ<sub>water</sub>) → de vis <b>zinkt</b>;</li>
<li>F<sub>A</sub> precies gelijk aan F<sub>z</sub> (ρ<sub>vis</sub> = ρ<sub>water</sub>) → de vis <b>zweeft</b>.</li></ul>
{tool('druk.html#s10', 'Bestuur de vis in de tool')}
{denk('denk_3', 'Een duikboot werkt een beetje zoals een vis, maar het volume van de duikboot kan niet veranderen. Hoe kan een duikboot dan toch zinken en stijgen?', [
  ('Wat kan niet veranderen?', 'Het volume van de duikboot, dus ook F<sub>A</sub> als hij helemaal onder water is.'),
  ('Wat kan wél veranderen?', 'De massa: een duikboot heeft tanks die hij met zeewater kan vullen of met perslucht kan leegblazen.'),
  ('Krachtenbalans', 'Tanks vol water: F<sub>z</sub> &gt; F<sub>A</sub>, de duikboot zinkt. Tanks leeggeblazen: F<sub>z</sub> &lt; F<sub>A</sub>, hij stijgt.'),
], 'Een vis verandert F<sub>A</sub> (het volume), een duikboot verandert F<sub>z</sub> (de massa).')}"""

a3 = f'''<p>Ook een gas oefent een archimedeskracht uit. De wet van Archimedes geldt dus ook in lucht:</p>
<div class="formule">F<sub>A</sub> = ρ<sub>gas</sub> · g · V</div>
<p>Lucht heeft een kleine massadichtheid (ongeveer 1,29 kg/m³). Daarom is de archimedeskracht in lucht meestal klein en merk je ze niet. Voor een voorwerp met een groot volume en een kleine massa, zoals een ballon, maakt ze wel het verschil:</p>
<table class="vb"><tr><td>F<sub>A</sub> &lt; F<sub>z</sub></td><td>het voorwerp <b>daalt</b></td></tr><tr><td>F<sub>A</sub> = F<sub>z</sub></td><td>het voorwerp <b>zweeft</b></td></tr><tr><td>F<sub>A</sub> &gt; F<sub>z</sub></td><td>het voorwerp <b>stijgt op</b></td></tr></table>
<p>Een heliumballon stijgt op omdat helium veel lichter is dan lucht: de ballon met helium heeft een kleinere massa dan de lucht die hij verplaatst. Een heteluchtballon warmt de lucht in de ballon op. Warme lucht is ijler, dus de massa in de ballon wordt kleiner terwijl F<sub>A</sub> gelijk blijft.</p>
{tool('druk.html#s11', 'Laat een ballon opstijgen in de tool')}
{denk('denk_4', 'Een heteluchtballon zweeft boven het Zoniënwoud. De piloot wil dalen. Wat moet hij doen, en waarom?', [
  ('Wat is er nu aan de hand?', 'De ballon zweeft: F<sub>A</sub> = F<sub>z</sub>.'),
  ('Wat kan de piloot veranderen?', 'De temperatuur van de lucht in de ballon: de brander uitzetten of een klep openen.'),
  ('Wat gebeurt er dan?', 'De lucht in de ballon koelt af en wordt dichter: er komt koudere lucht bij, de massa in de ballon wordt groter. F<sub>z</sub> wordt groter dan F<sub>A</sub>.'),
], 'De piloot laat de lucht in de ballon afkoelen: de ballon wordt zwaarder en daalt.')}'''

a_oef = f'''{oef('opl_1', 1, 'Steen in water', 'Een steen met een volume van 0,50 dm³ ligt helemaal onder water. Bereken de archimedeskracht.', [
  ('Gegeven', 'V<sub>ond</sub> = 0,50 dm³ = 5,0 · 10⁻⁴ m³ · ρ<sub>vl</sub> = 1000 kg/m³ · g = 9,81 N/kg'), ('Formule', 'F<sub>A</sub> = ρ<sub>vl</sub> · g · V<sub>ond</sub>'), ('Oplossing', 'F<sub>A</sub> = 1000 · 9,81 · 5,0 · 10⁻⁴ = 4,9 N')], 'F<sub>A</sub> = 4,9 N')}
{oef('opl_2', 2, 'Zinkt de steen?', 'Dezelfde steen heeft een massa van 1,3 kg.<ol class="deelvragen" type="a"><li>Bereken de zwaartekracht op de steen.</li><li>Zinkt de steen? Leg uit met de krachtenbalans.</li><li>Hoe groot is de kracht die je nodig hebt om de steen onder water omhoog te houden?</li></ol>', [
  ('a', 'F<sub>z</sub> = 1,3 · 9,81 = 12,8 N'), ('b', 'F<sub>z</sub> = 12,8 N &gt; F<sub>A</sub> = 4,9 N: de steen zinkt.'), ('c', 'F = F<sub>z</sub> − F<sub>A</sub> = 12,75 − 4,91 = 7,8 N')], 'Onder water heb je maar 7,8 N nodig in plaats van 12,8 N.')}
{oef('opl_3', 3, 'Volume berekenen', 'Op een voorwerp dat helemaal onder water zit, werkt een archimedeskracht van 2,0 N. Bereken het volume van het voorwerp in cm³.', [
  ('Formule', 'V<sub>ond</sub> = F<sub>A</sub> / (ρ<sub>vl</sub> · g)'), ('Oplossing', 'V = 2,0 / (1000 · 9,81) = 2,04 · 10⁻⁴ m³ = 204 cm³')], 'V = 2,0 · 10² cm³')}
{oef('opl_4', 4, 'Welke vloeistof?', 'Een blokje van 100 cm³ zit helemaal ondergedompeld in een vloeistof. De archimedeskracht is 0,78 N. Bereken de massadichtheid van de vloeistof.', [
  ('Gegeven', 'V<sub>ond</sub> = 100 cm³ = 1,00 · 10⁻⁴ m³ · F<sub>A</sub> = 0,78 N · g = 9,81 N/kg'), ('Formule', 'ρ<sub>vl</sub> = F<sub>A</sub> / (g · V<sub>ond</sub>)'), ('Oplossing', 'ρ<sub>vl</sub> = 0,78 / (9,81 · 1,00 · 10⁻⁴) = 795 kg/m³')], 'ρ<sub>vl</sub> = 8,0 · 10² kg/m³')}
{oef('opl_5', 5, 'Zinken, zweven of stijgen?', 'Drie voorwerpen worden helemaal onder water geduwd en losgelaten. Bereken telkens F<sub>z</sub> en F<sub>A</sub> en zeg wat er gebeurt.<ol class="deelvragen" type="a"><li>m = 200 g, V = 250 cm³</li><li>m = 300 g, V = 300 cm³</li><li>m = 500 g, V = 200 cm³</li></ol>', [
  ('a', 'F<sub>z</sub> = 0,200 · 9,81 = 1,96 N · F<sub>A</sub> = 1000 · 9,81 · 2,50 · 10⁻⁴ = 2,45 N → stijgt (en gaat drijven)'),
  ('b', 'F<sub>z</sub> = 2,94 N · F<sub>A</sub> = 2,94 N → zweeft'),
  ('c', 'F<sub>z</sub> = 4,91 N · F<sub>A</sub> = 1,96 N → zinkt')], 'Vergelijk F<sub>A</sub> met F<sub>z</sub> (of ρ<sub>voorwerp</sub> met ρ<sub>vl</sub>).')}
{oef('opl_6', 6, 'Binnenvaartschip', 'Een binnenvaartschip met een massa van 1500 ton drijft in het kanaal in Brussel (ρ = 1000 kg/m³).<ol class="deelvragen" type="a"><li>Hoe groot is de archimedeskracht op het schip?</li><li>Hoeveel m³ water verplaatst het schip?</li><li>Het schip laadt 500 ton zand. Hoeveel water verplaatst het nu?</li></ol>', [
  ('a', 'Het schip drijft: F<sub>A</sub> = F<sub>z</sub> = 1 500 000 · 9,81 = 1,47 · 10⁷ N'),
  ('b', 'V<sub>ond</sub> = F<sub>A</sub> / (ρ · g) = m / ρ = 1 500 000 / 1000 = 1500 m³'),
  ('c', 'm = 2000 ton → V<sub>ond</sub> = 2 000 000 / 1000 = 2000 m³')], 'Een drijvend schip verplaatst zijn eigen massa aan water: 1500 m³, en 2000 m³ als het geladen is.')}
{oef('opl_7', 7, 'De vis', 'Leg met de krachtenbalans uit wat een vis doet met zijn zwemblaas om (a) naar de bodem te zakken en (b) op dezelfde diepte te blijven.', [
  ('a', 'Zwemblaas kleiner maken → V kleiner → F<sub>A</sub> kleiner dan F<sub>z</sub> → de vis zinkt.'),
  ('b', 'Het volume zo regelen dat F<sub>A</sub> = F<sub>z</sub> → de vis zweeft.')], 'De vis verandert zijn volume en dus F<sub>A</sub>; F<sub>z</sub> blijft gelijk.')}
{oef('opl_8', 8, 'Heliumballon', 'Een heliumballon heeft een volume van 6,0 L. De ballon met het helium heeft een massa van 5,0 g. De massadichtheid van lucht is 1,29 kg/m³.<ol class="deelvragen" type="a"><li>Bereken de archimedeskracht op de ballon.</li><li>Bereken de zwaartekracht op de ballon.</li><li>Stijgt de ballon?</li></ol>', [
  ('a', 'V = 6,0 L = 6,0 · 10⁻³ m³ → F<sub>A</sub> = 1,29 · 9,81 · 6,0 · 10⁻³ = 0,076 N'),
  ('b', 'F<sub>z</sub> = 0,0050 · 9,81 = 0,049 N'), ('c', 'F<sub>A</sub> &gt; F<sub>z</sub>: de ballon stijgt op.')], 'De ballon stijgt: F<sub>A</sub> = 0,076 N &gt; F<sub>z</sub> = 0,049 N.')}
{oef('opl_9', 9, 'Heteluchtballon', 'Een heteluchtballon heeft een volume van 2500 m³. De buitenlucht heeft een massadichtheid van 1,2 kg/m³.<ol class="deelvragen" type="a"><li>Bereken de archimedeskracht.</li><li>Hoe groot mag de totale massa (ballon, mand, mensen én de warme lucht erin) ten hoogste zijn om te kunnen opstijgen?</li></ol>', [
  ('a', 'F<sub>A</sub> = 1,2 · 9,81 · 2500 = 29 430 N'), ('b', 'Opstijgen als F<sub>z</sub> &lt; F<sub>A</sub>: m &lt; F<sub>A</sub> / g = 29 430 / 9,81 = 3000 kg')], 'F<sub>A</sub> = 2,9 · 10⁴ N; de totale massa moet kleiner zijn dan 3,0 · 10³ kg.')}'''

a_oef += f'''
{oef('opl_10', 10, 'Zinkt het of drijft het?', 'Gebruik de tabel met massadichtheden. Zinkt of drijft het voorwerp in water, in spiritus en in kwik?<ol class="deelvragen" type="a"><li>een kurk</li><li>een kaars (paraffine, 900 kg/m³)</li><li>een blokje aluminium</li><li>een ijzeren spijker</li></ol>', [
  ('a', 'kurk (240): drijft in water, spiritus en kwik'), ('b', 'kaars (900): drijft in water en kwik, zinkt in spiritus (800)'),
  ('c', 'aluminium (2700): zinkt in water en spiritus, drijft in kwik'), ('d', 'ijzer (7870): zinkt in water en spiritus, drijft in kwik')], 'ρ<sub>v</sub> &lt; ρ<sub>vl</sub>: drijven · ρ<sub>v</sub> &gt; ρ<sub>vl</sub>: zinken.')}
{oef('opl_11', 11, 'Het topje van de ijsberg', 'Een ijsberg (ρ = 917 kg/m³) drijft in zeewater (ρ = 1030 kg/m³). Welk deel van de ijsberg zit onder water? Welk deel steekt erboven uit?', [
  ('Drijven', 'F<sub>A</sub> = F<sub>z</sub> → V<sub>ond</sub> / V = ρ<sub>v</sub> / ρ<sub>vl</sub>'), ('Oplossing', 'V<sub>ond</sub> / V = 917 / 1030 = 0,89')], 'Ongeveer 89 % zit onder water, maar 11 % steekt erboven uit.')}
{oef('opl_12', 12, 'Krachten tekenen', 'Teken telkens het voorwerp in de vloeistof met F<sub>z</sub> en F<sub>A</sub>. Let op het aangrijpingspunt en op de lengte van de pijlen.<ol class="deelvragen" type="a"><li>een stalen kogel die naar de bodem zakt (nog in het water)</li><li>een vis die op dezelfde diepte zweeft</li><li>een houten blok (700 kg/m³) dat drijft in water</li></ol>', [
  ('a', 'Kogel helemaal onder water. Beide pijlen starten in het midden van de kogel. F<sub>z</sub> naar beneden is veel langer dan F<sub>A</sub> naar boven (ρ<sub>staal</sub> ≈ 8 keer ρ<sub>water</sub>, dus F<sub>z</sub> ≈ 8 keer F<sub>A</sub>).'),
  ('b', 'Vis helemaal onder water. Beide pijlen starten in het midden van de vis en zijn even lang.'),
  ('c', '70 % van het blok onder water. F<sub>z</sub> start in het midden van het blok, F<sub>A</sub> in het midden van het ondergedompelde deel (dus lager). Beide pijlen zijn even lang.')], 'Zinken: F<sub>z</sub> langer · zweven en drijven: even lang · F<sub>A</sub> grijpt aan in het midden van het ondergedompelde deel.')}
{oef('opl_13', 13, 'De formule verklaren', 'Een blok hangt volledig onder water. Teken de krachten die het water op de bovenkant en op de onderkant uitoefent. Leg met je tekening uit waarom er een archimedeskracht naar boven is, en waarom die gelijk is aan het gewicht van de verplaatste vloeistof.', [
  ('Tekening', 'Op de bovenkant een kracht naar beneden, op de onderkant een grotere kracht naar boven; de krachten op de zijkanten heffen elkaar op.'), ('Waarom', 'De onderkant ligt dieper: daar is de hydrostatische druk groter, dus de kracht naar boven is groter.'),
  ('Formule', 'Verschil = ρ<sub>vl</sub> · g · (h<sub>onder</sub> − h<sub>boven</sub>) · A = ρ<sub>vl</sub> · g · V<sub>ond</sub>: dat is het gewicht van de vloeistof die het blok opzij duwt.')],
  'De archimedeskracht ontstaat door het drukverschil tussen onder- en bovenkant.')}'''

a_samenv = '''<p>De <b>archimedeskracht</b> is de opwaartse kracht van een vloeistof of gas op een ondergedompeld voorwerp. Ze ontstaat doordat de druk onderaan groter is dan bovenaan.</p>
<p><b>F<sub>A</sub> = ρ<sub>vl</sub> · g · V<sub>ond</sub></b>: even groot als het gewicht van de verplaatste vloeistof. Aangrijpingspunt in het midden van het ondergedompelde deel, verticaal, naar boven.</p>
<p>Helemaal ondergedompeld vergelijk je de massadichtheden: ρ<sub>v</sub> &gt; ρ<sub>vl</sub> <b>zinkt</b> · ρ<sub>v</sub> = ρ<sub>vl</sub> <b>zweeft</b> · ρ<sub>v</sub> &lt; ρ<sub>vl</sub> <b>stijgt</b>. Drijvend: V<sub>ond</sub> / V = ρ<sub>v</sub> / ρ<sub>vl</sub>.</p>
<p>Met krachten: F<sub>A</sub> &lt; F<sub>z</sub> <b>zinkt</b> · F<sub>A</sub> = F<sub>z</sub> <b>zweeft</b> · F<sub>A</sub> &gt; F<sub>z</sub> <b>stijgt</b>. Drijven: F<sub>A</sub> = F<sub>z</sub> met een deel boven het oppervlak.</p>
<p>Vis: verandert met de zwemblaas zijn volume en dus F<sub>A</sub>.</p>
<p>In een gas: <b>F<sub>A</sub> = ρ<sub>gas</sub> · g · V</b>; dalen, zweven of opstijgen.</p>'''

maak('cursus-archimedes.html', 'Fysica 4de jaar · Thema 1 Druk · Hoofdstuk 4', 'Archimedeskracht',
     'Werk dit hoofdstuk samen met de tool <a href="druk.html">Druk</a>. Oefeningen maak je op papier.',
     [a_doelen, ('Waar komt de archimedeskracht vandaan?', a1), ('Onderzoek: waarvan hangt de archimedeskracht af?', a_onderzoek), ('Zinken, zweven, stijgen en drijven', a2), ('Archimedeskracht in gassen', a3)],
     a_oef, a_samenv, 13, ('druk.html#s12', 'Extra oefenen in de tool (kies: archimedeskracht)'),
     vk=voorkennis('<b>Hydrostatische druk</b>: p<sub>h</sub> = ρ · g · h; dieper → grotere druk (hoofdstuk 3).', '<b>F = p · A</b> (hoofdstuk 1).', '<b>Massadichtheid</b> ρ = m / V en volumes omzetten: 1 L = 1 dm³ = 0,001 m³, 1 mL = 1 cm³ = 10⁻⁶ m³.', '<b>Krachten</b>: een kracht is een vector en begint op het voorwerp. Twee tegengestelde krachten: de resulterende kracht is het verschil. Resulterende kracht nul: evenwicht.'))

# =====================================================================
#  THEMA 2 · HOOFDSTUK 1: ENERGIE IN SYSTEMEN
# =====================================================================
e_doelen = lesdoelen(
    'het verschil uitleggen tussen een <b>open</b>, <b>gesloten</b> en <b>geïsoleerd</b> systeem;',
    'uitleggen waarom een <b>zwaarteveld</b>, een <b>magnetisch veld</b> en een <b>elektrisch veld</b> potentiële energie bevatten;',
    'in voorbeelden uit het dagelijks leven de <b>energieomzetting</b> noteren met gravitationele, elastische, kinetische, chemische, thermische, stralings-, kern- en elektrische energie;',
    'uitleggen hoe een <b>waterreservoir op een heuvel</b> energie kan opslaan;',
    'de formules voor <b>gravitationele potentiële energie</b>, <b>kinetische energie</b> en <b>elastische potentiële energie</b> gebruiken en omvormen.')

e1 = f'''<p>Wil je energie bestuderen, dan kies je eerst een <b>systeem</b>: het deel van de wereld waar je naar kijkt, bv. een pot soep, een fiets met fietser of een gsm. Alles daarbuiten is de <b>omgeving</b>. Tussen systeem en omgeving kunnen energie en materie uitgewisseld worden.</p>
<table class="vb"><tr><td>Open systeem</td><td>wisselt <b>energie én materie</b> uit met de omgeving</td><td>een kokende pot zonder deksel: warmte gaat naar buiten en waterdamp ontsnapt</td></tr>
<tr><td>Gesloten systeem</td><td>wisselt <b>enkel energie</b> uit, geen materie</td><td>een pot met een goed sluitend deksel: warmte gaat erin en eruit, het water blijft erin</td></tr>
<tr><td>Geïsoleerd systeem</td><td>wisselt <b>niets</b> uit: geen energie en geen materie</td><td>een (ideale) thermosfles die goed dicht is</td></tr></table>
<p>Een volmaakt geïsoleerd systeem bestaat in werkelijkheid niet: ook een thermosfles koelt na een tijd af. Het is een model dat je gebruikt als de uitwisseling heel klein is.</p>
{tool('energie-vermogen.html#s1', 'Vergelijk de drie systemen in de tool')}
{tool('energie-vermogen.html#s2', 'Oefen: welk systeem is het?')}
{denk('denk_1', 'Is een mens een open, gesloten of geïsoleerd systeem?', [
  ('Wisselt een mens energie uit?', 'Ja: je geeft warmte af aan de omgeving en je neemt energie op via voedsel.'),
  ('Wisselt een mens materie uit?', 'Ja: je eet, drinkt, ademt in en uit en zweet.'),
  ('Besluit', 'Er is uitwisseling van energie én materie.'),
], 'Een mens is een open systeem.')}'''

e2 = f'''<p>Til je een boek op, dan krijgt het energie: laat je het los, dan valt het en krijgt het snelheid. Die energie zat "opgeslagen" omdat het boek zich in het <b>zwaarteveld</b> van de aarde bevindt. In een veld werkt er een kracht op afstand. Verplaats je een voorwerp tegen die kracht in, dan sla je energie op in het systeem. Die energie noem je <b>potentiële energie</b>.</p>
<ul><li><b>Zwaarteveld</b>: de aarde trekt aan elke massa. Een voorwerp hoger tillen slaat gravitationele potentiële energie op.</li>
<li><b>Magnetisch veld</b>: twee magneten trekken elkaar aan. Trek je ze uit elkaar, dan sla je energie op. Laat je los, dan klikken ze tegen elkaar.</li>
<li><b>Elektrisch veld</b>: een positieve en een negatieve lading trekken elkaar aan. Haal je ze uit elkaar, dan sla je elektrische potentiële energie op.</li></ul>
{kader('Potentiële energie in een veld', '<p>Een veld oefent een kracht uit op afstand. Verplaats je een voorwerp tegen die kracht in, dan neemt de <b>potentiële energie</b> toe. Laat je los, dan doet de kracht het voorwerp bewegen en wordt die energie omgezet, bv. in kinetische energie.</p>')}
{tool('energie-vermogen.html#s3', 'Bekijk potentiële energie in de drie velden')}
{denk('denk_2', 'Twee magneten stoten elkaar af. Wanneer bevat dit systeem de meeste potentiële energie: als de magneten dicht bij elkaar of ver uit elkaar zijn?', [
  ('Welke kracht werkt er?', 'De magneten stoten elkaar af: de kracht duwt ze uit elkaar.'),
  ('Wanneer doe je moeite?', 'Je moet tegen die kracht in werken om ze dichter bij elkaar te brengen.'),
  ('Wat gebeurt er bij loslaten?', 'Laat je ze dicht bij elkaar los, dan vliegen ze uit elkaar: de opgeslagen energie wordt kinetische energie.'),
], 'Dicht bij elkaar bevat het systeem de meeste potentiële energie.')}'''

e3 = f'''<h3>Vormen van energie</h3>
<table class="vb"><tr><td>gravitationele potentiële energie</td><td>door de hoogte in het zwaarteveld</td><td>water achter een stuwdam</td></tr>
<tr><td>elastische potentiële energie</td><td>door vervorming</td><td>een uitgerekte elastiek, een ingedrukte veer</td></tr>
<tr><td>kinetische energie</td><td>door beweging</td><td>een rijdende tram</td></tr>
<tr><td>chemische energie</td><td>opgeslagen in stoffen</td><td>voedsel, benzine, een batterij</td></tr>
<tr><td>thermische energie</td><td>door de beweging van de deeltjes (temperatuur)</td><td>warm water</td></tr>
<tr><td>stralingsenergie</td><td>energie van licht en andere straling</td><td>zonlicht</td></tr>
<tr><td>kernenergie</td><td>opgeslagen in atoomkernen</td><td>uranium in een kerncentrale</td></tr>
<tr><td>elektrische energie</td><td>door elektrische stroom</td><td>stroom uit het stopcontact</td></tr></table>
{kader('Wet van behoud van energie', '<p>Energie kan niet ontstaan en niet verdwijnen. Ze kan enkel <b>omgezet</b> worden van de ene vorm in de andere of <b>overgedragen</b> worden van het ene voorwerp naar het andere.</p>')}
<h3>Energieomzettingen</h3>
<p>Een tram van de MIVB zet <b>elektrische energie</b> om in <b>kinetische energie</b>; een deel wordt <b>thermische energie</b> (de motor en de remmen warmen op). Een zonnepaneel op een dak in Schaarbeek zet <b>stralingsenergie</b> om in <b>elektrische energie</b>. Fietsen: de <b>chemische energie</b> uit je voedsel wordt <b>kinetische energie</b> en thermische energie (je krijgt het warm).</p>
{tool('energie-vermogen.html#s5', 'Stel energieketens op in de tool')}
<h3>Energie opslaan in een waterreservoir op een heuvel</h3>
<p>Stroom kan je moeilijk in grote hoeveelheden bewaren. Een <b>pompcentrale</b>, zoals die van Coo in de Ardennen, gebruikt twee waterbekkens op een verschillende hoogte:</p>
<ul><li>Is er een <b>overschot</b> aan elektrische energie (bv. ’s nachts of als het hard waait), dan pompen elektrische pompen water naar het bovenste bekken: <b>elektrische energie → gravitationele potentiële energie</b>.</li>
<li>Is er een <b>tekort</b>, dan stroomt het water naar beneden door een turbine met generator: <b>gravitationele potentiële energie → kinetische energie → elektrische energie</b>.</li></ul>
<p>Er gaat telkens een deel verloren als thermische energie (wrijving in de leidingen, de pomp en de turbine).</p>
{tool('energie-vermogen.html#s6', 'Bedien de pompcentrale in de tool')}
{denk('denk_3', 'Een leerling zegt: "Bij een pompcentrale verdwijnt er energie, want je krijgt minder elektrische energie terug dan je erin stopt." Klopt dat met de wet van behoud van energie?', [
  ('Wat zegt de wet?', 'Energie kan niet verdwijnen, enkel omgezet worden.'),
  ('Waar gaat het verschil naartoe?', 'Een deel van de energie wordt thermische energie door wrijving in de leidingen, de pomp en de turbine.'),
  ('Herformuleer', 'De energie is niet weg, maar ze is niet meer in een nuttige vorm.'),
], 'De energie verdwijnt niet: een deel wordt thermische energie. Die is wel niet meer nuttig.')}'''

e4 = f'''<table class="vb"><tr><td>Gravitationele potentiële energie</td><td><b>E<sub>pot,g</sub> = m · g · h</b></td><td>m in kg · g in N/kg · h in m</td></tr>
<tr><td>Kinetische energie</td><td><b>E<sub>k</sub> = ½ · m · v²</b></td><td>m in kg · v in m/s</td></tr>
<tr><td>Elastische potentiële energie</td><td><b>E<sub>pot,el</sub> = ½ · k · x²</b></td><td>k: veerconstante in N/m · x: uitrekking of indrukking in m</td></tr></table>
<p>Energie druk je uit in <b>joule</b> (J). Let op: v en x staan in het <b>kwadraat</b>. Een 2 keer zo grote snelheid geeft een 4 keer zo grote kinetische energie.</p>
<h3>Omvormen</h3>
<p>m = E<sub>pot,g</sub> / (g · h) &nbsp;·&nbsp; h = E<sub>pot,g</sub> / (m · g)<br>
m = 2 · E<sub>k</sub> / v² &nbsp;·&nbsp; v = √(2 · E<sub>k</sub> / m)<br>
k = 2 · E<sub>pot,el</sub> / x² &nbsp;·&nbsp; x = √(2 · E<sub>pot,el</sub> / k)</p>
<p>Zet snelheden in km/h eerst om naar m/s: delen door 3,6. Bv. 36 km/h = 10 m/s.</p>
{denk('denk_4', 'Een auto rijdt eerst 30 km/h in een zone 30 in Elsene, daarna 60 km/h op een invalsweg. Hoeveel keer zo groot is zijn kinetische energie bij 60 km/h? Wat betekent dat voor het remmen?', [
  ('Factor van v', 'v wordt × 2.'),
  ('Wat zegt de formule?', 'E<sub>k</sub> = ½ · m · v²: v staat in het kwadraat, dus E<sub>k</sub> wordt × 2² = × 4.'),
  ('Remmen', 'Bij het remmen moet al die kinetische energie omgezet worden (in thermische energie in de remmen).'),
], 'De kinetische energie wordt 4 keer zo groot. Daarom is de remafstand bij 60 km/h veel groter dan bij 30 km/h.')}'''

e_oef = f'''{oef('opl_1', 1, 'Welk systeem?', 'Open, gesloten of geïsoleerd? Leg uit.<ol class="deelvragen" type="a"><li>een kop thee zonder deksel</li><li>een gesloten blikje frisdrank in de koelkast</li><li>een plant</li><li>een goed afgesloten thermosfles met soep (ideaal)</li></ol>', [
  ('a', 'open: warmte en waterdamp gaan naar buiten'), ('b', 'gesloten: het blikje koelt af (energie), maar er gaat geen materie in of uit'),
  ('c', 'open: de plant neemt licht, water en CO₂ op en geeft O₂ en waterdamp af'), ('d', 'geïsoleerd: geen uitwisseling van energie of materie')], 'Kijk naar energie én materie.')}
{oef('opl_2', 2, 'Energieomzettingen', 'Noteer de belangrijkste energieomzetting.<ol class="deelvragen" type="a"><li>een ledlamp</li><li>een batterij die een zaklamp laat branden</li><li>een appel die van een boom valt</li><li>een boogschutter laat de pees los</li><li>een kerncentrale</li><li>een waterkoker</li></ol>', [
  ('a', 'elektrische → stralingsenergie (+ thermische)'), ('b', 'chemische → elektrische → stralingsenergie (+ thermische)'), ('c', 'gravitationele potentiële → kinetische'),
  ('d', 'elastische potentiële → kinetische (van de pijl)'), ('e', 'kernenergie → thermische → kinetische (turbine) → elektrische'), ('f', 'elektrische → thermische')], 'Bij bijna elke omzetting ontstaat er ook wat thermische energie.')}
{oef('opl_3', 3, 'Op het Atomium', 'Een leerling van 55 kg neemt de lift naar een uitkijkplatform op 90 m hoogte. Bereken de toename van zijn gravitationele potentiële energie.', [
  ('Gegeven', 'm = 55 kg · g = 9,81 N/kg · h = 90 m'), ('Formule', 'E<sub>pot,g</sub> = m · g · h'), ('Oplossing', 'E<sub>pot,g</sub> = 55 · 9,81 · 90 = 48 560 J')], 'E<sub>pot,g</sub> = 4,9 · 10⁴ J')}
{oef('opl_4', 4, 'Tram', 'Een tram van 40 ton rijdt 36 km/h. Bereken zijn kinetische energie.', [
  ('Gegeven', 'm = 40 ton = 40 000 kg · v = 36 km/h = 10 m/s'), ('Formule', 'E<sub>k</sub> = ½ · m · v²'), ('Oplossing', 'E<sub>k</sub> = ½ · 40 000 · 10² = 2 000 000 J')], 'E<sub>k</sub> = 2,0 · 10⁶ J')}
{oef('opl_5', 5, 'Veer', 'Een veer met een veerconstante van 200 N/m wordt 5,0 cm ingedrukt. Bereken de elastische potentiële energie.', [
  ('Gegeven', 'k = 200 N/m · x = 5,0 cm = 0,050 m'), ('Formule', 'E<sub>pot,el</sub> = ½ · k · x²'), ('Oplossing', 'E<sub>pot,el</sub> = ½ · 200 · 0,050² = 0,25 J')], 'E<sub>pot,el</sub> = 0,25 J')}
{oef('opl_6', 6, 'Snelheid berekenen', 'Een voetbal van 0,45 kg heeft na een trap een kinetische energie van 20 J. Bereken zijn snelheid.', [
  ('Formule', 'v = √(2 · E<sub>k</sub> / m)'), ('Oplossing', 'v = √(2 · 20 / 0,45) = √88,9 = 9,4 m/s')], 'v = 9,4 m/s')}
{oef('opl_7', 7, 'Hoogte berekenen', 'Een boek van 2,0 kg ligt op een kast. Zijn gravitationele potentiële energie ten opzichte van de vloer is 30 J. Hoe hoog is de kast?', [
  ('Formule', 'h = E<sub>pot,g</sub> / (m · g)'), ('Oplossing', 'h = 30 / (2,0 · 9,81) = 1,53 m')], 'h = 1,5 m')}
{oef('opl_8', 8, 'Pompcentrale', 'Een pompcentrale pompt ’s nachts 1000 m³ water (1000 ton) 250 m omhoog.<ol class="deelvragen" type="a"><li>Hoeveel gravitationele potentiële energie wordt er opgeslagen?</li><li>Welke energieomzetting gebeurt er ’s nachts? En overdag, bij een tekort?</li></ol>', [
  ('a', 'm = 1 000 000 kg → E<sub>pot,g</sub> = 1 000 000 · 9,81 · 250 = 2,45 · 10⁹ J'),
  ('b', '’s Nachts: elektrische → gravitationele potentiële energie. Bij een tekort: gravitationele potentiële → kinetische → elektrische energie (+ thermische).')], 'E<sub>pot,g</sub> = 2,5 · 10⁹ J')}
{oef('opl_9', 9, 'Redeneren', 'Wat gebeurt er met de energie?<ol class="deelvragen" type="a"><li>Een fietser rijdt 3 keer zo snel: wat gebeurt er met E<sub>k</sub>?</li><li>Je tilt een doos 2 keer zo hoog: wat gebeurt er met E<sub>pot,g</sub>?</li><li>Je drukt een veer 2 keer zo ver in: wat gebeurt er met E<sub>pot,el</sub>?</li></ol>', [
  ('a', 'v × 3 → E<sub>k</sub> × 3² = × 9'), ('b', 'h × 2 → E<sub>pot,g</sub> × 2'), ('c', 'x × 2 → E<sub>pot,el</sub> × 2² = × 4')], 'Let op de kwadraten bij v en x.')}
{oef('opl_10', 10, 'Energie in een veld', 'Leg telkens uit waar de potentiële energie zit en wanneer ze vrijkomt.<ol class="deelvragen" type="a"><li>een boek op de bovenste plank van de kast</li><li>twee magneten die je uit elkaar houdt</li><li>een ballon die je tegen je trui wreef en die je van de muur wegtrekt</li></ol>', [
  ('a', 'zwaarteveld: het boek heeft gravitationele potentiële energie; die komt vrij als het valt'), ('b', 'magnetisch veld: de magneten trekken elkaar aan; laat je los, dan wordt de energie kinetische energie'), ('c', 'elektrisch veld: geladen ballon en muur trekken elkaar aan; laat je los, dan beweegt de ballon terug')],
  'In elk veld kan een kracht arbeid verrichten: daarom zit er potentiële energie in.')}'''

e_samenv = '''<p><b>Open</b> systeem: energie en materie uitwisselen · <b>gesloten</b>: enkel energie · <b>geïsoleerd</b>: niets.</p>
<p>In een zwaarteveld, magnetisch veld en elektrisch veld werkt een kracht op afstand: verplaats je tegen die kracht in, dan sla je <b>potentiële energie</b> op.</p>
<p><b>Behoud van energie</b>: energie wordt enkel omgezet of overgedragen. Er ontstaat bijna altijd ook thermische energie.</p>
<p><b>Pompcentrale</b>: overschot → water omhoog pompen (elektrisch → gravitationeel); tekort → water door turbine (gravitationeel → elektrisch).</p>
<p><b>E<sub>pot,g</sub> = m · g · h</b> · <b>E<sub>k</sub> = ½ · m · v²</b> · <b>E<sub>pot,el</sub> = ½ · k · x²</b></p>'''

maak('cursus-energie-systemen.html', 'Fysica 4de jaar · Thema 2 Energie en vermogen · Hoofdstuk 1', 'Energie in systemen',
     'Werk dit hoofdstuk samen met de tool <a href="energie-vermogen.html">Energie en vermogen</a>. Oefeningen maak je op papier.',
     [e_doelen, ('Systemen', e1), ('Potentiële energie in velden', e2), ('Vormen van energie en omzettingen', e3), ('Formules van energie', e4)],
     e_oef, e_samenv, 10, ('energie-vermogen.html#s10', 'Extra oefenen in de tool'),
     vk=voorkennis('<b>Energie</b> druk je uit in joule (J). Je kent al vormen van energie uit de vorige jaren (bv. bij voeding of elektriciteit).', '<b>Zwaartekracht</b>: F<sub>z</sub> = m · g met g = 9,81 N/kg.', '<b>Snelheid</b> omzetten: km/h → m/s (÷ 3,6).', 'Op je rekenmachine een <b>kwadraat</b> (x²) en een <b>vierkantswortel</b> (√) nemen.'))

# =====================================================================
#  THEMA 2 · HOOFDSTUK 2: ARBEID EN VERMOGEN
# =====================================================================
import math
_a = math.radians(30)
fig_valies = svg(
    '<rect x="0" y="0" width="600" height="220" fill="#fff"/>'
    '<line x1="20" y1="160" x2="580" y2="160" stroke="#94a3b8" stroke-width="2"/>'
    '<rect x="150" y="100" width="90" height="56" rx="8" fill="#334155"/><circle cx="165" cy="160" r="5" fill="#0f172a"/><circle cx="225" cy="160" r="5" fill="#0f172a"/>'
    + pijl(240, 110, 240 + 130 * math.cos(_a), 110 - 130 * math.sin(_a), POS) + punt(240, 110, POS) + t(360, 50, 'F', 16, POS, 'start', 700) +
    f'<line x1="240" y1="110" x2="400" y2="110" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5,4"/>'
    f'<path d="M290,110 A50,50 0 0,0 {240 + 50*math.cos(_a):.1f},{110 - 50*math.sin(_a):.1f}" fill="none" stroke="{INK}" stroke-width="1.5"/>' + t(300, 102, 'α', 15, INK, 'start', 700) +
    pijl(150, 190, 450, 190, BLAUW, 3) + t(300, 212, 'verplaatsing s', 14, BLAUW) +
    t(300, 24, 'Je trekt een valies over de grond', 14, INK, 'middle', 700), 600, 220)

w_doelen = lesdoelen(
    'het begrip <b>arbeid geleverd door een kracht op een voorwerp</b> omschrijven;',
    'de formule voor <b>arbeid</b> gebruiken en omvormen om de kracht en de verplaatsing te berekenen;',
    'de formule van het <b>arbeid-energietheorema</b> noteren en met een voorbeeld illustreren;',
    'het begrip <b>vermogen</b> omschrijven;',
    'de formule voor vermogen gebruiken en omvormen om het tijdsverloop en de hoeveelheid energie te berekenen.')

w1 = f'''<p>Duw je een kar vooruit, dan geef je energie aan de kar: ze gaat sneller rijden. Een kracht die een voorwerp verplaatst, draagt energie over. Die overgedragen energie noem je <b>arbeid</b>.</p>
{kader('Definitie', '<p>De <b>arbeid W</b> geleverd door een kracht op een voorwerp is de energie die die kracht overdraagt terwijl het voorwerp zich verplaatst.</p>')}
{figuur(fig_valies, 'De kracht F maakt een hoek α met de verplaatsing s. Enkel het deel van F in de richting van s levert arbeid.')}
<div class="formule">W = F · s · cos α</div>
<table class="vb"><tr><td>W</td><td>arbeid, in joule (J) &nbsp;·&nbsp; 1 J = 1 N · m</td></tr><tr><td>F</td><td>kracht, in N</td></tr><tr><td>s</td><td>verplaatsing, in m</td></tr><tr><td>α</td><td>hoek tussen de kracht en de verplaatsing</td></tr></table>
<h3>Drie gevallen</h3>
<ul><li><b>α = 0°</b> (kracht in de zin van de beweging): cos 0° = 1, dus <b>W = F · s</b>. De kracht geeft energie aan het voorwerp.</li>
<li><b>α = 90°</b> (kracht loodrecht op de beweging): cos 90° = 0, dus <b>W = 0</b>. Draag je een rugzak horizontaal over de speelplaats, dan levert de kracht van je schouders op de rugzak geen arbeid.</li>
<li><b>α = 180°</b> (kracht tegen de beweging in, bv. wrijving of remmen): cos 180° = −1, dus <b>W = −F · s</b>. De kracht neemt energie weg.</li></ul>
<p>Omvormen: <b>F = W / (s · cos α)</b> &nbsp;·&nbsp; <b>s = W / (F · cos α)</b></p>
<h3>Arbeid-energietheorema</h3>
<p>Werken er meerdere krachten op een voorwerp, dan bepaalt de <b>resulterende kracht</b> hoe de snelheid verandert. De arbeid van de resulterende kracht is gelijk aan de verandering van de kinetische energie:</p>
<div class="formule">W<sub>res</sub> = ΔE<sub>k</sub> = E<sub>k,eind</sub> − E<sub>k,begin</sub></div>
<p>Voorbeeld: een tram van de MIVB remt af voor een halte. De resulterende kracht staat tegen de beweging in: W<sub>res</sub> is negatief, dus E<sub>k</sub> neemt af en de tram vertraagt. Trekt de tram weer op, dan is W<sub>res</sub> positief en neemt E<sub>k</sub> toe.</p>
{denk('denk_1', 'Je trekt een valies met een kracht van 50 N over 10 m. Eerst trek je horizontaal, daarna schuin omhoog onder 60°. In welk geval lever je de meeste arbeid?', [
  ('Horizontaal', 'α = 0°: W = 50 · 10 · cos 0° = 500 J.'),
  ('Onder 60°', 'W = 50 · 10 · cos 60° = 50 · 10 · 0,5 = 250 J.'),
  ('Waarom het verschil?', 'Onder een hoek werkt maar een deel van de kracht in de richting van de verplaatsing. De rest trekt de valies omhoog.'),
], 'Horizontaal trekken levert de meeste arbeid: 500 J tegenover 250 J.')}'''

w2 = f'''<p>Twee leerlingen van 60 kg lopen dezelfde trap op. De ene loopt in 10 s naar boven, de andere wandelt rustig in 20 s. Ze krijgen allebei evenveel gravitationele potentiële energie: m · g · h. Wat verschilt, is <b>hoe snel</b> ze die energie omzetten. Dat is het <b>vermogen</b>.</p>
{kader('Definitie', '<p>Het <b>vermogen P</b> is de hoeveelheid energie die per seconde wordt omgezet (of de arbeid die per seconde geleverd wordt).</p>')}
<div class="formule">P = E / Δt</div>
<table class="vb"><tr><td>P</td><td>vermogen, in watt (W) &nbsp;·&nbsp; 1 W = 1 J/s</td></tr><tr><td>E</td><td>omgezette energie (of arbeid W), in J</td></tr><tr><td>Δt</td><td>tijdsverloop, in s</td></tr></table>
<p>Omvormen: <b>E = P · Δt</b> &nbsp;·&nbsp; <b>Δt = E / P</b></p>
<p>Op toestellen staat het vermogen: een ledlamp van 8 W zet elke seconde 8 J elektrische energie om, een waterkoker van 2000 W elke seconde 2000 J. Zet tijden in minuten of uren eerst om naar seconden.</p>
{tool('energie-vermogen.html#s7', 'Laat twee leerlingen de trap oplopen in de tool')}
{tool('energie-vermogen.html#s8', 'Vergelijk het vermogen van toestellen')}
{denk('denk_2', 'Een waterkoker van 2000 W en een van 1000 W brengen elk 1 L water aan de kook. Welke waterkoker zet meer energie om? Welke is sneller klaar?', [
  ('Hoeveel energie is nodig?', 'Om 1 L water even warm te maken, is in beide gevallen ongeveer dezelfde energie nodig.'),
  ('Wat betekent het vermogen?', '2000 W zet per seconde 2 keer zoveel energie om als 1000 W.'),
  ('Tijd', 'Δt = E / P: met een 2 keer zo groot vermogen duurt het 2 keer zo kort.'),
], 'Ze zetten (ongeveer) evenveel energie om, maar de waterkoker van 2000 W is 2 keer zo snel klaar.')}'''

w_oef = f'''{oef('opl_1', 1, 'Kar duwen', 'Je duwt een winkelkar met een horizontale kracht van 150 N over 20 m. Bereken de arbeid.', [
  ('Gegeven', 'F = 150 N · s = 20 m · α = 0°'), ('Formule', 'W = F · s · cos α'), ('Oplossing', 'W = 150 · 20 · 1 = 3000 J')], 'W = 3,0 · 10³ J')}
{oef('opl_2', 2, 'Valies onder een hoek', 'In het Zuidstation trek je een valies met een kracht van 50 N onder een hoek van 30° met de grond. Je wandelt 40 m. Bereken de arbeid van je kracht.', [
  ('Gegeven', 'F = 50 N · s = 40 m · α = 30°'), ('Formule', 'W = F · s · cos α'), ('Oplossing', 'W = 50 · 40 · cos 30° = 2000 · 0,866 = 1732 J')], 'W = 1,7 · 10³ J')}
{oef('opl_3', 3, 'Geen arbeid?', 'Leg uit of de kracht arbeid levert.<ol class="deelvragen" type="a"><li>Je houdt een zware boekentas 5 minuten stil vast.</li><li>Je draagt een rugzak horizontaal over de speelplaats: de kracht van je schouders op de rugzak.</li><li>De wrijvingskracht op een fietser die uitbolt.</li><li>Je tilt een doos van de grond op een tafel.</li></ol>', [
  ('a', 'Geen arbeid: er is geen verplaatsing (s = 0).'), ('b', 'Geen arbeid: de kracht staat loodrecht op de verplaatsing (cos 90° = 0).'),
  ('c', 'Negatieve arbeid: de kracht staat tegen de beweging in (cos 180° = −1).'), ('d', 'Positieve arbeid: kracht en verplaatsing zijn naar boven gericht.')], 'Arbeid vraagt een verplaatsing en een kracht die (deels) in de richting van die verplaatsing werkt.')}
{oef('opl_4', 4, 'Kracht berekenen', 'Een kraan levert een arbeid van 600 J om een balk 4,0 m verticaal omhoog te hijsen. Bereken de kracht van de kraan op de balk.', [
  ('Gegeven', 'W = 600 J · s = 4,0 m · α = 0°'), ('Formule', 'F = W / (s · cos α)'), ('Oplossing', 'F = 600 / (4,0 · 1) = 150 N')], 'F = 1,5 · 10² N')}
{oef('opl_5', 5, 'Arbeid-energietheorema', 'Een fietser en zijn fiets hebben samen een massa van 70 kg. Ze vertrekken uit stilstand en halen na 30 m een snelheid van 6,0 m/s.<ol class="deelvragen" type="a"><li>Bereken de arbeid van de resulterende kracht.</li><li>Bereken de grootte van de resulterende kracht.</li></ol>', [
  ('a', 'W<sub>res</sub> = ΔE<sub>k</sub> = ½ · 70 · 6,0² − 0 = 1260 J'), ('b', 'F<sub>res</sub> = W<sub>res</sub> / s = 1260 / 30 = 42 N')], 'W<sub>res</sub> = 1,26 · 10³ J en F<sub>res</sub> = 42 N')}
{oef('opl_6', 6, 'De trap op', 'Lina (60 kg) loopt de trap op naar de derde verdieping, 9,0 m hoger, in 12 s.<ol class="deelvragen" type="a"><li>Hoeveel energie zet ze om in gravitationele potentiële energie?</li><li>Bereken haar vermogen.</li></ol>', [
  ('a', 'E = m · g · h = 60 · 9,81 · 9,0 = 5297 J'), ('b', 'P = E / Δt = 5297 / 12 = 441 W')], 'E = 5,3 · 10³ J en P = 4,4 · 10² W')}
{oef('opl_7', 7, 'Waterkoker', 'Een waterkoker van 2000 W heeft 330 kJ nodig om water aan de kook te brengen. Hoe lang duurt dat?', [
  ('Gegeven', 'P = 2000 W · E = 330 kJ = 330 000 J'), ('Formule', 'Δt = E / P'), ('Oplossing', 'Δt = 330 000 / 2000 = 165 s')], 'Δt = 165 s = 2 min 45 s')}
{oef('opl_8', 8, 'Ledlamp', 'Een ledlamp van 8,0 W brandt 5,0 uur. Hoeveel elektrische energie zet ze om?', [
  ('Gegeven', 'P = 8,0 W · Δt = 5,0 h = 5,0 · 3600 s = 18 000 s'), ('Formule', 'E = P · Δt'), ('Oplossing', 'E = 8,0 · 18 000 = 144 000 J')], 'E = 1,4 · 10⁵ J')}
{oef('opl_9', 9, 'De lift', 'Een lift tilt een cabine met mensen, samen 3000 kg, in 25 s naar een uitkijkplatform 90 m hoger. Bereken het vermogen van de liftmotor (zonder verliezen).', [
  ('Energie', 'E = m · g · h = 3000 · 9,81 · 90 = 2 648 700 J'), ('Vermogen', 'P = E / Δt = 2 648 700 / 25 = 105 948 W')], 'P = 1,1 · 10⁵ W (ongeveer 106 kW)')}'''

w_samenv = '''<p><b>Arbeid</b> is de energie die een kracht overdraagt bij een verplaatsing: <b>W = F · s · cos α</b>, in joule.</p>
<p>α = 0°: W = F · s · α = 90°: W = 0 · α = 180°: W negatief.</p>
<p><b>Arbeid-energietheorema</b>: W<sub>res</sub> = ΔE<sub>k</sub>.</p>
<p><b>Vermogen</b> is de energie die per seconde wordt omgezet: <b>P = E / Δt</b>, in watt (1 W = 1 J/s). Omvormen: E = P · Δt en Δt = E / P.</p>'''

maak('cursus-arbeid-vermogen.html', 'Fysica 4de jaar · Thema 2 Energie en vermogen · Hoofdstuk 2', 'Arbeid en vermogen',
     'Werk dit hoofdstuk samen met de tool <a href="energie-vermogen.html">Energie en vermogen</a>. Oefeningen maak je op papier.',
     [w_doelen, ('Arbeid', w1), ('Vermogen', w2)],
     w_oef, w_samenv, 9, ('energie-vermogen.html#s10', 'Extra oefenen in de tool'),
     vk=voorkennis('<b>Krachten</b> als vector en de <b>resulterende kracht</b>.', '<b>Energieformules</b>: E<sub>pot,g</sub> = m · g · h en E<sub>k</sub> = ½ · m · v² (hoofdstuk 1).', 'Een <b>hoek</b> tussen twee richtingen aflezen en <b>cos</b> berekenen op je rekenmachine (in graden: DEG).', 'Tijd omzetten: 1 min = 60 s, 1 h = 3600 s.'))
print('ok')
