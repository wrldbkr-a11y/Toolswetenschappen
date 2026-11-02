exec(open('/home/claude/cursus/ac_help.py', encoding='utf-8').read())
zet_hfst(2)
TOOL = 'krachten-op-ladingen.html'
BL = '#1D4ED8'

def fpijl(x, y, L, kleur=BL, w=3):
    """kracht die op de lading begint (x,y) en L lang is (negatief = naar links)"""
    return pijl(x, y, x + L, y, kleur, w)

def fig_zin():
    s = ''
    rijen = [(1, 1, 'gelijke ladingen: afstoting'), (-1, -1, 'gelijke ladingen: afstoting'), (1, -1, 'tegengestelde ladingen: aantrekking')]
    for i, (a, b, t) in enumerate(rijen):
        y = 40 + i * 70; xa, xb = 200, 360
        s += f'<line x1="{xa}" y1="{y}" x2="{xb}" y2="{y}" stroke="#CBD5E1" stroke-dasharray="4 4"/>'
        if a == b: s += fpijl(xa, y, -70) + fpijl(xb, y, 70)
        else: s += fpijl(xa, y, 60) + fpijl(xb, y, -60)
        s += q(xa, y, a, 11) + q(xb, y, b, 11) + tx(450, y + 5, t, 13, INK, 'start', 600)
    s += tx(280, 228, 'De krachten liggen op de verbindingslijn, zijn even groot en tegengesteld.', 13, DIM, 'middle', 400)
    return svg(s, 720, 240)

def fig_grafiek():
    X0, Y0, W, H = 70, 20, 440, 200
    pts = ' L'.join(f'{X0 + r * W / 4:.1f},{Y0 + H - min(H, H * 0.9 / r**2):.1f}' for r in [i / 50 for i in range(48, 201)])
    s = f'<path d="M{X0},{Y0} V{Y0+H} H{X0+W}" fill="none" stroke="{INK}" stroke-width="2"/>'
    s += f'<path d="M{pts}" fill="none" stroke="{BL}" stroke-width="3"/>'
    for r, lab in [(1, 'F'), (2, 'F/4'), (3, 'F/9')]:
        x, y = X0 + r * W / 4, Y0 + H - H * 0.9 / r**2
        s += f'<line x1="{x}" y1="{y}" x2="{x}" y2="{Y0+H}" stroke="#94A3B8" stroke-dasharray="4 3"/><circle cx="{x}" cy="{y}" r="5" fill="{BL}"/>'
        s += tx(x + 8, y - 8, lab, 14, BL, 'start') + tx(x, Y0 + H + 18, ['r', '2r', '3r'][r - 1], 13, INK)
    s += tx(X0 - 10, Y0 + 10, 'F', 15, INK, 'end') + tx(X0 + W, Y0 + H + 18, 'afstand', 13, DIM, 'end', 400)
    return svg(s, 560, 250)

def fig_lijn():
    y = 70; sc = 1500
    x1, x2, x3 = 70, 70 + 0.10 * sc, 70 + 0.30 * sc
    s = f'<line x1="40" y1="{y}" x2="600" y2="{y}" stroke="#CBD5E1"/>'
    s += pijl(x2, y, x2 + 146, y, POS, 5) + tx(x2 + 75, y - 14, 'F_r = 4,0 N', 13, POS)
    for x, l, t in [(x1, 1, 'Q₁ = +4,0 μC'), (x2, 1, 'Q₂ = +1,0 μC'), (x3, -1, 'Q₃ = −2,0 μC')]:
        s += q(x, y, l, 11) + tx(x, y + 34, t, 13)
    s += tx((x1 + x2) / 2, y + 56, '10 cm', 12, DIM, 'middle', 400) + tx((x2 + x3) / 2, y + 56, '20 cm', 12, DIM, 'middle', 400)
    # krachtendiagram kop-staart
    yd = 175; xd = 230
    s += tx(70, yd + 5, 'krachten op Q₂ (kop-staart):', 13, INK, 'start')
    s += pijl(xd + 30, yd, xd + 160, yd, BL) + tx(xd + 95, yd - 10, 'F₁₂ = 3,6 N', 12, BL)
    s += pijl(xd + 160, yd, xd + 176, yd, '#0F766E') + tx(xd + 230, yd - 10, 'F₃₂ = 0,45 N', 12, '#0F766E')
    s += pijl(xd + 30, yd + 22, xd + 176, yd + 22, POS, 4) + tx(xd + 103, yd + 42, 'F_r', 12, POS)
    return svg(s.replace('F_r', 'F<tspan baseline-shift="sub" font-size="10">r</tspan>'), 640, 230)

