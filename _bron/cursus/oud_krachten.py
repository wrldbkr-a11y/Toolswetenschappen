# =====================================================================
#  HOOFDSTUK: KRACHTEN, TRAAGHEID EN BEWEGING (3de jaar)
# =====================================================================
def svg_vec(inner, w=560, h=170):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg"><defs><marker id="pk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs>{inner}</svg>'
def pl(x1, y1, x2, y2, kleur, w=4, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    m = '' if dash else ' marker-end="url(#pk)"'
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{kleur}" stroke-width="{w}"{d}{m} stroke-linecap="round"/>'
def tx(x, y, t, kleur='#1D2A36', anker='middle', size=14):
    return f'<text x="{x}" y="{y}" fill="{kleur}" font-size="{size}" font-weight="700" text-anchor="{anker}" font-family="Inter,sans-serif">{t}</text>'
B, G, R = '#2563eb', '#059669', '#dc2626'

fig_vector = svg_vec(f'<circle cx="80" cy="100" r="5" fill="#1D2A36"/>{pl(80,100,330,100,B,5)}{tx(80,128,"aangrijpingspunt")}{tx(210,86,"lengte = grootte (schaal 1 cm ≙ 10 N)",B)}{tx(345,105,"zin →","#1D2A36","start")}<line x1="40" y1="100" x2="520" y2="100" stroke="#94a3b8" stroke-dasharray="5 5"/>{tx(470,90,"richting (werklijn)","#51606E")}', 560, 150)
fig_kopstaart = svg_vec(f'{pl(40,50,200,50,B)}{tx(120,40,"F₁ = 40 N",B)}{pl(40,80,160,80,G)}{tx(100,70,"F₂ = 30 N",G)}{pl(260,60,420,60,B)}{pl(420,60,540,60,G)}{pl(260,100,540,100,R,5)}{tx(400,128,"Fr = F₁ + F₂ = 70 N",R)}', 560, 140)
fig_parall = svg_vec(f'{pl(60,140,260,140,B)}{tx(160,162,"F₁",B)}{pl(60,140,60,40,G)}{tx(42,90,"F₂",G,"end")}{pl(260,140,260,40,"#94a3b8",2,"6 5")}{pl(60,40,260,40,"#94a3b8",2,"6 5")}{pl(60,140,260,40,R,5)}{tx(175,82,"Fr",R)}<rect x="60" y="128" width="12" height="12" fill="none" stroke="#1D2A36"/>{tx(400,70,"1. teken F₁ en F₂ vanuit O","#1D2A36","start",13)}{tx(400,92,"2. hulplijnen evenwijdig","#1D2A36","start",13)}{tx(400,114,"3. diagonaal = Fr","#1D2A36","start",13)}', 560, 175)

k_lesdoelen = '''<p>Na dit hoofdstuk kan je:</p><ul class="doelen">
<li>een kracht voorstellen als <b>vector</b> met aangrijpingspunt, richting, zin en grootte;</li>
<li>de <b>resulterende kracht</b> van twee krachten met <b>dezelfde richting</b> construeren en berekenen;</li>
<li>de resulterende kracht van twee krachten met een <b>verschillende richting</b> construeren met de <b>parallellogrammethode</b>, en ze berekenen als de krachten loodrecht staan;</li>
<li>uitleggen wat <b>traagheid</b> is, en dat een grotere massa een grotere traagheid heeft;</li>
<li>de <b>traagheidswet</b> formuleren en toepassen;</li>
<li>uit de resulterende kracht afleiden of de snelheid van een voorwerp <b>toeneemt, afneemt, gelijk blijft of van richting verandert</b>.</li></ul>
<div class="kader"><div class="kop">Voor de leerkracht</div><p>Deze lesdoelen zijn geformuleerd op basis van de tools. Pas ze aan aan je leerplandoelen als dat nodig is.</p></div>'''

k1 = f'''<p>Een kracht heeft niet alleen een <b>grootte</b>, maar ook een <b>richting</b> en een <b>zin</b>. Daarom stellen we een kracht voor met een pijl: een <b>vector</b>.</p>
{figuur(fig_vector, 'De vier kenmerken van een krachtvector.')}
{kader('Kenmerken van een kracht', '<p><b>Aangrijpingspunt</b>: waar de kracht aangrijpt.<br><b>Richting</b>: de rechte waarop de pijl ligt (horizontaal, verticaal, schuin …).<br><b>Zin</b>: naar welke kant de pijl wijst.<br><b>Grootte</b>: hoe groot de kracht is, in newton (N). Op een tekening is dat de lengte van de pijl, op schaal.</p>')}
{denk('denk_1', 'Je tekent een kracht van 35 N met de schaal 1 cm ≙ 10 N. Hoe lang wordt de pijl?', [
  ('Schaal', '1 cm op papier stelt 10 N voor.'), ('Hoeveel keer 10 N?', '35 N / 10 N = 3,5'), ('Lengte', '3,5 · 1 cm = 3,5 cm')], 'De pijl is 3,5 cm lang.')}'''

k2 = f'''<p>Werken er twee krachten op een voorwerp, dan kan je ze vervangen door <b>één kracht</b> die hetzelfde effect heeft: de <b>resulterende kracht F<sub>r</sub></b>.</p>
<h3>Twee krachten met dezelfde richting</h3>
{figuur(fig_kopstaart, 'Kop-staartmethode: teken F₂ verder vanaf de kop van F₁.')}
<p><b>Zelfde zin</b>: tel de groottes op, F<sub>r</sub> = F₁ + F₂. F<sub>r</sub> heeft dezelfde zin.<br><b>Tegengestelde zin</b>: trek de groottes af, F<sub>r</sub> = F₁ − F₂. F<sub>r</sub> heeft de zin van de grootste kracht.</p>
{tool('krachten-construeren.html#1.1', 'Stap voor stap: zelfde zin')} {tool('krachten-construeren.html#1.2', 'Stap voor stap: tegengestelde zin')}
<h3>Twee krachten met een verschillende richting</h3>
{figuur(fig_parall, 'Parallellogrammethode: de diagonaal vanuit O is de resulterende kracht.')}
<p>Gebruik de <b>parallellogrammethode</b>: teken beide krachten vanuit hetzelfde punt O, teken met je geodriehoek hulplijnen evenwijdig aan de krachten, en teken de diagonaal. Meet de lengte en zet om met de schaal.</p>
<p>Staan de krachten <b>loodrecht</b> op elkaar, dan kan je F<sub>r</sub> ook berekenen met de <b>stelling van Pythagoras</b>: F<sub>r</sub> = √(F₁² + F₂²).</p>
{tool('krachten-construeren.html#2.1', 'Stap voor stap: loodrechte krachten')} {tool('krachten-construeren.html#2.2', 'Stap voor stap: schuine krachten')}
{denk('denk_2', 'Twee krachten van 30 N en 40 N werken op hetzelfde voorwerp. Hoe groot kan de resulterende kracht zijn? Wat is de kleinste en de grootste waarde?', [
  ('Grootste', 'Zelfde richting en zin: 30 N + 40 N = 70 N.'), ('Kleinste', 'Zelfde richting, tegengestelde zin: 40 N − 30 N = 10 N.'), ('Daartussen', 'Bij elke andere hoek ligt F<sub>r</sub> tussen 10 N en 70 N. Loodrecht: √(30² + 40²) = 50 N.')], 'F<sub>r</sub> ligt tussen 10 N en 70 N, afhankelijk van de hoek tussen de krachten.')}'''

k3 = f'''<p>Sta je in een bus of tram van de MIVB die plots vertrekt, dan val je naar achter. Remt de tram, dan val je naar voor. Niemand duwt je: je lichaam wil gewoon blijven doen wat het deed. Dat noemen we <b>traagheid</b>.</p>
{kader('Traagheid', '<p>Elk voorwerp verzet zich tegen een verandering van zijn snelheid: het wil blijven <b>stilstaan</b>, of <b>even snel rechtdoor</b> blijven bewegen. Traagheid is <b>geen kracht</b>.</p><p>Hoe <b>groter de massa</b>, hoe <b>groter de traagheid</b>: een zwaar voorwerp is moeilijk in beweging te brengen en moeilijk te stoppen.</p>')}
{tool('krachten-beweging.html#s1', 'Bekijk de bus in de tool')} {tool('krachten-beweging.html#s2', 'Vergelijk een lege en een volle kar')}
{denk('denk_3', 'Waarom moet een volgeladen vrachtwagen veel vroeger beginnen remmen dan een lege vrachtwagen die even snel rijdt?', [
  ('Wat is verschillend?', 'De volgeladen vrachtwagen heeft een veel grotere massa.'), ('Wat betekent dat?', 'Grotere massa → grotere traagheid: hij verzet zich meer tegen een verandering van snelheid.'), ('Met dezelfde remkracht', 'neemt zijn snelheid trager af. Hij heeft meer tijd en een langere afstand nodig om te stoppen.')], 'De volle vrachtwagen heeft een langere remweg, door zijn grotere traagheid.')}'''

k4 = f'''{kader('Traagheidswet (eerste wet van Newton)', '<p>Is de resulterende kracht op een voorwerp <b>nul</b>, dan blijft het voorwerp in <b>rust</b>, of beweegt het <b>eenparig rechtlijnig</b>: even snel en rechtdoor.</p>')}
<p>Is de resulterende kracht <b>niet nul</b>, dan verandert de snelheid. Vergelijk F<sub>r</sub> met de beweging:</p>
<table class="vb">
<tr><td>F<sub>r</sub> = 0</td><td>de snelheid blijft gelijk (rust of ERB)</td></tr>
<tr><td>F<sub>r</sub> mee met v</td><td>de snelheid neemt toe</td></tr>
<tr><td>F<sub>r</sub> tegen v in</td><td>de snelheid neemt af</td></tr>
<tr><td>F<sub>r</sub> loodrecht op v</td><td>de richting van de snelheid verandert (bocht)</td></tr></table>
<p>Let op: om <b>te blijven bewegen</b> heb je <b>geen</b> kracht nodig. Je hebt een kracht nodig om de snelheid te <b>veranderen</b>.</p>
{tool('krachten-beweging.html#s3', 'Probeer het met de slee in de tool')} {tool('krachten-beweging.html#s3b', 'Een bal die je hand verlaat')}
{denk('denk_4', 'Je rolt een bal weg over het gras. Na een tijdje stopt hij. Sofia zegt: "De bal rolt eerst nog verder omdat de kracht van je hand nog in de bal zit." Klopt dat?', [
  ('Wanneer werkt de kracht van je hand?', 'Alleen zolang je hand de bal raakt. Daarna bestaat die kracht niet meer.'), ('Waarom rolt de bal verder?', 'Door zijn traagheid: hij wil even snel blijven bewegen.'), ('Welke kracht werkt er dan nog (horizontaal)?', 'Alleen de wrijving, tegen de beweging in. F<sub>r</sub> wijst dus naar achter.'), ('Gevolg', 'De snelheid neemt af tot de bal stilligt.')], 'Sofia heeft geen gelijk. De bal krijgt geen kracht mee: hij rolt door zijn traagheid en stopt door de wrijving.')}
{denk('denk_5', 'Een fietser rijdt met constante snelheid rechtdoor. Hij trapt dus. Is de resulterende kracht op de fietser dan groter dan nul?', [
  ('Wat weet je over de beweging?', 'Constante snelheid, rechtdoor: een ERB.'), ('Traagheidswet', 'Bij een ERB is F<sub>r</sub> = 0.'), ('Welke krachten?', 'De trapkracht naar voor is even groot als de wrijving (lucht en weg) naar achter.')], 'F<sub>r</sub> = 0: de trapkracht en de wrijving heffen elkaar op.')}'''

k_oef = f'''<p>Maak deze oefeningen <b>op papier</b>. Bij constructies gebruik je een lat en een geodriehoek. De oplossingen verschijnen hier nadat we de oefeningen in de les besproken hebben.</p>
<p><button class="knop licht" data-print="oef">🖨 Druk de oefeningen af</button></p>
{oef('opl_1', 1, 'Zelfde zin', 'Twee krachten van 30 N en 50 N werken op hetzelfde punt, in dezelfde richting en zin. Construeer F<sub>r</sub> met de schaal 1 cm ≙ 10 N en bereken F<sub>r</sub>.', [
  ('Constructie', 'F₁ = 3,0 cm, F₂ = 5,0 cm kop aan staart: F<sub>r</sub> = 8,0 cm.'), ('Berekening', 'F<sub>r</sub> = 30 N + 50 N = 80 N')], 'F<sub>r</sub> = 80 N, in dezelfde zin als beide krachten.')}
{oef('opl_2', 2, 'Tegengestelde zin', 'Op een kar werkt een kracht van 70 N naar rechts en een kracht van 25 N naar links. Construeer F<sub>r</sub> (1 cm ≙ 10 N) en bereken F<sub>r</sub>. Welke zin heeft F<sub>r</sub>?', [
  ('Berekening', 'F<sub>r</sub> = 70 N − 25 N = 45 N'), ('Zin', 'de zin van de grootste kracht: naar rechts')], 'F<sub>r</sub> = 45 N naar rechts (4,5 cm op de tekening).')}
{oef('opl_3', 3, 'Touwtrekken', 'Team A trekt met 4 kinderen van elk 150 N naar links. Team B trekt met 3 kinderen van elk 180 N naar rechts. Bereken F<sub>r</sub> op het touw. Welk team wint?', [
  ('Team A', '4 · 150 N = 600 N naar links'), ('Team B', '3 · 180 N = 540 N naar rechts'), ('F<sub>r</sub>', '600 N − 540 N = 60 N naar links')], 'F<sub>r</sub> = 60 N naar links: team A wint.')}
{oef('opl_4', 4, 'Loodrechte krachten', 'F₁ = 40 N werkt horizontaal naar rechts, F₂ = 30 N verticaal naar boven, in hetzelfde punt. Construeer F<sub>r</sub> met de parallellogrammethode (1 cm ≙ 10 N). Meet F<sub>r</sub> en controleer met de stelling van Pythagoras.', [
  ('Constructie', 'De diagonaal van de rechthoek (4,0 cm × 3,0 cm) is 5,0 cm lang.'), ('Pythagoras', 'F<sub>r</sub> = √(40² + 30²) = √2500 = 50 N')], 'F<sub>r</sub> = 50 N, schuin naar rechtsboven.')}
{oef('opl_5', 5, 'Schuine krachten', 'Twee krachten van elk 50 N werken in hetzelfde punt. De hoek tussen beide is 60°. Construeer F<sub>r</sub> met de parallellogrammethode (1 cm ≙ 10 N) en meet de grootte.', [
  ('Constructie', 'Het parallellogram is een ruit. De diagonaal meet ongeveer 8,7 cm.'), ('Controle', 'F<sub>r</sub> ligt tussen 0 N en 100 N en precies in het midden tussen beide krachten (30° met elk).')], 'F<sub>r</sub> ≈ 87 N')}
{oef('opl_6', 6, 'Traagheid uitleggen', 'Leg telkens uit met het begrip traagheid.<ol class="deelvragen" type="a"><li>Waarom draag je een gordel in de auto?</li><li>Waarom kan je een tafelkleed snel wegtrekken zonder dat de borden vallen?</li><li>Waarom is een volle winkelkar moeilijker te stoppen dan een lege?</li></ol>', [
  ('a', 'Remt de auto plots, dan wil je lichaam even snel verder bewegen. De gordel houdt je tegen.'), ('b', 'De borden willen blijven stilstaan. Trek je snel, dan hebben ze geen tijd om mee te bewegen.'), ('c', 'De volle kar heeft een grotere massa, dus een grotere traagheid.')], 'Traagheid: een voorwerp wil blijven doen wat het deed.')}
{oef('opl_7', 7, 'Wat gebeurt er met de snelheid?', 'Bepaal telkens F<sub>r</sub> (grootte en zin). Zeg dan of de snelheid toeneemt, afneemt of gelijk blijft.<ol class="deelvragen" type="a"><li>Een auto rijdt rechtdoor. De motorkracht is 2000 N naar voor, de wrijving 2000 N naar achter.</li><li>Een fietser stopt met trappen. Alleen de wrijving van 30 N naar achter werkt nog.</li><li>Een slee staat stil. Een kind trekt met 40 N naar voor, de wrijving is 15 N.</li><li>Een ruimtesonde vliegt ver in de ruimte met uitgeschakelde motor.</li></ol>', [
  ('a', 'F<sub>r</sub> = 0 → snelheid blijft gelijk (ERB).'), ('b', 'F<sub>r</sub> = 30 N naar achter, tegen de beweging → snelheid neemt af.'), ('c', 'F<sub>r</sub> = 40 N − 15 N = 25 N naar voor → de slee begint te bewegen, de snelheid neemt toe.'), ('d', 'F<sub>r</sub> ≈ 0 → de sonde vliegt even snel rechtdoor.')], 'Vergelijk altijd de zin van F<sub>r</sub> met de zin van de beweging.')}
{oef('opl_8', 8, 'Juist of fout?', 'Juist of fout? Verbeter de foute uitspraken.<ol class="deelvragen" type="a"><li>Een voorwerp dat beweegt, heeft altijd een kracht nodig om te blijven bewegen.</li><li>Als F<sub>r</sub> = 0, dan staat het voorwerp zeker stil.</li><li>Een bal die je weggooit, krijgt een kracht mee van je hand.</li><li>Hoe groter de massa, hoe groter de traagheid.</li></ol>', [
  ('a', 'Fout: om te blijven bewegen is geen kracht nodig. Een kracht is nodig om de snelheid te veranderen.'), ('b', 'Fout: het voorwerp staat stil óf beweegt even snel rechtdoor.'), ('c', 'Fout: de kracht van je hand bestaat alleen zolang je de bal raakt.'), ('d', 'Juist.')], 'Alleen d is juist.')}
{tool('krachten-beweging.html#s7', 'Extra oefenen in de tool')}'''

k_cornell = d_cornell
k_samenv = f'''{kader('Samenvatting', '''<p>Een <b>kracht</b> is een vector: aangrijpingspunt, richting, zin en grootte (N).</p>
<p><b>Resulterende kracht</b>: zelfde zin → F<sub>r</sub> = F₁ + F₂; tegengestelde zin → F<sub>r</sub> = F₁ − F₂; verschillende richting → parallellogrammethode (loodrecht: Pythagoras).</p>
<p><b>Traagheid</b>: een voorwerp wil zijn snelheid behouden. Meer massa → meer traagheid.</p>
<p><b>Traagheidswet</b>: F<sub>r</sub> = 0 → rust of ERB. F<sub>r</sub> mee met v → sneller; tegen v → trager; loodrecht → bocht.</p>''')}'''

bouw('cursus-krachten-beweging.html', 'Fysica 3de jaar · Krachten', 'Krachten, traagheid en beweging',
     'Werk dit hoofdstuk samen met de tools <a href="krachten-construeren.html">Krachten samenstellen</a> en <a href="krachten-beweging.html">Traagheid, resulterende kracht en beweging</a>. Oefeningen maak je op papier.',
     [blok('lesdoelen', '', 'Lesdoelen', k_lesdoelen),
      blok('voorkennis', '', 'Voorkennis', '<p>Dit moet je al kennen. Twijfel je? Herhaal het dan eerst.</p><ul><li><b>Grootheden en eenheden</b>: elke grootheid heeft een symbool en een SI-eenheid, bv. massa m in kg, kracht F in N (hoofdstuk Rekenen in de fysica).</li><li><b>Zwaartekracht</b>: F<sub>z</sub> = m · g met g = 9,81 N/kg.</li><li>Met een <b>lat</b> lengtes meten en met een <b>geodriehoek</b> hoeken meten en tekenen.</li><li><b>Stelling van Pythagoras</b> (wiskunde): in een rechthoekige driehoek is c² = a² + b².</li></ul>'),
      blok('deel1', 1, 'Een kracht is een vector', k1, 'deel1'),
      blok('deel2', 2, 'Krachten samenstellen', k2, 'deel2'),
      blok('deel3', 3, 'Traagheid', k3, 'deel3'),
      blok('deel4', 4, 'Resulterende kracht en beweging', k4, 'deel4'),
      blok('oefeningen', '', 'Oefeningen op papier', k_oef, 'oefeningen'),
      blok('samenvatting', '', 'Samenvatting', k_samenv, 'samenvatting')],
     [('deel1', True, 'Een kracht is een vector'), ('deel2', False, 'Krachten samenstellen'), ('deel3', False, 'Traagheid'), ('deel4', False, 'Resulterende kracht en beweging'),
      ('denk_1', False, 'redenering denkvraag deel 1'), ('denk_2', False, 'redenering denkvraag deel 2'), ('denk_3', False, 'redenering denkvraag deel 3'), ('denk_4', False, 'redenering denkvraag deel 4 (bal)'), ('denk_5', False, 'redenering denkvraag deel 4 (fietser)'),
      ('oefeningen', False, 'de oefeningen zelf (opgaven)')] + [(f'opl_{i}', False, f'oplossing oefening {i}') for i in range(1, 9)] + [('samenvatting', False, 'samenvatting')],
     [['Wat zijn de kenmerken van een kracht?', 26], ['Hoe bepaal je F<sub>r</sub> bij krachten met dezelfde richting?', 30], ['Hoe construeer je F<sub>r</sub> bij krachten met een verschillende richting?', 34], ['Wat is traagheid? Hoe hangt ze af van de massa?', 26], ['Wat zegt de traagheidswet?', 22], ['Wat gebeurt er met de snelheid bij F<sub>r</sub> = 0, mee met v, tegen v, loodrecht op v?', 34]])
