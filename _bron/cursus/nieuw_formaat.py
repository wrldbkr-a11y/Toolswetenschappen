# Gedeelde bouwstenen voor cursussen in het nieuwe formaat (biologie, chemie ...).
# Laden met:  exec(open(B + 'nieuw_formaat.py').read(), ns)  in een namespace met blok, oef, kader, tool, denk, BM, EDI_CSS, edi, wisbord.
# AANPAK_SCHEMA: de plan-stap in "Zo pak je een uitdaging aan" (vakspecifiek).
# ---- bouwstenen
IDEE_STIJL = 'background:#FEF9C3;border-left:4px solid #CA8A04;border-radius:0 10px 10px 0;padding:10px 14px;margin:6px 0 14px'
LET_STIJL = 'background:#FFF7ED;border-left:4px solid #D97706;border-radius:0 8px 8px 0;padding:8px 12px;margin:12px 0'
def idee(t_): return f'<div class="idee" style="{IDEE_STIJL}"><b style="color:#854D0E">Het idee.</b> {t_}</div>'
def letop(t_): return f'<div style="{LET_STIJL}"><b style="color:#B45309">Let op.</b> {t_}</div>'
def vb(titel, opgave, stappen):
    punt = '' if titel.endswith(('?', '!', '.')) else '.'
    return f'<p><b>Uitgewerkt voorbeeld · {titel}{punt}</b> {opgave}</p><ol>' + ''.join(f'<li><b>{s}:</b> {u}</li>' for s, u in stappen) + '</ol>'
def test(nr, vragen):
    q = '<b>Test jezelf.</b> Kan je dit uitleggen zonder in je cursus te kijken?' + ''.join(f'<br>{i}. {v}' for i, (v, _) in enumerate(vragen, start=1))
    return denk(f'denk_{100 + nr}', q, [(str(i + 1), a) for i, (_, a) in enumerate(vragen)], 'Lukt het niet? Lees het idee en het uitgewerkte voorbeeld opnieuw.')
def drie(start, tijdens, einde):
    ol = lambda l: '<ol>' + ''.join(W(*v) for v in l) + '</ol>'
    return edi([('Start', ol(start)), ('Tijdens de uitleg', ol(tijdens)), ('Einde', ol(einde))])
def aanpak(t_): return f'<p style="margin-top:6px;font-size:.95em;color:#475569"><i>Tip voor de aanpak:</i> {t_}</p>'
AANPAK = kader('Zo pak je een uitdaging aan', f'''<p>Deze oefeningen combineren leerstof. Vlieg er niet blind in. De tips worden telkens korter: bij de laatste oefening kies je de aanpak zelf.</p>
<ol><li><b>Lees</b> de opgave twee keer. Onderstreep {AANPAK_LEES} en de vraag.</li>
<li><b>Analyseer:</b> welke leerstof heb je nodig (welk deel, welk hoofdstuk)?</li>
<li><b>Plan:</b> {AANPAK_SCHEMA}</li>
<li><b>Leg uit</b> met de juiste vaktermen.</li>
<li><b>Controleer:</b> beantwoord je echt de vraag? Is je uitleg logisch?</li></ol>''')
STEUN = '<p style="font-size:.93em;color:#475569;margin:10px 0 4px">🧭 <i>Zo pak je een uitdaging aan: lees · analyseer · plan · leg uit met vaktermen · controleer.</i></p>'

def denkstappen(titel, stappen):
    return kader('Denkstappen · ' + titel, '<ol>' + ''.join(f'<li><b>{v}</b> {u}</li>' for v, u in stappen) + '</ol>')
def geheugensteun(t_): return f'<p style="font-size:.93em;color:#475569;margin:10px 0">🧭 <i>{t_}</i></p>'
def stappenplannen(s):
    """<h3>Stappenplan: X</h3><ol>…</ol> → kader Denkstappen · X"""
    return re.sub(r'<h3>Stappenplan: ([^<]*)</h3>\s*(<ol>.*?</ol>)', lambda m: kader('Denkstappen · ' + m.group(1)[0].upper() + m.group(1)[1:], m.group(2)), s, flags=re.S)

