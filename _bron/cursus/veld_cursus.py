exec(open('/home/claude/cursus/ac_help.py', encoding='utf-8').read())
zet_hfst(3)
TOOL = 'elektrisch-veld.html'
BL, GR_ = '#1D4ED8', '#0F766E'
LIJN = '#64748B'

# ---------- veldlijnen numeriek ----------
def veld(ladingen, x, y):
    ex = ey = 0
    for (qx, qy, Q) in ladingen:
        dx, dy = x - qx, y - qy; r2 = dx * dx + dy * dy
        if r2 < 1: r2 = 1
        r3 = r2 ** 1.5; ex += Q * dx / r3; ey += Q * dy / r3
    return ex, ey

def veldlijn(ladingen, x, y, richting=1, stap=2.0, n=900, box=(0, 0, 600, 300), stop_r=12):
    pts = [(x, y)]
    for _ in range(n):
        ex, ey = veld(ladingen, x, y); e = math.hypot(ex, ey)
        if e == 0: break
        x += richting * stap * ex / e; y += richting * stap * ey / e
        if not (box[0] <= x <= box[2] and box[1] <= y <= box[3]): pts.append((x, y)); break
        if any(math.hypot(x - qx, y - qy) < stop_r for qx, qy, _ in ladingen): pts.append((x, y)); break
        pts.append((x, y))
    return pts

def pad(pts, kleur=LIJN, pijlpos=0.45, omkeren=False):
    if len(pts) < 4: return ''
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    i = max(1, int(len(pts) * pijlpos)); (x1, y1), (x2, y2) = pts[i - 1], pts[i]
    if omkeren: (x1, y1), (x2, y2) = (x2, y2), (x1, y1)
    a = math.atan2(y2 - y1, x2 - x1)
    tip = f'<path d="M{x2+7*math.cos(a):.1f},{y2+7*math.sin(a):.1f} L{x2-7*math.cos(a-0.45):.1f},{y2-7*math.sin(a-0.45):.1f} L{x2-7*math.cos(a+0.45):.1f},{y2-7*math.sin(a+0.45):.1f}Z" fill="{kleur}"/>'
    return f'<path d="{d}" fill="none" stroke="{kleur}" stroke-width="1.6"/>' + tip

def fig_lijnen(ladingen, w, h, n=12, titel=''):
    s = ''
    for (qx, qy, Q) in ladingen:
        # lijnen vertrekken uit + ladingen; uit − ladingen volgen we de lijn achteruit en houden we
        # enkel de lijnen die niet op een + lading uitkomen (die komen van buitenaf binnen)
        for i in range(n):
            a = 2 * math.pi * (i + 0.5) / n
            r = 14
            pts = veldlijn(ladingen, qx + r * math.cos(a), qy + r * math.sin(a), 1 if Q > 0 else -1, box=(0, 0, w, h))
            if Q < 0:
                ex, ey = pts[-1]
                if any(L[2] > 0 and math.hypot(ex - L[0], ey - L[1]) < 13 for L in ladingen): continue
            s += pad(pts, omkeren=Q < 0)
    for (qx, qy, Q) in ladingen: s += q(qx, qy, 1 if Q > 0 else -1, 11)
    if titel: s += tx(w / 2, h - 8, titel, 13)
    return s

