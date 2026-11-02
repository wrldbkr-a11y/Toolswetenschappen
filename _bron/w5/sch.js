//////////////////// SCHAKELINGEN: rekenkern ////////////////////
const nl=(x,d=2)=>{ if(!isFinite(x)) return '–'; const r=Math.round(x*10**d)/10**d; return r.toLocaleString('nl-BE',{maximumFractionDigits:d}); };
const R_=n=>({t:'R',n}), S_=(...c)=>({t:'S',c}), P_=(...c)=>({t:'P',c});
function idx(node){ return node.t==='R'?[node.n]:node.c.flatMap(idx); }
function naam(node,root){ if(node===root) return 'R<sub>s</sub>'; return 'R<sub>'+idx(node).join('')+'</sub>'; }
function req(node,R){ if(node.t==='R') return R[node.n]; const v=node.c.map(c=>req(c,R)); return node.t==='S'?v.reduce((a,b)=>a+b,0):1/v.reduce((a,b)=>a+1/b,0); }
function los(node,R,U,I){ node.U=U; node.I=I; node.R=req(node,R); if(node.t==='S') node.c.forEach(c=>{ const r=req(c,R); los(c,R,I*r,I); }); else if(node.t==='P') node.c.forEach(c=>{ const r=req(c,R); los(c,R,U,U/r); }); }
function stappen(root,R,U){
  los(root,R,U,U/req(root,R)); const st=[];
  (function post(n){ if(n.t==='R') return; n.c.forEach(post);
    const delen=n.c.map(c=>naam(c,root)), waarden=n.c.map(c=>nl(c.R)+' Ω');
    if(n.t==='S') st.push({h:idx(n),t:'<b>Serie:</b> '+naam(n,root)+' = '+delen.join(' + ')+' = '+waarden.join(' + ')+' = <b>'+nl(n.R)+' Ω</b>'});
    else st.push({h:idx(n),t:'<b>Parallel:</b> 1/'+naam(n,root)+' = '+delen.map(d=>'1/'+d).join(' + ')+' = '+waarden.map(w=>'1/'+w.replace(' Ω','')).join(' + ')+' &nbsp;→&nbsp; '+naam(n,root)+' = <b>'+nl(n.R)+' Ω</b>'});
  })(root);
  st.push({h:idx(root),t:'<b>Totale stroom:</b> I = U / R<sub>s</sub> = '+nl(U)+' V / '+nl(root.R)+' Ω = <b>'+nl(root.I)+' A</b>'});
  (function neer(n){ if(n.t==='R') return;
    if(n.t==='S'){ st.push({h:idx(n),t:'<b>Serie</b> ('+naam(n,root)+'): overal dezelfde stroom I = '+nl(n.I)+' A. De spanning verdeelt zich: '+n.c.map(c=>'U = '+nl(c.R)+' Ω · '+nl(n.I)+' A = <b>'+nl(c.U)+' V</b> over '+naam(c,root)).join('; ')+'.'}); }
    else { st.push({h:idx(n),t:'<b>Parallel</b> ('+naam(n,root)+'): over elke tak dezelfde spanning U = '+nl(n.U)+' V. De stroom verdeelt zich: '+n.c.map(c=>'I = '+nl(n.U)+' V / '+nl(c.R)+' Ω = <b>'+nl(c.I)+' A</b> door '+naam(c,root)).join('; ')+'.'}); }
    n.c.forEach(neer);
  })(root);
  st.push({h:[],t:'<b>Controle:</b> '+(root.t==='S'?'de deelspanningen samen geven de bronspanning':'de takstromen samen geven de totale stroom')+'. Klik op een weerstand om zijn waarden te zien.'});
  return st;
}
// ---------- tekenen ----------
const RW=104, RH=96;
function maat(n){ if(n.t==='R') return {w:RW,h:RH}; const m=n.c.map(maat);
  if(n.t==='S') return {w:m.reduce((a,b)=>a+b.w,0),h:Math.max(...m.map(x=>x.h))};
  return {w:Math.max(...m.map(x=>x.w))+52,h:m.reduce((a,b)=>a+b.h,0)}; }
