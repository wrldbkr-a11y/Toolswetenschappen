import json, html

SJABLOON = open('/home/claude/cursus/sjabloon.html', encoding='utf-8').read()

def denk(id, vraag, stappen, besluit):
    lis = ''.join(f'<li><span class="stap">{s[0]}</span> {s[1]}</li>' for s in stappen)
    return f'''<div class="denk" data-vrij="{id}">
  <div class="vraag"><div class="kop">Denkvraag</div><p>{vraag}</p></div>
  <div class="onder"><div class="redenering"><ol>{lis}</ol><div class="besluit">{besluit}</div></div></div>
</div>'''

def oef(id, nr, titel, tekst, stappen, besluit):
    lis = ''.join(f'<li><span class="stap">{s[0]}</span> {s[1]}</li>' for s in stappen)
    return f'''<div class="oef" data-vrij="{id}">
  <div class="titel"><span class="nr">{nr}</span>{titel}</div>
  <div class="tekst">{tekst}</div>
  <div class="onder" style="margin-top:8px"></div>
  <div class="redenering"><ol>{lis}</ol><div class="besluit">{besluit}</div></div>
</div>'''

def blok(id, nr, titel, inhoud, vrij=None):
    v = f' data-vrij="{vrij}"' if vrij else ''
    n = f'<span class="nr">{nr}</span>' if nr else ''
    return f'<section class="blok" id="{id}"{v}>\n<h2>{n}{titel}</h2>\n{inhoud}\n</section>\n'

def tool(href, tekst):
    return f'<a class="toolknop" href="{href}" target="_blank" rel="noopener">▶ {tekst}</a>'

def kader(kop, tekst):
    return f'<div class="kader"><div class="kop">{kop}</div>{tekst}</div>'

def figuur(svg, onderschrift=''):
    return f'<figure class="figuur">{svg}<figcaption>{onderschrift}</figcaption></figure>'

def bouw(bestand, eyebrow, titel, intro, blokken, vrijgave, cornell):
    vr = '\n'.join(f'  {k}: {"true" if v else "false"},' + ' '*(24-len(k)-len(str(v))) + f'// {uitleg}' for k, v, uitleg in vrijgave)
    s = (SJABLOON.replace('{{TITEL}}', titel).replace('{{EYEBROW}}', eyebrow).replace('{{INTRO}}', intro)
         .replace('{{INHOUD}}', ''.join(blokken)).replace('{{VRIJGAVE}}', vr)
         .replace('{{CORNELL}}', json.dumps(cornell, ensure_ascii=False)).replace('{{BESTAND}}', bestand).replace('{{FOOTER}}', FOOTER))
    open('/home/claude/toolswetenschappen/' + bestand, 'w', encoding='utf-8').write(s)

FOOTER = 'Cursus fysica — gemaakt voor klasgebruik, bij de tools op Oefentools wetenschappen.'
STAP = '<div class="stappenplan"><span>1 · gegeven</span><span>2 · gevraagd</span><span>3 · formule</span><span>4 · oplossing</span><span>5 · antwoord met eenheid</span></div>'

# =====================================================================
#  HOOFDSTUK: DRUK BIJ VASTE STOFFEN (4de jaar)
# =====================================================================
fig_steen = '''<svg viewBox="0 0 600 190" width="600" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="140" width="600" height="50" fill="#e9d29a"/>
<g><rect x="40" y="128" width="140" height="20" fill="#b4532a" stroke="#7c2d12"/><text x="110" y="178" text-anchor="middle" font-size="14" font-family="Inter,sans-serif" fill="#1D2A36">plat: A = 200 cm²</text></g>
<g><rect x="240" y="114" width="140" height="40" fill="#b4532a" stroke="#7c2d12"/><text x="310" y="178" text-anchor="middle" font-size="14" font-family="Inter,sans-serif" fill="#1D2A36">zijkant: A = 100 cm²</text></g>
<g><rect x="470" y="40" width="40" height="122" fill="#b4532a" stroke="#7c2d12"/><text x="490" y="182" text-anchor="middle" font-size="14" font-family="Inter,sans-serif" fill="#1D2A36">rechtop: A = 50 cm²</text></g>
<text x="300" y="24" text-anchor="middle" font-size="14" font-weight="700" font-family="Inter,sans-serif" fill="#1D2A36">Dezelfde baksteen (F = 19,6 N), drie keer een ander contactoppervlak</text>
</svg>'''

