# Cursus chemie 3de jaar (3NW) · Thema 1 Van mengsels tot zuivere stoffen · Thema 2 De atoombouw en het PSE
import json, math
_src = open('/home/claude/cursus/optica_cursus.py', encoding='utf-8').read()
exec(_src.split('# ================================================================ H1')[0])   # helpers + maak()

TECH = json.load(open('/home/claude/cursus/chemfig/tech.json'))
EL = json.load(open('/home/claude/cursus/chemfig/el.json'))
GHS = json.load(open('/home/claude/cursus/chemfig/ghs.json'))
ELZ = {e['Z']: e for e in EL.values()}
import sys as _sys; _sys.path.insert(0, '/home/claude/cursus/chemfig')
from pse_fig import pse_svg
from modellen import fig_adsorberen, fig_extraheren
def figuur_liggend(svgcode, onderschrift=''):
    return f'<figure class="figuur liggend">{svgcode}<figcaption>{onderschrift}</figcaption></figure>'
MODEL = {'extraheren': (fig_extraheren, 'Deeltjesmodel: in een koffieboon zitten kleurstoffen, smaakstoffen en geurstoffen. In heet water lossen ze op: het extract. De gemalen koffie blijft over als residu.'),
         'adsorberen': (fig_adsorberen, 'Deeltjesmodel: kleur- en geurstoffen blijven kleven aan het oppervlak van de actieve kool (het adsorptiemiddel). De watermoleculen gaan er gewoon langs.')}

def oefblok(inhoud, toolref=None):
    s = f'''<p>Maak deze oefeningen <b>op papier</b>. Gebruik bij thema 2 je <b>PSE</b>. De oplossingen verschijnen hier nadat we de oefeningen in de les besproken hebben.</p>
<p><button class="knop licht" data-print="oef">🖨 Druk de oefeningen af</button></p>
{inhoud}'''
    return s + (tool(*toolref) if toolref else '')

def ttabel(kop, rijen):
    h = '<table class="vb grid"><tr>' + ''.join(f'<td><b>{k}</b></td>' for k in kop) + '</tr>'
    return h + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rijen) + '</table>'

T1 = 'Chemie 3de jaar · Thema 1 Van mengsels tot zuivere stoffen · Hoofdstuk '
T2 = 'Chemie 3de jaar · Thema 2 De atoombouw en het PSE · Hoofdstuk '

# ================================================================ figuren thema 1
def fig_fys_chem():
    o = t(160, 22, 'fysisch verschijnsel', BLAUW, size=15) + t(480, 22, 'chemisch verschijnsel', ROOD, size=15)
    # ijsblokje -> plasje water
    o += '<rect x="60" y="70" width="56" height="56" rx="8" fill="#e0f2fe" stroke="#60a5fa" stroke-width="2.5"/>'
    o += straal(130, 100, 180, 100, INK, 2.5)
    o += '<ellipse cx="240" cy="118" rx="48" ry="12" fill="#bfdbfe" stroke="#60a5fa" stroke-width="2"/>'
    o += t(88, 150, 'ijs', INK, size=13) + t(240, 150, 'water', INK, size=13)
    o += t(160, 185, 'nog altijd water: geen nieuwe stof', GRIJS, size=13, w=600)
    # papier -> as + rook
    o += '<rect x="380" y="74" width="46" height="58" fill="#fff" stroke="#475569" stroke-width="2"/>' + ''.join(lijn(387, y, 419, y, '#94a3b8', 1.2) for y in (86, 96, 106, 116))
    o += straal(440, 100, 490, 100, INK, 2.5)
    o += '<path d="M515,128 q20,-10 40,-2 q16,-6 30,2 z" fill="#4b5563"/>'
    o += ''.join(f'<circle cx="{545+dx}" cy="{y}" r="{r}" fill="#cbd5e1" opacity=".8"/>' for dx, y, r in ((0, 104, 9), (8, 84, 11), (-4, 62, 13)))
    o += t(403, 150, 'papier', INK, size=13) + t(550, 150, 'as en rook', INK, size=13)
    o += t(480, 185, 'nieuwe stoffen ontstaan', GRIJS, size=13, w=600)
    o += lijn(320, 40, 320, 190, '#e5e7eb', 2)
    return svg(o, 640, 200)

def ghs_svg(code, x, y, s=86, naam=None, nr=None):
    g = f'<g transform="translate({x},{y}) scale({s/100})"><polygon points="50,5 95,50 50,95 5,50" fill="#fff" stroke="#d6001c" stroke-width="6" stroke-linejoin="round"/><g fill="#111">{GHS[code]}</g></g>'
    if naam:
        w = naam.split(' ')
        if len(naam) > 14:
            h = len(w) // 2 if len(w) > 2 else 1
            g += t(x + s/2, y + s + 14, ' '.join(w[:h]), INK, size=12) + t(x + s/2, y + s + 28, ' '.join(w[h:]), INK, size=12)
        else: g += t(x + s/2, y + s + 14, naam, INK, size=12)
    if nr: g += f'<circle cx="{x+8}" cy="{y+10}" r="11" fill="{INK}"/>' + t(x + 8, y + 14.5, str(nr), '#fff', size=12)
    return g
