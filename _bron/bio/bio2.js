//////////////////// PRIKKEL → REACTIE ////////////////////
(function(){
  const s=$('svg-schema'), read=$('schema-read'), box=$('schema-vb');
  const VB=[
    {n:'hete kookplaat',p:'warmte van de kookplaat',r:'thermo- en pijnreceptoren in de huid',v:'ruggenmerg (reflex)',e:'spieren van de arm',ef:'je trekt je hand terug',m:'extern',b:'onbewust'},
    {n:'fel licht',p:'veel licht',r:'fotoreceptoren in het netvlies',v:'hersenen',e:'kringspier van de iris',ef:'de pupil wordt kleiner',m:'extern',b:'onbewust'},
    {n:'geur van eten',p:'geurstoffen in de lucht',r:'chemoreceptoren in de neus',v:'hersenen',e:'speekselklieren',ef:'je maakt meer speeksel',m:'extern',b:'onbewust'},
    {n:'dorst',p:'te weinig water in het bloed',r:'receptoren in de hersenen',v:'hersenen',e:'spieren (je gaat drinken)',ef:'het watergehalte wordt weer normaal',m:'intern',b:'bewust'},
    {n:'plant en licht',p:'licht valt van één kant',r:'lichtgevoelige cellen in de stengeltop',v:'groeistof (plantenhormoon)',e:'cellen aan de schaduwkant groeien sneller',ef:'de stengel buigt naar het licht',m:'extern',b:'—'},
  ];
  let k=0;
  VB.forEach((v,i)=>{ const b=document.createElement('button'); b.className='btn'; b.textContent=v.n; b.onclick=()=>{ k=i; teken(); }; box.appendChild(b); });
  const ICO={prikkel:'M-14,8 L0,-14 L14,8 Z',receptor:'M-12,-6 a12,12 0 1,0 24,0 a12,12 0 1,0 -24,0 M-4,-6 a4,4 0 1,0 8,0 a4,4 0 1,0 -8,0',verwerking:'M-14,4 C-18,-14 0,-18 2,-10 C10,-18 20,-6 12,4 C14,14 -12,16 -14,4Z',effector:'M-14,6 C-10,-12 10,-12 14,6 C8,10 -8,10 -14,6Z',effect:'M-12,0 L-3,9 L13,-9'};
  function teken(){
    [...box.children].forEach((b,i)=>b.classList.toggle('on',i===k));
    const v=VB[k], st=[['prikkel',v.p,'#dc2626'],['receptor',v.r,'#7c3aed'],['verwerking',v.v,'#2F6FB0'],['effector',v.e,'#059669'],['effect (reactie)',v.ef,'#d97706']];
    let h=`<defs><marker id="sch-p" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="#64748b"/></marker></defs>`;
    st.forEach(([t,inh,kl],i)=>{ const x=20+i*170;
      h+=`<rect x="${x}" y="70" width="150" height="150" rx="14" fill="#fff" stroke="${kl}" stroke-width="3"/><rect x="${x}" y="70" width="150" height="38" rx="14" fill="${kl}"/><rect x="${x}" y="94" width="150" height="14" fill="${kl}"/>`;
      h+=`<text x="${x+75}" y="96" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">${t}</text>`;
      h+=`<g transform="translate(${x+75},134)"><path d="${ICO[t.split(' ')[0]]}" fill="${t==='effect (reactie)'?'none':kl}" fill-opacity=".18" stroke="${kl}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/></g>`;
      const w=inh.split(' '); let r=[''],j=0; w.forEach(x=>{ if((r[j]+' '+x).length>17){ r.push(x); j++; } else r[j]=(r[j]?r[j]+' ':'')+x; });
      r.forEach((l,q)=>h+=`<text x="${x+75}" y="${172+q*18}" text-anchor="middle" font-size="14" fill="#1D2A36">${esc(l)}</text>`);
      if(i<4) h+=`<path d="M${x+152},145 L${x+168},145" stroke="#64748b" stroke-width="3" marker-end="url(#sch-p)"/>`;
    });
    h+=`<path d="M${20+4*170+75},224 V280 H${20+75} V226" fill="none" stroke="#94a3b8" stroke-width="2.5" stroke-dasharray="7 6" marker-end="url(#sch-p)"/><text x="430" y="300" text-anchor="middle" font-size="14" fill="#51606E">bij een feedbacksysteem werkt het effect terug op de prikkel</text>`;
    h+=`<text x="20" y="40" font-size="15" fill="#51606E">prikkel uit het <tspan font-weight="700" fill="#1D2A36">${v.m} milieu</tspan>${v.b!=='—'?' · reactie: <tspan font-weight="700" fill="#1D2A36">'+v.b+'</tspan>':''}</text>`;
    s.innerHTML=h;
    read.innerHTML=`<b>${esc(v.n)}</b><br>Een receptor vangt de prikkel op en zet ze om in een impuls. De verwerking bepaalt de reactie. De effector voert ze uit.`;
  }
  teken();
  // oefening intern/extern
  const IE=[['de temperatuur van de lucht','extern'],['de hoeveelheid suiker in je bloed','intern'],['een harde knal','extern'],['te weinig water in je lichaam','intern'],['licht dat op een plant valt','extern'],['de hoeveelheid CO₂ in je bloed','intern'],['een geur','extern'],['je lichaamstemperatuur','intern'],['de zwaartekracht op een kiemende wortel','extern'],['een volle maag','intern']];
  let goed=0,tot=0,q=null;
  function vraag(){ q=IE[Math.floor(Math.random()*IE.length)];
    $('ie-vraag').innerHTML=`<p class="vraag">Is <b>${q[0]}</b> een prikkel uit het intern of het extern milieu?</p><div class="keuzes"><button class="btn" data-a="intern">intern milieu</button><button class="btn" data-a="extern">extern milieu</button></div><div class="feedback" id="ie-fb"></div>`;
    $('ie-vraag').querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>{ if(b.parentNode.dataset.klaar) return; b.parentNode.dataset.klaar=1; tot++; const ok=b.dataset.a===q[1]; if(ok) goed++; b.classList.add(ok?'goed':'fout');
      $('ie-score').textContent=goed+' / '+tot; $('ie-fb').className='feedback '+(ok?'goed':'fout'); $('ie-fb').innerHTML=(ok?'Juist!':'Niet juist: het is '+q[1]+' milieu.')+'<span class="uitleg">'+(q[1]==='intern'?'Het gaat om een verandering <b>in</b> het lichaam.':'Het gaat om een verandering in de <b>omgeving</b>.')+'</span> <button class="btn" id="ie-nx" style="margin-top:8px">Volgende</button>'; $('ie-nx').onclick=vraag; }); }
  vraag();
})();

