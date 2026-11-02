import numpy as np, json
from scipy.spatial import Voronoi
from shapely.geometry import LineString, Point, box
rng=np.random.default_rng(7)
W,H=820,520; cx,cy=W/2,H/2
pts=[]
# rooster met jitter, cellen langgerekt
for j in range(-1,8):
    for i in range(-1,10):
        x=i*100+(50 if j%2 else 0)+rng.uniform(-22,22); y=j*78+rng.uniform(-16,16)
        if ((x-cx)/150)**2+((y-cy)/140)**2<1: continue
        pts.append((x,y))
# ring van cellen rond het huidmondje (bijcellen)
for k in range(6):
    a=k*np.pi/3+0.3; pts.append((cx+175*np.cos(a)*1.0, cy+150*np.sin(a)))
vor=Voronoi(np.array(pts))
clip=box(0,0,W,H)
paden=[]
for (a,b) in vor.ridge_vertices:
    if a<0 or b<0: continue
    p,q=vor.vertices[a],vor.vertices[b]
    L=LineString([p,q]).intersection(clip)
    if L.is_empty or L.geom_type!='LineString': continue
    (x1,y1),(x2,y2)=L.coords[0],L.coords[-1]
    # sla randen binnen de stomacomplex-ellips over
    mx,my=(x1+x2)/2,(y1+y2)/2
    if ((mx-cx)/112)**2+((my-cy)/122)**2<1: continue
    d=np.hypot(x2-x1,y2-y1);
    if d<4: continue
    nx,ny=-(y2-y1)/d,(x2-x1)/d
    n=max(3,int(d/14)); amp=min(7,d/9); ph=rng.uniform(0,6.28)
    s=f'M{x1:.1f},{y1:.1f}'
    for i in range(1,n+1):
        t=i/n; off=amp*np.sin(t*np.pi*n/1.5+ph)*np.sin(t*np.pi)
        x=x1+(x2-x1)*t+nx*off; y=y1+(y2-y1)*t+ny*off
        s+=f' L{x:.1f},{y:.1f}'
    paden.append(s)
open('epidermis.json','w').write(json.dumps({'W':W,'H':H,'d':' '.join(paden)}))
print(len(paden))
