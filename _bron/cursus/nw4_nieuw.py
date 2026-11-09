# Cursussen fysica 4NW in het nieuwe formaat: Thema 1 Druk (H1-H4) en Thema 2 Energie en vermogen (H1-H2).
# Gebruik:  cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/nw4_nieuw.py
# Bestaande inhoud en figuren uit druk_vast.py en vierde_cursus.py (de oude bouw-aanroepen worden opgevangen);
# nieuwe inhoud (idee, uitgewerkt voorbeeld, Test jezelf, wisbord, uitdagingen, begrippen) in nw4_inhoud.py.
# Tekenoefeningen op ruitjes met de helpers uit aso_krachten.py.
import re, sys
B_ = '/home/claude/toolswetenschappen/_bron/cursus/'
sys.path.insert(0, '/home/claude/cursus')
import bouw as BM
BM.FOOTER = 'Cursus fysica — gemaakt voor klasgebruik, bij de tools op Oefentools wetenschappen.'

a = {'__name__': 'aso'}
exec(open(B_ + 'aso_krachten.py', encoding='utf-8').read().split("exec(open('/home/claude/toolswetenschappen/_bron/cursus/aso_extra.py'")[0], a)
blok, oef, kader, tool, denk, figuur = a['blok'], a['oef'], a['kader'], a['tool'], a['denk'], a['figuur']
EDI_CSS, edi, W = a['EDI_CSS'], a['edi'], a['wisbord']
svg, t, pijl, punt, label, rooster, doos = a['svg'], a['t'], a['pijl'], a['punt'], a['label'], a['rooster'], a['doos']
INK, PAARS, G, ORANJE, B, R, HK, oef_fig, oplfig, TEKEN = a['INK'], a['PAARS'], a['G'], a['ORANJE'], a['B'], a['R'], a['HK'], a['oef_fig'], a['oplfig'], a['TEKEN']
AANPAK_SCHEMA = 'maak een schets met de gegevens en de krachten. Kies de juiste formule, vorm ze om als het moet en zet eerst alles om naar SI-eenheden (m², m³, Pa, J, s).'
AANPAK_LEES = 'de gegevens met hun eenheid'
exec(open(B_ + 'nieuw_formaat.py', encoding='utf-8').read())

# ------------------------------------------------------------------ oude inhoud opvangen
MAAK = []
dv = {'__name__': 'druk_vast'}
exec(open(B_ + 'druk_vast.py', encoding='utf-8').read().split("bouw('cursus-druk-vaste-stoffen.html'")[0], dv)
v = {'__name__': 'vierde', '_MAAK': lambda *x, **k: MAAK.append((x, k))}
exec(open(B_ + 'vierde_cursus.py', encoding='utf-8').read().replace('\nmaak(', '\n_MAAK('), v)
exec(open(B_ + 'nw4_inhoud.py', encoding='utf-8').read())
def fsub(x):
    if isinstance(x, str): return re.sub(r'(?<![A-Za-z])([FpVEWρ])_((?:pot,)?[a-zA-Z]+)', r'\1<sub>\2</sub>', x)
    if isinstance(x, (list, tuple)): return type(x)(fsub(y) for y in x)
    if isinstance(x, dict): return {k: fsub(v) for k, v in x.items()}
    return x
C = fsub(C)

def hernummer(html):
    n = [0]
    def f(m):
        n[0] += 1
        return f'<div class="oef" data-vrij="opl_{n[0]}">\n  <div class="titel"><span class="nr">{n[0]}</span>'
    return re.sub(r'<div class="oef" data-vrij="opl_\w+">\s*<div class="titel"><span class="nr">\w+</span>', f, html)

def oef_opl(titel, tekst, stappen, besluit, oplossing):
    """oefening zonder opgavefiguur, met een figuur in de oplossing"""
    return oef('opl_x', 0, titel, tekst, stappen, besluit).replace('<div class="besluit">', oplfig(oplossing) + '<div class="besluit">', 1)