//////////////////// FEEDBACK ////////////////////
(function(){
  const s=$('svg-fb'), read=$('fb-read'), kn=$('fb-knoppen'), vbBox=$('fb-vb');
  const VB={
    water:{n:'water in je lichaam',as:'watergehalte van het lichaam (%)',norm:60,L:59.2,U:60.8,min:57.5,max:62.5,d:1,
      st:[['🏃 Je sport en zweet','sport'],['🥤 Je drinkt veel in één keer','drink']],
      eff:{laag:{naam:'dorst → je drinkt',kl:'#2563eb'},hoog:{naam:'genoeg gedronken → je stopt',kl:'#7c3aed'}},
      uitleg:{laag:'Het watergehalte daalt. Receptoren in de hersenen merken dat: je krijgt <b>dorst</b> en je <b>drinkt</b>. Het watergehalte stijgt.',
              hoog:'Het watergehalte is hoog genoeg. Je hersenen geven het signaal dat je <b>genoeg</b> hebt: je stopt met drinken, en de <b>nieren</b> maken meer urine. Het watergehalte daalt weer, tot je opnieuw dorst krijgt.',
              rust:'Je verliest voortdurend wat water (zweet, adem, urine). Het watergehalte daalt langzaam, tot het weer onder de ondergrens komt.'}},
    suiker:{n:'bloedsuikerspiegel',as:'suiker in het bloed (g/l)',norm:1.0,L:0.85,U:1.15,min:0.6,max:1.5,d:2,
      st:[['🍞 Je eet een boterham','eet'],['🏃 Je sport','sport']],
      eff:{laag:{naam:'glucagon en adrenaline',kl:'#d97706'},hoog:{naam:'insuline',kl:'#059669'}},
      uitleg:{laag:'De bloedsuikerspiegel daalt. De alvleesklier maakt <b>glucagon</b> (en de bijnieren <b>adrenaline</b>). Daardoor zet de lever opgeslagen glycogeen om in <b>glucose</b> en geeft die af aan het bloed. De spiegel stijgt.',
              hoog:'De bloedsuikerspiegel stijgt (bv. na het eten). De alvleesklier maakt <b>insuline</b>. Daardoor nemen de cellen glucose op en slaat de lever het op als glycogeen. De spiegel daalt.',
              rust:'Je cellen verbruiken voortdurend glucose. De spiegel daalt langzaam.'}},
    temp:{n:'lichaamstemperatuur',as:'lichaamstemperatuur (°C)',norm:37,L:36.7,U:37.3,min:36.0,max:38.0,d:1,
      st:[['🏃 Je gaat sporten','sport'],['❄ Je gaat de kou in','koud'],['☀ Een warme dag','warm']],
      eff:{laag:{naam:'rillen, bloedvaten vernauwen',kl:'#2563eb'},hoog:{naam:'zweten, bloedvaten verwijden',kl:'#dc2626'}},
      uitleg:{laag:'De temperatuur daalt. Thermoreceptoren sturen een signaal naar de hersenen: je gaat <b>rillen</b> (spieren maken warmte) en de bloedvaten in je huid <b>vernauwen</b> (minder warmteverlies). De temperatuur stijgt.',
              hoog:'De temperatuur stijgt. Je hersenen sturen een signaal: je gaat <b>zweten</b> (verdampend zweet koelt af) en de bloedvaten in je huid <b>verwijden</b> (meer warmte naar buiten). De temperatuur daalt.',
              rust:'Je lichaam maakt voortdurend wat warmte. De temperatuur stijgt of daalt langzaam, afhankelijk van de omgeving.'}},
  };
  let soort='neg', k='water', x, eff=null, sterk={laag:0,hoog:0}, vsn={laag:0,hoog:0}, data=[], vlag=[], t=0, stor={}, pos=0, posData=[], posKlaar='';
  const TW=120;
  Object.entries(VB).forEach(([id,v])=>{ const b=document.createElement('button'); b.className='btn'; b.dataset.id=id; b.textContent=v.n; b.onclick=()=>{ k=id; reset(); }; vbBox.appendChild(b); });
  document.querySelectorAll('[data-fb]').forEach(b=>b.onclick=()=>{ soort=b.dataset.fb; document.querySelectorAll('[data-fb]').forEach(o=>o.classList.toggle('on',o===b)); reset(); });
  function reset(){
    const v=VB[k]; x=v.norm+(v.U-v.norm)*0.6; vx=0; eff=null; sterk={laag:0,hoog:0}; vsn={laag:0,hoog:0}; data=[]; vlag=[]; t=0; stor={}; posData=[]; pos=0; posKlaar='';
    [...vbBox.children].forEach(b=>b.classList.toggle('on',b.dataset.id===k));
    $('fb-vb-g').style.display=soort==='neg'?'':'none';
    if(soort==='neg'){ $('fb-st-l').textContent='Verstoring'; kn.innerHTML=v.st.map(([t2,id])=>`<button class="btn" data-s="${id}">${t2}</button>`).join(''); kn.querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>{ stor[b.dataset.s]=8; }); }
    else { $('fb-st-l').textContent='Start'; kn.innerHTML='<button class="btn primary" id="fb-start">▶ De bevalling begint</button>'; $('fb-start').onclick=()=>{ posData=[]; pos=1; t=0; posKlaar=''; }; }
  }
  // golf rond de normwaarde: herstel naar de norm met vertraging (blijft netjes binnen de grenzen)
  const VERST={sport:{water:-1,suiker:-1,temp:1},drink:{water:1},eet:{suiker:1},koud:{temp:-1},warm:{temp:0.6}};
  let vx=0;
  function stap(dt){
    const v=VB[k], A=(v.U-v.norm)*0.42, w=0.32, y=(x-v.norm)/A;
    let f=-w*w*y - 0.25*(y*y-1)*(vx/A);
    Object.keys(stor).forEach(n=>{ f+=0.9*((VERST[n]||{})[k]||0); });
    const vorigV=vx; vx+=f*A*dt; x+=vx*dt;
    Object.keys(stor).forEach(n=>{ stor[n]-=dt; if(stor[n]<=0) delete stor[n]; });
    // reactie in gang: stijgend → de verhogende reactie, dalend → de verlagende
    const nieuw=Math.abs(x-v.norm)<A*0.15?eff:(vx>0?'laag':'hoog');
    if(vorigV<0&&vx>=0) vlag.push({t,y:x,tekst:v.eff.laag.naam,kl:v.eff.laag.kl});
    if(vorigV>0&&vx<=0) vlag.push({t,y:x,tekst:v.eff.hoog.naam,kl:v.eff.hoog.kl});
    eff=nieuw; data.push([t,x]);
  }
  lus('f2',dt=>{
    let h='';
    const X0=60,Y0=40,GW=730,GH=320;
    if(soort==='neg'){
      const v=VB[k], dts=dt*2.5; t+=dts; stap(dts);
      const tmin=Math.max(0,t-TW); data=data.filter(d=>d[0]>tmin-1); vlag=vlag.filter(f=>f.t>tmin);
      const tx=q=>X0+(q-tmin)/TW*GW, ty=y=>Y0+GH-(y-v.min)/(v.max-v.min)*GH, cl=y=>Math.max(Y0,Math.min(Y0+GH,y));
      h+=`<rect x="${X0}" y="${Y0}" width="${GW}" height="${GH}" fill="#fbfcfe" stroke="#d3dce5"/>`;
      h+=`<rect x="${X0}" y="${ty(v.U)}" width="${GW}" height="${ty(v.L)-ty(v.U)}" fill="#dcfce7" opacity=".7"/>`;
      h+=`<line x1="${X0}" x2="${X0+GW}" y1="${ty(v.U)}" y2="${ty(v.U)}" stroke="#16a34a" stroke-width="1.5" stroke-dasharray="4 4"/><line x1="${X0}" x2="${X0+GW}" y1="${ty(v.L)}" y2="${ty(v.L)}" stroke="#16a34a" stroke-width="1.5" stroke-dasharray="4 4"/>`;
      h+=`<line x1="${X0}" x2="${X0+GW}" y1="${ty(v.norm)}" y2="${ty(v.norm)}" stroke="#059669" stroke-width="2" stroke-dasharray="9 6"/>`;
      const f=n=>n.toLocaleString('nl-BE',{minimumFractionDigits:v.d,maximumFractionDigits:v.d});
      h+=`<g font-size="12.5" font-weight="700" fill="#15803d"><text x="${X0+GW+6}" y="${ty(v.U)+4}">boven</text><text x="${X0+GW+6}" y="${ty(v.norm)+4}">norm</text><text x="${X0+GW+6}" y="${ty(v.L)+4}">onder</text></g><text x="${X0+8}" y="${Y0+GH-10}" font-size="12.5" font-weight="700" fill="#15803d">groene zone: tussen ondergrens ${f(v.L)} en bovengrens ${f(v.U)} · normwaarde ${f(v.norm)}</text>`;
      for(let i=0;i<=4;i++){ const y=v.min+(v.max-v.min)*i/4; h+=`<text x="${X0-8}" y="${ty(y)+4}" text-anchor="end" font-size="12" fill="#51606E">${f(y)}</text>`; }
      // achtergrond tijdens een effectorreactie
      let seg=null; const segs=[]; vlag.concat([{t,einde:1}]).forEach(()=>{});
      h+=`<path d="M${data.map(d=>[tx(d[0]),cl(ty(d[1]))]).join(' L')}" fill="none" stroke="#1D2A36" stroke-width="3"/>`;
      vlag.forEach((fl,i)=>{ const xx=tx(fl.t), yy=cl(ty(fl.y)), toon=i>=vlag.length-2, onder=fl.y<v.norm; const ly=onder?Math.min(Y0+GH-8,yy+38):Math.max(Y0+14,yy-30);
        h+=`<circle cx="${xx}" cy="${yy}" r="5" fill="${fl.kl}"/>`; if(toon) h+=`<path d="M${xx},${yy} L${xx},${ly+(onder?-12:4)}" stroke="${fl.kl}" stroke-width="1.5"/><text x="${Math.min(xx,X0+GW-200)}" y="${ly}" font-size="12.5" font-weight="700" fill="${fl.kl}" stroke="#fff" stroke-width="3" paint-order="stroke">${fl.tekst}</text>`; });
      h+=`<text x="${X0}" y="${Y0-14}" font-size="14" font-weight="700">${v.as}</text><text x="${X0+GW}" y="${Y0+GH+24}" text-anchor="end" font-size="13" fill="#51606E">tijd →</text>`;
      // terugkoppellus
      const e=eff?v.eff[eff]:null, stand=x<v.L?'te laag':x>v.U?'te hoog':'binnen de grenzen';
      h+=`<g transform="translate(${X0},${Y0+GH+44})" font-size="13"><rect width="${GW}" height="40" rx="8" fill="${e?'#fff7ed':'#f1f5f9'}" stroke="${e?e.kl:'#cbd5e1'}"/><text x="14" y="25"><tspan font-weight="700">nu:</tspan> ${stand} · <tspan font-weight="700" fill="${e?e.kl:'#51606E'}">${e?'reactie: '+e.naam:'normwaarde'}</tspan>${Object.keys(stor).length?' · verstoring bezig':''}</text></g>`;
      s.innerHTML=h;
      read.innerHTML=`<b>Negatieve feedback</b> werkt een verandering <b>tegen</b>. Wijkt de waarde af van de normwaarde, dan gaat er een signaal naar de hersenen (of een klier) en volgt een reactie die de waarde terugbrengt. Omdat elke reactie wat tijd nodig heeft, schiet de waarde telkens een beetje door: zo ontstaat een golf rond de normwaarde, binnen de grenzen.<br><span style="color:${e?e.kl:'#51606E'}">${v.uitleg[eff||'rust']}</span>`;
    } else {
      if(pos){ t+=dt; const y=Math.min(100,2*Math.exp(t/2.2)); posData.push([t,y]); if(y>=100){ pos=0; posKlaar='geboorte: de lus stopt'; } }
      const tx=q=>X0+q/12*GW, ty=y=>Y0+GH-y/100*GH;
      h+=`<rect x="${X0}" y="${Y0}" width="${GW}" height="${GH}" fill="#fbfcfe" stroke="#d3dce5"/>`;
      if(posData.length) h+=`<path d="M${posData.map(d=>[tx(d[0]),ty(d[1])]).join(' L')}" fill="none" stroke="#7c3aed" stroke-width="3"/>`;
      h+=`<text x="${X0}" y="${Y0-14}" font-size="14" font-weight="700">sterkte van de weeën en hoeveelheid oxytocine</text><text x="${X0+GW}" y="${Y0+GH+24}" text-anchor="end" font-size="13" fill="#51606E">tijd →</text>`;
      if(posKlaar) h+=`<text x="${X0+12}" y="${Y0+GH+24}" font-size="14" font-weight="700" fill="#7c3aed">${posKlaar}</text>`;
      h+=`<g transform="translate(${X0+30},${Y0+30})" font-size="13" fill="#334155"><text>weeën → druk op de baarmoederhals →</text><text y="20">meer oxytocine → sterkere weeën → …</text></g>`;
      s.innerHTML=h;
      read.innerHTML='<b>Positieve feedback</b> <b>versterkt</b> de verandering. Bij een bevalling duwt de baby tegen de baarmoederhals. Daardoor maakt het lichaam het hormoon oxytocine, dat de weeën sterker maakt. Sterkere weeën duwen nog harder, en zo verder, tot de baby geboren is. Er is geen evenwicht: de lus stopt pas als het doel bereikt is.';
    }
  });
  reset();
  $('fb-kaarten').innerHTML=[
    ['Lichaamstemperatuur','negatief','Te warm → zweten. Te koud → rillen. De temperatuur blijft rond 37 °C.'],
    ['Bloedsuikerspiegel','negatief','Na het eten stijgt de suiker in je bloed. De alvleesklier maakt insuline, waardoor de suiker daalt.'],
    ['Waterhuishouding in je lichaam','negatief','Te weinig water → je nieren houden water vast en je krijgt dorst.'],
    ['Huidmondjes bij watertekort','negatief','Bij watertekort sluiten de huidmondjes. De plant verdampt minder water.'],
    ['Bevalling','positief','Weeën → meer oxytocine → sterkere weeën, tot de baby geboren is.'],
    ['Bloedstolling','positief','Bij een wonde lokken stollingsstoffen nog meer stollingsstoffen uit, tot de wonde dicht is.'],
    ['Rijpen van fruit','positief','Rijpe appels maken het gas etheen. Dat laat ander fruit (en zichzelf) sneller rijpen.'],
  ].map(([t,s,u])=>`<div class="card"><div class="txt"><span class="tag ${s==='positief'?'paars':''}">${s}e feedback</span><h4>${t}</h4><p>${u}</p></div></div>`).join('');
})();

