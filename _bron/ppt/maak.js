const pptxgen = require('pptxgenjs');
const fs = require('fs');
const React = require('react');
const RDS = require('react-dom/server');
const sharp = require('sharp');
const FA = require('react-icons/fa');
const JSZip = require('/opt/npm-tools/node_modules/jszip');
const { applyTheme } = require('/root/.claude/skills/synced/1fe33a63-f4ea-4cfc-950e-0e79e049737b_a8573341-fcc3-4e00-a94c-615572386dea/pptx/scripts/apply_theme.js');

const UIT = '/home/claude/ppt/Waterhuishouding_planten.pptx';
const THEME = {
  name: 'Waterhuishouding', headFontFace: 'Calibri', bodyFontFace: 'Calibri',
  colors: { dk1: '1D2A36', lt1: 'FFFFFF', dk2: '1F4D2B', lt2: 'EEF6EC', accent1: '3E8E41', accent2: '2563EB', accent3: 'D97706',
    accent4: '7AB55C', accent5: 'B91C1C', accent6: '51606E', hlink: '2563EB', folHlink: '1F4D2B' }
};
const K = { donker: '1F4D2B', groen: '3E8E41', licht: 'EEF6EC', mint: 'DDEED8', water: '2563EB', waterL: 'E3ECFD', amber: 'B45309', amberL: 'FDF0DC', tekst: '1D2A36', grijs: '51606E', wit: 'FFFFFF', rood: 'B91C1C' };

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'Homeostase van de waterhuishouding in planten';
pres.author = 'Biologie 3de jaar';
const C = pres.SchemeColor;

// ---------- lay-outs ----------
pres.defineSlideMaster({ title: 'TITEL', background: { color: K.donker }, objects: [
  { placeholder: { options: { name: 'kicker', type: 'body', x: 0.9, y: 2.0, w: 11.5, h: 0.5, fontSize: 18, color: 'BFE3B8', bold: true, margin: 0 }, text: '' } },
  { placeholder: { options: { name: 'title', type: 'title', x: 0.9, y: 2.55, w: 11.5, h: 1.9, fontSize: 48, bold: true, color: K.wit, valign: 'top', align: 'left', margin: 0 }, text: '' } },
  { placeholder: { options: { name: 'sub', type: 'body', x: 0.9, y: 4.6, w: 11.5, h: 0.9, fontSize: 20, color: 'DDEED8', valign: 'top', margin: 0 }, text: '' } },
] });
pres.defineSlideMaster({ title: 'INHOUD', background: { color: K.wit }, margin: [0.5, 0.6, 0.6, 0.6], objects: [
  { placeholder: { options: { name: 'kicker', type: 'body', x: 0.6, y: 0.32, w: 10, h: 0.36, fontSize: 14, color: K.groen, bold: true, margin: 0 }, text: '' } },
  { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.68, w: 12.1, h: 0.7, fontSize: 32, bold: true, color: K.donker, valign: 'top', align: 'left', margin: 0 }, text: '' } },
  { text: { text: 'Biologie 3 · Waterhuishouding in planten', options: { x: 0.6, y: 7.08, w: 6, h: 0.3, fontSize: 10, color: '8A96A3', margin: 0 } } },
], slideNumber: { x: 12.25, y: 7.08, w: 0.5, h: 0.3, fontSize: 10, color: '8A96A3', align: 'right' } });

