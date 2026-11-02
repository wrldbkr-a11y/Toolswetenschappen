<script>
/* =====================================================================
   NIEUWE TABBLADEN: meerdere ladingen, geleiders/isolatoren, energie
   ===================================================================== */
(function(){
const POS='#d64550', NEG='#2a6f97', EC='#4f6fd0', LIJN='#5b6b85', ACC='#2F6FB0';
const nl=(x,d=2)=>x.toLocaleString('nl-BE',{maximumFractionDigits:d});
function sci(x,u){ if(x===0) return '0 '+u; const e=Math.floor(Math.log10(Math.abs(x))); if(e>=-2&&e<5) return nl(x,2)+' '+u; const m=x/10**e; return nl(m,2)+' · 10'+String(e).replace(/-/g,'⁻').replace(/\d/g,d=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[d])+' '+u; }
function hd(cv){ const dpr=window.devicePixelRatio||1, w=cv.width, h=cv.height; cv.width=w*dpr; cv.height=h*dpr; const ctx=cv.getContext('2d'); ctx.scale(dpr,dpr); cv._w=w; cv._h=h; return ctx; }
function pijl(ctx,x1,y1,x2,y2,kleur,b=2.5){ const a=Math.atan2(y2-y1,x2-x1), L=Math.hypot(x2-x1,y2-y1); if(L<2) return; const s=Math.min(11,4+b*2.4); ctx.save(); ctx.strokeStyle=kleur; ctx.fillStyle=kleur; ctx.lineWidth=b; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2-Math.cos(a)*s*0.7,y2-Math.sin(a)*s*0.7); ctx.stroke(); ctx.beginPath(); ctx.moveTo(x2,y2); ctx.lineTo(x2-s*Math.cos(a-0.45),y2-s*Math.sin(a-0.45)); ctx.lineTo(x2-s*Math.cos(a+0.45),y2-s*Math.sin(a+0.45)); ctx.closePath(); ctx.fill(); ctx.restore(); }
function kop(ctx,x,y,a,kleur,s=7){ ctx.save(); ctx.fillStyle=kleur; ctx.beginPath(); ctx.moveTo(x+Math.cos(a)*s*0.6,y+Math.sin(a)*s*0.6); ctx.lineTo(x-s*Math.cos(a-0.5),y-s*Math.sin(a-0.5)); ctx.lineTo(x-s*Math.cos(a+0.5),y-s*Math.sin(a+0.5)); ctx.closePath(); ctx.fill(); ctx.restore(); }
function txt(ctx,t,x,y,o={}){ ctx.save(); ctx.font=(o.w||600)+' '+(o.s||13)+'px Inter, sans-serif'; ctx.fillStyle=o.c||'#1D2A36'; ctx.textAlign=o.a||'left'; ctx.fillText(t,x,y); ctx.restore(); }
function bolLading(ctx,x,y,Q,r=14,sel=false){ const g=ctx.createRadialGradient(x-r*0.35,y-r*0.35,2,x,y,r); g.addColorStop(0,'#fff'); g.addColorStop(0.3,Q>0?POS:NEG); g.addColorStop(1,Q>0?'#8f2430':'#173f57'); ctx.fillStyle=g; ctx.beginPath(); ctx.arc(x,y,r,0,7); ctx.fill(); if(sel){ ctx.strokeStyle='#f59e0b'; ctx.lineWidth=3; ctx.stroke(); } txt(ctx,(Q>0?'+':'−')+Math.abs(Q),x,y+4.5,{c:'#fff',w:700,s:12,a:'center'}); }

/* ---------------- MEERDERE LADINGEN ---------------- */
const SC=20; // px per cm
const ml={q:[],P:null,sel:0,bijdr:false}; window.mlState=ml;
const PRE={gelijk:[[-5,0,4],[5,0,4]],dipool:[[-5,0,4],[5,0,-4]],ongelijk:[[-5,0,6],[5,0,-2]],drie:[[-6,-3,4],[6,-3,4],[0,5,-4]]};
function zet(p){ ml.q=PRE[p].map(([x,y,Q])=>({x,y,Q})); ml.sel=0; ml.P=null; }
zet('gelijk');
function veld(x,y){ let ex=0,ey=0; for(const c of ml.q){ const dx=(x-c.x)*0.01, dy=(y-c.y)*0.01, r2=dx*dx+dy*dy; if(r2<1e-8) continue; const f=8.99e9*c.Q*1e-6/(r2*Math.sqrt(r2)); ex+=f*dx; ey+=f*dy; } return [ex,ey]; }
function lijn(x,y,dir,maxN=1600){ const pts=[[x,y]]; for(let i=0;i<maxN;i++){ let [ex,ey]=veld(x,y); const L=Math.hypot(ex,ey); if(!L) break; x+=dir*ex/L*0.07; y+=dir*ey/L*0.07; pts.push([x,y]);
    if(Math.abs(x)>17||Math.abs(y)>13) break; if(ml.q.some(c=>Math.hypot(c.x-x,c.y-y)<0.35)) break; } return pts; }
let cacheKey='', cacheLijnen=[];
function alleLijnen(){
  const key=JSON.stringify(ml.q); if(key===cacheKey) return cacheLijnen;
  const pos=ml.q.filter(c=>c.Q>0).reduce((a,c)=>a+c.Q,0), neg=-ml.q.filter(c=>c.Q<0).reduce((a,c)=>a+c.Q,0), vanPos=pos>=neg, out=[];
  ml.q.forEach(c=>{ if((c.Q>0)!==vanPos) return; const n=3*Math.abs(c.Q)+2;
    for(let i=0;i<n;i++){ const a=(i+0.5)*2*Math.PI/n; out.push({pts:lijn(c.x+0.4*Math.cos(a),c.y+0.4*Math.sin(a),vanPos?1:-1),dir:vanPos?1:-1}); } });
  cacheKey=key; cacheLijnen=out; return out;
}
const mcv=document.getElementById('ml_cv'), mctx=hd(mcv), MW=mcv._w, MH=mcv._h;
const toPx=(x,y)=>[MW/2+x*SC,MH/2+y*SC], toCm=(px,py)=>[(px-MW/2)/SC,(py-MH/2)/SC];
function tekenPad(ctx,pts,kleur,b,dir,pijlen=true){ ctx.strokeStyle=kleur; ctx.lineWidth=b; ctx.beginPath(); pts.forEach((p,i)=>{ const [X,Y]=toPx(p[0],p[1]); i?ctx.lineTo(X,Y):ctx.moveTo(X,Y); }); ctx.stroke();
  if(!pijlen) return; let s=0; for(let i=1;i<pts.length;i++){ s+=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]); if(s>5.5&&i<pts.length-8){ s=0; const [X,Y]=toPx(pts[i][0],pts[i][1]), [X0,Y0]=toPx(pts[i-1][0],pts[i-1][1]); kop(ctx,X,Y,Math.atan2(Y-Y0,X-X0)+(dir<0?Math.PI:0),kleur); } } }
