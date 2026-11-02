import json, math
ns = {}
src = open('/home/claude/cursus/bouw.py', encoding='utf-8').read()
exec(src.split('STAP = ')[0], ns)
ns['FOOTER'] = 'Cursus biologie — gemaakt voor klasgebruik, bij de tools op Oefentools wetenschappen.'
denk, oef, blok, tool, kader, figuur, bouw = (ns[k] for k in ['denk', 'oef', 'blok', 'tool', 'kader', 'figuur', 'bouw'])
lees = lambda f: open('/home/claude/cursus/' + f, encoding='utf-8').read()
TOOL = 'biologie-prikkels.html'
FONT = 'font-family="Inter,sans-serif"'

# ---------------------------------------------------------------
# figuren met namen (theorie) of nummers (oefening)
# ---------------------------------------------------------------
def aanwijs(inner, w, h, punten, modus='naam', ml=200, mr=200, fs=20, gap=34, breedte=640, top=0, bot=0):
    """punten: lijst (naam, x, y, kant). modus 'naam' toont namen, 'nr' toont nummers + invullijnen."""
    P = []
    for i, (naam, x, y, kant) in enumerate(punten):
        P.append(dict(i=i, naam=naam, x=x, y=y, kant=kant, yy=y))
    for k in 'lr':
        L = sorted([p for p in P if p['kant'] == k], key=lambda p: p['yy'])
        for _ in range(80):
            for j in range(1, len(L)):
                d = L[j]['yy'] - L[j-1]['yy']
                if d < gap:
                    m = (gap - d) / 2; L[j]['yy'] += m; L[j-1]['yy'] -= m
            for p in L: p['yy'] = max(18 - top, min(h + bot - 10, p['yy']))
    s = f'<svg viewBox="{-ml} {-top} {w+ml+mr} {h+top+bot}" width="{breedte}" xmlns="http://www.w3.org/2000/svg" {FONT}>{inner}'
    for p in P:
        l = p['kant'] == 'l'
        ex = -8 if l else w + 8
        kx = min(p['x'] - 20, ex + 40) if l else max(p['x'] + 20, ex - 40)
        s += f'<path d="M{p["x"]},{p["y"]} L{kx},{p["yy"]} L{ex},{p["yy"]}" fill="none" stroke="#1D2A36" stroke-width="1.8"/>'
        s += f'<circle cx="{p["x"]}" cy="{p["y"]}" r="5" fill="#1D2A36"/>'
        tx = ex - 6 if l else ex + 6
        anc = 'end' if l else 'start'
        if modus == 'naam':
            s += f'<text x="{tx}" y="{p["yy"]+6}" text-anchor="{anc}" font-size="{fs}" font-weight="700" fill="#1D2A36" stroke="#fff" stroke-width="5" paint-order="stroke">{p["naam"]}</text>'
        else:
            cx = tx - 14 if l else tx + 14
            s += f'<circle cx="{cx}" cy="{p["yy"]}" r="15" fill="#fff" stroke="#1D2A36" stroke-width="2"/><text x="{cx}" y="{p["yy"]+6}" text-anchor="middle" font-size="17" font-weight="700" fill="#1D2A36">{p["i"]+1}</text>'
    return s + '</svg>'

def invullijst(punten):
    return '<ol class="invul">' + ''.join('<li>……………………………………………</li>' for _ in punten) + '</ol>'

# --- plant
geo = json.load(open('/home/claude/cursus/plantgeo.json'))
plant_in = lees('plant.svgi')
b0 = geo['bladen'][0]
P_PLANT = [('bloem', 320, 74, 'r'), ('blad', b0['tip'][0]-40, b0['tip'][1]+4, 'r'), ('stengel', geo['stam'][2][0], geo['stam'][2][1]+20, 'l'), ('wortel', 320, 520, 'l')]

# --- blad (afbeelding)
blad_in = '<image href="img/bio-blad.webp" x="0" y="0" width="900" height="897"/>'
P_BLAD = [('dekweefsel', 70, 240, 'l'), ('vulweefsel', 150, 380, 'l'), ('sluitcellen', 280, 762, 'l'), ('huidmondje', 323, 782, 'r'), ('vacuole', 470, 500, 'r')]

# --- stengel
st = json.load(open('/home/claude/bio/stengel.json'))['bundels']
def bun(i, s_, t_):
    bx, by, a = st[i]; a = math.radians(a)
    return (bx + math.cos(a)*s_ - math.sin(a)*t_, by + math.sin(a)*s_ + math.cos(a)*t_)
pol = lambda r, d: (400 + r*math.cos(math.radians(d)), 400 + r*math.sin(math.radians(d)))
stengel_in = '<image href="img/bio-stengel.svg" x="0" y="0" width="800" height="800"/>'
P_STENGEL = [('dekweefsel', *pol(352, -62), 'r'), ('cortex', *pol(318, 40), 'r'), ('vaatbundel', *bun(7, 2, -41), 'r'),
             ('zeefvaten', *bun(0, 22, 8), 'r'), ('deelweefsel', *bun(1, -0.5, 10), 'r'), ('houtvaten', *bun(7, -34, 0), 'r'),
             ('vulweefsel', 400, 400, 'l')]

# --- wortel
wortel_in = '<g transform="translate(-60,-60) scale(1.15)"><image href="img/bio-wortel.svg" x="0" y="0" width="800" height="800"/></g>'
W = lambda x, y: (-60 + 1.15*x, -60 + 1.15*y)
P_WORTEL = [('wortelhaartjes', *W(700, 262), 'r'), ('dekweefsel', *W(636, 455), 'r'), ('cortex', *W(540, 560), 'r'),
            ('houtvaten', *W(430, 430), 'l'), ('zeefvaten', *W(448, 400), 'r'), ('vaatbundel', *W(400, 318), 'l')]