GHSNAAM = ['ontplofbaar', 'ontvlambaar', 'oxiderend', 'gas onder druk', 'bijtend', 'giftig', 'schadelijk of irriterend', 'gevaar voor de gezondheid', 'gevaarlijk voor het milieu']
def fig_ghs(namen=True, volgorde=range(9)):
    o = ''
    for i, k in enumerate(volgorde):
        x, y = 22 + (i % 5) * 124, 10 + (i // 5) * 136
        o += ghs_svg(f'GHS0{k+1}', x, y, 86, GHSNAAM[k] if namen else None, None if namen else i + 1)
    return svg(o, 640, 278)

def fig_etiket():
    o = '<rect x="20" y="10" width="600" height="230" rx="10" fill="#fff" stroke="#475569" stroke-width="2"/>'
    o += t(40, 44, 'Buisvrij ontstopper', INK, 'start', 22, 800) + t(40, 66, 'bevat natriumhydroxide', GRIJS, 'start', 13, 600)
    o += ghs_svg('GHS05', 40, 82, 90)
    o += t(150, 110, 'GEVAAR', ROOD, 'start', 18, 800)
    for i, (c, z) in enumerate([('H290', 'Kan bijtend zijn voor metalen.'), ('H314', 'Veroorzaakt ernstige brandwonden en oogletsel.'),
                                ('P102', 'Buiten het bereik van kinderen houden.'), ('P280', 'Handschoenen en oogbescherming dragen.'),
                                ('P305+P351+P338', 'In de ogen: voorzichtig spoelen met water …')]):
        y = 140 + i * 20
        o += t(150, y, c, ROOD if c[0] == 'H' else BLAUW, 'start', 12, 800) + t(268, y, z, INK, 'start', 12, 500)
    return svg(o, 640, 250)

def deeltjes(cx, cy, w, h, soorten, n=26, gemengd=True, zaad=1, rand=True):
    """deeltjesmodel in een kader; soorten = lijst (kleur, aandeel); gemengd=False -> soorten in aparte gebieden"""
    import random
    r = random.Random(zaad); o = ''
    if rand: o += f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>'
    pts = []
    while len(pts) < n:
        x, y = cx - w/2 + 12 + r.random()*(w - 24), cy - h/2 + 12 + r.random()*(h - 24)
        if all((x-a)**2 + (y-b)**2 > 15**2 for a, b in pts): pts.append((x, y))
    tot = sum(a for _, a in soorten)
    if gemengd:
        kl = []
        for k, a in soorten: kl += [k] * round(n * a / tot)
        r.shuffle(kl)
        for (x, y), k in zip(pts, kl + [soorten[0][0]] * n): o += punt(x, y, k, 6)
    else:  # klonters: sorteer op x
        pts.sort(); i = 0
        for k, a in soorten:
            m = round(n * a / tot)
            for x, y in pts[i:i+m]: o += punt(x, y, k, 6)
            i += m
    return o

def fig_zuiver_mengsel():
    o = deeltjes(110, 95, 170, 130, [(BLAUW, 1)], zaad=3) + t(110, 185, 'zuivere stof', INK) + t(110, 202, 'één soort deeltjes', GRIJS, size=12, w=600)
    o += deeltjes(320, 95, 170, 130, [(BLAUW, 1), (ROOD, 1)], zaad=5) + t(320, 185, 'homogeen mengsel', INK) + t(320, 202, 'deeltjes overal goed verdeeld', GRIJS, size=12, w=600)
    o += deeltjes(530, 95, 170, 130, [(BLAUW, 1), (ROOD, 1)], gemengd=False, zaad=7) + t(530, 185, 'heterogeen mengsel', INK) + t(530, 202, 'klontjes van elke soort', GRIJS, size=12, w=600)
    return svg(o, 640, 215)

def fig_schema():
    def vak(x, y, s, k='#f1f5f9', w=150):
        return f'<rect x="{x-w/2}" y="{y-18}" width="{w}" height="36" rx="8" fill="{k}" stroke="#475569" stroke-width="1.5"/>' + t(x, y + 5, s, INK, size=14)
    o = vak(320, 30, 'materie', '#e2e8f0')
    o += lijn(320, 48, 170, 92, GRIJS, 1.5) + lijn(320, 48, 470, 92, GRIJS, 1.5)
    o += vak(170, 110, 'zuivere stof', '#dbeafe') + vak(470, 110, 'mengsel', '#fee2e2')
    o += lijn(470, 128, 380, 172, GRIJS, 1.5) + lijn(470, 128, 560, 172, GRIJS, 1.5)
    o += vak(380, 190, 'homogeen', '#fef3c7', 130) + vak(560, 190, 'heterogeen', '#fef3c7', 130)
    o += t(170, 150, '1 stof · vaste smelt- en', GRIJS, size=12, w=600) + t(170, 166, 'kooktemperatuur', GRIJS, size=12, w=600)
    o += t(380, 228, 'je ziet de bestanddelen niet,', GRIJS, size=12, w=600) + t(380, 244, 'ook niet met een microscoop', GRIJS, size=12, w=600)
    o += t(560, 228, 'je ziet de bestanddelen', GRIJS, size=12, w=600) + t(560, 244, '(met oog of microscoop)', GRIJS, size=12, w=600)
    return svg(o, 640, 255)

def tech_fig(k, soort='lab'):
    return TECH[k][soort]

# ================================================================ T1 H1 CHEMIE ALS WETENSCHAP
h1_doelen = ['beschrijven wat in de <b>chemie</b> bestudeerd wordt;',
             'het verschil uitleggen tussen een <b>fysisch</b> en een <b>chemisch verschijnsel</b>;',
             'de <b>gevarensymbolen</b> herkennen en benoemen;',
             '<b>H-zinnen</b> en <b>P-zinnen</b> op een etiket indelen als <b>gevaar</b> of <b>voorzorg</b>;',
             'producten in het <b>labo</b> en in het <b>dagelijks leven</b> op een <b>verantwoorde</b> manier gebruiken.']
h1_vk = vk('Alles rondom je bestaat uit <b>stoffen</b>: water, zout, ijzer, lucht …',
           'Een stof kan <b>vast</b>, <b>vloeibaar</b> of <b>gasvormig</b> zijn (aggregatietoestanden).',
           'In het labo volg je altijd de <b>veiligheidsregels</b>: labojas, veiligheidsbril, niet eten of drinken.')
h1_1 = f'''<p>Fysica en chemie zijn allebei <b>natuurwetenschappen</b>. Ze bestuderen <b>verschijnselen</b>: dingen die in de natuur gebeuren. Er is één groot verschil.</p>
{figuur(fig_fys_chem(), 'Links blijft het dezelfde stof, rechts ontstaan nieuwe stoffen.')}
{ttabel(['', 'Fysisch verschijnsel', 'Chemisch verschijnsel'], [
  ['Wat gebeurt er?', 'de stof blijft <b>dezelfde stof</b>', 'er ontstaat een <b>nieuwe stof</b>'],
  ['Voorbeelden', 'ijs smelt, water kookt, suiker lost op, glas breekt', 'papier verbrandt, ijzer roest, brood bakt, melk wordt zuur']])}
{kader('Vraag jezelf af: is er een nieuwe stof ontstaan?', '<p>Ja → chemie. Nee → fysica. Een nieuwe stof herken je vaak aan: <b>een andere kleur</b>, <b>een gas</b> (bubbels), <b>een nieuwe geur</b>, <b>licht of warmte</b>, of <b>het gaat niet meer terug</b>.</p>')}
{kader('Definitie', '<p><b>Chemie</b> is de wetenschap van de stoffen. Ze onderzoekt drie dingen van stoffen:</p><ul><li>hun <b>samenstelling</b>: uit welke deeltjes bestaat een stof?</li><li>hun <b>eigenschappen</b>: hoe herken je een stof?</li><li>hun <b>omzettingen</b>: hoe verandert een stof in een nieuwe stof?</li></ul>')}
{tool('chemie-stoffen.html', 'Bekijk de filmpjes over samenstelling, eigenschappen en omzettingen')}
{denk('denk_1', 'Je laat een fiets een hele winter buiten staan aan het Flageyplein. De ketting wordt bruin en ruw. Is dat fysica of chemie?', [
  ('Kijk naar de stof', 'Het glanzende ijzer verandert in een bruine, brokkelige stof: roest.'),
  ('Gaat het terug?', 'Nee, roest wordt niet vanzelf weer ijzer.'),
  ('Nieuwe stof?', 'Ja: een andere kleur en het gaat niet terug.')], 'Roesten is een chemisch verschijnsel: er ontstaat een nieuwe stof.')}
{denk('denk_2', 'Suiker lost op in je thee. Je ziet de suiker niet meer. Is er een nieuwe stof ontstaan?', [
  ('Proef het', 'De thee smaakt zoet: de suiker is er nog.'),
  ('Kan het terug?', 'Laat je het water verdampen, dan blijft de suiker over.')], 'Oplossen is een fysisch verschijnsel: de suiker blijft suiker.')}'''

h1_2 = f'''<p>Veel stoffen zijn gevaarlijk: in het labo, maar ook thuis (ontstopper, bleekwater, aanstekergas). Op de verpakking staat dan een <b>gevarensymbool</b>: een zwarte tekening in een <b>rode ruit</b> op een witte achtergrond.</p>
{figuur(fig_ghs(), 'De negen gevarensymbolen.')}
{ttabel(['Symbool', 'Betekenis', 'Voorbeeld'], [
  ['ontplofbaar', 'kan ontploffen door een schok, wrijving, vuur of warmte', 'vuurwerk'],
  ['ontvlambaar', 'vat heel gemakkelijk vlam', 'aceton, alcohol, aanstekergas, benzine'],
  ['oxiderend', 'helpt een brand: het vuur wordt groter', 'geconcentreerd waterstofperoxide'],
  ['gas onder druk', 'de fles kan ontploffen bij warmte', 'gasfles met propaan of CO₂'],
  ['bijtend', 'beschadigt huid en ogen ernstig, tast metalen aan', 'ontstopper, zoutzuur'],
  ['giftig', 'een kleine hoeveelheid kan al dodelijk zijn', 'methanol, rattengif'],
  ['schadelijk of irriterend', 'irriteert huid of ogen, minder erg dan giftig', 'sommige wasmiddelen'],
  ['gevaar voor de gezondheid', 'kan je op lange termijn ernstig ziek maken', 'benzine, terpentine'],
  ['gevaarlijk voor het milieu', 'giftig voor planten en dieren, vooral in water', 'bleekwater, insectengif']])}
<h3>H-zinnen en P-zinnen</h3>
<p>Op het etiket staan ook korte zinnen met een code.</p>
{ttabel(['Code', 'Komt van', 'Betekent', 'Voorbeeld'], [
  ['<b>H</b>-zin', '<i>hazard</i>', '<b>gevaar</b>: wat kan de stof doen?', 'H314: veroorzaakt ernstige brandwonden'],
  ['<b>P</b>-zin', '<i>precaution</i>', '<b>voorzorg</b>: wat moet jij doen?', 'P280: draag handschoenen en een veiligheidsbril']])}
{figuur(fig_etiket(), 'Het etiket van een ontstopper: symbool, signaalwoord, H-zinnen (rood) en P-zinnen (blauw).')}
{tool('chemie-stoffen.html#les12', 'Oefen met de gevarensymbolen en het etiket')}
{denk('denk_3', 'Op een fles staat: "H225 Licht ontvlambare vloeistof en damp" en "P210 Verwijderd houden van warmte en open vuur". Welke zin zegt wat jij moet doen? Welk gevarensymbool verwacht je?', [
  ('H225', 'Een H-zin: dat is het gevaar (de stof vat gemakkelijk vlam).'),
  ('P210', 'Een P-zin: dat is de voorzorg, wat jij moet doen.'),
  ('Symbool', 'Gemakkelijk vlam vatten: het symbool met de vlam.')], 'P210 zegt wat jij moet doen. Je verwacht het symbool ontvlambaar.')}'''

h1_3 = f'''<p>Je kent nu de symbolen. Maar hoe gebruik je gevaarlijke producten <b>veilig</b>?</p>
{ttabel(['In het labo', 'Thuis'], [
  ['Draag een <b>labojas</b> en een <b>veiligheidsbril</b>; bind lange haren samen.', 'Lees altijd eerst het <b>etiket</b>: symbool, H-zinnen en P-zinnen.'],
  ['Eet en drink nooit in het labo. Ruik niet rechtstreeks aan een fles: <b>waaier</b> de geur naar je toe.', '<b>Meng nooit</b> schoonmaakproducten. Bleekwater met een ontkalker of een zuur product geeft een giftig gas (chloorgas).'],
  ['Giet een stof nooit terug in de voorraadfles. Werk met kleine hoeveelheden.', 'Bewaar producten in de <b>originele verpakking</b>, nooit in een drankfles.'],
  ['Gooi resten niet zomaar in de gootsteen: volg de afspraken van je leerkracht.', 'Bewaar ze <b>buiten het bereik van kinderen</b>. Breng resten naar het containerpark (Recypark van Net Brussel).'],
  ['Meld elk ongeval meteen. Spat er iets in je ogen: <b>spoelen met water</b>, minstens 15 minuten.', 'Gebruik niet meer dan nodig: dat is beter voor jou én voor het milieu.']])}
{kader('Onthoud', '<p>Veilig werken = <b>etiket lezen</b>, je <b>beschermen</b> (bril, handschoenen), <b>nooit mengen</b>, <b>juist bewaren</b> en <b>juist weggooien</b>.</p>')}
{denk('denk_4', 'Iemand wil de badkamer extra proper maken en giet bleekwater en een ontkalker samen in een emmer. Wat zeg je?', [
  ('Gevaar', 'Bleekwater en een zuur product (zoals een ontkalker) vormen samen een giftig gas.'),
  ('Wat doen?', 'Nooit mengen. Eén product per keer gebruiken, goed spoelen en verluchten.')], 'Schoonmaakproducten meng je nooit.')}'''

h1_oef = f'''{oef('opl_1', 1, 'Fysisch of chemisch?', 'Is het een fysisch of een chemisch verschijnsel?<ol class="deelvragen" type="a"><li>Een kaars brandt.</li><li>Kaarsvet smelt.</li><li>Een appel wordt bruin als je hem doorsnijdt.</li><li>Water bevriest in de vriezer.</li><li>Een bruistablet in water geeft bubbels.</li><li>Je maalt koffiebonen tot poeder.</li></ol>', [
  ('a', 'chemisch: er ontstaan rook en gassen, licht en warmte'), ('b', 'fysisch: vast wordt vloeibaar, nog altijd kaarsvet'), ('c', 'chemisch: andere kleur, gaat niet terug'),
  ('d', 'fysisch: water wordt ijs'), ('e', 'chemisch: er ontstaat een gas'), ('f', 'fysisch: kleinere stukjes van dezelfde stof')], 'Nieuwe stof → chemisch; dezelfde stof → fysisch.')}
{oef('opl_2', 2, 'Wat onderzoekt de chemie?', 'Gaat de onderzoeksvraag over de <b>samenstelling</b>, de <b>eigenschappen</b> of de <b>omzettingen</b> van een stof?<ol class="deelvragen" type="a"><li>Bij welke temperatuur kookt alcohol?</li><li>Uit welke deeltjes bestaat water?</li><li>Wat ontstaat er als je aardgas verbrandt?</li><li>Lost zout op in water?</li></ol>', [
  ('a', 'eigenschappen'), ('b', 'samenstelling'), ('c', 'omzettingen'), ('d', 'eigenschappen')], 'Samenstelling = deeltjes · eigenschappen = herkennen · omzettingen = nieuwe stof.')}
{oef_fig('opl_3', 3, 'Gevarensymbolen benoemen', 'Noteer de naam van elk gevarensymbool.', fig_ghs(False, [4, 1, 5, 8, 6, 0, 3, 7, 2]), [
  ('1–3', 'bijtend · ontvlambaar · giftig'), ('4–6', 'gevaarlijk voor het milieu · schadelijk of irriterend · ontplofbaar'), ('7–9', 'gas onder druk · gevaar voor de gezondheid · oxiderend')],
  'Kijk naar de tekening in de rode ruit.', fig_ghs(True, [4, 1, 5, 8, 6, 0, 3, 7, 2]))}
{oef('opl_4', 4, 'Welk symbool hoort erbij?', 'Welk gevarensymbool verwacht je op de verpakking?<ol class="deelvragen" type="a"><li>een spuitbus met haarlak</li><li>gootsteenontstopper</li><li>een fles met benzine</li><li>insectengif dat in het water niet mag komen</li></ol>', [
  ('a', 'ontvlambaar (en gas onder druk)'), ('b', 'bijtend'), ('c', 'ontvlambaar, gevaar voor de gezondheid'), ('d', 'gevaarlijk voor het milieu')], 'Denk na wat de stof kan doen.')}
{oef('opl_5', 5, 'H of P?', 'Is het een H-zin (gevaar) of een P-zin (voorzorg)?<ol class="deelvragen" type="a"><li>Veroorzaakt ernstige oogirritatie.</li><li>Na het werken handen grondig wassen.</li><li>Giftig bij inslikken.</li><li>Niet roken.</li><li>Zeer giftig voor in het water levende organismen.</li></ol>', [
  ('a', 'H'), ('b', 'P'), ('c', 'H'), ('d', 'P'), ('e', 'H')], 'Zegt de zin wat de stof doet (H) of wat jij moet doen (P)?')}
{oef('opl_6', 6, 'Redeneren: veilig in het labo', 'Op een fles in het labo staat het symbool <b>bijtend</b>. Je klasgenoot wil de stof zonder bril overgieten. Wat zeg je? Noteer twee voorzorgen.', [
  ('Gevaar', 'Een bijtende stof beschadigt je ogen en huid ernstig.'), ('Voorzorg', 'Draag een veiligheidsbril en handschoenen; giet langzaam boven de tafel, niet boven ooghoogte.')],
  'Bijtend → altijd bril en handschoenen.')}
{oef('opl_7', 7, 'Verantwoord gebruiken', 'Wat is er fout? Schrijf wat je wel moet doen.<ol class="deelvragen" type="a"><li>Een leerling ruikt rechtstreeks aan een fles azijnzuur.</li><li>Thuis wordt ontstopper bewaard in een oude limonadefles.</li><li>Een rest verf wordt in de gootsteen gegoten.</li><li>Iemand mengt twee wc-reinigers om sneller te poetsen.</li></ol>', [
  ('a', 'De geur met je hand naar je toe waaieren.'), ('b', 'In de originele verpakking bewaren, met het etiket, buiten het bereik van kinderen.'), ('c', 'Naar het containerpark brengen.'), ('d', 'Nooit mengen: er kan een giftig gas ontstaan.')],
  'Etiket lezen, beschermen, niet mengen, juist bewaren, juist weggooien.')}'''
h1_samenv = '''<p><b>Fysisch verschijnsel</b>: dezelfde stof blijft. <b>Chemisch verschijnsel</b>: er ontstaat een nieuwe stof (kleur, gas, geur, licht/warmte, niet terug).</p>
<p><b>Chemie</b> = de wetenschap van de stoffen: samenstelling, eigenschappen, omzettingen.</p>
<p><b>Gevarensymbolen</b>: zwarte tekening in een rode ruit (9 soorten). <b>H-zin</b> = gevaar (hazard). <b>P-zin</b> = voorzorg (precaution).</p>
<p><b>Verantwoord gebruiken</b>: etiket lezen, je beschermen, nooit mengen, in de originele verpakking bewaren, resten naar het containerpark.</p>'''

# ================================================================ T1 H2 ZUIVERE STOFFEN EN MENGSELS
h2_doelen = ['de begrippen <b>zuivere stof</b>, <b>bestanddeel</b> en <b>mengsel</b> onderscheiden;',
             'uitleggen waarom een mengsel <b>homogeen</b> of <b>heterogeen</b> is;',
             'de soorten mengsels onderscheiden op basis van de <b>aggregatietoestand</b> van hun bestanddelen;',
             'beschrijven wat een <b>stofeigenschap</b> is en voorbeelden noteren;',
             'het onderscheid maken tussen een <b>stofeigenschap</b> en een <b>voorwerpseigenschap</b>.']
h2_vk = vk('Het <b>deeltjesmodel</b>: elke stof bestaat uit heel kleine deeltjes.', 'De drie <b>aggregatietoestanden</b>: vast, vloeibaar, gas.', 'Fysisch en chemisch verschijnsel (hoofdstuk 1).')
h2_1 = f'''{kader('Definities', '<ul><li>Een <b>zuivere stof</b> bestaat uit <b>één soort deeltjes</b>. Bv. gedestilleerd water, suiker, goud.</li><li>Een <b>mengsel</b> bestaat uit <b>twee of meer zuivere stoffen</b>. Bv. kraantjeswater, lucht, cola.</li><li>Een <b>bestanddeel</b> is een zuivere stof die in een mengsel zit. Bv. water en suiker zijn bestanddelen van suikerwater.</li></ul>')}
{figuur(fig_zuiver_mengsel(), 'Het deeltjesmodel van een zuivere stof, een homogeen en een heterogeen mengsel.')}
<p>Een zuivere stof heeft een <b>vaste smelttemperatuur en kooktemperatuur</b>. Zuiver water kookt bij 100 °C. Zout water kookt bij een hogere temperatuur, en die stijgt nog tijdens het koken.</p>
{ttabel(['', 'Homogeen mengsel', 'Heterogeen mengsel'], [
  ['Wat zie je?', 'je ziet de bestanddelen <b>niet</b>, ook niet met een microscoop', 'je ziet de bestanddelen (met het oog of met een microscoop)'],
  ['Voorbeelden', 'suikerwater, lucht, kraantjeswater, azijn', 'zand in water, melk (onder de microscoop vetbolletjes), muesli']])}
{figuur(fig_schema(), 'Overzicht: zo deel je materie in.')}
{tool('chemie-mengsels.html', 'Sorteer zuivere stoffen en mengsels in de tool')}
{denk('denk_1', 'Melk lijkt helemaal wit en gelijk. Toch noemen we melk een heterogeen mengsel. Hoe kan dat?', [
  ('Met het oog', 'Je ziet geen aparte deeltjes: het lijkt homogeen.'),
  ('Met een microscoop', 'Je ziet kleine vetbolletjes in het water zweven.')], 'Ziet men de bestanddelen met een microscoop, dan is het mengsel heterogeen.')}'''
h2_2 = f'''<p>Mengsels krijgen een naam volgens de <b>aggregatietoestand</b> van hun bestanddelen.</p>
<h3>Heterogene mengsels</h3>
{ttabel(['Naam', 'Bestanddelen', 'Voorbeeld'], [
  ['grof mengsel', 'vast in vast', 'muesli, zand met kiezels op een bouwwerf'],
  ['suspensie', 'vast in vloeistof', 'modderwater, fruitsap met vruchtvlees'],
  ['emulsie', 'vloeistof in vloeistof (mengen niet)', 'mayonaise, vinaigrette, melk'],
  ['schuim', 'gas in vloeistof of vast', 'slagroom, scheerschuim, piepschuim'],
  ['rook', 'vast in gas', 'rook van een vuur, uitlaatgassen met roet'],
  ['nevel', 'vloeistof in gas', 'mist boven het Ter Kamerenbos, wolk']])}
<p>Rook en nevel uit een spuitbus noemen we samen een <b>aerosol</b>.</p>
<h3>Homogene mengsels</h3>
{ttabel(['Naam', 'Bestanddelen', 'Voorbeeld'], [
  ['oplossing', 'vast, vloeistof of gas opgelost in een vloeistof', 'suikerwater, zout water, cola (CO₂ in water)'],
  ['gasmengsel', 'gas in gas', 'lucht'],
  ['legering', 'vast in vast (gesmolten metalen samen gestold)', 'brons (Manneken Pis), roestvrij staal (bollen van het Atomium)']])}
{tool('chemie-mengsels.html#les22', 'Oefen de soorten mengsels in de tool')}
{denk('denk_2', 'Je schudt een fles vinaigrette (olie en azijn). Even later liggen er weer twee lagen. Welk soort mengsel is vinaigrette?', [
  ('Bestanddelen', 'Olie en azijn: twee vloeistoffen.'),
  ('Mengen ze?', 'Nee, ze vormen opnieuw twee lagen: je ziet ze apart.')], 'Vinaigrette is een emulsie: een heterogeen mengsel van twee vloeistoffen.')}'''
h2_3 = f'''{kader('Definitie', '<p>Een <b>stofeigenschap</b> is een eigenschap die hoort bij de <b>stof</b>, niet bij het voorwerp. Ze verandert niet als je meer of minder van de stof neemt. Daarmee kan je een stof <b>herkennen</b>.</p>')}
{ttabel(['Stofeigenschappen', 'Voorwerpseigenschappen'], [
  ['kleur, geur, smaak', 'massa'], ['smelttemperatuur, kooktemperatuur', 'volume'], ['massadichtheid', 'vorm, lengte'], ['oplosbaarheid in water', 'temperatuur'], ['geleidt elektrische stroom of niet, magnetisch of niet', '']])}
<p>Een ijzeren spijker en een ijzeren brug hebben een andere massa en vorm (voorwerpseigenschappen), maar dezelfde massadichtheid (7,87 g/cm³) en smelttemperatuur (1538 °C): stofeigenschappen van ijzer.</p>
<p><b>Atomium</b>: de bollen waren eerst bekleed met <b>aluminium</b>. Die bekleding was dof en aangetast. Bij de renovatie (2004–2006) koos men <b>roestvrij staal</b>: een stof die beter bestand is tegen weer en wind. Men koos dus een andere stof met betere stofeigenschappen.</p>
{tool('chemie-mengsels.html#les23', 'Oefen stofeigenschap of voorwerpseigenschap in de tool')}
{denk('denk_3', 'Een blokje kaarsvet en een kaars van 1 kg smelten allebei bij ongeveer 60 °C. Is de smelttemperatuur een stofeigenschap?', [
  ('Hoeveelheid', 'De massa is heel verschillend.'), ('Smelttemperatuur', 'Toch is ze dezelfde: ze hangt niet af van hoeveel kaarsvet je hebt.')], 'Ja, de smelttemperatuur is een stofeigenschap.')}'''
h2_oef = f'''{oef('opl_1', 1, 'Zuivere stof of mengsel?', 'Zuivere stof of mengsel? Is het mengsel homogeen of heterogeen?<ol class="deelvragen" type="a"><li>gedestilleerd water</li><li>kraantjeswater</li><li>lucht</li><li>goud (24 karaat)</li><li>soep met groentjes</li><li>cola</li><li>suiker</li></ol>', [
  ('a', 'zuivere stof'), ('b', 'homogeen mengsel (water met opgeloste zouten)'), ('c', 'homogeen mengsel (stikstof, zuurstof, …)'), ('d', 'zuivere stof'),
  ('e', 'heterogeen mengsel'), ('f', 'homogeen mengsel'), ('g', 'zuivere stof')], 'Eén soort deeltjes = zuivere stof.')}
{oef_fig('opl_2', 2, 'Deeltjesmodel lezen', 'Welke tekening stelt een zuivere stof voor, welke een homogeen mengsel en welke een heterogeen mengsel?', svg(deeltjes(110, 80, 170, 130, [(GROEN, 1), (LICHT, 1)], gemengd=False, zaad=11) + t(110, 165, 'A') + deeltjes(320, 80, 170, 130, [(ROOD, 1)], zaad=12) + t(320, 165, 'B') + deeltjes(530, 80, 170, 130, [(GROEN, 1), (LICHT, 1)], zaad=13) + t(530, 165, 'C'), 640, 175), [
  ('A', 'twee soorten deeltjes in klontjes: heterogeen mengsel'), ('B', 'één soort deeltjes: zuivere stof'), ('C', 'twee soorten goed verdeeld: homogeen mengsel')], 'Tel de soorten deeltjes en kijk of ze goed verdeeld zijn.',
  svg(t(320, 30, 'A heterogeen · B zuivere stof · C homogeen', INK, size=16), 640, 50))}
{oef('opl_3', 3, 'Welk soort mengsel?', 'Geef de naam van het mengsel en de aggregatietoestand van de bestanddelen.<ol class="deelvragen" type="a"><li>slagroom</li><li>mayonaise</li><li>mist</li><li>modderwater</li><li>brons</li><li>zout water</li><li>rook van een barbecue</li><li>muesli</li></ol>', [
  ('a', 'schuim: gas in vloeistof'), ('b', 'emulsie: vloeistof in vloeistof'), ('c', 'nevel: vloeistof in gas'), ('d', 'suspensie: vast in vloeistof'),
  ('e', 'legering: vast in vast'), ('f', 'oplossing: vast in vloeistof'), ('g', 'rook: vast in gas'), ('h', 'grof mengsel: vast in vast')], 'Kijk naar de aggregatietoestand van elk bestanddeel.')}
{oef('opl_4', 4, 'Stofeigenschap of voorwerpseigenschap?', '<ol class="deelvragen" type="a"><li>Koper is roodbruin.</li><li>Het blokje weegt 20 g.</li><li>Alcohol kookt bij 78 °C.</li><li>De staaf is 30 cm lang.</li><li>Zout lost op in water.</li><li>IJzer wordt aangetrokken door een magneet.</li><li>Het water in het glas is 18 °C.</li></ol>', [
  ('a', 'stofeigenschap'), ('b', 'voorwerpseigenschap'), ('c', 'stofeigenschap'), ('d', 'voorwerpseigenschap'), ('e', 'stofeigenschap'), ('f', 'stofeigenschap'), ('g', 'voorwerpseigenschap')],
  'Verandert het als je meer of minder neemt (of het voorwerp anders vormt)? Dan is het een voorwerpseigenschap.')}
{oef('opl_5', 5, 'Redeneren: bestanddelen', 'Zeewater bevat water en zout. Noteer de bestanddelen. Is zeewater een zuivere stof? Hoe kan je met de kooktemperatuur bewijzen dat het geen zuivere stof is?', [
  ('Bestanddelen', 'water en zout (en nog andere zouten)'), ('Zuivere stof?', 'Nee, een mengsel: twee of meer stoffen.'),
  ('Bewijs', 'Zuiver water kookt bij precies 100 °C. Zeewater kookt boven 100 °C en de temperatuur stijgt verder tijdens het koken.')], 'Een mengsel heeft geen vaste kooktemperatuur.')}
{oef('opl_6', 6, 'Redeneren: het Atomium', 'Waarom koos men bij de renovatie van het Atomium voor roestvrij staal en niet opnieuw voor aluminium? Gaat het om een stofeigenschap of een voorwerpseigenschap?', [
  ('Probleem', 'De aluminium bekleding werd dof en aangetast door weer en wind.'), ('Keuze', 'Roestvrij staal is beter bestand tegen corrosie.'), ('Soort', 'Bestand zijn tegen corrosie hoort bij de stof.')],
  'Men koos een stof met een betere stofeigenschap.')}'''
h2_samenv = '''<p><b>Zuivere stof</b>: één soort deeltjes, vaste smelt- en kooktemperatuur. <b>Mengsel</b>: twee of meer zuivere stoffen = <b>bestanddelen</b>.</p>
<p><b>Homogeen</b>: bestanddelen niet zichtbaar, ook niet met een microscoop (oplossing, gasmengsel, legering). <b>Heterogeen</b>: bestanddelen zichtbaar (grof mengsel, suspensie, emulsie, schuim, rook, nevel).</p>
<p><b>Stofeigenschap</b>: hoort bij de stof (kleur, geur, smelt- en kooktemperatuur, massadichtheid, oplosbaarheid, geleiding, magnetisch). <b>Voorwerpseigenschap</b>: massa, volume, vorm, lengte, temperatuur.</p>'''

# ================================================================ T1 H3 SCHEIDINGSTECHNIEKEN
h3_doelen = ['de definitie van <b>scheidingstechniek</b> noteren;',
             'het principe van <b>zeven, decanteren, filtreren en centrifugeren</b> uitleggen met een tekening en de stofeigenschap noteren;',
             'het principe van <b>uitdampen, destilleren, extraheren en adsorberen</b> uitleggen met een tekening en de stofeigenschap noteren;',
             'de <b>onderdelen</b> van elke opstelling benoemen;',
             'bij een voorbeeld uit het dagelijks leven de gebruikte scheidingstechniek noteren.']
h3_vk = vk('Zuivere stof, mengsel en bestanddeel; homogeen en heterogeen (hoofdstuk 2).', 'De soorten mengsels: suspensie, emulsie, oplossing …', '<b>Stofeigenschappen</b>: deeltjesgrootte, massadichtheid, kooktemperatuur, oplosbaarheid.')
def techblok(k):
    v = TECH[k]
    return f'''<h3>{v['naam']}</h3>
{figuur(tech_fig(k), v['naam'] + ': de onderdelen van de opstelling.')}
{figuur(MODEL[k][0](), MODEL[k][1]) if k in MODEL else ''}
<ol>{''.join(f'<li>{c}</li>' for c in v['caps'])}</ol>
{ttabel(['Soort mengsel', 'Gebaseerd op', 'Dagelijks leven'], [[v['mengsel'], '<b>' + v['eig'] + '</b>', v['vb']]])}'''
h3_1 = f'''<p>In een mengsel houdt elk bestanddeel zijn eigen <b>stofeigenschappen</b>. IJzer blijft magnetisch, ook als het met zand gemengd is. Met een magneet haal je het ijzer eruit.</p>
{kader('Definitie', '<p>Een <b>scheidingstechniek</b> is een methode om de bestanddelen van een mengsel van elkaar te scheiden. Elke techniek gebruikt een <b>verschil in een stofeigenschap</b> van de bestanddelen.</p>')}
<p>Een <b>heterogeen</b> mengsel scheid je met zeven, decanteren, filtreren of centrifugeren. Een <b>homogeen</b> mengsel scheid je met uitdampen, destilleren, extraheren of adsorberen.</p>
{tool('chemie-scheidingstechnieken.html', 'Bekijk de scheidingstechnieken stap voor stap')}'''
h3_2 = ''.join(techblok(k) for k in ('zeven', 'decanteren', 'filtreren', 'centrifugeren')) + denk('denk_1', 'Je wil zand uit water halen. Je kan decanteren of filtreren. Welke techniek geeft het helderste water? Waarom?', [
  ('Decanteren', 'Je giet het water voorzichtig af. Fijne zandkorrels gaan toch mee.'),
  ('Filtreren', 'Het filtreerpapier houdt ook de fijne korrels tegen.')], 'Filtreren geeft helderder water; decanteren gaat sneller voor grote hoeveelheden.')
h3_3 = ''.join(techblok(k) for k in ('uitdampen', 'destilleren', 'extraheren', 'adsorberen')) + denk('denk_2', 'Bij uitdampen en bij destilleren verwarm je zout water. Wat is het verschil in wat je overhoudt?', [
  ('Uitdampen', 'Het water verdampt en gaat verloren in de lucht. Je houdt het zout over.'),
  ('Destilleren', 'Het water verdampt, koelt af in de koeler en wordt opgevangen als destillaat. Je houdt zout én zuiver water over.')], 'Wil je ook het water terug, dan destilleer je.')
h3_4 = f'''{ttabel(['Techniek', 'Mengsel', 'Gebaseerd op'], [[TECH[k]['naam'], TECH[k]['mengsel'].split(':')[0], TECH[k]['eig'].split(' (')[0]] for k in TECH])}
<h3>Scheiden in Brussel en thuis</h3>
<p><b>Waterzuiveringsstation Brussel-Noord (Haren)</b>: roosters houden takken en plastic tegen (<b>zeven</b>). Daarna zakt het zand naar de bodem en schept men het vet bovenaan af (<b>decanteren</b>). Bacteriën breken opgeloste vuilstoffen af: dat is geen scheidingstechniek, want daar ontstaan nieuwe stoffen.</p>
<p><b>Vivaqua (Tailfer)</b>: een filter met <b>actieve kool</b> houdt resten van pesticiden vast (<b>adsorberen</b>). Gewoon filtreren is niet genoeg: die stoffen zijn opgelost, de deeltjes zijn te klein.</p>
<p><b>Muntthee</b>: geur-, smaak- en kleurstoffen uit de muntblaadjes lossen op in heet water (<b>extraheren</b>). Een theezakje houdt de blaadjes tegen (<b>filtreren</b>).</p>
{tool('chemie-scheidingstechnieken.html#lesov', 'Oefen het overzicht en de voorbeelden in de tool')}
{denk('denk_3', 'Een koffiezetapparaat werkt met gemalen koffie, heet water en een koffiefilter. Welke twee scheidingstechnieken herken je?', [
  ('Heet water', 'Het water lost smaak- en kleurstoffen uit de koffie op: extraheren (oplosbaarheid).'),
  ('Koffiefilter', 'De filter houdt het koffiedik tegen: filtreren (deeltjesgrootte).')], 'Koffie zetten = extraheren + filtreren.')}'''
h3_oef = f'''{oef('opl_1', 1, 'Definitie', 'Noteer de definitie van scheidingstechniek. Waarom kan je water en alcohol scheiden met destilleren?', [
  ('Definitie', 'Een methode om de bestanddelen van een mengsel te scheiden op basis van een verschil in een stofeigenschap.'),
  ('Water en alcohol', 'Ze hebben een andere kooktemperatuur (100 °C en 78 °C).')], 'Elk bestanddeel houdt zijn eigen stofeigenschappen.')}
{oef_fig('opl_2', 2, 'Onderdelen: filtreren', 'Benoem de onderdelen 1 tot 6.', tech_fig('filtreren', 'num'), [
  (str(i + 1), n) for i, n in enumerate(TECH['filtreren']['labels'])], 'Wat op het filter blijft, is het residu; wat erdoor gaat, het filtraat.', tech_fig('filtreren'))}
{oef_fig('opl_3', 3, 'Onderdelen: destilleren', 'Benoem de onderdelen 1 tot 8.', tech_fig('destilleren', 'num'), [
  (str(i + 1), n) for i, n in enumerate(TECH['destilleren']['labels'])], 'Het koelwater stroomt onderaan in en bovenaan uit.', tech_fig('destilleren'))}
{oef_fig('opl_4', 4, 'Onderdelen: uitdampen', 'Benoem de onderdelen 1 tot 5. Welke stofeigenschap gebruik je?', tech_fig('uitdampen', 'num'), [
  (str(i + 1), n) for i, n in enumerate(TECH['uitdampen']['labels'])] + [('Stofeigenschap', 'verschil in kooktemperatuur')], 'Het water verdampt, de opgeloste stof blijft over als residu.', tech_fig('uitdampen'))}
{oef('opl_5', 5, 'Welke techniek?', 'Welke scheidingstechniek gebruik je? Op welke stofeigenschap is ze gebaseerd?<ol class="deelvragen" type="a"><li>bloem zonder klontjes voor een cake</li><li>zout halen uit zeewater in een zoutpan</li><li>thee zetten met een theezakje</li><li>pasta afgieten in een vergiet</li><li>bloed scheiden in het labo van het UZ Brussel</li><li>een aquariumfilter met actieve kool</li><li>sterkedrank maken uit gegist fruit</li><li>olie afgieten van water</li></ol>', [
  ('a', 'zeven: deeltjesgrootte'), ('b', 'uitdampen: kooktemperatuur'), ('c', 'extraheren: oplosbaarheid'), ('d', 'zeven of filtreren: deeltjesgrootte'),
  ('e', 'centrifugeren: massadichtheid'), ('f', 'adsorberen: adsorptievermogen'), ('g', 'destilleren: kooktemperatuur'), ('h', 'decanteren: massadichtheid')], 'Zoek eerst welk verschil tussen de bestanddelen je gebruikt.')}
{oef('opl_6', 6, 'Redeneren: een mengsel in stappen scheiden', 'Je hebt een mengsel van <b>zand, zout en ijzervijlsel</b>. Beschrijf in drie stappen hoe je de drie stoffen zuiver terugkrijgt. Noteer bij elke stap de stofeigenschap.', [
  ('Stap 1', 'Haal het ijzervijlsel eruit met een magneet (magnetisch).'), ('Stap 2', 'Doe zand en zout in water: het zout lost op. Filtreer: het zand blijft als residu op het filter (deeltjesgrootte, oplosbaarheid).'),
  ('Stap 3', 'Damp het filtraat (zout water) uit: het zout blijft over (kooktemperatuur).')], 'Magneet → oplossen en filtreren → uitdampen.')}
{oef('opl_7', 7, 'Redeneren: Brussel-Noord', 'In het waterzuiveringsstation Brussel-Noord breken bacteriën vuilstoffen af. Een leerling zegt: "Dat is ook een scheidingstechniek." Klopt dat?', [
  ('Wat gebeurt er?', 'De bacteriën zetten de vuilstoffen om in andere stoffen.'), ('Scheidingstechniek?', 'Bij scheiden blijven de stoffen dezelfde; hier ontstaan nieuwe stoffen.')], 'Nee: dat is een chemisch proces, geen scheidingstechniek.')}'''
h3_samenv = '<p><b>Scheidingstechniek</b>: bestanddelen van een mengsel scheiden op basis van een verschil in stofeigenschap.</p>' + ttabel(['Techniek', 'Gebaseerd op'], [[TECH[k]['naam'], TECH[k]['eig'].split(' (')[0]] for k in TECH])

maak('cursus-chemie-wetenschap.html', T1 + '1', 'Chemie als wetenschap',
     'Werk dit hoofdstuk samen met de tool <a href="chemie-stoffen.html">Chemie en veiligheid</a>. Oefeningen maak je op papier.',
     h1_doelen, h1_vk, [('Fysica of chemie?', h1_1), ('Veilig werken: gevarensymbolen en H- en P-zinnen', h1_2), ('Verantwoord omgaan met producten', h1_3)], h1_oef, h1_samenv, ('chemie-stoffen.html', 'Oefen verder in de tool'))
maak('cursus-chemie-mengsels.html', T1 + '2', 'Zuivere stoffen en mengsels',
     'Werk dit hoofdstuk samen met de tool <a href="chemie-mengsels.html">Mengsels</a>. Oefeningen maak je op papier.',
     h2_doelen, h2_vk, [('Zuivere stof, mengsel en bestanddeel', h2_1), ('Soorten mengsels', h2_2), ('Stofeigenschappen en voorwerpseigenschappen', h2_3)], h2_oef, h2_samenv, ('chemie-mengsels.html', 'Oefen verder in de tool'))
maak('cursus-chemie-scheidingstechnieken.html', T1 + '3', 'Scheidingstechnieken',
     'Werk dit hoofdstuk samen met de tool <a href="chemie-scheidingstechnieken.html">Scheidingstechnieken</a>. Oefeningen maak je op papier.',
     h3_doelen, h3_vk, [('Wat is een scheidingstechniek?', h3_1), ('Heterogene mengsels scheiden', h3_2), ('Homogene mengsels scheiden', h3_3), ('Overzicht en voorbeelden uit Brussel en thuis', h3_4)], h3_oef, h3_samenv, ('chemie-scheidingstechnieken.html', 'Oefen verder in de tool'))

exec(open('/home/claude/cursus/chemie_t2.py', encoding='utf-8').read())
print('chemie ok')
