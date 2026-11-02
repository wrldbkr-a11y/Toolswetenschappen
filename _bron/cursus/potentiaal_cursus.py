exec(open('/home/claude/cursus/ac_help.py', encoding='utf-8').read())
zet_hfst(4)
TOOL = 'elektrisch-veld.html'
BL, LIJN = '#1D4ED8', '#64748B'

def platen(x_neg, x_pos, y0, h, n=7):
    """negatieve plaat links, positieve plaat rechts; E wijst van + naar − (naar links)"""
    s = f'<rect x="{x_neg-14}" y="{y0}" width="14" height="{h}" fill="{NEG}" opacity=".85"/><rect x="{x_pos}" y="{y0}" width="14" height="{h}" fill="{POS}" opacity=".85"/>'
    for i in range(n):
        y = y0 + 14 + i * (h - 28) / (n - 1)
        s += q(x_neg - 7, y, -1, 6) + q(x_pos + 7, y, 1, 6)
    return s

def fig_analogie():
    s = f'<rect x="20" y="230" width="260" height="14" fill="#A3B18A"/>' + tx(150, 262, 'grond: E_pot = 0', 12, DIM, 'middle', 400)
    s += f'<circle cx="150" cy="80" r="16" fill="#F59E0B" stroke="#92400E"/>' + pijl(150, 96, 150, 150, '#B45309', 3) + tx(160, 130, 'F_z = m·g', 13, '#B45309', 'start')
    s += f'<line x1="70" y1="80" x2="70" y2="230" stroke="{INK}" stroke-width="1.5"/>' + tx(60, 160, 'h', 15, INK, 'end')
    s += tx(150, 30, 'zwaarteveld', 15) + tx(150, 50, 'E_pot = m · g · h', 14, INK, 'middle', 400)
    s += platen(380, 600, 70, 170)
    s += q(520, 155, 1, 12) + pijl(508, 155, 450, 155, BL, 3) + tx(470, 145, 'F = Q·E', 13, BL)
    s += f'<line x1="380" y1="205" x2="520" y2="205" stroke="{INK}" stroke-width="1.5"/>' + tx(450, 222, 'd', 15)
    s += pijl(590, 85, 395, 85, LIJN, 1.5) + tx(492, 78, 'E', 13, LIJN)
    s += tx(490, 30, 'homogeen elektrisch veld', 15) + tx(490, 50, 'E_pot = Q · E · d', 14, INK, 'middle', 400) + tx(380, 262, 'negatieve plaat: E_pot = 0', 12, DIM, 'start', 400)
    s = s.replace('E_pot', 'E<tspan baseline-shift="sub" font-size="9">pot</tspan>').replace('F_z', 'F<tspan baseline-shift="sub" font-size="9">z</tspan>')
    return svg(s, 640, 275)

def fig_equi():
    x0, x1, y0, h = 120, 520, 40, 180
    s = platen(x0, x1, y0, h)
    for i in range(6):
        y = y0 + 15 + i * 30; s += pijl(x1 - 4, y, x0 + 4, y, '#CBD5E1', 1.4)
    for i in range(5):
        x = x0 + i * (x1 - x0) / 4
        if 0 < i < 4: s += f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y0+h}" stroke="#7C3AED" stroke-width="2" stroke-dasharray="6 4"/>'
        s += tx(x, y0 + h + 22, f'{i*50} V', 13, '#7C3AED')
    s += tx(320, 24, 'U = 200 V tussen de platen, D = 4,0 cm', 13)
    s += tx(320, y0 + h + 46, 'stippellijnen: equipotentiaalvlakken (loodrecht op de veldlijnen)', 13, DIM, 'middle', 400)
    return svg(s, 640, 280)