def fig_plant(m): return aanwijs(plant_in, 640, 640, P_PLANT, m, 150, 170, 22, 40, 520)
def fig_blad(m): return aanwijs(blad_in, 900, 897, P_BLAD, m, 330, 280, 26, 48, 600)
def fig_stengel(m): return aanwijs(stengel_in, 800, 800, P_STENGEL, m, 260, 300, 26, 46, 600)
def fig_wortel(m): return aanwijs(wortel_in, 800, 800, P_WORTEL, m, 230, 280, 26, 46, 600)

# --- huidmondje open en dicht naast elkaar
def stoma_klein(inner, titel):
    inner = inner.replace('>epidermiscellen<', '>cellen van het dekweefsel<')
    return f'<g>{inner}<text x="410" y="548" text-anchor="middle" font-size="34" font-weight="700" fill="#1D2A36">{titel}</text></g>'
fig_stoma = (f'<svg viewBox="0 0 1680 570" width="640" xmlns="http://www.w3.org/2000/svg" {FONT}><style>text{{font-size:30px;font-weight:700}}</style>'
             + stoma_klein(lees('stoma_open.svgi'), 'open: veel turgor')
             + '<g transform="translate(860,0)">' + stoma_klein(lees('stoma_dicht.svgi'), 'gesloten: weinig turgor') + '</g></svg>')

fig_vaten = f'<svg viewBox="0 0 900 330" width="640" xmlns="http://www.w3.org/2000/svg" {FONT}>{lees("vaten.svgi")}</svg>'

# --- transportschema op de plant
def pijl(x1, y1, x2, y2, k):
    a = math.atan2(y2-y1, x2-x1)
    return (f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{k}" stroke-width="7" stroke-linecap="round"/>'
            f'<path d="M{x2+math.cos(a)*6},{y2+math.sin(a)*6} L{x2-16*math.cos(a-0.5)},{y2-16*math.sin(a-0.5)} L{x2-16*math.cos(a+0.5)},{y2-16*math.sin(a+0.5)}Z" fill="{k}"/>')
tr = plant_in
sx = 320
tr += pijl(sx-14, 560, sx-14, 420, '#2563eb') + pijl(sx-14, 330, sx-14, 150, '#2563eb')
tr += pijl(sx+16, 150, sx+16, 330, '#d97706') + pijl(sx+16, 420, sx+16, 560, '#d97706')
tr += pijl(b0['st'][0]+20, b0['st'][1]+10, b0['st'][0]+90, b0['st'][1]-10, '#2563eb')
tr += f'<g font-size="20" font-weight="700" stroke="#fff" stroke-width="5" paint-order="stroke"><text x="440" y="40" fill="#2563eb">waterdamp</text><text x="440" y="64" fill="#2563eb">(huidmondjes)</text></g>'
fig_transport = f'<svg viewBox="0 0 640 640" width="420" xmlns="http://www.w3.org/2000/svg" {FONT}>{tr}</svg><div style="font-size:14px;margin-top:6px"><span style="color:#2563eb;font-weight:700">▲ blauw</span>: water en mineralen via de houtvaten, opwaarts &nbsp; <span style="color:#b45309;font-weight:700">▼ oranje</span>: assimilaten via de zeefvaten, vooral neerwaarts</div>'

# --- negatieve feedback: grafiek
def fig_feedback():
    X0, Y0, GW, GH = 70, 30, 520, 200
    pts = ' L'.join(f'{X0+t:.1f},{Y0+GH/2-60*math.sin(t/GW*4*math.pi):.1f}' for t in range(0, GW+1, 4))
    s = f'<svg viewBox="0 0 720 290" width="600" xmlns="http://www.w3.org/2000/svg" {FONT}>'
    s += f'<rect x="{X0}" y="{Y0+GH/2-80}" width="{GW}" height="160" fill="#dcfce7"/>'
    s += f'<line x1="{X0}" x2="{X0+GW}" y1="{Y0+GH/2}" y2="{Y0+GH/2}" stroke="#059669" stroke-width="2" stroke-dasharray="9 6"/>'
    for y, t in [(Y0+GH/2-80, 'bovengrens'), (Y0+GH/2, 'normwaarde'), (Y0+GH/2+80, 'ondergrens')]:
        s += f'<line x1="{X0}" x2="{X0+GW}" y1="{y}" y2="{y}" stroke="#16a34a" stroke-width="1.3" stroke-dasharray="4 4"/><text x="{X0+GW+6}" y="{y+5}" font-size="14" font-weight="700" fill="#15803d">{t}</text>'
    s += f'<path d="M{pts}" fill="none" stroke="#1D2A36" stroke-width="3"/>'
    s += f'<path d="M{X0},{Y0} V{Y0+GH} H{X0+GW}" fill="none" stroke="#1D2A36" stroke-width="2"/>'
    s += f'<text x="{X0}" y="{Y0-10}" font-size="15" font-weight="700">waarde (bv. water in de plant)</text><text x="{X0+GW}" y="{Y0+GH+22}" text-anchor="end" font-size="14">tijd →</text>'
    s += f'<text x="{X0+GW*0.375}" y="{Y0+GH/2+108}" text-anchor="middle" font-size="14" font-weight="700" fill="#2563eb">te weinig → reactie verhoogt</text>'
    s += f'<text x="{X0+GW*0.125}" y="{Y0+GH/2-92}" text-anchor="middle" font-size="14" font-weight="700" fill="#b91c1c">te veel → reactie verlaagt</text>'
    return s + '</svg>'

def lijnen(n): return '<div class="schrijflijnen">' + '<div></div>'*n + '</div>'


# ---------------------------------------------------------------
# voorkennis
# ---------------------------------------------------------------
def vk(items):
    return '<div class="voorkennis"><div class="kop">📐 Voorkennis</div><ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul></div>'

