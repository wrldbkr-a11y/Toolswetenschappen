# Biologie 3de jaar · Thema 3 · Hoofdstuk 3 (reactie door klieren) en 4 (reactie bij andere organismen), nieuw formaat.
# Wordt uitgevoerd aan het einde van bio3_nieuw.py (zelfde naamruimte: pagina, kader, oef, D-structuur ...).
# Figuren: het schema exocrien/endocrien (_bron/figuren/klieren_schema.py, eigen tekening) en de figuren uit de tool biologie-klieren.html
# (biofig/klieren/figuren.json: huid met zweetklier, speekselklieren, hormoonklieren, kikker, banaan).
import json
sys.path.insert(0, '/home/claude/toolswetenschappen/_bron/figuren')
from klieren_schema import figuur as klierschema
KF = json.load(open('/home/claude/toolswetenschappen/_bron/cursus/biofig/klieren/figuren.json', encoding='utf-8'))
figuur, ttabel, vk, oef_fig = g['figuur'], g['ttabel'], g['vk'], g['oef_fig']
def kf(naam, breed=560):
    s = KF[naam]
    return re.sub(r'<svg\b', f'<svg style="width:100%;max-width:{breed}px;height:auto"', s, count=1)
def schema(labels=True, pijlen=True):
    return klierschema(labels, pijlen).replace('width="760" xmlns', 'style="width:100%;max-width:760px;height:auto" xmlns')
KTOOL = 'biologie-klieren.html'

def Dk(idee, vb, test, wb, letop=None):
    return dict(idee=idee, vb=vb, test=test, wb=wb, letop=letop, stappen=None, steun=None)

k_doelen = ['het verschil uitleggen tussen <b>excretie</b>- en <b>secretieproducten</b>;',
            'uitleggen welke <b>kliertypes</b> bij de mens voorkomen: <b>exocriene</b> en <b>endocriene</b> klieren;',
            'twee voorbeelden geven van <b>exocriene klieren</b>, hun klierafscheiding en hun functie;',
            'twee voorbeelden geven van <b>endocriene klieren</b>, hun hormoon en hun functie;',
            'uitleggen hoe ook <b>dieren</b> (kikker: metamorfose) en <b>planten</b> (banaan: ethyleen) met hormonen reageren.']
k_vk = vk('<b>Effectoren</b>: spieren en klieren voeren een reactie uit (hoofdstuk 1).',
          'Het schema <b>prikkel → receptor → verwerking → effector → effect</b>.',
          '<b>Homeostase</b>: je lichaam houdt bv. de temperatuur constant (thema 1).',
          'Het <b>bloed</b> stroomt door het hele lichaam: via de <b>slagaders</b> van het hart weg, via de <b>aders</b> terug.')

k1 = f'''<p>Je lichaam geeft veel stoffen af. Sommige zijn <b>afval</b>, andere hebben een <b>taak</b>.</p>
{ttabel(['', 'Excretie', 'Secretie'], [
  ['wat?', 'het lichaam verwijdert <b>afvalstoffen</b> die het niet meer kan gebruiken', '<b>kliercellen</b> maken stoffen <b>met een functie</b> en geven die af'],
  ['voorbeelden', 'urine (via de nieren), koolstofdioxide (via de longen)', 'speeksel, traanvocht, zweet, hormonen']])}
{kader('Definitie', '<p>Een <b>klier</b> is een orgaan of een groep cellen die stoffen maakt en afgeeft. Die stof heet een <b>klierafscheiding</b> of <b>secreet</b>.</p>')}
{tool(KTOOL + '#lesA', 'Bekijk excretie en secretie in de tool')}'''

