# Schematische figuur: exocriene klier (met afvoerbuis) en endocriene klier (zonder afvoerbuis), eigen tekening.
# Gebruik: from klieren_schema import figuur ; figuur() geeft een <svg> terug. Wordt gebruikt in de tool biologie-klieren.html en in de biologiecursus.
import math

GEEL, GEELR, KERN = '#FBE7A1', '#C9A227', '#8A6D1C'
ROOD, ROODL, BLAUW, BLAUWL = '#C62828', '#EF9A9A', '#1565C0', '#90CAF9'
PIJL, INK = '#4FA3D9', '#1D2A36'

def defs():
    return (f'<defs><marker id="kp" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="3.4" markerHeight="3.4" orient="auto-start-reverse">'
            f'<path d="M0 0.5L9.5 5L0 9.5z" fill="{PIJL}"/></marker>'
            f'<clipPath id="endoclip"><ellipse cx="560" cy="215" rx="118" ry="150"/></clipPath></defs>')

def pijl(d, w=7):
    return (f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{w + 3}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{PIJL}" stroke-width="{w}" stroke-linecap="round" marker-end="url(#kp)"/>')

def label(x, y, tekst, x2, y2, anker='start'):
    w = len(tekst) * 8.6                        # geschatte breedte van de tekst
    links, rechts = (x - w, x) if anker == 'end' else (x, x + w)
    xa = rechts + 4 if x2 > rechts else (links - 4 if x2 < links else x2)
    ya = y - 5 if (x2 > rechts or x2 < links) else (y + 5 if y2 > y else y - 20)
    return (f'<line x1="{x2}" y1="{y2}" x2="{xa:.0f}" y2="{ya}" stroke="{INK}" stroke-width="1.2"/>'
            f'<circle cx="{x2}" cy="{y2}" r="2.5" fill="{INK}"/>'
            f'<text x="{x}" y="{y}" text-anchor="{anker}" font-size="17" font-weight="700" fill="{INK}" font-style="italic">{tekst}</text>')

def bloedvat(d, kleur, licht):
    return (f'<path d="{d}" fill="none" stroke="{kleur}" stroke-width="30" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{licht}" stroke-width="18" stroke-linecap="round"/>')

def exo():
    cx = 190
    o = bloedvat('M8 318 C60 320 110 372 190 388', ROOD, ROODL) + bloedvat('M190 388 C270 372 320 320 372 318', BLAUW, BLAUWL)
    OUT = 'M168 46 V128 C112 150 86 200 86 258 C86 326 132 366 190 366 C248 366 294 326 294 258 C294 200 268 150 212 128 V46 Z'
    INN = 'M181 46 V140 C152 170 142 214 142 258 C142 298 162 318 190 318 C218 318 238 298 238 258 C238 214 228 170 199 140 V46 Z'
    o += f'<path d="{OUT}" fill="{GEEL}" stroke="{GEELR}" stroke-width="2.5"/><path d="{INN}" fill="#FFF8E1" stroke="{GEELR}" stroke-width="1.8"/>'
    # celwanden in de klierwand: van de binnenrand naar de buitenrand
    def p(a, b, t, cy=258): return cx + a * math.cos(t), cy + b * math.sin(t)
    for g in range(-68, 260, 23):
        t = math.radians(g)
        x1, y1 = p(48, 60, t); x2, y2 = p(104, 108, t)
        o += f'<path d="M{x1:.0f} {y1:.0f} Q{(x1 + x2) / 2 + 3:.0f} {(y1 + y2) / 2:.0f} {x2:.0f} {y2:.0f}" stroke="{GEELR}" stroke-width="1.4" fill="none"/>'
        xm, ym = p(76, 84, t + math.radians(11.5))
        o += f'<ellipse cx="{xm:.0f}" cy="{ym:.0f}" rx="6" ry="5" fill="{KERN}" opacity=".85"/>'
    for y in range(58, 128, 23):   # cellen in de afvoerbuis
        o += f'<path d="M168 {y} H181 M199 {y} H212" stroke="{GEELR}" stroke-width="1.4"/>'
        o += f'<circle cx="174.5" cy="{y + 12}" r="3.6" fill="{KERN}" opacity=".85"/><circle cx="205.5" cy="{y + 12}" r="3.6" fill="{KERN}" opacity=".85"/>'
    # stoffen: uit het bloed naar de kliercellen, naar de holte, door de afvoerbuis naar buiten
    o += pijl('M120 372 C118 350 122 336 132 322') + pijl('M258 372 C262 352 258 336 248 322')
    o += pijl('M160 300 C170 292 176 288 182 284', 5) + pijl('M222 300 C212 292 206 288 200 284', 5)
    o += pijl('M190 300 V54 C190 44 184 40 172 36', 7)
    o += pijl('M190 70 C191 50 197 42 210 36', 6)
    o += label(30, 100, 'afvoerbuis', 168, 96)
    o += label(6, 214, 'kliercellen', 104, 214)
    o += label(14, 296, 'slagader', 36, 318)
    o += label(374, 296, 'ader', 352, 318, 'end')
    o += f'<text x="{cx}" y="24" text-anchor="middle" font-size="19" font-weight="800" fill="{INK}">exocriene klier</text>'
    return o

def endo():
    cx, cy = 560, 215
    vaten = bloedvat('M410 330 C440 340 470 400 560 396', ROOD, ROODL) + bloedvat('M560 396 C650 400 680 340 710 330', BLAUW, BLAUWL)
    o = f'<ellipse cx="{cx}" cy="{cy}" rx="118" ry="150" fill="{GEEL}"/>'
    cellen = ''
    for r, y in enumerate(range(70, 380, 38)):
        sh = 0 if r % 2 == 0 else 26
        for x in range(430 + sh, 700, 52):
            cellen += f'<rect x="{x}" y="{y}" width="52" height="38" rx="9" fill="{GEEL}" stroke="{GEELR}" stroke-width="1.4"/><ellipse cx="{x + 26}" cy="{y + 19}" rx="6" ry="5" fill="{KERN}" opacity=".85"/>'
    o += f'<g clip-path="url(#endoclip)">{cellen}</g><ellipse cx="{cx}" cy="{cy}" rx="118" ry="150" fill="none" stroke="{GEELR}" stroke-width="2.5"/>'
    # stoffen uit de slagader in de klier, hormonen uit de klier in de ader
    o += vaten
    o += pijl('M488 384 C476 330 500 290 506 240 C510 200 498 170 486 150', 8)
    o += pijl('M622 140 C636 180 618 220 624 270 C628 310 636 345 632 382', 8)
    o += label(420, 62, 'kliercellen', 500, 92, 'end')
    o += label(410, 450, 'slagader', 440, 352)
    o += label(712, 450, 'ader', 682, 352, 'end')
    o += label(752, 62, 'geen afvoerbuis', 640, 90, 'end')
    o += f'<text x="{cx}" y="24" text-anchor="middle" font-size="19" font-weight="800" fill="{INK}">endocriene klier</text>'
    return o

def legende():
    return (f'<g font-size="14" fill="{INK}"><path d="M30 470 H60" stroke="{PIJL}" stroke-width="7" marker-end="url(#kp)"/>'
            f'<text x="70" y="475">exocrien: de klierafscheiding gaat via de afvoerbuis naar buiten of naar een holte</text>'
            f'<text x="70" y="495">endocrien: de klier geeft hormonen af aan het bloed</text></g>')

def figuur():
    return (f'<svg viewBox="0 0 760 510" width="760" xmlns="http://www.w3.org/2000/svg" font-family="Inter,Atkinson Hyperlegible,sans-serif" role="img" '
            f'aria-label="schema van een exocriene klier met afvoerbuis en een endocriene klier zonder afvoerbuis">'
            f'<rect width="760" height="510" fill="#fff"/>{defs()}{exo()}{endo()}{legende()}</svg>')

if __name__ == '__main__':
    open('/tmp/klieren_schema.svg', 'w').write(figuur())
