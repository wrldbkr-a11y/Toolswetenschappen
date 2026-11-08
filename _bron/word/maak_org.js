// Advance organizers (overzicht van het jaar) als Word-bestand, één per vak en jaar.
// Gebruik: node maak_org.js  (leest org.json en de iconen <id>_<n>.png uit deze map)
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
        ImageRun, AlignmentType, ExternalHyperlink, VerticalAlign, LevelFormat } = require('docx');

const DIR = '/home/claude/word/org';
const ORG = JSON.parse(fs.readFileSync(path.join(DIR, 'org.json'), 'utf8'));
const SITE = 'https://wrldbkr-a11y.github.io/Toolswetenschappen/';
const FONT = 'Arial', INK = '1D2A36', DIM = '51606E', DEC = '1F7A4D', JUN = '7C3AED';
const W = 9638;                      // A4 met marges van 2 cm
const geen = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const lijn = (kleur, dikte = 4) => ({ style: BorderStyle.SINGLE, size: dikte, color: kleur });

const tekst = (t, o = {}) => new TextRun({ text: t, font: FONT, size: o.size || 20, bold: o.bold, italics: o.italics, color: o.color || INK });
let HOUD = false;   // binnen een thematabel: alles bij elkaar houden
const alinea = (runs, o = {}) => new Paragraph({ spacing: { before: o.before || 0, after: o.after ?? 60 }, keepNext: o.keepNext ?? HOUD, alignment: o.align, children: runs });

function cel(kinderen, breedte, o = {}) {
  return new TableCell({ width: { size: breedte, type: WidthType.DXA }, children: kinderen, verticalAlign: o.v || VerticalAlign.TOP,
    margins: { top: o.mt ?? 60, bottom: o.mb ?? 60, left: 100, right: 100 }, columnSpan: o.span,
    shading: o.fill ? { type: ShadingType.CLEAR, color: 'auto', fill: o.fill } : undefined,
    borders: o.borders || { top: geen, bottom: geen, left: geen, right: geen } });
}

function themaTabel(o, th, i) {
  const kleur = o.kleur.replace('#', '');
  const ico = path.join(DIR, `${o.id}_${i}.png`);
  const kol = [1150, 3300, 3238, 1950];         // icoon/nummer · hoofdstuk · wat je leert · examen
  const rand = { top: lijn(kleur, 10), bottom: lijn('CBD5DE'), left: geen, right: geen };
  HOUD = true;
  const kop = new TableRow({ cantSplit: true, children: [
    cel([fs.existsSync(ico) ? alinea([new ImageRun({ type: 'png', data: fs.readFileSync(ico), transformation: { width: 44, height: 44 } })], { align: AlignmentType.CENTER, after: 0 }) : alinea([]),
         alinea([tekst(th.nr, { bold: true, size: 17, color: kleur })], { align: AlignmentType.CENTER, after: 0 })], kol[0], { borders: { ...rand, bottom: geen }, v: VerticalAlign.TOP }),
    cel([alinea([tekst(th.titel, { bold: true, size: 28 })], { after: 20 }),
         alinea([tekst(th.vraag, { bold: true, italics: true, size: 21, color: '334155' })], { after: 60 }),
         alinea([tekst(th.idee, { size: 20 })], { after: 40 }),
         alinea([tekst('Je kent al: ', { bold: true, size: 18 }), tekst(th.kent, { size: 18, color: DIM })], { after: 20 })], kol[1] + kol[2] + kol[3], { span: 3, borders: { ...rand, bottom: geen } })] });
  const rijen = th.hfd.map(([nr, titel, wat, ex, link], k) => {
    HOUD = k < th.hfd.length - 1;
    const randRij = { top: lijn('E2E8F0'), bottom: k === th.hfd.length - 1 ? lijn('CBD5DE') : geen, left: geen, right: geen };
    const titelRuns = link ? [new ExternalHyperlink({ link: SITE + link, children: [new TextRun({ text: titel, font: FONT, size: 20, bold: true, color: INK, underline: {} })] })] : [tekst(titel, { bold: true })];
    return new TableRow({ cantSplit: true, children: [
      cel([alinea([tekst('H' + nr, { bold: true, color: DIM })], { align: AlignmentType.CENTER, after: 0 })], kol[0], { borders: randRij }),
      cel([alinea(titelRuns, { after: 0 })], kol[1], { borders: randRij }),
      cel([alinea([tekst(wat, { size: 18, color: DIM })], { after: 0 })], kol[2], { borders: randRij }),
      cel([alinea([tekst(ex === 'dec' ? ' december ' : ' juni ', { bold: true, size: 17, color: ex === 'dec' ? DEC : JUN })], { align: AlignmentType.CENTER, after: 0 })], kol[3],
          { borders: randRij, fill: ex === 'dec' ? 'EAF5EE' : 'F3EEFF', v: VerticalAlign.CENTER })] });
  });
  HOUD = false;
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: kol, rows: [kop, ...rijen] });
}