d_lesdoelen = '''<p>Na dit hoofdstuk kan je:</p><ul class="doelen">
<li>het begrip <b>druk</b> uitleggen;</li>
<li>de formule van druk gebruiken en ze <b>omvormen</b> om de kracht en de oppervlakte te berekenen;</li>
<li>met de factoren die de druk beïnvloeden uitleggen waarom een voorwerp <b>drukverhogend</b> of <b>drukverlagend</b> is (bv. een mes, rupsbanden);</li>
<li><b>beredeneren</b> wat er met de druk gebeurt als de kracht en/of de oppervlakte met een bepaalde factor groter of kleiner worden.</li></ul>'''

d1 = f'''<p>Druk je met je duim op een stuk hout, dan gebeurt er niets. Druk je even hard op een <b>punaise</b>, dan gaat de punaise in het hout. De kracht is dezelfde, maar het <b>contactoppervlak</b> is veel kleiner. Daardoor is de <b>druk</b> veel groter.</p>
{figuur(fig_steen, 'Hoe kleiner het contactoppervlak, hoe dieper de steen in het zand zakt.')}
{kader('Definitie', '<p><b>Druk</b> is de kracht per oppervlakte-eenheid. Druk vertelt hoe sterk een kracht verdeeld is over een oppervlak.</p>')}
<p>Om de druk te berekenen, deel je de kracht door de oppervlakte waarop ze werkt:</p>
<div class="formule">p = F / A</div>
<table class="vb"><tr><td>p</td><td>druk, in pascal (Pa)</td></tr><tr><td>F</td><td>kracht loodrecht op het oppervlak, in newton (N)</td></tr><tr><td>A</td><td>oppervlakte, in vierkante meter (m²)</td></tr></table>
<p>1 Pa = 1 N/m². Dat is een kleine druk: een blad papier dat plat op tafel ligt, geeft ongeveer 1 Pa. Daarom gebruik je vaak <b>kPa</b> (1 kPa = 1000 Pa) of <b>hPa</b> (1 hPa = 100 Pa).</p>
{tool('druk.html#s1', 'Probeer het in de tool: bakstenen op zand')}
{denk('denk_1', 'Waarom zak je met gewone schoenen diep weg in verse sneeuw, maar met sneeuwschoenen niet? Je gewicht is toch hetzelfde?', [
  ('Wat blijft gelijk?', 'Je gewicht, dus de kracht F op de sneeuw, is in beide gevallen even groot.'),
  ('Wat verandert er?', 'Sneeuwschoenen hebben een veel grotere oppervlakte A dan gewone schoenen.'),
  ('Wat zegt de formule?', 'p = F / A: dezelfde F gedeeld door een grotere A geeft een kleinere p.'),
], 'Met sneeuwschoenen is de druk op de sneeuw kleiner, daarom zak je minder diep weg.')}'''

