# Oefening "Van pijlen naar zinnen": een redenering met pijlen omzetten naar correct Nederlands met verbindingswoorden.
# Per cursuspagina twee ketens met een modelantwoord. Wordt gebruikt door nieuw_formaat.pagina().

VERBIND = '''<p>In een redenering schrijf je vaak pijlen: <i>vaker botsen → grotere druk</i>. Dat is een goede kladversie. In een antwoord schrijf je volzinnen met <b>verbindingswoorden</b>.</p>
<table class="vb grid"><tr><th>oorzaak</th><td><b>omdat</b>, <b>doordat</b> (werkwoord achteraan) · <b>want</b> (gewone volgorde)</td></tr>
<tr><th>gevolg</th><td><b>dus</b>, <b>daardoor</b>, <b>daarom</b> (werkwoord meteen erna) · <b>zodat</b> (werkwoord achteraan)</td></tr>
<tr><th>voorwaarde</th><td><b>als</b> … , <b>dan</b> …</td></tr>
<tr><th>volgorde</th><td><b>eerst</b>, <b>daarna</b>, <b>ten slotte</b></td></tr>
<tr><th>tegenstelling</th><td><b>maar</b>, <b>toch</b></td></tr></table>
<p><i>vaker botsen → grotere druk</i> wordt: "<b>Doordat</b> de deeltjes vaker botsen, wordt de druk groter." of "De deeltjes botsen vaker. <b>Daardoor</b> wordt de druk groter."</p>'''

