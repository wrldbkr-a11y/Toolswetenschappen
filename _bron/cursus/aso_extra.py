# Uitgewerkte voorbeelden, extra oefeningen per hoofdstuk, gemengde reeks en begrippenlijst
# voor de cursus Krachten 3ASO. Uitgevoerd in de naamruimte van aso_krachten.py (na aso_wisbord.py).

def voor_tool(deel, extra):
    """zet extra inhoud net voor de laatste toolknop van een deel (of achteraan als er geen is)"""
    i = deel.rfind('<a class="toolknop"')
    return deel[:i] + extra + deel[i:] if i >= 0 else deel + extra

def vb(titel, opgave, stappen, fig=''):
    lis = ''.join(f'<li><b>{s}:</b> {u}</li>' for s, u in stappen)
    return f'<p><b>Uitgewerkt voorbeeld · {titel}.</b> {opgave}</p>' + fig + f'<ol>{lis}</ol>'

def sc_twee(f1, f2, opl, voorwerp='kar'):
    """twee krachten op één lijn (f1 naar rechts, f2 naar links, in hokjes); F_r apart erboven"""
    w, h = 600, 220
    o = rooster(w, h) + f'<rect x="0" y="160" width="{w}" height="60" fill="#e5e7eb"/>'
    if voorwerp == 'kar':
        o += doos(255, 112, 90, 40, '#93c5fd', '#1e3a8a') + '<circle cx="272" cy="156" r="6" fill="#334155"/><circle cx="328" cy="156" r="6" fill="#334155"/>'
    o += punt(300, 132, INK, 4)
    o += pijl(300, 132, 300 + f1 * HK, 132, B) + label(300 + f1 * HK + 6, 120, 'F', '1', B)
    o += pijl(300, 132, 300 - f2 * HK, 132, R) + label(300 - f2 * HK - 6, 120, 'F', '2', R, 'end')
    if opl:
        fr = f1 - f2
        o += punt(300, 70, INK, 4) + pijl(300, 70, 300 + fr * HK, 70, '#111827') + label(300 + fr * HK + (6 if fr > 0 else -6), 58, 'F', 'r', '#111827', 'start' if fr > 0 else 'end')
    return svg(o, w, h)

def sc_duw(opl):
    w, h = 600, 200
    o = rooster(w, h) + f'<rect x="0" y="150" width="{w}" height="50" fill="#e5e7eb"/>' + doos(300, 90, 100, 60, '#fde68a', '#92400e') + punt(300, 120, INK, 4)
    if opl: o += pijl(300, 120, 300 + 4 * HK, 120, B) + label(386, 108, 'F', '', B)
    return svg(o, w, h)

# ---------- uitgewerkte voorbeelden in de theorie ----------
h1 = voor_tool(h1,
    vb('Omzetten', 'Zet 2,4 km en 750 mg om naar de SI-eenheid.',
       [('Welke SI-eenheid?', 'lengte → m, massa → kg'), ('2,4 km', 'k = 1000 → 2,4 · 1000 m = 2400 m'),
        ('750 mg', 'm = 0,001 → 750 · 0,001 g = 0,750 g → 0,750 : 1000 kg = 0,000750 kg = 7,50 · 10<sup>−4</sup> kg')])
  + vb('Beduidende cijfers in een berekening', 'Een plank is 1,20 m lang en 0,35 m breed. Bereken de oppervlakte.',
       [('Rekenen', 'A = 1,20 m · 0,35 m = 0,42 m²'), ('BC van de gegevens', '1,20 → 3 BC, 0,35 → 2 BC'),
        ('Afronden', 'de uitkomst krijgt het kleinste aantal: 2 BC → A = 0,42 m²')]))

h3c = voor_tool(h3c,
    vb('De resulterende kracht tekenen', 'Amir duwt een winkelkar met F<sub>1</sub> = 60 N naar rechts. De wrijving is F<sub>2</sub> = 20 N naar links (schaal: 1 hokje ≙ 5 N).',
       [('Zelfde richting, tegengestelde zin', 'F<sub>r</sub> = 60 N − 20 N = 40 N'), ('Zin', 'die van de grootste kracht: naar rechts'),
        ('Tekening', '40 N : 5 N = 8 hokjes naar rechts'), ('Besluit', 'F<sub>r</sub> wijst mee met de beweging: de kar gaat sneller')],
       figuur(sc_twee(12, 4, True), 'F<sub>1</sub> en F<sub>2</sub> werken op de kar. F<sub>r</sub> is apart erboven getekend.')))

