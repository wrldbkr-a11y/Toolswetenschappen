//////////////////// SCHEMA INVULLEN (effectoren) ////////////////////
(function(){
  const SC=[
    {s:'Je trapt per ongeluk op een punaise en trekt je voet terug.',r:'pijnreceptoren',e:'spieren',b:'onbewust'},
    {s:'Je ruikt frietjes en het water loopt je in de mond.',r:'chemoreceptoren',e:'klieren',b:'onbewust'},
    {s:'De bal komt op je af en je vangt hem.',r:'fotoreceptoren',e:'spieren',b:'bewust'},
    {s:'Je komt uit een donkere kamer in de zon en je pupillen worden klein.',r:'fotoreceptoren',e:'spieren',b:'onbewust'},
    {s:'Het is heel warm en je begint te zweten.',r:'thermoreceptoren',e:'klieren',b:'onbewust'},
    {s:'Je hoort de schoolbel en je pakt je boekentas.',r:'mechanoreceptoren',e:'spieren',b:'bewust'},
    {s:'Iemand roept plots luid achter je. Je schrikt en je hart gaat sneller slaan door adrenaline.',r:'mechanoreceptoren',e:'klieren',b:'onbewust'},
    {s:'Je voelt een mug op je arm en je slaat ze weg.',r:'mechanoreceptoren',e:'spieren',b:'bewust'},
  ];
  const REC=['fotoreceptoren','mechanoreceptoren','thermoreceptoren','chemoreceptoren','pijnreceptoren'];
  let goed=0,tot=0,q,ant={};
  function vraag(){ q=SC[Math.floor(Math.random()*SC.length)]; ant={};
    const blok=(k,t,opts)=>`<div class="schema-stap"><div class="schema-k">${t}</div><div class="keuzes" data-k="${k}">${opts.map(o=>`<button class="btn" data-a="${o}">${o}</button>`).join('')}</div></div>`;
    $('eff-vraag').innerHTML=`<p class="vraag">${q.s}</p><div class="schema">${blok('r','Welke receptor vangt de prikkel op?',REC)}${blok('e','Welke effector reageert?',['spieren','klieren'])}${blok('b','Is de reactie bewust of onbewust?',['bewust','onbewust'])}</div><div class="ctrl-row"><button class="btn primary" id="eff-ok">Controleer</button></div><div class="feedback" id="eff-fb"></div>`;
    $('eff-vraag').querySelectorAll('.keuzes').forEach(kz=>kz.querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>{ if(kz.dataset.klaar) return; ant[kz.dataset.k]=b.dataset.a; kz.querySelectorAll('[data-a]').forEach(x=>x.classList.toggle('on',x===b)); }));
    $('eff-ok').onclick=()=>{ if(Object.keys(ant).length<3){ $('eff-fb').className='feedback fout'; $('eff-fb').textContent='Kies eerst bij elke vraag een antwoord.'; return; }
      let n=0; ['r','e','b'].forEach(k=>{ const kz=$('eff-vraag').querySelector(`[data-k="${k}"]`); kz.dataset.klaar=1; kz.querySelectorAll('[data-a]').forEach(x=>{ x.classList.remove('on'); if(x.dataset.a===q[k]) x.classList.add('goed'); else if(x.dataset.a===ant[k]) x.classList.add('fout'); }); if(ant[k]===q[k]) n++; });
      tot+=3; goed+=n; $('eff-score').textContent=goed+' / '+tot;
      $('eff-fb').className='feedback '+(n===3?'goed':'fout');
      $('eff-fb').innerHTML=`${n} van de 3 juist.<span class="uitleg">prikkel → <b>${q.r}</b> → verwerking in het zenuwstelsel → <b>${q.e}</b> → reactie (<b>${q.b}</b>)</span><button class="btn" id="eff-nx" style="margin-top:8px">Volgende</button>`; $('eff-nx').onclick=vraag; };
  }
  vraag();
})();

