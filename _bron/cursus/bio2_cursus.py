# Cursus biologie 3de jaar · T1H2 homeostase · T2 receptoren · T3 effectoren
import sys, math
_src = open('/home/claude/cursus/optica_cursus.py', encoding='utf-8').read()
exec(_src.split('# ================================================================ H1')[0])
sys.path.insert(0, '/home/claude/cursus/biofig')
from bio_figs import lab, num, namen, plat

def oefblok(inhoud, toolref=None):
    s = f'''<p>Maak deze oefeningen <b>op papier</b>. De oplossingen verschijnen hier nadat we de oefeningen in de les besproken hebben.</p>
<p><button class="knop licht" data-print="oef">🖨 Druk de oefeningen af</button></p>
{inhoud}'''
    return s + (tool(*toolref) if toolref else '')
def ttabel(kop, rijen):
    h = '<table class="vb grid"><tr>' + ''.join(f'<td><b>{k}</b></td>' for k in kop) + '</tr>'
    return h + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rijen) + '</table>'
def invul(n): return '<ol class="invul" style="columns:2;line-height:2">' + ''.join('<li>……………………………………</li>' for _ in range(n)) + '</ol>'
TOOL = 'biologie-prikkels.html'
T1 = 'Biologie 3de jaar · Thema 1 Belang en werking van feedbacksystemen · Hoofdstuk '
T2 = 'Biologie 3de jaar · Thema 2 Receptoren vangen prikkels op · Hoofdstuk '
T3 = 'Biologie 3de jaar · Thema 3 Effectoren reageren op prikkels · Hoofdstuk '
GROEN_Z = '#dcfce7'

# ================================================================ eigen figuren
def grafiek_kader(x0, y0, w, h, ylab, xlab='tijd →'):
    return (f'<path d="M{x0},{y0} V{y0+h} H{x0+w}" fill="none" stroke="{INK}" stroke-width="2"/>'
            + t(x0, y0 - 10, ylab, INK, 'start', 14) + t(x0 + w, y0 + h + 20, xlab, GRIJS, 'end', 13, 600))
def fig_neg():
    x0, y0, w, h = 60, 34, 520, 190; m = y0 + h / 2
    o = f'<rect x="{x0}" y="{m-55}" width="{w}" height="110" fill="{GROEN_Z}"/>'
    o += lijn(x0, m, x0 + w, m, GROEN, 2, '8 6') + t(x0 + w + 6, m + 5, 'norm', GROEN, 'start', 13)
    o += lijn(x0, m - 55, x0 + w, m - 55, GROEN, 1.2, '4 4') + t(x0 + w + 6, m - 50, 'bovengrens', GROEN, 'start', 12, 600)
    o += lijn(x0, m + 55, x0 + w, m + 55, GROEN, 1.2, '4 4') + t(x0 + w + 6, m + 60, 'ondergrens', GROEN, 'start', 12, 600)
    pts = ' L'.join(f'{x0+i:.1f},{m-42*math.sin(i/w*5*math.pi)*math.exp(-i/w*0.3):.1f}' for i in range(0, w + 1, 4))
    o += f'<path d="M{pts}" fill="none" stroke="{INK}" stroke-width="3"/>'
    o += grafiek_kader(x0, y0, w, h, 'lichaamstemperatuur')
    o += t(x0 + w * .25, m - 66, 'te warm → zweten', ROOD, 'middle', 13) + t(x0 + w * .3, m + 76, 'te koud → rillen', BLAUW, 'middle', 13)
    return svg(o, 680, 255)
def fig_pos():
    x0, y0, w, h = 60, 34, 520, 190
    pts = ' L'.join(f'{x0+i:.1f},{y0+h-8-(h-30)*(math.exp(i/w*3.2)-1)/(math.exp(3.2)-1):.1f}' for i in range(0, int(w * .82) + 1, 4))
    o = f'<path d="M{pts}" fill="none" stroke="{INK}" stroke-width="3"/>'
    xe = x0 + w * .82
    o += lijn(xe, y0 + 6, xe, y0 + h, ROOD, 2, '6 5') + t(xe - 8, y0 + 20, 'baby geboren:', ROOD, 'end', 13) + t(xe - 8, y0 + 38, 'het stopt', ROOD, 'end', 13)
    o += lijn(xe, y0 + 22, xe + 8, y0 + h - 8, INK, 3) + lijn(xe + 8, y0 + h - 8, x0 + w, y0 + h - 8, INK, 3)
    o += grafiek_kader(x0, y0, w, h, 'sterkte van de weeën')
    o += t(x0 + w * .35, y0 + h - 40, 'weeën → meer hormoon → sterkere weeën → …', GRIJS, 'middle', 13)
    return svg(o, 680, 255)
def fig_drempel(gewenning=False):
    x0, y0, w, h = 70, 30, 520, 160; dy = y0 + 60
    o = ''
    if gewenning:
        o += f'<rect x="{x0}" y="{dy-30}" width="{w}" height="{y0+h-dy+30}" fill="#dbeafe" opacity=".7"/>'
        o += f'<path d="M{x0},{dy} C{x0+180},{dy} {x0+260},{dy-50} {x0+w},{dy-58}" fill="none" stroke="{ROOD}" stroke-width="2.5" stroke-dasharray="8 6"/>'
        o += t(x0 + w - 4, dy - 66, 'prikkeldrempel stijgt', ROOD, 'end', 13)
        o += t(x0 + 10, dy - 38, 'een prikkel die even sterk blijft', BLAUW, 'start', 13)
        o += t(x0 + 120, y0 + h + 44, 'eerst neem je ze waar, later niet meer: prikkelgewenning', INK, 'start', 13)
    else:
        o += lijn(x0, dy, x0 + w, dy, ROOD, 2.5, '8 6') + t(x0 + w + 6, dy + 5, 'prikkeldrempel', ROOD, 'start', 13)
        for i, (hh, ok) in enumerate([(50, 0), (90, 0), (125, 1), (150, 1)]):
            x = x0 + 40 + i * 120
            o += f'<rect x="{x}" y="{y0+h-hh}" width="60" height="{hh}" rx="4" fill="{GROEN if ok else "#94a3b8"}"/>'
            o += t(x + 30, y0 + h + 40, 'impuls' if ok else 'geen impuls', GROEN if ok else GRIJS, 'middle', 13)
    o += grafiek_kader(x0, y0, w, h, 'sterkte van de prikkel')
    return svg(o, 720, 255 if gewenning else 245)
def fig_lichtweg():
    o = ''
    cx, cy, R = 470, 150, 105
    o += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#fff7ed" stroke="{INK}" stroke-width="2.5"/>'
    o += f'<path d="M{cx-R+8},{cy-58} A70,70 0 0,0 {cx-R+8},{cy+58}" fill="#e0f2fe" stroke="#60a5fa" stroke-width="2"/>'
    o += f'<ellipse cx="{cx-R+40}" cy="{cy}" rx="13" ry="34" fill="#e0e7ff" stroke="{INK}" stroke-width="2"/>'
    o += f'<path d="M{cx+R-3},{cy-80} A{R-3},{R-3} 0 0,1 {cx+R-3},{cy+80}" fill="none" stroke="#f59e0b" stroke-width="7" opacity=".7"/>'
    o += f'<path d="M{cx+R-6},{cy+40} L{cx+R+70},{cy+70}" stroke="#eab308" stroke-width="10" stroke-linecap="round"/>'
    # kaars (voorwerp)
    kx, kb, kt = 80, 210, 110
    o += f'<rect x="{kx-10}" y="{kt}" width="20" height="{kb-kt}" fill="#fde68a" stroke="{INK}" stroke-width="1.5"/><path d="M{kx},{kt-28} q10,14 0,24 q-10,-10 0,-24z" fill="#f97316"/>'
    lx = cx - R + 40
    ix = cx + R - 4
    vlam = (kx, kt - 18); voet = (kx, kb)
    for (px, py) in (vlam, voet):
        # stralen door het midden van de lens rechtdoor naar het netvlies
        yi = cy + (cy - py) * (ix - lx) / (lx - px)
        o += lijn(px, py, lx, cy, LICHT, 2) + lijn(lx, cy, ix, yi, LICHT, 2)
    # omgekeerde kaars op het netvlies
    y_vl = cy + (cy - vlam[1]) * (ix - lx) / (lx - vlam[0]); y_vt = cy + (cy - voet[1]) * (ix - lx) / (lx - voet[0])
    o += f'<rect x="{ix-14}" y="{y_vt}" width="8" height="{y_vl-y_vt-6}" fill="#fde68a" stroke="{INK}" stroke-width="1"/><path d="M{ix-10},{y_vl+8} q4,-6 0,-11 q-4,5 0,11z" fill="#f97316"/>'
    o += t(kx, kb + 22, 'voorwerp', INK, size=13) + t(cx - R + 2, cy - 72, 'hoornvlies', INK, 'end', 12) + t(lx, cy + 52, 'lens', INK, size=12)
    o += t(cx + 10, cy - R - 10, 'glasachtig lichaam', GRIJS, size=12) + t(ix + 10, cy - 70, 'netvlies', INK, 'start', 12) + t(cx + R + 40, cy + 92, 'oogzenuw', INK, 'start', 12)
    o += t(cx + 20, cy + R + 24, 'op het netvlies: een omgekeerd en verkleind beeld', ROOD, 'middle', 12)
    return svg(o, 680, 300)
