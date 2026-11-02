const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, BorderStyle, ShadingType, Footer, PageNumber, TabStopType, LevelFormat,
  PageBreak, VerticalAlign,
} = require("docx");

const F = "/home/claude/work/fig/";
const FONT = "Calibri";
const CM = 37.8; // px per cm

function img(name, wcm, ratio) {
  const w = Math.round(wcm * CM);
  return new ImageRun({ type: "png", data: fs.readFileSync(F + name + ".png"),
    transformation: { width: w, height: Math.round(w * ratio) } });
}
function figure(name, wcm, ratio, after = 160) {
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after }, children: [img(name, wcm, ratio)] });
}
// rich text: **bold** segments
function runs(text, extra = {}) {
  return text.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map(t =>
    t.startsWith("**") ? new TextRun({ text: t.slice(2, -2), bold: true, ...extra }) : new TextRun({ text: t, ...extra }));
}
const P = (text, opt = {}) => new Paragraph({ spacing: { after: 100 }, ...opt, children: runs(text) });
const H = (text) => new Paragraph({ spacing: { before: 240, after: 120 },
  children: [new TextRun({ text, bold: true, size: 28, color: "1F4E79" })] });
const SUB = (text) => new Paragraph({ spacing: { before: 200, after: 80 },
  children: [new TextRun({ text, bold: true, underline: {} })] });
const bullet = (text) => new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 60 }, children: runs(text) });
const num = (ref, text) => new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 80 }, children: runs(text) });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: none, bottom: none, left: none, right: none, insideHorizontal: none, insideVertical: none };

// 2x2 construction steps
const CONTENT = 9638;
const half = CONTENT / 2;
const steps = [
  ["verhoging_1", "Teken de **normaal** in elk punt waar een lichtstraal het wateroppervlak raakt."],
  ["verhoging_2", "Teken de gebroken lichtstralen in de lucht. Van water naar lucht: de straal breekt **van de normaal weg**."],
  ["verhoging_3", "**Verleng** de gebroken stralen naar achter (stippellijn) tot ze elkaar snijden. Dat snijpunt is het **schijnbaar punt V'**."],
  ["verhoging_4", "Teken in V' het **schijnbaar voorwerp** (stippellijn). Het ligt **hoger** dan het echte voorwerp."],
];
const stepCell = ([name, txt], i) => new TableCell({
  width: { size: half, type: WidthType.DXA }, borders: noBorders,
  margins: { top: 80, bottom: 120, left: 80, right: 80 },
  children: [
    new Paragraph({ alignment: AlignmentType.CENTER, children: [img(name, 8.0, 899 / 1259)] }),
    new Paragraph({ spacing: { before: 60 }, children: [new TextRun({ text: `Stap ${i + 1}: `, bold: true }), ...runs(txt)] }),
  ],
});
const stepsTable = new Table({
  width: { size: CONTENT, type: WidthType.DXA }, columnWidths: [half, half], borders: noBorders,
  rows: [0, 2].map(r => new TableRow({ cantSplit: true, children: [stepCell(steps[r], r), stepCell(steps[r + 1], r + 1)] })),
});

// "Let op" box
function box(title, lines) {
  return new Table({
    width: { size: CONTENT, type: WidthType.DXA }, columnWidths: [CONTENT],
    rows: [new TableRow({ children: [new TableCell({
      width: { size: CONTENT, type: WidthType.DXA },
      shading: { fill: "FFF4D6", type: ShadingType.CLEAR, color: "auto" },
      borders: { top: { style: BorderStyle.SINGLE, size: 8, color: "E0A800" }, bottom: { style: BorderStyle.SINGLE, size: 8, color: "E0A800" },
                 left: { style: BorderStyle.SINGLE, size: 8, color: "E0A800" }, right: { style: BorderStyle.SINGLE, size: 8, color: "E0A800" } },
      margins: { top: 100, bottom: 100, left: 160, right: 160 },
      children: [new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: title, bold: true })] }),
                 ...lines.map(l => new Paragraph({ spacing: { after: 40 }, children: runs(l) }))],
    })] })],
  });
}

