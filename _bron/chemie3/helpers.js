const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const shuffle = a => { a=a.slice(); for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];} return a; };
const norm = s => String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/\s+/g,' ').trim();
const komma = (x,d=1) => x.toFixed(d).replace('.',',');
const scores = {};
let ikkanFn = () => {};
const updateIkKan = () => ikkanFn();

/* tabbladen + #anker */
function tabs(){
  const toon = id => {
    $$('.lestab').forEach(t => t.setAttribute('aria-selected', t.getAttribute('aria-controls')===id?'true':'false'));
    $$('main.les').forEach(m => m.hidden = m.id!==id);
    document.dispatchEvent(new CustomEvent('tab', {detail:id}));
  };
  $$('.lestab').forEach(t => t.addEventListener('click', () => toon(t.getAttribute('aria-controls'))));
  const h = location.hash.slice(1);
  if (h && document.getElementById(h) && document.getElementById(h).matches('main.les')) toon(h);
}

/* sorteeroefening: opties per oefening of per item, antwoord mag een lijst zijn */
function sorteer(el, cfg){
  function render(){
    const items = cfg.vast ? cfg.items : shuffle(cfg.items);
    el.innerHTML = `<div class="oef-kop"><h3>${cfg.titel}</h3><span class="score" data-score>0 / ${items.length}</span></div>
      ${cfg.opdracht?`<p>${cfg.opdracht}</p>`:''}<ul class="items"></ul><button class="knop opnieuw" type="button">↺ Opnieuw</button>`;
    const ul = el.querySelector('.items'); let juist=0, klaar=0;
    scores[cfg.id] = {juist:0,totaal:items.length,klaar:false};
    items.forEach(it => {
      const opties = it.opties || cfg.opties;
      const goed = [].concat(it.antwoord);
      const li = document.createElement('li'); li.className='item';
      li.innerHTML = `<span class="zin">${it.tekst}</span><div class="opties">${(it.opties?shuffle(opties):opties).map(o=>`<button type="button" data-k="${o.k}">${o.label}</button>`).join('')}</div><div class="uitleg" hidden></div>`;
      li.querySelectorAll('.opties button').forEach(b => b.addEventListener('click', () => {
        const ok = goed.includes(b.dataset.k);
        li.classList.add(ok?'juist':'fout'); b.classList.add('gekozen');
        li.querySelectorAll('.opties button').forEach(x => x.disabled=true);
        const lbl = goed.map(k => opties.find(o=>o.k===k).label).join(' of ');
        const u = li.querySelector('.uitleg'); u.hidden=false;
        u.innerHTML = (ok?'<b>Juist!</b> ':`<b>Niet juist.</b> Het is: ${lbl}. `) + (it.uitleg||'');
        klaar++; if(ok) juist++;
        el.querySelector('[data-score]').textContent = `${juist} / ${items.length}`;
        scores[cfg.id] = {juist,totaal:items.length,klaar:klaar===items.length}; updateIkKan();
      }));
      ul.appendChild(li);
    });
    el.querySelector('.opnieuw').addEventListener('click', () => { render(); updateIkKan(); });
  }
  render();
}

/* invuloefening: leerling typt het antwoord */
function invul(el, cfg){
  function render(){
    const pool = typeof cfg.items==='function' ? cfg.items() : cfg.items;
    const items = cfg.vast ? pool : shuffle(pool);
    el.innerHTML = `<div class="oef-kop"><h3>${cfg.titel}</h3><span class="score" data-score>0 / ${items.length}</span></div>
      ${cfg.opdracht?`<p>${cfg.opdracht}</p>`:''}<ul class="items"></ul><button class="knop opnieuw" type="button">↺ ${cfg.opnieuwTekst||'Opnieuw'}</button>`;
    const ul = el.querySelector('.items'); let juist=0, klaar=0;
    scores[cfg.id] = {juist:0,totaal:items.length,klaar:false};
    items.forEach((it,i) => {
      const li = document.createElement('li'); li.className='item';
      li.innerHTML = `<span class="zin">${it.tekst}</span><form class="invul"><input type="text" autocomplete="off" aria-label="antwoord ${i+1}" id="${cfg.id}-in-${i}"><button class="knop" type="submit">Controleer</button></form><div class="uitleg" hidden></div>`;
      li.querySelector('form').addEventListener('submit', e => {
        e.preventDefault();
        const inp = li.querySelector('input'); const v = inp.value.trim(); if(!v) return;
        const res = (it.check || cfg.check || standaardCheck)(v, it);
        const u = li.querySelector('.uitleg'); u.hidden=false;
        if (res.bijna){ u.innerHTML = `<b>Bijna.</b> ${res.bijna}`; return; }
        li.classList.add(res.ok?'juist':'fout'); inp.disabled = true; li.querySelector('button').disabled = true;
        u.innerHTML = (res.ok?'<b>Juist!</b> ':`<b>Niet juist.</b> Het is: ${it.toon||it.antwoord[0]}. `) + (it.uitleg||'');
        klaar++; if(res.ok) juist++;
        el.querySelector('[data-score]').textContent = `${juist} / ${items.length}`;
        scores[cfg.id] = {juist,totaal:items.length,klaar:klaar===items.length}; updateIkKan();
      });
      ul.appendChild(li);
    });
    el.querySelector('.opnieuw').addEventListener('click', () => { render(); updateIkKan(); });
  }
  render();
  return {render};
}
function standaardCheck(v, it){ return {ok: it.antwoord.some(a => norm(a)===norm(v))}; }
function symboolCheck(v, it){
  const s = it.antwoord[0];
  if (v===s) return {ok:true};
  if (v.toLowerCase()===s.toLowerCase()) return {bijna:`Let op de hoofdletters: een symbool begint met een hoofdletter, de tweede letter is klein.`};
  return {ok:false};
}

