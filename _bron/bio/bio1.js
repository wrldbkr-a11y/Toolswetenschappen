//////////////////// HULP ////////////////////
const SVGNS='http://www.w3.org/2000/svg';
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
const shuffle=a=>{ a=a.slice(); for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; };
function lus(id,fn){ let last=performance.now(); (function f(now){ const dt=Math.min(0.05,(now-last)/1000); last=now; if(isActive(id)) fn(dt,now); requestAnimationFrame(f); })(last); }

//////////////////// LABELFIGUUR ////////////////////
// Een afbeelding (of SVG-tekening) met aanwijspunten. Modus 'bekijk': namen zichtbaar, klik voor uitleg.
// Modus 'oefen': namen verborgen, de leerling duidt het gevraagde deel aan.
function labelFig(o){
  const wrap=$(o.wrap), ctl=$(o.ctl), ml=o.ml??230, mr=o.mr??230, W=o.w, H=o.h, top=o.top??0, bot=o.bot??0;
  let modus='bekijk', sel=null, vraag=null, rest=[], goed=0, tot=0;
  ctl.innerHTML=`<div class="ctrl-row"><button class="btn on" data-m="bekijk">Bekijken</button><button class="btn" data-m="oefen">Zelf aanduiden</button></div>
    <div class="readout lf-read"></div><div class="chips"></div>${o.noot?`<div class="note">${o.noot}</div>`:''}`;
  const read=ctl.querySelector('.lf-read'), chips=ctl.querySelector('.chips');
  ctl.querySelectorAll('[data-m]').forEach(b=>b.onclick=()=>{ modus=b.dataset.m; ctl.querySelectorAll('[data-m]').forEach(x=>x.classList.toggle('on',x===b)); if(modus==='oefen') start(); else { sel=null; teken(); } });
  // labelposities per kant, zonder overlap
  const P=o.punten.map((p,i)=>({...p,i}));
  ['l','r'].forEach(k=>{ const L=P.filter(p=>(p.kant||(p.x<W/2?'l':'r'))===k).sort((a,b)=>(a.ly??a.y)-(b.ly??b.y));
    L.forEach(p=>{ p.kant=k; p.yy=p.ly??p.y; });
    const G=o.gap??34;
    for(let it=0;it<60;it++){ for(let j=1;j<L.length;j++){ const d=L[j].yy-L[j-1].yy; if(d<G){ const m=(G-d)/2; L[j].yy+=m; L[j-1].yy-=m; } } L.forEach(p=>p.yy=Math.max(18-top,Math.min(H+bot-12,p.yy))); } });
  function start(){ rest=shuffle(P.map(p=>p.i)); goed=0; tot=0; volgende(); }
  function volgende(){ vraag=rest.shift(); sel=null; teken(); }
  function kies(i){
    if(modus==='bekijk'){ sel=i; teken(); return; }
    if(vraag==null) return;
    tot++; const ok=i===vraag; if(ok) goed++;
    sel=ok?i:null;
    const juist=P[vraag];
    read.innerHTML=(ok?`<span class="ok">Juist!</span> Dat is ${esc(juist.naam)}.`:`<span class="flag">Niet juist.</span> Je klikte op ${esc(P[i].naam)}. Kijk waar ${esc(juist.naam)} ligt.`)+`<br><span class="k">${juist.info||''}</span>`;
    flits=ok?null:vraag;
    if(ok) setTimeout(()=>{ if(modus==='oefen'){ if(rest.length) volgende(); else { vraag=null; teken(); read.innerHTML=`<span class="ok">Klaar!</span> ${goed} van de ${tot} keer juist geklikt. <button class="btn" style="margin-top:8px" id="${o.wrap}-opn">↻ Opnieuw</button>`; $(o.wrap+'-opn').onclick=start; } } },900);
    else teken(true);
  }
  let flits=null;
  function teken(behoudRead){
    const kant=x=>x;
    let s=`<svg viewBox="${-ml} ${-top} ${W+ml+mr} ${H+top+bot}" style="display:block;width:100%;height:auto;font-family:Inter,sans-serif">`;
    s+=o.img?`<image href="${o.img}" x="0" y="0" width="${W}" height="${H}"/>`:o.inner;
    P.forEach(p=>{
      const on=sel===p.i, toonNaam=modus==='bekijk';
      const lx=p.kant==='l'?-14:W+14, anchor=p.kant==='l'?'end':'start';
      const kleur=on?'#d97706':(flits===p.i?'#dc2626':'#1D2A36');
      if(toonNaam){
        const ex=p.kant==='l'?-8:W+8;
        s+=`<path d="M${p.x},${p.y} L${p.kant==='l'?Math.min(p.x-20,ex+40):Math.max(p.x+20,ex-40)},${p.yy} L${ex},${p.yy}" fill="none" stroke="${kleur}" stroke-width="${on?2.6:1.6}"/>`;
        s+=`<text x="${lx}" y="${p.yy+6}" text-anchor="${anchor}" font-size="${o.fs||19}" font-weight="${on?700:600}" fill="${kleur}" style="cursor:pointer" data-i="${p.i}" stroke="#fff" stroke-width="4" paint-order="stroke">${esc(p.naam)}</text>`;
      }
      s+=`<g data-i="${p.i}" style="cursor:pointer"><circle cx="${p.x}" cy="${p.y}" r="${o.r||11}" fill="${on?'#d97706':(flits===p.i?'#dc2626':'#fff')}" stroke="${on?'#7c2d12':'#1D2A36'}" stroke-width="2.5" opacity="0.95"/>`+
        (!toonNaam?`<text x="${p.x}" y="${p.y+5}" text-anchor="middle" font-size="13" font-weight="700" fill="${on?'#fff':'#1D2A36'}" pointer-events="none">?</text>`:`<circle cx="${p.x}" cy="${p.y}" r="3.5" fill="${on?'#fff':'#1D2A36'}"/>`)+`</g>`;
    });
    s+='</svg>';
    wrap.innerHTML=s;
    wrap.querySelectorAll('[data-i]').forEach(e=>e.onclick=()=>kies(+e.dataset.i));
    chips.innerHTML=modus==='bekijk'?P.map(p=>`<button class="chip${sel===p.i?' on':''}" data-c="${p.i}">${esc(p.naam)}</button>`).join(''):'';
    chips.querySelectorAll('[data-c]').forEach(b=>b.onclick=()=>kies(+b.dataset.c));
    if(behoudRead) return;
    if(modus==='bekijk') read.innerHTML=sel==null?'<span class="k">Klik op een punt of een naam.</span>':`<b>${esc(P[sel].naam)}</b><br>${P[sel].info||''}`;
    else if(vraag!=null) read.innerHTML=`Klik op: <b style="font-size:17px">${esc(P[vraag].naam)}</b><br><span class="k">nog ${rest.length+1} te gaan</span>`;
  }
  teken();
}

