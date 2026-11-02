const POS='#d64550', NEG='#2a6f97';
function teken(ctx,x,y,s,r=8){ ctx.save(); ctx.fillStyle=s>0?POS:NEG; ctx.beginPath(); ctx.arc(x,y,r,0,7); ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=Math.max(1.5,r/4); ctx.beginPath(); ctx.moveTo(x-r*0.55,y); ctx.lineTo(x+r*0.55,y); if(s>0){ ctx.moveTo(x,y-r*0.55); ctx.lineTo(x,y+r*0.55); } ctx.stroke(); ctx.restore(); }
function bg(ctx,W,H,c='#fff'){ ctx.clearRect(0,0,W,H); ctx.fillStyle=c; ctx.fillRect(0,0,W,H); }
const ease=t=>t<0?0:t>1?1:t*t*(3-2*t);
function lus(id,fn){ (function f(now){ if(isActive(id)) fn(now); requestAnimationFrame(f); })(performance.now()); }
const sup=n=>String(n).replace(/-/g,'⁻').replace(/\d/g,d=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[d]);

//////////////////// 1 — ELEMENTAIRE LADING ////////////////////
(function(){
  const c=document.getElementById('c-l1'), ctx=hiDPI(c), W=c._w, H=c._h;
  const EL=['','waterstof (H)','helium (He)','lithium (Li)','beryllium (Be)','boor (B)','koolstof (C)','stikstof (N)','zuurstof (O)','fluor (F)','neon (Ne)','natrium (Na)'];
  const Zs=document.getElementById('l1-Z'); let Z=3, e=3;
  Zs.oninput=()=>{ Z=+Zs.value; e=Z; draw(); };
  document.getElementById('l1-plus').onclick=()=>{ if(e<Math.min(18,Z+3)) e++; draw(); };
  document.getElementById('l1-min').onclick=()=>{ if(e>0) e--; draw(); };
  function draw(){
    document.getElementById('l1-Z-l').textContent='Element: '+EL[Z]+' · Z = '+Z;
    bg(ctx,W,H); const cx=270, cy=210, RS=[70,120,170], CAP=[2,8,8];
    RS.forEach(r=>{ ctx.strokeStyle='#CBD5E1'; ctx.lineWidth=1.5; ctx.setLineDash([4,5]); ctx.beginPath(); ctx.arc(cx,cy,r,0,7); ctx.stroke(); }); ctx.setLineDash([]);
    // kern
    const g=ctx.createRadialGradient(cx-8,cy-8,4,cx,cy,34); g.addColorStop(0,'#fca5a5'); g.addColorStop(1,'#b91c1c'); ctx.fillStyle=g; ctx.beginPath(); ctx.arc(cx,cy,32,0,7); ctx.fill();
    text(ctx,Z+' p⁺',cx,cy+5,{color:'#fff',weight:700,align:'center',size:15});
    let rest=e; RS.forEach((r,k)=>{ const n=Math.min(CAP[k],rest); rest-=n; for(let i=0;i<n;i++){ const a=-Math.PI/2+i*2*Math.PI/n+k*0.3; teken(ctx,cx+r*Math.cos(a),cy+r*Math.sin(a),-1,9); } });
    const net=Z-e;
    text(ctx,'protonen (+)',520,120,{color:'#51606E'}); text(ctx,String(Z),740,120,{weight:700,align:'right',color:POS,size:18});
    text(ctx,'elektronen (−)',520,160,{color:'#51606E'}); text(ctx,String(e),740,160,{weight:700,align:'right',color:NEG,size:18});
    ctx.strokeStyle='#CBD5E1'; ctx.beginPath(); ctx.moveTo(520,180); ctx.lineTo(740,180); ctx.stroke();
    text(ctx,'netto',520,210,{color:'#51606E'}); text(ctx,(net>0?'+':net<0?'−':'')+Math.abs(net)+' e',740,210,{weight:700,align:'right',size:18,color:net>0?POS:net<0?NEG:'#1D2A36'});
    text(ctx,net===0?'neutraal':net>0?'positief geladen':'negatief geladen',630,260,{weight:700,align:'center',size:18,color:net>0?POS:net<0?NEG:'#1D2A36'});
    const Q=net===0?'0 C':(net>0?'+':'−')+nl(Math.abs(net)*1.6,1)+' · 10⁻¹⁹ C';
    document.getElementById('l1-read').innerHTML=(net===0?'Evenveel protonen als elektronen: het atoom is <b>neutraal</b>.':net>0?'<b>Elektronentekort</b> van '+net+': het deeltje is <b>positief</b> geladen (positief ion).':'<b>Elektronenoverschot</b> van '+(-net)+': het deeltje is <b>negatief</b> geladen (negatief ion).')+'<br>Q = n · e = '+(net>=0?net:'−'+(-net))+' · 1,6 · 10⁻¹⁹ C = <b>'+Q+'</b>';
  }
  draw();
})();

