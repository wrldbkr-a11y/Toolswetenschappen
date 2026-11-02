# Cursus fysica 5de jaar · Thema 2 Elektrodynamica · Hoofdstuk 3 Gemengde schakelingen
_src = open('/home/claude/cursus/optica_cursus.py', encoding='utf-8').read()
exec(_src.split('# ================================================================ H1')[0])
TOOL = 'schakelingen.html'
EY = 'Fysica 5de jaar · Thema 2 Elektrodynamica · Hoofdstuk 3'

def ttabel(kop, rijen):
    h = '<table class="vb grid"><tr>' + ''.join(f'<td><b>{k}</b></td>' for k in kop) + '</tr>'
    return h + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rijen) + '</table>'

# ---------------- schakelschema's ----------------
# element: ('R', 'R1', '4 Ω') | ('S', [..]) | ('P', [..])
RW, RH, GAP = 54, 22, 18
def maat(e):
    if e[0] == 'R': return RW + 2 * GAP, 74
    ms = [maat(x) for x in e[1]]
    if e[0] == 'S': return sum(m[0] for m in ms), max(m[1] for m in ms)
    return max(m[0] for m in ms) + 2 * GAP, sum(m[1] for m in ms)
def teken(e, x, y):
    """teken element e met linkeraansluiting (x, y); geeft svg terug"""
    w, h = maat(e); o = ''
    if e[0] == 'R':
        o += lijn(x, y, x + GAP, y, INK, 2) + lijn(x + GAP + RW, y, x + w, y, INK, 2)
        o += f'<rect x="{x+GAP}" y="{y-RH/2}" width="{RW}" height="{RH}" fill="#fff" stroke="{INK}" stroke-width="2.2"/>'
        o += t(x + GAP + RW / 2, y - RH / 2 - 6, e[1], INK, size=13)
        if len(e) > 2 and e[2]: o += t(x + GAP + RW / 2, y + RH / 2 + 15, e[2], GRIJS, size=12, w=600)
        return o
    if e[0] == 'S':
        for x_ in e[1]:
            o += teken(x_, x, y); x += maat(x_)[0]
        return o
    # parallel: takken onder elkaar, gecentreerd rond y
    ms = [maat(t_) for t_ in e[1]]; tot = sum(m[1] for m in ms)
    yy = y - tot / 2
    ys = []
    for t_, m in zip(e[1], ms):
        yc = yy + m[1] / 2; ys.append(yc)
        o += lijn(x + GAP, yc, x + GAP + (w - 2 * GAP - m[0]) / 2, yc, INK, 2)
        o += teken(t_, x + GAP + (w - 2 * GAP - m[0]) / 2, yc)
        o += lijn(x + GAP + (w - 2 * GAP - m[0]) / 2 + m[0], yc, x + w - GAP, yc, INK, 2)
        yy += m[1]
    o += lijn(x, y, x + GAP, y, INK, 2) + lijn(x + w - GAP, y, x + w, y, INK, 2)
    o += lijn(x + GAP, ys[0], x + GAP, ys[-1], INK, 2) + lijn(x + w - GAP, ys[0], x + w - GAP, ys[-1], INK, 2)
    o += punt(x + GAP, y, INK, 3.5) + punt(x + w - GAP, y, INK, 3.5)
    return o
def schema(e, U='', breed=None):
    w, h = maat(e)
    x0, y0 = 50, 20 + h / 2
    yb = y0 + h / 2 + 45
    o = teken(e, x0, y0)
    o += lijn(x0, y0, x0 - 20, y0, INK, 2) + lijn(x0 - 20, y0, x0 - 20, yb, INK, 2)
    o += lijn(x0 + w, y0, x0 + w + 20, y0, INK, 2) + lijn(x0 + w + 20, y0, x0 + w + 20, yb, INK, 2)
    xm = x0 + w / 2
    o += lijn(x0 - 20, yb, xm - 8, yb, INK, 2) + lijn(xm + 8, yb, x0 + w + 20, yb, INK, 2)
    o += lijn(xm - 8, yb - 16, xm - 8, yb + 16, INK, 3) + lijn(xm + 8, yb - 9, xm + 8, yb + 9, INK, 5)
    o += t(xm - 20, yb - 20, '+', ROOD, size=15) + t(xm + 22, yb - 14, '−', BLAUW, size=15)
    if U: o += t(xm, yb + 34, f'U = {U}', INK, size=14)
    W, Hh = int(w + 120), int(yb + 48)
    return svg(o, W, Hh).replace(f'width="{W}"', f'width="{breed or min(640, W*1.15):.0f}"', 1)

