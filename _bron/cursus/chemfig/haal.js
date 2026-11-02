// haalt de tekeningen van de scheidingstechnieken uit de lessite als zelfstandige SVG (stijlen ingevuld)
const { chromium } = require('playwright');
const fs = require('fs');
const ROOT = '/home/claude/toolswetenschappen/';
const INLINE = `
window.platSVG = function(svg){
  const kl = svg.cloneNode(true);
  const bron = [svg, ...svg.querySelectorAll('*')], doel = [kl, ...kl.querySelectorAll('*')];
  const props = ['fill','stroke','stroke-width','stroke-dasharray','stroke-linecap','stroke-linejoin','opacity','fill-opacity','stroke-opacity','font-size','font-weight','font-family','text-anchor','transform'];
  const weg = [];
  bron.forEach((e,i) => {
    const cs = getComputedStyle(e), d = doel[i];
    if (cs.display==='none' || cs.visibility==='hidden' || parseFloat(cs.opacity)===0) { weg.push(d); return; }
    if (e.tagName==='defs' || e.closest('defs')) return;
    for (const p of props) {
      let v = cs.getPropertyValue(p);
      if (!v) continue;
      if (p==='transform') { if (v!=='none' && !e.getAttribute('transform') ) d.setAttribute('style', (d.getAttribute('style')||'')+';transform:'+v+';transform-box:'+cs.transformBox+';transform-origin:'+cs.transformOrigin); continue; }
      if (p==='font-family') v = 'Inter, sans-serif';
      d.setAttribute(p, v);
    }
    d.removeAttribute('class');
  });
  weg.forEach(d => d.remove());
  kl.setAttribute('xmlns','http://www.w3.org/2000/svg');
  kl.removeAttribute('class'); kl.removeAttribute('role');
  return kl.outerHTML;
};`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1100,height:900}});
  await p.goto('file://' + ROOT + 'chemie-scheidingstechnieken.html'); await p.waitForTimeout(500);
  await p.addScriptTag({content: INLINE});
  await p.addStyleTag({content:'*{transition:none!important;animation:none!important}'});
  const uit = {};
  await p.evaluate(()=>document.querySelectorAll('[hidden]').forEach(e=>{if(e.closest('section'))e.hidden=false}));
  const spelers = await p.$$('.speler');
  for (const sp of spelers) {
    const ids = await sp.$$eval('[data-t]', bs => bs.map(b => b.dataset.t));
    for (const id of ids) {
      await sp.$eval(`[data-t="${id}"]`, b=>b.click());
      await sp.$eval('[data-m="onderdelen"]', b=>b.click());
      await sp.$eval('[data-o="toon"]', b=>b.click()); await p.waitForTimeout(150);
      const lab = await sp.$eval('svg.tech', s => platSVG(s));
      await sp.$eval('[data-o="test"]', b=>b.click()); await p.waitForTimeout(150);
      const num = await sp.$eval('svg.tech', s => platSVG(s));
      const namen = await sp.$$eval('.testlijst li', ls => ls.length);
      uit[id] = {lab, num};
    }
  }
  fs.writeFileSync('/home/claude/cursus/chemfig/tech.json', JSON.stringify(uit));
  console.log(Object.keys(uit).join(' '));
  await b.close();
})();