def ken(s):
    """kaders als vaste soort: Ken dit (leerstof) of Voorbeeld (leefwereld)"""
    def f(m):
        k = m.group(1)
        if k.startswith(('Ken dit', 'Samenvatting', 'Voorbeeld', 'Let op', 'Zo pak', 'Denkstappen')): return m.group(0)
        k2 = 'Voorbeeld · ' + k if k.startswith('Brussel') else ('Ken dit' if k == 'Onthoud' else 'Ken dit · ' + k)
        return f'<div class="kader"><div class="kop">{k2}</div>'
    return re.sub(r'<div class="kader"><div class="kop">([^<]*)</div>', f, s)

def voor_tool(s, extra):
    i = s.rfind('<a class="toolknop"')
    return s[:i] + extra + s[i:] if i >= 0 else s + extra

def deel(inh, d, nr):
    inh = ken(stappenplannen(inh))
    if d is None: return inh
    inh = re.sub(r'<div class="schrijflijnen">(?:<div></div>)*</div>', '', inh)   # geen invulboek
    inh = inh.replace('<p>Let op het verschil: ', '<p>Het verschil: ')
    m = re.match(r'\s*<div class="voorkennis">.*?</ul></div>', inh, re.S)
    kop = m.group(0) if m else ''
    rest = inh[len(kop):]
    extra = ((denkstappen(*d['stappen']) if d.get('stappen') else '') + (geheugensteun(d['steun']) if d.get('steun') else '')
             + (vb(*d['vb']) if d.get('vb') else '')) + (letop(d['letop']) if d.get('letop') else '')
    return drie(*d['wb']) + kop + idee(d['idee']) + voor_tool(rest, extra) + test(nr, d['test'])

def uitdagingen(lijst, eerste):
    s = '<h3 style="margin-top:28px">Uitdagingen</h3>' + (AANPAK if eerste else STEUN)
    for i, (titel, tekst, stappen, besluit, tip) in enumerate(lijst, start=1):
        s += oef(f'opl_u{i}', f'U{i}', titel.replace('Uitdaging · ', ''), tekst + (aanpak(tip) if tip else ''), stappen, besluit)
    return s

exec(open('/home/claude/toolswetenschappen/_bron/cursus/zinnen_inhoud.py', encoding='utf-8').read())
def zinnen_oef(bestand, eerste, nr):
    """oefening: een redenering met pijlen in correcte zinnen met verbindingswoorden schrijven"""
    lijst = Z.get(bestand)
    if not lijst: return ''
    kop = (kader('Ken dit · Van pijlen naar zinnen', VERBIND) if eerste else
           '<p style="font-size:.93em;color:#475569;margin:10px 0 4px">✍️ <i>Van pijlen naar zinnen: gebruik omdat, doordat, want, dus, daardoor, daarom, zodat, als … dan.</i></p>')
    tekst = ('Schrijf de redenering in correcte Nederlandse zinnen. Gebruik verbindingswoorden.<ol class="deelvragen" type="a">'
             + ''.join(f'<li>{keten}</li>' for keten, _ in lijst) + '</ol>')
    return kop + oef(f'opl_{nr}', nr, 'Van pijlen naar zinnen', tekst, [(chr(97 + i), m) for i, (_, m) in enumerate(lijst)],
                     'Andere zinnen kunnen ook juist zijn, als de verbindingswoorden kloppen.')

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
    oefeningen += zinnen_oef(bestand, eerste, oefeningen.count('class="oef"') + 1)
    blokken += [blok('oefeningen', '', 'Oefeningen op papier', oefeningen + uitdagingen(c['uitd'], eerste), 'oefeningen'),
                blok('begrippen', '', 'Begrippenlijst', begrippen(c['begrip'])),
                blok('samenvatting', '', 'Samenvatting', samenv, 'samenvatting')]
    BM.bouw(bestand, eyebrow, titel, intro, blokken, vrijgave(blokken, delen), cornell or [])
    print('gemaakt:', bestand)