//////////////////// SOORTEN RECEPTOREN ////////////////////
(function(){
  const R=[
    ['fotoreceptoren','licht','staafjes en kegeltjes in het netvlies van het oog','#d97706'],
    ['mechanoreceptoren','druk, aanraking, trilling en geluid','tastlichaampjes in de huid, haarcellen in het oor','#2563eb'],
    ['thermoreceptoren','warmte en koude','vrije zenuwuiteinden in de huid','#dc2626'],
    ['chemoreceptoren','chemische stoffen (geur, smaak)','reukcellen in de neus, smaakpapillen op de tong','#059669'],
    ['pijnreceptoren','beschadiging van weefsel','vrije zenuwuiteinden, bijna overal in het lichaam','#7c3aed'],
  ];
  const ICO={fotoreceptoren:'<circle cx="0" cy="0" r="14" fill="none" stroke="C" stroke-width="3"/><circle r="6" fill="C"/>'+[0,1,2,3,4,5,6,7].map(i=>`<path d="M${Math.cos(i*.785)*19},${Math.sin(i*.785)*19} L${Math.cos(i*.785)*25},${Math.sin(i*.785)*25}" stroke="C" stroke-width="3" stroke-linecap="round"/>`).join(''),
    mechanoreceptoren:'<path d="M-18,10 h36 M-10,10 v-14 a10,10 0 0,1 20,0 v14" fill="none" stroke="C" stroke-width="3"/><path d="M0,-26 v12 M-6,-20 l6,6 l6,-6" fill="none" stroke="C" stroke-width="3"/>',
    thermoreceptoren:'<path d="M-4,-20 a4,4 0 0,1 8,0 v20 a9,9 0 1,1 -8,0z" fill="none" stroke="C" stroke-width="3"/><circle cx="0" cy="8" r="5" fill="C"/>',
    chemoreceptoren:'<path d="M-8,-20 h16 M-5,-20 v12 l-10,22 h30 l-10,-22 v-12" fill="none" stroke="C" stroke-width="3" stroke-linejoin="round"/><circle cx="-2" cy="8" r="3" fill="C"/><circle cx="5" cy="4" r="2.5" fill="C"/>',
    pijnreceptoren:'<path d="M-4,-24 L8,-4 L-2,-2 L6,22 L-10,-2 L0,-4 Z" fill="C" opacity=".85"/>'};
  $('rec-kaarten').innerHTML=R.map(([n,p,w,k])=>`<div class="card"><svg viewBox="-150 -40 300 80"><g transform="translate(0,0)">${ICO[n].replace(/C/g,k)}</g></svg><div class="txt"><h4 style="color:${k}">${n}</h4><p>prikkel: <b>${p}</b><br>voorbeeld: ${w}</p></div></div>`).join('');
  const Q=[['Je ziet een bliksemflits.','fotoreceptoren'],['Iemand tikt op je schouder.','mechanoreceptoren'],['Je ruikt verse koekjes.','chemoreceptoren'],['Je stapt in een koud bad.','thermoreceptoren'],['Je snijdt in je vinger.','pijnreceptoren'],['Je hoort een fluitje.','mechanoreceptoren'],['Je proeft dat de soep zout is.','chemoreceptoren'],['Je voelt de zon warm op je huid.','thermoreceptoren'],['Je voelt dat je trui kriebelt.','mechanoreceptoren'],['Het wordt donker in de klas.','fotoreceptoren']];
  let goed=0,tot=0;
  function vraag(){ const q=Q[Math.floor(Math.random()*Q.length)];
    $('rec-vraag').innerHTML=`<p class="vraag">${q[0]}</p><div class="keuzes">${R.map(r=>`<button class="btn" data-a="${r[0]}">${r[0]}</button>`).join('')}</div><div class="feedback" id="rec-fb"></div>`;
    $('rec-vraag').querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>{ const par=b.parentNode; if(par.dataset.klaar) return; par.dataset.klaar=1; tot++; const ok=b.dataset.a===q[1]; if(ok) goed++; b.classList.add(ok?'goed':'fout'); if(!ok) par.querySelector(`[data-a="${q[1]}"]`).classList.add('goed');
      $('rec-score').textContent=goed+' / '+tot; $('rec-fb').className='feedback '+(ok?'goed':'fout'); $('rec-fb').innerHTML=(ok?'Juist!':'Niet juist.')+` De prikkel wordt opgevangen door <b>${q[1]}</b>. <button class="btn" id="rec-nx">Volgende</button>`; $('rec-nx').onclick=vraag; }); }
  vraag();
})();