def fig_cel():
    s = f'<svg viewBox="-70 0 710 330" width="580" xmlns="http://www.w3.org/2000/svg" {FONT}>'
    s += '<rect x="170" y="30" width="300" height="270" rx="26" fill="#cfe8a8" stroke="#4d7a2a" stroke-width="10"/>'
    s += '<rect x="181" y="41" width="278" height="248" rx="18" fill="#eef7e2" stroke="#7aa35a" stroke-width="2.5"/>'
    s += '<path d="M215,70 Q320,48 425,72 Q445,170 420,262 Q320,282 220,262 Q198,170 215,70Z" fill="#cfeaf6" stroke="#5aa0c0" stroke-width="2"/>'
    for x, y, a in [(196, 90, 70), (196, 160, 95), (196, 230, 80), (444, 110, 100), (444, 200, 80), (300, 274, 0), (370, 274, 10), (260, 56, 5), (380, 56, -5)]:
        s += f'<ellipse cx="{x}" cy="{y}" rx="14" ry="7" transform="rotate({a} {x} {y})" fill="#3f8f34" stroke="#255c1d"/>'
    s += '<ellipse cx="236" cy="200" rx="22" ry="17" fill="#c9a36b" stroke="#7a5a2c" stroke-width="2"/><circle cx="240" cy="198" r="6" fill="#7a5a2c"/>'
    lab = lambda x1, y1, x2, y2, t, anc: f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#1D2A36" stroke-width="1.6"/><circle cx="{x1}" cy="{y1}" r="4" fill="#1D2A36"/><text x="{x2+(6 if anc=="start" else -6)}" y="{y2+5}" text-anchor="{anc}" font-size="17" font-weight="700" fill="#1D2A36">{t}</text>'
    s += lab(172, 60, 120, 40, 'celwand', 'end') + lab(183, 130, 120, 120, 'celmembraan', 'end') + lab(196, 230, 120, 250, 'bladgroenkorrel', 'end')
    s += lab(236, 200, 120, 190, 'celkern', 'end') + lab(330, 160, 520, 140, 'vacuole', 'start') + lab(452, 270, 520, 270, 'cytoplasma', 'start')
    return s + '</svg>'

def fig_osmose():
    s = f'<svg viewBox="0 0 640 210" width="560" xmlns="http://www.w3.org/2000/svg" {FONT}>'
    for cx, vr, t1, t2 in [(160, 0.55, 'weinig water in de cel', 'vacuole klein, slap'), (480, 0.92, 'veel water opgenomen', 'vacuole groot, stevig')]:
        s += f'<rect x="{cx-90}" y="20" width="180" height="140" rx="18" fill="#cfe8a8" stroke="#4d7a2a" stroke-width="7"/>'
        s += f'<ellipse cx="{cx}" cy="90" rx="{80*vr}" ry="{60*vr}" fill="#cfeaf6" stroke="#5aa0c0" stroke-width="2"/>'
        s += f'<text x="{cx}" y="182" text-anchor="middle" font-size="15" font-weight="700" fill="#1D2A36">{t1}</text><text x="{cx}" y="202" text-anchor="middle" font-size="14" fill="#51606E">{t2}</text>'
    s += '<path d="M265,90 L370,90" stroke="#2563eb" stroke-width="6"/><path d="M382,90 l-16,-10 v20z" fill="#2563eb"/><text x="318" y="78" text-anchor="middle" font-size="15" font-weight="700" fill="#2563eb">water erin</text>'
    return s + '</svg>'

voorkennis = f"""<p>Voor dit hoofdstuk heb je leerstof uit de vorige jaren nodig. Kijk na of je die nog kent. Twijfel je? Lees dan de korte herhaling en maak de controlevragen.</p>
{vk(['Ik ken de delen van een <b>plantencel</b>: celwand, celmembraan, cytoplasma, celkern, vacuole en bladgroenkorrels.',
     'Ik weet dat <b>cellen</b> samen <b>weefsels</b> vormen, en weefsels samen <b>organen</b>.',
     'Ik weet wat <b>fotosynthese</b> is: met licht maakt de plant glucose en zuurstof uit koolstofdioxide en water.',
     'Ik weet wat <b>osmose</b> is: water gaat door een membraan naar de kant met de meeste opgeloste stoffen.',
     'Ik kan een correcte <b>biologische tekening</b> maken.'])}
<h3>Herhaling: de plantencel</h3>
{figuur(fig_cel(), 'Een plantencel.')}
<table class="vb"><tr><td>celwand</td><td>stevige buitenwand: geeft de cel haar vorm</td></tr>
<tr><td>celmembraan</td><td>vlies binnen de celwand: bepaalt wat de cel in- en uitgaat</td></tr>
<tr><td>vacuole</td><td>grote blaas met celvocht, vooral water</td></tr>
<tr><td>bladgroenkorrels</td><td>hier gebeurt de fotosynthese</td></tr>
<tr><td>celkern</td><td>stuurt de werking van de cel</td></tr></table>
<h3>Herhaling: van cel tot organisme</h3>
<div class="formule" style="font-size:16px">cel → weefsel → orgaan → organisme</div>
<p>Een <b>weefsel</b> is een groep gelijke cellen met dezelfde functie. Een <b>orgaan</b> is opgebouwd uit verschillende weefsels die samenwerken.</p>
<h3>Herhaling: fotosynthese</h3>
<div class="formule" style="font-size:16px">koolstofdioxide + water → (licht, bladgroen) → glucose + zuurstof</div>
<h3>Herhaling: osmose</h3>
{figuur(fig_osmose(), 'Neemt een plantencel water op, dan zwelt de vacuole en drukt ze tegen de celwand.')}
<p>Water verplaatst zich door het celmembraan naar de kant met de <b>meeste opgeloste stoffen</b>. Zo kan een plantencel water opnemen of verliezen. Dat heb je nodig om de huidmondjes te begrijpen.</p>
<h3>Herhaling: een biologische tekening</h3>
<p>Teken met <b>potlood</b>, met <b>dunne, ononderbroken lijnen</b>, zonder arcering of kleur. Schrijf er een <b>titel</b> boven. Zet de namen <b>rechts</b> van de tekening, met <b>horizontale</b> verwijslijnen die elkaar niet kruisen.</p>
{oef('vk_opl', '✓', 'Controlevragen voorkennis', '<ol class="deelvragen" type="a"><li>Welke twee delen heeft een plantencel wel en een dierlijke cel niet? (Er zijn er drie; noem er twee.)</li><li>Zet in de juiste volgorde: orgaan, cel, organisme, weefsel.</li><li>Welke stoffen heeft een plant nodig voor fotosynthese? Wat maakt ze?</li><li>Een plantencel komt in zuiver water. Neemt ze water op of verliest ze water? Wat gebeurt er met de vacuole?</li></ol>' + lijnen(5),
  [('a', 'celwand, vacuole (groot), bladgroenkorrels'), ('b', 'cel → weefsel → orgaan → organisme'), ('c', 'nodig: koolstofdioxide, water en licht; ze maakt glucose en zuurstof'), ('d', 'Ze neemt water op, want in de cel zijn meer opgeloste stoffen. De vacuole zwelt.')], 'Kon je alles? Dan ben je klaar om te starten.')}"""

