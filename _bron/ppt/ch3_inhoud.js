pres.title = 'Scheidingstechnieken';
const TECH = JSON.parse(fs.readFileSync('/home/claude/ppt/tech.json'));
(async () => {
  const BL = '2563EB', BLL = 'E3ECFD', GR = '15803D', GRL = 'E6F4EA', PA = '7C3AED', PAL = 'EDE7FB', TE = '0F766E', TEL = 'DDF3F0';
  const EIGK = { 'deeltjesgrootte': [K.groen, K.mint], 'massadichtheid': [BL, BLL], 'kooktemperatuur': ['B91C1C', 'FDE8E8'], 'oplosbaarheid': [GR, GRL], 'adsorptievermogen': [PA, PAL] };


  // 1 TITEL
  pres.addSection({ title: 'Start' });
  let s = pres.addSlide({ masterName: 'TITEL', sectionTitle: 'Start' });
  s.addText('Chemie 3de jaar · Thema 1 · Hoofdstuk 3', { placeholder: 'kicker' });
  s.addText('Scheidingstechnieken', { placeholder: 'title' });
  s.addText('Hoe haal je de bestanddelen van een mengsel weer uit elkaar?', { placeholder: 'sub' });

  // 2 LESDOELEN
  s = nieuw('Lesdoelen', 'Na dit hoofdstuk kan je …', 'Start');
  [['3.1', 'p. 31', 'de definitie van **scheidingstechniek** noteren'],
   ['3.2', 'p. 32', 'het principe van **zeven, decanteren, filtreren en centrifugeren** uitleggen met een tekening, de stofeigenschap noteren en de onderdelen benoemen'],
   ['3.3', 'p. 35', 'het principe van **uitdampen, destilleren, extraheren en adsorberen** uitleggen met een tekening, de stofeigenschap noteren en de onderdelen benoemen'],
   ['Σ', 'p. 35 en 40', 'bij een voorbeeld uit het **dagelijks leven** de scheidingstechniek noteren']]
    .forEach(([n, p, t], i) => {
      const y = 1.6 + i * 1.33;
      s.addText([{ text: n === 'Σ' ? 'Overzicht' : 'Lesdoel ' + n, options: { bold: true, color: K.groen, fontSize: 17, breakLine: true } }, { text: p, options: { color: K.grijs, fontSize: 14 } }],
        { x: 0.6, y, w: 1.9, h: 1.15, margin: 0, valign: 'middle', isTextBox: true, objectName: nm(i + 1) });
      kaart(s, i + 1, 2.6, y, 10.1, 1.15, '', md('Ik kan ' + t + '.'), { fs: 17 });
    });

  // 3 WAAROM SCHEIDEN
  pres.addSection({ title: '3.1 Scheiden van mengsels' });
  const S1 = '3.1 Scheiden van mengsels';
  s = nieuw('Lesdoel 3.1 · Scheiden van mengsels', 'Waarom kan je een mengsel scheiden?', S1);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.15, x: 0.6, y: 1.65, w: 6.3, h: 4.6, fill: { color: 'F4F6F8' }, line: { color: 'F4F6F8' }, objectName: vast() });
  { const p = png('sch/magneet'); s.addImage({ path: p.path, x: 0.9, y: 2.2, w: 5.7, h: 5.7 / p.r, objectName: vast(), altText: 'magneet boven zand met ijzervijlsel' }); }
  kaart(s, 1, 7.2, 1.65, 5.5, 1.45, 'In een mengsel', md('houdt elk bestanddeel zijn **eigen stofeigenschappen**.'), { fs: 17 });
  kaart(s, 2, 7.2, 3.3, 5.5, 1.45, 'Voorbeeld', md('IJzer blijft **magnetisch**, ook als het met zand gemengd is. Zand is niet magnetisch.'), { fs: 17 });
  s.addText([{ text: 'Dus ', options: { bold: true, color: K.lab } }, { text: 'hebben twee bestanddelen een verschillende stofeigenschap? Dan kan je ze daarmee scheiden.', options: { color: K.wit } }],
    { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 7.2, y: 4.95, w: 5.5, h: 1.3, fill: { color: K.donker }, line: { color: K.donker }, fontSize: 17, margin: [4, 14, 4, 14], valign: 'middle', objectName: nm(3) });

  // 4 DEFINITIE
  s = nieuw('Lesdoel 3.1 · Scheiden van mengsels', 'De definitie', S1);
  s.addText('Vul samen aan. Welk woord past?', { x: 0.6, y: 1.55, w: 12.1, h: 0.45, fontSize: 18, italic: true, color: K.grijs, margin: 0, isTextBox: true, objectName: vast() });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.12, x: 0.6, y: 2.2, w: 12.1, h: 1.7, fill: { color: K.licht }, line: { color: K.licht }, objectName: vast() });
  s.addText([{ text: 'Een ' }, { text: 'scheidingstechniek', options: { bold: true } }, { text: ' is een  (1)\u00a0………………  om de  (2)\u00a0………………  van een  (3)\u00a0………………  van elkaar te scheiden. Ze is gebaseerd op een verschil in een  (4)\u00a0……………… .' }],
    { x: 0.95, y: 2.3, w: 11.4, h: 1.5, fontSize: 24, color: K.tekst, valign: 'middle', margin: 0, isTextBox: true, objectName: vast() });
  ['methode', 'bestanddelen', 'mengsel', 'stofeigenschap'].forEach((w, i) => {
    const x = 0.6 + i * 3.08;
    nummer(s, i + 1, x, 4.08, i + 1, K.groen, 0.5);
    chip(s, i + 1, x + 0.6, 4.0, 2.25, 0.66, w, K.groen, K.mint, 18);
  });
  kaart(s, 5, 0.6, 5.2, 5.95, 1.55, 'Heterogeen mengsel', 'zeven, decanteren, filtreren of centrifugeren (3.2)', { fs: 17, fill: BLL, kleur: BL });
  kaart(s, 6, 6.75, 5.2, 5.95, 1.55, 'Homogeen mengsel', 'uitdampen, destilleren, extraheren of adsorberen (3.3)', { fs: 17, fill: GRL, kleur: GR });

  // 5-12 TECHNIEKEN
  const techSlide = (key, sectie, kicker) => {
    const T = TECH[key];
    const s = nieuw(kicker, T.naam, sectie);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.15, x: 0.6, y: 1.6, w: 6.6, h: 5.2, fill: { color: 'F4F6F8' }, line: { color: 'F4F6F8' }, objectName: vast() });
    const p = png('sch/' + key); const w = Math.min(6.3, 4.9 * p.r);
    s.addImage({ path: p.path, x: 0.6 + (6.6 - w) / 2, y: 1.75, w, h: w / p.r, objectName: vast(), altText: 'opstelling ' + T.naam });
    s.addText([{ text: 'Mengsel  ', options: { bold: true, color: K.grijs } }, { text: T.mengsel, options: { color: K.tekst } }], { x: 7.5, y: 1.55, w: 5.2, h: 0.6, fontSize: 14, margin: 0, valign: 'middle', isTextBox: true, objectName: vast() });
    T.caps.forEach((c, i) => { kaart(s, i + 1, 8.1, 2.25 + i * 1.05, 4.6, 0.95, '', c, { fs: 14 }); nummer(s, i + 1, 7.5, 2.48 + i * 1.05, i + 1, K.groen, 0.45); });
    const eig = T.eig.replace('verschil in ', '').replace(/ \(.*\)/, '');
    const kk = EIGK[Object.keys(EIGK).find(k => eig.startsWith(k))];
    s.addText([{ text: 'Gebaseerd op een verschil in ', options: { color: K.tekst } }, { text: eig, options: { bold: true, color: kk[0] } }],
      { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 7.5, y: 5.45, w: 5.2, h: 0.62, fill: { color: kk[1] }, line: { color: kk[1] }, fontSize: 15, margin: [2, 10, 2, 10], valign: 'middle', objectName: nm(4) });
    s.addText([{ text: 'In het dagelijks leven: ', options: { bold: true, color: K.groen } }, { text: T.vb, options: { color: K.tekst } }],
      { x: 7.5, y: 6.15, w: 5.2, h: 0.7, fontSize: 14, margin: 0, valign: 'top', isTextBox: true, objectName: nm(5) });
  };
  pres.addSection({ title: '3.2 Heterogene mengsels' });
  ['zeven', 'decanteren', 'filtreren', 'centrifugeren'].forEach(k => techSlide(k, '3.2 Heterogene mengsels', 'Lesdoel 3.2 · Heterogene mengsels scheiden'));
  pres.addSection({ title: '3.3 Homogene mengsels' });
  ['uitdampen', 'destilleren', 'extraheren', 'adsorberen'].forEach(k => techSlide(k, '3.3 Homogene mengsels', 'Lesdoel 3.3 · Homogene mengsels scheiden'));

  // 13 OVERZICHT
  pres.addSection({ title: 'Overzicht en oefenen' });
  const S4 = 'Overzicht en oefenen';
  s = nieuw('Overzicht', 'Op welke stofeigenschap?', S4);
  [['deeltjesgrootte', 'zeven, filtreren'], ['massadichtheid', 'decanteren, centrifugeren'], ['kooktemperatuur', 'uitdampen, destilleren'], ['oplosbaarheid', 'extraheren'], ['adsorptievermogen', 'adsorberen']]
    .forEach(([e, t], i) => {
      const y = 1.65 + i * 1.0, [kl, fl] = EIGK[e];
      s.addText('verschil in ' + e, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 0.6, y, w: 4.6, h: 0.85, fill: { color: fl }, line: { color: fl }, fontSize: 18, bold: true, color: kl, valign: 'middle', margin: [2, 14, 2, 14], objectName: vast() });
      s.addShape(pres.shapes.RIGHT_ARROW, { x: 5.4, y: y + 0.24, w: 0.6, h: 0.38, fill: { color: K.grijs }, line: { color: K.grijs }, objectName: nm(i + 1) });
      s.addText(t, { x: 6.2, y, w: 6.5, h: 0.85, fontSize: 22, bold: true, color: K.tekst, valign: 'middle', margin: 0, isTextBox: true, objectName: nm(i + 1) });
    });
  s.addText('adsorptievermogen = hoe goed een stof aan actieve kool blijft hangen', { x: 0.6, y: 6.6, w: 12.1, h: 0.35, fontSize: 13, italic: true, color: K.grijs, margin: 0, isTextBox: true, objectName: vast() });

  // SCHEIDEN IN BRUSSEL
  const bxl = (titel, plaats, zinnen, vraag, antw, slot) => {
    const s = nieuw('In Brussel · ' + plaats, titel, S4);
    zinnen.forEach((z, i) => { kaart(s, 0, 0.6, 1.6 + i * 0.95, 6.3, 0.85, '', md(z), { fs: 16 }); });
    s.addText([{ text: 'Denk na  ', options: { bold: true, color: K.amber } }, { text: vraag, options: { color: K.tekst } }],
      { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 7.2, y: 1.6, w: 5.5, h: 1.3, fill: { color: K.amberL }, line: { color: K.amberL }, fontSize: 17, margin: [6, 14, 6, 14], valign: 'middle', objectName: vast() });
    antw.forEach(([wat, tech], i) => {
      const e = TECH[tech].eig.replace('verschil in ', '').replace(/ \(.*\)/, ''); const kk = EIGK[Object.keys(EIGK).find(k => e.startsWith(k))];
      kaart(s, i + 1, 7.2, 3.1 + i * 1.05, 5.5, 0.92, tech, wat + ' · ' + e, { fs: 15, fill: kk[1], kleur: kk[0], inline: false });
    });
    if (slot) s.addText(slot, { x: 7.2, y: 3.1 + antw.length * 1.05, w: 5.5, h: 0.7, fontSize: 14, italic: true, color: K.grijs, margin: 0, isTextBox: true, objectName: nm(antw.length + 1) });
  };
  bxl('Waterzuiveringsstation Brussel-Noord', 'Haren', [
    'Het grootste zuiveringsstation van België zuivert het afvalwater van het **grootste deel van Brussel**.',
    '**Roosters** houden grof afval tegen, zoals takken en plastic.',
    'Het **zand** zakt naar de bodem; het **vet** dat bovenaan drijft, wordt afgeschept.',
    'Bacteriën breken opgeloste vuilstoffen af. Het slib laat men **bezinken**.',
    'Het gezuiverde water gaat naar de **Zenne**.'],
    'Welke scheidingstechnieken herken je? Op welke stofeigenschap zijn ze gebaseerd?',
    [['roosters', 'zeven'], ['zand en vet', 'decanteren'], ['slib laten bezinken', 'decanteren']],
    'Het werk van de bacteriën is geen scheidingstechniek: daar ontstaan nieuwe stoffen.');
  bxl('Kraantjeswater van Vivaqua', 'drinkwater', [
    'Een deel van het Brusselse kraantjeswater komt uit de **Maas**.',
    'In de fabriek van **Tailfer** maakt Vivaqua er drinkwater van.',
    'Een van de stappen: een filter met **actieve kool**. Resten van vervuiling en pesticiden blijven eraan hangen.'],
    'Welke techniek is dit? Waarom is gewoon filtreren niet genoeg?',
    [['vervuiling aan actieve kool', 'adsorberen']],
    'De pesticiden zijn opgelost: een homogeen mengsel. Filtreerpapier houdt ze niet tegen.');
  bxl('Brouwerij Cantillon', 'Anderlecht', [
    'Cantillon is de laatste brouwerij in Brussel die nog **lambiek** brouwt zoals vroeger.',
    'Het brouwen begint met gemalen graan en **heet water**.',
    'De **suikers** uit het graan lossen op: zo ontstaat de **wort**.',
    'Daarna haalt men de vaste **graanresten** uit de wort.'],
    'Welke twee scheidingstechnieken gebruikt de brouwer?',
    [['suikers oplossen in heet water', 'extraheren'], ['graanresten tegenhouden', 'filtreren']], '');

  const C = (t) => { const e = TECH[t.toLowerCase()].eig.replace('verschil in ', ''); const kk = EIGK[Object.keys(EIGK).find(k => e.startsWith(k))]; return [t.toLowerCase(), kk[0], kk[1]]; };
  // 14 OEFENING MET FOTO'S
  const FOTO = JSON.parse(fs.readFileSync('/home/claude/ppt/foto_data.json')).map(([techniek, tekst]) => ({ techniek, tekst }));
  const ICO = { zeven: 'GiFlour', filtreren: 'GiCoffeeCup', decanteren: 'GiWineBottle', centrifugeren: 'GiTestTubes', uitdampen: 'GiSaltShaker', destilleren: 'GiBottleVapors', extraheren: 'GiTeapot', adsorberen: 'GiWaterBottle' };
  s = nieuw('Oefening', 'Welke scheidingstechniek?', S4);
  s.addText('Welke scheidingstechniek hoort hierbij? Denk eerst zelf.', { x: 0.6, y: 1.5, w: 12.1, h: 0.4, fontSize: 17, italic: true, color: K.grijs, margin: 0, isTextBox: true, objectName: vast() });
  for (const [i, f] of FOTO.entries()) {
    const x = 0.6 + (i % 4) * 3.08, y = 2.0 + Math.floor(i / 4) * 2.5, w = 2.85, h = 1.55;
    const foto = '/home/claude/ppt/foto/' + f.techniek + '.jpg';
    if (fs.existsSync(foto)) s.addImage({ path: foto, x, y, w, h, sizing: { type: 'cover', w, h }, objectName: vast(), altText: f.tekst });
    else {
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.1, x, y, w, h, fill: { color: 'F4F6F8' }, line: { color: 'F4F6F8' }, objectName: vast() });
      s.addImage({ data: await icoon(ICO[f.techniek], '475569'), x: x + w / 2 - 0.5, y: y + 0.27, w: 1.0, h: 1.0, objectName: vast(), altText: f.tekst });
    }
    s.addText(f.tekst, { x, y: y + 1.6, w: 1.6, h: 0.42, fontSize: 15, bold: true, color: K.tekst, valign: 'middle', margin: 0, isTextBox: true, objectName: vast() });
    const kk = C(f.techniek[0].toUpperCase() + f.techniek.slice(1));
    chip(s, i + 1, x + 1.55, y + 1.62, 1.3, 0.38, kk[0], kk[1], kk[2], 12);
  }

  // 15-17 CHALLENGE IN HET KLEIN
  const KETENS = [
    ['Uitdaging 1 · Zuiver zout', 'water, zout, zand en kiezels', 'zuiver zout overhouden',
     [['zeven', 'kiezels eruit'], ['filtreren', 'zand eruit'], ['uitdampen', 'water verdampt, zout blijft']]],
    ['Uitdaging 2 · Helder water uit de vijver', 'bruin vijverwater met modder; het ruikt vreemd', 'helder water zonder kleur of geur',
     [['decanteren', 'modder bezinkt, water afgieten'], ['filtreren', 'fijne deeltjes eruit'], ['adsorberen', 'kleur en geur aan actieve kool']]],
    ['Uitdaging 3 · Drinkwater uit zee', 'troebel zeewater met schelpjes en zand', 'zuiver drinkwater',
     [['zeven', 'schelpjes eruit'], ['filtreren', 'zand eruit'], ['destilleren', 'zuiver water als destillaat, zout blijft']]]];
  KETENS.forEach(([titel, mengsel, doel, stappen]) => {
    s = nieuw('Challenge in het klein · drie technieken na elkaar', titel, S4);
    s.addText([{ text: 'Mengsel  ', options: { bold: true, color: K.groen } }, { text: mengsel, options: { breakLine: true } }, { text: 'Doel  ', options: { bold: true, color: K.groen } }, { text: doel }],
      { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 0.6, y: 1.6, w: 12.1, h: 1.15, fill: { color: K.licht }, line: { color: K.licht }, fontSize: 20, color: K.tekst, margin: [6, 16, 6, 16], valign: 'middle', objectName: vast() });
    s.addText('Welke drie scheidingstechnieken gebruik je, en in welke volgorde? Wat haal je er bij elke stap uit?', { x: 0.6, y: 2.9, w: 12.1, h: 0.4, fontSize: 16, italic: true, color: K.grijs, margin: 0, isTextBox: true, objectName: vast() });
    stappen.forEach(([tech, wat], j) => {
      const x = 0.6 + j * 4.15, kk = C(tech[0].toUpperCase() + tech.slice(1)), st = j + 1;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.12, x, y: 3.45, w: 3.75, h: 3.35, fill: { color: 'F4F6F8' }, line: { color: 'F4F6F8' }, objectName: vast() });
      nummer(s, 0, x + 0.2, 3.6, j + 1, K.grijs, 0.5);
      if (j < 2) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 3.78, y: 4.9, w: 0.34, h: 0.4, fill: { color: K.grijs }, line: { color: K.grijs }, objectName: vast() });
      const p = png('sch/' + tech + '_eind'); const w = 2.6, h = w / p.r;
      s.addImage({ path: p.path, x: x + (3.75 - w) / 2, y: 3.75, w, h, objectName: nm(st), altText: tech });
      s.addText(tech, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.15, x: x + 0.3, y: 5.5, w: 3.15, h: 0.5, fill: { color: kk[2] }, line: { color: kk[2] }, fontSize: 18, bold: true, color: kk[1], align: 'center', valign: 'middle', margin: 0, objectName: nm(st) });
      s.addText(wat, { x: x + 0.2, y: 6.05, w: 3.35, h: 0.65, fontSize: 15, color: K.tekst, align: 'center', valign: 'top', margin: 0, isTextBox: true, objectName: nm(st) });
    });
  });

  // 15 SAMENVATTING
  pres.addSection({ title: 'Samenvatting' });
  s = pres.addSlide({ masterName: 'TITEL', sectionTitle: 'Samenvatting' });
  s.addText('Samenvatting', { x: 0.6, y: 0.4, w: 12, h: 0.8, fontSize: 36, bold: true, color: K.wit, margin: 0, isTextBox: true, objectName: vast() });
  [['Scheidingstechniek', 'methode om de bestanddelen van een mengsel te scheiden, op basis van een verschil in een stofeigenschap'],
   ['Heterogeen mengsel', 'zeven, decanteren, filtreren, centrifugeren'], ['Homogeen mengsel', 'uitdampen, destilleren, extraheren, adsorberen'],
   ['Deeltjesgrootte', 'zeven, filtreren'], ['Massadichtheid', 'decanteren, centrifugeren'], ['Kooktemperatuur', 'uitdampen, destilleren'],
   ['Oplosbaarheid', 'extraheren'], ['Adsorptievermogen', 'adsorberen']]
    .forEach(([t, u], i) => {
      const x = 0.6 + (i % 2) * 6.2, y = 1.45 + Math.floor(i / 2) * 1.4;
      s.addText([{ text: t, options: { bold: true, color: K.lab, fontSize: 18, breakLine: true } }, { text: u, options: { color: K.wit, fontSize: 15 } }],
        { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x, y, w: 5.9, h: 1.2, fill: { color: K.kaartD }, line: { color: K.kaartD }, margin: [6, 14, 6, 14], valign: 'middle', objectName: nm(i + 1) });
    });

  await pres.writeFile({ fileName: UIT });
  await applyTheme(UIT, THEME);
  await animeer(UIT);
  console.log('ok');
})();