Z = {
 # ---------------- biologie
 'cursus-waterhuishouding-planten.html': [
  ('watertekort → sluitcellen verliezen water → turgor daalt → huidmondjes sluiten → minder verdamping',
   'Bij een watertekort verliezen de sluitcellen water. Daardoor daalt de turgor, zodat de huidmondjes sluiten. Daarom verdampt de plant minder water.'),
  ('wortelhaartjes → grote oppervlakte → veel wateropname',
   'De wortelhaartjes maken de oppervlakte van de wortel groot. Daardoor kan de wortel veel water tegelijk opnemen.')],
 'cursus-homeostase.html': [
  ('bloedsuiker stijgt → alvleesklier maakt insuline → bloedsuiker daalt → negatieve feedback',
   'Als de bloedsuiker stijgt, maakt de alvleesklier insuline. Daardoor daalt de bloedsuiker weer. Omdat de reactie de verandering tegenwerkt, is dit negatieve feedback.'),
  ('weeën → meer hormoon → sterkere weeën → positieve feedback',
   'De weeën zorgen voor meer hormoon, en dat hormoon maakt de weeën sterker. Omdat de reactie de verandering versterkt, is dit positieve feedback.')],
 'cursus-receptoren.html': [
  ('prikkel duurt lang → prikkeldrempel stijgt → minder impulsen → je merkt de prikkel niet meer',
   'Omdat de prikkel lang duurt, stijgt de prikkeldrempel. Daardoor stuurt de receptor minder impulsen, zodat je de prikkel niet meer merkt.'),
  ('geluid → mechanoreceptoren → impuls → hersenen',
   'Het geluid prikkelt de mechanoreceptoren in je oor. Die zetten de prikkel om in een impuls, en die impuls gaat naar de hersenen.')],
 'cursus-oog.html': [
  ('weinig licht → pupil wordt groot → meer licht in het oog',
   'Als er weinig licht is, wordt de pupil groot. Zo komt er meer licht in het oog.'),
  ('weinig licht → alleen staafjes werken → staafjes zien geen kleur → alles grijs',
   'Bij weinig licht werken alleen de staafjes. Omdat staafjes geen kleur zien, zie je in het donker alles grijs.')],
 'cursus-receptoren-organismen.html': [
  ('licht van één kant → stengel groeit naar het licht → meer fotosynthese',
   'Doordat het licht van één kant komt, groeit de stengel naar het licht. Daardoor kan de plant meer fotosynthese doen.'),
  ('vleermuis maakt geluid → echo → mechanoreceptoren → vindt de mug',
   'De vleermuis maakt hoge geluiden. Ze vangt de echo op met de mechanoreceptoren in haar oren, zodat ze de mug ook in het donker vindt.')],
 'cursus-reageren.html': [
  ('geur van wafels → chemoreceptoren → hersenen → speekselklieren → speeksel · onbewust',
   'De geur van wafels prikkelt de chemoreceptoren in je neus. Die sturen een impuls naar de hersenen. Daarna maken de speekselklieren speeksel. Dat gebeurt onbewust.'),
  ('hete pot → pijnreceptoren → reflex → hand terug',
   'Als je een hete pot aanraakt, worden je pijnreceptoren geprikkeld. Daardoor trek je je hand terug voor je erover nadenkt: dat is een reflex.')],
 'cursus-spieren.html': [
  ('biceps trekt samen → arm buigt → triceps wordt uitgerekt',
   'Als de biceps samentrekt, buigt de arm. Daardoor wordt de triceps uitgerekt.'),
  ('kringspieren achter de hap trekken samen → slokdarm daar nauw → hap gaat naar de maag',
   'Achter de hap trekken de kringspieren samen, zodat de slokdarm daar nauw wordt. Daardoor wordt de hap naar de maag geduwd.')],
 # ---------------- chemie
 'cursus-chemie-wetenschap.html': [
  ('papier verbrandt → nieuwe stof → chemisch',
   'Als papier verbrandt, ontstaat er een nieuwe stof. Daarom is verbranden een chemisch verschijnsel.'),
  ('suiker lost op → je proeft de suiker nog → geen nieuwe stof → fysisch',
   'Suiker die oplost, blijft suiker, want je proeft ze nog. Er ontstaat dus geen nieuwe stof: oplossen is een fysisch verschijnsel.')],
 'cursus-chemie-mengsels.html': [
  ('melk → vetbolletjes onder de microscoop → heterogeen',
   'Onder een microscoop zie je vetbolletjes in melk. Omdat je de bestanddelen kan zien, is melk een heterogeen mengsel.'),
  ('massa hangt af van de grootte → geen stofeigenschap',
   'De massa hangt af van hoe groot het voorwerp is. Daarom is massa geen stofeigenschap, maar een voorwerpseigenschap.')],
 'cursus-chemie-scheidingstechnieken.html': [
  ('magneet → oplossen en filtreren → uitdampen (zand, zout en ijzer)',
   'Eerst haal je het ijzer eruit met een magneet. Daarna los je het zout op in water en filtreer je het zand eruit. Ten slotte damp je het water uit, zodat het zout overblijft.'),
  ('zand zwaarder dan water → zakt naar de bodem → water afgieten → decanteren',
   'Omdat zand een grotere massadichtheid heeft dan water, zakt het naar de bodem. Daarna giet je het water voorzichtig af: dat is decanteren.')],
 'cursus-chemie-atomen-elementen.html': [
  ('bijna alle deeltjes rechtdoor → atoom vooral leeg · een paar terug → kleine, zware kern',
   'Omdat bijna alle deeltjes rechtdoor gingen, besloot Rutherford dat het atoom vooral lege ruimte is. Een paar deeltjes kaatsten terug, dus moest er een kleine, zware kern zijn.'),
  ('nieuw experiment → oud model klopt niet → nieuw model → dynamisch',
   'Als een nieuw experiment iets toont dat het oude model niet kan verklaren, past men het model aan. Daarom noemen we het atoommodel dynamisch.')],
 'cursus-chemie-atoombouw.html': [
  ('5 elektronen → 5 protonen → atoomnummer 5 → boor',
   'Het atoom heeft 5 elektronen. Omdat een neutraal atoom evenveel protonen als elektronen heeft, heeft het ook 5 protonen. Het atoomnummer is dus 5: het is boor.'),
  ('K-schil vol (2) → L-schil vol (8) → 11de elektron op de M-schil',
   'De K-schil is vol met 2 elektronen en de L-schil met 8. Daarom komt het 11de elektron op de M-schil.')],
 'cursus-chemie-pse.html': [
  ('zelfde groep → evenveel valentie-elektronen → zelfde chemische eigenschappen',
   'Natrium en kalium staan in dezelfde groep. Daardoor hebben ze evenveel valentie-elektronen, zodat ze op dezelfde manier reageren.'),
  ('lage elektronegativiteit → geeft een elektron af → edelgasconfiguratie',
   'Natrium heeft een lage elektronegativiteit. Daarom geeft het gemakkelijk een elektron af, zodat het een edelgasconfiguratie krijgt.')],
 # ---------------- fysica 3NW
 'cursus-zien-door-licht.html': [
  ('maan → weerkaatst zonlicht → licht in je oog → je ziet de maan',
   'De maan maakt zelf geen licht, maar ze weerkaatst het licht van de zon. Doordat dat licht in je oog komt, zie je de maan.'),
  ('licht gaat rechtdoor → voorwerp houdt licht tegen → schaduw',
   'Omdat licht rechtdoor gaat, kan het niet om een voorwerp heen. Daardoor ontstaat er achter het voorwerp een schaduw.')],
 'cursus-weerkaatsing.html': [
  ('ruw oppervlak → licht alle kanten op → van overal zichtbaar',
   'Een muur heeft een ruw oppervlak. Daardoor weerkaatst het licht alle kanten op, zodat je de muur van overal ziet.'),
  ('beeld even ver achter de spiegel → afstand tot je beeld = 2 × afstand tot de spiegel',
   'Omdat het beeld even ver achter de spiegel staat als jij ervoor, is de afstand tot je beeld twee keer de afstand tot de spiegel.')],
 'cursus-lichtbreking.html': [
  ('water → lucht: dicht → ijl → van de normaal weg → voorwerp lijkt hoger',
   'Het licht gaat van water naar lucht, dus van dicht naar ijl. Daardoor breekt het van de normaal weg. Omdat je oog de gebroken straal terug verlengt, lijkt het voorwerp hoger te liggen.'),
  ('dicht → ijl en i > g → geen gebroken straal → totale weerkaatsing',
   'Als het licht van dicht naar ijl gaat en de invalshoek groter is dan de grenshoek, is er geen gebroken straal meer. Het licht wordt dan totaal weerkaatst.')],
 'cursus-lenzen.html': [
  ('voorwerp tussen F en 2F → beeld reëel, omgekeerd en vergroot → beamer',
   'Als het voorwerp tussen F en 2F staat, is het beeld reëel, omgekeerd en vergroot. Daarom gebruikt een beamer die positie.'),
  ('voorwerp binnen F → stralen gaan uit elkaar → verlengden snijden → virtueel beeld',
   'Staat het voorwerp binnen F, dan gaan de stralen na de lens uit elkaar. Alleen hun verlengden snijden, dus het beeld is virtueel.')],
 'cursus-krachten-beweging.html': [
  ('remmen → resulterende kracht tegen de beweging → snelheid neemt af',
   'Als een auto remt, werkt de resulterende kracht tegen de beweging in. Daardoor neemt de snelheid af.'),
  ('resulterende kracht = 0 → snelheid verandert niet → rust of ERB',
   'Als de resulterende kracht nul is, verandert de snelheid niet. Het voorwerp blijft dus stilstaan of beweegt even snel rechtdoor.')],
 'cursus-zwaartekracht-wrijving-veer.html': [
  ('volle kast → grotere normaalkracht → grotere maximale statische wrijvingskracht → moeilijker te verschuiven',
   'Een volle kast drukt harder op de vloer, zodat de normaalkracht groter is. Daardoor is ook de maximale statische wrijvingskracht groter. Daarom is een volle kast moeilijker te verschuiven.'),
  ('wielen blokkeren → banden schuiven → dynamische wrijving → kleiner → langere remweg',
   'Als de wielen blokkeren, schuiven de banden over de weg. Dan werkt de dynamische wrijving, en die is kleiner dan de statische. Daardoor wordt de remweg langer.')],
 # ---------------- fysica 3ASO
 'cursus-krachten-3aso.html': [
  ('volle winkelkar → grotere massa → meer traagheid → moeilijker te stoppen',
   'Een volle winkelkar heeft een grotere massa. Daardoor heeft ze meer traagheid, zodat ze moeilijker te stoppen is.'),
  ('veer verder uitgerekt → grotere veerkracht',
   'Hoe verder je een veer uitrekt, hoe groter de veerkracht. Als je de uitrekking verdubbelt, verdubbelt dus ook de veerkracht.')],
 'cursus-snelheid-3aso.html': [
  ('steilere x(t)-grafiek → meer meter per seconde → grotere snelheid',
   'Hoe steiler de x(t)-grafiek, hoe meer meter het voorwerp per seconde aflegt. Daarom betekent een steilere grafiek een grotere snelheid.'),
  ('tram staat stil → positie verandert niet → horizontaal stuk in de x(t)-grafiek',
   'Als de tram stilstaat, verandert zijn positie niet. Daardoor is de x(t)-grafiek daar een horizontaal stuk.')],
 # ---------------- fysica 4NW
 'cursus-druk-vaste-stoffen.html': [
  ('scherp mes → kleine oppervlakte → grote druk → snijdt makkelijk',
   'Een scherp mes heeft een kleine oppervlakte. Daardoor is de druk groot bij dezelfde kracht, zodat het mes makkelijk snijdt.'),
  ('sneeuwschoenen → grote oppervlakte → kleine druk → je zakt niet weg',
   'Omdat sneeuwschoenen een grote oppervlakte hebben, is de druk op de sneeuw klein. Daarom zak je niet weg.')],
 'cursus-druk-gassen.html': [
  ('temperatuur stijgt → deeltjes sneller → vaker en harder botsen → druk stijgt',
   'Als de temperatuur stijgt, bewegen de deeltjes sneller. Daardoor botsen ze vaker en harder tegen de wand, zodat de druk stijgt.'),
  ('lucht onder zuignap weg → onderdruk → buitenlucht drukt zuignap vast',
   'Onder de zuignap is de lucht weggeduwd, dus daar is er onderdruk. De lucht buiten oefent daardoor een grotere kracht uit en drukt de zuignap vast.')],
 'cursus-druk-vloeistoffen.html': [
  ('dieper → meer water erboven → grotere hydrostatische druk',
   'Hoe dieper je komt, hoe meer water er boven je is. Daardoor is de hydrostatische druk groter.'),
  ('kleine kracht op kleine zuiger → druk overal gelijk (Pascal) → grote kracht op grote zuiger',
   'Je oefent een kleine kracht uit op de kleine zuiger. Omdat de druk volgens Pascal overal even groot is, ontstaat er een grote kracht op de grote zuiger.')],
 'cursus-archimedes.html': [
  ('ondervlak dieper → grotere druk onder dan boven → kracht naar boven',
   'Het ondervlak ligt dieper dan het bovenvlak. Daardoor is de druk onderaan groter, zodat er een kracht naar boven overblijft: de archimedeskracht.'),
  ('zwemblaas groter → volume groter → archimedeskracht groter → vis stijgt',
   'Als de vis zijn zwemblaas groter maakt, wordt zijn volume groter. Daardoor wordt de archimedeskracht groter dan de zwaartekracht, dus de vis stijgt.')],
 'cursus-energie-systemen.html': [
  ('overschot stroom → water omhoog pompen → elektrische energie wordt potentiële energie',
   'Als er een overschot aan stroom is, pompt de centrale water omhoog. Zo wordt de elektrische energie opgeslagen als gravitationele potentiële energie.'),
  ('snelheid × 2 → kinetische energie × 4 → langere remweg',
   'Als de snelheid 2 keer zo groot wordt, wordt de kinetische energie 4 keer zo groot. Daarom is de remweg veel langer.')],
 'cursus-arbeid-vermogen.html': [
  ('kracht loodrecht op verplaatsing → cos 90° = 0 → geen arbeid',
   'Als de kracht loodrecht op de verplaatsing staat, is cos 90° gelijk aan nul. Daardoor levert de kracht geen arbeid.'),
  ('groter vermogen → meer joule per seconde → sneller klaar',
   'Een toestel met een groter vermogen zet meer joule per seconde om. Daardoor is het sneller klaar met dezelfde hoeveelheid energie.')],
}