function tekenMl(){
  const ctx=mctx; ctx.clearRect(0,0,MW,MH); ctx.fillStyle='#fbfcfd'; ctx.fillRect(0,0,MW,MH);
  alleLijnen().forEach(l=>tekenPad(ctx,l.pts,LIJN,1.4,l.dir));
  if(ml.P){ const [px,py]=[ml.P.x,ml.P.y];
    const voor=lijn(px,py,1,900), achter=lijn(px,py,-1,900);
    tekenPad(ctx,achter.slice().reverse().concat(voor),ACC,3,1,false);
    const [ex,ey]=veld(px,py), E=Math.hypot(ex,ey), [X,Y]=toPx(px,py);
    if(E>0){ const ux=ex/E, uy=ey/E, L=Math.max(30,Math.min(75,18*Math.log10(E)-60));
      ctx.setLineDash([5,5]); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(X-ux*110,Y-uy*110); ctx.lineTo(X+ux*110,Y+uy*110); ctx.stroke(); ctx.setLineDash([]);
      if(ml.bijdr) ml.q.forEach((c,i)=>{ const dx=(px-c.x)*0.01, dy=(py-c.y)*0.01, r2=dx*dx+dy*dy, f=8.99e9*c.Q*1e-6/(r2*Math.sqrt(r2)), e=[f*dx,f*dy], Ei=Math.hypot(...e), Li=L*Ei/E;
        pijl(ctx,X,Y,X+e[0]/Ei*Li,Y+e[1]/Ei*Li,c.Q>0?'#e88a93':'#7fb0cf',2); txt(ctx,'E'+'₁₂₃'[i],X+e[0]/Ei*(Li+12),Y+e[1]/Ei*(Li+12)+4,{c:c.Q>0?POS:NEG,s:12,a:'center'}); });
      pijl(ctx,X,Y,X+ux*L,Y+uy*L,EC,3.5); txt(ctx,'E',X+ux*(L+14),Y+uy*(L+14)+5,{c:EC,w:700,s:15,a:'center'}); }
    ctx.fillStyle='#1D2A36'; ctx.beginPath(); ctx.arc(X,Y,4.5,0,7); ctx.fill(); txt(ctx,'P',X+8,Y-8,{w:700});
  }
  ml.q.forEach((c,i)=>{ const [X,Y]=toPx(c.x,c.y); bolLading(ctx,X,Y,c.Q,14,i===ml.sel); txt(ctx,'Q'+'₁₂₃'[i],X,Y+30,{a:'center',s:12,c:c.Q>0?POS:NEG}); });
  // uitlezing
  const c=ml.q[ml.sel]; document.getElementById('ml_selNaam').textContent='Gekozen lading Q'+'₁₂₃'[ml.sel]; document.getElementById('ml_qVal').textContent=(c.Q>0?'+':'−')+Math.abs(c.Q)+' µC'; document.getElementById('ml_q').value=c.Q;
  const box=document.getElementById('ml_readout');
  if(!ml.P){ box.innerHTML='<span class="empty">Klik in het veld om punt P te plaatsen.</span>'; return; }
  const [ex,ey]=veld(ml.P.x,ml.P.y);
  box.innerHTML=ml.q.map((c,i)=>{ const r=Math.hypot(ml.P.x-c.x,ml.P.y-c.y)*0.01; return `<div class="readout-row"><span class="k">E${'₁₂₃'[i]} = k·|Q${'₁₂₃'[i]}|/r² (r = ${nl(r*100,1)} cm)</span><span class="num">${sci(8.99e9*Math.abs(c.Q)*1e-6/(r*r),'N/C')}</span></div>`; }).join('')+
    `<div class="divider" style="margin:8px 0"></div><div class="readout-row"><span class="k"><b>resulterend E</b> (vectorsom)</span><span class="num"><b>${sci(Math.hypot(ex,ey),'N/C')}</b></span></div><div class="k" style="margin-top:6px">E raakt aan de blauwe veldlijn door P.</div>`;
}
let sleep=null, verplaatst=false;
function pos(e){ const r=mcv.getBoundingClientRect(); return toCm((e.clientX-r.left)*MW/r.width,(e.clientY-r.top)*MH/r.height); }
mcv.addEventListener('pointerdown',e=>{ const [x,y]=pos(e); const i=ml.q.findIndex(c=>Math.hypot(c.x-x,c.y-y)<1); verplaatst=false; if(i>=0){ sleep=i; ml.sel=i; mcv.setPointerCapture(e.pointerId); } else { ml.P={x,y}; } tekenMl(); });
mcv.addEventListener('pointermove',e=>{ if(sleep==null) return; const [x,y]=pos(e); ml.q[sleep].x=Math.max(-14,Math.min(14,x)); ml.q[sleep].y=Math.max(-10,Math.min(10,y)); verplaatst=true; tekenMl(); });
mcv.addEventListener('pointerup',()=>{ sleep=null; });
document.querySelectorAll('#ml_preset button').forEach(b=>b.onclick=()=>{ document.querySelectorAll('#ml_preset button').forEach(o=>o.classList.toggle('active',o===b)); zet(b.dataset.p); tekenMl(); });
document.getElementById('ml_q').oninput=e=>{ let v=+e.target.value; if(v===0) v=ml.q[ml.sel].Q>0?-1:1; ml.q[ml.sel].Q=v; tekenMl(); };
document.getElementById('ml_bijdr').onchange=e=>{ ml.bijdr=e.target.checked; tekenMl(); };
document.getElementById('ml_clearP').onclick=()=>{ ml.P=null; tekenMl(); };
window.mlLijnen3D=null;

