# Cursus fysica 3de jaar · andere richtingen · Thema 2 Rechtlijnige bewegingen (hoofdstuk 1 en 2), nieuw formaat.
# Gebruik:  cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/snelheid_3aso.py
# 3ASO: x(t) bestaat uit rechte stukken met plotse knikken; geen versnellen of vertragen in x(t), geen oppervlakte onder v(t).
import re, sys
B = '/home/claude/toolswetenschappen/_bron/cursus/'
sys.path.insert(0, '/home/claude/cursus')
import bouw as BM
BM.FOOTER = 'Cursus fysica — gemaakt voor klasgebruik, bij de tools op Oefentools wetenschappen.'
g = {'__name__': 'snel'}
exec(open('/home/claude/cursus/optica_cursus.py', encoding='utf-8').read().split('# ================================================================ H1')[0], g)
exec(open(B + 'aso_veer.py', encoding='utf-8').read().split('GX, GY')[0], g)
blok, oef, kader, tool, denk, figuur = g['blok'], g['oef'], g['kader'], g['tool'], g['denk'], g['figuur']
EDI_CSS, edi, W = g['EDI_CSS'], g['edi'], g['wisbord']
AANPAK_SCHEMA = 'zet de gegevens op een rij (met eenheden), kies de formule of lees de grafiek af, en reken pas dan.'
AANPAK_LEES = 'de gegevens met hun eenheid'
exec(open(B + 'nieuw_formaat.py', encoding='utf-8').read())

# ------------------------------------------------------------------ figuren
INK, GRIJS, ROOD, BLAUW, GROEN = '#1D2A36', '#cbd5e1', '#dc2626', '#2563eb', '#16a34a'
F = 'font-family="Inter,sans-serif"'
def tx(x, y, s, k=INK, a='middle', size=14, w=600): return f'<text x="{x:.1f}" y="{y:.1f}" fill="{k}" font-size="{size}" font-weight="{w}" text-anchor="{a}" {F}>{s}</text>'
def lijn(x1, y1, x2, y2, k=INK, d=2, dash=None): return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{k}" stroke-width="{d}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'
def pijl(x1, y1, x2, y2, k=INK, d=2.5):
    import math
    a = math.atan2(y2 - y1, x2 - x1); L = 10
    p1 = (x2 - L * math.cos(a - .4), y2 - L * math.sin(a - .4)); p2 = (x2 - L * math.cos(a + .4), y2 - L * math.sin(a + .4))
    return lijn(x1, y1, x2 - 6 * math.cos(a), y2 - 6 * math.sin(a), k, d) + f'<path d="M{x2:.1f},{y2:.1f} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f}Z" fill="{k}"/>'
def svg(inner, w, h): return f'<svg viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg"><rect width="{w}" height="{h}" fill="#fff"/>{inner}</svg>'

def grafiek(punten=(), tmax=60, ymax=400, dt=10, dy=100, ylab='x (m)', w=440, h=300, extra='', kleur=BLAUW, leeg=False, labels=()):
    """x(t)- of v(t)-grafiek op ruitjes; punten = [(t, y), ...] verbonden met rechte stukken"""
    X0, Y0, X1, Y1 = 58, h - 42, w - 24, 22
    sx, sy = (X1 - X0) / tmax, (Y0 - Y1) / ymax
    o = ''
    nt, ny = int(tmax / dt * 2), int(ymax / dy * 2)
    for i in range(nt + 1): o += lijn(X0 + i * dt / 2 * sx, Y0, X0 + i * dt / 2 * sx, Y1, '#e2e8f0', 1)
    for j in range(ny + 1): o += lijn(X0, Y0 - j * dy / 2 * sy, X1, Y0 - j * dy / 2 * sy, '#e2e8f0', 1)
    o += pijl(X0, Y0, X1 + 14, Y0) + pijl(X0, Y0, X0, Y1 - 12)
    for i in range(0, int(tmax / dt) + 1): o += tx(X0 + i * dt * sx, Y0 + 18, f'{i*dt:g}'.replace('.', ','), INK, size=12, w=500)
    for j in range(0, int(ymax / dy) + 1): o += tx(X0 - 8, Y0 - j * dy * sy + 4, f'{j*dy:g}'.replace('.', ','), INK, 'end', 12, 500)
    o += tx(X1 + 12, Y0 + 32, 't (s)', INK, 'end', 13) + tx(X0 + 8, Y1 - 4, ylab, INK, 'start', 13)
    if not leeg:
        for (a, b), (c, d) in zip(punten, punten[1:]): o += lijn(X0 + a * sx, Y0 - b * sy, X0 + c * sx, Y0 - d * sy, kleur, 3.5)
    for (t_, y_, s_, k_) in labels: o += tx(X0 + t_ * sx, Y0 - y_ * sy, s_, k_, 'middle', 13, 700)
    if extra: o += extra(X0, Y0, sx, sy)
    return svg(o, w, h)

