// atoom en molecule (natieve vormen)
function atoom(s, stap, x, y, d, soort) {
  const O = soort === 'O';
  s.addText(soort, { shape: pres.shapes.OVAL, x: x - d / 2, y: y - d / 2, w: d, h: d, fill: { color: O ? 'D62828' : 'FFFFFF' }, line: { color: O ? '9B1C1C' : '64748B', width: 1.5 },
    color: O ? 'FFFFFF' : '1D2A36', bold: true, fontSize: Math.round(d * 22), align: 'center', valign: 'middle', margin: 0, objectName: stap === null ? vast() : nm(stap) });
}
function h2(s, stap, x, y) { atoom(s, stap, x - 0.22, y, 0.55, 'H'); atoom(s, stap, x + 0.22, y, 0.55, 'H'); }
function o2(s, stap, x, y) { atoom(s, stap, x - 0.3, y, 0.75, 'O'); atoom(s, stap, x + 0.3, y, 0.75, 'O'); }
function h2o(s, stap, x, y, f = 1) { atoom(s, stap, x - 0.42 * f, y + 0.34 * f, 0.55 * f, 'H'); atoom(s, stap, x + 0.42 * f, y + 0.34 * f, 0.55 * f, 'H'); atoom(s, stap, x, y, 0.8 * f, 'O'); }
function chip(s, stap, x, y, w, h, t, kl, fl, fs = 15) {
  s.addText(t, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.15, x, y, w, h, fill: { color: fl }, line: { color: fl }, color: kl, bold: true, fontSize: fs, align: 'center', valign: 'middle', margin: 2, objectName: nm(stap) });
}
// oefendia: zin staat er, antwoord verschijnt per klik
function oefening(kicker, titel, sectie, opdracht, items, kol = 2) {
  const s = nieuw(kicker, titel, sectie);
  s.addText(opdracht, { x: 0.6, y: 1.55, w: 12.1, h: 0.45, fontSize: 18, italic: true, color: K.grijs, margin: 0, isTextBox: true, objectName: vast() });
  const per = Math.ceil(items.length / kol), W = (12.1 - (kol - 1) * 0.3) / kol, rh = Math.min(1.0, 4.75 / per);
  items.forEach(([zin, ant, kl, fl], i) => {
    const c = Math.floor(i / per), r = i % per, x = 0.6 + c * (W + 0.3), y = 2.15 + r * rh;
    s.addText(zin, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x, y, w: W, h: rh - 0.12, fill: { color: 'F4F6F8' }, line: { color: 'F4F6F8' }, fontSize: 16, color: K.tekst, valign: 'middle', margin: [4, 10, 4, 12], objectName: vast() });
    chip(s, i + 1, x + W - 2.05, y + 0.1, 1.9, rh - 0.32, ant, kl, fl, 14);
  });
  return s;
}