def neem_weg(s, oud):
    """verwijder een oude oefening op titel"""
    s2 = re.sub(r'<div class="oef" data-vrij="opl_\d+">\s*<div class="titel"><span class="nr">\d+</span>' + re.escape(oud) + r'</div>.*?</div>\s*</div>\s*</div>\n?', '', s, count=1, flags=re.S)
    assert s2 != s, oud
    return s2

# ------------------------------------------------------------------ tekenoefeningen
GROND = '#d6d3d1'
def f_kist(opl):
    w, h = 600, 300
    o = rooster(w, h) + f'<rect x="0" y="160" width="{w}" height="140" fill="{GROND}" opacity=".55"/>' + doos(240, 80, 120, 80) + punt(300, 160, INK, 4)
    if opl: o += pijl(300, 160, 300, 160 + 6 * HK, ORANJE) + label(308, 270, 'F', 'G', ORANJE)
    return svg(o, w, h)
def f_punaise(opl):
    w, h = 600, 200
    o = rooster(w, h) + '<rect x="320" y="0" width="280" height="200" fill="#e9c891" opacity=".8"/>' + t(560, 24, 'hout', INK, 'end', 13, 600)
    o += '<rect x="196" y="70" width="14" height="60" rx="4" fill="#94a3b8" stroke="#334155" stroke-width="2"/>'   # kop
    o += '<path d="M210 96 H322 L340 100 L322 104 H210 Z" fill="#cbd5e1" stroke="#334155" stroke-width="1.5"/>'   # pin met punt
    o += punt(196, 82, INK, 4) + punt(340, 100, INK, 4)
    if opl:
        o += pijl(196, 82, 196 + 4 * HK, 82, B) + label(214, 70, 'F', 'duim', B)
        o += pijl(340, 100, 340 + 4 * HK, 100, R) + label(384, 88, 'F', 'punt', R)
    return svg(o, w, h)
def f_zuignap(opl):
    w, h = 600, 220
    o = rooster(w, h) + '<rect x="0" y="0" width="200" height="220" fill="#e2e8f0"/><line x1="200" y1="0" x2="200" y2="220" stroke="#64748b" stroke-width="3"/>' + t(100, 24, 'tegel', INK, 'middle', 13, 600)
    o += '<path d="M200 70 Q240 80 244 110 Q240 140 200 150 Z" fill="#fca5a5" stroke="#b91c1c" stroke-width="2"/><rect x="244" y="102" width="40" height="16" rx="5" fill="#b91c1c"/>'
    o += punt(244, 110, INK, 4)
    if opl: o += pijl(244, 110, 244 - 4 * HK, 110, B) + label(186, 148, 'F', 'lucht', B, 'end')
    return svg(o, w, h)
def f_pan(opl):
    w, h = 600, 260
    o = rooster(w, h) + '<path d="M180 120 V230 H420 V120" fill="#e5e7eb" stroke="#334155" stroke-width="3"/><rect x="170" y="108" width="260" height="12" fill="#475569"/>'
    o += '<rect x="290" y="94" width="20" height="14" fill="#475569"/>' + t(300, 200, 'gas met overdruk', INK, 'middle', 13, 600) + punt(300, 120, INK, 4)
    if opl: o += pijl(300, 120, 300, 120 - 4 * HK, R) + label(308, 44, 'F', 'gas', R)
    return svg(o, w, h)
def f_pers(opl):
    w, h = 600, 440
    o = rooster(w, h) + '<path d="M120 300 V420 H480 V292 H380 V380 H160 V300 Z" fill="#fde68a" stroke="#475569" stroke-width="2.5"/>'
    o += '<rect x="118" y="288" width="44" height="12" fill="#64748b"/><rect x="378" y="280" width="104" height="12" fill="#64748b"/>'
    o += t(172, 318, 'A₁', INK, 'start', 14) + t(500, 330, 'A₂ = 3 · A₁', INK, 'start', 14)
    o += pijl(140, 288, 140, 288 + 4 * HK, B) + punt(140, 288, INK, 4) + label(112, 360, 'F', '1', B, 'end') + punt(430, 292, INK, 4)
    if opl: o += pijl(430, 292, 430, 292 - 12 * HK, R) + label(440, 66, 'F', '2', R)
    return svg(o, w, h)