k2 = f'''<p>Er zijn twee soorten klieren. Het verschil: <b>waar</b> gaat de klierafscheiding naartoe?</p>
{figuur(schema(), 'Volg de blauwe pijlen. Bij een exocriene klier gaat de afscheiding via de afvoerbuis naar buiten. Bij een endocriene klier gaat ze naar het bloed.')}
{kader('Exocriene klier', '<p>Heeft een <b>afvoerbuis</b>. De klierafscheiding gaat via de afvoerbuis naar <b>buiten het lichaam</b> (huid) of naar een <b>holte</b> (mond, darm).</p>')}
{kader('Endocriene klier (hormoonklier)', '<p>Heeft <b>geen afvoerbuis</b>. De klier geeft <b>hormonen</b> af aan het <b>bloed</b>. Het bloed brengt ze naar de <b>doelorganen</b>.</p>')}
<p>Ezelsbruggetje: <b>exo</b> = naar buiten (zoals een <b>exit</b>), <b>endo</b> = naar binnen, in het bloed.</p>
{tool(KTOOL + '#lesA', 'Bekijk klierweefsel onder de microscoop in de tool')}'''

k3 = f'''<h3>De zweetklieren</h3>
<p>Een zweetklier is een opgerolde buis diep in de lederhuid. Een lange <b>afvoerbuis</b> brengt het zweet naar een <b>zweetporie</b> op je huid. Het zweet verdampt. Daarvoor is warmte nodig, die uit je huid komt. Zo <b>koel je af</b>.</p>
{figuur(kf('huid', 520), 'Doorsnede van de huid met een zweetklier en een talgklier.')}
<h3>De speekselklieren</h3>
<p>Je hebt drie paar grote speekselklieren. Hun afvoerbuizen monden uit in je <b>mondholte</b>.</p>
{figuur(kf('speeksel', 420), 'De drie paar speekselklieren.')}
{ttabel(['Exocriene klier', 'Klierafscheiding', 'Functie'], [
  ['speekselklier', 'speeksel', 'maakt voedsel nat en glad, en begint met de vertering van zetmeel'],
  ['zweetklier', 'zweet', 'koelt het lichaam af als het zweet verdampt'],
  ['traanklier', 'traanvocht', 'houdt het oog vochtig en spoelt vuil weg'],
  ['talgklier', 'talg (huidvet)', 'houdt huid en haar soepel'],
  ['melkklier', 'moedermelk', 'voeding voor een baby']])}
{tool(KTOOL + '#lesB', 'Oefen met de exocriene klieren in de tool')}'''

k4 = f'''<p>Hormoonklieren liggen verspreid over het hele lichaam. Ze hebben geen afvoerbuis: hun <b>hormonen</b> gaan in het bloed.</p>
{figuur(kf('hormoon', 420), 'De belangrijkste hormoonklieren.')}
{kader('Hormoon', '<p>Een <b>hormoon</b> is een stof die een endocriene klier aan het bloed afgeeft. Het werkt alleen op bepaalde <b>doelorganen</b>. Al is er heel weinig van, toch heeft het een groot effect.</p>')}
{ttabel(['Endocriene klier', 'Hormoon', 'Functie'], [
  ['hypofyse', 'groeihormoon, en hormonen die andere hormoonklieren aansturen', 'de "baas" van veel hormoonklieren; regelt de groei'],
  ['schildklier', 'thyroxine', 'regelt hoe snel je stofwisseling werkt en helpt bij de groei'],
  ['bijnier', 'adrenaline', 'maakt je lichaam klaar voor actie bij schrik of stress'],
  ['alvleesklier', 'insuline en glucagon', 'regelt de hoeveelheid suiker in je bloed'],
  ['eierstok / teelbal', 'oestrogeen / testosteron', 'vrouwelijke / mannelijke geslachtskenmerken']])}
<p>De <b>alvleesklier</b> is bijzonder: ze is ook een <b>exocriene</b> klier. Via een afvoerbuis brengt ze alvleessap naar de darm, voor de vertering.</p>
{tool(KTOOL + '#lesC', 'Klik de hormoonklieren aan in de tool')}'''