/* ---------------- GELEIDERS EN ISOLATOREN ---------------- */
const fcv=document.getElementById('fd_cv'), fctx=hd(fcv), FW=fcv._w, FH=fcv._h; let fdV='hol';
const FT={geen:'Zonder voorwerp: een homogeen veld. De veldlijnen zijn evenwijdige rechten.',
  hol:'<b>Holle geleider (kooi van Faraday).</b> De vrije elektronen verschuiven tot het veld <b>binnenin nul</b> is: links komt er negatieve lading, rechts blijft positieve lading over. Die ladingen maken samen een veld dat het buitenveld binnenin precies opheft. Wat binnenin zit, is <b>afgeschermd</b>. De veldlijnen staan <b>loodrecht</b> op het oppervlak.',
  vol:'<b>Volle geleider.</b> Ook in een volle geleider is het veld <b>nul</b>. De lading zit alleen aan het oppervlak. Of de geleider hol of vol is, maakt voor het veld binnenin niets uit.',
  iso:'<b>Isolator.</b> Er zijn geen vrije elektronen. De moleculen worden <b>gepolariseerd</b> (kleine dipolen). Daardoor wordt het veld binnenin <b>zwakker</b>, maar niet nul. Een isolator schermt niet af.'};
const VB={auto:'<b>Auto:</b> de metalen carrosserie werkt als kooi van Faraday. Slaat de bliksem in, dan loopt de lading over de buitenkant naar de grond. De inzittenden zijn veilig (zolang ze de carrosserie niet aanraken).',
  vliegtuig:'<b>Vliegtuig:</b> de metalen romp leidt de lading van een blikseminslag over de buitenkant weg. Passagiers en elektronica binnenin worden afgeschermd.',
  micro:'<b>Microgolfoven:</b> de metalen wanden en het metalen rooster in het deurtje vormen een kooi van Faraday. De elektromagnetische golven blijven <b>binnen</b> de oven, zodat ze jou niet bereiken.',
  coax:'<b>Coaxkabel:</b> rond de middelste draad zit een omhulsel van metaalvlechtwerk. Dat schermt het signaal af van storende velden van buitenaf (en omgekeerd).'};