# ---------------------------------------------------------------
# inhoud
# ---------------------------------------------------------------
lesdoelen = '''<p>Na dit hoofdstuk kan je:</p><ul class="doelen">
<li>uitleggen wat <b>waterhuishouding</b> bij planten inhoudt;</li>
<li><b>wortel, stengel, blad en bloem</b> benoemen als plantenorganen;</li>
<li>de plantenweefsels <b>deelweefsel, vaatbundels, dekweefsel, huidmondjes, houtvaten, zeefvaten, sluitcellen, cellen van het vulweefsel en cortex</b> benoemen, herkennen en hun functie geven;</li>
<li>uitleggen hoe de <b>gasuitwisseling via de huidmondjes</b> gebeurt, met de woorden <b>vacuole, turgor</b> en <b>openen of sluiten</b>;</li>
<li>verwoorden dat <b>assimilaten</b> (eindproducten van de fotosynthese) bestaan uit glucose, zetmeel, eiwitten en vetten;</li>
<li>uitleggen hoe het <b>water- en assimilatentransport</b> verloopt, met de woorden wortelhaartjes, houtvaten, zeefvaten, huidmondjes en opwaarts en neerwaarts transport;</li>
<li>tekeningen maken van <b>houtvaten, zeefvaten en deelweefsel</b> in stengel en wortel;</li>
<li>uitleggen hoe de plant haar waterhuishouding in evenwicht houdt met een <b>negatief feedbacksysteem</b>.</li></ul>'''

d1 = f'''<p>Een plant neemt voortdurend water op en verliest ook voortdurend water. De <b>waterhuishouding</b> is het geheel van <b>opname, transport en afgifte van water</b> in de plant. Een plant moet die in evenwicht houden: te weinig water en ze verwelkt, maar ze kan ook niet onbeperkt water opnemen.</p>
{kader('Definitie', '<p><b>Waterhuishouding</b> bij planten: de manier waarop een plant water opneemt, vervoert en afgeeft, zodat er altijd genoeg water in de plant is.</p>')}
<p>Een plant bestaat uit vier <b>organen</b>. Elk orgaan speelt een rol in de waterhuishouding.</p>
{figuur(fig_plant('naam'), 'De vier plantenorganen.')}
<table class="vb"><tr><td>wortel</td><td>verankert de plant en neemt <b>water en mineralen</b> op</td></tr>
<tr><td>stengel</td><td>draagt bladeren en bloemen en <b>vervoert</b> water en assimilaten</td></tr>
<tr><td>blad</td><td>maakt suikers door <b>fotosynthese</b> en geeft <b>waterdamp</b> af</td></tr>
<tr><td>bloem</td><td>zorgt voor de <b>voortplanting</b></td></tr></table>
<p>Een orgaan is opgebouwd uit <b>weefsels</b>: groepen gelijke cellen met dezelfde functie. In de volgende delen bekijk je de weefsels van blad, stengel en wortel. Je ziet telkens hoe ze aangepast zijn aan de waterhuishouding.</p>
{tool(TOOL+'#p1', 'Bekijk het in de tool: de plant en haar organen')}'''

d2 = f'''{vk(['Ik ken de delen van een plantencel.', 'Ik weet wat fotosynthese is.'])}
<p>Het blad is het orgaan waar de plant het meeste water verliest. Toch moet het blad openstaan voor gassen: het heeft <b>CO₂</b> nodig voor de fotosynthese.</p>
{figuur(fig_blad('naam'), 'Een stukje blad, sterk vergroot en opengesneden. Tekening: Zephyris, Wikimedia Commons, CC BY-SA 3.0.')}
<table class="vb"><tr><td>dekweefsel</td><td>één laag doorzichtige cellen aan de boven- en onderkant. <b>Beschermt</b> het blad. Een waslaagje erop beperkt de verdamping.</td></tr>
<tr><td>cellen van het vulweefsel</td><td>cellen vol <b>bladgroenkorrels</b>: hier gebeurt de fotosynthese. Onderaan liggen ze losser. De ruimte tussen de cellen heet de <b>intercellulaire ruimte</b>: daarin verspreiden de gassen zich.</td></tr>
<tr><td>huidmondje</td><td>opening in het onderste dekweefsel: hier gaan <b>CO₂</b> naar binnen en <b>O₂ en waterdamp</b> naar buiten.</td></tr>
<tr><td>sluitcellen</td><td>twee boonvormige cellen rond een huidmondje. Ze kunnen het huidmondje <b>openen en sluiten</b>.</td></tr>
<tr><td>vaatbundels</td><td>de <b>nerven</b> van het blad: ze brengen water aan en voeren assimilaten af.</td></tr></table>
{kader('Aangepast aan de waterhuishouding', '<p>Het waslaagje op het dekweefsel beperkt de verdamping. De meeste huidmondjes liggen aan de <b>onderkant</b> van het blad, in de schaduw: daar verdampt minder water.</p>')}
{tool(TOOL+'#p2', 'Oefen in de tool: zelf de delen van het blad aanduiden')}
{denk('denk_1', 'Waarom liggen de meeste huidmondjes aan de onderkant van het blad en niet aan de bovenkant?', [
  ('Wat gebeurt er bij een huidmondje?', 'Langs het huidmondje verdampt water.'),
  ('Waar is het warmst?', 'De bovenkant van het blad ligt in de zon en wordt warmer. Daar zou meer water verdampen.'),
  ('Besluit', 'Aan de koelere onderkant gaat er minder water verloren, terwijl de gaswisseling toch kan gebeuren.')],
  'Huidmondjes aan de onderkant beperken het waterverlies.')}{lijnen(3)}'''