def fig_grafieken():
    s = ''
    def as_(X0, Y0, W, H, ylab, titel):
        return (f'<path d="M{X0},{Y0} V{Y0+H} H{X0+W}" fill="none" stroke="{INK}" stroke-width="2"/>' + tx(X0 - 6, Y0 + 8, ylab, 13, INK, 'end')
                + tx(X0 + W, Y0 + H + 16, 'd', 13, INK, 'end') + tx(X0 + W / 2, Y0 + H + 38, titel, 12))
    X, Y, W, H = 45, 30, 160, 130
    s += as_(X, Y, W, H, 'E', 'veldsterkte: constant') + f'<path d="M{X},{Y+50} H{X+W}" stroke="{BL}" stroke-width="3"/>'
    X = 255
    s += as_(X, Y, W, H, 'V', 'potentiaal: stijgt lineair') + f'<path d="M{X},{Y+H} L{X+W},{Y+10}" stroke="#7C3AED" stroke-width="3"/>'
    X = 465; Ym = Y + H / 2
    s += f'<path d="M{X},{Y} V{Y+H}" fill="none" stroke="{INK}" stroke-width="2"/><path d="M{X},{Ym} H{X+W}" stroke="{INK}" stroke-width="2"/>' + tx(X - 6, Y + 8, 'E_pot', 13, INK, 'end') + tx(X + W, Ym + 16, 'd', 13, INK, 'end')
    s += f'<path d="M{X},{Ym} L{X+W},{Y+5}" stroke="{POS}" stroke-width="3"/><path d="M{X},{Ym} L{X+W},{Y+H-5}" stroke="{NEG}" stroke-width="3"/>'
    s += tx(X + W - 4, Y + 24, '+Q', 12, POS, 'end') + tx(X + W - 4, Y + H - 14, '−Q', 12, NEG, 'end') + tx(X + W / 2, Y + H + 38, 'potentiële energie', 12)
    s = s.replace('E_pot', 'E<tspan baseline-shift="sub" font-size="9">pot</tspan>')
    return svg(s, 640, 210)

lesdoelen = '''<p>De lesdoelen volgen het leerstofoverzicht. Na dit hoofdstuk kan je:</p>
<ul class="doelen">
<li>de analogie uitleggen tussen de potentiële gravitationele energie <i>E</i><sub>pot,g</sub> = <i>m</i>·<i>g</i>·<i>h</i> en <i>E</i><sub>pot,E</sub> = <i>Q</i>·<i>E</i>·<i>d</i>;</li>
<li>het verband uitleggen tussen potentiële elektrische energie en de arbeid verricht door het elektrisch veld;</li>
<li>de potentiële elektrische energie op een plaats in een homogeen veld berekenen voor een positieve en een negatieve lading (op de negatieve plaat is ze 0);</li>
<li>verwoorden dat de elektrische potentiaal in een punt de potentiële energie per lading is (de potentiële energie van een testlading van +1 C);</li>
<li>de elektrische potentiaal op een plaats in een homogeen veld berekenen;</li>
<li>het verband uitleggen tussen elektrisch veld, elektrische energie en elektrische potentiaal, de grafieken tekenen en hun vorm uitleggen;</li>
<li>verwoorden wat een equipotentiaaloppervlak is en het in een homogeen veld tekenen;</li>
<li>de definitie van spanning (potentiaalverschil) noteren;</li>
<li>het verband uitleggen tussen potentiaalverschil en de verandering van potentiële en kinetische energie van een positieve en een negatieve lading in een homogeen veld;</li>
<li>verwoorden wat de eenheid elektronvolt (eV) betekent.</li></ul>
<p>Leerboek p. 47–60.</p>'''

voorkennis = '''<ul class="doelen">
<li>Potentiële gravitationele energie: <i>E</i><sub>pot</sub> = <i>m</i>·<i>g</i>·<i>h</i>; kinetische energie: <i>E</i><sub>kin</sub> = ½·<i>m</i>·<i>v</i>².</li>
<li>Arbeid: <i>W</i> = <i>F</i>·<i>s</i> als kracht en verplaatsing dezelfde zin hebben.</li>
<li>Behoud van energie: valt een voorwerp, dan wordt potentiële energie omgezet in kinetische energie.</li>
<li>Homogeen veld tussen twee platen; <i>F</i> = |<i>q</i>|·<i>E</i> (hoofdstuk 3).</li></ul>'''