function tekenNet(ctx,n,x,y,o,hits){
  const draad=(x1,y1,x2,y2)=>{ ctx.strokeStyle='#1D2A36'; ctx.lineWidth=2.2; ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke(); };
  if(n.t==='R'){
    const lit=o.licht&&o.licht.includes(n.n), sel=o.sel===n.n;
    draad(x,y,x+24,y); draad(x+RW-24,y,x+RW,y);
    ctx.fillStyle=sel?'#FDE68A':lit?'#E4EEF8':'#fff'; ctx.strokeStyle=lit||sel?'#2F6FB0':'#1D2A36'; ctx.lineWidth=lit||sel?3:2.2;
    ctx.fillRect(x+24,y-12,RW-48,24); ctx.strokeRect(x+24,y-12,RW-48,24);
    text(ctx,'R'+n.n,x+RW/2,y+5,{size:13,weight:700,align:'center'});
    if(o.waarde) text(ctx,nl(o.R[n.n],1)+' Ω',x+RW/2,y-19,{size:12,weight:600,align:'center',color:'#51606E'});
    if(o.toonUI&&n.U!=null){ text(ctx,nl(n.U)+' V',x+RW/2,y+29,{size:12,weight:700,align:'center',color:'#B45309'}); text(ctx,nl(n.I)+' A',x+RW/2,y+44,{size:12,weight:700,align:'center',color:'#1D4ED8'}); }
    hits.push({n:n.n,x:x+20,y:y-28,w:RW-40,h:60}); return;
  }
  const m=maat(n);
  if(n.t==='S'){ let cx=x; n.c.forEach(c=>{ const mc=maat(c); tekenNet(ctx,c,cx,y,o,hits); cx+=mc.w; }); return; }
  let top=y-m.h/2; const ys=[];
  n.c.forEach(c=>{ const mc=maat(c), cy=top+mc.h/2; ys.push(cy); tekenNet(ctx,c,x+26,cy,o,hits); if(mc.w<m.w-52) draad(x+26+mc.w,cy,x+m.w-26,cy); draad(x+12,cy,x+26,cy); draad(x+m.w-26,cy,x+m.w-12,cy); top+=mc.h; });
  draad(x,y,x+12,y); draad(x+m.w-12,y,x+m.w,y); draad(x+12,ys[0],x+12,ys[ys.length-1]); draad(x+m.w-12,ys[0],x+m.w-12,ys[ys.length-1]);
  ctx.fillStyle='#1D2A36'; [x+12,x+m.w-12].forEach(px=>{ ctx.beginPath(); ctx.arc(px,y,3.5,0,7); ctx.fill(); });
}
function tekenKring(c,ctx,root,o){
  const W=c._w,H=c._h; ctx.setTransform(1,0,0,1,0,0); const dpr=c.width/W; ctx.scale(dpr,dpr);
  ctx.clearRect(0,0,W,H); ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H);
  const m=maat(root), w=m.w+80, h=m.h+90, s=Math.min(1,(W-40)/w,(H-30)/h);
  ctx.translate(W/2-w*s/2,H/2-h*s/2); ctx.scale(s,s);
  const x0=40, y0=20+m.h/2, yb=m.h+60, hits=[];
  const draad=(x1,y1,x2,y2)=>{ ctx.strokeStyle='#1D2A36'; ctx.lineWidth=2.2; ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke(); };
  draad(0,y0,x0,y0); draad(x0+m.w,y0,x0+m.w+40,y0); draad(0,y0,0,yb); draad(x0+m.w+40,y0,x0+m.w+40,yb);
  const bx=(x0*2+m.w)/2; draad(0,yb,bx-8,yb); draad(bx+8,yb,x0+m.w+40,yb);
  ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(bx-8,yb-20); ctx.lineTo(bx-8,yb+20); ctx.stroke(); ctx.lineWidth=6; ctx.beginPath(); ctx.moveTo(bx+8,yb-10); ctx.lineTo(bx+8,yb+10); ctx.stroke();
  text(ctx,'+',bx-22,yb-12,{weight:700,align:'center'}); text(ctx,'−',bx+22,yb-12,{weight:700,align:'center'});
  text(ctx,'U = '+nl(o.U,1)+' V',bx,yb+38,{weight:700,align:'center'});
  if(o.toonI) { arrow(ctx,bx-40,yb,bx-80,yb,'#1D4ED8',2.5); text(ctx,'I = '+nl(root.I)+' A',bx-60,yb+20,{size:12,weight:700,color:'#1D4ED8',align:'center'}); }
  tekenNet(ctx,root,x0,y0,o,hits);
  c._hits=hits.map(b=>({n:b.n,x:(b.x)*s+W/2-w*s/2,y:b.y*s+H/2-h*s/2,w:b.w*s,h:b.h*s}));
}
function hitTest(c,e){ const r=c.getBoundingClientRect(), x=(e.clientX-r.left)*c._w/r.width, y=(e.clientY-r.top)*c._h/r.height; const b=(c._hits||[]).find(b=>x>=b.x&&x<=b.x+b.w&&y>=b.y&&y<=b.y+b.h); return b?b.n:null; }
function vindR(n,k){ if(n.t==='R') return n.n===k?n:null; for(const c of n.c){ const f=vindR(c,k); if(f) return f; } return null; }
function sliders(div,ids,R,cb,pref){
  div.innerHTML=ids.map(i=>`<div class="ctrl-group"><label id="${pref}-l${i}">R${i}</label><input type="range" id="${pref}-r${i}" min="1" max="30" step="1" value="${R[i]}"></div>`).join('');
  ids.forEach(i=>{ const s=document.getElementById(pref+'-r'+i); const lab=()=>document.getElementById(pref+'-l'+i).textContent='R'+i+' = '+R[i]+' Ω'; lab(); s.oninput=()=>{ R[i]=+s.value; lab(); cb(); }; });
}

