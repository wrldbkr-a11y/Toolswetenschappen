/* Organische vormen voor biologische tekeningen: geen cirkels en rechthoeken,
   maar vloeiende, onregelmatige contouren met kleurverloop en textuur. */
function rng(seed){ let s = seed >>> 0 || 1; return () => { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) % 100000) / 100000; }; }
/* Catmull-Rom door punten → kubische bezier */
function glad(pts, dicht=true, k=1){
  const n = pts.length; if (n < 2) return '';
  const P = i => dicht ? pts[(i + n) % n] : pts[Math.max(0, Math.min(n - 1, i))];
  let d = `M${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)}`;
  const m = dicht ? n : n - 1;
  for (let i = 0; i < m; i++){
    const p0 = P(i-1), p1 = P(i), p2 = P(i+1), p3 = P(i+2);
    const c1 = [p1[0] + (p2[0]-p0[0])/6*k, p1[1] + (p2[1]-p0[1])/6*k], c2 = [p2[0] - (p3[0]-p1[0])/6*k, p2[1] - (p3[1]-p1[1])/6*k];
    d += `C${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
  }
  return d + (dicht ? 'Z' : '');
}
/* onregelmatige blob rond een middelpunt */
function blob(cx, cy, rx, ry, R, n=9, j=.18, rot=0){
  const p = []; for (let i = 0; i < n; i++){ const a = rot + i / n * Math.PI * 2, f = 1 + (R() - .5) * 2 * j; p.push([cx + Math.cos(a) * rx * f, cy + Math.sin(a) * ry * f]); }
  return glad(p);
}
/* punt en raaklijn op een open pad van punten (lineair geïnterpoleerd) */
function langs(pts, t){
  const L = []; let tot = 0; for (let i = 1; i < pts.length; i++){ const d = Math.hypot(pts[i][0]-pts[i-1][0], pts[i][1]-pts[i-1][1]); L.push(d); tot += d; }
  let s = Math.max(0, Math.min(1, t)) * tot;
  for (let i = 0; i < L.length; i++){ if (s <= L[i] || i === L.length-1){ const f = L[i] ? s / L[i] : 0; const a = pts[i], b = pts[i+1]; return [a[0] + (b[0]-a[0])*f, a[1] + (b[1]-a[1])*f, Math.atan2(b[1]-a[1], b[0]-a[0])]; } s -= L[i]; }
}
/* bemonster een bezier-pad tot punten (via een tijdelijk SVG-pad) */
function bemonster(d, n=80){
  const ns = 'http://www.w3.org/2000/svg', s = document.createElementNS(ns, 'svg'), p = document.createElementNS(ns, 'path');
  p.setAttribute('d', d); s.appendChild(p); s.style.position = 'absolute'; s.style.width = s.style.height = '0'; document.body.appendChild(s);
  const L = p.getTotalLength(), r = []; for (let i = 0; i <= n; i++){ const q = p.getPointAtLength(L * i / n); r.push([q.x, q.y]); }
  s.remove(); return r;
}
/* gemeenschappelijke kleurverlopen en filters (één keer in de pagina) */
(function(){
  const d = document.createElement('div');
  d.innerHTML = `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <radialGradient id="o-cel" cx="40%" cy="35%" r="75%"><stop offset="0" stop-color="#fbd7de"/><stop offset=".7" stop-color="#f0b2c0"/><stop offset="1" stop-color="#e293a6"/></radialGradient>
    <radialGradient id="o-celklier" cx="40%" cy="35%" r="75%"><stop offset="0" stop-color="#f7cfe0"/><stop offset=".7" stop-color="#e7a9c6"/><stop offset="1" stop-color="#d48aae"/></radialGradient>
    <radialGradient id="o-kern" cx="38%" cy="35%" r="70%"><stop offset="0" stop-color="#9b78c2"/><stop offset=".6" stop-color="#6a4596"/><stop offset="1" stop-color="#4b2b73"/></radialGradient>
    <radialGradient id="o-rbc" cx="50%" cy="50%" r="55%"><stop offset="0" stop-color="#e46a6a"/><stop offset=".45" stop-color="#cf3b3b"/><stop offset=".8" stop-color="#b52a2a"/><stop offset="1" stop-color="#8f1d1d"/></radialGradient>
    <radialGradient id="o-vet" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#fff6cf"/><stop offset=".6" stop-color="#f5df8e"/><stop offset="1" stop-color="#ddbb5c"/></radialGradient>
    <radialGradient id="o-druppel" cx="35%" cy="30%" r="70%"><stop offset="0" stop-color="#ffffff"/><stop offset=".4" stop-color="#9fd6f5"/><stop offset="1" stop-color="#3f93c8"/></radialGradient>
    <radialGradient id="o-secreet" cx="35%" cy="30%" r="70%"><stop offset="0" stop-color="#fff7d6"/><stop offset=".5" stop-color="#f3c74f"/><stop offset="1" stop-color="#c98f12"/></radialGradient>
    <radialGradient id="o-hormoon" cx="35%" cy="30%" r="70%"><stop offset="0" stop-color="#e8fff1"/><stop offset=".5" stop-color="#3fbf7f"/><stop offset="1" stop-color="#1d7a4b"/></radialGradient>
    <linearGradient id="o-lederhuid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6d0c8"/><stop offset="1" stop-color="#efc0b6"/></linearGradient>
    <linearGradient id="o-opperhuid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9c3a6"/><stop offset=".25" stop-color="#e2a98f"/><stop offset="1" stop-color="#d98f84"/></linearGradient>
    <filter id="o-textuur" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="3" seed="4" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 .92  0 0 0 0 .95  0 0 0 -1.1 .62" result="vlek"/><feComposite in="vlek" in2="SourceGraphic" operator="in" result="v2"/><feBlend in="SourceGraphic" in2="v2" mode="multiply"/></filter>
    <filter id="o-zacht"><feGaussianBlur stdDeviation="1.2"/></filter>
    <filter id="o-schaduw" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-color="#5a2433" flood-opacity=".28"/></filter>
  </defs></svg>`;
  document.body.prepend(d.firstChild);
})();
/* collageenvezels: zachte golvende lijnen in bindweefsel */
function vezels(x0, y0, w, h, R, n=26, kleur='#e7a7b4', op=.45){
  let s = ''; for (let i = 0; i < n; i++){ const y = y0 + R() * h, x = x0 + R() * w * .3, L = w * (.35 + R() * .5), a = (R() - .5) * .5; const pts = []; for (let k = 0; k <= 5; k++){ const t = k / 5; pts.push([x + t * L * Math.cos(a), y + t * L * Math.sin(a) + Math.sin(t * 6 + i) * 4]); }
    s += `<path d="${glad(pts, false)}" fill="none" stroke="${kleur}" stroke-width="${(1 + R() * 2).toFixed(1)}" stroke-linecap="round" opacity="${op}"/>`; }
  return s;
}
/* één cel met kern */
function cel(cx, cy, rx, ry, R, opts={}){
  const vul = opts.vul || 'url(#o-cel)', rot = opts.rot || 0;
  let s = `<path d="${blob(cx, cy, rx, ry, R, 10, .12, rot)}" fill="${vul}" stroke="#c47a8e" stroke-width=".9"/>`;
  const kx = cx + (opts.kdx || 0), ky = cy + (opts.kdy || 0), kr = Math.min(rx, ry) * (opts.kf || .42);
  s += `<path d="${blob(kx, ky, kr * 1.1, kr * .9, R, 8, .1, rot)}" fill="url(#o-kern)"/>`;
  for (let i = 0; i < 3; i++) s += `<circle cx="${(kx + (R() - .5) * kr).toFixed(1)}" cy="${(ky + (R() - .5) * kr).toFixed(1)}" r="${(kr * .12).toFixed(1)}" fill="#2f1a4d" opacity=".55"/>`;
  return s;
}
/* rode bloedcel: schijf met lichter midden */
const rbc = (x, y, r, a=0) => `<g transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${(a*57.3).toFixed(0)})"><ellipse rx="${r}" ry="${(r*.72).toFixed(1)}" fill="url(#o-rbc)"/><ellipse rx="${(r*.42).toFixed(1)}" ry="${(r*.28).toFixed(1)}" fill="#e98181" opacity=".7"/></g>`;
const zichtbaar = el => el && el.offsetParent !== null;