def f_wand(opl):
    w, h = 600, 300
    o = rooster(w, h) + '<rect x="0" y="40" width="360" height="260" fill="#bfdbfe" opacity=".8"/><rect x="360" y="0" width="240" height="300" fill="#d6d3d1"/>'
    o += '<line x1="0" y1="40" x2="360" y2="40" stroke="#2563eb" stroke-width="2"/>' + t(20, 32, 'wateroppervlak', B, 'start', 12, 600) + t(580, 24, 'wand', INK, 'end', 13, 600)
    for i, d in enumerate((1, 2, 3), start=1):
        y = 40 + 3 * HK * d
        o += t(300, y + 5, f'{d},0 m', INK, 'end', 12, 600) + punt(360, y, INK, 4)
        if opl: o += pijl(360, y, 360 + 2 * d * HK, y, R) + label(364 + 2 * d * HK, y - 8, 'F', str(d), R)
    return svg(o, w, h)
def f_steen(opl):
    w, h = 600, 300
    o = rooster(w, h) + '<rect x="0" y="20" width="600" height="280" fill="#bfdbfe" opacity=".7"/>' + '<ellipse cx="300" cy="150" rx="56" ry="36" fill="#9ca3af" stroke="#374151" stroke-width="2"/>' + punt(300, 150, INK, 4)
    if opl: o += pijl(303, 150, 303, 150 + 6 * HK, PAARS) + label(310, 276, 'F', 'z', PAARS) + pijl(297, 150, 297, 150 - 2 * HK, G) + label(287, 108, 'F', 'A', G, 'end')
    return svg(o, w, h)
def f_blok(opl):
    w, h = 600, 300
    o = rooster(w, h) + '<rect x="0" y="130" width="600" height="170" fill="#bfdbfe" opacity=".7"/><line x1="0" y1="130" x2="600" y2="130" stroke="#2563eb" stroke-width="2"/>'
    o += doos(250, 100, 100, 100, '#d6a96b', '#7c2d12') + punt(300, 150, INK, 4) + punt(300, 165, INK, 4)
    if opl: o += pijl(303, 150, 303, 150 + 4 * HK, PAARS) + label(310, 240, 'F', 'z', PAARS) + pijl(297, 165, 297, 165 - 4 * HK, G) + label(287, 92, 'F', 'A', G, 'end')
    return svg(o, w, h)
def vak(x, y, tekst, w=128, kleur='#eef2ff'):
    regels = tekst.split('|')
    s = f'<rect x="{x}" y="{y}" width="{w}" height="58" rx="8" fill="{kleur}" stroke="#64748b" stroke-width="1.5"/>'
    for i, r_ in enumerate(regels):
        s += t(x + w / 2, y + 26 + (i - (len(regels) - 1) / 2) * 16, r_, INK, 'middle', 12, 600)
    return s
def keten(vakken, toestellen, extra=None, w=600, h=150):
    o = '<rect width="%d" height="%d" fill="#fff"/>' % (w, h)
    n = len(vakken); stap = (w - 20) / n; bw = stap - 26
    for i, (v_, k) in enumerate(zip(vakken, toestellen + [''])):
        x = 10 + i * stap
        o += vak(x, 30, v_, bw)
        if i < n - 1:
            o += pijl(x + bw + 2, 59, x + stap - 2, 59, INK) + t(x + bw + 13, 22, k, B, 'middle', 11, 600)
    if extra: o += pijl(w - 20 - bw / 2 + 10, 88, w - 20 - bw / 2 + 10, 116, R) + t(w - 20 - bw / 2 + 10, 136, extra, R, 'middle', 12, 600)
    return svg(o, w, h)