d2 = f'''<p>In de formule moet de oppervlakte in <b>m²</b> staan. Vaak krijg je ze in cm² of mm². Dan moet je eerst omzetten.</p>
{kader('Oppervlakte omzetten', '<p>1 m = 100 cm, dus <b>1 m² = 100 cm × 100 cm = 10 000 cm²</b><br>1 m = 1000 mm, dus <b>1 m² = 1 000 000 mm²</b></p><p>Van cm² naar m²: <b>delen door 10 000</b>. Bv. 250 cm² = 250 / 10 000 m² = 0,025 m²</p>')}
<h3>Formule omvormen</h3>
<p>Ken je de druk en zoek je de kracht of de oppervlakte? Vorm dan de formule om:</p>
<div class="formule">F = p · A</div> &nbsp; <div class="formule">A = F / p</div>
<h3>Uitgewerkt voorbeeld</h3>
<p>Een kist van 24 kg staat op de grond. Het contactoppervlak is 400 cm². Bereken de druk op de grond.</p>
{STAP}
<table class="vb">
<tr><td>Gegeven</td><td>m = 24 kg &nbsp;·&nbsp; A = 400 cm² = 0,0400 m² &nbsp;·&nbsp; g = 9,81 N/kg</td></tr>
<tr><td>Gevraagd</td><td>p = ?</td></tr>
<tr><td>Formule</td><td>F = m · g en p = F / A</td></tr>
<tr><td>Oplossing</td><td>F = 24 kg · 9,81 N/kg = 235,4 N<br>p = 235,4 N / 0,0400 m² = 5886 Pa</td></tr>
<tr><td>Antwoord</td><td>De druk op de grond is 5,9 · 10³ Pa (= 5,9 kPa).</td></tr></table>
{denk('denk_2', 'Yasmine berekent de druk van dezelfde kist, maar vult 400 in voor A in plaats van 0,0400. Welke druk vindt zij? Is die te groot of te klein, en hoeveel keer?', [
  ('Wat rekent Yasmine uit?', 'p = 235,4 N / 400 = 0,59 Pa.'),
  ('Vergelijk met de juiste uitkomst.', '5886 Pa / 0,59 Pa = 10 000.'),
  ('Waar komt die factor vandaan?', '400 cm² is maar 0,0400 m². Het getal 400 is dus 10 000 keer te groot, en daardoor wordt haar druk 10 000 keer te klein.'),
], 'Haar druk is 10 000 keer te klein. Zet de oppervlakte altijd eerst om naar m².')}'''

d3 = f'''<p>Uit p = F / A volgt: hoe <b>kleiner</b> de oppervlakte, hoe <b>groter</b> de druk. Hoe <b>groter</b> de oppervlakte, hoe <b>kleiner</b> de druk.</p>
{kader('Drukverhogend en drukverlagend', '<p><b>Drukverhogend</b>: een kleine oppervlakte zorgt voor een grote druk. Bv. een scherp mes, de punt van een spijker of naald, de noppen onder voetbalschoenen, de smalle stalen wielen van een tram van de MIVB op de rails.</p><p><b>Drukverlagend</b>: een grote oppervlakte zorgt voor een kleine druk. Bv. sneeuwschoenen, rupsbanden, brede schouderbanden van een rugzak, brede banden van een tractor.</p>')}
{tool('druk.html#s2', 'Bekijk de voorbeelden in de tool')}
{denk('denk_3', 'Een punaise is tegelijk drukverhogend én drukverlagend. Hoe kan dat?', [
  ('Kijk naar de twee uiteinden.', 'De punaise heeft een scherpe punt en een brede, platte kop.'),
  ('Wat is de kracht?', 'De kracht van je duim gaat door de punaise heen: op de kop en op de punt werkt even veel kracht.'),
  ('Vergelijk de oppervlakten.', 'De punt heeft een heel kleine oppervlakte: grote druk op het hout. De kop heeft een grote oppervlakte: kleine druk op je duim.'),
], 'De punt is drukverhogend (ze dringt in het hout), de kop is drukverlagend (je duim doet geen pijn).')}'''