d41 = f'''<p>Til je een steen op, dan verricht je arbeid tegen de zwaartekracht in. Die energie zit opgeslagen als <b>potentiële gravitationele energie</b>. Laat je de steen los, dan verricht de zwaartekracht arbeid en wordt die energie kinetische energie. In een homogeen elektrisch veld gebeurt precies hetzelfde met een lading (figuur 4.1).</p>
{figuur(fig_analogie(), 'Analogie tussen het zwaarteveld en een homogeen elektrisch veld. De negatieve plaat speelt de rol van de grond.')}
{defi('Potentiële elektrische energie in een homogeen veld', '<p>Een lading <i>Q</i> op afstand <i>d</i> van de <b>negatieve</b> plaat heeft een potentiële elektrische energie <i>E</i><sub>pot,E</sub> = <i>Q</i>·<i>E</i>·<i>d</i>. Op de negatieve plaat is <i>E</i><sub>pot,E</sub> = 0.</p>')}
{vgl('<i>E</i><sub>pot,E</sub> = <i>Q</i> · <i>E</i> · <i>d</i>')}
<table class="vb"><tr><td><i>Q</i></td><td>lading, in C, <b>met</b> teken</td></tr><tr><td><i>E</i></td><td>veldsterkte, in N/C</td></tr><tr><td><i>d</i></td><td>afstand tot de negatieve plaat, in m</td></tr></table>
<p>Voor een <b>positieve</b> lading is <i>E</i><sub>pot,E</sub> positief en het grootst bij de positieve plaat. Voor een <b>negatieve</b> lading is <i>E</i><sub>pot,E</sub> negatief en het kleinst (meest negatief) bij de positieve plaat.</p>
{vb('Positieve en negatieve lading', '<p>Tussen twee platen is <i>E</i> = 5,0 · 10³ N/C. Bereken de potentiële energie op 4,0 cm van de negatieve plaat van (a) een lading van +2,0 μC en (b) een elektron.</p><p>(a) <i>E</i><sub>pot</sub> = 2,0 · 10⁻⁶ · 5,0 · 10³ · 0,040 = 4,0 · 10⁻⁴ J<br>(b) <i>E</i><sub>pot</sub> = −1,602 · 10⁻¹⁹ · 5,0 · 10³ · 0,040 = −3,2 · 10⁻¹⁷ J</p>')}
<h3>Arbeid door het veld</h3>
<p>Beweegt een lading in de zin van de elektrische kracht, dan verricht het veld <b>positieve</b> arbeid en <b>daalt</b> de potentiële energie. Beweegt ze tegen de kracht in, dan moet jij arbeid leveren en <b>stijgt</b> de potentiële energie.</p>
{vgl('<i>W</i><sub>veld</sub> = −Δ<i>E</i><sub>pot,E</sub>')}
{denk('denk_1', 'Een positieve lading en een elektron worden allebei losgelaten in het midden tussen twee platen. Naar welke plaat beweegt elk? Neemt hun potentiële energie toe of af?', [
  ('Positieve lading', 'De kracht wijst mee met E, naar de negatieve plaat. d wordt kleiner, Q > 0: E<sub>pot</sub> daalt.'), ('Elektron', 'De kracht wijst tegen E in, naar de positieve plaat. d wordt groter, maar Q < 0: E<sub>pot</sub> wordt negatiever, dus daalt ook.'), ('Algemeen', 'Een vrije lading beweegt altijd zo dat het veld positieve arbeid verricht.')], 'Beide bewegen naar de plaat met het tegengestelde teken; bij beide daalt de potentiële energie en stijgt de kinetische energie.')}'''