def f_valies(opl):
    w, h = 600, 240
    o = rooster(w, h) + f'<rect x="0" y="180" width="{w}" height="60" fill="{GROND}" opacity=".55"/>' + '<rect x="160" y="120" width="100" height="60" rx="8" fill="#334155"/>' + punt(260, 140, INK, 4)
    o += pijl(260, 140, 260 + 4 * HK, 140 - 3 * HK, B) + label(350, 72, 'F', '', B) + pijl(160, 214, 440, 214, INK) + t(300, 234, 'verplaatsing', INK, 'middle', 12, 600)
    if opl:
        o += pijl(260, 140, 260 + 4 * HK, 140, R, dash='6 4') + label(348, 160, 'F', '∥', R)
        o += pijl(260, 140, 260, 140 - 3 * HK, G, dash='6 4') + label(250, 84, 'F', '⊥', G, 'end')
    return svg(o, w, h)
def f_doos(opl):
    w, h = 600, 280
    o = rooster(w, h) + doos(250, 120, 100, 60, '#e7c9a9', '#7c2d12') + '<path d="M268 180 Q300 172 332 180 L332 192 Q300 186 268 192 Z" fill="#8d5524"/>' + punt(300, 180, INK, 4)
    o += t(300, 226, 'je handen onder de doos', INK, 'middle', 12, 600)
    if opl: o += pijl(300, 180, 300, 180 - 4 * HK, B) + label(310, 110, 'F', 'hand', B) + pijl(460, 200, 460, 100, INK, dash='6 4') + t(470, 150, 's = 1,5 m', INK, 'start', 12, 600)
    return svg(o, w, h)

T = {}
T['druk-vast'] = [
 oef_fig('opl_x', 0, 'Tekenen: een kist op de vloer', 'Een kist van 30 kg staat op de vloer (g ≈ 10 N/kg). Het contactoppervlak is 0,20 m².<ol class="deelvragen" type="a"><li>Teken de kracht van de kist op de vloer. Schaal: 1 hokje ≙ 50 N. Begin in de stip.</li><li>Bereken de druk op de vloer.</li></ol>', f_kist(False),
   [('a', 'De kracht van de kist op de vloer is het gewicht F<sub>G</sub> = m · g = 30 kg · 10 N/kg = 300 N. Ze werkt op de vloer, in het contactvlak, naar beneden: 300 N : 50 N = 6 hokjes.'),
    ('b', 'p = F / A = 300 N / 0,20 m² = 1500 Pa')], 'F<sub>G</sub>: 6 hokjes naar beneden, vanuit het contactvlak. p = 1,5 · 10³ Pa.', f_kist(True)),
 oef_fig('opl_x', 0, 'Tekenen: de punaise', 'Je duwt met je duim een punaise in een houten plank, met een kracht van 20 N. Schaal: 1 hokje ≙ 5 N.<ol class="deelvragen" type="a"><li>Teken de kracht van je duim op de kop van de punaise (stip links).</li><li>Teken de kracht van de punt op het hout (stip rechts). Die is even groot.</li><li>De kop heeft een oppervlakte van 1,0 cm², de punt 0,10 mm². Bereken de druk onder de kop en onder de punt.</li></ol>', f_punaise(False),
   [('a', '20 N : 5 N = 4 hokjes, naar rechts, vanuit de stip op de kop'), ('b', '4 hokjes naar rechts, vanuit de punt, in het hout'),
    ('c', 'kop: A = 1,0 · 10⁻⁴ m² → p = 20 / 1,0 · 10⁻⁴ = 2,0 · 10⁵ Pa · punt: A = 0,10 mm² = 1,0 · 10⁻⁷ m² → p = 20 / 1,0 · 10⁻⁷ = 2,0 · 10⁸ Pa')],
   'Twee even lange pijlen, maar de druk onder de punt is 1000 keer zo groot.', f_punaise(True))]