function document(o) {
  const kleur = o.kleur.replace('#', '');
  const kids = [
    alinea([tekst(`${o.vak} · ${o.jaar} · ${o.richting}`, { bold: true, size: 20, color: kleur })], { after: 40 }),
    alinea([tekst('Overzicht van het jaar', { bold: true, size: 44 })], { after: 160 }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 200 }, border: { left: { style: BorderStyle.SINGLE, size: 24, color: kleur, space: 10 } },
      children: [tekst('DE GROTE VRAAG', { bold: true, size: 16, color: DIM }), new TextRun({ break: 1 }), tekst(o.vraag, { bold: true, size: 26 })] }),
    alinea([tekst(' december ', { bold: true, size: 17, color: 'FFFFFF' }), tekst('  leerstof voor het examen van december      ', { size: 17, color: DIM }),
            tekst(' juni ', { bold: true, size: 17, color: JUN }), tekst('  leerstof voor het examen van juni', { size: 17, color: DIM })], { after: 200 }),
  ];
  // markering van de legende: achtergrondkleur via shading op de run
  kids[3] = new Paragraph({ spacing: { after: 200 }, children: [
    new TextRun({ text: ' december ', font: FONT, size: 17, bold: true, color: DEC, shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'EAF5EE' } }),
    tekst('  leerstof voor het examen van december      ', { size: 17, color: DIM }),
    new TextRun({ text: ' juni ', font: FONT, size: 17, bold: true, color: JUN, shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'F3EEFF' } }),
    tekst('  leerstof voor het examen van juni', { size: 17, color: DIM })] });
  o.themas.forEach((th, i) => { kids.push(themaTabel(o, th, i)); kids.push(alinea([], { after: 160 })); });
  kids.push(alinea([tekst('Zo gebruik je dit overzicht', { bold: true, size: 22 })], { before: 120, after: 60, keepNext: true }));
  ['Begin je aan een nieuw hoofdstuk? Kijk hier eerst: bij welk thema hoort het, en wat ken je al?',
   'Lees de grote vraag van het thema. Na het thema kan je ze beantwoorden.',
   'Voor een examen: kijk welke hoofdstukken bij december of juni horen.']
    .forEach(t => kids.push(new Paragraph({ numbering: { reference: 'bol', level: 0 }, spacing: { after: 40 }, children: [tekst(t, { size: 19 })] })));
  kids.push(alinea([tekst('Een onderstreepte titel is een link naar het hoofdstuk in de online cursus.', { italics: true, size: 16, color: DIM })], { before: 120 }));
  return new Document({
    creator: 'Oefentools wetenschappen', title: `${o.vak} ${o.jaar} · overzicht van het jaar`,
    styles: { default: { document: { run: { font: FONT, size: 20 } } } },
    numbering: { config: [{ reference: 'bol', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 260 } } } }] }] },
    sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1000, bottom: 1000, left: 1134, right: 1134 } } }, children: kids }] });
}

(async () => {
  for (const o of ORG) {
    const naam = `Overzicht_${o.vak}_${o.id.split('-')[1].toUpperCase()}.docx`;
    fs.writeFileSync(path.join(DIR, naam), await Packer.toBuffer(document(o)));
    console.log('ok', naam);
  }
})();