h4b = voor_tool(h4b,
    vb('Omvormen', 'Op de maan werkt op een astronaut met zijn pak een zwaartekracht van 194 N. Bereken zijn massa (g<sub>maan</sub> = 1,62 N/kg).',
       [('Gegeven en gevraagd', 'F<sub>z</sub> = 194 N · g = 1,62 N/kg · m = ?'), ('Formule', 'F<sub>z</sub> = m · g'),
        ('Omvormen', 'm staat vermenigvuldigd met g → deel beide kanten door g: m = F<sub>z</sub> / g'),
        ('Invullen', 'm = 194 N / 1,62 N/kg = 120 kg'), ('Controle', 'een volwassene met een zwaar pak: 120 kg is aannemelijk')]))

h4c = voor_tool(h4c,
    vb('Drie krachten tekenen', 'Een boek van 1,0 kg ligt op een tafel (g ≈ 10 N/kg). Teken F<sub>z</sub>, F<sub>N</sub> en F<sub>G</sub> (schaal: 1 hokje ≙ 2,5 N).',
       [('Grootte', 'F<sub>z</sub> = 1,0 kg · 10 N/kg = 10 N; F<sub>N</sub> = F<sub>G</sub> = 10 N → 10 : 2,5 = 4 hokjes'),
        ('F<sub>z</sub>', 'op het boek, vanuit het zwaartepunt, naar beneden'), ('F<sub>N</sub>', 'op het boek, vanuit het contactvlak, naar boven'),
        ('F<sub>G</sub>', 'op de tafel, vanuit het contactvlak, naar beneden')], figuur(sc_boek(True), 'De drie pijlen staan dicht bij elkaar, elk in het juiste aangrijpingspunt.'))
  + '<p>Hangt een voorwerp aan een touw, dan is er geen normaalkracht. Het gewicht werkt dan op het <b>ophangpunt</b>:</p>'
  + figuur(sc_lamp(True), 'Een lamp van 1,5 kg (1 hokje ≙ 5 N): F<sub>z</sub> op de lamp, F<sub>G</sub> op het plafond.'))

# ---------- extra oefeningen ----------
n1a = oef('opl_x', 0, 'Omzetten met voorvoegsels', 'Zet om naar de SI-eenheid.<ol class="deelvragen" type="a"><li>0,45 km</li><li>2500 mg</li><li>1,5 h</li></ol>',
    [('a', '0,45 · 1000 m = 450 m'), ('b', '2500 mg = 2,500 g = 0,002500 kg = 2,500 · 10<sup>−3</sup> kg'), ('c', '1,5 · 3600 s = 5400 s')], 'm, kg, s')
n1b = oef('opl_x', 0, 'Rekenen met beduidende cijfers', 'Een fietser legt 120 m af in 15,0 s. Bereken de snelheid met het juiste aantal BC.',
    [('Rekenen', '120 m / 15,0 s = 8 m/s'), ('BC', '120 (3 BC) en 15,0 (3 BC) → 3 BC')], 'v = 8,00 m/s')
n2 = oef_fig('opl_x', 0, 'Een duwkracht tekenen', 'Een kind duwt een kist met 80 N horizontaal naar rechts. Noteer de vier kenmerken en teken de kracht (schaal: 1 hokje ≙ 20 N).', sc_duw(False),
    [('Kenmerken', 'aangrijpingspunt: de stip · richting: horizontaal · zin: naar rechts · grootte: 80 N'), ('Lengte', '80 N : 20 N = 4 hokjes')], 'Een pijl van 4 hokjes naar rechts, vanuit de stip.', sc_duw(True))
n3 = oef('opl_x', 0, 'Wat doet de resulterende kracht?', 'Wat gebeurt er met de beweging?<ol class="deelvragen" type="a"><li>Een fietser trapt harder: F<sub>r</sub> wijst mee met de beweging.</li><li>Een auto remt: F<sub>r</sub> wijst tegen de beweging in.</li><li>Een bal aan een touw: F<sub>r</sub> staat loodrecht op de beweging.</li><li>Een hockeypuck glijdt op glad ijs: F<sub>r</sub> = 0.</li></ol>',
    [('a', 'sneller'), ('b', 'trager'), ('c', 'de richting verandert: een bocht'), ('d', 'blijft even snel rechtdoor glijden (ERB)')], 'Mee: sneller · tegen: trager · loodrecht: bocht · nul: niets verandert.')
n3b = oef_fig('opl_x', 0, 'Twee krachten op een kar', 'Twee kinderen trekken aan een kar: F<sub>1</sub> = 30 N naar rechts en F<sub>2</sub> = 50 N naar links (schaal: 1 hokje ≙ 5 N). Teken F<sub>r</sub> boven de kar. Wat gebeurt er als de kar stilstond?', sc_twee(6, 10, False),
    [('Grootte', 'F<sub>r</sub> = 50 N − 30 N = 20 N'), ('Zin', 'naar links, de zin van de grootste kracht'), ('Tekening', '20 N : 5 N = 4 hokjes naar links')], 'F<sub>r</sub> = 20 N naar links: de kar vertrekt naar links.', sc_twee(6, 10, True))