d4 = f'''<p>Je hoeft niet altijd te rekenen. Vaak kan je <b>redeneren</b> met de formule p = F / A:</p>
<ul><li>F wordt <b>2 keer zo groot</b>, A blijft gelijk → p wordt <b>2 keer zo groot</b> (p is recht evenredig met F).</li>
<li>A wordt <b>2 keer zo groot</b>, F blijft gelijk → p wordt <b>2 keer zo klein</b> (p is omgekeerd evenredig met A).</li></ul>
{kader('Werkwijze', '<p>Schrijf de factor van F boven de breuk en de factor van A eronder. Bv. F × 3 en A × 2: p wordt × 3/2 = × 1,5.</p>')}
{tool('druk.html#s2', 'Oefen met de factoren in de tool')}
{denk('denk_4', 'Een kast staat op 4 poten. Je zet er boeken in, waardoor de kracht op de vloer 2 keer zo groot wordt. Je vervangt ook de poten door poten met een 4 keer zo grote oppervlakte. Wat gebeurt er met de druk op de vloer?', [
  ('Factor van F', 'F wordt × 2.'),
  ('Factor van A', 'A wordt × 4.'),
  ('Combineer', 'p wordt × 2/4 = × 1/2.'),
], 'De druk wordt 2 keer zo klein (gehalveerd).')}'''

