# Hoofdstuk 5 Veerkracht voor de cursus Krachten 3ASO, volgens de leerlijn
# start · uitleg + uitgewerkt voorbeeld · nu jij · controleer · tool.
# Wordt uitgevoerd in de naamruimte van aso_krachten.py (exec), dus alle helpers zijn beschikbaar.

def fase(naam):
    return ('<h3 style="display:flex;align-items:center;gap:8px"><span style="background:#e2e8f0;border-radius:999px;'
            'padding:2px 10px;font-size:.8rem;letter-spacing:.04em;text-transform:uppercase">%s</span></h3>' % naam)

GX, GY = 60, 260   # oorsprong van de grafiek

def grafiek(punten=None, lijnen=(), w=360, h=300):
    """F(Δl)-grafiek op ruitjes: x 1 hokje = 1 cm, y 1 hokje = 0,25 N"""
    o = rooster(w, h) + f'<line x1="{GX}" y1="{GY}" x2="{w-10}" y2="{GY}" stroke="{INK}" stroke-width="2"/><line x1="{GX}" y1="{GY}" x2="{GX}" y2="10" stroke="{INK}" stroke-width="2"/>'
    for k in range(0, 13, 2):
        o += t(GX + k * HK, GY + 18, str(k), INK, size=11, w=500)
        o += t(GX - 8, GY - k * HK + 4, f'{k*0.25:.1f}'.replace('.', ','), INK, 'end', 11, 500)
    o += t(w - 12, GY - 8, 'Δl (cm)', INK, 'end', 12) + t(GX + 6, 22, 'F (N)', INK, 'start', 12)
    for (x1, y1, x2, y2, kl, lab) in lijnen:
        o += lijn(GX + x1 * HK, GY - y1 / 0.25 * HK, GX + x2 * HK, GY - y2 / 0.25 * HK, kl, 3, None)
        if lab: o += t(GX + x2 * HK + 6, GY - y2 / 0.25 * HK + 4, lab, kl, 'start', 14)
    for (x, y) in (punten or []):
        o += f'<circle cx="{GX + x * HK}" cy="{GY - y / 0.25 * HK}" r="5" fill="{B}"/>'
    return svg(o, w, h)

def veer(n_z=0, n_v=0, w=600, h=340):
    """massa aan een veer; n_z en n_v = lengte van F_z en F_v in hokjes (0 = niet getekend)"""
    o = (rooster(w, h) + '<rect x="220" y="0" width="160" height="16" fill="#94a3b8"/>'
         '<path d="M300,16 v14 l-14,8 l28,12 l-28,12 l28,12 l-28,12 l28,12 l-28,12 l28,12 l-14,8 v10" fill="none" stroke="#94a3b8" stroke-width="3"/>'
         + doos(270, 140, 60, 50, '#cbd5e1', '#334155') + punt(300, 140, INK, 4) + punt(300, 165, INK, 4))
    if n_v: o += pijl(300, 140, 300, 140 - n_v * HK, G) + label(312, 140 - n_v * HK + 18, 'F', 'v', G)
    if n_z: o += pijl(300, 165, 300, 165 + n_z * HK, PAARS) + label(306, 165 + n_z * HK - 6, 'F', 'z', PAARS)
    return svg(o, w, h)

MEET = [(50, 2.0), (100, 4.0), (150, 6.0), (200, 8.0)]
TD = '<td style="min-width:56px;text-align:center">'
tab_meet = ('<table style="border-collapse:collapse;margin:8px 0 12px;font-size:15px" cellpadding="6" border="1" bordercolor="#cbd5e1">'
    '<tr><th>massa m (g)</th>' + ''.join(f'{TD}{m}</td>' for m, _ in MEET) + '</tr>'
    '<tr><th>F<sub>z</sub> = F<sub>v</sub> (N)</th>' + ''.join(f'{TD}</td>' for _ in MEET) + '</tr>'
    '<tr><th>uitrekking Δl (cm)</th>' + ''.join(f'{TD}' + f'{d:.1f}'.replace('.', ',') + '</td>' for _, d in MEET) + '</tr>'
    '<tr><th>F<sub>v</sub> / Δl (N/cm)</th>' + ''.join(f'{TD}</td>' for _ in MEET) + '</tr></table>')