const children = [
  // ---------- Schijnbare verhoging ----------
  H("Schijnbare verhoging"),
  P("Een mooi voorbeeld van breking van het licht is de **schijnbare verhoging** van een voorwerp in water."),
  figure("verhoging_0", 15.5, 899 / 1259),
  SUB("Uitleg:"),
  bullet("Het licht van punt V gaat van **water** naar **lucht**: van optisch dicht naar optisch ijl."),
  bullet("Aan het wateroppervlak **breekt** het licht **van de normaal weg**."),
  bullet("Onze hersenen denken dat licht altijd **rechtdoor** gaat. We zien punt V dus op de plaats waar de **verlengde** lichtstralen samenkomen: in **V'**."),
  bullet("V' ligt hoger dan V. Het voorwerp lijkt **minder diep** te liggen dan het echt ligt. Dat noemen we **schijnbare verhoging**."),
  bullet("Gevolg: een zwembad of een rivier lijkt **minder diep** dan in werkelijkheid. Opgelet dus!"),
  pageBreak(),
  SUB("Zo teken je de schijnbare verhoging:"),
  stepsTable,
  pageBreak(),

  // ---------- Oefeningen (zoals origineel) ----------
  P("**Oefeningen:**"),
  new Paragraph({ spacing: { after: 100 }, children: [new TextRun({ text: "Tip oefeningen:", underline: {} })] }),
  P("Stap 1: **Teken** altijd eerst de **normaal**!"),
  P("Stap 2: **Optisch dicht**: lichtstraal ligt het **dichtst** bij de **normaal**."),
  P("**Optisch ijl**: lichtstraal ligt het **verst** van de **normaal**.", { indent: { left: 850 } }),
  num("oef", "Teken het vervolg van de lichtstralen."),
  figure("oef1", 15.6, 166 / 492, 360),
  num("oef", "Teken het vervolg van de lichtstralen."),
  figure("oef2", 16.4, 170 / 516),
  pageBreak(),

  // ---------- Regenboog ----------
  H("Nog een voorbeeld: de regenboog"),
  P("Een regenboog ontstaat door **breking** én **weerkaatsing** van zonlicht in **regendruppels**. Je ziet een regenboog alleen als:"),
  bullet("de zon schijnt;"),
  bullet("de zon **in je rug** staat;"),
  bullet("er regendruppels **vóór je** in de lucht hangen."),
  SUB("Wat gebeurt er in één druppel?"),
  figure("druppel", 10.5, 1000 / 1180),
  num("drup", "**Breking bij het binnengaan.** Het witte zonlicht gaat van lucht naar water en breekt **naar de normaal toe**. Elke kleur breekt een beetje anders: **violet** breekt het **sterkst**, **rood** het **minst**. Zo wordt wit licht opgesplitst in kleuren."),
  num("drup", "**Weerkaatsing aan de achterkant.** Het licht botst tegen de achterkant van de druppel en wordt **weerkaatst**. Het licht keert dus terug naar de kant van de zon. Daarom moet de zon **in je rug** staan."),
  num("drup", "**Breking bij het buitengaan.** Het licht gaat van water naar lucht en breekt **van de normaal weg**. De kleuren gaan nog verder uit elkaar."),
  P("Rood licht komt uit de druppel onder een hoek van ongeveer **42°** met het zonlicht, violet licht onder ongeveer **40°**."),
  box("Let op: is dit totale terugkaatsing?", [
    "**Nee.** De lichtstraal raakt de achterkant van de druppel onder ongeveer 40°. Dat is **kleiner dan de grenshoek** van water (ongeveer 49°).",
    "Een deel van het licht wordt weerkaatst, een ander deel gaat door de druppel naar buiten. Daarom is een regenboog nooit heel fel.",
  ]),
  pageBreak(),
  SUB("Iedereen ziet zijn eigen regenboog"),
  figure("eigen_regenboog", 15.5, 820 / 1500),
  bullet("Denk een lijn van de zon, door je hoofd, naar de **schaduw van je hoofd** (stippellijn)."),
  bullet("Druppels die **42°** boven die lijn hangen, sturen **rood** licht naar jouw oog. Druppels op **40°** sturen **violet** licht naar jouw oog. Daarom is een regenboog **rood aan de buitenkant** en **violet aan de binnenkant**."),
  bullet("Al die druppels liggen samen op een **cirkelboog** rond de schaduw van je hoofd."),
  bullet("Je buur staat op een andere plaats. Zijn lijn ligt anders, dus zijn licht komt van **andere druppels**. Hij ziet **zijn eigen regenboog**."),
  bullet("Wandel je verder, dan wandelt de regenboog met je mee. Je kan het einde van een regenboog dus **nooit** bereiken."),
  SUB("Proef: zelf een regenboog maken met een tuinsproeier"),
  figure("sproeier", 11.5, 720 / 1400),
  P("**Nodig:** een zonnige dag en een tuinslang met sproeikop (stand: fijne nevel)."),
  num("proef", "Kies een moment waarop de zon **laag** staat: in de ochtend of de late namiddag."),
  num("proef", "Ga met de **zon in je rug** staan. Kijk naar je schaduw."),
  num("proef", "Spuit een **fijne nevel** vóór je uit. Zoek de regenboog in de nevel."),
  num("proef", "Stap een paar passen opzij. Wat doet de regenboog? Hij **schuift mee**."),
  num("proef", "Laat een klasgenoot naast je staan. Wijs allebei naar de plek waar je de regenboog ziet. Jullie wijzen naar **andere druppels**."),
  P("**Besluit:** de regenboog hangt niet op één vaste plaats. **Iedereen ziet zijn eigen regenboog.**"),
];

const numberedCfg = (ref) => ({ reference: ref, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
  style: { paragraph: { indent: { left: 425, hanging: 360 } } } }] });

const doc = new Document({
  creator: "Scienceboy²", title: "Cursus fysica – schijnbare verhoging en regenboog",
  styles: { default: { document: { run: { font: FONT, size: 22 } } } },
  numbering: { config: [
    { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 425, hanging: 284 } } } }] },
    numberedCfg("oef"), numberedCfg("drup"), numberedCfg("proef"),
  ] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    footers: { default: new Footer({ children: [new Paragraph({
      tabStops: [{ type: TabStopType.RIGHT, position: CONTENT }],
      children: [new TextRun({ text: "Cursus fysica 3 ASO1", size: 18 }), new TextRun({ text: "\t", size: 18 }),
                 new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "C00000" })],
    })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then(b => { fs.writeFileSync("/home/claude/work/schijnbare_verhoging_en_regenboog.docx", b); console.log("ok"); });