d_oef = f'''<p>Maak deze oefeningen <b>op papier</b>, in je schrift. Gebruik telkens het stappenplan. De oplossingen verschijnen hier nadat we de oefeningen in de les besproken hebben.</p>
{STAP}
<p><button class="knop licht" data-print="oef">🖨 Druk de oefeningen af</button></p>
{oef('opl_1', 1, 'Omzetten', 'Zet om.<ol class="deelvragen" type="a"><li>25 cm² = … m²</li><li>0,30 m² = … cm²</li><li>4 mm² = … m²</li><li>3,5 kPa = … Pa</li></ol>', [
  ('a', '25 / 10 000 = 0,0025 m²'), ('b', '0,30 · 10 000 = 3000 cm²'), ('c', '4 / 1 000 000 = 0,000004 m² = 4 · 10⁻⁶ m²'), ('d', '3,5 · 1000 = 3500 Pa')], 'Van cm² naar m²: ÷ 10 000. Van mm² naar m²: ÷ 1 000 000.')}
{oef('opl_2', 2, 'Druk van een kist', 'Een kist van 30 kg staat op een vloer. Het contactoppervlak is 0,25 m². Bereken de druk op de vloer.', [
  ('Gegeven', 'm = 30 kg · A = 0,25 m² · g = 9,81 N/kg'), ('Gevraagd', 'p'), ('Formule', 'F = m · g en p = F / A'),
  ('Oplossing', 'F = 30 · 9,81 = 294,3 N &nbsp;→&nbsp; p = 294,3 N / 0,25 m² = 1177 Pa')], 'p = 1,18 · 10³ Pa')}
{oef('opl_3', 3, 'Naaldhak of olifant?', 'Een vrouw van 60 kg staat even op één naaldhak met een oppervlakte van 1,0 cm². Een olifant van 4000 kg staat op 4 poten van elk 700 cm².<ol class="deelvragen" type="a"><li>Bereken de druk onder de naaldhak.</li><li>Bereken de druk onder de olifant.</li><li>Wie veroorzaakt de grootste druk? Hoeveel keer zo groot?</li></ol>', [
  ('a', 'F = 60 · 9,81 = 588,6 N · A = 1,0 cm² = 1,0 · 10⁻⁴ m² · p = 588,6 / 1,0 · 10⁻⁴ = 5,9 · 10⁶ Pa'),
  ('b', 'F = 4000 · 9,81 = 39 240 N · A = 4 · 700 cm² = 2800 cm² = 0,28 m² · p = 39 240 / 0,28 = 1,4 · 10⁵ Pa'),
  ('c', '5,9 · 10⁶ / 1,4 · 10⁵ ≈ 42')], 'De naaldhak geeft een ongeveer 42 keer zo grote druk als de olifant!')}
{oef('opl_4', 4, 'Kracht berekenen', 'De band van een tractor oefent een druk van 80 kPa uit op de grond. Het contactoppervlak van de band is 0,15 m². Hoe groot is de kracht van die band op de grond?', [
  ('Gegeven', 'p = 80 kPa = 80 000 Pa · A = 0,15 m²'), ('Gevraagd', 'F'), ('Formule', 'F = p · A'), ('Oplossing', 'F = 80 000 Pa · 0,15 m² = 12 000 N')], 'F = 1,2 · 10⁴ N')}
{oef('opl_5', 5, 'Oppervlakte berekenen', 'Een kast oefent een kracht van 900 N uit op een houten vloer. De vloer kan een druk van ten hoogste 30 kPa verdragen. Hoe groot moet het contactoppervlak minstens zijn? Geef je antwoord in cm².', [
  ('Gegeven', 'F = 900 N · p = 30 kPa = 30 000 Pa'), ('Gevraagd', 'A (in cm²)'), ('Formule', 'A = F / p'), ('Oplossing', 'A = 900 N / 30 000 Pa = 0,030 m² = 0,030 · 10 000 cm² = 300 cm²')], 'Het contactoppervlak moet minstens 300 cm² zijn.')}
{oef('opl_6', 6, 'Redeneren', 'Wat gebeurt er met de druk? Leg uit met de formule.<ol class="deelvragen" type="a"><li>F wordt 3 keer zo groot, A blijft gelijk.</li><li>F blijft gelijk, A wordt 2 keer zo klein.</li><li>F wordt 2 keer zo groot, A wordt 4 keer zo groot.</li><li>F en A worden allebei 2 keer zo klein.</li></ol>', [
  ('a', 'p × 3: de druk wordt 3 keer zo groot.'), ('b', 'p × 1 / (1/2) = × 2: de druk wordt 2 keer zo groot.'), ('c', 'p × 2/4 = × 1/2: de druk wordt 2 keer zo klein.'), ('d', 'p × (1/2)/(1/2) = × 1: de druk blijft gelijk.')], 'Factor van F boven, factor van A onder de breuk.')}
{oef('opl_7', 7, 'Uitleggen', 'Is het drukverhogend of drukverlagend? Leg telkens uit met de oppervlakte en de druk.<ol class="deelvragen" type="a"><li>Een rugzak heeft brede schouderbanden.</li><li>Een spijker heeft een scherpe punt.</li><li>Een vrachtwagen voor zacht terrein heeft brede banden.</li><li>Een schaats heeft een dun ijzer.</li></ol>', [
  ('a', 'Drukverlagend: grote oppervlakte → kleine druk op je schouders.'), ('b', 'Drukverhogend: kleine oppervlakte → grote druk, de spijker gaat makkelijk in het hout.'),
  ('c', 'Drukverlagend: grote oppervlakte → kleine druk, de vrachtwagen zakt niet weg.'), ('d', 'Drukverhogend: kleine oppervlakte → grote druk op het ijs.')], 'Kleine A → grote p (drukverhogend). Grote A → kleine p (drukverlagend).')}
{oef('opl_8', 8, 'De baksteen', 'Een baksteen van 2,0 kg is 20 cm lang, 10 cm breed en 5,0 cm hoog. Bereken de druk op de grond als de steen (a) plat ligt, (b) op de zijkant ligt en (c) rechtop staat. Wanneer is de druk het grootst?', [
  ('Kracht', 'F = 2,0 · 9,81 = 19,6 N (in alle gevallen gelijk)'),
  ('a', 'A = 20 · 10 = 200 cm² = 0,020 m² → p = 19,6 / 0,020 = 981 Pa'),
  ('b', 'A = 20 · 5,0 = 100 cm² = 0,010 m² → p = 1962 Pa'),
  ('c', 'A = 10 · 5,0 = 50 cm² = 0,0050 m² → p = 3924 Pa')], 'Rechtop is de druk het grootst: het kleinste contactoppervlak.')}
{tool('druk.html#s12', 'Extra oefenen in de tool (kies: vaste stoffen)')}'''