d42 = f'''<h3>4.2.1 De elektrische potentiaal</h3>
<p>De potentiële energie hangt af van de lading die je in het veld brengt. Deel je ze door die lading, dan krijg je een grootheid die alleen nog van het <b>veld</b> en de <b>plaats</b> afhangt: de potentiaal.</p>
{defi('Elektrische potentiaal', '<p>De <b>elektrische potentiaal</b> <i>V</i> in een punt is de potentiële elektrische energie per eenheid van lading in dat punt. Het is de potentiële energie die een testlading van +1 C daar zou hebben.</p>')}
{vgl('<i>V</i> = <i>E</i><sub>pot,E</sub> / <i>Q</i> &nbsp;&nbsp; (eenheid volt: 1 V = 1 J/C)')}
<p>In een homogeen veld volgt daaruit, met <i>V</i> = 0 op de negatieve plaat:</p>
{vgl('<i>V</i> = <i>E</i> · <i>d</i>')}
<h3>Veld, energie en potentiaal: de grafieken</h3>
{figuur(fig_grafieken(), 'In een homogeen veld, in functie van de afstand d tot de negatieve plaat: het veld is constant, de potentiaal stijgt lineair, de potentiële energie stijgt (positieve lading) of daalt (negatieve lading) lineair.')}
<p>Het veld is overal gelijk. Omdat <i>V</i> = <i>E</i>·<i>d</i>, is de grafiek van de potentiaal een <b>rechte</b> door de oorsprong met als richtingscoëfficiënt <i>E</i>. De potentiële energie is <i>Q</i>·<i>V</i>: dezelfde rechte, vermenigvuldigd met <i>Q</i>. Voor een negatieve lading keert de rechte dus om.</p>
<h3>4.2.2 Equipotentiaaloppervlakken</h3>
{defi('Equipotentiaaloppervlak', '<p>Een <b>equipotentiaaloppervlak</b> is een oppervlak waarop elk punt dezelfde potentiaal heeft. Het staat overal <b>loodrecht</b> op de veldlijnen. Een lading verplaatsen langs zo’n oppervlak kost geen arbeid.</p>')}
{figuur(fig_equi(), 'Equipotentiaalvlakken in een homogeen veld: vlakken evenwijdig aan de platen, op gelijke afstanden.')}
{tool(TOOL, 'Tool: tabblad Energie en potentiaal')}'''

d43 = f'''{defi('Spanning', '<p>De <b>spanning</b> of het <b>potentiaalverschil</b> tussen twee punten A en B is het verschil van hun potentiaal: <i>U</i><sub>AB</sub> = <i>V</i><sub>A</sub> − <i>V</i><sub>B</sub>. Eenheid: volt (V).</p>')}
{vgl('<i>U</i><sub>AB</sub> = <i>V</i><sub>A</sub> − <i>V</i><sub>B</sub>')}
<p>Tussen twee platen op afstand <i>D</i> is de spanning <i>U</i> = <i>E</i>·<i>D</i>. Zo vind je ook het veld als je de spanning kent: <i>E</i> = <i>U</i>/<i>D</i>. Daarom gebruik je voor het veld ook de eenheid V/m (1 V/m = 1 N/C).</p>
<h3>Spanning en energie</h3>
<p>Beweegt een lading <i>Q</i> van A naar B en werkt alleen de elektrische kracht, dan geldt:</p>
{vgl('Δ<i>E</i><sub>kin</sub> = −Δ<i>E</i><sub>pot,E</sub> = <i>Q</i> · <i>U</i><sub>AB</sub>')}
<ul><li>Een <b>positieve</b> lading die van hoge naar lage potentiaal gaat (<i>U</i><sub>AB</sub> &gt; 0), wint kinetische energie.</li>
<li>Een <b>negatieve</b> lading die van lage naar hoge potentiaal gaat (<i>U</i><sub>AB</sub> &lt; 0), wint ook kinetische energie: <i>Q</i> en <i>U</i><sub>AB</sub> zijn allebei negatief.</li></ul>
{vb('Een elektron versnellen', '<p>Tussen twee platen staat een spanning van 200 V. Een elektron vertrekt in rust aan de negatieve plaat. Met welke snelheid komt het aan bij de positieve plaat?</p><p>Δ<i>E</i><sub>kin</sub> = <i>e</i>·<i>U</i> = 1,602 · 10⁻¹⁹ · 200 = 3,2 · 10⁻¹⁷ J.<br><i>v</i> = √(2·<i>E</i><sub>kin</sub>/<i>m</i>) = √(2 · 3,2 · 10⁻¹⁷ / 9,11 · 10⁻³¹) = 8,4 · 10⁶ m/s.</p>')}
<h3>De elektronvolt</h3>
{defi('Elektronvolt', '<p>Eén <b>elektronvolt</b> (eV) is de energie die een elektron wint als het een potentiaalverschil van 1 V doorloopt.</p>')}
{vgl('1 eV = 1,602 · 10⁻¹⁹ J')}
<p>In het voorbeeld hierboven wint het elektron dus 200 eV. De eenheid is handig voor de kleine energieën van atomen en deeltjes.</p>
{kader('Brussel · de metro', '<p>Volgens de MIVB staat er op de sporen van de Brusselse metro een spanning van ongeveer 900 V. Daarom mag niemand op de sporen komen. Voor de metro is die spanning nodig om de elektrische motoren aan te drijven.</p>')}
{denk('denk_2', 'Een proton en een elektron doorlopen allebei een potentiaalverschil van 1000 V, elk in de zin waarin het versnelt. Wie krijgt de meeste kinetische energie? Wie de grootste snelheid?', [
  ('Energie', 'ΔE<sub>kin</sub> = |Q|·|U| = 1000 eV voor allebei: dezelfde lading in absolute waarde.'), ('Snelheid', 'E<sub>kin</sub> = ½mv²: bij dezelfde energie heeft het lichtste deeltje de grootste snelheid.'), ('Vergelijk', 'Het elektron is ongeveer 1840 keer lichter dan het proton.')], 'Even veel energie (1000 eV), maar het elektron is veel sneller.')}'''

