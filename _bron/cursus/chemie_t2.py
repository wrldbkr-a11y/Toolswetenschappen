# thema 2 (wordt via exec ingelezen door chemie_cursus.py)
PROT, NEUT, ELEK, VAL = '#ef4444', '#94a3b8', '#2563eb', '#facc15'
ROM = {1: 'Ia', 2: 'IIa', 13: 'IIIa', 14: 'IVa', 15: 'Va', 16: 'VIa', 17: 'VIIa', 18: 'VIIIa'}

def schillen(z):
    s, cap = [], [2, 8, 8, 2]
    for c in cap:
        if z <= 0: break
        s.append(min(c, z)); z -= min(c, z)
    return s

def bohr(Z, cx, cy, schaal=1.0, naam=True, kerntekst=True, valentie=True, leeg=False, n=None):
    e = ELZ[Z]; sch = schillen(Z); n = e['A'] - Z if n is None else n
    R = [r * schaal for r in (0, 34, 54, 74, 94)]
    o = ''
    for i in range(1, len(sch) + 1):
        o += f'<circle cx="{cx}" cy="{cy}" r="{R[i]:.1f}" fill="none" stroke="#94a3b8" stroke-width="1.6"/>'
        o += t(cx + R[i] * 0.71 + 3, cy - R[i] * 0.71 - 3, 'KLMN'[i - 1], GRIJS, 'start', 10, 600)
    kr = 20 * schaal
    o += f'<circle cx="{cx}" cy="{cy}" r="{kr:.1f}" fill="#fee2e2" stroke="{INK}" stroke-width="1.4"/>'
    if kerntekst and schaal >= 0.7:
        o += t(cx, cy - 2, f'{Z} p⁺', ROOD, size=10 * schaal + 1) + t(cx, cy + 10 * schaal, f'{n} n⁰', GRIJS, size=10 * schaal + 1)
    if not leeg:
        for i, cnt in enumerate(sch):
            laatste = i == len(sch) - 1
            for k in range(cnt):
                a = -math.pi / 2 + k * 2 * math.pi / cnt + i * 0.3
                o += f'<circle cx="{cx + R[i+1]*math.cos(a):.1f}" cy="{cy + R[i+1]*math.sin(a):.1f}" r="{5*schaal:.1f}" fill="{VAL if laatste and valentie else ELEK}" stroke="{INK}" stroke-width="1"/>'
    if naam:
        o += t(cx, cy + R[len(sch)] + 20, f'{e["naam"]} ({e["s"]}) · {"/".join(map(str, sch))}', INK, size=13)
    return o

def fig_bohr(zs, schaal=0.8, w=640, h=None, **kw):
    n = len(zs); h = h or int(200 * schaal + 60)
    return svg(''.join(bohr(z, w / n * (i + .5), h / 2 - 12, schaal, **kw) for i, z in enumerate(zs)), w, h)

def fig_modellen():
    o = ''; xs = [55, 160, 265, 370, 475, 578]; y = 80
    # Democritus: ondeelbaar bolletje (idee)
    o += f'<circle cx="{xs[0]}" cy="{y}" r="30" fill="#e2e8f0" stroke="{INK}" stroke-width="2" stroke-dasharray="5 4"/>'
    # Dalton: massief bolletje
    o += f'<circle cx="{xs[1]}" cy="{y}" r="30" fill="#94a3b8" stroke="{INK}" stroke-width="2"/><circle cx="{xs[1]-10}" cy="{y-10}" r="8" fill="#e2e8f0" opacity=".7"/>'
    # Thomson: positieve bol met elektronen (krenten) erin; plus- en mintekens binnen de bol
    def el(x, y):
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{ELEK}"/>' + t(x, y + 3.5, '−', '#fff', size=11, w=800)
    o += f'<circle cx="{xs[2]}" cy="{y}" r="34" fill="#fecaca" stroke="{INK}" stroke-width="2"/>'
    for dx, dy in ((-15, -14), (12, -18), (19, 7), (-5, 17), (-21, 7), (3, -1)):
        o += el(xs[2] + dx, y + dy)
    for dx, dy in ((-2, -22), (20, -6), (-14, -1), (9, 15), (-17, 20), (24, 18)):
        o += t(xs[2] + dx, y + dy + 4, '+', ROOD, size=12, w=800)
    # Rutherford: kleine positieve kern, negatieve elektronen in veel lege ruimte
    o += f'<circle cx="{xs[3]}" cy="{y}" r="36" fill="none" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3 4"/><circle cx="{xs[3]}" cy="{y}" r="8" fill="{PROT}"/>' + t(xs[3], y + 4.5, '+', '#fff', size=13, w=800)
    for a in (20, 140, 250, 320):
        o += el(xs[3] + 29 * math.cos(math.radians(a)), y + 25 * math.sin(math.radians(a)))
    # Bohr: schillen
    o += f'<circle cx="{xs[4]}" cy="{y}" r="18" fill="none" stroke="#94a3b8" stroke-width="1.5"/><circle cx="{xs[4]}" cy="{y}" r="34" fill="none" stroke="#94a3b8" stroke-width="1.5"/><circle cx="{xs[4]}" cy="{y}" r="7" fill="{PROT}"/>'
    for r, a in ((18, 90), (18, 270), (34, 0), (34, 120), (34, 240)):
        o += f'<circle cx="{xs[4]+r*math.cos(math.radians(a)):.1f}" cy="{y+r*math.sin(math.radians(a)):.1f}" r="4.5" fill="{ELEK}"/>'
    # wolk
    o += f'<defs><radialGradient id="wolk"><stop offset="0" stop-color="{ELEK}" stop-opacity=".75"/><stop offset="1" stop-color="{ELEK}" stop-opacity="0"/></radialGradient></defs><circle cx="{xs[5]}" cy="{y}" r="38" fill="url(#wolk)"/><circle cx="{xs[5]}" cy="{y}" r="5" fill="{PROT}"/>'
    namen = [('± 400 v.C.', 'Democritus', 'atomos-idee'), ('1803', 'Dalton', 'bolletjesmodel'), ('1904', 'Thomson', 'krentenbolmodel'),
             ('1911', 'Rutherford', 'kernmodel'), ('1913', 'Bohr', 'schillenmodel'), ('1926', 'Schrödinger', 'elektronenwolkmodel')]
    o += lijn(20, 150, 625, 150, INK, 2) + kop(630, 150, 0, INK)
    for x, (j, n, m) in zip(xs, namen):
        o += punt(x, 150, INK, 4) + t(x, 172, j, GRIJS, size=12) + t(x, 190, n, INK, size=13) + t(x, 206, m, BLAUW, size=11, w=600)
    return svg(o, 640, 215)

