import math, subprocess, os

OUT = "/home/claude/work/fig"
os.makedirs(OUT, exist_ok=True)
FONT = "Carlito, Calibri, sans-serif"

def save(name, svg, width_px):
    p = f"{OUT}/{name}.svg"
    open(p, "w").write(svg)
    subprocess.run(["rsvg-convert", "-w", str(width_px), "-o", f"{OUT}/{name}.png", p], check=True)

def arrowhead(x, y, dx, dy, color, size=26):
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    px, py = -uy, ux
    bx, by = x - ux * size, y - uy * size
    return (f'<polygon points="{x:.1f},{y:.1f} {bx+px*size*0.42:.1f},{by+py*size*0.42:.1f} '
            f'{bx-px*size*0.42:.1f},{by-py*size*0.42:.1f}" fill="{color}"/>')

# ------------------------------------------------------------------
# 1. Schijnbare verhoging – based on the teacher's drawing (no circle)
# ------------------------------------------------------------------
N = 1.33
SURF = 289
V = (182, 815)
HITS = {"blue": 582, "red": 682}
COL = {"blue": "#2233dd", "red": "#dd1a1a"}
TOP = 40

refr = {}
for k, hx in HITS.items():
    dx, dy = hx - V[0], SURF - V[1]          # dy negative (upwards)
    i = math.atan2(dx, -dy)                   # angle with the normal in water
    r = math.asin(N * math.sin(i))            # angle with the normal in air
    refr[k] = (i, r)
# virtual point: intersection of the back-extended refracted rays
tb, tr = math.tan(refr["blue"][1]), math.tan(refr["red"][1])
depth = (HITS["red"] - HITS["blue"]) / (tr - tb)
VV = (HITS["blue"] - depth * tb, SURF + depth)
print("i (deg):", {k: round(math.degrees(v[0]), 1) for k, v in refr.items()})
print("r (deg):", {k: round(math.degrees(v[1]), 1) for k, v in refr.items()})
print("V' =", VV, " real depth", V[1] - SURF, " apparent depth", depth)

def eye(cx, cy, angle_deg, s=1.0):
    # simple eye looking in direction angle_deg (svg degrees)
    return (f'<g transform="translate({cx},{cy}) rotate({angle_deg}) scale({s})">'
            f'<path d="M-46,0 Q0,-34 46,0 Q0,34 -46,0 Z" fill="#fff" stroke="#222" stroke-width="4"/>'
            f'<circle cx="14" cy="0" r="15" fill="#3b6ea8"/><circle cx="18" cy="0" r="7" fill="#111"/></g>')

