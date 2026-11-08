# Cursus chemie 3de jaar · thema 1-2 (december) in het nieuwe formaat (zie nieuw_formaat.py).
# Gebruik:  cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/chemie3_nieuw.py
# Bestaande inhoud en figuren uit chemie_cursus.py en chemie_t2.py; nieuwe inhoud in chemie3_inhoud.py.
import re, sys
B = '/home/claude/toolswetenschappen/_bron/cursus/'
sys.path.insert(0, '/home/claude/cursus')
import bouw as BM
BM.FOOTER = 'Cursus chemie — gemaakt voor klasgebruik, bij de tools op Oefentools wetenschappen.'

g = {'__name__': 'chemie'}
exec(open(B + 'chemie_cursus.py', encoding='utf-8').read().split("maak('cursus-chemie-wetenschap.html'")[0], g)
exec(open(B + 'chemie_t2.py', encoding='utf-8').read().split("maak('cursus-chemie-atomen-elementen.html'")[0], g)
exec(open(B + 'aso_veer.py', encoding='utf-8').read().split('GX, GY')[0], g)       # EDI_CSS, wisbord, edi
exec(open(B + 'chemie3_inhoud.py', encoding='utf-8').read(), g)                   # C
blok, oef, kader, tool, denk = g['blok'], g['oef'], g['kader'], g['tool'], g['denk']
C, edi, W, EDI_CSS = g['C'], g['edi'], g['wisbord'], g['EDI_CSS']
AANPAK_SCHEMA = 'zet de stappen in volgorde. Bij een mengsel: welke bestanddelen, welk verschil in stofeigenschap? Bij een atoom: Z → elektronen → schillen → groep en periode.'
AANPAK_LEES = 'de stoffen of de elementen, de gegevens'
exec(open(B + 'nieuw_formaat.py', encoding='utf-8').read())

# ---- extra tekenoefeningen elektronenconfiguratie (schillen en kern altijd voorgetekend)
import math
bohr, svg_, t_, ELZ, INK_, ROOD_, ELEK_, VAL_ = g['bohr'], g['svg'], g['t'], g['ELZ'], g['INK'], g['ROOD'], g['ELEK'], g['VAL']
def rij(zs, y=100, onder=lambda z: ELZ[z]['naam'], vraag=False, w=640):
    """lege schillen voor elk element; vraag=True: kern toont '? p⁺' (element nog onbekend)"""
    o = ''
    for i, z in enumerate(zs):
        cx = w / len(zs) * (i + .5)
        o += bohr(z, cx, y, 0.8, naam=False, leeg=True, kerntekst=not vraag)
        if vraag: o += t_(cx, y + 4, '?', ROOD_, size=13)
        o += t_(cx, y + 92, onder(z), INK_, size=13)
    return o
def met_elektronen(z, sch, cx, cy, schaal=0.8):
    """atoom met een (eventueel foute) verdeling sch over de schillen van element z"""
    o = bohr(z, cx, cy, schaal, naam=False, leeg=True)
    R = [r * schaal for r in (0, 34, 54, 74, 94)]
    for i, cnt in enumerate(sch):
        for k in range(cnt):
            a = -math.pi / 2 + k * 2 * math.pi / cnt + i * 0.3
            o += f'<circle cx="{cx + R[i+1]*math.cos(a):.1f}" cy="{cy + R[i+1]*math.sin(a):.1f}" r="{5*schaal:.1f}" fill="{ELEK_}" stroke="{INK_}" stroke-width="1"/>'
    return o
fig = g['fig_bohr']
CONF = {5: '2/3', 13: '2/8/3', 19: '2/8/8/1'}
FOUT = [(11, [2, 9, 0], 'Yasmine: natrium'), (8, [3, 5], 'Yasmine: zuurstof'), (17, [2, 8, 7], 'Yasmine: chloor')]
fout_fig = svg_(''.join(met_elektronen(z, sch, 640 / 3 * (i + .5), 100) + t_(640 / 3 * (i + .5), 192, lab, INK_, size=13) for i, (z, sch, lab) in enumerate(FOUT))
                + rij([11, 8, 17], y=320, onder=lambda z: 'jouw tekening: ' + ELZ[z]['naam']), 640, 420)
EXTRA_A2 = (g['oef_fig']('opl_2', 2, 'Van configuratie naar tekening', 'Je krijgt de elektronenconfiguratie. Teken de elektronen op de schillen en kleur de valentie-elektronen. Hoeveel protonen heeft het atoom? Welk element is het?',
        svg_(rij([5, 13, 19], vraag=True, onder=lambda z: CONF[z]), 640, 205),
        [('2/3', '5 elektronen → 5 protonen → boor (B); 3 valentie-elektronen'), ('2/8/3', '13 → aluminium (Al); 3 valentie-elektronen'), ('2/8/8/1', '19 → kalium (K); 1 valentie-elektron')],
        'Tel alle elektronen: dat is het aantal protonen, dus Z.', fig([5, 13, 19], 0.8))
    + g['oef_fig']('opl_2', 2, 'Zoek de fout', 'Yasmine tekende drie atomen. Welke tekeningen zijn fout? Leg uit welke regel ze vergat. Teken de juiste verdeling in de lege schillen eronder.',
        fout_fig,
        [('Natrium', 'fout: de L-schil heeft maximaal 8 elektronen. Juist: 2/8/1.'), ('Zuurstof', 'fout: de K-schil heeft maximaal 2 elektronen. Juist: 2/6.'), ('Chloor', 'juist: 2/8/7.')],
        'Vul eerst K (max 2), dan L (max 8), dan M (max 8). Controleer: som = Z.', fig([11, 8, 17], 0.8)))