// ---------- hulpfuncties ----------
const png = f => { const b = fs.readFileSync('/home/claude/ppt/fig/' + f + '.png'); return { path: '/home/claude/ppt/fig/' + f + '.png', r: b.readUInt32BE(16) / b.readUInt32BE(20) }; };
async function icoon(naam, kleur) {
  const svg = RDS.renderToStaticMarkup(React.createElement(FA[naam], { color: '#' + kleur, size: 256 }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return 'image/png;base64,' + buf.toString('base64');
}
let naamTeller = 0;
const nm = stap => `a${stap}-${++naamTeller}`;      // stap 0 = meteen zichtbaar
const vast = () => `v-${++naamTeller}`;

function nieuw(kicker, titel, sectie) {
  const s = pres.addSlide({ masterName: 'INHOUD', sectionTitle: sectie });
  s.addText(kicker, { placeholder: 'kicker' });
  s.addText(titel, { placeholder: 'title' });
  return s;
}
function fig(s, f, x, y, w, stap = 0, bijschrift) {
  const p = png(f); const h = w / p.r;
  s.addImage({ path: p.path, x, y, w, h, objectName: stap ? nm(stap) : vast(), altText: bijschrift || f });
  if (bijschrift) s.addText(bijschrift, { x, y: y + h + 0.05, w, h: 0.3, fontSize: 10, italic: true, color: K.grijs, margin: 0, isTextBox: true, objectName: stap ? nm(stap) : vast() });
  return h;
}
// kaart met vetgedrukte term en uitleg
function kaart(s, stap, x, y, w, h, term, uitleg, o = {}) {
  const fill = o.fill || K.licht, kleur = o.kleur || K.groen, fs = o.fs || 16;
  const runs = term ? [{ text: term, options: { bold: true, color: kleur, fontSize: fs + 1, breakLine: !o.inline } }] : [];
  if (term && o.inline) runs.push({ text: '  ' });
  (Array.isArray(uitleg) ? uitleg : [{ text: uitleg }]).forEach(r => runs.push({ text: r.text, options: { fontSize: fs, color: K.tekst, bold: !!r.b } }));
  s.addText(runs, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x, y, w, h, fill: { color: fill }, line: { color: fill }, margin: [6, 12, 6, 12], valign: 'middle', objectName: nm(stap) });
}
function nummer(s, stap, x, y, n, kleur = K.groen, d = 0.5) {
  s.addText(String(n), { shape: pres.shapes.OVAL, x, y, w: d, h: d, fill: { color: kleur }, line: { color: kleur }, color: K.wit, bold: true, fontSize: 16, align: 'center', valign: 'middle', margin: 0, objectName: nm(stap) });
}
// uitleg met **vet** markeringen
const md = t => t.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map(p => p.startsWith('**') ? { text: p.slice(2, -2), b: true } : { text: p });

function denkvraag(kicker, titel, sectie, vraag, stappen, besluit) {
  const s = nieuw(kicker, titel, sectie);
  s.addText([{ text: 'Denkvraag  ', options: { bold: true, color: K.amber } }, { text: vraag, options: { color: K.tekst } }],
    { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 0.6, y: 1.6, w: 12.1, h: 1.25, fill: { color: K.amberL }, line: { color: K.amberL }, fontSize: 20, margin: [8, 16, 8, 16], valign: 'middle', objectName: vast() });
  s.addText('Denk eerst zelf na. Bespreek daarna met je buur.', { x: 0.6, y: 2.95, w: 12.1, h: 0.35, fontSize: 14, italic: true, color: K.grijs, margin: 0, isTextBox: true, objectName: vast() });
  const w = (12.1 - 2 * 0.3) / 3;
  stappen.forEach(([kop, txt], i) => {
    const x = 0.6 + i * (w + 0.3);
    kaart(s, i + 1, x, 3.5, w, 2.05, kop, md(txt), { fs: 16 });
    nummer(s, i + 1, x + w - 0.62, 3.6, i + 1, K.groen, 0.45);
  });
  s.addText([{ text: 'Besluit  ', options: { bold: true, color: 'BFE3B8' } }, { text: besluit, options: { color: K.wit } }],
    { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 0.6, y: 5.8, w: 12.1, h: 0.95, fill: { color: K.donker }, line: { color: K.donker }, fontSize: 19, margin: [6, 16, 6, 16], valign: 'middle', objectName: nm(4) });
  return s;
}

(async () => {
  const I = {
    tint: await icoon('FaTint', K.water), pijl: await icoon('FaLongArrowAltUp', K.groen), wind: await icoon('FaWind', K.water),
    zon: await icoon('FaSun', 'D97706'), maan: await icoon('FaMoon', '475569'), droog: await icoon('FaTintSlash', K.rood), lamp: await icoon('FaLightbulb', 'D97706'),
  };

  // 1 TITEL
  pres.addSection({ title: 'Start' });
  let s = pres.addSlide({ masterName: 'TITEL', sectionTitle: 'Start' });
  s.addText('Biologie 3de jaar · Thema 1 Feedbacksystemen · Hoofdstuk 1', { placeholder: 'kicker' });
  s.addText('Homeostase van de waterhuishouding in planten', { placeholder: 'title' });
  s.addText('Hoe neemt een plant water op, hoe vervoert ze het en hoe houdt ze alles in evenwicht?', { placeholder: 'sub' });

  // 2 LESDOELEN
  s = nieuw('Lesdoelen', 'Na dit hoofdstuk kan je …', 'Start');
  const doelen = ['uitleggen wat **waterhuishouding** bij planten is', '**wortel, stengel, blad en bloem** benoemen als plantenorganen',
    'de **weefsels** van blad, stengel en wortel herkennen en hun functie geven', 'uitleggen hoe **huidmondjes** openen en sluiten (vacuole, turgor)',
    'zeggen wat **assimilaten** zijn', 'het **water- en assimilatentransport** uitleggen',
    '**houtvaten, zeefvaten en deelweefsel** tekenen', 'uitleggen hoe de plant haar water in **evenwicht** houdt'];
  doelen.forEach((d, i) => {
    const kol = i < 4 ? 0 : 1, rij = i % 4, x = 0.6 + kol * 6.2, y = 1.65 + rij * 1.3;
    kaart(s, i + 1, x + 0.7, y, 5.25, 1.1, '', md(d), { fs: 17 });
    nummer(s, i + 1, x, y + 0.27, i + 1);
  });

  // 3 VOORKENNIS: plantencel
  pres.addSection({ title: 'Voorkennis' });
  s = nieuw('Voorkennis', 'De plantencel', 'Voorkennis');
  fig(s, 'cel', 0.4, 2.3, 6.6);
  [['celwand', 'stevige buitenwand: geeft de cel haar vorm'], ['celmembraan', 'vlies binnen de celwand: bepaalt wat de cel in- en uitgaat'],
   ['vacuole', 'grote blaas met celvocht, vooral water'], ['bladgroenkorrels', 'hier gebeurt de fotosynthese'], ['celkern', 'stuurt de werking van de cel']]
    .forEach(([t, u], i) => kaart(s, i + 1, 7.3, 1.6 + i * 1.03, 5.4, 0.9, t, u, { fs: 15 }));

  // 4 VOORKENNIS: cel tot organisme + fotosynthese
  s = nieuw('Voorkennis', 'Van cel tot organisme, en fotosynthese', 'Voorkennis');
  ['cel', 'weefsel', 'orgaan', 'organisme'].forEach((t, i) => {
    const x = 0.6 + i * 3.15;
    s.addText(t, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x, y: 1.7, w: 2.5, h: 0.9, fill: { color: i === 3 ? K.groen : K.mint }, line: { color: i === 3 ? K.groen : K.mint }, fontSize: 22, bold: true, color: i === 3 ? K.wit : K.donker, align: 'center', valign: 'middle', objectName: nm(i + 1) });
    if (i < 3) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 2.6, y: 1.97, w: 0.45, h: 0.36, fill: { color: K.groen }, line: { color: K.groen }, objectName: nm(i + 2) });
  });
  kaart(s, 5, 0.6, 2.9, 5.95, 1.2, 'Weefsel', 'een groep gelijke cellen met dezelfde functie', { fs: 17 });
  kaart(s, 5, 6.75, 2.9, 5.95, 1.2, 'Orgaan', 'opgebouwd uit verschillende weefsels die samenwerken', { fs: 17 });
  s.addText('Fotosynthese', { x: 0.6, y: 4.45, w: 6, h: 0.45, fontSize: 20, bold: true, color: K.donker, margin: 0, isTextBox: true, objectName: nm(6) });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.1, x: 0.6, y: 5.0, w: 12.1, h: 1.6, fill: { color: K.licht }, line: { color: K.licht }, objectName: nm(6) });
  s.addText('koolstofdioxide + water', { x: 0.9, y: 5.3, w: 4.4, h: 1.0, fontSize: 24, bold: true, color: K.tekst, align: 'right', valign: 'middle', margin: 0, isTextBox: true, objectName: nm(6) });
  s.addShape(pres.shapes.RIGHT_ARROW, { x: 5.55, y: 5.62, w: 2.2, h: 0.4, fill: { color: K.groen }, line: { color: K.groen }, objectName: nm(6) });
  s.addText('licht, bladgroen', { x: 5.3, y: 5.15, w: 2.7, h: 0.4, fontSize: 15, italic: true, color: K.groen, align: 'center', margin: 0, isTextBox: true, objectName: nm(6) });
  s.addText('glucose + zuurstof', { x: 8.0, y: 5.3, w: 4.4, h: 1.0, fontSize: 24, bold: true, color: K.tekst, valign: 'middle', margin: 0, isTextBox: true, objectName: nm(6) });

  // 5 VOORKENNIS: osmose
  s = nieuw('Voorkennis', 'Osmose', 'Voorkennis');
  fig(s, 'osmose', 0.5, 2.0, 7.0);
  kaart(s, 1, 7.9, 1.75, 4.8, 1.75, 'Osmose', md('water gaat door het celmembraan naar de kant met de **meeste opgeloste stoffen**'), { fs: 17 });
  kaart(s, 2, 7.9, 3.7, 4.8, 1.45, 'Water erin', md('de vacuole zwelt en drukt tegen de celwand: de cel wordt **stevig**'), { fs: 17, fill: K.waterL, kleur: K.water });
  kaart(s, 3, 7.9, 5.35, 4.8, 1.3, 'Waarom kennen?', 'dit heb je nodig om de huidmondjes te begrijpen', { fs: 17, fill: K.amberL, kleur: K.amber });

  // 6 DEEL 1: wat is waterhuishouding
  pres.addSection({ title: 'Deel 1 · Plantenorganen' });
  s = nieuw('Deel 1 · Waterhuishouding en plantenorganen', 'Wat is waterhuishouding?', 'Deel 1 · Plantenorganen');
  s.addText('Een plant neemt voortdurend water op en verliest ook voortdurend water.', { x: 0.6, y: 1.55, w: 12.1, h: 0.5, fontSize: 19, color: K.tekst, margin: 0, isTextBox: true, objectName: vast() });
  [['opname', 'de wortel neemt water en mineralen op uit de bodem', I.tint], ['transport', 'de stengel vervoert het water naar boven', I.pijl], ['afgifte', 'het blad geeft waterdamp af', I.wind]].forEach(([t, u, ic], i) => {
    const x = 0.6 + i * 4.15;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.12, x, y: 2.3, w: 3.8, h: 2.55, fill: { color: K.licht }, line: { color: K.licht }, objectName: nm(i + 1) });
    s.addShape(pres.shapes.OVAL, { x: x + 0.3, y: 2.55, w: 0.95, h: 0.95, fill: { color: K.wit }, line: { color: K.mint }, objectName: nm(i + 1) });
    s.addImage({ data: ic, x: x + 0.52, y: 2.77, w: 0.51, h: 0.51, objectName: nm(i + 1) });
    s.addText(t, { x: x + 1.4, y: 2.6, w: 2.3, h: 0.85, fontSize: 26, bold: true, color: K.donker, valign: 'middle', margin: 0, isTextBox: true, objectName: nm(i + 1) });
    s.addText(u, { x: x + 0.3, y: 3.65, w: 3.3, h: 1.05, fontSize: 17, color: K.tekst, valign: 'top', margin: 0, isTextBox: true, objectName: nm(i + 1) });
  });
  s.addText([{ text: 'Definitie  ', options: { bold: true, color: 'BFE3B8' } }, { text: 'Waterhuishouding is de manier waarop een plant water opneemt, vervoert en afgeeft, zodat er altijd genoeg water in de plant is.', options: { color: K.wit } }],
    { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 0.6, y: 5.2, w: 12.1, h: 1.3, fill: { color: K.donker }, line: { color: K.donker }, fontSize: 20, margin: [6, 16, 6, 16], valign: 'middle', objectName: nm(4) });

  // 7 DEEL 1: plantenorganen
  s = nieuw('Deel 1 · Waterhuishouding en plantenorganen', 'De vier plantenorganen', 'Deel 1 · Plantenorganen');
  fig(s, 'plant', 0.4, 1.75, 6.9);
  [['wortel', 'verankert de plant en neemt **water en mineralen** op'], ['stengel', 'draagt bladeren en bloemen en **vervoert** water en assimilaten'],
   ['blad', 'maakt suikers door **fotosynthese** en geeft **waterdamp** af'], ['bloem', 'zorgt voor de **voortplanting**']]
    .forEach(([t, u], i) => kaart(s, i + 1, 7.6, 1.6 + i * 1.08, 5.1, 0.95, t, md(u), { fs: 15 }));
  kaart(s, 5, 7.6, 5.98, 5.1, 0.8, 'Let op', 'een orgaan is opgebouwd uit weefsels', { fs: 15, fill: K.amberL, kleur: K.amber, inline: true });

  // 8 DEEL 2: blad
  pres.addSection({ title: 'Deel 2 · Blad' });
  s = nieuw('Deel 2 · Aanpassingen van het blad', 'De weefsels van het blad', 'Deel 2 · Blad');
  fig(s, 'blad', 0.4, 1.7, 6.7, 0, 'Tekening blad: Zephyris, Wikimedia Commons, CC BY-SA 3.0');
  [['dekweefsel', 'één laag doorzichtige cellen; **beschermt**, met een waslaagje tegen verdamping'], ['vulweefsel', 'vol **bladgroenkorrels**: hier gebeurt de fotosynthese'],
   ['huidmondje', 'opening onderaan: **CO₂** erin, **O₂ en waterdamp** eruit'], ['sluitcellen', 'twee boonvormige cellen: **openen en sluiten** het huidmondje'],
   ['vaatbundels', 'de **nerven**: brengen water aan en voeren assimilaten af']]
    .forEach(([t, u], i) => kaart(s, i + 1, 7.4, 1.6 + i * 1.05, 5.3, 0.95, t, md(u), { fs: 15 }));

  // 9 DEEL 2: denkvraag
  denkvraag('Deel 2 · Aanpassingen van het blad', 'Waarom zitten huidmondjes onderaan?', 'Deel 2 · Blad',
    'Waarom liggen de meeste huidmondjes aan de onderkant van het blad en niet aan de bovenkant?',
    [['Wat gebeurt er bij een huidmondje?', 'Langs het huidmondje **verdampt water**.'], ['Waar is het warmst?', 'De bovenkant ligt in de zon en wordt **warmer**: daar zou meer water verdampen.'],
     ['Gevolg?', 'Aan de koelere onderkant gaat **minder water** verloren. De gaswisseling kan toch.']],
    'Huidmondjes aan de onderkant beperken het waterverlies.');

  // 10 DEEL 3: openen en sluiten
  pres.addSection({ title: 'Deel 3 · Huidmondjes' });
  s = nieuw('Deel 3 · Gasuitwisseling via de huidmondjes', 'Hoe opent en sluit een huidmondje?', 'Deel 3 · Huidmondjes');
  fig(s, 'stoma', 2.35, 1.55, 8.6);
  kaart(s, 1, 0.6, 4.65, 5.95, 1.55, 'Openen', md('sluitcellen nemen water op → vacuole zwelt → **turgor stijgt** → de sluitcellen buigen uit elkaar'), { fs: 16, fill: K.waterL, kleur: K.water });
  kaart(s, 2, 6.75, 4.65, 5.95, 1.55, 'Sluiten', md('sluitcellen verliezen water → vacuole krimpt → **turgor daalt** → de opening gaat dicht'), { fs: 16, fill: K.amberL, kleur: K.amber });
  kaart(s, 3, 0.6, 6.33, 12.1, 0.6, 'Turgor', 'de druk van de vacuole tegen de celwand', { fs: 16, inline: true });

  // 11 DEEL 3: wanneer open of dicht
  s = nieuw('Deel 3 · Gasuitwisseling via de huidmondjes', 'Wanneer open, wanneer dicht?', 'Deel 3 · Huidmondjes');
  kaart(s, 0, 0.6, 1.6, 12.1, 1.0, 'Huidmondje open = gasuitwisseling', md('**CO₂** komt binnen voor de fotosynthese · **O₂** en **waterdamp** gaan naar buiten'), { fs: 18 });
  [['licht en genoeg water', 'open', 'fotosynthese kan', I.zon, K.groen], ['donker', 'dicht', 'geen fotosynthese, dus geen CO₂ nodig', I.maan, '475569'], ['watertekort', 'dicht', 'de plant verliest minder water', I.droog, K.rood]]
    .forEach(([sit, toestand, waarom, ic, kl], i) => {
      const x = 0.6 + i * 4.15;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.12, x, y: 2.95, w: 3.8, h: 3.75, fill: { color: K.licht }, line: { color: K.licht }, objectName: nm(i + 1) });
      s.addShape(pres.shapes.OVAL, { x: x + 1.42, y: 3.2, w: 0.95, h: 0.95, fill: { color: K.wit }, line: { color: K.mint }, objectName: nm(i + 1) });
      s.addImage({ data: ic, x: x + 1.64, y: 3.42, w: 0.51, h: 0.51, objectName: nm(i + 1) });
      s.addText(sit, { x: x + 0.2, y: 4.3, w: 3.4, h: 0.5, fontSize: 19, bold: true, color: K.tekst, align: 'center', margin: 0, isTextBox: true, objectName: nm(i + 1) });
      s.addText('huidmondjes ' + toestand, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.2, x: x + 0.55, y: 4.95, w: 2.7, h: 0.55, fill: { color: kl }, line: { color: kl }, fontSize: 17, bold: true, color: K.wit, align: 'center', valign: 'middle', margin: 0, objectName: nm(i + 1) });
      s.addText(waterNiet(waarom), { x: x + 0.25, y: 5.65, w: 3.3, h: 0.85, fontSize: 16, color: K.grijs, align: 'center', valign: 'top', margin: 0, isTextBox: true, objectName: nm(i + 1) });
    });
  function waterNiet(t) { return t; }

  // 12 DEEL 3: denkvraag
  denkvraag('Deel 3 · Gasuitwisseling via de huidmondjes', 'Gesloten in de zon?', 'Deel 3 · Huidmondjes',
    'Op een hete zomerdag zijn de huidmondjes ’s middags gesloten, ook al schijnt de zon. Hoe kan dat?',
    [['Wat gebeurt er bij hitte?', 'Er verdampt veel water. De plant krijgt een **watertekort**.'], ['Wat doen de sluitcellen?', 'Ze verliezen water: de vacuole krimpt en de **turgor daalt**.'],
     ['Gevolg?', 'De huidmondjes **sluiten**: minder waterverlies, maar ook minder CO₂.']],
    'Bij een watertekort is water sparen belangrijker dan fotosynthese.');

  // 13 DEEL 4: stengel
  pres.addSection({ title: 'Deel 4 · Stengel' });
  s = nieuw('Deel 4 · Aanpassingen van de stengel', 'De stengel in dwarsdoorsnede', 'Deel 4 · Stengel');
  fig(s, 'stengel', 0.3, 1.75, 6.75);
  [['dekweefsel', 'buitenste cellaag: **beschermt** de stengel'], ['cortex', 'cellen van het vulweefsel onder het dekweefsel: steun en opslag'],
   ['vaatbundels', 'liggen in een **kring**: houtvaten, deelweefsel en zeefvaten'], ['houtvaten', 'aan de **binnenkant**: water en mineralen omhoog'],
   ['zeefvaten', 'aan de **buitenkant**: vervoeren assimilaten'], ['deelweefsel', 'ertussen: cellen blijven **delen**, de stengel wordt dikker'],
   ['vulweefsel', 'in het midden (merg): opslag']]
    .forEach(([t, u], i) => kaart(s, i + 1, 7.3, 1.55 + i * 0.77, 5.4, 0.68, t, md(u), { fs: 14, inline: true }));

  // 14 DEEL 4: houtvat en zeefvat
  s = nieuw('Deel 4 · Aanpassingen van de stengel', 'Houtvat of zeefvat?', 'Deel 4 · Stengel');
  fig(s, 'vaten', 1.2, 1.6, 10.9);
  kaart(s, 1, 0.6, 5.95, 5.95, 0.85, 'Houtvat', md('dood en hol: **water** omhoog'), { fs: 17, inline: true, fill: K.waterL, kleur: K.water });
  kaart(s, 2, 6.75, 5.95, 5.95, 0.85, 'Zeefvat', md('levend, met zeefplaten: **assimilaten** op en neer'), { fs: 17, inline: true, fill: K.amberL, kleur: K.amber });

  // 15 DEEL 5: wortel
  pres.addSection({ title: 'Deel 5 · Wortel' });
  s = nieuw('Deel 5 · Aanpassingen van de wortel', 'De wortel in dwarsdoorsnede', 'Deel 5 · Wortel');
  fig(s, 'wortel', 0.3, 1.75, 6.75);
  [['wortelhaartjes', 'maken de oppervlakte voor wateropname heel **groot**'], ['dekweefsel', 'buitenste cellaag van de wortel'],
   ['cortex', 'cellen van het vulweefsel: het water gaat erdoor naar het midden'], ['vaatbundel', 'één vaatbundel in het **midden**'],
   ['houtvaten', 'in een **ster** in het midden: water omhoog'], ['zeefvaten', '**tussen** de armen van de ster: assimilaten']]
    .forEach(([t, u], i) => kaart(s, i + 1, 7.3, 1.6 + i * 0.88, 5.4, 0.78, t, md(u), { fs: 15, inline: true }));

  // 16 DEEL 5: vergelijking
  s = nieuw('Deel 5 · Aanpassingen van de wortel', 'Stengel en wortel vergeleken', 'Deel 5 · Wortel');
  fig(s, 'stengel', 0.5, 1.55, 5.9);
  fig(s, 'wortel', 6.9, 1.55, 5.9);
  kaart(s, 1, 0.6, 5.35, 5.95, 1.4, 'Stengel', md('**veel** vaatbundels in een **kring**; houtvaten binnen, zeefvaten buiten'), { fs: 17 });
  kaart(s, 2, 6.75, 5.35, 5.95, 1.4, 'Wortel', md('**één** vaatbundel in het **midden**; houtvaten en zeefvaten naast elkaar'), { fs: 17 });

  // 17 DEEL 6: watertransport
  pres.addSection({ title: 'Deel 6 · Transport' });
  s = nieuw('Deel 6 · Water- en assimilatentransport', 'Watertransport: opwaarts', 'Deel 6 · Transport');
  fig(s, 'transport', 0.6, 1.55, 5.25);
  [['wortelhaartjes', 'nemen water en mineralen op uit de bodem'], ['cortex', 'het water gaat naar de houtvaten in het midden van de wortel'],
   ['houtvaten', 'water stijgt door wortel en stengel naar het blad: **opwaarts**'], ['huidmondjes', 'water verdampt; die verdamping **trekt** nieuw water omhoog']]
    .forEach(([t, u], i) => { kaart(s, i + 1, 7.25, 1.6 + i * 1.18, 5.45, 1.02, t, md(u), { fs: 16, fill: K.waterL, kleur: K.water }); nummer(s, i + 1, 6.6, 1.86 + i * 1.18, i + 1, K.water); });
  s.addText([{ text: '▲ blauw', options: { bold: true, color: K.water } }, { text: ' water via houtvaten   ' }, { text: '▼ oranje', options: { bold: true, color: K.amber } }, { text: ' assimilaten via zeefvaten' }],
    { x: 6.6, y: 6.4, w: 6.1, h: 0.4, fontSize: 14, color: K.grijs, margin: 0, isTextBox: true, objectName: nm(5) });

  // 18 DEEL 6: assimilaten
  s = nieuw('Deel 6 · Water- en assimilatentransport', 'Assimilaten: vooral neerwaarts', 'Deel 6 · Transport');
  s.addText([{ text: 'Definitie  ', options: { bold: true, color: 'BFE3B8' } }, { text: 'Assimilaten zijn de eindproducten van de fotosynthese.', options: { color: K.wit } }],
    { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 0.6, y: 1.6, w: 12.1, h: 0.95, fill: { color: K.donker }, line: { color: K.donker }, fontSize: 21, margin: [6, 16, 6, 16], valign: 'middle', objectName: nm(1) });
  ['glucose', 'zetmeel', 'eiwitten', 'vetten'].forEach((t, i) => {
    s.addText(t, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.12, x: 0.6 + i * 3.08, y: 2.85, w: 2.85, h: 1.15, fill: { color: K.amberL }, line: { color: K.amberL }, fontSize: 26, bold: true, color: K.amber, align: 'center', valign: 'middle', objectName: nm(2 + i) });
  });
  [['1', 'In het blad maakt de plant **glucose** door fotosynthese, en daarmee zetmeel, eiwitten en vetten.'],
   ['2', 'De assimilaten gaan via de **zeefvaten** naar alle delen van de plant.'],
   ['3', 'Een groot deel gaat naar de **wortel** en wordt opgeslagen, bv. als zetmeel: **neerwaarts transport**.']]
    .forEach(([n, u], i) => { kaart(s, 6 + i, 1.3, 4.3 + i * 0.85, 11.4, 0.72, '', md(u), { fs: 17 }); nummer(s, 6 + i, 0.6, 4.39 + i * 0.85, n, K.amber); });

  // 19 DEEL 6: denkvraag
  denkvraag('Deel 6 · Water- en assimilatentransport', 'Een geringde boom', 'Deel 6 · Transport',
    'Rond een boom wordt net boven de grond een ring schors weggesneden. De zeefvaten zitten in de schors, de houtvaten niet. Na een tijd sterft de boom. Waarom?',
    [['Wat wordt onderbroken?', 'De **zeefvaten**: de assimilaten kunnen niet meer naar de wortel.'], ['Wat blijft werken?', 'De **houtvaten**: de bladeren krijgen nog water.'],
     ['Gevolg?', 'De wortel krijgt geen voedsel en **sterft af**. Dan neemt ze geen water meer op.']],
    'Zonder assimilaten naar de wortel sterft de wortel, en daarna de hele boom.');

  // 20 DEEL 7: feedback
  pres.addSection({ title: 'Deel 7 · Homeostase' });
  s = nieuw('Deel 7 · Homeostase van de waterhuishouding', 'Negatieve feedback bij de huidmondjes', 'Deel 7 · Homeostase');
  kaart(s, 1, 0.6, 1.6, 12.1, 0.9, 'Homeostase', 'het intern milieu constant houden, met een feedbacksysteem', { fs: 18, inline: true });
  [['Prikkel', 'de plant verliest veel water: **watertekort**', K.rood, 'FDE8E8'], ['Reactie', 'sluitcellen verliezen water, turgor daalt: huidmondjes **sluiten**', K.amber, K.amberL], ['Effect', 'minder waterverlies: het watergehalte **stijgt** weer', K.groen, K.licht]]
    .forEach(([t, u, kl, fl], i) => {
      const x = 0.6 + i * 4.15;
      kaart(s, 2 + i, x, 2.85, 3.6, 2.0, t, md(u), { fs: 17, fill: fl, kleur: kl });
      if (i < 2) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 3.66, y: 3.65, w: 0.44, h: 0.4, fill: { color: K.grijs }, line: { color: K.grijs }, objectName: nm(3 + i) });
    });
  s.addShape(pres.shapes.CURVED_UP_ARROW, { x: 2.2, y: 4.95, w: 8.9, h: 0.85, flipH: true, fill: { color: K.water }, line: { color: K.water }, objectName: nm(5) });
  kaart(s, 5, 0.6, 5.95, 12.1, 0.85, 'Weer genoeg water?', md('Dan gaan de huidmondjes opnieuw **open**. De reactie werkt de verandering **tegen**: negatieve feedback.'), { fs: 17, inline: true, fill: K.waterL, kleur: K.water });

  // 21 DEEL 7: dynamisch evenwicht
  s = nieuw('Deel 7 · Homeostase van de waterhuishouding', 'Een dynamisch evenwicht', 'Deel 7 · Homeostase');
  fig(s, 'feedback', 0.4, 2.55, 7.6);
  [['Negatief', 'de reactie werkt de verandering **tegen**'], ['Schommelen', 'het watergehalte schommelt rond een **normwaarde**'],
   ['Binnen grenzen', 'het blijft tussen een onder- en bovengrens'], ['Dynamisch evenwicht', 'niet stil, maar toch in evenwicht']]
    .forEach(([t, u], i) => kaart(s, i + 1, 8.3, 1.65 + i * 1.28, 4.4, 1.12, t, md(u), { fs: 16 }));

  // 22 SAMENVATTING
  pres.addSection({ title: 'Samenvatting' });
  s = pres.addSlide({ masterName: 'TITEL', sectionTitle: 'Samenvatting' });
  s.addText('Samenvatting', { x: 0.6, y: 0.4, w: 12, h: 0.8, fontSize: 36, bold: true, color: K.wit, margin: 0, isTextBox: true, objectName: vast() });
  const sam = [['Waterhuishouding', 'opname, transport en afgifte van water'], ['Organen', 'wortel, stengel, blad en bloem'],
    ['Blad', 'dekweefsel, cellen van het vulweefsel, huidmondjes met sluitcellen'], ['Huidmondje', 'water erin → turgor ↑ → open; water eruit → dicht'],
    ['Stengel', 'vaatbundels in een kring: houtvaten binnen, zeefvaten buiten'], ['Wortel', 'wortelhaartjes; één vaatbundel in het midden'],
    ['Transport', 'water opwaarts via houtvaten; assimilaten vooral neerwaarts via zeefvaten'], ['Homeostase', 'bij watertekort sluiten de huidmondjes: negatieve feedback']];
  sam.forEach(([t, u], i) => {
    const kol = i % 2, rij = Math.floor(i / 2), x = 0.6 + kol * 6.2, y = 1.45 + rij * 1.4;
    s.addText([{ text: t, options: { bold: true, color: 'BFE3B8', fontSize: 18, breakLine: true } }, { text: u, options: { color: K.wit, fontSize: 16 } }],
      { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x, y, w: 5.9, h: 1.2, fill: { color: '2B6239' }, line: { color: '2B6239' }, margin: [6, 14, 6, 14], valign: 'middle', objectName: nm(i + 1) });
  });

  await pres.writeFile({ fileName: UIT });
  await applyTheme(UIT, THEME);
  await animeer(UIT);
  console.log('ok');
})();