def fig_notatie(s='Na', A=23, Z=11):
    o = t(380, 125, s, INK, size=90, w=800) + t(312, 72, str(A), ROOD, 'end', 34) + t(312, 148, str(Z), BLAUW, 'end', 34)
    o += straal(200, 62, 262, 62, ROOD, 2, pos=1) + t(190, 58, 'massagetal A', ROOD, 'end', 14) + t(190, 76, '= protonen + neutronen', ROOD, 'end', 12, 600)
    o += straal(200, 140, 262, 140, BLAUW, 2, pos=1) + t(190, 136, 'atoomnummer Z', BLAUW, 'end', 14) + t(190, 154, '= aantal protonen', BLAUW, 'end', 12, 600)
    o += t(520, 90, 'symbool', INK, 'start', 14) + straal(515, 85, 455, 95, INK, 2, pos=1)
    o += t(320, 190, f'{Z} protonen · {Z} elektronen · {A} − {Z} = {A-Z} neutronen', INK, size=14)
    return svg(o, 640, 205)

KAT = {'m': '#bfdbfe', 'nm': '#bbf7d0', 'eg': '#fde68a'}
def fig_pse(kleur=True, en=False, tekst=True, markeer=(), perioden=5):
    cw, ch, x0, y0 = 70, 52, 50, 40
    kol = [1, 2, 13, 14, 15, 16, 17, 18]
    o = ''
    for i, g in enumerate(kol):
        o += t(x0 + i * cw + cw / 2, y0 - 10, ROM[g], GRIJS, size=13)
    for p in range(1, perioden + 1):
        o += t(x0 - 14, y0 + (p - 1) * ch + ch / 2 + 5, str(p), GRIJS, size=13)
    for e in EL.values():
        if e['p'] > perioden or e['g'] not in kol: continue
        x, y = x0 + kol.index(e['g']) * cw, y0 + (e['p'] - 1) * ch
        f = KAT[e['cat']] if kleur else '#fff'
        sw = 3 if e['s'] in markeer else 1.2
        o += f'<rect x="{x+2}" y="{y+2}" width="{cw-4}" height="{ch-4}" rx="5" fill="{f}" stroke="{ROOD if e["s"] in markeer else "#64748b"}" stroke-width="{sw}"/>'
        o += t(x + 8, y + 15, str(e['Z']), GRIJS, 'start', 10, 600)
        if tekst: o += t(x + cw / 2, y + 35, e['s'], INK, size=17, w=800)
        if en and e['en']: o += t(x + cw - 7, y + 15, f"{e['en']:.1f}".replace('.', ','), ROOD, 'end', 10, 700)
    # trap tussen metalen en niet-metalen (a-groepen): na Be|B, Al|Si, Ge|As, Sb|Te
    trap = [(2, 2, 2), (3, 3, 3), (4, 4, 4), (5, 5, 5)]  # (periode, index kolom waar niet-metaal start)
    pts = [(x0 + 2 * cw, y0 + ch)]
    for p, k, _ in trap:
        pts += [(x0 + k * cw, y0 + (p - 1) * ch), (x0 + k * cw, y0 + p * ch)]
        if p < perioden: pts.append((x0 + (k + 1) * cw, y0 + p * ch))
    pts = [pp for pp in pts if pp[1] <= y0 + perioden * ch]
    o += '<polyline points="' + ' '.join(f'{a},{b}' for a, b in pts) + f'" fill="none" stroke="{ROOD}" stroke-width="4"/>'
    if kleur:
        for i, (k, n) in enumerate((('m', 'metalen'), ('nm', 'niet-metalen'), ('eg', 'edelgassen'))):
            o += f'<rect x="{x0 + 8*cw + 22}" y="{y0 + 10 + i*28}" width="20" height="18" rx="3" fill="{KAT[k]}" stroke="#64748b"/>' + t(x0 + 8 * cw + 48, y0 + 24 + i * 28, n, INK, 'start', 13)
        o += lijn(x0 + 8 * cw + 22, y0 + 104, x0 + 8 * cw + 42, y0 + 104, ROOD, 4) + t(x0 + 8 * cw + 48, y0 + 108, 'trap', INK, 'start', 13)
    if en:
        yb = y0 + perioden * ch + 22
        o += straal(x0, yb, x0 + 7 * cw, yb, ROOD, 2.5, pos=1) + t(x0 + 3.5 * cw, yb + 18, 'EN stijgt naar rechts in een periode', ROOD, size=12)
        o += straal(x0 + 8 * cw + 30, y0 + perioden * ch - 10, x0 + 8 * cw + 30, y0 + 130, ROOD, 2.5, pos=1) + t(x0 + 8 * cw + 42, y0 + 170, 'EN stijgt', ROOD, 'start', 12) + t(x0 + 8 * cw + 42, y0 + 186, 'naar boven', ROOD, 'start', 12)
    return svg(o, 760, y0 + perioden * ch + (50 if en else 12)).replace('width="760"', 'width="640"')

def fig_vakje(s='Na'):
    e = EL[s]
    o = f'<rect x="230" y="20" width="180" height="180" rx="12" fill="{KAT[e["cat"]]}" stroke="{INK}" stroke-width="2"/>'
    o += t(248, 52, str(e['Z']), INK, 'start', 22) + t(392, 52, f"{e['en']:.1f}".replace('.', ','), INK, 'end', 18)
    o += t(320, 125, s, INK, size=64, w=800) + t(320, 158, e['naam'], INK, size=16, w=600) + t(320, 186, f"{e['Ar']:.1f}".replace('.', ','), INK, size=18)
    o += t(210, 50, 'atoomnummer Z', BLAUW, 'end', 14) + straal(214, 46, 244, 46, BLAUW, 2, pos=1)
    o += t(430, 50, 'elektronegativiteit', BLAUW, 'start', 14) + straal(426, 46, 398, 46, BLAUW, 2, pos=1)
    o += t(430, 118, 'symbool', BLAUW, 'start', 14) + straal(426, 114, 365, 108, BLAUW, 2, pos=1)
    o += t(430, 160, 'naam', BLAUW, 'start', 14) + straal(426, 156, 360, 154, BLAUW, 2, pos=1)
    o += t(210, 188, 'relatieve atoommassa Ar', BLAUW, 'end', 14) + straal(214, 184, 292, 182, BLAUW, 2, pos=1)
    return svg(o, 640, 215)

# ================================================================ T2 H1 ATOMEN EN ELEMENTEN
a1_doelen = ['uitleggen waarom het atoommodel een <b>dynamisch model</b> is;',
             'de namen van de <b>atoommodellen</b> en hun kenmerken noteren en ze <b>chronologisch</b> rangschikken;',
             'het <b>chemisch symbool</b> noteren als de naam gegeven is, en omgekeerd.']
