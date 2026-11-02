const { chromium } = require('playwright');
const fs = require('fs');
const INLINE = eval(fs.readFileSync("inline.js","utf8").replace(/^const INLINE = /,"").replace(/;\s*$/,""));
(async () => {
  const b = await chromium.launch();
  const uit = JSON.parse(fs.readFileSync('bio.json'));
  for (const [hash, sel, naam, klik] of [['f2','#svg-fb','svg-fb'],['r2','#svg-drempel','svg-drempel'],['e4','#svg-arm','svg-arm'],['e4','#svg-arm','svg-arm-tri','Triceps trekt samen'],['e4','#svg-slok','svg-slok']]) {
    const p = await b.newPage({ viewport: { width: 1300, height: 1000 } });
    await p.goto('file:///home/claude/toolswetenschappen/biologie-prikkels.html#' + hash); await p.waitForTimeout(900);
    await p.addScriptTag({ content: INLINE });
    if (klik) { await p.evaluate(t => [...document.querySelectorAll('#e4 button')].find(b => b.textContent.trim() === t).click(), klik); await p.waitForTimeout(1500); }
    else await p.waitForTimeout(1200);
    uit[naam] = await p.$eval(sel, s => platSVG(s));
    console.log(naam, uit[naam].length);
    await p.close();
  }
  fs.writeFileSync('bio.json', JSON.stringify(uit));
  await b.close();
})();