//////////////////// 2 — GELEIDERS EN ISOLATOREN ////////////////////
(function(){
  const c=document.getElementById('c-l2'), ctx=hiDPI(c), W=c._w, H=c._h;
  const MAT=[{n:'koper',g:true,k:'#d97706'},{n:'aluminium',g:true,k:'#9ca3af'},{n:'PVC',g:false,k:'#e5e7eb'},{n:'glas',g:false,k:'#bae6fd'},{n:'droog hout',g:false,k:'#d6a56b'}];
  let m=0, t0=null; const box=document.getElementById('l2-mat'), read=document.getElementById('l2-read');
  MAT.forEach((q,i)=>{ const b=document.createElement('button'); b.className='btn'; b.textContent=q.n; b.onclick=()=>{ m=i; t0=null; upd(); }; box.appendChild(b); });
  document.getElementById('l2-raak').onclick=()=>{ t0=performance.now(); upd(); };
  document.getElementById('l2-reset').onclick=()=>{ t0=null; upd(); };
  function upd(){ [...box.children].forEach((b,i)=>b.classList.toggle('on',i===m));
    const q=MAT[m]; read.innerHTML=t0==null?'<b>'+q.n+'</b> is een <b>'+(q.g?'geleider':'isolator')+'</b>. Klik op <b>Aanraken</b>.':
      (q.g?'<b>Geleider:</b> de extra elektronen stoten elkaar af en kunnen vrij bewegen. Ze verspreiden zich over het <b>hele</b> oppervlak van de staaf.':'<b>Isolator:</b> de elektronen kunnen niet vrij bewegen. De lading blijft op de plaats waar je de staaf aanraakte.'); }
  const N=10;
  lus('l2',now=>{
    const q=MAT[m], t=t0==null?0:Math.min(1,(now-t0)/3000);
    bg(ctx,W,H); const x0=170,x1=690,y=200;
    ctx.fillStyle=q.k; ctx.strokeStyle='#475569'; ctx.lineWidth=2; roundRect(ctx,x0,y-26,x1-x0,52,10); ctx.fill(); ctx.stroke();
    text(ctx,q.n+' ('+(q.g?'geleider':'isolator')+')',(x0+x1)/2,y+60,{align:'center',weight:700});
    // geladen bol
    const ph=ease(t/0.3), weg=ease((t-0.4)/0.25), bx=x0-60+ph*28-weg*60;
    ctx.fillStyle='#e2e8f0'; ctx.strokeStyle='#475569'; ctx.beginPath(); ctx.arc(bx-10,y,30,0,7); ctx.fill(); ctx.stroke();
    const over=t<0.32?N:0; for(let i=0;i<4;i++) teken(ctx,bx-10+Math.cos(i*1.6)*15,y+Math.sin(i*1.6)*15,-1,6);
    // elektronen op de staaf
    if(t>=0.32){ const s=ease((t-0.4)/0.6);
      for(let i=0;i<N;i++){ const sx=x0+14+(i%5)*10, sy=y+(i<5?-12:12);
        const tx=q.g?x0+24+(i%5)*((x1-x0-48)/4.5)+(i<5?0:(x1-x0-48)/9):sx, ty=q.g?y+(i<5?-14:14):sy;
        teken(ctx,sx+(tx-sx)*s,sy+(ty-sy)*s,-1,7); } }
  });
  upd();
})();