function fdTeken(){
  const ctx=fctx; ctx.clearRect(0,0,FW,FH); ctx.fillStyle='#fbfcfd'; ctx.fillRect(0,0,FW,FH);
  const cx=300, cy=220, R=78, K=fdV==='geen'?0:fdV==='iso'?0.6:1, geleider=fdV==='hol'||fdV==='vol', X0=48, X1=552;
  const psi=(x,y)=>{ const r2=x*x+y*y; return r2<R*R? (geleider?NaN:y*(1-K)) : y*(1-K*R*R/r2); };
  function yVoor(x,c){ let lo=0, hi=260; if(geleider&&Math.abs(x)<R) lo=Math.sqrt(R*R-x*x)+0.01; const f=y=>{ const v=psi(x,y); return v-c; };
    if(f(lo)>0) return null; for(let k=0;k<40;k++){ const m=(lo+hi)/2; if(f(m)>0) hi=m; else lo=m; } return (lo+hi)/2; }
  ctx.strokeStyle=LIJN; ctx.lineWidth=1.5;
  for(let c=-195;c<=195;c+=26){
    const s=c<0?-1:1, ca=Math.abs(c);
    if(c===0||Math.abs(c)<1){ if(geleider){ ctx.beginPath(); ctx.moveTo(X0,cy); ctx.lineTo(cx-R,cy); ctx.moveTo(cx+R,cy); ctx.lineTo(X1,cy); ctx.stroke(); kop(ctx,140,cy,0,LIJN); kop(ctx,470,cy,0,LIJN); } else { ctx.beginPath(); ctx.moveTo(X0,cy); ctx.lineTo(X1,cy); ctx.stroke(); kop(ctx,140,cy,0,LIJN); kop(ctx,470,cy,0,LIJN); } continue; }
    ctx.beginPath(); let eerste=true, prev=null;
    for(let X=X0;X<=X1;X+=3){ const y=yVoor(X-cx,ca); if(y==null||y>250){ eerste=true; continue; } const Y=cy-s*y; if(eerste) ctx.moveTo(X,Y); else ctx.lineTo(X,Y); eerste=false; prev=[X,Y]; }
    ctx.stroke();
    [140,470].forEach(X=>{ const y=yVoor(X-cx,ca); if(y!=null&&y<215) kop(ctx,X,cy-s*y,0,LIJN); });
  }
  // platen
  ctx.fillStyle='#fde2e4'; ctx.fillRect(20,20,24,400); ctx.fillStyle='#dbeafe'; ctx.fillRect(556,20,24,400);
  for(let i=0;i<9;i++){ txt(ctx,'+',32,48+i*45,{c:POS,w:700,s:18,a:'center'}); txt(ctx,'−',568,48+i*45,{c:NEG,w:700,s:18,a:'center'}); }
  if(geleider){
    ctx.fillStyle=fdV==='vol'?'#cbd5e1':'#cbd5e1'; ctx.beginPath(); ctx.arc(cx,cy,R,0,7); ctx.fill(); ctx.strokeStyle='#475569'; ctx.lineWidth=2; ctx.stroke();
    if(fdV==='hol'){ ctx.fillStyle='#fbfcfd'; ctx.beginPath(); ctx.arc(cx,cy,R-12,0,7); ctx.fill(); ctx.stroke(); }
    for(let i=0;i<16;i++){ const a=i*Math.PI/8+Math.PI/16, co=Math.cos(a); if(Math.abs(co)<0.3) continue; txt(ctx,co>0?'+':'−',cx+(R+11)*co,cy+(R+11)*Math.sin(a)+5,{c:co>0?POS:NEG,w:700,s:16,a:'center'}); }
    txt(ctx,'E = 0',cx,cy+6,{w:700,s:18,a:'center'}); txt(ctx,fdV==='hol'?'holle geleider':'volle geleider',cx,cy+R+38,{w:700,a:'center',c:'#51606E'});
  } else if(fdV==='iso'){
    ctx.fillStyle='rgba(253,230,138,0.45)'; ctx.beginPath(); ctx.arc(cx,cy,R,0,7); ctx.fill(); ctx.strokeStyle='#b45309'; ctx.lineWidth=2; ctx.stroke();
    for(let i=-2;i<=2;i++) for(let j=-2;j<=2;j++){ const x=cx+i*26, y=cy+j*26+13; if(Math.hypot(x-cx,y-cy)>R-14) continue; ctx.fillStyle='rgba(255,255,255,0.8)'; ctx.strokeStyle='#b45309'; ctx.lineWidth=1; ctx.beginPath(); ctx.ellipse(x,y,10,6,0,0,7); ctx.fill(); ctx.stroke(); txt(ctx,'−',x-5,y+4,{c:NEG,w:700,s:10,a:'center'}); txt(ctx,'+',x+5,y+4,{c:POS,w:700,s:10,a:'center'}); }
    txt(ctx,'isolator',cx,cy+R+38,{w:700,a:'center',c:'#51606E'});
  }
  document.getElementById('fd_title').textContent=fdV==='geen'?'Homogeen veld zonder voorwerp':fdV==='iso'?'Isolator in een homogeen veld':'Geleider in een homogeen veld';
  document.getElementById('fd_readout').innerHTML=FT[fdV];
}
document.querySelectorAll('#fd_keuze button').forEach(b=>b.onclick=()=>{ fdV=b.dataset.v; document.querySelectorAll('#fd_keuze button').forEach(o=>o.classList.toggle('active',o===b)); fdTeken(); });
document.querySelectorAll('#fd_vb button').forEach(b=>b.onclick=()=>{ document.querySelectorAll('#fd_vb button').forEach(o=>o.classList.toggle('active',o===b)); document.getElementById('fd_vbTekst').innerHTML=VB[b.dataset.vb]; });

