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