//////////////////// PLANT (zelf getekend) ////////////////////
const PLANT=(function(){
  const GY=372;
  const stam=t=>[320+7*Math.sin(t*3.2),GY-t*292];
  const stamPad=n=>[...Array(n+1)].map((_,i)=>stam(i/n));
  // bladeren: [t op de stengel, kant (+1 rechts / -1 links), hoek, lengte]
  const BL=[[0.24,1,-18,150],[0.43,-1,-22,140],[0.6,1,-30,128],[0.76,-1,-36,108]];
  const bladen=BL.map(([t,k,h,L])=>{
    const [x0,y0]=stam(t), a=(k>0?h:180-h)*Math.PI/180, ux=Math.cos(a), uy=Math.sin(a);
    const st=[x0+ux*22,y0+uy*22-4], tip=[st[0]+ux*L,st[1]+uy*L];
    return {t,k,x0,y0,ux,uy,L,st,tip,
      nerf:[...Array(9)].map((_,i)=>[st[0]+ux*L*i/8,st[1]+uy*L*i/8-Math.sin(i/8*Math.PI)*6])};
  });
  // wortels
  const wortels=[];
  function wortel(x,y,a,L,dikte,diepte){
    const pts=[[x,y]]; let cx=x,cy=y,ca=a;
    for(let i=1;i<=10;i++){ ca+=Math.sin(i*1.7+x*0.05)*0.06; cx+=Math.cos(ca)*L/10; cy+=Math.sin(ca)*L/10; pts.push([cx,cy]); }
    wortels.push({pts,dikte});
    if(diepte>0) [0.35,0.6,0.8].forEach((f,j)=>{ const p=pts[Math.round(f*10)]; const s=(j%2?1:-1)*(diepte===2?1:(x>320?1:-1)); wortel(p[0],p[1],a+s*0.75,L*0.45,dikte*0.5,diepte-1); });
  }
  wortel(320,GY,Math.PI/2,230,9,2);
  [[-1,0.18],[1,0.32],[-1,0.5],[1,0.66]].forEach(([k,f])=>{ const p=wortels[0].pts[Math.round(f*10)]; wortel(p[0],p[1],Math.PI/2+k*1.05,150*(1-f*0.5),5,1); });
  function bladVorm(b){
    const {st,tip,ux,uy,L}=b, nx=-uy, ny=ux, w=L*0.32;
    const m1=[st[0]+ux*L*0.35+nx*w,st[1]+uy*L*0.35+ny*w], m2=[st[0]+ux*L*0.35-nx*w,st[1]+uy*L*0.35-ny*w];
    const q1=[st[0]+ux*L*0.8+nx*w*0.55,st[1]+uy*L*0.8+ny*w*0.55], q2=[st[0]+ux*L*0.8-nx*w*0.55,st[1]+uy*L*0.8-ny*w*0.55];
    return `M${st} C${m1} ${q1} ${tip} C${q2} ${m2} ${st}Z`;
  }
  function svg(P='a'){
    let s=`<defs><linearGradient id="pl-lucht${P}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eaf4fb"/><stop offset="1" stop-color="#f7fbf2"/></linearGradient>
      <linearGradient id="pl-grond${P}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b98d5e"/><stop offset="1" stop-color="#8a6239"/></linearGradient>
      <linearGradient id="pl-blad${P}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7cc35a"/><stop offset="1" stop-color="#3f8f34"/></linearGradient>
      <radialGradient id="pl-kroon${P}"><stop offset="0" stop-color="#fff3a8"/><stop offset="1" stop-color="#f4a62a"/></radialGradient></defs>`;
    s+=`<rect x="0" y="0" width="640" height="${GY}" fill="url(#pl-lucht${P})"/><rect x="0" y="${GY}" width="640" height="${640-GY}" fill="url(#pl-grond${P})"/>`;
    for(let i=0;i<70;i++){ const x=(i*97)%640, y=GY+12+((i*53)%250); s+=`<ellipse cx="${x}" cy="${y}" rx="${2+i%3}" ry="${1.5+i%2}" fill="#6f4c2c" opacity=".35"/>`; }
    s+=`<path d="M0,${GY} L640,${GY}" stroke="#5d4026" stroke-width="2"/>`;
    // wortels
    wortels.forEach(w=>{ s+=`<path d="M${w.pts.join(' L')}" fill="none" stroke="#e9dcc0" stroke-width="${w.dikte+2}" stroke-linecap="round" stroke-linejoin="round"/><path d="M${w.pts.join(' L')}" fill="none" stroke="#f8f0de" stroke-width="${w.dikte}" stroke-linecap="round" stroke-linejoin="round"/>`;
      // wortelhaartjes bij de punt
      const n=w.pts.length; for(let i=n-4;i<n-1;i++){ const [x,y]=w.pts[i],[x2,y2]=w.pts[i+1], a=Math.atan2(y2-y,x2-x); for(const s2 of [-1,1]){ const b=a+s2*1.25; s+=`<path d="M${x},${y} l${Math.cos(b)*9},${Math.sin(b)*9}" stroke="#f4ead2" stroke-width="1.2"/>`; } } });
    // stengel
    const sp=stamPad(30);
    s+=`<path d="M${sp.join(' L')}" fill="none" stroke="#2f6b25" stroke-width="15" stroke-linecap="round"/><path d="M${sp.join(' L')}" fill="none" stroke="#5aa53f" stroke-width="11" stroke-linecap="round"/><path d="M${sp.map(([x,y])=>[x-2.5,y]).join(' L')}" fill="none" stroke="#8fd16b" stroke-width="2.5" opacity=".7"/>`;
    // bladeren
    bladen.forEach(b=>{
      s+=`<path d="M${b.x0},${b.y0} L${b.st}" stroke="#3f8f34" stroke-width="5" stroke-linecap="round"/>`;
      s+=`<path d="${bladVorm(b)}" fill="url(#pl-blad${P})" stroke="#2c6b22" stroke-width="2"/>`;
      s+=`<path d="M${b.nerf.join(' L')}" fill="none" stroke="#c8ecb0" stroke-width="2"/>`;
      for(let i=1;i<7;i++){ const p=b.nerf[i], f=1-i/8, nx=-b.uy, ny=b.ux;
        for(const k of [-1,1]) s+=`<path d="M${p} q${b.ux*14+nx*k*b.L*0.18*f},${b.uy*14+ny*k*b.L*0.18*f} ${b.ux*24+nx*k*b.L*0.26*f},${b.uy*24+ny*k*b.L*0.26*f}" fill="none" stroke="#b5e298" stroke-width="1.1" opacity=".85"/>`; }
    });
    // bloem
    const [fx,fy]=stam(1);
    s+=`<path d="M${fx-14},${fy+10} q14,10 28,0" fill="#4f9a3a"/>`;
    for(let i=0;i<8;i++){ const a=i*Math.PI/4; s+=`<ellipse cx="${fx+Math.cos(a)*30}" cy="${fy-6+Math.sin(a)*22}" rx="26" ry="12" transform="rotate(${a*180/Math.PI} ${fx+Math.cos(a)*30} ${fy-6+Math.sin(a)*22})" fill="#f2c94c" stroke="#c98d12" stroke-width="1.5"/>`; }
    s+=`<circle cx="${fx}" cy="${fy-6}" r="17" fill="#8a5a1c" stroke="#5e3a0e" stroke-width="2"/>`;
    for(let i=0;i<14;i++){ const a=i*2.4; s+=`<circle cx="${fx+Math.cos(a)*i*0.9}" cy="${fy-6+Math.sin(a)*i*0.9}" r="1.6" fill="#d9a441"/>`; }
    return s;
  }
  return {GY,stam,stamPad,bladen,wortels,svg};
})();

