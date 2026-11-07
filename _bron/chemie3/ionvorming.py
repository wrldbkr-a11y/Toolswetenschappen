from bouw import pagina
body = r'''
  <main class="les" id="lesA" role="tabpanel">
    <section class="blok">
      <div class="blok-kop"><span class="letter">A</span><h2>Wanneer ontstaat een ion?</h2></div>
      <p>Een atoom is <b>neutraal</b>: het heeft evenveel protonen (+) als elektronen (−). Toch willen veel atomen hun aantal elektronen veranderen. Ze willen een <b>edelgasconfiguratie</b>: een volle buitenste schil, zoals een edelgas.</p>
      <div class="duo">
        <div class="kaart"><h3>Metaal: geeft elektronen af</h3><p>Een metaal staat links in het PSE. Het heeft maar <b>1, 2 of 3 valentie-elektronen</b>. Die geeft het af. Dan is de schil eronder de buitenste schil, en die is vol.</p><p>Er zijn nu <b>minder elektronen dan protonen</b>: het deeltje is <b>positief</b>.</p></div>
        <div class="kaart"><h3>Niet-metaal: neemt elektronen op</h3><p>Een niet-metaal staat rechts in het PSE. Het heeft <b>6 of 7 valentie-elektronen</b>. Het neemt er 2 of 1 bij. Dan is de buitenste schil vol met 8 elektronen.</p><p>Er zijn nu <b>meer elektronen dan protonen</b>: het deeltje is <b>negatief</b>.</p></div>
      </div>
      <div class="def"><span class="eyebrow">Definitie</span><p>Een <b>ion</b> is een geladen deeltje. Het ontstaat als een atoom één of meer elektronen <b>afgeeft</b> of <b>opneemt</b>.</p></div>
      <div class="tip"><b>Let op</b><p>Het aantal <b>protonen</b> verandert nooit. Alleen het aantal elektronen verandert. De lading van het ion = aantal protonen − aantal elektronen.</p></div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">A</span><h2>Ionbouwer</h2></div>
      <p>Kies een element. Je ziet het atoom en het ion dat ervan gemaakt wordt.</p>
      <div class="knoppen" id="ib-knoppen"></div>
      <div class="fig"><div class="ib" id="ib"></div></div>
      <div class="tabelwrap"><table><thead><tr><th></th><th>atoom</th><th>ion</th></tr></thead><tbody id="ib-tabel"></tbody></table></div>
      <div class="tip" id="ib-zin"></div>
    </section>
  </main>

  <main class="les" id="lesB" role="tabpanel" hidden>
    <section class="blok">
      <div class="blok-kop"><span class="letter">B</span><h2>De notatie van een ion</h2></div>
      <p>Je schrijft het <b>symbool</b> van het element. Rechtsboven schrijf je de <b>lading</b>: eerst het getal, dan het teken. Is de lading 1, dan schrijf je het getal 1 niet.</p>
      <div class="trio">
        <div class="kaart" style="text-align:center"><span style="font-family:var(--f-display);font-size:2.4rem;font-weight:800">Na<sup style="font-size:.55em">+</sup></span><p>1 elektron afgegeven</p></div>
        <div class="kaart" style="text-align:center"><span style="font-family:var(--f-display);font-size:2.4rem;font-weight:800">Mg<sup style="font-size:.55em">2+</sup></span><p>2 elektronen afgegeven</p></div>
        <div class="kaart" style="text-align:center"><span style="font-family:var(--f-display);font-size:2.4rem;font-weight:800">O<sup style="font-size:.55em">2−</sup></span><p>2 elektronen opgenomen</p></div>
      </div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">B</span><h2>De naam van een ion</h2></div>
      <div class="duo">
        <div class="kaart"><h3>Positief ion</h3><p>naam van het element + <b>ion</b></p><p>Na<sup>+</sup> = natrium<b>ion</b><br>Al<sup>3+</sup> = aluminium<b>ion</b></p></div>
        <div class="kaart"><h3>Negatief ion</h3><p>verkorte naam + <b>-ide</b> + <b>-ion</b></p><p>Cl<sup>−</sup> = chlor<b>ide-ion</b><br>O<sup>2−</sup> = ox<b>ide-ion</b></p></div>
      </div>
      <div class="tabelwrap"><table><thead><tr><th>groep</th><th>valentie-elektronen</th><th>wat gebeurt er?</th><th>lading</th><th>voorbeelden</th></tr></thead><tbody id="groeptabel"></tbody></table></div>
      <div class="tip"><b>Tip: kijk naar de groep</b><p>Uit het groepsnummer in het PSE haal je de lading. Groep Ia geeft 1+, IIa geeft 2+, IIIa geeft 3+. Groep VIa geeft 2−, VIIa geeft 1−. Edelgassen (VIIIa) vormen geen ionen: hun buitenste schil is al vol.</p></div>
    </section>
  </main>

  <main class="les" id="lesC" role="tabpanel" hidden>
    <section class="blok">
      <div class="oefening" id="oef-teken"></div>
      <div class="oefening" id="oef-wat"></div>
      <div class="oefening" id="oef-not"></div>
      <div class="oefening" id="oef-naam"></div>
      <div class="oefening" id="oef-deel"></div>
    </section>
    <section class="ikkan" id="ikkan"></section>
  </main>
'''
css = r'''
.ib{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center}
.ib .kol{display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center}
.ib svg{max-width:240px}
.ib .pijl{font-family:var(--f-display);font-weight:800;color:var(--accent);text-align:center;font-size:1.05rem;max-width:11em}
.ib .pijl span{display:block;font-size:2rem;line-height:1}
.ib .not{font-family:var(--f-display);font-weight:800;font-size:1.8rem}
@media (max-width:620px){.ib{grid-template-columns:1fr}.ib .pijl span{transform:rotate(90deg)}}
'''
js = r'''
const IONEN = {Li:1, Na:1, K:1, Mg:2, Ca:2, Al:3, O:-2, S:-2, F:-1, Cl:-1, Br:-1, I:-1};
const STAM = {O:'ox', S:'sulf', F:'fluor', Cl:'chlor', Br:'brom', I:'jod'};
const ladTxt = q => q===0 ? '0' : (Math.abs(q)===1?'':Math.abs(q)) + (q>0?'+':'−');
const ionHtml = (s,q) => `${s}<sup>${ladTxt(q)}</sup>`;
const ionNaam = s => IONEN[s]>0 ? BIJZ.sym[s].naam+'ion' : STAM[s]+'ide-ion';
function ionBouwer(sym){
  const e = BIJZ.sym[sym], q = IONEN[sym], p = e.Z, n = e.A - e.Z, eIon = p - q;
  const kort = Math.min(e.Z, 20) === e.Z && e.Z <= 20;
  const atoomSch = kort ? schillen(p) : null;
  $('#ib').innerHTML = `<div class="kol">${bohrSvg(p, n, p, kort?{}:{schillen:schil36(p)})}<span class="not">${sym}</span><span>${e.naam}atoom</span></div>
    <div class="pijl"><span>→</span>${q>0?`geeft ${q} elektron${q>1?'en':''} af`:`neemt ${-q} elektron${q<-1?'en':''} op`}</div>
    <div class="kol">${bohrSvg(p, n, eIon, {valentie:false, schillen: kort && eIon<=20 ? schillen(eIon) : schil36(eIon)})}<span class="not">${ionHtml(sym,q)}</span><span>${ionNaam(sym)}</span></div>`;
  $('#ib-tabel').innerHTML = `<tr><td>protonen (+)</td><td>${p}</td><td>${p}</td></tr><tr><td>elektronen (−)</td><td>${p}</td><td><b>${eIon}</b></td></tr>
    <tr><td>lading</td><td>${p} − ${p} = 0</td><td><b>${p} − ${eIon} = ${q>0?'+':'−'}${Math.abs(q)}</b></td></tr>`;
  $('#ib-zin').innerHTML = `<b>${e.naam[0].toUpperCase()+e.naam.slice(1)} is een ${e.cat==='m'?'metaal':'niet-metaal'} uit groep ${GROEP_ROMEINS[e.g]}.</b><p>Het heeft ${valentie(e)} valentie-elektron${valentie(e)>1?'en':''}. ${q>0?`Het geeft er ${q} af`:`Het neemt er ${-q} op`}, zodat de buitenste schil vol is. Zo ontstaat het <b>${ionNaam(sym)}</b> ${ionHtml(sym,q)}.</p>`;
  $$('#ib-knoppen .knop').forEach(b => b.setAttribute('aria-pressed', b.dataset.s===sym));
}
function schil36(e){ const max=[2,8,18,18]; const r=[]; let rest=e; for(const m of max){ if(rest<=0) break; const k=Math.min(m,rest); r.push(k); rest-=k; } return r; }
$('#ib-knoppen').innerHTML = Object.keys(IONEN).filter(s=>BIJZ.sym[s].Z<=20).map(s=>`<button type="button" class="knop" data-s="${s}">${BIJZ.sym[s].naam}</button>`).join('');
$$('#ib-knoppen .knop').forEach(b => b.onclick = () => ionBouwer(b.dataset.s));
ionBouwer('Na');

$('#groeptabel').innerHTML = [['Ia',1,'geeft 1 e⁻ af','1+','Li⁺, Na⁺, K⁺'],['IIa',2,'geeft 2 e⁻ af','2+','Mg²⁺, Ca²⁺'],['IIIa',3,'geeft 3 e⁻ af','3+','Al³⁺'],['VIa',6,'neemt 2 e⁻ op','2−','O²⁻, S²⁻'],['VIIa',7,'neemt 1 e⁻ op','1−','F⁻, Cl⁻, Br⁻, I⁻']]
  .map(r=>`<tr><td><b>${r[0]}</b></td><td>${r[1]}</td><td>${r[2]}</td><td><b>${r[3]}</b></td><td>${r[4]}</td></tr>`).join('');

const PN = [{k:'p',label:'positief ion'},{k:'n',label:'negatief ion'},{k:'g',label:'geen ion'}];
sorteer($('#oef-teken'), {id:'teken', titel:'Oefening 1 · Positief of negatief?', opdracht:'Welk ion vormt dit element?', opties:PN, items:[
  {tekst:'natrium', antwoord:'p', uitleg:'Een metaal: het geeft 1 elektron af.'},
  {tekst:'chloor', antwoord:'n', uitleg:'Een niet-metaal: het neemt 1 elektron op.'},
  {tekst:'calcium', antwoord:'p', uitleg:'Een metaal uit groep IIa: het geeft 2 elektronen af.'},
  {tekst:'zuurstof', antwoord:'n', uitleg:'Een niet-metaal uit groep VIa: het neemt 2 elektronen op.'},
  {tekst:'aluminium', antwoord:'p', uitleg:'Een metaal uit groep IIIa: het geeft 3 elektronen af.'},
  {tekst:'neon', antwoord:'g', uitleg:'Een edelgas heeft al een volle buitenste schil.'},
  {tekst:'zwavel', antwoord:'n', uitleg:'Groep VIa: het neemt 2 elektronen op.'}]});
sorteer($('#oef-wat'), {id:'wat', titel:'Oefening 2 · Wat gebeurt er?', items:[
  {tekst:'Een magnesiumatoom wordt een ion. Wat gebeurt er?', opties:[{k:'a',label:'het geeft 2 elektronen af'},{k:'b',label:'het neemt 2 elektronen op'},{k:'c',label:'het geeft 2 protonen af'}], antwoord:'a', uitleg:'Magnesium staat in groep IIa: 2 valentie-elektronen.'},
  {tekst:'Een fluoratoom wordt een ion. Wat gebeurt er?', opties:[{k:'a',label:'het geeft 7 elektronen af'},{k:'b',label:'het neemt 1 elektron op'},{k:'c',label:'het neemt 1 proton op'}], antwoord:'b', uitleg:'Fluor heeft 7 valentie-elektronen. Er ontbreekt er 1 voor een volle schil.'},
  {tekst:'Waarom vormen atomen ionen?', opties:[{k:'a',label:'om een edelgasconfiguratie te krijgen'},{k:'b',label:'om zwaarder te worden'},{k:'c',label:'om meer protonen te krijgen'}], antwoord:'a'},
  {tekst:'Een atoom neemt elektronen op. Welke lading krijgt het?', opties:[{k:'a',label:'positief'},{k:'b',label:'negatief'},{k:'c',label:'geen lading'}], antwoord:'b', uitleg:'Er zijn dan meer elektronen (−) dan protonen (+).'},
  {tekst:'Wat verandert er nooit als een ion ontstaat?', opties:[{k:'a',label:'het aantal elektronen'},{k:'b',label:'het aantal protonen'},{k:'c',label:'de lading'}], antwoord:'b', uitleg:'Met meer of minder protonen zou het een ander element zijn.'}]});
const SUP = {'⁺':'+','⁻':'-','²':'2','³':'3','¹':'1','−':'-'};
const ionNorm = v => { let s = v.replace(/[⁺⁻²³¹−]/g, c=>SUP[c]).replace(/\s/g,''); const m = s.match(/^([A-Z][a-z]?)(\d?)([+-])(\d?)$/); if(!m) return s; let g = m[2]||m[4]||''; if(g==='1') g=''; return m[1]+g+m[3]; };
const ionCheck = (v, it) => { const a = ionNorm(v), w = it.antwoord[0];
  if (a===w) return {ok:true};
  if (a.toLowerCase()===w.toLowerCase()) return {bijna:'Let op de hoofdletters van het symbool.'};
  return {ok:false}; };
invul($('#oef-not'), {id:'not', titel:'Oefening 3 · Schrijf de notatie', opdracht:'Typ het symbool en daarna de lading, bv. <b>Na+</b> of <b>O2-</b>.', check:ionCheck,
  items: () => shuffle(Object.keys(IONEN)).slice(0,6).map(s => ({tekst:`het ion van ${BIJZ.sym[s].naam}`, antwoord:[s+(Math.abs(IONEN[s])>1?Math.abs(IONEN[s]):'')+(IONEN[s]>0?'+':'-')], toon:ionHtml(s,IONEN[s]), uitleg:`${BIJZ.sym[s].naam[0].toUpperCase()+BIJZ.sym[s].naam.slice(1)} staat in groep ${GROEP_ROMEINS[BIJZ.sym[s].g]}.`})) });
const naamCheck = (v, it) => ({ok: norm(v).replace(/[\s-]/g,'') === it.antwoord[0].replace(/-/g,'')});
invul($('#oef-naam'), {id:'naam', titel:'Oefening 4 · Geef de naam', check:naamCheck,
  items: () => shuffle(Object.keys(IONEN)).slice(0,6).map(s => ({tekst:ionHtml(s,IONEN[s]), antwoord:[ionNaam(s)], toon:ionNaam(s), uitleg: IONEN[s]>0?'Positief ion: naam van het element + ion.':'Negatief ion: verkorte naam + ide-ion.'})) });
sorteer($('#oef-deel'), {id:'deel', titel:'Oefening 5 · Protonen en elektronen in een ion', items:[
  {tekst:'Na<sup>+</sup> (Z = 11)', opties:[{k:'a',label:'11 p en 10 e⁻'},{k:'b',label:'11 p en 12 e⁻'},{k:'c',label:'10 p en 11 e⁻'}], antwoord:'a', uitleg:'1 elektron afgegeven: 11 − 1 = 10.'},
  {tekst:'Cl<sup>−</sup> (Z = 17)', opties:[{k:'a',label:'17 p en 16 e⁻'},{k:'b',label:'17 p en 18 e⁻'},{k:'c',label:'18 p en 17 e⁻'}], antwoord:'b', uitleg:'1 elektron opgenomen: 17 + 1 = 18.'},
  {tekst:'Al<sup>3+</sup> (Z = 13)', opties:[{k:'a',label:'13 p en 10 e⁻'},{k:'b',label:'13 p en 16 e⁻'},{k:'c',label:'10 p en 13 e⁻'}], antwoord:'a', uitleg:'3 elektronen afgegeven: 13 − 3 = 10.'},
  {tekst:'O<sup>2−</sup> (Z = 8)', opties:[{k:'a',label:'8 p en 6 e⁻'},{k:'b',label:'8 p en 10 e⁻'},{k:'c',label:'10 p en 8 e⁻'}], antwoord:'b', uitleg:'2 elektronen opgenomen: 8 + 2 = 10.'}]});
ikkanFn = () => { $('#ikkan').innerHTML = `<h3>Controle hoofdstuk 4</h3><ul>
  ${regel('Ik leg uit wanneer een ion gevormd wordt.', scores.teken && scores.wat ? {juist:scores.teken.juist+scores.wat.juist, totaal:scores.teken.totaal+scores.wat.totaal, klaar:scores.teken.klaar&&scores.wat.klaar} : (scores.teken||scores.wat))}
  ${regel('Ik benoem een ion en geef de notatie weer.', scores.not && scores.naam ? {juist:scores.not.juist+scores.naam.juist, totaal:scores.not.totaal+scores.naam.totaal, klaar:scores.not.klaar&&scores.naam.klaar} : (scores.not||scores.naam))}
  ${regel('Ik bereken het aantal protonen en elektronen in een ion.', scores.deel)}</ul>`; };
updateIkKan();
'''
pagina('chemie-ionvorming.html', 'Ionvorming', 'Chemie · 3de jaar · thema 2 · hoofdstuk 4',
  'Atomen kunnen elektronen afgeven of opnemen. Dan worden ze geladen deeltjes: ionen.',
  'LPD 6C: De leerlingen gebruiken een atoommodel om de structuur van atomen en ionen te beschrijven.',
  ['De bouw van een atoom: protonen, neutronen en elektronen.', 'Het schillenmodel en de <b>valentie-elektronen</b>.', 'De <b>edelgasconfiguratie</b>: een volle buitenste schil (hoofdstuk 3).'],
  ('Lesdoelen hoofdstuk 4 · p. 77', ['Ik leg uit wanneer een ion gevormd wordt.', 'Ik benoem een ion en geef de notatie weer.']),
  [('lesA','A','Wanneer een ion?','ionbouwer'),('lesB','B','Naam en notatie',''),('lesC','C','Oefenen','alle lesdoelen')],
  body, css, js)