g1 = oef('opl_x', 0, 'Gemengd · Een appel aan een veer', 'Een appel van 200 g hangt stil aan een veer met k = 40 N/m (g ≈ 10 N/kg). a) Bereken F<sub>z</sub>. b) Hoe groot is F<sub>v</sub>? c) Bereken de uitrekking in cm.',
    [('a', 'F<sub>z</sub> = 0,200 kg · 10 N/kg = 2,0 N'), ('b', 'de appel hangt stil: F<sub>v</sub> = F<sub>z</sub> = 2,0 N'), ('c', 'Δl = 2,0 N / 40 N/m = 0,050 m = 5,0 cm')], 'Δl = 5,0 cm')
g2 = oef('opl_x', 0, 'Gemengd · Een rugzak op de maan', 'Een rugzak heeft een massa van 7500 g. a) Zet om naar kg. b) Bereken F<sub>z</sub> op de maan (g = 1,62 N/kg). c) Is de massa op de maan kleiner, gelijk of groter?',
    [('a', '7500 g = 7,500 kg'), ('b', 'F<sub>z</sub> = 7,500 kg · 1,62 N/kg = 12,2 N'), ('c', 'gelijk: massa hangt niet af van de plaats')], 'F<sub>z</sub> = 12,2 N; m blijft 7,500 kg')
g3 = oef('opl_x', 0, 'Gemengd · De bus vertrekt', 'Je staat in een bus die vertrekt. a) In welke zin val je? Leg uit met traagheid. b) Wat voor effect heeft de motorkracht op de bus? c) De bus rijdt daarna aan een constante snelheid rechtdoor. Hoe groot is F<sub>r</sub>?',
    [('a', 'naar achter: je lichaam wil door traagheid stil blijven staan'), ('b', 'dynamisch: de bus gaat sneller'), ('c', 'F<sub>r</sub> = 0 (ERB)')], 'Traagheid, dynamisch effect, F<sub>r</sub> = 0 bij ERB.')

# ---------- begrippenlijst ----------
BEGRIP = [
 ('aangrijpingspunt', 'het punt waar een kracht op een voorwerp werkt; daar begint de pijl'),
 ('beduidende cijfers (BC)', 'de cijfers die tonen hoe nauwkeurig een meting is'),
 ('bewegingstoestand', 'hoe snel een voorwerp gaat en in welke richting'),
 ('contactvlak', 'de plaats waar twee voorwerpen elkaar raken'),
 ('dynamisch effect', 'een kracht verandert de beweging (vertrekken, sneller, trager, stoppen, bocht)'),
 ('elasticiteitsgrens', 'tot daar komt een voorwerp terug in zijn vorm; verder blijft het vervormd'),
 ('gewicht F<sub>G</sub>', 'de kracht waarmee een voorwerp op zijn steun drukt of aan zijn ophangpunt trekt'),
 ('massa m', 'hoeveel stof een voorwerp bevat (kg); overal even groot'),
 ('normaalkracht F<sub>N</sub>', 'de kracht van een steun op een voorwerp, loodrecht op het contactvlak'),
 ('recht evenredig', 'wordt de ene grootheid 2 keer zo groot, dan ook de andere'),
 ('resulterende kracht F<sub>r</sub>', 'de ene kracht die hetzelfde effect heeft als alle krachten samen'),
 ('richting', 'de lijn waarlangs een kracht werkt (bv. horizontaal, verticaal)'),
 ('schaal', 'hoeveel newton één cm of één hokje voorstelt'),
 ('statisch effect', 'een kracht verandert de vorm van een voorwerp'),
 ('traagheid', 'een voorwerp wil zijn snelheid behouden; geen kracht, maar een eigenschap'),
 ('vector', 'een pijl met aangrijpingspunt, richting, zin en grootte'),
 ('veerconstante k', 'hoeveel newton nodig is per meter uitrekking (N/m); grote k = stijve veer'),
 ('veerkracht F<sub>v</sub>', 'de kracht van een vervormde veer, die terug naar haar oorspronkelijke lengte wil'),
 ('zin', 'naar welke kant een kracht wijst (bv. naar links, naar boven)'),
 ('zwaartekracht F<sub>z</sub>', 'de kracht waarmee een hemellichaam aan een voorwerp trekt'),
 ('zwaarteveld', 'het gebied rond een hemellichaam waar de zwaartekracht werkt'),
 ('zwaartepunt', 'het aangrijpingspunt van de zwaartekracht (het midden van het voorwerp)'),
]
begrippen = ('<p>Weet je niet meer wat een woord betekent? Zoek het hier op.</p>'
    '<table style="border-collapse:collapse;margin:8px 0 12px;font-size:15px;width:100%" cellpadding="6" border="1" bordercolor="#cbd5e1">'
    + ''.join(f'<tr><th style="text-align:left;white-space:nowrap">{w_}</th><td>{u}</td></tr>' for w_, u in BEGRIP) + '</table>')