//////////////////// DREMPEL EN GEWENNING ////////////////////
(function(){
  const s=$('svg-drempel'), read=$('dr-read'), sl=$('dr-sterkte');
  let modus='drempel', t=-1, lopend=false;
  document.querySelectorAll('[data-dr]').forEach(b=>b.onclick=()=>{ modus=b.dataset.dr; t=-1; document.querySelectorAll('[data-dr]').forEach(x=>x.classList.toggle('on',x===b)); $('dr-sterkte-g').style.display=modus==='drempel'?'':'none'; upd(); });
  $('dr-start').onclick=()=>{ t=0; };
  sl.oninput=()=>{ t=-1; upd(); };
  const DREMPEL=50;
  function upd(){ $('dr-sterkte-l').textContent='Sterkte van de prikkel: '+sl.value;
    if(modus==='drempel') read.innerHTML=+sl.value>=DREMPEL?'De prikkel is <b>sterker dan de prikkeldrempel</b>: de receptor maakt <b>impulsen</b>. Hoe sterker de prikkel, hoe <b>meer impulsen</b> per seconde.':'De prikkel is <b>zwakker dan de prikkeldrempel</b>: er ontstaat <b>geen impuls</b>. Je neemt de prikkel niet waar.<br><span class="k">Voorbeeld: een heel zachte aanraking voel je niet. Een heel stil geluid hoor je niet.</span>';
    else read.innerHTML='De prikkel blijft even sterk, maar de <b>prikkeldrempel stijgt</b> (gewenning). Na een tijd is de prikkel zwakker dan de drempel en neem je ze niet meer waar.<br><span class="k">Voorbeeld: na een paar minuten ruik je de geur in een bakkerij niet meer. Je voelt je horloge niet meer om je pols.</span>'; }
  lus('r2',dt=>{
    if(t>=0) t+=dt*0.5; if(t>1.2) t=1.2;
    const X0=70,Y0=40,GW=740,GH=150,X1=70,Y1=260,GH2=110;
    let h=`<text x="${X0}" y="${Y0-14}" font-size="14" font-weight="700">sterkte van de prikkel</text><rect x="${X0}" y="${Y0}" width="${GW}" height="${GH}" fill="#fbfcfe" stroke="#d3dce5"/>`;
    const st=modus==='drempel'?+sl.value:60;
    const drem=u=>modus==='drempel'?DREMPEL:DREMPEL+Math.min(1,u/0.9)*30;
    const py=v=>Y0+GH-v/100*GH;
    // drempellijn
    let dp=''; for(let i=0;i<=60;i++){ const u=i/60; dp+=(i?' L':'M')+(X0+u*GW)+','+py(drem(u)); }
    h+=`<path d="${dp}" fill="none" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="9 6"/><text x="${X0+GW-6}" y="${py(drem(1))-8}" text-anchor="end" font-size="13" font-weight="700" fill="#dc2626">prikkeldrempel</text>`;
    // prikkel
    const u0=0.1,u1=0.9, vis=t<0?1:Math.min(1,t);
    h+=`<path d="M${X0},${py(0)} L${X0+u0*GW},${py(0)} L${X0+u0*GW},${py(st)} L${X0+Math.min(u1,u0+(u1-u0)*vis/1)*GW},${py(st)} ${vis>=1?`L${X0+u1*GW},${py(0)} L${X0+GW},${py(0)}`:''}" fill="none" stroke="#2563eb" stroke-width="3.5"/>`;
    // impulsen
    h+=`<text x="${X1}" y="${Y1-14}" font-size="14" font-weight="700">impulsen in de zenuw</text><rect x="${X1}" y="${Y1}" width="${GW}" height="${GH2}" fill="#fbfcfe" stroke="#d3dce5"/>`;
    let ip=`M${X1},${Y1+GH2-15}`; const tot=t<0?1:Math.min(1,t);
    let u=u0; while(u<u0+(u1-u0)*tot){ const d=drem(u); if(st>=d){ const f=0.012+0.05*(1-(st-d)/60); const x=X1+u*GW; ip+=` L${x},${Y1+GH2-15} L${x+3},${Y1+12} L${x+7},${Y1+GH2-8} L${x+10},${Y1+GH2-15}`; u+=Math.max(0.012,f); } else u+=0.01; }
    h+=`<path d="${ip} L${X1+GW},${Y1+GH2-15}" fill="none" stroke="#059669" stroke-width="2.5" stroke-linejoin="round"/>`;
    s.innerHTML=h;
  });
  upd();
})();

//////////////////// OOG ////////////////////
const OOGPUNTEN=[
  {naam:'hoornvlies',x:22,y:395,kant:'l',info:'Doorzichtig, bol vlies vooraan. Het licht wordt hier al sterk <b>gebroken</b>.'},
  {naam:'voorste oogkamer (kamervocht)',x:58,y:315,kant:'l',info:'Ruimte met helder vocht tussen hoornvlies en iris. Het kamervocht voedt hoornvlies en lens.'},
  {naam:'regenboogvlies (iris)',x:100,y:280,kant:'l',info:'Gekleurde ring met spiertjes. Ze maakt de <b>pupil</b> groter of kleiner en regelt zo hoeveel licht binnenvalt.'},
  {naam:'pupil',x:113,y:395,kant:'l',ly:430,info:'De opening in de iris. Ze ziet er zwart uit. Bij veel licht wordt ze klein, bij weinig licht groot.'},
  {naam:'lens',x:175,y:385,kant:'l',ly:520,info:'Doorzichtig en vervormbaar. Ze <b>breekt</b> het licht zodat er een scherp beeld op het netvlies valt.'},
  {naam:'straalvormig lichaam',x:138,y:205,kant:'l',ly:175,info:'Bevat de spiertjes die de lens boller of platter maken (accommodatie).'},
  {naam:'lensbandjes',x:160,y:240,kant:'l',ly:225,info:'Dunne vezels die de lens verbinden met het straalvormig lichaam.'},
  {naam:'glasachtig lichaam',x:400,y:250,kant:'r',ly:90,info:'Doorzichtige gelei die het oog zijn bolle vorm geeft.'},
  {naam:'harde oogrok',x:697,y:205,kant:'r',ly:150,info:'Stevige, witte buitenlaag. Ze <b>beschermt</b> het oog. Vooraan gaat ze over in het hoornvlies.'},
  {naam:'vaatvlies',x:667,y:215,kant:'r',ly:205,info:'Laag vol <b>bloedvaten</b> die het oog voeden. De donkere kleur voorkomt weerkaatsing van licht.'},
  {naam:'netvlies',x:650,y:228,kant:'r',ly:260,info:'Binnenste laag met de <b>fotoreceptoren</b> (staafjes en kegeltjes). Ze vangen het licht op.'},
  {naam:'gele vlek',x:683,y:345,kant:'r',info:'Plaats met de <b>meeste kegeltjes</b>. Hier zie je het <b>scherpst</b> en in kleur.'},
  {naam:'blinde vlek',x:648,y:512,kant:'r',ly:470,info:'Plaats waar de oogzenuw het oog verlaat. Hier liggen <b>geen fotoreceptoren</b>: je ziet er niets.'},
  {naam:'oogzenuw',x:800,y:560,kant:'r',ly:560,info:'Brengt de impulsen van het netvlies naar de <b>hersenen</b>.'},
];
labelFig({wrap:'fig-oog',ctl:'ctl-oog',img:IMG.oog,w:900,h:791,ml:400,mr:260,fs:22,r:12,gap:40,punten:OOGPUNTEN,noot:'Tekening: Rhcastilhos en Jmarchn, Wikimedia Commons, publiek domein (zonder Engelse namen, gedraaid).'});

