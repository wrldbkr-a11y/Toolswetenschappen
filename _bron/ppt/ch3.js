const pptxgen = require('pptxgenjs');
const fs = require('fs');
const React = require('react');
const RDS = require('react-dom/server');
const sharp = require('sharp');
const FA = Object.assign({}, require('react-icons/fa'), require('react-icons/gi'));
const JSZip = require('/opt/npm-tools/node_modules/jszip');
const { applyTheme } = require('/root/.claude/skills/synced/1fe33a63-f4ea-4cfc-950e-0e79e049737b_a8573341-fcc3-4e00-a94c-615572386dea/pptx/scripts/apply_theme.js');

const UIT = '/home/claude/ppt/Chemie_H3_Scheidingstechnieken.pptx';
const THEME = {
  name: 'Chemie H3', headFontFace: 'Calibri', bodyFontFace: 'Calibri',
  colors: { dk1: '1D2A36', lt1: 'FFFFFF', dk2: '5C260B', lt2: 'FDF1E7', accent1: 'C25414', accent2: '2563EB', accent3: 'B91C1C',
    accent4: '15803D', accent5: 'B91C1C', accent6: '51606E', hlink: '2563EB', folHlink: '1F4D2B' }
};
const K = { lab: 'FBD3B0', sub: 'F9DCC4', kaartD: '7A3512', donker: '5C260B', groen: 'C25414', licht: 'FDF1E7', mint: 'F9DCC4', water: '2563EB', waterL: 'E3ECFD', amber: 'B45309', amberL: 'FDF0DC', tekst: '1D2A36', grijs: '51606E', wit: 'FFFFFF', rood: 'B91C1C' };

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'Stoffen onder de loep';
pres.author = 'Chemie 3de jaar';
const C = pres.SchemeColor;

// ---------- lay-outs ----------
pres.defineSlideMaster({ title: 'TITEL', background: { color: K.donker }, objects: [
  { placeholder: { options: { name: 'kicker', type: 'body', x: 0.9, y: 2.0, w: 11.5, h: 0.5, fontSize: 18, color: K.lab, bold: true, margin: 0 }, text: '' } },
  { placeholder: { options: { name: 'title', type: 'title', x: 0.9, y: 2.55, w: 11.5, h: 1.9, fontSize: 48, bold: true, color: K.wit, valign: 'top', align: 'left', margin: 0 }, text: '' } },
  { placeholder: { options: { name: 'sub', type: 'body', x: 0.9, y: 4.6, w: 11.5, h: 0.9, fontSize: 20, color: K.sub, valign: 'top', margin: 0 }, text: '' } },
] });
pres.defineSlideMaster({ title: 'INHOUD', background: { color: K.wit }, margin: [0.5, 0.6, 0.6, 0.6], objects: [
  { placeholder: { options: { name: 'kicker', type: 'body', x: 0.6, y: 0.32, w: 10, h: 0.36, fontSize: 14, color: K.groen, bold: true, margin: 0 }, text: '' } },
  { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.68, w: 12.1, h: 0.7, fontSize: 32, bold: true, color: K.donker, valign: 'top', align: 'left', margin: 0 }, text: '' } },
  { text: { text: 'Chemie 3 · Scheidingstechnieken', options: { x: 0.6, y: 7.08, w: 6, h: 0.3, fontSize: 10, color: '8A96A3', margin: 0 } } },
], slideNumber: { x: 12.25, y: 7.08, w: 0.5, h: 0.3, fontSize: 10, color: '8A96A3', align: 'right' } });

// ---------- hulpfuncties ----------
const png = f => { const b = fs.readFileSync('/home/claude/ppt/' + f + '.png'); return { path: '/home/claude/ppt/' + f + '.png', r: b.readUInt32BE(16) / b.readUInt32BE(20) }; };
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
  s.addText([{ text: 'Besluit  ', options: { bold: true, color: K.lab } }, { text: besluit, options: { color: K.wit } }],
    { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 0.6, y: 5.8, w: 12.1, h: 0.95, fill: { color: K.donker }, line: { color: K.donker }, fontSize: 19, margin: [6, 16, 6, 16], valign: 'middle', objectName: nm(4) });
  return s;
}

// atoom en molecule (natieve vormen)
function atoom(s, stap, x, y, d, soort) {
  const O = soort === 'O';
  s.addText(soort, { shape: pres.shapes.OVAL, x: x - d / 2, y: y - d / 2, w: d, h: d, fill: { color: O ? 'D62828' : 'FFFFFF' }, line: { color: O ? '9B1C1C' : '64748B', width: 1.5 },
    color: O ? 'FFFFFF' : '1D2A36', bold: true, fontSize: Math.round(d * 22), align: 'center', valign: 'middle', margin: 0, objectName: stap === null ? vast() : nm(stap) });
}
function h2(s, stap, x, y) { atoom(s, stap, x - 0.22, y, 0.55, 'H'); atoom(s, stap, x + 0.22, y, 0.55, 'H'); }
function o2(s, stap, x, y) { atoom(s, stap, x - 0.3, y, 0.75, 'O'); atoom(s, stap, x + 0.3, y, 0.75, 'O'); }
function h2o(s, stap, x, y, f = 1) { atoom(s, stap, x - 0.42 * f, y + 0.34 * f, 0.55 * f, 'H'); atoom(s, stap, x + 0.42 * f, y + 0.34 * f, 0.55 * f, 'H'); atoom(s, stap, x, y, 0.8 * f, 'O'); }
function chip(s, stap, x, y, w, h, t, kl, fl, fs = 15) {
  s.addText(t, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.15, x, y, w, h, fill: { color: fl }, line: { color: fl }, color: kl, bold: true, fontSize: fs, align: 'center', valign: 'middle', margin: 2, objectName: nm(stap) });
}
// oefendia: zin staat er, antwoord verschijnt per klik
function oefening(kicker, titel, sectie, opdracht, items, kol = 2) {
  const s = nieuw(kicker, titel, sectie);
  s.addText(opdracht, { x: 0.6, y: 1.55, w: 12.1, h: 0.45, fontSize: 18, italic: true, color: K.grijs, margin: 0, isTextBox: true, objectName: vast() });
  const per = Math.ceil(items.length / kol), W = (12.1 - (kol - 1) * 0.3) / kol, rh = Math.min(1.0, 4.75 / per);
  items.forEach(([zin, ant, kl, fl], i) => {
    const c = Math.floor(i / per), r = i % per, x = 0.6 + c * (W + 0.3), y = 2.15 + r * rh;
    s.addText(zin, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x, y, w: W, h: rh - 0.12, fill: { color: 'F4F6F8' }, line: { color: 'F4F6F8' }, fontSize: 16, color: K.tekst, valign: 'middle', margin: [4, 10, 4, 12], objectName: vast() });
    chip(s, i + 1, x + W - 2.05, y + 0.1, 1.9, rh - 0.32, ant, kl, fl, 14);
  });
  return s;
}

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
