# Cursus fysica 3NW · Thema 2 Krachten · hoofdstuk 1 (rekenen), 3 (zwaartekracht), 5 (wrijving) en 6 (veerkracht), nieuw formaat.
# Gebruik:  cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/nw3_krachten2.py
# Hergebruikt figuren, tekenoefeningen en teksten uit de 3ASO-cursus (aso_krachten.py / aso_veer.py), met de NW-tools als link.
import re, sys
B_ = '/home/claude/toolswetenschappen/_bron/cursus/'
sys.path.insert(0, '/home/claude/cursus')
import bouw as BM
BM.FOOTER = 'Cursus fysica — gemaakt voor klasgebruik, bij de tools op Oefentools wetenschappen.'

a = {'__name__': 'aso'}
src = open(B_ + 'aso_krachten.py', encoding='utf-8').read()
exec(src.split("exec(open('/home/claude/toolswetenschappen/_bron/cursus/aso_extra.py'")[0], a)
NW = lambda s: s.replace('krachten-3aso.html', 'krachten.html').replace('rekenen-fysica-3aso.html', 'rekenen-fysica.html')
blok, oef, kader, tool, denk, figuur = a['blok'], a['oef'], a['kader'], a['tool'], a['denk'], a['figuur']
EDI_CSS, edi, W = a['EDI_CSS'], a['edi'], a['wisbord']
svg, t, pijl, punt, label, rooster, doos, sub, LET = a['svg'], a['t'], a['pijl'], a['punt'], a['label'], a['rooster'], a['doos'], a['sub'], a['LET']
INK, PAARS, G, ORANJE, B, R, HK, oef_fig = a['INK'], a['PAARS'], a['G'], a['ORANJE'], a['B'], a['R'], a['HK'], a['oef_fig']
AANPAK_SCHEMA = 'maak een schets met alle krachten op het voorwerp. Kies dan de formule (F<sub>z</sub> = m · g, F<sub>w,s,max</sub> = μ<sub>s</sub> · F<sub>N</sub>, F<sub>v</sub> = k · Δl) en reken met eenheden.'
AANPAK_LEES = 'het voorwerp, de gegevens met hun eenheid'
exec(open(B_ + 'nieuw_formaat.py', encoding='utf-8').read())
FW = 'F<sub>w,s</sub>'; FWM = 'F<sub>w,s,max</sub>'; FWD = 'F<sub>w,d</sub>'; MU = 'μ<sub>s</sub>'

# ------------------------------------------------------------------ figuren (nieuw voor NW)
def mini(titel, punten, xl, yl, x0=0):
    """kleine schetsgrafiek zonder getallen"""
    o = f'<g transform="translate({x0},0)">' + pijl(30, 150, 180, 150, INK) + pijl(30, 150, 30, 20, INK)
    o += t(176, 168, xl, INK, 'end', 12, 600) + t(36, 22, yl, INK, 'start', 12, 600) + t(105, 192, titel, INK, 'middle', 13, 700)
    o += '<polyline points="' + ' '.join(f'{30+x*1.4:.0f},{150-y*1.2:.0f}' for x, y in punten) + f'" fill="none" stroke="{B}" stroke-width="3.5"/></g>'
    return o
fig_graf = svg(mini('F<tspan dy="4" font-size="10">z</tspan><tspan dy="-4"> en m (g vast)</tspan>', [(0, 0), (100, 100)], 'm', 'Fz')
               + mini('F<tspan dy="4" font-size="10">z</tspan><tspan dy="-4"> en g (m vast)</tspan>', [(0, 0), (100, 75)], 'g', 'Fz', 210)
               + mini('m en g', [(0, 60), (100, 60)], 'g', 'm', 420), 620, 205)

def kist(opl=False, schuift=False, duw=3, wr=None, m_hok=4):
    """kist op de vloer, je duwt naar rechts met duw hokjes; opl: F_w (links, op het contactvlak), F_z, F_N"""
    w, h = 600, 260
    o = rooster(w, h) + f'<rect x="0" y="180" width="{w}" height="80" fill="#d6d3d1" opacity=".55"/>' + doos(250, 110, 100, 70, '#e7c9a9', '#7c2d12')
    o += punt(300, 145, INK, 4) + punt(250, 128, INK, 4) + punt(300, 180, INK, 4)
    o += pijl(250, 128, 250 + duw * HK, 128, B) + label(240, 124, 'F', 'duw', B, 'end')   # je duwt op de linkerkant van de kist
    if opl:
        n = duw if wr is None else wr
        o += pijl(300, 180, 300 - n * HK, 180, R) + label(300 - n * HK - 2, 202, 'F', 'w,d' if schuift else 'w,s', R, 'end')
        o += pijl(300, 145, 300, 145 + m_hok * HK, PAARS) + label(306, 145 + m_hok * HK, 'F', 'z', PAARS)
        o += pijl(286, 180, 286, 180 - m_hok * HK, G) + label(278, 180 - m_hok * HK + 14, 'F', 'N', G, 'end')
    return svg(o, w, h)

