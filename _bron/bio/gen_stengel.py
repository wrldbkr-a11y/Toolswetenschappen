import numpy as np, json, math
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, Point, box
from shapely import affinity
from shapely.ops import unary_union
rng=np.random.default_rng(5)
C=400; R=360
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
def poisson(region,sp,n=6000,seed=None):
    minx,miny,maxx,maxy=region.bounds; pts=[]
    for _ in range(n):
        x,y=rng.uniform(minx,maxx),rng.uniform(miny,maxy)
        if not region.contains(Point(x,y)): continue
        if any((x-a)**2+(y-b)**2<sp*sp for a,b in pts): continue
        pts.append((x,y))
    return pts
disk=Point(C,C).buffer(R,256)
NB=8; RB=248
def L2W(a,bx,by,s,t): return bx+math.cos(a)*s-math.sin(a)*t, by+math.sin(a)*s+math.cos(a)*t
def localpoly(a,bx,by,g): return affinity.translate(affinity.rotate(g,math.degrees(a),origin=(0,0)),bx,by)
out={'par':[],'epi':[],'floeem':[],'vezel':[],'camb':[]}; vessels=[]; outlines=[]
bundle_geoms=[]
bundles=[]
for k in range(NB):
    a=k*2*math.pi/NB+0.2; bx,by=C+RB*math.cos(a),C+RB*math.sin(a)
    shape=localpoly(a,bx,by,affinity.scale(Point(0,0).buffer(1,64),62,42))
    bundle_geoms.append(shape); bundles.append((a,bx,by))
    # houtvaten
    for s,rv in [(-16,9.5),(-34,8),(-50,5.5)]:
        for t in (-21,0,21):
            if abs(t)==21 and s==-50: continue
            x,y=L2W(a,bx,by,s,t); vessels.append((x,y,rv))
    # gebieden
    def reg(s0,s1): return localpoly(a,bx,by,box(s0,-45,s1,45)).intersection(shape)
    xyl=reg(-62,-6); flo=reg(5,40); vez=reg(40,62)
    # cambium: rij platte cellen
    for t in np.linspace(-30,30,8):
        cx_,cy_=L2W(a,bx,by,-0.5,t)
        r=localpoly(a,0,0,box(-4.5,-3.6,4.5,3.6)); r=affinity.translate(r,cx_,cy_)
        out['camb'].append(pd(r.buffer(0.8,join_style=1).intersection(shape)))
    for P_,key,sp,bw in [(flo,'floeem',8.5,-1.1),(vez,'vezel',7.5,-2.2)]:
        pts=poisson(P_,sp,1500)
        if len(pts)<4: continue
        for i,c in vcells(pts,P_): out[key].append(pd(c.buffer(bw,join_style=1)))
    # houtparenchym tussen de vaten
    pts=poisson(xyl,9,1500); pts=[p for p in pts if all((p[0]-x)**2+(p[1]-y)**2>(rv+4)**2 for x,y,rv in vessels)]
    for i,c in vcells(pts,xyl):
        for x,y,rv in vessels: c=c.difference(Point(x,y).buffer(rv+2,24))
        out['par'].append(('x',pd(c.buffer(-1,join_style=1))))
    outlines.append(pd(shape))
bu=unary_union(bundle_geoms)
# epidermis
NE=160; epi=[]
for k in range(NE):
    a0,a1=k*2*math.pi/NE,(k+1)*2*math.pi/NE
    pts=[(C+R*math.cos(a),C+R*math.sin(a)) for a in np.linspace(a0,a1,4)]+[(C+(R-17)*math.cos(a),C+(R-17)*math.sin(a)) for a in np.linspace(a1,a0,4)]
    out['epi'].append(pd(Polygon(pts).buffer(-1.2,join_style=1)))
# parenchym
inner=disk.difference(Point(C,C).buffer(R-17,256).symmetric_difference(Point(C,C).buffer(R+5))).difference(bu.buffer(2))
inner=Point(C,C).buffer(R-17,256).difference(bu.buffer(2))
pts=[]
for _ in range(9000):
    r=math.sqrt(rng.uniform(0,1))*(R-20); a=rng.uniform(0,6.283); x,y=C+r*math.cos(a),C+r*math.sin(a)
    if not inner.contains(Point(x,y)): continue
    sp=17 if r>RB+60 else (36 if r<RB-75 else 22)
    if any((x-p)**2+(y-q)**2<sp*sp for p,q in pts): continue
    pts.append((x,y))
for i,c in vcells(pts,inner):
    r=math.hypot(pts[i][0]-C,pts[i][1]-C)
    out['par'].append(('s' if r>RB else 'm',pd(c.buffer(-1.1,join_style=1))))
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800"><circle cx="{C}" cy="{C}" r="{R+1}" fill="#7d9348"/>']
svg.append('<path fill="#f7f5e8" d="'+''.join(d for t,d in out['par'] if t=='m')+'"/>')
svg.append('<path fill="#dcedc4" d="'+''.join(d for t,d in out['par'] if t=='s')+'"/>')
svg.append('<path fill="#efe4c8" d="'+''.join(d for t,d in out['par'] if t=='x')+'"/>')
svg.append('<path fill="#f4eda9" d="'+''.join(out['floeem'])+'"/>')
svg.append('<path fill="#e8cfa0" d="'+''.join(out['vezel'])+'"/>')
svg.append('<path fill="#9fd65a" stroke="#5f8f2a" stroke-width="0.8" d="'+''.join(out['camb'])+'"/>')
svg.append('<path fill="#bfe08f" d="'+''.join(out['epi'])+'"/>')
for x,y,rv in vessels: svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rv+1.8}" fill="#a0522d"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{rv-0.8}" fill="#fdfaf5"/>')
svg.append(f'<path fill="none" stroke="#5e7a2c" stroke-width="1.6" d="{"".join(outlines)}"/>')
svg.append(f'<circle cx="{C}" cy="{C}" r="{R+1}" fill="none" stroke="#5b7a2a" stroke-width="3"/></svg>')
open('stengel.svg','w').write(''.join(svg))
info={'bundels':[(round(x),round(y),round(math.degrees(a))) for a,x,y in bundles]}
json.dump(info,open('stengel.json','w')); print(info, len(''.join(svg))//1024,'KB')
