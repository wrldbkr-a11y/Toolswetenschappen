import sys, base64, pathlib
HIER = pathlib.Path(__file__).parent
sys.path.insert(0, str(HIER.parent / 'chemie3'))
from bouw import pagina
ORG = (HIER/'organisch.js').read_text()
img = lambda n: 'data:image/jpeg;base64,' + base64.b64encode((HIER/'img'/n).read_bytes()).decode()
body = r'''
  <main class="les" id="lesA" role="tabpanel">
    <section class="blok">
      <div class="blok-kop"><span class="letter">3.1</span><h2>Excretie of secretie</h2></div>
      <p>Je lichaam scheidt veel stoffen af. Er zijn twee soorten.</p>
      <div class="duo">
        <div class="def"><span class="eyebrow">Excretie</span><p>Het lichaam verwijdert <b>afvalstoffen</b> die het niet meer kan gebruiken. Voorbeelden: <b>urine</b> via de nieren, <b>koolstofdioxide</b> via de longen.</p></div>
        <div class="def"><span class="eyebrow">Secretie</span><p><b>Kliercellen</b> maken stoffen <b>met een functie</b> en geven die af. Voorbeelden: <b>speeksel</b>, <b>traanvocht</b>, <b>hormonen</b>.</p></div>
      </div>
      <div class="def"><span class="eyebrow">Definitie</span><p>Een <b>klier</b> is een orgaan of een groep cellen die stoffen maakt en afgeeft. Die stof heet een <b>klierafscheiding</b> of <b>secreet</b>.</p></div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">3.2</span><h2>Soorten klieren</h2></div>
      <p>Zo ziet klierweefsel eruit onder de microscoop. Kijk waar de klierafscheiding naartoe gaat.</p>
      <div class="fig"><svg id="kt-svg" viewBox="0 0 920 480" role="img" aria-label="exocriene klier met afvoerbuis en endocriene klier die hormonen afgeeft aan het bloed"></svg></div>
      <div class="duo">
        <div class="def"><span class="eyebrow">Exocriene klier</span><p>Heeft een <b>afvoerbuis</b>. De klierafscheiding gaat via de afvoerbuis naar <b>buiten het lichaam</b> (huid) of naar een <b>holte</b> (mond, darm).</p></div>
        <div class="def"><span class="eyebrow">Endocriene klier (hormoonklier)</span><p>Heeft <b>geen afvoerbuis</b>. De klier geeft <b>hormonen</b> af aan het <b>bloed</b>. Het bloed brengt ze naar de doelorganen.</p></div>
      </div>
    </section>
  </main>

  <main class="les" id="lesB" role="tabpanel" hidden>
    <section class="blok">
      <div class="blok-kop"><span class="letter">3.3</span><h2>De zweetklieren in je huid</h2></div>
      <p>Een zweetklier is een opgerolde buis diep in de lederhuid. Een lange <b>afvoerbuis</b> brengt het zweet naar een <b>zweetporie</b> op je huid.</p>
      <div class="fig"><svg id="huid-svg" viewBox="0 0 640 500" role="img" aria-label="doorsnede van de huid met een zweetklier en een talgklier"></svg></div>
      <p>Het zweet verdampt op je huid. Daarvoor is warmte nodig, die uit je huid komt. Zo <b>koel je af</b>.</p>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">3.3</span><h2>De speekselklieren</h2></div>
      <p>Je hebt drie paar grote speekselklieren. Hun afvoerbuizen monden uit in je mondholte.</p>
      <div class="fig"><svg viewBox="0 0 1500 1420" role="img" aria-label="hoofd met de drie speekselklieren">
        <image href="__SPEEKSEL__" x="0" y="0" width="1500" height="1500"/>
        <g font-size="46" font-weight="700" text-anchor="middle">
          <rect x="140" y="458" width="500" height="80" rx="16" fill="#fff" opacity=".92"/><text x="390" y="512">oorspeekselklier</text>
          <rect x="10" y="1020" width="620" height="80" rx="16" fill="#fff" opacity=".92"/><text x="320" y="1074">onderkaakspeekselklier</text>
          <rect x="910" y="1286" width="580" height="80" rx="16" fill="#fff" opacity=".92"/><text x="1200" y="1340">ondertongspeekselklier</text></g></svg></div>
      <div class="tabelwrap"><table><thead><tr><th>exocriene klier</th><th>klierafscheiding</th><th>functie</th></tr></thead><tbody>
        <tr><td><b>speekselklier</b></td><td>speeksel</td><td>maakt voedsel nat en glad, en begint met de vertering van zetmeel</td></tr>
        <tr><td><b>zweetklier</b></td><td>zweet</td><td>koelt het lichaam af als het zweet verdampt</td></tr>
        <tr><td><b>traanklier</b></td><td>traanvocht</td><td>houdt het oog vochtig en spoelt vuil weg</td></tr>
        <tr><td><b>talgklier</b></td><td>talg (huidvet)</td><td>houdt huid en haar soepel</td></tr>
        <tr><td><b>melkklier</b></td><td>moedermelk</td><td>voeding voor een baby</td></tr></tbody></table></div>
    </section>
  </main>

  <main class="les" id="lesC" role="tabpanel" hidden>
    <section class="blok">
      <div class="blok-kop"><span class="letter">3.4</span><h2>De hormoonklieren</h2></div>
      <p>Hormoonklieren liggen verspreid over het hele lichaam. Klik op een naam.</p>
      <div class="duo hk">
        <div class="fig"><svg id="hk-svg" viewBox="0 0 262.54 258.57" role="img" aria-label="hormoonklieren bij een vrouw en een man">
          <image href="__HORMOON__" x="0" y="0" width="262.54" height="258.57"/><g id="hk-labels"></g></svg></div>
        <div class="kaart" id="hk-info"></div>
      </div>
      <div class="tip"><b>Hormoon</b><p>Een <b>hormoon</b> is een stof die een endocriene klier aan het bloed afgeeft. Het werkt alleen op bepaalde <b>doelorganen</b>. Al is er heel weinig van, toch heeft het een groot effect.</p></div>
    </section>
  </main>

  <main class="les" id="lesD" role="tabpanel" hidden>
    <section class="blok">
      <div class="blok-kop"><span class="letter">4</span><h2>Ook dieren reageren met hormonen</h2></div>
      <div class="fig"><svg id="kikker-svg" viewBox="0 0 900 260" role="img" aria-label="van kikkervisje tot kikker"></svg></div>
      <p>Een kikkervisje leeft in het water, ademt met kieuwen en heeft een staart. Als zijn <b>schildklier</b> het hormoon <b>thyroxine</b> afgeeft, verandert het lichaam: er groeien poten, de staart verdwijnt en er komen longen. Die verandering heet <b>metamorfose</b>. Zonder thyroxine blijft het een kikkervisje.</p>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">4</span><h2>Ook planten maken hormonen</h2></div>
      <p>Planten hebben geen klieren, maar hun cellen maken wel <b>plantenhormonen</b>. Een rijpe banaan geeft het gas <b>ethyleen</b> af. Dat is een rijpingshormoon: het laat vruchten in de buurt sneller rijpen.</p>
      <div class="knoppen"><button type="button" class="knop" id="ban-met" aria-pressed="true">groene bananen + rijpe banaan in een zak</button><button type="button" class="knop" id="ban-zonder" aria-pressed="false">groene bananen alleen</button></div>
      <div class="knoppen"><label>dagen: <input type="range" id="ban-dag" min="0" max="6" value="0"></label><b id="ban-dagtxt">dag 0</b></div>
      <div class="fig"><svg id="ban-svg" viewBox="0 0 700 280" role="img" aria-label="rijping van bananen"></svg></div>
      <p id="ban-zin"></p>
    </section>
  </main>

  <main class="les" id="lesE" role="tabpanel" hidden>
    <section class="blok">
      <div class="oefening" id="oef-es"></div>
      <div class="oefening" id="oef-type"></div>
      <div class="oefening" id="oef-exo"></div>
      <div class="oefening" id="oef-endo"></div>
      <div class="oefening" id="oef-ander"></div>
    </section>
    <section class="ikkan" id="ikkan"></section>
    <p class="credit">Afbeeldingen: speekselklieren naar <i>Blausen 0780 SalivaryGlands</i>, BruceBlaus, CC BY 3.0 (Engelse namen vervangen). Hormoonklieren naar <i>Endocrine English</i>, OpenStax &amp; Tomáš Kebert &amp; umimeto.org, CC BY-SA 4.0 (Engelse namen vervangen). Beide via Wikimedia Commons. De andere tekeningen zijn eigen werk.</p>
  </main>
'''
css = r'''
.fig svg{max-width:900px}
#hk-svg text{cursor:pointer}
#hk-svg .lab rect{fill:#fff;stroke:var(--line);stroke-width:.4}
#hk-svg .lab[aria-pressed="true"] rect{fill:var(--accent)}
#hk-svg .lab[aria-pressed="true"] text{fill:#fff}
#hk-svg .lab:focus-visible rect{stroke:var(--ink);stroke-width:1}
.hk{grid-template-columns:3fr 2fr}
@media (max-width:760px){.hk{grid-template-columns:1fr}}
'''
js = ORG + r'''
/* ---------- 3.2 exocriene en endocriene klier ---------- */
(function(){
  const S = $('#kt-svg'), R = rng(7); let st = '';
  const lab = (x, y, tx, ty, t, anchor='start') => `<path d="M${x} ${y} L${tx} ${ty}" stroke="#1d2a36" stroke-width="1.3"/><circle cx="${x}" cy="${y}" r="2.4" fill="#1d2a36"/><text x="${tx + (anchor==='start'?4:anchor==='end'?-4:0)}" y="${ty+5}" font-size="15" font-weight="700" text-anchor="${anchor}" paint-order="stroke" stroke="#fff" stroke-width="4">${t}</text>`;
  st += `<clipPath id="kt-l"><rect x="10" y="10" width="430" height="460" rx="18"/></clipPath><clipPath id="kt-r"><rect x="480" y="10" width="430" height="460" rx="18"/></clipPath>`;
  // weefsel
  st += `<g clip-path="url(#kt-l)"><rect x="10" y="10" width="430" height="460" fill="url(#o-lederhuid)" filter="url(#o-textuur)"/>${vezels(10,110,430,360,R,34)}<rect x="10" y="10" width="430" height="60" fill="#e8f3f8"/></g>`;
  st += `<g clip-path="url(#kt-r)"><rect x="480" y="10" width="430" height="460" fill="url(#o-lederhuid)" filter="url(#o-textuur)"/>${vezels(480,10,430,460,R,40)}</g>`;
  // dekweefsel bovenaan (links)
  let ep = '';
  for (let x = 22; x < 440; x += 25){ if (x > 196 && x < 252) continue; ep += cel(x, 92 + Math.sin(x/40)*3, 12.5, 23, R, {kdy:9, kf:.38}); }
  // afvoerbuis: middellijn van opening naar de klierblaasjes
  const as = bemonster(glad([[224,66],[219,120],[232,180],[222,240],[228,268]], false), 40);
  const takken = [[[228,268],[200,300],[168,330]], [[228,268],[232,320],[236,362]], [[228,268],[262,298],[300,326]]].map(p => bemonster(glad(p,false),14));
  let buis = '';
  const lijnBuis = pts => `<path d="${glad(pts,false)}" fill="none" stroke="#c47a8e" stroke-width="34" stroke-linecap="round"/><path d="${glad(pts,false)}" fill="none" stroke="#f3c6d1" stroke-width="31" stroke-linecap="round"/>`;
  buis += lijnBuis(as); takken.forEach(t => buis += lijnBuis(t));
  const wandcellen = (pts, step=2) => { let o=''; for (let i = 1; i < pts.length-1; i += step){ const [x0,y0] = pts[i-1], [x1,y1] = pts[i+1]; const a = Math.atan2(y1-y0, x1-x0), nx = -Math.sin(a), ny = Math.cos(a); [-1,1].forEach(z => o += cel(pts[i][0] + nx*z*11.5, pts[i][1] + ny*z*11.5, 6.5, 8.5, R, {kf:.45, rot:a})); } return o; };
  buis += wandcellen(as, 2); takken.forEach(t => buis += wandcellen(t, 2));
  [as, ...takken].forEach(p => buis += `<path d="${glad(p,false)}" fill="none" stroke="#fff3d9" stroke-width="7" stroke-linecap="round"/>`);
  // klierblaasjes (druiventrosjes van kliercellen rond een kleine holte)
  const acini = [[168,342],[236,380],[302,338],[120,300],[350,294]];
  let ac = '';
  acini.forEach(([cx,cy],k) => { const n = 9, rO = 44 + R()*6;
    ac += `<path d="${blob(cx,cy,rO+5,rO+3,R,12,.06)}" fill="#d98fa6" opacity=".9"/>`;
    for (let i = 0; i < n; i++){ const a0 = i/n*Math.PI*2 + k, a1 = (i+1)/n*Math.PI*2 + k, am = (a0+a1)/2, ri = 9, ro = rO*(0.94+R()*.1);
      const pts = [[cx+Math.cos(a0+.03)*ri, cy+Math.sin(a0+.03)*ri],[cx+Math.cos(a0+.02)*ro*.6, cy+Math.sin(a0+.02)*ro*.6],[cx+Math.cos(a0+.05)*ro, cy+Math.sin(a0+.05)*ro],[cx+Math.cos(am)*ro*1.03, cy+Math.sin(am)*ro*1.03],[cx+Math.cos(a1-.05)*ro, cy+Math.sin(a1-.05)*ro],[cx+Math.cos(a1-.02)*ro*.6, cy+Math.sin(a1-.02)*ro*.6],[cx+Math.cos(a1-.03)*ri, cy+Math.sin(a1-.03)*ri]];
      ac += `<path d="${glad(pts)}" fill="url(#o-celklier)" stroke="#b9708f" stroke-width=".9"/>`;
      const kx = cx+Math.cos(am)*ro*.72, ky = cy+Math.sin(am)*ro*.72; ac += `<path d="${blob(kx,ky,6,5,R,8,.12,am)}" fill="url(#o-kern)"/>`;
      for (let g = 0; g < 3; g++){ const rr = ri + 4 + R()*10, aa = a0 + (a1-a0)*(.25+R()*.5); ac += `<circle cx="${(cx+Math.cos(aa)*rr).toFixed(1)}" cy="${(cy+Math.sin(aa)*rr).toFixed(1)}" r="1.8" fill="url(#o-secreet)"/>`; } }
    ac += `<path d="${blob(cx,cy,8,8,R,7,.15)}" fill="#fff3d9"/>`; });
  st += `<g clip-path="url(#kt-l)">${ac}${buis}${ep}</g>`;
  // haarvaten en kliercellen (rechts)
  const cap1 = bemonster(glad([[470,96],[560,80],[640,122],[720,96],[810,134],[920,104]], false), 90);
  const cap2 = bemonster(glad([[470,400],[560,368],[660,414],[760,376],[850,416],[920,392]], false), 90);
  const cap3 = bemonster(glad([[470,262],[540,236],[610,280],[700,300],[790,250],[860,282],[920,262]], false), 90);
  const caps = [cap1, cap2, cap3];
  const capWand = pts => { let o = `<path d="${glad(pts,false)}" fill="none" stroke="#a83838" stroke-width="38" stroke-linecap="round"/><path d="${glad(pts,false)}" fill="none" stroke="#fbe2d8" stroke-width="31" stroke-linecap="round"/>`;
    for (let i = 4; i < pts.length-2; i += 9){ const [x0,y0] = pts[i-1], [x1,y1] = pts[i+1]; const a = Math.atan2(y1-y0,x1-x0); const z = i%18<9?1:-1; o += `<path d="${blob(pts[i][0]-Math.sin(a)*z*16.5, pts[i][1]+Math.cos(a)*z*16.5, 8, 2.6, R, 8, .1, a)}" fill="url(#o-kern)"/>`; } return o; };
  const afst = (x,y) => Math.min(...caps.map(c => Math.min(...c.map(p => Math.hypot(p[0]-x, p[1]-y)))));
  let kc = '';
  for (let gy = 26; gy < 470; gy += 24) for (let gx = 486 + ((gy/24)%2)*12; gx < 915; gx += 25){ const x = gx + (R()-.5)*10, y = gy + (R()-.5)*10; if (afst(x,y) < 33) continue; kc += cel(x, y, 12 + R()*3, 10.5 + R()*3, R, {vul:'url(#o-celklier)', rot:R()*3, kf:.42}); }
  st += `<g clip-path="url(#kt-r)">${kc}${caps.map(capWand).join('')}</g>`;
  // labels
  st += lab(110, 92, 60, 40, 'dekweefsel') + lab(224, 60, 285, 36, 'opening naar buiten') + lab(214, 170, 92, 170, 'afvoerbuis', 'end') + lab(330, 350, 385, 430, 'kliercellen', 'middle');
  st += lab(640, 190, 640, 452, 'kliercellen', 'middle') + lab(612, 278, 540, 330, 'bloedvat', 'middle') + lab(790, 252, 902, 46, 'hormonen naar het bloed', 'end');
  st += `<text x="225" y="30" text-anchor="middle" font-size="19" font-weight="800">exocriene klier</text>`;
  st += `<rect x="488" y="10" width="200" height="32" rx="9" fill="#fff" opacity=".9"/><text x="588" y="32" text-anchor="middle" font-size="19" font-weight="800">endocriene klier</text>`;
  S.innerHTML = st + '<g id="kt-dyn"></g>';
  // animatie: secreet door de buis, hormonen naar het bloed, rode bloedcellen stromen
  const opw = [...as].reverse().concat([[224,40],[226,14]]);
  const dr = []; for (let i = 0; i < 16; i++) dr.push({t:i/16, k:i%3});
  const hm = []; for (let i = 0; i < 18; i++) hm.push({x:600, y:200, s:1 + R()});
  const rb = []; for (let i = 0; i < 33; i++) rb.push({t:R(), c:i%3});
  let t0 = 0;
  (function lus(ts){ requestAnimationFrame(lus); if (!zichtbaar(S)) return; const dt = ts && t0 ? Math.min(50, ts - t0) / 1000 : 0; t0 = ts || 0; let o = '';
    dr.forEach(d => { d.t += dt*.07; if (d.t > 1) d.t -= 1; const tak = [...takken[d.k]].reverse(); const L1 = .3; let p;
      if (d.t < L1) p = langs(tak, d.t/L1); else p = langs(opw, (d.t-L1)/(1-L1)); o += `<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="3.6" fill="url(#o-secreet)" stroke="#a87410" stroke-width=".6"/>`; });
    o += '<g clip-path="url(#kt-r)">'; rb.forEach(b => { b.t += dt*.05; if (b.t > 1) b.t -= 1; const p = langs(caps[b.c], b.t); o += rbc(p[0], p[1] + Math.sin(b.t*40)*5, 8, p[2]); });
    hm.forEach(h => { h.s += dt*.3; if (h.s > 1){ h.s = 0; do { h.x = 500 + R()*400; h.y = 30 + R()*420; } while (afst(h.x,h.y) < 33); }
      if (h.cap == null || h.s === 0) h.cap = caps.reduce((b,c,i) => { const d = Math.min(...c.map(p=>Math.hypot(p[0]-h.x,p[1]-h.y))); return d < b[0] ? [d,i] : b; }, [1e9,0])[1];
      const c = caps[h.cap], tq = Math.max(0, Math.min(1, (h.x-470)/450)); const vt = Math.min(1, tq + Math.max(0, h.s-.55)*.5); const q = langs(c, vt); const f = Math.min(1, h.s*1.8); const x = h.x + (q[0]-h.x)*f, y = h.y + (q[1]-h.y)*f;
      o += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4" fill="url(#o-hormoon)" stroke="#145c37" stroke-width=".5"/>`; });
    $('#kt-dyn').innerHTML = o + '</g>'; })();
})();

/* ---------- 3.3 huid met zweetklier ---------- */
(function(){
  const S = $('#huid-svg'), R = rng(21); let s = '';
  const W = 640, opp = x => 46 + Math.sin(x/37)*2.5 + Math.sin(x/11)*1, grens = x => 108 + Math.sin(x/26)*13 + Math.sin(x/9)*3;
  const lijn = f => { const p = []; for (let x = 0; x <= W; x += 8) p.push([x, f(x)]); return p; };
  s += `<rect width="${W}" height="500" fill="#eef5f9"/>`;
  // onderhuids bindweefsel met vetcellen
  s += `<rect x="0" y="330" width="${W}" height="170" fill="#f0d9b5"/>`;
  for (let y = 345; y < 510; y += 30) for (let x = -10 + (y/30%2)*16; x < W+20; x += 33) s += `<path d="${blob(x + (R()-.5)*8, y + (R()-.5)*6, 17, 14, R, 9, .13)}" fill="url(#o-vet)" stroke="#c9a14e" stroke-width="1"/>`;
  // lederhuid
  const lh = lijn(grens); s += `<path d="M0 352 ${lh.map(p=>`L${p[0]} ${p[1].toFixed(1)}`).join(' ')} L${W} 352 Q${W*.75} 338 ${W/2} 350 T0 352 Z" fill="url(#o-lederhuid)" filter="url(#o-textuur)"/>`;
  s += vezels(0, 130, W, 210, R, 50, '#e09aa8', .5);
  // bloedvaatjes in de lederhuid
  const vat = (pts, kl) => `<path d="${glad(pts,false)}" fill="none" stroke="${kl}" stroke-width="5" stroke-linecap="round" opacity=".85"/><path d="${glad(pts,false)}" fill="none" stroke="#fff" stroke-width="1.2" stroke-linecap="round" opacity=".35"/>`;
  s += vat([[0,300],[90,290],[180,305],[300,286],[420,300],[540,288],[640,296]], '#c0392b') + vat([[0,312],[100,304],[200,318],[320,300],[440,314],[560,302],[640,310]], '#3d5a9e');
  for (let x = 30; x < W; x += 104 + R()*30){ if (x > 120 && x < 240) continue; const top = grens(x+16) + 6 + R()*8, w = 10 + R()*8;
    const pts = [[x, 298], [x - 8 + R()*10, 250], [x + 4 + R()*8, 200 + R()*20], [x + (R()-.5)*10, top + 30], [x + w*.3, top + 4], [x + w, top], [x + w*1.6, top + 8], [x + w*1.4 + (R()-.5)*8, top + 40], [x + w + 8 + R()*8, 220], [x + w + R()*10, 260], [x + w + 14, 308]];
    s += vat(pts.slice(0,6), '#c0392b') + vat(pts.slice(5), '#4a5fa3');
    const tak = [[x + 2, 240], [x - 18 - R()*10, 216], [x - 26 - R()*10, 190]]; s += vat(tak, '#c0392b'); }
  // opperhuid
  const op = lijn(opp); s += `<path d="M${op.map(p=>`${p[0]} ${p[1].toFixed(1)}`).join(' L')} L${W} ${grens(W)} ${[...lh].reverse().map(p=>`L${p[0]} ${p[1].toFixed(1)}`).join(' ')} Z" fill="url(#o-opperhuid)"/>`;
  s += `<path d="M${op.map(p=>`${p[0]} ${p[1].toFixed(1)}`).join(' L')}" fill="none" stroke="#c99377" stroke-width="2"/>`;
  for (let i = 0; i < 4; i++) s += `<path d="M${op.map(p=>`${p[0]} ${(p[1]+3+i*3).toFixed(1)}`).join(' L')}" fill="none" stroke="#f2dcc8" stroke-width=".9" stroke-dasharray="${18+i*7} ${6+i*3}" opacity=".9"/>`;
  for (let x = 4; x < W; x += 9){ const y = grens(x) - 5; s += `<ellipse cx="${x}" cy="${y.toFixed(1)}" rx="2.6" ry="3.6" fill="#6d4a8c" opacity=".65"/>`; }
  for (let i = 0; i < 160; i++){ const x = R()*W, y = opp(x) + 14 + R()*(grens(x)-opp(x)-24); s += `<ellipse cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" rx="2.2" ry="1.6" fill="#7b5a92" opacity=".35"/>`; }
  // haarzakje met talgklier
  const fol = bemonster(glad([[138,428],[150,340],[168,240],[186,140],[198,56]], false), 30);
  s += `<path d="${glad(fol,false)}" fill="none" stroke="#c9826f" stroke-width="40" stroke-linecap="round"/><path d="${glad(fol,false)}" fill="none" stroke="#e9b29f" stroke-width="33" stroke-linecap="round"/>`;
  s += `<path d="${blob(140,436,26,22,R,10,.08)}" fill="#a8604e"/><path d="${blob(141,428,13,11,R,8,.1)}" fill="#f0c8b4"/>`;
  [[212,214,22,15],[226,236,17,13],[214,240,16,12]].forEach(([x,y,a,b]) => s += `<path d="${blob(x,y,a,b,R,10,.12)}" fill="#f6e7b3" stroke="#d1b366" stroke-width="1.2"/>` + `<circle cx="${x-4}" cy="${y-3}" r="4" fill="#fff8de" opacity=".8"/>`);
  s += `<path d="${glad([[140,430],[152,340],[170,240],[188,140],[200,52],[208,10],[222,-30]], false)}" fill="none" stroke="#4a2c1d" stroke-width="9" stroke-linecap="round"/><path d="${glad([[141,430],[153,340],[171,240],[189,140],[201,52],[209,10],[223,-30]], false)}" fill="none" stroke="#8a5a3c" stroke-width="2.4" stroke-linecap="round" opacity=".7"/>`;
  // zweetklier: opgerold kluwen
  const kl = []; for (let t = 0; t <= Math.PI*7; t += .12){ kl.push([430 + Math.cos(t*1.0)*(30+6*Math.sin(t*1.7)) + Math.sin(t*.45)*14, 300 + Math.sin(t)*(16+4*Math.cos(t*2.3)) + (t-11)*1.3]); }
  const afv = bemonster(glad([kl[kl.length-1], [440,250], [432,200], [446,150], [438,118]], false), 30);
  const spir = []; for (let y = 118; y >= opp(440)+2; y -= 3){ spir.push([440 + Math.sin(y/5)*7, y]); }
  const zweetpad = [...kl.slice(Math.floor(kl.length*.6)), ...afv, ...spir];
  const buis = (pts, w) => `<path d="${glad(pts,false)}" fill="none" stroke="#a4566c" stroke-width="${w+4}" stroke-linecap="round" stroke-linejoin="round"/><path d="${glad(pts,false)}" fill="none" stroke="#e8a2b5" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/><path d="${glad(pts,false)}" fill="none" stroke="#fbe4ea" stroke-width="${w*.28}" stroke-linecap="round" opacity=".9"/>`;
  s += `<g filter="url(#o-schaduw)"><path d="${glad(kl,false)}" fill="none" stroke="#9c4d63" stroke-width="17" stroke-linecap="round" stroke-linejoin="round"/><path d="${glad(kl,false)}" fill="none" stroke="#e39aae" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/><path d="${glad(kl,false)}" fill="none" stroke="#f6c9d5" stroke-width="4" stroke-linecap="round" opacity=".55"/></g>` + buis(afv, 8) + buis(spir, 6);
  s += `<path d="M430 ${opp(440)-1} Q440 ${opp(440)+7} 450 ${opp(440)-1}" fill="#cfe6f2" stroke="#c99377" stroke-width="1.5"/>`;
  // labels
  const lab = (x, y, tx, ty, t, a='start') => `<path d="M${x} ${y} L${tx} ${ty}" stroke="#1d2a36" stroke-width="1.3"/><circle cx="${x}" cy="${y}" r="2.6" fill="#1d2a36"/><text x="${tx+(a==='start'?5:-5)}" y="${ty+5}" font-size="15" font-weight="700" text-anchor="${a}" paint-order="stroke" stroke="#fff" stroke-width="4">${t}</text>`;
  s += lab(600, 70, 600, 70, '') + `<text x="632" y="80" text-anchor="end" font-size="15" font-weight="700" paint-order="stroke" stroke="#fff" stroke-width="4">opperhuid</text><text x="632" y="230" text-anchor="end" font-size="15" font-weight="700" paint-order="stroke" stroke="#fff" stroke-width="4">lederhuid</text><text x="632" y="480" text-anchor="end" font-size="15" font-weight="700" paint-order="stroke" stroke="#fff" stroke-width="4">onderhuids bindweefsel</text>`;
  s += lab(455, 315, 520, 380, 'zweetklier') + lab(446, 190, 520, 190, 'afvoerbuis') + lab(441, 46, 500, 18, 'zweetporie') + lab(196, 40, 258, 18, 'haar') + lab(232, 230, 300, 250, 'talgklier') + lab(100, 296, 40, 210, 'bloedvaatje', 'start');
  S.innerHTML = s + '<g id="huid-dyn"></g>';
  const dr = []; for (let i = 0; i < 9; i++) dr.push(i/9); let t0 = 0, druppel = 0;
  (function lus(ts){ requestAnimationFrame(lus); if (!zichtbaar(S)) return; const dt = ts && t0 ? Math.min(50, ts - t0) / 1000 : 0; t0 = ts || 0; let o = '';
    for (let i = 0; i < dr.length; i++){ dr[i] += dt*.08; if (dr[i] > 1){ dr[i] -= 1; druppel = Math.min(1, druppel + .18); } const p = langs(zweetpad, dr[i]); o += `<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="3" fill="url(#o-druppel)" stroke="#2b6f99" stroke-width=".5"/>`; }
    druppel = Math.max(0, druppel - dt*.04); const r = 3 + druppel*9; const y0 = opp(440);
    o += `<path d="M${440-r} ${y0} C${440-r} ${y0-r*1.2} ${440-r*.2} ${y0-r*1.9} 440 ${y0-r*2.1} C${440+r*.2} ${y0-r*1.9} ${440+r} ${y0-r*1.2} ${440+r} ${y0} Z" fill="url(#o-druppel)" opacity=".9"/>`;
    $('#huid-dyn').innerHTML = o; })();
})();

/* ---------- 3.4 hormoonklieren ---------- */
const HK = [
  ['pijnappelklier', [46.4,8.4,95.1,18.9], 'melatonine', 'regelt je slaap-waakritme: je wordt ’s avonds slaperig.'],
  ['hypofyse', [155.6,17.4,211.8,27.8], 'groeihormoon en hormonen die andere hormoonklieren aansturen', 'Ze ligt onder de hersenen en is de ‘baas’ van veel andere hormoonklieren.'],
  ['bijschildklieren', [104,63.3,173.8,73.8], 'parathormoon', 'regelt de hoeveelheid calcium in je bloed en je botten.'],
  ['schildklier', [116.8,128.2,143.9,147.5], 'thyroxine', 'regelt hoe snel je stofwisseling werkt en helpt bij de groei.'],
  ['bijnier', [115.3,156,145.4,175.3], 'adrenaline', 'maakt je lichaam snel klaar voor actie bij schrik of stress: je hart klopt sneller, je ademt sneller.'],
  ['alvleesklier', [111.8,178.5,148.9,189], 'insuline en glucagon', 'regelt de hoeveelheid suiker in je bloed. De alvleesklier is ook een exocriene klier: ze maakt alvleessap voor de vertering in de darm.'],
  ['eierstok', [119.3,203.6,141.6,214], 'oestrogeen en progesteron', 'zorgt voor de vrouwelijke geslachtskenmerken en regelt de menstruatiecyclus.'],
  ['teelbal', [119.8,228.3,140.9,238.5], 'testosteron', 'zorgt voor de mannelijke geslachtskenmerken en de vorming van zaadcellen.']];
function toonHK(i){
  $$('#hk-labels .lab').forEach((g,k) => g.setAttribute('aria-pressed', k===i));
  const [n,,h,f] = HK[i]; $('#hk-info').innerHTML = `<h3>${n[0].toUpperCase()+n.slice(1)}</h3><p><b>Hormoon:</b> ${h}</p><p><b>Functie:</b> ${f}</p>`;
}
$('#hk-labels').innerHTML = HK.map(([n,[x0,y0,x1,y1]],i) => { const cx = (x0+x1)/2, w = Math.max(40, n.length*4.1+6); return `<g class="lab" role="button" tabindex="0" aria-pressed="false" data-i="${i}"><rect x="${cx-w/2}" y="${(y0+y1)/2-5.5}" width="${w}" height="11" rx="2.5"/><text x="${cx}" y="${(y0+y1)/2+2.6}" font-size="7.4" font-weight="700" text-anchor="middle">${n}</text></g>`; }).join('');
$$('#hk-labels .lab').forEach(g => { g.onclick = () => toonHK(+g.dataset.i); g.onkeydown = e => { if (e.key==='Enter'||e.key===' '){ e.preventDefault(); toonHK(+g.dataset.i); } }; });
toonHK(3);

/* ---------- 4 kikker: metamorfose ---------- */
(function(){
  const S = $('#kikker-svg'), R = rng(5);
  let s = `<defs><linearGradient id="kk-water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bcd9d6"/><stop offset="1" stop-color="#8fb9b3"/></linearGradient>
    <linearGradient id="kk-lijf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7f9b3e"/><stop offset=".6" stop-color="#5b7a2a"/><stop offset="1" stop-color="#46601f"/></linearGradient>
    <linearGradient id="kk-vis" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b6038"/><stop offset=".7" stop-color="#4a4226"/><stop offset="1" stop-color="#3a341e"/></linearGradient>
    <radialGradient id="kk-oog" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#f6dc7a"/><stop offset=".7" stop-color="#c7962a"/><stop offset="1" stop-color="#7d5a14"/></radialGradient></defs>`;
  s += `<rect width="900" height="260" rx="16" fill="#eef4ef"/><path d="M0 118 C150 112 300 124 450 116 S750 110 900 118 V260 H0Z" fill="url(#kk-water)"/>`;
  for (let i = 0; i < 14; i++){ const x = R()*900; s += `<path d="M${x.toFixed(0)} 262 C${(x-8).toFixed(0)} 220 ${(x+10).toFixed(0)} 190 ${(x+2).toFixed(0)} ${(130+R()*50).toFixed(0)}" stroke="#6f9a63" stroke-width="${(2+R()*2).toFixed(1)}" fill="none" opacity=".55"/>`; }
  s += `<path d="M560 120 C600 104 700 102 760 118 C700 126 620 128 560 120Z" fill="#7d9a52" opacity=".7"/>`;
  const spikkels = (Q, x0, y0, w, h, n, k='#2f3a14', op=.5) => { let o=''; for (let i=0;i<n;i++) o += `<path d="${blob(x0+Q()*w, y0+Q()*h, 1.4+Q()*3, 1.2+Q()*2.2, Q, 7, .2)}" fill="${k}" opacity="${op}"/>`; return o; };
  const visje = (x, y, sc, poten, seed) => { const Q = rng(seed); let o = `<g transform="translate(${x} ${y}) scale(${sc})">`;
    o += `<path d="${glad([[14,-3],[40,-16],[72,-14],[100,-4],[72,2],[40,4],[14,4]])}" fill="#8d8a62" opacity=".35"/><path d="${glad([[14,4],[40,13],[72,10],[100,-2],[72,4],[40,6]])}" fill="#8d8a62" opacity=".3"/>`;
    o += `<path d="${glad([[10,-5],[40,-5],[70,-3],[98,-3],[70,1],[40,4],[10,5]])}" fill="#5c5434" opacity=".85"/>`;
    if (poten) o += `<path d="M22 6 C30 14 30 22 22 30" stroke="#4d4529" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M22 30 l-7 3 M22 30 l-4 6 M22 30 l1 7" stroke="#4d4529" stroke-width="2" stroke-linecap="round"/>`;
    o += `<path d="${glad([[-24,0],[-20,-13],[-4,-18],[14,-12],[20,0],[14,11],[-4,16],[-20,12]])}" fill="url(#kk-vis)"/>` + spikkels(Q,-18,-12,32,22,10,'#2b2614',.5);
    o += `<path d="${glad([[-16,-6],[-6,-12],[8,-9],[0,-4]])}" fill="#fff" opacity=".12"/><circle cx="-12" cy="-6" r="3.4" fill="#151209"/><circle cx="-13" cy="-7.2" r="1" fill="#fff" opacity=".9"/></g>`; return o; };
  const kikker = (x, y, sc, staart, seed) => { const Q = rng(seed); let o = `<g transform="translate(${x} ${y}) scale(${sc})">`;
    if (staart) o += `<path d="${glad([[36,-2],[60,-8],[78,-4],[60,2],[40,6]])}" fill="#5b7a2a"/>`;
    o += `<path d="${glad([[44,2],[66,0],[62,22],[34,28],[10,30]])}" fill="#4f6b22"/>`;  // dij
    o += `<path d="M30 26 C18 32 4 34 -6 34" stroke="#4f6b22" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-6 34 l-12 -2 M-6 34 l-12 3 M-6 34 l-10 7" stroke="#4f6b22" stroke-width="3" stroke-linecap="round"/>`;
    o += `<path d="${glad([[-50,-4],[-46,-20],[-30,-27],[-6,-25],[20,-21],[42,-10],[52,6],[44,22],[18,26],[-12,24],[-36,16],[-50,6]])}" fill="url(#kk-lijf)"/>`;
    o += `<path d="${glad([[-42,10],[-14,20],[18,22],[40,16],[30,24],[0,27],[-30,22]])}" fill="#cfcd92" opacity=".85"/>`;
    o += spikkels(Q,-30,-22,70,26,16);
    o += `<path d="M-30 14 C-34 26 -36 34 -38 40" stroke="#557424" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M-38 40 l-9 1 M-38 40 l-6 5 M-38 40 l1 6" stroke="#557424" stroke-width="2.6" stroke-linecap="round"/>`;
    o += `<path d="${blob(-29,-24,9,8,Q,8,.06)}" fill="#6a8a33"/><circle cx="-30" cy="-25" r="6.2" fill="url(#kk-oog)"/><ellipse cx="-30" cy="-25" rx="4.6" ry="2" fill="#120f08"/><circle cx="-32" cy="-27" r="1.3" fill="#fff" opacity=".9"/>`;
    o += `<path d="${blob(-13,-13,6,6,Q,8,.06)}" fill="#6b5a2a" opacity=".8"/><circle cx="-47" cy="-9" r="1.2" fill="#1f2a0c"/><path d="M-50 2 C-40 5 -28 4 -18 0" stroke="#2f4014" stroke-width="1.5" fill="none"/>`;
    o += `<path d="${glad([[-40,-20],[-20,-24],[10,-20],[-6,-18]])}" fill="#fff" opacity=".12"/></g>`; return o; };
  s += visje(90, 185, 1.25, false, 1) + visje(300, 180, 1.35, true, 2) + kikker(540, 150, 1.05, true, 3) + kikker(770, 104, 1.35, false, 4);
  const pijl = x => `<path d="M${x} 52 H${x+56}" stroke="#1d7a4b" stroke-width="4"/><path d="M${x+56} 44 L${x+70} 52 L${x+56} 60Z" fill="#1d7a4b"/><text x="${x+35}" y="38" text-anchor="middle" font-size="14" font-weight="700" fill="#1d7a4b">thyroxine</text>`;
  s += pijl(160) + pijl(400) + pijl(625);
  const t = (x,tx) => `<text x="${x}" y="246" text-anchor="middle" font-size="15" font-weight="700" paint-order="stroke" stroke="#eef4ef" stroke-width="3">${tx}</text>`;
  s += t(110,'kikkervisje') + t(330,'achterpoten groeien') + t(545,'staart verdwijnt') + t(775,'kikker');
  S.innerHTML = s;
})();

/* ---------- 4 bananen en ethyleen ---------- */
(function(){
  const S = $('#ban-svg'), R = rng(11); let met = true, gid = 0;
  const mix = (a,c,f) => a.map((v,i)=>Math.round(v+(c[i]-v)*f));
  const kleur = (r, f=0) => { const g = [124,168,58], y = [238,204,66], b = [150,110,50]; let c = r < .7 ? mix(g,y,r/.7) : mix(y,b,(r-.7)/.3*.3); c = mix(c,[40,30,10],f); return `rgb(${c})`; };
  function banaan(x, y, rot, r, seed){ const Q = rng(seed), id = 'bn' + (gid++);
    let o = `<defs><linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${kleur(r,-.0)}"/><stop offset=".45" stop-color="${kleur(r,.08)}"/><stop offset="1" stop-color="${kleur(r,.32)}"/></linearGradient></defs>`;
    const top = [[-74,-12],[-50,4],[-20,13],[12,14],[44,6],[70,-12]], bod = [[74,-6],[50,18],[16,30],[-20,30],[-52,20],[-76,-4]];
    o += `<g transform="translate(${x} ${y}) rotate(${rot})"><path d="M-82 -18 C-80 -14 -78 -12 -74 -10" stroke="#6a5a2c" stroke-width="9" stroke-linecap="round"/>`;
    o += `<path d="${glad([...top, ...bod])}" fill="url(#${id})" stroke="rgba(70,55,20,.55)" stroke-width="1.4"/>`;
    o += `<path d="${glad([[-70,-6],[-44,12],[-16,21],[16,22],[46,12],[70,-8]], false)}" fill="none" stroke="rgba(60,50,20,.28)" stroke-width="1.6"/>`;
    o += `<path d="${glad([[-66,-8],[-44,4],[-14,10],[16,10],[44,4],[64,-10]], false)}" fill="none" stroke="rgba(255,255,255,.4)" stroke-width="3" stroke-linecap="round"/>`;
    o += `<path d="${blob(74,-9,4.5,3.5,Q,7,.1)}" fill="#3b2d16"/><path d="${blob(-80,-17,5,4,Q,7,.1)}" fill="#5a4a24"/>`;
    const nv = Math.max(0, (r - .72) / .28) * 26; for (let i = 0; i < nv; i++){ const t = Q()*1.7 - .85; o += `<path d="${blob(t*62, 13 + (1-t*t)*6 + (Q()-.5)*12, 1.4+Q()*2.6, 1+Q()*1.6, Q, 7, .25)}" fill="#4b3212" opacity=".75"/>`; }
    return o + '</g>'; }
  function teken(){ gid = 0; const d = +$('#ban-dag').value; $('#ban-dagtxt').textContent = 'dag ' + d;
    const rGroen = met ? Math.min(.98, d*.17) : Math.min(.98, d*.075);
    let s = `<rect width="700" height="280" rx="16" fill="#f4efe4"/><path d="M0 236 H700 V280 H0Z" fill="#dccfb4"/>`;
    if (met) s += `<path d="M140 26 C118 110 112 200 136 242 H564 C588 200 582 110 560 26 C470 36 230 36 140 26Z" fill="rgba(196,160,104,.38)" stroke="rgba(140,108,60,.6)" stroke-width="2"/><path d="M140 26 C230 44 470 44 560 26" fill="none" stroke="rgba(140,108,60,.5)" stroke-width="2"/><text x="350" y="64" text-anchor="middle" font-size="14" font-weight="700" fill="#6b5530">papieren zak</text>`;
    [[262,120,-10,1],[352,138,3,2],[442,116,12,3]].forEach(([x,y,a,sd]) => s += banaan(x, y, a, rGroen, sd));
    if (met){ s += banaan(350, 198, 2, .97, 9); for (let i = 0; i < 12; i++){ const x = 220 + R()*260, y = 80 + R()*130; s += `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="3.2" fill="#6f9fc4" opacity=".6"/>`; } s += `<text x="350" y="264" text-anchor="middle" font-size="13" fill="#2f5a7a">blauwe stipjes = ethyleen</text>`; }
    S.innerHTML = s;
    $('#ban-zin').innerHTML = met ? (d ? 'De rijpe banaan geeft <b>ethyleen</b> af. In de zak blijft het gas bij de groene bananen: ze worden <b>sneller</b> geel.' : 'Groene bananen en één rijpe banaan zitten samen in een zak.') : (d ? 'Zonder extra ethyleen rijpen de bananen <b>trager</b>.' : 'Groene bananen liggen alleen op tafel.');
    $('#ban-met').setAttribute('aria-pressed', met); $('#ban-zonder').setAttribute('aria-pressed', !met); }
  $('#ban-met').onclick = () => { met = true; teken(); }; $('#ban-zonder').onclick = () => { met = false; teken(); }; $('#ban-dag').oninput = teken; teken();
})();

/* ---------- oefeningen ---------- */
sorteer($('#oef-es'), {id:'es', titel:'Oefening 1 · Excretie of secretie?', opties:[{k:'x',label:'excretie (afvalstof)'},{k:'s',label:'secretie (stof met een functie)'}], items:[
  {tekst:'urine', antwoord:'x'},{tekst:'speeksel', antwoord:'s'},{tekst:'koolstofdioxide in de uitgeademde lucht', antwoord:'x'},{tekst:'insuline', antwoord:'s', uitleg:'Een hormoon heeft een functie.'},{tekst:'traanvocht', antwoord:'s'},{tekst:'moedermelk', antwoord:'s'}]});
sorteer($('#oef-type'), {id:'type', titel:'Oefening 2 · Exocrien of endocrien?', opties:[{k:'exo',label:'exocriene klier'},{k:'endo',label:'endocriene klier'}], items:[
  {tekst:'De klier heeft een afvoerbuis.', antwoord:'exo'},{tekst:'De klier geeft haar stof af aan het bloed.', antwoord:'endo'},{tekst:'zweetklier', antwoord:'exo'},{tekst:'schildklier', antwoord:'endo'},{tekst:'speekselklier', antwoord:'exo'},{tekst:'bijnier', antwoord:'endo'},{tekst:'traanklier', antwoord:'exo'},{tekst:'hypofyse', antwoord:'endo'}]});
sorteer($('#oef-exo'), {id:'exo', titel:'Oefening 3 · Exocriene klieren', items:[
  {tekst:'Wat maakt de speekselklier?', opties:[{k:'a',label:'speeksel'},{k:'b',label:'zweet'},{k:'c',label:'adrenaline'}], antwoord:'a'},
  {tekst:'Wat is de functie van zweet?', opties:[{k:'a',label:'het lichaam afkoelen'},{k:'b',label:'voedsel verteren'},{k:'c',label:'de groei regelen'}], antwoord:'a', uitleg:'Als zweet verdampt, neemt het warmte op uit je huid.'},
  {tekst:'Wat is een functie van speeksel?', opties:[{k:'a',label:'voedsel nat maken en zetmeel beginnen te verteren'},{k:'b',label:'de bloedsuiker regelen'},{k:'c',label:'het oog vochtig houden'}], antwoord:'a'},
  {tekst:'Waar komt het traanvocht terecht?', opties:[{k:'a',label:'op het oog'},{k:'b',label:'in het bloed'},{k:'c',label:'in de maag'}], antwoord:'a'}]});
sorteer($('#oef-endo'), {id:'endo', titel:'Oefening 4 · Hormoonklieren', items:[
  {tekst:'Welk hormoon maakt de schildklier?', opties:[{k:'a',label:'thyroxine'},{k:'b',label:'insuline'},{k:'c',label:'adrenaline'}], antwoord:'a'},
  {tekst:'Welke klier maakt adrenaline?', opties:[{k:'a',label:'de bijnier'},{k:'b',label:'de hypofyse'},{k:'c',label:'de speekselklier'}], antwoord:'a'},
  {tekst:'Wat doet insuline?', opties:[{k:'a',label:'het regelt de hoeveelheid suiker in het bloed'},{k:'b',label:'het koelt het lichaam af'},{k:'c',label:'het maakt je slaperig'}], antwoord:'a'},
  {tekst:'Hoe komt een hormoon bij zijn doelorgaan?', opties:[{k:'a',label:'via het bloed'},{k:'b',label:'via een afvoerbuis'},{k:'c',label:'via de zenuwen'}], antwoord:'a'},
  {tekst:'Wat doet adrenaline?', opties:[{k:'a',label:'het maakt het lichaam klaar voor actie'},{k:'b',label:'het regelt de groei van de botten'},{k:'c',label:'het maakt speeksel'}], antwoord:'a'}]});
sorteer($('#oef-ander'), {id:'ander', titel:'Oefening 5 · Dieren en planten', items:[
  {tekst:'Welk hormoon zorgt voor de metamorfose van een kikkervisje?', opties:[{k:'a',label:'thyroxine uit de schildklier'},{k:'b',label:'ethyleen'},{k:'c',label:'adrenaline'}], antwoord:'a'},
  {tekst:'Welk plantenhormoon laat vruchten rijpen?', opties:[{k:'a',label:'ethyleen'},{k:'b',label:'insuline'},{k:'c',label:'thyroxine'}], antwoord:'a'},
  {tekst:'Je legt groene bananen bij een rijpe banaan in een zak. Wat gebeurt er?', opties:[{k:'a',label:'ze rijpen sneller'},{k:'b',label:'ze rijpen trager'},{k:'c',label:'er verandert niets'}], antwoord:'a', uitleg:'De rijpe banaan geeft ethyleen af.'}]});
ikkanFn = () => { $('#ikkan').innerHTML = `<h3>Controle hoofdstuk 3 en 4</h3><ul>
  ${regel('Ik leg het verschil uit tussen excretie- en secretieproducten.', scores.es)}
  ${regel('Ik leg uit welke kliertypes bij de mens voorkomen.', scores.type)}
  ${regel('Ik geef twee voorbeelden van exocriene klieren, hun klierafscheidingen en hun functie.', scores.exo)}
  ${regel('Ik geef twee voorbeelden van endocriene klieren, hun klierafscheidingen en hun functie.', scores.endo)}
  ${regel('Ik beschrijf hoe ook dieren en planten met hormonen reageren.', scores.ander)}</ul>`; };
updateIkKan();
'''
body = body.replace('__SPEEKSEL__', img('speekselklieren.jpg')).replace('__HORMOON__', img('hormoonklieren.jpg'))
pagina('biologie-klieren.html', 'Reactie door klieren', 'Biologie · 3de jaar · thema 3 · hoofdstuk 3 en 4',
  'Klieren maken stoffen en geven ze af. Sommige via een afvoerbuis, andere rechtstreeks aan het bloed.',
  'LPD 6B: De leerlingen vergelijken de bouw en werking van exocriene en endocriene klieren.',
  ['Een <b>effector</b> voert een reactie uit op een prikkel (hoofdstuk 1).', 'Spieren zijn effectoren (hoofdstuk 2). Klieren zijn ook effectoren.'],
  ('Lesdoelen hoofdstuk 3 · p. 84–95', ['Ik leg het verschil uit tussen excretie- en secretieproducten.', 'Ik leg uit welke kliertypes bij de mens voorkomen.', 'Ik geef twee voorbeelden van exocriene klieren, hun klierafscheidingen en hun functie.', 'Ik geef twee voorbeelden van endocriene klieren, hun klierafscheidingen en hun functie.']),
  [('lesA','3.1–3.2','Soorten klieren','excretie, secretie'),('lesB','3.3','Exocriene klieren','zweet en speeksel'),('lesC','3.4','Endocriene klieren','hormonen'),('lesD','4','Andere organismen','dieren en planten'),('lesE','✎','Oefenen','alle lesdoelen')],
  body, css, js)