d3 = f'''{vk(['Ik ken de weefsels van het blad (deel 2): dekweefsel, huidmondjes, sluitcellen.', 'Ik weet wat osmose is en hoe een cel water opneemt of afgeeft.'])}
<p>Een huidmondje is geen gat dat altijd openstaat. De twee <b>sluitcellen</b> bepalen of het open of dicht is. Dat hangt af van de hoeveelheid water in hun <b>vacuole</b>.</p>
{figuur(fig_stoma, 'Een huidmondje van onderaf gezien, door een microscoop.')}
{kader('Openen en sluiten', '''<p><b>Openen</b>: de sluitcellen nemen water op. Hun <b>vacuole</b> zwelt, de <b>turgor</b> (de druk van de vacuole tegen de celwand) stijgt. Omdat hun wand aan de kant van de opening dikker is, buigen de sluitcellen uit elkaar: het huidmondje <b>gaat open</b>.</p>
<p><b>Sluiten</b>: de sluitcellen verliezen water. De vacuole krimpt, de turgor daalt en de sluitcellen sluiten de opening: het huidmondje <b>gaat dicht</b>.</p>''')}
<p>Is het huidmondje open, dan vindt er <b>gasuitwisseling</b> plaats: <b>CO₂</b> komt binnen voor de fotosynthese, <b>O₂</b> en <b>waterdamp</b> gaan naar buiten.</p>
<table class="vb"><tr><td>licht en genoeg water</td><td>huidmondjes <b>open</b>: fotosynthese kan</td></tr>
<tr><td>donker</td><td>huidmondjes <b>dicht</b>: geen fotosynthese, dus geen CO₂ nodig</td></tr>
<tr><td>watertekort</td><td>huidmondjes <b>dicht</b>: de plant verliest minder water</td></tr></table>
{tool(TOOL+'#p3', 'Probeer het in de tool: licht, donker en watertekort')}
{kader('Brussel · de Koninklijke Serres van Laken', '<p>De Koninklijke Serres van Laken zijn glazen serres met een metalen skelet, gebouwd tussen 1874 en 1905. Er staan veel tropische planten, zoals palmen. Binnen is de lucht <b>warm en vochtig</b>, zoals in het regenwoud.</p>')}
{denk('denk_serre', 'Verliest een palm in de vochtige lucht van de serre meer of minder water via zijn huidmondjes dan dezelfde palm buiten, op een droge en winderige dag?', [
  ('Wat gebeurt er bij een huidmondje?', 'Waterdamp gaat van de vochtige intercellulaire ruimten in het blad naar de lucht buiten.'),
  ('Vochtige lucht', 'In de serre zit al veel waterdamp in de lucht. Er kan maar weinig extra waterdamp bij.'),
  ('Droge, winderige lucht', 'Droge lucht neemt veel waterdamp op, en de wind voert de vochtige lucht rond het blad weg.')],
  'In de vochtige serre verliest de palm minder water. Daarom kunnen tropische planten er hun huidmondjes openhouden zonder uit te drogen.')}
{denk('denk_2', 'Op een hete zomerdag zijn de huidmondjes van een plant ’s middags gesloten, ook al schijnt de zon. Hoe kan dat?', [
  ('Wat gebeurt er bij hitte?', 'Er verdampt veel water. De plant krijgt een watertekort.'),
  ('Wat doen de sluitcellen?', 'Ze verliezen water: de vacuole krimpt en de turgor daalt.'),
  ('Gevolg', 'De huidmondjes sluiten. Zo verdampt er minder water, maar er komt ook minder CO₂ binnen.')],
  'Bij een watertekort is water sparen belangrijker dan fotosynthese: de huidmondjes sluiten.')}{lijnen(3)}'''

d4 = f'''{vk(['Ik weet dat cellen samen weefsels vormen.', 'Ik kan een correcte biologische tekening maken.'])}
<p>De stengel verbindt de wortel met de bladeren. Het transport gebeurt in de <b>vaatbundels</b>. In de stengel liggen ze in een <b>kring</b>.</p>
{figuur(fig_stengel('naam'), 'Dwarsdoorsnede van een stengel.')}
<table class="vb"><tr><td>dekweefsel</td><td>buitenste cellaag: <b>beschermt</b> de stengel</td></tr>
<tr><td>cortex</td><td>laag <b>vulweefsel</b> onder het dekweefsel: steun en opslag</td></tr>
<tr><td>vaatbundel</td><td>bevat houtvaten, deelweefsel en zeefvaten</td></tr>
<tr><td>houtvaten</td><td>aan de <b>binnenkant</b> van de vaatbundel: vervoeren <b>water en mineralen</b> omhoog</td></tr>
<tr><td>zeefvaten</td><td>aan de <b>buitenkant</b> van de vaatbundel: vervoeren <b>assimilaten</b></td></tr>
<tr><td>deelweefsel</td><td>tussen houtvaten en zeefvaten: cellen die blijven <b>delen</b>, zodat de stengel dikker wordt</td></tr>
<tr><td>cellen van het vulweefsel</td><td>in het midden (merg) en in de cortex: opslag</td></tr></table>
{figuur(fig_vaten, 'Houtvat en zeefvat in lengtedoorsnede.')}
{kader('Houtvat of zeefvat?', '<p><b>Houtvat</b>: dode, holle cellen zonder tussenwanden. De wand is verstevigd met houtstof (ringen, spiralen). <b>Water en mineralen</b> gaan omhoog.</p><p><b>Zeefvat</b>: levende cellen. Tussen de cellen zitten <b>zeefplaten</b> met gaatjes. <b>Assimilaten</b> gaan op en neer.</p>')}
{tool(TOOL+'#p4', 'Oefen in de tool: de stengel')}'''