//////////////////// 3 — AARDING ////////////////////
(function(){
  const c=document.getElementById('c-l3'), ctx=hiDPI(c), W=c._w, H=c._h;
  let s=-1, t0=null; const read=document.getElementById('l3-read'), N=8;
  document.querySelectorAll('[data-l3]').forEach(b=>b.onclick=()=>{ s=+b.dataset.l3; t0=null; document.querySelectorAll('[data-l3]').forEach(o=>o.classList.toggle('on',o===b)); upd(); });
  document.getElementById('l3-aard').onclick=()=>{ t0=performance.now(); upd(); };
  function upd(){ read.innerHTML=t0==null?(s<0?'De bol heeft een <b>overschot</b> aan elektronen.':'De bol heeft een <b>tekort</b> aan elektronen.')+' Verbind de bol met de aarde.':
    (s<0?'De extra elektronen stoten elkaar af en stromen <b>van de bol naar de aarde</b>.':'Elektronen stromen <b>van de aarde naar de bol</b> en vullen het tekort aan.')+' Daarna is de bol <b>neutraal</b>.'; }
  const pad=[[380,170],[600,170],[600,320]];
  function op(u){ const L1=220,L2=150,d=u*(L1+L2); return d<L1?[380+d,170]:[600,170+(d-L1)]; }
  lus('l3',now=>{
    const t=t0==null?-1:(now-t0)/1000;
    bg(ctx,W,H); ctx.fillStyle='#E7DCC8'; ctx.fillRect(0,340,W,60); text(ctx,'aarde',700,375,{color:'#7c5e2f',weight:700});
    ctx.fillStyle='#94a3b8'; ctx.fillRect(312,230,16,110); text(ctx,'isolerende voet',320,360,{align:'center',size:12,color:'#51606E'});
    ctx.fillStyle='#e2e8f0'; ctx.strokeStyle='#475569'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(320,170,62,0,7); ctx.fill(); ctx.stroke();
    // draad + schakelaar
    ctx.strokeStyle='#1D2A36'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(382,170); ctx.lineTo(480,170); ctx.moveTo(530,170); ctx.lineTo(600,170); ctx.lineTo(600,330); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(480,170); if(t>=0) ctx.lineTo(530,170); else ctx.lineTo(525,145); ctx.stroke();
    ctx.beginPath(); [0,1,2].forEach(i=>{ ctx.moveTo(600-22+i*7,330+i*7); ctx.lineTo(600+22-i*7,330+i*7); }); ctx.stroke();
    const k=t<0?0:Math.min(N,Math.floor(t/0.45));
    for(let i=0;i<N;i++){ const a=i*2*Math.PI/N; const x=320+38*Math.cos(a), y=170+38*Math.sin(a);
      if(s<0){ if(i>=k) teken(ctx,x,y,-1,9); } else { if(i>=k) teken(ctx,x,y,1,9); } }
    if(t>=0) for(let i=0;i<N;i++){ const u=(t-i*0.45)/0.9; if(u>0&&u<1){ const p=op(s<0?u:1-u); teken(ctx,p[0],p[1],-1,7); } }
    text(ctx,'lading op de bol: '+(N-k===0?'0 (neutraal)':(s<0?'−':'+')+(N-k)+' e'),320,70,{align:'center',weight:700,color:N-k===0?'#1D2A36':s<0?NEG:POS});
  });
  upd();
})();