def fig_blindevlek():
    o = f'<rect x="20" y="20" width="600" height="120" rx="10" fill="#fff" stroke="{GRIJS}" stroke-width="1.5"/>'
    o += t(160, 98, '✚', INK, size=44) + f'<circle cx="480" cy="82" r="18" fill="{INK}"/>'
    return svg(o, 640, 160)
def fig_muller():
    o = ''
    for y, uit in ((70, True), (170, False)):
        o += lijn(180, y, 460, y, INK, 4)
        d = 30 if uit else -30
        for x, s in ((180, -1), (460, 1)):
            o += lijn(x, y, x - s * d, y - 28, INK, 4) + lijn(x, y, x - s * d, y + 28, INK, 4)
    o += t(100, 76, 'A', INK, size=18) + t(100, 176, 'B', INK, size=18)
    return svg(o, 640, 230)
def fig_arm(buigen=True, tx=330):
    o = ''
    sx, sy = 200, 60
    ex, ey = 200, 260
    hx, hy = (380, 170) if buigen else (200, 440)
    o += lijn(sx, sy, ex, ey, '#d6c7a1', 16) + lijn(ex, ey, hx, hy, '#d6c7a1', 14)
    o += f'<circle cx="{ex}" cy="{ey}" r="14" fill="#e5e7eb" stroke="{INK}" stroke-width="2"/>'
    vx, vy = (hx - ex), (hy - ey); L = math.hypot(vx, vy); ax, ay = ex + vx / L * 45, ey + vy / L * 45
    dik_b, dik_t = (30, 10) if buigen else (11, 24)
    # biceps vooraan (rechts), triceps achteraan (links)
    o += f'<path d="M{sx+10},{sy+20} Q{sx+18+dik_b*2},{(sy+ey)/2} {ax},{ay}" fill="none" stroke="#b91c1c" stroke-width="{dik_b}" stroke-linecap="round" opacity=".85"/>'
    o += f'<path d="M{sx-10},{sy+20} Q{sx-16-dik_t*1.6},{(sy+ey)/2} {ex-8},{ey+22}" fill="none" stroke="#7f1d1d" stroke-width="{dik_t}" stroke-linecap="round" opacity=".85"/>'
    o += t(sx + 70, sy + 80, 'biceps', '#b91c1c', 'start', 15) + t(sx - 50, sy + 80, 'triceps', '#7f1d1d', 'end', 15)
    o += t(ex - 26, ey + 6, 'elleboog', GRIJS, 'end', 13)
    if buigen: o += t(tx, 330, 'biceps trekt samen:', INK, size=14) + t(tx, 350, 'de arm buigt', INK, size=14)
    else: o += t(tx, 470, 'triceps trekt samen:', INK, size=14) + t(tx, 488, 'de arm strekt', INK, size=14)
    return o
def fig_armen():
    return svg(fig_arm(True, 230) + f'<g transform="translate(330,0)">{fig_arm(False, 200)}</g>', 680, 500)
def slokdarm(o, x0, x1, yc, bx, hw=26, toon_spieren=True, labels=False):
    """slokdarm van x0 tot x1 (mond links, maag rechts); voedselbrok in bx.
    Achter de brok (links): kringspieren samen -> nauw. Voor de brok (rechts): lengtespieren samen -> wijd."""
    def straal_(x):
        d = x - bx
        return hw - 15 * math.exp(-((d + 72) / 24) ** 2) + 9 * math.exp(-(d / 30) ** 2) + 8 * (1 / (1 + math.exp(-(d - 50) / 12)))
    xs = list(range(x0, x1 + 1, 4))
    boven = [(x, yc - straal_(x)) for x in xs]; onder = [(x, yc + straal_(x)) for x in xs]
    o.append(f'<path d="M{" L".join(f"{x},{y:.1f}" for x, y in boven)} L{" L".join(f"{x},{y:.1f}" for x, y in reversed(onder))}Z" fill="#fef2f2"/>')
    for pts in (boven, onder):
        o.append(f'<path d="M{" L".join(f"{x},{y:.1f}" for x, y in pts)}" fill="none" stroke="#b91c1c" stroke-width="9" stroke-linecap="round"/>')
    if toon_spieren:
        # kringspieren: korte dwarse streepjes in de wand (donker = samengetrokken)
        for x in range(x0 + 6, x1, 12):
            samen = -100 < x - bx < -40
            for y in (yc - straal_(x), yc + straal_(x)):
                o.append(f'<line x1="{x}" y1="{y-5}" x2="{x}" y2="{y+5}" stroke="{"#450a0a" if samen else "#fca5a5"}" stroke-width="{3 if samen else 2}"/>')
        # lengtespieren: lijn langs de wand (dik = samengetrokken voor de brok)
        for teken_ in (-1, 1):
            for (a, b, samen) in ((x0, bx + 40, False), (bx + 40, x1, True)):
                pts = [(x, yc + teken_ * (straal_(x) + 8)) for x in range(a, b + 1, 4)]
                o.append(f'<path d="M{" L".join(f"{x},{y:.1f}" for x, y in pts)}" fill="none" stroke="{"#1d4ed8" if samen else "#93c5fd"}" stroke-width="{4 if samen else 2}"/>')
    o.append(f'<ellipse cx="{bx}" cy="{yc}" rx="30" ry="{hw+2}" fill="#d6a76c" stroke="{INK}" stroke-width="1.5"/>')
def fig_slok():
    o = []
    slokdarm(o, 40, 620, 145, 330)
    o.append(t(330, 150, 'voedsel', INK, size=13))
    o.append(t(150, 50, 'achter het voedsel', '#7f1d1d', size=14) + t(150, 68, 'kringspieren trekken samen', '#7f1d1d', size=13, w=600) + t(150, 86, 'lengtespieren ontspannen → nauw', '#7f1d1d', size=13, w=600))
    o.append(t(510, 42, 'vóór het voedsel', '#1e3a8a', size=14) + t(510, 60, 'lengtespieren trekken samen', '#1e3a8a', size=13, w=600) + t(510, 78, 'kringspieren ontspannen → kort en wijd', '#1e3a8a', size=13, w=600))
    o.append(straal(40, 222, 620, 222, INK, 2.5, pos=1) + t(330, 244, 'mond → maag', INK, size=13))
    o.append(f'<line x1="60" y1="272" x2="80" y2="272" stroke="#450a0a" stroke-width="4"/>' + t(88, 277, 'kringspieren samengetrokken', INK, 'start', 12, 600))
    o.append(f'<line x1="300" y1="272" x2="320" y2="272" stroke="#1d4ed8" stroke-width="4"/>' + t(328, 277, 'lengtespieren samengetrokken', INK, 'start', 12, 600))
    return svg(''.join(o), 660, 290)
def fig_golf():
    o = []
    for i, bx in enumerate((170, 330, 490)):
        y = 50 + i * 80
        slokdarm(o, 40, 620, y, bx, hw=20, toon_spieren=False)
        o.append(t(20, y + 5, f'{i+1}', INK, 'middle', 15))
    o.append(t(330, 290, 'de golf van samentrekkingen schuift op van de mond naar de maag: dat is peristaltiek', INK, size=13))
    return svg(''.join(o), 660, 305)

# ================================================================ B1 HOMEOSTASE EN FEEDBACK
b1_doelen = ['verwoorden dat planten en dieren als een <b>systeem</b> werken: ze vangen <b>prikkels</b> op, verwerken ze en reageren erop;',
             'de definitie van <b>prikkel</b> noteren en 4 voorbeelden geven uit het <b>intern</b> of het <b>extern milieu</b>;',
             'de definitie van <b>homeostase</b> noteren en 3 voorbeelden in ons lichaam geven;',
             'een <b>feedbacksysteem</b> schematisch en in eigen woorden voorstellen;',
             'uitleggen hoe een <b>negatief</b> en een <b>positief feedbacksysteem</b> werken en er een grafiek van tekenen;',
             '3 voorbeelden van feedbacksystemen bij planten en dieren geven.']
