const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  AlignmentType, LevelFormat, TabStopType, ImageRun, ExternalHyperlink, Footer, Header, PageNumber, TableOfContents, PageBreak, PageOrientation } = require('docx');

const D = JSON.parse(fs.readFileSync('/home/claude/word/data/cursus.json'));
const UIT = process.argv[2] || '/home/claude/word/Cursus_Elektrostatica_5Wet.docx';
const META = Object.assign({ boven: 'FYSICA 5DE JAAR · THEMA 1', titel: 'Elektrostatica', sub: 'Ladingen · Krachten tussen ladingen · Elektrisch veld · Potentiaal', maker: 'Fysica 5de jaar',
  intro: 'Deze cursus hoort bij de tools op Oefentools wetenschappen. De nummering van definities, vergelijkingen en figuren loopt per hoofdstuk. Oefeningen maak je op papier, in je schrift. De redeneringen bij de denkvragen en de oplossingen van de oefeningen staan in de bijlage achteraan.' },
  process.argv[3] ? JSON.parse(process.argv[3]) : {});
const SERIF = 'Cambria', SANS = 'Calibri';
const NAVY = '1F3A5F', DIM = '51606E', W = 9026;

let lijstInstantie = 0;
const runs = (rs, extra = {}) => (rs || []).map(r => r.br ? new TextRun({ break: 1 }) :
  new TextRun({ text: r.t, bold: r.b || extra.bold, italics: r.i || extra.italics, subScript: r.sub, superScript: r.sup, font: extra.font || SERIF, size: extra.size, color: extra.color }));
const par = (rs, o = {}) => new Paragraph({ spacing: { after: 100, line: 300 }, ...o, children: Array.isArray(rs) && rs[0] instanceof TextRun ? rs : runs(rs, o.run || {}) });

function doos(kinderen, { fill = 'FFFFFF', rand = NAVY, links = 24, stijl = BorderStyle.SINGLE, alle = 'D9D6CC' } = {}) {
  const b = { style: stijl, size: 4, color: alle };
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [W],
    rows: [new TableRow({ cantSplit: true, children: [new TableCell({ width: { size: W, type: WidthType.DXA },
      shading: { fill, type: ShadingType.CLEAR, color: 'auto' }, margins: { top: 100, bottom: 100, left: 180, right: 180 },
      borders: { top: b, bottom: b, right: b, left: { style: BorderStyle.SINGLE, size: links, color: rand } }, children: kinderen })] })] });
}
const ruimte = () => new Paragraph({ spacing: { after: 60 }, children: [] });