//////////////////// SPIEREN (zelf getekend) ////////////////////
const SPIEREN=(function(){
  // gesloten vloeiende vorm door punten (Catmull-Rom → Bezier)
  function vorm(p){ const n=p.length; let d=`M${p[0][0]},${p[0][1]}`;
    for(let i=0;i<n;i++){ const p0=p[(i-1+n)%n],p1=p[i],p2=p[(i+1)%n],p3=p[(i+2)%n];
      d+=` C${(p1[0]+(p2[0]-p0[0])/6).toFixed(1)},${(p1[1]+(p2[1]-p0[1])/6).toFixed(1)} ${(p2[0]-(p3[0]-p1[0])/6).toFixed(1)},${(p2[1]-(p3[1]-p1[1])/6).toFixed(1)} ${p2[0]},${p2[1]}`; }
    return d+'Z'; }
  const spiegel=(p,cx,k)=>p.map(([x,y])=>[cx+k*x,y]);
  let defs=`<defs><linearGradient id="sp-r" x1="0" x2="1"><stop offset="0" stop-color="#a8322c"/><stop offset=".45" stop-color="#d8574c"/><stop offset="1" stop-color="#9a2b26"/></linearGradient>
    <linearGradient id="sp-h" x1="0" x2="1"><stop offset="0" stop-color="#e5b48e"/><stop offset="1" stop-color="#f3cfaf"/></linearGradient></defs>`;
  let huid='', spier='', id=0;
  function deel(p,cx,soort,hoek){ for(const k of [-1,1]){ const q=spiegel(p,cx,k), d=vorm(q);
      huid+=`<path d="${d}" fill="#f0c9a6" stroke="#f0c9a6" stroke-width="16" stroke-linejoin="round"/>`;
      if(soort==='huid'){ spier+=`<path d="${d}" fill="url(#sp-h)" stroke="#c48d66" stroke-width="1.5"/>`; continue; }
      if(soort==='pees'){ spier+=`<path d="${d}" fill="#f4efe2" stroke="#b9ae93" stroke-width="1.5"/>`; continue; }
      const c=`spc${id++}`; const xs=q.map(a=>a[0]), ys=q.map(a=>a[1]); const mx=(Math.min(...xs)+Math.max(...xs))/2, my=(Math.min(...ys)+Math.max(...ys))/2;
      spier+=`<clipPath id="${c}"><path d="${d}"/></clipPath><path d="${d}" fill="url(#sp-r)"/><g clip-path="url(#${c})" transform="rotate(${k*(hoek||0)} ${mx} ${my})">`;
      for(let x=Math.min(...xs)-60;x<Math.max(...xs)+60;x+=5) spier+=`<path d="M${x},${Math.min(...ys)-60} L${x},${Math.max(...ys)+60}" stroke="#7d1f1b" stroke-width="1" opacity=".38"/>`;
      spier+=`</g><path d="${d}" fill="none" stroke="#6b1a17" stroke-width="1.8"/>`; } }
  function hoofd(cx,achter){ huid+=`<ellipse cx="${cx}" cy="56" rx="34" ry="42" fill="#f0c9a6"/><rect x="${cx-15}" y="88" width="30" height="30" fill="#f0c9a6"/>`;
    spier+=`<ellipse cx="${cx}" cy="56" rx="33" ry="41" fill="url(#sp-h)" stroke="#c48d66" stroke-width="1.5"/>`+(achter?`<path d="M${cx-30},40 Q${cx},-6 ${cx+30},40 Q${cx+34},70 ${cx+24},84 Q${cx},70 ${cx-24},84 Q${cx-34},70 ${cx-30},40Z" fill="#5b3a24"/>`:`<path d="M${cx-30},40 Q${cx},0 ${cx+30},40 Q${cx+20},22 ${cx},22 Q${cx-20},22 ${cx-30},40Z" fill="#5b3a24"/><ellipse cx="${cx-12}" cy="56" rx="4" ry="3" fill="#3b2a1e"/><ellipse cx="${cx+12}" cy="56" rx="4" ry="3" fill="#3b2a1e"/><path d="M${cx-9},76 Q${cx},82 ${cx+9},76" stroke="#9a5b45" stroke-width="2" fill="none"/>`); }
  // ---- voorkant
  const F=230; hoofd(F,false);
  deel([[0,96],[16,98],[22,120],[0,124]],F,'huid');
  deel([[0,124],[30,118],[62,124],[76,150],[60,176],[30,184],[2,178]],F,'spier',60); // borstspier
  deel([[40,116],[64,112],[82,126],[90,152],[86,178],[74,162],[60,142],[46,128]],F,'spier',20); // deltaspier
  deel([[76,174],[90,168],[98,192],[102,232],[98,262],[90,268],[82,250],[76,214]],F,'spier',4); // biceps
  deel([[92,270],[105,266],[117,300],[123,350],[119,382],[108,384],[98,340],[92,300]],F,'spier',-8);
  deel([[108,384],[122,384],[130,410],[124,432],[112,434],[104,410]],F,'huid');
  for(const [y0,y1] of [[188,220],[224,254],[258,288],[292,336]]) deel([[3,y0],[28,y0+2],[29,y1],[3,y1]],F,'spier',0); // buikspieren
  deel([[30,186],[54,182],[64,220],[62,280],[56,322],[38,338],[31,300]],F,'spier',-25); // schuine buikspier
  deel([[2,336],[36,338],[56,330],[60,352],[30,356],[4,358]],F,'huid');
  deel([[16,356],[42,344],[62,354],[68,402],[60,452],[48,478],[30,478],[20,442],[13,394]],F,'spier',-6); // quadriceps
  deel([[26,478],[50,478],[52,500],[26,500]],F,'pees');
  deel([[24,500],[48,500],[56,540],[52,590],[45,612],[34,612],[28,570],[23,530]],F,'spier',4);
  deel([[30,612],[50,612],[64,628],[60,636],[28,636]],F,'huid');
  // ---- achterkant
  const A=670; hoofd(A,true);
  deel([[0,96],[16,98],[22,120],[0,124]],A,'huid');
  deel([[0,96],[14,100],[30,120],[66,126],[38,152],[12,212],[0,226]],A,'spier',-40); // trapeziusspier
  deel([[40,116],[64,112],[82,126],[90,152],[86,178],[74,162],[60,142],[46,128]],A,'spier',20);
  deel([[74,172],[90,166],[100,194],[102,238],[96,266],[86,270],[78,240],[72,200]],A,'spier',3); // triceps
  deel([[92,270],[105,266],[117,300],[123,350],[119,382],[108,384],[98,340],[92,300]],A,'spier',-8);
  deel([[108,384],[122,384],[130,410],[124,432],[112,434],[104,410]],A,'huid');
  deel([[8,218],[36,154],[72,172],[74,204],[62,252],[42,302],[12,314]],A,'spier',35); // brede rugspier
  deel([[2,226],[12,222],[14,330],[2,334]],A,'spier',0); // rugstrekker
  deel([[2,330],[32,316],[60,330],[66,364],[50,392],[14,396],[2,384]],A,'spier',-30); // bilspier
  deel([[10,394],[50,394],[62,422],[58,470],[46,492],[28,492],[16,460],[10,422]],A,'spier',2); // hamstrings
  deel([[20,500],[48,498],[60,532],[56,572],[45,592],[33,592],[23,562],[17,530]],A,'spier',0); // kuit
  deel([[33,590],[45,590],[44,616],[34,616]],A,'pees'); // achillespees
  deel([[28,614],[50,614],[56,630],[52,638],[26,638]],A,'huid');
  const tekst=`<text x="${F}" y="672" text-anchor="middle" font-size="20" font-weight="700" fill="#51606E">voorkant</text><text x="${A}" y="672" text-anchor="middle" font-size="20" font-weight="700" fill="#51606E">achterkant</text>`;
  return {svg:defs+huid+spier+tekst,F,A};
})();
labelFig({wrap:'fig-spieren',ctl:'ctl-spieren',inner:SPIEREN.svg,w:900,h:690,ml:210,mr:220,top:10,fs:22,r:12,gap:40,
  punten:[
    {naam:'biceps',x:SPIEREN.F-90,y:218,kant:'l',info:'Spier vooraan op de bovenarm. Trekt ze samen, dan <b>buig</b> je je arm.'},
    {naam:'buikspieren',x:SPIEREN.F-16,y:240,kant:'l',ly:300,info:'Spieren in de buikwand. Ze <b>beschermen</b> de organen, buigen de romp en helpen bij het uitademen.'},
    {naam:'quadriceps',x:SPIEREN.F-40,y:410,kant:'l',info:'Grote spier vooraan op de dij. Trekt ze samen, dan <b>strek</b> je je been (bv. bij een trap tegen een bal).'},
    {naam:'gewricht (knie)',x:SPIEREN.F+38,y:490,kant:'l',ly:520,info:'Een <b>gewricht</b> is een beweegbare verbinding tussen twee botten. In de knie scharnieren bovenbeen en onderbeen.'},
    {naam:'triceps',x:SPIEREN.A+88,y:218,kant:'r',info:'Spier achteraan op de bovenarm: de antagonist van de biceps. Trekt ze samen, dan <b>strek</b> je je arm.'},
    {naam:'rugspieren',x:SPIEREN.A-40,y:230,kant:'r',ly:300,info:'O.a. de trapeziusspier, de brede rugspier en de rugstrekkers. Ze houden je <b>rechtop</b> en bewegen schouders en armen.'},
    {naam:'hamstrings',x:SPIEREN.A+36,y:440,kant:'r',info:'Spieren achteraan op de dij. Ze <b>buigen</b> de knie: de antagonist van de quadriceps.'},
    {naam:'pees (achillespees)',x:SPIEREN.A+39,y:604,kant:'r',info:'Een <b>pees</b> is stevig, niet-rekbaar bindweefsel dat een spier aan een bot vastmaakt. De achillespees verbindt de kuitspier met het hielbeen.'},
  ],noot:'Gestileerde tekening: de spieren zijn rood, pezen wit.'});