//////////////////// 1 — WET VAN OHM ////////////////////
(function(){
  const c=document.getElementById('c-ohm'), ctx=hiDPI(c), W=c._w, H=c._h;
  const Us=document.getElementById('ohm-U'), Rs=document.getElementById('ohm-R'), read=document.getElementById('ohm-read');
  function meter(x,y,t){ ctx.fillStyle='#fff'; ctx.strokeStyle='#1D2A36'; ctx.lineWidth=2.2; ctx.beginPath(); ctx.arc(x,y,17,0,7); ctx.fill(); ctx.stroke(); text(ctx,t,x,y+5,{weight:700,align:'center'}); }
  function draw(){
    const RV=[47,68,100,150,220,330,470,680,1000], U=+Us.value, R=RV[+Rs.value], I=U/R;
    document.getElementById('ohm-U-l').textContent='Spanning U = '+nl(U,1)+' V';
    document.getElementById('ohm-R-l').textContent='Weerstand R = '+R+' Ω';
    ctx.clearRect(0,0,W,H); ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H);
    const d=(a,b,cc,e)=>{ ctx.strokeStyle='#1D2A36'; ctx.lineWidth=2.2; ctx.beginPath(); ctx.moveTo(a,b); ctx.lineTo(cc,e); ctx.stroke(); };
    // kring
    d(40,90,120,90); meter(137,90,'A'); d(154,90,190,90); d(270,90,330,90); d(330,90,330,290); d(40,90,40,290); d(40,290,175,290); d(195,290,330,290);
    ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(175,270); ctx.lineTo(175,310); ctx.stroke(); ctx.lineWidth=6; ctx.beginPath(); ctx.moveTo(191,280); ctx.lineTo(191,300); ctx.stroke();
    ctx.fillStyle='#fff'; ctx.strokeStyle='#2F6FB0'; ctx.lineWidth=2.5; ctx.fillRect(190,78,80,24); ctx.strokeRect(190,78,80,24); text(ctx,'R',230,95,{weight:700,align:'center'});
    d(180,90,180,150); d(280,90,280,150); d(180,150,213,150); d(247,150,280,150); meter(230,150,'V');
    text(ctx,nl(U,1)+' V',230,190,{weight:700,align:'center',color:'#B45309'}); text(ctx,nl(I*1000,0)+' mA',137,60,{weight:700,align:'center',color:'#1D4ED8'});
    text(ctx,'U = '+nl(U,1)+' V',183,340,{weight:600,align:'center'});
    if(I>0){ const L=Math.min(60,10+I*200); arrow(ctx,60,70,60+L,70,'#1D4ED8',2.5); }
    // grafiek U(I)
    const gx=420,gy=320,gw=340,gh=270, Imax=0.3, Umax=12;
    ctx.strokeStyle='#E2E8F0'; ctx.lineWidth=1; for(let i=0;i<=6;i++){ const ia=i*0.05, u=i*2; ctx.beginPath(); ctx.moveTo(gx+ia/Imax*gw,gy); ctx.lineTo(gx+ia/Imax*gw,gy-gh); ctx.stroke(); ctx.beginPath(); ctx.moveTo(gx,gy-u/Umax*gh); ctx.lineTo(gx+gw,gy-u/Umax*gh); ctx.stroke();
      text(ctx,String(i*50),gx+ia/Imax*gw,gy+16,{size:11,align:'center',color:'#51606E'}); text(ctx,String(u),gx-8,gy-u/Umax*gh+4,{size:11,align:'right',color:'#51606E'}); }
    arrow(ctx,gx,gy,gx+gw+18,gy,'#1D2A36',1.6); arrow(ctx,gx,gy,gx,gy-gh-18,'#1D2A36',1.6);
    text(ctx,'I (mA)',gx+gw+14,gy+34,{size:12,weight:600,align:'center'}); text(ctx,'U (V)',gx,gy-gh-24,{size:12,weight:600,align:'center'});
    const Iend=Math.min(Imax,Umax/R); ctx.strokeStyle='#2F6FB0'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(gx,gy); ctx.lineTo(gx+Iend/Imax*gw,gy-Iend*R/Umax*gh); ctx.stroke();
    const px=gx+Math.min(I,Imax)/Imax*gw, py=gy-U/Umax*gh; ctx.setLineDash([4,4]); ctx.strokeStyle='#94A3B8'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(px,gy); ctx.lineTo(px,py); ctx.lineTo(gx,py); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle='#dc2626'; ctx.beginPath(); ctx.arc(px,py,5,0,7); ctx.fill();
    text(ctx,'R = '+R+' Ω',gx+Iend/Imax*gw+6,gy-Iend*R/Umax*gh+(Iend>=Imax?14:-6),{size:12,weight:700,color:'#2F6FB0'});
    read.innerHTML='I = U / R = '+nl(U,1)+' V / '+R+' Ω = '+nl(I,4)+' A = <b>'+nl(I*1000,1)+' mA</b><br><span class="k">Dubbele spanning → dubbele stroom (zelfde R).</span>';
  }
  Us.oninput=Rs.oninput=draw; draw();
})();