function blokken(items, ctx) {
  const out = [];
  for (const it of items) {
    switch (it.type) {
      case 'p': out.push(par(it.runs)); break;
      case 'h3': out.push(new Paragraph({ heading: HeadingLevel.HEADING_3, keepNext: true, children: [new TextRun({ text: it.t })] })); break;
      case 'h4': out.push(new Paragraph({ heading: HeadingLevel.HEADING_4, keepNext: true, children: [new TextRun({ text: it.t })] })); break;
      case 'ul': {
        const ref = ctx.doelen ? 'vink' : 'bol';
        it.items.forEach(li => out.push(new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 60, line: 290 }, children: runs(li) })));
        break; }
      case 'ol': {
        const inst = ++lijstInstantie;
        it.items.forEach(li => out.push(new Paragraph({ numbering: { reference: it.letters ? 'letter' : 'cijfer', level: 0, instance: inst }, spacing: { after: 60, line: 290 }, children: runs(li) })));
        break; }
      case 'table': {
        const nk = Math.max(...it.rows.map(r => r.length));
        if (nk > 2 || it.grid) {   // echte tabel met rasterlijnen; eerste rij als kop
          const rand = { style: BorderStyle.SINGLE, size: 4, color: 'B8C2CC' };
          const ws = Array.from({ length: nk }, () => Math.floor(W / nk));
          out.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: ws,
            rows: it.rows.map((r, ri) => new TableRow({ cantSplit: true, tableHeader: ri === 0, children: ws.map((w, k) => new TableCell({ width: { size: w, type: WidthType.DXA },
              borders: { top: rand, bottom: rand, left: rand, right: rand }, shading: ri === 0 ? { type: ShadingType.CLEAR, fill: 'E8EEF4', color: 'auto' } : undefined,
              margins: { top: 30, bottom: 30, left: 70, right: 70 }, children: [new Paragraph({ children: runs(r[k] || [], Object.assign({ size: 19 }, ri === 0 ? { bold: true, color: NAVY } : {})) })] })) })) }));
          out.push(ruimte()); break;
        }
        const ws = [1900, W - 1900];
        out.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: ws,
          rows: it.rows.map(r => new TableRow({ cantSplit: true, children: r.slice(0, 2).map((c, k) => new TableCell({ width: { size: ws[k], type: WidthType.DXA },
            borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
            margins: { top: 20, bottom: 20, left: 60, right: 60 }, children: [new Paragraph({ children: runs(c, k === 0 ? { bold: true, color: NAVY } : {}) })] })) })) }));
        out.push(ruimte()); break; }
      case 'fig': {
        const f = ctx.figs[it.i];
        if (it.liggend) {   // aparte liggende pagina, zo groot mogelijk
          const sch = Math.min(1000 / f.w, 600 / f.h);
          out.push({ __liggend: [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new ImageRun({ type: 'png', data: fs.readFileSync(f.f), transformation: { width: Math.round(f.w * sch), height: Math.round(f.h * sch) }, altText: { title: 'figuur', description: (it.cap || []).map(r => r.t || '').join(''), name: 'figuur' } })] }),
            new Paragraph({ alignment: AlignmentType.CENTER, children: runs(it.cap, { size: 19, color: DIM }) })] });
          break; }
        const maxw = 590; const sch = Math.min(1, maxw / f.w);
        out.push(new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 120, after: 40 },
          children: [new ImageRun({ type: 'png', data: fs.readFileSync(f.f), transformation: { width: Math.round(f.w * sch), height: Math.round(f.h * sch) }, altText: { title: 'figuur', description: (it.cap || []).map(r => r.t || '').join(''), name: 'figuur' } })] }));
        out.push(new Paragraph({ spacing: { after: 200 }, children: runs(it.cap, { size: 19, color: DIM }) }));
        break; }
      case 'tool': out.push(new Paragraph({ spacing: { after: 100 }, children: [new TextRun({ text: 'Online: ', font: SANS, size: 19, color: DIM }), new ExternalHyperlink({ link: it.href.replace('file:///home/claude/toolswetenschappen/', 'https://wrldbkr-a11y.github.io/Toolswetenschappen/'), children: [new TextRun({ text: it.t, style: 'Hyperlink', font: SANS, size: 19 })] })] })); break;
      case 'vgl': out.push(new Paragraph({ tabStops: [{ type: TabStopType.CENTER, position: W / 2 }, { type: TabStopType.RIGHT, position: W }], spacing: { before: 120, after: 160 },
        children: [new TextRun({ text: '\t', font: SERIF }), ...runs(it.runs, { size: 26 }), new TextRun({ text: '\t' + it.n, font: SERIF, color: DIM })] })); break;
      case 'def': out.push(doos([new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: it.kop, bold: true, font: SANS, color: it.wet ? '8A2B2B' : NAVY, size: 20 })] }), ...blokken(it.body, ctx)],
        { fill: 'FFFFFF', rand: it.wet ? '8A2B2B' : NAVY })); out.push(ruimte()); break;
      case 'vb': out.push(doos([new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: it.kop, bold: true, font: SANS, size: 20 })] }), ...blokken(it.body, ctx)], { fill: 'F6F5F1', rand: 'B8B3A3', links: 4 })); out.push(ruimte()); break;
      case 'kader': out.push(doos([new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: it.kop, bold: true, font: SANS, color: NAVY, size: 20 })] }), ...blokken(it.body, ctx)], { fill: 'EAEFF5' })); out.push(ruimte()); break;
      case 'verd': out.push(doos([new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: it.kop.toUpperCase(), bold: true, font: SANS, color: '6B5D33', size: 18 })] }), ...blokken(it.body, ctx)], { fill: 'FBF8F0', rand: '8A7F63', stijl: BorderStyle.DASHED, alle: '8A7F63', links: 4 })); out.push(ruimte()); break;
      case 'denk': {
        const nr = ++ctx.denk; ctx.bijlage.push({ soort: 'denk', nr, it });
        out.push(doos([new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: `DENKVRAAG ${nr}`, bold: true, font: SANS, color: '9A5B00', size: 18 })] }),
          par(it.vraag), new Paragraph({ children: [new TextRun({ text: (META.geenBijlage ? 'Denk eerst zelf na. De redenering staat online in de cursus.' : 'Denk eerst zelf na. De redenering staat in de bijlage achteraan.'), italics: true, font: SERIF, size: 19, color: DIM })] })],
          { fill: 'FFF4D6', rand: '9A5B00', alle: 'F2D9A0' })); out.push(ruimte()); break; }
      case 'oef': {
        ctx.bijlage.push({ soort: 'oef', it });
        out.push(new Paragraph({ keepNext: true, spacing: { before: 200, after: 60 }, children: [new TextRun({ text: `Oefening ${it.nr} · ${it.titel}`, bold: true, font: SANS, color: NAVY, size: 22 })] }));
        out.push(...blokken(it.body, ctx)); break; }
      default: break;
    }
  }
  return out;
}