def wgraf():
    """wrijvingskracht in functie van de trekkracht: stijgt tot F_w,s,max, valt dan terug tot F_w,d"""
    o = '<rect width="600" height="250" fill="#fff"/>' + pijl(60, 210, 560, 210, INK) + pijl(60, 210, 60, 20, INK)
    o += t(556, 232, 'trekkracht F', INK, 'end', 13) + t(66, 24, 'wrijvingskracht', INK, 'start', 13)
    o += f'<polyline points="60,210 300,70" fill="none" stroke="{R}" stroke-width="3.5"/><polyline points="300,70 310,110 540,110" fill="none" stroke="{R}" stroke-width="3.5"/>'
    o += f'<line x1="60" y1="70" x2="300" y2="70" stroke="#94a3b8" stroke-dasharray="5 4"/><line x1="300" y1="70" x2="300" y2="210" stroke="#94a3b8" stroke-dasharray="5 4"/>'
    o += t(54, 74, FWM.replace('<sub>', '').replace('</sub>', ''), R, 'end', 12) + t(54, 114, 'Fw,d', R, 'end', 12)
    o += t(180, 196, 'kist staat stil: statisch', INK, 'middle', 13, 600) + t(430, 196, 'kist schuift: dynamisch', INK, 'middle', 13, 600)
    return svg(o, 600, 250)

# ------------------------------------------------------------------ delen
d1 = NW(a['h1'])
d2 = NW(a['h4a'])
d3 = NW(a['h4b']) + '''<table style="border-collapse:collapse;margin:8px 0 12px;font-size:15px" cellpadding="5" border="1" bordercolor="#cbd5e1"><tr><th>hemellichaam</th><th>g (N/kg)</th></tr>
<tr><td>aarde</td><td>9,81</td></tr><tr><td>maan</td><td>1,62</td></tr><tr><td>Mars</td><td>3,71</td></tr><tr><td>Jupiter</td><td>24,8</td></tr></table>
<p><b>Grafieken.</b> F<sub>z</sub> en m zijn <b>recht evenredig</b>: een rechte door de oorsprong. Hetzelfde voor F<sub>z</sub> en g. De massa hangt niet af van g: een horizontale lijn.</p>''' + \
    figuur(fig_graf, 'Links: dubbele massa, dubbele zwaartekracht. Midden: dubbele g, dubbele zwaartekracht. Rechts: de massa blijft gelijk, waar je ook bent.')
d4 = kader('Definities', '''<p><b>Massa m</b> (kg): hoeveel stof een voorwerp bevat. Ze is overal even groot.</p>
<p><b>Gewicht F<sub>G</sub></b> (N): de kracht waarmee een voorwerp op zijn steun drukt of aan zijn ophangpunt trekt.</p>
<p><b>Gewichtloosheid</b>: een voorwerp drukt op geen enkele steun en trekt aan geen ophangpunt: F<sub>G</sub> = 0. De zwaartekracht werkt nog wel.</p>''') + \
'''<p>Een astronaut in het ISS en een springer op een trampoline in de lucht zijn <b>gewichtloos</b>. Ze vallen samen met alles rond hen: niets drukt op een steun. De zwaartekracht werkt wel: zonder zwaartekracht zou het ISS rechtdoor de ruimte in vliegen.</p>''' + \
LET + 'Op een weegschaal lees je een massa in kg af, maar de weegschaal meet je <b>gewicht</b>: hoe hard je erop drukt. Spring je op de weegschaal, dan geeft ze even meer aan.</div>'
_h4c = NW(a['h4c'])
d5 = _h4c[_h4c.index('<p>Een <b>normaalkracht'):]
d6 = kader('Definities', f'''<p><b>Wrijvingskracht</b>: de kracht die de beweging van een voorwerp tegenwerkt. Ze werkt op het voorwerp, in het contactvlak, evenwijdig met de ondergrond.</p>
<p><b>Statische wrijvingskracht {FW}</b>: zorgt dat een voorwerp in rust niet begint te bewegen. Ze is even groot als je duwkracht, tot een maximum: <b>{FWM}</b>.</p>
<p><b>Dynamische wrijvingskracht {FWD}</b>: werkt als het voorwerp over de ondergrond schuift. Ze is kleiner dan {FWM}.</p>''') + \
    figuur(wgraf(), 'Je trekt steeds harder. Eerst groeit de statische wrijving mee. Boven het maximum schuift de kist en is de wrijving kleiner.') + \
    f'''<p>Daarom is een kast moeilijk <b>in beweging</b> te krijgen, en gaat het daarna makkelijker.</p>
<p><b>Statisch of dynamisch?</b> Beweegt het contactvlak niet tegenover de ondergrond, dan is het statisch. Een rollend wiel en de voet van een stappende persoon raken de grond telkens op één plaats zonder te schuiven: statisch. Schuift het oppervlak, dan is het dynamisch.</p>
<p><b>ABS</b>: blokkeren de wielen bij hard remmen, dan schuiven de banden (dynamisch: minder wrijving, en je kan niet sturen). ABS laat de remmen telkens even los, zodat de wielen blijven draaien: statische wrijving, die groter is. <b>Aquaplaning</b>: een laagje water tussen band en weg maakt de wrijving bijna nul; de auto glijdt.</p>''' + \
    tool('krachten.html#wr1', 'Trek aan de kist in de tool') + tool('krachten.html#wr3', 'ABS en aquaplaning in de tool')
