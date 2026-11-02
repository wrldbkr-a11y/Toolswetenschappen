# bouwt remediering.html: één kaart per hoofdstuk, gebouwd op de 7 leerstrategieën voor leerlingen
import re, json, html as H
ROOT = '/home/claude/toolswetenschappen/'

STRAT = {
 'doelen':  ('Vertrek van doelen', 'Lees de doelen. Wat moet ik kennen, wat moet ik kunnen?'),
 'fouten':  ('Leer uit je fouten', 'Kijk je toets na: wat is fout en waarom?'),
 'spreiden':('Spreiden', 'Leer in korte stukken, op meerdere dagen.'),
 'toets':   ('Toets jezelf', 'Cursus dicht. Schrijf op wat je nog weet. Kijk dan na.'),
 'redenering': ('Leg de redenering uit', 'Zeg in eigen woorden waarom en hoe.'),
 'schema':  ('Schema of tekening', 'Zet de leerstof om in een tekening of schema met woorden erbij.'),
 'elkaar':  ('Oefen door elkaar', 'Maak oefeningen van verschillende soorten door elkaar.'),
}
ZIN = {
 'toets': ['Ik weet nog: …', 'Ik was vergeten dat …'],
 'redenering': ['… omdat …', 'Als … groter wordt, dan wordt … want …'],
 'schema': ['Dit deel heet … Het zorgt voor …', 'Eerst … daarna … tot slot …'],
}

