const { chromium } = require('playwright');
const fs = require('fs');
const INLINE = eval(fs.readFileSync("inline.js","utf8").replace(/^const INLINE = /,"").replace(/;\s*$/,""));
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1300, height: 1000 } });
  await p.goto('file:///home/claude/toolswetenschappen/biologie-prikkels.html'); await p.waitForTimeout(800);
  await p.addScriptTag({ content: INLINE });
  await p.addStyleTag({ content: '*{transition:none!important;animation:none!important} .scene{display:block!important}' });
  await p.waitForTimeout(300);
  const uit = {};
  const neem = async (naam, sel) => { uit[naam] = await p.$eval(sel, s => platSVG(s)); };
  for (const id of ['fig-oog', 'fig-netvlies', 'fig-spieren']) await neem(id, `#${id} svg`);
  for (const id of ['svg-schema', 'svg-fb', 'svg-drempel', 'svg-kleur', 'svg-spiertypes', 'svg-arm', 'svg-slok']) await neem(id, `#${id}`);
  // arm: triceps
  const knoppen = await p.$$eval('#e4 button', bs => bs.map(b => b.textContent.trim()));
  uit._armknoppen = knoppen;
  fs.writeFileSync('bio.json', JSON.stringify(uit));
  console.log(Object.keys(uit).map(k => k + ':' + (uit[k].length)).join(' '));
  await b.close();
})();
