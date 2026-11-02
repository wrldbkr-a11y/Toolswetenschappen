const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType,
        AlignmentType, LevelFormat, BorderStyle, ExternalHyperlink, Footer, PageNumber, TableOfContents } = require('docx');
const BASIS = 'https://wrldbkr-a11y.github.io/Toolswetenschappen/';
const water = JSON.parse(fs.readFileSync('/home/claude/wv/water_data.json'));
const rest = require('./rest.js').DELEN;
const conv = d => ({ t: d.titel, doel: d.doel, w: d.wv.map(x => [x.n, x.d, x.g, x.m, x.s]) });
const VAKKEN = [
 { vak: 'Biologie', kleur: '3E8E41', tools: [
   { tool: 'Homeostase van de waterhuishouding in planten (cursus en tool)', bestand: 'cursus-waterhuishouding-planten.html', jaar: '3de jaar', items: water.map(conv) },
   { tool: 'Water, prikkels en reacties: feedback, receptoren en effectoren', bestand: 'biologie-prikkels.html', jaar: '3de jaar', items: rest.map(conv) } ] },
 { vak: 'Chemie', kleur: 'D46A1A', tools: require('./chem.js') },
 { vak: 'Fysica', kleur: '2F6FB0', tools: [...require('./fys3.js'), ...require('./fys45.js')] },
];
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
kids.push(new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun({ text: 'Activerende werkvormen wetenschappen', font: FONT })] }));
kids.push(p([r('Bundel bij de tools en cursussen op Oefentools wetenschappen · biologie, chemie en fysica', { bold: true, color: GRIJS, size: 24 })]));
kids.push(p('Deze bundel geeft per onderdeel van elke tool één tot drie activerende werkvormen. Kies wat bij je klas past en schrap de rest. De werkvormen houden rekening met een taalzwakke klas: vaste zinsmodellen, veel visuele steun en eerst zelf denken voor je spreekt.'));
kids.push(p([r('Groepering: ', { bold: true }), r('I = individueel · D = in duo · G = in groepjes van 3 à 4 · K = klassikaal. Een pijl (I → D → K) toont de volgorde.')]));
kids.push(p([r('Veiligheid: ', { bold: true }), r('controleer bij proeven met vuur, lasers, hoogspanning of chemicaliën altijd de schoolregels en voorzie een veiligheidsbril.')]));
kids.push(new Paragraph({ pageBreakBefore: true, spacing: { after: 200 }, children: [new TextRun({ text: 'Inhoud', font: FONT, bold: true, size: 32 })] }));
kids.push(new TableOfContents('Inhoud', { hyperlink: true, headingStyleRange: '1-3' }));
let teller = 0;
VAKKEN.forEach(V => {
  kids.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun({ text: V.vak, font: FONT, color: V.kleur })] }));
  V.tools.forEach((T, ti) => {
    kids.push(new Paragraph({ heading: HeadingLevel.HEADING_2, pageBreakBefore: ti > 0, children: [new TextRun({ text: `${T.tool}`, font: FONT, color: V.kleur })] }));
    kids.push(p([r(T.jaar + ' · ', { color: GRIJS }), new ExternalHyperlink({ link: BASIS + T.bestand, children: [new TextRun({ text: BASIS + T.bestand, font: FONT, size: 18, style: 'Hyperlink' })] })]));
    T.items.forEach(I => {
      kids.push(new Paragraph({ heading: HeadingLevel.HEADING_3, keepNext: true, children: [new TextRun({ text: I.t, font: FONT })] }));
      kids.push(p([r('Lesdoel: ', { bold: true }), r(I.doel, { italics: true, color: GRIJS })], { keepNext: true }));
      I.w.forEach(([n, d, g, m, st]) => {
        teller++;
        kids.push(new Paragraph({ keepNext: true, spacing: { before: 160, after: 80 }, children: [new TextRun({ text: `${teller}. ${n}`, font: FONT, bold: true, size: 23, color: V.kleur })] }));
        kids.push(infoTabel({ d, g, m }));
        kids.push(p([r('Verloop', { bold: true })], { spacing: { before: 100, after: 60 }, keepNext: true }));
        st.forEach((x, si) => kids.push(new Paragraph({ numbering: { reference: `stap${teller}`, level: 0 }, spacing: { after: 60 }, keepNext: si < st.length - 1, keepLines: true, children: [r(x)] })));
      });
    });
  });
});
const numbering = { config: [] };
for (let i = 1; i <= teller; i++) numbering.config.push({ reference: `stap${i}`, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 300 } } } }] });
const doc = new Document({
  features: { updateFields: true },
  styles: { default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: 'Title', name: 'Title', basedOn: 'Normal', run: { size: 48, bold: true, color: '1D2A36', font: FONT }, paragraph: { spacing: { after: 160 } } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 40, bold: true, font: FONT }, paragraph: { spacing: { after: 200 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 30, bold: true, font: FONT }, paragraph: { spacing: { before: 120, after: 80 }, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 25, bold: true, color: '1D2A36', font: FONT }, paragraph: { spacing: { before: 300, after: 60 }, outlineLevel: 2, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'C9D6C9', space: 2 } } } } ] },
  numbering,
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1300, bottom: 1300, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: 'Activerende werkvormen wetenschappen · p. ', font: FONT, size: 18, color: GRIJS }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18, color: GRIJS })] })] }) },
    children: kids }]
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync('/home/claude/wv/Activerende_werkvormen_wetenschappen_bundel.docx', b); console.log('ok', teller); });