//////////////////// 4 — WRIJVING ////////////////////
(function(){
  const c=document.getElementById('c-l4'), ctx=hiDPI(c), W=c._w, H=c._h;
  const R=[['glas','#bae6fd'],['menselijk haar','#92400e'],['nylon','#e9d5ff'],['wol','#f5f0e1'],['zijde','#fde68a'],['papier','#ffffff'],['katoen','#f1f5f9'],['hout','#d6a56b'],['barnsteen','#f59e0b'],['rubber (ballon)','#fca5a5'],['polyester','#c7d2fe'],['PVC (plastic)','#e5e7eb']];
  const A=document.getElementById('l4-a'), B=document.getElementById('l4-b'), read=document.getElementById('l4-read');
  R.forEach((r,i)=>{ A.add(new Option(r[0],i)); B.add(new Option(r[0],i)); }); A.value=3; B.value=9;
  let t0=null; A.onchange=B.onchange=()=>{ t0=null; upd(); };
  document.getElementById('l4-wrijf').onclick=()=>{ t0=performance.now(); upd(); };
  document.getElementById('l4-reset').onclick=()=>{ t0=null; upd(); };
  const n=()=>{ const d=Math.abs(+A.value-+B.value); return d===0?0:Math.min(6,2+Math.floor(d/2)); };
  function upd(){ const a=+A.value,b=+B.value;
    if(a===b){ read.innerHTML='Twee keer dezelfde stof: er gaan <b>geen</b> elektronen over.'; return; }
    const hoog=a<b?a:b, laag=a<b?b:a;
    read.innerHTML=t0==null?'Klik op <b>Wrijven</b>.':'<b>'+R[hoog][0]+'</b> staat hoger in de reeks: het <b>verliest</b> elektronen en wordt <b>positief</b>.<br><b>'+R[laag][0]+'</b> staat lager: het <b>krijgt</b> elektronen en wordt <b>negatief</b>.<br><span class="k">Hoe verder de stoffen uit elkaar staan, hoe meer lading er overgaat. Er ontstaat geen nieuwe lading: '+n()+' elektronen verhuizen.</span>'; }
  lus('l4',now=>{
    const a=+A.value,b=+B.value, t=t0==null?-1:(now-t0)/2600;
    bg(ctx,W,H);
    // reeks
    text(ctx,'+  geeft gemakkelijk elektronen af',30,28,{size:12,weight:700,color:POS});
    R.forEach((r,i)=>{ const y=50+i*29, on=i===a||i===b; ctx.fillStyle=on?'#E4EEF8':'#F5F8FB'; ctx.strokeStyle=on?'#2F6FB0':'#D3DCE5'; ctx.lineWidth=on?2:1; roundRect(ctx,30,y,190,24,6); ctx.fill(); ctx.stroke(); text(ctx,r[0],42,y+17,{size:13,weight:on?700:500}); });
    text(ctx,'−  neemt gemakkelijk elektronen op',30,50+12*29+14,{size:12,weight:700,color:NEG});
    // blokken
    const wr=t>0&&t<0.7?Math.sin(t*60)*14:0;
    const blok=(x,i,dy)=>{ ctx.fillStyle=R[i][1]; ctx.strokeStyle='#475569'; ctx.lineWidth=2; roundRect(ctx,x,130+dy,150,200,10); ctx.fill(); ctx.stroke(); text(ctx,R[i][0],x+75,120+dy,{align:'center',weight:700}); };
    blok(330,a,wr); blok(482,b,0);
    const hoog=a<b?'A':'B', k=a===b?0:n(), prog=t<0?0:Math.min(1,Math.max(0,(t-0.15)/0.7));
    const paren=(x,dy,wie)=>{ for(let r=0;r<6;r++) for(let q=0;q<2;q++){ const id=r*2+q, px=x+40+q*70, py=160+r*30+dy;
        ctx.fillStyle=POS; text(ctx,'+',px-10,py+5,{weight:700,color:POS,size:15});
        const weg=wie===hoog&&id<k; if(!weg) teken(ctx,px+12,py,-1,7); } };
    paren(330,wr,'A'); paren(482,0,'B');
    for(let i=0;i<k;i++){ const r=Math.floor(i/2),q=i%2, fromX=(hoog==='A'?330:482)+40+q*70+12, fromY=160+r*30+(hoog==='A'?wr:0);
      const toX=(hoog==='A'?482+16:330+134), toY=160+i*30;
      if(prog<1){ const u=ease(prog*1.2-i*0.03); teken(ctx,fromX+(toX-fromX)*u,fromY+(toY-fromY)*u,-1,7); } else teken(ctx,toX,toY,-1,7); }
    // samenvatting
    if(prog>=1&&k>0){ const tA=hoog==='A'?'+':'−', tB=hoog==='A'?'−':'+';
      text(ctx,'netto '+tA+k+' e',405,365,{align:'center',weight:700,size:16,color:tA==='+'?POS:NEG}); text(ctx,'netto '+tB+k+' e',557,365,{align:'center',weight:700,size:16,color:tB==='+'?POS:NEG}); }
  });
  upd();
})();