/* ---------------- ENERGIE EN POTENTIAAL ---------------- */
const ecv=document.getElementById('en_cv'), ectx=hd(ecv), EW=ecv._w, EH=ecv._h;
const DL={p:{q:1,m:1.673e-27,n:'proton'},e:{q:-1,m:9.109e-31,n:'elektron'},a:{q:2,m:6.645e-27,n:'α-deeltje'}};
const en={d:'p',h0:0.5,h:0.5,t0:null};
const YT=60, YB=380, XP=150; // + plaat boven, − plaat onder
function U(){ return +document.getElementById('en_U').value; } function D(){ return +document.getElementById('en_d').value; }
function enTeken(now){
  const u=U(), d=D(), p=DL[en.d];
  if(en.t0!=null){ const doel=p.q>0?0:1, tt=Math.min(1,(now-en.t0)/1800); en.h=en.h0+(doel-en.h0)*tt*tt; if(tt>=1) en.t0=null; }
  const ctx=ectx; ctx.clearRect(0,0,EW,EH); ctx.fillStyle='#fbfcfd'; ctx.fillRect(0,0,EW,EH);
  const yOf=h=>YB-h*(YB-YT);
  // equipotentiaal
  if(document.getElementById('en_eq').checked){ for(let i=1;i<5;i++){ const y=yOf(i/5); ctx.setLineDash([6,5]); ctx.strokeStyle='#2f8f6b'; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(40,y); ctx.lineTo(300,y); ctx.stroke(); ctx.setLineDash([]); txt(ctx,'V = '+nl(u*i/5,0)+' V',302,y+4,{c:'#2f8f6b',s:11}); } }
  // veldlijnen
  for(let i=0;i<5;i++){ const x=60+i*50; ctx.strokeStyle=LIJN; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(x,YT+6); ctx.lineTo(x,YB-6); ctx.stroke(); kop(ctx,x,(YT+YB)/2+20,Math.PI/2,LIJN); }
  ctx.fillStyle='#fde2e4'; ctx.fillRect(30,YT-16,280,14); ctx.fillStyle='#dbeafe'; ctx.fillRect(30,YB+2,280,14);
  for(let i=0;i<9;i++){ txt(ctx,'+',45+i*32,YT-4,{c:POS,w:700,a:'center'}); txt(ctx,'−',45+i*32,YB+14,{c:NEG,w:700,a:'center'}); }
  txt(ctx,'V = '+u+' V',312,YT-4,{c:POS,w:700,s:12}); txt(ctx,'V = 0 V',312,YB+14,{c:NEG,w:700,s:12});
  txt(ctx,'E',22,(YT+YB)/2,{c:LIJN,w:700,s:14,a:'center'});
  // deeltje
  const y=yOf(en.h), y0=yOf(en.h0);
  if(Math.abs(en.h-en.h0)>0.01){ ctx.setLineDash([3,4]); ctx.strokeStyle='#94a3b8'; ctx.beginPath(); ctx.arc(XP,y0,9,0,7); ctx.stroke(); ctx.setLineDash([]); txt(ctx,'A',XP-22,y0+4,{w:700}); txt(ctx,'B',XP-22,y+4,{w:700}); }
  bolLading(ctx,XP,y,p.q,11); pijl(ctx,XP+22,y,XP+22,y+(p.q>0?1:-1)*(16+10*Math.abs(p.q)),'#d64550',3); txt(ctx,'F',XP+36,y+(p.q>0?18:-12),{c:'#d64550',w:700});
  // hoogte d
  ctx.strokeStyle='#1D2A36'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(250,YB); ctx.lineTo(250,y); ctx.stroke(); txt(ctx,'d = '+nl(en.h*d,1)+' cm',256,(YB+y)/2+4,{s:12});
  // energiebalken (in eV)
  const V=u*en.h, V0=u*en.h0, Ep=p.q*V, Ep0=p.q*V0, Ek=Ep0-Ep, Etot=Ep0;
  const bx=400, zero=230, sc=150/(2*u), bar=(x,v,k,l)=>{ ctx.fillStyle=k; const hpx=v*sc; ctx.fillRect(x,zero-Math.max(0,hpx),40,Math.abs(hpx)); txt(ctx,l,x+20,EH-48,{a:'center',w:700,s:12}); txt(ctx,nl(v,0)+' eV',x+20,(hpx>=0?zero-hpx-6:zero-hpx+16),{a:'center',s:11}); };
  ctx.strokeStyle='#1D2A36'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(bx-10,zero); ctx.lineTo(bx+170,zero); ctx.stroke();
  bar(bx,Ep,'#2f8f6b','E_pot'); bar(bx+60,Ek,'#d97706','E_kin'); bar(bx+120,Etot,'#64748b','E_tot');
  txt(ctx,'energie (eV)',bx+80,32,{a:'center',w:700});
  // uitlezing
  const E=u/(d*0.01), v=Math.sqrt(Math.max(0,2*Ek*1.602e-19/p.m));
  document.getElementById('en_UVal').textContent=u+' V'; document.getElementById('en_dVal').textContent=d+' cm · E = '+nl(E,0)+' N/C';
  document.getElementById('en_readout').innerHTML=
   `<div class="readout-row"><span class="k">potentiaal in B: V = E · d</span><span class="num">${nl(V,0)} V</span></div>`+
   `<div class="readout-row"><span class="k">E<sub>pot</sub> = Q · V</span><span class="num">${nl(Ep,0)} eV = ${sci(Ep*1.602e-19,'J')}</span></div>`+
   `<div class="readout-row"><span class="k">U<sub>AB</sub> = V<sub>A</sub> − V<sub>B</sub></span><span class="num">${nl(V0-V,0)} V</span></div>`+
   `<div class="readout-row"><span class="k">W<sub>veld</sub> = −ΔE<sub>pot</sub> = ΔE<sub>kin</sub></span><span class="num">${nl(Ek,0)} eV</span></div>`+
   `<div class="readout-row"><span class="k">snelheid in B</span><span class="num">${sci(v,'m/s')}</span></div>`+
   `<div class="k" style="margin-top:6px">${p.q>0?'Een positieve lading beweegt <b>met</b> de veldlijnen mee, naar lagere potentiaal.':'Een negatieve lading beweegt <b>tegen</b> de veldlijnen in, naar hogere potentiaal.'} E<sub>pot</sub> neemt af, E<sub>kin</sub> neemt evenveel toe.</div>`;
}
let enSleep=false;
ecv.addEventListener('pointerdown',e=>{ en.t0=null; enSleep=true; ecv.setPointerCapture(e.pointerId); zetH(e); });
ecv.addEventListener('pointermove',e=>{ if(enSleep) zetH(e); });
ecv.addEventListener('pointerup',()=>enSleep=false);
function zetH(e){ const r=ecv.getBoundingClientRect(), y=(e.clientY-r.top)*EH/r.height; en.h0=en.h=Math.max(0,Math.min(1,(YB-y)/(YB-YT))); }
document.querySelectorAll('#en_deeltje button').forEach(b=>b.onclick=()=>{ en.d=b.dataset.d; en.h=en.h0; en.t0=null; document.querySelectorAll('#en_deeltje button').forEach(o=>o.classList.toggle('active',o===b)); });
document.getElementById('en_los').onclick=()=>{ en.h=en.h0; en.t0=performance.now(); };
document.getElementById('en_reset').onclick=()=>{ en.h=en.h0; en.t0=null; };

/* ---------------- tabbladen ---------------- */
const VIEWS={meer:'viewMeer',faraday:'viewFaraday',energie:'viewEnergie'};
document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>{
  const m=t.dataset.mode; Object.entries(VIEWS).forEach(([k,id])=>document.getElementById(id).style.display=k===m?'block':'none');
  document.getElementById('weergave').style.display=(m==='faraday'||m==='energie')?'none':'';
  if(m==='meer') tekenMl(); if(m==='faraday') fdTeken();
}));
(function lus(now){ if(state.mode==='energie') enTeken(now); requestAnimationFrame(lus); })(performance.now());
window.mlVeld=veld;
})();
</script>