b1_vk = vk('Je lichaamstemperatuur is ongeveer 37 °C.', 'Huidmondjes bij planten gaan open en dicht (hoofdstuk 1).', 'Een grafiek lezen: wat staat er op de horizontale en op de verticale as?')
b1_1 = f'''{kader('Definitie', '<p>Een <b>prikkel</b> is een verandering in het <b>extern milieu</b> (de omgeving) of in het <b>intern milieu</b> (in het lichaam) die door een <b>receptor</b> kan worden opgevangen.</p>')}
<p>Planten en dieren werken als een <b>systeem</b>: ze vangen een prikkel op, verwerken die en reageren erop.</p>
{figuur(plat('svg-schema'), 'Van prikkel tot reactie: je raakt een hete kookplaat aan.')}
{ttabel(['Stap', 'Wat gebeurt er?'], [['prikkel', 'een verandering, bv. warmte'], ['receptor', 'vangt de prikkel op en zet ze om in een impuls'], ['verwerking', 'de hersenen of het ruggenmerg beslissen wat er moet gebeuren'], ['effector', 'voert de reactie uit: een spier of een klier'], ['effect (reactie)', 'wat er gebeurt, bv. je trekt je hand terug']])}
{ttabel(['Extern milieu (omgeving)', 'Intern milieu (in het lichaam)'], [['licht, geluid, warmte, een geur', 'te weinig water (dorst), te veel suiker in het bloed'], ['de bel van de tram aan de Beurs', 'een volle maag, een te hoge lichaamstemperatuur']])}
{tool(TOOL + '#f1', 'Oefen: intern of extern milieu?')}
{denk('denk_1', 'Je ruikt frieten bij een frietkot op het Flageyplein en je krijgt honger. Welke prikkel is dat, en komt hij uit het intern of het extern milieu?', [
  ('Prikkel', 'de geur van de frieten'), ('Milieu', 'De geur komt van buiten je lichaam: extern milieu.'), ('Let op', 'Je honger zelf (een lege maag) is een prikkel uit het intern milieu.')], 'De geur is een prikkel uit het extern milieu.')}'''
b1_2 = f'''{kader('Definitie', '<p><b>Homeostase</b> is het constant houden van het intern milieu.</p>')}
<p>Voorbeelden in ons lichaam:</p>
<ul><li>de <b>lichaamstemperatuur</b> blijft rond 37 °C;</li><li>de <b>bloedsuikerspiegel</b> (hoeveel suiker in je bloed zit) blijft binnen grenzen;</li><li>de <b>hoeveelheid water</b> in je lichaam blijft ongeveer gelijk.</li></ul>
<p>Constant betekent niet dat de waarde nooit verandert. De waarde schommelt een beetje rond een <b>normwaarde</b>, tussen een ondergrens en een bovengrens. Het evenwicht is <b>dynamisch</b>.</p>
{kader('Definitie', '<p>Een <b>feedbacksysteem</b> (terugkoppeling) is een systeem waarbij het <b>effect</b> van een reactie de reactie zelf bijstuurt.</p>')}
{denk('denk_2', 'Je sport in het Jubelpark en zweet veel. Je krijgt dorst en drinkt. Waarom is dit een voorbeeld van homeostase?', [
  ('Verstoring', 'Door zweten verlies je water: het intern milieu verandert.'), ('Reactie', 'Je krijgt dorst en drinkt, en je nieren houden water vast.'), ('Effect', 'De hoeveelheid water komt terug in de buurt van de normwaarde.')], 'Het lichaam houdt de hoeveelheid water constant: dat is homeostase.')}'''
b1_3 = f'''<h3>Negatief feedbacksysteem</h3>
<p>Bij een <b>negatief</b> feedbacksysteem werkt de reactie de verandering <b>tegen</b>. De waarde gaat terug naar de normwaarde. Zo zorgt het lichaam voor homeostase.</p>
{figuur(fig_neg(), 'Negatieve feedback: de lichaamstemperatuur schommelt rond de normwaarde.')}
<h3>Positief feedbacksysteem</h3>
<p>Bij een <b>positief</b> feedbacksysteem <b>versterkt</b> de reactie de verandering. De waarde gaat steeds verder weg, tot een gebeurtenis het proces stopt.</p>
{figuur(fig_pos(), 'Positieve feedback: de weeën worden steeds sterker, tot de baby geboren is.')}
{ttabel(['Voorbeeld', 'Soort', 'Hoe werkt het?'], [
  ['lichaamstemperatuur', 'negatief', 'te warm → zweten · te koud → rillen'],
  ['bloedsuikerspiegel', 'negatief', 'na het eten stijgt de suiker; de alvleesklier maakt insuline en de suiker daalt'],
  ['huidmondjes bij watertekort (plant)', 'negatief', 'de huidmondjes sluiten, de plant verdampt minder water'],
  ['bevalling', 'positief', 'weeën → meer hormoon → sterkere weeën'],
  ['bloedstolling', 'positief', 'stollingsstoffen lokken nog meer stollingsstoffen uit, tot de wonde dicht is'],
  ['rijpen van fruit (plant)', 'positief', 'rijpe appels maken etheen; dat laat ander fruit sneller rijpen']])}
{tool(TOOL + '#f2', 'Bekijk negatieve en positieve feedback in de tool')}
{denk('denk_3', 'Een rijpe appel ligt in een fruitschaal tussen groene bananen. Na twee dagen zijn de bananen geel. Is dat negatieve of positieve feedback?', [
  ('Wat gebeurt er?', 'De rijpe appel maakt etheen. Daardoor rijpen de bananen, en die maken zelf ook etheen.'), ('Gevolg', 'Er komt steeds meer etheen: het rijpen versnelt.')], 'Positieve feedback: de reactie versterkt zichzelf.')}'''
b1_oef = f'''{oef('opl_1', 1, 'Intern of extern milieu?', 'Komt de prikkel uit het intern of het extern milieu?<ol class="deelvragen" type="a"><li>de sirene van een ambulance</li><li>een lege maag</li><li>fel zonlicht</li><li>te weinig water in je lichaam</li><li>de geur van verse koffie</li><li>een te hoge lichaamstemperatuur door koorts</li></ol>', [
  ('a', 'extern'), ('b', 'intern'), ('c', 'extern'), ('d', 'intern'), ('e', 'extern'), ('f', 'intern')], 'Van buiten het lichaam = extern; in het lichaam = intern.')}
{oef('opl_2', 2, 'Het schema invullen', 'Vul voor elke situatie het schema in: prikkel → receptor → verwerking → effector → effect.<ol class="deelvragen" type="a"><li>Je hoort je naam en je draait je om.</li><li>Er vliegt stof in je oog en je knippert.</li></ol>', [
  ('a', 'geluid → mechanoreceptoren in het oor → hersenen → spieren van de nek → je draait je om'), ('b', 'stof (aanraking) → mechanoreceptoren in het oog → hersenstam (reflex) → oogspieren → je knippert')], 'Elke reactie volgt hetzelfde schema.')}
{oef('opl_3', 3, 'Definities', 'Noteer de definitie van <b>prikkel</b>, <b>homeostase</b> en <b>feedbacksysteem</b>.', [
  ('Prikkel', 'een verandering in het extern of intern milieu die door een receptor kan worden opgevangen'), ('Homeostase', 'het constant houden van het intern milieu'), ('Feedbacksysteem', 'een systeem waarbij het effect van een reactie de reactie zelf bijstuurt')], 'Leer deze drie definities woordelijk.')}
{oef('opl_4', 4, 'Grafiek tekenen', 'Teken een grafiek van de lichaamstemperatuur bij een negatief feedbacksysteem. Duid aan: normwaarde, bovengrens, ondergrens, en waar het lichaam zweet en waar het rilt.', [
  ('Assen', 'horizontaal: tijd · verticaal: lichaamstemperatuur'), ('Lijn', 'golft rond de normwaarde (37 °C), binnen de grenzen'), ('Reacties', 'boven de norm: zweten; onder de norm: rillen')], 'Bij negatieve feedback blijft de waarde schommelen rond de norm.')}
{oef('opl_5', 5, 'Negatief of positief?', '<ol class="deelvragen" type="a"><li>Je hebt het koud en je krijgt kippenvel en rilt.</li><li>Na een maaltijd daalt de suiker in je bloed weer.</li><li>Bij een wonde stolt het bloed steeds sneller.</li><li>Een plant in de zon sluit haar huidmondjes.</li><li>De weeën bij een bevalling worden steeds sterker.</li></ol>', [
  ('a', 'negatief'), ('b', 'negatief'), ('c', 'positief'), ('d', 'negatief'), ('e', 'positief')], 'Tegenwerken = negatief, versterken = positief.')}
{oef('opl_6', 6, 'Redeneren: waarom negatief?', 'Waarom zorgt vooral negatieve feedback voor homeostase, en positieve feedback niet?', [
  ('Negatief', 'De reactie werkt de verandering tegen: de waarde gaat terug naar de norm.'), ('Positief', 'De reactie versterkt de verandering: de waarde gaat verder weg van de norm, tot er iets het proces stopt.')], 'Homeostase = constant houden; dat lukt met tegenwerken.')}
{oef('opl_7', 7, 'Redeneren: de thermostaat', 'In de klas hangt een thermostaat op 20 °C. Wordt het 22 °C, wat doet de verwarming dan? Vergelijk met je lichaam: wat is de receptor, de verwerking en de effector?', [
  ('Thermostaat', 'Bij 22 °C slaat de verwarming af; de temperatuur daalt weer: negatieve feedback.'), ('Receptor', 'thermometer ↔ thermoreceptoren in de huid'), ('Verwerking', 'de thermostaat ↔ de hersenen'), ('Effector', 'de verwarming ↔ zweetklieren en spieren (rillen)')], 'Een technisch feedbacksysteem werkt zoals homeostase in je lichaam.')}'''