$('gewrichten').innerHTML=[['schoudergewricht','kogelgewricht: bewegen in alle richtingen'],['ellebooggewricht','scharniergewricht: buigen en strekken'],['heupgewricht','kogelgewricht'],['kniegewricht','scharniergewricht'],['polsgewricht','bewegen in twee richtingen'],['enkelgewricht','voet op en neer bewegen'],['vingergewrichten','scharniergewrichten']].map(([t,u])=>`<div class="card"><div class="txt"><h4>${t}</h4><p>${u}</p></div></div>`).join('');

//////////////////// SOORTEN SPIERWEEFSEL ////////////////////
(function(){
  const s=$('svg-spiertypes'); let h='';
  const paneel=(x,titel,sub,inner,id)=>{ h+=`<clipPath id="${id}"><circle cx="${x+140}" cy="160" r="120"/></clipPath><circle cx="${x+140}" cy="160" r="124" fill="#2b2b2b"/><g clip-path="url(#${id})"><rect x="${x+20}" y="40" width="240" height="240" fill="#fbe9ee"/>${inner}</g><circle cx="${x+140}" cy="160" r="122" fill="none" stroke="#475569" stroke-width="4"/>`;
    h+=`<text x="${x+140}" y="312" text-anchor="middle" font-size="18" font-weight="700" fill="#1D2A36">${titel}</text><text x="${x+140}" y="332" text-anchor="middle" font-size="13" fill="#51606E">${sub}</text>`; };
  // dwarsgestreept
  let a='';
  for(let i=0;i<4;i++){ const y=58+i*58; a+=`<rect x="0" y="${y}" width="320" height="50" rx="10" fill="#e79aa8" stroke="#a8455a" stroke-width="2"/>`;
    for(let x=10;x<320;x+=9) a+=`<rect x="${x}" y="${y+2}" width="4" height="46" fill="#b95a6e" opacity=".75"/>`;
    for(let k=0;k<4;k++){ const nx=40+k*70+i*13; a+=`<ellipse cx="${nx}" cy="${y+(k%2?6:44)}" rx="14" ry="4.5" fill="#5b2a8a"/>`; } }
  paneel(10,'dwarsgestreepte spier','skeletspieren (bv. biceps)',a,'cpa');
  // glad
  let b='';
  for(let r=0;r<6;r++) for(let c=0;c<4;c++){ const x=320+c*72+(r%2?36:0), y=58+r*40;
    b+=`<path d="M${x-50},${y} Q${x},${y-18} ${x+50},${y} Q${x},${y+18} ${x-50},${y}Z" fill="#f0b3bf" stroke="#b0566b" stroke-width="1.8"/><ellipse cx="${x}" cy="${y}" rx="15" ry="4" fill="#5b2a8a"/>`; }
  paneel(310,'gladde spier','wand van darmen en bloedvaten',b,'cpb');
  // hartspier
  let c='';
  const X=620;
  for(let i=0;i<4;i++){ const y=62+i*56; c+=`<path d="M${X},${y} L${X+300},${y+4} L${X+300},${y+40} L${X},${y+38}Z" fill="#e48d9f" stroke="#a3435a" stroke-width="2"/>`;
    for(let x=X+6;x<X+300;x+=9) c+=`<rect x="${x}" y="${y+2}" width="3.5" height="36" fill="#b5566b" opacity=".7"/>`;
    for(const dx of [70,170,250]) c+=`<path d="M${X+dx+i*8},${y+1} l5,9 l-5,9 l5,9 l-5,9" fill="none" stroke="#3b1430" stroke-width="3.5"/>`;
    for(const dx of [30,120,210]) c+=`<ellipse cx="${X+dx+i*8}" cy="${y+20}" rx="10" ry="6" fill="#5b2a8a"/>`;
    if(i<3) c+=`<path d="M${X+130+i*20},${y+38} L${X+150+i*20},${y+56} L${X+175+i*20},${y+56} L${X+158+i*20},${y+38}Z" fill="#e48d9f" stroke="#a3435a" stroke-width="2"/>`; }
  paneel(610,'hartspier','alleen in het hart',c,'cpc');
  s.innerHTML=h;
  // vergelijkingstabel
  const R=[['heeft dwarse strepen',[1,0,1]],['veel kernen per cel, aan de rand',[1,0,0]],['één kern per cel, in het midden',[0,1,1]],['cellen zijn vertakt',[0,0,1]],['werkt bewust (je kan ze sturen)',[1,0,0]],['werkt onbewust (vanzelf)',[0,1,1]],['raakt snel vermoeid',[1,0,0]]];
  const t=$('st-tabel');
  t.innerHTML='<tr><th></th><th>dwarsgestreept</th><th>glad</th><th>hartspier</th></tr>'+R.map((r,i)=>`<tr><th>${r[0]}</th>${[0,1,2].map(j=>`<td><input type="checkbox" data-r="${i}" data-j="${j}"></td>`).join('')}</tr>`).join('');
  $('st-check').onclick=()=>{ let g=0; t.querySelectorAll('input').forEach(c=>{ const ok=c.checked===!!R[+c.dataset.r][1][+c.dataset.j]; c.parentNode.className=ok?'ok-cel':'fout-cel'; if(ok) g++; }); $('st-score').textContent=g+' / '+R.length*3+' vakjes juist'; };
  $('st-opl').onclick=()=>{ t.querySelectorAll('input').forEach(c=>{ c.checked=!!R[+c.dataset.r][1][+c.dataset.j]; c.parentNode.className='ok-cel'; }); };
})();