a1_vk = vk('Het <b>deeltjesmodel</b>: alle stoffen bestaan uit heel kleine deeltjes.', 'Zuivere stof en mengsel (thema 1).', 'Een <b>model</b> is een vereenvoudigde voorstelling van de werkelijkheid.')
a1_1 = f'''<p>Een atoom is zo klein dat niemand het echt kan zien: op de dikte van een blad papier passen ongeveer een miljoen atomen naast elkaar. Daarom maken wetenschappers een <b>atoommodel</b>: een vereenvoudigde voorstelling van hoe een atoom eruitziet.</p>
{kader('Onthoud', '<p>Het atoommodel is <b>dynamisch</b>: het verandert telkens als nieuwe experimenten nieuwe dingen tonen. Een oud model wordt dan aangepast of vervangen.</p><p>Let op: "dynamisch" betekent hier <b>niet</b> dat atomen bewegen. Het betekent dat het <b>model</b> verandert in de loop van de tijd.</p>')}
{figuur(fig_modellen(), 'De atoommodellen door de tijd. Elektronen zijn blauw, positieve lading rood.')}
{ttabel(['Model', 'Wie en wanneer', 'Kenmerk', 'Waarom een nieuw model?'], [
  ['atomos-idee', 'Democritus, ± 400 v.C.', 'alles bestaat uit ondeelbare deeltjes: atomen', 'alleen een idee, geen experimenten'],
  ['bolletjesmodel', 'Dalton, 1803', 'een atoom is een massief, ondeelbaar bolletje; elk element heeft zijn eigen soort atomen', 'Thomson ontdekte het elektron: het atoom is dus deelbaar'],
  ['krentenbolmodel', 'Thomson, 1904', 'een positief geladen bol met negatieve elektronen erin, zoals krenten in een krentenbol', 'goudfolie-experiment van Rutherford'],
  ['kernmodel', 'Rutherford, 1911', 'een heel kleine, positieve <b>kern</b>; de elektronen bewegen errond; het atoom is vooral lege ruimte', 'waarom vallen de elektronen niet in de kern?'],
  ['schillenmodel', 'Bohr, 1913', 'de elektronen bewegen op vaste afstanden rond de kern: de <b>schillen</b>', 'elektronen hebben geen vaste baan'],
  ['elektronenwolkmodel', 'Schrödinger, 1926', 'je weet alleen waar een elektron waarschijnlijk is: een <b>wolk</b>', 'het huidige model']])}
<p>Wij werken verder met het <b>model van Bohr</b>: het is eenvoudig en goed genoeg voor wat we doen.</p>
{tool('chemie-atoommodellen.html', 'Klik door de tijdlijn van de atoommodellen')}
{denk('denk_1', 'Rutherford schoot heel kleine positieve deeltjes op een dun goudfolie. Bijna alle deeltjes gingen er rechtdoor. Een paar kaatsten terug. Wat besloot hij?', [
  ('Bijna alles rechtdoor', 'Het atoom is vooral lege ruimte.'),
  ('Een paar terug', 'Ze botsten op iets heel kleins, zwaars en positiefs: de kern.'),
  ('Gevolg', 'Het krentenbolmodel van Thomson klopte niet meer.')], 'Het atoom heeft een kleine positieve kern met veel lege ruimte errond: het kernmodel.')}'''
a1_2 = f'''<p>Een <b>element</b> is een soort atoom. Elk element heeft een <b>chemisch symbool</b>.</p>
{kader('De regels', '<ul><li>Een symbool heeft <b>1 of 2 letters</b>.</li><li>De eerste letter is altijd een <b>hoofdletter</b>.</li><li>De tweede letter is altijd een <b>kleine letter</b>.</li></ul><p><b>Co</b> is kobalt (een element). <b>CO</b> is koolstofmonoxide (een stof uit C en O). Eén hoofdletter maakt het verschil.</p>')}
<h3>Symbolen uit het Latijn</h3>
{ttabel(['Symbool', 'Naam', 'Latijn'], [['Na', 'natrium', 'natrium'], ['K', 'kalium', 'kalium'], ['Fe', 'ijzer', 'ferrum'], ['Cu', 'koper', 'cuprum'], ['Ag', 'zilver', 'argentum'], ['Au', 'goud', 'aurum'], ['Hg', 'kwik', 'hydrargyrum'], ['Pb', 'lood', 'plumbum'], ['Sn', 'tin', 'stannum']])}
<h3>De elementen 1 tot 20</h3>
{ttabel(['Z', 'Symbool', 'Naam', 'Z', 'Symbool', 'Naam'], [[ELZ[z]['Z'], ELZ[z]['s'], ELZ[z]['naam'], ELZ[z+10]['Z'], ELZ[z+10]['s'], ELZ[z+10]['naam']] for z in range(1, 11)])}
{tool('chemie-atoommodellen.html#les12', 'Leer de symbolen met de tegels in de tool')}
{denk('denk_2', 'Een leerling schrijft het symbool van chloor als "CL". Waarom is dat fout?', [
  ('Regel', 'De tweede letter is altijd een kleine letter.'), ('Gevolg', 'CL lijkt op twee elementen C en L, en L bestaat niet.')], 'Chloor schrijf je Cl.')}'''
