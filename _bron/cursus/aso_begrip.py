# Begrip zichtbaar maken in de cursus Krachten 3ASO: het idee per deel, denkstappen, test jezelf,
# en uitdagende oefeningen (DOK 3) met een aanpak. Uitgevoerd in de naamruimte van aso_krachten.py,
# na aso_extra.py en vóór aso_wisbord.py.

IDEE_STIJL = 'background:#FEF9C3;border-left:4px solid #CA8A04;border-radius:0 10px 10px 0;padding:10px 14px;margin:6px 0 14px'
def idee(tekst):
    return f'<div class="idee" style="{IDEE_STIJL}"><b style="color:#854D0E">Het idee.</b> {tekst}</div>'

def denkstappen(titel, stappen):
    lis = ''.join(f'<li><b>{v}</b> {u}</li>' for v, u in stappen)
    return kader('Denkstappen · ' + titel, f'<ol>{lis}</ol>')

def test(nr, vragen):
    """Test jezelf: vragen die je niet beantwoordt door naar een figuur te kijken; antwoorden online (vrijgave)"""
    q = '<b>Test jezelf.</b> Kan je dit uitleggen zonder in je cursus te kijken?' + ''.join(f'<br>{i}. {v}' for i, (v, _) in enumerate(vragen, start=1))
    return denk(f'denk_{100 + nr}', q, [(str(i + 1), a) for i, (_, a) in enumerate(vragen)], 'Lukt het niet? Lees het idee en het uitgewerkte voorbeeld opnieuw.')

IDEE = {
 'h1': 'In de fysica spreek je allemaal dezelfde taal: dezelfde eenheden (SI) en even nauwkeurig als je gemeten hebt. Zo kan iedereen je resultaat begrijpen en controleren.',
 'h2a': 'Een kracht zie je niet. Je ziet alleen wat ze doet: een voorwerp van vorm laten veranderen (statisch) of de beweging laten veranderen (dynamisch).',
 'h2b': 'Een getal alleen zegt niet genoeg over een kracht: je moet ook weten waar ze werkt en in welke richting en zin. Daarom teken je een kracht als een pijl.',
 'h3a': 'Een voorwerp verandert pas van beweging (sneller, trager of van richting) als er een kracht op werkt. De snelheid is ook een pijl: hoe langer, hoe sneller.',
 'h3b': 'Een voorwerp "wil" blijven doen wat het deed: stilstaan of even snel rechtdoor. Dat is traagheid. Hoe groter de massa, hoe moeilijker je dat verandert.',
 'h3c': 'Niet elke kracht apart bepaalt de beweging, maar alle krachten samen: de resulterende kracht. Is die nul, dan verandert er niets aan de beweging.',
 'h4a': 'De aarde trekt aan alles in haar buurt, ook zonder het aan te raken. Altijd naar haar middelpunt, dus voor ons naar beneden.',
 'h4b': 'Hoe meer massa, hoe harder de aarde trekt. Op een ander hemellichaam trekt het veld sterker of zwakker: dat zegt g.',
 'h4c': 'Massa is hoeveel stof je hebt en blijft overal gelijk. Gewicht is hoe hard je op je steun drukt. Normaalkracht is hoe hard de steun terugduwt.',
 'h5': 'Een veer wil altijd terug naar haar eigen lengte. Hoe verder je ze uitrekt of samendrukt, hoe harder ze terug trekt of duwt.',
}