def fig_soorten():
    w, h = 300, 240
    panelen = [([(150, 110, 1)], 'positieve puntlading'), ([(150, 110, -1)], 'negatieve puntlading'),
               ([(100, 110, 1), (200, 110, -1)], 'tegengestelde ladingen'), ([(100, 110, 1), (200, 110, 1)], 'gelijke ladingen')]
    s = ''
    for i, (lad, t) in enumerate(panelen):
        x0, y0 = (i % 2) * 320, (i // 2) * 250
        inner = fig_lijnen(lad, w, h - 20, 12)
        s += f'<g transform="translate({x0},{y0})"><rect x="0" y="0" width="{w}" height="{h}" fill="#fff" stroke="#E2E8F0"/>{inner}{tx(w/2, h-8, t, 13)}</g>'
    return svg(s, 620, 500)

def fig_vector():
    s = ''
    for i, (Q, t) in enumerate([(1, 'positieve bronlading'), (-1, 'negatieve bronlading')]):
        x0 = i * 320; qx, qy, px, py = x0 + 70, 90, x0 + 210, 90
        s += f'<line x1="{qx}" y1="{qy}" x2="{px+80}" y2="{py}" stroke="#E2E8F0" stroke-dasharray="4 4"/>'
        s += q(qx, qy, Q, 13) + f'<circle cx="{px}" cy="{py}" r="4" fill="{INK}"/>' + tx(px, py + 22, 'P', 13)
        s += pijl(px, py, px + (70 if Q > 0 else -70), py, BL, 3) + tx(px + (35 if Q > 0 else -35), py - 12, 'E', 15, BL)
        s += tx(x0 + 150, 160, t, 13) + tx(x0 + 150, 180, 'E wijst ' + ('weg van Q' if Q > 0 else 'naar Q toe'), 13, DIM, 'middle', 400)
    return svg(s, 640, 195)

def fig_proef():
    s = f'<rect x="20" y="20" width="600" height="130" fill="#F8FAFC" stroke="#E2E8F0"/>'
    for i in range(5): s += pijl(40, 40 + i * 25, 600, 40 + i * 25, '#CBD5E1', 1.2)
    s += tx(590, 16, 'E', 14, LIJN, 'end')
    s += pijl(200, 85, 290, 85, BL, 3) + q(200, 85, 1, 12) + tx(250, 75, 'F', 14, BL)
    s += pijl(440, 85, 350, 85, BL, 3) + q(440, 85, -1, 12) + tx(395, 75, 'F', 14, BL)
    s += tx(200, 128, 'positieve lading: F mee met E', 13, INK) + tx(440, 128, 'negatieve lading: F tegen E in', 13, INK)
    return svg(s, 640, 165)

def fig_homogeen():
    s = '<rect x="60" y="30" width="16" height="200" fill="#d64550" opacity=".85"/><rect x="420" y="30" width="16" height="200" fill="#2a6f97" opacity=".85"/>'
    for i in range(8):
        y = 42 + i * 25; s += q(68, y, 1, 7) + q(428, y, -1, 7)
        s += pijl(80, y, 414, y, LIJN, 1.6)
    s += tx(250, 252, 'homogeen veld: evenwijdige, even ver uit elkaar liggende veldlijnen', 13, INK)
    s += tx(520, 120, 'E is overal', 13, INK, 'middle', 400) + tx(520, 140, 'even groot', 13, INK, 'middle', 400) + tx(520, 160, 'en even gericht', 13, INK, 'middle', 400)
    return svg(s, 640, 265)

def fig_bol():
    cx, cy, R = 170, 140, 55
    s = ''
    for i in range(16):
        a = 2 * math.pi * i / 16
        s += pijl(cx + R * math.cos(a), cy + R * math.sin(a), cx + 125 * math.cos(a), cy + 125 * math.sin(a), LIJN, 1.6)
    s += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{METAAL}" stroke="{RAND}" stroke-width="2"/>'
    for i in range(12):
        a = 2 * math.pi * (i + 0.5) / 12; s += q(cx + (R - 9) * math.cos(a), cy + (R - 9) * math.sin(a), 1, 6)
    s += tx(cx, cy + 5, 'E = 0', 13, INK)
    # grafiek
    X0, Y0, W, H = 360, 40, 250, 180
    s += f'<path d="M{X0},{Y0} V{Y0+H} H{X0+W}" fill="none" stroke="{INK}" stroke-width="2"/>'
    rR = 60
    pts = ' L'.join(f'{X0 + r:.1f},{Y0 + H - 150 * (rR / r) ** 2:.1f}' for r in range(rR, W + 1, 3))
    s += f'<path d="M{X0},{Y0+H-1} H{X0+rR}" stroke="{BL}" stroke-width="3"/><path d="M{X0+rR},{Y0+H} V{Y0+H-150}" stroke="{BL}" stroke-width="1.5" stroke-dasharray="4 3"/><path d="M{pts}" fill="none" stroke="{BL}" stroke-width="3"/>'
    s += tx(X0 - 8, Y0 + 8, 'E', 14, INK, 'end') + tx(X0 + W, Y0 + H + 18, 'r', 14, INK, 'end') + tx(X0 + rR, Y0 + H + 18, 'R', 13, INK)
    s += tx(X0 + rR / 2, Y0 + H - 10, 'binnen: 0', 11, BL, 'middle', 600) + tx(X0 + 150, Y0 + 70, 'buiten: k·Q/r²', 12, BL, 'start', 600)
    return svg(s, 640, 260)

def fig_grafieken():
    s = ''
    X0, Y0, W, H = 50, 30, 230, 160
    s += f'<path d="M{X0},{Y0} V{Y0+H} H{X0+W}" fill="none" stroke="{INK}" stroke-width="2"/>'
    pts = ' L'.join(f'{X0 + r:.1f},{Y0 + H - H * (28 / r) ** 2:.1f}' for r in range(28, W + 1, 2))
    s += f'<path d="M{pts}" fill="none" stroke="{BL}" stroke-width="3"/>' + tx(X0 + W / 2, Y0 + H + 36, 'radiaal veld (puntlading)', 13)
    s += tx(X0 - 8, Y0 + 8, 'E', 14, INK, 'end') + tx(X0 + W, Y0 + H + 18, 'r', 14, INK, 'end')
    X1 = 360
    s += f'<path d="M{X1},{Y0} V{Y0+H} H{X1+W}" fill="none" stroke="{INK}" stroke-width="2"/>'
    s += f'<path d="M{X1},{Y0+H-1} H{X1+40} M{X1+40},{Y0+H} V{Y0+70} H{X1+190} V{Y0+H} M{X1+190},{Y0+H-1} H{X1+W}" fill="none" stroke="{BL}" stroke-width="3"/>'
    s += tx(X1 + 115, Y0 + 60, 'tussen de platen: constant', 12, BL) + tx(X1 + W / 2, Y0 + H + 36, 'homogeen veld (twee platen)', 13)
    s += tx(X1 - 8, Y0 + 8, 'E', 14, INK, 'end') + tx(X1 + W, Y0 + H + 18, 'x', 14, INK, 'end') + tx(X1 + 40, Y0 + H + 18, '+', 14, POS) + tx(X1 + 190, Y0 + H + 18, '−', 14, NEG)
    return svg(s, 640, 240)

def fig_faraday():
    s = '<rect x="20" y="20" width="16" height="200" fill="#d64550" opacity=".85"/><rect x="604" y="20" width="16" height="200" fill="#2a6f97" opacity=".85"/>'
    bx, by, bw, bh = 230, 60, 180, 120
    for i in range(8):
        y = 32 + i * 25
        if by < y < by + bh:
            s += pijl(40, y, bx - 2, y, LIJN, 1.6) + pijl(bx + bw, y, 598, y, LIJN, 1.6)
        else:
            s += pijl(40, y, 598, y, LIJN, 1.6)
    s += f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{METAAL}" stroke="{RAND}" stroke-width="3"/>'
    for i in range(4):
        s += q(bx + 9, by + 18 + i * 28, -1, 6) + q(bx + bw - 9, by + 18 + i * 28, 1, 6)
    s += tx(bx + bw / 2, by + bh / 2 - 4, 'binnenin:', 13, INK) + tx(bx + bw / 2, by + bh / 2 + 16, 'E = 0', 15, INK)
    s += tx(320, 245, 'De vrije elektronen verschuiven tot het veld binnenin nul is.', 13, DIM, 'middle', 400)
    return svg(s, 640, 260)

# ---------- inhoud ----------
lesdoelen = '''<p>De lesdoelen volgen het leerstofoverzicht. Na dit hoofdstuk kan je:</p>
<ul class="doelen">
<li>de elektrische veldvector ten gevolge van een positieve of negatieve bronlading in een bepaald punt tekenen;</li>
<li>noteren hoe de zin van de coulombkracht op een lading en de zin van het elektrisch veld zich tot elkaar verhouden;</li>
<li>de grootte van een radiaal en een homogeen elektrisch veld berekenen met de formule van de elektrische veldsterkte;</li>
<li>redeneervragen over de grootte van het elektrisch veld oplossen (let op voor verwarring met de coulombkracht);</li>
<li>de kenmerken van elektrische veldlijnen toepassen bij het tekenen van veldlijnen;</li>
<li>het elektrisch veld in een punt op een gegeven veldlijn tekenen;</li>
<li>de veldlijnen rond één of meerdere puntladingen, rond een bolvormige geleider en in een homogeen veld tekenen en berekenen;</li>
<li>de grafieken van de grootte van het elektrisch veld bij een radiaal en een homogeen veld tekenen;</li>
<li>het gedrag van geleiders en isolatoren in een elektrisch veld verklaren (kooi van Faraday);</li>
<li>twee voorbeelden van de kooi van Faraday noteren en hun functie uitleggen.</li></ul>
<p>Leerboek p. 35–46. Oefeningen in het leerboek: 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 17, 19, 20 (p. 44–46).</p>'''

voorkennis = '''<ul class="doelen">
<li>De wet van Coulomb: <i>F</i> = <i>k</i> · |<i>Q</i>₁| · |<i>Q</i>₂| / <i>r</i>² (hoofdstuk 2).</li>
<li>Geleiders hebben vrije elektronen; in isolatoren treedt polarisatie op (hoofdstuk 1).</li>
<li>Het zwaarteveld: elke massa ondervindt bij het aardoppervlak een kracht <i>F</i> = <i>m</i> · <i>g</i>, met <i>g</i> = 9,81 N/kg.</li></ul>'''

d31 = f'''<p>Een lading verandert de ruimte rond zich: elke andere lading in die ruimte ondervindt een kracht. Die ruimte noemen we een <b>elektrisch veld</b>. De lading die het veld maakt, is de <b>bronlading</b> <i>Q</i>. Om het veld te meten, gebruik je een kleine positieve <b>proeflading</b> <i>q</i>.</p>
<p>Je kent dit al van het zwaarteveld: <i>g</i> = <i>F</i> / <i>m</i> zegt hoeveel newton er per kilogram werkt. Het elektrisch veld zegt hoeveel newton er per coulomb werkt.</p>
{defi('Elektrische veldsterkte', '<p>De <b>elektrische veldsterkte</b> <b>E</b> in een punt is de coulombkracht per eenheid van (positieve) proeflading in dat punt. De richting en zin van <b>E</b> zijn die van de kracht op een <b>positieve</b> proeflading.</p>')}
{vgl('<i>E</i> = <i>F</i> / <i>q</i> &nbsp;&nbsp; (eenheid N/C)')}
{figuur(fig_vector(), 'De elektrische veldvector in een punt P. Hij begint in P.')}
<h3>3.1.1 Kracht en veld</h3>
<p>Op een <b>positieve</b> lading werkt de kracht <b>mee</b> met het veld, op een <b>negatieve</b> lading <b>tegen</b> het veld in (figuur 3.2). Voor de grootte geldt <i>F</i> = |<i>q</i>| · <i>E</i>.</p>
{figuur(fig_proef(), 'Zin van de coulombkracht in een elektrisch veld.')}
<h3>3.1.2 Radiaal veld van een puntlading</h3>
<p>Combineer je <i>E</i> = <i>F</i> / <i>q</i> met de wet van Coulomb, dan valt de proeflading weg:</p>
{vgl('<i>E</i> = <i>k</i> · |<i>Q</i>| / <i>r</i>²')}
<p>Het veld hangt dus alleen af van de bronlading <i>Q</i> en de afstand <i>r</i>, <b>niet</b> van de proeflading. Zo'n veld, dat langs rechten vanuit de lading loopt, heet een <b>radiaal veld</b>.</p>
{vb('Veld van een puntlading', '<p>Bereken de veldsterkte op 20 cm van een lading van +5,0 μC.</p><p><i>E</i> = 8,99 · 10⁹ · 5,0 · 10⁻⁶ / 0,20² = 1,1 · 10⁶ N/C, weg van de lading.</p>')}
<h3>3.1.3 Homogeen veld</h3>
<p>Tussen twee evenwijdige, tegengesteld geladen platen is het veld overal <b>even groot en even gericht</b>: een <b>homogeen veld</b>. De grootte vind je met <i>E</i> = <i>F</i> / <i>q</i>.</p>
{vb('Elektron in een homogeen veld', '<p>Tussen twee platen is <i>E</i> = 2,0 · 10⁴ N/C, naar rechts. Welke kracht werkt er op een elektron?</p><p><i>F</i> = |<i>q</i>| · <i>E</i> = 1,602 · 10⁻¹⁹ · 2,0 · 10⁴ = 3,2 · 10⁻¹⁵ N. Het elektron is negatief: de kracht wijst naar <b>links</b>, tegen het veld in.</p>')}
{kader('Let op: veld of kracht?', '<p>Verdubbel je de <b>proeflading</b>, dan verdubbelt de <b>kracht</b>, maar het <b>veld</b> blijft gelijk. Verdubbel je de <b>bronlading</b>, dan verdubbelen veld én kracht. Verdubbel je de <b>afstand</b> tot een puntlading, dan worden veld en kracht 4 keer kleiner.</p>')}
{tool(TOOL, 'Tool: tabbladen Bron- en proeflading en Puntlading')}
{denk('denk_1', 'In punt P meet je met een proeflading van +1 nC een veld van 500 N/C. Je vervangt de proeflading door een lading van −3 nC. Hoe groot is het veld nu in P? En de kracht?', [
  ('Veld', 'Het veld hangt niet af van de proeflading: nog altijd 500 N/C, met dezelfde zin.'), ('Kracht', '<i>F</i> = |<i>q</i>| · <i>E</i> = 3 · 10⁻⁹ · 500 = 1,5 · 10⁻⁶ N.'), ('Zin', 'De lading is negatief: de kracht wijst tegen het veld in.')], 'E = 500 N/C (onveranderd); F = 1,5 · 10⁻⁶ N, tegen het veld in.')}'''

d32 = f'''<h3>3.2.1 Elektrische veldlijnen</h3>
<p>Een veld teken je met <b>veldlijnen</b>. Die geven in één tekening de richting en de sterkte van het veld weer.</p>
{defi('Kenmerken van veldlijnen', '<ol><li>Veldlijnen vertrekken op <b>positieve</b> ladingen en eindigen op <b>negatieve</b> ladingen (of in het oneindige).</li><li>De <b>raaklijn</b> aan een veldlijn geeft de richting van <b>E</b>; de pijl geeft de zin.</li><li>Waar de veldlijnen <b>dichter</b> bij elkaar liggen, is het veld <b>sterker</b>.</li><li>Veldlijnen <b>snijden</b> elkaar nooit.</li><li>Veldlijnen staan <b>loodrecht</b> op het oppervlak van een geleider.</li></ol>')}
<p>Is een veldlijn gegeven, dan teken je het veld in een punt als een pijl die in dat punt <b>raakt</b> aan de veldlijn, in de zin van de veldlijn.</p>
<h3>3.2.2 Soorten elektrische velden</h3>
{figuur(fig_soorten(), 'Veldlijnen rond één en twee puntladingen, berekend met de wet van Coulomb.')}
<p>Rond <b>één puntlading</b> zijn de veldlijnen rechten: een radiaal veld. Bij <b>twee tegengestelde ladingen</b> lopen de veldlijnen van de positieve naar de negatieve lading. Bij <b>twee gelijke ladingen</b> buigen de veldlijnen van elkaar weg; midden tussen de ladingen is het veld nul.</p>
<p>Bij een <b>geladen geleidende bol</b> zit alle lading aan het oppervlak. Binnenin is het veld nul. Buiten de bol is het veld hetzelfde als dat van een puntlading in het middelpunt (figuur 3.4).</p>
{figuur(fig_bol(), 'Geladen geleidende bol: veldlijnen en de grootte van het veld in functie van de afstand tot het middelpunt.')}
{figuur(fig_homogeen(), 'Homogeen veld tussen twee evenwijdige geladen platen.')}
{figuur(fig_grafieken(), 'De grootte van het veld: bij een puntlading daalt ze met 1/r², tussen twee platen is ze constant.')}
{tool(TOOL, 'Tool: tabbladen Meerdere ladingen, Geleidende bol en Homogeen veld')}

<h3>3.2.3 Geleiders en isolatoren in een elektrisch veld</h3>
<p>Breng je een <b>geleider</b> in een elektrisch veld, dan verschuiven de vrije elektronen (influentie). Ze verschuiven tot het veld dat ze zelf maken, het uitwendige veld binnenin precies opheft (figuur 3.7).</p>
{figuur(fig_faraday(), 'Een metalen doos in een homogeen veld. Binnenin is het veld nul: een kooi van Faraday.')}
{defi('Kooi van Faraday', '<p>Een <b>kooi van Faraday</b> is een gesloten geleidende omhulling. Binnenin is het elektrisch veld <b>nul</b>, wat er buiten ook gebeurt. Ook een metalen gaas werkt als kooi, als de mazen klein genoeg zijn.</p>')}
<p>Een <b>isolator</b> heeft geen vrije elektronen. Door polarisatie wordt het veld binnenin wel <b>zwakker</b>, maar niet nul.</p>
<h4>Voorbeelden</h4>
<ul>
<li><b>Auto en vliegtuig</b>: slaat de bliksem in, dan loopt de lading over de metalen buitenkant. Binnenin ben je veilig. Ook een vliegtuig dat in een onweer landt op Brussels Airport, beschermt zo zijn passagiers.</li>
<li><b>Tram</b>: een tram van de MIVB heeft een metalen koetswerk. Tijdens een onweer zit je er veiliger in dan onder een boom.</li>
<li><b>Microgolfoven</b>: de wanden en het metalen rooster in de deur houden de microgolven binnen. De gaatjes zijn veel kleiner dan de golflengte.</li>
<li><b>Coaxkabel</b>: een metalen mantel rond de binnengeleider schermt het signaal af van storende velden van buiten.</li></ul>
{tool(TOOL, 'Tool: tabblad Geleiders en isolatoren')}
{kader('Brussel · onweer', '<p>Onder een onweerswolk is het elektrisch veld aan de grond veel sterker dan bij mooi weer. De negatieve onderkant van de wolk maakt de grond positief (influentie, hoofdstuk 1): het veld wijst dan van de grond <b>naar boven</b>, naar de wolk. Het KMI in Ukkel registreert de ontladingen die volgen.</p>')}
{denk('denk_2', 'Waarom is het gevaarlijk om tijdens een onweer op het grasveld van het Jubelpark te staan, maar veilig om in een auto te zitten?', [
  ('Grasveld', 'Je bent het hoogste punt in de buurt en je lichaam geleidt: de bliksem kan via jou naar de aarde gaan.'), ('Auto', 'Het metalen koetswerk is een kooi van Faraday: de lading loopt over de buitenkant naar de aarde.'), ('Binnenin', 'Het veld in de auto is nul; er gaat geen stroom door je lichaam.')], 'In de auto ben je beschermd door de kooi van Faraday.')}'''

oefs = f'''<p>Maak deze oefeningen op papier. Teken telkens eerst het veld en de kracht, vertrekkend in het punt of op de lading. Maak ook de oefeningen 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 17, 19 en 20 in het leerboek (p. 44–46).</p>
<p><button class="knop licht" data-print="oef">Oefeningen afdrukken</button></p>
{oef('opl_1', 1, 'Veldsterkte meten', 'Een proeflading van +4,0 nC ondervindt in punt P een kracht van 2,0 · 10⁻⁴ N naar rechts.<ol class="deelvragen" type="a"><li>Bereken de veldsterkte in P.</li><li>Welke kracht ondervindt een elektron in P?</li></ol>', [
  ('a', '<i>E</i> = <i>F</i> / <i>q</i> = 2,0 · 10⁻⁴ / 4,0 · 10⁻⁹ = 5,0 · 10⁴ N/C, naar rechts'), ('b', '<i>F</i> = 1,602 · 10⁻¹⁹ · 5,0 · 10⁴ = 8,0 · 10⁻¹⁵ N, naar links')], '<i>E</i> = 5,0 · 10⁴ N/C naar rechts')}
{oef('opl_2', 2, 'Radiaal veld', 'Een lading van −2,0 μC ligt in de oorsprong.<ol class="deelvragen" type="a"><li>Bereken de veldsterkte op 10 cm en op 30 cm.</li><li>Teken de veldvector in beide punten.</li><li>Waar is het veld 1,0 · 10⁵ N/C?</li></ol>', [
  ('a', '10 cm: 8,99 · 10⁹ · 2,0 · 10⁻⁶ / 0,10² = 1,8 · 10⁶ N/C; 30 cm: 9 keer kleiner, 2,0 · 10⁵ N/C'), ('b', 'Beide vectoren wijzen naar de lading toe; de pijl op 30 cm is 9 keer korter.'), ('c', '<i>r</i> = √(<i>k</i>|<i>Q</i>|/<i>E</i>) = √(8,99 · 10⁹ · 2,0 · 10⁻⁶ / 1,0 · 10⁵) = 0,42 m')], 'Op 42 cm van de lading.')}
{oef('opl_3', 3, 'Veld of kracht?', 'Juist of fout? Verbeter.<ol class="deelvragen" type="a"><li>Als je de proeflading verdubbelt, verdubbelt het veld.</li><li>Als je de afstand tot een puntlading halveert, wordt het veld 4 keer groter.</li><li>Op een negatieve lading werkt de kracht tegen het veld in.</li><li>In een homogeen veld is de kracht op een lading overal even groot.</li></ol>', [
  ('a', 'Fout: het veld hangt niet af van de proeflading; de kracht verdubbelt.'), ('b', 'Juist.'), ('c', 'Juist.'), ('d', 'Juist: E is overal gelijk, dus F = |q|·E ook.')], '')}
{oef('opl_4', 4, 'Veldlijnen tekenen', 'Teken de veldlijnen<ol class="deelvragen" type="a"><li>rond een lading van −Q;</li><li>rond twee ladingen +Q en −Q;</li><li>rond twee ladingen +2Q en −Q (let op het aantal lijnen);</li><li>tussen twee evenwijdige platen.</li></ol>Gebruik telkens de vijf kenmerken van veldlijnen.', [
  ('a', 'Rechte lijnen die naar de lading toe wijzen.'), ('b', 'Lijnen van + naar −, gebogen; dichtst bij elkaar tussen de ladingen.'), ('c', 'Dubbel zoveel lijnen vertrekken bij +2Q; de helft eindigt op −Q, de rest gaat naar het oneindige.'), ('d', 'Evenwijdige lijnen op gelijke afstand, van + naar −, loodrecht op de platen.')], '')}
{oef('opl_5', 5, 'Geleidende bol', 'Een metalen bol met straal 10 cm heeft een lading van +3,0 nC.<ol class="deelvragen" type="a"><li>Hoe groot is het veld in het middelpunt?</li><li>Bereken het veld net buiten het oppervlak en op 30 cm van het middelpunt.</li><li>Schets de grafiek E(r).</li></ol>', [
  ('a', '0 N/C: binnen een geleider is het veld nul.'), ('b', '<i>r</i> = 0,10 m: 8,99 · 10⁹ · 3,0 · 10⁻⁹ / 0,10² = 2,7 · 10³ N/C; <i>r</i> = 0,30 m: 3,0 · 10² N/C'), ('c', 'Nul tot <i>R</i>, dan een sprong naar het maximum, daarna dalend met 1/r².')], '')}
{oef('opl_6', 6, 'Brussel · regendruppel onder een onweerswolk', 'Boven Brussel hangt een onweerswolk. Aan de grond is het veld 5,0 · 10³ N/C, naar boven gericht. Een regendruppel heeft een lading van −2,0 · 10⁻¹² C.<ol class="deelvragen" type="a"><li>Bereken de elektrische kracht op de druppel. Welke zin heeft ze?</li><li>De druppel heeft een massa van 4,0 · 10⁻⁶ kg. Vergelijk met zijn gewicht.</li></ol>', [
  ('a', '<i>F</i> = 2,0 · 10⁻¹² · 5,0 · 10³ = 1,0 · 10⁻⁸ N, naar beneden (negatieve lading: tegen het veld in)'), ('b', '<i>F</i><sub>z</sub> = 4,0 · 10⁻⁶ · 9,81 = 3,9 · 10⁻⁵ N: ongeveer 4000 keer groter dan de elektrische kracht.')], 'De elektrische kracht is hier verwaarloosbaar tegenover het gewicht.')}
{oef('opl_7', 7, 'Kooi van Faraday', 'Geef twee voorbeelden van een kooi van Faraday en leg telkens uit wat de functie is. Waarom werkt een raam in de deur van een microgolfoven met een metalen rooster wel, en een gewoon glazen raam niet?', [
  ('Voorbeelden', 'Auto of vliegtuig (bescherming bij bliksem), coaxkabel (afscherming van het signaal), microgolfoven (golven binnenhouden).'), ('Raam', 'Glas is een isolator: het veld gaat erdoor. Het metalen rooster is een geleider met kleine gaatjes: het werkt als kooi.')], '')}
{oef('opl_8', 8, 'Veld op een veldlijn', 'Teken een gebogen veldlijn met een pijl erop. Kies drie punten A, B en C op die lijn.<ol class="deelvragen" type="a"><li>Teken in elk punt de richting en de zin van het elektrisch veld.</li><li>Teken in A de kracht op een proton en op een elektron.</li><li>Waar is het veld het sterkst, als de lijnen daar dichter bij elkaar liggen?</li></ol>', [
  ('a', 'In elk punt: de raaklijn aan de veldlijn, met de zin van de pijl op de lijn.'), ('b', 'Proton: zelfde zin als E. Elektron: tegengestelde zin. Beide vertrekken in A.'), ('c', 'Waar de veldlijnen het dichtst bij elkaar liggen.')],
  'Het veld raakt aan de veldlijn; de zin volgt de pijl.')}'''

begrippen = '''<div class="begrippen">
<p><b>bronlading</b> — lading die het elektrisch veld maakt</p>
<p><b>proeflading</b> — kleine positieve lading waarmee je het veld meet</p>
<p><b>elektrische veldsterkte</b> — kracht per eenheid van lading, <i>E</i> = <i>F</i>/<i>q</i>, in N/C</p>
<p><b>radiaal veld</b> — veld van een puntlading, langs rechten vanuit de lading</p>
<p><b>homogeen veld</b> — veld dat overal even groot en even gericht is</p>
<p><b>veldlijn</b> — lijn waarvan de raaklijn in elk punt de richting van het veld geeft</p>
<p><b>kooi van Faraday</b> — gesloten geleidende omhulling waarbinnen het veld nul is</p>
</div>'''

cornell = '''<p>Op het bord bouwen we samen een Cornellschema op. Dek thuis de rechterkolom af en overhoor jezelf.</p>
<p><button class="knop licht" data-print="cornell">Cornellblad afdrukken</button></p>'''

samenv = kader('Samenvatting', '''<p><b>Veldsterkte</b>: <i>E</i> = <i>F</i>/<i>q</i> (N/C), in de zin van de kracht op een positieve lading. Op een negatieve lading werkt de kracht tegen het veld in.</p>
<p><b>Radiaal veld</b>: <i>E</i> = <i>k</i>|<i>Q</i>|/<i>r</i>², onafhankelijk van de proeflading. <b>Homogeen veld</b>: overal gelijk (tussen twee platen).</p>
<p><b>Veldlijnen</b>: van + naar −, raaklijn = richting, dichtheid = sterkte, snijden nooit, loodrecht op geleiders.</p>
<p><b>Geleidende bol</b>: binnenin E = 0, buiten zoals een puntlading. <b>Kooi van Faraday</b>: binnenin E = 0 (auto, vliegtuig, microgolfoven, coaxkabel).</p>''')

delen = [('deel31', '3.1', 'Grootte van het elektrisch veld', d31), ('deel32', '3.2', 'Eigenschappen van het elektrisch veld', d32)]
blokken = [blok('lesdoelen', '', 'Lesdoelen', lesdoelen), blok('voorkennis', '', 'Voorkennis', voorkennis)] + \
          [blok(i, n, t, c, i) for i, n, t, c in delen] + \
          [blok('oefeningen', '', 'Oefeningen', oefs, 'oefeningen'), blok('begrippen', '', 'Begrippenlijst', begrippen), blok('samenvatting', '', 'Samenvatting', samenv, 'samenvatting')]
vrij = [('deel31', True, '3.1 Grootte van het elektrisch veld'), ('deel32', False, '3.2 Eigenschappen van het elektrisch veld'),
        ('denk_1', False, 'redenering denkvraag 1'), ('denk_2', False, 'redenering denkvraag 2'),
        ('oefeningen', False, 'de oefeningen zelf (opgaven)')] + [(f'opl_{i}', False, f'oplossing oefening {i}') for i in range(1, 9)] + [('samenvatting', False, 'samenvatting')]
cvr = [['Wat is de elektrische veldsterkte? Formule, eenheid, zin?', 30], ['Verband tussen de zin van F en van E?', 22], ['Formule radiaal veld? Waarvan hangt E af, waarvan niet?', 30],
       ['Wat is een homogeen veld?', 20], ['Kenmerken van veldlijnen?', 32], ['Veld rond een geleidende bol? Grafiek?', 28], ['Wat is een kooi van Faraday? Voorbeelden?', 30]]
bouw('cursus-elektrisch-veld.html', 'Fysica 5de jaar · Thema 1 Elektrostatica · Hoofdstuk 3', 'Elektrisch veld',
     'Deze cursus hoort bij de tool <a href="elektrisch-veld.html">Elektrisch veld</a>. Oefeningen maak je op papier.',
     blokken, vrij, cvr)
print('ok')
