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