//////////////////// WEG VAN HET LICHT ////////////////////
(function(){
  const wrap=$('fig-lichtweg'), read=$('lw-read'), lijst=$('lw-lijst');
  const ST=[['hoornvlies',22,'Het licht valt eerst door het <b>hoornvlies</b> en wordt gebroken.'],['voorste oogkamer',62,'Dan door het <b>kamervocht</b> in de voorste oogkamer.'],['pupil',113,'Door de <b>pupil</b>, de opening in de iris.'],['lens',176,'De <b>lens</b> breekt het licht nog eens, zodat de stralen samenkomen.'],['glasachtig lichaam',420,'Door het <b>glasachtig lichaam</b> naar achter.'],['netvlies',650,'Op het <b>netvlies</b> ontstaat een scherp, <b>omgekeerd</b> en verkleind beeld. De fotoreceptoren zetten het licht om in impulsen.'],['oogzenuw',800,'De impulsen gaan via de <b>oogzenuw</b> naar de hersenen. Die draaien het beeld weer om.']];
  let stap=0;
  lijst.innerHTML=ST.map((x,i)=>`<li data-i="${i}">${x[0]}</li>`).join('');
  lijst.querySelectorAll('li').forEach(li=>li.onclick=()=>{ stap=+li.dataset.i; t0=performance.now(); });
  $('lw-verder').onclick=()=>{ stap=Math.min(ST.length-1,stap+1); t0=performance.now(); };
  $('lw-terug').onclick=()=>{ stap=Math.max(0,stap-1); t0=performance.now(); };
  let t0=performance.now();
  const ML=260, F=[650,370];
  // stralen vanuit een voorwerp (pijl) links, door het oog naar het netvlies
  const obj=[[-200,300],[-200,470]];
  const ray=(p,yLens)=>[[p[0],p[1]],[22,p[1]+(yLens-p[1])*0.85],[113,yLens],[176,yLens],[650,p===obj[0]?455:300]];
  lus('r4',(dt,now)=>{
    const xmax=Math.min(ST[stap][1],ST[stap][1]>=650?650:ST[stap][1]), anim=Math.min(1,(now-t0)/900);
    let s=`<svg viewBox="${-ML} 0 ${900+ML+40} 791" style="display:block;width:100%;height:auto;font-family:Inter,sans-serif"><image href="${IMG.oog}" width="900" height="791"/>`;
    // voorwerp: kaars
    s+=`<rect x="-212" y="380" width="24" height="90" rx="4" fill="#f4e7c6" stroke="#b08b4a" stroke-width="2"/><path d="M-200,380 q-10,-22 0,-40 q10,18 0,40z" fill="#f59e0b"/><text x="-200" y="500" text-anchor="middle" font-size="18" font-weight="700" fill="#1D2A36">voorwerp</text>`;
    const top=[-200,345], bot=[-200,470];
    const paden=[[top,[22,365],[113,375],[176,378],[650,445]],[top,[22,350],[113,350],[176,355],[650,445]],[bot,[22,420],[113,412],[176,410],[650,300]],[bot,[22,438],[113,438],[176,432],[650,300]]];
    const grens=xmax+(stap>0?0:0);
    paden.forEach(p=>{ let d=`M${p[0]}`; for(let i=1;i<p.length;i++){ const [x0,y0]=p[i-1],[x1,y1]=p[i]; if(x0>=grens) break; if(x1<=grens) d+=` L${x1},${y1}`; else { const u=(grens-x0)/(x1-x0); d+=` L${x0+(x1-x0)*u},${y0+(y1-y0)*u}`; break; } } s+=`<path d="${d}" fill="none" stroke="#f59e0b" stroke-width="3.5" opacity=".9"/>`; });
    if(stap>=5){ s+=`<g opacity="${anim}"><path d="M650,445 L650,300" stroke="#b45309" stroke-width="4"/><path d="M650,445 l-9,-14 l18,0z" fill="#b45309"/><text x="590" y="380" text-anchor="end" font-size="17" font-weight="700" fill="#7c2d12" stroke="#fff" stroke-width="4" paint-order="stroke">omgekeerd beeld</text></g>`; }
    if(stap>=6){ for(let i=0;i<4;i++){ const u=((now/1000)*0.7+i/4)%1; s+=`<circle cx="${650+u*180}" cy="${512+u*70}" r="6" fill="#7c3aed" opacity="${1-u*0.5}"/>`; } s+=`<text x="860" y="660" text-anchor="end" font-size="17" font-weight="700" fill="#7c3aed" stroke="#fff" stroke-width="4" paint-order="stroke">impulsen naar de hersenen</text>`; }
    const p=OOGPUNTEN.find(q=>q.naam.startsWith(ST[stap][0].split(' ')[0]));
    if(p) s+=`<circle cx="${p.x}" cy="${p.y}" r="${16+3*Math.sin(now/200)}" fill="none" stroke="#d97706" stroke-width="4"/>`;
    s+='</svg>';
    wrap.innerHTML=s;
    read.innerHTML=`<b>Stap ${stap+1}: ${ST[stap][0]}</b><br>${ST[stap][2]}`;
    lijst.querySelectorAll('li').forEach((li,i)=>{ li.classList.toggle('on',i===stap); li.classList.toggle('gedaan',i<stap); });
  });
})();