d7 = kader('Formule', f'''<p class="formule">{FWM} = {MU} · F<sub>N</sub></p>
<p>{MU} = <b>statische wrijvingscoëfficiënt</b> (geen eenheid). Hij hangt af van de twee oppervlakken: rubber op droog asfalt ≈ 0,9, rubber op nat asfalt ≈ 0,5, ijzer op ijs ≈ 0,03.</p>
<p>Omvormen: <b>{MU} = {FWM} / F<sub>N</sub></b> en <b>F<sub>N</sub> = {FWM} / {MU}</b>.</p>''') + \
    f'''<p>In woorden: hoe groter de normaalkracht, hoe groter de maximale statische wrijvingskracht (recht evenredig). Een volle kast duwt harder op de vloer, dus moet je harder duwen. Op een horizontale vloer is F<sub>N</sub> = F<sub>z</sub> = m · g.</p>''' + \
    tool('krachten.html#wr2', 'Verander de normaalkracht en de oppervlakken in de tool')
d8 = ('<p>Hang je een massa aan een veer, dan rekt de veer uit. De veer trekt terug omhoog: dat is de <b>veerkracht F<sub>v</sub></b>. Hangt de massa stil, dan is F<sub>v</sub> even groot als F<sub>z</sub>.</p>'
      '<p>Amina hing telkens meer massa aan dezelfde veer en mat de uitrekking Δl (g ≈ 10 N/kg):</p>' + a['tab_meet']
      + figuur(a['grafiek']([(2, .5), (4, 1), (6, 1.5), (8, 2)], [(0, 0, 10, 2.5, B, '')]), 'De punten liggen op een rechte door de oorsprong: dubbel zoveel kracht geeft dubbel zoveel uitrekking.')
      + NW(a['KEN']) + a['VOORBEELD'] + a['VINGERS']
      + kader('Wet van Hooke', '<p>F<sub>v</sub> = k · Δl geldt alleen zolang de vervorming <b>elastisch</b> is: de veer neemt haar oorspronkelijke lengte terug aan. Voorbij de <b>elasticiteitsgrens</b> wordt de vervorming <b>plastisch</b>: de veer blijft langer, en de rechte in de grafiek buigt af.</p>')
      + figuur(a['grafiek'](lijnen=a['TWEE']), 'Twee veren: hoe steiler de rechte, hoe groter k, hoe stijver de veer.')
      + tool('krachten.html#ve1', 'Doe de proef zelf in de tool') + tool('krachten.html#ve2', 'Wet van Hooke en grafieken in de tool'))

delen = [('Rekenen in de fysica', d1), ('Zwaartekracht en zwaarteveld', d2), ('Zwaartekracht, massa en zwaarteveldsterkte', d3), ('Massa, gewicht en gewichtloosheid', d4),
         ('Normaalkracht, zwaartekracht en gewicht', d5), ('Statische en dynamische wrijvingskracht', d6), ('De maximale statische wrijvingskracht', d7), ('Veerkracht', d8)]
NRS = ['1', '3.1', '3.2', '3.3', '3.4', '5.1', '5.2', '6']