d5 = f'''<p>De wortel neemt water en mineralen op uit de bodem. Ze is daaraan aangepast met <b>wortelhaartjes</b>.</p>
{figuur(fig_wortel('naam'), 'Dwarsdoorsnede van een wortel.')}
<table class="vb"><tr><td>wortelhaartjes</td><td>uitstulpingen van cellen van het dekweefsel: ze maken de oppervlakte voor de wateropname heel <b>groot</b></td></tr>
<tr><td>dekweefsel</td><td>buitenste cellaag van de wortel</td></tr>
<tr><td>cortex</td><td>cellen van het vulweefsel: het water gaat erdoor naar het midden</td></tr>
<tr><td>vaatbundel</td><td>één vaatbundel in het <b>midden</b> van de wortel</td></tr>
<tr><td>houtvaten</td><td>liggen in een <b>ster</b> in het midden: water omhoog</td></tr>
<tr><td>zeefvaten</td><td>liggen <b>tussen</b> de armen van de ster: assimilaten naar de wortel</td></tr></table>
{kader('Stengel en wortel vergeleken', '<p>In de <b>stengel</b> liggen veel vaatbundels in een kring, met de houtvaten binnen en de zeefvaten buiten.<br>In de <b>wortel</b> ligt één vaatbundel in het midden, met houtvaten en zeefvaten <b>naast elkaar</b>.</p>')}
{tool(TOOL+'#p5', 'Oefen in de tool: de wortel')}'''

d6 = f'''{vk(['Ik ken de houtvaten en zeefvaten uit deel 4 en 5.', 'Ik weet wat fotosynthese is en welke stoffen de plant daarbij maakt.'])}
<p>In een plant zijn er twee transportstromen.</p>
{figuur(fig_transport, 'Water gaat omhoog, assimilaten gaan vooral naar beneden.')}
<h3>Watertransport: opwaarts</h3>
<ol class="doelen"><li>De <b>wortelhaartjes</b> nemen water en mineralen op uit de bodem.</li>
<li>Het water gaat door de cortex naar de <b>houtvaten</b> in het midden van de wortel.</li>
<li>Via de houtvaten stijgt het water door wortel en stengel naar het blad: <b>opwaarts transport</b>.</li>
<li>In het blad verdampt een deel van het water via de <b>huidmondjes</b>. Die verdamping trekt nieuw water omhoog.</li></ol>
<h3>Assimilatentransport: vooral neerwaarts</h3>
<p>In het blad maakt de plant <b>glucose</b> door fotosynthese. Daarmee maakt ze ook <b>zetmeel, eiwitten en vetten</b>. Al deze eindproducten van de fotosynthese heten <b>assimilaten</b>.</p>
{kader('Definitie', '<p><b>Assimilaten</b> zijn de eindproducten van de fotosynthese: <b>glucose, zetmeel, eiwitten en vetten</b>.</p>')}
<p>De assimilaten gaan via de <b>zeefvaten</b> van het blad naar alle delen van de plant. Een groot deel gaat naar de wortel en wordt daar opgeslagen, bv. als zetmeel: <b>neerwaarts transport</b>. Een deel gaat naar de bloem en later naar zaden en vruchten.</p>
{tool(TOOL+'#p6', 'Bekijk het transport in de tool')}
{denk('denk_3', 'Een boom wordt rondom geringd: er wordt een ring schors weggesneden, net boven de grond. De zeefvaten zitten in de schors, de houtvaten niet. Na een tijd sterft de boom. Waarom?', [
  ('Wat wordt onderbroken?', 'De zeefvaten: de assimilaten kunnen niet meer naar de wortel.'),
  ('Wat blijft werken?', 'De houtvaten: de bladeren krijgen nog water.'),
  ('Gevolg', 'De wortel krijgt geen voedsel meer en sterft af. Dan kan ze geen water meer opnemen, en sterft de hele boom.')],
  'Zonder assimilatentransport naar de wortel sterft de wortel, en daarna de boom.')}{lijnen(3)}'''

d7 = f'''{vk(['Ik weet hoe huidmondjes openen en sluiten (deel 3).'])}
<p>Een plant kan haar waterhuishouding in evenwicht houden. Het constant houden van het intern milieu heet <b>homeostase</b>. Dat gebeurt met een <b>feedbacksysteem</b>: het effect van een reactie stuurt de reactie zelf bij.</p>
{kader('Negatief feedbacksysteem bij de huidmondjes', '<p><b>Prikkel</b>: de plant verliest veel water (watertekort).<br><b>Reactie</b>: de sluitcellen verliezen water, de turgor daalt en de huidmondjes <b>sluiten</b>.<br><b>Effect</b>: de plant verliest minder water, het watergehalte stijgt weer.<br>Is er weer genoeg water, dan gaan de huidmondjes opnieuw <b>open</b>.</p>')}
<p>Een <b>negatief</b> feedbacksysteem werkt de verandering <b>tegen</b>. Het watergehalte blijft niet precies gelijk: het schommelt rond een normwaarde, maar blijft binnen vaste grenzen. Het evenwicht is <b>dynamisch</b>.</p>
{figuur(fig_feedback(), 'Bij negatieve feedback schommelt de waarde rond de normwaarde, binnen vaste grenzen.')}
{tool(TOOL+'#f2', 'Bekijk negatieve feedback in de tool')}'''