labelFig({wrap:'fig-plant',ctl:'ctl-plant',inner:PLANT.svg(),w:640,h:640,ml:150,mr:170,
  punten:[
    {naam:'bloem',x:320,y:74,kant:'r',info:'De <b>bloem</b> zorgt voor de voortplanting: er ontstaan zaden en vruchten.'},
    {naam:'blad',x:PLANT.bladen[0].tip[0]-40,y:PLANT.bladen[0].tip[1]+4,kant:'r',info:'In het <b>blad</b> gebeurt de fotosynthese. Via de huidmondjes wisselt het blad gassen uit en verdampt er water.'},
    {naam:'stengel',x:PLANT.stam(0.5)[0],y:PLANT.stam(0.5)[1]+20,kant:'l',info:'De <b>stengel</b> draagt de bladeren en bloemen en vervoert water en assimilaten tussen wortel en blad.'},
    {naam:'wortel',x:320,y:520,kant:'l',info:'De <b>wortel</b> verankert de plant in de bodem en neemt water en mineralen op via de wortelhaartjes.'},
  ]});

//////////////////// BLAD ////////////////////
labelFig({wrap:'fig-blad',ctl:'ctl-blad',img:IMG.blad,w:900,h:897,ml:300,mr:300,fs:24,r:13,gap:44,
  punten:[
    {naam:'epidermis',x:70,y:240,kant:'l',info:'Eén laag doorzichtige cellen aan de boven- en onderkant van het blad. Ze <b>beschermt</b> het blad en laat het licht door. Een waslaagje erop beperkt de verdamping.'},
    {naam:'parenchymcellen',x:150,y:380,kant:'l',info:'Cellen vol <b>bladgroenkorrels</b>. Bovenaan staan ze dicht tegen elkaar (veel fotosynthese), onderaan liggen ze losser met luchtholtes ertussen voor de gasuitwisseling.'},
    {naam:'sluitcellen',x:280,y:762,kant:'l',info:'Twee boonvormige cellen die samen een huidmondje vormen. Ze kunnen het huidmondje <b>openen en sluiten</b>.'},
    {naam:'huidmondje',x:323,y:782,kant:'r',ly:820,info:'De opening tussen twee sluitcellen. Langs hier <b>komt CO₂ binnen</b> en gaan <b>O₂ en waterdamp naar buiten</b>.'},
    {naam:'vacuole',x:470,y:500,kant:'r',info:'Grote blaas met celvocht (vooral water). De druk van de vacuole tegen de celwand heet <b>turgor</b>.'},
  ],noot:'Tekening: Zephyris, Wikimedia Commons, CC BY-SA 3.0 (zonder Engelse namen).'});