def scene(step, labels=True):
    s = []
    s.append(f'<rect x="0" y="{TOP}" width="1259" height="{SURF-TOP}" fill="#ffffff"/>')
    s.append(f'<rect x="0" y="{SURF}" width="1259" height="{939-SURF}" fill="#dce8f8"/>')
    s.append(f'<line x1="0" y1="{SURF}" x2="1259" y2="{SURF}" stroke="#9db8d6" stroke-width="3"/>')
    s.append('<rect x="182" y="822" width="322" height="48" fill="#2ea3c0" stroke="#1d6e86" stroke-width="2"/>')
    if labels:
        s.append(f'<rect x="1100" y="{SURF-66}" width="140" height="50" fill="#e8f6fb"/>'
                 f'<text x="1170" y="{SURF-31}" font-family="{FONT}" font-size="40" font-weight="bold" text-anchor="middle">lucht</text>')
        s.append(f'<rect x="1100" y="{SURF+16}" width="140" height="50" fill="#fff6c8"/>'
                 f'<text x="1170" y="{SURF+52}" font-family="{FONT}" font-size="40" font-weight="bold" text-anchor="middle">water</text>')
    # rays in water (always)
    for k, hx in HITS.items():
        s.append(f'<line x1="{V[0]}" y1="{V[1]}" x2="{hx}" y2="{SURF}" stroke="{COL[k]}" stroke-width="5"/>')
        mx, my = V[0] + 0.5 * (hx - V[0]), V[1] + 0.5 * (SURF - V[1])
        s.append(arrowhead(mx, my, hx - V[0], SURF - V[1], COL[k], 30))
    s.append(f'<circle cx="{V[0]}" cy="{V[1]}" r="7" fill="#000"/>')
    s.append(f'<text x="{V[0]-52}" y="{V[1]+14}" font-family="{FONT}" font-size="56" font-weight="bold">V</text>')
    if step >= 1:   # normals
        for hx in HITS.values():
            s.append(f'<line x1="{hx}" y1="{SURF-190}" x2="{hx}" y2="{SURF+95}" stroke="#222" '
                     f'stroke-width="3" stroke-dasharray="14,10"/>')
        s.append(f'<text x="{HITS["red"]+10}" y="{SURF-160}" font-family="{FONT}" font-size="46" font-style="italic">n</text>')
        s.append(f'<text x="{HITS["blue"]-30}" y="{SURF-160}" font-family="{FONT}" font-size="46" font-style="italic">n</text>')
    if step >= 2:   # refracted rays in air
        for k, hx in HITS.items():
            r = refr[k][1]
            L = (SURF - TOP - 20) / math.cos(r)
            ex, ey = hx + L * math.sin(r), SURF - L * math.cos(r)
            ex = min(ex, 1240)
            L2 = (ex - hx) / math.sin(r)
            ey = SURF - L2 * math.cos(r)
            s.append(f'<line x1="{hx}" y1="{SURF}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{COL[k]}" stroke-width="5"/>')
            mx, my = hx + 0.55 * (ex - hx), SURF + 0.55 * (ey - SURF)
            s.append(arrowhead(mx, my, ex - hx, ey - SURF, COL[k], 30))
        s.append(f'<text x="1120" y="125" font-family="{FONT}" font-size="40" font-style="italic" text-anchor="middle">naar het oog</text>')
    if step >= 3:   # back-extensions
        for k, hx in HITS.items():
            s.append(f'<line x1="{hx}" y1="{SURF}" x2="{VV[0]:.1f}" y2="{VV[1]:.1f}" stroke="{COL[k]}" '
                     f'stroke-width="4" stroke-dasharray="12,9"/>')
        s.append(f'<circle cx="{VV[0]:.1f}" cy="{VV[1]:.1f}" r="8" fill="#000"/>')
        s.append(f'<text x="{VV[0]-78:.1f}" y="{VV[1]+12:.1f}" font-family="{FONT}" font-size="56" font-weight="bold">V\'</text>')
    if step >= 4:   # apparent object
        s.append(f'<rect x="{VV[0]:.1f}" y="{VV[1]+7:.1f}" width="322" height="48" fill="#2ea3c0" fill-opacity="0.35" '
                 f'stroke="#1d6e86" stroke-width="3" stroke-dasharray="12,8"/>')
        s.append(f'<text x="{VV[0]+161:.1f}" y="{VV[1]+105:.1f}" font-family="{FONT}" font-size="46" '
                 f'text-anchor="middle" font-style="italic">schijnbaar voorwerp</text>')
        s.append(f'<text x="343" y="858" font-family="{FONT}" font-size="34" text-anchor="middle" fill="#fff" '
                 f'font-style="italic">echt voorwerp</text>')
    return s

def badge(n):
    return (f'<circle cx="60" cy="{TOP+56}" r="40" fill="#222"/>'
            f'<text x="60" y="{TOP+72}" font-family="{FONT}" font-size="48" font-weight="bold" fill="#fff" text-anchor="middle">{n}</text>')

for st in range(0, 5):
    body = "".join(scene(st)) + (badge(st) if st else "")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {TOP} 1259 {939-TOP}">'
           f'{body}<rect x="0" y="{TOP}" width="1259" height="{939-TOP}" fill="none" stroke="#888" stroke-width="3"/></svg>')
    save(f"verhoging_{st}", svg, 1259)

# ------------------------------------------------------------------
# 2. Path of light through one raindrop
# ------------------------------------------------------------------
def refract(d, nrm, n1, n2):
    # d incoming unit dir, nrm unit normal pointing against d
    cosi = -(d[0] * nrm[0] + d[1] * nrm[1])
    eta = n1 / n2
    k = 1 - eta * eta * (1 - cosi * cosi)
    c = eta * cosi - math.sqrt(k)
    return (eta * d[0] + c * nrm[0], eta * d[1] + c * nrm[1])