a1_oef = f'''{oef('opl_1', 1, 'Dynamisch model', 'Leg in je eigen woorden uit waarom het atoommodel een dynamisch model is. Wat betekent "dynamisch" hier <b>niet</b>?', [
  ('Dynamisch', 'Het model verandert telkens als nieuwe experimenten nieuwe dingen tonen.'), ('Niet', 'Het betekent niet dat atomen bewegen.')], 'Het model verandert, niet het atoom.')}
{oef('opl_2', 2, 'Chronologisch rangschikken', 'Zet de modellen in de juiste volgorde: <i>schillenmodel – bolletjesmodel – elektronenwolkmodel – kernmodel – atomos-idee – krentenbolmodel</i>. Noteer bij elk de wetenschapper.', [
  ('Volgorde', 'atomos-idee (Democritus) → bolletjesmodel (Dalton) → krentenbolmodel (Thomson) → kernmodel (Rutherford) → schillenmodel (Bohr) → elektronenwolkmodel (Schrödinger)')], 'D – D – T – R – B – S.')}
{oef_fig('opl_3', 3, 'Welk model?', 'Noteer de naam van elk atoommodel.', fig_modellen().replace('Democritus', '?').replace('Dalton', '?').replace('Thomson', '?').replace('Rutherford', '?').replace('>Bohr<', '>?<').replace('Schrödinger', '?').replace('atomos-idee', '').replace('bolletjesmodel', '').replace('krentenbolmodel', '').replace('elektronenwolkmodel', '').replace('kernmodel', '').replace('schillenmodel', ''), [
  ('Van links naar rechts', 'atomos-idee · bolletjesmodel · krentenbolmodel · kernmodel · schillenmodel · elektronenwolkmodel')], 'Kijk naar de kern, de schillen en de plaats van de elektronen.', fig_modellen())}
{oef('opl_4', 4, 'Kenmerken', 'Bij welk model hoort de zin?<ol class="deelvragen" type="a"><li>Het atoom is een positieve bol met elektronen erin.</li><li>Elektronen bewegen op vaste afstanden van de kern.</li><li>Het atoom is vooral lege ruimte met een kleine kern.</li><li>Een atoom is een massief bolletje.</li><li>Je weet alleen waar een elektron waarschijnlijk is.</li></ol>', [
  ('a', 'krentenbolmodel (Thomson)'), ('b', 'schillenmodel (Bohr)'), ('c', 'kernmodel (Rutherford)'), ('d', 'bolletjesmodel (Dalton)'), ('e', 'elektronenwolkmodel (Schrödinger)')], 'Elk model voegt iets nieuws toe.')}
{oef('opl_5', 5, 'Symbool en naam', 'Noteer het symbool of de naam.<ol class="deelvragen" type="a"><li>zuurstof</li><li>Fe</li><li>natrium</li><li>Ca</li><li>koper</li><li>Pb</li><li>stikstof</li><li>Ag</li><li>chloor</li><li>Hg</li><li>kalium</li><li>Au</li></ol>', [
  ('a–d', 'O · ijzer · Na · calcium'), ('e–h', 'Cu · lood · N · zilver'), ('i–l', 'Cl · kwik · K · goud')], 'Leer vooral de Latijnse symbolen goed.')}
{oef('opl_6', 6, 'Juist of fout geschreven?', 'Is het symbool juist geschreven? Verbeter waar nodig.<ol class="deelvragen" type="a"><li>MG (magnesium)</li><li>s (zwavel)</li><li>Ne (neon)</li><li>CO (kobalt)</li><li>He (helium)</li></ol>', [
  ('a', 'fout: Mg'), ('b', 'fout: S'), ('c', 'juist'), ('d', 'fout: Co (CO is koolstofmonoxide)'), ('e', 'juist')], 'Hoofdletter + kleine letter.')}
{oef('opl_7', 7, 'Redeneren: het model van Thomson', 'Waarom was het krentenbolmodel van Thomson na het goudfolie-experiment niet meer goed?', [
  ('Thomson', 'De positieve lading is gelijk verdeeld over de hele bol.'), ('Experiment', 'Een paar deeltjes kaatsten terug: er moet een kleine plaats zijn met veel positieve lading en massa.')],
  'Het experiment toonde een kleine positieve kern: het model moest veranderen.')}'''
a1_samenv = '''<p>Het <b>atoommodel is dynamisch</b>: het verandert door nieuwe experimenten.</p>
<p>Democritus (atomos-idee) → Dalton (bolletjesmodel, 1803) → Thomson (krentenbolmodel, 1904) → Rutherford (kernmodel, 1911) → Bohr (schillenmodel, 1913) → Schrödinger (elektronenwolkmodel, 1926).</p>
<p><b>Symbool</b>: 1 of 2 letters, eerst een hoofdletter, dan een kleine letter. Latijn: Na, K, Fe, Cu, Ag, Au, Hg, Pb, Sn.</p>'''

# ================================================================ T2 H2 BOUW VAN HET ATOOM
a2_doelen = ['beschrijven hoe een atoom is opgebouwd (<b>kern</b>, <b>protonen</b>, <b>neutronen</b>, <b>elektronen</b>, <b>elektronenmantel</b>);',
             'de <b>elementaire deeltjes</b> noteren;',
             'voor de eerste 18 elementen de <b>elektronenconfiguratie</b> tekenen en noteren;',
             'de definitie van <b>valentie-elektronen</b> noteren en noteren dat de schillen <b>energieniveaus</b> zijn;',
             'met het <b>atoomnummer Z</b> en het <b>massagetal A</b> het aantal protonen, neutronen en elektronen bepalen;',
             'een element <b>symbolisch</b> voorstellen met atoomnummer en massagetal;',
             'het verband tussen <b>absolute</b> en <b>relatieve atoommassa</b> uitleggen.']
a2_vk = vk('De atoommodellen, vooral het <b>model van Bohr</b>: een kern met elektronen op schillen (hoofdstuk 1).', 'De <b>symbolen</b> van de elementen (hoofdstuk 1).', '<b>Ladingen</b>: positief en negatief trekken elkaar aan.', 'Machten van 10: 10⁻²⁶ is een heel klein getal.')
a2_1 = f'''<p>Een atoom bestaat uit twee delen.</p>
{ttabel(['Deel', 'Wat zit er?'], [['<b>kern</b>', 'in het midden: de <b>protonen</b> en de <b>neutronen</b>. Bijna alle massa zit in de kern.'], ['<b>elektronenmantel</b>', 'de ruimte rond de kern: hier bewegen de <b>elektronen</b>, op schillen.']])}
{kader('Onthoud: de elementaire deeltjes', ttabel(['Deeltje', 'Symbool', 'Lading', 'Massa', 'Waar?'], [['proton', 'p⁺', '+1 (positief)', '1 u', 'in de kern'], ['neutron', 'n⁰', '0 (neutraal)', '1 u', 'in de kern'], ['elektron', 'e⁻', '−1 (negatief)', 'bijna 0 (1/1840 u)', 'in de elektronenmantel']]))}
<p>Een atoom is <b>neutraal</b>: er zijn evenveel elektronen (−) als protonen (+).</p>
{figuur(fig_bohr([6], 1.0, h=230), 'Een koolstofatoom in het model van Bohr: 6 protonen en 6 neutronen in de kern, 6 elektronen op twee schillen.')}
{tool('chemie-atoombouw.html', 'Bouw zelf atomen met de atoombouwer')}'''
a2_2 = f'''{kader('Onthoud', '<p>De schillen zijn <b>energieniveaus</b>. De <b>K-schil</b> ligt het dichtst bij de kern en heeft de laagste energie. Elektronen vullen <b>eerst</b> de schil met de laagste energie.</p>')}
<p><b>Zo vul je de schillen</b> (eerste 18 elementen): K-schil maximaal <b>2</b> elektronen, L-schil maximaal <b>8</b>, M-schil maximaal <b>8</b>. Pas als een schil vol is, ga je naar de volgende. Je noteert de <b>elektronenconfiguratie</b> zo: natrium = <b>2/8/1</b>.</p>
{kader('Definitie', '<p><b>Valentie-elektronen</b> zijn de elektronen op de <b>buitenste schil</b> van een atoom. In de tekeningen zijn ze geel.</p>')}
{figuur(fig_bohr([3, 8, 11, 17], 0.62), 'Lithium, zuurstof, natrium en chloor. De valentie-elektronen zijn geel.')}
{ttabel(['Z', 'Element', 'Configuratie', 'Valentie-e⁻', 'Z', 'Element', 'Configuratie', 'Valentie-e⁻'], [
  [z, ELZ[z]['s'], '/'.join(map(str, schillen(z))), schillen(z)[-1], z + 9, ELZ[z+9]['s'], '/'.join(map(str, schillen(z + 9))), schillen(z + 9)[-1]] for z in range(1, 10)])}
{tool('elektronenconfiguratie.html', 'Oefen elektronenconfiguraties in de tool Elektronenconfiguratie')}
{denk('denk_1', 'Waarom komt het 11de elektron van natrium op de M-schil en niet op de L-schil?', [
  ('K-schil', 'vol met 2 elektronen'), ('L-schil', 'vol met 8 elektronen: samen al 10'), ('11de elektron', 'past niet meer op K of L, dus naar de volgende schil: M')], 'Natrium: 2/8/1, met 1 valentie-elektron.')}'''