def baan(w=640, h=170, tram=None, x1=None, x2=None):
    """rechte tramlijn met posities in m; tram = positie van de puntmassa"""
    X0, sx, Y = 50, 0.68, 100
    o = lijn(X0 - 20, Y, w - 20, Y, '#64748b', 4)
    for m in range(0, 801, 100):
        o += lijn(X0 + m * sx, Y - 6, X0 + m * sx, Y + 6, INK, 2) + tx(X0 + m * sx, Y + 24, str(m), INK, size=12, w=500)
    o += tx(w - 22, Y + 44, 'x (m)', INK, 'end', 13) + tx(X0, Y + 44, 'oorsprong', '#64748b', 'middle', 12, 500)
    for m, n in ((0, 'Halte A'), (300, 'Halte B'), (700, 'Halte C')):
        o += f'<rect x="{X0+m*sx-26:.1f}" y="{Y-64}" width="52" height="20" rx="4" fill="#fef3c7" stroke="#d97706"/>' + tx(X0 + m * sx, Y - 50, n, '#92400e', size=11)
    if tram is not None:
        cx = X0 + tram * sx
        o += f'<rect x="{cx-30:.1f}" y="{Y-38}" width="60" height="26" rx="8" fill="#e0f2fe" stroke="{BLAUW}" stroke-width="2"/><circle cx="{cx:.1f}" cy="{Y}" r="6" fill="{ROOD}"/>'
    if x1 is not None and x2 is not None:
        o += pijl(X0 + x1 * sx, Y + 62, X0 + x2 * sx, Y + 62, GROEN, 3) + tx((X0 + (x1 + x2) / 2 * sx), Y + 56 + (0 if x2 > x1 else 0), 'Δx', GROEN, size=14)
    return svg(o, w, h + 10)

# grafieken van de cursus
TRAM = [(0, 0), (20, 300), (40, 300), (60, 700)]                     # rit A→B (15 m/s), halte, B→C (20 m/s)
G_TRAM = grafiek(TRAM, 60, 800, 10, 100, labels=[(30, 340, 'stilstand', '#64748b')])
G_TRAM_V = grafiek([(0, 15), (20, 15)], 60, 25, 10, 5, 'v (m/s)', extra=lambda X0, Y0, sx, sy:
                   lijn(X0 + 20 * sx, Y0, X0 + 40 * sx, Y0, BLAUW, 3.5) + lijn(X0 + 40 * sx, Y0 - 20 * sy, X0 + 60 * sx, Y0 - 20 * sy, BLAUW, 3.5))
G_STEIL = grafiek([(0, 0), (40, 400)], 40, 400, 10, 100, kleur=BLAUW, extra=lambda X0, Y0, sx, sy:
                  lijn(X0, Y0, X0 + 40 * sx, Y0 - 200 * sy, ROOD, 3.5) + tx(X0 + 30 * sx, Y0 - 330 * sy, 'fiets A', BLAUW, 'end', 13) + tx(X0 + 30 * sx, Y0 - 115 * sy, 'fiets B', ROOD, 'start', 13))
def helling(X0, Y0, sx, sy):
    return (lijn(X0 + 10 * sx, Y0 - 100 * sy, X0 + 30 * sx, Y0 - 100 * sy, GROEN, 2.5, '6 4') + lijn(X0 + 30 * sx, Y0 - 100 * sy, X0 + 30 * sx, Y0 - 300 * sy, ROOD, 2.5, '6 4')
            + tx(X0 + 20 * sx, Y0 - 100 * sy + 18, 'Δt = 20 s', GROEN, size=13) + tx(X0 + 30 * sx + 8, Y0 - 200 * sy, 'Δx = 200 m', ROOD, 'start', 13))
G_HELLING = grafiek([(0, 0), (40, 400)], 40, 400, 10, 100, extra=helling)

