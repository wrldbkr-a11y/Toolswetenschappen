const pptxgen = require('pptxgenjs');
const fs = require('fs');
const React = require('react');
const RDS = require('react-dom/server');
const sharp = require('sharp');
const FA = Object.assign({}, require('react-icons/fa'), require('react-icons/gi'));
const JSZip = require('/opt/npm-tools/node_modules/jszip');
const { applyTheme } = require('/root/.claude/skills/synced/1fe33a63-f4ea-4cfc-950e-0e79e049737b_a8573341-fcc3-4e00-a94c-615572386dea/pptx/scripts/apply_theme.js');

const UIT = '/home/claude/ppt/Chemie_H2_Mengsels_en_stofeigenschappen.pptx';
const THEME = {
  name: 'Chemie H2', headFontFace: 'Calibri', bodyFontFace: 'Calibri',
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
  { text: { text: 'Chemie 3 · Mengsels en stofeigenschappen', options: { x: 0.6, y: 7.08, w: 6, h: 0.3, fontSize: 10, color: '8A96A3', margin: 0 } } },
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

pres.title = 'Mengsels en stofeigenschappen';
// deeltjes in een kader: lijst van [x,y,kleur]
function deeltjes(s, stap, x0, y0, w, h, punten, d = 0.32) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.1, x: x0, y: y0, w, h, fill: { color: 'FFFFFF' }, line: { color: '94A3B8', width: 1.5 }, objectName: stap ? nm(stap) : vast() });
  punten.forEach(([x, y, k]) => s.addShape(pres.shapes.OVAL, { x: x0 + x * w - d / 2, y: y0 + y * h - d / 2, w: d, h: d, fill: { color: k }, line: { color: '334155', width: 0.75 }, objectName: stap ? nm(stap) : vast() }));
}
const raster = (n, m, f) => { const p = []; for (let i = 0; i < n; i++) for (let j = 0; j < m; j++) p.push([(i + 0.5 + (j % 2) * 0.25) / (n + 0.3), (j + 0.5) / m, f(i, j)]); return p; };
function glas(s, stap, x, y, kleur, korrels) {
  const o = () => (stap ? nm(stap) : vast());
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.08, x, y, w: 1.7, h: 2.4, fill: { color: 'FFFFFF' }, line: { color: '1D2A36', width: 2.5 }, objectName: o() });
  s.addShape(pres.shapes.RECTANGLE, { x: x + 0.09, y: y + 0.5, w: 1.52, h: 1.81, fill: { color: kleur }, line: { color: kleur }, objectName: o() });
  (korrels || []).forEach(([dx, dy, k]) => s.addShape(pres.shapes.OVAL, { x: x + 0.15 + dx * 1.3, y: y + 0.6 + dy * 1.6, w: 0.11, h: 0.11, fill: { color: k }, line: { color: k }, objectName: o() }));
}