//////////////////// 2 — SERIE EN PARALLEL ////////////////////
(function(){
  const c=document.getElementById('c-basis'), ctx=hiDPI(c);
  let soort='S', n=2; const R=[0,4,6,12];
  const Us=document.getElementById('basis-U'), read=document.getElementById('basis-read');
  document.querySelectorAll('#basis [data-soort]').forEach(b=>b.onclick=()=>{ soort=b.dataset.soort; document.querySelectorAll('#basis [data-soort]').forEach(o=>o.classList.toggle('on',o===b)); bouwS(); });
  document.querySelectorAll('#basis [data-aantal]').forEach(b=>b.onclick=()=>{ n=+b.dataset.aantal; document.querySelectorAll('#basis [data-aantal]').forEach(o=>o.classList.toggle('on',o===b)); bouwS(); });
  function bouwS(){ sliders(document.getElementById('basis-R'),[1,2,3].slice(0,n),R,draw,'bas'); draw(); }
  function draw(){
    const U=+Us.value; document.getElementById('basis-U-l').textContent='Bronspanning U = '+U+' V';
    const kids=[1,2,3].slice(0,n).map(R_), root=soort==='S'?S_(...kids):P_(...kids);
    los(root,R,U,U/req(root,R));
    tekenKring(c,ctx,root,{U,R,waarde:true,toonUI:true,toonI:true});
    const k=root.c;
    if(soort==='S') read.innerHTML='<b>Serie</b><br>R<sub>s</sub> = '+k.map(x=>'R'+x.n).join(' + ')+' = <b>'+nl(root.R)+' Ω</b><br>I = U / R<sub>s</sub> = <b>'+nl(root.I)+' A</b> (overal dezelfde)<br>U = '+k.map(x=>'U'+x.n).join(' + ')+' = '+k.map(x=>nl(x.U)).join(' + ')+' = '+nl(U)+' V<br><span class="k">Grootste weerstand → grootste deelspanning.</span>';
    else read.innerHTML='<b>Parallel</b><br>1/R<sub>s</sub> = '+k.map(x=>'1/R'+x.n).join(' + ')+' → R<sub>s</sub> = <b>'+nl(root.R)+' Ω</b><br>U = <b>'+U+' V</b> over elke tak<br>I = '+k.map(x=>'I'+x.n).join(' + ')+' = '+k.map(x=>nl(x.I)).join(' + ')+' = <b>'+nl(root.I)+' A</b><br><span class="k">R<sub>s</sub> is kleiner dan de kleinste weerstand. Kleinste weerstand → grootste stroom.</span>';
  }
  Us.oninput=draw; bouwS();
})();

