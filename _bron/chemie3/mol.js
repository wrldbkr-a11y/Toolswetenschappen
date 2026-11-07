/* bolmodellen van kleine deeltjes */
const AK = {H:'#f4f4f4', O:'#e5484d', C:'#3d3d3d', N:'#3b6fd8', Cl:'#3fae49', Na:'#8e5bd0', Fe:'#9aa3ab', He:'#7fd3e8', S:'#e8c23b', Mg:'#5aa469', Cu:'#c87533', Al:'#b9c2cc', K:'#a05fd0', Ca:'#c9a46b'};
const AR = s => s==='H' ? 9 : (s==='Na'||s==='Cl'||s==='K') ? 15 : 13;
const VORM = {
  H2:[['H',-8,0],['H',8,0]], O2:[['O',-10,0],['O',10,0]], N2:[['N',-10,0],['N',10,0]], Cl2:[['Cl',-12,0],['Cl',12,0]],
  O3:[['O',-17,7],['O',0,-4],['O',17,7]], He:[['He',0,0]], Fe:[['Fe',0,0]], Cu:[['Cu',0,0]],
  H2O:[['O',0,0],['H',-14,10],['H',14,10]], CO2:[['O',-22,0],['C',0,0],['O',22,0]],
  NH3:[['N',0,0],['H',-15,9],['H',15,9],['H',0,-16]], CH4:[['C',0,0],['H',-15,-11],['H',15,-11],['H',-15,11],['H',15,11]],
  HCl:[['H',-11,0],['Cl',8,0]], NaCl:[['Na',-12,0],['Cl',12,0]], CO:[['C',-10,0],['O',10,0]], SO2:[['O',-19,8],['S',0,0],['O',19,8]],
  Mg:[['Mg',0,0]], Na:[['Na',0,0]], C:[['C',0,0]], Al:[['Al',0,0]], MgO:[['Mg',-12,0],['O',11,0]],
  Al2O3:[['O',-34,9],['Al',-17,-5],['O',0,9],['Al',17,-5],['O',34,9]], FeS:[['Fe',-11,0],['S',11,0]], S:[['S',0,0]]
};
let gradId = 0;
function molSvg(f, x, y, sc=1, rot=0){
  const v = VORM[f]; const c = Math.cos(rot), s = Math.sin(rot);
  return v.map(([el,dx,dy]) => [el, x+(dx*c-dy*s)*sc, y+(dx*s+dy*c)*sc]).sort((a,b)=>a[2]-b[2]).map(([el,ax,ay]) =>
    `<circle cx="${ax.toFixed(1)}" cy="${ay.toFixed(1)}" r="${(AR(el)*sc).toFixed(1)}" fill="url(#g-${el})" stroke="#1a1a1a" stroke-width="${0.8*sc}"/>`).join('');
}
function molDefsGlobaal(){
  const d=document.createElement('div'); d.innerHTML='<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + Object.entries(AK).map(([el,k]) => `<radialGradient id="g-${el}" cx="35%" cy="30%" r="70%"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".35" stop-color="${k}"/><stop offset="1" stop-color="${k}" stop-opacity="1"/></radialGradient>`).join('') + '</defs></svg>'; document.body.prepend(d.firstChild);
}
molDefsGlobaal();
const molDefs = () => '';
const fHtml = f => f.replace(/(\d+)/g,'<sub>$1</sub>');
const telAtomen = f => { const r = {}; for (const m of f.matchAll(/([A-Z][a-z]?)(\d*)/g)) r[m[1]] = (r[m[1]]||0) + (+m[2]||1); return r; };
function doosSvg(f, n=6, w=220, h=150, sc=1){
  const pos = [[45,40],[115,32],[180,50],[60,108],[132,98],[188,118],[100,66]];
  let s = `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="deeltjesmodel">${molDefs()}<rect x="2" y="2" width="${w-4}" height="${h-4}" rx="10" fill="#f8fbfa" stroke="var(--line)" stroke-width="2"/>`;
  for (let i=0;i<n;i++) s += molSvg(f, pos[i][0]*w/220, pos[i][1]*h/150, sc, (i*1.3)%3);
  return s + '</svg>';
}