oefs = f'''<p>Maak deze oefeningen op papier. Let bij energie altijd op het <b>teken</b> van de lading.</p>
<p><button class="knop licht" data-print="oef">Oefeningen afdrukken</button></p>
{oef('opl_1', 1, 'Potentiële energie', 'Twee platen staan 5,0 cm uit elkaar, met <i>E</i> = 4,0 · 10⁴ N/C. Bereken de potentiële energie op 2,0 cm van de negatieve plaat van<ol class="deelvragen" type="a"><li>een lading van +3,0 nC;</li><li>een lading van −3,0 nC.</li></ol>', [
  ('a', '3,0 · 10⁻⁹ · 4,0 · 10⁴ · 0,020 = 2,4 · 10⁻⁶ J'), ('b', '−2,4 · 10⁻⁶ J')], '')}
{oef('opl_2', 2, 'Potentiaal', 'Gebruik de platen van oefening 1.<ol class="deelvragen" type="a"><li>Bereken de potentiaal op 2,0 cm en op 5,0 cm van de negatieve plaat.</li><li>Hoe groot is de spanning tussen de platen?</li><li>Teken de equipotentiaalvlakken van 0 V, 500 V, 1000 V, 1500 V en 2000 V.</li></ol>', [
  ('a', '<i>V</i> = <i>E</i>·<i>d</i>: 800 V en 2000 V'), ('b', '<i>U</i> = 2000 V − 0 V = 2,0 · 10³ V'), ('c', 'Vijf vlakken evenwijdig aan de platen, telkens 1,25 cm uit elkaar.')], '')}
{oef('opl_3', 3, 'Grafieken', 'Schets voor de platen van oefening 1, in functie van <i>d</i>: (a) <i>E</i>, (b) <i>V</i>, (c) <i>E</i><sub>pot</sub> van een proton, (d) <i>E</i><sub>pot</sub> van een elektron. Leg de vorm van elke grafiek uit.', [
  ('a', 'Horizontale rechte: het veld is homogeen.'), ('b', 'Rechte door de oorsprong, van 0 V tot 2000 V.'), ('c', 'Stijgende rechte: Q > 0.'), ('d', 'Dalende rechte onder de d-as: Q < 0.')], '')}
{oef('opl_4', 4, 'Energie en snelheid', 'Een proton vertrekt in rust aan de positieve plaat en beweegt naar de negatieve plaat. De spanning is 500 V.<ol class="deelvragen" type="a"><li>Hoeveel kinetische energie wint het proton, in eV en in J?</li><li>Bereken de eindsnelheid (<i>m</i> = 1,67 · 10⁻²⁷ kg).</li></ol>', [
  ('a', '500 eV = 500 · 1,602 · 10⁻¹⁹ = 8,0 · 10⁻¹⁷ J'), ('b', '<i>v</i> = √(2 · 8,0 · 10⁻¹⁷ / 1,67 · 10⁻²⁷) = 3,1 · 10⁵ m/s')], '')}
{oef('opl_5', 5, 'Tekens', 'Een elektron beweegt van punt A (<i>V</i> = 100 V) naar punt B (<i>V</i> = 300 V).<ol class="deelvragen" type="a"><li>Bereken <i>U</i><sub>AB</sub>.</li><li>Neemt de kinetische energie toe of af? Met hoeveel eV?</li><li>Wat als een proton dezelfde weg aflegt?</li></ol>', [
  ('a', '<i>U</i><sub>AB</sub> = 100 − 300 = −200 V'), ('b', 'Δ<i>E</i><sub>kin</sub> = <i>Q</i>·<i>U</i><sub>AB</sub> = (−e)(−200 V) = +200 eV: neemt toe.'), ('c', 'Δ<i>E</i><sub>kin</sub> = (+e)(−200 V) = −200 eV: het proton wordt afgeremd.')], '')}
{oef('opl_6', 6, 'Brussel · de metro', 'Stel dat een elektron in vacuüm het potentiaalverschil van ongeveer 900 V van de metrosporen doorloopt.<ol class="deelvragen" type="a"><li>Hoeveel energie wint het, in eV en in J?</li><li>Waarom is de energie van één elektron zo klein, terwijl 900 V toch gevaarlijk is?</li></ol>', [
  ('a', '900 eV = 900 · 1,602 · 10⁻¹⁹ = 1,4 · 10⁻¹⁶ J'), ('b', 'Gevaarlijk is niet één elektron, maar het enorme aantal elektronen dat per seconde door je lichaam kan stromen.')], '')}
{oef('opl_7', 7, 'Analogie', 'Vul de tabel aan. <table class="vb"><tr><td>zwaarteveld</td><td>homogeen elektrisch veld</td></tr><tr><td>massa <i>m</i></td><td>…</td></tr><tr><td><i>g</i></td><td>…</td></tr><tr><td>hoogte <i>h</i></td><td>…</td></tr><tr><td>grond: <i>E</i><sub>pot</sub> = 0</td><td>…</td></tr><tr><td><i>E</i><sub>pot</sub> = <i>m</i>·<i>g</i>·<i>h</i></td><td>…</td></tr></table>', [
  ('Lading', '<i>Q</i>'), ('Veld', '<i>E</i>'), ('Afstand', '<i>d</i> tot de negatieve plaat'), ('Nulniveau', 'negatieve plaat: <i>E</i><sub>pot</sub> = 0'), ('Formule', '<i>E</i><sub>pot</sub> = <i>Q</i>·<i>E</i>·<i>d</i>')], 'Verschil: Q kan negatief zijn, m niet.')}
{oef('opl_8', 8, 'Arbeid van het veld', 'Tussen twee platen staat een spanning van 2000 V. Een proton vertrekt aan de positieve plaat en komt aan bij de negatieve plaat.<ol class="deelvragen" type="a"><li>Hoeveel arbeid verricht het elektrisch veld op het proton?</li><li>Wat is het verband met de verandering van de potentiële energie?</li><li>Wat gebeurt er als het een elektron is dat van de negatieve naar de positieve plaat beweegt?</li></ol>', [
  ('a', 'W = Q · U = 1,602 · 10⁻¹⁹ · 2000 = 3,2 · 10⁻¹⁶ J (2000 eV)'), ('b', 'W = −ΔE<sub>pot</sub>: de potentiële energie daalt met 3,2 · 10⁻¹⁶ J en de kinetische energie stijgt evenveel.'), ('c', 'Ook dan verricht het veld positieve arbeid: het elektron wint 2000 eV kinetische energie en zijn potentiële energie daalt.')],
  'Arbeid van het veld = afname van de potentiële energie.')}'''