def R(n, w=''): return ('R', n, w)
def S(*a): return ('S', list(a))
def P(*a): return ('P', list(a))

f_serie = schema(S(R('R1', '4 Ω'), R('R2', '6 Ω')), '12 V')
f_par = schema(P(R('R1', '4 Ω'), R('R2', '6 Ω')), '12 V')
f_gem = schema(S(R('R1', '4 Ω'), P(R('R2', '6 Ω'), R('R3', '12 Ω'))), '12 V')

doelen = ['de <b>wet van Ohm</b> kennen en gebruiken in oefeningen over gemengde schakelingen;',
          'de formules van de <b>substitutieweerstand</b> gebruiken om de substitutieweerstand van een gemengde schakeling te bepalen;',
          'de formules van de <b>stroom- en spanningsverdeling</b> bij serie- en parallelschakelingen gebruiken om U, I en R te bepalen van weerstanden in een gemengde schakeling.']
voork = vk('<b>Spanning</b> U in volt (V), <b>stroomsterkte</b> I in ampère (A), <b>weerstand</b> R in ohm (Ω).', 'Een <b>ampèremeter</b> staat in serie, een <b>voltmeter</b> staat parallel over het onderdeel.', 'Formules omvormen: als a = b · c, dan b = a / c.')

d1 = f'''{kader('Wet van Ohm', '<p>Bij een ohmse weerstand (bij constante temperatuur) is de stroomsterkte recht evenredig met de spanning:</p><p style="text-align:center;font-size:1.2em"><b>U = R · I</b></p><p>Omvormen: <b>I = U / R</b> en <b>R = U / I</b>.</p>')}
<p>Voorbeeld: over een weerstand van 100 Ω staat 6 V. Dan is I = 6 V / 100 Ω = 0,06 A = 60 mA. Verdubbel je de spanning, dan verdubbelt de stroom.</p>
<p>In een U(I)-grafiek is een ohmse weerstand een rechte door de oorsprong. Hoe steiler de rechte, hoe groter R.</p>
{tool(TOOL + '#ohm', 'Experimenteer met de wet van Ohm')}
{denk('denk_1', 'Een lamp van een fietslicht werkt op 6 V en er loopt 0,30 A door. Hoe groot is haar weerstand? Wat gebeurt er met de stroom als de batterij nog maar 3 V geeft (R blijft gelijk)?', [
  ('Weerstand', 'R = U / I = 6 V / 0,30 A = 20 Ω'), ('Halve spanning', 'I = 3 V / 20 Ω = 0,15 A: de stroom halveert.')], 'R = 20 Ω; bij de halve spanning loopt de halve stroom.')}'''