def fig_driehoek():
    ox, oy, sc = 300, 200, 400
    s = f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy-0.40*sc}" stroke="#CBD5E1" stroke-dasharray="4 4"/><line x1="{ox}" y1="{oy}" x2="{ox+0.30*sc}" y2="{oy}" stroke="#CBD5E1" stroke-dasharray="4 4"/>'
    a, b = 0.1686 * 300, 0.2997 * 300  # schaal 1 N ≙ 300 px
    s += pijl(ox, oy, ox, oy + a, BL) + tx(ox + 10, oy + a - 4, 'F₁₃', 13, BL, 'start')
    s += pijl(ox, oy, ox - b, oy, '#0F766E') + tx(ox - b / 2, oy - 10, 'F₂₃', 13, '#0F766E')
    s += f'<line x1="{ox-b}" y1="{oy}" x2="{ox-b}" y2="{oy+a}" stroke="#94A3B8" stroke-dasharray="5 4"/><line x1="{ox}" y1="{oy+a}" x2="{ox-b}" y2="{oy+a}" stroke="#94A3B8" stroke-dasharray="5 4"/>'
    s += pijl(ox, oy, ox - b, oy + a, POS, 5) + tx(ox - b - 8, oy + a + 18, 'F_r', 14, POS, 'start')
    s += q(ox, oy - 0.40 * sc, 1, 11) + tx(ox + 18, oy - 0.40 * sc + 5, 'Q₁ = +3,0 μC', 13, INK, 'start')
    s += q(ox + 0.30 * sc, oy, 1, 11) + tx(ox + 0.30 * sc + 16, oy + 5, 'Q₂ = +3,0 μC', 13, INK, 'start')
    s += q(ox, oy, 1, 11) + tx(ox + 14, oy + 26, 'Q₃ = +1,0 μC', 13, INK, 'start')
    s += tx(ox - 20, oy - 70, '40 cm', 12, DIM, 'end', 400) + tx(ox + 60, oy - 8, '30 cm', 12, DIM, 'middle', 400)
    return svg(s.replace('F_r', 'F<tspan baseline-shift="sub" font-size="10">r</tspan>'), 640, 290)

lesdoelen = '''<p>De lesdoelen volgen het leerstofoverzicht. Na dit hoofdstuk kan je:</p>
<ul class="doelen">
<li>de richting, de zin en de grootte bepalen van de coulombkracht die twee ladingen op elkaar uitoefenen, en de formule van de coulombkracht omvormen om andere grootheden te berekenen;</li>
<li>redeneervragen over de coulombkracht tussen twee ladingen oplossen;</li>
<li>de richting, de zin en de grootte bepalen van de coulombkracht die meerdere ladingen op één lijn op elkaar uitoefenen, en de formule omvormen;</li>
<li>in een geometrie van drie ladingen die niet op één lijn liggen, de resulterende coulombkracht op één welbepaalde lading tekenen (eenvoudige opgaven).</li></ul>
<p>Leerboek p. 27–32. Oefeningen in het leerboek: 1 tot en met 11 (p. 31–32).</p>'''

