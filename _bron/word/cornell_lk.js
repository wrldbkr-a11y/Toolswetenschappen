const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, AlignmentType, Footer, Header, PageNumber } = require('docx');
const SANS = 'Calibri', SERIF = 'Cambria', NAVY = '1F3A5F', W = 9026, LW = 2700;

// [titel, ondertitel, [[kernwoord, uitleg], ...], samenvatting]
const H = [
 ['Ladingen', 'Fysica 5de jaar · Elektrostatica · hoofdstuk 1', [
  ['#', '1.1 Lading in materie'],
  ['#', '1.1.1 De elementaire lading'],
  ['elementaire lading', 'e = 1,602 · 10⁻¹⁹ C = lading van één proton; elektron: −e. Lading is altijd een veelvoud: Q = ±n · e.'],
  ['positief / negatief geladen', 'Positief = elektronentekort, negatief = elektronenoverschot. Alleen elektronen verplaatsen, protonen zitten vast in de kern.'],
  ['#', '1.1.2 De tribo-elektrische reeks'],
  ['tribo-elektrische reeks', 'Bij wrijven wordt de stof die hoger staat positief, de stof die lager staat negatief. Vb. wol (+) en PVC (−). Verder uit elkaar → meer lading.'],
  ['#', '1.1.3 Geleiders en isolatoren'],
  ['geleider – isolator', 'Geleider: vrije ladingdragers (metaal, lichaam, aarde). Isolator: geen vrije ladingdragers (kunststof, glas, droge lucht).'],
  ['#', '1.1.4 Aarding'],
  ['aarding', 'Geleidende verbinding met de aarde → voorwerp wordt neutraal. Negatief voorwerp: e⁻ naar de aarde; positief voorwerp: e⁻ van de aarde.'],
  ['#', '1.2 Laden van voorwerpen'],
  ['#', '1.2.1 Laden door wrijving en door contact'],
  ['laden door wrijving', 'Elektronen gaan over van de ene stof naar de andere: even grote, tegengestelde ladingen.'],
  ['laden door contact', 'Lading verdeelt zich over beide voorwerpen, met hetzelfde teken. Identieke bollen: elk de helft van de totale lading.'],
  ['behoud van lading', 'Lading ontstaat niet en verdwijnt niet; ze verplaatst alleen.'],
  ['#', '1.2.2 Influentie en polarisatie'],
  ['influentie', 'Vrije e⁻ in een geleider verschuiven door een geladen voorwerp in de buurt. Laden: staaf erbij → aarden → aarding verbreken → staaf weg: tegengesteld teken.'],
  ['polarisatie', 'In een isolator: elk molecule wordt een dipool. Tegengestelde kant ligt dichter → netto aantrekking (snippers, ballon aan de muur).'],
  ['#', '1.2.3 Toepassingen'],
  ['bliksem', 'Onderkant wolk −, grond + door influentie; lucht wordt geleidend → ontlading. Bliksemafleider = aarding. KMI (Ukkel) meet bliksem met BELLS.'],
  ['fotokopieertoestel', 'Trommel in het donker + geladen; licht maakt witte delen geleidend → lading weg; negatieve toner op de letters; papier sterker +; fixeren met warmte en druk.'],
  ['swifferdoekje', 'Wrijving → doekje negatief; stofdeeltje wordt gepolariseerd → aangetrokken.']],
  'Voorwerpen worden geladen doordat elektronen overgaan (wrijving, contact) of verschuiven (influentie, polarisatie). De lading is een veelvoud van e en blijft behouden. Geleiders hebben vrije elektronen, isolatoren niet. Aarding maakt een geleider neutraal.'],
 ['Krachten tussen ladingen', 'Fysica 5de jaar · Elektrostatica · hoofdstuk 2', [
  ['#', '2.1 Krachten tussen twee ladingen'],
  ['#', '2.1.1 De wet van Coulomb'],
  ['coulombkracht: richting en zin', 'Op de verbindingslijn. Gelijke ladingen stoten af, tegengestelde trekken aan. Beide krachten even groot en tegengesteld (actie-reactie).'],
  ['wet van Coulomb', 'F = k · |Q₁| · |Q₂| / r², met k = 8,99 · 10⁹ N·m²/C²; Q in C, r in m.'],
  ['#', '2.1.2 De formule omvormen'],
  ['omvormen', '|Q₁| = F · r² / (k · |Q₂|);  r = √(k · |Q₁| · |Q₂| / F).'],
  ['#', '2.1.3 Redeneren met de wet van Coulomb'],
  ['redeneren', 'Lading × n → F × n. Afstand × n → F ÷ n².'],
  ['#', '2.2 Krachten tussen meerdere ladingen'],
  ['superpositie', 'Elke kracht afzonderlijk bepalen en vectorieel optellen.'],
  ['ladingen op één lijn', 'Positieve zin kiezen, krachten met teken optellen.'],
  ['ladingen niet op één lijn', 'Krachten tekenen vanuit de lading, parallellogrammethode. Loodrecht: Pythagoras.'],
  ['elektrisch vs. zwaartekracht', 'In een waterstofatoom is de coulombkracht ongeveer 2,3 · 10³⁹ keer groter.']],
  'De coulombkracht ligt op de verbindingslijn, is recht evenredig met het product van de ladingen en omgekeerd evenredig met het kwadraat van de afstand. Bij meerdere ladingen tel je de krachten vectorieel op.'],
 ['Elektrisch veld', 'Fysica 5de jaar · Elektrostatica · hoofdstuk 3', [
  ['#', '3.1 Grootte van het elektrisch veld'],
  ['elektrisch veld', 'Ruimte waarin een lading een kracht ondervindt. Bronlading Q maakt het veld; positieve proeflading q meet het.'],
  ['veldsterkte', 'E = F / q, in N/C. Zin = zin van de kracht op een positieve lading.'],
  ['#', '3.1.1 Kracht en veld'],
  ['kracht in een veld', 'F = |q| · E. Positieve lading: F mee met E; negatieve lading: F tegen E in.'],
  ['#', '3.1.2 Radiaal veld van een puntlading'],
  ['radiaal veld', 'E = k · |Q| / r²; hangt niet af van de proeflading. Afstand × 2 → E ÷ 4.'],
  ['#', '3.1.3 Homogeen veld'],
  ['homogeen veld', 'Tussen twee evenwijdige platen: overal even groot en even gericht.'],
  ['valkuil: veld of kracht', 'Proeflading × 2 → kracht × 2, veld blijft gelijk.'],
  ['#', '3.2 Eigenschappen van het elektrisch veld'],
  ['#', '3.2.1 Elektrische veldlijnen'],
  ['veldlijnen', 'Van + naar −; raaklijn = richting van E; dichter = sterker; snijden nooit; loodrecht op een geleider.'],
  ['#', '3.2.2 Soorten elektrische velden'],
  ['soorten velden', 'Puntlading: radiaal. Twee ladingen: gebogen lijnen. Geleidende bol: binnen E = 0, buiten zoals een puntlading. Platen: homogeen.'],
  ['grafieken', 'Puntlading: E daalt met 1/r². Bol: 0 tot R, dan 1/r². Platen: constant tussen de platen.'],
  ['#', '3.2.3 Geleiders en isolatoren in een elektrisch veld'],
  ['kooi van Faraday', 'Gesloten geleider: binnenin E = 0. Vb. auto, vliegtuig, MIVB-tram, microgolfoven, coaxkabel.'],
  ['isolator in een veld', 'Polarisatie verzwakt het veld binnenin, maar maakt het niet nul.']],
  'Het elektrisch veld is de kracht per coulomb: E = F/q. Rond een puntlading daalt het met 1/r², tussen platen is het constant. Veldlijnen tonen richting en sterkte. In een gesloten geleider is het veld nul: de kooi van Faraday.'],
 ['Potentiaal', 'Fysica 5de jaar · Elektrostatica · hoofdstuk 4', [
  ['#', '4.1 Potentiële elektrische energie in een homogeen veld'],
  ['analogie', 'm · g · h ↔ Q · E · d. De grond ↔ de negatieve plaat (E_pot = 0).'],
  ['potentiële elektrische energie', 'E_pot,E = Q · E · d, met d de afstand tot de negatieve plaat en Q met teken.'],
  ['arbeid door het veld', 'W_veld = −ΔE_pot. Beweegt de lading mee met de kracht, dan daalt E_pot.'],
  ['#', '4.2 Elektrische potentiaal in een homogeen veld'],
  ['#', '4.2.1 De elektrische potentiaal'],
  ['potentiaal', 'V = E_pot / Q, in volt (1 V = 1 J/C). Homogeen veld: V = E · d.'],
  ['grafieken', 'E: constant. V: lineair stijgend. E_pot: stijgend voor +Q, dalend voor −Q.'],
  ['#', '4.2.2 Equipotentiaaloppervlakken'],
  ['equipotentiaalvlak', 'Overal dezelfde potentiaal; loodrecht op de veldlijnen; verplaatsen kost geen arbeid.'],
  ['#', '4.3 Potentiaalverschil'],
  ['spanning', 'U_AB = V_A − V_B. Tussen platen U = E · D, dus E = U / D (V/m).'],
  ['spanning en energie', 'ΔE_kin = Q · U_AB. Positieve lading van hoge naar lage V versnelt; negatieve lading van lage naar hoge V.'],
  ['elektronvolt', '1 eV = 1,602 · 10⁻¹⁹ J: energie van een elektron dat 1 V doorloopt.']],
  'In een homogeen veld is E_pot = Q·E·d, analoog aan m·g·h. De potentiaal is energie per coulomb (V = E·d). Spanning is een potentiaalverschil; een lading die een spanning U doorloopt, wint Q·U aan kinetische energie.'],
 ['Druk bij vaste stoffen', 'Fysica 4de jaar · Druk · hoofdstuk 1', [
  ['#', '1 Wat is druk?'],
  ['druk', 'Kracht per oppervlakte-eenheid: p = F / A, in pascal (1 Pa = 1 N/m²). Ook kPa en hPa.'],
  ['#', '2 Rekenen met druk'],
  ['omvormen', 'F = p · A;  A = F / p.'],
  ['eenheden omzetten', '1 m² = 10 000 cm² = 1 000 000 mm². Oppervlakte altijd eerst in m².'],
  ['#', '3 Drukverhogend en drukverlagend'],
  ['drukverhogend', 'Kleine oppervlakte → grote druk: mes, spijker, noppen, stalen tramwielen.'],
  ['drukverlagend', 'Grote oppervlakte → kleine druk: sneeuwschoenen, rupsbanden, brede schouderbanden.'],
  ['#', '4 Redeneren met druk'],
  ['redeneren', 'p recht evenredig met F, omgekeerd evenredig met A. Factor van F boven, factor van A onder.']],
  'Druk is kracht per oppervlakte: p = F/A. Hoe kleiner de oppervlakte, hoe groter de druk. Zet de oppervlakte altijd om naar m².'],
 ['Krachten', 'Fysica 3de jaar · Thema 2 Krachten · hoofdstuk 2', [
  ['#', '1 Effect van een kracht'],
  ['statisch effect', 'De vorm verandert: uitrekken, indrukken, buigen (veer, spons, plank).'],
  ['dynamisch effect', 'De bewegingstoestand verandert: vertrekken, sneller, trager, stoppen, van richting veranderen.'],
  ['kracht', 'Oorzaak van een vormverandering of van een verandering in bewegingstoestand.'],
  ['#', '2 Een kracht is een vector'],
  ['kenmerken', 'Aangrijpingspunt, richting, zin en grootte (N). De pijl begint op het voorwerp.'],
  ['tekenen op schaal', 'Lengte = grootte : schaalwaarde. Bv. 35 N met 1 cm ≙ 10 N → 3,5 cm.'],
  ['grootte aflezen', 'Grootte = lengte · schaalwaarde. Bv. 4,2 cm met 1 cm ≙ 20 N → 84 N.'],
  ['#', '3 Krachten samenstellen'],
  ['resulterende kracht', 'Eén kracht met hetzelfde effect als alle krachten samen.'],
  ['zelfde richting, zelfde zin', 'Kop-staart; F_r = F₁ + F₂, zelfde zin.'],
  ['zelfde richting, tegengestelde zin', 'Kop-staart; F_r = F₁ − F₂, zin van de grootste. Even groot: F_r = 0, evenwicht.'],
  ['verschillende richting', 'Parallellogrammethode: diagonaal vanuit O. Loodrecht: F_r = √(F₁² + F₂²).'],
  ['#', '4 Krachten ontbinden'],
  ['ontbinden', 'Eén kracht vervangen door twee componenten; de kracht is de diagonaal. Bv. koffer trekken: F_x vooruit, F_y omhoog.'],
  ['#', '5 Traagheid'],
  ['traagheid', 'Een voorwerp wil zijn snelheid behouden. Geen kracht. Meer massa → meer traagheid (bus of tram die vertrekt of remt).'],
  ['#', '6 Resulterende kracht en beweging'],
  ['traagheidswet', 'F_r = 0 → rust of eenparig rechtlijnige beweging.'],
  ['F_r en beweging', 'F_r mee met v: sneller; tegen v: trager; loodrecht op v: bocht.']],
  'Een kracht herken je aan haar effect: statisch of dynamisch. Krachten zijn vectoren die je samenstelt tot een resulterende kracht of ontbindt in componenten. Is de resulterende kracht nul, dan blijft het voorwerp in rust of beweegt het even snel rechtdoor.'],
 ['Homeostase van de waterhuishouding in planten', 'Biologie 3de jaar · Thema 1 · hoofdstuk 1', [
  ['#', '1 Waterhuishouding en plantenorganen'],
  ['waterhuishouding', 'Opname, transport en afgifte van water, zodat er genoeg water in de plant is.'],
  ['plantenorganen', 'Wortel (opname, verankering), stengel (dragen, vervoer), blad (fotosynthese, verdamping), bloem (voortplanting).'],
  ['#', '2 Aanpassingen van het blad'],
  ['blad', 'Epidermis met waslaag; cellen van het vulweefsel (fotosynthese); huidmondje met sluitcellen; vaatbundels (nerven).'],
  ['#', '3 Gasuitwisseling via de huidmondjes'],
  ['huidmondje open/dicht', 'Water in sluitcellen → vacuole zwelt → turgor ↑ → open. Water weg → turgor ↓ → dicht. Licht + water: open; donker of watertekort: dicht.'],
  ['#', '4 Aanpassingen van de stengel'],
  ['stengel', 'Vaatbundels in een kring: houtvaten binnen, zeefvaten buiten, deelweefsel ertussen. Cortex, epidermis, merg.'],
  ['houtvat – zeefvat', 'Houtvat: dood, hol, houtstof, water omhoog. Zeefvat: levend, zeefplaten, assimilaten.'],
  ['#', '5 Aanpassingen van de wortel'],
  ['wortel', 'Wortelhaartjes vergroten de oppervlakte; één vaatbundel in het midden: houtvaten in een ster, zeefvaten ertussen.'],
  ['#', '6 Water- en assimilatentransport'],
  ['assimilaten', 'Eindproducten van de fotosynthese: glucose, zetmeel, eiwitten, vetten.'],
  ['transport', 'Water: wortelhaartjes → houtvaten → blad → huidmondjes (opwaarts). Assimilaten: zeefvaten, vooral neerwaarts.'],
  ['#', '7 Homeostase van de waterhuishouding'],
  ['negatieve feedback', 'Watertekort → huidmondjes sluiten → minder waterverlies. Waarde schommelt rond een normwaarde: dynamisch evenwicht.']],
  'Een plant neemt water op via de wortelhaartjes, vervoert het via de houtvaten en verliest het via de huidmondjes. De sluitcellen regelen dat verlies met een negatief feedbacksysteem. Assimilaten gaan via de zeefvaten vooral naar beneden.']
];