def reflect(d, nrm):
    dot = d[0] * nrm[0] + d[1] * nrm[1]
    return (d[0] - 2 * dot * nrm[0], d[1] - 2 * dot * nrm[1])

def hit_circle(p, d, R):
    # second intersection of ray p + t d with circle centred at origin (p on circle)
    t = -2 * (p[0] * d[0] + p[1] * d[1])
    return (p[0] + t * d[0], p[1] + t * d[1])

# math coords (y up), centre (0,0)
R = 300
i_deg = 59.4
P = (-R * math.cos(math.radians(i_deg)), R * math.sin(math.radians(i_deg)))
# drawn with an exaggerated difference in refractive index so the split is visible
NS = {"rood": (1.33, "#e01b1b"), "violet": (1.37, "#7a2bd6")}
paths = {}
for name, (n, c) in NS.items():
    d0 = (1.0, 0.0)
    nrm = (P[0] / R, P[1] / R)
    d1 = refract(d0, nrm, 1.0, n)
    Q = hit_circle(P, d1, R)
    d2 = reflect(d1, (-Q[0] / R, -Q[1] / R))
    S = hit_circle(Q, d2, R)
    d3 = refract(d2, (-S[0] / R, -S[1] / R), n, 1.0)
    dev_from_back = math.degrees(math.acos(-d3[0]))   # angle with direction back toward the sun
    ang_in = math.degrees(math.acos(abs(d1[0] * Q[0] / R + d1[1] * Q[1] / R)))
    paths[name] = (Q, S, d3, c)
    print(name, "angle exit vs incoming (deg):", round(dev_from_back, 1), " incidence at back:", round(ang_in, 1))

# real-world check with n = 1.333
n = 1.333
r = math.asin(math.sin(math.radians(i_deg)) / n)
print("real: incidence at back =", round(math.degrees(r), 1), " grenshoek =",
      round(math.degrees(math.asin(1 / n)), 1), " rainbow angle =",
      round(4 * math.degrees(r) - 2 * i_deg, 1))

CX, CY = 640, 380
def T(p):  # math -> svg
    return (CX + p[0], CY - p[1])

s = []
s.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="#e3f0fc" stroke="#4a7fb5" stroke-width="5"/>')
Ps = T(P)
# incoming white light (drawn as a thick light-grey/yellow ray)
s.append(f'<line x1="40" y1="{Ps[1]:.1f}" x2="{Ps[0]:.1f}" y2="{Ps[1]:.1f}" stroke="#f2b705" stroke-width="10"/>')
s.append(arrowhead(250, Ps[1], 1, 0, "#f2b705", 34))
s.append(f'<text x="40" y="{Ps[1]-24:.1f}" font-family="{FONT}" font-size="34" font-weight="bold">wit zonlicht</text>')
# normals (dashed, through the centre)
def normal_line(p, ext_out=110, ext_in=150):
    ux, uy = p[0] / R, p[1] / R
    a = T((p[0] + ux * ext_out, p[1] + uy * ext_out)); b = T((p[0] - ux * ext_in, p[1] - uy * ext_in))
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#333" stroke-width="3" stroke-dasharray="12,9"/>'
s.append(normal_line(P))
for name, (Q, S, d3, c) in paths.items():
    a, b, e = T(P), T(Q), T(S)
    s.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{c}" stroke-width="5"/>')
    s.append(f'<line x1="{b[0]:.1f}" y1="{b[1]:.1f}" x2="{e[0]:.1f}" y2="{e[1]:.1f}" stroke="{c}" stroke-width="5"/>')
    end = T((S[0] + d3[0] * 300, S[1] + d3[1] * 300))
    s.append(f'<line x1="{e[0]:.1f}" y1="{e[1]:.1f}" x2="{end[0]:.1f}" y2="{end[1]:.1f}" stroke="{c}" stroke-width="5"/>')
    mid = T((S[0] + d3[0] * 220, S[1] + d3[1] * 220))
    s.append(arrowhead(mid[0], mid[1], d3[0], -d3[1], c, 28))
    _off = -45 if name == "violet" else 40
    s.append(f'<text x="{end[0]+_off:.1f}" y="{end[1]+30:.1f}" font-family="{FONT}" font-size="32" font-weight="bold" fill="{c}" text-anchor="middle">{name}</text>')