voorkennis = '''<ul class="doelen">
<li>Gelijke ladingen stoten elkaar af, tegengestelde ladingen trekken elkaar aan (hoofdstuk 1).</li>
<li>Een kracht is een vector: aangrijpingspunt, richting, zin en grootte. De kracht begint op het voorwerp waarop ze werkt.</li>
<li>Krachten samenstellen: kop-staartmethode, parallellogrammethode en de stelling van Pythagoras.</li>
<li>Voorvoegsels: μ (micro) = 10⁻⁶, n (nano) = 10⁻⁹, m (milli) = 10⁻³. Afstanden in m.</li></ul>'''

d21 = f'''<h3>2.1.1 De wet van Coulomb</h3>
<p>Twee geladen voorwerpen oefenen een kracht op elkaar uit: de <b>coulombkracht</b> of elektrische kracht. Als de voorwerpen klein zijn tegenover hun afstand, noemen we ze <b>puntladingen</b>.</p>
{figuur(fig_zin(), 'Richting en zin van de coulombkracht. Elke kracht begint op de lading waarop ze werkt.')}
{defi('Richting en zin van de coulombkracht', '<p>De coulombkracht ligt op de <b>verbindingslijn</b> van de twee ladingen. Gelijke ladingen <b>stoten af</b>, tegengestelde ladingen <b>trekken aan</b>. De kracht van Q₁ op Q₂ en die van Q₂ op Q₁ zijn <b>even groot</b> en <b>tegengesteld</b> (actie en reactie).</p>')}
{defi('Wet van Coulomb', '<p>De grootte van de coulombkracht is recht evenredig met het product van de ladingen en omgekeerd evenredig met het kwadraat van de afstand.</p>', True)}
{vgl('<i>F</i> = <i>k</i> · |<i>Q</i>₁| · |<i>Q</i>₂| / <i>r</i>²')}
<table class="vb"><tr><td><i>F</i></td><td>grootte van de coulombkracht, in N</td></tr><tr><td><i>Q</i>₁, <i>Q</i>₂</td><td>de ladingen, in C (zonder teken: het teken bepaalt alleen de zin)</td></tr>
<tr><td><i>r</i></td><td>afstand tussen de middelpunten van de ladingen, in m</td></tr><tr><td><i>k</i></td><td>constante van Coulomb, 8,99 · 10⁹ N·m²/C²</td></tr></table>
{vb('Twee ladingen', '<p>Een lading van +2,0 μC en een lading van −3,0 μC liggen 30 cm uit elkaar. Bepaal de coulombkracht.</p><p>Gegeven: |<i>Q</i>₁| = 2,0 · 10⁻⁶ C, |<i>Q</i>₂| = 3,0 · 10⁻⁶ C, <i>r</i> = 0,30 m. Gevraagd: <i>F</i>.<br>Oplossing: <i>F</i> = 8,99 · 10⁹ · 2,0 · 10⁻⁶ · 3,0 · 10⁻⁶ / 0,30² = 0,60 N.<br>Antwoord: elke lading ondervindt een kracht van 0,60 N. De ladingen zijn tegengesteld: de krachten zijn <b>aantrekkend</b>.</p>')}
<h3>2.1.2 De formule omvormen</h3>
<p>Ken je de kracht, dan kan je een lading of de afstand berekenen:</p>
{vgl('|<i>Q</i>₁| = <i>F</i> · <i>r</i>² / (<i>k</i> · |<i>Q</i>₂|) &nbsp;&nbsp;&nbsp; <i>r</i> = √( <i>k</i> · |<i>Q</i>₁| · |<i>Q</i>₂| / <i>F</i> )')}
{vb('Twee gelijke ladingen', '<p>Twee gelijke ladingen op 5,0 cm van elkaar stoten elkaar af met een kracht van 0,90 N. Hoe groot is elke lading?</p><p>Omdat <i>Q</i>₁ = <i>Q</i>₂ = <i>Q</i>: <i>Q</i>² = <i>F</i> · <i>r</i>² / <i>k</i> = 0,90 · 0,050² / 8,99 · 10⁹ = 2,5 · 10⁻¹³ C².<br><i>Q</i> = 5,0 · 10⁻⁷ C = 0,50 μC. Beide ladingen hebben hetzelfde teken (afstoting), maar welk teken kan je niet weten.</p>')}
<h3>2.1.3 Redeneren met de wet van Coulomb</h3>
<p>Vaak hoef je niet te rekenen. Kijk hoe <i>F</i> afhangt van elke grootheid (figuur 2.2):</p>
<ul><li><i>Q</i>₁ of <i>Q</i>₂ wordt <b>×&nbsp;n</b> → <i>F</i> wordt <b>×&nbsp;n</b>;</li><li><i>r</i> wordt <b>×&nbsp;n</b> → <i>F</i> wordt <b>÷&nbsp;n²</b>.</li></ul>
{figuur(fig_grafiek(), 'De coulombkracht in functie van de afstand. Dubbele afstand: vier keer kleinere kracht.')}
{tool(TOOL, 'Tool: krachten op ladingen')}
{denk('denk_1', 'Je verdubbelt beide ladingen en ook de afstand ertussen. Wat gebeurt er met de coulombkracht?', [
  ('Ladingen', 'Elke lading × 2: het product |<i>Q</i>₁| · |<i>Q</i>₂| wordt × 4.'), ('Afstand', '<i>r</i> × 2: <i>r</i>² wordt × 4.'), ('Samen', '<i>F</i> wordt × 4 / 4 = × 1.')], 'De kracht blijft even groot.')}
{verd('Elektrische kracht tegenover zwaartekracht', '<p>In een waterstofatoom trekken het proton en het elektron elkaar aan met de coulombkracht en met de gravitatiekracht. De coulombkracht is ongeveer 2,3 · 10³⁹ keer groter. Daarom bepalen elektrische krachten hoe atomen en moleculen samenhangen.</p>')}'''

