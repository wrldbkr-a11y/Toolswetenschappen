# Cursussen fysica 3NW in het nieuwe formaat: optica (thema 1, hoofdstuk 1-4) en krachten (thema 2, hoofdstuk 2).
# Gebruik:  cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/nw3_nieuw.py
# Bestaande inhoud en figuren uit optica_cursus.py en derde_krachten.py; nieuwe inhoud in nw3_inhoud.py.
# Let op: aso_krachten.py gebruikt derde_krachten.py alleen tot 'delen = [' en overschrijft deze pagina's niet.
import re, sys
B = '/home/claude/toolswetenschappen/_bron/cursus/'
sys.path.insert(0, '/home/claude/cursus')
import bouw as BM
BM.FOOTER = 'Cursus fysica — gemaakt voor klasgebruik, bij de tools op Oefentools wetenschappen.'

# ---- optica: alle delen inlezen, de oude maak()-aanroepen opvangen in plaats van bouwen
g = {'__name__': 'optica'}
MAAK = []
src = open(B + 'optica_cursus.py', encoding='utf-8').read().replace('\nmaak(', '\n_MAAK(')
g['_MAAK'] = lambda *a, **k: MAAK.append(a)
exec(src, g)
exec(open(B + 'aso_veer.py', encoding='utf-8').read().split('GX, GY')[0], g)
exec(open(B + 'nw3_inhoud.py', encoding='utf-8').read(), g)
blok, oef, kader, tool, denk = g['blok'], g['oef'], g['kader'], g['tool'], g['denk']
EDI_CSS, edi, W = g['EDI_CSS'], g['edi'], g['wisbord']
AANPAK_SCHEMA = 'maak een schets en kies de juiste regel of formule: welke stralen of krachten heb je nodig, welke wet geldt?'
AANPAK_LEES = 'de gegevens (hoeken, afstanden, krachten) met hun eenheid'
exec(open(B + 'nieuw_formaat.py', encoding='utf-8').read())

def sub(x):
    """F_r → F<sub>r</sub> in alle teksten van de inhoud"""
    if isinstance(x, str): return re.sub(r'F_([a-zA-Z0-9]+)', r'F<sub>\1</sub>', x)
    if isinstance(x, (list, tuple)): return type(x)(sub(y) for y in x)
    if isinstance(x, dict): return {k: sub(v) for k, v in x.items()}
    return x
C = sub(g['C'])

LD = lambda doelen: '<p>Na dit hoofdstuk kan je:</p><ul class="doelen">' + ''.join(f'<li>{d}</li>' for d in doelen) + '</ul>'
SLEUTELS = ['zien', 'weerk', 'breking', 'lenzen']
for i, (bestand, eyebrow, titel, intro, doelen, vk, delen, oefeningen, samenv, *rest) in enumerate(MAAK):
    toolref = rest[0] if rest else None
    intro = intro.replace('Oefeningen maak je op papier.', 'Oefeningen maak je op papier. De oplossingen staan online, zodra ze in de les besproken zijn.')
    pagina(bestand, eyebrow, titel, intro, LD(doelen), vk, delen, g['oefblok'](g['hernummer'](oefeningen), toolref),
           kader('Samenvatting', samenv), C[SLEUTELS[i]], eerste=(i == 0))

# ---- krachten (thema 2, hoofdstuk 2)
k = {'__name__': 'krachten'}
exec(open(B + 'derde_krachten.py', encoding='utf-8').read().split('delen = [')[0], k)
k_delen = [('Effect van een kracht', k['d1']), ('Een kracht is een vector', k['d2']), ('Krachten samenstellen', k['d3']), ('Krachten ontbinden', k['d4']),
           ('Traagheid', k['k_traag']), ('Resulterende kracht en beweging', k['k_beweg'])]
pagina('cursus-krachten-beweging.html', 'Fysica 3de jaar · Thema 2 Krachten · Hoofdstuk 2', 'Krachten',
       'Werk dit hoofdstuk samen met de tools <a href="krachten-beweging.html">Krachten en beweging</a> en <a href="krachten-construeren.html">Krachten samenstellen en ontbinden</a>. Oefeningen maak je op papier. De oplossingen staan online, zodra ze in de les besproken zijn.',
       k['lesdoelen'], k['voorkennis'], k_delen, k['oefs'], k['samenv'], C['krachten'], eerste=True)
