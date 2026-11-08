# Cursus biologie 3de jaar · thema 1-3 (december) in het nieuwe formaat:
# het idee, Ken dit, uitgewerkt voorbeeld met het waarom, Let op, Test jezelf, wisbordvragen (leerkracht),
# oefeningen + uitdagingen (DOK 3, tips bouwen af), begrippenlijst. Geen schrijflijnen in de theorie.
# Oplossingen en redeneringen alleen online (vrijgave).
#
# Gebruik:  cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/bio3_nieuw.py
# (bio_cursus.py en bio2_cursus.py leveren de bestaande inhoud en figuren.)
import re, sys
B = '/home/claude/toolswetenschappen/_bron/cursus/'
sys.path.insert(0, '/home/claude/cursus')
import bouw as BM
BM.FOOTER = 'Cursus biologie — gemaakt voor klasgebruik, bij de tools op Oefentools wetenschappen.'

# ---- bestaande inhoud laden (zonder de oude bouwstappen)
g = {'__name__': 'bio2'}
exec(open(B + 'bio2_cursus.py', encoding='utf-8').read().split('I = lambda deel')[0], g)
w = {'__name__': 'bio1'}
_b1 = open(B + 'bio_cursus.py', encoding='utf-8').read()
exec(_b1.split("delen = [('deel1'")[0], w)
exec(_b1[_b1.index('cvr = ['):_b1.index("bouw('cursus-water")], w)      # Cornellvragen
exec(open(B + 'aso_veer.py', encoding='utf-8').read().split('GX, GY')[0], g)       # EDI_CSS, wisbord, edi
exec(open(B + 'bio3_inhoud.py', encoding='utf-8').read(), g)                      # C
blok, oef, kader, tool, denk = g['blok'], g['oef'], g['kader'], g['tool'], g['denk']
C, edi, W, EDI_CSS = g['C'], g['edi'], g['wisbord'], g['EDI_CSS']

AANPAK_SCHEMA = 'zet de stappen in volgorde, bv. met het schema prikkel → receptor → verwerking → effector → effect.'
AANPAK_LEES = 'de prikkel, het organisme'
exec(open(B + 'nieuw_formaat.py', encoding='utf-8').read())

# ---- T1 H1 waterhuishouding (bio_cursus.py)
w_delen = [('Waterhuishouding en plantenorganen', w['d1']), ('Aanpassingen van het blad', w['d2']), ('Gasuitwisseling via de huidmondjes', w['d3']),
           ('Aanpassingen van de stengel', w['d4']), ('Aanpassingen van de wortel', w['d5']), ('Water- en assimilatentransport', w['d6']),
           ('Homeostase van de waterhuishouding', w['d7'])]
w_oefs = w['oefs'].replace(' Druk ze af of maak ze in je schrift.', '')
pagina('cursus-waterhuishouding-planten.html', 'Biologie 3de jaar · Thema 1 Feedbacksystemen · Hoofdstuk 1', 'Homeostase van de waterhuishouding in planten',
       'Werk dit hoofdstuk samen met de tool <a href="biologie-prikkels.html">Water, prikkels en reacties</a>. Oefeningen maak je op papier. De oplossingen staan online, zodra ze in de les besproken zijn.' + w['css_extra'],
       w['lesdoelen'], w['voorkennis'], w_delen, w_oefs, w['samenv'], C['water'], eerste=True, cornell=w['cvr'])

# ---- de andere hoofdstukken (bio2_cursus.py)
TOOL = g['TOOL']
I = lambda d: f'Werk dit hoofdstuk samen met de tool <a href="{TOOL}{d}">Water, prikkels en reacties</a>. Oefeningen maak je op papier. De oplossingen staan online, zodra ze in de les besproken zijn.'
LD = lambda doelen: '<p>Na dit hoofdstuk kan je:</p><ul class="doelen">' + ''.join(f'<li>{d}</li>' for d in doelen) + '</ul>'
OEF = lambda o, ref: g['oefblok'](g['hernummer'](o), ref)
SAM = lambda s: kader('Samenvatting', s)
T1, T2, T3 = g['T1'], g['T2'], g['T3']
pagina('cursus-homeostase.html', T1 + '2', 'Homeostase en feedbacksystemen', I('#f1'), LD(g['b1_doelen']), g['b1_vk'],
       [('Een organisme als systeem', g['b1_1']), ('Homeostase', g['b1_2']), ('Negatieve en positieve feedback', g['b1_3'])], OEF(g['b1_oef'], (TOOL + '#f2', 'Oefen verder in de tool')), SAM(g['b1_sam']), C['homeo'])
pagina('cursus-receptoren.html', T2 + '1', 'Receptoren bij de mens', I('#r1'), LD(g['b2_doelen']), g['b2_vk'],
       [('Soorten receptoren', g['b2_1']), ('Prikkeldrempel en prikkelgewenning', g['b2_2']), ('De prikkelfilter', g['b2_3'])], OEF(g['b2_oef'], (TOOL + '#r1', 'Oefen verder in de tool')), SAM(g['b2_sam']), C['rec'])
pagina('cursus-oog.html', T2 + '2 en 3', 'Bouw en werking van het oog', I('#r3'), LD(g['b3_doelen']), g['b3_vk'],
       [('Bouw van het oog', g['b3_1']), ('De weg van het licht', g['b3_2']), ('Het netvlies: staafjes en kegeltjes', g['b3_3']), ('Beeldverwerking in de hersenen', g['b3_4'])],
       OEF(g['b3_oef'], (TOOL + '#r3', 'Oefen verder in de tool')), SAM(g['b3_sam']), C['oog'])
pagina('cursus-receptoren-organismen.html', T2 + '4', 'Receptoren bij andere organismen', I('#r8'), LD(g['b4_doelen']), g['b4_vk'],
       [('Receptoren bij dieren', g['b4_1']), ('Receptoren bij planten', g['b4_2'])], OEF(g['b4_oef'], (TOOL + '#r8', 'Bekijk de voorbeelden in de tool')), SAM(g['b4_sam']), C['org'])
pagina('cursus-reageren.html', T3 + '1', 'De mens reageert op prikkels', I('#e1'), LD(g['b5_doelen']), g['b5_vk'],
       [('Effectoren: spieren en klieren', g['b5_1'])], OEF(g['b5_oef'], (TOOL + '#e1', 'Oefen verder in de tool')), SAM(g['b5_sam']), C['reag'])
pagina('cursus-spieren.html', T3 + '2', 'Reactie door spieren', I('#e2'), LD(g['b6_doelen']), g['b6_vk'],
       [('Spieren, pezen en gewrichten', g['b6_1']), ('Soorten spierweefsel', g['b6_2']), ('Samentrekken en ontspannen', g['b6_3'])], OEF(g['b6_oef'], (TOOL + '#e4', 'Oefen verder in de tool')), SAM(g['b6_sam']), C['spier'])

# ---- T3 H3-H4 klieren en andere organismen
exec(open(B + 'bio3_klieren.py', encoding='utf-8').read())