/* "ik kan"-regel */
function regel(label, s){
  if(!s) return `<li><span class="st">nog niet</span><span>${label}</span></li>`;
  const ok = s.klaar && s.juist/s.totaal>=.8;
  const st = s.klaar ? `${s.juist}/${s.totaal}` : (s.juist?`${s.juist}/${s.totaal} …`:'nog niet');
  return `<li><span class="st ${ok?'ok':''}">${ok?'✓ ':''}${st}</span><span>${label}</span></li>`;
}

/* notatie met massagetal en atoomnummer */
const notatie = (sym, A, Z, lading='') => `<span class="notatie"><span class="ge"><span>${A}</span><span>${Z}</span></span><span class="sy">${sym}</span>${lading?`<sup style="font-size:.6em">${lading}</sup>`:''}</span>`;

/* verdeling elektronen over schillen (eenvoudig: 2, 8, 8, 2) */
function schillen(e){ const max=[2,8,8,2]; const r=[]; let rest=e; for(const m of max){ if(rest<=0) break; const n=Math.min(m,rest); r.push(n); rest-=n; } return r; }

/* schillenmodel tekenen */
function bohrSvg(p, n, e, opt={}){
  const sch = opt.schillen || schillen(e); const R = sch.length>4 ? [0,36,58,80,102,124] : [0,46,72,98,122]; const cx=140, cy=140; const er = sch.length>4 || Math.max(...sch,0)>8 ? 4.5 : 6;
  let s = `<svg viewBox="0 0 280 280" role="img" aria-label="schillenmodel">`;
  for (let i=1;i<=Math.max(sch.length, opt.minSchillen||0);i++) s += `<circle cx="${cx}" cy="${cy}" r="${R[i]}" fill="none" stroke="var(--line)" stroke-width="2"/>`;
  // kern
  const tot = p+n; const kr = tot ? Math.min(sch.length>4?26:30, 10+Math.sqrt(tot)*3.6) : 8;
  s += `<circle cx="${cx}" cy="${cy}" r="${kr}" fill="var(--surface)" stroke="var(--ink)" stroke-width="1.5"/>`;
  const deeltjes = []; for(let i=0;i<p;i++) deeltjes.push('p'); for(let i=0;i<n;i++) deeltjes.push('n');
  // mengen
  const gemengd = []; let ip=0, inn=0; while(ip<p||inn<n){ if(ip<p){gemengd.push('p');ip++;} if(inn<n){gemengd.push('n');inn++;} }
  gemengd.forEach((d,i) => { const a=i*2.39996, r=Math.sqrt(i+0.5)*(kr-5)/Math.sqrt(Math.max(tot,1)); const x=cx+r*Math.cos(a), y=cy+r*Math.sin(a);
    s += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${tot>60?2.4:tot>24?3.2:4}" fill="${d==='p'?'var(--proton)':'var(--neutron)'}" stroke="var(--ink)" stroke-width=".5"/>`; });
  sch.forEach((cnt,i) => { const laatste = i===sch.length-1;
    for(let k=0;k<cnt;k++){ const a = -Math.PI/2 + k*2*Math.PI/cnt + i*0.3; const x=cx+R[i+1]*Math.cos(a), y=cy+R[i+1]*Math.sin(a);
      s += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${er}" fill="${laatste&&opt.valentie!==false?'var(--valentie)':'var(--elektron)'}" stroke="var(--ink)" stroke-width="1"/>`; } });
  if (opt.labels) ['K','L','M','N','O'].slice(0,sch.length).forEach((l,i)=>{ s += `<text x="${cx+R[i+1]*0.71+4}" y="${cy-R[i+1]*0.71-4}" font-size="12" font-family="var(--f-mono)" fill="var(--muted)">${l}</text>`; });
  return s + '</svg>';
}

/* elementen: Z, symbool, naam, (meest voorkomend) massagetal, Ar, groep (1-18), periode, EN, categorie */
const ELEM = [
 [1,'H','waterstof',1,1.0,1,1,2.1,'nm'],[2,'He','helium',4,4.0,18,1,null,'eg'],
 [3,'Li','lithium',7,6.9,1,2,1.0,'m'],[4,'Be','beryllium',9,9.0,2,2,1.5,'m'],[5,'B','boor',11,10.8,13,2,2.0,'nm'],[6,'C','koolstof',12,12.0,14,2,2.5,'nm'],[7,'N','stikstof',14,14.0,15,2,3.0,'nm'],[8,'O','zuurstof',16,16.0,16,2,3.5,'nm'],[9,'F','fluor',19,19.0,17,2,4.0,'nm'],[10,'Ne','neon',20,20.2,18,2,null,'eg'],
 [11,'Na','natrium',23,23.0,1,3,0.9,'m'],[12,'Mg','magnesium',24,24.3,2,3,1.2,'m'],[13,'Al','aluminium',27,27.0,13,3,1.5,'m'],[14,'Si','silicium',28,28.1,14,3,1.8,'nm'],[15,'P','fosfor',31,31.0,15,3,2.1,'nm'],[16,'S','zwavel',32,32.1,16,3,2.5,'nm'],[17,'Cl','chloor',35,35.5,17,3,3.0,'nm'],[18,'Ar','argon',40,39.9,18,3,null,'eg'],
 [19,'K','kalium',39,39.1,1,4,0.8,'m'],[20,'Ca','calcium',40,40.1,2,4,1.0,'m'],[31,'Ga','gallium',69,69.7,13,4,1.6,'m'],[32,'Ge','germanium',74,72.6,14,4,1.8,'m'],[33,'As','arseen',75,74.9,15,4,2.0,'nm'],[34,'Se','seleen',80,79.0,16,4,2.4,'nm'],[35,'Br','broom',79,79.9,17,4,2.8,'nm'],[36,'Kr','krypton',84,83.8,18,4,null,'eg'],
 [37,'Rb','rubidium',85,85.5,1,5,0.8,'m'],[38,'Sr','strontium',88,87.6,2,5,1.0,'m'],[49,'In','indium',115,114.8,13,5,1.7,'m'],[50,'Sn','tin',120,118.7,14,5,1.8,'m'],[51,'Sb','antimoon',121,121.8,15,5,1.9,'m'],[52,'Te','telluur',130,127.6,16,5,2.1,'nm'],[53,'I','jood',127,126.9,17,5,2.5,'nm'],[54,'Xe','xenon',132,131.3,18,5,null,'eg'],
 [55,'Cs','cesium',133,132.9,1,6,0.7,'m'],[56,'Ba','barium',138,137.3,2,6,0.9,'m'],[81,'Tl','thallium',205,204.4,13,6,1.8,'m'],[82,'Pb','lood',208,207.2,14,6,1.8,'m'],[83,'Bi','bismut',209,209.0,15,6,1.9,'m'],[84,'Po','polonium',209,209,16,6,2.0,'m'],[85,'At','astaat',210,210,17,6,2.2,'nm'],[86,'Rn','radon',222,222,18,6,null,'eg'],
 [87,'Fr','francium',223,223,1,7,0.7,'m'],[88,'Ra','radium',226,226,2,7,0.9,'m']
].map(([Z,sym,naam,A,Ar,g,per,en,cat])=>({Z,sym,naam,A,Ar,g,per,en,cat}));
const BIJZ = {Z:{}, sym:{}}; ELEM.forEach(e => { BIJZ.Z[e.Z]=e; BIJZ.sym[e.sym]=e; });
const GROEP_ROMEINS = {1:'Ia',2:'IIa',13:'IIIa',14:'IVa',15:'Va',16:'VIa',17:'VIIa',18:'VIIIa'};
const VALENTIE = g => g<=2 ? g : g-10;


const CATNAAM = {m:'metaal', nm:'niet-metaal', eg:'edelgas'};
const CATKLEUR = {m:'--c-metaal', nm:'--c-nietmetaal', eg:'--c-edelgas'};
const GROEPNAAM = e => e.g===1 && e.Z!==1 ? 'alkalimetalen' : e.g===2 ? 'aardalkalimetalen' : e.g===17 ? 'halogenen' : e.g===18 ? 'edelgassen' : '';
const GROEPKLEUR = {alkalimetalen:'--c-alkali', aardalkalimetalen:'--c-aardalkali', halogenen:'--c-halogeen', edelgassen:'--c-edelgas'};
const valentie = e => e.Z===2 ? 2 : VALENTIE(e.g);
const BG = {4:['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn',21], 5:['Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd',39], 6:['La','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg',0], 7:['Ac','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn',0]};
const BGZ = {6:[57,72,73,74,75,76,77,78,79,80], 7:[89,104,105,106,107,108,109,110,111,112]};
const P7 = [['Nh',113,13],['Fl',114,14],['Mc',115,15],['Lv',116,16],['Ts',117,17],['Og',118,18]];