//////////////////// ANTAGONISTEN: ARM EN BEEN ////////////////////
(function(){
  const s=$('svg-arm'), read=$('arm-read');
  let led='arm', th=80, doel=80, actief=null;
  const S=[300,70], E=[300,292];
  const CFG={arm:{rust:80,a:-28,b:80,LV:215,sA:'biceps',sB:'triceps',bA:'Biceps trekt samen',bB:'Triceps trekt samen',gew:'elleboog (gewricht)',bot:'opperarmbeen'},
             been:{rust:90,a:90,b:180,LV:190,sA:'quadriceps',sB:'hamstrings',bA:'Quadriceps trekt samen',bB:'Hamstrings trekken samen',gew:'knie (gewricht)',bot:'dijbeen'}};
  function zet(){ const c=CFG[led]; $('arm-buig').textContent=c.bA; $('arm-strek').textContent=c.bB; th=doel=c.rust; actief=null; }
  document.querySelectorAll('[data-ledemaat]').forEach(b=>b.onclick=()=>{ led=b.dataset.ledemaat; document.querySelectorAll('[data-ledemaat]').forEach(x=>x.classList.toggle('on',x===b)); zet(); });
  $('arm-buig').onclick=()=>{ doel=CFG[led].a; actief='a'; };
  $('arm-strek').onclick=()=>{ doel=CFG[led].b; actief='b'; };
  const lijn=(a,b,w,k)=>`<path d="M${a} L${b}" stroke="${k}" stroke-width="${w}" stroke-linecap="round"/>`;
  const bot=(a,b,w)=>lijn(a,b,w+5,'#a8946a')+lijn(a,b,w,'#f3e9d3')+lijn(a,b,w*0.35,'#fbf6ea');
  // spier: buik vanaf de oorsprong, pees (vaste lengte T) tot de aanhechting, eventueel over een omleidingspunt (knieschijf)
  function spier(pad,kant,vol,T,kleur){
    const d=(a,b)=>Math.hypot(b[0]-a[0],b[1]-a[1]);
    let Leff=0; for(let k=1;k<pad.length;k++) Leff+=d(pad[k-1],pad[k]);
    const o=pad[0], q=pad[1], L1=d(o,q), ux=(q[0]-o[0])/L1, uy=(q[1]-o[1])/L1;
    const B=Math.max(50,Math.min(L1-6,Leff-T));
    let nx=-uy, ny=ux; if(nx*kant<0){ nx=-nx; ny=-ny; }
    const w=Math.min(60,vol/B), a=[o[0]+ux*B*0.1,o[1]+uy*B*0.1], b=[o[0]+ux*B,o[1]+uy*B], m=[(a[0]+b[0])/2,(a[1]+b[1])/2];
    const c1=[m[0]+nx*w*1.7,m[1]+ny*w*1.7], c2=[m[0]-nx*w*0.25,m[1]-ny*w*0.25];
    const pees=[b,...pad.slice(1)].map(p=>p.join(',')).join(' L');
    let h=lijn(o,a,10,'#a8946a')+lijn(o,a,7,'#f4efe2')+`<path d="M${pees}" fill="none" stroke="#a8946a" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><path d="M${pees}" fill="none" stroke="#f4efe2" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`;
    h+=`<path d="M${a} Q${c1} ${b} Q${c2} ${a}Z" fill="${kleur}" stroke="#6b1a17" stroke-width="2.4"/>`;
    for(let k=1;k<6;k++){ const f=k/6; h+=`<path d="M${a} Q${m[0]+nx*w*(1.7*f-0.25*(1-f))},${m[1]+ny*w*(1.7*f-0.25*(1-f))} ${b}" fill="none" stroke="#7d1f1b" stroke-width="1.1" opacity=".45"/>`; }
    return {h,mid:[m[0]+nx*w*0.75,m[1]+ny*w*0.75],L:B};
  }
  lus('e4',dt=>{
    const c=CFG[led], vorig=th; th+=(doel-th)*Math.min(1,dt*2.2); const beweegt=Math.abs(th-vorig)>0.05;
    const a=th*Math.PI/180, u=[Math.cos(a),Math.sin(a)], n=[-u[1],u[0]], W=[E[0]+u[0]*c.LV,E[1]+u[1]*c.LV];
    s.setAttribute('viewBox',led==='arm'?'0 0 820 440':'0 0 820 530');
    let h=`<rect width="820" height="530" fill="#fbfcfe"/>`;
    h+=lijn([S[0],S[1]+10],E,led==='arm'?92:120,'rgba(240,201,166,.35)')+lijn(E,W,led==='arm'?74:90,'rgba(240,201,166,.35)');
    if(led==='arm') h+=`<path d="M250,26 L360,34 L350,92 L272,96Z" fill="#efe3c8" stroke="#a8946a" stroke-width="2.5"/>`;
    else h+=`<path d="M220,20 Q300,0 380,24 L360,80 Q300,96 240,80Z" fill="#efe3c8" stroke="#a8946a" stroke-width="2.5"/>`;
    h+=`<circle cx="${S[0]}" cy="${S[1]}" r="24" fill="#f3e9d3" stroke="#a8946a" stroke-width="2.5"/>`+bot(S,E,led==='arm'?26:32)+`<circle cx="${E[0]}" cy="${E[1]}" r="19" fill="#f3e9d3" stroke="#a8946a" stroke-width="2.5"/>`;
    let padA, padB, botLab='';
    if(led==='arm'){
      const U0=[E[0]+n[0]*7-u[0]*22,E[1]+n[1]*7-u[1]*22], U1=[W[0]+n[0]*7,W[1]+n[1]*7], R0=[E[0]-n[0]*9+u[0]*8,E[1]-n[1]*9+u[1]*8], R1=[W[0]-n[0]*8,W[1]-n[1]*8];
      h+=bot(U0,U1,15)+bot(R0,R1,14); const mU=[U0[0]+(U1[0]-U0[0])*0.7+n[0]*36,U0[1]+(U1[1]-U0[1])*0.7+n[1]*36], mR=[R0[0]+(R1[0]-R0[0])*0.7-n[0]*36,R0[1]+(R1[1]-R0[1])*0.7-n[1]*36]; botLab=`<text x="${mU[0]}" y="${mU[1]}" text-anchor="middle" font-size="14" font-weight="700" fill="#7a6a45" stroke="#fff" stroke-width="4" paint-order="stroke">ellepijp</text><text x="${mR[0]}" y="${mR[1]}" text-anchor="middle" font-size="14" font-weight="700" fill="#7a6a45" stroke="#fff" stroke-width="4" paint-order="stroke">spaakbeen</text>`;
      h+=`<g transform="translate(${W[0]},${W[1]}) rotate(${th})"><path d="M-4,-20 C24,-24 52,-20 64,-8 C70,0 64,12 52,14 C38,20 14,20 -4,18Z" fill="#f0c9a6" stroke="#c48d66" stroke-width="2"/></g>`;
      padA=[[318,92],[E[0]+u[0]*40-n[0]*14,E[1]+u[1]*40-n[1]*14]]; padB=[[282,96],[E[0]-u[0]*24+n[0]*10,E[1]-u[1]*24+n[1]*10]];
    } else {
      h+=bot([E[0]+u[0]*6,E[1]+u[1]*6],W,24);
      h+=`<g transform="translate(${W[0]},${W[1]}) rotate(${th-90})"><path d="M-22,-6 C-24,14 -10,22 10,22 L70,24 C80,24 82,10 70,6 L18,-6Z" fill="#f0c9a6" stroke="#c48d66" stroke-width="2"/></g>`;
      const f=(th-90)*Math.PI/360, P=[E[0]+34*Math.cos(f),E[1]+34*Math.sin(f)];
      padA=[[318,92],P,[E[0]+u[0]*50-n[0]*14,E[1]+u[1]*50-n[1]*14]]; padB=[[282,96],[E[0]+u[0]*34+n[0]*16,E[1]+u[1]*34+n[1]*16]];
      h+=`<ellipse cx="${P[0]}" cy="${P[1]}" rx="9" ry="13" fill="#f3e9d3" stroke="#a8946a" stroke-width="2"/>`;
    }
    const A=spier(padA,1,led==='arm'?5500:6500,led==='arm'?60:90,actief==='a'&&beweegt?'#e2574c':'#c7463e');
    const B=spier(padB,-1,led==='arm'?5000:5500,led==='arm'?50:60,actief==='b'&&beweegt?'#e2574c':'#b23e38');
    h+=B.h+A.h;
    h+=`<circle cx="${E[0]}" cy="${E[1]}" r="32" fill="none" stroke="#2F6FB0" stroke-width="2.5" stroke-dasharray="6 5"/>`;
    const imp=p=>`<path d="M${p[0]-6},${p[1]-16} l10,0 l-6,10 l8,0 l-14,20 l4,-14 l-8,0z" fill="#facc15" stroke="#a16207" stroke-width="1.2"/>`;
    if(beweegt&&actief==='a') h+=imp([A.mid[0]+34,A.mid[1]]); if(beweegt&&actief==='b') h+=imp([B.mid[0]-34,B.mid[1]]);
    const lab=(t,p,q,kl='#1D2A36')=>`<path d="M${p} L${q}" stroke="${kl}" stroke-width="1.4"/><text x="${q[0]+6}" y="${q[1]+5}" font-size="16" font-weight="700" fill="${kl}" stroke="#fff" stroke-width="4" paint-order="stroke">${t}</text>`;
    const lb=(t,p,q,kl='#1D2A36')=>`<path d="M${p} L${q}" stroke="${kl}" stroke-width="1.4"/><text x="${q[0]-6}" y="${q[1]+5}" text-anchor="end" font-size="16" font-weight="700" fill="${kl}" stroke="#fff" stroke-width="4" paint-order="stroke">${t}</text>`;
    h+=lab(c.sA+(led==='been'?' (voorkant)':''),A.mid,[580,120],'#9a2b26')+lb(c.sB+(led==='been'?' (achterkant)':''),B.mid,[236,160],'#9a2b26')+lab('pees',led==='arm'?[318,86]:padA[2],led==='arm'?[470,40]:[560,250])+(led==='arm'?lb(c.gew,[E[0]-32,E[1]],[200,300],'#2F6FB0'):lab(c.gew,[E[0]+30,E[1]+12],[560,310],'#2F6FB0'))+lb(c.bot,[S[0]-14,S[1]+70],[200,60]);
    h+=botLab;
    h+=`<g transform="translate(600,350)" font-size="14"><text font-weight="700">lengte ${c.sA}</text><rect y="8" width="${A.L}" height="10" rx="5" fill="#c7463e"/><text y="44" font-weight="700">lengte ${c.sB}</text><rect y="52" width="${B.L}" height="10" rx="5" fill="#b23e38"/></g>`;
    s.innerHTML=h;
    const T={arm:{a:'De <b>biceps</b> krijgt een impuls en <b>trekt samen</b>: ze wordt korter en dikker. Via de pees trekt ze aan de onderarm: de arm <b>buigt</b>.<br>De <b>triceps</b> ontspant en wordt <b>uitgerekt</b>.',b:'De <b>triceps</b> trekt samen: de arm <b>strekt</b>.<br>De <b>biceps</b> ontspant en wordt uitgerekt. Biceps en triceps zijn elkaars <b>antagonisten</b>.'},
      been:{a:'De <b>quadriceps</b> (voorkant van de dij) trekt samen. Via de pees over de knieschijf trekt ze aan het scheenbeen: het been <b>strekt</b> (zoals bij een trap tegen een bal).<br>De <b>hamstrings</b> ontspannen en worden uitgerekt.',b:'De <b>hamstrings</b> (achterkant van de dij) trekken samen: de knie <b>buigt</b>.<br>De <b>quadriceps</b> ontspant en wordt uitgerekt. Quadriceps en hamstrings zijn elkaars <b>antagonisten</b>.'}};
    read.innerHTML=actief?T[led][actief]:'Klik op een knop om een spier een impuls te geven.';
  });
})();