b1_sam = '''<p><b>Prikkel</b>: verandering in het extern of intern milieu die een receptor opvangt. Schema: prikkel → receptor → verwerking → effector → effect.</p>
<p><b>Homeostase</b>: het intern milieu constant houden (temperatuur, bloedsuiker, water). Dynamisch evenwicht rond een normwaarde.</p>
<p><b>Feedbacksysteem</b>: het effect stuurt de reactie bij. <b>Negatief</b>: werkt de verandering tegen (temperatuur, bloedsuiker, huidmondjes). <b>Positief</b>: versterkt de verandering (bevalling, bloedstolling, rijpen van fruit).</p>'''

# ================================================================ B2 RECEPTOREN BIJ DE MENS
b2_doelen = ['uitleggen welke <b>receptoren</b> welke prikkels opvangen en omzetten: foto-, mechano-, thermo-, chemo- en pijnreceptoren;',
             'met 2 voorbeelden uitleggen wat een <b>prikkeldrempel</b> is;',
             'met 2 voorbeelden uitleggen wat <b>prikkelgewenning</b> is en wat het effect is op de prikkeldrempel;',
             'uitleggen wat een <b>prikkelfilter</b> is.']
b2_vk = vk('<b>Prikkel</b>: een verandering in het extern of intern milieu (hoofdstuk feedbacksystemen).', 'Het schema prikkel → receptor → verwerking → effector → effect.')
b2_1 = f'''{kader('Definitie', '<p>Een <b>receptor</b> is een cel of een groep cellen die één soort prikkel opvangt en omzet in een <b>impuls</b> (een zenuwsignaal).</p>')}
{ttabel(['Receptor', 'Prikkel', 'Voorbeeld'], [
  ['fotoreceptoren', 'licht', 'staafjes en kegeltjes in het netvlies van het oog'],
  ['mechanoreceptoren', 'druk, aanraking, trilling en geluid', 'tastlichaampjes in de huid, haarcellen in het oor'],
  ['thermoreceptoren', 'warmte en koude', 'vrije zenuwuiteinden in de huid'],
  ['chemoreceptoren', 'chemische stoffen (geur, smaak)', 'reukcellen in de neus, smaakpapillen op de tong'],
  ['pijnreceptoren', 'beschadiging van weefsel', 'vrije zenuwuiteinden, bijna overal in het lichaam']])}
<p>Het woord helpt je: <i>foto</i> = licht, <i>mechano</i> = beweging, <i>thermo</i> = warmte, <i>chemo</i> = stof.</p>
{tool(TOOL + '#r1', 'Oefen: welke receptor vangt de prikkel op?')}
{denk('denk_1', 'Je hoort de metro aankomen in station De Brouckère. Welke receptoren vangen die prikkel op?', [
  ('Prikkel', 'geluid: trillingen van de lucht'), ('Receptor', 'trilling is beweging: mechanoreceptoren (haarcellen in het oor)')], 'Geluid vang je op met mechanoreceptoren.')}'''
b2_2 = f'''{kader('Definitie', '<p>De <b>prikkeldrempel</b> is de kleinste sterkte die een prikkel moet hebben om een impuls te veroorzaken.</p>')}
{figuur(fig_drempel(), 'Alleen een prikkel die sterker is dan de prikkeldrempel geeft een impuls.')}
<p>Voorbeelden: een heel zachte aanraking voel je niet. Een heel stil geluid hoor je niet.</p>
{kader('Definitie', '<p><b>Prikkelgewenning</b>: als een prikkel lang duurt, went de receptor eraan. De <b>prikkeldrempel stijgt</b> en je neemt de prikkel niet meer waar.</p>')}
{figuur(fig_drempel(True), 'Prikkelgewenning: de prikkel blijft even sterk, maar de drempel stijgt.')}
<p>Voorbeelden: na een paar minuten voel je je horloge niet meer. In een bakkerij ruik je de geur van brood na een tijd niet meer.</p>
{tool(TOOL + '#r2', 'Experimenteer met de prikkeldrempel in de tool')}
{denk('denk_2', 'Je stapt een bad in en het water voelt heel warm. Na vijf minuten voelt het gewoon aangenaam. Is het water afgekoeld?', [
  ('Water', 'Het water is nauwelijks afgekoeld.'), ('Receptoren', 'Je thermoreceptoren zijn gewend aan de warmte: hun prikkeldrempel is gestegen.')], 'Dat is prikkelgewenning.')}'''
b2_3 = f'''{kader('Definitie', '<p>De <b>prikkelfilter</b>: je hersenen laten niet alle impulsen door tot je bewustzijn. Onbelangrijke prikkels worden weggefilterd.</p>')}
<p>Zo hoor je het tikken van de klok niet, en voel je je kleren niet op je huid. Daardoor kan je je concentreren op wat belangrijk is.</p>
<p>Let op het verschil: bij <b>prikkelgewenning</b> stuurt de <b>receptor</b> minder impulsen. Bij de <b>prikkelfilter</b> komen de impulsen wel aan, maar je <b>hersenen</b> letten er niet op.</p>
{denk('denk_3', 'In een drukke klas hoor je plots je eigen naam, ook al was er veel lawaai. Hoe verklaar je dat?', [
  ('Lawaai', 'Je hersenen filteren de onbelangrijke geluiden weg.'), ('Je naam', 'Je naam is belangrijk voor jou: de prikkelfilter laat die impuls door.')], 'De prikkelfilter kiest wat belangrijk is.')}'''
b2_oef = f'''{oef('opl_1', 1, 'Welke receptor?', '<ol class="deelvragen" type="a"><li>Je ziet een bliksemflits.</li><li>Je proeft citroensap.</li><li>Je brandt je aan een kopje thee.</li><li>Je voelt een mug op je arm.</li><li>Je voelt dat het buiten vriest.</li><li>Je ruikt gas.</li><li>Je snijdt je in je vinger.</li></ol>', [
  ('a', 'fotoreceptoren'), ('b', 'chemoreceptoren'), ('c', 'thermoreceptoren en pijnreceptoren'), ('d', 'mechanoreceptoren'), ('e', 'thermoreceptoren'), ('f', 'chemoreceptoren'), ('g', 'pijnreceptoren')], 'Kijk naar het soort prikkel.')}
{oef('opl_2', 2, 'Definities', 'Noteer de definitie van receptor, prikkeldrempel, prikkelgewenning en prikkelfilter.', [
  ('Receptor', 'een cel of groep cellen die één soort prikkel opvangt en omzet in een impuls'), ('Prikkeldrempel', 'de kleinste sterkte van een prikkel die een impuls veroorzaakt'), ('Prikkelgewenning', 'bij een lange prikkel stijgt de prikkeldrempel: je neemt de prikkel niet meer waar'), ('Prikkelfilter', 'de hersenen laten onbelangrijke impulsen niet door tot je bewustzijn')], '')}
{oef('opl_3', 3, 'Drempel of gewenning?', 'Gaat het over de prikkeldrempel, prikkelgewenning of de prikkelfilter?<ol class="deelvragen" type="a"><li>Een stofje op je arm voel je niet.</li><li>Je voelt je ring na een tijd niet meer.</li><li>Tijdens een spannende film hoor je de auto\'s buiten niet.</li><li>In het zwembad lijkt het water eerst koud en later niet meer.</li></ol>', [
  ('a', 'prikkeldrempel: de prikkel is te zwak'), ('b', 'prikkelgewenning'), ('c', 'prikkelfilter'), ('d', 'prikkelgewenning')], 'Gewenning: de receptor went. Filter: de hersenen letten niet op.')}
{oef('opl_4', 4, 'Grafiek lezen', 'Teken een grafiek met een prikkeldrempel en vier prikkels van verschillende sterkte. Duid aan welke prikkels een impuls geven.', [
  ('Grafiek', 'een horizontale stippellijn voor de drempel en vier balkjes'), ('Impuls', 'alleen de balkjes die boven de drempel uitkomen')], 'Sterker dan de drempel → impuls.')}
{oef('opl_5', 5, 'Redeneren: gasgeur', 'Aan aardgas wordt een sterk ruikende stof toegevoegd. Waarom is prikkelgewenning bij een gaslek gevaarlijk?', [
  ('Lek', 'Je ruikt eerst de gasgeur.'), ('Gewenning', 'Na een tijd stijgt je prikkeldrempel en ruik je het gas niet meer, ook al is het er nog.')], 'Je denkt dat het gas weg is, terwijl het er nog is.')}
{oef('opl_6', 6, 'Redeneren: verschil', 'Leg het verschil uit tussen prikkelgewenning en de prikkelfilter. Waar gebeurt het telkens: in de receptor of in de hersenen?', [
  ('Prikkelgewenning', 'in de receptor: die stuurt minder impulsen, de drempel stijgt'), ('Prikkelfilter', 'in de hersenen: de impulsen komen aan, maar worden niet bewust')], 'Receptor tegenover hersenen.')}'''