k5 = f'''<h3>Dieren: de kikker</h3>
<p>Een kikkervisje leeft in het water, ademt met kieuwen en heeft een staart. Als zijn <b>schildklier</b> het hormoon <b>thyroxine</b> afgeeft, verandert het lichaam: er groeien poten, de staart verdwijnt en er komen longen. Die verandering heet <b>metamorfose</b>. Zonder thyroxine blijft het een kikkervisje.</p>
{figuur(kf('kikker', 640), 'Van kikkervisje tot kikker: de metamorfose wordt gestuurd door thyroxine.')}
<h3>Planten: de banaan</h3>
<p>Planten hebben geen klieren, maar hun cellen maken wel <b>plantenhormonen</b>. Een rijpe banaan geeft het gas <b>ethyleen</b> af. Dat is een rijpingshormoon: het laat vruchten in de buurt sneller rijpen.</p>
{figuur(kf('banaan', 560), 'Groene bananen rijpen sneller in een zak met een rijpe banaan.')}
{tool(KTOOL + '#lesD', 'Bekijk de kikker en de bananen in de tool')}'''

oefs_k = f'''{oef('opl_1', 1, 'Excretie of secretie?', 'Is het excretie of secretie? Leg kort uit.<ol class="deelvragen" type="a"><li>urine</li><li>speeksel</li><li>koolstofdioxide die je uitademt</li><li>insuline</li><li>traanvocht</li></ol>', [
  ('a', 'excretie: afvalstof'), ('b', 'secretie: helpt bij de vertering'), ('c', 'excretie: afvalstof van de verbranding'), ('d', 'secretie: een hormoon met een taak'), ('e', 'secretie: houdt het oog vochtig')],
  'Afval = excretie. Stof met een functie uit kliercellen = secretie.')}
{oef_fig('opl_2', 2, 'Klieren benoemen', 'Schrijf bij elk nummer de juiste naam.', schema(False, False), [
  ('1', 'afvoerbuis'), ('2 en 5', 'kliercellen'), ('3 en 6', 'slagader'), ('4 en 7', 'ader')], 'De linkse klier heeft een afvoerbuis: exocrien. De rechtse niet: endocrien.', schema(True, False))}
{oef_fig('opl_3', 3, 'Tekenen: de weg van de stoffen', 'Teken met pijlen op de figuur hoe de stoffen bewegen: uit het bloed in de klier, en uit de klier weer weg. Teken het bij beide klieren.', schema(False, False), [
  ('Exocrien', 'pijlen uit de bloedvaten naar de kliercellen, dan naar de holte en door de afvoerbuis naar buiten'),
  ('Endocrien', 'een pijl uit de slagader in de klier, en een pijl uit de klier naar de ader: de hormonen gaan in het bloed')], 'Exocrien: naar buiten. Endocrien: naar het bloed.', schema(True, True))}
{oef('opl_4', 4, 'Exocriene klieren', 'Geef bij elke klier de klierafscheiding en de functie.<ol class="deelvragen" type="a"><li>speekselklier</li><li>zweetklier</li><li>traanklier</li></ol>', [
  ('a', 'speeksel: voedsel nat en glad maken, vertering van zetmeel beginnen'), ('b', 'zweet: afkoelen als het verdampt'), ('c', 'traanvocht: oog vochtig houden, vuil wegspoelen')], '')}
{oef('opl_5', 5, 'Endocriene klieren', 'Welke klier maakt het hormoon, en wat doet het?<ol class="deelvragen" type="a"><li>adrenaline</li><li>insuline</li><li>thyroxine</li></ol>', [
  ('a', 'bijnier: maakt je lichaam klaar voor actie bij schrik'), ('b', 'alvleesklier: regelt de suiker in je bloed'), ('c', 'schildklier: regelt de snelheid van de stofwisseling en de groei')], '')}
{oef('opl_6', 6, 'Exocrien of endocrien?', 'Exocrien of endocrien? Waarom?<ol class="deelvragen" type="a"><li>een talgklier</li><li>de hypofyse</li><li>een melkklier</li><li>de schildklier</li></ol>', [
  ('a', 'exocrien: talg gaat via een afvoerbuis naar de huid'), ('b', 'endocrien: hormonen in het bloed'), ('c', 'exocrien: melk gaat via afvoerbuizen naar buiten'), ('d', 'endocrien: thyroxine in het bloed')],
  'Afvoerbuis naar buiten of naar een holte: exocrien. Hormonen in het bloed: endocrien.')}
{oef('opl_7', 7, 'Dieren en planten', '<ol class="deelvragen" type="a"><li>Wat gebeurt er met een kikkervisje als het geen thyroxine kan maken?</li><li>Je wil groene bananen sneller laten rijpen. Wat doe je, en waarom werkt het?</li></ol>', [
  ('a', 'Het blijft een kikkervisje: zonder thyroxine is er geen metamorfose.'), ('b', 'Leg ze in een zak met een rijpe banaan. Die geeft ethyleen af, een rijpingshormoon.')], '')}'''