def D(idee, vb, test, wb, letop=None, stappen=None, steun=None): return dict(idee=idee, vb=vb, test=test, wb=wb, letop=letop, stappen=stappen, steun=steun)
FZ = 'F<sub>z</sub>'; FN = 'F<sub>N</sub>'; FG = 'F<sub>G</sub>'; FV = 'F<sub>v</sub>'
C = dict(delen=[
 D('Een meting is een getal mét eenheid. Je zet om naar de SI-eenheid, je schrijft grote en kleine getallen kort, en je toont met beduidende cijfers hoe nauwkeurig je meet.',
   ('Afronden met BC', 'Een kist is 1,25 m lang en 0,8 m breed. Bereken de oppervlakte.',
    [('Rekenmachine', '1,25 m · 0,8 m = 1 m²... de rekenmachine toont 1.'), ('BC', '1,25 heeft 3 BC, 0,8 heeft 1 BC: de uitkomst krijgt er 1, want de minst nauwkeurige meting beslist.'),
     ('Antwoord', 'A = 1 m². Meer cijfers zou nauwkeuriger lijken dan je gemeten hebt.')]),
   [('Waarom rond je een uitkomst af op het kleinste aantal BC?', 'Een berekening kan niet nauwkeuriger zijn dan de minst nauwkeurige meting.'),
    ('Wanneer gebruik je wetenschappelijke notatie?', 'Bij heel grote of heel kleine getallen: zo zie je meteen de grootte-orde.')],
   ([('1 km = ? m', '1000 m')], [('350 g in kg?', '0,350 kg', '350 000 kg'), ('Hoeveel BC heeft 0,0450?', '3', '5')], [('0,00052 in wetenschappelijke notatie?', '5,2 · 10⁻⁴')]),
   'Nullen <b>vooraan</b> tellen niet mee als BC, nullen <b>achteraan</b> na de komma wel: 0,0450 heeft 3 BC.'),
 D('De aarde trekt aan alles in haar buurt: dat is de zwaartekracht. Het gebied waar die kracht werkt, is het zwaarteveld.',
   ('Zwaartekracht tekenen in Sydney', 'Een leerling in Brussel en een leerling in Australië laten elk een bal los. Teken de zwaartekracht op beide ballen.',
    [('Aangrijpingspunt', 'in het zwaartepunt van elke bal, want de kracht werkt op de hele bal.'), ('Richting en zin', 'naar het middelpunt van de aarde, want daar trekt de aarde naar toe.'),
     ('Besluit', 'in Brussel naar "onder", in Australië ook naar "onder" voor hen, maar in de tekening wijzen de pijlen naar elkaar toe.')]),
   [('Wat is het verschil tussen zwaarteveld en zwaartekracht?', 'Het zwaarteveld is het gebied rond een hemellichaam. De zwaartekracht is de kracht op een voorwerp in dat gebied.'),
    ('Waarom valt de maan niet op de aarde, terwijl de aarde eraan trekt?', 'De maan beweegt snel opzij. De zwaartekracht buigt die beweging telkens af: zo draait ze rond de aarde.')],
   ([('Waarom valt een appel naar beneden?', 'de aarde trekt eraan')], [('Waar teken je F<sub>z</sub>?', 'in het zwaartepunt', 'onderaan, op de grond'), ('Zin van F<sub>z</sub>?', 'naar het middelpunt van de aarde')], [('Zwaarteveld = …', 'gebied waar de zwaartekracht werkt')])),
 D('Hoe groot de zwaartekracht is, hangt af van de massa en van het zwaarteveld: F_z = m · g.',
   ('Een rover op Mars', 'Een rover heeft een massa van 900 kg. Hoe groot is de zwaartekracht op aarde en op Mars?',
    [('Gegeven', 'm = 900 kg; g = 9,81 N/kg op aarde en 3,71 N/kg op Mars.'), ('Aarde', 'F<sub>z</sub> = m · g = 900 kg · 9,81 N/kg = 8,83 · 10³ N.'),
     ('Mars', 'F<sub>z</sub> = 900 kg · 3,71 N/kg = 3,34 · 10³ N. Dezelfde massa, maar een kleinere g, dus een kleinere zwaartekracht.')]),
   [('Wat betekent g = 9,81 N/kg?', 'Op aarde werkt op elke kilogram een zwaartekracht van 9,81 N.'),
    ('Welke grafiek hoort bij F<sub>z</sub> en m?', 'Een rechte door de oorsprong: ze zijn recht evenredig.')],
   ([('Eenheid van kracht?', 'N')], [('F<sub>z</sub> = 98 N op aarde: m?', '10 kg', '961 kg'), ('Massa op de maan tegenover de aarde?', 'gelijk', 'kleiner')], [('Grafiek m in functie van g?', 'horizontale lijn')]),
   steun='Gegeven → gevraagd → formule → oplossing met eenheden → antwoordzin.'),
 D('Massa is hoeveel stof je hebt. Gewicht is hoe hard je op je steun drukt. Zonder steun ben je gewichtloos, maar de zwaartekracht werkt nog.',
   ('In de lift', 'Je staat op een weegschaal in een lift. De kabel breekt (in gedachten!) en de lift valt. Wat toont de weegschaal?',
    [('Massa', 'blijft gelijk: dezelfde hoeveelheid stof.'), ('Zwaartekracht', 'werkt nog: je valt.'),
     ('Gewicht', 'jij en de weegschaal vallen even snel: je drukt er niet meer op. De weegschaal toont 0: gewichtloos.')]),
   [('Waarom is een astronaut in het ISS gewichtloos, terwijl de zwaartekracht daar nog bijna even groot is?', 'Hij valt samen met het ISS rond de aarde: hij drukt op geen steun. F<sub>G</sub> = 0, F<sub>z</sub> ≠ 0.'),
    ('Wat is het verschil tussen massa en gewicht?', 'Massa: hoeveelheid stof (kg), overal gelijk. Gewicht: kracht op de steun of het ophangpunt (N).')],
   ([('Wat meet een weegschaal echt?', 'je gewicht')], [('Gewicht: eenheid?', 'N', 'kg'), ('Gewichtloos: werkt F<sub>z</sub> nog?', 'ja', 'nee')], [('Waar werkt het gewicht op?', 'op de steun of het ophangpunt')]),
   '"Gewichtloos" betekent <b>niet</b> "geen zwaartekracht". De zwaartekracht werkt nog, je drukt alleen op niets.'),
 D('Ligt een voorwerp op een steun, dan werken er drie verschillende krachten: F_z op het voorwerp, F_N op het voorwerp, en F_G op de steun.',
   ('Een laptop op je knieën', 'Je laptop (2,0 kg) ligt op je knieën. Benoem de drie krachten en zeg waar ze werken.',
    [(FZ, 'de aarde trekt aan de laptop: op de laptop, in het zwaartepunt, 20 N naar beneden.'), (FN, 'je knieën duwen op de laptop: op de laptop, vanuit het contactvlak, 20 N naar boven.'),
     (FG, 'de laptop drukt op je knieën: op jou, vanuit het contactvlak, 20 N naar beneden.')]),
   [('Waarom zijn F<sub>z</sub> en F<sub>G</sub> niet dezelfde kracht, ook al zijn ze even groot?', 'Ze werken op een ander voorwerp en worden door iets anders uitgeoefend: F<sub>z</sub> door de aarde op het voorwerp, F<sub>G</sub> door het voorwerp op de steun.'),
    ('Waarom is er geen normaalkracht bij een hangende lamp?', 'De lamp ligt niet op een steun; het snoer trekt eraan.')],
   ([('Wie oefent F<sub>N</sub> uit?', 'de steun')], [('Op wat werkt F<sub>G</sub>?', 'op de steun', 'op het voorwerp'), ('Waar begint de pijl van F<sub>N</sub>?', 'in het contactvlak, op het voorwerp')], [('Drie krachten bij een boek op tafel?', 'F<sub>z</sub>, F<sub>N</sub>, F<sub>G</sub>')]),
   stappen=('Een kracht tekenen', [('Op welk voorwerp werkt de kracht?', 'daarop teken je de pijl.'), ('Wie oefent ze uit?', 'dat geeft de naam: aarde → F<sub>z</sub>, steun → F<sub>N</sub>, voorwerp op steun → F<sub>G</sub>.'),
                                   ('Aangrijpingspunt?', 'F<sub>z</sub> in het zwaartepunt; F<sub>N</sub> en F<sub>G</sub> in het contactvlak.'), ('Richting, zin en grootte?', 'grootte ÷ schaal = aantal hokjes.')])),
 D('Wrijving werkt de beweging tegen. Staat het voorwerp stil, dan is ze statisch en groeit ze mee met je duwkracht. Schuift het, dan is ze dynamisch en kleiner.',
   ('Een kast verschuiven', 'Je duwt met 100 N tegen een kast. Ze beweegt niet. Je duwt met 300 N: ze schuift. Daarna houd je ze in beweging met 200 N. Verklaar.',
    [('100 N', 'statisch: de wrijving is ook 100 N, de kast blijft staan (F<sub>r</sub> = 0).'), ('300 N', 'je duw is groter dan F<sub>w,s,max</sub>: de kast komt in beweging.'),
     ('200 N', 'nu werkt de dynamische wrijving, die kleiner is: minder kracht nodig.')]),
   [('Waarom is de wrijving tussen een rollend wiel en de weg statisch?', 'Het stukje band dat de weg raakt, schuift niet over de weg: het staat even stil tegenover de grond.'),
    ('Waarom remt een auto met ABS korter?', 'De wielen blokkeren niet: de statische wrijving werkt, en die is groter dan de dynamische. Je kan bovendien blijven sturen.')],
   ([('Waarom glij je uit op ijs?', 'weinig wrijving')], [('Je duwt 50 N, de kast blijft staan. F<sub>w,s</sub>?', '50 N', '0 N'), ('Blokkerende wielen: statisch of dynamisch?', 'dynamisch')], [('Wat is aquaplaning?', 'water tussen band en weg: bijna geen wrijving')]),
   'Wrijving is niet altijd lastig: zonder wrijving kan je niet stappen, niet fietsen en niet remmen.'),
 D('De maximale statische wrijvingskracht hangt af van hoe hard het voorwerp op de ondergrond drukt (F_N) en van de twee oppervlakken (μ_s).',
   ('Kan Youssef de kast verschuiven?', 'Een kast van 60 kg staat op een houten vloer (μ<sub>s</sub> = 0,40). Youssef duwt met 200 N. Komt ze in beweging? (g = 9,81 N/kg)',
    [('Normaalkracht', 'op een horizontale vloer is F<sub>N</sub> = F<sub>z</sub> = 60 kg · 9,81 N/kg = 589 N.'), ('Maximum', 'F<sub>w,s,max</sub> = μ<sub>s</sub> · F<sub>N</sub> = 0,40 · 589 N = 236 N.'),
     ('Besluit', '200 N < 236 N: de kast blijft staan. Hij moet harder duwen dan 236 N.')]),
   [('Waarom is het makkelijker een lege kast te verschuiven dan een volle?', 'De lege kast heeft een kleinere F<sub>N</sub>, dus een kleinere F<sub>w,s,max</sub>.'),
    ('Waarom heeft μ<sub>s</sub> geen eenheid?', 'Je deelt twee krachten door elkaar: N / N.')],
   ([('Op een horizontale vloer: F<sub>N</sub> = …', 'F<sub>z</sub>')], [('F<sub>N</sub> = 500 N, μ<sub>s</sub> = 0,30: F<sub>w,s,max</sub>?', '150 N'), ('Nat asfalt tegenover droog: μ<sub>s</sub>?', 'kleiner', 'groter')], [('μ<sub>s</sub> = …', 'F<sub>w,s,max</sub> / F<sub>N</sub>')]),
   steun='Gegeven → gevraagd → formule → oplossing met eenheden → antwoordzin.'),
 D('Een vervormde veer wil terug naar haar oorspronkelijke lengte. Hoe verder je ze uitrekt, hoe groter de veerkracht: F_v = k · Δl.',
   ('Een veerweegschaal', 'Een veerweegschaal heeft k = 200 N/m. Je hangt er een tas aan; de veer rekt 4,5 cm uit. Wat is de massa van de tas? (g = 9,81 N/kg)',
    [('Eenheid', 'Δl = 4,5 cm = 0,045 m, want k is in N/m.'), ('Veerkracht', 'F<sub>v</sub> = k · Δl = 200 N/m · 0,045 m = 9,0 N.'),
     ('Massa', 'de tas hangt stil: F<sub>z</sub> = F<sub>v</sub> = 9,0 N, dus m = F<sub>z</sub> / g = 9,0 N / 9,81 N/kg = 0,92 kg.')]),
   [('Wat betekent k = 200 N/m?', 'Je hebt 200 N nodig om de veer 1 m uit te rekken: een stijve veer.'),
    ('Wanneer geldt de wet van Hooke niet meer?', 'Voorbij de elasticiteitsgrens: de vervorming is dan plastisch en de veer komt niet meer terug.')],
   ([('Wat is elastisch?', 'krijgt zijn vorm terug')], [('Grote k: stijf of slap?', 'stijf'), ('Dubbele massa: Δl?', 'verdubbelt', 'blijft gelijk')], [('F<sub>v</sub> = 6,0 N, Δl = 0,20 m: k?', '30 N/m')]))],
 uitd=[('Uitdaging · Remmen op een natte weg', 'Een auto (1200 kg) remt met ABS. Op droog asfalt is μ<sub>s</sub> = 0,90, op nat asfalt 0,50. Bereken de maximale remkracht in beide gevallen (g = 9,81 N/kg). Leg uit waarom je bij regen meer afstand moet houden, en waarom ABS helpt.',
        [('Normaalkracht', 'F<sub>N</sub> = F<sub>z</sub> = 1200 kg · 9,81 N/kg = 1,18 · 10⁴ N.'), ('Droog', 'F<sub>w,s,max</sub> = 0,90 · 1,18 · 10⁴ N = 1,06 · 10⁴ N.'),
         ('Nat', '0,50 · 1,18 · 10⁴ N = 5,9 · 10³ N: bijna de helft.'), ('Besluit', 'minder remkracht = langere remweg. ABS houdt de wrijving statisch, en die is groter dan dynamisch.')],
        'Op een natte weg is de remkracht bijna gehalveerd.',
        'Teken eerst de auto met F<sub>z</sub>, F<sub>N</sub> en de wrijvingskracht. Welke formule verbindt F<sub>N</sub> met de wrijving? Reken dan voor droog en nat, en vergelijk.'),
       ('Uitdaging · Dezelfde kist op de maan', 'Op aarde moet je met minstens 120 N duwen om een kist van 40 kg te verschuiven. Hoe hard moet je duwen op de maan (g = 1,62 N/kg), op dezelfde ondergrond? Wat verandert er, en wat niet?',
        [('μ<sub>s</sub> op aarde', 'F<sub>N</sub> = 40 · 9,81 = 392 N; μ<sub>s</sub> = 120 N / 392 N = 0,31.'), ('Maan', 'F<sub>N</sub> = 40 · 1,62 = 64,8 N; F<sub>w,s,max</sub> = 0,31 · 64,8 N = 20 N.'),
         ('Wat blijft?', 'de massa (40 kg) en μ<sub>s</sub> (zelfde oppervlakken); F<sub>z</sub>, F<sub>N</sub> en de wrijving worden kleiner.')],
        'Op de maan volstaat ongeveer 20 N.',
        'Zoek eerst μ<sub>s</sub>.'),
       ('Uitdaging · Een veerweegschaal op de maan', 'Je neemt een veerweegschaal (k = 200 N/m) en een keukenweegschaal met gewichten (een balans) mee naar de maan. Je weegt een zak appelen van 1,5 kg. Wat toont elk toestel? Welk toestel meet massa, welk meet een kracht?',
        [('Veer op aarde', 'F<sub>v</sub> = 1,5 · 9,81 = 14,7 N → Δl = 14,7 / 200 = 0,074 m.'), ('Veer op de maan', 'F<sub>v</sub> = 1,5 · 1,62 = 2,4 N → Δl = 0,012 m: de veer toont veel minder.'),
         ('Balans', 'vergelijkt met gewichten die ook lichter worden: toont nog altijd 1,5 kg.'), ('Besluit', 'de balans meet massa, de veerweegschaal meet een kracht.')],
        'Een veer meet kracht, een balans vergelijkt massa\'s.', None)],
 begrip=[('SI-eenheid', 'standaardeenheid: m, kg, s, N'), ('wetenschappelijke notatie', 'a · 10ⁿ met 1 ≤ a < 10'), ('beduidende cijfers', 'cijfers die tonen hoe nauwkeurig je meet'),
         ('zwaartekracht F<sub>z</sub>', 'kracht van een hemellichaam op een voorwerp; F<sub>z</sub> = m · g'), ('zwaarteveld', 'gebied waar de zwaartekracht werkt'), ('zwaarteveldsterkte g', 'zwaartekracht per kg (N/kg)'),
         ('massa m', 'hoeveelheid stof (kg); overal gelijk'), ('gewicht F<sub>G</sub>', 'kracht van het voorwerp op de steun of het ophangpunt (N)'), ('gewichtloosheid', 'F<sub>G</sub> = 0; de zwaartekracht werkt nog'),
         ('normaalkracht F<sub>N</sub>', 'kracht van de steun op het voorwerp, loodrecht op het contactvlak'), ('statische wrijvingskracht', 'houdt een voorwerp in rust'), ('maximale statische wrijvingskracht', 'F<sub>w,s,max</sub> = μ<sub>s</sub> · F<sub>N</sub>'),
         ('dynamische wrijvingskracht', 'wrijving als het voorwerp schuift; kleiner dan het maximum'), ('statische wrijvingscoëfficiënt μ<sub>s</sub>', 'hangt af van de twee oppervlakken; geen eenheid'),
         ('ABS', 'voorkomt dat de wielen blokkeren'), ('aquaplaning', 'water tussen band en weg: bijna geen wrijving'), ('veerkracht F<sub>v</sub>', 'F<sub>v</sub> = k · Δl'),
         ('veerconstante k', 'N/m; grote k = stijve veer'), ('wet van Hooke', 'F<sub>v</sub> recht evenredig met Δl, zolang de vervorming elastisch is'), ('elasticiteitsgrens', 'daarboven is de vervorming plastisch')])