T['gassen'] = [
 oef_fig('opl_x', 0, 'Tekenen: de zuignap', 'Een zuignap met een oppervlakte van 10 cm² zit op een tegel. Onder de zuignap zit (bijna) geen lucht meer. De luchtdruk is 100 kPa.<ol class="deelvragen" type="a"><li>Bereken de kracht van de buitenlucht op de zuignap.</li><li>Teken die kracht. Schaal: 1 hokje ≙ 25 N. Begin in de stip.</li></ol>', f_zuignap(False),
   [('a', 'A = 10 cm² = 0,0010 m² → F = p · A = 100 000 Pa · 0,0010 m² = 100 N'), ('b', '100 N : 25 N = 4 hokjes, naar de tegel toe (naar links), vanuit de stip')],
   'F = 100 N: de buitenlucht drukt de zuignap tegen de tegel.', f_zuignap(True)),
 oef_fig('opl_x', 0, 'Tekenen: het deksel van de snelkookpan', 'In een snelkookpan is er een overdruk van 80 kPa. Het deksel heeft een oppervlakte van 0,050 m².<ol class="deelvragen" type="a"><li>Bereken de extra kracht van het gas op het deksel.</li><li>Teken die kracht. Schaal: 1 hokje ≙ 1000 N. Begin in de stip.</li></ol>', f_pan(False),
   [('a', 'F = p · A = 80 000 Pa · 0,050 m² = 4000 N'), ('b', '4000 N : 1000 N = 4 hokjes, naar boven, vanuit de onderkant van het deksel')],
   'F = 4,0 · 10³ N naar boven: daarom moet het deksel vergrendeld zijn.', f_pan(True))]
T['vloeistoffen'] = [
 oef_fig('opl_x', 0, 'Tekenen: de hydraulische pers', 'Op de kleine zuiger werkt een kracht F<sub>1</sub> van 40 N (getekend, 1 hokje ≙ 10 N). De grote zuiger heeft een 3 keer zo grote oppervlakte.<ol class="deelvragen" type="a"><li>Bereken de kracht F<sub>2</sub> van de olie op de grote zuiger.</li><li>Teken F<sub>2</sub> vanuit de stip op de grote zuiger.</li></ol>', f_pers(False),
   [('a', 'F₁ / A₁ = F₂ / A₂ → F₂ = F₁ · A₂ / A₁ = 40 N · 3 = 120 N'), ('b', '120 N : 10 N = 12 hokjes, naar boven, vanuit de onderkant van de grote zuiger')],
   'F<sub>2</sub> = 120 N: een pijl van 12 hokjes, 3 keer zo lang als F<sub>1</sub>.', f_pers(True)),
 oef_fig('opl_x', 0, 'Tekenen: water tegen een wand', 'Op de wand van een waterbassin zitten drie luikjes van 0,010 m² elk, op 1,0 m, 2,0 m en 3,0 m diepte (g ≈ 10 N/kg).<ol class="deelvragen" type="a"><li>Bereken de kracht van het water op elk luikje (alleen de hydrostatische druk).</li><li>Teken de drie krachten op de wand. Schaal: 1 hokje ≙ 50 N.</li><li>Waarom is een stuwdam onderaan dikker dan bovenaan?</li></ol>', f_wand(False),
   [('a', 'p<sub>h</sub> = ρ · g · h = 1000 · 10 · 1,0 = 10 000 Pa → F = p · A = 10 000 · 0,010 = 100 N. Op 2,0 m: 200 N. Op 3,0 m: 300 N.'),
    ('b', '2, 4 en 6 hokjes, loodrecht op de wand, vanuit de stippen, de wand in'), ('c', 'Dieper is de druk groter, dus de kracht van het water op de wand ook. Onderaan moet de wand het sterkst zijn.')],
   'Hoe dieper, hoe langer de pijl: de kracht neemt evenredig toe met de diepte.', f_wand(True))]