KEN = kader('Ken dit · Veerkracht', '''<p><b>Veerkracht F<sub>v</sub>:</b> de kracht die een vervormd elastisch voorwerp uitoefent om zijn oorspronkelijke vorm terug aan te nemen.</p>
<p class="formule">F<sub>v</sub> = k · Δl</p>
<p>F<sub>v</sub> = veerkracht (N) · k = <b>veerconstante</b> (N/m) · Δl = lengteverandering (m). Omvormen: <b>k = F<sub>v</sub> / Δl</b> en <b>Δl = F<sub>v</sub> / k</b>.</p>
<p><b>Wat betekent k?</b> Bij k = 25 N/m heb je 25 N nodig om de veer 1 m uit te rekken. Een grote k: een <b>stijve</b> veer. Een kleine k: een <b>slappe</b> veer.</p>
<p>In woorden: hoe groter de lengteverandering, hoe groter de veerkracht (recht evenredig).</p>''')

VOORBEELD = ('<p><b>Uitgewerkt voorbeeld.</b> Amina hangt 300 g aan haar veer (k = 25 N/m). Teken de krachten op de massa (schaal: 1 hokje ≙ 0,5 N) en bereken de uitrekking.</p>'
    + figuur(veer(6, 6), 'De massa hangt stil: F<sub>v</sub> en F<sub>z</sub> zijn even groot en tegengesteld.')
    + '''<ol><li><b>Gegeven:</b> m = 300 g = 0,300 kg · k = 25 N/m · g ≈ 10 N/kg</li>
<li><b>Zwaartekracht:</b> F<sub>z</sub> = m · g = 0,300 kg · 10 N/kg = 3,0 N → 3,0 N : 0,5 N = <b>6 hokjes</b>, vanuit het midden naar beneden.</li>
<li><b>Veerkracht:</b> de massa hangt stil, dus F<sub>v</sub> = 3,0 N → <b>6 hokjes</b>, vanuit het ophangpunt naar boven.</li>
<li><b>Uitrekking:</b> Δl = F<sub>v</sub> / k = 3,0 N / 25 N/m = 0,12 m = <b>12 cm</b>.</li></ol>''')

TWEE = [(0, 0, 4, 2.5, R, 'A'), (0, 0, 10, 1.5, B, 'B')]