b2_sam = '''<p><b>Receptor</b>: vangt één soort prikkel op en zet die om in een impuls. Foto (licht), mechano (druk, aanraking, geluid), thermo (warmte, koude), chemo (geur, smaak), pijn (beschadiging).</p>
<p><b>Prikkeldrempel</b>: kleinste sterkte die een impuls geeft. <b>Prikkelgewenning</b>: bij een lange prikkel stijgt de drempel. <b>Prikkelfilter</b>: de hersenen houden onbelangrijke impulsen buiten je bewustzijn.</p>'''

# ================================================================ B3 HET OOG
OOG = namen('fig-oog'); NET = namen('fig-netvlies')
b3_doelen = ['de <b>inwendige delen van het oog</b> benoemen, herkennen en hun functie geven;',
             'de delen van het <b>netvlies</b> benoemen en herkennen: zenuwcellen, fotoreceptoren, pigmentcellen;',
             'op tekeningen de <b>weg van het licht</b> in het oog aanduiden;',
             '<b>staafjes</b> en <b>kegeltjes</b> vergelijken: vorm, aantal, plaats, waarneming en werking;',
             'uitleggen hoe de fotoreceptoren beelden en <b>kleuren</b> opvangen;',
             'uitleggen dat het beeld in de <b>hersenen</b> verwerkt wordt en wat een <b>optische illusie</b> is.']
b3_vk = vk('<b>Fotoreceptoren</b> vangen licht op (hoofdstuk 1).', 'Een bolle <b>lens</b> maakt een omgekeerd beeld (fysica, optica).', 'Licht gaat rechtdoor in een middenstof.')
b3_1 = f'''{figuur(lab('fig-oog'), 'Doorsnede van het oog. Het licht komt van links. Tekening: Rhcastilhos en Jmarchn, Wikimedia Commons, publiek domein.')}
{ttabel(['Deel', 'Functie'], [
  ['hoornvlies', 'doorzichtig, bol vlies vooraan; breekt het licht al sterk'],
  ['voorste oogkamer (kamervocht)', 'helder vocht; voedt hoornvlies en lens'],
  ['regenboogvlies (iris)', 'gekleurde ring met spiertjes; maakt de pupil groter of kleiner'],
  ['pupil', 'opening in de iris; laat licht binnen'],
  ['lens', 'doorzichtig en vervormbaar; breekt het licht zodat er een scherp beeld op het netvlies valt'],
  ['straalvormig lichaam en lensbandjes', 'spiertjes en vezels die de lens boller of platter maken'],
  ['glasachtig lichaam', 'doorzichtige gelei; geeft het oog zijn vorm'],
  ['harde oogrok', 'stevige, witte buitenlaag; beschermt het oog'],
  ['vaatvlies', 'bloedvaten die het oog voeden; donker, zodat licht niet weerkaatst'],
  ['netvlies', 'binnenste laag met de fotoreceptoren'],
  ['gele vlek', 'meeste kegeltjes; hier zie je het scherpst en in kleur'],
  ['blinde vlek', 'waar de oogzenuw vertrekt; geen fotoreceptoren, je ziet er niets'],
  ['oogzenuw', 'brengt de impulsen naar de hersenen']])}
{tool(TOOL + '#r3', 'Oefen de delen van het oog: Zelf aanduiden')}'''
b3_2 = f'''<p>Het licht gaat door: <b>hoornvlies → voorste oogkamer → pupil → lens → glasachtig lichaam → netvlies</b>. De fotoreceptoren zetten het licht om in impulsen. De <b>oogzenuw</b> brengt ze naar de hersenen.</p>
{figuur(fig_lichtweg(), 'Op het netvlies ontstaat een omgekeerd en verkleind beeld van de kaars.')}
<p>Op het netvlies ontstaat een <b>omgekeerd en verkleind</b> beeld. Je hersenen draaien het om: je ziet de wereld rechtop.</p>
{tool(TOOL + '#r4', 'Volg de weg van het licht stap voor stap')}
{figuur(fig_blindevlek(), 'Proef: de blinde vlek.')}
{denk('denk_1', 'Doe de proef met de figuur hierboven. Sluit je linkeroog. Kijk met je rechteroog naar het kruisje en breng het blad langzaam dichter. Op een bepaalde afstand verdwijnt de stip. Waarom?', [
  ('Wat gebeurt er?', 'Het beeld van de stip valt dan net op de blinde vlek.'), ('Blinde vlek', 'Daar vertrekt de oogzenuw en liggen geen fotoreceptoren.')], 'Licht dat op de blinde vlek valt, wordt niet opgevangen: je ziet de stip niet.')}'''
b3_3 = f'''<p>Het netvlies heeft drie lagen: <b>zenuwcellen</b>, <b>fotoreceptoren</b> (staafjes en kegeltjes) en <b>pigmentcellen</b>. Let op: het licht gaat eerst <b>door</b> de laag zenuwcellen voor het de fotoreceptoren bereikt.</p>
{figuur(lab('fig-netvlies'), 'Het netvlies. Het licht komt van boven.')}
{ttabel(['', 'Staafjes', 'Kegeltjes'], [['vorm', 'staafvormig', 'kegelvormig'], ['aantal', '± 120 miljoen', '± 6 miljoen'], ['plaats', 'vooral aan de rand van het netvlies', 'vooral in de gele vlek'],
  ['werkt bij', 'weinig licht (schemer, nacht)', 'veel licht (overdag)'], ['kleuren zien', 'nee: alleen grijstinten', 'ja: rood, groen en blauw'], ['scherpte', 'weinig scherp', 'scherp']])}
<h3>Kleuren zien</h3>
<p>Er zijn drie soorten kegeltjes: gevoelig voor <b>rood</b>, <b>groen</b> en <b>blauw</b> licht. Je hersenen maken van de combinatie van hun impulsen een kleur. Rood + groen geeft geel. In het donker werken alleen de staafjes: dan zie je alleen grijstinten.</p>
{figuur(plat('svg-kleur'), 'Rode en groene kegeltjes geven samen de kleur geel.')}
{tool(TOOL + '#r5', 'Oefen: staafje of kegeltje?')}
{denk('denk_2', "Waarom zie je 's nachts in het Zoniënwoud geen kleuren?", [
  ('Weinig licht', 'De kegeltjes werken alleen bij veel licht.'), ('Staafjes', 'Bij weinig licht werken alleen de staafjes, en die zien geen kleur.')], 'Je ziet alleen grijstinten.')}'''