//////////////////// 3 — GEMENGD STAP VOOR STAP ////////////////////
const PRESETS=[
  {naam:'R1 + (R2 // R3)', boom:()=>S_(R_(1),P_(R_(2),R_(3))), R:[0,4,6,12]},
  {naam:'(R1 + R2) // R3', boom:()=>P_(S_(R_(1),R_(2)),R_(3)), R:[0,4,8,6]},
  {naam:'R1 + (R2 // (R3 + R4))', boom:()=>S_(R_(1),P_(R_(2),S_(R_(3),R_(4)))), R:[0,3,12,4,8]},
  {naam:'(R1 // R2) + (R3 // R4)', boom:()=>S_(P_(R_(1),R_(2)),P_(R_(3),R_(4))), R:[0,6,3,10,15]},
];
(function(){
  const c=document.getElementById('c-gem'), ctx=hiDPI(c);
  let p=0, R=PRESETS[0].R.slice(), stap=0, sel=null, root, st;
  const Us=document.getElementById('gem-U'), box=document.getElementById('gem-stappen');
  const pre=document.getElementById('gem-preset');
  PRESETS.forEach((q,i)=>{ const b=document.createElement('button'); b.className='btn'; b.textContent=q.naam; b.onclick=()=>{ p=i; R=q.R.slice(); stap=0; sel=null; bouw(); }; pre.appendChild(b); });
  function bouw(){ [...pre.children].forEach((b,i)=>b.classList.toggle('on',i===p)); root=PRESETS[p].boom(); sliders(document.getElementById('gem-R'),idx(root),R,()=>{ draw(); },'gem'); draw(); }
  function draw(){
    const U=+Us.value; document.getElementById('gem-U-l').textContent='Bronspanning U = '+U+' V';
    st=stappen(root,R,U); stap=Math.min(stap,st.length);
    const klaar=stap>=st.length-1;
    tekenKring(c,ctx,root,{U,R,waarde:true,toonUI:klaar,toonI:stap>countDown(root),licht:stap>0?st[stap-1].h:[],sel});
    let html=st.slice(0,stap).map((s,i)=>'<div style="padding:4px 0;'+(i===stap-1?'':'color:#51606E')+'">'+(i+1)+'. '+s.t+'</div>').join('');
    if(!stap) html='<span class="k">Klik op <b>Volgende stap</b>. Stap 1 begint bij het binnenste deel van de schakeling.</span>';
    if(sel!=null&&klaar){ const r=vindR(root,sel); html+='<div style="margin-top:8px;padding:8px 10px;background:#FEF3C7;border-radius:8px"><b>R'+sel+'</b>: R = '+nl(R[sel],1)+' Ω · U = '+nl(r.U)+' V · I = '+nl(r.I)+' A &nbsp;(controle: R · I = '+nl(R[sel]*r.I)+' V)</div>'; }
    box.innerHTML=html;
    document.getElementById('gem-verder').disabled=stap>=st.length;
  }
  function countDown(n){ return n.t==='R'?0:1+n.c.reduce((a,c)=>a+countDown(c),0); }
  document.getElementById('gem-verder').onclick=()=>{ stap++; draw(); };
  document.getElementById('gem-terug').onclick=()=>{ stap=Math.max(0,stap-1); draw(); };
  document.getElementById('gem-alles').onclick=()=>{ stap=999; draw(); };
  document.getElementById('gem-reset').onclick=()=>{ stap=0; sel=null; draw(); };
  c.addEventListener('click',e=>{ const k=hitTest(c,e); sel=k; draw(); });
  Us.oninput=draw; bouw();
})();