a2_3 = f'''{kader('Atoomnummer en massagetal', '<ul><li><b>Atoomnummer Z</b> = het aantal <b>protonen</b>. Bij een neutraal atoom is dat ook het aantal <b>elektronen</b>.</li><li><b>Massagetal A</b> = het aantal <b>protonen + neutronen</b>.</li><li>Dus: aantal <b>neutronen = A − Z</b>.</li></ul>')}
{figuur(fig_notatie(), 'De symbolische voorstelling van een atoom: massagetal boven, atoomnummer onder, links van het symbool.')}
<p>Let op: protonen en neutronen zijn <b>niet altijd even veel</b>. Bij lichte atomen is het aantal neutronen gelijk aan of iets groter dan het aantal protonen. Hoe zwaarder het atoom, hoe meer neutronen. Reken daarom altijd: neutronen = A − Z.</p>
{ttabel(['Notatie', 'Z', 'A', 'p⁺', 'n⁰', 'e⁻'], [[f'<sup>{ELZ[z]["A"]}</sup><sub>{z}</sub>{ELZ[z]["s"]}', z, ELZ[z]['A'], z, ELZ[z]['A'] - z, z] for z in (1, 8, 13, 20)])}
{tool('chemie-atoombouw.html#les22', 'Bouw het atoom uit de notatie in de tool')}
{denk('denk_2', 'Een atoom heeft 17 protonen en 18 neutronen. Welk element is het? Schrijf de symbolische voorstelling.', [
  ('Z', 'Z = aantal protonen = 17 → chloor (Cl)'), ('A', 'A = 17 + 18 = 35')], 'Het is <sup>35</sup><sub>17</sub>Cl.')}'''
a2_4 = f'''<p>Een atoom is heel licht. Een zuurstofatoom weegt 0,000 000 000 000 000 000 000 000 026 6 kg = <b>2,66 · 10⁻²⁶ kg</b>. Dat is de <b>absolute atoommassa</b>: de echte massa in kg. Met zulke getallen rekenen is lastig.</p>
<p>Daarom vergelijken we met de <b>atomaire massa-eenheid u</b> = 1,66 · 10⁻²⁷ kg (1/12 van de massa van een koolstof-12-atoom).</p>
{kader('Verband', '<p><b>A<sub>r</sub> = absolute atoommassa ÷ u</b></p><p>De <b>relatieve atoommassa A<sub>r</sub></b> zegt hoeveel keer zwaarder een atoom is dan u. A<sub>r</sub> heeft <b>geen eenheid</b>. A<sub>r</sub> is ongeveer gelijk aan het massagetal A. Je vindt A<sub>r</sub> in het PSE.</p>')}
<p><b>Voorbeeld</b>: zuurstof: A<sub>r</sub> = 2,66 · 10⁻²⁶ kg ÷ 1,66 · 10⁻²⁷ kg = <b>16,0</b>.</p>
{denk('denk_3', 'Waarom is A<sub>r</sub> ongeveer gelijk aan het massagetal A?', [
  ('Massa', 'Een proton en een neutron hebben elk een massa van ongeveer 1 u. Elektronen wegen bijna niets.'),
  ('Dus', 'De massa van het atoom in u ≈ aantal protonen + neutronen = A.')], 'Bijna alle massa zit in de kern, en elk kerndeeltje weegt ongeveer 1 u.')}'''