//////////////////// 5 — INFLUENTIE EN POLARISATIE ////////////////////
(function(){
  const c=document.getElementById('c-l5'), ctx=hiDPI(c), W=c._w, H=c._h;
  let soort='geleider'; const ds=document.getElementById('l5-d'), read=document.getElementById('l5-read');
  document.querySelectorAll('[data-l5]').forEach(b=>b.onclick=()=>{ soort=b.dataset.l5; document.querySelectorAll('[data-l5]').forEach(o=>o.classList.toggle('on',o===b)); draw(); });
  ds.oninput=draw;
  function draw(){
    const d=+ds.value, f=Math.max(0,1-d/100)**1.2, tip=400-d*2.6, cy=190;
    bg(ctx,W,H);
    ctx.fillStyle='#e5e7eb'; ctx.strokeStyle='#475569'; ctx.lineWidth=2; roundRect(ctx,tip-300,cy-18,300,36,10); ctx.fill(); ctx.stroke();
    for(let i=0;i<7;i++) teken(ctx,tip-30-i*38,cy,-1,8); text(ctx,'negatief geladen staaf',tip-150,cy-30,{align:'center',size:13,weight:700});
    const ox=570;
    if(soort==='geleider'){
      const R=90; ctx.fillStyle='#e2e8f0'; ctx.beginPath(); ctx.arc(ox,cy,R,0,7); ctx.fill(); ctx.stroke();
      for(let i=0;i<8;i++){ const a=i*Math.PI/4+Math.PI/8; const px=ox+0.62*R*Math.cos(a), py=cy+0.62*R*Math.sin(a);
        text(ctx,'+',px,py+6,{align:'center',weight:700,color:POS,size:18});
        const ta=-1.1+ (i/7)*2.2, tx=ox+0.82*R*Math.cos(ta), ty=cy+0.82*R*Math.sin(ta), sx=px+14, sy=py;
        teken(ctx,sx+(tx-sx)*f,sy+(ty-sy)*f,-1,8); }
      text(ctx,'metalen bol op isolerende voet',ox,cy+R+28,{align:'center',size:13,weight:700});
    } else {
      ctx.fillStyle='#fffdf5'; ctx.strokeStyle='#94a3b8'; roundRect(ctx,ox-110,cy-80,220,160,6); ctx.fill(); ctx.stroke();
      for(let r=0;r<3;r++) for(let q=0;q<4;q++){ const mx=ox-75+q*50, my=cy-48+r*48, sp=4+10*f;
        ctx.fillStyle='#f1f5f9'; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.ellipse(mx,my,12+sp*0.7,12,0,0,7); ctx.fill(); ctx.stroke();
        text(ctx,'+',mx-sp*0.7,my+5,{align:'center',weight:700,color:POS,size:13}); text(ctx,'−',mx+sp*0.7,my+5,{align:'center',weight:700,color:NEG,size:13}); }
      text(ctx,'papiersnipper (vergroot: moleculen)',ox,cy+108,{align:'center',size:13,weight:700});
    }
    if(f>0.05){ const L=20+90*f*f; arrow(ctx,ox-(soort==='geleider'?100:120),cy+60,ox-(soort==='geleider'?100:120)-L,cy+60,'#1D4ED8',4,'F',0,-10); }
    read.innerHTML=(soort==='geleider'?'<b>Influentie:</b> de vrije elektronen worden <b>afgestoten</b> naar de verre kant. Aan de kant van de staaf blijft een <b>positieve</b> lading over. De bol is nog altijd neutraal.':'<b>Polarisatie:</b> er zijn geen vrije elektronen. In elke molecule schuiven de elektronen een klein beetje weg van de staaf. De moleculen worden kleine <b>dipolen</b>.')+'<br>De + kant ligt het dichtst bij de staaf. De aantrekking is daardoor groter dan de afstoting: het voorwerp wordt <b>aangetrokken</b>.'+(f<0.05?'<br><span class="k">Schuif de staaf dichterbij.</span>':'');
  }
  draw();
})();