T['archimedes'] = [
 oef_fig('opl_x', 0, 'Tekenen: een steen onder water', 'Een steen van 1,2 kg met een volume van 0,40 dm³ ligt helemaal onder water (g ≈ 10 N/kg). Schaal: 1 hokje ≙ 2 N.<ol class="deelvragen" type="a"><li>Bereken de zwaartekracht en de archimedeskracht.</li><li>Teken beide krachten op de steen. Begin in de stip.</li><li>Zinkt de steen? Leg uit met de krachten.</li></ol>', f_steen(False),
   [('a', 'F<sub>z</sub> = 1,2 · 10 = 12 N · F<sub>A</sub> = 1000 · 10 · 0,40 · 10⁻³ = 4,0 N'), ('b', 'F<sub>z</sub>: 6 hokjes naar beneden · F<sub>A</sub>: 2 hokjes naar boven, allebei vanuit het midden (de steen is helemaal ondergedompeld)'),
    ('c', 'F<sub>z</sub> &gt; F<sub>A</sub>: de steen zinkt.')], 'Een lange pijl naar beneden, een korte naar boven: de steen zinkt.', f_steen(True)),
 oef_fig('opl_x', 0, 'Tekenen: een drijvend blok', 'Een houten blok van 0,80 kg drijft in water (g ≈ 10 N/kg). Schaal: 1 hokje ≙ 2 N. De bovenste stip is het zwaartepunt van het blok, de onderste het midden van het ondergedompelde deel.<ol class="deelvragen" type="a"><li>Hoe groot is de archimedeskracht? Leg uit.</li><li>Teken de zwaartekracht en de archimedeskracht, elk in het juiste aangrijpingspunt.</li></ol>', f_blok(False),
   [('a', 'Het blok drijft: het is in evenwicht, dus F<sub>A</sub> = F<sub>z</sub> = 0,80 · 10 = 8,0 N.'), ('b', 'F<sub>z</sub>: 4 hokjes naar beneden vanuit het zwaartepunt · F<sub>A</sub>: 4 hokjes naar boven vanuit het midden van het ondergedompelde deel. Beide op dezelfde verticale lijn.')],
   'Twee even lange pijlen op dezelfde werklijn, met een ander aangrijpingspunt.', f_blok(True))]
T['energie'] = [
 oef_opl('Tekenen: de energieketen van een fietslamp', 'Kenza fietst ’s avonds. Een dynamo aan haar wiel laat de lamp branden. Teken de energieketen met vakjes en pijlen: schrijf in elk vakje een energievorm en bij elke pijl het toestel of het voorwerp dat de energie omzet. Teken ook de energie die niet nuttig is.',
   [('Begin', 'chemische energie in het voedsel van Kenza'), ('Omzettingen', 'spieren → kinetische energie van het wiel → dynamo → elektrische energie → lamp → stralingsenergie'), ('Niet nuttig', 'bij elke omzetting ontstaat ook thermische energie')],
   'chemisch → kinetisch → elektrisch → straling (+ thermisch)', keten(['chemische|energie', 'kinetische|energie', 'elektrische|energie', 'stralings-|energie'], ['spieren', 'dynamo', 'lamp'], '+ thermische energie')),
 oef_opl('Tekenen: de pompcentrale bij een tekort', 'Bij een tekort aan stroom laat de pompcentrale van Coo water naar beneden stromen. Teken de energieketen met vakjes en pijlen, met bij elke pijl het toestel. Teken ook de energie die niet nuttig is.',
   [('Begin', 'gravitationele potentiële energie van het water in het bovenste bekken'), ('Omzettingen', 'het water stroomt naar beneden → kinetische energie → turbine en generator → elektrische energie'), ('Niet nuttig', 'wrijving in de leidingen en de turbine: thermische energie')],
   'gravitationeel → kinetisch → elektrisch (+ thermisch)', keten(['grav. potentiële|energie', 'kinetische|energie', 'elektrische|energie'], ['vallend water', 'turbine + generator'], '+ thermische energie'))]