# (id, groep, titel, cursus, strategie dag 1, opdracht dag 1, tool(url,label), oefeningen dag 2, extra tool (url,label) of None)
K = [
 ('chemie-wetenschap', 'Chemie 3de jaar', 'Chemie als wetenschap', 'cursus-chemie-wetenschap.html', 'toets',
  'Schrijf met je cursus dicht de 9 gevarensymbolen op: teken de ruit en schrijf de naam erbij. Schrijf ook op wat een H-zin en een P-zin is, met een voorbeeld. Kijk daarna na in je cursus en verbeter in het groen.',
  ('chemie-stoffen.html#les12', 'Stoffen onder de loep · gevarensymbolen'), [1, 3, 5, 6], ('chemie-stoffen.html#les12', 'Oefen de gevarensymbolen in de tool')),
 ('chemie-mengsels', 'Chemie 3de jaar', 'Zuivere stoffen en mengsels', 'cursus-chemie-mengsels.html', 'schema',
  'Maak een schema: materie → zuivere stof of mengsel → homogeen of heterogeen → de soorten mengsels. Schrijf bij elk vakje één voorbeeld uit je eigen leven.',
  ('chemie-mengsels.html#les22', 'Mengsels en stofeigenschappen'), [1, 3, 4, 5], ('chemie-mengsels.html', 'Sorteeroefeningen in de tool')),
 ('chemie-scheiding', 'Chemie 3de jaar', 'Scheidingstechnieken', 'cursus-chemie-scheidingstechnieken.html', 'schema',
  'Teken de opstelling van filtreren en van destilleren. Schrijf de namen van alle onderdelen erbij. Schrijf onder elke tekening op welke stofeigenschap je gebruikt.',
  ('chemie-scheidingstechnieken.html#les32', 'Scheidingstechnieken · werking en onderdelen'), [2, 3, 5, 6], ('chemie-scheidingstechnieken.html#lesov', 'Test jezelf: onderdelen en voorbeelden')),
 ('chemie-atomen', 'Chemie 3de jaar', 'Atomen en elementen', 'cursus-chemie-atomen-elementen.html', 'toets',
  'Schrijf met je cursus dicht: de 6 atoommodellen in de juiste volgorde, met de wetenschapper en één kenmerk. Schrijf daarna de symbolen van de elementen 1 tot 20 en de Latijnse symbolen. Kijk na en verbeter in het groen.',
  ('chemie-atoommodellen.html', 'Atomen en elementen'), [2, 4, 5, 6], ('chemie-atoommodellen.html#les12', 'Test jezelf: symbolen')),
 ('chemie-atoombouw', 'Chemie 3de jaar', 'Bouw van het atoom', 'cursus-chemie-atoombouw.html', 'schema',
  'Teken het schillenmodel van zuurstof, natrium en chloor. Schrijf het aantal protonen en neutronen in de kern, kleur de valentie-elektronen en noteer de elektronenconfiguratie.',
  ('chemie-atoombouw.html', 'Bouw van het atoom · atoombouwer'), [3, 5, 6, 7], ('elektronenconfiguratie.html', 'Oefen elektronenconfiguraties')),
 ('chemie-pse', 'Chemie 3de jaar', 'Het periodiek systeem', 'cursus-chemie-pse.html', 'redenering',
  'Kies 3 elementen uit verschillende groepen. Leg voor elk uit wat je uit de plaats in het PSE weet: groep → aantal valentie-elektronen, periode → aantal schillen, links of rechts van de trap → metaal of niet-metaal.',
  ('chemie-pse.html#lesC', 'Periodiek systeem · groep en periode'), [3, 4, 6, 7], ('chemie-pse.html', 'Oefenen in de tool')),
 ('optica-zien', 'Fysica 3de jaar', 'Zien door licht', 'cursus-zien-door-licht.html', 'schema',
  'Teken de schaduw van een bal met één lamp, en daarna met twee lampen. Duid kernschaduw en bijschaduw aan. Teken ook zon, maan en aarde bij een zonsverduistering.',
  ('optica.html#z3', 'Optica · schaduw'), [3, 4, 6, 7], ('optica.html#z4', 'Bekijk zons- en maansverduistering in de tool')),
 ('optica-weerkaatsing', 'Fysica 3de jaar', 'Zien door weerkaatsing', 'cursus-weerkaatsing.html', 'schema',
  'Teken op ruitjespapier een spiegel, een invallende straal en de weerkaatste straal. Duid de normaal, de invalshoek en de weerkaatsingshoek aan. Teken daarna het beeld van een potlood in een vlakke spiegel.',
  ('optica.html#s12', 'Optica · beeld bij een vlakke spiegel'), [2, 3, 6, 9], ('optica.html#s13', 'Oefen het gezichtsveld in de tool')),
 ('optica-breking', 'Fysica 3de jaar', 'Lichtbreking', 'cursus-lichtbreking.html', 'redenering',
  'Leg uit, met een tekening erbij: wat gebeurt er met een lichtstraal van lucht naar water? En van water naar lucht? Wanneer krijg je totale weerkaatsing? Gebruik de woorden normaal, ijl, dicht en grenshoek.',
  ('optica.html#s5', 'Optica · breking'), [2, 4, 5, 8], ('optica.html#s6', 'Bekijk totale weerkaatsing in de tool')),
 ('optica-lenzen', 'Fysica 3de jaar', 'Lenzen', 'cursus-lenzen.html', 'schema',
  'Teken op ruitjespapier een bolle lens met F en F\'. Teken de 3 hoofdstralen vanuit de top van een pijl die voorbij 2F staat. Schrijf bij elke straal de regel. Noteer de kenmerken van het beeld.',
  ('optica.html#s10', 'Optica · bolle lens'), [2, 5, 10, 13], ('optica.html#s16', 'Oefen de vergrotingsfactor in de tool')),
 ('krachten', 'Fysica 3de jaar', 'Krachten', 'cursus-krachten-beweging.html', 'schema',
  'Teken op schaal (1 cm = 10 N) twee krachten van 30 N en 50 N: eens in dezelfde zin, eens in tegengestelde zin en eens loodrecht op elkaar. Teken telkens de resulterende kracht en schrijf de grootte erbij.',
  ('krachten-construeren.html#1.1', 'Krachten samenstellen en ontbinden'), [3, 6, 9, 12], ('krachten-beweging.html', 'Oefenen in de tool Traagheid en beweging')),
 ('druk-vast', 'Fysica 4de jaar', 'Druk bij vaste stoffen', 'cursus-druk-vaste-stoffen.html', 'redenering',
  'Leg uit waarom een naaldhak een parketvloer beschadigt en een olifant niet. Gebruik de formule p = F / A en de woorden kracht, oppervlakte en druk.',
  ('druk.html#s1', 'Druk · vaste stoffen'), [2, 3, 5, 6], ('druk.html#s12', 'Oefenen in de tool Druk')),
 ('druk-gas', 'Fysica 4de jaar', 'Druk bij gassen', 'cursus-druk-gassen.html', 'redenering',
  'Leg met het deeltjesmodel uit hoe gasdruk ontstaat. Leg daarna uit waarom een zak chips opzwelt in een vliegtuig. Gebruik de woorden overdruk en onderdruk.',
  ('druk.html#s3', 'Druk · gassen'), [1, 2, 4, 6], ('druk.html#s12', 'Oefenen in de tool Druk')),
 ('druk-vloeistof', 'Fysica 4de jaar', 'Druk bij vloeistoffen', 'cursus-druk-vloeistoffen.html', 'redenering',
  'Maak een tabel: wat gebeurt er met de hydrostatische druk als de diepte, de massadichtheid of de zwaarteveldsterkte groter wordt? Schrijf bij elke rij waarom. Leg ook uit hoe een garagekrik werkt.',
  ('druk.html#s6', 'Druk · hydrostatische druk'), [1, 3, 7, 8], ('druk.html#s12', 'Oefenen in de tool Druk')),
 ('archimedes', 'Fysica 4de jaar', 'Archimedeskracht', 'cursus-archimedes.html', 'redenering',
  'Leg uit wanneer een voorwerp zinkt, zweeft, stijgt of drijft. Gebruik telkens de zwaartekracht en de archimedeskracht, en vergelijk de massadichtheid van het voorwerp met die van de vloeistof. Teken bij elke situatie de twee krachtpijlen.',
  ('druk.html#s9', 'Druk · zinken, zweven, stijgen of drijven'), [1, 3, 5, 10], ('druk.html#s12', 'Oefenen in de tool Druk')),
 ('energie', 'Fysica 4de jaar', 'Energie in systemen', 'cursus-energie-systemen.html', 'schema',
  'Teken een energieschema van een tram die vertrekt aan de halte en van een bal die van een trap valt. Schrijf welke energievormen er zijn en in welke vorm ze omgezet worden.',
  ('energie-vermogen.html', 'Energie, vermogen en rendement'), [2, 4, 6, 9], ('energie-vermogen.html', 'Oefenen in de tool (laatste deel)')),
 ('arbeid', 'Fysica 4de jaar', 'Arbeid en vermogen', 'cursus-arbeid-vermogen.html', 'redenering',
  'Leg uit wanneer een kracht arbeid levert en wanneer niet. Geef bij elk een voorbeeld. Leg daarna uit wat vermogen is, met een voorbeeld van twee toestellen.',
  ('energie-vermogen.html', 'Energie, vermogen en rendement'), [1, 3, 6, 7], ('formuleredeneertool.html', 'Oefen de formules omvormen')),
 ('ladingen', 'Fysica 5de jaar', 'Ladingen', 'cursus-ladingen.html', 'schema',
  'Teken een geleidende bol en een geladen staaf die in de buurt komt. Teken de ladingen in de bol (influentie). Teken ook wat er gebeurt als je de bol aardt.',
  ('ladingen.html#l5', 'Ladingen · influentie en polarisatie'), [2, 4, 6, 7], ('elektrostatica.html', 'Oefen influentie in de tool Elektrostatische inductie')),
 ('coulomb', 'Fysica 5de jaar', 'Krachten tussen ladingen', 'cursus-coulomb.html', 'schema',
  'Teken drie ladingen op één lijn. Teken op de middelste lading de twee coulombkrachten, met het aangrijpingspunt op de lading. Teken de resulterende kracht.',
  ('krachten-op-ladingen.html', 'Krachten op ladingen'), [1, 3, 5, 7], ('krachten-op-ladingen.html', 'Nieuwe oefeningen in de tool Krachten op ladingen')),
 ('veld', 'Fysica 5de jaar', 'Elektrisch veld', 'cursus-elektrisch-veld.html', 'schema',
  'Teken de veldlijnen van een positieve lading, een negatieve lading, twee tegengestelde ladingen en een homogeen veld tussen twee platen. Schrijf bij elke tekening één kenmerk van de veldlijnen.',
  ('elektrisch-veld.html', 'Elektrisch veld'), [1, 3, 4, 5], ('elektrisch-veld.html', 'Oefen in de tool Elektrisch veld')),
 ('potentiaal', 'Fysica 5de jaar', 'Potentiaal', 'cursus-potentiaal.html', 'redenering',
  'Leg de vergelijking uit tussen een massa in het zwaarteveld en een lading in een homogeen elektrisch veld. Wat is potentiële energie, wat is potentiaal, wat is spanning? Gebruik een tabel met twee kolommen.',
  ('elektrisch-veld.html', 'Elektrisch veld (homogeen veld)'), [1, 2, 4, 5], ('formuleredeneertool.html', 'Oefen de formules omvormen')),
 ('schakelingen', 'Fysica 5de jaar', 'Gemengde schakelingen', 'cursus-schakelingen.html', 'elkaar',
  'Teken de schakeling R1 + (R2 // R3) met U = 12 V, R1 = 4 Ω, R2 = 6 Ω en R3 = 12 Ω. Los ze stap voor stap op met het stappenplan: eerst van binnen naar buiten, dan van buiten naar binnen. Controleer aan het einde of de stromen en spanningen kloppen.',
  ('schakelingen.html#gemengd', 'Gemengde schakelingen · stap voor stap'), [2, 3, 4, 7], ('schakelingen.html#oefenen', 'Nieuwe opgaven in de tool')),
 ('water-planten', 'Biologie 3de jaar', 'Waterhuishouding in planten', 'cursus-waterhuishouding-planten.html', 'schema',
  'Teken een plant met wortel, stengel en blad. Teken met pijlen de weg van het water (houtvaten, opwaarts) en van de assimilaten (zeefvaten). Schrijf bij elk deel welk weefsel het werk doet.',
  ('biologie-prikkels.html#p6', 'Water, prikkels en reacties · transport'), [2, 5, 7, 8], ('biologie-prikkels.html#p2', 'Oefen de weefsels in de tool')),
 ('bio-homeostase', 'Biologie 3de jaar', 'Homeostase en feedbacksystemen', 'cursus-homeostase.html', 'schema',
  'Teken het schema prikkel → receptor → verwerking → effector → effect voor zweten bij warmte. Teken daarna een grafiek van negatieve feedback (lichaamstemperatuur) en een grafiek van positieve feedback (bevalling).',
  ('biologie-prikkels.html#f2', 'Water, prikkels en reacties · feedback'), [1, 3, 5, 6], ('biologie-prikkels.html#f1', 'Oefen: intern of extern milieu')),
 ('bio-receptoren', 'Biologie 3de jaar', 'Receptoren bij de mens', 'cursus-receptoren.html', 'toets',
  'Schrijf met je cursus dicht de 5 soorten receptoren op, met de prikkel en een voorbeeld. Schrijf daarna de definitie van prikkeldrempel, prikkelgewenning en prikkelfilter, met telkens een voorbeeld. Kijk na en verbeter in het groen.',
  ('biologie-prikkels.html#r1', 'Water, prikkels en reacties · receptoren'), [1, 3, 5, 6], ('biologie-prikkels.html#r2', 'Experimenteer met de prikkeldrempel')),
 ('bio-oog', 'Biologie 3de jaar', 'Bouw en werking van het oog', 'cursus-oog.html', 'schema',
  'Teken een doorsnede van het oog en schrijf de namen van de delen erbij. Teken met pijlen de weg van het licht tot op het netvlies. Schrijf bij 4 delen de functie.',
  ('biologie-prikkels.html#r3', 'Water, prikkels en reacties · bouw van het oog'), [1, 3, 5, 6], ('biologie-prikkels.html#r5', 'Oefen: staafje of kegeltje')),
 ('bio-organismen', 'Biologie 3de jaar', 'Receptoren bij andere organismen', 'cursus-receptoren-organismen.html', 'redenering',
  'Kies 3 dieren en 2 planten uit de cursus. Leg voor elk uit welke prikkel ze opvangen en waarom dat nuttig is om te overleven.',
  ('biologie-prikkels.html#r8', 'Water, prikkels en reacties · andere organismen'), [1, 2, 3, 4], ('biologie-prikkels.html#r8', 'Bekijk de voorbeelden in de tool')),
 ('bio-reageren', 'Biologie 3de jaar', 'De mens reageert op prikkels', 'cursus-reageren.html', 'schema',
  'Vul het schema prikkel → receptor → verwerking → effector → effect in voor 4 situaties uit je eigen dag: 2 met een spier en 2 met een klier. Schrijf er telkens bij of de reactie bewust of onbewust is.',
  ('biologie-prikkels.html#e1', 'Water, prikkels en reacties · reageren'), [1, 2, 3, 4], ('biologie-prikkels.html#e1', 'Vul het schema in de tool in')),
 ('bio-spieren', 'Biologie 3de jaar', 'Reactie door spieren', 'cursus-spieren.html', 'redenering',
  'Leg uit hoe je je arm buigt en strekt. Gebruik de woorden biceps, triceps, samentrekken, ontspannen, pees en antagonist. Leg daarna uit hoe voedsel door je slokdarm gaat.',
  ('biologie-prikkels.html#e4', 'Water, prikkels en reacties · samentrekken'), [1, 3, 4, 5], ('biologie-prikkels.html#e3', 'Oefen de soorten spierweefsel')),
]