d2 = f'''{figuur(f_serie, 'Serieschakeling: de weerstanden staan na elkaar.')}
{figuur(f_par, 'Parallelschakeling: de weerstanden staan naast elkaar, in aparte takken.')}
{ttabel(['', 'Serie', 'Parallel'], [
  ['stroomsterkte', 'overal <b>dezelfde</b>: I = I₁ = I₂', 'verdeelt zich: <b>I = I₁ + I₂</b>'],
  ['spanning', 'verdeelt zich: <b>U = U₁ + U₂</b>', 'over elke tak <b>dezelfde</b>: U = U₁ = U₂'],
  ['substitutieweerstand', '<b>R<sub>s</sub> = R₁ + R₂ + …</b>', '<b>1/R<sub>s</sub> = 1/R₁ + 1/R₂ + …</b><br>bij twee: R<sub>s</sub> = R₁ · R₂ / (R₁ + R₂)'],
  ['let op', 'R<sub>s</sub> is groter dan de grootste weerstand', 'R<sub>s</sub> is kleiner dan de kleinste weerstand'],
  ['verdeling', 'grootste weerstand → grootste deelspanning', 'kleinste weerstand → grootste deelstroom']])}
{kader('Definitie', '<p>De <b>substitutieweerstand</b> R<sub>s</sub> is de ene weerstand die je in de plaats van een groep weerstanden kan zetten, zonder dat de stroom uit de bron verandert.</p>')}
<p><b>Voorbeeld serie</b> (12 V, 4 Ω en 6 Ω): R<sub>s</sub> = 10 Ω, I = 12 / 10 = 1,2 A, U₁ = 4 · 1,2 = 4,8 V, U₂ = 6 · 1,2 = 7,2 V. Controle: 4,8 + 7,2 = 12 V.</p>
<p><b>Voorbeeld parallel</b> (12 V, 4 Ω en 6 Ω): R<sub>s</sub> = 4 · 6 / 10 = 2,4 Ω, I = 12 / 2,4 = 5 A, I₁ = 12 / 4 = 3 A, I₂ = 12 / 6 = 2 A. Controle: 3 + 2 = 5 A.</p>
{tool(TOOL + '#basis', 'Vergelijk serie en parallel in de tool')}
{denk('denk_2', 'Waarom is de substitutieweerstand van twee parallelle weerstanden kleiner dan de kleinste weerstand?', [
  ('Meer wegen', 'Elke extra tak is een extra weg voor de stroom.'), ('Gevolg', 'Bij dezelfde spanning loopt er in totaal meer stroom: dat betekent een kleinere weerstand (R = U / I).')], 'Meer takken → meer stroom → kleinere substitutieweerstand.')}'''

d3 = f'''<p>In een <b>gemengde schakeling</b> staan sommige weerstanden in serie en andere parallel. Je lost ze op in <b>twee richtingen</b>.</p>
{kader('Stappenplan', '<ol><li><b>Van binnen naar buiten</b>: zoek een deel dat zuiver serie of zuiver parallel is. Vervang het door één substitutieweerstand. Herhaal tot je één R<sub>s</sub> hebt.</li><li>Bereken de <b>totale stroom</b>: I = U / R<sub>s</sub>.</li><li><b>Van buiten naar binnen</b>: verdeel spanning en stroom terug over de delen, met de regels van serie en parallel en de wet van Ohm.</li><li><b>Controleer</b>: tellen de deelspanningen en de deelstromen juist op?</li></ol>')}
{figuur(f_gem, 'Een gemengde schakeling: R₁ in serie met (R₂ parallel R₃).')}
{ttabel(['Stap', 'Berekening'], [
  ['1. binnenste deel', 'R₂ // R₃: R<sub>23</sub> = 6 · 12 / (6 + 12) = 4 Ω'],
  ['2. hele schakeling', 'R<sub>s</sub> = R₁ + R<sub>23</sub> = 4 + 4 = 8 Ω'],
  ['3. totale stroom', 'I = U / R<sub>s</sub> = 12 V / 8 Ω = 1,5 A (die gaat door R₁)'],
  ['4. spanningen', 'U₁ = R₁ · I = 4 · 1,5 = 6 V; U<sub>23</sub> = 12 − 6 = 6 V'],
  ['5. stromen in de takken', 'I₂ = 6 V / 6 Ω = 1,0 A; I₃ = 6 V / 12 Ω = 0,5 A'],
  ['6. controle', 'I₂ + I₃ = 1,5 A = I ✓ · U₁ + U<sub>23</sub> = 12 V ✓']])}
{tool(TOOL + '#gemengd', 'Los gemengde schakelingen stap voor stap op in de tool')}
{denk('denk_3', 'In de schakeling hierboven brandt R₃ door (de tak is onderbroken). Wordt de stroom door R₁ groter of kleiner? Redeneer zonder te rekenen, en controleer daarna.', [
  ('Redeneren', 'Er is één tak minder: het paralleldeel wordt alleen R₂ = 6 Ω, groter dan 4 Ω. R<sub>s</sub> wordt groter, dus de totale stroom kleiner.'),
  ('Controle', 'R<sub>s</sub> = 4 + 6 = 10 Ω; I = 12 / 10 = 1,2 A, kleiner dan 1,5 A.')], 'De stroom door R₁ wordt kleiner.')}'''