T['arbeid'] = [
 oef_fig('opl_x', 0, 'Tekenen: kracht ontbinden bij een valies', 'Je trekt een valies schuin omhoog met een kracht F van 50 N (getekend, schaal: 1 hokje ≙ 10 N). Je wandelt 20 m.<ol class="deelvragen" type="a"><li>Ontbind F in een component evenwijdig met de verplaatsing en een component loodrecht erop.</li><li>Lees de grootte van beide componenten af.</li><li>Bereken de arbeid van F. Welke component levert arbeid?</li></ol>', f_valies(False),
   [('a', 'Teken vanuit het aangrijpingspunt een horizontale en een verticale component; de kop van F is de overstaande hoek van de rechthoek.'), ('b', 'evenwijdig: 4 hokjes = 40 N · loodrecht: 3 hokjes = 30 N'),
    ('c', 'Alleen de component evenwijdig met de verplaatsing levert arbeid: W = 40 N · 20 m = 800 J. (Controle: W = F · Δx · cos α = 50 · 20 · 0,80 = 800 J.)')],
   'W = 8,0 · 10² J: alleen het deel van F in de richting van de verplaatsing telt.', f_valies(True)),
 oef_fig('opl_x', 0, 'Tekenen: een doos optillen en dragen', 'Je tilt een doos van 2,0 kg met constante snelheid 1,5 m op (g ≈ 10 N/kg). Daarna draag je ze 5,0 m horizontaal.<ol class="deelvragen" type="a"><li>Teken de kracht van je handen op de doos. Schaal: 1 hokje ≙ 5 N. Begin in de stip.</li><li>Bereken de arbeid van je kracht bij het optillen.</li><li>Hoeveel arbeid levert dezelfde kracht bij het horizontaal dragen? Waarom?</li><li>Bereken de arbeid van de zwaartekracht bij het optillen. Vergelijk met b.</li></ol>', f_doos(False),
   [('a', 'Constante snelheid: F<sub>hand</sub> = F<sub>z</sub> = 2,0 · 10 = 20 N → 4 hokjes naar boven, vanuit het contactvlak onder de doos'),
    ('b', 'W = F · Δx · cos 0° = 20 N · 1,5 m = 30 J'), ('c', 'W = 0 J: de kracht staat loodrecht op de verplaatsing (cos 90° = 0).'),
    ('d', 'De zwaartekracht wijst omlaag, de verplaatsing omhoog: W<sub>z</sub> = 20 N · 1,5 m · cos 180° = −30 J. Even groot als b, maar negatief: samen 0 J, want de snelheid is constant (W<sub>res</sub> = ΔE<sub>k</sub> = 0).')],
   'Optillen: 30 J (handen) en −30 J (zwaartekracht). Horizontaal dragen: 0 J.', f_doos(True))]

# ------------------------------------------------------------------ pagina's
def LD(lesdoelen_html): return lesdoelen_html
SLEUTEL = {'cursus-druk-gassen.html': 'gassen', 'cursus-druk-vloeistoffen.html': 'vloeistoffen', 'cursus-archimedes.html': 'archimedes',
           'cursus-energie-systemen.html': 'energie', 'cursus-arbeid-vermogen.html': 'arbeid'}
INTRO_EXTRA = ' De oplossingen staan online, zodra ze in de les besproken zijn.'
OEF_INTRO = ('<p>Maak deze oefeningen <b>op papier</b>, in je schrift. Gebruik telkens het stappenplan. Tekenoefeningen maak je op de figuur of op ruitjespapier, met een lat en een potlood. '
             'De oplossingen verschijnen hier nadat we de oefeningen in de les besproken hebben.</p>' + BM.STAP + '<p><button class="knop licht" data-print="oef">🖨 Druk de oefeningen af</button></p>')