d22 = f'''<h3>2.2.1 Ladingen op één lijn</h3>
<p>Werken er meerdere ladingen op één lading, dan bepaal je elke coulombkracht <b>afzonderlijk</b>, alsof de andere ladingen er niet zijn. De resulterende kracht is de <b>vectoriële som</b> van die krachten.</p>
{defi('Superpositie', '<p>De resulterende coulombkracht op een lading is de vectoriële som van de coulombkrachten die alle andere ladingen afzonderlijk op die lading uitoefenen.</p>')}
{vgl('<b>F</b><sub>r</sub> = <b>F</b><sub>1</sub> + <b>F</b><sub>2</sub> + …')}
<p>Liggen alle ladingen op één lijn, dan liggen alle krachten op die lijn. Kies een positieve zin (bv. naar rechts) en tel de krachten op met hun teken.</p>
{figuur(fig_lijn(), 'Drie ladingen op één lijn. Onderaan: de twee krachten op Q₂ kop aan staart samengesteld.')}
{vb('Kracht op de middelste lading', '<p>Bepaal de resulterende kracht op <i>Q</i>₂ in figuur 2.3.</p><p><i>F</i>₁₂ = 8,99 · 10⁹ · 4,0 · 10⁻⁶ · 1,0 · 10⁻⁶ / 0,10² = 3,6 N, naar rechts (Q₁ en Q₂ stoten af).<br><i>F</i>₃₂ = 8,99 · 10⁹ · 2,0 · 10⁻⁶ · 1,0 · 10⁻⁶ / 0,20² = 0,45 N, naar rechts (Q₃ trekt Q₂ aan).<br><i>F</i><sub>r</sub> = 3,6 N + 0,45 N = 4,0 N, naar rechts.</p>')}
<h3>2.2.2 Ladingen die niet op één lijn liggen</h3>
<p>Liggen de ladingen niet op één lijn, dan teken je elke kracht vanuit de lading waarop ze werkt en stel je ze samen met de <b>parallellogrammethode</b>. Staan de twee krachten loodrecht op elkaar, dan bereken je de grootte met de stelling van Pythagoras.</p>
{figuur(fig_driehoek(), 'Drie ladingen in een rechthoekige driehoek. De resulterende kracht op Q₃ is de diagonaal van het parallellogram.')}
{vb('Drie ladingen in een driehoek', '<p>Bepaal de resulterende kracht op <i>Q</i>₃ in figuur 2.4.</p><p><i>F</i>₁₃ = 8,99 · 10⁹ · 3,0 · 10⁻⁶ · 1,0 · 10⁻⁶ / 0,40² = 0,17 N, naar beneden (afstoting, weg van Q₁).<br><i>F</i>₂₃ = 8,99 · 10⁹ · 3,0 · 10⁻⁶ · 1,0 · 10⁻⁶ / 0,30² = 0,30 N, naar links (afstoting, weg van Q₂).<br>De krachten staan loodrecht: <i>F</i><sub>r</sub> = √(0,17² + 0,30²) = 0,34 N, schuin naar linksonder.</p>')}
{tool(TOOL, 'Tool: oefen met meerdere ladingen')}
{denk('denk_2', 'In figuur 2.3 vervang je Q₃ door een positieve lading van +2,0 μC. Wordt de resulterende kracht op Q₂ groter of kleiner? Verandert de zin?', [
  ('F₁₂', 'Verandert niet: 3,6 N naar rechts.'), ('F₃₂', 'Q₃ stoot Q₂ nu af: 0,45 N naar links.'), ('Samen', '3,6 N − 0,45 N = 3,1 N, nog altijd naar rechts.')], 'De resulterende kracht wordt kleiner (3,1 N), de zin blijft naar rechts.')}'''

