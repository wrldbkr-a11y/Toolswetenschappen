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