lege_bohr = svg(''.join(bohr(z, 640 / 3 * (i + .5), 100, 0.8, naam=False, leeg=True, kerntekst=True) + t(640 / 3 * (i + .5), 192, ELZ[z]['naam'], INK, size=13) for i, z in enumerate((7, 12, 16))), 640, 205)
a2_oef = f'''{oef('opl_1', 1, 'Elementaire deeltjes', 'Vul aan.<ol class="deelvragen" type="a"><li>Welke deeltjes zitten in de kern?</li><li>Welk deeltje is negatief geladen?</li><li>Welk deeltje heeft geen lading?</li><li>Waar zit bijna alle massa van het atoom?</li><li>Waarom is een atoom neutraal?</li></ol>', [
  ('a', 'protonen en neutronen'), ('b', 'het elektron'), ('c', 'het neutron'), ('d', 'in de kern'), ('e', 'evenveel protonen (+) als elektronen (−)')], 'Proton +1 · neutron 0 · elektron −1.')}
{oef_fig('opl_2', 2, 'Schillenmodel tekenen', 'Teken de elektronen op de schillen. Kleur de valentie-elektronen. Noteer de elektronenconfiguratie.', lege_bohr, [
  ('stikstof', '7 elektronen: 2/5 → 5 valentie-elektronen'), ('magnesium', '12 elektronen: 2/8/2 → 2 valentie-elektronen'), ('zwavel', '16 elektronen: 2/8/6 → 6 valentie-elektronen')],
  'Vul eerst K (2), dan L (8), dan M (8).', fig_bohr([7, 12, 16], 0.8))}
{oef('opl_3', 3, 'Elektronenconfiguratie noteren', 'Noteer de elektronenconfiguratie en het aantal valentie-elektronen.<ol class="deelvragen" type="a"><li>helium</li><li>koolstof</li><li>fluor</li><li>aluminium</li><li>fosfor</li><li>argon</li></ol>', [
  ('a', '2 → 2'), ('b', '2/4 → 4'), ('c', '2/7 → 7'), ('d', '2/8/3 → 3'), ('e', '2/8/5 → 5'), ('f', '2/8/8 → 8')], 'Het laatste getal is het aantal valentie-elektronen.')}
{oef('opl_4', 4, 'Welk element?', 'Welk element heeft deze configuratie?<ol class="deelvragen" type="a"><li>2/6</li><li>2/8/7</li><li>2/1</li><li>2/8/8/1</li></ol>', [
  ('a', '8 elektronen → zuurstof'), ('b', '17 → chloor'), ('c', '3 → lithium'), ('d', '19 → kalium')], 'Tel alle elektronen op: dat is Z.')}
{oef('opl_5', 5, 'Vul de tabel aan', '<table class="vb"><tr><td><b>Notatie</b></td><td><b>Z</b></td><td><b>A</b></td><td><b>p⁺</b></td><td><b>n⁰</b></td><td><b>e⁻</b></td></tr><tr><td><sup>23</sup><sub>11</sub>Na</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td>6</td><td>12</td><td></td><td></td><td></td></tr><tr><td></td><td></td><td>32</td><td>16</td><td></td><td></td></tr><tr><td></td><td></td><td></td><td>20</td><td>20</td><td></td></tr><tr><td><sup>27</sup><sub>13</sub>Al</td><td></td><td></td><td></td><td></td><td></td></tr></table>', [
  ('Na', 'Z = 11 · A = 23 · 11 p⁺ · 12 n⁰ · 11 e⁻'), ('C', '<sup>12</sup><sub>6</sub>C · 6 p⁺ · 6 n⁰ · 6 e⁻'), ('S', '<sup>32</sup><sub>16</sub>S · Z = 16 · 16 n⁰ · 16 e⁻'),
  ('Ca', 'Z = 20 · A = 40 · <sup>40</sup><sub>20</sub>Ca · 20 e⁻'), ('Al', 'Z = 13 · A = 27 · 13 p⁺ · 14 n⁰ · 13 e⁻')], 'p⁺ = e⁻ = Z · n⁰ = A − Z.')}
{oef('opl_6', 6, 'Neutronen tellen', 'Een ijzeratoom heeft Z = 26 en A = 56. Een loodatoom heeft Z = 82 en A = 207. Bereken telkens het aantal neutronen. Wat valt op?', [
  ('IJzer', '56 − 26 = 30 neutronen (4 meer dan protonen)'), ('Lood', '207 − 82 = 125 neutronen (43 meer dan protonen)'), ('Besluit', 'Hoe zwaarder het atoom, hoe meer neutronen in vergelijking met de protonen.')], 'Reken altijd n⁰ = A − Z.')}
{oef('opl_7', 7, 'Relatieve atoommassa', 'Een natriumatoom heeft een absolute atoommassa van 3,82 · 10⁻²⁶ kg. Bereken A<sub>r</sub>. (u = 1,66 · 10⁻²⁷ kg)', [
  ('Formule', 'A<sub>r</sub> = absolute atoommassa ÷ u'), ('Invullen', 'A<sub>r</sub> = 3,82 · 10⁻²⁶ kg ÷ 1,66 · 10⁻²⁷ kg = 23,0'), ('Eenheid', 'geen: kg ÷ kg')], 'A<sub>r</sub>(Na) = 23,0: een natriumatoom is 23 keer zwaarder dan u.')}
{oef('opl_8', 8, 'Redeneren: een fout in de atoombouwer', 'Ilyas bouwt een atoom met 9 protonen, 10 neutronen en 10 elektronen. Hij zegt: "Dit is neon, want er zijn 10 elektronen." Klopt dat?', [
  ('Welk element?', 'Het aantal protonen bepaalt het element: 9 protonen = fluor.'), ('Lading', '9 (+) en 10 (−): het deeltje is niet neutraal, maar −1 geladen.')], 'Nee: het is een fluordeeltje met één elektron te veel (een negatief ion).')}
{oef('opl_9', 9, 'Schillen zijn energieniveaus', '<ol class="deelvragen" type="a"><li>Welke schil heeft de laagste energie?</li><li>Waarom vult een elektron eerst de K-schil?</li><li>Wat zijn valentie-elektronen? Hoeveel heeft zwavel (2/8/6)?</li></ol>', [
  ('a', 'de K-schil, het dichtst bij de kern'), ('b', 'Elektronen vullen eerst de schil met de laagste energie.'), ('c', 'de elektronen op de buitenste schil; zwavel heeft er 6')], 'Schillen = energieniveaus; K is het laagste.')}'''
a2_samenv = '''<p><b>Kern</b>: protonen (p⁺, +1, 1 u) en neutronen (n⁰, 0, 1 u). <b>Elektronenmantel</b>: elektronen (e⁻, −1, bijna 0 u) op schillen.</p>
<p><b>Schillen = energieniveaus</b>. K max. 2, L max. 8, M max. 8; eerst de laagste. Configuratie bv. Na = 2/8/1. <b>Valentie-elektronen</b> = elektronen op de buitenste schil.</p>
<p><b>Z</b> = aantal protonen (= elektronen bij een neutraal atoom). <b>A</b> = protonen + neutronen. <b>n⁰ = A − Z</b>. Notatie: <sup>A</sup><sub>Z</sub>X.</p>
<p><b>A<sub>r</sub> = absolute atoommassa ÷ u</b>, met u = 1,66 · 10⁻²⁷ kg. A<sub>r</sub> heeft geen eenheid en is ongeveer A.</p>'''

# ================================================================ T2 H3 PSE
a3_doelen = ['noteren dat de elementen in <b>eenzelfde groep</b> dezelfde chemische eigenschappen hebben en dus op dezelfde manier reageren;',
             'met het PSE het verband noteren tussen het <b>groepsnummer</b>, het <b>periodenummer</b> en de bouw van het atoom;',
             'met het PSE de <b>opbouw van een atoom</b> noteren en omgekeerd;',
             'uitleggen wat een hoge of lage <b>elektronegativiteit</b> betekent;',
             'uitleggen wat de <b>edelgasconfiguratie</b> is;',
             'de <b>categorieën</b> van elementen noteren en aanduiden waar ze in het PSE staan.']