oefs = f'''{oef('opl_1', 1, 'Wet van Ohm', '<ol class="deelvragen" type="a"><li>Over een weerstand van 220 Ω staat 9,0 V. Bereken I.</li><li>Door een weerstand loopt 25 mA bij 5,0 V. Bereken R.</li><li>Door een weerstand van 47 Ω loopt 0,20 A. Bereken U.</li></ol>', [
  ('a', 'I = U / R = 9,0 / 220 = 0,041 A = 41 mA'), ('b', 'R = U / I = 5,0 / 0,025 = 200 Ω'), ('c', 'U = R · I = 47 · 0,20 = 9,4 V')], 'U = R · I, en omgevormd.')}
{oef('opl_2', 2, 'Serie', 'Drie weerstanden van 2,0 Ω, 3,0 Ω en 5,0 Ω staan in serie op 20 V. Bereken R<sub>s</sub>, I en de spanning over elke weerstand.', [
  ('R<sub>s</sub>', '2,0 + 3,0 + 5,0 = 10 Ω'), ('I', '20 / 10 = 2,0 A, overal'), ('U', 'U₁ = 4,0 V · U₂ = 6,0 V · U₃ = 10 V (samen 20 V)')], 'In serie: zelfde stroom, de spanning verdeelt zich.')}
{oef('opl_3', 3, 'Parallel', 'Twee weerstanden van 6,0 Ω en 3,0 Ω staan parallel op 12 V. Bereken R<sub>s</sub>, de totale stroom en de stroom in elke tak.', [
  ('R<sub>s</sub>', '6 · 3 / (6 + 3) = 2,0 Ω'), ('I', '12 / 2,0 = 6,0 A'), ('Takken', 'I₁ = 12 / 6 = 2,0 A · I₂ = 12 / 3 = 4,0 A (samen 6,0 A)')], 'Parallel: zelfde spanning, de stroom verdeelt zich.')}
{oef_fig('opl_4', 4, 'Gemengd: (R₁ + R₂) // R₃', 'U = 12 V, R₁ = 2,0 Ω, R₂ = 4,0 Ω, R₃ = 6,0 Ω. Bereken R<sub>s</sub>, I, de stroom in elke tak en U₁ en U₂.', schema(P(S(R('R1'), R('R2')), R('R3')), '12 V'), [
  ('R<sub>12</sub>', '2 + 4 = 6,0 Ω'), ('R<sub>s</sub>', '6 · 6 / (6 + 6) = 3,0 Ω'), ('I', '12 / 3 = 4,0 A'), ('Takken', 'I<sub>12</sub> = 12 / 6 = 2,0 A · I₃ = 12 / 6 = 2,0 A'), ('Spanningen', 'U₁ = 2 · 2 = 4,0 V · U₂ = 4 · 2 = 8,0 V')],
  'Eerst de serie in de tak, dan parallel.', schema(P(S(R('R1', '2 Ω'), R('R2', '4 Ω')), R('R3', '6 Ω')), '12 V'))}
{oef_fig('opl_5', 5, 'Gemengd: R₁ + (R₂ // (R₃ + R₄))', 'U = 20 V, R₁ = 5,0 Ω, R₂ = 10 Ω, R₃ = 4,0 Ω, R₄ = 6,0 Ω. Bereken R<sub>s</sub>, I, U₁ en de stroom en spanning bij R₂, R₃ en R₄.', schema(S(R('R1'), P(R('R2'), S(R('R3'), R('R4')))), '20 V'), [
  ('R<sub>34</sub>', '4 + 6 = 10 Ω'), ('Paralleldeel', '10 // 10 = 5,0 Ω'), ('R<sub>s</sub>', '5 + 5 = 10 Ω'), ('I', '20 / 10 = 2,0 A'),
  ('U₁', '5 · 2 = 10 V, dus over het paralleldeel 10 V'), ('Takken', 'I₂ = 10 / 10 = 1,0 A · I<sub>34</sub> = 1,0 A · U₃ = 4,0 V · U₄ = 6,0 V')],
  'Van binnen naar buiten, dan van buiten naar binnen.', schema(S(R('R1', '5 Ω'), P(R('R2', '10 Ω'), S(R('R3', '4 Ω'), R('R4', '6 Ω')))), '20 V'))}
{oef_fig('opl_6', 6, 'Gemengd: (R₁ // R₂) + (R₃ // R₄)', 'U = 18 V, R₁ = R₂ = 6,0 Ω, R₃ = 12 Ω, R₄ = 4,0 Ω. Bereken R<sub>s</sub>, I en de stroom door elke weerstand.', schema(S(P(R('R1'), R('R2')), P(R('R3'), R('R4'))), '18 V'), [
  ('R<sub>12</sub>', '6 // 6 = 3,0 Ω'), ('R<sub>34</sub>', '12 · 4 / 16 = 3,0 Ω'), ('R<sub>s</sub>', '3 + 3 = 6,0 Ω'), ('I', '18 / 6 = 3,0 A'),
  ('Spanningen', 'U<sub>12</sub> = 3 · 3 = 9,0 V · U<sub>34</sub> = 9,0 V'), ('Stromen', 'I₁ = I₂ = 1,5 A · I₃ = 9 / 12 = 0,75 A · I₄ = 9 / 4 = 2,25 A')],
  'Controleer: I₁ + I₂ = I₃ + I₄ = 3,0 A.', schema(S(P(R('R1', '6 Ω'), R('R2', '6 Ω')), P(R('R3', '12 Ω'), R('R4', '4 Ω'))), '18 V'))}
{oef('opl_7', 7, 'Redeneren: een lamp erbij', 'Op een batterij staat één lamp. Je plaatst er een tweede, identieke lamp bij.<ol class="deelvragen" type="a"><li>in serie: wat gebeurt er met R<sub>s</sub>, met de stroom uit de batterij en met de helderheid?</li><li>parallel: idem.</li></ol>', [
  ('a', 'R<sub>s</sub> verdubbelt, de stroom halveert; elke lamp krijgt de halve spanning en brandt zwakker.'), ('b', 'R<sub>s</sub> halveert, de stroom uit de batterij verdubbelt; elke lamp krijgt de volle spanning en brandt even fel.')],
  'Daarom staan toestellen in huis parallel.')}
{oef('opl_8', 8, 'Brussel · de kerstverlichting', 'Op de Grote Markt hangen lange snoeren lampjes. In een oud snoer staan alle lampjes in serie; in een nieuw snoer staan groepjes lampjes parallel. Eén lampje gaat kapot. Wat gebeurt er in elk snoer? Leg uit.', [
  ('Serie', 'De stroomkring is onderbroken: alle lampjes gaan uit.'), ('Parallel', 'Alleen de tak met het kapotte lampje valt uit; de andere takken krijgen nog altijd de volle spanning.')],
  'Een onderbreking in serie stopt alles; in parallel alleen die tak.')}'''

samenv = '''<p><b>Wet van Ohm</b>: U = R · I (I = U / R, R = U / I).</p>
<p><b>Serie</b>: I overal gelijk; U = U₁ + U₂; R<sub>s</sub> = R₁ + R₂. <b>Parallel</b>: U over elke tak gelijk; I = I₁ + I₂; 1/R<sub>s</sub> = 1/R₁ + 1/R₂.</p>
<p><b>Gemengd</b>: van binnen naar buiten vervangen door substitutieweerstanden → I = U / R<sub>s</sub> → van buiten naar binnen U en I verdelen → controleren.</p>'''

maak('cursus-schakelingen.html', EY, 'Gemengde schakelingen', 'Werk dit hoofdstuk samen met de tool <a href="schakelingen.html">Gemengde schakelingen</a>. Oefeningen maak je op papier.',
     doelen, voork, [('De wet van Ohm', d1), ('Serie en parallel', d2), ('Gemengde schakelingen stap voor stap', d3)], oefs, samenv, (TOOL + '#oefenen', 'Oefen met nieuwe opgaven in de tool'))
print('schakel ok')