# ------------------------------------------------------------------ teksten
LD = ('<p>Na dit thema kan je:</p><ul class="doelen">'
      '<li>het verschil uitleggen tussen <b>puntmassa</b>, <b>baan</b>, <b>positie</b>, <b>tijdstip</b>, <b>verplaatsing</b> en <b>tijdsverloop</b>;</li>'
      '<li>het begrip <b>snelheid</b> uitleggen;</li><li>het verschil uitleggen tussen <b>gemiddelde</b> en <b>ogenblikkelijke snelheid</b>;</li>'
      '<li>een <b>eenparig rechtlijnige beweging</b> (ERB) beschrijven en herkennen;</li><li>de formule v = Δx / Δt gebruiken en <b>omvormen</b> om Δx of Δt te berekenen;</li>'
      '<li>de <b>x(t)-grafiek</b> en de <b>v(t)-grafiek</b> van een ERB tekenen;</li><li>het verband uitleggen tussen de <b>helling</b> van de x(t)-grafiek en de snelheid;</li>'
      '<li>het <b>differentiequotiënt Δx/Δt</b> uitleggen.</li></ul>')
VK = g['vk']('Een getal met een <b>eenheid</b>: 300 m, 20 s. Zonder eenheid betekent een getal niets.',
             'Omzetten: 1 km = 1000 m, 1 h = 60 min = 3600 s.',
             'Een formule omvormen: uit a = b ÷ c volgt b = a · c en c = b ÷ a.',
             'Zo los je een vraagstuk op (thema Krachten): gegeven, gevraagd, formule, oplossing met eenheden, antwoordzin.')