h5 = (fase('Start')
 + '<p>Hang je een massa aan een veer, dan rekt de veer uit. De veer trekt terug omhoog: dat is de <b>veerkracht F<sub>v</sub></b>. Hangt de massa stil, dan is F<sub>v</sub> even groot als F<sub>z</sub>.</p>'
 + '<p>Amina hangt telkens meer massa aan dezelfde veer en meet de uitrekking Δl (g ≈ 10 N/kg).</p>' + tab_meet
 + oef_fig('opl_v1', '5.1', 'Ontdek het verband', 'a) Vul de tabel aan: bereken F<sub>z</sub> = m · g (zet de massa eerst om naar kg) en daarna F<sub>v</sub> / Δl. b) Zet de punten in de grafiek en verbind ze. c) Wat valt je op?', grafiek(),
    [('a', 'F<sub>z</sub> = 0,5 N · 1,0 N · 1,5 N · 2,0 N. F<sub>v</sub> / Δl = 0,25 N/cm bij elke meting.'), ('b', 'de punten liggen op een rechte door de oorsprong'),
     ('c', 'dubbel zoveel kracht → dubbel zoveel uitrekking. F<sub>v</sub> / Δl is altijd hetzelfde getal.')],
    'F<sub>v</sub> en Δl zijn recht evenredig. Het vaste getal heet de veerconstante k.', grafiek([(2, .5), (4, 1), (6, 1.5), (8, 2)], [(0, 0, 10, 2.5, B, '')]))
 + fase('Uitleg') + KEN
 + LET + 'Werk met Δl in <b>meter</b>: 8,0 cm = 0,080 m. De veer van Amina heeft dus k = 2,0 N / 0,080 m = <b>25 N/m</b>.</div>'
 + VOORBEELD
 + fase('Nu jij')
 + oef_fig('opl_v2', '5.2', 'Vul de tekening aan', 'Aan dezelfde veer hangt 150 g. F<sub>z</sub> is al getekend (1 hokje ≙ 0,5 N). Teken F<sub>v</sub> en zet het symbool erbij.', veer(3, 0),
    [('Grootte', 'F<sub>v</sub> = F<sub>z</sub> = 1,5 N → 3 hokjes'), ('Tekening', 'vanuit het ophangpunt (bovenste stip), naar boven')], 'Een pijl van 3 hokjes naar boven.', veer(3, 3))
 + oef_fig('opl_v3', '5.3', 'Zelf tekenen en rekenen', 'Nu hangt 250 g aan de veer (k = 25 N/m). Teken F<sub>z</sub> en F<sub>v</sub> (1 hokje ≙ 0,5 N) en bereken de uitrekking.', veer(0, 0),
    [('F<sub>z</sub>', '0,250 kg · 10 N/kg = 2,5 N → 5 hokjes naar beneden'), ('F<sub>v</sub>', '2,5 N → 5 hokjes naar boven'), ('Δl', 'Δl = F<sub>v</sub> / k = 2,5 N / 25 N/m = 0,10 m = 10 cm')], 'Δl = 10 cm', veer(5, 5))
 + oef('opl_v4', '5.4', 'De veerconstante berekenen', 'Een kracht van 4,0 N rekt een andere veer 10 cm uit. Bereken k. Is die veer stijver of slapper dan de veer van Amina?',
    [('Gegeven', 'F<sub>v</sub> = 4,0 N · Δl = 10 cm = 0,10 m'), ('Formule', 'k = F<sub>v</sub> / Δl'), ('Berekening', '4,0 N / 0,10 m = 40 N/m'), ('Vergelijk', '40 N/m is meer dan 25 N/m')], 'k = 40 N/m: deze veer is stijver.')
 + oef('opl_v5', '5.5', 'De uitrekking berekenen', 'In een balpen zit een veertje met k = 200 N/m. Je drukt er met 3,0 N op. Hoeveel wordt het veertje ingedrukt?',
    [('Gegeven', 'F<sub>v</sub> = 3,0 N · k = 200 N/m'), ('Formule', 'Δl = F<sub>v</sub> / k'), ('Berekening', '3,0 N / 200 N/m = 0,015 m')], 'Δl = 0,015 m = 1,5 cm')
 + oef_fig('opl_v6', '5.6', 'Twee veren vergelijken', 'De grafiek toont veer A en veer B. a) Welke veer is het stijfst? b) Bereken k van veer A.', grafiek(lijnen=TWEE),
    [('a', 'bij dezelfde kracht rekt A minder uit: A is het stijfst (steilere lijn)'), ('b', 'A: 2,5 N bij 4 cm = 0,04 m → k = 2,5 N / 0,04 m = 62,5 N/m')], 'Steilere lijn = stijvere veer = grotere k.', grafiek(lijnen=TWEE))
 + fase('Controleer')
 + denk('denk_9', 'Je hangt dubbel zoveel massa aan dezelfde veer. Wat gebeurt er met de uitrekking? En met k?', [
    ('Kracht', 'dubbele massa → dubbele F<sub>z</sub> → dubbele F<sub>v</sub>'), ('Verband', 'F<sub>v</sub> en Δl zijn recht evenredig'), ('k', 'k hoort bij de veer zelf')],
    'De uitrekking verdubbelt. k blijft dezelfde.')
 + denk('denk_10', 'Je hangt een heel zware massa aan een veer. Als je ze eraf haalt, blijft de veer langer. Hoe komt dat? Geldt F<sub>v</sub> = k · Δl dan nog?', [
    ('Grens', 'je bent voorbij de elasticiteitsgrens gegaan'), ('Vervorming', 'de vervorming is plastisch: de veer blijft vervormd')],
    'Voorbij de elasticiteitsgrens geldt de formule niet meer.')
 + tool('krachten-3aso.html#ve1', 'Doe de proef zelf in de tool en oefen extra'))