d_cornell = f'''<p>Op het bord bouwen we samen een <b>Cornellschema</b> op. Links staan de vragen, rechts noteer je de antwoorden die we samen opbouwen. Onderaan vat je alles samen in je eigen woorden. Dek thuis de rechterkolom af en overhoor jezelf met de vragen links.</p>
<p><button class="knop licht" data-print="cornell">🖨 Druk het Cornellblad af</button></p>'''

d_samenv = f'''{kader('Samenvatting', '''<p><b>Druk</b> is kracht per oppervlakte-eenheid: <b>p = F / A</b>, in pascal (1 Pa = 1 N/m²).</p>
<p>Omvormen: <b>F = p · A</b> en <b>A = F / p</b>. Zet de oppervlakte altijd om naar <b>m²</b> (1 m² = 10 000 cm²).</p>
<p>Kleine oppervlakte → grote druk: <b>drukverhogend</b> (mes, spijker). Grote oppervlakte → kleine druk: <b>drukverlagend</b> (sneeuwschoenen, rupsbanden).</p>
<p>p is recht evenredig met F en omgekeerd evenredig met A.</p>''')}'''

bouw('cursus-druk-vaste-stoffen.html', 'Fysica 4de jaar · Thema 1 Druk · Hoofdstuk 1', 'Druk bij vaste stoffen',
     'Werk dit hoofdstuk samen met de tool <a href="druk.html">Druk</a>. Oefeningen maak je op papier.',
     [blok('lesdoelen', '', 'Lesdoelen', d_lesdoelen),
      blok('voorkennis', '', 'Voorkennis', '<p>Dit moet je al kennen. Twijfel je? Herhaal het dan eerst.</p><ul><li>Een <b>kracht</b> is een vector, in newton (N). De kracht begint op het voorwerp waarop ze werkt.</li><li><b>Zwaartekracht</b>: F<sub>z</sub> = m · g met g = 9,81 N/kg. Massa in kg (1 kg = 1000 g).</li><li><b>Oppervlakte</b> berekenen: rechthoek = lengte · breedte, cirkel = π · r².</li><li>Lengtes omzetten: 1 m = 100 cm = 1000 mm.</li></ul>'),
      blok('deel1', 1, 'Wat is druk?', d1, 'deel1'),
      blok('deel2', 2, 'Rekenen met druk', d2, 'deel2'),
      blok('deel3', 3, 'Drukverhogend en drukverlagend', d3, 'deel3'),
      blok('deel4', 4, 'Redeneren met druk', d4, 'deel4'),
      blok('oefeningen', '', 'Oefeningen op papier', d_oef, 'oefeningen'),
      blok('samenvatting', '', 'Samenvatting', d_samenv, 'samenvatting')],
     [('deel1', True, 'Wat is druk?'), ('deel2', False, 'Rekenen met druk'), ('deel3', False, 'Drukverhogend en drukverlagend'), ('deel4', False, 'Redeneren met druk'),
      ('denk_1', False, 'redenering denkvraag deel 1'), ('denk_2', False, 'redenering denkvraag deel 2'), ('denk_3', False, 'redenering denkvraag deel 3'), ('denk_4', False, 'redenering denkvraag deel 4'),
      ('oefeningen', False, 'de oefeningen zelf (opgaven)')] + [(f'opl_{i}', False, f'oplossing oefening {i}') for i in range(1, 9)] + [('samenvatting', False, 'samenvatting')],
     [['Wat is druk?', 22], ['Met welke formule bereken je druk? Wat is de eenheid?', 26], ['Hoe bereken je F of A als je p kent?', 22], ['Hoe zet je cm² en mm² om naar m²?', 22], ['Wanneer is iets drukverhogend of drukverlagend? Geef voorbeelden.', 34], ['Wat gebeurt er met p als F of A verandert?', 30]])

print('klaar')