//////////////////// STENGEL ////////////////////
(function(){
  const B=STENGEL.bundels[0]; const a=B[2]*Math.PI/180, L=(s,t)=>[B[0]+Math.cos(a)*s-Math.sin(a)*t,B[1]+Math.sin(a)*s+Math.cos(a)*t];
  const B3=STENGEL.bundels[1]; const a3=B3[2]*Math.PI/180, L3=(s,t)=>[B3[0]+Math.cos(a3)*s-Math.sin(a3)*t,B3[1]+Math.sin(a3)*s+Math.cos(a3)*t];
  const B2=STENGEL.bundels[7]; const a2=B2[2]*Math.PI/180, L2=(s,t)=>[B2[0]+Math.cos(a2)*s-Math.sin(a2)*t,B2[1]+Math.sin(a2)*s+Math.cos(a2)*t];
  const pol=(r,deg)=>[400+r*Math.cos(deg*Math.PI/180),400+r*Math.sin(deg*Math.PI/180)];
  const pt=(p)=>({x:p[0],y:p[1]});
  labelFig({wrap:'fig-stengel',ctl:'ctl-stengel',inner:STENGEL.svg,w:800,h:800,ml:200,mr:330,fs:22,r:12,gap:42,
    punten:[
      {naam:'epidermis',...pt(pol(352,-62)),kant:'r',info:'De buitenste laag cellen. Ze beschermt de stengel. Aan de buitenkant ligt een waslaag (cuticula).'},
      {naam:'cortex',...pt(pol(318,40)),kant:'r',info:'Laag parenchymcellen tussen de epidermis en de vaatbundels. Ze geven steun en kunnen stoffen opslaan.'},
      {naam:'vaatbundel',...pt(L2(2,-41)),kant:'r',info:'Een bundel met <b>houtvaten</b>, <b>deelweefsel</b> en <b>zeefvaten</b>. In de stengel liggen de vaatbundels in een <b>kring</b>.'},
      {naam:'zeefvaten',...pt(L(22,8)),kant:'r',info:'Levende cellen met zeefplaten. Ze vervoeren de <b>assimilaten</b> (vooral suikers) door de plant. Ze liggen aan de <b>buitenkant</b> van de vaatbundel.'},
      {naam:'deelweefsel',...pt(L3(-0.5,10)),kant:'r',info:'Cellen die blijven <b>delen</b>. Naar binnen maken ze nieuwe houtvaten, naar buiten nieuwe zeefvaten. Zo wordt de stengel dikker.'},
      {naam:'houtvaten',...pt(L2(-34,0)),kant:'r',info:'Dode, holle buizen met verdikte wanden. Ze vervoeren <b>water en mineralen</b> omhoog. Ze liggen aan de <b>binnenkant</b> van de vaatbundel.'},
      {naam:'parenchymcellen',x:400,y:400,kant:'l',info:'Grote parenchymcellen in het midden van de stengel (het merg) en in de cortex. Ze kunnen stoffen opslaan.'},
    ]});
})();