def doelen_van(cursus):
    h = open(ROOT + cursus, encoding='utf-8').read()
    ul = re.search(r'<ul class="doelen">(.*?)</ul>', h, re.S).group(1)
    ds = [re.sub(r'\s+', ' ', re.sub(r'<(?!/?(sub|sup)>)[^>]+>', '', li)).strip().rstrip(';.') for li in re.findall(r'<li>(.*?)</li>', ul, re.S)]
    ds = ['Ik kan ' + d for d in ds]
    oefs = dict((int(n), re.sub('<[^>]+>', '', t).strip()) for n, t in re.findall(r'<div class="oef"[^>]*>\s*<div class="titel"><span class="nr">(\d+)</span>(.*?)</div>', h))
    return ds, oefs

exec(open('/home/claude/remediering/vragen.py', encoding='utf-8').read())
VAKTAAL = json.load(open('/home/claude/remediering/vaktaal.json', encoding='utf-8'))
PAD = {'chemie-wetenschap': 'Hoofdstuk 1 · Chemie als wetenschap', 'chemie-mengsels': 'Hoofdstuk 2 · Zuivere stoffen', 'chemie-scheiding': 'Hoofdstuk 3 · Scheidingstechnieken',
 'chemie-atomen': 'Hoofdstuk 1 · Atomen en elementen', 'chemie-atoombouw': 'Hoofdstuk 2 · Bouw van het atoom', 'chemie-pse': 'Hoofdstuk 3 · Periodiek',
 'optica-zien': '1. Zien door licht', 'optica-weerkaatsing': '2. Zien door weerkaatsing', 'optica-breking': '3. Lichtbreking', 'optica-lenzen': '4. Lenzen',
 'krachten': 'Hoofdstuk 2 · Krachten', 'druk-vast': 'Druk bij vaste', 'druk-gas': 'Druk bij gassen', 'druk-vloeistof': 'Druk bij vloeistoffen', 'archimedes': 'Hoofdstuk 4 · Archimedeskracht',
 'energie': 'Energie in systemen', 'arbeid': 'Arbeid en vermogen', 'ladingen': 'Hoofdstuk 1 · Ladingen', 'coulomb': 'Krachten tussen ladingen', 'veld': 'Hoofdstuk 3 · Elektrisch veld',
 'potentiaal': 'Hoofdstuk 4 · Potentiaal', 'water-planten': 'Homeostase van de waterhuishouding', 'bio-homeostase': 'A. Basisbegrippen', 'bio-receptoren': 'Hoofdstuk 1 · Receptoren bij de mens', 'bio-oog': ('Hoofdstuk 2 · Bouw van het oog', 'Hoofdstuk 3 · Werking van het oog'), 'bio-organismen': 'Hoofdstuk 4 · Receptoren bij andere', 'bio-reageren': 'Hoofdstuk 1 · De mens reageert', 'bio-spieren': 'Hoofdstuk 2 · Reactie door spieren', 'schakelingen': 'GEEN'}
