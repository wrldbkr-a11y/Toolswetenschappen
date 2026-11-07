from bouw import pagina, HIER
MOL = (HIER/'mol.js').read_text()
body = r'''
  <main class="les" id="lesA" role="tabpanel">
    <section class="blok">
      <div class="blok-kop"><span class="letter">A</span><h2>Enkelvoudige en samengestelde stoffen</h2></div>
      <p>Een zuivere stof bestaat uit één soort deeltjes. Kijk naar de <b>atomen</b> in één deeltje.</p>
      <div class="duo">
        <div class="def"><span class="eyebrow">Definitie</span><p>Een <b>enkelvoudige stof</b> bestaat uit deeltjes met <b>één soort atomen</b>.</p></div>
        <div class="def"><span class="eyebrow">Definitie</span><p>Een <b>samengestelde stof</b> bestaat uit deeltjes met <b>twee of meer soorten atomen</b>.</p></div>
      </div>
      <p>Kies een stof en bekijk het deeltjesmodel.</p>
      <div class="knoppen" id="dm-knoppen"></div>
      <div class="duo"><div class="fig" id="dm-fig"></div><div class="kaart" id="dm-uitleg"></div></div>
      <div class="tip"><b>Atoomsoorten in de tekening</b><p id="dm-legende"></p></div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">A</span><h2>Analyse en synthese</h2></div>
      <div class="duo">
        <div class="def"><span class="eyebrow">Definitie</span><p>Bij een <b>analyse</b> ontleed je een samengestelde stof in eenvoudigere stoffen.</p></div>
        <div class="def"><span class="eyebrow">Definitie</span><p>Bij een <b>synthese</b> maak je een samengestelde stof uit eenvoudigere stoffen.</p></div>
      </div>
      <div class="knoppen"><button class="knop" type="button" id="as-a" aria-pressed="true">analyse: elektrolyse van water</button><button class="knop" type="button" id="as-s" aria-pressed="false">synthese van water</button></div>
      <div class="fig"><svg id="as-svg" viewBox="0 0 640 230"></svg></div>
      <p id="as-zin"></p>
      <div class="tip"><b>Nog een analyse</b><p>Verwarm je suiker sterk, dan ontleedt het in <b>koolstof</b> (zwart) en <b>water</b> (damp). Dat is een <b>thermolyse</b>: een analyse door warmte. Suiker is dus een samengestelde stof.</p></div>
    </section>
  </main>

  <main class="les" id="lesB" role="tabpanel" hidden>
    <section class="blok">
      <div class="blok-kop"><span class="letter">B</span><h2>Een formule lezen</h2></div>
      <p>Een <b>formule</b> zegt welke atomen in één deeltje zitten en hoeveel.</p>
      <div class="fig"><svg viewBox="0 0 560 170" role="img" aria-label="coëfficiënt en index in 3 H2O">
        <text x="150" y="105" font-size="78" font-weight="800" style="font-family:var(--f-display)">3</text>
        <text x="205" y="105" font-size="78" font-weight="800" style="font-family:var(--f-display)">H</text>
        <text x="262" y="122" font-size="40" font-weight="800" style="font-family:var(--f-display)">2</text>
        <text x="290" y="105" font-size="78" font-weight="800" style="font-family:var(--f-display)">O</text>
        <path d="M172 112 L120 150" stroke="var(--accent)" stroke-width="2"/><text x="20" y="160" font-size="16"><tspan font-weight="700">coëfficiënt</tspan>: 3 deeltjes</text>
        <path d="M272 126 L330 150" stroke="var(--accent)" stroke-width="2"/><text x="300" y="166" font-size="16"><tspan font-weight="700">index</tspan>: 2 H-atomen per deeltje</text>
        <text x="380" y="70" font-size="16">geen index bij O:</text><text x="380" y="92" font-size="16">1 O-atoom per deeltje</text>
      </svg></div>
      <div class="duo">
        <div class="kaart"><h3>Index</h3><p>Het <b>kleine getal rechtsonder</b> een symbool. Het zegt hoeveel atomen van die soort in <b>één deeltje</b> zitten. Staat er geen index, dan is het 1.</p></div>
        <div class="kaart"><h3>Coëfficiënt</h3><p>Het <b>grote getal vóór</b> de formule. Het zegt <b>hoeveel deeltjes</b> er zijn. Staat er geen coëfficiënt, dan is het 1.</p></div>
      </div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">B</span><h2>Formulelezer</h2></div>
      <div class="knoppen" id="fl-knoppen"></div>
      <div class="knoppen"><span>coëfficiënt:</span><button class="knop" type="button" id="fl-min">−</button><b id="fl-c" style="font-family:var(--f-display);font-size:1.4rem;min-width:1.5em;text-align:center">1</b><button class="knop" type="button" id="fl-plus">+</button></div>
      <div class="duo"><div class="fig" id="fl-fig"></div><div class="kaart" id="fl-uitleg"></div></div>
      <div class="tip"><b>Enkelvoudig of samengesteld? Kijk naar de formule.</b><p>Staat er <b>één symbool</b> in de formule (O<sub>2</sub>, Fe, He), dan is het een <b>enkelvoudige stof</b>. Staan er <b>twee of meer verschillende symbolen</b> (H<sub>2</sub>O, NaCl), dan is het een <b>samengestelde stof</b>. Ook de naam helpt: zuurstof<b>gas</b>, stikstof<b>gas</b> en een metaal zijn enkelvoudig. Natrium<b>chloride</b> en koolstof<b>dioxide</b> zijn samengesteld.</p></div>
    </section>
  </main>

  <main class="les" id="lesC" role="tabpanel" hidden>
    <section class="blok">
      <div class="blok-kop"><span class="letter">C</span><h2>Waarom binden atomen?</h2></div>
      <p>Atomen binden om een <b>edelgasconfiguratie</b> te krijgen: een volle buitenste schil. Dat kan op drie manieren. Welke binding het wordt, lees je af uit het PSE: is het element een <b>metaal</b> of een <b>niet-metaal</b>?</p>
      <div class="tabelwrap"><table><thead><tr><th>atomen</th><th>binding</th><th>wat gebeurt er?</th><th>voorbeeld</th></tr></thead><tbody>
        <tr><td>metaal + niet-metaal</td><td><b>ionbinding</b></td><td>het metaal geeft elektronen <b>af</b> aan het niet-metaal</td><td>NaCl, MgO</td></tr>
        <tr><td>niet-metaal + niet-metaal</td><td><b>atoombinding</b></td><td>de atomen <b>delen</b> elektronen</td><td>H<sub>2</sub>, H<sub>2</sub>O, CO<sub>2</sub></td></tr>
        <tr><td>metaal + metaal</td><td><b>metaalbinding</b></td><td>de metaalatomen geven elektronen af aan een <b>elektronenzee</b></td><td>Fe, Cu, Al</td></tr></tbody></table></div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">C</span><h2>Ionbinding</h2></div>
      <div class="knoppen" id="ion-stap"><button class="knop" type="button" data-s="1" aria-pressed="true">1 · de atomen</button><button class="knop" type="button" data-s="2" aria-pressed="false">2 · een elektron gaat over</button><button class="knop" type="button" data-s="3" aria-pressed="false">3 · ionen trekken elkaar aan</button></div>
      <div class="fig" id="ion-fig"></div>
      <p id="ion-zin"></p>
      <div class="def"><span class="eyebrow">Ionbinding</span><p>Een metaal geeft elektronen af en wordt een <b>positief ion</b>. Een niet-metaal neemt die elektronen op en wordt een <b>negatief ion</b>. De tegengestelde ladingen <b>trekken elkaar aan</b>. De stof is een <b>ionverbinding</b>.</p></div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">C</span><h2>Atoombinding</h2></div>
      <div class="knoppen" id="ab-knoppen"><button class="knop" type="button" data-m="H2" aria-pressed="true">waterstofgas H<sub>2</sub></button><button class="knop" type="button" data-m="Cl2" aria-pressed="false">chloorgas Cl<sub>2</sub></button><button class="knop" type="button" data-m="HCl" aria-pressed="false">waterstofchloride HCl</button></div>
      <div class="fig"><svg id="ab-svg" viewBox="0 0 520 240"></svg></div>
      <p id="ab-zin"></p>
      <div class="def"><span class="eyebrow">Atoombinding</span><p>Twee niet-metalen <b>delen</b> elektronen. Elk atoom geeft één elektron in een <b>gemeenschappelijk elektronenpaar</b>. Dat paar telt voor beide atomen mee. Zo krijgen ze allebei een volle buitenste schil. De stof is een <b>covalente verbinding</b> (of een enkelvoudige stof, zoals H<sub>2</sub>).</p></div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">C</span><h2>Metaalbinding</h2></div>
      <div class="fig"><svg id="mb-svg" viewBox="0 0 520 220"></svg></div>
      <div class="def"><span class="eyebrow">Metaalbinding</span><p>Metaalatomen geven hun valentie-elektronen af. Er ontstaan <b>positieve metaalionen</b> in een <b>zee van vrije elektronen</b>. De negatieve elektronenzee houdt de positieve ionen samen. Omdat de elektronen vrij kunnen bewegen, <b>geleiden metalen elektrische stroom</b>.</p></div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">C</span><h2>Welke binding? Gebruik het PSE</h2></div>
      <div class="knoppen"><label>atoom 1 <select id="bk-1" class="knop"></select></label><label>atoom 2 <select id="bk-2" class="knop"></select></label></div>
      <div class="tip" id="bk-zin"></div>
    </section>
  </main>

  <main class="les" id="lesD" role="tabpanel" hidden>
    <section class="blok">
      <div class="oefening" id="oef-dm"></div>
      <div class="oefening" id="oef-form"></div>
      <div class="oefening" id="oef-as"></div>
      <div class="oefening" id="oef-tel"></div>
      <div class="oefening" id="oef-ic"></div>
      <div class="oefening" id="oef-bind"></div>
      <div class="oefening" id="oef-cls"></div>
    </section>
    <section class="ikkan" id="ikkan"></section>
  </main>
'''
css = r'''
.fig svg{max-width:560px}
.ionrij{display:flex;gap:10px;align-items:center;justify-content:center;flex-wrap:wrap}
.ionrij .kol{display:flex;flex-direction:column;align-items:center;text-align:center;gap:2px}
.ionrij svg{width:200px}
.ionrij .not{font-family:var(--f-display);font-weight:800;font-size:1.5rem}
.ionrij .pijl{font-family:var(--f-display);font-weight:800;color:var(--accent);max-width:9em;text-align:center}
.item .zin svg{width:150px;height:auto;display:block;margin-top:4px}
select.knop{padding:6px 10px}
'''
js = MOL + r'''
const STOF = {H2:'waterstofgas',O2:'zuurstofgas',N2:'stikstofgas',Cl2:'chloorgas',O3:'ozon',He:'helium',Fe:'ijzer',H2O:'water',CO2:'koolstofdioxide',NH3:'ammoniak',CH4:'methaan',HCl:'waterstofchloride',NaCl:'natriumchloride',CO:'koolstofmonoxide',SO2:'zwaveldioxide'};
const NAAM_EL = {H:'waterstof',O:'zuurstof',C:'koolstof',N:'stikstof',Cl:'chloor',Na:'natrium',Fe:'ijzer',He:'helium',S:'zwavel'};
const soortTxt = f => Object.keys(telAtomen(f)).length===1 ? 'enkelvoudige stof' : 'samengestelde stof';
const DM = ['O2','N2','He','Fe','H2O','CO2','NH3','CH4','NaCl'];
function toonDM(f){
  $('#dm-fig').innerHTML = doosSvg(f, f==='Fe'?7:6, 220, 150, f==='Fe'?1.25:1.1);
  const t = telAtomen(f), soorten = Object.keys(t);
  $('#dm-uitleg').innerHTML = `<h3>${STOF[f]} · ${fHtml(f)}</h3><p>In één deeltje: ${soorten.map(s=>`${t[s]} ${NAAM_EL[s]}atom${t[s]>1?'en':'#'}`.replace('atom#','atoom')).join(' en ')}.</p><p><b>${soorten.length} soort${soorten.length>1?'en':''} atomen</b> → <b>${soortTxt(f)}</b>.</p>${f==='Fe'||f==='He'?'<p>De deeltjes zijn hier losse atomen.</p>':''}${f==='NaCl'?'<p>Natriumchloride bestaat uit ionen in een rooster. Hier zie je telkens één natriumion en één chloride-ion.</p>':''}`;
  $$('#dm-knoppen .knop').forEach(b => b.setAttribute('aria-pressed', b.dataset.f===f));
  $('#dm-legende').innerHTML = Object.keys(t).map(s=>`<span style="display:inline-flex;align-items:center;gap:6px;margin-right:14px"><svg width="22" height="22" viewBox="0 0 22 22"><circle cx="11" cy="11" r="9" fill="url(#g-${s})" stroke="#1a1a1a"/></svg>${NAAM_EL[s]} (${s})</span>`).join('');
}
$('#dm-knoppen').innerHTML = DM.map(f=>`<button type="button" class="knop" data-f="${f}">${STOF[f]}</button>`).join('');
$$('#dm-knoppen .knop').forEach(b => b.onclick = () => toonDM(b.dataset.f));
toonDM('O2');

/* analyse en synthese */
let asModus = 'a', asT = 0;
function tekenAS(t){
  const k = Math.min(1, Math.max(0, t)); const L = [[150,72],[150,158],[85,115],[215,115]];
  let s = '';
  s += `<text x="150" y="215" text-anchor="middle" font-size="15" font-weight="700">${asModus==='a'?'water':'waterstofgas + zuurstofgas'}</text>`;
  s += `<text x="490" y="215" text-anchor="middle" font-size="15" font-weight="700">${asModus==='a'?'waterstofgas + zuurstofgas':'water'}</text>`;
  s += `<path d="M285 115 H355" stroke="var(--accent)" stroke-width="4"/><path d="M355 105 L372 115 L355 125 Z" fill="var(--accent)"/>`;
  s += `<text x="328" y="98" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent)">${asModus==='a'?'elektrische energie':'ontbranding'}</text>`;
  const water = (x,y) => L.map(([a,b])=>molSvg('H2O', x+a-150, y+b-115, 1.15, 0)).join('');
  const los = (x,y) => [-84,-28,28,84].map(d=>molSvg('H2', x+d, y-35, 1.15, d>0?.4:-.4)).join('') + molSvg('O2', x-40, y+40, 1.15, .3) + molSvg('O2', x+40, y+40, 1.15, -.3);
  const links = asModus==='a' ? water(150,115) : los(150,115);
  const rechts = asModus==='a' ? los(490,115) : water(490,115);
  s += links + rechts;
  $('#as-svg').innerHTML = s;
}
function toonAS(m){ asModus = m; $('#as-a').setAttribute('aria-pressed', m==='a'); $('#as-s').setAttribute('aria-pressed', m==='s');
  $('#as-zin').innerHTML = m==='a' ? '<b>Analyse.</b> Met elektrische stroom ontleed je water in twee <b>enkelvoudige</b> stoffen: waterstofgas en zuurstofgas. Water is dus een <b>samengestelde stof</b>.' : '<b>Synthese.</b> Waterstofgas en zuurstofgas reageren samen tot water. Uit twee enkelvoudige stoffen ontstaat een samengestelde stof.';
  tekenAS(1); }
$('#as-a').onclick = () => toonAS('a'); $('#as-s').onclick = () => toonAS('s'); toonAS('a');

/* formulelezer */
const FL = ['H2O','CO2','O2','NH3','CH4','N2','HCl','O3'];
let flF = 'H2O', flC = 1;
function toonFL(){
  const t = telAtomen(flF); const w = 120*flC + 40;
  let s = `<svg viewBox="0 0 ${Math.max(w,260)} 150">`;
  for (let i=0;i<flC;i++) s += molSvg(flF, 80+i*120 + (Math.max(w,260)-w)/2, 72, 1.5);
  s += `<text x="${Math.max(w,260)/2}" y="140" text-anchor="middle" font-size="22" font-weight="800" style="font-family:var(--f-display)">${flC>1?flC+' ':''}${flF.replace(/(\d+)/g,'<tspan font-size="15" dy="6">$1</tspan><tspan dy="-6"></tspan>')}</text></svg>`;
  $('#fl-fig').innerHTML = s;
  $('#fl-c').textContent = flC;
  $('#fl-uitleg').innerHTML = `<h3>${flC>1?flC+' ':''}${fHtml(flF)} · ${STOF[flF]}</h3><p>${flC} deeltje${flC>1?'s':''}. Per deeltje:</p><ul style="margin:0;padding-left:20px">${Object.entries(t).map(([s,n])=>`<li>${n} ${s}-atoom${n>1?'en':''} → in totaal ${flC} · ${n} = <b>${flC*n}</b></li>`).join('')}</ul><p><b>${soortTxt(flF)}</b>: ${Object.keys(t).length===1?'één soort atomen':'meer soorten atomen'}.</p>`;
  $$('#fl-knoppen .knop').forEach(b => b.setAttribute('aria-pressed', b.dataset.f===flF));
}
$('#fl-knoppen').innerHTML = FL.map(f=>`<button type="button" class="knop" data-f="${f}">${fHtml(f)}</button>`).join('');
$$('#fl-knoppen .knop').forEach(b => b.onclick = () => { flF = b.dataset.f; toonFL(); });
$('#fl-min').onclick = () => { flC = Math.max(1, flC-1); toonFL(); }; $('#fl-plus').onclick = () => { flC = Math.min(4, flC+1); toonFL(); };
toonFL();

/* ionbinding */
function toonIon(st){
  const na = BIJZ.sym.Na, cl = BIJZ.sym.Cl;
  $$('#ion-stap .knop').forEach(b => b.setAttribute('aria-pressed', +b.dataset.s===st));
  const kol = (svg, not, txt) => `<div class="kol">${svg}<span class="not">${not}</span><span>${txt}</span></div>`;
  if (st===1) $('#ion-fig').innerHTML = `<div class="ionrij">${kol(bohrSvg(11,12,11),'Na','natriumatoom · 2/8/1')}${kol(bohrSvg(17,18,17),'Cl','chlooratoom · 2/8/7')}</div>`;
  if (st===2) $('#ion-fig').innerHTML = `<div class="ionrij">${kol(bohrSvg(11,12,10,{valentie:false}),'Na<sup>+</sup>','natriumion · 2/8')}<div class="pijl">1 elektron gaat van Na naar Cl →</div>${kol(bohrSvg(17,18,18,{valentie:false}),'Cl<sup>−</sup>','chloride-ion · 2/8/8')}</div>`;
  if (st===3){ let r = '<svg viewBox="0 0 360 230" style="max-width:360px">'; for (let i=0;i<5;i++) for (let j=0;j<4;j++){ const na=(i+j)%2===0; const x=60+i*60, y=30+j*55; r += `<circle cx="${x}" cy="${y}" r="${na?14:22}" fill="url(#g-${na?'Na':'Cl'})" stroke="#1a1a1a"/><text x="${x}" y="${y+5}" text-anchor="middle" font-size="13" font-weight="700" fill="${na?'#fff':'#0b2a10'}">${na?'+':'−'}</text>`; } r += '</svg>';
    $('#ion-fig').innerHTML = `<div class="ionrij">${r}</div>`; }
  $('#ion-zin').innerHTML = ['', 'Natrium is een <b>metaal</b> met 1 valentie-elektron. Chloor is een <b>niet-metaal</b> met 7 valentie-elektronen.', 'Natrium geeft zijn valentie-elektron aan chloor. Nu hebben <b>allebei</b> een volle buitenste schil. Er ontstaan een positief ion Na<sup>+</sup> en een negatief ion Cl<sup>−</sup>.', 'De positieve en negatieve ionen trekken elkaar aan. Zo ontstaat een <b>ionrooster</b>: natriumchloride (keukenzout), NaCl.'][st];
}
$$('#ion-stap .knop').forEach(b => b.onclick = () => toonIon(+b.dataset.s)); toonIon(1);

/* atoombinding: buitenste schillen die overlappen */
const AB = {H2:[['H',1],['H',1]], Cl2:[['Cl',7],['Cl',7]], HCl:[['H',1],['Cl',7]]};
function toonAB(m){
  const [[s1,v1],[s2,v2]] = AB[m]; const r1 = s1==='H'?62:85, r2 = s2==='H'?62:85; const x1 = 260-(r1+r2)/2+22, x2 = x1+(r1+r2)-44, y=118;
  let s = `<circle cx="${x1}" cy="${y}" r="${r1}" fill="color-mix(in srgb,var(--accent) 6%,transparent)" stroke="var(--accent)" stroke-width="2"/><circle cx="${x2}" cy="${y}" r="${r2}" fill="color-mix(in srgb,var(--accent) 6%,transparent)" stroke="var(--accent)" stroke-width="2"/>`;
  s += `<circle cx="${x1}" cy="${y}" r="20" fill="url(#g-${s1})" stroke="#1a1a1a"/><text x="${x1}" y="${y+6}" text-anchor="middle" font-size="17" font-weight="800">${s1}</text>`;
  s += `<circle cx="${x2}" cy="${y}" r="20" fill="url(#g-${s2})" stroke="#1a1a1a"/><text x="${x2}" y="${y+6}" text-anchor="middle" font-size="17" font-weight="800">${s2}</text>`;
  const xm = (x1*r2 + x2*r1)/(r1+r2) + (r1-r2)*0.25;
  const xs = x1 + (r1*r1 - r2*r2 + (x2-x1)**2)/(2*(x2-x1));
  s += `<circle cx="${xs}" cy="${y-9}" r="7" fill="var(--valentie)" stroke="var(--ink)"/><circle cx="${xs}" cy="${y+9}" r="7" fill="var(--valentie)" stroke="var(--ink)"/>`;
  const rest = (x, r, n, kant) => { let o=''; for(let i=0;i<n-1;i++){ const a = (kant<0?Math.PI:0) + (i-(n-2)/2)*0.62; const off = (i%2? 0.09:-0.09); o += `<circle cx="${(x+r*Math.cos(a+off)).toFixed(1)}" cy="${(y+r*Math.sin(a+off)).toFixed(1)}" r="7" fill="var(--elektron)" stroke="var(--ink)"/>`; } return o; };
  s += rest(x1, r1, v1, -1) + rest(x2, r2, v2, 1);
  s += `<text x="${xs}" y="228" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent)">gemeenschappelijk elektronenpaar</text>`;
  $('#ab-svg').innerHTML = s;
  $$('#ab-knoppen .knop').forEach(b => b.setAttribute('aria-pressed', b.dataset.m===m));
  const vol = e => e==='H' ? '2 elektronen (zoals helium)' : '8 elektronen (zoals argon)';
  $('#ab-zin').innerHTML = `Elk atoom brengt 1 elektron in het gele paar. Tel je de elektronen in de cirkel van een atoom, dan heeft ${s1==='H'?'waterstof':'chloor'} ${vol(s1)}${s1!==s2?` en chloor ${vol(s2)}`:''}. Alleen de <b>buitenste schil</b> is getekend.`;
}
$$('#ab-knoppen .knop').forEach(b => b.onclick = () => toonAB(b.dataset.m)); toonAB('H2');

/* metaalbinding: bewegende elektronen */
const MB = []; for(let i=0;i<22;i++) MB.push({x:Math.random()*500+10, y:Math.random()*200+10, vx:(Math.random()-.5)*1.6, vy:(Math.random()-.5)*1.6});
function tekenMB(){
  let s = ''; for (let i=0;i<7;i++) for (let j=0;j<3;j++){ const x=50+i*70, y=45+j*65; s += `<circle cx="${x}" cy="${y}" r="22" fill="url(#g-Fe)" stroke="#1a1a1a"/><text x="${x}" y="${y+6}" text-anchor="middle" font-size="17" font-weight="800">+</text>`; }
  MB.forEach(e => { e.x+=e.vx; e.y+=e.vy; if(e.x<8||e.x>512) e.vx*=-1; if(e.y<8||e.y>212) e.vy*=-1; s += `<circle cx="${e.x.toFixed(1)}" cy="${e.y.toFixed(1)}" r="5" fill="var(--elektron)" stroke="var(--ink)" stroke-width=".8"/>`; });
  $('#mb-svg').innerHTML = s;
}
(function lus(){ if(!$('#lesC').hidden) tekenMB(); requestAnimationFrame(lus); })();

/* bindingskiezer */
const BK = ['Na','K','Mg','Ca','Al','Fe','Cu','H','C','N','O','S','Cl'];
const MET = {Na:1,K:1,Mg:1,Ca:1,Al:1,Fe:1,Cu:1};
const elNaam = s => BIJZ.sym[s] ? BIJZ.sym[s].naam : ({Fe:'ijzer',Cu:'koper'})[s];
['#bk-1','#bk-2'].forEach((id,k) => { $(id).innerHTML = BK.map(s=>`<option value="${s}">${elNaam(s)} (${s})</option>`).join(''); $(id).value = k?'Cl':'Na'; $(id).onchange = toonBK; });
function toonBK(){
  const a = $('#bk-1').value, b = $('#bk-2').value, ma = !!MET[a], mb = !!MET[b];
  const wat = e => MET[e] ? 'een metaal' : 'een niet-metaal'; const H = t => t.startsWith('ij') ? 'IJ'+t.slice(2) : t[0].toUpperCase()+t.slice(1);
  let r;
  if (ma && mb) r = `<b>Metaalbinding.</b> ${H(elNaam(a))} en ${elNaam(b)} zijn allebei metalen.`;
  else if (!ma && !mb) r = `<b>Atoombinding.</b> ${H(elNaam(a))} en ${elNaam(b)} zijn allebei niet-metalen. Ze delen elektronen. ${a!==b?'De stof is een <b>covalente verbinding</b>.':''}`;
  else r = `<b>Ionbinding.</b> ${H(elNaam(ma?a:b))} is een metaal, ${elNaam(ma?b:a)} is een niet-metaal. Het metaal geeft elektronen af. De stof is een <b>ionverbinding</b>.`;
  $('#bk-zin').innerHTML = `<p>${r}</p>`;
}
toonBK();

/* oefeningen */
const ES = [{k:'e',label:'enkelvoudige stof'},{k:'s',label:'samengestelde stof'}];
sorteer($('#oef-dm'), {id:'dm', titel:'Oefening 1 · Deeltjesmodel', opdracht:'Is dit een enkelvoudige of een samengestelde stof?', opties:ES,
  items:['O2','H2O','N2','CO2','He','CH4','O3','HCl'].map(f => ({tekst:doosSvg(f, f==='He'?7:6, 220, 150, 1.1), antwoord:soortTxt(f)[0]==='e'?'e':'s', uitleg:`Dit is ${STOF[f]} (${fHtml(f)}): ${Object.keys(telAtomen(f)).length} soort${Object.keys(telAtomen(f)).length>1?'en':''} atomen.`}))});
sorteer($('#oef-form'), {id:'form', titel:'Oefening 2 · Formule of naam', opdracht:'Enkelvoudig of samengesteld?', opties:ES, items:[
  {tekst:'Cl<sub>2</sub>', antwoord:'e', uitleg:'Eén symbool: chloor.'},{tekst:'NaCl', antwoord:'s', uitleg:'Twee symbolen: Na en Cl.'},{tekst:'koper (Cu)', antwoord:'e'},
  {tekst:'koolstofdioxide', antwoord:'s', uitleg:'Gemaakt van koolstof en zuurstof.'},{tekst:'stikstofgas', antwoord:'e', uitleg:'Alleen stikstofatomen: N<sub>2</sub>.'},{tekst:'C<sub>6</sub>H<sub>12</sub>O<sub>6</sub> (glucose)', antwoord:'s'},{tekst:'ozon (O<sub>3</sub>)', antwoord:'e', uitleg:'Alleen zuurstofatomen.'}]});
sorteer($('#oef-as'), {id:'as', titel:'Oefening 3 · Analyse of synthese?', opties:[{k:'a',label:'analyse'},{k:'s',label:'synthese'}], items:[
  {tekst:'water → waterstofgas + zuurstofgas', antwoord:'a', uitleg:'Een samengestelde stof wordt ontleed.'},
  {tekst:'ijzer + zwavel → ijzersulfide', antwoord:'s', uitleg:'Uit twee enkelvoudige stoffen ontstaat een samengestelde stof.'},
  {tekst:'suiker → koolstof + water (door verwarmen)', antwoord:'a', uitleg:'Een thermolyse is een analyse.'},
  {tekst:'waterstofgas + chloorgas → waterstofchloride', antwoord:'s'},
  {tekst:'natriumchloride → natrium + chloorgas (met stroom)', antwoord:'a'}]});
const telItems = () => shuffle([['3 H2O','H',6],['2 CO2','O',4],['4 NH3','H',12],['CH4','H',4],['2 O3','O',6],['5 H2','H',10],['3 CO2','C',3],['2 NH3','N',2]]).slice(0,5)
  .map(([f,el,n]) => ({tekst:`Hoeveel ${el}-atomen zijn er in <b>${f.split(' ').map((x,i,a)=>a.length>1&&i===0?x:fHtml(x)).join(' ')}</b>?`, antwoord:[String(n)], uitleg:`coëfficiënt × index = ${n}.`}));
invul($('#oef-tel'), {id:'tel', titel:'Oefening 4 · Atomen tellen', items:telItems});
sorteer($('#oef-ic'), {id:'ic', titel:'Oefening 5 · Index of coëfficiënt?', opties:[{k:'i',label:'index'},{k:'c',label:'coëfficiënt'}], items:[
  {tekst:'de <b>2</b> in 2 H<sub>2</sub>O (vooraan)', antwoord:'c'},{tekst:'de <b>2</b> in H<sub>2</sub>O', antwoord:'i'},{tekst:'het getal dat zegt hoeveel deeltjes er zijn', antwoord:'c'},
  {tekst:'het getal dat zegt hoeveel atomen van één soort in één deeltje zitten', antwoord:'i'},{tekst:'de <b>3</b> in O<sub>3</sub>', antwoord:'i'}]});
sorteer($('#oef-bind'), {id:'bind', titel:'Oefening 6 · Welke binding?', opties:[{k:'i',label:'ionbinding'},{k:'a',label:'atoombinding'},{k:'m',label:'metaalbinding'}], items:[
  {tekst:'De atomen delen elektronen.', antwoord:'a'},{tekst:'Een metaal geeft elektronen af aan een niet-metaal.', antwoord:'i'},
  {tekst:'Positieve ionen zitten in een zee van vrije elektronen.', antwoord:'m'},{tekst:'koper (Cu)', antwoord:'m', uitleg:'Een metaal.'},
  {tekst:'magnesiumoxide (MgO)', antwoord:'i', uitleg:'Magnesium is een metaal, zuurstof een niet-metaal.'},{tekst:'water (H<sub>2</sub>O)', antwoord:'a', uitleg:'Waterstof en zuurstof zijn niet-metalen.'},
  {tekst:'Er ontstaat een gemeenschappelijk elektronenpaar.', antwoord:'a'}]});
sorteer($('#oef-cls'), {id:'cls', titel:'Oefening 7 · Ionverbinding of covalente verbinding?', opdracht:'Zoek de elementen op in het PSE: metaal of niet-metaal?', opties:[{k:'i',label:'ionverbinding'},{k:'c',label:'covalente verbinding'}], items:[
  {tekst:'NaCl', antwoord:'i', uitleg:'Na is een metaal, Cl een niet-metaal.'},{tekst:'CO<sub>2</sub>', antwoord:'c', uitleg:'C en O zijn niet-metalen.'},{tekst:'CaCl<sub>2</sub>', antwoord:'i', uitleg:'Ca is een metaal.'},
  {tekst:'NH<sub>3</sub>', antwoord:'c', uitleg:'N en H zijn niet-metalen.'},{tekst:'KBr', antwoord:'i'},{tekst:'CH<sub>4</sub>', antwoord:'c'},{tekst:'Al<sub>2</sub>O<sub>3</sub>', antwoord:'i', uitleg:'Al is een metaal.'},{tekst:'SO<sub>2</sub>', antwoord:'c'}]});
const som = (...k) => { const a = k.map(x=>scores[x]).filter(Boolean); if(!a.length) return null; return {juist:a.reduce((t,x)=>t+x.juist,0), totaal:k.map(x=>scores[x]?scores[x].totaal:0).reduce((t,x)=>t+x,0), klaar:k.every(x=>scores[x]&&scores[x].klaar)}; };
ikkanFn = () => { $('#ikkan').innerHTML = `<h3>Controle thema 3</h3><ul>
  ${regel('Ik verklaar met het deeltjesmodel het verschil tussen een enkelvoudige en een samengestelde stof.', scores.dm)}
  ${regel('Ik leg het verschil uit tussen een analyse en een synthese.', scores.as)}
  ${regel('Ik beschrijf de betekenis van een index en het verschil met een coëfficiënt.', som('tel','ic'))}
  ${regel('Ik classificeer stoffen met hun formule of naam als enkelvoudig of samengesteld.', scores.form)}
  ${regel('Ik leg uit hoe een ionbinding, een atoombinding en een metaalbinding tot stand komen.', scores.bind)}
  ${regel('Ik classificeer met het PSE stoffen als ionverbinding of covalente verbinding.', scores.cls)}</ul>`; };
updateIkKan();
'''
pagina('chemie-samenstelling.html', 'Chemische samenstelling van stoffen', 'Chemie · 3de jaar · thema 3 · hoofdstuk 1 en 2',
  'Uit welke atomen bestaat een stof? Hoe lees je een formule? En hoe houden atomen elkaar vast?',
  'LPD 3C: De leerlingen interpreteren de symbolische schrijfwijze van enkelvoudige en samengestelde stoffen. LPD 10C: De leerlingen stellen de ionbinding, de atoombinding en de metaalbinding op als streven van atomen naar de edelgasconfiguratie.',
  ['Een <b>zuivere stof</b> bestaat uit één soort deeltjes.', 'Metalen en niet-metalen in het PSE, en de <b>valentie-elektronen</b>.', 'De <b>edelgasconfiguratie</b> en <b>ionvorming</b> (thema 2).'],
  ('Lesdoelen thema 3 · p. 88–132', ['Ik gebruik het deeltjesmodel om het verschil tussen een enkelvoudige en een samengestelde stof te verklaren.', 'Ik leg het verschil uit tussen een analyse en synthese.', 'Ik beschrijf de betekenis van een index en ik interpreteer chemische formules.', 'Ik leg het verschil uit tussen een index en een coëfficiënt.', 'Ik gebruik de symbolische schrijfwijze of naamgeving van stoffen om de stoffen te classificeren als enkelvoudige of samengestelde stof.', 'Ik leg uit hoe een ionbinding, een atoombinding en een metaalbinding tot stand komt.', 'Ik gebruik het PSE om samengestelde stoffen als ionverbindingen of covalente verbindingen te classificeren.']),
  [('lesA','1.1','Enkelvoudig of samengesteld','analyse en synthese'),('lesB','1.2','Formules lezen','index en coëfficiënt'),('lesC','2','Chemische bindingen','ion, atoom, metaal'),('lesD','✎','Oefenen','alle lesdoelen')],
  body, css, js)