b3_4 = f'''<p>Je ogen vangen licht op, maar je <b>hersenen</b> maken er een beeld van. Daarbij gebruiken ze ervaring en verwachtingen.</p>
{kader('Definitie', '<p>Een <b>optische illusie</b> is een beeld dat je hersenen anders verwerken dan het in werkelijkheid is.</p>')}
{figuur(fig_muller(), 'Welke lijn is het langst?')}
<p>De twee lijnen zijn even lang. Door de pijlpunten verwerken je hersenen lijn A als langer.</p>
{tool(TOOL + '#r7', 'Bekijk meer optische illusies')}'''
b3_oef = f'''{oef_fig('opl_1', 1, 'Delen van het oog', 'Schrijf de naam van elk deel.', num('fig-oog'), [(str(i + 1), n) for i, n in enumerate(OOG)], 'Werk van voor (links) naar achter (rechts).', lab('fig-oog'))}
{oef('opl_2', 2, 'Functies', 'Welk deel van het oog …<ol class="deelvragen" type="a"><li>maakt de pupil groter of kleiner?</li><li>brengt impulsen naar de hersenen?</li><li>breekt het licht en kan boller of platter worden?</li><li>bevat de fotoreceptoren?</li><li>beschermt het oog aan de buitenkant?</li><li>is de plaats waar je het scherpst ziet?</li></ol>', [
  ('a', 'het regenboogvlies (iris)'), ('b', 'de oogzenuw'), ('c', 'de lens'), ('d', 'het netvlies'), ('e', 'de harde oogrok'), ('f', 'de gele vlek')], '')}
{oef('opl_3', 3, 'De weg van het licht', 'Zet in de juiste volgorde: <i>lens – netvlies – hoornvlies – glasachtig lichaam – pupil – voorste oogkamer</i>.', [
  ('Volgorde', 'hoornvlies → voorste oogkamer → pupil → lens → glasachtig lichaam → netvlies')], 'Van buiten naar binnen.')}
{oef_fig('opl_4', 4, 'Het netvlies', 'Benoem de delen van het netvlies. Duid met een pijl aan van waar het licht komt.', num('fig-netvlies'), [(str(i + 1), n) for i, n in enumerate(NET)] + [('Licht', 'van boven: eerst door de zenuwcellen')], 'Het licht gaat eerst door de zenuwcellen.', lab('fig-netvlies'))}
{oef('opl_5', 5, 'Staafje of kegeltje?', '<ol class="deelvragen" type="a"><li>Ik zie kleuren.</li><li>Ik werk in het donker.</li><li>Ik zit vooral in de gele vlek.</li><li>Er zijn er ongeveer 120 miljoen van mij.</li><li>Ik geef een scherp beeld.</li></ol>', [
  ('a', 'kegeltje'), ('b', 'staafje'), ('c', 'kegeltje'), ('d', 'staafje'), ('e', 'kegeltje')], '')}
{oef('opl_6', 6, 'Redeneren: een ster zien', 'Een zwakke ster zie je beter als je er een beetje <b>naast</b> kijkt dan als je er recht naar kijkt. Leg uit.', [
  ('Recht kijken', 'Het beeld valt op de gele vlek: daar zitten vooral kegeltjes, die weinig licht niet opvangen.'), ('Naast kijken', 'Het beeld valt naast de gele vlek, waar meer staafjes zitten. Die werken wel bij weinig licht.')], 'Staafjes zijn gevoeliger voor zwak licht.')}
{oef('opl_7', 7, 'Redeneren: optische illusie', 'Leg uit waarom je bij een optische illusie iets anders ziet dan er is. Gebruik de woorden ogen, impulsen en hersenen.', [
  ('Ogen', 'Je ogen vangen het licht juist op en sturen impulsen.'), ('Hersenen', 'Je hersenen verwerken de impulsen met ervaring en verwachtingen, en maken er een ander beeld van.')], 'Je ziet met je hersenen, niet alleen met je ogen.')}
{oef('opl_8', 8, 'Kleuren zien', '<ol class="deelvragen" type="a"><li>Welke drie soorten kegeltjes heb je?</li><li>Het licht van een gele banaan prikkelt vooral je rode en groene kegeltjes. Welke kleur maken je hersenen?</li><li>Waarom zie je de kleur van de banaan niet in een donkere kamer?</li><li>Elke pixel op het scherm van je gsm of spelconsole heeft een rood, een groen en een blauw lichtje. Hoe kan je scherm dan geel tonen?</li></ol>', [
  ('a', 'kegeltjes voor rood, groen en blauw licht'), ('b', 'geel: de hersenen combineren de impulsen van de rode en groene kegeltjes'), ('c', 'Bij weinig licht werken alleen de staafjes, en die zien geen kleuren.'), ('d', 'De rode en groene lichtjes branden samen. Ze prikkelen je rode en groene kegeltjes, net als de banaan. Je hersenen maken er geel van.')], 'De hersenen maken de kleur uit de impulsen van de kegeltjes.')}'''
b3_sam = '''<p><b>Delen</b>: hoornvlies, voorste oogkamer, iris, pupil, lens, straalvormig lichaam, lensbandjes, glasachtig lichaam, harde oogrok, vaatvlies, netvlies, gele vlek, blinde vlek, oogzenuw.</p>
<p><b>Weg van het licht</b>: hoornvlies → voorste oogkamer → pupil → lens → glasachtig lichaam → netvlies. Op het netvlies: omgekeerd, verkleind beeld. Oogzenuw → hersenen.</p>
<p><b>Netvlies</b>: zenuwcellen, fotoreceptoren, pigmentcellen. <b>Staafjes</b>: veel, rand, weinig licht, geen kleur. <b>Kegeltjes</b>: minder, gele vlek, veel licht, kleur (rood, groen, blauw), scherp.</p>
<p>De <b>hersenen</b> maken het beeld. <b>Optische illusie</b>: de hersenen verwerken een beeld anders dan het is.</p>'''

# ================================================================ B4 RECEPTOREN BIJ ANDERE ORGANISMEN
b4_doelen = ['verschillende <b>receptoren bij dieren</b> herkennen aan de hand van voorbeelden;', 'verschillende <b>receptoren bij planten</b> herkennen aan de hand van voorbeelden.']
b4_vk = vk('De vijf soorten receptoren bij de mens: foto-, mechano-, thermo-, chemo- en pijnreceptoren (hoofdstuk 1).')
b4_1 = f'''<p>Ook dieren vangen prikkels op. Sommige dieren hebben receptoren voor prikkels die wij <b>niet</b> waarnemen.</p>
{ttabel(['Dier', 'Prikkel', 'Receptor'], [
  ['groefkopslang', 'warmte (lichaamswarmte van een prooi)', 'warmtegevoelige putjes tussen oog en neusgat: thermoreceptoren'],
  ['vleermuis', 'de echo van haar eigen hoge geluiden (echolocatie)', 'oren: mechanoreceptoren'],
  ['haai', 'zwakke elektrische velden van de spieren van prooien', 'elektroreceptoren'],
  ['bij', 'ultraviolet licht (uv-patronen op bloemen)', 'ogen: fotoreceptoren'],
  ['kat', 'luchtstroompjes, de breedte van een opening', 'snorharen met mechanoreceptoren']])}
{tool(TOOL + '#r8', 'Bekijk receptoren bij dieren en planten')}'''
b4_2 = f'''<p>Planten hebben geen zenuwen, maar ze vangen wel prikkels op en reageren erop.</p>
{ttabel(['Plant', 'Prikkel', 'Reactie'], [
  ['zonnebloem', 'licht', 'de stengel groeit naar het licht toe (<b>fototropie</b>)'],
  ['kiemende boon', 'zwaartekracht', 'de wortel groeit naar beneden, de stengel naar boven (<b>geotropie</b>)'],
  ['kruidje-roer-mij-niet', 'aanraking', 'de blaadjes vouwen dicht'],
  ['venusvliegenval', 'aanraking van de haartjes (twee keer)', 'de val klapt dicht']])}
{denk('denk_1', 'Een plant staat op de vensterbank van de klas. Na een week buigt de stengel naar het raam. Welke prikkel, en hoe heet die reactie?', [
  ('Prikkel', 'licht dat van één kant komt'), ('Reactie', 'de stengel groeit naar het licht')], 'Fototropie.')}'''
b4_oef = f'''{oef('opl_1', 1, 'Welke prikkel?', 'Welke prikkel vangt het organisme op?<ol class="deelvragen" type="a"><li>Een vleermuis vindt een mug in het donker.</li><li>Een slang vindt een muis in het donker.</li><li>Een bij vindt de nectar van een bloem.</li><li>Een haai vindt een vis die onder het zand zit.</li><li>De wortel van een boon groeit naar beneden.</li></ol>', [
  ('a', 'geluid (echo)'), ('b', 'warmte'), ('c', 'uv-licht'), ('d', 'zwakke elektrische velden'), ('e', 'zwaartekracht')], '')}
{oef('opl_2', 2, 'Welke receptor?', 'Welke soort receptor gebruikt het dier?<ol class="deelvragen" type="a"><li>de snorharen van een kat</li><li>de putjes van een groefkopslang</li><li>de ogen van een bij</li></ol>', [
  ('a', 'mechanoreceptoren'), ('b', 'thermoreceptoren'), ('c', 'fotoreceptoren')], '')}
{oef('opl_3', 3, 'Fototropie of geotropie?', '<ol class="deelvragen" type="a"><li>Een kamerplant groeit scheef naar het raam.</li><li>Je legt een kiemende boon schuin, en de wortel buigt naar beneden.</li><li>Zonnebloemen draaien mee met de zon.</li></ol>', [
  ('a', 'fototropie'), ('b', 'geotropie'), ('c', 'fototropie')], 'Foto = licht, geo = aarde (zwaartekracht).')}
{oef('opl_4', 4, 'Redeneren: de venusvliegenval', 'De val van een venusvliegenval klapt pas dicht als een haartje <b>twee keer</b> aangeraakt wordt. Waarom is dat nuttig voor de plant?', [
  ('Eén keer', 'Een regendruppel of een blad kan de val per ongeluk één keer raken.'), ('Twee keer', 'Een levend insect beweegt en raakt de haartjes meerdere keren.'), ('Nut', 'De plant verspilt geen energie aan dichtklappen voor niets.')], 'Zo reageert de val alleen op een prooi.')}'''
b4_sam = '''<p><b>Dieren</b>: groefkopslang (warmte), vleermuis (echo), haai (elektrische velden), bij (uv-licht), kat (snorharen).</p>
<p><b>Planten</b>: fototropie (groeien naar het licht), geotropie (wortel naar beneden), kruidje-roer-mij-niet en venusvliegenval (aanraking).</p>'''

# ================================================================ B5 DE MENS REAGEERT
b5_doelen = ['voor eigen voorbeelden het schema <b>prikkel → receptor → verwerking → effector → effect</b> invullen en noteren of de reactie <b>bewust</b> of <b>onbewust</b> is;',
             'uitleggen hoe je via <b>spieren</b> of <b>klieren</b>, bewust of onbewust, op prikkels reageert.']