def woorden(id_):
    uit, gezien = [], set()
    for p, v in VAKTAAL:
        keys = PAD[id_] if isinstance(PAD[id_], tuple) else (PAD[id_],)
        if any(k in p for k in keys):
            for b in v:
                if b['begrip'] not in gezien: gezien.add(b['begrip']); uit.append([b['begrip'], b['uitleg'], b.get('zin', '')])
    return uit
def vraag(x):
    if x[0] == 'mc': return {'t': 'mc', 'dok': 3, 'v': x[1], 'o': x[2], 'j': x[3], 'u': x[4]}
    return {'t': 'open', 'dok': x[0], 'v': x[1], 'a': x[2]}
EXTRA_WOORDEN = {'schakelingen': [
  ['de wet van Ohm', 'Bij een ohmse weerstand is de spanning gelijk aan weerstand maal stroomsterkte: U = R · I.', 'Met de wet van Ohm bereken je de stroom door een weerstand.'],
  ['de serieschakeling', 'Onderdelen staan na elkaar: overal loopt dezelfde stroom.', 'In een serieschakeling verdeelt de spanning zich over de weerstanden.'],
  ['de parallelschakeling', 'Onderdelen staan in aparte takken naast elkaar: over elke tak staat dezelfde spanning.', 'De toestellen in huis staan in een parallelschakeling.'],
  ['de substitutieweerstand', 'De ene weerstand die een groep weerstanden kan vervangen zonder dat de stroom uit de bron verandert.', 'De substitutieweerstand van twee parallelle weerstanden is kleiner dan de kleinste.'],
  ['de gemengde schakeling', 'Een schakeling met zowel serie- als paralleldelen.', 'Een gemengde schakeling los je op van binnen naar buiten.']],
 'bio-organismen': [
  ['de receptor', 'Een cel of groep cellen die één soort prikkel opvangt en omzet in een impuls.', 'De snorharen van een kat zijn verbonden met receptoren voor aanraking.'],
  ['de echolocatie', 'Een dier stoot geluid uit en vangt de echo op om de weg of een prooi te vinden.', 'Een vleermuis vindt insecten in het donker met echolocatie.'],
  ['de fototropie', 'Een plant groeit naar het licht toe.', 'Door fototropie buigt de kamerplant naar het raam.'],
  ['de geotropie', 'Een plant groeit volgens de zwaartekracht: de wortel naar beneden, de stengel naar boven.', 'Door geotropie groeit de wortel van een boon altijd naar beneden.']]}
kaarten = []
for (id_, groep, titel, cursus, strat, opdr, tool, oef, extra) in K:
    ds, oefs = doelen_van(cursus)
    assert all(n in oefs for n in oef), (id_, oef)
    kaarten.append(dict(id=id_, groep=groep, titel=titel, cursus=cursus, strat=strat, opdr=opdr, tool=tool,
                        oef=[[n, oefs[n]] for n in oef], rest=[[n, t] for n, t in oefs.items() if n not in oef], extra=extra, doelen=ds, woorden=woorden(id_), vragen=[vraag(x) for x in V[id_]]))
    if not kaarten[-1]['woorden']: kaarten[-1]['woorden'] = EXTRA_WOORDEN[id_]

tpl = open('/home/claude/remediering/sjabloon.html', encoding='utf-8').read()
out = tpl.replace('/*KAARTEN*/', json.dumps(kaarten, ensure_ascii=False)).replace('/*STRAT*/', json.dumps(STRAT, ensure_ascii=False)).replace('/*ZIN*/', json.dumps(ZIN, ensure_ascii=False))
open(ROOT + 'remediering.html', 'w', encoding='utf-8').write(out)
print(len(kaarten), 'kaarten')