d1 = f'''<p>Een tram van de MIVB rijdt van halte naar halte. Om die beweging te beschrijven, maken we het eenvoudig: we kijken naar <b>één punt</b> van de tram.</p>
{kader('Definities', '<ul><li>Een <b>puntmassa</b> is een voorwerp waarvan je de afmetingen verwaarloost. Je stelt het voor als een punt.</li><li>De <b>baan</b> is de lijn die de puntmassa volgt. Is de baan een rechte, dan is de beweging <b>rechtlijnig</b>.</li></ul>')}
{figuur(baan(tram=150), 'De tram als puntmassa (rood punt) op een rechte baan.')}
<p>Of je een voorwerp als puntmassa mag zien, hangt af van de vraag. Voor de rit van Halte A naar Halte C is de tram klein tegenover de afstand. Wil je weten of de tram onder een brug past, dan zijn zijn afmetingen net belangrijk.</p>'''
d2 = f'''<p>Op de baan kies je een <b>oorsprong</b> (de plaats 0 m). Elke plaats op de baan heeft dan een getal: de <b>positie</b>.</p>
{kader('Definities', '<ul><li><b>Positie x</b>: de plaats op de baan, gemeten vanaf de oorsprong (in m).</li><li><b>Tijdstip t</b>: het moment waarop iets gebeurt (in s).</li><li><b>Verplaatsing Δx</b> = x<sub>2</sub> − x<sub>1</sub>: eindpositie min beginpositie.</li><li><b>Tijdsverloop Δt</b> = t<sub>2</sub> − t<sub>1</sub>: de tijd tussen twee tijdstippen.</li></ul><p>Δ (delta) betekent: <b>verschil</b>, altijd "eind min begin".</p>')}
{figuur(baan(tram=700, x1=300, x2=700), 'Van Halte B (x₁ = 300 m) naar Halte C (x₂ = 700 m): Δx = 700 m − 300 m = 400 m.')}
<p>Een <b>tijdstip</b> is één moment ("om 8.05 u", "t = 20 s"). Een <b>tijdsverloop</b> is een stuk tijd ("de rit duurt 40 s").</p>'''
d3 = f'''{kader('Definities', '<ul><li>De <b>snelheid</b> zegt hoeveel meter een voorwerp zich verplaatst per seconde.</li><li>De <b>gemiddelde snelheid</b> = verplaatsing gedeeld door het tijdsverloop: <b>v<sub>gem</sub> = Δx / Δt</b>.</li><li>De <b>ogenblikkelijke snelheid</b> is de snelheid op één tijdstip. Je leest ze af op de snelheidsmeter.</li></ul>')}
<p>De eenheid van snelheid is <b>m/s</b>. In het verkeer gebruik je <b>km/h</b>. Omzetten: <b>1 m/s = 3,6 km/h</b>. Van m/s naar km/h: × 3,6. Van km/h naar m/s: ÷ 3,6.</p>
{figuur(G_TRAM, 'De x(t)-grafiek van de tram: van A naar B, een halte van 20 s, dan van B naar C.')}
<p>De tram rijdt 700 m in 60 s: v<sub>gem</sub> = 700 m ÷ 60 s ≈ 12 m/s. Toch was de snelheid nooit 12 m/s: eerst 15 m/s, dan 0 m/s (halte), dan 20 m/s. De gemiddelde snelheid zegt niets over de snelheid op één moment.</p>
{tool('snelheid-3aso.html#s2', 'Kies een tijdsinterval in de tool en vergelijk')}'''
d4 = f'''{kader('Definitie', '<p>Een <b>eenparig rechtlijnige beweging (ERB)</b> is een beweging langs een <b>rechte</b> baan met een <b>constante snelheid</b>. In elke seconde legt het voorwerp dezelfde afstand af.</p>')}
{kader('Formules', '<p><b>v = Δx / Δt</b> &nbsp;&nbsp; → &nbsp;&nbsp; <b>Δx = v · Δt</b> &nbsp;&nbsp; → &nbsp;&nbsp; <b>Δt = Δx / v</b></p><p>v in m/s, Δx in m, Δt in s. Bij een ERB is de gemiddelde snelheid gelijk aan de snelheid op elk moment.</p>')}
<p>Voorbeelden: een tram op een recht stuk met de snelheidsmeter op 54 km/h, een roltrap in het metrostation, een lift die even snel blijft stijgen. Het vertrekken en stoppen hoort er niet bij.</p>'''
d5 = f'''<p>Bij een ERB komt er elke seconde evenveel bij: de x(t)-grafiek is een <b>schuine rechte</b>. De snelheid verandert niet: de v(t)-grafiek is een <b>horizontale rechte</b>.</p>
{figuur(G_TRAM_V, 'De v(t)-grafiek van dezelfde tramrit: 15 m/s, dan 0 m/s, dan 20 m/s.')}
{kader('Helling = snelheid', '<p>Hoe <b>steiler</b> de x(t)-grafiek, hoe <b>groter</b> de snelheid. Een <b>horizontaal</b> stuk betekent <b>stilstand</b>.</p><p>De helling bereken je met het <b>differentiequotiënt Δx/Δt</b>: neem twee punten van de grafiek, deel het verschil in x door het verschil in t. Dat is de (gemiddelde) snelheid tussen die twee tijdstippen.</p>')}
{figuur(G_HELLING, 'Tussen t = 10 s en t = 30 s: Δx/Δt = 200 m ÷ 20 s = 10 m/s.')}
{figuur(G_STEIL, 'Twee fietsers. Fiets A is steiler, dus sneller: 400 m in 40 s = 10 m/s. Fiets B: 200 m in 40 s = 5 m/s.')}
<p><b>Een x(t)-grafiek tekenen</b> bij een ERB: je hebt maar <b>twee punten</b> nodig, bv. het begin en het einde. Verbind ze met een lat.</p>
{tool('snelheid-3aso.html#s3', 'Verander snelheid en beginpositie in de tool en kijk naar de grafieken')}'''

delen = [('Puntmassa en baan', d1), ('Positie, tijdstip, verplaatsing en tijdsverloop', d2),
         ('Gemiddelde en ogenblikkelijke snelheid', d3), ('Eenparig rechtlijnige beweging', d4), ('De x(t)- en v(t)-grafiek van een ERB', d5)]
NRS = ['1', '1', '2.1', '2.2', '2.2']