Qr = paths["rood"][0]; Sr = paths["rood"][1]
# part of the light leaves the drop at the back (no total reflection)
_d1 = refract((1.0, 0.0), (P[0]/R, P[1]/R), 1.0, 1.33)
_dt = refract(_d1, (-Qr[0]/R, -Qr[1]/R), 1.33, 1.0)
_a = T(Qr); _b = T((Qr[0] + _dt[0]*170, Qr[1] + _dt[1]*170))
s.append(f'<line x1="{_a[0]:.1f}" y1="{_a[1]:.1f}" x2="{_b[0]:.1f}" y2="{_b[1]:.1f}" stroke="#e01b1b" stroke-width="3" stroke-dasharray="6,6" opacity="0.7"/>')
s.append(f'<text x="{_b[0]-10:.1f}" y="{_b[1]+40:.1f}" font-family="{FONT}" font-size="26" font-style="italic" text-anchor="middle">een deel gaat door</text>')

s.append(normal_line(Qr, 90, 120))
s.append(normal_line(Sr, 110, 140))

def num(x, y, k):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="27" fill="#222"/>'
            f'<text x="{x:.1f}" y="{y+11:.1f}" font-family="{FONT}" font-size="34" font-weight="bold" fill="#fff" text-anchor="middle">{k}</text>')
a = T(P); s.append(num(a[0] - 40, a[1] - 70, 1))
b = T(Qr); s.append(num(b[0] + 70, b[1] - 10, 2))
e = T(Sr); s.append(num(e[0] + 60, e[1] + 35, 3))
s.append(f'<text x="590" y="985" font-family="{FONT}" font-size="30" text-anchor="middle" font-style="italic">'
         f'regendruppel (sterk vergroot) – het kleurverschil is overdreven getekend</text>')
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 1000"><rect width="1180" height="1000" fill="#fff"/>{"".join(s)}</svg>'
save("druppel", svg, 1180)

# ------------------------------------------------------------------
# 3. Everyone sees their own rainbow
# ------------------------------------------------------------------
W, H = 1500, 820
GROUND = 700
sun_dir_deg = 14                     # sunlight travels to the right and 14° downward
sd = (math.cos(math.radians(sun_dir_deg)), math.sin(math.radians(sun_dir_deg)))  # svg coords (y down)
s = []
s.append(f'<rect width="{W}" height="{H}" fill="#fff"/>')
s.append(f'<rect x="0" y="{GROUND}" width="{W}" height="{H-GROUND}" fill="#cfe3b4"/>')
# rain zone
s.append(f'<rect x="760" y="40" width="720" height="{GROUND-40}" fill="#e8eef6"/>')
for k in range(140):
    x = 775 + (k * 97) % 700; y = 60 + (k * 53) % (GROUND - 80)
    s.append(f'<line x1="{x}" y1="{y}" x2="{x-4}" y2="{y+14}" stroke="#a9bfd8" stroke-width="2"/>')
s.append(f'<text x="1460" y="80" font-family="{FONT}" font-size="32" text-anchor="end" font-style="italic">regendruppels</text>')
# sun
s.append(f'<circle cx="70" cy="90" r="46" fill="#ffd21f" stroke="#e8a300" stroke-width="4"/>')
s.append(f'<text x="130" y="60" font-family="{FONT}" font-size="34" font-weight="bold">zon</text>')

def person(x, label, col):
    eyey = GROUND - 150
    g = []
    g.append(f'<circle cx="{x}" cy="{eyey}" r="22" fill="{col}"/>')
    g.append(f'<line x1="{x}" y1="{eyey+22}" x2="{x}" y2="{GROUND-60}" stroke="{col}" stroke-width="10"/>')
    g.append(f'<line x1="{x}" y1="{GROUND-60}" x2="{x-24}" y2="{GROUND}" stroke="{col}" stroke-width="10"/>')
    g.append(f'<line x1="{x}" y1="{GROUND-60}" x2="{x+24}" y2="{GROUND}" stroke="{col}" stroke-width="10"/>')
    g.append(f'<line x1="{x}" y1="{eyey+50}" x2="{x+30}" y2="{eyey+95}" stroke="{col}" stroke-width="9"/>')
    g.append(f'<text x="{x}" y="{GROUND+48}" font-family="{FONT}" font-size="32" font-weight="bold" text-anchor="middle" fill="{col}">{label}</text>')
    return g, (x + 6, eyey)

