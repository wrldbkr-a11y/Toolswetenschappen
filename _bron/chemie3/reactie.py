from bouw import pagina, HIER
MOL = (HIER/'mol.js').read_text()
body = r'''
  <main class="les" id="lesA" role="tabpanel">
    <section class="blok">
      <div class="blok-kop"><span class="letter">1.1</span><h2>De reactievergelijking</h2></div>
      <p>Bij een <b>chemische reactie</b> verdwijnen stoffen en ontstaan er <b>nieuwe stoffen</b>. Je schrijft dat met een <b>reactievergelijking</b>.</p>
      <div class="fig"><svg viewBox="0 0 600 190" role="img" aria-label="reactievergelijking van de vorming van water">
        <g style="font-family:var(--f-display)" font-weight="800" font-size="44">
          <text x="40" y="95">2 H<tspan font-size="26" dy="10">2</tspan><tspan dy="-10"> + O</tspan><tspan font-size="26" dy="10">2</tspan></text>
          <text x="300" y="95" fill="var(--accent)">→</text>
          <text x="380" y="95">2 H<tspan font-size="26" dy="10">2</tspan><tspan dy="-10">O</tspan></text></g>
        <path d="M40 120 H260" stroke="var(--ink)" stroke-width="2"/><text x="150" y="146" text-anchor="middle" font-size="17" font-weight="700">reagentia</text><text x="150" y="168" text-anchor="middle" font-size="14">de stoffen die reageren</text>
        <path d="M380 120 H540" stroke="var(--ink)" stroke-width="2"/><text x="460" y="146" text-anchor="middle" font-size="17" font-weight="700">reactieproducten</text><text x="460" y="168" text-anchor="middle" font-size="14">de stoffen die ontstaan</text>
        <text x="318" y="40" text-anchor="middle" font-size="14" fill="var(--accent)" font-weight="700">reactiepijl</text></svg></div>
      <div class="duo">
        <div class="kaart"><h3>Reagentia en reactieproducten</h3><p>Links van de pijl staan de <b>reagentia</b> (beginstoffen). Rechts van de pijl staan de <b>reactieproducten</b> (eindstoffen). Lees de pijl als ‘reageert tot’.</p></div>
        <div class="kaart"><h3>Aflopende reactie</h3><p>Een <b>aflopende reactie</b> verloopt in één richting, tot minstens één reagens volledig op is. Je schrijft één pijl: →.</p></div>
      </div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">1.1</span><h2>Wet van behoud van massa</h2></div>
      <div class="def"><span class="eyebrow">Wet van Lavoisier</span><p>Bij een chemische reactie is de <b>totale massa van de reagentia</b> gelijk aan de <b>totale massa van de reactieproducten</b>.</p></div>
      <p>Proef: azijn en bakpoeder reageren. Er ontstaat een gas (koolstofdioxide). Kies of de fles open of dicht is.</p>
      <div class="knoppen"><button class="knop" type="button" id="la-dicht" aria-pressed="true">fles met ballon (dicht)</button><button class="knop" type="button" id="la-open" aria-pressed="false">open fles</button><button class="knop hoofd" type="button" id="la-start">▶ Laat reageren</button></div>
      <div class="fig"><svg id="la-svg" viewBox="0 0 520 280"></svg></div>
      <p id="la-zin"></p>
      <div class="tip"><b>Rekenen met de wet</b><p>56 g ijzer reageert volledig met 32 g zwavel tot ijzersulfide. Dan ontstaat 56 g + 32 g = <b>88 g</b> ijzersulfide.</p></div>
    </section>
  </main>

  <main class="les" id="lesB" role="tabpanel" hidden>
    <section class="blok">
      <div class="blok-kop"><span class="letter">1.2</span><h2>Wet van behoud van atomen</h2></div>
      <div class="def"><span class="eyebrow">Wet van behoud van atomen</span><p>Bij een chemische reactie gaan er <b>geen atomen verloren</b> en komen er <b>geen atomen bij</b>. De atomen worden alleen <b>anders gegroepeerd</b>. Links en rechts van de pijl staan evenveel atomen van elke soort.</p></div>
      <div class="tip"><b>Uitbalanceren in 3 stappen</b><ol style="margin:4px 0 0;padding-left:22px"><li>Tel de atomen van elke soort links en rechts van de pijl.</li><li>Is het niet gelijk? Zet een <b>coëfficiënt</b> vóór een formule.</li><li>Tel opnieuw tot alles gelijk is.</li></ol><p><b>Verander nooit een index.</b> Dan maak je een andere stof: H<sub>2</sub>O is water, H<sub>2</sub>O<sub>2</sub> is waterstofperoxide.</p></div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">1.2</span><h2>Balanceer de reactie</h2></div>
      <div class="knoppen" id="bal-kies"></div>
      <div class="fig"><div class="bal" id="bal"></div></div>
      <div id="bal-fig" class="fig"></div>
      <div class="tabelwrap"><table><thead><tr><th>atoom</th><th>links</th><th>rechts</th><th></th></tr></thead><tbody id="bal-tabel"></tbody></table></div>
      <p class="fb" id="bal-zin"></p>
    </section>
  </main>

  <main class="les" id="lesC" role="tabpanel" hidden>
    <section class="blok">
      <div class="blok-kop"><span class="letter">2</span><h2>Energie bij chemische reacties</h2></div>
      <p>Bij elke chemische reactie wordt er energie uitgewisseld met de <b>omgeving</b>: warmte, licht of elektrische energie.</p>
      <div class="duo">
        <div class="def"><span class="eyebrow">2.1 · Endo-energetisch</span><p>De reactie <b>neemt energie op</b> uit de omgeving. De omgeving koelt af, of je moet energie blijven toevoegen.</p></div>
        <div class="def"><span class="eyebrow">2.2 · Exo-energetisch</span><p>De reactie <b>geeft energie af</b> aan de omgeving. De omgeving warmt op, of er komt licht of stroom vrij.</p></div>
      </div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">2</span><h2>Het energiediagram</h2></div>
      <p>Kies een reactie. Het energiediagram vergelijkt de energie van de reagentia met de energie van de reactieproducten.</p>
      <div class="knoppen" id="ed-kies"></div>
      <div class="duo"><div class="fig"><svg id="ed-svg" viewBox="0 0 420 300"></svg></div><div class="kaart" id="ed-uitleg"></div></div>
      <div class="tip"><b>Zo lees je het diagram</b><p>Liggen de <b>reactieproducten lager</b> dan de reagentia? Dan is er energie <b>afgegeven</b>: <b>exo-energetisch</b>. Liggen ze <b>hoger</b>? Dan is er energie <b>opgenomen</b>: <b>endo-energetisch</b>.</p></div>
    </section>
  </main>

  <main class="les" id="lesD" role="tabpanel" hidden>
    <section class="blok">
      <div class="oefening" id="oef-beg"></div>
      <div class="oefening" id="oef-massa"></div>
      <div class="oefening" id="oef-atoom"></div>
      <div class="oefening" id="oef-bal"></div>
      <div class="oefening" id="oef-ee"></div>
      <div class="oefening" id="oef-ed"></div>
    </section>
    <section class="ikkan" id="ikkan"></section>
  </main>
'''
css = r'''
.bal{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:center;font-family:var(--f-display);font-weight:800;font-size:1.6rem}
.bal .st{display:inline-flex;align-items:center;gap:4px;background:var(--surface-2);border-radius:12px;padding:4px 6px}
.bal .st button{width:34px;height:34px;border-radius:8px;border:2px solid var(--line);background:var(--surface);font-weight:800;font-size:1.1rem}
.bal .st .c{min-width:1.1em;text-align:center;color:var(--accent)}
.bal .op{color:var(--muted)}
.item .zin svg{width:320px;max-width:100%;height:auto;display:block;margin-top:4px}
'''
js = MOL + r'''
/* proef van Lavoisier */
let laDicht = true, laT = 0, laLoopt = false;
function tekenLa(){
  const k = Math.min(1, laT); const m0 = 412.5; const ontsnapt = laDicht ? 0 : 2.2*k; const m = m0 - ontsnapt;
  let s = `<rect x="110" y="232" width="300" height="26" rx="6" fill="#cfd8dc" stroke="var(--ink)"/><rect x="220" y="240" width="80" height="14" rx="3" fill="#10261f"/><text x="260" y="251" text-anchor="middle" font-size="12" fill="#7CFFB2" style="font-family:var(--f-mono)">${m.toFixed(1).replace('.',',')} g</text>`;
  s += `<path d="M215 232 V150 Q215 128 240 118 V92 H280 V118 Q305 128 305 150 V232 Z" fill="rgba(180,220,240,.35)" stroke="var(--ink)" stroke-width="2"/>`;
  s += `<path d="M217 230 V${200-20*k} H303 V230 Z" fill="rgba(240,230,190,.8)"/>`;
  for (let i=0;i<10*k;i++){ const x = 228+((i*37)%70), y = 220 - ((laT*90 + i*23)%110); if (y>130) s += `<circle cx="${x}" cy="${y}" r="3" fill="#fff" stroke="#9aa"/>`; }
  if (laDicht){ const r = 14 + 30*k; s += `<ellipse cx="260" cy="${90 - r*0.9}" rx="${r*0.8}" ry="${r}" fill="#e5484d" opacity=".85" stroke="var(--ink)"/><rect x="246" y="84" width="28" height="12" rx="3" fill="#e5484d" stroke="var(--ink)"/>`; }
  else for (let i=0;i<8*k;i++){ const y = 80 - ((laT*80+i*19)%60); s += `<circle cx="${250+((i*13)%22)}" cy="${y}" r="2.5" fill="none" stroke="#889"/>`; }
  s += `<text x="20" y="30" font-size="14" font-weight="700">massa vóór de reactie: ${m0.toFixed(1).replace('.',',')} g</text><text x="20" y="52" font-size="14" font-weight="700">massa nu: ${m.toFixed(1).replace('.',',')} g</text>`;
  $('#la-svg').innerHTML = s;
  $('#la-zin').innerHTML = laT<0.01 ? 'Druk op <b>Laat reageren</b>.' : laDicht ? '<b>De massa blijft gelijk.</b> Het gas blijft in de ballon. Alle reactieproducten worden mee gewogen.' : '<b>De massa lijkt te dalen.</b> Het gas ontsnapt uit de fles en wordt niet meer gewogen. Er gaat geen massa verloren: ze zit in de lucht.';
}
function laKies(d){ laDicht = d; laT = 0; $('#la-dicht').setAttribute('aria-pressed', d); $('#la-open').setAttribute('aria-pressed', !d); tekenLa(); }
$('#la-dicht').onclick = () => laKies(true); $('#la-open').onclick = () => laKies(false);
$('#la-start').onclick = () => { laT = 0; if (laLoopt) return; laLoopt = true; (function stap(){ laT += 0.012; tekenLa(); if (laT < 1.6) requestAnimationFrame(stap); else laLoopt = false; })(); };
tekenLa();

/* balanceren */
const RX = [
  {l:['H2','O2'], r:['H2O'], o:[2,1,2]}, {l:['N2','H2'], r:['NH3'], o:[1,3,2]}, {l:['H2','Cl2'], r:['HCl'], o:[1,1,2]},
  {l:['Mg','O2'], r:['MgO'], o:[2,1,2]}, {l:['Na','Cl2'], r:['NaCl'], o:[2,1,2]}, {l:['CH4','O2'], r:['CO2','H2O'], o:[1,2,1,2]}, {l:['Al','O2'], r:['Al2O3'], o:[4,3,2]}];
let rx = 0, co = [];
const atomenKant = (fs, cs) => { const t = {}; fs.forEach((f,i) => Object.entries(telAtomen(f)).forEach(([e,n]) => t[e] = (t[e]||0) + n*cs[i])); return t; };
function toonBal(){
  const R = RX[rx], alle = [...R.l, ...R.r], cl = co.slice(0, R.l.length), cr = co.slice(R.l.length);
  const st = (f,i) => `<span class="st"><button type="button" data-i="${i}" data-d="-1" aria-label="minder">−</button><span class="c">${co[i]>1?co[i]:''}</span><span>${fHtml(f)}</span><button type="button" data-i="${i}" data-d="1" aria-label="meer">+</button></span>`;
  $('#bal').innerHTML = R.l.map((f,i)=>st(f,i)).join('<span class="op">+</span>') + '<span class="op">→</span>' + R.r.map((f,i)=>st(f,i+R.l.length)).join('<span class="op">+</span>');
  $$('#bal .st button').forEach(b => b.onclick = () => { const i = +b.dataset.i; co[i] = Math.min(6, Math.max(1, co[i] + +b.dataset.d)); toonBal(); });
  const L = atomenKant(R.l, cl), Rr = atomenKant(R.r, cr); let ok = true;
  $('#bal-tabel').innerHTML = Object.keys(L).map(e => { const g = L[e]===Rr[e]; ok = ok && g; return `<tr><td><b>${e}</b></td><td>${L[e]}</td><td>${Rr[e]}</td><td>${g?'<span class="ok-t">✓ gelijk</span>':'<span class="nok-t">✗ niet gelijk</span>'}</td></tr>`; }).join('');
  let w = 0; const groep = (fs, cs) => { let o = ''; fs.forEach((f,i) => { for (let k=0;k<cs[i];k++){ o += molSvg(f, w + 34, 60, 1.05, 0); w += 72; } w += 26; }); return o; };
  let svg = groep(R.l, cl); const pijlX = w; w += 50; svg += `<path d="M${pijlX} 60 H${pijlX+34}" stroke="var(--accent)" stroke-width="4"/><path d="M${pijlX+34} 52 L${pijlX+46} 60 L${pijlX+34} 68 Z" fill="var(--accent)"/>`; svg += groep(R.r, cr);
  $('#bal-fig').innerHTML = `<svg viewBox="0 0 ${Math.max(w,300)} 120" style="max-width:${Math.min(900,Math.max(w,300)*2)}px">${svg}</svg>`;
  $('#bal-zin').innerHTML = ok ? '<b class="ok-t">Uitgebalanceerd!</b> Links en rechts staan evenveel atomen van elke soort.' : 'Pas de coëfficiënten aan met + en −.';
  $$('#bal-kies .knop').forEach((b,i) => b.setAttribute('aria-pressed', i===rx));
}
$('#bal-kies').innerHTML = RX.map((R,i) => `<button type="button" class="knop" data-i="${i}">${R.l.map(fHtml).join(' + ')} → ${R.r.map(fHtml).join(' + ')}</button>`).join('');
$$('#bal-kies .knop').forEach(b => b.onclick = () => { rx = +b.dataset.i; co = RX[rx].o.map(()=>1); toonBal(); });
co = RX[0].o.map(()=>1); toonBal();

/* energiediagram */
const ED = [
  ['verbranding van aardgas','exo','Er komt warmte en licht vrij: je kookt erop.'],
  ['fotosynthese','endo','De plant neemt lichtenergie op om glucose te maken.'],
  ['een batterij die een lamp laat branden','exo','Er komt elektrische energie vrij.'],
  ['elektrolyse van water','endo','Je moet elektrische energie blijven toevoegen.'],
  ['een coldpack','endo','De zak wordt koud: de reactie neemt warmte op uit je hand.'],
  ['een handwarmer','exo','De zak wordt warm: er komt warmte vrij.'],
  ['suiker verhitten tot koolstof en water','endo','Je moet blijven verwarmen.'],
  ['ijzer dat roest','exo','Er komt (heel langzaam) warmte vrij.']];
function diagram(soort, w=420, h=300, klein=false){
  const yb = soort==='exo' ? 110 : 200, ye = soort==='exo' ? 210 : 100, top = 60, fs = klein ? 18 : 14;
  let s = `<path d="M50 ${h-30} V20" stroke="var(--ink)" stroke-width="2"/><path d="M44 28 L50 14 L56 28 Z" fill="var(--ink)"/><path d="M50 ${h-30} H${w-20}" stroke="var(--ink)" stroke-width="2"/>`;
  s += `<text x="38" y="${h/2}" font-size="${fs}" transform="rotate(-90 38 ${h/2})" text-anchor="middle">energie</text><text x="${w-24}" y="${h-10}" font-size="${fs}" text-anchor="end">verloop van de reactie</text>`;
  s += `<path d="M70 ${yb} H150 C190 ${yb} 190 ${top} 220 ${top} C250 ${top} 250 ${ye} 290 ${ye} H${w-22}" fill="none" stroke="var(--accent)" stroke-width="4"/>`;
  s += `<path d="M300 ${yb} H${w-22}" stroke="var(--muted)" stroke-dasharray="5 5"/><path d="M${w-32} ${yb} V${ye+(ye>yb?-10:10)}" stroke="${soort==='exo'?'var(--bad)':'var(--good)'}" stroke-width="3"/><path d="M${w-39} ${ye+(ye>yb?-12:12)} L${w-32} ${ye} L${w-25} ${ye+(ye>yb?-12:12)} Z" fill="${soort==='exo'?'var(--bad)':'var(--good)'}"/>`;
  if (!klein) s += `<text x="110" y="${yb-10}" font-size="14" font-weight="700" text-anchor="middle">reagentia</text><text x="${w-90}" y="${ye+24}" font-size="14" font-weight="700" text-anchor="middle">reactieproducten</text>`;
  return s;
}
function toonED(i){
  const [n, soort, uitleg] = ED[i];
  $('#ed-svg').innerHTML = diagram(soort);
  $('#ed-uitleg').innerHTML = `<h3>${n[0].toUpperCase()+n.slice(1)}</h3><p>${uitleg}</p><p><b>${soort==='exo'?'Exo-energetisch':'Endo-energetisch'}.</b> De reactieproducten liggen <b>${soort==='exo'?'lager':'hoger'}</b> dan de reagentia: er is energie ${soort==='exo'?'afgegeven aan':'opgenomen uit'} de omgeving.</p>`;
  $$('#ed-kies .knop').forEach((b,k) => b.setAttribute('aria-pressed', k===i));
}
$('#ed-kies').innerHTML = ED.map((e,i) => `<button type="button" class="knop" data-i="${i}">${e[0]}</button>`).join('');
$$('#ed-kies .knop').forEach(b => b.onclick = () => toonED(+b.dataset.i)); toonED(0);

/* oefeningen */
sorteer($('#oef-beg'), {id:'beg', titel:'Oefening 1 · Begrippen', opdracht:'Reactie: koolstof + zuurstofgas → koolstofdioxide.', items:[
  {tekst:'koolstof', opties:[{k:'r',label:'reagens'},{k:'p',label:'reactieproduct'}], antwoord:'r', uitleg:'Het staat links van de pijl.'},
  {tekst:'koolstofdioxide', opties:[{k:'r',label:'reagens'},{k:'p',label:'reactieproduct'}], antwoord:'p', uitleg:'Het staat rechts van de pijl.'},
  {tekst:'zuurstofgas', opties:[{k:'r',label:'reagens'},{k:'p',label:'reactieproduct'}], antwoord:'r'},
  {tekst:'Wat is een aflopende reactie?', opties:[{k:'a',label:'een reactie die verloopt tot minstens één reagens op is'},{k:'b',label:'een reactie die nooit stopt'},{k:'c',label:'een reactie zonder reactieproducten'}], antwoord:'a'},
  {tekst:'Wat staat er in een reactievergelijking links van de pijl?', opties:[{k:'a',label:'de reagentia'},{k:'b',label:'de reactieproducten'},{k:'c',label:'de energie'}], antwoord:'a'}]});
invul($('#oef-massa'), {id:'massa', titel:'Oefening 2 · Wet van behoud van massa', opdracht:'Geef je antwoord in gram, zonder eenheid.', items:() => {
  const r = (a,b) => a + Math.floor(Math.random()*(b-a+1));
  const a = r(20,60), b = r(10,40), c = r(30,80), d = r(5,20), e = r(40,90), f = r(10,30);
  return [{tekst:`${a} g ijzer reageert volledig met ${b} g zwavel. Hoeveel gram ijzersulfide ontstaat er?`, antwoord:[String(a+b)], uitleg:`${a} g + ${b} g = ${a+b} g.`},
    {tekst:`Bij een analyse ontleed je ${c+d} g kwikoxide. Er ontstaat ${c} g kwik. Hoeveel gram zuurstofgas ontstaat er?`, antwoord:[String(d)], uitleg:`${c+d} g − ${c} g = ${d} g.`},
    {tekst:`${e} g magnesium verbrandt met zuurstofgas tot ${e+f} g magnesiumoxide. Hoeveel gram zuurstofgas heeft gereageerd?`, antwoord:[String(f)], uitleg:`${e+f} g − ${e} g = ${f} g.`}]; }});
sorteer($('#oef-atoom'), {id:'atoom', titel:'Oefening 3 · Behoud van atomen', items:[
  {tekst:'Wat gebeurt er met de atomen bij een chemische reactie?', opties:[{k:'a',label:'Ze worden anders gegroepeerd.'},{k:'b',label:'Er verdwijnen atomen.'},{k:'c',label:'Er ontstaan nieuwe atomen.'}], antwoord:'a'},
  {tekst:'Wat mag je veranderen om een reactievergelijking uit te balanceren?', opties:[{k:'a',label:'de coëfficiënten'},{k:'b',label:'de indexen'},{k:'c',label:'de symbolen'}], antwoord:'a', uitleg:'Als je een index verandert, krijg je een andere stof.'},
  {tekst:'Is H<sub>2</sub> + O<sub>2</sub> → H<sub>2</sub>O uitgebalanceerd?', opties:[{k:'j',label:'ja'},{k:'n',label:'nee'}], antwoord:'n', uitleg:'Links 2 O-atomen, rechts maar 1.'},
  {tekst:'Is 2 H<sub>2</sub> + O<sub>2</sub> → 2 H<sub>2</sub>O uitgebalanceerd?', opties:[{k:'j',label:'ja'},{k:'n',label:'nee'}], antwoord:'j', uitleg:'Links en rechts 4 H en 2 O.'}]});
sorteer($('#oef-bal'), {id:'bal', titel:'Oefening 4 · Kies de juiste coëfficiënten', items:[
  {tekst:'… N<sub>2</sub> + … H<sub>2</sub> → … NH<sub>3</sub>', opties:[{k:'a',label:'1, 3, 2'},{k:'b',label:'1, 1, 1'},{k:'c',label:'2, 3, 2'}], antwoord:'a', uitleg:'Links 2 N en 6 H, rechts 2 N en 6 H.'},
  {tekst:'… Mg + … O<sub>2</sub> → … MgO', opties:[{k:'a',label:'1, 1, 1'},{k:'b',label:'2, 1, 2'},{k:'c',label:'1, 2, 2'}], antwoord:'b'},
  {tekst:'… Na + … Cl<sub>2</sub> → … NaCl', opties:[{k:'a',label:'2, 1, 2'},{k:'b',label:'1, 1, 1'},{k:'c',label:'1, 2, 1'}], antwoord:'a'},
  {tekst:'… CH<sub>4</sub> + … O<sub>2</sub> → … CO<sub>2</sub> + … H<sub>2</sub>O', opties:[{k:'a',label:'1, 1, 1, 1'},{k:'b',label:'1, 2, 1, 2'},{k:'c',label:'2, 2, 1, 2'}], antwoord:'b', uitleg:'Links 1 C, 4 H, 4 O. Rechts 1 C, 4 H, 2 + 2 = 4 O.'},
  {tekst:'… H<sub>2</sub> + … Cl<sub>2</sub> → … HCl', opties:[{k:'a',label:'2, 1, 2'},{k:'b',label:'1, 1, 2'},{k:'c',label:'1, 1, 1'}], antwoord:'b'}]});
sorteer($('#oef-ee'), {id:'ee', titel:'Oefening 5 · Exo- of endo-energetisch?', opties:[{k:'exo',label:'exo-energetisch'},{k:'endo',label:'endo-energetisch'}],
  items: ED.map(([n,s,u]) => ({tekst:n, antwoord:s, uitleg:u})).concat([{tekst:'De temperatuur van de omgeving stijgt.', antwoord:'exo'},{tekst:'De reactie neemt energie op.', antwoord:'endo'}])});
sorteer($('#oef-ed'), {id:'ed', titel:'Oefening 6 · Lees het energiediagram', opties:[{k:'exo',label:'exo-energetisch'},{k:'endo',label:'endo-energetisch'}],
  items: ['exo','endo','endo','exo'].map((s,i) => ({tekst:`Is deze reactie exo- of endo-energetisch?<svg viewBox="0 0 420 300">${diagram(s)}</svg>`, antwoord:s, uitleg: s==='exo'?'De reactieproducten liggen lager: energie afgegeven.':'De reactieproducten liggen hoger: energie opgenomen.'}))});
const som = (...k) => { const a = k.map(x=>scores[x]).filter(Boolean); if(!a.length) return null; return {juist:a.reduce((t,x)=>t+x.juist,0), totaal:k.map(x=>scores[x]?scores[x].totaal:0).reduce((t,x)=>t+x,0), klaar:k.every(x=>scores[x]&&scores[x].klaar)}; };
ikkanFn = () => { $('#ikkan').innerHTML = `<h3>Controle thema 4</h3><ul>
  ${regel('Ik hanteer de begrippen reactievergelijking, aflopende reactie, reagentia en reactieproducten.', scores.beg)}
  ${regel('Ik geef de wet van behoud van massa weer en hanteer ze correct.', scores.massa)}
  ${regel('Ik geef de wet van behoud van atomen weer en hanteer ze correct.', scores.atoom)}
  ${regel('Ik kan een reactievergelijking uitbalanceren.', scores.bal)}
  ${regel('Ik onderscheid exo- en endo-energetische reacties vanuit de energie-uitwisseling.', scores.ee)}
  ${regel('Ik leid uit een energiediagram af of een reactie endo- of exo-energetisch is.', scores.ed)}</ul>`; };
updateIkKan();
'''
pagina('chemie-reactie.html', 'De chemische reactie', 'Chemie · 3de jaar · thema 4 · hoofdstuk 1 en 2',
  'Bij een chemische reactie ontstaan nieuwe stoffen. Massa en atomen blijven behouden, en er wordt energie uitgewisseld.',
  'LPD 4C: De leerlingen balanceren gegeven eenvoudige anorganische chemische reacties door gebruik te maken van de wet van behoud van massa. LPD 5C: De leerlingen interpreteren bij een chemische reactie de energie-uitwisseling met de omgeving.',
  ['Het verschil tussen een <b>chemisch</b> en een <b>fysisch</b> verschijnsel.', 'Formules lezen: <b>index</b> en <b>coëfficiënt</b> (thema 3).'],
  ('Lesdoelen thema 4 · p. 136–157', ['Ik hanteer de begrippen reactievergelijking, aflopende reactie, reagentia en reactieproducten.', 'Ik geef de wet van behoud van massa (Lavoisier) weer en hanteer ze correct.', 'Ik geef de wet van behoud van atomen weer en hanteer ze correct.', 'Ik kan een reactievergelijking uitbalanceren.', 'Ik interpreteer het onderscheid tussen exo-energetische en endo-energetische reacties vanuit gegeven energie-uitwisselingen.', 'Ik leid uit een energiediagram af of de reactie endo- of exo-energetisch is.']),
  [('lesA','1.1','Reactievergelijking en massa','wet van Lavoisier'),('lesB','1.2','Behoud van atomen','uitbalanceren'),('lesC','2','Energie','exo en endo'),('lesD','✎','Oefenen','alle lesdoelen')],
  body, css, js)