EXTRA_A3 = (g['oef_fig']('opl_3', 3, 'Tekenen: drie edelgassen', 'Teken helium, neon en argon in het schillenmodel. Kleur de valentie-elektronen. Wat hebben de drie atomen gemeen? Waarom reageren ze (bijna) niet?',
        svg_(rij([2, 10, 18]), 640, 205),
        [('Helium', '2'), ('Neon', '2/8'), ('Argon', '2/8/8'), ('Gemeen', 'de buitenste schil is vol: edelgasconfiguratie, daarom zijn ze stabiel.')],
        'Edelgassen hebben een volle buitenste schil.', fig([2, 10, 18], 0.8))
    + g['oef_fig']('opl_3', 3, 'Tekenen: één groep, drie perioden', 'Teken lithium, natrium en kalium in het schillenmodel. Zoek ze op in het PSE. Wat is hetzelfde, en wat verschilt? Verbind met groep en periode.',
        svg_(rij([3, 11, 19]), 640, 205),
        [('Lithium', '2/1: 2 schillen, 1 valentie-elektron'), ('Natrium', '2/8/1: 3 schillen, 1 valentie-elektron'), ('Kalium', '2/8/8/1: 4 schillen, 1 valentie-elektron'),
         ('Besluit', 'zelfde groep (Ia) = evenveel valentie-elektronen; andere periode = ander aantal schillen.')],
        'Groep = valentie-elektronen, periode = schillen.', fig([3, 11, 19], 0.8)))
i2 = g['a2_oef'].index('<div class="oef" data-vrij="opl_3">'); g['a2_oef'] = g['a2_oef'][:i2] + EXTRA_A2 + g['a2_oef'][i2:]
i3 = g['a3_oef'].index('<div class="oef" data-vrij="opl_4">'); g['a3_oef'] = g['a3_oef'][:i3] + EXTRA_A3 + g['a3_oef'][i3:]

I = lambda tool_, naam, pse=False: (f'Werk dit hoofdstuk samen met de tool <a href="{tool_}">{naam}</a>.' + (' Gebruik je eigen PSE.' if pse else '')
                                    + ' Oefeningen maak je op papier. De oplossingen staan online, zodra ze in de les besproken zijn.')
LD = lambda doelen: '<p>Na dit hoofdstuk kan je:</p><ul class="doelen">' + ''.join(f'<li>{d}</li>' for d in doelen) + '</ul>'
OEF = lambda o, ref: g['oefblok'](g['hernummer'](o), ref)
SAM = lambda s: kader('Samenvatting', s)
T1, T2 = g['T1'], g['T2']

def P(bestand, eyebrow, titel, tool_, naam, pre, delen, c, eerste=False, pse=False):
    pagina(bestand, eyebrow, titel, I(tool_, naam, pse), LD(g[pre + '_doelen']), g[pre + '_vk'],
           [(k, g[f'{pre}_{i}']) for i, k in enumerate(delen, start=1)], OEF(g[pre + '_oef'], (tool_, 'Oefen verder in de tool')), SAM(g[pre + '_samenv']), c, eerste)

P('cursus-chemie-wetenschap.html', T1 + '1', 'Chemie als wetenschap', 'chemie-stoffen.html', 'Chemie en veiligheid', 'h1',
  ['Fysica of chemie?', 'Veilig werken: gevarensymbolen en H- en P-zinnen', 'Verantwoord omgaan met producten'], C['wet'], eerste=True)
P('cursus-chemie-mengsels.html', T1 + '2', 'Zuivere stoffen en mengsels', 'chemie-mengsels.html', 'Mengsels', 'h2',
  ['Zuivere stof, mengsel en bestanddeel', 'Soorten mengsels', 'Stofeigenschappen en voorwerpseigenschappen'], C['meng'])
P('cursus-chemie-scheidingstechnieken.html', T1 + '3', 'Scheidingstechnieken', 'chemie-scheidingstechnieken.html', 'Scheidingstechnieken', 'h3',
  ['Wat is een scheidingstechniek?', 'Heterogene mengsels scheiden', 'Homogene mengsels scheiden', 'Overzicht en voorbeelden uit Brussel en thuis'], C['scheid'])
P('cursus-chemie-atomen-elementen.html', T2 + '1', 'Atomen en elementen', 'chemie-atoommodellen.html', 'Atomen en elementen', 'a1',
  ['Het atoommodel als dynamisch model', 'Symbolen van de elementen'], C['atel'])
P('cursus-chemie-atoombouw.html', T2 + '2', 'Bouw van het atoom', 'chemie-atoombouw.html', 'Bouw van het atoom', 'a2',
  ['Bouwstenen van het atoom', 'Schillen en valentie-elektronen', 'Atoomnummer en massagetal', 'Absolute en relatieve atoommassa'], C['bouw'])
P('cursus-chemie-pse.html', T2 + '3', 'Het periodiek systeem', 'chemie-pse.html', 'Periodiek systeem', 'a3',
  ['Het PSE lezen en de categorieën', 'Groep en periode', 'Elektronegativiteit en edelgasconfiguratie', "Drie PSE's om af te drukken"], C['pse'], pse=True)