# ---------------------------------------------------------------
# oefeningen
# ---------------------------------------------------------------
oefs = f'''<p>Maak deze oefeningen <b>op papier</b>. Druk ze af of maak ze in je schrift. De oplossingen verschijnen hier nadat we de oefeningen in de les besproken hebben.</p>
<p><button class="knop licht" data-print="oef">🖨 Druk de oefeningen af</button></p>
{oef('opl_1', 1, 'Plantenorganen', 'Schrijf bij elk nummer de naam van het orgaan en geef de functie in één zin.' + figuur(fig_plant('nr')) + invullijst(P_PLANT),
  [(str(i+1), f'{n}') for i, n in enumerate(['bloem: voortplanting', 'blad: fotosynthese en gasuitwisseling', 'stengel: draagt de plant en vervoert water en assimilaten', 'wortel: verankert de plant en neemt water en mineralen op'])], 'Wortel, stengel, blad en bloem zijn de vier plantenorganen.')}
{oef('opl_2', 2, 'Het blad', 'Benoem de delen van het blad.' + figuur(fig_blad('nr')) + invullijst(P_BLAD),
  [(str(i+1), n) for i, (n, *_) in enumerate(P_BLAD)], 'Let op: het huidmondje is de opening, de sluitcellen liggen errond.')}
{oef('opl_3', 3, 'De stengel', 'Benoem de delen van de stengel.' + figuur(fig_stengel('nr')) + invullijst(P_STENGEL),
  [(str(i+1), n) for i, (n, *_) in enumerate(P_STENGEL)], 'Houtvaten liggen aan de binnenkant van de vaatbundel, zeefvaten aan de buitenkant.')}
{oef('opl_4', 4, 'De wortel', 'Benoem de delen van de wortel.' + figuur(fig_wortel('nr')) + invullijst(P_WORTEL),
  [(str(i+1), n) for i, (n, *_) in enumerate(P_WORTEL)], 'In de wortel ligt één vaatbundel in het midden.')}
{oef('opl_5', 5, 'Welk weefsel?', 'Schrijf de naam van het weefsel dat deze functie heeft.<ol class="deelvragen" type="a"><li>vervoert water en mineralen omhoog</li><li>vervoert assimilaten</li><li>cellen die blijven delen, zodat de stengel dikker wordt</li><li>vergroot de oppervlakte voor de opname van water</li><li>opent en sluit het huidmondje</li><li>beschermt het blad en beperkt de verdamping</li><li>cellen vol bladgroenkorrels, waar de fotosynthese gebeurt</li></ol>' + lijnen(7),
  [('a', 'houtvaten'), ('b', 'zeefvaten'), ('c', 'deelweefsel'), ('d', 'wortelhaartjes'), ('e', 'sluitcellen'), ('f', 'dekweefsel'), ('g', 'vulweefsel')], '')}
{oef('opl_6', 6, 'Tekenen: houtvaten en zeefvaten', 'Maak twee tekeningen in je schrift, met potlood.<ol class="deelvragen" type="a"><li>Teken een stukje <b>houtvat</b> en een stukje <b>zeefvat</b> in lengtedoorsnede. Duid aan: houtstof (ringen), zeefplaat, begeleidende cel.</li><li>Teken één <b>vaatbundel</b> van een stengel in dwarsdoorsnede. Duid aan: houtvaten, deelweefsel, zeefvaten. Teken een pijl naar het midden van de stengel.</li><li>Teken het <b>midden van een wortel</b> in dwarsdoorsnede. Duid aan: houtvaten (ster) en zeefvaten.</li></ol>',
  [('a', 'Houtvat: lange holle buis zonder tussenwanden, met ringen of spiralen. Zeefvat: rij cellen met zeefplaten ertussen en een begeleidende cel ernaast.'), ('b', 'Houtvaten aan de kant van het midden, dan het deelweefsel als smalle band, dan de zeefvaten aan de buitenkant.'), ('c', 'Houtvaten in een ster in het midden, zeefvaten tussen de armen van de ster.')], 'Vergelijk je tekening met de figuren in deel 4 en 5.')}
{oef('opl_7', 7, 'Huidmondjes: juist of fout?', 'Zet een kruisje bij <b>juist</b> of <b>fout</b>. Verbeter wat fout is.<table class="jf"><tr><th></th><th>juist</th><th>fout</th></tr>'
  + ''.join(f'<tr><td>{z}</td><td>☐</td><td>☐</td></tr>' for z in [
    'a. Als de sluitcellen water opnemen, gaat het huidmondje dicht.',
    'b. Turgor is de druk van de vacuole tegen de celwand.',
    'c. Bij watertekort sluiten de huidmondjes.',
    'd. Door een open huidmondje komt O₂ binnen voor de fotosynthese.',
    'e. In het donker zijn de huidmondjes meestal gesloten.',
    'f. De meeste huidmondjes liggen aan de bovenkant van het blad.']) + '</table>' + lijnen(3),
  [('a', 'fout: dan gaat het huidmondje <b>open</b> (de turgor stijgt).'), ('b', 'juist'), ('c', 'juist'), ('d', 'fout: <b>CO₂</b> komt binnen, O₂ gaat naar buiten.'), ('e', 'juist'), ('f', 'fout: aan de <b>onderkant</b>.')], '')}
{oef('opl_8', 8, 'Transport in de plant', 'Vul aan met: <i>wortelhaartjes, houtvaten, zeefvaten, huidmondjes, opwaarts, neerwaarts, assimilaten</i>.<p style="line-height:2.2">Water en mineralen worden opgenomen door de ……………………. Via de ……………………. gaan ze ……………………. naar het blad. Een deel van het water verdampt via de ……………………. . In het blad worden ……………………. gemaakt. Ze worden via de ……………………. vooral ……………………. vervoerd.</p>',
  [('1', 'wortelhaartjes'), ('2', 'houtvaten'), ('3', 'opwaarts'), ('4', 'huidmondjes'), ('5', 'assimilaten'), ('6', 'zeefvaten'), ('7', 'neerwaarts')], '')}
{oef('opl_9', 9, 'Assimilaten', '<ol class="deelvragen" type="a"><li>Wat zijn assimilaten?</li><li>Noem de vier soorten assimilaten.</li><li>Waar worden ze gemaakt?</li></ol>' + lijnen(4),
  [('a', 'de eindproducten van de fotosynthese'), ('b', 'glucose, zetmeel, eiwitten en vetten'), ('c', 'in de bladgroenkorrels van de cellen van het vulweefsel van het blad')], '')}
{oef('opl_10', 10, 'Feedback', 'Een plant staat in de volle zon en krijgt te weinig water.<ol class="deelvragen" type="a"><li>Wat gebeurt er met de turgor van de sluitcellen?</li><li>Wat doen de huidmondjes?</li><li>Wat is het gevolg voor het waterverlies?</li><li>Is dit een positief of een negatief feedbacksysteem? Leg uit.</li></ol>' + lijnen(5),
  [('a', 'De sluitcellen verliezen water: de turgor daalt.'), ('b', 'Ze sluiten.'), ('c', 'De plant verliest minder water.'), ('d', 'Negatief: de reactie werkt de verandering (watertekort) tegen.')], '')}'''

