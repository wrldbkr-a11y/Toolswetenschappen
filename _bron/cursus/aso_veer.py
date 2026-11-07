# Hoofdstuk 5 Veerkracht voor de cursus Krachten 3ASO.
# Leerlingen: een ingevulde naslag (niets in te vullen). Leerkracht (?leerkracht): een EDI-draaiboek met wisbordvragen.
# Wordt uitgevoerd in de naamruimte van aso_krachten.py (exec), dus alle helpers zijn beschikbaar.

# ---- EDI-draaiboek: alleen zichtbaar in de leerkrachtweergave (en in de Word-versie voor de leerkracht) ----
EDI_CSS = ('<style>.edi{display:none;border:2px solid #7c3aed;border-radius:12px;padding:12px 16px;margin:12px 0 18px;background:#faf5ff}'
           '.edi .kop{font-weight:800;color:#6d28d9;margin-bottom:6px}.edi h4{margin:12px 0 4px;color:#5b21b6;font-size:1rem}'
           '.edi .wb{font-weight:700}.edi .antw{color:#047857}.edi .fout{color:#b45309}</style>'
           '<script>if(new URLSearchParams(location.search).has("leerkracht"))document.write("<style>.edi{display:block}</style>")</script>')

VF = '<span style="position:relative;display:inline-block">F<span style="position:absolute;left:.05em;top:-.62em;font-size:.75em">→</span></span>'

def wisbord(vraag, antwoord, fout=''):
    f = f' <span class="fout">(fout: {fout})</span>' if fout else ''
    return f'<li><span class="wb">{vraag}</span> <span class="antw">→ {antwoord}</span>{f}</li>'

def edi(fasen):
    """fasen: lijst van (titel, html). Geeft een blok dat leerlingen niet zien."""
    return '<div class="edi"><div class="kop">Wisbordvragen (alleen voor de leerkracht)</div>' + ''.join(f'<h4>{t_}</h4>{h}' for t_, h in fasen) + '</div>'

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

# ---- leerlingentekst (ingevuld) ----
MEET = [(50, '0,50', '2,0'), (100, '1,0', '4,0'), (150, '1,5', '6,0'), (200, '2,0', '8,0')]
TD = '<td style="min-width:56px;text-align:center">'
tab_meet = ('<table style="border-collapse:collapse;margin:8px 0 12px;font-size:15px" cellpadding="6" border="1" bordercolor="#cbd5e1">'
    '<tr><th>massa m (g)</th>' + ''.join(f'{TD}{m}</td>' for m, _, _ in MEET) + '</tr>'
    '<tr><th>F<sub>v</sub> = F<sub>z</sub> (N)</th>' + ''.join(f'{TD}{f}</td>' for _, f, _ in MEET) + '</tr>'
    '<tr><th>uitrekking Δl (cm)</th>' + ''.join(f'{TD}{d}</td>' for _, _, d in MEET) + '</tr>'
    '<tr><th>F<sub>v</sub> / Δl (N/cm)</th>' + ''.join(f'{TD}0,25</td>' for _ in MEET) + '</tr></table>')

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

DRAAIBOEK = edi([
 ('Start', '<ol>'
   + wisbord('200 g hangt aan een touw. F<sub>z</sub>? (g ≈ 10 N/kg)', '2,0 N', '2000 N')
   + wisbord('8,0 cm in meter?', '0,080 m', '0,8 m') + '</ol>'),
 ('Tijdens de uitleg', '<ol>'
   + wisbord('Veer P: k = 200 N/m, veer Q: k = 25 N/m. Welke is het stijfst?', 'P')
   + wisbord('Teken ' + VF + '<sub>v</sub> op een massa aan een veer.', 'vanuit het ophangpunt, naar boven', 'vanuit het midden of naar beneden')
   + wisbord('Dubbele massa: wat gebeurt er met Δl? En met k?', 'Δl verdubbelt, k blijft gelijk', 'k verdubbelt')
   + wisbord('150 g aan de veer van Amina (k = 25 N/m). Δl?', '1,5 N / 25 N/m = 0,060 m = 6,0 cm') + '</ol>'),
 ('Einde', '<ol>'
   + wisbord('F<sub>v</sub> = 6,0 N en Δl = 0,20 m. k?', '30 N/m')
   + wisbord('De veer blijft langer na een zware massa. Waarom?', 'voorbij de elasticiteitsgrens (plastisch)') + '</ol>'),
])

h5 = (DRAAIBOEK
 + '<p>Hang je een massa aan een veer, dan rekt de veer uit. De veer trekt terug omhoog: dat is de <b>veerkracht F<sub>v</sub></b>. Hangt de massa stil, dan is F<sub>v</sub> even groot als F<sub>z</sub>.</p>'
 + '<p>Amina hing telkens meer massa aan dezelfde veer en mat de uitrekking Δl (g ≈ 10 N/kg):</p>' + tab_meet
 + figuur(grafiek([(2, .5), (4, 1), (6, 1.5), (8, 2)], [(0, 0, 10, 2.5, B, '')]), 'De punten liggen op een rechte door de oorsprong: dubbel zoveel kracht geeft dubbel zoveel uitrekking.')
 + '<p>F<sub>v</sub> / Δl is bij elke meting hetzelfde getal. Dat vaste getal is de <b>veerconstante k</b> van die veer.</p>'
 + KEN
 + LET + 'Werk met Δl in <b>meter</b>: 8,0 cm = 0,080 m. De veer van Amina heeft dus k = 2,0 N / 0,080 m = <b>25 N/m</b>.</div>'
 + VOORBEELD
 + LET + 'Rek je een veer te ver uit, dan komt ze niet meer terug: <b>plastische vervorming</b>. Voorbij die <b>elasticiteitsgrens</b> geldt F<sub>v</sub> = k · Δl niet meer.</div>'
 + tool('krachten-3aso.html#ve1', 'Doe de proef zelf in de tool'))

# ---- extra oefeningen voor de oefenreeks (zelfstandige inoefening) ----
o_balpen = oef('opl_x', 0, 'Een veertje in een balpen', 'In een balpen zit een veertje met k = 200 N/m. Je drukt er met 3,0 N op. Hoeveel wordt het veertje ingedrukt?',
    [('Gegeven', 'F<sub>v</sub> = 3,0 N · k = 200 N/m'), ('Formule', 'Δl = F<sub>v</sub> / k'), ('Berekening', '3,0 N / 200 N/m = 0,015 m')], 'Δl = 0,015 m = 1,5 cm')
o_twee = oef_fig('opl_x', 0, 'Twee veren vergelijken', 'De grafiek toont veer A en veer B. a) Welke veer is het stijfst? b) Bereken k van veer A.', grafiek(lijnen=TWEE),
    [('a', 'bij dezelfde kracht rekt A minder uit: A is het stijfst (steilere lijn)'), ('b', 'A: 2,5 N bij 4 cm = 0,04 m → k = 2,5 N / 0,04 m = 62,5 N/m')], 'Steilere lijn = stijvere veer = grotere k.', grafiek(lijnen=TWEE))