//////////////////// SLOKDARM: PERISTALTIEK ////////////////////
(function(){
  const s=$('svg-slok'), read=$('slok-read');
  let p=-60, loopt=false, v=22, model='echt';
  document.querySelectorAll('[data-pm]').forEach(b=>b.onclick=()=>{ model=b.dataset.pm; document.querySelectorAll('[data-pm]').forEach(x=>x.classList.toggle('on',x===b)); p=-60; loopt=false; });
  $('slok-start').onclick=()=>{ p=-60; loopt=true; $('slok-pauze').textContent='⏸ Pauze'; };
  $('slok-pauze').onclick=()=>{ loopt=!loopt; $('slok-pauze').textContent=loopt?'⏸ Pauze':'▶ Verder'; };
  $('slok-v').oninput=e=>{ v=+e.target.value; };
  const X0=40,X1=860,CY=165,R0=58,BR=44;
  const g=(x,m,w)=>Math.exp(-(((x-m)/w)**2));
  lus('e4',dt=>{
    if(loopt){ p+=dt*v; if(p>X1+90){ p=X1+90; loopt=false; } }
    $('slok-v-l').textContent='Snelheid: '+(v<20?'heel traag':v<40?'traag':'sneller');
    const kring=x=>g(x,p-BR-8,38), lengte=x=>model==='boek'?g(x,p+BR+12,38):Math.min(1,1.15*g(x,p-BR*0.2,Math.max(1,(x>p-BR*0.2)?95:55)));
    const r=x=>{ let rr=R0-34*kring(x)+12*lengte(x); if(Math.abs(x-p)<BR+6) rr=Math.max(rr,Math.sqrt(Math.max(0,(BR+6)**2-(x-p)**2))+6); return rr; };
    // lengtespieren trekken samen: wand korter → merktekens schuiven naar elkaar
    const verschuif=x=>{ let d=0; for(let t=X0;t<x;t+=6) d+=lengte(t)*0.28*6; return x-d*0.5; };
    let h=`<rect width="900" height="470" fill="#fbfcfe"/>`;
    let top='',bot='',tin='',bin='';
    for(let x=X0;x<=X1;x+=4){ const rr=r(x); top+=(x===X0?'M':' L')+x+','+(CY-rr-18); bot+=(x===X0?'M':' L')+x+','+(CY+rr+18); tin+=(x===X0?'M':' L')+x+','+(CY-rr); bin+=(x===X0?'M':' L')+x+','+(CY+rr); }
    // binnenkant (lumen)
    h+=`<path d="${tin} L${X1},${CY} L${X0},${CY}Z" fill="#fde7e2"/><path d="${bin} L${X1},${CY} L${X0},${CY}Z" fill="#fde7e2"/>`;
    // wand: lengtespieren (buiten, blauw) en kringspieren (binnen, rood)
    for(const k of [-1,1]){
      for(let x=X0;x<X1;x+=4){ const rr=r(x), l=lengte(x), c=kring(x);
        h+=`<rect x="${x}" y="${k<0?CY-rr-18:CY+rr+9}" width="4.5" height="9" fill="rgb(${Math.round(150-110*l)},${Math.round(180-110*l)},${Math.round(230-40*l)})"/>`;
        h+=`<rect x="${x}" y="${k<0?CY-rr-9:CY+rr}" width="4.5" height="9" fill="rgb(${Math.round(240-30*c)},${Math.round(170-130*c)},${Math.round(170-130*c)})"/>`; }
    }
    // merktekens van de lengte (tonen de verkorting)
    for(let x=X0+20;x<X1;x+=40){ const xx=verschuif(x), rr=r(xx); h+=`<path d="M${xx},${CY-rr-18} v-10 M${xx},${CY+rr+18} v10" stroke="#1e3a8a" stroke-width="2"/>`; }
    // kringspieren als ringen
    for(let x=X0+12;x<X1;x+=22){ const c=kring(x), rr=r(x); h+=`<ellipse cx="${x}" cy="${CY}" rx="${2.5+6*c}" ry="${rr+9}" fill="none" stroke="${c>0.25?'#b91c1c':'#e7a3a3'}" stroke-width="${1.6+3.5*c}" opacity="${0.35+0.6*c}"/>`; }
    h+=`<path d="${top}" fill="none" stroke="#475569" stroke-width="1.5"/><path d="${bot}" fill="none" stroke="#475569" stroke-width="1.5"/>`;
    if(p>X0-BR&&p<X1+BR) h+=`<ellipse cx="${p}" cy="${CY}" rx="${BR}" ry="${BR-4}" fill="#a0723f" stroke="#6b4423" stroke-width="2"/><text x="${p}" y="${CY+5}" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">voedselbrok</text>`;
    // pijlen en uitleg bij de zones
    if(p>X0&&p<X1){
      const xa=p-BR-8, xv=p+BR+12;
      if(xa>X0+10){ h+=`<path d="M${xa},40 V${CY-r(xa)-24}" stroke="#b91c1c" stroke-width="2"/><text x="${xa}" y="26" text-anchor="end" font-size="14" font-weight="700" fill="#b91c1c">achter de brok</text>`;
}
      if(xv<X1-10) h+=`<path d="M${xv},40 V${CY-r(xv)-24}" stroke="#1e40af" stroke-width="2"/><text x="${xv}" y="26" text-anchor="start" font-size="14" font-weight="700" fill="#1e40af">voor de brok</text>`;
    }
    // staafjes: toestand per plaats
    const rij=(y,t,f,kl,kl0)=>{ h+=`<text x="${X0}" y="${y-8}" font-size="14" font-weight="700" fill="#1D2A36">${t}</text>`;
      for(let x=X0;x<X1;x+=6){ const a=f(x); h+=`<rect x="${x}" y="${y}" width="6.5" height="16" fill="${a>0.4?kl:kl0}" opacity="${0.3+0.7*a}"/>`; } };
    rij(330,'kringspieren',kring,'#b91c1c','#f3c4c4'); rij(390,'lengtespieren',lengte,'#1e40af','#c7d2fe');
    h+=`<g font-size="12" fill="#51606E"><text x="${X1}" y="322" text-anchor="end">donker = samengetrokken · licht = ontspannen</text><text x="${X0}" y="445">mond →</text><text x="${X1}" y="445" text-anchor="end">→ maag</text></g>`;
    // vaste plaats markeren
    const XZ=260, rz=r(XZ);
    h+=`<circle cx="${XZ}" cy="${CY-rz-9}" r="17" fill="none" stroke="#d97706" stroke-width="3"/><circle cx="${XZ}" cy="${CY+rz+9}" r="17" fill="none" stroke="#d97706" stroke-width="3"/><path d="M${XZ+12},${CY+rz+21} l14,14" stroke="#d97706" stroke-width="4" stroke-linecap="round"/><text x="${XZ+30}" y="${CY+rz+52}" font-size="13" font-weight="700" fill="#b45309">vergrootglas</text>`;
    s.innerHTML=h;
    // ----- vergrootglas -----
    const c=kring(XZ), l=lengte(XZ), brokHier=Math.abs(p-XZ)<BR;
    let fase=0; if(c>0.3) fase=3; else if(brokHier) fase=2; else if(l>0.3) fase=1; else if(p>XZ) fase=4;
    const echt=model==='echt';
    const bxz=230+(p-XZ)*2.4, brokZ=Math.abs(bxz-230)<190; const Lz=260*(1-0.28*l+0.1*c), Rz=Math.max(26,70*(1-0.55*c+0.25*l)), Rx=x=>{ const d=Math.abs(x-bxz); return brokZ&&d<62?Math.max(Rz,Math.sqrt(62*62-d*d)+2):Rz; }, mx=230, my=165, xa=mx-Lz/2, xb=mx+Lz/2;
    let z=`<rect width="900" height="330" fill="#fbfcfe"/>`;
    // wand: buitenlaag lengtespieren, binnenlaag kringspieren
    const pad=(off,k)=>{ let d=''; for(let x=xa;x<=xb;x+=4) d+=(x===xa?'M':' L')+x+','+(my+k*(Rx(x)+off)); return d; };
    z+=`<path d="${pad(16,-1)} L${xb},${my} L${xa},${my}Z" fill="#fde7e2"/><path d="${pad(16,1)} L${xb},${my} L${xa},${my}Z" fill="#fde7e2"/>`;
    if(brokZ) z+=`<clipPath id="zclip"><rect x="${xa}" y="0" width="${Lz}" height="330"/></clipPath><ellipse clip-path="url(#zclip)" cx="${bxz}" cy="${my}" rx="60" ry="58" fill="#a0723f" opacity=".9"/>`;
    for(const [off,k] of [[12,-1],[4,-1],[4,1],[12,1]]) z+=`<path d="${pad(off,k)}" fill="none" stroke="${l>0.3?'#1e3a8a':'#93a8d8'}" stroke-width="${3+5*l}" stroke-linecap="round"/>`;
    for(let k=0;k<5;k++){ const x=xa+Lz*(k+0.5)/5; z+=`<ellipse cx="${x}" cy="${my}" rx="${6+4*c}" ry="${Rx(x)}" fill="none" stroke="${c>0.3?'#b91c1c':'#eba3a3'}" stroke-width="${3+6*c}"/>`; }
    // pijlen
    const pijl=(x1,y1,x2,y2,k)=>{ const a=Math.atan2(y2-y1,x2-x1); return `<path d="M${x1},${y1} L${x2},${y2}" stroke="${k}" stroke-width="3"/><path d="M${x2},${y2} l${-10*Math.cos(a-0.5)},${-10*Math.sin(a-0.5)} M${x2},${y2} l${-10*Math.cos(a+0.5)},${-10*Math.sin(a+0.5)}" stroke="${k}" stroke-width="3"/>`; };
    if(fase===1){ z+=pijl(xa-50,my,xa-14,my,'#1e3a8a')+pijl(xb+50,my,xb+14,my,'#1e3a8a')+pijl(mx,my-Rz+18,mx,my-Rz-34,'#b91c1c')+pijl(mx,my+Rz-18,mx,my+Rz+34,'#b91c1c'); }
    if(fase===3){ z+=pijl(mx,my-Rz-44,mx,my-Rz-6,'#b91c1c')+pijl(mx,my+Rz+44,mx,my+Rz+6,'#b91c1c')+(echt&&l>0.3?pijl(xa-50,my,xa-14,my,'#1e3a8a')+pijl(xb+50,my,xb+14,my,'#1e3a8a'):pijl(xa-6,my,xa-46,my,'#1e3a8a')+pijl(xb+6,my,xb+46,my,'#1e3a8a')); }
    if(echt&&fase===1){ z=z; }
    const st=(t,y,kl,on)=>`<text x="${mx}" y="${y}" text-anchor="middle" font-size="14" font-weight="700" fill="${kl}">${t}</text>`;
    z+=`<text x="${mx}" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#1e3a8a">lengtespieren: ${l>0.3?'trekken samen → korter':(fase===3&&!echt?'ontspannen, worden uitgerekt':'ontspannen')}</text>`;
    z+=`<text x="${mx}" y="318" text-anchor="middle" font-size="14" font-weight="700" fill="#b91c1c">kringspieren: ${c>0.3?'trekken samen → smaller':(fase===1?'ontspannen, worden uitgerekt':'ontspannen')}</text>`;
    // stappen
    const STe=['Rust: beide spierlagen ontspannen.','De brok komt eraan: de <b>lengtespieren</b> beginnen samen te trekken. Dit stuk wordt <b>korter en wijder</b>: de wand schuift als het ware over de brok heen.','De brok glijdt erdoor. De lengtespieren blijven samengetrokken.','De <b>kringspieren</b> trekken samen terwijl de <b>lengtespieren nog samengetrokken</b> zijn. Het stuk is kort, dus de spiervezels liggen dicht op elkaar: de kringspieren knijpen <b>krachtiger</b>. De wand is ingekort, dus de brok legt per samentrekking een <b>langere weg</b> af.','Rust: beide spierlagen weer ontspannen.'];
    const ST=['Rust: beide spierlagen ontspannen.','De brok komt eraan: de <b>lengtespieren trekken samen</b>. Dit stuk wordt korter en wijder. De ontspannen <b>kringspieren worden uitgerekt</b>.','De brok glijdt erdoor.','De brok is voorbij: de <b>kringspieren trekken samen</b>. Dit stuk wordt smal en duwt de brok verder. De ontspannen <b>lengtespieren worden uitgerekt</b>.','Rust: beide spierlagen weer ontspannen.'];
    const kort=echt?['rust','lengtespieren samen','brok passeert','beide samen','rust']:['rust','lengtespieren samen','brok passeert','kringspieren samen','rust'];
    kort.forEach((t,i)=>{ const x=480+i*84, on=i===fase; z+=`<rect x="${x}" y="40" width="78" height="44" rx="8" fill="${on?'#fef3c7':'#f1f5f9'}" stroke="${on?'#d97706':'#cbd5e1'}" stroke-width="${on?2.5:1}"/><text x="${x+39}" y="${t.length>12?58:66}" text-anchor="middle" font-size="10.5" font-weight="${on?700:500}" fill="#1D2A36">${t.length>12?t.split(' ')[0]:t}</text>${t.length>12?`<text x="${x+39}" y="74" text-anchor="middle" font-size="10.5" font-weight="${on?700:500}" fill="#1D2A36">${t.split(' ').slice(1).join(' ')}</text>`:''}`; if(i<4) z+=`<path d="M${x+79},62 h4" stroke="#94a3b8" stroke-width="2"/>`; });
    z+=`<foreignObject x="480" y="100" width="410" height="200"><div xmlns="http://www.w3.org/1999/xhtml" style="font:15px/1.55 Inter,sans-serif;color:#1D2A36">${(echt?STe:ST)[fase]}<br/><span style="color:#51606E;font-size:13.5px">${echt?'Metingen tonen dat lengte- en kringspieren grotendeels tegelijk samentrekken. Na de golf worden ze door elkaar en door de elasticiteit van de wand weer uitgerekt.':'Trekt de ene laag samen, dan ontspant de andere en wordt ze uitgerekt. Kringspieren en lengtespieren zijn <b>antagonisten</b>.'}</span></div></foreignObject>`;
    $('svg-slok-zoom').innerHTML=z;
    if(echt&&p>=X0&&p<=X1){ read.innerHTML='<b style="color:#1e40af">Lengtespieren:</b> trekken samen vanaf net voor de brok tot net erachter. De slokdarm wordt daar <b>korter</b>: de wand wordt over de brok getrokken en wordt er <b>wijder</b>.<br><b style="color:#b91c1c">Kringspieren:</b> trekken samen achter de brok, <b>terwijl</b> de lengtespieren nog samengetrokken zijn. Doordat het stuk korter is, liggen de spiervezels dichter op elkaar en knijpen ze <b>krachtiger</b>.<br>Samen verplaatsen ze de brok sneller en met meer kracht. Deze golf heet <b>peristaltiek</b> en gebeurt onbewust.'; return; }
    read.innerHTML=(p<X0||p>X1)?'Klik op <b>Slikken</b> en volg de brok. Kijk naar de kleuren in de wand: <b style="color:#b91c1c">rood</b> zijn de kringspieren, <b style="color:#1e40af">blauw</b> de lengtespieren. Donker = samengetrokken.':
      '<b style="color:#b91c1c">Achter de brok:</b> de <b>kringspieren trekken samen</b> en de lengtespieren ontspannen. De slokdarm wordt daar <b>smal</b> en duwt de brok verder.<br><b style="color:#1e40af">Voor de brok:</b> de <b>lengtespieren trekken samen</b> en de kringspieren ontspannen. De slokdarm wordt daar <b>korter en wijder</b> (kijk naar de streepjes), zodat de brok erin kan.<br>Kringspieren en lengtespieren zijn <b>antagonisten</b>. Deze golf heet <b>peristaltiek</b> en gebeurt <b>onbewust</b>.';
  });
})();