//////////////////// NETVLIES ////////////////////
const NETVLIES=(function(){
  // licht komt van boven. Lagen: zenuwvezels, ganglioncellen, bipolaire cellen, staafjes en kegeltjes, pigmentcellen, vaatvlies.
  // Alle cellen zijn vloeiende vormen; uitlopers eindigen precies op de cel waar ze op aansluiten.
  const W=900,H=640;
  const rng=seed=>{let s=seed>>>0||1;return()=>{s^=s<<13;s^=s>>>17;s^=s<<5;return((s>>>0)%100000)/100000;};};
  const glad=(p,dicht=true)=>{const n=p.length,P=i=>dicht?p[(i+n)%n]:p[Math.max(0,Math.min(n-1,i))];let d=`M${p[0][0].toFixed(1)} ${p[0][1].toFixed(1)}`;const m=dicht?n:n-1;
    for(let i=0;i<m;i++){const a=P(i-1),b=P(i),c=P(i+1),e=P(i+2);d+=`C${(b[0]+(c[0]-a[0])/6).toFixed(1)} ${(b[1]+(c[1]-a[1])/6).toFixed(1)} ${(c[0]-(e[0]-b[0])/6).toFixed(1)} ${(c[1]-(e[1]-b[1])/6).toFixed(1)} ${c[0].toFixed(1)} ${c[1].toFixed(1)}`;}return d+(dicht?'Z':'');};
  const blob=(cx,cy,rx,ry,R,n=10,j=.12,rot=0)=>{const p=[];for(let i=0;i<n;i++){const a=rot+i/n*Math.PI*2,f=1+(R()-.5)*2*j;p.push([cx+Math.cos(a)*rx*f,cy+Math.sin(a)*ry*f]);}return glad(p);};
  const lijn=(pts,n=24)=>{const r=[];for(let k=0;k<pts.length-1;k++){for(let i=0;i<n;i++){const t=i/n;r.push([pts[k][0]+(pts[k+1][0]-pts[k][0])*t,pts[k][1]+(pts[k+1][1]-pts[k][1])*t]);}}r.push(pts[pts.length-1]);return r;};
  const zacht=(pts)=>{ // Catmull-Rom bemonsterd
    const r=[];const n=pts.length;const P=i=>pts[Math.max(0,Math.min(n-1,i))];
    for(let i=0;i<n-1;i++){const a=P(i-1),b=P(i),c=P(i+1),e=P(i+2);for(let k=0;k<12;k++){const t=k/12,t2=t*t,t3=t2*t;
      r.push([0,1].map(q=>.5*((2*b[q])+(-a[q]+c[q])*t+(2*a[q]-5*b[q]+4*c[q]-e[q])*t2+(-a[q]+3*b[q]-3*c[q]+e[q])*t3)));}}r.push(pts[n-1]);return r;};
  const buis=(pts,w0,w1,rond=true)=>{const P=pts.length>8?pts:zacht(pts);const n=P.length,L=[],Rr=[];
    for(let i=0;i<n;i++){const a=P[Math.max(0,i-1)],b=P[Math.min(n-1,i+1)];const g=Math.atan2(b[1]-a[1],b[0]-a[0]);const w=(w0+(w1-w0)*i/(n-1))/2;L.push([P[i][0]-Math.sin(g)*w,P[i][1]+Math.cos(g)*w]);Rr.push([P[i][0]+Math.sin(g)*w,P[i][1]-Math.cos(g)*w]);}
    const e=P[n-1],pe=P[n-2],ea=Math.atan2(e[1]-pe[1],e[0]-pe[0]),k=[];if(rond)for(let q=1;q<6;q++){const a=ea-Math.PI/2+q/6*Math.PI;k.push([e[0]+Math.cos(a)*w1/2,e[1]+Math.sin(a)*w1/2]);}
    return'M'+[...L,...k.reverse(),...Rr.reverse()].map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' L')+'Z';};
  const R=rng(7);
  let s=`<defs>
    <filter id="nv-3d" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">
      <feMorphology in="SourceAlpha" operator="dilate" radius="1.2" result="dik"/><feFlood flood-color="#2a1d2c" flood-opacity=".7"/><feComposite in2="dik" operator="in" result="rand"/>
      <feGaussianBlur in="SourceAlpha" stdDeviation="2.4" result="bl"/>
      <feSpecularLighting in="bl" surfaceScale="5" specularConstant=".7" specularExponent="16" lighting-color="#fff" result="spec"><fePointLight x="-400" y="-600" z="500"/></feSpecularLighting>
      <feComposite in="spec" in2="SourceAlpha" operator="in" result="glans"/>
      <feDiffuseLighting in="bl" surfaceScale="4" diffuseConstant="1" lighting-color="#fff" result="dif"><feDistantLight azimuth="235" elevation="55"/></feDiffuseLighting>
      <feComposite in="SourceGraphic" in2="dif" operator="arithmetic" k1="1" result="sch"/><feComposite in="sch" in2="SourceGraphic" operator="arithmetic" k2=".55" k3=".55" result="mix"/>
      <feComposite in="glans" in2="mix" operator="arithmetic" k2=".5" k3="1" result="licht"/><feComposite in="licht" in2="SourceAlpha" operator="in" result="vorm"/>
      <feMerge><feMergeNode in="rand"/><feMergeNode in="vorm"/></feMerge></filter>
    <radialGradient id="nv-kern" cx="38%" cy="35%" r="70%"><stop offset="0" stop-color="#9b78c2"/><stop offset=".6" stop-color="#6a4596"/><stop offset="1" stop-color="#4b2b73"/></radialGradient>
    <linearGradient id="nv-pig" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b4a2f"/><stop offset="1" stop-color="#3c2616"/></linearGradient>
    <radialGradient id="nv-rbc" cx="50%" cy="50%" r="55%"><stop offset="0" stop-color="#e46a6a"/><stop offset=".5" stop-color="#cf3b3b"/><stop offset="1" stop-color="#8f1d1d"/></radialGradient></defs>`;
  s+=`<rect width="${W}" height="${H}" fill="#fdf6f0"/><rect y="0" width="${W}" height="72" fill="#f4ece6"/>`;
  // vaatvlies met bloedvaten
  s+=`<path d="M0 566 C200 556 400 572 600 562 S800 556 900 566 V640 H0Z" fill="#9b3a43"/>`;
  [[0,596,900,600],[0,620,900,616]].forEach(([x0,y0,x1,y1],i)=>{const pts=zacht([[x0,y0],[220,y0+(i?6:-8)],[460,y0+(i?-6:8)],[700,y0+(i?6:-6)],[x1,y1]]);s+=`<path d="${buis(pts,22,22,false)}" fill="${i?'#5a3f8f':'#c9434d'}" opacity=".9"/>`;
    for(let k=0;k<12;k++){const p=pts[Math.floor((k+.5)/12*(pts.length-1))];s+=`<g transform="translate(${p[0].toFixed(0)} ${p[1].toFixed(0)}) rotate(${(R()*60-30).toFixed(0)})"><ellipse rx="7" ry="5" fill="url(#nv-rbc)"/><ellipse rx="3" ry="2" fill="#e98181" opacity=".7"/></g>`;}});
  // pigmentcellen: vloeiende cellen met uitlopers tussen de buitensegmenten
  let pig='';for(let i=0;i<15;i++){const x=i*62+31;pig+=`<path d="${glad([[x-31,564],[x-31,520],[x-20,504],[x,500],[x+20,504],[x+31,520],[x+31,564]])}"/>`;
    for(let k=0;k<5;k++){const px=x-22+k*11;pig+=`<path d="${buis([[px,508],[px+1,496],[px,480]],5,2.5)}"/>`;}}
  s+=`<g filter="url(#nv-3d)" fill="#6b4a2f">${pig}</g>`;
  for(let i=0;i<15;i++){const x=i*62+31;s+=`<path d="${blob(x,538,9,7,R,8,.1)}" fill="#a3825e"/>`;for(let k=0;k<14;k++)s+=`<circle cx="${(x-26+R()*52).toFixed(1)}" cy="${(512+R()*46).toFixed(1)}" r="1.4" fill="#2a190c" opacity=".7"/>`;}
  // fotoreceptoren
  const recs=[];for(let i=0;i<34;i++){const x=14+i*26.4;recs.push({x,k:(i%4===2),t:[x,302]});}
  let staaf='',kegel=['','',''],schijf='',kn=0;
  recs.forEach(r=>{const x=r.x;
    if(!r.k){ staaf+=`<path d="${buis([[x,298],[x,312],[x+1,326]],5,3.2,false)}"/><path d="${blob(x,302,5.5,5,R,8,.1)}"/><path d="${blob(x,336,6.5,10,R,9,.08)}"/>`+
        `<path d="${buis([[x+1,344],[x,372],[x,398]],5,9,false)}"/><path d="${buis([[x,396],[x,450],[x,496]],10,10)}"/>`;
      for(let y=404;y<492;y+=6)schijf+=`<path d="M${x-4} ${y} H${x+4}" stroke="#6b6f85" stroke-width="1" opacity=".55"/>`; }
    else { const c=kn++%3; kegel[c]+=`<path d="${buis([[x,298],[x,312],[x+1,326]],6,3.6,false)}"/><path d="${blob(x,302,6.5,5.5,R,8,.1)}"/><path d="${blob(x,340,8,11,R,9,.08)}"/>`+
        `<path d="${buis([[x,350],[x,392],[x,432]],7,19,false)}"/><path d="${buis([[x,430],[x,462],[x,490]],19,4)}"/>`;
      for(let y=438;y<486;y+=6){const w=9-(y-430)/60*7.5;schijf+=`<path d="M${(x-w).toFixed(1)} ${y} H${(x+w).toFixed(1)}" stroke="#ffffff" stroke-width="1" opacity=".45"/>`;} } });
  s+=`<g filter="url(#nv-3d)" fill="#b9bccb">${staaf}</g>`+['#e5484d','#3fae49','#3b6fd8'].map((k,i)=>`<g filter="url(#nv-3d)" fill="${k}">${kegel[i]}</g>`).join('')+schijf;
  recs.forEach(r=>{s+=`<path d="${blob(r.x,r.k?340:336,r.k?4.2:3.4,r.k?5.6:5,R,8,.08)}" fill="url(#nv-kern)"/>`;});
  // bipolaire cellen: dendrieten eindigen op de eindknopjes van de fotoreceptoren, axon omhoog
  const bip=[];let bv='';for(let j=0;j<12;j++){const xb=40+j*74;bip.push(xb);
    recs.filter(r=>Math.abs(r.x-xb)<38).forEach(r=>{bv+=`<path d="${buis([[xb,262],[xb+(r.x-xb)*.4,276],[r.x,288],[r.x,296]],6,2.6)}"/>`;});
    bv+=`<path d="${blob(xb,248,12,17,R,10,.08)}"/><path d="${buis([[xb,236],[xb+1,214],[xb,198]],6,3.4)}"/><path d="${blob(xb,196,6,5.5,R,8,.1)}"/>`;}
  s+=`<g filter="url(#nv-3d)" fill="#f2a65a">${bv}</g>`;bip.forEach(xb=>s+=`<path d="${blob(xb,248,5.5,7,R,8,.08)}" fill="url(#nv-kern)"/>`);
  // ganglioncellen: dendrieten eindigen op de axonuiteinden van de bipolaire cellen, axon naar de oogzenuw
  let gv='';const gang=[];for(let k=0;k<7;k++){const xg=70+k*128;gang.push(xg);
    bip.filter(xb=>Math.abs(xb-xg)<=64).forEach(xb=>{gv+=`<path d="${buis([[xg,160],[xg+(xb-xg)*.5,176],[xb,188],[xb,193]],7,3)}"/>`;});
    gv+=`<path d="${blob(xg,140,24,22,R,11,.1)}"/><path d="${buis([[xg,118],[xg+8,90],[xg+50,66],[xg+120,52],[W+20,38+k*4]],6.5,5,false)}"/>`;}
  s+=`<g filter="url(#nv-3d)" fill="#b48ddb">${gv}</g>`;gang.forEach(xg=>s+=`<path d="${blob(xg+2,138,9,8,R,9,.08)}" fill="url(#nv-kern)"/><circle cx="${xg+4}" cy="136" r="2.4" fill="#2a1240"/>`);
  // lichtpijlen
  for(let i=0;i<5;i++){const x=120+i*170;s+=`<path d="M${x},-30 L${x},20" stroke="#f59e0b" stroke-width="5"/><path d="M${x-10},12 l10,16 l10,-16z" fill="#f59e0b"/>`;}
  s+=`<text x="${W-10}" y="22" text-anchor="end" font-size="18" font-weight="700" fill="#b45309">licht ↓</text>`;
  return {svg:s,W,H,recs};
})();
(function(){
  const r=NETVLIES.recs, st=r.find(x=>!x.k&&x.x>500), ke=r.find(x=>x.k&&x.x>300);
  labelFig({wrap:'fig-netvlies',ctl:'ctl-netvlies',inner:NETVLIES.svg,w:900,h:640,ml:250,mr:250,top:40,fs:22,r:12,gap:40,
    punten:[
      {naam:'zenuwcellen',x:198,y:140,kant:'l',ly:140,info:'Twee lagen zenuwcellen. Ze verwerken de impulsen van de fotoreceptoren en sturen ze via de <b>oogzenuw</b> naar de hersenen. Het licht gaat eerst <b>door</b> deze laag.'},
      {naam:'oogzenuwvezels',x:820,y:46,kant:'r',ly:46,info:'De uitlopers van de zenuwcellen komen samen in de <b>oogzenuw</b>.'},
      {naam:'staafje',x:st.x,y:450,kant:'r',ly:420,info:'Fotoreceptor met een <b>staafvormig</b> buitensegment. Heel gevoelig: werkt ook bij <b>weinig licht</b>, maar ziet <b>geen kleuren</b>.'},
      {naam:'kegeltje',x:ke.x,y:455,kant:'l',ly:430,info:'Fotoreceptor met een <b>kegelvormig</b> buitensegment. Werkt bij <b>veel licht</b> en ziet <b>kleuren</b>. Er zijn drie soorten: rood, groen en blauw.'},
      {naam:'pigmentcellen',x:150,y:530,kant:'l',ly:540,info:'Donkere cellen achteraan. Ze <b>slorpen het licht op</b> dat door de fotoreceptoren is gegaan, zodat het niet weerkaatst.'},
      {naam:'vaatvlies',x:700,y:600,kant:'r',ly:600,info:'Laag met bloedvaten achter het netvlies.'},
    ],noot:'Het licht komt van boven, door de zenuwcellen heen, tot bij de staafjes en kegeltjes.'});
  // vergelijking
  const RIJ=[['vorm','staafvormig','kegelvormig'],['aantal','± 120 miljoen','± 6 miljoen'],['plaats','vooral aan de rand van het netvlies','vooral in de gele vlek'],['werkt bij','weinig licht (schemer, nacht)','veel licht (overdag)'],['kleuren zien','nee: alleen grijstinten','ja: rood, groen en blauw'],['scherpte','weinig scherp','scherp']];
  $('sk-tabel').innerHTML='<tr><th></th><th>staafjes</th><th>kegeltjes</th></tr>'+RIJ.map(r=>`<tr><th>${r[0]}</th><td>${r[1]}</td><td>${r[2]}</td></tr>`).join('');
  $('sk-tabel').style.display='none';
  const Q=[['Ik zie ’s nachts nog vormen, maar geen kleuren.','staafjes'],['Ik zit vooral in de gele vlek.','kegeltjes'],['Er zijn er ongeveer 120 miljoen van.','staafjes'],['Ik zorg dat je een rode appel ziet.','kegeltjes'],['Ik werk al bij heel weinig licht.','staafjes'],['Ik heb een kegelvormig buitensegment.','kegeltjes'],['Ik lig vooral aan de rand van het netvlies.','staafjes'],['Met mij zie je scherp.','kegeltjes']];
  let goed=0,tot=0;
  function vraag(){ const q=Q[Math.floor(Math.random()*Q.length)];
    $('sk-vraag').innerHTML=`<p class="vraag">${q[0]}</p><div class="keuzes"><button class="btn" data-a="staafjes">staafjes</button><button class="btn" data-a="kegeltjes">kegeltjes</button><button class="btn" id="sk-tab">tabel tonen</button></div><div class="feedback" id="sk-fb"></div>`;
    $('sk-tab').onclick=()=>{ const t=$('sk-tabel'); t.style.display=t.style.display==='none'?'':'none'; };
    $('sk-vraag').querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>{ const par=b.parentNode; if(par.dataset.klaar) return; par.dataset.klaar=1; tot++; const ok=b.dataset.a===q[1]; if(ok) goed++; b.classList.add(ok?'goed':'fout');
      $('sk-score').textContent=goed+' / '+tot; $('sk-fb').className='feedback '+(ok?'goed':'fout'); $('sk-fb').innerHTML=(ok?'Juist!':'Niet juist: dat zijn de '+q[1]+'.')+' <button class="btn" id="sk-nx">Volgende</button>'; $('sk-nx').onclick=vraag; }); }
  vraag();
})();

