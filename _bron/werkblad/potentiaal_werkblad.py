"""Maakt werkblad-potentiaal.html (5Wet, thema 1, hoofdstuk 4).

    python3 _bron/werkblad/potentiaal_werkblad.py

Oplossingen: zichtbaar met ?leerkracht in de url, of voor iedereen als OPLOSSINGEN_VRIJ = true
(regel in de pagina, zoek op VRIJGAVE).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
POS, NEG, LIJN, KR = '#d64550', '#2a6f97', '#94a3b8', '#d64550'

# (lading in e, naam, oriëntatie, kant van de + plaat, A=(s,t), B=(s,t))
# s = afstand tot de − plaat (0 = op de − plaat, 1 = op de + plaat), t = plaats langs de plaat (0..1)
SITUATIES = [
    (1,  'proton',   'v', 'links',  (0.80, 0.22), (0.20, 0.62)),   # mee met de kracht
    (-1, 'elektron', 'h', 'boven',  (0.20, 0.25), (0.80, 0.62)),   # naar hogere potentiaal, toch W > 0
    (1,  'proton',   'v', 'rechts', (0.20, 0.30), (0.75, 0.68)),   # tegen de kracht in (weggeschoten)
    (-1, 'elektron', 'v', 'links',  (0.50, 0.20), (0.50, 0.80)),   # evenwijdig met de platen
]

W, H = 280, 210
X0, X1, Y0, Y1 = 46, 234, 30, 180   # ruimte tussen de platen


def punt(orient, plus, s, t):
    if orient == 'v':
        x = X1 - s * (X1 - X0) if plus == 'links' else X0 + s * (X1 - X0)
        return x, Y0 + t * (Y1 - Y0)
    y = Y1 - s * (Y1 - Y0) if plus == 'boven' else Y0 + s * (Y1 - Y0)
    return X0 + t * (X1 - X0), y


def kracht_richting(q, orient, plus):
    """Eenheidsvector van de elektrische kracht (schermcoördinaten)."""
    # veld wijst van + naar −
    if orient == 'v':
        e = (1, 0) if plus == 'links' else (-1, 0)
    else:
        e = (0, 1) if plus == 'boven' else (0, -1)
    z = 1 if q > 0 else -1
    return e[0] * z, e[1] * z


def pijl(x1, y1, x2, y2, kleur, b=1.6, streep=False):
    import math
    a = math.atan2(y2 - y1, x2 - x1); s = 8
    p = (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2 - math.cos(a)*s*0.7:.1f}" y2="{y2 - math.sin(a)*s*0.7:.1f}" '
         f'stroke="{kleur}" stroke-width="{b}"{" stroke-dasharray=\"5 4\"" if streep else ""}/>')
    p += (f'<polygon points="{x2:.1f},{y2:.1f} {x2 - s*math.cos(a-0.42):.1f},{y2 - s*math.sin(a-0.42):.1f} '
          f'{x2 - s*math.cos(a+0.42):.1f},{y2 - s*math.sin(a+0.42):.1f}" fill="{kleur}"/>')
    return p


def figuur(q, orient, plus, A, B):
    o = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" class="fig" xmlns="http://www.w3.org/2000/svg" font-family="Atkinson Hyperlegible, Arial, sans-serif">']
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>')
    # platen
    if orient == 'v':
        xp, xm = (X0 - 14, X1 + 2) if plus == 'links' else (X1 + 2, X0 - 14)
        o.append(f'<rect x="{xp}" y="{Y0-10}" width="12" height="{Y1-Y0+20}" fill="#fde2e4" stroke="{POS}"/>')
        o.append(f'<rect x="{xm}" y="{Y0-10}" width="12" height="{Y1-Y0+20}" fill="#dbeafe" stroke="{NEG}"/>')
        for i in range(6):
            y = Y0 + i * (Y1 - Y0) / 5
            o.append(f'<text x="{xp+6}" y="{y+4:.0f}" text-anchor="middle" font-weight="700" font-size="12" fill="{POS}">+</text>')
            o.append(f'<text x="{xm+6}" y="{y+4:.0f}" text-anchor="middle" font-weight="700" font-size="12" fill="{NEG}">−</text>')
        for i in range(4):
            y = Y0 + 10 + i * (Y1 - Y0 - 20) / 3
            x1, x2 = (X0 + 4, X1 - 4) if plus == 'links' else (X1 - 4, X0 + 4)
            o.append(f'<line x1="{x1}" y1="{y:.0f}" x2="{x2}" y2="{y:.0f}" stroke="{LIJN}" stroke-width="1"/>')
            xm_ = (x1 + x2) / 2 + (6 if plus == 'links' else -6)
            d = 1 if plus == 'links' else -1
            o.append(f'<polygon points="{xm_+5*d:.0f},{y:.0f} {xm_-3*d:.0f},{y-4:.0f} {xm_-3*d:.0f},{y+4:.0f}" fill="{LIJN}"/>')
    else:
        yp, ym = (Y0 - 14, Y1 + 2) if plus == 'boven' else (Y1 + 2, Y0 - 14)
        o.append(f'<rect x="{X0-10}" y="{yp}" width="{X1-X0+20}" height="12" fill="#fde2e4" stroke="{POS}"/>')
        o.append(f'<rect x="{X0-10}" y="{ym}" width="{X1-X0+20}" height="12" fill="#dbeafe" stroke="{NEG}"/>')
        for i in range(8):
            x = X0 + i * (X1 - X0) / 7
            o.append(f'<text x="{x:.0f}" y="{yp+10}" text-anchor="middle" font-weight="700" font-size="12" fill="{POS}">+</text>')
            o.append(f'<text x="{x:.0f}" y="{ym+10}" text-anchor="middle" font-weight="700" font-size="12" fill="{NEG}">−</text>')
        for i in range(5):
            x = X0 + 12 + i * (X1 - X0 - 24) / 4
            y1, y2 = (Y0 + 4, Y1 - 4) if plus == 'boven' else (Y1 - 4, Y0 + 4)
            o.append(f'<line x1="{x:.0f}" y1="{y1}" x2="{x:.0f}" y2="{y2}" stroke="{LIJN}" stroke-width="1"/>')
            ym_ = (y1 + y2) / 2 + (8 if plus == 'boven' else -8)
            d = 1 if plus == 'boven' else -1
            o.append(f'<polygon points="{x:.0f},{ym_+5*d:.0f} {x-4:.0f},{ym_-3*d:.0f} {x+4:.0f},{ym_-3*d:.0f}" fill="{LIJN}"/>')
    ax, ay = punt(orient, plus, *A); bx, by = punt(orient, plus, *B)
    # verplaatsing
    import math
    L = math.hypot(bx - ax, by - ay); ux, uy = (bx - ax) / L, (by - ay) / L
    o.append(pijl(ax + ux * 13, ay + uy * 13, bx - ux * 6, by - uy * 6, '#1D2A36', 1.4, streep=True))
    o.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="3.5" fill="#1D2A36"/>')
    # lading in A
    kleur = POS if q > 0 else NEG
    lab = {1: '+', -1: '−', 2: '2+'}[q]
    o.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="10" fill="{kleur}"/>')
    o.append(f'<text x="{ax:.1f}" y="{ay+4.5:.1f}" text-anchor="middle" font-weight="700" font-size="{11 if q==2 else 14}" fill="#fff">{lab}</text>')
    # labels A en B (weg van de verplaatsing)
    o.append(f'<text x="{ax - ux*20 + (uy*14):.1f}" y="{ay - uy*20 - (ux*0) + 5:.1f}" text-anchor="middle" font-weight="700" font-size="14">A</text>')
    o.append(f'<text x="{bx + ux*14 + (uy*10):.1f}" y="{by + uy*14 + 5:.1f}" text-anchor="middle" font-weight="700" font-size="14">B</text>')
    # oplossing: kracht in A
    fx, fy = kracht_richting(q, orient, plus)
    Lf = 34 if abs(q) == 1 else 46
    sx, sy = ax + fx * 11, ay + fy * 11
    o.append(f'<g class="opl">{pijl(sx, sy, sx + fx*Lf, sy + fy*Lf, KR, 1.6)}'
             f'<text x="{sx + fx*Lf + (8 if fx>=0 else -16) + (10 if fx==0 else 0):.1f}" y="{sy + fy*Lf + (4 if fy==0 else (12 if fy>0 else -2)):.1f}" font-weight="700" font-size="13" fill="{KR}">F</text>'
             f'<line x1="{sx + fx*Lf + (8 if fx>=0 else -16) + (10 if fx==0 else 0):.1f}" y1="{sy + fy*Lf + (4 if fy==0 else (12 if fy>0 else -2)) - 12:.1f}" x2="{sx + fx*Lf + (17 if fx>=0 else -7) + (10 if fx==0 else 0):.1f}" y2="{sy + fy*Lf + (4 if fy==0 else (12 if fy>0 else -2)) - 12:.1f}" stroke="{KR}" stroke-width="1"/></g>')
    o.append('</svg>')
    return ''.join(o)


def antwoorden(q, A, B):
    """Teken van arbeid, Ekin, Epot, potentiaal, spanning. V ~ s."""
    dV = B[0] - A[0]                  # V_B − V_A (in eenheden U)
    W = -q * dV                       # W = Q·U_AB = Q·(V_A − V_B)
    sg = lambda x: 0 if abs(x) < 1e-9 else (1 if x > 0 else -1)
    w = sg(W)
    return {
        'arbeid':     {1: 'positief', -1: 'negatief', 0: 'nul'}[w],
        'ekin':       {1: 'neemt toe', -1: 'neemt af', 0: 'blijft gelijk'}[w],
        'epot':       {1: 'neemt af', -1: 'neemt toe', 0: 'blijft gelijk'}[w],
        'potentiaal': {1: 'neemt toe', -1: 'neemt af', 0: 'blijft gelijk'}[sg(dV)],
        'spanning':   {1: 'positief', -1: 'negatief', 0: 'nul'}[sg(-dV)],
    }


UITLEG = [
    'Het proton wordt naar de − plaat geduwd en beweegt ook naar de − plaat: mee met de kracht, dus positieve arbeid. De potentiële energie wordt kinetische energie.',
    'Het elektron wordt naar de + plaat getrokken en beweegt naar de + plaat: mee met de kracht, dus positieve arbeid. De potentiaal neemt toe, maar omdat de lading negatief is, neemt de potentiële energie af (E<sub>pot</sub> = Q · V).',
    'Het proton wordt naar de − plaat geduwd, maar beweegt naar de + plaat: tegen de kracht in, dus negatieve arbeid. Dat kan alleen als het proton al snelheid had (weggeschoten). Kinetische energie wordt potentiële energie.',
    'Het elektron beweegt evenwijdig met de platen, loodrecht op de kracht. A en B liggen op hetzelfde equipotentiaalvlak: de arbeid is nul en de energie verandert niet.',
]

VRAGEN = [
    ('arbeid', 'De arbeid van het elektrisch veld is', ['positief', 'negatief', 'nul']),
    ('ekin', 'De kinetische energie', ['neemt toe', 'neemt af', 'blijft gelijk']),
    ('epot', 'De potentiële elektrische energie', ['neemt toe', 'neemt af', 'blijft gelijk']),
    ('potentiaal', 'De potentiaal van A naar B', ['neemt toe', 'neemt af', 'blijft gelijk']),
    ('spanning', 'Het potentiaalverschil tussen A en B is', ['positief', 'negatief', 'nul']),
]


def situatie(i, sit):
    q, naam, orient, plus, A, B = sit
    ant = antwoorden(q, A, B)
    rijen = ''.join(
        f'<tr><td>{tekst}</td><td>' + ''.join(
            f'<span class="keuze{" juist" if ant[k]==opt else ""}">{opt}</span>' for opt in opties) + '</td></tr>'
        for k, tekst, opties in VRAGEN)
    return (f'<div class="sit"><div class="sitkop"><b>{i}</b> Een {naam} beweegt van A naar B.</div>'
            f'{figuur(q, orient, plus, A, B)}'
            f'<p class="opdr">Teken de elektrische kracht op het {naam} in A. Omcirkel daarna.</p>'
            f'<table class="kz">{rijen}</table>'
            f'<p class="waarom"><b>Leg uit</b> waarom de arbeid positief, negatief of nul is.</p><div class="lijnen"></div>'
            f'<p class="oplossing">{UITLEG[i-1]}</p></div>')


KEN = '''<div class="ken"><div class="kop">Ken dit</div>
<p>Arbeid van het veld: <b>W = Q · U<sub>AB</sub> = −ΔE<sub>pot</sub> = ΔE<sub>kin</sub></b><br>
Potentiaalverschil: <b>U<sub>AB</sub> = V<sub>A</sub> − V<sub>B</sub></b>. Dicht bij de + plaat is de potentiaal hoog, op de − plaat is ze 0 V.</p></div>'''

STAPPEN = '''<div class="denk"><div class="kop">Denkstappen</div><ol>
<li><b>Kracht.</b> Een positieve lading wordt naar de − plaat geduwd, een negatieve lading naar de + plaat.</li>
<li><b>Arbeid.</b> Beweegt de lading mee met de kracht? Dan is de arbeid positief. Ertegenin? Dan negatief. Loodrecht erop (evenwijdig met de platen)? Dan nul.</li>
<li><b>Energie.</b> Positieve arbeid: de kinetische energie neemt toe, de potentiële energie neemt evenveel af. Negatieve arbeid: omgekeerd.</li>
<li><b>Potentiaal.</b> Gaat B dichter naar de + plaat? Dan neemt de potentiaal toe. Kijk alleen naar de plaats, niet naar de lading.</li>
<li><b>Potentiaalverschil.</b> U<sub>AB</sub> = V<sub>A</sub> − V<sub>B</sub>: positief als A een hogere potentiaal heeft dan B.</li></ol></div>'''

LETOP = '''<div class="letop"><div class="kop">Let op</div>
<p>Bij een <b>elektron</b> loopt de potentiaal en de potentiële energie niet gelijk: gaat het elektron naar een hogere potentiaal, dan <b>daalt</b> zijn potentiële energie.</p></div>'''

OPGAVEN = '''<h2>Deel 2 · Rekenen</h2>
<div class="opg"><div class="opgkop"><b>Opgave 1</b></div>
<p>Tussen twee evenwijdige platen op 3,0 cm van elkaar staat een spanning van 600 V. Punt A ligt op 2,0 cm van de negatieve plaat, punt B op 0,50 cm van de negatieve plaat.</p>
<ol type="a">
<li>Bereken de elektrische veldsterkte tussen de platen.</li>
<li>Bereken de potentiaal in A en in B.</li>
<li>Bereken het potentiaalverschil tussen A en B.</li>
<li>Een proton beweegt van A naar B. Bereken de arbeid van het elektrisch veld in eV en in J. Neemt de kinetische energie toe of af?</li>
<li>Een elektron beweegt van A naar B. Hoeveel kinetische energie moet het in A minstens hebben om B te bereiken?</li>
</ol><div class="schrijf"></div>
<div class="oplossing"><div class="kop">Oplossing</div><ol type="a">
<li>E = U / D = 600 V / 0,030 m = 2,0 · 10<sup>4</sup> N/C</li>
<li>V<sub>A</sub> = E · d<sub>A</sub> = 2,0 · 10<sup>4</sup> N/C · 0,020 m = 400 V; V<sub>B</sub> = 2,0 · 10<sup>4</sup> N/C · 0,0050 m = 100 V</li>
<li>U<sub>AB</sub> = V<sub>A</sub> − V<sub>B</sub> = 400 V − 100 V = +300 V</li>
<li>W = Q · U<sub>AB</sub> = (+e) · (+300 V) = +300 eV = 300 · 1,602 · 10<sup>−19</sup> J = 4,8 · 10<sup>−17</sup> J. Positieve arbeid: de kinetische energie neemt toe met 300 eV (het proton beweegt mee met de kracht, naar de − plaat).</li>
<li>W = (−e) · (+300 V) = −300 eV. Het veld neemt 300 eV kinetische energie af. Het elektron moet in A dus minstens 300 eV kinetische energie hebben.</li></ol></div></div>

<div class="opg"><div class="opgkop"><b>Opgave 2</b></div>
<p>Een elektron start in rust op de negatieve plaat (punt A). De spanning tussen de platen is 250 V.</p>
<ol type="a">
<li>Naar welke plaat beweegt het elektron? Leg uit.</li>
<li>Het elektron komt aan op de andere plaat (punt B). Bereken het potentiaalverschil tussen A en B.</li>
<li>Bereken de arbeid van het elektrisch veld in eV en in J.</li>
<li>Bereken de snelheid van het elektron in B. (massa van een elektron: 9,11 · 10<sup>−31</sup> kg)</li>
</ol><div class="schrijf"></div>
<div class="oplossing"><div class="kop">Oplossing</div><ol type="a">
<li>Naar de positieve plaat: een negatieve lading wordt tegen de veldlijnen in geduwd.</li>
<li>U<sub>AB</sub> = V<sub>A</sub> − V<sub>B</sub> = 0 V − 250 V = −250 V</li>
<li>W = Q · U<sub>AB</sub> = (−e) · (−250 V) = +250 eV = 4,0 · 10<sup>−17</sup> J</li>
<li>Het start in rust, dus E<sub>kin,B</sub> = W = 4,0 · 10<sup>−17</sup> J. v = √(2 · E<sub>kin</sub> / m) = √(2 · 4,0 · 10<sup>−17</sup> J / 9,11 · 10<sup>−31</sup> kg) = 9,4 · 10<sup>6</sup> m/s</li></ol></div></div>

<div class="samen"><div class="uitdaging"><div class="kop">Zo pak je een uitdaging aan</div><ol>
<li>Teken de platen, de lading en de kracht. Beweegt de lading mee met de kracht of ertegenin?</li>
<li>Schrijf de energie op in het begin en op het einde. De totale energie blijft gelijk: wat er aan kinetische energie verdwijnt, komt erbij als potentiële energie.</li>
<li>Reken in eV: bij een lading e is de energie in eV gelijk aan het getal van de spanning in V.</li></ol></div>
<div class="opg"><div class="opgkop"><b>Opgave 3 · Uitdaging</b></div>
<p>Tussen twee platen op 4,0 cm van elkaar staat een spanning van 400 V. Een proton wordt vanaf de negatieve plaat weggeschoten naar de positieve plaat, met een kinetische energie van 150 eV.</p>
<ol type="a">
<li>Bereikt het proton de positieve plaat? Leg uit met energie.</li>
<li>Op welke afstand van de negatieve plaat keert het proton om?</li>
<li>Met welke kinetische energie komt het proton terug aan op de negatieve plaat?</li>
</ol><div class="schrijf"></div>
<div class="oplossing"><div class="kop">Oplossing</div><ol type="a">
<li>Nee. Om de positieve plaat te bereiken, moet de potentiële energie stijgen van 0 eV naar (+e) · 400 V = 400 eV. Het proton heeft maar 150 eV kinetische energie.</li>
<li>Het keert om waar alle kinetische energie potentiële energie is geworden: E<sub>pot</sub> = 150 eV, dus V = 150 V. Met E = U / D = 400 V / 0,040 m = 1,0 · 10<sup>4</sup> N/C: d = V / E = 150 V / 1,0 · 10<sup>4</sup> N/C = 0,015 m = 1,5 cm.</li>
<li>Terug op de negatieve plaat is de potentiële energie weer 0 eV, dus E<sub>kin</sub> = 150 eV (behoud van energie).</li></ol></div></div></div>'''

CSS = '''
:root{--ink:#1D2A36;--muted:#51606E;--line:#CBD5DE}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;background:#EEF2F5;color:var(--ink);font-family:"Atkinson Hyperlegible",system-ui,Arial,sans-serif;font-size:16px;line-height:1.45}
main{max-width:52rem;margin:0 auto;padding:1.5rem 1rem 3rem;background:#fff}
.terug{font-size:.9rem;color:var(--muted);text-decoration:none}
h1{font-size:1.7rem;margin:.4rem 0 .1rem}
.sub{color:var(--muted);margin:0 0 .8rem}
.naam{display:flex;gap:2rem;margin:.4rem 0 1rem;font-size:.95rem}.naam span{flex:1;border-bottom:1px solid var(--ink);padding-bottom:2px}
h2{font-size:1.25rem;margin:1.4rem 0 .5rem;border-bottom:2px solid #2F6FB0;padding-bottom:2px}
.ken,.denk,.letop,.uitdaging,.oplossing{border-radius:10px;padding:8px 14px;margin:8px 0 12px}
.ken{background:#E8F5EC;border-left:5px solid #2E8B57}.ken .kop{color:#1F6B41}
.letop{background:#FFF1E0;border-left:5px solid #D97706}.letop .kop{color:#9A4F00}
.denk,.uitdaging{background:#EEF4FB;border-left:5px solid #2F6FB0}.denk .kop,.uitdaging .kop{color:#1F4F80}
.kop{font-weight:700;margin-bottom:2px}
.ken p,.letop p{margin:2px 0}.denk ol,.uitdaging ol{margin:4px 0;padding-left:1.3rem}
.raster{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.sit{border:1px solid var(--line);border-radius:10px;padding:8px 10px;break-inside:avoid}
.sitkop{margin-bottom:4px}.sitkop b{display:inline-block;background:#2F6FB0;color:#fff;border-radius:50%;width:1.5em;height:1.5em;text-align:center;margin-right:4px}
.fig{display:block;width:100%;height:auto;max-width:300px;margin:0 auto}
.opdr{font-size:.85rem;margin:2px 0 4px;color:var(--muted)}
table.kz{width:100%;border-collapse:collapse;font-size:.82rem}
table.kz td{padding:3px 2px;border-top:1px dashed var(--line);vertical-align:middle}
table.kz td:first-child{width:42%}
.keuze{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:0 7px;margin:1px 2px;white-space:nowrap}
.waarom{font-size:.85rem;margin:6px 0 0}.lijnen{height:3.6rem;background-image:linear-gradient(#d7dee6 1px,transparent 1px);background-size:100% 1.8rem}
.toon .lijnen{display:none}.sit .oplossing{font-size:.85rem;margin:4px 0 0}
.samen{break-inside:avoid}
.opg{border:1px solid var(--line);border-radius:10px;padding:8px 14px;margin:10px 0;break-inside:avoid}
.opg ol{margin:4px 0;padding-left:1.4rem}.opg p{margin:4px 0}
.schrijf{height:9rem;background-image:linear-gradient(#d7dee6 1px,transparent 1px);background-size:100% 1.8rem;margin-top:6px}
.opl,.oplossing{display:none}
.toon .opl{display:inline}.toon .oplossing{display:block;background:#F5F3FF;border-left:5px solid #7c3aed}.toon .oplossing .kop{color:#6d28d9}
.toon .keuze.juist{background:#DCFCE7;border-color:#16a34a;font-weight:700}
.toon .schrijf{display:none}
.knop{font:inherit;font-size:.9rem;border:1px solid var(--line);background:#fff;border-radius:8px;padding:4px 12px;cursor:pointer}
.balk{display:flex;gap:8px;justify-content:flex-end;margin-top:-1.2rem}
.leerkracht{background:#7c3aed;color:#fff;text-align:center;font-size:.85rem;padding:4px;display:none}.toon .leerkracht{display:block}
.credit{margin-top:2rem;font-size:.8rem;color:var(--muted)}
@media (max-width:640px){.raster{grid-template-columns:1fr}}
@media print{body{background:#fff;font-size:11pt}.raster{display:block;orphans:1;widows:1}.sit{display:inline-block;width:49.3%;vertical-align:top;margin-bottom:6px}main{padding:0;max-width:none}.terug,.balk{display:none}
 .raster{gap:6px}.sit{padding:4px 8px;font-size:10pt}.fig{max-width:175px}table.kz{font-size:8pt}table.kz td{padding:1px 2px}.keuze{padding:0 5px;margin:0 1px}.opdr{margin:0 0 2px}.ken,.denk,.letop{font-size:10pt;padding:4px 10px;margin:4px 0 6px}.lijnen{height:2.8rem;background-size:100% 1.4rem}h1{font-size:18pt}h2{break-after:avoid}.intro{display:grid;grid-template-columns:1fr 1.3fr;gap:8px}.intro .denk{margin-top:4px}.naam{margin:2px 0 6px}h2{margin:.6rem 0 .3rem}}
@page{size:A4;margin:12mm}
'''


def bouw():
    sits = ''.join(situatie(i + 1, s) for i, s in enumerate(SITUATIES))
    html = f'''<!DOCTYPE html>
<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Werkblad · Arbeid, energie en potentiaal</title>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="leerkracht">Leerkrachtversie: oplossingen zichtbaar</div>
<main>
<a class="terug" href="index.html">← Alle tools</a>
<h1>Werkblad · Arbeid, energie en potentiaal</h1>
<p class="sub">5Wet · Thema 1 · Hoofdstuk 4 Potentiaal · Homogeen elektrisch veld</p>
<div class="balk"><a class="knop" href="potentiaal.html">Naar de tool</a><button class="knop" onclick="window.print()">Afdrukken</button></div>
<div class="naam"><span>Naam:</span><span>Klas:</span><span>Datum:</span></div>
<div class="intro"><div>{KEN}
{LETOP}</div>{STAPPEN}</div>
<h2>Deel 1 · Redeneren</h2>
<p>Bij elke figuur beweegt een lading van A naar B (stippellijn). De dunne lijnen zijn veldlijnen. Gebruik de denkstappen.</p>
<div class="raster">{sits}</div>
<div class="deel2">{OPGAVEN}</div>
<p class="credit">Vakgroep wetenschappen · Maria Assumpta Lyceum · ontwikkeld met hulp van AI · CC BY-NC-SA 4.0</p>
</main>
<script>
/* VRIJGAVE: zet op true om de oplossingen voor iedereen te tonen */
const OPLOSSINGEN_VRIJ = false;
if (OPLOSSINGEN_VRIJ || new URLSearchParams(location.search).has('leerkracht')) document.body.classList.add('toon');
</script>
</body></html>'''
    (ROOT / 'werkblad-potentiaal.html').write_text(html, encoding='utf-8')
    print('werkblad-potentiaal.html gemaakt')


if __name__ == '__main__':
    bouw()