//////////////////// 6 — BLIKSEM ////////////////////
(function(){
  const c=document.getElementById('c-l6'), ctx=hiDPI(c), W=c._w, H=c._h;
  const ST=['Ladingen in de wolk','Influentie in de grond','Ontlading','Bliksemafleider'];
  const TX=['In een onweerswolk botsen ijskristallen en hagelkorrels. Daarbij gaan elektronen over (wrijving). De <b>onderkant</b> van de wolk wordt <b>negatief</b>, de bovenkant positief.',
    'De negatieve onderkant van de wolk <b>stoot elektronen af</b> in de grond eronder. Het aardoppervlak onder de wolk wordt daardoor <b>positief</b>: dat is <b>influentie</b>.',
    'Wordt het ladingsverschil groot genoeg, dan wordt de lucht even <b>geleidend</b>. Elektronen springen van de wolk naar de aarde: de <b>bliksem</b>. De lucht wordt zo heet dat ze ontploffend uitzet: dat hoor je als <b>donder</b>.',
    'Een <b>bliksemafleider</b> is een metalen spits op het dak, met een dikke geleider verbonden met de aarde. De bliksem slaat in op de spits en de lading wordt via de geleider veilig naar de <b>aarde</b> afgevoerd (aarding). Zo gaat de stroom niet door het huis.'];
  let s=0; const box=document.getElementById('l6-stap');
  ST.forEach((n,i)=>{ const b=document.createElement('button'); b.className='btn'; b.textContent=(i+1)+'. '+n; b.onclick=()=>{ s=i; upd(); }; box.appendChild(b); });
  function upd(){ [...box.children].forEach((b,i)=>b.classList.toggle('on',i===s)); document.getElementById('l6-read').innerHTML=TX[s]; }
  function bolt(x0,y0,x1,y1,seed){ ctx.strokeStyle='#fde047'; ctx.lineWidth=5; ctx.shadowColor='#fef08a'; ctx.shadowBlur=18; ctx.beginPath(); ctx.moveTo(x0,y0); const n=9; for(let i=1;i<n;i++){ const u=i/n; ctx.lineTo(x0+(x1-x0)*u+Math.sin(seed*7+i*3.1)*22,y0+(y1-y0)*u); } ctx.lineTo(x1,y1); ctx.stroke(); ctx.shadowBlur=0; ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.stroke(); }
  lus('l6',now=>{
    const fl=(Math.floor(now/110)%7)<4;
    const g=ctx.createLinearGradient(0,0,0,H); g.addColorStop(0,s>=2&&fl?'#64748b':'#334155'); g.addColorStop(1,'#94a3b8'); ctx.fillStyle=g; ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#6b7280'; [[300,90,120,48],[400,70,130,56],[500,95,120,46],[400,120,190,44]].forEach(([x,y,rx,ry])=>{ ctx.beginPath(); ctx.ellipse(x,y,rx,ry,0,0,7); ctx.fill(); });
    for(let i=0;i<7;i++) teken(ctx,260+i*48,62,1,8); for(let i=0;i<8;i++) teken(ctx,235+i*48,140,-1,9);
    ctx.fillStyle='#3f6212'; ctx.fillRect(0,360,W,80);
    // huis
    ctx.fillStyle='#e7e5e4'; ctx.fillRect(560,290,120,70); ctx.fillStyle='#b45309'; ctx.beginPath(); ctx.moveTo(550,292); ctx.lineTo(620,240); ctx.lineTo(690,292); ctx.fill();
    if(s===3){ ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(620,240); ctx.lineTo(620,205); ctx.moveTo(620,240); ctx.lineTo(690,292); ctx.lineTo(700,292); ctx.lineTo(700,380); ctx.stroke(); text(ctx,'bliksemafleider',630,200,{color:'#fff',weight:700,size:13}); }
    if(s>=1) for(let i=0;i<9;i++) teken(ctx,200+i*50,372,1,8);
    if(s===2&&fl){ bolt(380,160,360,362,Math.floor(now/90)); text(ctx,'e⁻ ↓',395,260,{color:'#fff',weight:700}); }
    if(s===3&&fl){ bolt(560,150,620,205,Math.floor(now/90)); arrow(ctx,712,300,712,370,'#fde047',3); }
    text(ctx,'wolk',620,60,{color:'#fff',weight:700}); text(ctx,'aarde',30,400,{color:'#fff',weight:700});
  });
  upd();
})();