//////////////////// KLEUREN ////////////////////
(function(){
  const s=$('svg-kleur'), read=$('k-read'); let donker=false;
  ['r','g','b'].forEach(c=>$('k-'+c).oninput=teken);
  $('k-donker').onclick=()=>{ donker=!donker; $('k-donker').classList.toggle('on',donker); $('k-donker').textContent=donker?'☀ Weer licht':'☾ In het donker'; teken(); };
  function teken(){
    const r=+$('k-r').value, g=+$('k-g').value, b=+$('k-b').value;
    ['r','g','b'].forEach((c,i)=>$('k-'+c+'-l').textContent=['Rode','Groene','Blauwe'][i]+' kegeltjes: '+$('k-'+c).value+' %');
    let kl=`rgb(${r*2.55|0},${g*2.55|0},${b*2.55|0})`;
    if(donker){ const gr=Math.min(255,(r+g+b)/3*1.2|0); kl=`rgb(${gr},${gr},${gr})`; }
    let h=`<rect width="860" height="400" fill="#f8fafc"/>`;
    const kg=[['rood','#dc2626',r],['groen','#16a34a',g],['blauw','#2563eb',b]];
    kg.forEach(([n,k,v],i)=>{ const x=90, y=60+i*110;
      h+=`<path d="M${x-26},${y} L${x+26},${y} L${x+6},${y+70} L${x-6},${y+70}Z" fill="${k}" opacity="${donker?0.15:0.25+0.75*v/100}" stroke="${k}" stroke-width="2"/>`;
      h+=`<text x="${x+40}" y="${y+28}" font-size="16" font-weight="700" fill="${k}">${n}</text><rect x="${x+40}" y="${y+40}" width="200" height="12" rx="6" fill="#e2e8f0"/><rect x="${x+40}" y="${y+40}" width="${donker?0:2*v}" height="12" rx="6" fill="${k}"/>`;
      h+=`<path d="M${x+250},${y+46} C${x+330},${y+46} ${x+340},200 ${x+400},200" fill="none" stroke="${k}" stroke-width="${donker?1:1+5*v/100}" opacity="${donker?0.2:1}"/>`;
    });
    h+=`<path d="M560,140 C540,140 520,170 525,200 C520,240 560,270 600,260 C640,280 700,270 710,230 C740,210 730,150 690,140 C670,110 590,110 560,140Z" fill="#f4c9c9" stroke="#b05c5c" stroke-width="2.5"/><text x="618" y="300" text-anchor="middle" font-size="15" font-weight="700" fill="#1D2A36">hersenen</text>`;
    h+=`<circle cx="790" cy="200" r="52" fill="${kl}" stroke="#334155" stroke-width="3"/><text x="790" y="285" text-anchor="middle" font-size="15" font-weight="700" fill="#1D2A36">je ziet</text>`;
    s.innerHTML=h;
    read.innerHTML=donker?'In het donker werken de kegeltjes niet. Alleen de <b>staafjes</b> werken: je ziet <b>grijstinten</b>.':'De hersenen combineren de impulsen van de drie soorten kegeltjes tot één kleur. Rood + groen geeft geel. Alle drie even sterk geeft wit.';
  }
  teken();
})();