b5_vk = vk('Het schema prikkel → receptor → verwerking → effector → effect (thema 1).', 'De vijf soorten receptoren (thema 2).')
b5_1 = f'''{kader('Definitie', '<p>Een <b>effector</b> voert de reactie uit. Bij de mens zijn dat <b>spieren</b> (beweging) en <b>klieren</b> (afscheiding van een stof).</p>')}
{figuur(plat('svg-schema'), 'Het schema van een reactie.')}
{ttabel(['', 'Bewuste reactie', 'Onbewuste reactie'], [['wat?', 'je denkt erover na en kiest', 'gebeurt vanzelf, zonder nadenken'], ['voorbeeld', 'je hoort de bel en je pakt je boekentas', 'je trekt je hand terug van een hete pot (reflex), je hart slaat sneller bij schrik']])}
{ttabel(['Effector', 'Voorbeeld van een reactie'], [['spieren', 'je trapt op de rem van je fiets; je knippert met je ogen'], ['klieren', 'speekselklieren maken speeksel als je eten ruikt; zweetklieren maken zweet; de bijnieren maken adrenaline bij schrik']])}
{tool(TOOL + '#e1', 'Vul het schema in voor verschillende situaties')}
{denk('denk_1', 'Iemand roept plots luid achter je op de tram. Je schrikt en je hart gaat sneller slaan. Vul het schema in. Is de reactie bewust of onbewust?', [
  ('Prikkel en receptor', 'luid geluid → mechanoreceptoren in het oor'), ('Verwerking', 'hersenen'), ('Effector en effect', 'klieren (bijnieren) maken adrenaline → het hart slaat sneller'), ('Bewust?', 'Nee, het gebeurt vanzelf.')], 'Een onbewuste reactie via een klier.')}'''
b5_oef = f'''{oef('opl_1', 1, 'Schema invullen', 'Vul het schema in en noteer of de reactie bewust of onbewust is.<ol class="deelvragen" type="a"><li>Je ruikt pannenkoeken en je mond wordt nat.</li><li>Je ziet het voetgangerslicht op groen springen en je steekt over.</li><li>Je stapt op een punaise en trekt meteen je voet op.</li><li>Het is warm in de klas en je begint te zweten.</li><li>Je gamet. Op je scherm duikt plots een tegenstander op en je drukt op de knop.</li></ol>', [
  ('a', 'geur → chemoreceptoren → hersenen → speekselklieren → speeksel · onbewust'), ('b', 'licht → fotoreceptoren → hersenen → beenspieren → je stapt · bewust'),
  ('c', 'beschadiging → pijnreceptoren → ruggenmerg (reflex) → beenspieren → voet omhoog · onbewust'), ('d', 'warmte → thermoreceptoren → hersenen → zweetklieren → zweet · onbewust'), ('e', 'licht → fotoreceptoren → hersenen → spieren in je vingers → je drukt · bewust')], 'Spieren bewegen, klieren maken een stof.')}
{oef('opl_2', 2, 'Spier of klier?', '<ol class="deelvragen" type="a"><li>tranen bij het snijden van ajuin</li><li>je hoofd draaien</li><li>kippenvel</li><li>maagsap na het eten</li></ol>', [
  ('a', 'klier (traanklier)'), ('b', 'spier'), ('c', 'spier (haarspiertjes)'), ('d', 'klier')], '')}
{oef('opl_3', 3, 'Redeneren: reflex', 'Waarom is het nuttig dat je je hand van een hete kookplaat terugtrekt <b>zonder</b> erover na te denken?', [
  ('Sneller', 'Bij een reflex gaat de impuls via het ruggenmerg en niet eerst naar de bewuste hersenen.'), ('Gevolg', 'Je reageert sneller en verbrandt je minder erg.')], 'Een reflex beschermt je.')}
{oef('opl_4', 4, 'Eigen voorbeeld', 'Bedenk zelf een voorbeeld van een bewuste reactie en een onbewuste reactie uit je dag. Vul telkens het volledige schema in.', [
  ('Bewust', 'bv. je ziet de tram aankomen → je loopt sneller: licht → fotoreceptoren → hersenen → beenspieren'), ('Onbewust', 'bv. fel zonlicht → je pupil wordt kleiner: licht → fotoreceptoren → hersenen → spiertjes van de iris')], 'Controleer: elke stap van het schema moet erin staan.')}'''
b5_sam = '''<p><b>Effectoren</b> voeren de reactie uit: <b>spieren</b> (beweging) en <b>klieren</b> (afscheiding van een stof).</p>
<p>Schema: prikkel → receptor → verwerking → effector → effect. Een reactie is <b>bewust</b> (je kiest) of <b>onbewust</b> (vanzelf, bv. een reflex).</p>'''

# ================================================================ B6 SPIEREN
SP = namen('fig-spieren')
def spiertypes_abc():
    import re
    f = plat('svg-spiertypes')
    for oud, nieuw in (('dwarsgestreepte spier', 'C'), ('gladde spier', 'A'), ('hartspier', 'B')):
        f = f.replace('>' + oud + '<', '>' + nieuw + '<')
    for weg in ('skeletspieren (bv. biceps)', 'wand van darmen en bloedvaten', 'alleen in het hart'):
        f = f.replace('>' + weg + '<', '><')
    return f
b6_doelen = ['deze spieren aanduiden en benoemen: <b>biceps, triceps, buikspieren, rugspieren, hamstrings, quadriceps</b>;',
             'de functie van <b>spieren</b> uitleggen;', 'de functie van een <b>pees</b> en van een <b>gewricht</b> uitleggen en 5 voorbeelden van gewrichten geven;',
             '<b>dwarsgestreepte spier, gladde spier en hartspier</b> vergelijken en op een afbeelding herkennen;',
             'uitleggen hoe spieren <b>samentrekken</b> en hoe ze <b>ontspannen</b> door hun <b>antagonist</b>, bij biceps en triceps en bij de <b>kringspieren</b> van de slokdarm.']
b6_vk = vk('<b>Effector</b>: spieren en klieren voeren de reactie uit (hoofdstuk 1).', 'Je skelet bestaat uit botten.')
b6_1 = f'''{kader('Onthoud', '<p>Spieren zorgen voor <b>beweging</b>. Een spier kan alleen <b>samentrekken</b> (korter en dikker worden). Ze kan zichzelf niet uitrekken.</p>')}
{figuur(lab('fig-spieren'), 'Belangrijke spieren aan de voorkant en de achterkant.')}
<ul><li>Een <b>pees</b> verbindt een spier met een bot. Bv. de achillespees.</li><li>Een <b>gewricht</b> is een beweegbare verbinding tussen twee botten.</li></ul>
{ttabel(['Gewricht', 'Soort', 'Beweging'], [['schoudergewricht', 'kogelgewricht', 'in alle richtingen'], ['heupgewricht', 'kogelgewricht', 'in alle richtingen'], ['ellebooggewricht', 'scharniergewricht', 'buigen en strekken'], ['kniegewricht', 'scharniergewricht', 'buigen en strekken'], ['vingergewrichten', 'scharniergewrichten', 'buigen en strekken'], ['polsgewricht', '', 'in twee richtingen'], ['enkelgewricht', '', 'voet op en neer']])}
{tool(TOOL + '#e2', 'Oefen de spieren: Zelf aanduiden')}'''
b6_2 = f'''{figuur(plat('svg-spiertypes'), 'De drie soorten spierweefsel onder de microscoop.')}
{ttabel(['', 'Dwarsgestreepte spier', 'Gladde spier', 'Hartspier'], [
  ['waar?', 'skeletspieren (bv. biceps)', 'wand van darmen en bloedvaten', 'alleen in het hart'],
  ['dwarse strepen', 'ja', 'nee', 'ja'], ['kernen', 'veel kernen per cel, aan de rand', 'één kern per cel, in het midden', 'één kern per cel, in het midden'],
  ['cellen vertakt', 'nee', 'nee', 'ja'], ['werking', 'bewust (je kan ze sturen)', 'onbewust (vanzelf)', 'onbewust (vanzelf)'], ['vermoeid', 'raakt snel vermoeid', 'raakt niet snel vermoeid', 'raakt niet vermoeid']])}
{tool(TOOL + '#e3', 'Oefen: kruis de juiste vakjes aan')}'''
b6_3 = f'''<p>Een spier trekt samen als ze een <b>impuls</b> krijgt. Ze kan zichzelf niet uitrekken. Dat doet haar <b>antagonist</b>: de spier die de tegengestelde beweging maakt.</p>
{figuur(fig_armen(), 'Biceps en triceps zijn antagonisten.')}
<p>Andere antagonisten: <b>quadriceps</b> (been strekken) en <b>hamstrings</b> (been buigen).</p>
<h3>De slokdarm: peristaltiek</h3>
<p>In de wand van de slokdarm liggen twee lagen <b>gladde spieren</b>:</p>
<ul><li><b>kringspieren</b> liggen in een kring rond de slokdarm. Trekken ze samen, dan wordt de slokdarm <b>nauwer</b>.</li>
<li><b>lengtespieren</b> liggen in de lengte van de slokdarm. Trekken ze samen, dan wordt de slokdarm <b>korter en wijder</b>.</li></ul>
<p>Kringspieren en lengtespieren zijn <b>antagonisten</b>: als de ene soort samentrekt, ontspant de andere.</p>
{figuur(fig_slok(), 'Achter het voedsel wordt de slokdarm nauw, vóór het voedsel wordt hij kort en wijd.')}
{ttabel(['Plaats', 'Kringspieren', 'Lengtespieren', 'Gevolg'], [['achter het voedsel', 'trekken samen', 'ontspannen', 'de slokdarm wordt nauw en duwt het voedsel verder'], ['vóór het voedsel', 'ontspannen', 'trekken samen', 'de slokdarm wordt kort en wijd: het voedsel kan erin']])}
{kader('Definitie', '<p><b>Peristaltiek</b> is een golf van samentrekkingen van de kringspieren en de lengtespieren, die het voedsel door de slokdarm (en de darmen) naar de maag duwt. Ze gebeurt <b>onbewust</b>.</p>')}
{figuur(fig_golf(), 'Drie momenten na elkaar: de vernauwing en het voedsel schuiven samen op.')}
{tool(TOOL + '#e4', 'Bekijk het samentrekken en ontspannen in de tool')}
{denk('denk_1', 'Je kan een glas water ondersteboven drinken (bv. met je hoofd naar beneden). Hoe komt het water dan toch in je maag?', [
  ('Zwaartekracht', 'Die helpt hier niet.'), ('Slokdarm', 'Door peristaltiek: achter het water trekken de kringspieren samen, ervoor de lengtespieren. Die golf duwt het water naar de maag.')], 'De spieren van de slokdarm doen het werk, niet de zwaartekracht.')}'''
