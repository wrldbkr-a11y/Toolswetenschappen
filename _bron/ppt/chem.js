const pptxgen = require('pptxgenjs');
const fs = require('fs');
const React = require('react');
const RDS = require('react-dom/server');
const sharp = require('sharp');
const FA = Object.assign({}, require('react-icons/fa'), require('react-icons/gi'));
const JSZip = require('/opt/npm-tools/node_modules/jszip');
const { applyTheme } = require('/root/.claude/skills/synced/1fe33a63-f4ea-4cfc-950e-0e79e049737b_a8573341-fcc3-4e00-a94c-615572386dea/pptx/scripts/apply_theme.js');

const UIT = '/home/claude/ppt/Chemie_H1_Stoffen_onder_de_loep.pptx';
const THEME = {
  name: 'Chemie H1', headFontFace: 'Calibri', bodyFontFace: 'Calibri',
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
  { text: { text: 'Chemie 3 · Stoffen onder de loep', options: { x: 0.6, y: 7.08, w: 6, h: 0.3, fontSize: 10, color: '8A96A3', margin: 0 } } },
], slideNumber: { x: 12.25, y: 7.08, w: 0.5, h: 0.3, fontSize: 10, color: '8A96A3', align: 'right' } });

// ---------- hulpfuncties ----------
const png = f => { const b = fs.readFileSync('/home/claude/ppt/chem/' + f + '.png'); return { path: '/home/claude/ppt/chem/' + f + '.png', r: b.readUInt32BE(16) / b.readUInt32BE(20) }; };
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