def opschonen(s):
    s = s.replace('<div class="kader"><div class="kop">Werkvorm: expertgroepen</div>', '<div class="kader"><div class="kop">Voorbeeld · Zo werk je in expertgroepen</div>')
    s = re.sub(r'<h3>Uitgewerkt voorbeeld</h3>.*?</table>', '', s, flags=re.S)   # vervangen door het nieuwe uitgewerkte voorbeeld met het waarom
    s = s.replace('<p>Let op de woorden: het zijn de <b>deeltjes</b> (of het gas) die een kracht uitoefenen. De druk zelf duwt niet: druk vertelt hoe groot de kracht is per m².</p>', '')
    s = s.replace('Yasmine berekent de druk van dezelfde kist', 'Yasmine berekent de druk van de kist uit het uitgewerkte voorbeeld hieronder')
    return s

# hoofdstuk 1: druk bij vaste stoffen
oefs1 = dv['d_oef'].split(BM.STAP, 1)[1].split('</button></p>', 1)[1]
oefs1 = oefs1.replace(tool('druk.html#s12', 'Extra oefenen in de tool (kies: vaste stoffen)'), '')
oefs1 = OEF_INTRO + hernummer(oefs1 + ''.join(T['druk-vast'])) + tool('druk.html#s12', 'Extra oefenen in de tool (kies: vaste stoffen)')
VK1 = '<p>Dit moet je al kennen. Twijfel je? Herhaal het dan eerst.</p><ul><li>Een <b>kracht</b> is een vector, in newton (N). De kracht begint op het voorwerp waarop ze werkt.</li><li><b>Zwaartekracht</b>: F<sub>z</sub> = m · g met g = 9,81 N/kg. Massa in kg (1 kg = 1000 g).</li><li><b>Gewicht</b> F<sub>G</sub>: de kracht van een voorwerp op zijn steun.</li><li><b>Oppervlakte</b> berekenen: rechthoek = lengte · breedte, cirkel = π · r².</li><li>Lengtes omzetten: 1 m = 100 cm = 1000 mm.</li></ul>'
delen1 = [('Wat is druk?', dv['d1']), ('Rekenen met druk', opschonen(dv['d2'])), ('Drukverhogend en drukverlagend', dv['d3']), ('Redeneren met druk', dv['d4'])]
pagina('cursus-druk-vaste-stoffen.html', 'Fysica 4de jaar · Thema 1 Druk · Hoofdstuk 1', 'Druk bij vaste stoffen',
       'Werk dit hoofdstuk samen met de tool <a href="druk.html">Druk</a>. Oefeningen maak je op papier.' + INTRO_EXTRA,
       dv['d_lesdoelen'], VK1, delen1, oefs1, dv['d_samenv'], C['druk-vast'], eerste=True,
       cornell=[['Wat is druk?', 22], ['Met welke formule bereken je druk? Wat is de eenheid?', 26], ['Hoe bereken je F of A als je p kent?', 22], ['Hoe zet je cm² en mm² om naar m²?', 22], ['Wanneer is iets drukverhogend of drukverlagend? Geef voorbeelden.', 34], ['Wat gebeurt er met p als F of A verandert?', 30]])

for (bestand, eyebrow, titel, intro, delen, oefeningen, samenv, n_oef, toolref), kw in MAAK:
    k = SLEUTEL[bestand]
    if k == 'archimedes': oefeningen = neem_weg(oefeningen, 'Krachten tekenen')
    oefs = OEF_INTRO + hernummer(oefeningen + ''.join(T[k])) + (tool(*toolref) if toolref else '')
    pagina(bestand, eyebrow, titel, intro + INTRO_EXTRA, delen[0], kw['vk'], [(kop, opschonen(inh)) for kop, inh in delen[1:]],
           oefs, kader('Samenvatting', samenv), C[k])