const rb = { style: BorderStyle.SINGLE, size: 6, color: '555555' };
const cel = (w, kinderen, fill) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders: { top: rb, bottom: rb, left: rb, right: rb }, margins: { top: 40, bottom: 40, left: 110, right: 110 },
  shading: fill ? { fill, type: ShadingType.CLEAR, color: 'auto' } : undefined, children: kinderen });
const t = (s, o = {}) => new TextRun({ text: s, font: o.font || SERIF, size: o.size || 20, bold: o.bold, color: o.color, italics: o.italics });

const tr = (s, o = {}) => { const out = []; let last = 0; const re = /([A-Za-z])_([A-Za-z,]+)/g; let m;
  while ((m = re.exec(s))) { if (m.index > last) out.push(t(s.slice(last, m.index), o)); out.push(t(m[1], o)); out.push(new TextRun({ text: m[2], font: o.font || SERIF, size: o.size || 20, subScript: true, bold: o.bold, color: o.color })); last = re.lastIndex; }
  if (last < s.length) out.push(t(s.slice(last), o)); return out; };
const KEUZE = process.argv[2] !== undefined ? [+process.argv[2]] : null;
const kids = [];
if (!KEUZE) kids.push(new Paragraph({ children: [t('Cornellschema’s · leerkrachtversie', { font: SANS, size: 40, bold: true, color: '1D2A36' })] }));
if (!KEUZE) kids.push(new Paragraph({ spacing: { after: 300 }, children: [t('Volledig ingevuld, als houvast bij het samen opbouwen op het bord. Links de kernwoorden, rechts de uitleg, onderaan de samenvatting.', { italics: true, color: '51606E' })] }));
H.forEach(([titel, sub, rijen, samenv], i) => {
  if (KEUZE && !KEUZE.includes(i)) return;
  kids.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: !KEUZE && i > 0, spacing: { after: 40 }, children: [t('Cornellschema · ' + titel, { font: SANS, size: 32, bold: true, color: NAVY })] }));
  kids.push(new Paragraph({ spacing: { after: 160 }, children: [t(sub, { font: SANS, size: 18, color: '51606E' })] }));
  kids.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [LW, W - LW], rows: [
    new TableRow({ tableHeader: true, children: [cel(LW, [new Paragraph({ children: [t('Kernwoorden', { font: SANS, bold: true })] })], 'EAEFF5'), cel(W - LW, [new Paragraph({ children: [t('Uitleg', { font: SANS, bold: true })] })], 'EAEFF5')] }),
    ...rijen.map(([k, u]) => k === '#'
      ? new TableRow({ cantSplit: true, children: [new TableCell({ columnSpan: 2, width: { size: W, type: WidthType.DXA }, borders: { top: rb, bottom: rb, left: rb, right: rb }, margins: { top: 35, bottom: 35, left: 110, right: 110 },
          shading: { fill: /^\d+(\.\d+)?\s/.test(u) && !/^\d+\.\d+\.\d+/.test(u) ? 'D6E0EC' : 'F1F4F8', type: ShadingType.CLEAR, color: 'auto' },
          children: [new Paragraph({ keepNext: true, children: [t(u, { font: SANS, bold: true, color: NAVY, size: /^\d+\.\d+\.\d+/.test(u) ? 20 : 23 })] })] })] })
      : new TableRow({ cantSplit: true, children: [cel(LW, [new Paragraph({ children: tr(k, { bold: true, color: NAVY }) })]), cel(W - LW, [new Paragraph({ children: tr(u) })])] }))] }));
  kids.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [W], rows: [new TableRow({ cantSplit: true, children: [cel(W, [
    new Paragraph({ spacing: { after: 60 }, children: [t('Samenvatting', { font: SANS, bold: true })] }), new Paragraph({ children: tr(samenv) })], 'F6F5F1')] })] }));
});
const doc = new Document({ styles: { default: { document: { run: { font: SERIF, size: 21 } } } },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1100, bottom: 1100, left: 1440, right: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [t('Cornellschema’s · leerkracht', { font: SANS, size: 16, color: '8A96A3' })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: SANS, size: 18, color: '8A96A3' })] })] }) },
    children: kids }] });
const NAMEN = ['Cornellschema_Fysica5_H1_Ladingen', 'Cornellschema_Fysica5_H2_Krachten_tussen_ladingen', 'Cornellschema_Fysica5_H3_Elektrisch_veld', 'Cornellschema_Fysica5_H4_Potentiaal',
  'Cornellschema_Fysica4_Druk_bij_vaste_stoffen', 'Cornellschema_Fysica3_Krachten', 'Cornellschema_Biologie3_Waterhuishouding_planten'];
const uit = KEUZE ? '/home/claude/word/cornell/' + NAMEN[KEUZE[0]] + '.docx' : '/home/claude/word/Cornellschemas_leerkracht.docx';
Packer.toBuffer(doc).then(b => { fs.writeFileSync(uit, b); console.log('ok', uit); });