TEST = {
 'h1': [('Waarom mag je de uitkomst van je rekenmachine niet zomaar overnemen?', 'Je rekenmachine weet niet hoe nauwkeurig je gemeten hebt. De uitkomst mag niet nauwkeuriger zijn dan je minst nauwkeurige meting.'),
        ('Waarom schrijf je 0,00052 m liever als 5,2 · 10<sup>−4</sup> m?', 'Korter, je telt geen nullen verkeerd, en je ziet meteen hoe groot het getal is.')],
 'h2a': [('Een auto rijdt even snel door een bocht. Werkt er een kracht? Hoe weet je dat?', 'Ja: de richting van de beweging verandert. Dat is een dynamisch effect, dus er werkt een kracht.'),
         ('Kan een kracht werken zonder dat je iets ziet veranderen?', 'Ja, als andere krachten ze opheffen, bv. een boek op een tafel: de krachten heffen elkaar op.')],
 'h2b': [('Twee krachten van 50 N: kunnen ze een ander effect hebben? Hoe?', 'Ja: een ander aangrijpingspunt, een andere richting of een andere zin.'),
         ('Waarom heb je een schaal nodig?', 'Een kracht in newton kan je niet meten met een lat. De schaal zegt hoeveel newton één cm of hokje voorstelt.')],
 'h3a': [('Waarom is "even snel door een bocht" toch een andere bewegingstoestand?', 'De richting van de snelheid verandert, en de snelheid is een vector.'),
         ('Wat zegt een kortere snelheidsvector op een later tijdstip?', 'Het voorwerp gaat trager.')],
 'h3b': [('Waarom val je naar voor als de bus remt? Er duwt toch niemand?', 'Door je traagheid wil je even snel verder bewegen; de bus stopt onder je.'),
         ('Is traagheid een kracht? Waarom (niet)?', 'Nee. Het is een eigenschap van een voorwerp: het verzet zich tegen een verandering van beweging.')],
 'h3c': [('Een fiets rijdt even snel rechtdoor. De fietser trapt toch. Hoe kan F<sub>r</sub> dan 0 zijn?', 'De trapkracht en de wrijving zijn even groot en tegengesteld: samen geven ze 0.'),
         ('Wat gebeurt er met een voorwerp als F<sub>r</sub> loodrecht op de beweging staat?', 'Het gaat een bocht maken: de richting verandert, niet de grootte van de snelheid.')],
 'h4a': [('Waarom vallen mensen in Australië niet van de aarde?', 'De zwaartekracht wijst overal naar het middelpunt van de aarde, ook daar.'),
         ('Waarom begint de pijl van F<sub>z</sub> in het midden van het voorwerp?', 'De zwaartekracht trekt aan het hele voorwerp; je tekent ze in het zwaartepunt.')],
 'h4b': [('Je massa op de maan is 55 kg. Waarom is F<sub>z</sub> daar toch kleiner?', 'g is op de maan kleiner (1,62 N/kg), dus F<sub>z</sub> = m · g is kleiner.'),
         ('Hoe kan je g van een planeet bepalen als je een voorwerp met gekende massa hebt?', 'Meet F<sub>z</sub> en reken g = F<sub>z</sub> / m.')],
 'h4c': [('F<sub>z</sub> en F<sub>G</sub> zijn bij een boek op tafel even groot. Waarom zijn het toch verschillende krachten?', 'F<sub>z</sub> werkt op het boek (door de aarde), F<sub>G</sub> werkt op de tafel (door het boek).'),
         ('Waarom begint F<sub>N</sub> niet in het midden van het boek?', 'F<sub>N</sub> is een contactkracht van de tafel: ze werkt waar het boek de tafel raakt.')],
 'h5': [('Waarom duwt een samengedrukte veer naar buiten en trekt een uitgerekte veer naar binnen?', 'De veerkracht wil de veer altijd terug naar haar oorspronkelijke lengte brengen.'),
        ('Twee veren rekken even ver uit onder verschillende massa\'s. Welke veer is het stijfst?', 'De veer met de grootste massa: ze heeft meer kracht nodig voor dezelfde uitrekking, dus een grotere k.')],
}

D_KRACHT = denkstappen('Een kracht tekenen', [
 ('Op welk voorwerp werkt de kracht?', 'Daarop teken je de pijl.'),
 ('Wie oefent de kracht uit?', 'Dat geeft haar naam: de aarde → F<sub>z</sub>, een steun → F<sub>N</sub>, een veer → F<sub>v</sub>.'),
 ('Waar is het aangrijpingspunt?', 'Zwaartekracht: in het zwaartepunt. Een kracht door contact: waar de voorwerpen elkaar raken.'),
 ('Welke richting en zin?', 'Langs welke lijn, en naar welke kant?'),
 ('Hoe groot?', 'Grootte : schaal = lengte van de pijl (in cm of hokjes).')])