def D(idee, vb, test, wb, letop=None): return dict(idee=idee, vb=vb, test=test, wb=wb, letop=letop)
GEHEUGEN = ' <span style="color:#475569">🧭 Gegeven → gevraagd → formule → oplossing met eenheden → antwoordzin.</span>'
C = dict(delen=[
 D('Om een beweging te beschrijven maken we ze eenvoudig: het voorwerp wordt een punt, en de lijn die het volgt is de baan.',
   ('Puntmassa of niet?', 'Een bus rijdt van het Zuidstation naar Schaarbeek. Mag je de bus als een puntmassa zien als je de duur van de rit wil berekenen?',
    [('Afmetingen', 'de bus is 12 m lang.'), ('Afstand', 'de rit is ongeveer 6 km: de bus is heel klein tegenover de afstand.'),
     ('Besluit', 'ja: de afmetingen spelen geen rol, dus je mag de bus als een punt zien.')]),
   [('Wanneer mag je een voorwerp níet als puntmassa zien?', 'Als de afmetingen belangrijk zijn voor de vraag, bv. of een vrachtwagen onder een brug past.'),
    ('Wat betekent "rechtlijnig"?', 'De baan is een rechte lijn.')],
   ([('Beschrijf hoe je naar school komt.', 'eigen antwoord: bus, tram, te voet …')],
    [('Wat is de baan?', 'de lijn die de puntmassa volgt', 'de weg zelf, met zijn breedte'), ('Een bal die je recht omhoog gooit: rechtlijnig?', 'ja')],
    [('Puntmassa = …', 'voorwerp zonder afmetingen, voorgesteld als punt')])),
 D('Positie is waar je bent. Verplaatsing is hoeveel je positie veranderd is. Tijdstip is wanneer, tijdsverloop is hoelang.',
   ('Verplaatsing berekenen', 'De tram staat om t₁ = 20 s aan Halte B (x₁ = 300 m) en om t₂ = 60 s aan Halte C (x₂ = 700 m). Bereken Δx en Δt.',
    [('Δx', 'x₂ − x₁ = 700 m − 300 m = 400 m, want Δ is altijd eind min begin.'),
     ('Δt', 't₂ − t₁ = 60 s − 20 s = 40 s, om dezelfde reden.'),
     ('Controle', 'de eenheden kloppen: Δx in m, Δt in s.')]),
   [('Wat is het verschil tussen een tijdstip en een tijdsverloop?', 'Een tijdstip is één moment. Een tijdsverloop is de tijd tussen twee tijdstippen.'),
    ('Waarom heb je een oorsprong nodig om een positie te geven?', 'Een positie is een afstand tot een vast punt. Zonder oorsprong weet je niet vanaf waar je meet.')],
   ([('Wat betekent Δ?', 'verschil')],
    [('x₁ = 200 m, x₂ = 500 m: Δx?', '300 m', '700 m'), ('"De les duurt 50 minuten": tijdstip of tijdsverloop?', 'tijdsverloop', 'tijdstip')],
    [('Δx = …', 'x₂ − x₁')]),
   'Δ betekent altijd <b>eind min begin</b>, nooit begin min eind.'),
 D('Snelheid zegt hoeveel meter je per seconde aflegt. De gemiddelde snelheid kijkt naar de hele rit, de ogenblikkelijke snelheid naar één moment.',
   ('Gemiddelde snelheid van Amina', 'Amina fietst 3,6 km naar school in 12 minuten. Wat is haar gemiddelde snelheid in m/s en in km/h?' + GEHEUGEN,
    [('Eenheden', 'Δx = 3,6 km = 3600 m en Δt = 12 min = 720 s, want de formule werkt met m en s.'),
     ('Formule', 'v<sub>gem</sub> = Δx / Δt = 3600 m ÷ 720 s = 5,0 m/s.'),
     ('km/h', '5,0 m/s × 3,6 = 18 km/h.'),
     ('Antwoord', 'Amina fietst gemiddeld 5,0 m/s, of 18 km/h.')]),
   [('Waarom is de gemiddelde snelheid van een tramrit lager dan de snelheid tussen de haltes?', 'De tram staat ook stil aan de haltes. Dat tijdsverloop telt mee, maar de tram verplaatst zich dan niet.'),
    ('Wat toont de snelheidsmeter van een auto?', 'De ogenblikkelijke snelheid: de snelheid op dat moment.')],
   ([('Hoeveel seconden zitten in een uur?', '3600')],
    [('10 m/s = ? km/h', '36 km/h', '2,8 km/h'), ('72 km/h = ? m/s', '20 m/s')],
    [('Gemiddeld of ogenblikkelijk: de flitspaal meet …', 'ogenblikkelijk')]),
   'm/s → km/h: <b>× 3,6</b>. km/h → m/s: <b>÷ 3,6</b>. Controleer: km/h is altijd het grootste getal.'),
 D('Bij een ERB blijft de snelheid gelijk. Met v = Δx / Δt bereken je de snelheid, en met de omgevormde formules de verplaatsing of het tijdsverloop.',
   ('Hoelang duurt de roltrap?', 'Een roltrap in het metrostation Louiza is 40 m lang en beweegt met 0,50 m/s. Hoelang sta je erop?' + GEHEUGEN,
    [('Gegeven', 'Δx = 40 m, v = 0,50 m/s. Gevraagd: Δt.'),
     ('Formule', 'Δt = Δx / v, want uit v = Δx / Δt haal je Δt door te wisselen.'),
     ('Oplossing', 'Δt = 40 m ÷ 0,50 m/s = 80 s.'),
     ('Antwoord', 'Je staat 80 s (1 min 20 s) op de roltrap.')]),
   [('Waarom is een tram die vertrekt aan een halte geen ERB?', 'Zijn snelheid verandert: hij versnelt. Bij een ERB blijft de snelheid gelijk.'),
    ('Hoe vorm je v = Δx / Δt om naar Δx?', 'Vermenigvuldig beide kanten met Δt: Δx = v · Δt.')],
   ([('a = b ÷ c. Hoe vind je b?', 'b = a · c')],
    [('v = 15 m/s, Δt = 4 s: Δx?', '60 m', '3,75 m'), ('ERB: wat blijft constant?', 'de snelheid', 'de positie')],
    [('Geef de drie vormen van de formule.', 'v = Δx/Δt, Δx = v·Δt, Δt = Δx/v')]),
   'Reken eerst om naar <b>m</b> en <b>s</b>. Met km en s door elkaar komt er een fout uit.'),
 D('Bij een ERB is de x(t)-grafiek een schuine rechte en de v(t)-grafiek een horizontale rechte. Hoe steiler de x(t)-grafiek, hoe groter de snelheid.',
   ('Snelheid aflezen uit een grafiek', 'In de x(t)-grafiek van fiets A lees je af: op t = 10 s is x = 100 m, op t = 30 s is x = 300 m. Wat is de snelheid?',
    [('Twee punten', 'kies twee punten die je goed kan aflezen, op een hoek van het rooster.'),
     ('Differentiequotiënt', 'Δx/Δt = (300 m − 100 m) ÷ (30 s − 10 s) = 200 m ÷ 20 s.'),
     ('Besluit', 'v = 10 m/s. Omdat de grafiek een rechte is, is de snelheid overal 10 m/s.')]),
   [('Waarom is de v(t)-grafiek van een ERB een horizontale rechte?', 'De snelheid verandert niet. Op elk tijdstip staat hetzelfde getal.'),
    ('Wat betekent een horizontaal stuk in een x(t)-grafiek?', 'De positie verandert niet: het voorwerp staat stil, v = 0 m/s.')],
   ([('Wat staat op de horizontale as?', 'de tijd t')],
    [('Steilere x(t)-lijn: sneller of trager?', 'sneller'), ('Horizontaal stuk in x(t)?', 'stilstand', 'constante snelheid')],
    [('Hoeveel punten heb je nodig om de x(t)-grafiek van een ERB te tekenen?', 'twee')]),
   'Een <b>horizontale</b> lijn betekent in een x(t)-grafiek <b>stilstand</b>, maar in een v(t)-grafiek een <b>constante snelheid</b>. Kijk altijd eerst naar de as.')],
 uitd=[('Uitdaging · Te laat voor de bus?', 'Yassin staat 300 m van de bushalte. De bus vertrekt over 4 minuten. Yassin wandelt 1,2 m/s. Haalt hij de bus als hij wandelt? Hoe snel moet hij minstens gaan?',
        [('Eenheden', 'Δt = 4 min = 240 s; Δx = 300 m.'),
         ('Wandelen', 'Δt = Δx / v = 300 m ÷ 1,2 m/s = 250 s: dat is meer dan 240 s, hij is te laat.'),
         ('Minimum', 'v = Δx / Δt = 300 m ÷ 240 s = 1,25 m/s: iets sneller wandelen is genoeg.')],
        'Hij haalt de bus niet als hij 1,2 m/s wandelt; met 1,25 m/s lukt het net.',
        'Zet eerst alles in m en s. Bereken dan de tijd die hij nodig heeft en vergelijk met de tijd die hij heeft.'),
       ('Uitdaging · Grafiek lezen en vertellen', 'Kijk naar de x(t)-grafiek van de tram (deel 3). Vertel in drie zinnen wat de tram doet. Bereken de snelheid in elk stuk, in m/s en in km/h. Teken daarna de v(t)-grafiek op ruitjespapier.',
        [('0–20 s', 'van 0 m naar 300 m: v = 300 m ÷ 20 s = 15 m/s = 54 km/h.'),
         ('20–40 s', 'de positie blijft 300 m: stilstand aan Halte B, v = 0 m/s.'),
         ('40–60 s', 'van 300 m naar 700 m: v = 400 m ÷ 20 s = 20 m/s = 72 km/h.'),
         ('v(t)', 'drie horizontale stukken: 15, 0 en 20 m/s.')],
        'Elk recht stuk in de x(t)-grafiek is een horizontaal stuk in de v(t)-grafiek.',
        'Verdeel de grafiek in stukken.'),
       ('Uitdaging · Inhalen op de fietsweg', 'Sara vertrekt om t = 0 s aan het begin van een rechte fietsweg en fietst 5 m/s. Tom vertrekt 20 s later op dezelfde plaats en fietst 7 m/s. Na hoeveel meter haalt Tom Sara in? Schets beide x(t)-grafieken (twee punten per lijn).',
        [('Voorsprong', 'na 20 s staat Sara op 5 m/s · 20 s = 100 m.'),
         ('Inlopen', 'Tom rijdt 2 m/s sneller: hij loopt 2 m per seconde in. 100 m ÷ 2 m/s = 50 s na zijn vertrek.'),
         ('Plaats', 'Tom: 7 m/s · 50 s = 350 m. Controle Sara: 5 m/s · 70 s = 350 m.'),
         ('Grafiek', 'de twee rechten snijden in (70 s; 350 m).')],
        'Tom haalt Sara in na 350 m, op t = 70 s.', None)],
 begrip=[('puntmassa', 'voorwerp waarvan je de afmetingen verwaarloost'), ('baan', 'lijn die de puntmassa volgt'), ('rechtlijnige beweging', 'de baan is een rechte'),
         ('oorsprong', 'plaats 0 m op de baan'), ('positie x', 'plaats op de baan, gemeten vanaf de oorsprong (m)'), ('tijdstip t', 'één moment (s)'),
         ('verplaatsing Δx', 'x₂ − x₁ (m)'), ('tijdsverloop Δt', 't₂ − t₁ (s)'), ('snelheid v', 'verplaatsing per seconde (m/s)'),
         ('gemiddelde snelheid', 'v_gem = Δx / Δt over een heel tijdsverloop'), ('ogenblikkelijke snelheid', 'snelheid op één tijdstip (snelheidsmeter)'),
         ('ERB', 'eenparig rechtlijnige beweging: rechte baan, constante snelheid'), ('x(t)-grafiek', 'positie in functie van de tijd'),
         ('v(t)-grafiek', 'snelheid in functie van de tijd'), ('helling', 'hoe steil de x(t)-grafiek is; = snelheid'), ('differentiequotiënt', 'Δx/Δt tussen twee punten van de grafiek')])

