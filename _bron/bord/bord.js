const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,ShadingType,BorderStyle,AlignmentType,PageBreak}=require('docx');
const W=9638, L=3000, Rw=W-L;
const run=(t,o={})=>new TextRun({text:t,font:'Calibri',size:22,...o});
// rich: **vet**
const rich=t=>t.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map(s=>s.startsWith('**')?run(s.slice(2,-2),{bold:true}):run(s));
const par=(t,o={})=>new Paragraph({spacing:{after:60},...o,children:rich(t)});
const rand={style:BorderStyle.SINGLE,size:6,color:'555555'};
const randen={top:rand,bottom:rand,left:rand,right:rand};
function cel(w,inhoud,fill){ return new TableCell({width:{size:w,type:WidthType.DXA},borders:randen,margins:{top:80,bottom:80,left:120,right:120},shading:fill?{fill,type:ShadingType.CLEAR,color:'auto'}:undefined,children:inhoud}); }
function schema(titel,sub,rijen,samenv){
  const kop=new TableRow({tableHeader:true,children:[cel(L,[par('**Vragen**')],'E4EEF8'),cel(Rw,[par('**Notities op het bord**')],'E4EEF8')]});
  const r=rijen.map(([v,lijnen])=>new TableRow({cantSplit:true,children:[cel(L,[par('**'+v+'**')]),cel(Rw,lijnen.map(l=>par(l)))]}));
  const s=new TableRow({cantSplit:true,children:[new TableCell({columnSpan:2,width:{size:W,type:WidthType.DXA},borders:randen,margins:{top:80,bottom:80,left:120,right:120},shading:{fill:'F5F8FB',type:ShadingType.CLEAR,color:'auto'},children:[par('**Samenvatting** (laat de leerlingen dit eerst zelf formuleren)'),...samenv.map(l=>par(l))]})]});
  return [new Paragraph({spacing:{after:40},children:[run(titel,{bold:true,size:32,color:'1F4E79'})]}),new Paragraph({spacing:{after:160},children:[run(sub,{italics:true,color:'51606E'})]}),
    new Table({width:{size:W,type:WidthType.DXA},columnWidths:[L,Rw],rows:[kop,...r,s]})];
}
const druk=schema('Bordschema · Druk bij vaste stoffen (4de jaar)','Cornellschema voor het bord: links de vragen (staan voorgedrukt op het leerlingenblad), rechts wat je samen opbouwt.',[
 ['Wat is druk?',['Proef: duim vs. punaise, baksteen in zand → zelfde kracht, ander effect.','**Druk = kracht per oppervlakte-eenheid**','Schets: baksteen plat / zijkant / rechtop → kleiner A, dieper in zand.']],
 ['Met welke formule bereken je druk? Wat is de eenheid?',['**p = F / A**','p: druk (Pa) · F: kracht ⊥ op oppervlak (N) · A: oppervlakte (m²)','1 Pa = 1 N/m² · 1 kPa = 1000 Pa · 1 hPa = 100 Pa']],
 ['Hoe bereken je F of A als je p kent?',['**F = p · A** · **A = F / p**','Voorbeeld: p = 80 kPa, A = 0,15 m² → F = 12 000 N']],
 ['Hoe zet je cm² en mm² om naar m²?',['1 m² = 100 cm × 100 cm = **10 000 cm²** → cm² ÷ 10 000','1 m² = **1 000 000 mm²** → mm² ÷ 1 000 000','Valkuil: 400 i.p.v. 0,0400 → p 10 000 × te klein']],
 ['Wanneer is iets drukverhogend of drukverlagend? Geef voorbeelden.',['Kleine A → grote p: **drukverhogend** (mes, spijker, naald, punt punaise)','Grote A → kleine p: **drukverlagend** (sneeuwschoenen, rupsbanden, rugzakbanden, kop punaise)']],
 ['Wat gebeurt er met p als F of A verandert?',['p recht evenredig met F, omgekeerd evenredig met A','Factor F boven, factor A onder: F × 2 en A × 4 → p × 2/4 = p ÷ 2']],
],['p = F / A in Pa; A altijd in m². Kleine A → grote p (drukverhogend), grote A → kleine p (drukverlagend). p ∼ F en p ∼ 1/A.']);
const kr=schema('Bordschema · Krachten, traagheid en beweging (3de jaar)','Cornellschema voor het bord: links de vragen (staan voorgedrukt op het leerlingenblad), rechts wat je samen opbouwt.',[
 ['Wat zijn de kenmerken van een kracht?',['Kracht = **vector**: aangrijpingspunt · richting · zin · grootte (N)','Schets: pijl met schaal 1 cm ≙ 10 N']],
 ['Hoe bepaal je Fr bij krachten met dezelfde richting?',['Kop-staartmethode','Zelfde zin: **Fr = F₁ + F₂** · Tegengestelde zin: **Fr = F₁ − F₂**, zin van de grootste','Vb. touwtrekken 600 N ← en 540 N → : Fr = 60 N ←']],
 ['Hoe construeer je Fr bij krachten met een verschillende richting?',['**Parallellogrammethode**: F₁ en F₂ vanuit O, hulplijnen evenwijdig (geodriehoek), diagonaal = Fr','Loodrecht: **Fr = √(F₁² + F₂²)** · vb. 40 N en 30 N → 50 N']],
 ['Wat is traagheid? Hoe hangt ze af van de massa?',['Voorwerp verzet zich tegen verandering van snelheid; **geen kracht**','Bus vertrekt → val naar achter; bus remt → val naar voor (gordel!)','**Meer massa → meer traagheid**: volle kar moeilijker te starten én te stoppen']],
 ['Wat zegt de traagheidswet?',['**Fr = 0 → rust of ERB** (even snel, rechtdoor)','Om te blijven bewegen is GEEN kracht nodig (ruimtesonde, fietser: trapkracht = wrijving)']],
 ['Wat gebeurt er met de snelheid bij Fr = 0, mee met v, tegen v, loodrecht op v?',['Fr = 0 → v blijft gelijk · Fr mee met v → sneller · Fr tegen v → trager · Fr ⊥ v → bocht','Misvatting: bal krijgt geen kracht mee van je hand; na loslaten enkel wrijving → trager']],
],['Kracht = vector. Fr: optellen/aftrekken of parallellogram. Traagheid: voorwerp behoudt zijn snelheid, groter bij meer massa. Fr = 0 → rust of ERB; Fr ≠ 0 → snelheid verandert.']);
const doc=new Document({styles:{default:{document:{run:{font:'Calibri',size:22}}}},sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:1134,bottom:1134,left:1134,right:1134}}},children:[...druk,new Paragraph({children:[new PageBreak()]}),...kr]}]});
Packer.toBuffer(doc).then(b=>{ fs.writeFileSync('/home/claude/bord/Bordschema_Cornell_druk_en_krachten.docx',b); console.log('ok'); });
