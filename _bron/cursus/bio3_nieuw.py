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

# ---- bouwstenen
IDEE_STIJL = 'background:#FEF9C3;border-left:4px solid #CA8A04;border-radius:0 10px 10px 0;padding:10px 14px;margin:6px 0 14px'
LET_STIJL = 'background:#FFF7ED;border-left:4px solid #D97706;border-radius:0 8px 8px 0;padding:8px 12px;margin:12px 0'
def idee(t_): return f'<div class="idee" style="{IDEE_STIJL}"><b style="color:#854D0E">Het idee.</b> {t_}</div>'
def letop(t_): return f'<div style="{LET_STIJL}"><b style="color:#B45309">Let op.</b> {t_}</div>'
def vb(titel, opgave, stappen):
    punt = '' if titel.endswith(('?', '!', '.')) else '.'
    return f'<p><b>Uitgewerkt voorbeeld · {titel}{punt}</b> {opgave}</p><ol>' + ''.join(f'<li><b>{s}:</b> {u}</li>' for s, u in stappen) + '</ol>'
def test(nr, vragen):
    q = '<b>Test jezelf.</b> Kan je dit uitleggen zonder in je cursus te kijken?<ol>' + ''.join(f'<li>{v}</li>' for v, _ in vragen) + '</ol>'
    return denk(f'denk_{100 + nr}', q, [(str(i + 1), a) for i, (_, a) in enumerate(vragen)], 'Lukt het niet? Lees het idee en het uitgewerkte voorbeeld opnieuw.')
def drie(start, tijdens, einde):
    ol = lambda l: '<ol>' + ''.join(W(*v) for v in l) + '</ol>'
    return edi([('Start', ol(start)), ('Tijdens de uitleg', ol(tijdens)), ('Einde', ol(einde))])
def aanpak(t_): return f'<p style="margin-top:6px;font-size:.95em;color:#475569"><i>Tip voor de aanpak:</i> {t_}</p>'
AANPAK = kader('Zo pak je een uitdaging aan', '''<p>Deze oefeningen combineren leerstof. Vlieg er niet blind in. De tips worden telkens korter: bij de laatste oefening kies je de aanpak zelf.</p>
<ol><li><b>Lees</b> de opgave twee keer. Onderstreep de prikkel, het organisme en de vraag.</li>
<li><b>Analyseer:</b> welke leerstof heb je nodig (welk deel, welk hoofdstuk)?</li>
<li><b>Plan:</b> zet de stappen in volgorde, bv. met het schema prikkel → receptor → verwerking → effector → effect.</li>
<li><b>Leg uit</b> met de juiste vaktermen.</li>
<li><b>Controleer:</b> beantwoord je echt de vraag? Is je uitleg logisch?</li></ol>''')
STEUN = '<p style="font-size:.93em;color:#475569;margin:10px 0 4px">🧭 <i>Zo pak je een uitdaging aan: lees · analyseer · plan · leg uit met vaktermen · controleer.</i></p>'

def ken(s):
    """kaders als vaste soort: Ken dit (leerstof) of Voorbeeld (leefwereld)"""
    def f(m):
        k = m.group(1)
        if k.startswith(('Ken dit', 'Samenvatting', 'Voorbeeld', 'Let op', 'Zo pak')): return m.group(0)
        k2 = 'Voorbeeld · ' + k if k.startswith('Brussel') else ('Ken dit' if k == 'Onthoud' else 'Ken dit · ' + k)
        return f'<div class="kader"><div class="kop">{k2}</div>'
    return re.sub(r'<div class="kader"><div class="kop">([^<]*)</div>', f, s)

def voor_tool(s, extra):
    i = s.rfind('<a class="toolknop"')
    return s[:i] + extra + s[i:] if i >= 0 else s + extra

def deel(inh, d, nr):
    inh = ken(inh)
    inh = re.sub(r'<div class="schrijflijnen">(?:<div></div>)*</div>', '', inh)   # geen invulboek
    inh = inh.replace('<p>Let op het verschil: ', '<p>Het verschil: ')
    m = re.match(r'\s*<div class="voorkennis">.*?</ul></div>', inh, re.S)
    kop = m.group(0) if m else ''
    rest = inh[len(kop):]
    extra = vb(*d['vb']) + (letop(d['letop']) if d.get('letop') else '')
    return drie(*d['wb']) + kop + idee(d['idee']) + voor_tool(rest, extra) + test(nr, d['test'])

def uitdagingen(lijst, eerste):
    s = '<h3 style="margin-top:28px">Uitdagingen</h3>' + (AANPAK if eerste else STEUN)
    for i, (titel, tekst, stappen, besluit, tip) in enumerate(lijst, start=1):
        s += oef(f'opl_u{i}', f'U{i}', titel.replace('Uitdaging · ', ''), tekst + (aanpak(tip) if tip else ''), stappen, besluit)
    return s

def begrippen(lijst):
    return ('<p>Weet je niet meer wat een woord betekent? Zoek het hier op.</p><table class="vb grid">'
            + ''.join(f'<tr><th style="text-align:left;white-space:nowrap">{a}</th><td>{b}</td></tr>' for a, b in lijst) + '</table>')

def vrijgave(blokken, delen):
    alle = ''.join(blokken); uit, gezien = [], set()
    for x in re.findall(r'data-vrij="([^"]+)"', alle):
        if x in gezien: continue
        gezien.add(x)
        if x.startswith('deel'): uit.append((x, x == 'deel1', delen[int(x[4:]) - 1][0]))
        elif x == 'vk_opl': uit.append((x, True, 'oplossing controlevragen voorkennis'))
        elif x.startswith('denk_') and x[5:].isdigit() and int(x[5:]) > 100: uit.append((x, False, f'antwoorden Test jezelf, deel {int(x[5:]) - 100}'))
        elif x.startswith('denk_'): uit.append((x, False, 'redenering ' + x.replace('_', 'vraag ')))
        elif x.startswith('opl_u'): uit.append((x, False, 'oplossing uitdaging ' + x[5:]))
        elif x.startswith('opl_'): uit.append((x, False, 'oplossing oefening ' + x[4:]))
        else: uit.append((x, False, x))
    return uit

def pagina(bestand, eyebrow, titel, intro, lesdoelen, voorkennis, delen, oefeningen, samenv, c, eerste=False, cornell=None):
    assert len(delen) == len(c['delen']), bestand
    blokken = [blok('lesdoelen', '', 'Lesdoelen', lesdoelen), blok('voorkennis', '', 'Voorkennis', voorkennis)]
    for i, (k, inh) in enumerate(delen, start=1):
        inh = deel(inh, c['delen'][i - 1], i)
        if i == 1: inh = EDI_CSS + inh
        blokken.append(blok(f'deel{i}', i, k, inh, f'deel{i}'))
    blokken += [blok('oefeningen', '', 'Oefeningen op papier', oefeningen + uitdagingen(c['uitd'], eerste), 'oefeningen'),
                blok('begrippen', '', 'Begrippenlijst', begrippen(c['begrip'])),
                blok('samenvatting', '', 'Samenvatting', samenv, 'samenvatting')]
    BM.bouw(bestand, eyebrow, titel, intro, blokken, vrijgave(blokken, delen), cornell or [])
    print('gemaakt:', bestand)

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
