const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType,
        AlignmentType, LevelFormat, BorderStyle, ExternalHyperlink, PageBreak, Footer, PageNumber } = require('docx');


// ---------- inhoud ----------
const CFG = require(process.argv[2]);
const DELEN = CFG.DELEN, TOOL = 'https://wrldbkr-a11y.github.io/Toolswetenschappen/biologie-prikkels.html', CURSUS = CFG.CURSUS;
// ---------- opmaak ----------
const FONT = 'Arial', GROEN = '3E8E41', LICHT = 'E8F3E8', GRIJS = '51606E';
const W = 9026; // A4 met marges van 1 inch
const rand = { style: BorderStyle.SINGLE, size: 4, color: 'C9D6C9' };
const randen = { top: rand, bottom: rand, left: rand, right: rand };
const p = (t, o = {}) => new Paragraph({ spacing: { after: 100 }, ...o, children: Array.isArray(t) ? t : [new TextRun({ text: t, font: FONT, size: 22 })] });
const r = (text, o = {}) => new TextRun({ text, font: FONT, size: 22, ...o });

function infoTabel(w) {
  const rij = (k, v) => new TableRow({ cantSplit: true, children: [
    new TableCell({ width: { size: 1800, type: WidthType.DXA }, borders: randen, shading: { fill: LICHT, type: ShadingType.CLEAR, color: 'auto' }, margins: { top: 60, bottom: 60, left: 110, right: 110 }, children: [p([r(k, { bold: true })], { spacing: { after: 0 }, keepNext: true, keepLines: true })] }),
    new TableCell({ width: { size: W - 1800, type: WidthType.DXA }, borders: randen, margins: { top: 60, bottom: 60, left: 110, right: 110 }, children: [p([r(v)], { spacing: { after: 0 }, keepNext: true, keepLines: true })] }) ] });
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [1800, W - 1800], rows: [rij('Duur', w.d), rij('Groepering', w.g), rij('Materiaal', w.m)] });
}

const kids = [];
kids.push(new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun({ text: 'Activerende werkvormen', font: FONT })] }));
kids.push(p([r(CFG.ONDERTITEL, { bold: true, color: GROEN, size: 24 })]));
kids.push(p(CFG.INLEIDING + ' Ze houden rekening met een taalzwakke klas: vaste zinsmodellen, veel visuele steun en eerst zelf denken voor je spreekt.'));
if (CFG.CURSUS) kids.push(p([r('Cursus: '), new ExternalHyperlink({ link: CURSUS, children: [new TextRun({ text: CURSUS, font: FONT, size: 20, style: 'Hyperlink' })] })]));
kids.push(p([r('Tool: '), new ExternalHyperlink({ link: TOOL, children: [new TextRun({ text: TOOL, font: FONT, size: 20, style: 'Hyperlink' })] })]));
kids.push(p([r('Groepering: ', { bold: true }), r('I = individueel · D = in duo · G = in groepjes van 3 à 4 · K = klassikaal. Een pijl (I → D → K) toont de volgorde.')]));

let teller = 0;
DELEN.forEach((d, di) => {
  kids.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: di > 0, children: [new TextRun({ text: d.titel, font: FONT })] }));
  kids.push(p([r('Lesdoel: ', { bold: true }), r(d.doel, { italics: true, color: GRIJS })]));
  d.wv.forEach((w, wi) => {
    teller++;
    kids.push(new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, children: [new TextRun({ text: `${teller}. ${w.n}`, font: FONT })] }));
    kids.push(infoTabel(w));
    kids.push(p([r('Verloop', { bold: true })], { spacing: { before: 120, after: 60 }, keepNext: true }));
    w.s.forEach((st, si) => kids.push(new Paragraph({ numbering: { reference: `stap${teller}`, level: 0 }, spacing: { after: 60 }, keepNext: si < w.s.length - 1, keepLines: true, children: [r(st)] })));
  });
});

const numbering = { config: [] };
for (let i = 1; i <= teller; i++) numbering.config.push({ reference: `stap${i}`, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 300 } } } }] });

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: 'Title', name: 'Title', basedOn: 'Normal', run: { size: 44, bold: true, color: '1D2A36', font: FONT }, paragraph: { spacing: { after: 120 } } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 32, bold: true, color: GROEN, font: FONT }, paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 25, bold: true, color: '1D2A36', font: FONT }, paragraph: { spacing: { before: 280, after: 100 }, outlineLevel: 1 } } ] },
  numbering,
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: CFG.VOET + ' · p. ', font: FONT, size: 18, color: GRIJS }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18, color: GRIJS })] })] }) },
    children: kids }]
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(CFG.UIT, b); console.log('ok', teller); });