// ---------- animaties: elk stapnummer = één klik, vervagend verschijnen ----------
async function animeer(f) {
  const zip = await JSZip.loadAsync(fs.readFileSync(f));
  const slides = Object.keys(zip.files).filter(n => /^ppt\/slides\/slide\d+\.xml$/.test(n));
  for (const n of slides) {
    let x = await zip.file(n).async('string');
    const stappen = {};
    const re = /<p:cNvPr id="(\d+)" name="a(\d+)-\d+"/g; let m;
    const isSp = {};
    while ((m = re.exec(x))) {
      (stappen[m[2]] = stappen[m[2]] || []).push(m[1]);
      isSp[m[1]] = x.slice(m.index - 15, m.index).includes('<p:nvSpPr>');
    }
    const keys = Object.keys(stappen).map(Number).filter(k => k > 0).sort((a, b) => a - b);
    if (!keys.length) continue;
    let id = 3, par = '';
    keys.forEach(k => {
      let inner = '';
      stappen[k].forEach((sp, j) => {
        inner += `<p:par><p:cTn id="${id++}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" grpId="0" nodeType="${j === 0 ? 'clickEffect' : 'withEffect'}"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>`
          + `<p:set><p:cBhvr><p:cTn id="${id++}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${sp}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>`
          + `<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="${id++}" dur="400"/><p:tgtEl><p:spTgt spid="${sp}"/></p:tgtEl></p:cBhvr></p:animEffect></p:childTnLst></p:cTn></p:par>`;
      });
      const a = id++, b = id++;
      par += `<p:par><p:cTn id="${a}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="${b}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>${inner}</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>`;
    });
    const bld = keys.flatMap(k => stappen[k]).filter(sp => isSp[sp]).map(sp => `<p:bldP spid="${sp}" grpId="0" animBg="1"/>`).join('');
    const timing = `<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>${par}</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>${bld ? `<p:bldLst>${bld}</p:bldLst>` : ''}</p:timing>`;
    x = x.includes('</p:clrMapOvr>') ? x.replace('</p:clrMapOvr>', '</p:clrMapOvr>' + timing) : x.replace('</p:sld>', timing + '</p:sld>');
    zip.file(n, x);
  }
  fs.writeFileSync(f, await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' }));
}