oefs = f'''<p>Maak deze oefeningen op papier. Gebruik: gegeven, gevraagd, formule, oplossing, antwoord met eenheid. Teken bij elke opgave eerst de krachten, vertrekkend op de lading waarop ze werken. Maak ook de oefeningen 1 tot en met 11 in het leerboek (p. 31–32).</p>
<p><button class="knop licht" data-print="oef">Oefeningen afdrukken</button></p>
{oef('opl_1', 1, 'Basis', 'Twee ladingen van +5,0 nC en +8,0 nC liggen 4,0 cm uit elkaar. Bereken de coulombkracht. Is ze aantrekkend of afstotend?', [
  ('Oplossing', '<i>F</i> = 8,99 · 10⁹ · 5,0 · 10⁻⁹ · 8,0 · 10⁻⁹ / 0,040² = 2,2 · 10⁻⁴ N'), ('Zin', 'Gelijke ladingen: afstotend.')], '<i>F</i> = 2,2 · 10⁻⁴ N, afstotend')}
{oef('opl_2', 2, 'Afstand berekenen', 'Een elektron en een proton trekken elkaar aan met een kracht van 8,2 · 10⁻⁸ N. Hoe ver liggen ze uit elkaar?', [
  ('Formule', '<i>r</i> = √(<i>k</i> · <i>e</i> · <i>e</i> / <i>F</i>)'), ('Oplossing', '<i>r</i> = √(8,99 · 10⁹ · (1,602 · 10⁻¹⁹)² / 8,2 · 10⁻⁸) = 5,3 · 10⁻¹¹ m')], '<i>r</i> = 5,3 · 10⁻¹¹ m (de straal van een waterstofatoom)')}
{oef('opl_3', 3, 'Redeneren', 'Wat gebeurt er met de coulombkracht?<ol class="deelvragen" type="a"><li>De afstand wordt 3 keer zo groot.</li><li>Eén lading wordt 4 keer zo groot en de afstand 2 keer zo groot.</li><li>De afstand wordt gehalveerd.</li><li>Je maakt één lading 2 keer zo groot en de andere 2 keer zo klein.</li></ol>', [
  ('a', '÷ 9'), ('b', '× 4 / 4 = × 1: blijft gelijk'), ('c', '× 4'), ('d', '× 2 / 2 = × 1: blijft gelijk')], 'Factor van de ladingen boven, factor van de afstand in het kwadraat onder.')}
{oef('opl_4', 4, 'Tegenstrijdig?', 'Een lading van 1,0 μC ligt naast een lading van 4,0 μC. Lisa zegt: "De grote lading duwt harder op de kleine dan omgekeerd." Klopt dat?', [
  ('Wet van Coulomb', 'In <i>F</i> = <i>k</i>|<i>Q</i>₁||<i>Q</i>₂|/<i>r</i>² zit het product van beide ladingen: voor beide ladingen dezelfde waarde.'), ('Actie-reactie', 'De krachten zijn even groot en tegengesteld.')], 'Lisa heeft geen gelijk: beide krachten zijn even groot.')}
{oef('opl_5', 5, 'Op één lijn', 'Q₁ = +2,0 μC ligt in x = 0, Q₂ = −1,0 μC in x = 20 cm en Q₃ = +4,0 μC in x = 40 cm. Bereken de resulterende kracht op Q₂.', [
  ('F₁₂', '8,99 · 10⁹ · 2,0 · 10⁻⁶ · 1,0 · 10⁻⁶ / 0,20² = 0,45 N naar links (aantrekking naar Q₁)'), ('F₃₂', '8,99 · 10⁹ · 4,0 · 10⁻⁶ · 1,0 · 10⁻⁶ / 0,20² = 0,90 N naar rechts (aantrekking naar Q₃)'), ('Samen', '0,90 N − 0,45 N = 0,45 N')], '<i>F</i><sub>r</sub> = 0,45 N naar rechts')}
{oef('opl_6', 6, 'Waar is de kracht nul?', 'Q₁ = +1,0 μC ligt in x = 0, Q₂ = +4,0 μC in x = 30 cm. Waar tussen beide moet je een kleine positieve lading leggen opdat de resulterende kracht erop nul is?', [
  ('Voorwaarde', '<i>k</i> · 1,0 · q / x² = <i>k</i> · 4,0 · q / (0,30 − x)²'), ('Oplossing', '(0,30 − x)² = 4x² → 0,30 − x = 2x → x = 0,10 m')], 'Op 10 cm van Q₁ (dichter bij de kleinste lading).')}
{oef('opl_7', 7, 'Niet op één lijn', 'Drie ladingen liggen op de hoekpunten van een vierkant met zijde 10 cm: Q₁ = +2,0 μC linksboven, Q₂ = +2,0 μC rechtsonder, Q₃ = −1,0 μC linksonder. Teken de krachten op Q₃ en bereken de resulterende kracht.', [
  ('F₁₃', '8,99 · 10⁹ · 2,0 · 10⁻⁶ · 1,0 · 10⁻⁶ / 0,10² = 1,8 N, naar boven (aantrekking naar Q₁)'), ('F₂₃', '1,8 N, naar rechts (aantrekking naar Q₂)'), ('Samen', '<i>F</i><sub>r</sub> = √(1,8² + 1,8²) = 2,5 N')], '<i>F</i><sub>r</sub> = 2,5 N, schuin naar rechtsboven (45°), naar het midden van het vierkant')}
{oef('opl_8', 8, 'Twee ballonnen', 'Je wrijft twee ballonnen over je trui. Elke ballon krijgt een lading van −0,10 μC. Je hangt ze aan een touwtje. Hun middelpunten liggen 30 cm uit elkaar.<ol class="deelvragen" type="a"><li>Bereken de coulombkracht tussen de ballonnen. Trekken ze elkaar aan of stoten ze af?</li><li>Een ballon heeft een massa van 3,0 g. Vergelijk de coulombkracht met zijn gewicht.</li><li>Mag je de ballonnen hier als puntladingen beschouwen? Verklaar.</li></ol>', [
  ('a', '<i>F</i> = 8,99 · 10⁹ · (0,10 · 10⁻⁶)² / 0,30² = 1,0 · 10⁻³ N; gelijke ladingen: ze stoten af.'), ('b', '<i>F</i><sub>z</sub> = 0,0030 · 9,81 = 2,9 · 10⁻² N: ongeveer 30 keer groter dan de coulombkracht. Daarom hangen de touwtjes maar een beetje scheef.'), ('c', 'Niet goed: een ballon is ongeveer 25 cm groot, bijna even groot als de afstand. De lading zit verspreid over het oppervlak. De berekening is maar een ruwe schatting.')], 'Hoe groter de afstand tegenover de afmetingen, hoe beter de benadering met puntladingen.')}'''