k_sam = '''<p><b>Excretie</b>: afvalstoffen verwijderen (urine, CO₂). <b>Secretie</b>: kliercellen maken stoffen met een functie (speeksel, traanvocht, hormonen).</p>
<p><b>Exocriene klier</b>: met afvoerbuis, naar buiten of naar een holte (speeksel-, zweet-, traan-, talg-, melkklier). <b>Endocriene klier</b>: zonder afvoerbuis, hormonen in het bloed (hypofyse, schildklier, bijnier, alvleesklier, eierstok, teelbal).</p>
<p>Een <b>hormoon</b> werkt alleen op zijn <b>doelorganen</b>; weinig hormoon, groot effect. De alvleesklier is exocrien én endocrien.</p>
<p><b>Dieren</b>: thyroxine stuurt de metamorfose van de kikker. <b>Planten</b>: het gas ethyleen laat vruchten rijpen.</p>'''

C['klier'] = dict(delen=[
 Dk('Je lichaam geeft afval af (excretie) en stoffen met een taak (secretie). Stoffen met een taak worden gemaakt door klieren.',
   ('Zweet: afval of niet?', 'Na het sporten zweet je. Is zweet een excretie- of een secretieproduct?',
    [('Wie maakt het?', 'de zweetklieren: kliercellen. <i>Waarom belangrijk?</i> Stoffen uit kliercellen zijn secretieproducten.'),
     ('Heeft het een taak?', 'ja: het zweet verdampt en koelt je af.'),
     ('Besluit', 'zweet is een secretieproduct. Urine en CO₂ zijn afval: excretie.')]),
   [('Waarom is urine een excretieproduct en speeksel een secretieproduct?', 'Urine bevat afvalstoffen die het lichaam verwijdert. Speeksel wordt door klieren gemaakt en heeft een taak: helpen bij de vertering.'),
    ('Wat is een klier?', 'Een orgaan of een groep cellen die stoffen maakt en afgeeft.')],
   ([('Noem iets dat je lichaam afgeeft.', 'zweet, urine, speeksel, tranen …')],
    [('CO₂ uitademen: excretie of secretie?', 'excretie', 'secretie'), ('Traanvocht?', 'secretie')],
    [('Wat maakt een klier?', 'een klierafscheiding (secreet)')])),
 Dk('Een exocriene klier heeft een afvoerbuis naar buiten of naar een holte. Een endocriene klier heeft geen afvoerbuis en geeft hormonen af aan het bloed.',
   ('Welke soort?', 'De traanklier brengt traanvocht via buisjes naar je oog. Is het een exocriene of een endocriene klier?',
    [('Afvoerbuis?', 'ja, de traanbuisjes. <i>Waarom belangrijk?</i> Een afvoerbuis betekent exocrien.'),
     ('Waar gaat het naartoe?', 'naar het oppervlak van je oog: naar buiten, niet in het bloed.'),
     ('Besluit', 'exocriene klier.')]),
   [('Hoe komt een hormoon bij zijn doelorgaan, als de klier geen afvoerbuis heeft?', 'De klier geeft het hormoon af aan het bloed. Het bloed brengt het overal naartoe.'),
    ('Wat is het verschil tussen een exocriene en een endocriene klier?', 'Exocrien: met afvoerbuis, naar buiten of naar een holte. Endocrien: zonder afvoerbuis, hormonen in het bloed.')],
   ([('Waardoor stroomt je bloed?', 'bloedvaten: slagaders en aders')],
    [('Klier met afvoerbuis?', 'exocrien', 'endocrien'), ('Hormonen gaan naar …', 'het bloed', 'een afvoerbuis')],
    [('Exo betekent …', 'naar buiten')]),
   'Een endocriene klier heeft <b>geen</b> afvoerbuis. Schrijf niet "de hormonen gaan via een buis naar het orgaan".'),
 Dk('Exocriene klieren brengen hun afscheiding naar buiten of naar een holte. Elke afscheiding heeft een eigen taak.',
   ('De speekselklieren', 'Leg uit waarom de speekselklieren exocriene klieren zijn, en wat speeksel doet.',
    [('Afvoerbuis', 'hun afvoerbuizen monden uit in de mondholte. <i>Waarom belangrijk?</i> Dat maakt ze exocrien.'),
     ('Afscheiding', 'speeksel.'),
     ('Functie', 'het maakt voedsel nat en glad en begint de vertering van zetmeel.')]),
   [('Hoe koelt zweet je af?', 'Het zweet verdampt op je huid. Daarvoor is warmte nodig, die uit je huid komt.'),
    ('Geef twee exocriene klieren met hun afscheiding en functie.', 'Bv. speekselklier: speeksel, voedsel nat maken en zetmeel verteren. Traanklier: traanvocht, oog vochtig houden.')],
   ([('Waarom krijg je een droge mond als je zenuwachtig bent?', 'je maakt minder speeksel')],
    [('Klier die talg maakt?', 'talgklier'), ('Waar monden speekselklieren uit?', 'in de mondholte', 'in het bloed')],
    [('Taak van traanvocht?', 'oog vochtig houden, vuil wegspoelen')])),
 Dk('Hormoonklieren geven hormonen af aan het bloed. Een hormoon werkt alleen op zijn doelorganen, maar heeft een groot effect.',
   ('Schrik!', 'Je schrikt van een hond. Je hart gaat sneller kloppen. Hoe zorgt je lichaam daarvoor?',
    [('Klier', 'de bijnier maakt adrenaline. <i>Waarom die?</i> Adrenaline maakt je lichaam klaar voor actie.'),
     ('Transport', 'de adrenaline gaat in het bloed, want de bijnier is een endocriene klier.'),
     ('Effect', 'bij het hart (een doelorgaan) gaat het hart sneller kloppen.')]),
   [('Waarom reageert niet elk orgaan op elk hormoon?', 'Een hormoon werkt alleen op zijn doelorganen.'),
    ('Waarom is de alvleesklier zowel exocrien als endocrien?', 'Ze maakt alvleessap dat via een afvoerbuis naar de darm gaat (exocrien), en insuline die in het bloed gaat (endocrien).')],
   ([('Waar ligt je schildklier?', 'in je hals')],
    [('Klier die adrenaline maakt?', 'de bijnier', 'de schildklier'), ('Insuline regelt …', 'de suiker in je bloed')],
    [('Wat is een doelorgaan?', 'een orgaan waarop een hormoon werkt')])),
 Dk('Ook dieren en planten reageren met hormonen. Bij de kikker stuurt thyroxine de metamorfose; bij planten laat ethyleen vruchten rijpen.',
   ('Rijpe en groene bananen', 'Je legt groene bananen in een zak, samen met één rijpe banaan. Na twee dagen zijn ze geel. Verklaar.',
    [('Wat geeft de rijpe banaan af?', 'het gas ethyleen. <i>Waarom belangrijk?</i> Ethyleen is een plantenhormoon.'),
     ('Effect', 'ethyleen laat vruchten in de buurt sneller rijpen.'),
     ('Waarom een zak?', 'zo blijft het gas bij de bananen.')]),
   [('Waarom blijft een kikkervisje zonder thyroxine een kikkervisje?', 'Thyroxine van de schildklier stuurt de metamorfose: poten, longen, de staart verdwijnt. Zonder dat hormoon gebeurt dat niet.'),
    ('Hebben planten klieren? Hoe maken ze dan hormonen?', 'Nee. Hun cellen maken plantenhormonen, zoals ethyleen.')],
   ([('Hoe ademt een kikkervisje?', 'met kieuwen')],
    [('Hormoon voor de metamorfose?', 'thyroxine', 'ethyleen'), ('Ethyleen is een …', 'gas, een plantenhormoon')],
    [('Wat is metamorfose?', 'een grote verandering van het lichaam, bv. van kikkervisje tot kikker')]))],
 uitd=[('Uitdaging · Twee klieren in één', 'De alvleesklier maakt alvleessap en insuline. Teken een schema van de alvleesklier met een exocrien en een endocrien deel. Duid met pijlen aan waar elke stof naartoe gaat.',
        [('Exocrien deel', 'kliercellen rond een holte, met een afvoerbuis naar de darm: alvleessap voor de vertering.'),
         ('Endocrien deel', 'groepjes kliercellen zonder afvoerbuis: insuline gaat in het bloed.'),
         ('Pijlen', 'alvleessap → afvoerbuis → darm; insuline → bloed → doelorganen (bv. lever, spieren).')],
        'Eén orgaan, twee soorten kliercellen.',
        'Bekijk eerst het schema van de exocriene en de endocriene klier. Teken beide delen in één figuur en zet bij elke pijl de naam van de stof.'),
       ('Uitdaging · Zweten en homeostase', 'Bij warm weer zweet je meer. Leg met het schema prikkel → receptor → verwerking → effector → effect uit hoe je lichaam je temperatuur constant houdt. Is dit negatieve of positieve feedback?',
        [('Prikkel en receptor', 'de temperatuur stijgt; warmtereceptoren vangen dat op.'), ('Effector', 'de zweetklieren (exocrien) maken meer zweet.'),
         ('Effect', 'het zweet verdampt en koelt je af: de temperatuur daalt weer. De reactie werkt de verandering tegen: negatieve feedback.')],
        'Zweten is negatieve feedback.', 'Gebruik thema 1 en thema 3.'),
       ('Uitdaging · Een proef met bananen', 'Ontwerp een proef om te bewijzen dat een rijpe banaan andere bananen sneller laat rijpen. Wat verander je, wat hou je gelijk, en wat meet je?',
        [('Veranderen', 'zak A: groene bananen + een rijpe banaan; zak B: alleen groene bananen.'), ('Gelijk houden', 'evenveel groene bananen, dezelfde temperatuur, dezelfde soort zak, even lang.'),
         ('Meten', 'elke dag de kleur van de groene bananen vergelijken.')],
        'Zijn de bananen in zak A eerder geel, dan versnelt de rijpe banaan het rijpen (door ethyleen).', None)],
 begrip=[('excretie', 'afvalstoffen uit het lichaam verwijderen'), ('secretie', 'kliercellen maken stoffen met een functie en geven ze af'), ('klier', 'orgaan of groep cellen die stoffen maakt en afgeeft'),
         ('klierafscheiding (secreet)', 'de stof die een klier afgeeft'), ('exocriene klier', 'klier met afvoerbuis, naar buiten of naar een holte'), ('endocriene klier (hormoonklier)', 'klier zonder afvoerbuis, geeft hormonen af aan het bloed'),
         ('afvoerbuis', 'buis die de klierafscheiding wegvoert'), ('hormoon', 'stof van een endocriene klier, werkt via het bloed op doelorganen'), ('doelorgaan', 'orgaan waarop een hormoon werkt'),
         ('metamorfose', 'grote verandering van het lichaam, bv. kikkervisje wordt kikker'), ('thyroxine', 'hormoon van de schildklier'), ('ethyleen', 'plantenhormoon (gas) dat vruchten laat rijpen')])

k_oefs = g['oefblok'](g['hernummer'](oefs_k), (KTOOL + '#lesE', 'Oefen alle lesdoelen in de tool'))
pagina('cursus-klieren.html', T3 + '3 en 4', 'Reactie door klieren en bij andere organismen',
       f'Werk dit hoofdstuk samen met de tool <a href="{KTOOL}">Klieren en hormonen</a>. Oefeningen maak je op papier. De oplossingen staan online, zodra ze in de les besproken zijn.',
       LD(k_doelen), k_vk, [('Excretie of secretie', k1), ('Soorten klieren', k2), ('Exocriene klieren', k3), ('Endocriene klieren', k4), ('Reactie bij andere organismen', k5)],
       k_oefs, SAM(k_sam), C['klier'])