a3_vk = vk('De bouw van een atoom: protonen, neutronen en elektronen (hoofdstuk 2).', 'Atoomnummer Z en massagetal A (hoofdstuk 2).', 'De elektronenconfiguratie van de eerste 18 elementen en de valentie-elektronen (hoofdstuk 2).')
a3_1 = f'''<p>In het <b>periodiek systeem van de elementen (PSE)</b> staan alle elementen in volgorde van <b>toenemend atoomnummer</b>. Elk element heeft een eigen vakje.</p>
{figuur(fig_vakje(), 'Wat vertelt één vakje? Op jouw PSE kunnen de getallen op een andere plaats staan.')}
<h3>Categorieën van elementen</h3>
{ttabel(['Categorie', 'Waar in het PSE?', 'Eigenschappen', 'Voorbeelden'], [
  ['<b>metalen</b>', 'links van de trap; de grootste groep', 'glanzen, geleiden warmte en elektrische stroom', 'natrium, ijzer, koper, aluminium'],
  ['<b>niet-metalen</b>', 'rechts van de trap, rechtsboven', 'geleiden geen stroom (uitzondering: koolstof als grafiet)', 'zuurstof, chloor, zwavel, koolstof'],
  ['<b>edelgassen</b>', 'de laatste kolom (groep VIIIa)', 'reageren (bijna) niet', 'helium, neon, argon']])}
<p>Let op: <b>waterstof</b> staat links, maar is een <b>niet-metaal</b>.</p>
{figuur_liggend(pse_svg('kat'), 'Het periodiek systeem van de elementen. Groepsnummers in Romeinse cijfers bovenaan, periodenummers links. De rode trap scheidt metalen en niet-metalen. In dit hoofdstuk werk je met de a-groepen.')}
{tool('chemie-pse.html#lesB', 'Klik op een element in het PSE van de tool')}'''
a3_2 = f'''{kader('Groep en periode', '<ul><li>Een <b>groep</b> is een <b>kolom</b>. Groepsnummer (a-groepen) = <b>aantal valentie-elektronen</b>. Bv. groep IIIa → 3 valentie-elektronen.</li><li>Een <b>periode</b> is een <b>rij</b>. Periodenummer = <b>aantal schillen</b>. Bv. periode 3 → 3 schillen (K, L, M).</li></ul>')}
{ttabel(['Van PSE naar atoom', 'Van atoom naar PSE'], [['<b>Magnesium</b>: periode 3, groep IIa, Z = 12 → 3 schillen, 2 valentie-elektronen, 12 protonen en 12 elektronen → 2/8/2.', '<b>2 schillen en 5 valentie-elektronen</b> → periode 2, groep Va → stikstof (N), Z = 7.']])}
{figuur(fig_bohr([3, 11, 19], 0.55), 'Lithium, natrium en kalium staan in groep Ia: elk 1 valentie-elektron, maar 2, 3 en 4 schillen.')}
{kader('Onthoud', '<p>Elementen in <b>dezelfde groep</b> hebben <b>evenveel valentie-elektronen</b>. Daarom hebben ze <b>dezelfde chemische eigenschappen</b>: ze reageren op dezelfde manier.</p>')}
<p>Lithium, natrium en kalium reageren alle drie met water en vormen waterstofgas. Hoe lager in de groep, hoe heftiger de reactie. Doe dit nooit zelf: alkalimetalen zijn gevaarlijk.</p>
{ttabel(['Groep', 'Naam', 'Valentie-elektronen', 'Voorbeelden'], [['Ia', 'alkalimetalen', '1', 'Li, Na, K (niet H)'], ['IIa', 'aardalkalimetalen', '2', 'Mg, Ca'], ['VIIa', 'halogenen', '7', 'F, Cl, Br, I'], ['VIIIa', 'edelgassen', '8 (helium: 2)', 'He, Ne, Ar']])}
{tool('chemie-pse.html#lesC', 'Bekijk de proef met de alkalimetalen in de tool')}
{denk('denk_1', 'Chloor wordt gebruikt om zwembadwater te ontsmetten. Waarom verwacht je dat broom ook ontsmet?', [
  ('PSE', 'Chloor en broom staan allebei in groep VIIa (halogenen).'), ('Valentie-elektronen', 'Ze hebben allebei 7 valentie-elektronen.')], 'Zelfde groep → zelfde chemische eigenschappen: broom reageert zoals chloor.')}'''
a3_3 = f'''{kader('Definitie', '<p>De <b>elektronegativiteit (EN)</b> is een maat voor hoe sterk een atoom elektronen naar zich toe trekt.</p>')}
{ttabel(['', 'Hoge EN', 'Lage EN'], [['Wat betekent het?', 'het atoom trekt elektronen <b>sterk</b> aan en <b>neemt</b> gemakkelijk elektronen <b>op</b>', 'het atoom trekt elektronen <b>zwak</b> aan en <b>geeft</b> gemakkelijk elektronen <b>af</b>'],
  ['Welke elementen?', 'niet-metalen, rechtsboven; fluor heeft de hoogste waarde: 4,0', 'metalen, linksonder; cesium en francium: 0,7']])}
{figuur_liggend(pse_svg('en'), 'De EN-waarden staan in het rood, rechtsboven in elk vakje. Edelgassen krijgen geen waarde.')}
<p>De EN <b>stijgt naar rechts</b> in een periode en <b>naar boven</b> in een groep. Edelgassen krijgen geen waarde: ze gaan (bijna) geen bindingen aan.</p>
{kader('Definitie', '<p>Een atoom heeft een <b>edelgasconfiguratie</b> als de <b>buitenste schil vol</b> is: <b>8 elektronen</b>, of <b>2</b> als er alleen een K-schil is (zoals bij helium).</p>')}
{figuur(fig_bohr([2, 10, 18], 0.6, valentie=True), 'Helium, neon en argon: de buitenste schil is vol.')}
<p>Edelgassen hebben al een edelgasconfiguratie: daarom zijn ze heel stabiel en reageren ze (bijna) niet. Andere atomen proberen ook een edelgasconfiguratie te krijgen. Dat doen ze door elektronen <b>af te geven</b> (metalen, lage EN) of <b>op te nemen</b> (niet-metalen, hoge EN): zo ontstaan <b>ionen</b>.</p>
{tool('elektronenconfiguratie.html', 'Zie in de tool Elektronenconfiguratie hoe atomen een edelgasconfiguratie bereiken')}
{denk('denk_2', 'Natrium (2/8/1) en chloor (2/8/7) willen allebei een edelgasconfiguratie. Wat doet elk atoom het gemakkelijkst?', [
  ('Natrium', 'Lage EN (0,9): het geeft 1 elektron af en houdt 2/8 over, zoals neon.'), ('Chloor', 'Hoge EN (3,0): het neemt 1 elektron op en krijgt 2/8/8, zoals argon.')],
  'Natrium geeft een elektron af, chloor neemt er een op.')}'''