def view_lines(eye, col, dist):
    g = []
    # line eye -> antisolar direction (parallel to the sunlight)
    ax, ay = eye[0] + sd[0] * 900, eye[1] + sd[1] * 900
    g.append(f'<line x1="{eye[0]}" y1="{eye[1]}" x2="{ax:.1f}" y2="{ay:.1f}" stroke="{col}" stroke-width="2.5" stroke-dasharray="10,8"/>')
    drops = {}
    for ang, c in ((42, "#e01b1b"), (40, "#7a2bd6")):
        a = math.radians(sun_dir_deg - ang)        # rotate upward
        dx, dy = math.cos(a), math.sin(a)
        px, py = eye[0] + dx * dist, eye[1] + dy * dist
        g.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{eye[0]}" y2="{eye[1]}" stroke="{c}" stroke-width="4"/>')
        g.append(arrowhead(eye[0] + dx * dist * 0.45, eye[1] + dy * dist * 0.45, -dx, -dy, c, 22))
        # incoming sunlight into that drop
        g.append(f'<line x1="{px - sd[0]*120:.1f}" y1="{py - sd[1]*120:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke="#f2b705" stroke-width="4"/>')
        g.append(arrowhead(px - sd[0] * 40, py - sd[1] * 40, sd[0], sd[1], "#f2b705", 18))
        g.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="13" fill="#bfe0ff" stroke="{c}" stroke-width="4"/>')
        drops[ang] = (px, py)
    return g, drops

p1, eA = person(260, "jij", "#222")
p2, eB = person(520, "je buur", "#2b7a3d")
s += p1 + p2
gA, dA = view_lines(eA, "#222", 830)
gB, dB = view_lines(eB, "#2b7a3d", 830)
s += gA + gB
# angle arc for observer A (between antisolar line and red line)
rA = 150
a0 = math.radians(sun_dir_deg); a1 = math.radians(sun_dir_deg - 42)
x0, y0 = eA[0] + rA * math.cos(a0), eA[1] + rA * math.sin(a0)
x1, y1 = eA[0] + rA * math.cos(a1), eA[1] + rA * math.sin(a1)
s.append(f'<path d="M{x0:.1f},{y0:.1f} A{rA},{rA} 0 0 0 {x1:.1f},{y1:.1f}" fill="none" stroke="#e01b1b" stroke-width="3"/>')
am = math.radians(sun_dir_deg - 21)
s.append(f'<text x="{eA[0] + (rA+12)*math.cos(am):.1f}" y="{eA[1] + (rA+12)*math.sin(am)+10:.1f}" font-family="{FONT}" font-size="34" font-weight="bold" fill="#e01b1b">42°</text>')
# sunlight arrows across the scene
for y in (150, 260):
    s.append(f'<line x1="140" y1="{y}" x2="{140+sd[0]*330:.1f}" y2="{y+sd[1]*330:.1f}" stroke="#f2b705" stroke-width="5"/>')
    s.append(arrowhead(140 + sd[0] * 330, y + sd[1] * 330, sd[0], sd[1], "#f2b705", 24))