begrippen = '''<div class="begrippen">
<p><b>coulombkracht</b> — kracht tussen twee geladen voorwerpen</p>
<p><b>constante van Coulomb</b> — <i>k</i> = 8,99 · 10⁹ N·m²/C²</p>
<p><b>puntlading</b> — geladen voorwerp dat klein is tegenover de afstanden in de opgave</p>
<p><b>superpositie</b> — de resulterende kracht is de vectoriële som van de afzonderlijke krachten</p>
<p><b>verbindingslijn</b> — rechte door de middelpunten van de twee ladingen: de richting van de coulombkracht</p>
</div>'''

cornell = '''<p>Op het bord bouwen we samen een Cornellschema op. Dek thuis de rechterkolom af en overhoor jezelf.</p>
<p><button class="knop licht" data-print="cornell">Cornellblad afdrukken</button></p>'''

samenv = kader('Samenvatting', '''<p><b>Wet van Coulomb</b>: <i>F</i> = <i>k</i> · |<i>Q</i>₁| · |<i>Q</i>₂| / <i>r</i>², met <i>k</i> = 8,99 · 10⁹ N·m²/C². Richting: de verbindingslijn. Zin: gelijke ladingen stoten af, tegengestelde trekken aan. Beide krachten zijn even groot en tegengesteld.</p>
<p><b>Redeneren</b>: lading × n → <i>F</i> × n; afstand × n → <i>F</i> ÷ n².</p>
<p><b>Meerdere ladingen</b>: bepaal elke kracht afzonderlijk en tel ze vectorieel op. Op één lijn: optellen met teken. Loodrecht: Pythagoras. Algemeen: parallellogrammethode.</p>''')