(async () => {
  const BL = '2563EB', BLL = 'E3ECFD', GR = '15803D', GRL = 'E6F4EA';
  const W1 = '60A5FA', OR = 'F59E0B', GRY = '9CA3AF';

  // 1 TITEL
  pres.addSection({ title: 'Start' });
  let s = pres.addSlide({ masterName: 'TITEL', sectionTitle: 'Start' });
  s.addText('Chemie 3de jaar · Thema 1 · Hoofdstuk 2', { placeholder: 'kicker' });
  s.addText('Mengsels en stofeigenschappen', { placeholder: 'title' });
  s.addText('Zuivere stof of mengsel? Welk soort mengsel? En welke eigenschappen horen bij een stof?', { placeholder: 'sub' });

  // 2 LESDOELEN (letterlijk uit het leerstofoverzicht)
  s = nieuw('Lesdoelen', 'Na dit hoofdstuk kan je …', 'Start');
  const doelblok = (st, y, h, n, titel, p, doelen) => {
    s.addText([{ text: n, options: { bold: true, color: K.groen, fontSize: 18, breakLine: true } }, { text: p, options: { color: K.grijs, fontSize: 14 } }],
      { x: 0.6, y, w: 1.3, h, margin: 0, valign: 'top', isTextBox: true, objectName: nm(st) });
    const runs = [{ text: titel, options: { bold: true, color: K.groen, fontSize: 17, breakLine: true } }];
    doelen.forEach((d, i) => runs.push({ text: d, options: { fontSize: 16, color: K.tekst, bullet: true, breakLine: i < doelen.length - 1 } }));
    s.addText(runs, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, x: 2.0, y, w: 10.7, h, fill: { color: K.licht }, line: { color: K.licht }, margin: [6, 12, 6, 12], valign: 'top', paraSpaceAfter: 2, objectName: nm(st) });
  };
  doelblok(1, 1.55, 1.3, '2.1', 'Soorten mengsels', 'p. 19', ['Ik onderscheid de begrippen zuivere stof, bestanddeel en mengsel.', 'Ik kan uitleggen waarom een bepaald mengsel homogeen of heterogeen is.']);
  doelblok(2, 3.0, 2.15, '2.2', 'Soorten heterogene en homogene mengsels', 'p. 21', ['Ik onderscheid de specifieke soorten homogene en heterogene mengsels op basis van de aggregatietoestand van hun bestanddelen.']);
  ['aerosol', 'rook', 'nevel', 'oplossing', 'schuim', 'suspensie', 'emulsie', 'legering'].forEach((t, i) => chip(s, 2, 2.25 + i * 1.3, 4.5, 1.2, 0.48, t, K.wit, K.groen, 14));
  doelblok(3, 5.3, 1.5, '2.3', 'Stofeigenschappen', 'p. 23', ['Ik beschrijf wat een stofeigenschap is en kan voorbeelden van stofeigenschappen noteren.', 'Ik kan het onderscheid maken tussen een stofeigenschap en een voorwerpseigenschap.']);

  // 3 ZUIVERE STOF, MENGSEL, BESTANDDEEL
  pres.addSection({ title: '2.1 Soorten mengsels' });
  const S1 = '2.1 Soorten mengsels';
  s = nieuw('Lesdoel 2.1 · Soorten mengsels', 'Zuivere stof, mengsel, bestanddeel', S1);
  s.addText('Alle stoffen bestaan uit heel kleine deeltjes. Zijn ze allemaal gelijk, of niet?', { x: 0.6, y: 1.5, w: 12.1, h: 0.45, fontSize: 18, color: K.tekst, margin: 0, isTextBox: true, objectName: vast() });
  const mix = (i, j) => ((i * 3 + j * 5) % 3 === 0 ? OR : W1);
  [['Zuivere stof', 'één soort deeltjes: alle deeltjes zijn gelijk', 'gedestilleerd water, suiker, zuurstofgas, zuiver goud', raster(5, 4, () => W1)],
   ['Mengsel', 'twee of meer soorten deeltjes: twee of meer zuivere stoffen samen', 'kraantjeswater, lucht, zeewater, melk', raster(5, 4, mix)],
   ['Bestanddeel', 'een zuivere stof die in een mengsel zit', 'zoutwater heeft twee bestanddelen: water en zout', null]]
    .forEach(([t, u, vb, pts], i) => {
      const x = 0.6 + i * 4.15, st = i + 1;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.12, x, y: 2.15, w: 3.8, h: 4.65, fill: { color: K.licht }, line: { color: K.licht }, objectName: nm(st) });
      if (pts) deeltjes(s, st, x + 0.6, 2.4, 2.6, 1.75, pts);
      else {
        deeltjes(s, st, x + 0.25, 2.4, 1.5, 1.75, raster(3, 4, () => W1));
        deeltjes(s, st, x + 2.05, 2.4, 1.5, 1.75, raster(3, 4, () => OR));
        s.addText('water', { x: x + 0.25, y: 4.18, w: 1.5, h: 0.3, fontSize: 13, color: K.grijs, align: 'center', margin: 0, isTextBox: true, objectName: nm(st) });
        s.addText('zout', { x: x + 2.05, y: 4.18, w: 1.5, h: 0.3, fontSize: 13, color: K.grijs, align: 'center', margin: 0, isTextBox: true, objectName: nm(st) });
      }
      s.addText(t, { x: x + 0.25, y: 4.5, w: 3.3, h: 0.5, fontSize: 22, bold: true, color: K.donker, margin: 0, isTextBox: true, objectName: nm(st) });
      s.addText(u, { x: x + 0.25, y: 5.0, w: 3.3, h: 0.85, fontSize: 15, color: K.tekst, valign: 'top', margin: 0, isTextBox: true, objectName: nm(st) });
      s.addText([{ text: 'bv. ', options: { bold: true } }, { text: vb }], { x: x + 0.25, y: 5.9, w: 3.3, h: 0.8, fontSize: 14, italic: true, color: K.grijs, valign: 'top', margin: 0, isTextBox: true, objectName: nm(st) });
    });

  // 4 LET OP: WATER
  s = nieuw('Lesdoel 2.1 · Soorten mengsels', 'Let op: verschillende atomen, toch zuiver', S1);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.15, x: 0.6, y: 1.65, w: 6.2, h: 5.1, fill: { color: 'F4F6F8' }, line: { color: 'F4F6F8' }, objectName: vast() });
  [[1.7, 2.4], [3.4, 2.6], [5.1, 2.35], [2.3, 4.0], [4.1, 4.15], [5.6, 3.95], [1.5, 5.5], [3.2, 5.6], [4.9, 5.45]].forEach(([x, y]) => h2o(s, 1, x, y, 0.9));
  kaart(s, 1, 7.2, 1.65, 5.5, 1.5, 'Watermolecule', md('Elk deeltje bestaat uit **verschillende atomen**: 1 O en 2 H.'), { fs: 17 });
  kaart(s, 2, 7.2, 3.35, 5.5, 1.5, 'Maar …', md('**alle deeltjes zijn gelijk**. Er is maar één soort deeltje.'), { fs: 17 });
  s.addText([{ text: 'Dus ', options: { bold: true, color: K.lab } }, { text: 'water (H₂O) is een zuivere stof, geen mengsel.', options: { color: K.wit } }],
    { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 7.2, y: 5.05, w: 5.5, h: 1.7, fill: { color: K.donker }, line: { color: K.donker }, fontSize: 20, margin: [4, 14, 4, 14], valign: 'middle', objectName: nm(3) });

  // 5 OEFENING ZUIVER OF MENGSEL
  const Z = ['zuivere stof', BL, BLL], M = ['mengsel', K.groen, K.mint];
  oefening('Lesdoel 2.1 · Oefening', 'Zuivere stof of mengsel?', S1, 'Eén soort deeltjes of meer soorten? Denk eerst zelf.', [
    ['gedestilleerd water', ...Z], ['kraantjeswater', ...M], ['lucht', ...M], ['zuurstofgas', ...Z],
    ['suiker', ...Z], ['zeewater', ...M], ['zuiver goud (24 karaat)', ...Z], ['brons', ...M]]);

  // 6 HOMOGEEN OF HETEROGEEN
  s = nieuw('Lesdoel 2.1 · Soorten mengsels', 'Homogeen of heterogeen?', S1);
  const korrels = []; for (let k = 0; k < 40; k++) korrels.push([((k * 37) % 100) / 100, ((k * 53) % 100) / 100 * 0.95, k % 3 ? '8B5A2B' : 'A0703C']);
  [['homogeen mengsel', 'Je ziet de bestanddelen niet apart, ook niet met een vergrootglas of een microscoop. Het mengsel ziet er overal hetzelfde uit.', 'bv. suikerwater, zoutwater', 'BFE3F7', null, BL, BLL],
   ['heterogeen mengsel', 'Je ziet de bestanddelen wel apart: met het blote oog, of pas met een microscoop. Het mengsel is niet overal hetzelfde.', 'bv. modderwater, melk', 'C9B79C', korrels, K.groen, K.licht]]
    .forEach(([t, u, vb, kl, kr, kk, fl], i) => {
      const x = 0.6 + i * 6.2, st = i + 1;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.12, x, y: 1.65, w: 5.9, h: 5.1, fill: { color: fl }, line: { color: fl }, objectName: nm(st) });
      glas(s, st, x + 0.4, 2.0, kl, kr);
      s.addText(t, { x: x + 2.4, y: 2.0, w: 3.3, h: 0.9, fontSize: 24, bold: true, color: kk, valign: 'top', margin: 0, isTextBox: true, objectName: nm(st) });
      s.addText(vb, { x: x + 2.4, y: 2.95, w: 3.3, h: 0.8, fontSize: 16, italic: true, color: K.grijs, valign: 'top', margin: 0, isTextBox: true, objectName: nm(st) });
      s.addText(u, { x: x + 0.4, y: 4.75, w: 5.1, h: 1.8, fontSize: 17, color: K.tekst, valign: 'top', margin: 0, isTextBox: true, objectName: nm(st) });
    });

  // 7 OEFENING HOMOGEEN/HETEROGEEN
  const HO = ['homogeen', BL, BLL], HE = ['heterogeen', K.groen, K.mint];
  oefening('Lesdoel 2.1 · Oefening', 'Kijk door de microscoop', S1, 'Zie je de bestanddelen apart, eventueel met een microscoop?', [
    ['suikerwater', ...HO], ['modderwater', ...HE], ['melk', ...HE], ['lucht', ...HO], ['sinaasappelsap met vruchtvlees', ...HE], ['messing (een metaal)', ...HO]], 1);

  // 8 NAAM HANGT AF VAN AGGREGATIETOESTAND
  pres.addSection({ title: '2.2 Homogeen en heterogeen' });
  const S2 = '2.2 Homogeen en heterogeen';
  s = nieuw('Lesdoel 2.2 · Homogene en heterogene mengsels', 'Welke naam krijgt een mengsel?', S2);
  kaart(s, 0, 0.6, 1.6, 12.1, 1.0, 'De naam hangt af van de aggregatietoestand', 'van de bestanddelen: vast, vloeibaar of gas.', { fs: 18, inline: true });
  [['Wat zit erin?', 'vast, vloeibaar of gas'], ['Waarin zit het?', 'in een vaste stof, een vloeistof of een gas'], ['Zie je de bestanddelen apart?', 'ja: heterogeen · nee: homogeen']].forEach(([t, u], i) => {
    const x = 0.6 + i * 4.15;
    kaart(s, i + 1, x, 3.0, 3.8, 2.2, t, u, { fs: 18 });
    nummer(s, i + 1, x + 3.15, 3.15, i + 1, K.groen, 0.5);
    if (i < 2) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 3.82, y: 3.9, w: 0.32, h: 0.38, fill: { color: K.grijs }, line: { color: K.grijs }, objectName: nm(i + 2) });
  });
  kaart(s, 4, 0.6, 5.5, 12.1, 1.15, 'Voorbeeld', md('modderwater: **vaste stof** (grond) **in een vloeistof** (water), je ziet de korrels → heterogeen: een **suspensie**'), { fs: 18, inline: true, fill: BLL, kleur: BL });

  // 9 HETEROGENE MENGSELS
  s = nieuw('Lesdoel 2.2 · Homogene en heterogene mengsels', 'Heterogene mengsels', S2);
  [['Grof mengsel', 'vaste stof in vaste stof', 'graniet, zand met ijzervijlsel, muesli'], ['Suspensie', 'vaste stof in vloeistof', 'modderwater, sinaasappelsap met vruchtvlees'],
   ['Emulsie', 'vloeistof in vloeistof', 'melk, mayonaise'], ['Schuim', 'gas in vloeistof of in vaste stof', 'slagroom, scheerschuim, piepschuim'],
   ['Rook', 'vaste stof in gas', 'rook van een kampvuur, stof in de lucht'], ['Nevel', 'vloeistof in gas', 'mist, spray uit een spuitbus']]
    .forEach(([n, w, vb], i) => {
      const y = 1.6 + i * 0.8;
      s.addText(n, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 0.6, y, w: 2.6, h: 0.68, fill: { color: K.groen }, line: { color: K.groen }, fontSize: 18, bold: true, color: K.wit, valign: 'middle', margin: [2, 12, 2, 12], objectName: nm(i + 1) });
      s.addText([{ text: w, options: { bold: true, color: K.tekst } }, { text: '   bv. ' + vb, options: { color: K.grijs, italic: true } }],
        { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 3.35, y, w: 9.35, h: 0.68, fill: { color: K.licht }, line: { color: K.licht }, fontSize: 17, valign: 'middle', margin: [2, 12, 2, 12], objectName: nm(i + 1) });
    });
  kaart(s, 7, 0.6, 6.45, 12.1, 0.55, 'Aerosol', 'verzamelnaam voor rook en nevel: vaste deeltjes of druppeltjes in een gas', { fs: 15, inline: true, fill: K.amberL, kleur: K.amber });

  // 10 HOMOGENE MENGSELS
  s = nieuw('Lesdoel 2.2 · Homogene en heterogene mengsels', 'Homogene mengsels', S2);
  [['Oplossing', 'vaste stof, vloeistof of gas opgelost in een vloeistof', 'suikerwater, zoutwater, frisdrank in een gesloten fles', 'BFE3F7'],
   ['Legering', 'metalen gemengd in vaste toestand', 'brons (koper en tin): Manneken Pis; roestvrij staal: de bollen van het Atomium', 'D6B36A'],
   ['Gasmengsel', 'gassen gemengd', 'lucht', 'E5EEF5']]
    .forEach(([n, w, vb, kl], i) => {
      const x = 0.6 + i * 4.15, st = i + 1;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.12, x, y: 1.65, w: 3.8, h: 5.1, fill: { color: BLL }, line: { color: BLL }, objectName: nm(st) });
      s.addShape(i === 1 ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.OVAL, { x: x + 1.15, y: 1.95, w: 1.5, h: 1.5, fill: { color: kl }, line: { color: '64748B', width: 1.5 }, objectName: nm(st) });
      s.addText(n, { x: x + 0.3, y: 3.65, w: 3.2, h: 0.55, fontSize: 24, bold: true, color: BL, align: 'center', margin: 0, isTextBox: true, objectName: nm(st) });
      s.addText(w, { x: x + 0.3, y: 4.3, w: 3.2, h: 1.1, fontSize: 17, color: K.tekst, align: 'center', valign: 'top', margin: 0, isTextBox: true, objectName: nm(st) });
      s.addText('bv. ' + vb, { x: x + 0.3, y: 5.5, w: 3.2, h: 1.0, fontSize: 15, italic: true, color: K.grijs, align: 'center', valign: 'top', margin: 0, isTextBox: true, objectName: nm(st) });
    });

  // 11 OEFENING SOORT MENGSEL
  const HT = t => [t, K.groen, K.mint], HM = t => [t, BL, BLL];
  oefening('Lesdoel 2.2 · Oefening', 'Welk soort mengsel?', S2, 'Wat zit waarin? Zie je het apart? Geef de naam.', [
    ['modderwater', ...HT('suspensie')], ['mayonaise', ...HT('emulsie')], ['slagroom', ...HT('schuim')], ['mist', ...HT('nevel')],
    ['rook van een kampvuur', ...HT('rook')], ['zoutwater', ...HM('oplossing')], ['brons', ...HM('legering')], ['graniet', ...HT('grof mengsel')]]);

  // 12 STOF OF VOORWERP
  pres.addSection({ title: '2.3 Stofeigenschappen' });
  const S3 = '2.3 Stofeigenschappen';
  s = nieuw('Lesdoel 2.3 · Stofeigenschappen', 'Stofeigenschap of voorwerpseigenschap?', S3);
  [['Stofeigenschap', 'hoort bij de stof', 'Een kenmerk van de stof zelf. Blijft hetzelfde, hoe groot het stuk ook is en welke vorm het ook heeft. Daarmee herken je een stof.',
    ['kleur', 'geur', 'smelttemperatuur', 'kooktemperatuur', 'massadichtheid', 'oplosbaarheid', 'geleidt stroom', 'magnetisch'], K.groen, K.licht, K.mint],
   ['Voorwerpseigenschap', 'hoort bij het voorwerp', 'Hoort bij één bepaald voorwerp. Verandert als je het voorwerp groter, kleiner of anders van vorm maakt.',
    ['massa', 'volume', 'vorm', 'lengte', 'temperatuur'], BL, BLL, 'C7D8FB']]
    .forEach(([t, kort, u, chips, kl, fl, cf], i) => {
      const x = 0.6 + i * 6.2;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.12, x, y: 1.6, w: 5.9, h: 5.2, fill: { color: fl }, line: { color: fl }, objectName: nm(i * 2 + 1) });
      s.addText([{ text: t, options: { bold: true, color: kl, fontSize: 24, breakLine: true } }, { text: kort, options: { color: K.grijs, fontSize: 16, italic: true } }], { x: x + 0.35, y: 1.8, w: 5.2, h: 0.95, margin: 0, valign: 'top', isTextBox: true, objectName: nm(i * 2 + 1) });
      s.addText(u, { x: x + 0.35, y: 2.85, w: 5.2, h: 1.5, fontSize: 16, color: K.tekst, valign: 'top', margin: 0, isTextBox: true, objectName: nm(i * 2 + 1) });
      chips.forEach((c, j) => chip(s, i * 2 + 2, x + 0.35 + (j % 2) * 2.65, 4.5 + Math.floor(j / 2) * 0.55, 2.5, 0.45, c, kl, cf, 14));
    });

  // 13 PROEF: BLOK ZAGEN
  s = nieuw('Lesdoel 2.3 · Stofeigenschappen', 'Zaag een blok aluminium in twee', S3);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.15, x: 0.6, y: 1.6, w: 5.6, h: 5.15, fill: { color: 'F4F6F8' }, line: { color: 'F4F6F8' }, objectName: vast() });
  s.addShape(pres.shapes.CUBE, { x: 1.4, y: 2.0, w: 3.6, h: 1.8, fill: { color: 'C9D1D9' }, line: { color: '64748B', width: 1.5 }, objectName: vast() });
  s.addText('voor', { x: 1.4, y: 3.85, w: 3.6, h: 0.35, fontSize: 14, color: K.grijs, align: 'center', margin: 0, isTextBox: true, objectName: vast() });
  s.addShape(pres.shapes.CUBE, { x: 1.0, y: 4.55, w: 1.9, h: 1.6, fill: { color: 'C9D1D9' }, line: { color: '64748B', width: 1.5 }, objectName: nm(1) });
  s.addShape(pres.shapes.CUBE, { x: 3.5, y: 4.55, w: 1.9, h: 1.6, fill: { color: 'C9D1D9' }, line: { color: '64748B', width: 1.5 }, objectName: nm(1) });
  s.addText('na het zagen', { x: 1.0, y: 6.25, w: 4.4, h: 0.35, fontSize: 14, color: K.grijs, align: 'center', margin: 0, isTextBox: true, objectName: nm(1) });
  s.addText('Wat verandert er? Wat blijft gelijk?', { x: 6.6, y: 1.6, w: 6.1, h: 0.45, fontSize: 18, bold: true, color: K.donker, margin: 0, isTextBox: true, objectName: vast() });
  [['massa', 'verandert', BL, BLL], ['volume', 'verandert', BL, BLL], ['vorm', 'verandert', BL, BLL], ['kleur', 'blijft gelijk', K.groen, K.mint], ['smelttemperatuur', 'blijft gelijk', K.groen, K.mint], ['massadichtheid', 'blijft gelijk', K.groen, K.mint]]
    .forEach(([e, a, kl, fl], i) => {
      const y = 2.2 + i * 0.75;
      s.addText(e, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x: 6.6, y, w: 6.1, h: 0.62, fill: { color: 'F4F6F8' }, line: { color: 'F4F6F8' }, fontSize: 17, color: K.tekst, valign: 'middle', margin: [2, 12, 2, 12], objectName: vast() });
      chip(s, i + 2, 10.4, y + 0.08, 2.2, 0.46, a, kl, fl, 15);
    });
  s.addText('verandert → voorwerpseigenschap · blijft gelijk → stofeigenschap', { x: 6.6, y: 6.75, w: 6.1, h: 0.3, fontSize: 13, italic: true, color: K.grijs, margin: 0, isTextBox: true, objectName: nm(8) });

  // 14 KIJK GOED: MASSADICHTHEID
  s = nieuw('Lesdoel 2.3 · Stofeigenschappen', 'Kijk goed: aluminium of koper?', S3);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.15, x: 0.6, y: 1.6, w: 6.6, h: 5.15, fill: { color: 'F4F6F8' }, line: { color: 'F4F6F8' }, objectName: vast() });
  [['aluminium', 'C9D1D9', '27 g', 1.2], ['koper', 'D08A4F', '90 g', 4.2]].forEach(([n, kl, m, x]) => {
    s.addShape(pres.shapes.CUBE, { x, y: 2.3, w: 2.2, h: 2.2, fill: { color: kl }, line: { color: '64748B', width: 1.5 }, objectName: vast() });
    s.addText([{ text: n, options: { bold: true, breakLine: true } }, { text: 'V = 10 cm³' }], { x: x - 0.2, y: 4.65, w: 2.6, h: 0.75, fontSize: 16, color: K.tekst, align: 'center', margin: 0, isTextBox: true, objectName: vast() });
    chip(s, 1, x + 0.1, 5.6, 2.0, 0.65, 'm = ' + m, K.groen, K.mint, 20);
  });
  kaart(s, 1, 7.5, 1.6, 5.2, 1.4, 'Zelfde volume', md('maar een **andere massa**.'), { fs: 18 });
  kaart(s, 2, 7.5, 3.2, 5.2, 1.6, 'Massadichtheid', md('= massa per volume. Aluminium: **2,7 g/cm³**. Koper: **9,0 g/cm³**.'), { fs: 18 });
  s.addText([{ text: 'Dus ', options: { bold: true, color: K.lab } }, { text: 'de massadichtheid is een stofeigenschap: zo hou je aluminium en koper uit elkaar.', options: { color: K.wit } }],
    { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 7.5, y: 5.0, w: 5.2, h: 1.75, fill: { color: K.donker }, line: { color: K.donker }, fontSize: 18, margin: [4, 14, 4, 14], valign: 'middle', objectName: nm(3) });

  // 14b ATOMIUM
  s = nieuw('Lesdoel 2.3 · In Brussel', 'Het Atomium: aluminium of staal?', S3);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.15, x: 0.6, y: 1.6, w: 5.2, h: 5.15, fill: { color: 'F4F6F8' }, line: { color: 'F4F6F8' }, objectName: vast() });
  { // ijzerkristal: 8 hoeken + midden
    const c = [[1.6, 2.5], [4.0, 2.5], [1.6, 4.9], [4.0, 4.9]], o = [0.7, -0.55], m = [3.15, 3.42];
    const hoek = [...c, ...c.map(([x, y]) => [x + o[0], y + o[1]])];
    [[0, 1], [0, 2], [1, 3], [2, 3], [4, 5], [4, 6], [5, 7], [6, 7], [0, 4], [1, 5], [2, 6], [3, 7]].forEach(([i, j]) => {
      const [x1, y1] = hoek[i], [x2, y2] = hoek[j];
      s.addShape(pres.shapes.LINE, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1) || 0.001, h: Math.abs(y2 - y1) || 0.001, flipV: (x2 - x1) * (y2 - y1) < 0, line: { color: '94A3B8', width: 3 }, objectName: vast() });
    });
    [...hoek, m].forEach(([x, y]) => s.addShape(pres.shapes.OVAL, { x: x - 0.3, y: y - 0.3, w: 0.6, h: 0.6, fill: { color: 'D1D5DB' }, line: { color: '64748B', width: 1.5 }, objectName: vast() }));
    s.addText('ijzerkristal, 165 miljard keer vergroot', { x: 0.8, y: 6.15, w: 4.8, h: 0.4, fontSize: 14, italic: true, color: K.grijs, align: 'center', margin: 0, isTextBox: true, objectName: vast() });
  }
  kaart(s, 1, 6.1, 1.6, 6.6, 1.15, 'Expo 58', md('De bollen werden bekleed met **aluminium**.'), { fs: 17 });
  kaart(s, 2, 6.1, 2.9, 6.6, 1.3, 'Renovatie 2004–2006', md('Nieuwe bekleding van **roestvrij staal**: een legering van vooral ijzer, met onder meer chroom en nikkel.'), { fs: 17 });
  kaart(s, 3, 6.1, 4.35, 6.6, 1.0, 'Waarom?', md('Roestvrij staal is beter bestand tegen **corrosie**.'), { fs: 17, fill: BLL, kleur: BL });
  s.addText([{ text: 'Dus ', options: { bold: true, color: K.lab } }, { text: 'corrosiebestendigheid is een stofeigenschap: ze hangt af van het materiaal, niet van de grootte of de vorm van de bol.', options: { color: K.wit } }],
    { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 6.1, y: 5.5, w: 6.6, h: 1.25, fill: { color: K.donker }, line: { color: K.donker }, fontSize: 17, margin: [4, 14, 4, 14], valign: 'middle', objectName: nm(4) });

  // 15 OEFENING STOF OF VOORWERP
  const SE = ['stofeigenschap', K.groen, K.mint], VE = ['voorwerp', BL, BLL];
  oefening('Lesdoel 2.3 · Oefening', 'Stof of voorwerp?', S3, 'Hoort de eigenschap bij de stof of bij dit ene voorwerp?', [
    ['Goud smelt bij 1064 °C.', ...SE], ['Deze ring weegt 5 g.', ...VE], ['Water kookt bij 100 °C.', ...SE], ['Het glas is 12 cm hoog.', ...VE],
    ['Koper is roodbruin.', ...SE], ['De fles heeft een volume van 1 L.', ...VE]], 1);

  // 16 SAMENVATTING
  pres.addSection({ title: 'Samenvatting' });
  s = pres.addSlide({ masterName: 'TITEL', sectionTitle: 'Samenvatting' });
  s.addText('Samenvatting', { x: 0.6, y: 0.4, w: 12, h: 0.8, fontSize: 36, bold: true, color: K.wit, margin: 0, isTextBox: true, objectName: vast() });
  [['Zuivere stof', 'één soort deeltjes'], ['Mengsel', 'twee of meer soorten deeltjes; elke zuivere stof erin is een bestanddeel'],
   ['Homogeen', 'bestanddelen niet apart te zien: oplossing, legering, gasmengsel'], ['Heterogeen', 'bestanddelen apart te zien: grof mengsel, suspensie, emulsie, schuim, rook, nevel'],
   ['Naam van een mengsel', 'hangt af van de aggregatietoestand van de bestanddelen'], ['Aerosol', 'rook en nevel: deeltjes of druppeltjes in een gas'],
   ['Stofeigenschap', 'hoort bij de stof: kleur, smelttemperatuur, massadichtheid …'], ['Voorwerpseigenschap', 'hoort bij het voorwerp: massa, volume, vorm …']]
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