def fsub(x):
    if isinstance(x, str): return re.sub(r'F_([a-zA-Z0-9]+)', r'F<sub>\1</sub>', x).replace('μ_s', 'μ<sub>s</sub>')
    if isinstance(x, (list, tuple)): return type(x)(fsub(y) for y in x)
    if isinstance(x, dict): return {k: fsub(v) for k, v in x.items()}
    return x
C = fsub(C)

# ------------------------------------------------------------------ oefeningen per hoofdstuk
O = a['_O'] if '_O' in a else None
TEKEN = a['TEKEN']
def zoek(titel):  # oefening uit de 3ASO-reeks op titel
    for o in a['_O']:
        if f'</span>{titel}</div>' in o: return NW(o)
    raise KeyError(titel)
o_graf = oef('opl_x', 0, 'Grafieken herkennen', 'Welke grafiek (een rechte door de oorsprong, een horizontale lijn of een dalende lijn) hoort bij:<ol class="deelvragen" type="a"><li>F<sub>z</sub> in functie van m, op aarde?</li><li>F<sub>z</sub> in functie van g, voor een massa van 5 kg?</li><li>m in functie van g?</li></ol>',
    [('a', 'rechte door de oorsprong (recht evenredig)'), ('b', 'rechte door de oorsprong'), ('c', 'horizontale lijn: de massa hangt niet af van g')], 'Alleen m in functie van g is horizontaal.')