// lengtedoorsnede van houtvat en zeefvat
(function(){
  const s=$('svg-vaten'); let h='';
  h+=`<defs><linearGradient id="hv" x1="0" x2="1"><stop offset="0" stop-color="#f3e3cf"/><stop offset=".5" stop-color="#fffaf2"/><stop offset="1" stop-color="#f3e3cf"/></linearGradient></defs>`;
  // houtvat
  const X=70,Y=40,Wd=90,Ht=250;
  h+=`<rect x="${X}" y="${Y}" width="${Wd}" height="${Ht}" fill="url(#hv)"/><path d="M${X},${Y} V${Y+Ht} M${X+Wd},${Y} V${Y+Ht}" stroke="#8a4b2a" stroke-width="5"/>`;
  for(let y=Y+8;y<Y+Ht;y+=17) h+=`<path d="M${X+3},${y} C${X+30},${y+10} ${X+60},${y+10} ${X+Wd-3},${y+3}" fill="none" stroke="#a0522d" stroke-width="4" stroke-linecap="round" opacity=".85"/>`;
  h+=`<text x="${X+Wd/2}" y="${Y+Ht+28}" text-anchor="middle" font-size="16" font-weight="700" fill="#1D2A36">houtvat</text>`;
  // pijlen water
  for(let i=0;i<3;i++) h+=`<path d="M${X+Wd/2},${Y+Ht-30-i*80} v-40" stroke="#2563eb" stroke-width="4"/><path d="M${X+Wd/2-8},${Y+Ht-62-i*80} l8,-12 l8,12z" fill="#2563eb"/>`;
  h+=`<g font-size="14" fill="#334155"><text x="${X+Wd+24}" y="${Y+30}">• <tspan font-weight="700">dode</tspan> cellen: hol, zonder inhoud</text><text x="${X+Wd+24}" y="${Y+56}">• geen tussenwanden: één lange buis</text><text x="${X+Wd+24}" y="${Y+82}">• wand verstevigd met</text><text x="${X+Wd+38}" y="${Y+102}">houtstof (ringen, spiralen)</text><text x="${X+Wd+24}" y="${Y+128}">• water en mineralen <tspan font-weight="700">omhoog</tspan></text></g>`;
  // zeefvat
  const X2=520,W2=72;
  for(let k=0;k<3;k++){ const y0=Y+k*84;
    h+=`<rect x="${X2}" y="${y0}" width="${W2}" height="82" rx="6" fill="#fbf6c9" stroke="#8a7a2a" stroke-width="2.5"/>`;
    h+=`<rect x="${X2+W2+2}" y="${y0+6}" width="22" height="70" rx="8" fill="#e7f0c4" stroke="#7a8a2a" stroke-width="2"/><ellipse cx="${X2+W2+13}" cy="${y0+40}" rx="6" ry="9" fill="#8a6d3b"/>`;
    if(k<2){ h+=`<rect x="${X2}" y="${y0+79}" width="${W2}" height="7" fill="#c9b85a"/>`; for(let i=0;i<6;i++) h+=`<rect x="${X2+6+i*11}" y="${y0+79}" width="5" height="7" fill="#fbf6c9"/>`; }
  }
  h+=`<path d="M${X2+W2/2},${Y+40} v150" stroke="#d97706" stroke-width="4" stroke-dasharray="2 9" stroke-linecap="round"/><path d="M${X2+W2/2-8},${Y+190} l8,12 l8,-12z" fill="#d97706"/>`;
  h+=`<text x="${X2+W2/2+10}" y="${Y+Ht+28}" text-anchor="middle" font-size="16" font-weight="700" fill="#1D2A36">zeefvat</text>`;
  h+=`<g font-size="14" fill="#334155"><text x="${X2+W2+40}" y="${Y+30}">• <tspan font-weight="700">levende</tspan> cellen</text><text x="${X2+W2+40}" y="${Y+56}">• tussenwanden met gaatjes:</text><text x="${X2+W2+54}" y="${Y+76}"><tspan font-weight="700">zeefplaten</tspan></text><text x="${X2+W2+40}" y="${Y+102}">• naast elk zeefvat: een</text><text x="${X2+W2+54}" y="${Y+122}">begeleidende cel met kern</text><text x="${X2+W2+40}" y="${Y+148}">• assimilaten <tspan font-weight="700">op en neer</tspan></text></g>`;
  h+=`<path d="M${X2-6},${Y+163} h-40" stroke="#334155" stroke-width="1.4"/><text x="${X2-50}" y="${Y+167}" text-anchor="end" font-size="13" fill="#334155">zeefplaat</text>`;
  s.innerHTML=h;
})();