//////////////////// 7 — FOTOKOPIEERTOESTEL ////////////////////
(function(){
  const c=document.getElementById('c-l7'), ctx=hiDPI(c), W=c._w, H=c._h;
  const E=['11111','10000','10000','11110','10000','10000','11111'];
  const ST=['Opladen','Belichten','Toner','Naar het papier','Fixeren'];
  const TX=['De trommel wordt in het donker overal <b>positief</b> geladen. De fotogeleidende laag is nu een isolator, dus de lading blijft zitten.',
    'Een lamp verlicht het origineel. De <b>witte</b> delen weerkaatsen licht naar de trommel. Daar wordt de laag <b>geleidend</b> en vloeit de lading weg via de geaarde trommel. Alleen waar de <b>letters</b> staan (donker, geen licht) blijft de trommel <b>positief</b>.',
    'De <b>toner</b> (zwart poeder) is <b>negatief</b> geladen. Hij wordt <b>aangetrokken</b> door de positieve delen van de trommel. Zo ontstaat een tonerbeeld van de letters.',
    'Het papier wordt <b>sterker positief</b> geladen dan de trommel. Daardoor trekt het papier de negatieve toner van de trommel naar zich toe.',
    'In de <b>fixeereenheid</b> smelten warmte en druk de toner vast in het papier. De trommel wordt ontladen en schoongemaakt voor de volgende kopie.'];
  let s=0; const box=document.getElementById('l7-stap');
  ST.forEach((n,i)=>{ const b=document.createElement('button'); b.className='btn'; b.textContent=(i+1)+'. '+n; b.onclick=()=>{ s=i; upd(); }; box.appendChild(b); });
  function upd(){ [...box.children].forEach((b,i)=>b.classList.toggle('on',i===s)); document.getElementById('l7-read').innerHTML=TX[s]; draw(); }
  const CS=26;
  function raster(x,y,fn){ for(let r=0;r<7;r++) for(let q=0;q<5;q++) fn(x+q*CS,y+r*CS,E[r][q]==='1'); }
  function vak(x,y,titel,kleur){ ctx.fillStyle=kleur; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.5; roundRect(ctx,x-15,y-15,5*CS+30,7*CS+30,6); ctx.fill(); ctx.stroke(); text(ctx,titel,x+2.5*CS,y-26,{align:'center',weight:700}); }
  function draw(){
    bg(ctx,W,H); const y=110, xo=60, xt=330, xp=600;
    vak(xo,y,'origineel','#fff'); raster(xo,y,(x,yy,l)=>{ if(l){ ctx.fillStyle='#111827'; ctx.fillRect(x+2,yy+2,CS-4,CS-4); } });
    vak(xt,y,'trommel (uitgerold)','#d1fae5');
    raster(xt,y,(x,yy,l)=>{ const plus=(s===0)||(s>=1&&s<=3&&l); if(plus&&!(s===3)) text(ctx,'+',x+CS/2,yy+CS/2+6,{align:'center',weight:700,color:POS,size:16});
      if(s===3&&l) text(ctx,'+',x+CS/2,yy+CS/2+6,{align:'center',weight:700,color:'#f0a8ae',size:16});
      if(s===2&&l){ ctx.fillStyle='#111827'; for(let i=0;i<6;i++){ ctx.beginPath(); ctx.arc(x+7+(i%3)*6,yy+9+Math.floor(i/3)*8,2.6,0,7); ctx.fill(); } } });
    text(ctx,'⏚ geaard',xt+2.5*CS,y+7*CS+40,{align:'center',size:12,color:'#51606E'});
    vak(xp,y,'papier','#fff');
    if(s>=3) raster(xp,y,(x,yy,l)=>{ if(s===3){ text(ctx,'+',x+CS/2,yy+CS/2+6,{align:'center',weight:700,color:'#f4b4ba',size:14}); }
      if(l){ ctx.fillStyle='#111827'; if(s===4) ctx.fillRect(x+2,yy+2,CS-4,CS-4); else for(let i=0;i<6;i++){ ctx.beginPath(); ctx.arc(x+7+(i%3)*6,yy+9+Math.floor(i/3)*8,2.6,0,7); ctx.fill(); } } });
    if(s===1){ for(let r=0;r<7;r++){ const yy=y+r*CS+CS/2; arrow(ctx,xo+5*CS+18,yy,xt-20,yy,'#f59e0b',2); } text(ctx,'licht van de witte delen',(xo+5*CS+xt)/2,y+7*CS+40,{align:'center',size:12,color:'#b45309',weight:700}); }
    if(s===2){ for(let i=0;i<6;i++){ const x=xt+20+i*22; teken(ctx,x,y+7*CS+70,-1,8); } text(ctx,'negatief geladen toner',xt+2.5*CS,y+7*CS+100,{align:'center',size:12,weight:700}); }
    if(s===3) arrow(ctx,xt+5*CS+22,y+3.5*CS,xp-22,y+3.5*CS,'#111827',3,'toner',0,-10);
    if(s===4){ ctx.fillStyle='rgba(239,68,68,0.15)'; roundRect(ctx,xp-15,y-15,5*CS+30,7*CS+30,6); ctx.fill(); text(ctx,'warmte + druk',xp+2.5*CS,y+7*CS+40,{align:'center',weight:700,color:'#b91c1c'}); }
  }
  upd();
})();