b6_oef = f'''{oef_fig('opl_1', 1, 'Spieren benoemen', 'Schrijf de naam bij elk nummer.', num('fig-spieren'), [(str(i + 1), n) for i, n in enumerate(SP)], '', lab('fig-spieren'))}
{oef('opl_2', 2, 'Pees en gewricht', '<ol class="deelvragen" type="a"><li>Wat is de functie van een pees?</li><li>Wat is een gewricht?</li><li>Noem 5 gewrichten.</li></ol>', [
  ('a', 'Een pees verbindt een spier met een bot.'), ('b', 'een beweegbare verbinding tussen twee botten'), ('c', 'bv. schouder, elleboog, pols, heup, knie, enkel, vingers')], '')}
{oef('opl_3', 3, 'Welk spierweefsel?', '<ol class="deelvragen" type="a"><li>Ik heb dwarse strepen en vertakte cellen.</li><li>Ik zit in de wand van je darmen.</li><li>Ik heb veel kernen aan de rand van de cel.</li><li>Ik werk bewust.</li><li>Ik word nooit moe.</li></ol>', [
  ('a', 'hartspier'), ('b', 'gladde spier'), ('c', 'dwarsgestreepte spier'), ('d', 'dwarsgestreepte spier'), ('e', 'hartspier')], '')}
{oef('opl_4', 4, 'Biceps en triceps', 'Je buigt je arm om een boekentas op te tillen. Daarna strek je hem. Welke spier trekt telkens samen, en welke ontspant?', [
  ('Buigen', 'de biceps trekt samen, de triceps ontspant'), ('Strekken', 'de triceps trekt samen, de biceps wordt uitgerekt')], 'Antagonisten werken tegen elkaar in.')}
{oef('opl_5', 5, 'Redeneren: waarom per twee?', 'Waarom moeten spieren in paren werken? Gebruik het woord antagonist.', [
  ('Spier', 'Een spier kan alleen samentrekken en zichzelf niet uitrekken.'), ('Antagonist', 'De spier met de tegengestelde beweging rekt ze weer uit.')], 'Zonder antagonist zou een gebogen arm gebogen blijven.')}
{oef('opl_6', 6, 'Peristaltiek', 'Een hap brood zit halverwege de slokdarm.<ol class="deelvragen" type="a"><li>Wat doen de kringspieren en de lengtespieren <b>achter</b> de hap?</li><li>En <b>vóór</b> de hap?</li><li>Wat is peristaltiek?</li><li>Is peristaltiek bewust of onbewust? Welk soort spierweefsel?</li></ol>', [
  ('a', 'kringspieren trekken samen, lengtespieren ontspannen: de slokdarm wordt nauw en duwt de hap verder'), ('b', 'lengtespieren trekken samen, kringspieren ontspannen: de slokdarm wordt kort en wijd'),
  ('c', 'een golf van samentrekkingen die het voedsel naar de maag duwt'), ('d', 'onbewust; gladde spieren')], 'Kringspieren en lengtespieren zijn antagonisten.')}
{oef('opl_7', 7, 'Redeneren: het hart', 'Waarom is het belangrijk dat de hartspier onbewust werkt en niet vermoeid raakt?', [
  ('Onbewust', 'Je hart moet ook kloppen als je slaapt of aan iets anders denkt.'), ('Niet vermoeid', 'Het hart klopt je hele leven zonder pauze.')], 'Zo blijft het bloed altijd stromen.')}
{oef('opl_8', 8, 'Spierweefsel herkennen', 'Je ziet drie soorten spierweefsel onder de microscoop. Welk weefsel is A, B en C? Waaraan herken je het?' + figuur(spiertypes_abc(), ''), [
  ('A', 'gladde spier: spoelvormige cellen zonder strepen, één kern in het midden'), ('B', 'hartspier: vertakte cellen met strepen, één kern in het midden'), ('C', 'dwarsgestreepte spier: lange cellen met dwarse strepen en veel kernen aan de rand')],
  'Let op de strepen, de kernen en de vertakkingen.')}'''
b6_sam = '''<p>Spieren zorgen voor <b>beweging</b>; ze kunnen alleen <b>samentrekken</b>. Een <b>pees</b> verbindt spier en bot. Een <b>gewricht</b> verbindt twee botten beweegbaar.</p>
<p><b>Dwarsgestreept</b>: skelet, strepen, veel kernen aan de rand, bewust, snel moe. <b>Glad</b>: darmen en bloedvaten, geen strepen, één kern, onbewust. <b>Hartspier</b>: strepen, vertakt, één kern, onbewust, nooit moe.</p>
<p><b>Antagonisten</b>: biceps (buigen) en triceps (strekken); quadriceps en hamstrings; kringspieren en lengtespieren van de slokdarm.</p>
<p><b>Peristaltiek</b>: achter het voedsel trekken de kringspieren samen (nauw), vóór het voedsel de lengtespieren (kort en wijd). Die golf duwt het voedsel naar de maag. Onbewust, gladde spieren.</p>'''

I = lambda deel: f'Werk dit hoofdstuk samen met de tool <a href="{TOOL}{deel}">Water, prikkels en reacties</a>. Oefeningen maak je op papier.'
maak('cursus-homeostase.html', T1 + '2', 'Homeostase en feedbacksystemen', I('#f1'), b1_doelen, b1_vk,
     [('Een organisme als systeem', b1_1), ('Homeostase', b1_2), ('Negatieve en positieve feedback', b1_3)], b1_oef, b1_sam, (TOOL + '#f2', 'Oefen verder in de tool'))
maak('cursus-receptoren.html', T2 + '1', 'Receptoren bij de mens', I('#r1'), b2_doelen, b2_vk,
     [('Soorten receptoren', b2_1), ('Prikkeldrempel en prikkelgewenning', b2_2), ('De prikkelfilter', b2_3)], b2_oef, b2_sam, (TOOL + '#r1', 'Oefen verder in de tool'))
maak('cursus-oog.html', T2 + '2 en 3', 'Bouw en werking van het oog', I('#r3'), b3_doelen, b3_vk,
     [('Bouw van het oog', b3_1), ('De weg van het licht', b3_2), ('Het netvlies: staafjes en kegeltjes', b3_3), ('Beeldverwerking in de hersenen', b3_4)], b3_oef, b3_sam, (TOOL + '#r3', 'Oefen verder in de tool'))
maak('cursus-receptoren-organismen.html', T2 + '4', 'Receptoren bij andere organismen', I('#r8'), b4_doelen, b4_vk,
     [('Receptoren bij dieren', b4_1), ('Receptoren bij planten', b4_2)], b4_oef, b4_sam, (TOOL + '#r8', 'Bekijk de voorbeelden in de tool'))
maak('cursus-reageren.html', T3 + '1', 'De mens reageert op prikkels', I('#e1'), b5_doelen, b5_vk,
     [('Effectoren: spieren en klieren', b5_1)], b5_oef, b5_sam, (TOOL + '#e1', 'Oefen verder in de tool'))
maak('cursus-spieren.html', T3 + '2', 'Reactie door spieren', I('#e2'), b6_doelen, b6_vk,
     [('Spieren, pezen en gewrichten', b6_1), ('Soorten spierweefsel', b6_2), ('Samentrekken en ontspannen', b6_3)], b6_oef, b6_sam, (TOOL + '#e4', 'Oefen verder in de tool'))
print('bio ok')