begrippen = '''<div class="begrippen">
<p><b>potentiële elektrische energie</b> — energie van een lading door haar plaats in een elektrisch veld</p>
<p><b>elektrische potentiaal</b> — potentiële energie per eenheid van lading, in volt (J/C)</p>
<p><b>equipotentiaaloppervlak</b> — oppervlak met overal dezelfde potentiaal, loodrecht op de veldlijnen</p>
<p><b>spanning (potentiaalverschil)</b> — <i>U</i><sub>AB</sub> = <i>V</i><sub>A</sub> − <i>V</i><sub>B</sub></p>
<p><b>elektronvolt</b> — energie die een elektron wint bij 1 V: 1,602 · 10⁻¹⁹ J</p>
</div>'''

cornell = '''<p>Op het bord bouwen we samen een Cornellschema op. Dek thuis de rechterkolom af en overhoor jezelf.</p>
<p><button class="knop licht" data-print="cornell">Cornellblad afdrukken</button></p>'''

samenv = kader('Samenvatting', '''<p><b>Potentiële elektrische energie</b> in een homogeen veld: <i>E</i><sub>pot,E</sub> = <i>Q</i>·<i>E</i>·<i>d</i>, met <i>d</i> de afstand tot de negatieve plaat (daar <i>E</i><sub>pot</sub> = 0). Analoog aan <i>m</i>·<i>g</i>·<i>h</i>. <i>W</i><sub>veld</sub> = −Δ<i>E</i><sub>pot</sub>.</p>
<p><b>Potentiaal</b>: <i>V</i> = <i>E</i><sub>pot</sub>/<i>Q</i> (volt); homogeen: <i>V</i> = <i>E</i>·<i>d</i>. Equipotentiaalvlakken staan loodrecht op de veldlijnen.</p>
<p><b>Spanning</b>: <i>U</i><sub>AB</sub> = <i>V</i><sub>A</sub> − <i>V</i><sub>B</sub>; tussen platen <i>U</i> = <i>E</i>·<i>D</i>. Δ<i>E</i><sub>kin</sub> = <i>Q</i>·<i>U</i><sub>AB</sub>. 1 eV = 1,602 · 10⁻¹⁹ J.</p>''')