//////////////////// ILLUSIES ////////////////////
(function(){
  const s=$('svg-illusie'), read=$('il-read'), box=$('il-keuze');
  let k=0, toon=false;
  const IL=[
    {n:'Müller-Lyer',u:'De twee horizontale lijnen zijn <b>even lang</b>. De pijlpunten doen je hersenen denken aan hoeken van een gebouw die dichterbij of verder weg zijn.',
     f:t=>{ let h=''; const L=320,x=270; [[110,1],[300,-1]].forEach(([y,d])=>{ h+=`<line x1="${x}" x2="${x+L}" y1="${y}" y2="${y}" stroke="#1D2A36" stroke-width="6"/>`; [x,x+L].forEach((xx,j)=>{ const s2=(j?1:-1)*d; h+=`<path d="M${xx+s2*-38},${y-38} L${xx},${y} L${xx+s2*-38},${y+38}" fill="none" stroke="#1D2A36" stroke-width="6"/>`; }); });
       if(t) h+=`<line x1="${x}" x2="${x}" y1="50" y2="360" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="8 6"/><line x1="${x+L}" x2="${x+L}" y1="50" y2="360" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="8 6"/>`; return h; }},
    {n:'Ebbinghaus',u:'De twee oranje cirkels zijn <b>even groot</b>. Omringd door grote cirkels lijkt een cirkel kleiner, omringd door kleine cirkels lijkt hij groter.',
     f:t=>{ let h=''; const c1=[230,220],c2=[630,220];
       for(let i=0;i<6;i++){ const a=i*Math.PI/3; h+=`<circle cx="${c1[0]+Math.cos(a)*120}" cy="${c1[1]+Math.sin(a)*120}" r="52" fill="#94a3b8"/>`; }
       for(let i=0;i<8;i++){ const a=i*Math.PI/4; h+=`<circle cx="${c2[0]+Math.cos(a)*62}" cy="${c2[1]+Math.sin(a)*62}" r="16" fill="#94a3b8"/>`; }
       h+=`<circle cx="${c1[0]}" cy="${c1[1]}" r="36" fill="#f97316"/><circle cx="${c2[0]}" cy="${c2[1]}" r="36" fill="#f97316"/>`;
       if(t) h+=`<line x1="194" x2="666" y1="${220-36}" y2="${220-36}" stroke="#dc2626" stroke-width="2" stroke-dasharray="7 5"/><line x1="194" x2="666" y1="${220+36}" y2="${220+36}" stroke="#dc2626" stroke-width="2" stroke-dasharray="7 5"/>`; return h; }},
    {n:'Kanizsa-driehoek',u:'Er is <b>geen witte driehoek</b> getekend. Je hersenen vullen de ontbrekende randen zelf in, omdat ze vormen willen herkennen.',
     f:t=>{ let h=''; const P=[[430,70],[250,360],[610,360]], c=[430,263];
       P.forEach(p=>{ const a=Math.atan2(c[1]-p[1],c[0]-p[0]); const a1=a-Math.PI/6, a2=a+Math.PI/6; h+=`<path d="M${p[0]},${p[1]} L${p[0]+Math.cos(a2)*55},${p[1]+Math.sin(a2)*55} A55,55 0 1,1 ${p[0]+Math.cos(a1)*55},${p[1]+Math.sin(a1)*55}Z" fill="#1D2A36"/>`; });
       const Q=[[430,380],[250,90],[610,90]]; Q.forEach((p,i)=>{ const q=Q[(i+1)%3]; const m1=[p[0]+(q[0]-p[0])*0.3,p[1]+(q[1]-p[1])*0.3], m2=[p[0]+(q[0]-p[0])*0.7,p[1]+(q[1]-p[1])*0.7]; h+=`<path d="M${p} L${m1} M${m2} L${q}" stroke="#1D2A36" stroke-width="4"/>`; });
       if(t) h+=`<path d="M${P[0]} L${P[1]} L${P[2]}Z" fill="none" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="8 6"/>`; return h; }},
    {n:'Schaakbord van Adelson',u:'Vak A en vak B hebben <b>dezelfde grijstint</b>. Je hersenen houden rekening met de schaduw van de cilinder en ‘corrigeren’ de kleur.',
     f:t=>{ let h=''; const n=5,sz=58,x0=280,y0=60; const kl=(i,j)=>{ const licht=(i+j)%2===0; const sch=Math.max(0,1-Math.hypot(i-3.2,j-3.4)/2.6); const base=licht?205:120; return Math.round(base*(1-0.42*sch)); };
       for(let i=0;i<n;i++) for(let j=0;j<n;j++){ let g=kl(i,j); if(i===1&&j===1) g=120; if(i===3&&j===3) g=120; h+=`<rect x="${x0+i*sz}" y="${y0+j*sz}" width="${sz}" height="${sz}" fill="rgb(${g},${g},${g})"/>`; }
       h+=`<ellipse cx="${x0+4.1*sz}" cy="${y0+3.9*sz}" rx="44" ry="18" fill="rgba(0,0,0,.25)"/><rect x="${x0+3.75*sz}" y="${y0+1.6*sz}" width="44" height="${2.3*sz}" fill="#4ade80"/><ellipse cx="${x0+3.75*sz+22}" cy="${y0+1.6*sz}" rx="22" ry="8" fill="#86efac"/><ellipse cx="${x0+3.75*sz+22}" cy="${y0+3.9*sz}" rx="22" ry="8" fill="#22c55e"/>`;
       h+=`<text x="${x0+1.5*sz}" y="${y0+1.5*sz+8}" text-anchor="middle" font-size="22" font-weight="700" fill="#fff">A</text><text x="${x0+3.5*sz}" y="${y0+3.5*sz+8}" text-anchor="middle" font-size="22" font-weight="700" fill="#fff">B</text>`;
       if(t) h+=`<rect x="${x0+1.5*sz-14}" y="${y0+1.5*sz+18}" width="28" height="${2*sz}" fill="rgb(120,120,120)"/><rect x="${x0+1.5*sz-14}" y="${y0+3.5*sz+10}" width="${2*sz}" height="20" fill="rgb(120,120,120)"/>`; return h; }},
  ];
  IL.forEach((x,i)=>{ const b=document.createElement('button'); b.className='btn'; b.textContent=x.n; b.onclick=()=>{ k=i; toon=false; teken(); }; box.appendChild(b); });
  $('il-toon').onclick=()=>{ toon=!toon; teken(); };
  function teken(){ [...box.children].forEach((b,i)=>b.classList.toggle('on',i===k)); s.innerHTML=`<rect width="860" height="440" fill="#fff"/>`+IL[k].f(toon); $('il-toon').textContent=toon?'Verberg':'Toon hoe het echt is'; read.innerHTML=toon?IL[k].u:'Wat zie je? Kijk goed en denk eerst na. Klik daarna op <b>Toon hoe het echt is</b>.'; }
  teken();
})();

//////////////////// RECEPTOREN BIJ ANDERE ORGANISMEN ////////////////////
$('org-kaarten').innerHTML=[
  ['dier','Slang','Groefkopslangen hebben <b>warmtegevoelige putjes</b> tussen oog en neusgat. Ze zien zo de lichaamswarmte van een muis, ook in het donker.'],
  ['dier','Vleermuis','Een vleermuis stoot hoge geluiden uit en vangt de <b>echo</b> op met haar oren (echolocatie). Zo vindt ze insecten in het donker.'],
  ['dier','Haai','Haaien hebben receptoren die <b>zwakke elektrische velden</b> opvangen van de spieren van prooidieren.'],
  ['dier','Bij','Bijen zien <b>ultraviolet licht</b>. Veel bloemen hebben uv-patronen die de weg naar de nectar tonen.'],
  ['dier','Kat','De snorharen van een kat zijn verbonden met <b>mechanoreceptoren</b>. Ze voelt zo luchtstroompjes en de breedte van een opening.'],
  ['plant','Zonnebloem','De stengeltop vangt <b>licht</b> op. De stengel groeit naar het licht toe (fototropie).'],
  ['plant','Kruidje-roer-mij-niet','De blaadjes vouwen dicht als je ze <b>aanraakt</b>. Zo beschermt de plant zich.'],
  ['plant','Venusvliegenval','Gevoelige haartjes in de val reageren op <b>aanraking</b>. Raakt een insect twee keer een haartje, dan klapt de val dicht.'],
  ['plant','Kiemende boon','De wortel groeit naar beneden, de stengel naar boven. De plant voelt de <b>zwaartekracht</b> (geotropie).'],
].map(([s,t,u])=>`<div class="card"><div class="txt"><span class="tag ${s==='plant'?'groen':''}">${s}</span><h4>${t}</h4><p>${u}</p></div></div>`).join('');