cornell = '''<p>Op het bord bouwen we samen een <b>Cornellschema</b> op. Links staan de vragen, rechts noteer je de antwoorden. Onderaan vat je alles samen in je eigen woorden.</p>
<p><button class="knop licht" data-print="cornell">🖨 Druk het Cornellblad af</button></p>'''

samenv = kader('Samenvatting', '''<p>De <b>waterhuishouding</b> is de opname, het transport en de afgifte van water in de plant.</p>
<p>De plantenorganen zijn <b>wortel, stengel, blad en bloem</b>.</p>
<p><b>Blad</b>: dekweefsel (bescherming, waslaagje), cellen van het vulweefsel (fotosynthese), huidmondjes met sluitcellen (gasuitwisseling).</p>
<p><b>Huidmondje open</b>: sluitcellen nemen water op, vacuole zwelt, turgor stijgt. <b>Dicht</b>: water weg, turgor daalt.</p>
<p><b>Stengel</b>: vaatbundels in een kring. Houtvaten binnen, zeefvaten buiten, deelweefsel ertussen. Cortex en dekweefsel errond.</p>
<p><b>Wortel</b>: wortelhaartjes vergroten de oppervlakte. Eén vaatbundel in het midden.</p>
<p><b>Water</b>: wortelhaartjes → houtvaten → blad → huidmondjes (opwaarts). <b>Assimilaten</b> (glucose, zetmeel, eiwitten, vetten): blad → zeefvaten → vooral wortel (neerwaarts).</p>
<p><b>Homeostase</b>: bij watertekort sluiten de huidmondjes. Dat is een <b>negatief feedbacksysteem</b>.</p>''')

css_extra = '''<style>
@media print{ h2,h3{break-after:avoid;} section.blok[id^="deel"]:not(#deel1), section#oefeningen, section#samenvatting, section#voorkennis{break-before:page;} html,body{background:#fff !important;} .printblad{display:none;} }
.voorkennis{background:#fff7e6;border:1px solid #f2c97d;border-left:4px solid #d99a1e;border-radius:0 8px 8px 0;padding:10px 14px;margin:0 0 14px;}
.voorkennis .kop{font-weight:700;color:#8a5a0a;font-size:14px;margin-bottom:4px;}
.voorkennis ul{margin:0;padding-left:20px;font-size:15px;line-height:1.6;}
ol.invul{columns:2;font-size:15px;line-height:2;}
table.jf{border-collapse:collapse;margin:8px 0;font-size:15px;}
table.jf td,table.jf th{border:1px solid #cbd5e1;padding:5px 10px;text-align:left;}
table.jf td:nth-child(2),table.jf td:nth-child(3){text-align:center;width:50px;}
.figuur svg{max-width:100%;height:auto;}
</style>'''

delen = [('deel1', 'Waterhuishouding en plantenorganen', d1), ('deel2', 'Aanpassingen van het blad', d2), ('deel3', 'Gasuitwisseling via de huidmondjes', d3),
         ('deel4', 'Aanpassingen van de stengel', d4), ('deel5', 'Aanpassingen van de wortel', d5), ('deel6', 'Water- en assimilatentransport', d6),
         ('deel7', 'Homeostase van de waterhuishouding', d7)]
blokken = [blok('lesdoelen', '', 'Lesdoelen', lesdoelen), blok('voorkennis', '', 'Voorkennis', voorkennis)] + [blok(i, n+1, t, c, i) for n, (i, t, c) in enumerate(delen)] + [
    blok('oefeningen', '', 'Oefeningen op papier', oefs, 'oefeningen'), blok('samenvatting', '', 'Samenvatting', samenv, 'samenvatting')]
vrij = [('vk_opl', True, 'oplossing controlevragen voorkennis')] + [(i, n == 0, t) for n, (i, t, c) in enumerate(delen)] + [(f'denk_{k}', False, f'redenering denkvraag {k}') for k in (1, 2, 3)] + [('denk_serre', False, 'redenering denkvraag serre')] + \
       [('oefeningen', False, 'de oefeningen zelf (opgaven)')] + [(f'opl_{i}', False, f'oplossing oefening {i}') for i in range(1, 11)] + [('samenvatting', False, 'samenvatting')]
cvr = [['Wat is waterhuishouding?', 20], ['Welke vier plantenorganen ken je?', 18], ['Welke weefsels heeft een blad? Functie?', 34],
       ['Hoe opent en sluit een huidmondje? (vacuole, turgor)', 34], ['Bouw van de stengel en de wortel?', 34], ['Houtvat of zeefvat: verschil?', 26],
       ['Wat zijn assimilaten?', 18], ['Hoe verloopt het water- en assimilatentransport?', 30], ['Hoe houdt de plant haar waterhuishouding in evenwicht?', 26]]
bouw('cursus-waterhuishouding-planten.html', 'Biologie 3de jaar · Thema 1 Feedbacksystemen · Hoofdstuk 1', 'Homeostase van de waterhuishouding in planten',
     'Werk dit hoofdstuk samen met de tool <a href="biologie-prikkels.html">Water, prikkels en reacties</a>. Oefeningen maak je op papier.' + css_extra,
     blokken, vrij, cvr)
print('ok')
