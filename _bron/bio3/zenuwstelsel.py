import sys, base64, pathlib
HIER = pathlib.Path(__file__).parent
sys.path.insert(0, str(HIER.parent / 'chemie3'))
from bouw import pagina
ORG = (HIER/'organisch.js').read_text()
img = lambda n: 'data:image/jpeg;base64,' + base64.b64encode((HIER/'img'/n).read_bytes()).decode()
body = r'''
  <main class="les" id="lesA" role="tabpanel">
    <section class="blok">
      <div class="blok-kop"><span class="letter">1</span><h2>Het menselijk organisme als systeem</h2></div>
      <p>Je lichaam reageert de hele tijd op prikkels. Twee stelsels zorgen ervoor dat alle organen goed samenwerken: ze <b>coördineren</b> de reacties.</p>
      <div class="fig"><svg id="sys-svg" viewBox="0 0 900 200" role="img" aria-label="van prikkel naar reactie"></svg></div>
      <div class="duo">
        <div class="kaart"><h3>Zenuwstelsel</h3><p>Stuurt <b>elektrische impulsen</b> via zenuwen. Snel en kort: je trekt je hand meteen terug van een hete pan.</p></div>
        <div class="kaart"><h3>Hormoonstelsel</h3><p>Stuurt <b>hormonen</b> via het bloed. Trager, maar het effect duurt langer: na schrik blijft je hart nog even snel kloppen.</p></div>
      </div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">2.1</span><h2>Centraal en perifeer zenuwstelsel</h2></div>
      <div class="duo zs">
        <div class="fig"><svg viewBox="0 0 600 1228" role="img" aria-label="zenuwstelsel van de mens"><image href="__ZS__" width="600" height="1228"/>
          <g font-size="40" font-weight="700"><path d="M318 70 L400 40" stroke="#1d2a36" stroke-width="3"/><rect x="390" y="8" width="200" height="60" rx="12" fill="#fff" opacity=".92"/><text x="490" y="52" text-anchor="middle">hersenen</text>
          <path d="M306 330 L420 360" stroke="#1d2a36" stroke-width="3"/><rect x="370" y="330" width="226" height="60" rx="12" fill="#fff" opacity=".92"/><text x="483" y="374" text-anchor="middle">ruggenmerg</text>
          <path d="M120 520 L20 600" stroke="#1d2a36" stroke-width="3"/><rect x="4" y="600" width="180" height="60" rx="12" fill="#fff" opacity=".92"/><text x="94" y="644" text-anchor="middle">zenuwen</text>
          <path d="M235 900 L130 960" stroke="#1d2a36" stroke-width="3"/><rect x="20" y="960" width="180" height="60" rx="12" fill="#fff" opacity=".92"/><text x="110" y="1004" text-anchor="middle">zenuwen</text></g></svg></div>
        <div>
          <div class="def"><span class="eyebrow">Centraal zenuwstelsel (CZS)</span><p>De <b>hersenen</b> en het <b>ruggenmerg</b> (geel). Hier wordt informatie verwerkt en worden bevelen gegeven.</p></div>
          <div class="def"><span class="eyebrow">Perifeer zenuwstelsel (PZS)</span><p>Alle <b>zenuwen</b> (blauw) die het CZS verbinden met de zintuigen, de spieren en de klieren.</p></div>
          <div class="tip"><b>Zo is het CZS beschermd</b><ul style="margin:4px 0 0;padding-left:20px"><li>De <b>schedel</b> rond de hersenen.</li><li>De <b>wervelkolom</b> rond het ruggenmerg.</li><li>De <b>hersenvliezen</b>: drie vliezen rond hersenen en ruggenmerg.</li><li>Het <b>hersenvocht</b> tussen de vliezen vangt schokken op.</li></ul></div>
        </div>
      </div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">2.2</span><h2>De delen van de hersenen</h2></div>
      <p>Een doorsnede van de hersenen, van opzij. De neus zit links. Klik op een naam.</p>
      <div class="duo hk">
        <div class="fig"><svg id="br-svg" viewBox="0 0 900 994" role="img" aria-label="doorsnede van de hersenen"><image href="__BRAIN__" width="900" height="994"/><g id="br-lab"></g></svg></div>
        <div class="kaart" id="br-info"></div>
      </div>
    </section>
  </main>

  <main class="les" id="lesB" role="tabpanel" hidden>
    <section class="blok">
      <div class="blok-kop"><span class="letter">3.1</span><h2>Het neuron</h2></div>
      <p>Het zenuwstelsel bestaat uit miljarden <b>neuronen</b> (zenuwcellen). Een <b>zenuw</b> is een bundel van uitlopers van heel veel neuronen.</p>
      <div class="fig"><svg id="neu-svg" viewBox="0 0 920 320" role="img" aria-label="bouw van een neuron"></svg></div>
      <div class="knoppen"><button type="button" class="knop hoofd" id="neu-start">▶ Stuur een impuls</button></div>
      <div class="tabelwrap"><table><thead><tr><th>deel</th><th>functie</th></tr></thead><tbody>
        <tr><td><b>dendrieten</b></td><td>korte, vertakte uitlopers: ze <b>ontvangen</b> impulsen</td></tr>
        <tr><td><b>cellichaam met kern</b></td><td>het centrum van de cel</td></tr>
        <tr><td><b>axon</b></td><td>lange uitloper: <b>geleidt</b> de impuls weg van het cellichaam</td></tr>
        <tr><td><b>myelineschede</b></td><td>vetlaagje rond het axon: isoleert en maakt de geleiding <b>sneller</b></td></tr>
        <tr><td><b>eindknopjes</b></td><td>geven de impuls <b>door</b> aan de volgende cel</td></tr></tbody></table></div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">3.1</span><h2>Drie soorten neuronen</h2></div>
      <div class="trio">
        <div class="kaart"><h3><span style="color:#c7372f">●</span> Sensorisch neuron</h3><p>Ook <b>gevoelszenuwcel</b>. Brengt een impuls van een <b>receptor</b> (zintuig) naar het CZS.</p><p><b>Voorbeelden:</b> van een pijnreceptor in je vingertop naar het ruggenmerg; van je oog naar je hersenen.</p></div>
        <div class="kaart"><h3><span style="color:#15803d">●</span> Schakelneuron</h3><p>Ligt in het <b>CZS</b>. Verbindt een sensorisch neuron met een motorisch neuron, of neuronen onderling.</p><p><b>Voorbeelden:</b> in het ruggenmerg bij een reflex; miljarden in je hersenen als je nadenkt.</p></div>
        <div class="kaart"><h3><span style="color:#1d5fb8">●</span> Motorisch neuron</h3><p>Ook <b>bewegingszenuwcel</b>. Brengt een impuls van het CZS naar een <b>effector</b>: een spier of een klier.</p><p><b>Voorbeelden:</b> van je ruggenmerg naar je armspier; van je hersenstam naar je speekselklieren.</p></div>
      </div>
      <div class="fig"><svg id="tn-svg" viewBox="0 0 1000 430" role="img" aria-label="drie soorten neuronen met cellichaam, dendrieten en axon"></svg></div>
      <p>Zo werken de drie samen als je een hete pan aanraakt. Druk op de knop en volg de impuls.</p>
      <div class="fig"><svg id="rb-svg" viewBox="0 0 1000 700" role="img" aria-label="reflexboog: receptor, sensorisch neuron, schakelneuron, motorisch neuron en effector"></svg></div>
      <div class="knoppen"><button type="button" class="knop hoofd" id="rb-start">▶ Raak de hete pan aan</button><button type="button" class="knop" id="rb-delen-k" aria-pressed="false">toon de delen van de neuronen</button></div>
      <p id="rb-zin">Receptor → sensorisch neuron → schakelneuron → motorisch neuron → effector.</p>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">3.2</span><h2>Impulsgeleiding binnen een neuron</h2></div>
      <div class="def"><span class="eyebrow">Elektrische impulsgeleiding</span><p>Een prikkel maakt een kleine <b>elektrische impuls</b>. Die loopt als een golf over het membraan van het neuron: van de dendrieten via het cellichaam en het axon naar de eindknopjes. Bij een axon met myelineschede <b>springt</b> de impuls van opening tot opening. Zo gaat het veel sneller, tot ongeveer 100 m/s.</p></div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">3.3</span><h2>Impulsoverdracht tussen neuronen: de synaps</h2></div>
      <p>Neuronen raken elkaar niet. Tussen een eindknopje en de volgende cel zit een smalle spleet: de <b>synapsspleet</b>. Een elektrische impuls kan daar niet over. Het doorgeven gaat <b>chemisch</b>.</p>
      <div class="knoppen" id="syn-stap"></div>
      <div class="fig"><svg id="syn-svg" viewBox="0 0 640 380" role="img" aria-label="synaps"></svg></div>
      <p id="syn-zin"></p>
    </section>
  </main>

  <main class="les" id="lesC" role="tabpanel" hidden>
    <section class="blok">
      <div class="blok-kop"><span class="letter">4.1</span><h2>Animaal en autonoom zenuwstelsel</h2></div>
      <div class="duo">
        <div class="def"><span class="eyebrow">Animaal zenuwstelsel</span><p>Regelt de dingen die je <b>bewust</b> waarneemt en doet, met de <b>skeletspieren</b>. Je kan het met je <b>wil</b> sturen. Voorbeeld: je pakt je gsm.</p></div>
        <div class="def"><span class="eyebrow">Autonoom zenuwstelsel</span><p>Regelt de organen <b>vanzelf</b>, zonder dat je erover nadenkt: hartslag, ademhaling, vertering, zweten. Je kan het <b>niet</b> met je wil sturen.</p></div>
      </div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">4.2–4.3</span><h2>Reflex of bewuste beweging?</h2></div>
      <p>Kies een situatie. Volg de impuls door het lichaam: <span style="color:#d97706;font-weight:700">oranje</span> = via een sensorisch neuron naar het CZS, <span style="color:#16a34a;font-weight:700">groen</span> = via een motorisch neuron naar de spier.</p>
      <div class="knoppen" id="rf-kies"></div>
      <div class="duo zs">
        <div class="fig"><svg id="rf-svg" viewBox="0 0 600 1228" role="img" aria-label="weg van de impuls in het lichaam"><image href="__ZS__" width="600" height="1228" opacity=".75"/><g id="rf-dyn"></g></svg></div>
        <div class="kaart" id="rf-info"></div>
      </div>
      <div class="duo">
        <div class="def"><span class="eyebrow">Reflex</span><p>Een <b>snelle, automatische</b> reactie. Je denkt er niet over na. De impuls gaat via het <b>ruggenmerg</b> of de <b>hersenstam</b>, niet via de grote hersenen. Dat bespaart tijd en beschermt je.</p></div>
        <div class="def"><span class="eyebrow">Bewuste beweging</span><p>Je <b>beslist</b> zelf. De impuls gaat via het ruggenmerg naar de <b>grote hersenen</b>. Daar wordt de informatie verwerkt en vertrekt het bevel naar de spieren. Dat duurt langer.</p></div>
      </div>
    </section>
  </main>

  <main class="les" id="lesD" role="tabpanel" hidden>
    <section class="blok">
      <div class="blok-kop"><span class="letter">5.1</span><h2>Zenuwstelsel en hormoonstelsel werken samen</h2></div>
      <div class="tabelwrap"><table><thead><tr><th></th><th>zenuwstelsel</th><th>hormoonstelsel</th></tr></thead><tbody>
        <tr><td><b>boodschapper</b></td><td>elektrische impuls (en neurotransmitter)</td><td>hormoon</td></tr>
        <tr><td><b>weg</b></td><td>via zenuwen</td><td>via het bloed</td></tr>
        <tr><td><b>snelheid</b></td><td>zeer snel (milliseconden)</td><td>trager (seconden tot uren)</td></tr>
        <tr><td><b>duur van het effect</b></td><td>kort</td><td>lang</td></tr>
        <tr><td><b>bereik</b></td><td>een bepaalde spier of klier</td><td>alle cellen met de juiste receptor (doelorganen)</td></tr></tbody></table></div>
      <div class="tip"><b>Voorbeeld: schrik</b><p>Je schrikt van een harde knal. Je zenuwstelsel laat je meteen opspringen. Tegelijk stuurt het een impuls naar de <b>bijnieren</b>. Die geven <b>adrenaline</b> af aan het bloed: je hart blijft nog een tijd sneller kloppen.</p></div>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">5.3</span><h2>Homeostase van de bloedsuikerspiegel</h2></div>
      <p><b>Homeostase</b> betekent dat het lichaam iets constant houdt. De hoeveelheid glucose (suiker) in je bloed moet tussen 0,7 en 1,1 gram per liter blijven. De <b>alvleesklier</b> regelt dat met twee hormonen.</p>
      <div class="fig"><svg id="bsch-svg" viewBox="0 0 920 470" role="img" aria-label="schema van de regeling van de bloedsuikerspiegel met insuline en glucagon"></svg></div>
      <div class="knoppen"><button type="button" class="knop" id="bs-eet">🍞 eet een boterham</button><button type="button" class="knop" id="bs-sport">🏃 sport een half uur</button><label class="knop" style="display:inline-flex;gap:6px;align-items:center"><input type="checkbox" id="bs-d1"> diabetes type 1 (geen insuline)</label></div>
      <div class="fig"><svg id="bs-svg" viewBox="0 0 760 300" role="img" aria-label="bloedsuikerspiegel in de tijd"></svg></div>
      <p id="bs-zin"></p>
    </section>
    <section class="blok">
      <div class="blok-kop"><span class="letter">5.3</span><h2>Drie vormen van diabetes</h2></div>
      <p>Bij <b>diabetes</b> (suikerziekte) werkt de regeling niet goed. De bloedsuikerspiegel blijft te hoog.</p>
      <div class="trio">
        <div class="kaart"><h3>Type 1</h3><p>De alvleesklier maakt <b>geen insuline</b> meer. Begint vaak bij kinderen en jongeren. De persoon moet insuline <b>inspuiten</b> of een insulinepomp gebruiken.</p></div>
        <div class="kaart"><h3>Type 2</h3><p>De cellen reageren <b>minder goed op insuline</b>. Komt vaker voor bij overgewicht en weinig beweging. Gezond eten, bewegen en soms medicijnen helpen.</p></div>
        <div class="kaart"><h3>Zwangerschapsdiabetes</h3><p>Ontstaat tijdens de <b>zwangerschap</b>. Meestal verdwijnt het na de bevalling.</p></div>
      </div>
    </section>
  </main>

  <main class="les" id="lesE" role="tabpanel" hidden>
    <section class="blok">
      <div class="oefening" id="oef-sys"></div>
      <div class="oefening" id="oef-czs"></div>
      <div class="oefening" id="oef-br"></div>
      <div class="oefening" id="oef-neu"></div>
      <div class="oefening" id="oef-imp"></div>
      <div class="oefening" id="oef-aa"></div>
      <div class="oefening" id="oef-rf"></div>
      <div class="oefening" id="oef-zh"></div>
      <div class="oefening" id="oef-bs"></div>
    </section>
    <section class="ikkan" id="ikkan"></section>
    <p class="credit">Afbeeldingen: zenuwstelsel naar <i>Nervous system diagram</i>, Medium69 &amp; Jmarchn, CC BY-SA 4.0 (Engelse namen weggelaten). Hersenen: <i>Brain human sagittal section</i>, Patrick J. Lynch (medisch illustrator) &amp; C. Carl Jaffe, CC BY 2.5. Alle via Wikimedia Commons. De andere tekeningen zijn eigen werk.</p>
  </main>
'''
css = r'''
.fig svg{max-width:900px}
.zs{grid-template-columns:2fr 3fr;align-items:start}
.zs .fig svg{max-height:560px}
.hk{grid-template-columns:3fr 2fr}
@media (max-width:760px){.zs,.hk{grid-template-columns:1fr}}
#br-svg .lab{cursor:pointer}
#br-svg .lab rect{fill:#fff;stroke:var(--line);stroke-width:2}
#br-svg .lab[aria-pressed="true"] rect{fill:var(--accent)}
#br-svg .lab[aria-pressed="true"] text{fill:#fff}
'''
js = ORG + r'''
const pijlSvg = (x1,y1,x2,y2,k='#1d7a4b') => { const a = Math.atan2(y2-y1,x2-x1); return `<path d="M${x1} ${y1} L${x2-Math.cos(a)*10} ${y2-Math.sin(a)*10}" stroke="${k}" stroke-width="4"/><path d="M${x2} ${y2} L${x2-Math.cos(a-.45)*16} ${y2-Math.sin(a-.45)*16} L${x2-Math.cos(a+.45)*16} ${y2-Math.sin(a+.45)*16}Z" fill="${k}"/>`; };
/* ---------- 1 systeem ---------- */
(function(){ const st = [['prikkel','een hete pan'],['zintuig','de huid voelt pijn'],['','verwerken en sturen'],['effector','spier of klier'],['reactie','hand terugtrekken']];
  let s = ''; st.forEach(([a,b],i) => { const x = 10 + i*180; s += `<rect x="${x}" y="50" width="150" height="100" rx="18" fill="${i===2?'color-mix(in srgb,var(--accent) 14%,#fff)':'#fff'}" stroke="var(--accent)" stroke-width="2"/><text x="${x+75}" y="${i===2?88:96}" text-anchor="middle" font-size="16" font-weight="800">${i===2?'<tspan x="'+(x+75)+'">zenuwstelsel</tspan><tspan x="'+(x+75)+'" dy="20">hormoonstelsel</tspan>':a}</text><text x="${x+75}" y="130" text-anchor="middle" font-size="13" fill="#51606e">${b}</text>`; if (i<4) s += pijlSvg(x+152, 100, x+178, 100); });
  $('#sys-svg').innerHTML = s; })();

/* ---------- 2.2 hersenen ---------- */
const BR = [
  ['grote hersenen', 225,150, 140,40, 'Het grootste deel. Hier <b>denk</b> je, <b>onthoud</b> je, word je je bewust van wat je zintuigen waarnemen en vertrekken de bevelen voor <b>bewuste bewegingen</b>.'],
  ['hersenbalk', 450,215, 470,330, 'Een brede band zenuwvezels die de linker- en de rechterhelft van de grote hersenen verbindt.'],
  ['kleine hersenen', 690,560, 690,770, 'Zorgen voor je <b>evenwicht</b> en voor <b>vloeiende, gecoördineerde</b> bewegingen.'],
  ['hersenstam', 478,590, 190,620, 'Verbindt de hersenen met het ruggenmerg. Regelt levensbelangrijke dingen <b>vanzelf</b>: <b>ademhaling</b>, <b>hartslag</b>, en reflexen zoals slikken, hoesten en knipperen. Het onderste deel heet het <b>verlengde merg</b>.'],
  ['ruggenmerg', 487,900, 700,920, 'Loopt in de wervelkolom. Geleidt impulsen tussen hersenen en lichaam, en regelt <b>reflexen</b> zoals de kniepeesreflex.']];
function toonBR(i){ $$('#br-lab .lab').forEach((g,k) => g.setAttribute('aria-pressed', k===i)); const b = BR[i]; $('#br-info').innerHTML = `<h3>${b[0][0].toUpperCase()+b[0].slice(1)}</h3><p>${b[5]}</p>`; }
$('#br-lab').innerHTML = BR.map(([n,px,py,lx,ly],i) => { const w = n.length*17+30; return `<g class="lab" role="button" tabindex="0" data-i="${i}" aria-pressed="false"><path d="M${px} ${py} L${lx} ${ly}" stroke="#1d2a36" stroke-width="3"/><circle cx="${px}" cy="${py}" r="7" fill="#1d2a36"/><rect x="${lx-w/2}" y="${ly-26}" width="${w}" height="50" rx="12"/><text x="${lx}" y="${ly+9}" text-anchor="middle" font-size="30" font-weight="700">${n}</text></g>`; }).join('');
$$('#br-lab .lab').forEach(g => { g.onclick = () => toonBR(+g.dataset.i); g.onkeydown = e => { if (e.key==='Enter'||e.key===' '){ e.preventDefault(); toonBR(+g.dataset.i); } }; });
toonBR(0);

/* ---------- 3.1 neuron ---------- */
let neuronPad = [];
(function(){
  const S = $('#neu-svg'), R = rng(3); let s = `<defs><radialGradient id="n-soma" cx="42%" cy="38%" r="70%"><stop offset="0" stop-color="#e9c6e0"/><stop offset=".6" stop-color="#c58bb7"/><stop offset="1" stop-color="#9a5f8f"/></radialGradient>
    <linearGradient id="n-myel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff8e4"/><stop offset=".5" stop-color="#f1dfb0"/><stop offset="1" stop-color="#cdb478"/></linearGradient>
    <radialGradient id="n-gloed"><stop offset="0" stop-color="#fffbe0"/><stop offset=".35" stop-color="#ffd23f" stop-opacity=".95"/><stop offset="1" stop-color="#ffb000" stop-opacity="0"/></radialGradient></defs>`;
  s += `<rect width="920" height="320" rx="16" fill="#f6f1f4"/>`;
  const K = '#b77aa8', KD = '#8e5482';
  // dendrieten: taps toelopende, vertakte uitlopers
  const takken = []; const tak = (x, y, a, L, w, d) => { const pts = [[x,y]]; let cx = x, cy = y, ca = a; for (let i = 0; i < 4; i++){ ca += (R()-.5)*.5; cx += Math.cos(ca)*L/4; cy += Math.sin(ca)*L/4; pts.push([cx,cy]); }
      takken.push([pts, w]); if (d > 0){ const n = 2; for (let k = 0; k < n; k++) tak(pts[2 + k][0], pts[2 + k][1], ca + (k ? .6 : -.6) + (R()-.5)*.3, L*.62, w*.6, d-1); } };
  const sx = 170, sy = 165;
  [[-2.6,1],[-2.0,1],[-1.3,1],[2.2,1],[2.8,1],[3.5,1],[-.7,0],[1.4,1]].forEach(([a,d],i) => tak(sx + Math.cos(a)*34, sy + Math.sin(a)*30, a, 70 + R()*40, 9, d+1));
  takken.forEach(([pts,w]) => { const d = glad(pts,false); s += `<path d="${d}" fill="none" stroke="${KD}" stroke-width="${w+2}" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${K}" stroke-width="${w}" stroke-linecap="round"/>`; });
  // axon
  const ax = bemonster(glad([[sx+30,sy],[260,170],[400,158],[560,172],[700,160],[790,166]], false), 120);
  s += `<path d="M${sx+20} ${sy-14} C${sx+44} ${sy-8} ${sx+56} ${sy-4} ${sx+70} ${sy+1} L${sx+70} ${sy+9} C${sx+56} ${sy+12} ${sx+44} ${sy+16} ${sx+20} ${sy+18}Z" fill="${K}"/>`;
  s += `<path d="${glad(ax,false)}" fill="none" stroke="${KD}" stroke-width="9" stroke-linecap="round"/><path d="${glad(ax,false)}" fill="none" stroke="${K}" stroke-width="7" stroke-linecap="round"/>`;
  // eindvertakkingen met eindknopjes
  const eind = []; [[-.7,60],[-.2,70],[.35,64],[.8,52]].forEach(([a,L]) => { const p0 = ax[ax.length-1]; const pts = [p0, [p0[0]+Math.cos(a)*L*.5, p0[1]+Math.sin(a)*L*.5 + (R()-.5)*8], [p0[0]+Math.cos(a)*L, p0[1]+Math.sin(a)*L]]; eind.push(pts);
    s += `<path d="${glad(pts,false)}" fill="none" stroke="${KD}" stroke-width="6" stroke-linecap="round"/><path d="${glad(pts,false)}" fill="none" stroke="${K}" stroke-width="4.4" stroke-linecap="round"/><path d="${blob(pts[2][0]+Math.cos(a)*6, pts[2][1]+Math.sin(a)*6, 9, 8, R, 8, .1, a)}" fill="url(#n-soma)" stroke="${KD}" stroke-width="1.2"/>`; });
  // myelineschede in segmenten
  for (let i = 0; i < 6; i++){ const t0 = .12 + i*.135, t1 = t0 + .115; const seg = ax.filter((p,k) => k/ax.length >= t0 && k/ax.length <= t1); if (seg.length < 2) continue; const d = glad(seg,false);
    s += `<path d="${d}" fill="none" stroke="#b8a064" stroke-width="25" stroke-linecap="round"/><path d="${d}" fill="none" stroke="url(#n-myel)" stroke-width="22" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#fffdf3" stroke-width="5" stroke-linecap="round" opacity=".7" transform="translate(0 -5)"/>`;
    const m = seg[Math.floor(seg.length/2)]; s += `<path d="${blob(m[0], m[1]+7, 7, 3.4, R, 8, .1)}" fill="url(#o-kern)" opacity=".85"/>`; }
  // cellichaam
  s += `<path d="${blob(sx, sy, 40, 34, R, 11, .14)}" fill="url(#n-soma)" stroke="${KD}" stroke-width="2"/><path d="${blob(sx-2, sy-2, 15, 13, R, 9, .08)}" fill="url(#o-kern)"/><circle cx="${sx+2}" cy="${sy-4}" r="4" fill="#2d1446"/>`;
  for (let i = 0; i < 14; i++){ const a = R()*6.28, r = 20 + R()*12; s += `<circle cx="${(sx+Math.cos(a)*r).toFixed(1)}" cy="${(sy+Math.sin(a)*r*.85).toFixed(1)}" r="1.4" fill="#7d3f72" opacity=".5"/>`; }
  const lab = (x, y, tx, ty, t, a='middle') => `<path d="M${x} ${y} L${tx} ${ty + (ty>y?-16:6)}" stroke="#1d2a36" stroke-width="1.4"/><circle cx="${x}" cy="${y}" r="2.6" fill="#1d2a36"/><text x="${tx}" y="${ty}" text-anchor="${a}" font-size="16" font-weight="700" paint-order="stroke" stroke="#f6f1f4" stroke-width="4">${t}</text>`;
  s += lab(98, 104, 70, 38, 'dendrieten') + lab(sx+16, sy+26, 170, 300, 'cellichaam') + lab(sx-2, sy-2, 250, 50, 'celkern') + lab(450, 158, 450, 300, 'axon') + lab(390, 150, 380, 50, 'myelineschede') + lab(830, 120, 850, 40, 'eindknopjes');
  S.innerHTML = s + '<g id="neu-dyn"></g>';
  neuronPad = [[60,110],[110,140],[sx-20,sy-6],[sx+30,sy], ...ax, ...eind[1].slice(1)];
  let t = -1, t0 = 0;
  $('#neu-start').onclick = () => { t = 0; };
  (function lus(ts){ requestAnimationFrame(lus); if (!zichtbaar(S)) return; const dt = ts && t0 ? Math.min(50, ts-t0)/1000 : 0; t0 = ts || 0; if (t < 0){ $('#neu-dyn').innerHTML=''; return; }
    t += dt*.45; if (t > 1.15){ t = -1; return; } const p = langs(neuronPad, Math.min(1,t));
    $('#neu-dyn').innerHTML = `<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="26" fill="url(#n-gloed)"/><text x="460" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#b45309">elektrische impuls</text>`; })();
})();

/* ---------- 3.3 synaps ---------- */
(function(){
  const S = $('#syn-svg'), R = rng(9); let stap = 0, t = 0, t0 = 0;
  const pre = glad([[220,-10],[226,60],[200,120],[150,170],[150,214],[230,236],[320,240],[410,236],[490,214],[490,170],[440,120],[414,60],[420,-10]]);
  const post = glad([[60,390],[80,300],[120,272],[220,262],[320,260],[420,262],[520,272],[560,300],[580,390]]);
  const blaasjes = []; for (let i = 0; i < 9; i++) blaasjes.push([200 + (i%4)*68 + (R()-.5)*20, 90 + Math.floor(i/4)*50 + (R()-.5)*16]);
  const rec = [190,250,320,390,450];
  let st = `<defs><radialGradient id="s-pre" cx="50%" cy="30%" r="80%"><stop offset="0" stop-color="#ead3e6"/><stop offset="1" stop-color="#c79abd"/></radialGradient><radialGradient id="s-post" cx="50%" cy="10%" r="90%"><stop offset="0" stop-color="#cfe3ef"/><stop offset="1" stop-color="#8db6cf"/></radialGradient>
    <radialGradient id="s-bl" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#fff"/><stop offset=".7" stop-color="#f7eef5"/><stop offset="1" stop-color="#d8bfd2"/></radialGradient><radialGradient id="n-gloed2"><stop offset="0" stop-color="#fffbe0"/><stop offset=".35" stop-color="#ffd23f" stop-opacity=".95"/><stop offset="1" stop-color="#ffb000" stop-opacity="0"/></radialGradient></defs>`;
  st += `<rect width="640" height="380" rx="16" fill="#f7f3ee"/><path d="${post}" fill="url(#s-post)" stroke="#5f8eab" stroke-width="3"/>`;
  rec.forEach(x => st += `<path d="M${x-9} 262 C${x-10} 252 ${x-6} 246 ${x-4} 244 L${x-2} 252 L${x+2} 252 L${x+4} 244 C${x+6} 246 ${x+10} 252 ${x+9} 262 Z" fill="#2e7d8c" stroke="#1f5a66" stroke-width="1.2"/>`);
  st += `<path d="${pre}" fill="url(#s-pre)" stroke="#9a6a8f" stroke-width="3"/>`;
  for (let i = 0; i < 20; i++){ const x = 170 + R()*300, y = 20 + R()*190; st += `<path d="${blob(x,y,10,4,R,7,.15,R()*3)}" fill="#e7cfe0" opacity=".7"/>`; }
  const lab = (x, y, tx, ty, t, a='start') => `<path d="M${x} ${y} L${tx} ${ty-5}" stroke="#1d2a36" stroke-width="1.4"/><circle cx="${x}" cy="${y}" r="2.6" fill="#1d2a36"/><text x="${tx + (a==='start'?4:-4)}" y="${ty}" text-anchor="${a}" font-size="15" font-weight="700" paint-order="stroke" stroke="#f7f3ee" stroke-width="4">${t}</text>`;
  const labels = lab(170, 150, 40, 120, 'eindknopje', 'start') + lab(172, 249, 20, 300, 'synapsspleet', 'start') + lab(450, 252, 560, 290, 'receptor', 'start') + lab(560, 330, 470, 360, 'volgend neuron', 'end');
  S.innerHTML = st + '<g id="syn-dyn"></g>' + labels;
  const STAP = [['1 · impuls komt aan','Een <b>elektrische impuls</b> komt aan in het eindknopje.'],['2 · blaasjes gaan open','De <b>blaasjes</b> smelten samen met het membraan. Ze laten <b>neurotransmitter</b> vrij in de synapsspleet.'],['3 · binden op receptoren','De neurotransmitter beweegt door de spleet en bindt op de <b>receptoren</b> van het volgende neuron.'],['4 · nieuwe impuls','Daardoor ontstaat in het volgende neuron een <b>nieuwe elektrische impuls</b>. Zo gaat de boodschap verder.']];
  $('#syn-stap').innerHTML = STAP.map((x,i) => `<button type="button" class="knop" data-i="${i}">${x[0]}</button>`).join('') + '<button type="button" class="knop hoofd" id="syn-alles">▶ Speel alles</button>';
  let auto = false; const kies = i => { stap = i; t = 0; $$('#syn-stap .knop[data-i]').forEach(b => b.setAttribute('aria-pressed', +b.dataset.i===i)); $('#syn-zin').innerHTML = STAP[i][1]; };
  $$('#syn-stap .knop[data-i]').forEach(b => b.onclick = () => { auto = false; kies(+b.dataset.i); }); $('#syn-alles').onclick = () => { auto = true; kies(0); };
  kies(0);
  const nt = []; for (let i = 0; i < 26; i++) nt.push({x0: 240 + R()*160, dx:(R()-.5)*60, r:rec[i%5] + (R()-.5)*6});
  (function lus(ts){ requestAnimationFrame(lus); if (!zichtbaar(S)) return; const dt = ts && t0 ? Math.min(50, ts-t0)/1000 : 0; t0 = ts || 0; t = Math.min(1, t + dt*.5); if (auto && t >= 1 && stap < 3) kies(stap+1);
    let o = ''; const e = t*t*(3-2*t);
    blaasjes.forEach(([x,y],i) => { let bx = x, by = y, open = 0; if (stap >= 1 && i < 4){ const f = stap===1 ? e : 1; by = y + (222 - y)*f; bx = x + (300 + i*14 - x)*f*.6; open = stap===1 ? Math.max(0,(e-.7)/.3) : 1; }
      if (open < 1) o += `<circle cx="${bx.toFixed(1)}" cy="${by.toFixed(1)}" r="${(15*(1-open*.5)).toFixed(1)}" fill="url(#s-bl)" stroke="#9a6a8f" stroke-width="1.6"/>`;
      if (open < 1) for (let k = 0; k < 5; k++) o += `<circle cx="${(bx + Math.cos(k*1.26+i)*6).toFixed(1)}" cy="${(by + Math.sin(k*1.26+i)*6).toFixed(1)}" r="2.4" fill="#e07b1f"/>`; });
    if (stap >= 1){ nt.forEach((n,i) => { let x, y; if (stap === 1){ if (e < .75) return; const f = (e-.75)/.25; x = n.x0; y = 236 + f*6; } else if (stap === 2){ x = n.x0 + (n.r - n.x0)*e; y = 242 + (248 - 242)*e + Math.sin(e*9+i)*3; } else { x = n.r; y = 248; } o += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="2.6" fill="#e07b1f"/>`; }); }
    if (stap === 0){ const y = -10 + e*200; o += `<circle cx="320" cy="${y.toFixed(1)}" r="30" fill="url(#n-gloed2)"/>`; }
    if (stap === 3){ const y = 280 + e*100; o += `<circle cx="320" cy="${y.toFixed(1)}" r="30" fill="url(#n-gloed2)"/>`; }
    $('#syn-dyn').innerHTML = o; })();
})();

/* ---------- 4.2–4.3 reflex en bewuste beweging (op de afbeelding) ---------- */
(function(){
  const G = (gx, gy) => [(gx-180)*1.3636, gy*1.3644];
  const arm = [G(552,505),G(540,470),G(522,420),G(505,350),G(492,280),G(478,200),G(455,160),G(420,150),G(402,200)];
  const been = [G(362,628),G(368,560),G(375,480),G(385,410),G(395,350),G(400,320)];
  const naarHersenen = [G(402,200),G(401,150),G(401,100),G(402,60)];
  const SIT = [
    {n:'terugtrekreflex', titel:'Terugtrekreflex: hand op een hete pan', in:arm, uit:[...arm].reverse().slice(0,6), uitleg:'De <b>huid</b> voelt pijn. Een sensorisch neuron brengt de impuls naar het <b>ruggenmerg</b>. Een schakelneuron geeft hem meteen door aan een motorisch neuron. De <b>armspier</b> trekt je hand terug. Pas daarna voel je de pijn in je hersenen.', soort:'reflex via het ruggenmerg'},
    {n:'kniepeesreflex', titel:'Kniepeesreflex: tik onder de knie', in:been, uit:[...been].reverse().slice(0,4), uitleg:'De tik rekt de <b>dijspier</b>. Een sensorisch neuron brengt de impuls naar het <b>ruggenmerg</b>. Een motorisch neuron gaat terug naar de dijspier: je onderbeen schiet vooruit.', soort:'reflex via het ruggenmerg'},
    {n:'knipperreflex', titel:'Knipperreflex: iets vliegt naar je oog', in:[G(386,62),G(395,75),G(401,90)], uit:[G(401,90),G(392,72),G(384,58)], uitleg:'Je <b>ogen</b> zien iets aankomen. De impuls gaat naar de <b>hersenstam</b>. Die stuurt meteen een bevel naar de spieren van je ooglid: je knippert.', soort:'reflex via de hersenstam'},
    {n:'bewuste beweging', titel:'Bewuste beweging: je pakt je gsm', in:[...arm, ...naarHersenen], uit:[...naarHersenen].reverse().concat([...arm].reverse().slice(1,6)), uitleg:'Je voelt de gsm in je hand. De impuls gaat via het ruggenmerg naar de <b>grote hersenen</b>. Daar <b>beslis</b> je wat je doet. Het bevel gaat via het ruggenmerg en een motorisch neuron naar je <b>armspieren</b>.', soort:'via de grote hersenen'}];
  let k = 0, t = 0, t0 = 0;
  const kies = i => { k = i; t = 0; $$('#rf-kies .knop').forEach((b,j) => b.setAttribute('aria-pressed', j===i)); const s = SIT[i]; $('#rf-info').innerHTML = `<h3>${s.titel}</h3><p class="eyebrow">${s.soort}</p><p>${s.uitleg}</p>`; };
  $('#rf-kies').innerHTML = SIT.map((s,i) => `<button type="button" class="knop" data-i="${i}">${s.n}</button>`).join(''); $$('#rf-kies .knop').forEach(b => b.onclick = () => kies(+b.dataset.i)); kies(0);
  const S = $('#rf-svg');
  (function lus(ts){ requestAnimationFrame(lus); if (!zichtbaar(S)) return; const dt = ts && t0 ? Math.min(50, ts-t0)/1000 : 0; t0 = ts || 0; t += dt*.32; if (t > 2.4) t = 0;
    const s = SIT[k]; let o = `<path d="${glad(s.in,false)}" fill="none" stroke="#d97706" stroke-width="12" stroke-linecap="round" opacity=".55"/><path d="${glad(s.uit.map(p=>[p[0]+12,p[1]+4]),false)}" fill="none" stroke="#16a34a" stroke-width="12" stroke-linecap="round" stroke-dasharray="3 16" opacity=".8"/>`;
    const gl = (p, kl) => `<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="38" fill="${kl}" opacity=".3"/><circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="17" fill="${kl}" stroke="#fff" stroke-width="4"/>`;
    if (t < 1) o += gl(langs(s.in, t), '#d97706'); else if (t < 2) { const q = langs(s.uit, t-1); o += gl([q[0]+12,q[1]+4], '#16a34a'); }
    $('#rf-dyn').innerHTML = o; })();
})();


/* ---------- 5.3 schema bloedsuiker ---------- */
(function(){
  const S = $('#bsch-svg');
  const box = (x, y, w, h, t, kl, id) => `<g id="${id||''}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="16" fill="#fff" stroke="${kl}" stroke-width="3"/>${t.map((r,i)=>`<text x="${x+w/2}" y="${y+h/2 + (i-(t.length-1)/2)*20 + 6}" text-anchor="middle" font-size="16" font-weight="${i?500:800}">${r}</text>`).join('')}</g>`;
  const pijl = (d, kl) => `<path d="${d}" fill="none" stroke="${kl}" stroke-width="4" marker-end="url(#bsch-${kl.slice(1)})"/>`;
  const B = '#2563eb', P = '#9333ea', G = '#16a34a';
  let s = `<defs>${[B,P,G].map(k=>`<marker id="bsch-${k.slice(1)}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="${k}"/></marker>`).join('')}</defs>`;
  s += `<g id="bsch-normaal">${box(330, 196, 260, 78, ['normale bloedsuikerspiegel','0,7 – 1,1 g/L'], G)}</g>`;
  s += `<g id="bsch-boven" class="tak">${box(20, 20, 220, 78, ['te veel suiker','bv. na het eten'], B)}${box(350, 20, 220, 78, ['alvleesklier','maakt insuline'], B)}${box(680, 20, 220, 78, ['lever en spieren','nemen glucose op'], B)}${box(680, 140, 220, 56, ['bloedsuikerspiegel daalt'], B)}
    ${pijl('M244 59 H344', B)}${pijl('M574 59 H674', B)}${pijl('M790 102 V134', B)}${pijl('M676 168 C640 168 620 190 596 214', B)}${pijl('M400 194 C300 170 160 150 130 104', G)}
    <text x="780" y="122" font-size="13" text-anchor="end" fill="#334155">glucose → glycogeen</text></g>`;
  s += `<g id="bsch-onder" class="tak">${box(20, 372, 220, 78, ['te weinig suiker','bv. na het sporten'], P)}${box(350, 372, 220, 78, ['alvleesklier','maakt glucagon'], P)}${box(680, 372, 220, 78, ['lever','geeft glucose af'], P)}${box(680, 274, 220, 56, ['bloedsuikerspiegel stijgt'], P)}
    ${pijl('M244 411 H344', P)}${pijl('M574 411 H674', P)}${pijl('M790 368 V336', P)}${pijl('M676 302 C640 302 620 280 596 258', P)}${pijl('M400 276 C300 300 160 320 130 366', G)}
    <text x="780" y="356" font-size="13" text-anchor="end" fill="#334155">glycogeen → glucose</text></g>`;
  S.innerHTML = s;
})();
const bschActief = w => { const b = $('#bsch-boven'), o = $('#bsch-onder'); if (!b) return; b.style.opacity = w==='o' ? .3 : 1; o.style.opacity = w==='b' ? .3 : 1; };

/* ---------- 3.1 drie soorten neuronen ---------- */
(function(){
  const S = $('#tn-svg');
  const RD = '#c7372f', RL = '#ef8a7f', GD = '#15803d', GL = '#86d29d', BD = '#1d5fb8', BL = '#7fb2ee';
  let s = `<defs>${[['r','#ffd2cc',RD],['g','#c9f0d4',GD],['b','#cfe2fb',BD]].map(([id,l,d])=>`<radialGradient id="tn-soma-${id}" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="${l}"/><stop offset="1" stop-color="${d}"/></radialGradient>`).join('')}
    ${[['r',RD],['b',BD]].map(([id,k])=>`<marker id="tn-p${id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="${k}"/></marker>`).join('')}</defs><rect width="1000" height="430" rx="16" fill="#fbf9f6"/>`;
  const myel = (pts, n, dk, lc) => { const P = bemonster(glad(pts,false), 160); let o = `<path d="${glad(P,false)}" fill="none" stroke="${dk}" stroke-width="4" stroke-linecap="round"/>`;
    for (let i = 0; i < n; i++){ const a = Math.floor((i+.12)/n*160), b = Math.floor((i+.88)/n*160); const d = glad(P.slice(a,b),false), m = P[Math.floor((a+b)/2)];
      o += `<path d="${d}" fill="none" stroke="${dk}" stroke-width="17" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${lc}" stroke-width="11" stroke-linecap="round"/><ellipse cx="${m[0].toFixed(1)}" cy="${m[1].toFixed(1)}" rx="4" ry="2.4" fill="#fff" opacity=".85"/>`; } return o; };
  const dendr = (x, y, a, len, w, d, k, Q) => { let o=''; const pts = [[x,y]]; let px=x, py=y, pa=a; for (let i=0;i<3;i++){ pa += (Q()-.5)*.4; px += Math.cos(pa)*len/3; py += Math.sin(pa)*len/3; pts.push([px,py]); }
    o += `<path d="${glad(pts,false)}" fill="none" stroke="${k}" stroke-width="${w}" stroke-linecap="round"/>`; if (d>0){ o += dendr(pts[2][0],pts[2][1],pa-.6,len*.55,w*.65,d-1,k,Q) + dendr(pts[3][0],pts[3][1],pa+.55,len*.5,w*.65,d-1,k,Q); } return o; };
  const soma = (x, y, r, id, k, Q) => `<path d="${blob(x, y, r, r*.9, Q, 10, .1)}" fill="url(#tn-soma-${id})" stroke="${k}" stroke-width="2.5"/><circle cx="${x}" cy="${y}" r="${r*.38}" fill="${k}"/>`;
  const knop = (x, y, a, k, l) => `<path d="M${x} ${y} l${(Math.cos(a)*14).toFixed(1)} ${(Math.sin(a)*14).toFixed(1)}" stroke="${k}" stroke-width="3" stroke-linecap="round"/><circle cx="${(x+Math.cos(a)*18).toFixed(1)}" cy="${(y+Math.sin(a)*18).toFixed(1)}" r="5.5" fill="${l}" stroke="${k}" stroke-width="1.5"/>`;
  const Q1 = rng(31), Q2 = rng(32), Q3 = rng(33);
  // sensorisch neuron (bovenaan, impuls van links naar rechts)
  s += dendr(96,120,Math.PI-.5,52,4.5,1,RD,Q1) + dendr(96,120,Math.PI,56,4.5,1,RD,Q1) + dendr(96,120,Math.PI+.5,52,4.5,1,RD,Q1);
  s += myel([[96,120],[300,120]], 4, RD, RL) + myel([[300,120],[540,122]], 4, RD, RL);
  s += `<path d="M300 120 V84" stroke="${RD}" stroke-width="5"/>` + soma(300, 68, 20, 'r', RD, Q1);
  [-.6,0,.6].forEach(d => s += knop(540, 122, d, RD, RL));
  // schakelneuron
  s += dendr(640,170,Math.PI+.2,58,5,1,GD,Q2) + dendr(640,170,-2.3,50,5,1,GD,Q2) + dendr(640,170,-1.3,48,4.5,1,GD,Q2) + dendr(640,170,-.4,52,4.5,1,GD,Q2) + dendr(640,170,.5,40,4,1,GD,Q2);
  s += `<path d="${glad([[650,190],[676,236],[700,276],[716,296]],false)}" fill="none" stroke="${GD}" stroke-width="5" stroke-linecap="round"/>` + soma(640, 170, 26, 'g', GD, Q2);
  [-.3,.5].forEach(d => s += knop(716, 296, 1.1 + d, GD, GL));
  // motorisch neuron (onderaan, impuls van rechts naar links)
  s += dendr(780,344,-1.6,52,5,1,BD,Q3) + dendr(780,344,-.6,54,5,1,BD,Q3) + dendr(780,344,.3,50,4.5,1,BD,Q3) + dendr(780,344,1.2,40,4.5,1,BD,Q3) + dendr(780,344,-2.4,46,4.5,1,BD,Q3);
  s += myel([[756,352],[600,362],[400,364],[180,362]], 7, BD, BL) + soma(780, 344, 28, 'b', BD, Q3);
  [Math.PI-.6, Math.PI, Math.PI+.6].forEach(a => s += knop(180, 362, a, BD, BL));
  // pijlen voor de richting van de impuls
  s += `<path d="M150 170 C220 196 300 196 360 176" stroke="${RD}" stroke-width="3" fill="none" marker-end="url(#tn-pr)"/><path d="M620 410 C540 418 460 418 380 408" stroke="${BD}" stroke-width="3" fill="none" marker-end="url(#tn-pb)"/>`;
  // labels
  const lab = (x, y, tx, ty, t, kl='#1d2a36', fs=15, a='middle') => `<path d="M${x} ${y} L${tx} ${ty}" stroke="#334155" stroke-width="1.3"/><circle cx="${x}" cy="${y}" r="2.6" fill="#334155"/><text x="${tx + (a==='start'?5:a==='end'?-5:0)}" y="${ty + (a==='middle' ? (ty>y?15:-6) : 5)}" text-anchor="${a}" font-size="${fs}" font-weight="700" fill="${kl}" paint-order="stroke" stroke="#fbf9f6" stroke-width="4">${t}</text>`;
  s += `<text x="40" y="44" font-size="19" font-weight="800" fill="${RD}">sensorisch neuron</text><text x="860" y="96" font-size="19" font-weight="800" fill="${GD}" text-anchor="middle">schakelneuron</text><text x="40" y="306" font-size="19" font-weight="800" fill="${BD}">motorisch neuron</text>`;
  s += lab(52, 140, 60, 210, 'dendrieten') + lab(310, 62, 390, 40, 'cellichaam', '#1d2a36', 15, 'start') + lab(450, 121, 450, 180, 'axon');
  s += lab(600, 150, 560, 230, 'dendrieten') + lab(650, 176, 800, 140, 'cellichaam', '#1d2a36', 15, 'start') + lab(690, 260, 600, 290, 'axon', '#1d2a36', 15, 'end');
  s += lab(830, 330, 900, 280, 'dendrieten', '#1d2a36', 15, 'start') + lab(790, 350, 880, 400, 'cellichaam', '#1d2a36', 15, 'start') + lab(480, 364, 480, 300, 'axon') + lab(150, 362, 120, 410, 'eindknopjes');
  s += `<text x="255" y="214" font-size="13" fill="${RD}" font-weight="700">impuls</text><text x="500" y="402" font-size="13" fill="${BD}" font-weight="700" text-anchor="middle">impuls</text>`;
  S.innerHTML = s;
})();

/* ---------- 3.1 reflexboog ---------- */
(function(){
  const S = $('#rb-svg'), R = rng(17);
  const RD = '#c7372f', RL = '#ef8a7f', GD = '#15803d', GL = '#86d29d', BD = '#1d5fb8', BL = '#7fb2ee';
  let s = `<defs>
    <linearGradient id="rb-huidtop" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9906f"/><stop offset="1" stop-color="#d8704f"/></linearGradient>
    <linearGradient id="rb-huidvoor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4b49b"/><stop offset="1" stop-color="#f7c9b5"/></linearGradient>
    <linearGradient id="rb-spier" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e07a6a"/><stop offset=".5" stop-color="#c9503f"/><stop offset="1" stop-color="#a23a2d"/></linearGradient>
    <radialGradient id="rb-gloed"><stop offset="0" stop-color="#fff"/><stop offset=".35" stop-color="#ffd23f" stop-opacity=".95"/><stop offset="1" stop-color="#ffb000" stop-opacity="0"/></radialGradient>
    ${[['r','#ffd2cc',RD],['g','#c9f0d4',GD],['b','#cfe2fb',BD]].map(([id,l,d])=>`<radialGradient id="rb-soma-${id}" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="${l}"/><stop offset="1" stop-color="${d}"/></radialGradient>`).join('')}</defs>`;
  s += `<rect width="1000" height="700" rx="16" fill="#fbf9f6"/>`;

  /* ruggenmerg met wortels */
  const cx = 805, cy = 365;
  const wortel = (pts, w) => `<path d="${glad(pts,false)}" fill="none" stroke="#dccb9f" stroke-width="${w+4}" stroke-linecap="round"/><path d="${glad(pts,false)}" fill="none" stroke="#f1e7c9" stroke-width="${w}" stroke-linecap="round"/>`;
  s += wortel([[680,262],[600,268],[520,300],[440,334],[396,344]], 46) + wortel([[680,470],[600,462],[520,430],[440,370],[396,350]], 46) + wortel([[420,346],[360,346]], 58);
  s += `<path d="${glad([[cx-30,cy-170],[cx+60,cy-176],[cx+150,cy-120],[cx+182,cy-10],[cx+160,cy+120],[cx+70,cy+178],[cx-50,cy+176],[cx-150,cy+128],[cx-176,cy+10],[cx-150,cy-116],[cx-90,cy-162]])}" fill="#f1e7c9" stroke="#cdb987" stroke-width="3"/>`;
  s += `<path d="${glad([[cx,cy-24],[cx+50,cy-58],[cx+86,cy-140],[cx+118,cy-140],[cx+104,cy-70],[cx+74,cy-12],[cx+118,cy+56],[cx+150,cy+120],[cx+104,cy+140],[cx+50,cy+60],[cx,cy+32],[cx-50,cy+60],[cx-104,cy+140],[cx-150,cy+120],[cx-118,cy+56],[cx-74,cy-12],[cx-104,cy-70],[cx-118,cy-140],[cx-86,cy-140],[cx-50,cy-58]])}" fill="#f6b3a6" stroke="#e48f80" stroke-width="2"/>`;
  s += `<ellipse cx="${cx}" cy="${cy+4}" rx="9" ry="6" fill="#fff" stroke="#e48f80"/>`;

  /* huidblok met receptoren */
  s += `<path d="M200 66 L236 32 H474 L438 66 Z" fill="url(#rb-huidtop)"/><path d="M438 66 L474 32 V126 L438 160 Z" fill="#c9644a"/>`;
  s += `<path d="M200 66 H438 V160 H200 Z" fill="url(#rb-huidvoor)"/><path d="M200 66 H438 V84 H200 Z" fill="#e9967a"/>`;
  for (let x = 206; x < 436; x += 11) s += `<ellipse cx="${x}" cy="88" rx="5.5" ry="4" fill="#f1b54a" stroke="#c8892a" stroke-width=".8"/>`;
  for (let i = 0; i < 26; i++){ const x = 206 + R()*226, y = 96 + R()*58; s += `<path d="${blob(x, y, 4 + R()*3, 3 + R()*2, R, 7, .2)}" fill="#f2a58c" opacity=".7"/>`; }
  s += `<path d="M360 20 L372 52 L380 16 Z" fill="#7cc243" stroke="#4d8a24" stroke-width="1.5"/><text x="390" y="22" font-size="15" font-weight="800" fill="#1d2a36">prikkel</text>`;

  /* spierweefsel */
  const vezel = (x, y, w, h) => { let o = `<path d="M${x} ${y} H${x+w} A${h*.28} ${h/2} 0 0 1 ${x+w} ${y+h} H${x} A${h*.28} ${h/2} 0 0 1 ${x} ${y}Z" fill="url(#rb-spier)" stroke="#8e2f24" stroke-width="1.5"/>`;
    for (let k = x + 14; k < x + w - 4; k += 13) o += `<path d="M${k} ${y+2} C${k-3} ${y+h*.35} ${k+3} ${y+h*.65} ${k} ${y+h-2}" stroke="#f2b2a6" stroke-width="2.2" fill="none" opacity=".75"/>`;
    return o + `<ellipse cx="${x+w}" cy="${y+h/2}" rx="${h*.28}" ry="${h/2}" fill="#d9897a" stroke="#8e2f24" stroke-width="1.5"/>`; };
  s += vezel(196, 588, 250, 50) + vezel(214, 556, 250, 46) + vezel(196, 632, 250, 50);
  for (let i = 0; i < 7; i++){ const x = 220 + R()*210, y = 566 + R()*110; s += `<ellipse cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" rx="9" ry="3.5" fill="#e98878" stroke="#a94735" stroke-width="1"/>`; }

  /* neuronen */
  const myel = (pts, n, dk, lc) => { const P = bemonster(glad(pts,false), 160); let o = `<path d="${glad(P,false)}" fill="none" stroke="${dk}" stroke-width="4" stroke-linecap="round"/>`;
    for (let i = 0; i < n; i++){ const a = Math.floor((i+.1)/n*160), b = Math.floor((i+.9)/n*160); const d = glad(P.slice(a,b),false), m = P[Math.floor((a+b)/2)];
      o += `<path d="${d}" fill="none" stroke="${dk}" stroke-width="17" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${lc}" stroke-width="11" stroke-linecap="round"/><ellipse cx="${m[0].toFixed(1)}" cy="${m[1].toFixed(1)}" rx="4" ry="2.4" fill="#fff" opacity=".85"/>`; } return [o, P]; };
  const dendr = (x, y, a, len, w, d, k, Q) => { let o=''; const pts = [[x,y]]; let px=x, py=y, pa=a; for (let i=0;i<3;i++){ pa += (Q()-.5)*.45; px += Math.cos(pa)*len/3; py += Math.sin(pa)*len/3; pts.push([px,py]); }
    o += `<path d="${glad(pts,false)}" fill="none" stroke="${k}" stroke-width="${w}" stroke-linecap="round"/>`; if (d>0){ o += dendr(pts[2][0],pts[2][1],pa-.6,len*.55,w*.65,d-1,k,Q) + dendr(pts[3][0],pts[3][1],pa+.55,len*.5,w*.65,d-1,k,Q); } return o; };
  const soma = (x, y, r, id, k, Q) => `<path d="${blob(x, y, r, r*.9, Q, 10, .1)}" fill="url(#rb-soma-${id})" stroke="${k}" stroke-width="2.5"/><circle cx="${x}" cy="${y}" r="${r*.38}" fill="${k}"/>`;
  const knop = (x, y, a, k, l) => `<path d="M${x} ${y} l${(Math.cos(a)*14).toFixed(1)} ${(Math.sin(a)*14).toFixed(1)}" stroke="${k}" stroke-width="3" stroke-linecap="round"/><circle cx="${(x+Math.cos(a)*18).toFixed(1)}" cy="${(y+Math.sin(a)*18).toFixed(1)}" r="5" fill="${l}" stroke="${k}" stroke-width="1.5"/>`;
  const Q1 = rng(1), Q2 = rng(2), Q3 = rng(3);
  // sensorisch (rood): dendriet van de receptoren, cellichaam op een steeltje, axon naar het ruggenmerg
  let sens = '';
  [[244,94],[272,98],[300,94],[328,98],[356,94]].forEach(([x,y]) => { sens += `<path d="M312 150 C312 128 ${x} 126 ${x} ${y+6}" fill="none" stroke="${RD}" stroke-width="3.5" stroke-linecap="round"/><circle cx="${x}" cy="${y}" r="6" fill="${RL}" stroke="${RD}" stroke-width="2"/>`; });
  const [sD, sDP] = myel([[312,150],[314,220],[322,286],[352,328],[410,340],[470,322]], 5, RD, RL);
  const [sA, sAP] = myel([[470,322],[540,292],[610,268],[680,262],[722,264]], 4, RD, RL);
  sens += sD + sA + `<path d="M540 292 C536 276 532 262 530 246" stroke="${RD}" stroke-width="5" fill="none"/>` + soma(530, 232, 17, 'r', RD, Q1);
  [-.7,0,.7].forEach(d => sens += knop(722, 264, d, RD, RL));
  // schakelneuron (groen) in de grijze stof
  let sch = dendr(790,306,-2.6,46,4,1,GD,Q2) + dendr(796,300,-1.6,40,4,1,GD,Q2) + dendr(806,312,-.5,36,3.5,1,GD,Q2) + dendr(788,322,2.8,32,3.5,0,GD,Q2);
  const schAx = bemonster(glad([[800,326],[808,360],[796,398],[772,418]],false), 30);
  sch += `<path d="${glad(schAx,false)}" fill="none" stroke="${GD}" stroke-width="5" stroke-linecap="round"/>` + soma(796, 312, 19, 'g', GD, Q2);
  [-.5,.4].forEach(d => sch += knop(772, 418, Math.PI*.82 + d, GD, GL));
  // motorisch neuron (blauw) in de voorhoorn
  let mot = dendr(742,448,-1.2,40,4.5,1,BD,Q3) + dendr(732,446,-2.2,44,4.5,1,BD,Q3) + dendr(728,464,2.6,40,4.5,1,BD,Q3) + dendr(746,470,1.6,36,4,1,BD,Q3) + dendr(756,456,.2,36,4,1,BD,Q3);
  const [mA, mAP] = myel([[722,462],[660,474],[580,454],[500,412],[440,372],[380,368],[330,392],[312,450],[310,520],[312,556]], 9, BD, BL);
  mot += mA + soma(740, 456, 21, 'b', BD, Q3);
  [[232,572],[268,600],[306,576],[344,604],[380,574],[414,604]].forEach(([x,y]) => { mot += `<path d="M312 556 C312 568 ${x} 560 ${x} ${y-8}" fill="none" stroke="${BD}" stroke-width="3.5" stroke-linecap="round"/><path d="${blob(x, y, 7, 4, Q3, 7, .1)}" fill="${BL}" stroke="${BD}" stroke-width="1.5"/>`; });
  s += mot + sch + sens;

  /* inzetjes: prikkel en reactie */
  const hand = (x, y, rot) => `<g transform="translate(${x} ${y}) rotate(${rot})"><path d="${glad([[-46,-14],[-10,-20],[22,-16],[30,-6],[30,8],[18,16],[-12,18],[-46,14]])}" fill="#f3bf9a" stroke="#c98d64" stroke-width="2"/>
    ${[-14,-5,4,13].map((dy,i)=>`<path d="M26 ${dy} H${54-Math.abs(i-1.5)*5}" stroke="#c98d64" stroke-width="10.5" stroke-linecap="round"/><path d="M26 ${dy} H${54-Math.abs(i-1.5)*5}" stroke="#f3bf9a" stroke-width="7.5" stroke-linecap="round"/>`).join('')}
    <path d="M-46 -16 H-62 V16 H-46 Z" fill="#e7a84a" stroke="#b97f26" stroke-width="2"/></g>`;
  const pan = (x, y) => `<g transform="translate(${x} ${y})"><ellipse cx="0" cy="0" rx="30" ry="9" fill="#3b3b3b"/><path d="M-30 0 V14 C-30 24 30 24 30 14 V0" fill="#2d2d2d"/><path d="M30 4 H62" stroke="#2a2a2a" stroke-width="7" stroke-linecap="round"/>${[-14,0,14].map(d=>`<path d="M${d} -12 C${d-5} -20 ${d+5} -26 ${d} -34" stroke="#ef4444" stroke-width="2" fill="none"/>`).join('')}</g>`;
  s += `<circle cx="100" cy="270" r="86" fill="#fde9b8"/>` + pan(118, 300) + hand(58, 278, 18) + `<circle cx="96" cy="292" r="9" fill="#ef4444" opacity=".5"/><text x="100" y="378" text-anchor="middle" font-size="16" font-weight="800" fill="#b91c1c">pijn</text>`;
  s += `<circle cx="100" cy="490" r="86" fill="#fde9b8"/>` + pan(118, 530) + hand(52, 470, -14) + `<path d="M146 486 C150 470 146 456 138 444" stroke="${BD}" stroke-width="3.5" fill="none" marker-end="url(#rb-pijlb)"/><text x="100" y="598" text-anchor="middle" font-size="16" font-weight="800" fill="${BD}">reactie</text>`;
  s += `<defs><marker id="rb-pijlb" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="${BD}"/></marker><marker id="rb-pijlr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="${RD}"/></marker></defs>`;
  s += `<path d="M344 190 C346 240 352 280 380 300" stroke="${RD}" stroke-width="3" fill="none" marker-end="url(#rb-pijlr)" opacity=".8"/><path d="M290 410 C280 450 278 490 282 530" stroke="${BD}" stroke-width="3" fill="none" marker-end="url(#rb-pijlb)" opacity=".8"/>`;

  /* labels */
  const lab = (x, y, tx, ty, t, kl, a='middle') => `<path d="M${x} ${y} L${tx} ${ty}" stroke="#334155" stroke-width="1.4"/><text x="${tx + (a==='start'?6:a==='end'?-6:0)}" y="${ty + (a==='middle' ? (ty>y?16:-6) : 5)}" text-anchor="${a}" font-size="17" font-weight="800" fill="${kl}" paint-order="stroke" stroke="#fbf9f6" stroke-width="4">${t}</text>`;
  s += lab(300, 100, 520, 110, 'receptoren in de huid', '#1d2a36', 'start') + lab(400, 304, 430, 214, 'sensorisch neuron', RD, 'middle') + lab(812, 304, 988, 186, 'schakelneuron', GD, 'end') + lab(560, 448, 560, 520, 'motorisch neuron', BD, 'middle') + lab(446, 640, 520, 640, 'effector: spier', '#9a3412', 'start');
  s += lab(cx+120, cy+60, 960, 520, 'grijze stof', '#9f3e33', 'end') + lab(cx+160, cy-40, 988, 96, 'witte stof', '#8a6f33', 'end') + `<text x="${cx}" y="${cy+218}" text-anchor="middle" font-size="22" font-weight="800" fill="#b45309">ruggenmerg</text>`;
  // delen van de neuronen (aan/uit)
  const deel = (x, y, tx, ty, t, a='middle') => `<path d="M${x} ${y} L${tx} ${ty}" stroke="#334155" stroke-width="1.2" stroke-dasharray="3 3"/><text x="${tx + (a==='start'?5:a==='end'?-5:0)}" y="${ty + (a==='middle' ? (ty>y?14:-5) : 4)}" text-anchor="${a}" font-size="14" font-weight="700" fill="#334155" paint-order="stroke" stroke="#fbf9f6" stroke-width="4">${t}</text>`;
  s += `<g id="rb-delen" style="display:none">` + deel(530, 232, 600, 200, 'cellichaam', 'start') + deel(314, 220, 250, 220, 'dendriet', 'end') + deel(640, 266, 640, 300, 'axon') + deel(740, 456, 640, 560, 'cellichaam', 'end') + deel(716, 420, 640, 400, 'dendrieten', 'end') + deel(500, 412, 470, 470, 'axon') + deel(380, 580, 470, 672, 'eindknopjes') + deel(796, 312, 870, 300, 'cellichaam', 'start') + `</g>`;
  S.innerHTML = s + '<g id="rb-dyn"></g>';
  const tog = $('#rb-delen-k'); if (tog) tog.onclick = () => { const g = $('#rb-delen'), aan = g.style.display === 'none'; g.style.display = aan ? '' : 'none'; tog.setAttribute('aria-pressed', aan); };

  const pad = [[300,96],[312,150], ...sDP, ...sAP, [790,306], ...schAx, [742,448], ...mAP, [312,570]];
  const n1 = 2 + sDP.length + sAP.length, n2 = n1 + 1 + schAx.length;
  const ZIN = ['De <b>receptoren</b> in je huid voelen de hitte en maken een elektrische impuls.', 'Het <b>sensorisch neuron</b> brengt de impuls naar het ruggenmerg.', 'In de grijze stof van het ruggenmerg geeft een <b>schakelneuron</b> de impuls door.', 'Het <b>motorisch neuron</b> brengt de impuls via zijn lange axon naar de spier.', 'De <b>effector</b>, je spier, trekt samen: je hand gaat weg van de pan.'];
  let t = -1, t0 = 0, fase = -1;
  $('#rb-start').onclick = () => { t = 0; };
  (function lus(ts){ requestAnimationFrame(lus); if (!zichtbaar(S)) return; const dt = ts && t0 ? Math.min(50, ts-t0)/1000 : 0; t0 = ts || 0;
    if (t < 0){ $('#rb-dyn').innerHTML = ''; return; } t += dt*.14;
    const L = pad.length - 1, i = Math.min(L, t*L); const f = i < 2 ? 0 : i < n1 ? 1 : i < n2 ? 2 : i < L-.5 ? 3 : 4;
    if (f !== fase){ fase = f; $('#rb-zin').innerHTML = `<b>${f+1}.</b> ` + ZIN[f]; }
    const p = langs(pad, Math.min(1,t)); let o = `<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="26" fill="url(#rb-gloed)"/>`;
    if (t > 1.5) t = -1;
    $('#rb-dyn').innerHTML = o; })();
})();

/* ---------- 5.3 bloedsuikerspiegel ---------- */
(function(){
  const S = $('#bs-svg'); let g = 0.9, ins = 0, glu = 0, hist = [], t0 = 0, acc = 0, opname = 0, verbruik = 0, msg = 'Kies een actie.';
  for (let i = 0; i < 240; i++) hist.push(0.9);
  $('#bs-eet').onclick = () => { opname += .9; msg = 'Je eet: glucose gaat van de darm naar het bloed.'; };
  $('#bs-sport').onclick = () => { verbruik += .6; msg = 'Je sport: je spieren verbruiken veel glucose.'; };
  (function lus(ts){ requestAnimationFrame(lus); if (!zichtbaar(S)) return; const dt = ts && t0 ? Math.min(50, ts-t0)/1000 : 0; t0 = ts || 0; if (!dt) return;
    const d1 = $('#bs-d1').checked;
    const inn = Math.min(opname, dt*.25); opname -= inn; const uit = Math.min(verbruik, dt*.18); verbruik -= uit;
    ins = d1 ? 0 : Math.max(0, (g - 1.0)) * 2.2; glu = Math.max(0, (0.8 - g)) * 2.2;
    g += inn - uit - ins*dt*.35 + glu*dt*.35 - (g-0.9)*dt*.01;
    g = Math.max(.3, Math.min(2.6, g));
    acc += dt; if (acc > .08){ acc = 0; hist.push(g); if (hist.length > 240) hist.shift(); }
    const X = i => 60 + i*2.8, Y = v => 260 - (v-0.3)/2.2*230;
    let s = `<rect width="760" height="300" rx="14" fill="#fbfaf7"/><rect x="60" y="${Y(1.1)}" width="672" height="${Y(0.7)-Y(1.1)}" fill="#dcfce7"/><text x="66" y="${Y(0.7)+16}" font-size="13" fill="#166534">normale zone: 0,7 – 1,1 g/L</text>`;
    s += `<path d="M60 20 V260 H735" stroke="#1d2a36" stroke-width="2" fill="none"/><text x="20" y="150" font-size="13" transform="rotate(-90 20 150)" text-anchor="middle">glucose in het bloed (g/L)</text><text x="735" y="285" text-anchor="end" font-size="13">tijd →</text>`;
    [0.5,1,1.5,2,2.5].forEach(v => s += `<text x="54" y="${Y(v)+4}" text-anchor="end" font-size="12">${String(v).replace('.',',')}</text><path d="M60 ${Y(v)} H735" stroke="#e5e7eb"/>`);
    s += `<path d="M${hist.map((v,i)=>`${X(i).toFixed(1)} ${Y(v).toFixed(1)}`).join(' L')}" fill="none" stroke="#c2410c" stroke-width="3.5"/>`;
    const bar = (x, v, kl, n) => `<rect x="${x}" y="30" width="16" height="70" rx="4" fill="#eee"/><rect x="${x}" y="${100-Math.min(1,v)*70}" width="16" height="${Math.min(1,v)*70}" rx="4" fill="${kl}"/><text x="${x+8}" y="118" text-anchor="middle" font-size="12" font-weight="700">${n}</text>`;
    s += bar(640, ins*1.2, '#2563eb', 'insuline') + bar(700, glu*1.2, '#9333ea', 'glucagon');
    S.innerHTML = s;
    bschActief(ins > .05 ? 'b' : glu > .05 ? 'o' : (d1 && g > 1.1) ? 'b' : ''); let z = msg; if (ins > .05) z += ' <b>De alvleesklier geeft insuline af</b>: de bloedsuikerspiegel daalt.'; else if (glu > .05) z += ' <b>De alvleesklier geeft glucagon af</b>: de lever geeft glucose af, de bloedsuikerspiegel stijgt.'; else if (d1 && g > 1.1) z += ' <b>Zonder insuline blijft de bloedsuikerspiegel te hoog.</b> Iemand met diabetes type 1 moet insuline inspuiten.'; else z += ' De bloedsuikerspiegel is normaal.';
    $('#bs-zin').innerHTML = z; })();
})();

/* ---------- oefeningen ---------- */
sorteer($('#oef-sys'), {id:'sys', titel:'Oefening 1 · Zenuwstelsel of hormoonstelsel?', opties:[{k:'z',label:'zenuwstelsel'},{k:'h',label:'hormoonstelsel'}], items:[
  {tekst:'De boodschap gaat via het bloed.', antwoord:'h'},{tekst:'De boodschap is een elektrische impuls.', antwoord:'z'},{tekst:'Het werkt zeer snel, maar kort.', antwoord:'z'},{tekst:'Het effect duurt lang.', antwoord:'h'},{tekst:'Je trekt je hand terug van een hete pan.', antwoord:'z'},{tekst:'Na een schrik blijft je hart nog lang snel kloppen.', antwoord:'h'}]});
sorteer($('#oef-czs'), {id:'czs', titel:'Oefening 2 · CZS of PZS?', opties:[{k:'c',label:'centraal zenuwstelsel'},{k:'p',label:'perifeer zenuwstelsel'}], items:[
  {tekst:'de hersenen', antwoord:'c'},{tekst:'het ruggenmerg', antwoord:'c'},{tekst:'de zenuwen in je arm', antwoord:'p'},{tekst:'de zenuw van je oog naar je hersenen', antwoord:'p'},
  {tekst:'Wat beschermt het ruggenmerg?', opties:[{k:'a',label:'de wervelkolom'},{k:'b',label:'de ribben'},{k:'c',label:'de schedel'}], antwoord:'a'},
  {tekst:'Wat vangt schokken op rond de hersenen?', opties:[{k:'a',label:'het hersenvocht'},{k:'b',label:'het bloed'},{k:'c',label:'de myelineschede'}], antwoord:'a'}]});
sorteer($('#oef-br'), {id:'br', titel:'Oefening 3 · Welk deel van de hersenen?', opties:[{k:'g',label:'grote hersenen'},{k:'k',label:'kleine hersenen'},{k:'s',label:'hersenstam'}], items:[
  {tekst:'Je bewaart je evenwicht op een fiets.', antwoord:'k'},{tekst:'Je denkt na over een vraag.', antwoord:'g'},{tekst:'Je ademhaling gaat vanzelf door als je slaapt.', antwoord:'s'},{tekst:'Je onthoudt een nieuw woord.', antwoord:'g'},{tekst:'Je slikt zonder erover na te denken.', antwoord:'s'},{tekst:'Je bewegingen zijn vloeiend.', antwoord:'k'}]});
sorteer($('#oef-neu'), {id:'neu', titel:'Oefening 4 · Het neuron', items:[
  {tekst:'Welk deel ontvangt impulsen?', opties:[{k:'a',label:'de dendrieten'},{k:'b',label:'het axon'},{k:'c',label:'de eindknopjes'}], antwoord:'a'},
  {tekst:'Welk deel geleidt de impuls weg van het cellichaam?', opties:[{k:'a',label:'het axon'},{k:'b',label:'de dendrieten'},{k:'c',label:'de kern'}], antwoord:'a'},
  {tekst:'Waarvoor dient de myelineschede?', opties:[{k:'a',label:'ze isoleert en maakt de geleiding sneller'},{k:'b',label:'ze maakt neurotransmitter'},{k:'c',label:'ze ontvangt prikkels'}], antwoord:'a'},
  {tekst:'Welk neuron brengt een impuls van een zintuig naar het CZS?', opties:[{k:'a',label:'een sensorisch neuron'},{k:'b',label:'een motorisch neuron'},{k:'c',label:'een schakelneuron'}], antwoord:'a'},
  {tekst:'Welk neuron brengt een impuls naar een spier?', opties:[{k:'a',label:'een motorisch neuron'},{k:'b',label:'een sensorisch neuron'},{k:'c',label:'een schakelneuron'}], antwoord:'a'},
  {tekst:'Waar ligt een schakelneuron?', opties:[{k:'a',label:'in het CZS'},{k:'b',label:'in een zintuig'},{k:'c',label:'in een spier'}], antwoord:'a'}]});
sorteer($('#oef-imp'), {id:'imp', titel:'Oefening 5 · Elektrisch of chemisch?', opties:[{k:'e',label:'elektrisch'},{k:'c',label:'chemisch'}], items:[
  {tekst:'De impuls loopt over het axon.', antwoord:'e'},{tekst:'Neurotransmitter gaat door de synapsspleet.', antwoord:'c'},{tekst:'De impuls springt van opening tot opening in de myelineschede.', antwoord:'e'},{tekst:'Neurotransmitter bindt op een receptor.', antwoord:'c'},
  {tekst:'Waarom kan een elektrische impuls niet over de synapsspleet?', opties:[{k:'e',label:'de neuronen raken elkaar niet'},{k:'c',label:'de spleet is vol bloed'}], antwoord:'e', uitleg:'Daarom gebeurt het doorgeven chemisch, met neurotransmitter.'}]});
sorteer($('#oef-aa'), {id:'aa', titel:'Oefening 6 · Animaal of autonoom?', opties:[{k:'an',label:'animaal'},{k:'au',label:'autonoom'}], items:[
  {tekst:'Je hart klopt sneller als je loopt.', antwoord:'au'},{tekst:'Je schrijft een bericht op je gsm.', antwoord:'an'},{tekst:'Je maag verteert je eten.', antwoord:'au'},{tekst:'Je schopt tegen een bal.', antwoord:'an'},{tekst:'Je begint te zweten in de zon.', antwoord:'au'}]});
sorteer($('#oef-rf'), {id:'rf', titel:'Oefening 7 · Reflex of bewuste beweging?', items:[
  {tekst:'Je trekt je hand terug van een hete pan.', opties:[{k:'r',label:'reflex via het ruggenmerg'},{k:'h',label:'reflex via de hersenstam'},{k:'b',label:'bewuste beweging'}], antwoord:'r'},
  {tekst:'Je knippert als er stof naar je oog vliegt.', opties:[{k:'r',label:'reflex via het ruggenmerg'},{k:'h',label:'reflex via de hersenstam'},{k:'b',label:'bewuste beweging'}], antwoord:'h'},
  {tekst:'Je steekt je hand op in de klas.', opties:[{k:'r',label:'reflex via het ruggenmerg'},{k:'h',label:'reflex via de hersenstam'},{k:'b',label:'bewuste beweging'}], antwoord:'b'},
  {tekst:'De dokter tikt onder je knie en je been schiet vooruit.', opties:[{k:'r',label:'reflex via het ruggenmerg'},{k:'h',label:'reflex via de hersenstam'},{k:'b',label:'bewuste beweging'}], antwoord:'r'},
  {tekst:'Waarom is een reflex sneller dan een bewuste beweging?', opties:[{k:'a',label:'de impuls gaat niet naar de grote hersenen'},{k:'b',label:'de impuls gaat via het bloed'},{k:'c',label:'er zijn geen neuronen nodig'}], antwoord:'a'}]});
sorteer($('#oef-zh'), {id:'zh', titel:'Oefening 8 · Bloedsuikerspiegel', items:[
  {tekst:'Na het eten stijgt je bloedsuikerspiegel. Welk hormoon geeft de alvleesklier af?', opties:[{k:'a',label:'insuline'},{k:'b',label:'glucagon'},{k:'c',label:'adrenaline'}], antwoord:'a'},
  {tekst:'Na het sporten is je bloedsuikerspiegel laag. Welk hormoon geeft de alvleesklier af?', opties:[{k:'a',label:'insuline'},{k:'b',label:'glucagon'},{k:'c',label:'thyroxine'}], antwoord:'b'},
  {tekst:'Wat doet insuline?', opties:[{k:'a',label:'de bloedsuikerspiegel daalt'},{k:'b',label:'de bloedsuikerspiegel stijgt'}], antwoord:'a'},
  {tekst:'Wat betekent homeostase?', opties:[{k:'a',label:'het lichaam houdt iets constant'},{k:'b',label:'het lichaam groeit'},{k:'c',label:'het lichaam maakt energie'}], antwoord:'a'}]});
sorteer($('#oef-bs'), {id:'bs', titel:'Oefening 9 · Welke vorm van diabetes?', opties:[{k:'1',label:'type 1'},{k:'2',label:'type 2'},{k:'z',label:'zwangerschapsdiabetes'}], items:[
  {tekst:'De alvleesklier maakt geen insuline meer.', antwoord:'1'},{tekst:'De cellen reageren minder goed op insuline.', antwoord:'2'},{tekst:'Het ontstaat tijdens de zwangerschap.', antwoord:'z'},{tekst:'De persoon moet insuline inspuiten.', antwoord:'1'},{tekst:'Meer bewegen en gezond eten helpen veel.', antwoord:'2'}]});
const som = (...k) => { const a = k.map(x=>scores[x]).filter(Boolean); if(!a.length) return null; return {juist:a.reduce((t,x)=>t+x.juist,0), totaal:k.map(x=>scores[x]?scores[x].totaal:0).reduce((t,x)=>t+x,0), klaar:k.every(x=>scores[x]&&scores[x].klaar)}; };
ikkanFn = () => { $('#ikkan').innerHTML = `<h3>Controle thema 4</h3><ul>
  ${regel('Ik leg uit hoe prikkels en reacties gecoördineerd worden door het zenuwstelsel en het hormoonstelsel.', scores.sys)}
  ${regel('Ik leg het verschil uit tussen het centrale en het perifere zenuwstelsel, en hoe hersenen en ruggenmerg beschermd worden.', scores.czs)}
  ${regel('Ik benoem en herken de grote delen van de hersenen.', scores.br)}
  ${regel('Ik herken en benoem de delen van het neuron en de soorten neuronen.', scores.neu)}
  ${regel('Ik leg uit hoe de elektrische impulsgeleiding en de chemische impulsoverdracht verlopen.', scores.imp)}
  ${regel('Ik leg het verschil uit tussen het animale en het autonome zenuwstelsel.', scores.aa)}
  ${regel('Ik leg uit hoe de informatieoverdracht verloopt bij reflexen en bij bewuste bewegingen.', scores.rf)}
  ${regel('Ik leg uit hoe de alvleesklier zorgt voor homeostase van de bloedsuikerspiegel.', scores.zh)}
  ${regel('Ik benoem de drie vormen van diabetes.', scores.bs)}</ul>`; };
updateIkKan();
'''
body = body.replace('__ZS__', img('zenuwstelsel.jpg')).replace('__BRAIN__', img('hersenen.jpg'))
pagina('biologie-zenuwstelsel.html', 'Coördinatie van reacties op prikkels', 'Biologie · 3de jaar · thema 4',
  'Je zenuwstelsel en je hormoonstelsel zorgen ervoor dat je lichaam op het juiste moment juist reageert.',
  'LPD 4B: De leerlingen lichten de overdracht van informatie via impulsgeleiding en impulsoverdracht in zenuwen toe. LPD 7B: De leerlingen leggen aan de hand van een voorbeeld uit hoe de coördinerende rol van het endocriene stelsel bij een reactie op een prikkel bijdraagt tot het functioneren van een dierlijk organisme.',
  ['Prikkel, zintuig (receptor), effector en reactie (thema 3).', 'Endocriene klieren en hormonen (thema 3, hoofdstuk 3).'],
  ('Lesdoelen thema 4 · p. 107–145', ['Ik leg uit hoe prikkels en reacties gecoördineerd worden door het zenuwstelsel en het hormoonstelsel.', 'Ik leg uit wat het verschil is tussen het centrale en het perifere zenuwstelsel.', 'Ik leg uit hoe de hersenen en het ruggenmerg beschermd worden.', 'Ik benoem en herken de grote delen van de hersenen.', 'Ik herken en benoem de delen van het neuron.', 'Ik benoem en herken de soorten neuronen.', 'Ik leg uit hoe de elektrische impulsgeleiding binnen neuronen verloopt.', 'Ik leg uit hoe de chemische impulsoverdracht tussen neuronen verloopt.', 'Ik leg uit wat het verschil is tussen het animale en het autonome zenuwstelsel.', 'Ik leg uit hoe de informatieoverdracht bij reflexen verloopt via het ruggenmerg of de hersenstam.', 'Ik leg uit hoe de informatieoverdracht bij bewuste bewegingen verloopt via de hersenen.', 'Ik leg uit wat het verschil is tussen de informatieoverdracht via het zenuw- of het hormoonstelsel.', 'Ik leg uit hoe de alvleesklier voor homeostase van de bloedsuikerspiegel zorgt.', 'Ik benoem de drie vormen van diabetes.']),
  [('lesA','1–2','Bouw van het zenuwstelsel','CZS, PZS, hersenen'),('lesB','3','Impulsen doorgeven','neuron en synaps'),('lesC','4','Reflexen en bewegingen','animaal, autonoom'),('lesD','5','Hormoonstelsel','bloedsuikerspiegel'),('lesE','✎','Oefenen','alle lesdoelen')],
  body, css, js)