o_w1 = oef('opl_x', 0, 'Statisch of dynamisch?', 'Welke wrijvingskracht werkt er?<ol class="deelvragen" type="a"><li>Een boek ligt op een schuine plank en blijft liggen.</li><li>Je schuift met een slee van een helling.</li><li>Een fiets rijdt: wrijving tussen band en weg.</li><li>Een auto remt met geblokkeerde wielen.</li></ol>',
    [('a', 'statisch'), ('b', 'dynamisch'), ('c', 'statisch: de band schuift niet'), ('d', 'dynamisch: de banden schuiven')], 'Schuift het contactvlak? Dan is het dynamisch.')
o_w2 = oef('opl_x', 0, 'Rekenen met μ<sub>s</sub>', 'a) Een doos van 25 kg staat op een vloer met μ<sub>s</sub> = 0,35. Bereken F<sub>w,s,max</sub>. b) Je moet minstens 90 N duwen om een kist met F<sub>N</sub> = 300 N te verschuiven. Bereken μ<sub>s</sub>. c) Bij μ<sub>s</sub> = 0,50 is F<sub>w,s,max</sub> = 40 N. Hoe groot is F<sub>N</sub>?',
    [('a', 'F<sub>N</sub> = 25 · 9,81 = 245 N; F<sub>w,s,max</sub> = 0,35 · 245 N = 86 N'), ('b', 'μ<sub>s</sub> = 90 N / 300 N = 0,30'), ('c', 'F<sub>N</sub> = 40 N / 0,50 = 80 N')], 'a) 86 N · b) 0,30 · c) 80 N')
