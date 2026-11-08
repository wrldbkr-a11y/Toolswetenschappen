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