D_REKEN = denkstappen('Een vraagstuk oplossen', [
 ('Gegeven', 'schrijf alle gegevens op en zet ze om naar de SI-eenheid.'),
 ('Gevraagd', 'welke grootheid zoek je?'),
 ('Formule', 'welke formule verbindt het gegeven met het gevraagde?'),
 ('Omvormen', 'zet het gevraagde alleen aan één kant.'),
 ('Invullen en rekenen', 'met eenheden.'),
 ('Controleer', 'juiste eenheid, juist aantal BC, en is het antwoord logisch?')])

# de uitgewerkte voorbeelden met het waarom bij elke stap
h3c = h3c.replace('<li><b>Zelfde richting, tegengestelde zin:</b> F<sub>r</sub> = 60 N − 20 N = 40 N</li>',
                  '<li><b>Zelfde richting, tegengestelde zin:</b> F<sub>r</sub> = 60 N − 20 N = 40 N, want de krachten werken elkaar tegen.</li>')
h3c = h3c.replace('<li><b>Zin:</b> die van de grootste kracht: naar rechts</li>', '<li><b>Zin:</b> naar rechts, want de duwkracht is de grootste.</li>')
h4c = h4c.replace('<li><b>F<sub>z</sub>:</b> op het boek, vanuit het zwaartepunt, naar beneden</li>',
                  '<li><b>F<sub>z</sub>:</b> de aarde trekt aan het boek → pijl op het boek, vanuit het zwaartepunt, naar beneden.</li>')
h4c = h4c.replace('<li><b>F<sub>N</sub>:</b> op het boek, vanuit het contactvlak, naar boven</li>',
                  '<li><b>F<sub>N</sub>:</b> de tafel duwt het boek omhoog → pijl op het boek, vanuit het contactvlak (daar raken ze elkaar), naar boven.</li>')
h4c = h4c.replace('<li><b>F<sub>G</sub>:</b> op de tafel, vanuit het contactvlak, naar beneden</li>',
                  '<li><b>F<sub>G</sub>:</b> het boek drukt op de tafel → pijl op de tafel, vanuit het contactvlak, naar beneden.</li>')

h1 = idee(IDEE['h1']) + h1 + test(1, TEST['h1'])
h2a = idee(IDEE['h2a']) + h2a + test(2, TEST['h2a'])
h2b = idee(IDEE['h2b']) + voor_tool(h2b, D_KRACHT) + test(3, TEST['h2b'])
h3a = idee(IDEE['h3a']) + h3a + test(4, TEST['h3a'])
h3b = idee(IDEE['h3b']) + h3b + test(5, TEST['h3b'])
h3c = idee(IDEE['h3c']) + h3c + test(6, TEST['h3c'])
h4a = idee(IDEE['h4a']) + h4a + test(7, TEST['h4a'])
h4b = idee(IDEE['h4b']) + voor_tool(h4b, D_REKEN) + test(8, TEST['h4b'])
h4c = idee(IDEE['h4c']) + h4c + test(9, TEST['h4c'])
h5 = idee(IDEE['h5']) + h5 + test(10, TEST['h5'])

# ---------- uitdagende oefeningen (DOK 3) ----------
AANPAK = kader('Zo pak je een uitdaging aan', '''<p>Deze oefeningen combineren leerstof uit verschillende hoofdstukken. Vlieg er niet blind in. De tips worden telkens korter: bij de laatste oefeningen kies je de aanpak zelf.</p>
<ol><li><b>Lees</b> de opgave twee keer en maak een kleine <b>schets</b>.</li>
<li><b>Analyseer:</b> wat weet je? Wat wordt er gevraagd? Welke leerstof heb je nodig (welk hoofdstuk)?</li>
<li><b>Plan</b> je stappen: wat moet je eerst berekenen om daarna verder te kunnen?</li>
<li><b>Voer uit</b> met de denkstappen (gegeven, gevraagd, formule …).</li>
<li><b>Controleer:</b> is je antwoord logisch? Klopt de eenheid?</li></ol>''')