# ------------------------------------------------------------------ oefeningen
LEEG = grafiek((), 50, 250, 10, 50, leeg=True)
LEEG_V = grafiek((), 50, 10, 10, 2, 'v (m/s)', leeg=True)
O3 = grafiek([(0, 100), (10, 100), (30, 300), (50, 300)], 50, 400, 10, 100)
oefs = ''.join([
 oef('opl_1', 1, 'Begrippen', 'Noteer bij elk zinsdeel het juiste begrip: positie, tijdstip, verplaatsing of tijdsverloop.<br>a) "Om 8.12 u vertrekt de tram."<br>b) "De rit duurt 25 minuten."<br>c) "De tram staat 300 m voorbij de oorsprong."<br>d) "De tram rijdt van 300 m naar 700 m."',
     [('a', 'tijdstip'), ('b', 'tijdsverloop'), ('c', 'positie'), ('d', 'verplaatsing (Δx = 400 m)')], 'Wanneer = tijdstip, hoelang = tijdsverloop, waar = positie, hoever veranderd = verplaatsing.'),
 oef('opl_2', 2, 'Omzetten', 'Zet om.<br>a) 15 m/s = … km/h &nbsp; b) 90 km/h = … m/s &nbsp; c) 30 km/h = … m/s (zone 30 in Brussel)',
     [('a', '15 × 3,6 = 54 km/h'), ('b', '90 ÷ 3,6 = 25 m/s'), ('c', '30 ÷ 3,6 ≈ 8,3 m/s')], 'm/s → km/h: × 3,6; km/h → m/s: ÷ 3,6.'),
 oef('opl_3', 3, 'Rekenen met de ERB', 'Een trein rijdt met een constante snelheid van 30 m/s.<br>a) Hoeveel meter legt hij af in 2,0 minuten?<br>b) Hoelang doet hij over 9,0 km?',
     [('a', 'Δt = 120 s; Δx = v · Δt = 30 m/s · 120 s = 3600 m = 3,6 km.'), ('b', 'Δx = 9000 m; Δt = Δx / v = 9000 m ÷ 30 m/s = 300 s = 5,0 min.')], 'Reken eerst om naar m en s.'),
 oef('opl_4', 4, 'Een grafiek lezen', 'Bekijk de x(t)-grafiek van een wandelaar.' + figuur(O3, '') + 'a) Wat doet de wandelaar tussen 0 s en 10 s?<br>b) Bereken zijn snelheid tussen 10 s en 30 s.<br>c) Hoe groot is zijn verplaatsing in de hele beweging?',
     [('a', 'de positie blijft 100 m: hij staat stil.'), ('b', 'Δx/Δt = (300 m − 100 m) ÷ (30 s − 10 s) = 10 m/s.'), ('c', 'Δx = 300 m − 100 m = 200 m.')], 'Horizontaal = stilstand; schuin = ERB.'),
 oef('opl_5', 5, 'Tekenen: x(t)-grafiek', 'Een skater vertrekt op x = 50 m en rijdt 4 m/s, 50 s lang. Teken de x(t)-grafiek. Bereken eerst twee punten.' + figuur(LEEG, 'Teken op deze grafiek of op ruitjespapier.'),
     [('Punt 1', 't = 0 s: x = 50 m.'), ('Punt 2', 'na 50 s: Δx = 4 m/s · 50 s = 200 m, dus x = 250 m.'), ('Tekenen', 'verbind (0 s; 50 m) en (50 s; 250 m) met een lat.')], 'Een schuine rechte van 50 m naar 250 m.'),
 oef('opl_6', 6, 'Tekenen: v(t)-grafiek', 'Teken de v(t)-grafiek van de wandelaar uit oefening 4.' + figuur(LEEG_V, ''),
     [('0–10 s', 'v = 0 m/s: een lijn op de tijdas.'), ('10–30 s', 'v = 10 m/s: een horizontale lijn op 10 m/s.'), ('30–50 s', 'v = 0 m/s.')],
     'Drie horizontale stukken: 0, 10 en 0 m/s.'),
])
oefs = g['oefblok'](oefs, ('snelheid-3aso.html', 'Oefen verder in de tool'))