delen = [('deel41', '4.1', 'Potentiële elektrische energie in een homogeen veld', d41), ('deel42', '4.2', 'Elektrische potentiaal in een homogeen veld', d42), ('deel43', '4.3', 'Potentiaalverschil', d43)]
blokken = [blok('lesdoelen', '', 'Lesdoelen', lesdoelen), blok('voorkennis', '', 'Voorkennis', voorkennis)] + \
          [blok(i, n, t, c, i) for i, n, t, c in delen] + \
          [blok('oefeningen', '', 'Oefeningen', oefs, 'oefeningen'), blok('begrippen', '', 'Begrippenlijst', begrippen), blok('samenvatting', '', 'Samenvatting', samenv, 'samenvatting')]
vrij = [('deel41', True, '4.1 Potentiële elektrische energie'), ('deel42', False, '4.2 Elektrische potentiaal'), ('deel43', False, '4.3 Potentiaalverschil'),
        ('denk_1', False, 'redenering denkvraag 1'), ('denk_2', False, 'redenering denkvraag 2'),
        ('oefeningen', False, 'de oefeningen zelf (opgaven)')] + [(f'opl_{i}', False, f'oplossing oefening {i}') for i in range(1, 9)] + [('samenvatting', False, 'samenvatting')]
cvr = [['Analogie tussen m·g·h en Q·E·d?', 28], ['Verband tussen arbeid en potentiële energie?', 22], ['E_pot van een positieve en een negatieve lading?', 26],
       ['Wat is potentiaal? Formule in een homogeen veld?', 26], ['Grafieken van E, V en E_pot?', 32], ['Wat is een equipotentiaaloppervlak?', 20], ['Wat is spanning? Verband met E_kin?', 30], ['Wat is een elektronvolt?', 16]]
bouw('cursus-potentiaal.html', 'Fysica 5de jaar · Thema 1 Elektrostatica · Hoofdstuk 4', 'Potentiaal',
     'Deze cursus hoort bij de tool <a href="elektrisch-veld.html">Elektrisch veld</a> (tabblad Energie en potentiaal). Oefeningen maak je op papier.',
     blokken, vrij, cvr)
print('ok')