//////////////////// 4 — OEFENEN ////////////////////
(function(){
  const c=document.getElementById('c-oef'), ctx=hiDPI(c);
  const WR=[2,3,4,5,6,8,10,12,15,20,24,30], WU=[6,9,12,18,24];
  let root,R,U,vragen,goed=0,tot=0,opl=false;
  const kies=a=>a[Math.floor(Math.random()*a.length)];
  function nieuw(){
    const p=Math.floor(Math.random()*PRESETS.length); root=PRESETS[p].boom(); R=[0]; idx(root).forEach(i=>R[i]=kies(WR)); U=kies(WU);
    los(root,R,U,U/req(root,R)); opl=false;
    const ids=idx(root), a=kies(ids); let b=kies(ids); while(ids.length>1&&b===a) b=kies(ids);
    const ra=vindR(root,a), rb=vindR(root,b);
    vragen=[{l:'R<sub>s</sub> (Ω)',w:root.R},{l:'I totaal (A)',w:root.I},{l:'U<sub>'+a+'</sub> over R'+a+' (V)',w:ra.U},{l:'I<sub>'+b+'</sub> door R'+b+' (A)',w:rb.I}];
    document.getElementById('oef-vragen').innerHTML=vragen.map((v,i)=>`<div class="ctrl-group"><label for="oef-${i}">${v.l}</label><input id="oef-${i}" inputmode="decimal" style="width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:8px;font:inherit"></div>`).join('');
    document.getElementById('oef-stappen').style.display='none'; draw();
  }
  function draw(){ tekenKring(c,ctx,root,{U,R,waarde:true,toonUI:opl,toonI:opl}); }
  document.getElementById('oef-check').onclick=()=>{
    let ok=0; vragen.forEach((v,i)=>{ const inp=document.getElementById('oef-'+i), x=parseFloat(inp.value.replace(',','.')); const j=isFinite(x)&&Math.abs(x-v.w)<=Math.max(0.011,Math.abs(v.w)*0.02); if(j) ok++; inp.style.borderColor=j?'var(--ok-text)':'var(--flag-text)'; inp.style.background=j?'var(--ok-bg)':'var(--flag-bg)'; });
    tot+=vragen.length; goed+=ok; document.getElementById('oef-read').innerHTML='<span class="score">'+goed+' / '+tot+'</span><br>'+(ok===vragen.length?'<span class="ok">Alles juist!</span>':'<span class="flag">'+ok+' van de '+vragen.length+' juist.</span> Kijk je berekening na of bekijk de oplossing.');
  };
  document.getElementById('oef-opl').onclick=()=>{ opl=true; const st=stappen(root,R,U); const b=document.getElementById('oef-stappen'); b.style.display=''; b.innerHTML=st.map((s,i)=>'<div style="padding:3px 0">'+(i+1)+'. '+s.t+'</div>').join(''); draw(); };
  document.getElementById('oef-nieuw').onclick=nieuw;
  nieuw();
})();