const kids = [];
// titelpagina
kids.push(new Paragraph({ spacing: { before: 2400, after: 120 }, children: [new TextRun({ text: META.boven, font: SANS, bold: true, color: NAVY, size: 22 })] }));
kids.push(new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: META.titel, font: SANS, bold: true, size: 64, color: '1D2A36' })] }));
kids.push(new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 6 } }, spacing: { after: 240 }, children: [new TextRun({ text: META.sub, font: SERIF, size: 26, color: DIM })] }));
kids.push(par([{ t: META.intro }]));
kids.push(new Paragraph({ spacing: { before: 600, after: 60 }, children: [new TextRun({ text: 'Gemaakt door de vakgroep wetenschappen · Maria Assumpta Lyceum · ontwikkeld met hulp van AI', font: SANS, size: 18, color: DIM })] }));
kids.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: 'Licentie: CC BY-NC-SA 4.0. Je mag dit materiaal gebruiken en aanpassen, niet commercieel, met naamsvermelding en onder dezelfde licentie.', font: SANS, size: 18, color: DIM })] }));
kids.push(new Paragraph({ spacing: { before: 600 }, children: [new TextRun({ text: 'Naam: ______________________________     Klas: ________', font: SANS, size: 22 })] }));
kids.push(new Paragraph({ children: [new PageBreak()] }));
kids.push(new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: 'Inhoud', font: SANS, bold: true, size: 32, color: NAVY })] }));
kids.push(new TableOfContents('Inhoud', { hyperlink: true, headingStyleRange: '1-2' }));

const bijlagen = [];
// kop per hoofdstuk: standaard 'Hoofdstuk n', of uit de eyebrow ('Thema 2 · Hoofdstuk 1') als META.kopUitEyebrow
const kopVan = (H, h) => { if (META.vasteKop) return META.vasteKop; if (META.kopUitEyebrow) { const m = H.eyebrow.match(/Thema (\d+).*Hoofdstuk (\d+)/); if (m) return `Thema ${m[1]} · Hoofdstuk ${m[2]}`; } return `Hoofdstuk ${h}`; };
D.forEach((H, hi) => {
  const h = hi + 1;
  const ctx = { h, figs: H.figs, denk: 0, bijlage: [] };
  kids.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun(`${kopVan(H, h)} · ${H.titel}`)] }));
  kids.push(new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: H.eyebrow, font: SANS, size: 18, color: DIM })] }));
  H.secties.forEach(S => {
    if (S.id === 'cornell') return;
    kids.push(new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, pageBreakBefore: S.id === 'oefeningen', children: [new TextRun((S.nr ? S.nr + '  ' : '') + S.titel)] }));
    ctx.doelen = S.id === 'lesdoelen' || S.id === 'voorkennis';
    kids.push(...blokken(S.body, ctx));
  });
  bijlagen.push({ h, kop: kopVan(H, h), titel: H.titel, items: ctx.bijlage, opl: H.opl || [] });
});