def aanpak(t_):
    return f'<p style="margin-top:6px;font-size:.95em;color:#475569"><i>Tip voor de aanpak:</i> {t_}</p>'

def sc_boekhand(opl):
    w, h = 600, 280
    o = (rooster(w, h) + '<rect x="160" y="180" width="280" height="14" fill="#b08968"/><rect x="176" y="194" width="12" height="86" fill="#9c7656"/><rect x="412" y="194" width="12" height="86" fill="#9c7656"/>'
         + doos(240, 140, 120, 40, '#60a5fa', '#1e3a8a') + punt(300, 160, INK, 4) + punt(330, 140, INK, 4) + t(380, 120, 'hier duwt je hand', INK, 'start', 12, 500))
    if opl:
        o += pijl(300, 160, 300, 160 + 4 * HK, PAARS) + label(306, 236, 'F', 'z', PAARS)
        o += pijl(330, 140, 330, 140 + 4 * HK, B) + label(372, 200, 'F', 'hand', B)
        o += pijl(270, 180, 270, 180 - 8 * HK, G) + label(260, 32, 'F', 'N', G, 'end')
    return svg(o, w, h)

u1 = oef('opl_x', 0, 'Uitdaging · Een veer op planeet X', 'Een rover van 900 kg ondervindt op planeet X een zwaartekracht van 3,3 kN. Op aarde rekt een veer 4,0 cm uit als je er 500 g aan hangt (g = 9,81 N/kg). Hoeveel rekt dezelfde veer uit met dezelfde 500 g op planeet X?'
    + aanpak('je hebt twee dingen nodig: g op planeet X (hoofdstuk 4) en k van de veer (hoofdstuk 5). Bereken die eerst.'),
    [('Analyse', 'gevraagd: Δl op planeet X. Daarvoor heb je F<sub>v</sub> op X en k nodig.'), ('g op X', 'g = F<sub>z</sub> / m = 3300 N / 900 kg = 3,7 N/kg'),
     ('k van de veer', 'op aarde: F<sub>v</sub> = 0,500 kg · 9,81 N/kg = 4,9 N; k = 4,9 N / 0,040 m = 123 N/m'),
     ('Op X', 'F<sub>v</sub> = 0,500 kg · 3,7 N/kg = 1,8 N; Δl = 1,8 N / 123 N/m = 0,015 m'),
     ('Controle', 'g is op X ongeveer 2,7 keer kleiner, dus Δl ook: 4,0 cm : 2,7 ≈ 1,5 cm. Logisch.')], 'Δl ≈ 1,5 cm')
u2 = oef('opl_x', 0, 'Uitdaging · Te zware koffer?', 'Op de luchthaven mag een koffer maximaal 23 kg wegen. Fatima hangt haar koffer aan een bagageweger met een veer (k = 2500 N/m). De veer rekt 9,6 cm uit (g ≈ 10 N/kg). Mag de koffer mee? Zo niet, hoeveel kilogram moet eruit?'
    + aanpak('hoofdstuk 5 en 4. Let op de eenheden.'),
    [('Analyse', 'gevraagd: de massa. Uit Δl en k haal je F<sub>v</sub>; de koffer hangt stil, dus F<sub>v</sub> = F<sub>z</sub>.'),
     ('Veerkracht', 'Δl = 9,6 cm = 0,096 m; F<sub>v</sub> = 2500 N/m · 0,096 m = 240 N'), ('Massa', 'm = F<sub>z</sub> / g = 240 N / 10 N/kg = 24 kg'),
     ('Besluit', '24 kg is meer dan 23 kg')], 'De koffer is 1 kg te zwaar.')