a3_4 = f'''<p>Hieronder staan drie versies van het PSE. Druk af wat je nodig hebt.</p>
<ul><li><b>Met namen</b>: om te leren en op te zoeken.</li><li><b>Zonder namen</b>: om de namen van de elementen te oefenen.</li><li><b>Enkel symbolen</b>, met de trap: zoals je het op een toets kan krijgen.</li></ul>
{figuur_liggend(pse_svg('kat'), 'PSE met de namen van de elementen.')}
{figuur_liggend(pse_svg('zonder'), 'PSE zonder de namen van de elementen.')}
{figuur_liggend(pse_svg('symbolen'), 'PSE met enkel de symbolen en de trap.')}'''
a3_oef = f'''{oef('opl_1', 1, 'Categorieën kleuren', 'Kleur in het PSE de <b>metalen</b> blauw, de <b>niet-metalen</b> groen en de <b>edelgassen</b> geel. Teken de trap.' + figuur_liggend(pse_svg('leeg'), ''), [
  ('Metalen', 'links van de trap (behalve H), ook alle b-groepen, lanthaniden en actiniden'), ('Niet-metalen', 'rechts van de trap, en H'), ('Edelgassen', 'groep VIIIa')], 'Waterstof staat links, maar is een niet-metaal.').replace('<div class="besluit">', oplfig(pse_svg('kat')) + '<div class="besluit">', 1)}
{oef('opl_2', 2, 'Metaal, niet-metaal of edelgas?', '<ol class="deelvragen" type="a"><li>kalium</li><li>zwavel</li><li>argon</li><li>aluminium</li><li>waterstof</li><li>broom</li></ol>', [
  ('a', 'metaal'), ('b', 'niet-metaal'), ('c', 'edelgas'), ('d', 'metaal'), ('e', 'niet-metaal'), ('f', 'niet-metaal')], 'Kijk waar het element staat ten opzichte van de trap.')}
{oef('opl_3', 3, 'Van PSE naar atoom', 'Zoek op in het PSE: groep, periode, aantal schillen, aantal valentie-elektronen, aantal protonen en de elektronenconfiguratie.<ol class="deelvragen" type="a"><li>silicium</li><li>calcium</li><li>zuurstof</li><li>chloor</li></ol>', [
  ('a', 'IVa · periode 3 · 3 schillen · 4 val. · 14 p⁺ · 2/8/4'), ('b', 'IIa · periode 4 · 4 schillen · 2 val. · 20 p⁺ · 2/8/8/2'),
  ('c', 'VIa · periode 2 · 2 schillen · 6 val. · 8 p⁺ · 2/6'), ('d', 'VIIa · periode 3 · 3 schillen · 7 val. · 17 p⁺ · 2/8/7')], 'Groep = valentie-elektronen, periode = schillen.')}
{oef('opl_4', 4, 'Van atoom naar PSE', 'Welk element is het?<ol class="deelvragen" type="a"><li>3 schillen en 3 valentie-elektronen</li><li>2 schillen en 7 valentie-elektronen</li><li>4 schillen en 1 valentie-elektron</li><li>1 schil die vol is</li></ol>', [
  ('a', 'periode 3, groep IIIa → aluminium (Al)'), ('b', 'periode 2, groep VIIa → fluor (F)'), ('c', 'periode 4, groep Ia → kalium (K)'), ('d', 'periode 1, groep VIIIa → helium (He)')], 'Schillen → periode, valentie-elektronen → groep.')}
{oef('opl_5', 5, 'Zelfde groep', 'Welk element reageert op dezelfde manier als magnesium: natrium, calcium of aluminium? Leg uit.', [
  ('Magnesium', 'groep IIa: 2 valentie-elektronen'), ('Calcium', 'ook groep IIa: 2 valentie-elektronen')], 'Calcium: zelfde groep, evenveel valentie-elektronen, dezelfde chemische eigenschappen.')}
{oef('opl_6', 6, 'Elektronegativiteit vergelijken', 'Welk atoom trekt het sterkst elektronen aan? Gebruik het PSE.<ol class="deelvragen" type="a"><li>Na of Cl</li><li>F of I</li><li>O of S</li><li>Li of K</li></ol>', [
  ('a', 'Cl (3,0 > 0,9): meer naar rechts'), ('b', 'F (4,0 > 2,5): hoger in de groep'), ('c', 'O (3,5 > 2,5)'), ('d', 'Li (1,0 > 0,8)')], 'EN stijgt naar rechts en naar boven.')}
{oef('opl_7', 7, 'Edelgasconfiguratie', 'Heeft het deeltje een edelgasconfiguratie? Leg uit.<ol class="deelvragen" type="a"><li>neon: 2/8</li><li>zuurstof: 2/6</li><li>een natriumatoom dat 1 elektron heeft afgegeven</li><li>een chlooratoom dat 1 elektron heeft opgenomen</li></ol>', [
  ('a', 'ja: buitenste schil vol (8)'), ('b', 'nee: 6 op de buitenste schil'), ('c', 'ja: 2/8, zoals neon'), ('d', 'ja: 2/8/8, zoals argon')], 'Edelgasconfiguratie = buitenste schil vol (8, of 2 bij alleen een K-schil).')}
{oef('opl_8', 8, 'Redeneren: waarom reageren edelgassen niet?', 'In de lichtreclames in de Nieuwstraat zit neongas. Waarom gebruikt men een edelgas en geen zuurstof? Gebruik het woord edelgasconfiguratie.', [
  ('Neon', 'heeft een edelgasconfiguratie (2/8): heel stabiel'), ('Gevolg', 'Het reageert niet met het metaal van de elektroden of met andere stoffen in de buis.'), ('Zuurstof', '2/6: wil 2 elektronen opnemen en reageert gemakkelijk.')],
  'Neon reageert (bijna) niet omdat de buitenste schil vol is.')}'''
a3_samenv = '''<p><b>PSE</b>: elementen volgens toenemend atoomnummer. <b>Metalen</b> links van de trap, <b>niet-metalen</b> rechts (en H), <b>edelgassen</b> in groep VIIIa.</p>
<p><b>Groep</b> (kolom) = aantal valentie-elektronen. <b>Periode</b> (rij) = aantal schillen. Zelfde groep → zelfde chemische eigenschappen.</p>
<p><b>Elektronegativiteit</b>: hoe sterk een atoom elektronen aantrekt. Hoog (rechtsboven, F = 4,0): neemt elektronen op. Laag (linksonder): geeft elektronen af.</p>
<p><b>Edelgasconfiguratie</b>: buitenste schil vol (8, of 2 bij helium). Atomen geven elektronen af of nemen er op om die te krijgen: zo ontstaan ionen.</p>'''

maak('cursus-chemie-atomen-elementen.html', T2 + '1', 'Atomen en elementen',
     'Werk dit hoofdstuk samen met de tool <a href="chemie-atoommodellen.html">Atomen en elementen</a>. Oefeningen maak je op papier.',
     a1_doelen, a1_vk, [('Het atoommodel als dynamisch model', a1_1), ('Symbolen van de elementen', a1_2)], a1_oef, a1_samenv, ('chemie-atoommodellen.html', 'Oefen verder in de tool'))
maak('cursus-chemie-atoombouw.html', T2 + '2', 'Bouw van het atoom',
     'Werk dit hoofdstuk samen met de tool <a href="chemie-atoombouw.html">Bouw van het atoom</a>. Oefeningen maak je op papier.',
     a2_doelen, a2_vk, [('Bouwstenen van het atoom', a2_1), ('Schillen en valentie-elektronen', a2_2), ('Atoomnummer en massagetal', a2_3), ('Absolute en relatieve atoommassa', a2_4)], a2_oef, a2_samenv, ('chemie-atoombouw.html', 'Oefen verder in de tool'))
maak('cursus-chemie-pse.html', T2 + '3', 'Het periodiek systeem',
     'Werk dit hoofdstuk samen met de tool <a href="chemie-pse.html">Periodiek systeem</a>. Gebruik je eigen PSE. Oefeningen maak je op papier.',
     a3_doelen, a3_vk, [('Het PSE lezen en de categorieën', a3_1), ('Groep en periode', a3_2), ('Elektronegativiteit en edelgasconfiguratie', a3_3), ("Drie PSE's om af te drukken", a3_4)], a3_oef, a3_samenv, ('chemie-pse.html', 'Oefen verder in de tool'))