//////////////////// WORTEL ////////////////////
labelFig({wrap:'fig-wortel',ctl:'ctl-wortel',inner:`<g transform="translate(-60,-60) scale(1.15)">${WORTEL.svg}</g>`,w:800,h:800,ml:230,mr:250,fs:22,r:12,gap:42,
  punten:[
    {naam:'wortelhaartjes',x:-60+1.15*700,y:-60+1.15*262,kant:'r',info:'Een lange, dunne uitstulping van een epidermiscel. Duizenden wortelhaartjes geven een <b>grote oppervlakte</b> om water en mineralen op te nemen.'},
    {naam:'epidermis',x:-60+1.15*636,y:-60+1.15*455,kant:'r',info:'De buitenste cellaag van de wortel. Sommige cellen vormen een wortelhaartje.'},
    {naam:'cortex',x:-60+1.15*540,y:-60+1.15*560,kant:'r',info:'Grote parenchymcellen. Het water gaat door de cortex naar het midden van de wortel.'},
    {naam:'houtvaten',x:-60+1.15*430,y:-60+1.15*430,kant:'l',ly:450,info:'In het midden liggen de houtvaten in een <b>ster</b>. Ze vervoeren water en mineralen <b>omhoog</b> naar de stengel.'},
    {naam:'zeefvaten',x:-60+1.15*448,y:-60+1.15*400,kant:'r',ly:360,info:'Tussen de armen van de ster liggen de zeefvaten. Ze brengen <b>assimilaten</b> uit het blad naar de wortel.'},
    {naam:'vaatbundel',x:-60+1.15*400,y:-60+1.15*318,kant:'l',ly:330,info:'In de wortel ligt één vaatbundel in het midden (centrale cilinder), met houtvaten en zeefvaten naast elkaar.'},
  ]});

//////////////////// HUIDMONDJES ////////////////////
(function(){
  const s=$('svg-stoma'), read=$('stoma-read');
  let licht=1, water=1, o=0.9, deeltjes=[];
  document.querySelectorAll('[data-licht]').forEach(b=>b.onclick=()=>{ licht=+b.dataset.licht; document.querySelectorAll('[data-licht]').forEach(x=>x.classList.toggle('on',x===b)); upd(); });
  document.querySelectorAll('[data-water]').forEach(b=>b.onclick=()=>{ water=+b.dataset.water; document.querySelectorAll('[data-water]').forEach(x=>x.classList.toggle('on',x===b)); upd(); });
  const doel=()=>licht&&water?1:0.04;
  function upd(){
    const open=doel()>0.5;
    read.innerHTML=open?'<b>Het huidmondje is open.</b><br>Er is licht en genoeg water. De sluitcellen nemen water op in hun <b>vacuole</b>: de <b>turgor</b> stijgt. Omdat hun binnenwand dikker is, buigen ze uit elkaar.<br>CO₂ komt binnen voor de fotosynthese. O₂ en waterdamp gaan naar buiten.':
      (water?'<b>Het huidmondje is gesloten.</b><br>In het donker is er geen fotosynthese, dus geen CO₂ nodig. De sluitcellen verliezen water: de vacuole krimpt, de <b>turgor daalt</b> en de opening sluit.':'<b>Het huidmondje is gesloten.</b><br>Bij <b>watertekort</b> verliezen de sluitcellen water: de vacuole krimpt, de <b>turgor daalt</b> en het huidmondje sluit. Zo verliest de plant <b>minder water</b> door verdamping. Dit is een <b>negatief feedbacksysteem</b>.');
  }
  const C=[410,260];
  function cel(k,rxo,ryo,rxp,ryp){ // k=-1 links, 1 rechts
    const sw0=k<0?0:1, sw1=k<0?1:0;
    return `M${C[0]},${C[1]-ryo} A${rxo},${ryo} 0 0 ${sw0} ${C[0]},${C[1]+ryo} L${C[0]},${C[1]+ryp} A${rxp},${ryp} 0 0 ${sw1} ${C[0]},${C[1]-ryp}Z`;
  }
  const bg=`<rect width="820" height="520" fill="#e9f2dc"/><path d="${EPI.d}" fill="none" stroke="#86a65f" stroke-width="5" stroke-linejoin="round"/><path d="${EPI.d}" fill="none" stroke="#c9dfae" stroke-width="1.6" stroke-linejoin="round"/>
    <ellipse cx="410" cy="260" rx="118" ry="128" fill="#e3eed3" stroke="#86a65f" stroke-width="4"/>`;
  lus('p3',(dt,now)=>{
    o+=(doel()-o)*Math.min(1,dt*1.6);
    const ryo=112, rxo=62+20*o, ryp=82, rxp=3+22*o;
    let h=bg;
    for(const k of [-1,1]){
      h+=`<path d="${cel(k,rxo,ryo,rxp,ryp)}" fill="#9fcf6c" stroke="#3d6b22" stroke-width="3"/>`;
      // vacuole
      const vx=rxo-15, vp=rxp+9, vy=ryo-22, vpy=ryp-12, sc=0.55+0.45*o;
      h+=`<path d="${cel(k,rxp+(vx-rxp)*1, vy, vp, vpy)}" fill="#b9e3f0" opacity="${0.35+0.55*o}" transform="translate(${k*(1-sc)*8},0)"/>`;
      // bladgroenkorrels
      for(let i=0;i<8;i++){ const th=(k<0?Math.PI:0)+(-1.05+i*0.3)*(k<0?1:-1), r1=(rxo+rxp)/2, r2=(ryo+ryp)/2+8;
        const x=C[0]+Math.cos(th)*r1*(k<0?1:1), y=C[1]+Math.sin(th)*r2*0.9; h+=`<ellipse cx="${x}" cy="${y}" rx="7" ry="4.5" transform="rotate(${th*57.3+90} ${x} ${y})" fill="#3f8f34" stroke="#255c1d" stroke-width="1"/>`; }
      // kern
      h+=`<ellipse cx="${C[0]+k*(rxo-10)*0.62}" cy="${C[1]+4}" rx="9" ry="12" fill="#c9a36b" stroke="#7a5a2c" stroke-width="1.5"/>`;
    }
    // dikke binnenwand + opening
    h+=`<ellipse cx="${C[0]}" cy="${C[1]}" rx="${rxp}" ry="${ryp}" fill="#1f2a15" stroke="#2c5a1a" stroke-width="7"/>`;
    h+=`<path d="M${C[0]},${C[1]-ryo} V${C[1]-ryp} M${C[0]},${C[1]+ryp} V${C[1]+ryo}" stroke="#3d6b22" stroke-width="3"/>`;
    // gassen
    if(o>0.5 && Math.random()<dt*9){ const in_=Math.random()<0.45, a=Math.random()*6.28;
      deeltjes.push({in:in_,soort:in_?'CO₂':(Math.random()<0.55?'H₂O':'O₂'),a,t:0}); }
    deeltjes.forEach(d=>d.t+=dt*0.45); deeltjes=deeltjes.filter(d=>d.t<1);
    deeltjes.forEach(d=>{ const r=d.in?(1-d.t)*230+10:d.t*230+10, x=C[0]+Math.cos(d.a)*r*0.9, y=C[1]+Math.sin(d.a)*r*0.75, op=d.in?Math.min(1,(1-d.t)*3):Math.min(1,d.t*3)*(1-d.t*0.6);
      const kl=d.soort==='CO₂'?'#475569':d.soort==='O₂'?'#dc2626':'#2563eb';
      h+=`<g opacity="${op}"><circle cx="${x}" cy="${y}" r="13" fill="#fff" stroke="${kl}" stroke-width="2"/><text x="${x}" y="${y+4}" text-anchor="middle" font-size="10" font-weight="700" fill="${kl}">${d.soort}</text></g>`; });
    // labels
    h+=`<g font-size="15" font-weight="700" fill="#1D2A36" stroke="#fff" stroke-width="4" paint-order="stroke"><text x="${C[0]-rxo-150}" y="120">sluitcel</text><text x="${C[0]+130}" y="470">opening</text><text x="40" y="490">epidermiscellen</text></g>
      <path d="M${C[0]-rxo-90},126 L${C[0]-rxo+10},${C[1]-40}" stroke="#1D2A36" stroke-width="1.5"/><path d="M${C[0]+128},464 L${C[0]+3},${C[1]+30}" stroke="#1D2A36" stroke-width="1.5"/>`;
    h+=`<g transform="translate(640,30)"><rect width="160" height="58" rx="8" fill="#fff" opacity=".9"/><text x="12" y="24" font-size="14" font-weight="700">turgor</text><rect x="12" y="34" width="136" height="12" rx="6" fill="#e2e8f0"/><rect x="12" y="34" width="${136*(0.15+0.85*o)}" height="12" rx="6" fill="#2563eb"/></g>`;
    s.innerHTML=h;
  });
  upd();
})();