o_w3 = oef_fig('opl_x', 0, 'Tekenen: een kist die niet beweegt', 'Je duwt een kist van 4,0 kg met 20 N naar rechts, maar ze blijft staan (g ≈ 10 N/kg). Teken F<sub>w,s</sub>, F<sub>z</sub> en F<sub>N</sub> op de kist. Schaal: 1 hokje ≙ 10 N. ' + TEKEN,
    kist(duw=2), [('Wrijving', 'de kist staat stil: F<sub>w,s</sub> = 20 N → 2 hokjes naar links, in het contactvlak'), ('F<sub>z</sub>', '4,0 kg · 10 N/kg = 40 N → 4 hokjes, vanuit het midden naar beneden'),
     ('F<sub>N</sub>', '40 N → 4 hokjes, vanuit het contactvlak naar boven')], 'F<sub>w,s</sub> is tegengesteld aan je duw; F<sub>N</sub> en F<sub>z</sub> zijn even groot.', kist(True, duw=2, m_hok=4))
o_w4 = oef_fig('opl_x', 0, 'Tekenen: een kist die schuift', 'Dezelfde kist schuift nu met constante snelheid naar rechts. Je duwt met 10 N. Teken F<sub>w,d</sub>. Schaal: 1 hokje ≙ 10 N. Is F<sub>w,d</sub> groter of kleiner dan bij de vorige oefening? Waarom?',
    kist(duw=1), [('Constante snelheid', 'F<sub>r</sub> = 0, dus F<sub>w,d</sub> = 10 N → 1 hokje naar links'), ('Vergelijking', 'kleiner dan F<sub>w,s,max</sub>: de dynamische wrijving is kleiner dan de maximale statische')],
    'F<sub>w,d</sub> = 10 N naar links.', kist(True, True, duw=1, m_hok=4))