// bijlage (niet bij META.geenBijlage: dan staan redeneringen en oplossingen alleen online)
if (!META.geenBijlage) {
kids.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun('Bijlage · Redeneringen en oplossingen')] }));
kids.push(par([{ t: 'Kijk pas hier nadat je zelf hebt nagedacht en de oefening hebt gemaakt.', i: true }]));
bijlagen.forEach(B => {
  kids.push(new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, children: [new TextRun(`${B.kop} · ${B.titel}`)] }));
  B.items.forEach(x => {
    const kop = x.soort === 'denk' ? `Denkvraag ${x.nr}` : `Oefening ${x.it.nr} · ${x.it.titel}`;
    kids.push(new Paragraph({ keepNext: true, spacing: { before: 160, after: 40 }, children: [new TextRun({ text: kop, bold: true, font: SANS, color: NAVY, size: 21 })] }));
    x.it.stappen.forEach(s => kids.push(new Paragraph({ spacing: { after: 40, line: 280 }, indent: { left: 280 }, children: [new TextRun({ text: s.stap + ': ', bold: true, font: SERIF }), ...runs(s.runs.map((r, i) => i === 0 && r.t ? { ...r, t: r.t.replace(/^\s+/, '') } : r))] })));
    (x.it.opl || []).forEach(k => { const f = B.opl[k]; if (!f) return;
      if (f.w > 1000) { const s2 = Math.min(1000 / f.w, 600 / f.h); kids.push({ __liggend: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new ImageRun({ type: 'png', data: fs.readFileSync(f.f), transformation: { width: Math.round(f.w * s2), height: Math.round(f.h * s2) }, altText: { title: 'oplossing', description: 'oplossing', name: 'oplossing' } })] })] }); return; }
      const sch = Math.min(1, 520 / f.w);
      kids.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60, after: 60 }, children: [new ImageRun({ type: 'png', data: fs.readFileSync(f.f), transformation: { width: Math.round(f.w * sch), height: Math.round(f.h * sch) }, altText: { title: 'oplossing', description: 'oplossing', name: 'oplossing' } })] })); });
    if (x.it.besluit && x.it.besluit.length) kids.push(new Paragraph({ spacing: { after: 80 }, indent: { left: 280 }, children: [new TextRun({ text: '→ ', bold: true, font: SERIF, color: '1F7A4A' }), ...runs(x.it.besluit, { bold: true, color: '1F7A4A' })] }));
  });
});
}

const nummer = (ref, fmt, text) => ({ reference: ref, levels: [{ level: 0, format: fmt, text, alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 320 } }, run: fmt === LevelFormat.BULLET ? { font: 'Segoe UI Symbol' } : {} } }] });
const doc = new Document({
  creator: META.maker, title: META.titel,
  features: { updateFields: true },
  styles: {
    default: { document: { run: { font: SERIF, size: 22, color: '1D2A36' } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: SANS, size: 40, bold: true, color: '1D2A36' }, paragraph: { spacing: { after: 80 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: SANS, size: 30, bold: true, color: NAVY }, paragraph: { spacing: { before: 320, after: 140 }, outlineLevel: 1, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'D9D6CC', space: 4 } } } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: SANS, size: 24, bold: true, color: '1D2A36' }, paragraph: { spacing: { before: 240, after: 100 }, outlineLevel: 2 } },
      { id: 'Heading4', name: 'Heading 4', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: SANS, size: 22, bold: true, color: DIM }, paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 3 } }] },
  numbering: { config: [nummer('bol', LevelFormat.BULLET, '•'), nummer('vink', LevelFormat.BULLET, '☐'), nummer('cijfer', LevelFormat.DECIMAL, '%1.'), nummer('letter', LevelFormat.LOWER_LETTER, '%1.')] },
  sections: secties()
});
function secties() {
  const kop = () => ({ default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: META.maker + ' · ' + META.titel, font: SANS, size: 16, color: '8A96A3' })] })] }) });
  const voet = () => ({ default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: SANS, size: 18, color: '8A96A3' })] })] }) });
  const staand = { page: { size: { width: 11906, height: 16838 }, margin: { top: 1300, bottom: 1200, left: 1440, right: 1440 } } };
  const liggend = { page: { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }, margin: { top: 900, bottom: 900, left: 900, right: 900 } } };
  const uit = []; let huidig = [];
  for (const k of kids) {
    if (k && k.__liggend) {
      uit.push({ properties: staand, headers: kop(), footers: voet(), children: huidig.length ? huidig : [new Paragraph('')] });
      uit.push({ properties: liggend, headers: kop(), footers: voet(), children: k.__liggend });
      huidig = [];
    } else huidig.push(k);
  }
  uit.push({ properties: staand, headers: kop(), footers: voet(), children: huidig.length ? huidig : [new Paragraph('')] });
  return uit;
}
Packer.toBuffer(doc).then(b => { fs.writeFileSync(UIT, b); console.log('ok', UIT); });