//////////////////// 8 — SWIFFER ////////////////////
(function(){
  const c=document.getElementById('c-l8'), ctx=hiDPI(c), W=c._w, H=c._h;
  let t0=null; const read=document.getElementById('l8-read');
  const stof=[...Array(14)].map((_,i)=>({x:110+i*42+((i*37)%17),r:4+(i*13)%4}));
  document.getElementById('l8-veeg').onclick=()=>{ t0=performance.now(); upd(); };
  document.getElementById('l8-reset').onclick=()=>{ t0=null; upd(); };
  function upd(){ read.innerHTML=t0==null?'Klik op <b>Vegen</b>.':'<b>1. Wrijving:</b> de vezels wrijven over het oppervlak en worden <b>negatief</b> geladen.<br><b>2. Polarisatie:</b> een stofdeeltje is neutraal, maar in de buurt van het negatieve doekje schuiven zijn elektronen weg. De <b>+ kant</b> komt naar het doekje toe.<br><b>3. Aantrekking:</b> de + kant ligt dichter bij het doekje dan de − kant. De aantrekking is groter dan de afstoting: het stof <b>kleeft</b> aan het doekje.'; }
  lus('l8',now=>{
    const t=t0==null?0:Math.min(1,(now-t0)/4000), cx=60+t*640, lad=Math.min(8,Math.floor(t*14));
    bg(ctx,W,H); ctx.fillStyle='#d6a56b'; ctx.fillRect(0,300,W,100); text(ctx,'tafel',30,330,{color:'#7c4a12',weight:700});
    // doekje
    ctx.fillStyle='#bfdbfe'; roundRect(ctx,cx-70,250,140,40,8); ctx.fill(); ctx.strokeStyle='#60a5fa'; ctx.lineWidth=1.5; for(let i=0;i<14;i++){ ctx.beginPath(); ctx.moveTo(cx-65+i*10,290); ctx.lineTo(cx-63+i*10,298); ctx.stroke(); }
    ctx.fillStyle='#64748b'; ctx.fillRect(cx-6,170,12,80); text(ctx,'swifferdoekje',cx,240,{align:'center',size:12,weight:700});
    for(let i=0;i<lad;i++) teken(ctx,cx-56+i*16,270,-1,6);
    stof.forEach((p,i)=>{ const dx=p.x-cx; if(t0!=null&&dx<40&&!p.vast&&lad>2) p.vast=dx;
      if(t0==null) p.vast=undefined;
      if(p.vast!=null){ ctx.fillStyle='#78350f'; ctx.beginPath(); ctx.arc(cx+Math.max(-60,Math.min(60,p.vast)),296-p.r*0.2,p.r,0,7); ctx.fill(); }
      else { ctx.fillStyle='#78350f'; ctx.beginPath(); ctx.arc(p.x,300-p.r,p.r,0,7); ctx.fill(); } });
    // vergroting
    const zx=640,zy=110; ctx.fillStyle='#F5F8FB'; ctx.strokeStyle='#94a3b8'; roundRect(ctx,zx-130,zy-90,260,170,10); ctx.fill(); ctx.stroke(); text(ctx,'vergroot: één stofdeeltje',zx,zy-70,{align:'center',size:12,weight:700});
    ctx.fillStyle='#bfdbfe'; ctx.fillRect(zx-110,zy-55,220,22); for(let i=0;i<6;i++) teken(ctx,zx-90+i*36,zy-44,-1,7);
    ctx.fillStyle='#d6b48a'; ctx.beginPath(); ctx.arc(zx,zy+25,30,0,7); ctx.fill(); text(ctx,'+  +',zx,zy+16,{align:'center',weight:700,color:POS}); text(ctx,'−  −',zx,zy+46,{align:'center',weight:700,color:NEG});
    arrow(ctx,zx+45,zy+20,zx+45,zy-20,'#1D4ED8',3); text(ctx,'aantrekking',zx+52,zy,{size:11,color:'#1D4ED8',weight:700});
    arrow(ctx,zx-45,zy+10,zx-45,zy+30,'#94a3b8',2); text(ctx,'afstoting',zx-52,zy+25,{size:11,color:'#64748b',weight:700,align:'right'});
  });
  upd();
})();