groepen = [('Hoofdstuk 1 · Rekenen in de fysica', [zoek('Eenheden omzetten'), zoek('Wetenschappelijke notatie'), zoek('Beduidende cijfers')]),
           ('Hoofdstuk 3 · Zwaartekracht, massa en gewicht', [zoek('Zwaartekracht berekenen'), zoek('Omvormen'), o_graf, zoek('Massa, zwaartekracht of gewicht?'), zoek('Drie krachten'),
                                                         zoek('Zwaartekracht tekenen'), zoek('Boek op tafel: drie krachten'), zoek('Een lamp aan het plafond')]),
           ('Hoofdstuk 5 · Wrijving', [o_w1, o_w2, o_w3, o_w4]),
           ('Hoofdstuk 6 · Veerkracht', [zoek('Veerkracht'), zoek('Een veertje in een balpen'), zoek('Twee veren vergelijken'), zoek('Veerkracht tekenen')])]
oefs = ('<p>Maak deze oefeningen <b>op papier</b>. Tekenoefeningen maak je op de figuur of op ruitjespapier, met een lat en een potlood. De oplossingen verschijnen hier nadat we de oefeningen in de les besproken hebben.</p>'
        '<p><button class="knop licht" data-print="oef">🖨 Druk de oefeningen af</button></p>'
        + ''.join(f'<h3 style="margin-top:22px">{k}</h3>' + ''.join(lst) for k, lst in groepen))
_n = [0]
def _nr(m):
    _n[0] += 1; return f'<div class="oef" data-vrij="opl_{_n[0]}">' + m.group(1) + f'<span class="nr">{_n[0]}</span>'
oefs = re.sub(r'<div class="oef" data-vrij="opl_\w+">(\s*<div class="titel">)<span class="nr">\d+</span>', _nr, oefs) + tool('krachten.html#oef', 'Oefen verder in de tool')

LD = ('<p>Na dit deel kan je:</p><ul class="doelen">' + ''.join(f'<li>{x}</li>' for x in [
    'meetresultaten weergeven in de SI-eenheid, in wetenschappelijke notatie en met het juiste aantal beduidende cijfers;',
    'het verschil uitleggen tussen <b>zwaarteveld</b> en <b>zwaartekracht</b>, en F<sub>z</sub> als vector tekenen;',
    'F<sub>z</sub> = m · g gebruiken en omvormen, en de juiste grafiek herkennen;',
    'het verschil uitleggen tussen <b>massa</b>, <b>gewicht</b> en <b>zwaartekracht</b>, en gewichtloosheid uitleggen;',
    'F<sub>N</sub>, F<sub>z</sub> en F<sub>G</sub> in woorden en als vector onderscheiden;',
    'statische en dynamische wrijving onderscheiden en ABS en aquaplaning uitleggen;',
    'F<sub>w,s,max</sub> = μ<sub>s</sub> · F<sub>N</sub> gebruiken en omvormen;',
    'veerkracht tekenen, F<sub>v</sub> = k · Δl gebruiken en omvormen, grafieken interpreteren en uitleggen wanneer de wet van Hooke geldt.']) + '</ul>')
VK = '<p>Dit moet je al kennen. Twijfel je? Herhaal het dan eerst.</p><ul><li>Een kracht is een <b>vector</b>: aangrijpingspunt, richting, zin, grootte (N).</li><li>Een kracht tekenen op schaal.</li><li>De <b>resulterende kracht</b> en de <b>traagheidswet</b>: F<sub>r</sub> = 0 → rust of ERB.</li><li>Een formule omvormen.</li></ul>'
samenv = kader('Samenvatting', '''<p><b>SI</b>: m, kg, s, N. Wetenschappelijke notatie a · 10<sup>n</sup>. Uitkomst afronden op het kleinste aantal BC.</p>
<p><b>Zwaartekracht</b> F<sub>z</sub> = m · g, in het zwaartepunt, naar het middelpunt van de aarde. <b>Massa</b> (kg) overal gelijk. <b>Gewicht</b> F<sub>G</sub> werkt op de steun; gewichtloos: F<sub>G</sub> = 0. <b>Normaalkracht</b> F<sub>N</sub> werkt op het voorwerp.</p>
<p><b>Wrijving</b>: statisch (in rust, tot F<sub>w,s,max</sub> = μ<sub>s</sub> · F<sub>N</sub>) en dynamisch (schuiven, kleiner).</p>
<p><b>Veerkracht</b> F<sub>v</sub> = k · Δl (wet van Hooke, alleen elastisch). Grote k: stijve veer.</p>''')

pagina('cursus-zwaartekracht-wrijving-veer.html', 'Fysica 3de jaar · Thema 2 Krachten · Hoofdstuk 1, 3, 5 en 6', 'Zwaartekracht, wrijving en veerkracht',
       'Werk dit deel samen met de tools <a href="rekenen-fysica.html">Rekenen in de fysica</a> en <a href="krachten.html">Zwaartekracht, wrijving en veerkracht</a>. Oefeningen maak je op papier. De oplossingen staan online, zodra ze in de les besproken zijn.',
       LD, VK, delen, oefs, samenv, C, eerste=False)