samenv = kader('Samenvatting', '''<p><b>Puntmassa</b>: voorwerp als punt. <b>Baan</b>: de lijn die het volgt. <b>Positie x</b> (m), <b>tijdstip t</b> (s). <b>Δx = x₂ − x₁</b>, <b>Δt = t₂ − t₁</b>.</p>
<p><b>v<sub>gem</sub> = Δx / Δt</b> (m/s). <b>Ogenblikkelijke snelheid</b>: op één moment. 1 m/s = 3,6 km/h.</p>
<p><b>ERB</b>: rechte baan, constante snelheid. Δx = v · Δt en Δt = Δx / v. x(t): schuine rechte (steiler = sneller, horizontaal = stilstand). v(t): horizontale rechte. <b>Helling = Δx/Δt = snelheid</b>.</p>''')

# ------------------------------------------------------------------ bouwen
blokken = [blok('lesdoelen', '', 'Lesdoelen', LD), blok('voorkennis', '', 'Voorkennis', VK)]
for i, (k, inh) in enumerate(delen, start=1):
    inh = deel(inh, C['delen'][i - 1], i)
    if i == 1: inh = EDI_CSS + inh
    blokken.append(blok(f'deel{i}', NRS[i - 1], k, inh, f'deel{i}'))
blokken += [blok('oefeningen', '', 'Oefeningen op papier', oefs + uitdagingen(C['uitd'], False), 'oefeningen'),
            blok('begrippen', '', 'Begrippenlijst', begrippen(C['begrip'])),
            blok('samenvatting', '', 'Samenvatting', samenv, 'samenvatting')]
BM.bouw('cursus-snelheid-3aso.html', 'Fysica 3de jaar · andere richtingen · Thema 2 Rechtlijnige bewegingen · Hoofdstuk 1 en 2', 'Snelheid',
        'Werk dit thema samen met de tool <a href="snelheid-3aso.html">Snelheid</a>. Oefeningen maak je op papier. De oplossingen staan online, zodra ze in de les besproken zijn.',
        blokken, vrijgave(blokken, delen), [])
print('gemaakt: cursus-snelheid-3aso.html')