//////////////////// TRANSPORT ////////////////////
(function(){
  const s=$('svg-transport'), read=$('tr-read'), lijst=$('tr-stappen');
  let wat='water', stap=0, deel=[];
  const ST={water:[
    ['Opname','De <b>wortelhaartjes</b> nemen water en mineralen op uit de bodem.',[[300,560,120]]],
    ['Door de cortex','Het water gaat door de cortex van de wortel naar de <b>houtvaten</b> in het midden.',[[320,470,70]]],
    ['Opwaarts transport','In de <b>houtvaten</b> stijgt het water door wortel en stengel omhoog: <b>opwaarts transport</b>.',[[322,240,60]]],
    ['Verdamping','In het blad gaat het water naar de cellen. Een deel <b>verdampt</b> via de <b>huidmondjes</b>. Die verdamping zuigt nieuw water omhoog.',[[470,250,90],[180,200,80]]]],
   assim:[
    ['Fotosynthese','In de bladgroenkorrels van het blad maakt de plant <b>glucose</b> met licht, CO₂ en water.',[[470,250,90],[180,200,80]]],
    ['Zeefvaten','De assimilaten gaan via de <b>zeefvaten</b> uit het blad naar de stengel.',[[330,250,60]]],
    ['Neerwaarts','Een groot deel gaat <b>neerwaarts</b> naar de wortel. Daar wordt het opgeslagen, bv. als <b>zetmeel</b>.',[[320,500,110]]],
    ['Ook opwaarts','Een deel gaat naar de <b>bloem</b> en later naar zaden en vruchten. Assimilaten zijn <b>glucose, zetmeel, eiwitten en vetten</b>.',[[320,80,60]]]]};
  ST.beide=ST.water.map((x,i)=>i===2?['Twee richtingen','Water gaat <b>opwaarts</b> door de houtvaten. Assimilaten gaan <b>vooral neerwaarts</b> door de zeefvaten.',[[322,300,90]]]:x).slice(0,3);
  document.querySelectorAll('[data-tr]').forEach(b=>b.onclick=()=>{ wat=b.dataset.tr; stap=0; deel=[]; document.querySelectorAll('[data-tr]').forEach(x=>x.classList.toggle('on',x===b)); bouw(); });
  function bouw(){ lijst.innerHTML=ST[wat].map((x,i)=>`<button class="btn${i===stap?' on':''}" data-st="${i}">${i+1}. ${x[0]}</button>`).join(''); lijst.querySelectorAll('[data-st]').forEach(b=>b.onclick=()=>{ stap=+b.dataset.st; bouw(); }); read.innerHTML=ST[wat][stap][1]; }
  // paden
  const W=PLANT.wortels, B=PLANT.bladen, stam=PLANT.stam;
  const tips=W.filter((w,i)=>i>0).map(w=>w.pts.slice().reverse());
  function stamTussen(y1,y2){ const n=24, out=[]; for(let i=0;i<=n;i++){ const y=y1+(y2-y1)*i/n, t=(PLANT.GY-y)/292; out.push(stam(Math.max(0,Math.min(1,t)))); } return out; }
  const naarBlad=b=>[...stamTussen(PLANT.GY,b.y0),[b.st[0],b.st[1]],...b.nerf];
  const waterPaden=[]; tips.forEach((tp,i)=>{ const b=B[i%B.length]; const hoofd=W[0].pts; const j=hoofd.reduce((bi,p,k)=>Math.hypot(p[0]-tp[tp.length-1][0],p[1]-tp[tp.length-1][1])<Math.hypot(hoofd[bi][0]-tp[tp.length-1][0],hoofd[bi][1]-tp[tp.length-1][1])?k:bi,0);
    waterPaden.push([...tp,...hoofd.slice(0,j+1).reverse(),...naarBlad(b)]); });
  waterPaden.push([...W[0].pts.slice().reverse(),...naarBlad(B[3])]);
  const assPaden=[]; B.forEach((b,i)=>{ const terug=[...b.nerf.slice().reverse(),b.st,[b.x0,b.y0]];
    const naarOnder=[...stamTussen(b.y0,PLANT.GY),...W[0].pts.slice(0,8)]; assPaden.push([...terug,...naarOnder]);
    if(i>=2) assPaden.push([...terug,...stamTussen(b.y0,stam(1)[1]+10)]); });
  const lengte=p=>{ let L=0; for(let i=1;i<p.length;i++) L+=Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]); return L; };
  const op=(p,f)=>{ let L=lengte(p)*f; for(let i=1;i<p.length;i++){ const d=Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]); if(L<=d){ const u=L/d; return [p[i-1][0]+(p[i][0]-p[i-1][0])*u,p[i-1][1]+(p[i][1]-p[i-1][1])*u]; } L-=d; } return p[p.length-1]; };
  const basis=PLANT.svg('b');
  lus('p6',(dt,now)=>{
    const water=wat!=='assim', ass=wat!=='water';
    if(water&&Math.random()<dt*14){ const p=waterPaden[Math.floor(Math.random()*waterPaden.length)]; deel.push({p,f:0,v:42/lengte(p),k:'#2563eb'}); }
    if(ass&&Math.random()<dt*9){ const p=assPaden[Math.floor(Math.random()*assPaden.length)]; deel.push({p,f:0,v:36/lengte(p),k:'#d97706'}); }
    deel.forEach(d=>d.f+=d.v*dt); deel=deel.filter(d=>d.f<1);
    let h=basis;
    ST[wat][stap][2].forEach(([x,y,r])=>h+=`<circle cx="${x}" cy="${y}" r="${r}" fill="#fde68a" opacity=".28" stroke="#d97706" stroke-width="2" stroke-dasharray="6 5"/>`);
    deel.forEach(d=>{ const [x,y]=op(d.p,d.f); h+=d.k==='#2563eb'?`<path d="M${x},${y-5} q4,5 0,8 q-4,-3 0,-8z" fill="${d.k}" stroke="#fff" stroke-width=".8"/>`:`<rect x="${x-3}" y="${y-3}" width="6" height="6" fill="${d.k}" stroke="#fff" stroke-width=".8" transform="rotate(45 ${x} ${y})"/>`; });
    if(water&&stap===ST[wat].length-1&&wat==='water') for(let i=0;i<5;i++){ const t=((now/1000+i*0.4)%2)/2; h+=`<text x="${150+i*90+Math.sin(i)*20}" y="${170-t*90}" font-size="13" fill="#2563eb" opacity="${1-t}">H₂O</text>`; }
    s.innerHTML=h;
  });
  bouw();
})();