u3 = oef_fig('opl_x', 0, 'Uitdaging · Duwen op een boek', 'Een boek van 1,0 kg ligt op een tafel. Je duwt met je hand verticaal naar beneden op het boek met 10 N (g ≈ 10 N/kg). Teken alle krachten op het boek (schaal: 1 hokje ≙ 2,5 N). Hoe groot is de normaalkracht nu?'
    + aanpak('het boek blijft liggen.'), sc_boekhand(False),
    [('Analyse', 'op het boek werken drie krachten: F<sub>z</sub> (aarde), F<sub>hand</sub> (je hand) en F<sub>N</sub> (tafel).'),
     ('Rust', 'het boek blijft liggen → F<sub>r</sub> = 0: naar boven = naar beneden'), ('Normaalkracht', 'F<sub>N</sub> = F<sub>z</sub> + F<sub>hand</sub> = 10 N + 10 N = 20 N'),
     ('Tekenen', 'F<sub>z</sub>: 4 hokjes vanuit het midden naar beneden · F<sub>hand</sub>: 4 hokjes vanuit de stip bovenaan (daar raakt je hand het boek), naar beneden · F<sub>N</sub>: 8 hokjes vanuit het contactvlak naar boven')],
    'F<sub>N</sub> = 20 N: de tafel duwt harder terug omdat jij mee duwt.', sc_boekhand(True))
u4 = oef('opl_x', 0, 'Uitdaging · Klopt de redenering?', 'Yasmine zegt: "Een astronaut in het ISS is gewichtloos. Dus werkt er geen zwaartekracht op hem." Het ISS vliegt op 400 km hoogte; daar is g ongeveer 8,7 N/kg. Beoordeel haar redenering en verbeter ze.',
    [('Analyse', 'Yasmine haalt gewicht en zwaartekracht door elkaar.'), ('Zwaartekracht', 'g = 8,7 N/kg is niet 0, dus er werkt wel zwaartekracht: bijna 90 % van die op aarde.'),
     ('Gewichtloos', 'hij drukt op geen steun (alles valt samen rond de aarde), dus zijn gewicht is 0.')], 'Gewichtloos betekent: geen gewicht, niet: geen zwaartekracht.')
u5 = oef('opl_x', 0, 'Uitdaging · Een rotonde', 'Een auto rijdt aan constant 30 km/h door een rotonde. Ilias zegt: "De snelheid blijft gelijk, dus is F<sub>r</sub> = 0." Maak een schets van de rotonde met de snelheidsvector op twee plaatsen. Heeft Ilias gelijk? Waar wijst F<sub>r</sub>?',
    [('Schets', 'twee even lange pijlen, rakend aan de cirkel, in verschillende richtingen'), ('Analyse', 'de grootte blijft gelijk, maar de richting verandert: de bewegingstoestand verandert'),
     ('Besluit', 'er is een resulterende kracht nodig, loodrecht op de beweging, naar het midden van de rotonde (de wrijving tussen banden en weg)')], 'Ilias heeft geen gelijk: F<sub>r</sub> ≠ 0 en wijst naar het midden.')

# leerlijn voor de denkstappen: volledig in 2.2 en 4.2, daarna enkel een korte geheugensteun, in hoofdstuk 5 niets meer
def steun(t_):
    return f'<p style="font-size:.93em;color:#475569;margin:10px 0 4px">🧭 <i>{t_}</i></p>'
_K = steun('Denkstappen van 2.2: op welk voorwerp? · wie oefent uit? · aangrijpingspunt? · richting en zin? · grootte → lengte.')
h3c = h3c.replace('<p><b>Uitgewerkt voorbeeld · De resulterende kracht tekenen.</b>', _K + '<p><b>Uitgewerkt voorbeeld · De resulterende kracht tekenen.</b>', 1)
h4c = h4c.replace('<p><b>Uitgewerkt voorbeeld · Drie krachten tekenen.</b>', steun('Gebruik de denkstappen van 2.2 voor elke kracht apart.') + '<p><b>Uitgewerkt voorbeeld · Drie krachten tekenen.</b>', 1)