(async () => {
  const I = {
    kleur: await icoon('GiPaintBucket', K.groen), gas: await icoon('GiBubbles', K.groen), geur: await icoon('GiNoseSide', K.groen),
    vuur: await icoon('GiFire', K.groen), terug: await icoon('GiAnticlockwiseRotation', K.groen),
    mol: await icoon('GiMolecule', K.groen), loep: await icoon('GiMagnifyingGlass', K.groen), reactie: await icoon('GiChemicalDrop', K.groen),
  };
  const BL = '2563EB', BLL = 'E3ECFD', RO = 'B91C1C', ROL = 'FDE8E8', GR = '15803D', GRL = 'E6F4EA';

  // 1 TITEL
  pres.addSection({ title: 'Start' });
  let s = pres.addSlide({ masterName: 'TITEL', sectionTitle: 'Start' });
  s.addText('Chemie 3de jaar · Thema 1 · Hoofdstuk 1', { placeholder: 'kicker' });
  s.addText('Stoffen onder de loep', { placeholder: 'title' });
  s.addText('Wat onderzoekt een chemicus? En hoe werk je veilig met stoffen?', { placeholder: 'sub' });

  // 2 LESDOELEN
  s = nieuw('Lesdoelen', 'Na dit hoofdstuk kan je …', 'Start');
  [['1.1', 'Ik beschrijf wat in de **chemie** bestudeerd wordt.', 'p. 11', I.loep], ['1.2', 'Ik ken de **gevarensymbolen** en kan **P- en H-zinnen** categoriseren als voorzorg of gevaar. Ik gebruik producten in een labo en in het dagelijks leven op een **verantwoorde manier**.', 'p. 13', I.reactie]]
    .forEach(([n, t, p, ic], i) => {
      const y = 1.75 + i * 2.5;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.12, x: 0.6, y, w: 12.1, h: 2.2, fill: { color: K.licht }, line: { color: K.licht }, objectName: nm(i + 1) });
      s.addShape(pres.shapes.OVAL, { x: 1.0, y: y + 0.55, w: 1.1, h: 1.1, fill: { color: K.wit }, line: { color: K.mint }, objectName: nm(i + 1) });
      s.addImage({ data: ic, x: 1.25, y: y + 0.8, w: 0.6, h: 0.6, objectName: nm(i + 1) });
      s.addText([{ text: 'Lesdoel ' + n + '   ', options: { bold: true, color: K.groen, fontSize: 18 } }, { text: p, options: { color: K.grijs, fontSize: 16 } }],
        { x: 2.5, y: y + 0.3, w: 9.8, h: 0.45, margin: 0, isTextBox: true, objectName: nm(i + 1) });
      s.addText(md(t).map(r => ({ text: r.text, options: { bold: !!r.b } })), { x: 2.5, y: y + 0.75, w: 9.8, h: 1.35, fontSize: i ? 20 : 24, color: K.tekst, valign: 'top', margin: 0, isTextBox: true, objectName: nm(i + 1) });
    });

  // 3 FYSICA OF CHEMIE
  pres.addSection({ title: '1.1 Chemie als wetenschap' });
  const S1 = '1.1 Chemie als wetenschap';
  s = nieuw('Lesdoel 1.1 · Chemie als wetenschap', 'Fysica of chemie?', S1);
  s.addText('Fysica en chemie zijn natuurwetenschappen. Ze bestuderen verschijnselen: dingen die gebeuren in de natuur.', { x: 0.6, y: 1.5, w: 12.1, h: 0.5, fontSize: 18, color: K.tekst, margin: 0, isTextBox: true, objectName: vast() });
  [['Fysica', 'De stof blijft dezelfde stof.', 'fysisch verschijnsel', 'IJs smelt. Het blijft water.', 'ijs', BL, BLL], ['Chemie', 'Er ontstaat een nieuwe stof.', 'chemisch verschijnsel', 'Papier verbrandt. Er ontstaan as en rook.', 'papier', K.groen, K.licht]]
    .forEach(([vak, kern, naam, vb, f, kl, fl], i) => {
      const x = 0.6 + i * 6.2;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.12, x, y: 2.2, w: 5.9, h: 3.75, fill: { color: fl }, line: { color: fl }, objectName: nm(i + 1) });
      s.addText(vak, { x: x + 0.35, y: 2.35, w: 5.2, h: 0.55, fontSize: 26, bold: true, color: kl, margin: 0, isTextBox: true, objectName: nm(i + 1) });
      s.addText([{ text: kern, options: { bold: true, breakLine: true } }, { text: 'Dat heet een ' + naam + '.' }], { x: x + 0.35, y: 2.95, w: 5.2, h: 0.9, fontSize: 18, color: K.tekst, margin: 0, valign: 'top', isTextBox: true, objectName: nm(i + 1) });
      const p = png(f); s.addImage({ path: p.path, x: x + 0.75, y: 3.9, w: 4.4, h: 4.4 / p.r, objectName: nm(i + 1), altText: vb });
      s.addText(vb, { x: x + 0.35, y: 5.5, w: 5.2, h: 0.4, fontSize: 16, italic: true, color: K.grijs, margin: 0, isTextBox: true, objectName: nm(i + 1) });
    });
  s.addText([{ text: 'Chemie ', options: { bold: true, color: K.lab } }, { text: 'is de wetenschap van de stoffen.', options: { color: K.wit } }],
    { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 0.6, y: 6.15, w: 12.1, h: 0.7, fill: { color: K.donker }, line: { color: K.donker }, fontSize: 20, margin: [4, 16, 4, 16], valign: 'middle', objectName: nm(3) });

  // 4 SLEUTELVRAAG
  s = nieuw('Lesdoel 1.1 · Chemie als wetenschap', 'Is er een nieuwe stof ontstaan?', S1);
  chip(s, 1, 0.6, 1.65, 5.9, 0.85, 'Ja → chemie', K.wit, K.groen, 24);
  chip(s, 1, 6.8, 1.65, 5.9, 0.85, 'Nee → fysica', K.wit, BL, 24);
  s.addText('Een nieuwe stof herken je vaak aan:', { x: 0.6, y: 2.85, w: 12.1, h: 0.5, fontSize: 20, bold: true, color: K.donker, margin: 0, isTextBox: true, objectName: nm(2) });
  [['een andere kleur', I.kleur], ['een gas (bubbels)', I.gas], ['een nieuwe geur', I.geur], ['licht of warmte', I.vuur], ['het gaat niet meer terug', I.terug]].forEach(([t, ic], i) => {
    const x = 0.6 + i * 2.46, st = 2 + i;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.12, x, y: 3.5, w: 2.22, h: 2.9, fill: { color: K.licht }, line: { color: K.licht }, objectName: nm(st) });
    s.addShape(pres.shapes.OVAL, { x: x + 0.56, y: 3.8, w: 1.1, h: 1.1, fill: { color: K.wit }, line: { color: K.mint }, objectName: nm(st) });
    s.addImage({ data: ic, x: x + 0.81, y: 4.05, w: 0.6, h: 0.6, objectName: nm(st) });
    s.addText(t, { x: x + 0.12, y: 5.1, w: 1.98, h: 1.0, fontSize: 17, bold: true, color: K.tekst, align: 'center', valign: 'top', margin: 0, isTextBox: true, objectName: nm(st) });
  });

  // 5 OEFENING FYSISCH OF CHEMISCH
  const F = ['fysica', BL, BLL], Ch = ['chemie', K.groen, K.mint];
  oefening('Lesdoel 1.1 · Oefening', 'Fysisch of chemisch?', S1, 'Ontstaat er een nieuwe stof? Denk eerst zelf, dan verschijnt het antwoord.', [
    ['IJs smelt tot water.', ...F], ['Papier verbrandt.', ...Ch], ['Een ijzeren hek roest.', ...Ch], ['Suiker lost op in thee.', ...F],
    ['Je bakt een ei.', ...Ch], ['Water kookt en wordt waterdamp.', ...F], ['Melk wordt zuur.', ...Ch], ['Een bruistablet bruist in water.', ...Ch]]);

  // 6 DRIE ONDERZOEKSGEBIEDEN
  s = nieuw('Lesdoel 1.1 · Chemie als wetenschap', 'Wat onderzoekt de chemie?', S1);
  s.addText('De chemie onderzoekt drie dingen van stoffen.', { x: 0.6, y: 1.5, w: 12.1, h: 0.5, fontSize: 19, color: K.tekst, margin: 0, isTextBox: true, objectName: vast() });
  [['samenstelling', 'Uit welke deeltjes bestaat een stof?', I.mol], ['eigenschappen', 'Hoe herken je een stof?', I.loep], ['omzettingen', 'Hoe verandert een stof in een nieuwe stof?', I.reactie]].forEach(([t, v, ic], i) => {
    const x = 0.6 + i * 4.15;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.12, x, y: 2.25, w: 3.8, h: 4.3, fill: { color: K.licht }, line: { color: K.licht }, objectName: nm(i + 1) });
    nummer(s, i + 1, x + 0.3, 2.5, i + 1, K.groen, 0.55);
    s.addShape(pres.shapes.OVAL, { x: x + 1.2, y: 3.0, w: 1.4, h: 1.4, fill: { color: K.wit }, line: { color: K.mint }, objectName: nm(i + 1) });
    s.addImage({ data: ic, x: x + 1.5, y: 3.3, w: 0.8, h: 0.8, objectName: nm(i + 1) });
    s.addText(t, { x: x + 0.2, y: 4.65, w: 3.4, h: 0.55, fontSize: 24, bold: true, color: K.donker, align: 'center', margin: 0, isTextBox: true, objectName: nm(i + 1) });
    s.addText(v, { x: x + 0.3, y: 5.3, w: 3.2, h: 1.0, fontSize: 17, color: K.tekst, align: 'center', valign: 'top', margin: 0, isTextBox: true, objectName: nm(i + 1) });
  });

  // 7 SAMENSTELLING
  s = nieuw('Lesdoel 1.1 · Onderzoeksgebied 1', 'Samenstelling: uit welke deeltjes?', S1);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.15, x: 0.6, y: 1.65, w: 6.2, h: 5.1, fill: { color: 'F4F6F8' }, line: { color: 'F4F6F8' }, objectName: vast() });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.1, x: 1.1, y: 2.3, w: 1.5, h: 2.6, fill: { color: 'FFFFFF' }, line: { color: '1D2A36', width: 2.5 }, objectName: vast() });
  s.addShape(pres.shapes.RECTANGLE, { x: 1.2, y: 2.9, w: 1.3, h: 1.9, fill: { color: 'A5D3EC' }, line: { color: 'A5D3EC' }, objectName: vast() });
  s.addText('een glas water', { x: 0.8, y: 5.0, w: 2.2, h: 0.4, fontSize: 15, color: K.grijs, align: 'center', margin: 0, isTextBox: true, objectName: vast() });
  s.addShape(pres.shapes.OVAL, { x: 3.4, y: 2.15, w: 3.1, h: 3.1, fill: { color: 'E6F2FA' }, line: { color: '1D2A36', width: 3 }, objectName: nm(1) });
  s.addShape(pres.shapes.LINE, { x: 2.0, y: 3.9, w: 1.45, h: 0, line: { color: '1D2A36', width: 2, dashType: 'dash' }, objectName: nm(1) });
  [[4.3, 3.0], [5.5, 3.1], [4.5, 4.35], [5.65, 4.3]].forEach(([x, y]) => h2o(s, 1, x, y, 0.75));
  s.addText('ver ingezoomd', { x: 3.4, y: 5.35, w: 3.1, h: 0.4, fontSize: 15, italic: true, color: K.grijs, align: 'center', margin: 0, isTextBox: true, objectName: nm(1) });
  kaart(s, 1, 7.2, 1.65, 5.5, 1.4, 'Moleculen', md('Water bestaat uit heel kleine deeltjes: **moleculen**. Je kan ze niet zien.'), { fs: 17 });
  kaart(s, 2, 7.2, 3.25, 3.9, 2.0, 'Eén watermolecule', md('**1 zuurstofatoom** (O) en **2 waterstofatomen** (H)'), { fs: 17 });
  h2o(s, 2, 11.9, 4.0, 1.1);
  s.addText([{ text: 'Daarom schrijven we water als ', options: { color: K.wit } }, { text: 'H₂O', options: { bold: true, color: K.lab } }],
    { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 7.2, y: 5.45, w: 5.5, h: 1.3, fill: { color: K.donker }, line: { color: K.donker }, fontSize: 21, margin: [4, 14, 4, 14], valign: 'middle', objectName: nm(3) });

  // 8 EIGENSCHAPPEN
  s = nieuw('Lesdoel 1.1 · Onderzoeksgebied 2', 'Eigenschappen: hoe herken je een stof?', S1);
  [['suiker', 'lost op: je ziet ze niet meer', false], ['zand', 'lost niet op: zakt naar de bodem', true]].forEach(([t, u, zand], i) => {
    const x = 0.8 + i * 3.2, st = i + 1;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.1, x, y: 1.8, w: 1.9, h: 3.0, fill: { color: 'FFFFFF' }, line: { color: '1D2A36', width: 2.5 }, objectName: vast() });
    s.addShape(pres.shapes.RECTANGLE, { x: x + 0.1, y: 2.4, w: 1.7, h: 2.3, fill: { color: 'A5D3EC' }, line: { color: 'A5D3EC' }, objectName: vast() });
    s.addText(t, { x: x - 0.3, y: 4.95, w: 2.5, h: 0.45, fontSize: 20, bold: true, color: K.donker, align: 'center', margin: 0, isTextBox: true, objectName: vast() });
    if (zand) for (let k = 0; k < 14; k++) s.addShape(pres.shapes.OVAL, { x: x + 0.15 + (k % 7) * 0.22, y: 4.45 - Math.floor(k / 7) * 0.13, w: 0.14, h: 0.12, fill: { color: 'A0703C' }, line: { color: '7A522A' }, objectName: nm(st) });
    s.addText(u, { x: x - 0.4, y: 5.45, w: 2.7, h: 0.8, fontSize: 16, color: K.tekst, align: 'center', valign: 'top', margin: 0, isTextBox: true, objectName: nm(st) });
  });
  kaart(s, 3, 7.2, 1.7, 5.5, 1.5, 'Oplosbaar zijn', md('is een **eigenschap** van een stof: zo kan je suiker en zand uit elkaar houden.'), { fs: 17 });
  s.addText('Andere eigenschappen:', { x: 7.2, y: 3.5, w: 5.5, h: 0.45, fontSize: 18, bold: true, color: K.donker, margin: 0, isTextBox: true, objectName: nm(4) });
  ['kleur', 'geur', 'smelttemperatuur', 'kooktemperatuur'].forEach((t, i) => chip(s, 4, 7.2 + (i % 2) * 2.8, 4.1 + Math.floor(i / 2) * 0.8, 2.6, 0.62, t, K.groen, K.mint, 16));

  // 9 OMZETTINGEN
  s = nieuw('Lesdoel 1.1 · Onderzoeksgebied 3', 'Omzettingen: een nieuwe stof', S1);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.15, x: 0.6, y: 1.6, w: 12.1, h: 3.35, fill: { color: 'F4F6F8' }, line: { color: 'F4F6F8' }, objectName: vast() });
  h2(s, null, 1.6, 2.6); h2(s, null, 1.6, 3.7); o2(s, null, 3.6, 3.15);
  s.addText('waterstofgas', { x: 0.9, y: 4.3, w: 1.8, h: 0.4, fontSize: 15, color: K.grijs, align: 'center', margin: 0, isTextBox: true, objectName: vast() });
  s.addText('zuurstofgas', { x: 2.7, y: 4.3, w: 1.8, h: 0.4, fontSize: 15, color: K.grijs, align: 'center', margin: 0, isTextBox: true, objectName: vast() });
  s.addShape(pres.shapes.RIGHT_ARROW, { x: 5.0, y: 2.95, w: 1.7, h: 0.45, fill: { color: K.groen }, line: { color: K.groen }, objectName: nm(1) });
  s.addText('vonk', { x: 5.0, y: 2.45, w: 1.7, h: 0.4, fontSize: 16, bold: true, color: K.groen, align: 'center', margin: 0, isTextBox: true, objectName: nm(1) });
  // losse atomen
  [[7.5, 2.3], [8.2, 2.5], [7.4, 3.8], [8.3, 3.9]].forEach(([x, y]) => atoom(s, 1, x, y, 0.55, 'H'));
  [[8.0, 3.15], [8.9, 3.15]].forEach(([x, y]) => atoom(s, 1, x, y, 0.75, 'O'));
  s.addText('losse atomen', { x: 7.0, y: 4.3, w: 2.4, h: 0.4, fontSize: 15, color: K.grijs, align: 'center', margin: 0, isTextBox: true, objectName: nm(1) });
  s.addShape(pres.shapes.RIGHT_ARROW, { x: 9.5, y: 2.95, w: 0.9, h: 0.45, fill: { color: K.groen }, line: { color: K.groen }, objectName: nm(2) });
  h2o(s, 2, 11.1, 2.35, 0.85); h2o(s, 2, 11.75, 3.45, 0.85);
  s.addText('water', { x: 10.5, y: 4.3, w: 2.0, h: 0.4, fontSize: 15, bold: true, color: K.groen, align: 'center', margin: 0, isTextBox: true, objectName: nm(2) });
  kaart(s, 3, 0.6, 5.2, 5.95, 1.55, 'Tellen', md('Links: 4 H en 2 O. Rechts: 4 H en 2 O. **Geen** atomen bijgekomen of verdwenen.'), { fs: 16 });
  s.addText([{ text: 'Omzetting ', options: { bold: true, color: K.lab } }, { text: '= chemische reactie: de atomen vormen nieuwe groepjes, er ontstaat een nieuwe stof.', options: { color: K.wit } }],
    { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 6.75, y: 5.2, w: 5.95, h: 1.55, fill: { color: K.donker }, line: { color: K.donker }, fontSize: 17, margin: [4, 14, 4, 14], valign: 'middle', objectName: nm(4) });

  // 10 OEFENING GEBIED
  const SA = ['samenstelling', K.groen, K.mint], EI = ['eigenschap', BL, BLL], OM = ['omzetting', GR, GRL];
  oefening('Lesdoel 1.1 · Oefening', 'Welk onderzoeksgebied?', S1, 'Een chemicus stelt deze vragen. Over welk gebied gaat elke vraag?', [
    ['Uit welke atomen bestaat koolstofdioxide?', ...SA], ['Bij welke temperatuur smelt ijzer?', ...EI], ['Wat ontstaat er als aardgas verbrandt?', ...OM],
    ['Lost zout op in water?', ...EI], ['Hoe ontstaat roest op ijzer?', ...OM], ['Welke kleur heeft koper?', ...EI]], 1);

  // 11-12 GEVARENSYMBOLEN
  pres.addSection({ title: '1.2 Veilig omgaan met stoffen' });
  const S2 = '1.2 Veilig omgaan met stoffen';
  const PICTOS = [
    ['GHS01', 'Ontplofbaar', 'kan ontploffen door een schok, wrijving, vuur of warmte', 'vuurwerk'],
    ['GHS02', 'Ontvlambaar', 'vat heel gemakkelijk vlam', 'aceton, alcohol, benzine'],
    ['GHS03', 'Oxiderend', 'helpt een brand: het vuur wordt groter en heviger', 'kaliumpermanganaat'],
    ['GHS04', 'Gas onder druk', 'de fles kan ontploffen bij warmte', 'gasfles met propaan of CO₂'],
    ['GHS05', 'Bijtend', 'beschadigt huid en ogen ernstig, tast metalen aan', 'ontstopper, zoutzuur'],
    ['GHS06', 'Giftig', 'een kleine hoeveelheid kan al dodelijk zijn', 'methanol, rattengif'],
    ['GHS07', 'Schadelijk of irriterend', 'irriteert huid of ogen; minder erg dan giftig', 'sommige wasmiddelen'],
    ['GHS08', 'Gevaar voor de gezondheid', 'kan je op lange termijn ernstig ziek maken', 'benzine, terpentine'],
    ['GHS09', 'Gevaarlijk voor het milieu', 'giftig voor planten en dieren, vooral in water', 'bleekwater, insectengif']];
  s = nieuw('Lesdoel 1.2 · Veilig omgaan met stoffen', 'De 9 gevarensymbolen', S2);
  s.addText('Een rode ruit, witte achtergrond, zwart teken. Overal in Europa hetzelfde. Wat betekent elk symbool?', { x: 0.6, y: 1.5, w: 12.1, h: 0.45, fontSize: 18, color: K.tekst, margin: 0, isTextBox: true, objectName: vast() });
  PICTOS.forEach(([id, naam], i) => {
    const x = 0.75 + i * 1.36;
    s.addImage({ path: png(id).path, x, y: 2.4, w: 1.2, h: 1.2, objectName: vast(), altText: naam });
    s.addText(String(i + 1), { x, y: 3.7, w: 1.2, h: 0.35, fontSize: 15, bold: true, color: K.grijs, align: 'center', margin: 0, isTextBox: true, objectName: vast() });
    s.addText(naam, { x: x - 0.05, y: 4.1, w: 1.3, h: 0.9, fontSize: 13, bold: true, color: K.groen, align: 'center', valign: 'top', margin: 0, isTextBox: true, objectName: nm(i + 1) });
  });
  kaart(s, 10, 0.6, 5.4, 12.1, 1.2, 'Tip', md('Kijk naar het **teken** in de ruit en zeg wat je ziet: een vlam, een doodshoofd, een gasfles … Dat helpt je de naam te onthouden.'), { fs: 17, inline: true });

  [[0, 5], [5, 9]].forEach(([a, b], k) => {
    s = nieuw('Lesdoel 1.2 · Veilig omgaan met stoffen', `Wat betekent het symbool? (${k + 1}/2)`, S2);
    PICTOS.slice(a, b).forEach(([id, naam, bet, vb], j) => {
      const y = 1.6 + j * 1.07;
      s.addImage({ path: png(id).path, x: 0.6, y, w: 0.95, h: 0.95, objectName: vast(), altText: naam });
      s.addText(naam, { x: 1.75, y, w: 3.2, h: 0.95, fontSize: 19, bold: true, color: K.donker, valign: 'middle', margin: 0, isTextBox: true, objectName: vast() });
      kaart(s, j + 1, 5.0, y + 0.03, 7.7, 0.9, '', [{ text: bet, b: false }, { text: '  · bv. ' + vb }], { fs: 15 });
    });
  });

  // 14 ETIKET
  s = nieuw('Lesdoel 1.2 · Veilig omgaan met stoffen', 'Een etiket lezen', S2);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.1, x: 0.6, y: 1.6, w: 6.0, h: 5.2, fill: { color: 'FFFFFF' }, line: { color: '94A3B8', width: 1.5 }, shadow: { type: 'outer', color: '000000', opacity: 0.15, blur: 6, offset: 2, angle: 90 }, objectName: vast() });
  s.addText([{ text: 'Buisvrij', options: { bold: true, fontSize: 26, breakLine: true } }, { text: 'Ontstopper voor afvoeren', options: { fontSize: 14, breakLine: true } }, { text: 'Bevat: natriumhydroxide', options: { fontSize: 14 } }],
    { x: 0.9, y: 1.8, w: 3.6, h: 1.25, color: K.tekst, margin: 0, valign: 'top', isTextBox: true, objectName: vast() });
  s.addImage({ path: png('GHS05').path, x: 4.85, y: 1.75, w: 1.45, h: 1.45, objectName: vast(), altText: 'Bijtend' });
  s.addText('GEVAAR', { x: 0.9, y: 3.2, w: 5.4, h: 0.5, fontSize: 22, bold: true, color: RO, margin: 0, isTextBox: true, objectName: vast() });
  s.addText([{ text: 'H290 ', options: { bold: true } }, { text: 'Kan bijtend zijn voor metalen.', options: { breakLine: true } }, { text: 'H314 ', options: { bold: true } }, { text: 'Veroorzaakt ernstige brandwonden en oogletsel.' }],
    { x: 0.9, y: 3.75, w: 5.4, h: 0.9, fontSize: 13, color: K.tekst, margin: 0, valign: 'top', isTextBox: true, objectName: vast() });
  s.addText([{ text: 'P102 ', options: { bold: true } }, { text: 'Buiten het bereik van kinderen houden.', options: { breakLine: true } }, { text: 'P280 ', options: { bold: true } }, { text: 'Beschermende handschoenen/oogbescherming dragen.', options: { breakLine: true } }, { text: 'P305+P351+P338 ', options: { bold: true } }, { text: 'BIJ CONTACT MET DE OGEN: voorzichtig afspoelen met water …' }],
    { x: 0.9, y: 4.75, w: 5.4, h: 1.8, fontSize: 13, color: K.tekst, margin: 0, valign: 'top', isTextBox: true, objectName: vast() });
  // nummers op het etiket
  [[0.45, 1.85], [6.45, 1.75], [0.45, 3.25], [0.45, 3.8], [0.45, 4.8]].forEach(([x, y], i) => nummer(s, i + 1, x - 0.2, y, i + 1, K.groen, 0.4));
  [['Naam en inhoud', 'wat is het product, welke gevaarlijke stof zit erin?'], ['Gevarensymbool', md('hier: **bijtend**')],
   ['Signaalwoord', md('**Gevaar** = ernstig, **Waarschuwing** = minder ernstig')], ['H-zinnen', md('wat is het **gevaar**?')], ['P-zinnen', md('wat moet jij doen: de **voorzorg**')]]
    .forEach(([t, u], i) => { kaart(s, i + 1, 7.55, 1.6 + i * 1.05, 5.15, 0.92, t, u, { fs: 15, inline: true }); nummer(s, i + 1, 7.0, 1.8 + i * 1.05, i + 1, K.groen, 0.45); });

  // 15 H OF P
  s = nieuw('Lesdoel 1.2 · Veilig omgaan met stoffen', 'H-zin of P-zin?', S2);
  [['H', 'hazard = gevaar', 'Een H-zin zegt wat het **gevaar** is: wat kan de stof met jou of met de natuur doen?', 'veroorzaakt … · kan … · schadelijk … · giftig … · ontvlambaar …', RO, ROL],
   ['P', 'precaution = voorzorg', 'Een P-zin zegt wat **jij moet doen** om veilig te zijn. Het is een opdracht.', 'dragen · houden · spoelen · niet inademen · niet roken …', GR, GRL]]
    .forEach(([l, en, uitleg, woorden, kl, fl], i) => {
      const x = 0.6 + i * 6.2, st = i * 2;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { rectRadius: 0.12, x, y: 1.65, w: 5.9, h: 5.1, fill: { color: fl }, line: { color: fl }, objectName: nm(st + 1) });
      s.addText(l, { shape: pres.shapes.OVAL, x: x + 0.35, y: 1.95, w: 1.2, h: 1.2, fill: { color: kl }, line: { color: kl }, color: K.wit, fontSize: 44, bold: true, align: 'center', valign: 'middle', margin: 0, objectName: nm(st + 1) });
      s.addText(en, { x: x + 1.8, y: 2.2, w: 3.9, h: 0.7, fontSize: 22, bold: true, color: kl, valign: 'middle', margin: 0, isTextBox: true, objectName: nm(st + 1) });
      s.addText(md(uitleg).map(r => ({ text: r.text, options: { bold: !!r.b } })), { x: x + 0.35, y: 3.45, w: 5.2, h: 1.4, fontSize: 18, color: K.tekst, valign: 'top', margin: 0, isTextBox: true, objectName: nm(st + 1) });
      s.addText([{ text: 'Typische woorden', options: { bold: true, color: kl, breakLine: true } }, { text: woorden }],
        { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x: x + 0.35, y: 5.05, w: 5.2, h: 1.4, fill: { color: K.wit }, line: { color: K.wit }, fontSize: 16, color: K.tekst, margin: [6, 12, 6, 12], valign: 'middle', objectName: nm(st + 2) });
    });

  // 16 OEFENING H/P
  const H = c => ['gevaar · ' + c, RO, ROL], P = c => ['voorzorg · ' + c, GR, GRL];
  oefening('Lesdoel 1.2 · Oefening', 'Gevaar of voorzorg?', S2, 'Zegt de zin wat het gevaar is (H)? Of wat jij moet doen (P)?', [
    ['Licht ontvlambare vloeistof en damp.', ...H('H225')], ['Buiten het bereik van kinderen houden.', ...P('P102')], ['Schadelijk bij inslikken.', ...H('H302')],
    ['Voorkom lozing in het milieu.', ...P('P273')], ['Veroorzaakt ernstige oogirritatie.', ...H('H319')], ['Damp niet inademen.', ...P('P260')],
    ['Kan slaperigheid of duizeligheid veroorzaken.', ...H('H336')], ['Beschermende handschoenen dragen.', ...P('P280')]], 1);

  // 17 VERANTWOORD GEBRUIK
  s = nieuw('Lesdoel 1.2 · Veilig omgaan met stoffen', 'Verantwoord omgaan met producten', S2);
  [['In het labo', ['Draag een **veiligheidsbril** en een labojas; bind lange haren samen.', 'Lees eerst het **etiket**: symbool, H- en P-zinnen.', '**Niet eten of drinken** in het labo. Ruik nooit rechtstreeks aan een stof.', 'Restafval in het **juiste afvalvat**, niet in de gootsteen.'], BL, 'E3ECFD'],
   ['Thuis', ['Bewaar producten in de **originele verpakking**.', 'Zet ze **buiten het bereik van kinderen**.', 'Meng **nooit** producten, bv. bleekwater met ontkalker.', 'Breng resten naar een **Recypark** van Net Brussel of naar **Proxy Chimik**.'], GR, GRL]]
    .forEach(([t, regels, kl, fl], i) => {
      const x = 0.6 + i * 6.2;
      s.addText(t, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x, y: 1.6, w: 5.9, h: 0.7, fill: { color: kl }, line: { color: kl }, fontSize: 22, bold: true, color: K.wit, valign: 'middle', margin: [2, 14, 2, 14], objectName: nm(i * 4 + 1) });
      regels.forEach((r, j) => kaart(s, i * 4 + 1 + j, x, 2.5 + j * 1.08, 5.9, 0.95, '', md(r), { fs: 16, fill: fl }));
    });

  // 17 SAMENVATTING
  pres.addSection({ title: 'Samenvatting' });
  s = pres.addSlide({ masterName: 'TITEL', sectionTitle: 'Samenvatting' });
  s.addText('Samenvatting', { x: 0.6, y: 0.4, w: 12, h: 0.8, fontSize: 36, bold: true, color: K.wit, margin: 0, isTextBox: true, objectName: vast() });
  [['Fysica of chemie?', 'nieuwe stof → chemisch verschijnsel; zelfde stof → fysisch'], ['Nieuwe stof herkennen', 'kleur, gas, geur, licht of warmte, niet meer terug'],
   ['Chemie onderzoekt', 'samenstelling, eigenschappen en omzettingen van stoffen'], ['Omzetting', 'atomen vormen nieuwe groepjes; geen atomen erbij of weg'],
   ['Gevarensymbolen', '9 rode ruiten met een zwart teken, overal in Europa hetzelfde'], ['Etiket', 'naam, symbool, signaalwoord, H-zinnen en P-zinnen; lees het altijd eerst'],
   ['H-zin', 'hazard: zegt wat het gevaar is'], ['P-zin', 'precaution: zegt wat jij moet doen']]
    .forEach(([t, u], i) => {
      const x = 0.6 + (i % 2) * 6.2, y = 1.45 + Math.floor(i / 2) * 1.4;
      s.addText([{ text: t, options: { bold: true, color: K.lab, fontSize: 18, breakLine: true } }, { text: u, options: { color: K.wit, fontSize: 16 } }],
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
