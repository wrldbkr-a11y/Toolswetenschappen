import numpy as np, json, math
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, Point, box, LineString
from shapely import affinity
from shapely.ops import unary_union
rng=np.random.default_rng(11)
C=400; R=250
exec(open('gen_stengel.py').read().split('disk=Point')[0].split('rng=np.random')[0])
def pd(p):
    if p.is_empty: return ''
    gs=p.geoms if hasattr(p,'geoms') else [p]; o=''
    for g in gs:
        if g.geom_type!='Polygon' or g.area<4: continue
        c=list(g.exterior.coords); o+='M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in c[:-1])+'Z'
    return o
def vcells(pts,clip):
    pts=np.array(pts); far=np.array([[C+4000*math.cos(a),C+4000*math.sin(a)] for a in np.linspace(0,6.28,8,endpoint=False)])
    vor=Voronoi(np.vstack([pts,far])); out=[]
    for i in range(len(pts)):
        reg=vor.regions[vor.point_region[i]]
        if -1 in reg or not reg: continue
        P=Polygon(vor.vertices[reg]).intersection(clip)
        if not P.is_empty: out.append((i,P))
    return out
def poisson(region,sp,n=6000):
    minx,miny,maxx,maxy=region.bounds; pts=[]
    for _ in range(n):
        x,y=rng.uniform(minx,maxx),rng.uniform(miny,maxy)
        if not region.contains(Point(x,y)): continue
        if any((x-a)**2+(y-b)**2<sp*sp for a,b in pts): continue
        pts.append((x,y))
    return pts
ring=lambda r1,r0: Point(C,C).buffer(r1,256).difference(Point(C,C).buffer(r0,256))
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800">']
# wortelharen (achter de epidermis)
haren=[]; hp=''
NE=96
for k in range(NE):
    if k%3: continue
    a=(k+0.5)*2*math.pi/NE+rng.uniform(-0.01,0.01); L=rng.uniform(70,135); w=7
    pts=[]; 
    for j in range(16):
        s=j/15; r=R-6+s*L; bend=math.sin(s*2.2+k)*10*s
        ang=a+bend/r
        pts.append((C+r*math.cos(ang),C+r*math.sin(ang)))
    line=LineString(pts).buffer(w/2,cap_style=1)
    haren.append(line); hp+=pd(line.buffer(0))
svg.append(f'<path d="{hp}" fill="#e8f2d8" stroke="#7d9348" stroke-width="2"/>')
svg.append(f'<circle cx="{C}" cy="{C}" r="{R+1}" fill="#7d9348"/>')
# epidermis
ep=''
for k in range(NE):
    a0,a1=k*2*math.pi/NE,(k+1)*2*math.pi/NE
    P=Polygon([(C+R*math.cos(a),C+R*math.sin(a)) for a in np.linspace(a0,a1,4)]+[(C+(R-15)*math.cos(a),C+(R-15)*math.sin(a)) for a in np.linspace(a1,a0,4)])
    ep+=pd(P.buffer(-1.1,join_style=1))
# schors
cor=ring(R-16,92); pts=[]
for _ in range(9000):
    r=math.sqrt(rng.uniform((94/R)**2,1))*(R-18); a=rng.uniform(0,6.283); x,y=C+r*math.cos(a),C+r*math.sin(a)
    if not cor.contains(Point(x,y)): continue
    sp=26 if r>120 else 16
    if any((x-p)**2+(y-q)**2<sp*sp for p,q in pts): continue
    pts.append((x,y))
cp=''
for i,c in vcells(pts,cor): cp+=pd(c.buffer(-1.3,join_style=1))
# endodermis + pericykel
en=''; band=''
for k in range(44):
    a0,a1=k*2*math.pi/44,(k+1)*2*math.pi/44
    P=Polygon([(C+92*math.cos(a),C+92*math.sin(a)) for a in np.linspace(a0,a1,4)]+[(C+80*math.cos(a),C+80*math.sin(a)) for a in np.linspace(a1,a0,4)])
    en+=pd(P.buffer(-1,join_style=1))
for k in range(40):
    a0,a1=k*2*math.pi/40,(k+1)*2*math.pi/40
    P=Polygon([(C+80*math.cos(a),C+80*math.sin(a)) for a in np.linspace(a0,a1,4)]+[(C+71*math.cos(a),C+71*math.sin(a)) for a in np.linspace(a1,a0,4)])
    band+=pd(P.buffer(-1,join_style=1))
# centrale cilinder: houtvaten in kruis
vat=[(C,C,12)]
for k in range(4):
    a=k*math.pi/2+math.pi/4
    for d,rv in [(24,10),(42,8),(57,5.5)]: vat.append((C+d*math.cos(a),C+d*math.sin(a),rv))
cen=Point(C,C).buffer(71,128)
flo=[]
for k in range(4):
    a=k*math.pi/2
    flo.append(Point(C+48*math.cos(a),C+48*math.sin(a)).buffer(17,48).intersection(cen))
flo_u=unary_union(flo)
pts=poisson(cen.difference(flo_u),9,3000); pts=[p for p in pts if all((p[0]-x)**2+(p[1]-y)**2>(rv+4)**2 for x,y,rv in vat)]
pp=''
for i,c in vcells(pts,cen.difference(flo_u)):
    for x,y,rv in vat: c=c.difference(Point(x,y).buffer(rv+2,24))
    pp+=pd(c.buffer(-0.9,join_style=1))
fp=''
for f in flo:
    for i,c in vcells(poisson(f,6.5,800),f): fp+=pd(c.buffer(-0.8,join_style=1))
svg.append(f'<path fill="#bfe08f" d="{ep}"/><path fill="#eef3df" d="{cp}"/><path fill="#d8c48a" d="{en}"/><path fill="#e7efcf" d="{band}"/><path fill="#efe7cf" d="{pp}"/><path fill="#f4eda9" d="{fp}"/>')
# bandje van Caspary
svg.append(f'<circle cx="{C}" cy="{C}" r="86" fill="none" stroke="#8a5a2b" stroke-width="2.2" stroke-dasharray="3 6.1"/>')
for x,y,rv in vat: svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rv+1.8}" fill="#a0522d"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{rv-0.8}" fill="#fdfaf5"/>')
svg.append('</svg>')
open('wortel.svg','w').write(''.join(svg)); print(len(''.join(svg))//1024,'KB')