s.append(f'<text x="160" y="{330}" font-family="{FONT}" font-size="30" font-style="italic">zonlicht</text>')
# label antisolar lines
tx, ty = eA[0]+sd[0]*620, eA[1]+sd[1]*620-12
s.append(f'<text x="{tx:.1f}" y="{ty:.1f}" transform="rotate({sun_dir_deg} {tx:.1f} {ty:.1f})" font-family="{FONT}" font-size="26" font-style="italic">richting van je schaduw</text>')
# labels for drops
s.append(f'<text x="{dA[42][0]-18:.1f}" y="{dA[42][1]-26:.1f}" font-family="{FONT}" font-size="28" text-anchor="end">druppels voor jou</text>')
s.append(f'<text x="{dB[40][0]+30:.1f}" y="{dB[40][1]+45:.1f}" font-family="{FONT}" font-size="28" fill="#2b7a3d" text-anchor="middle">druppels voor je buur</text>')
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><style>text{{paint-order:stroke;stroke:#fff;stroke-width:7px;stroke-linejoin:round}}</style>{"".join(s)}<rect width="{W}" height="{H}" fill="none" stroke="#888" stroke-width="3"/></svg>'
save("eigen_regenboog", svg, 1500)

# ------------------------------------------------------------------
# 4. Garden sprinkler experiment
# ------------------------------------------------------------------
W, H = 1400, 720
GROUND = 600
s = [f'<rect width="{W}" height="{H}" fill="#fff"/>',
     f'<rect x="0" y="{GROUND}" width="{W}" height="{H-GROUND}" fill="#cfe3b4"/>']
s.append(f'<circle cx="90" cy="90" r="50" fill="#ffd21f" stroke="#e8a300" stroke-width="4"/>')
s.append(f'<text x="155" y="70" font-family="{FONT}" font-size="34" font-weight="bold">zon in je rug</text>')
for y in (180, 270):
    s.append(f'<line x1="120" y1="{y}" x2="400" y2="{y+75}" stroke="#f2b705" stroke-width="5"/>')
    s.append(arrowhead(400, y + 75, 280, 75, "#f2b705", 24))
# person facing right
x = 470; hy = GROUND - 190
s.append(f'<circle cx="{x}" cy="{hy}" r="28" fill="#222"/>')
s.append(f'<line x1="{x}" y1="{hy+28}" x2="{x}" y2="{GROUND-75}" stroke="#222" stroke-width="12"/>')
s.append(f'<line x1="{x}" y1="{GROUND-75}" x2="{x-28}" y2="{GROUND}" stroke="#222" stroke-width="12"/>')
s.append(f'<line x1="{x}" y1="{GROUND-75}" x2="{x+28}" y2="{GROUND}" stroke="#222" stroke-width="12"/>')
s.append(f'<line x1="{x}" y1="{hy+60}" x2="{x+70}" y2="{hy+70}" stroke="#222" stroke-width="10"/>')
# hose
s.append(f'<path d="M{x+70},{hy+70} q-40,120 -140,{GROUND-hy-70-8} l-300,0" fill="none" stroke="#2b8a3e" stroke-width="10"/>')
s.append(f'<line x1="{x+60}" y1="{hy+72}" x2="{x+100}" y2="{hy+60}" stroke="#555" stroke-width="12"/>')
# mist
import random
random.seed(3)
for k in range(650):
    t = random.random()
    sx = x + 110 + t * 760
    top = hy + 40 - math.sin(t * math.pi) * 330
    sy = top + random.random() * (GROUND - top) * (0.35 + 0.65 * t)
    s.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="2.6" fill="#9ec3e6"/>')
# shadow of head on ground (antisolar point direction) and rainbow arc around it
shx = x + 270
s.append(f'<ellipse cx="{x+150}" cy="{GROUND+8}" rx="150" ry="10" fill="#7c8f63" opacity="0.6"/>')

cxr, cyr = 1020, GROUND + 8
bands = ["#e01b1b", "#f7861c", "#f5d21b", "#3aa83a", "#2a6fdb", "#7a2bd6"]
for k, c in enumerate(bands):
    rr = 300 - k * 13
    s.append(f'<path d="M{cxr-rr},{cyr} A{rr},{rr} 0 0 1 {cxr+rr},{cyr}" fill="none" stroke="{c}" stroke-width="13" opacity="0.85"/>')
s.append(f'<text x="{x+150}" y="{GROUND+56}" font-family="{FONT}" font-size="28" text-anchor="middle" font-style="italic">je schaduw</text>')
s.append(f'<text x="1040" y="{GROUND-330}" font-family="{FONT}" font-size="32" font-weight="bold" text-anchor="middle">regenboog in de nevel</text>')
s.append(f'<text x="900" y="{GROUND+100}" font-family="{FONT}" font-size="30" text-anchor="middle">fijne nevel uit de tuinslang</text>')
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">{"".join(s)}<rect width="{W}" height="{H}" fill="none" stroke="#888" stroke-width="3"/></svg>'
save("sproeier", svg, 1400)