delen = [('deel21', '2.1', 'Krachten tussen twee ladingen', d21), ('deel22', '2.2', 'Krachten tussen meerdere ladingen', d22)]
blokken = [blok('lesdoelen', '', 'Lesdoelen', lesdoelen), blok('voorkennis', '', 'Voorkennis', voorkennis)] + \
          [blok(i, n, t, c, i) for i, n, t, c in delen] + \
          [blok('oefeningen', '', 'Oefeningen', oefs, 'oefeningen'), blok('begrippen', '', 'Begrippenlijst', begrippen), blok('samenvatting', '', 'Samenvatting', samenv, 'samenvatting')]
vrij = [('deel21', True, '2.1 Krachten tussen twee ladingen'), ('deel22', False, '2.2 Krachten tussen meerdere ladingen'),
        ('denk_1', False, 'redenering denkvraag 1'), ('denk_2', False, 'redenering denkvraag 2'),
        ('oefeningen', False, 'de oefeningen zelf (opgaven)')] + [(f'opl_{i}', False, f'oplossing oefening {i}') for i in range(1, 9)] + [('samenvatting', False, 'samenvatting')]
cvr = [['Wat zegt de wet van Coulomb? Formule en eenheden?', 30], ['Richting en zin van de coulombkracht?', 24], ['Hoe vorm je de formule om naar Q of r?', 24],
       ['Wat gebeurt er met F als Q of r verandert?', 26], ['Hoe bepaal je de kracht van meerdere ladingen op één lijn?', 30], ['En als ze niet op één lijn liggen?', 30]]
bouw('cursus-coulomb.html', 'Fysica 5de jaar · Thema 1 Elektrostatica · Hoofdstuk 2', 'Krachten tussen ladingen',
     'Deze cursus hoort bij de tool <a href="krachten-op-ladingen.html">Krachten op ladingen</a>. Oefeningen maak je op papier.',
     blokken, vrij, cvr)
print('ok')
