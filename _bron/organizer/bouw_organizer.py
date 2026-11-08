# Bouwt per vak en jaar een advance organizer: overzicht-<id>.html (thema's, hoofdstukken, examenperiode, links naar de cursus).
# Gebruik: python3 /home/claude/toolswetenschappen/_bron/organizer/bouw_organizer.py
# De iconen komen uit index.html (zelfde iconen als op de startpagina).
import html, os, re
R = '/home/claude/toolswetenschappen/'
exec(open(R + '_bron/organizer/organizer_inhoud.py', encoding='utf-8').read())

idx = open(R + 'index.html', encoding='utf-8').read()
ICONEN_JS = idx[idx.index("const A = 'marker-end"):idx.index('};', idx.index('const ICONEN = {')) + 2]
E = html.escape

CSS = '''
:root{--bg:#EEF2F5;--paper:#fff;--ink:#1D2A36;--muted:#51606E;--line:#CBD5DE;--dec:#1F7A4D;--jun:#7C3AED}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Atkinson Hyperlegible",system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;font-size:1.0625rem;line-height:1.5}
main{max-width:56rem;margin:0 auto;padding:2rem 1.1rem 4rem}
.terug{font-size:.95rem;color:var(--muted);text-decoration:none}
.eyebrow{margin-top:1rem;font-weight:700;color:var(--c);letter-spacing:.02em}
h1{font-size:clamp(1.8rem,5vw,2.4rem);line-height:1.1;margin:.2rem 0 1rem}
.grote{background:var(--paper);border-left:6px solid var(--c);border-radius:0 12px 12px 0;padding:14px 18px;margin:0 0 14px}
.grote b{display:block;font-size:.85rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.grote span{font-size:1.25rem;font-weight:700}
.legende{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:.92rem;color:var(--muted);margin:0 0 22px}
.badge{display:inline-block;font-size:.78rem;font-weight:700;border-radius:999px;padding:1px 9px;white-space:nowrap}
.badge.dec{background:#fff;color:var(--dec);border:1.5px solid var(--dec)}.badge.jun{background:#fff;color:var(--jun);border:1.5px solid var(--jun)}
.thema{position:relative;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:16px 18px 12px;display:grid;grid-template-columns:64px 1fr;gap:4px 16px}
.thema + .pijl{height:26px;display:flex;justify-content:center}
.thema + .pijl::before{content:"";width:2px;background:var(--c);opacity:.5}
.ico{grid-row:1/3;color:var(--c)}
.ico svg{width:56px;height:56px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.ico .nr{display:block;text-align:center;font-weight:700;font-size:.8rem;color:var(--c);margin-top:2px}
.thema h2{margin:0;font-size:1.35rem;line-height:1.2}
.vraag{margin:2px 0 0;color:#334155;font-weight:700;font-style:italic}
.idee{margin:6px 0 0}
.kent{margin:6px 0 0;font-size:.92rem;color:var(--muted)}
.kent b{color:var(--ink)}
ol.hfd{grid-column:1/3;list-style:none;margin:12px 0 0;padding:0;border-top:1px solid var(--line)}
ol.hfd li{display:grid;grid-template-columns:2.4rem 1fr auto;gap:2px 10px;align-items:baseline;padding:8px 0;border-bottom:1px dashed var(--line)}
ol.hfd li:last-child{border-bottom:0}
.hnr{font-weight:700;color:var(--muted)}
.ht{font-weight:700}.ht a{color:inherit;text-decoration:underline;text-decoration-color:#94a3b8;text-underline-offset:3px}
.wat{grid-column:2/3;font-size:.92rem;color:var(--muted)}
.rechts{grid-row:1/3;grid-column:3;display:flex;flex-direction:column;align-items:flex-end;gap:4px}
.lees{font-size:.85rem;font-weight:700;color:var(--muted);text-decoration:none;white-space:nowrap}
.volgt{font-size:.8rem;color:var(--muted);white-space:nowrap}
.gebruik{margin-top:28px;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:14px 18px}
.gebruik h2{margin:0 0 6px;font-size:1.1rem}.gebruik ul{margin:0;padding-left:1.2rem}
.kaart{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin:0 0 26px}
.tegel{display:block;background:var(--paper);border:1px solid var(--line);border-top:3px solid var(--c);border-radius:12px;padding:10px 12px;text-decoration:none;color:var(--ink)}
.tegel svg{width:34px;height:34px;fill:none;stroke:var(--c);color:var(--c);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;float:right}
.tegel .tn{font-size:.8rem;font-weight:700;color:var(--muted)}.tegel .tt{display:block;font-weight:700;line-height:1.2;margin:2px 0 6px}
.tegel ul{list-style:none;margin:0;padding:0;font-size:.85rem;color:var(--muted)}.tegel li{line-height:1.35}
@media (max-width:560px){.thema{grid-template-columns:44px 1fr}.ico svg{width:40px;height:40px}ol.hfd li{grid-template-columns:2rem 1fr}.rechts{grid-row:auto;grid-column:2;flex-direction:row;align-items:center;justify-content:flex-start}}
@media print{@page{size:A4;margin:12mm}body{background:#fff;font-size:10.5pt}main{padding:0;max-width:none}.terug,.gebruik,.lees{display:none}
 .thema{break-inside:avoid;padding:8px 12px 6px;border-color:#999}.thema + .pijl{height:10px}ol.hfd li{padding:3px 0}h1{margin-bottom:6px}.grote{padding:8px 12px}}
'''

def pagina(o):
    themas, tegels = [], ''
    for i, th in enumerate(o['themas']):
        tegels += (f'<a class="tegel" href="#t{i+1}"><span data-icoon="{th["icoon"]}"></span><span class="tn">{E(th["nr"])}</span>'
                   f'<span class="tt">{E(th["titel"])}</span><ul>' + ''.join(f'<li>H{h[0]} {E(h[1])}</li>' for h in th['hfd']) + '</ul></a>')
        rijen = ''
        for nr, titel, wat, ex, link in th['hfd']:
            t = f'<a href="{E(link)}">{E(titel)}</a>' if link else E(titel)
            lees = f'<a class="lees" href="{E(link)}">Lees in de cursus ›</a>' if link else '<span class="volgt">cursus volgt</span>'
            rijen += (f'<li><span class="hnr">H{nr}</span><span class="ht">{t}</span>'
                      f'<span class="rechts"><span class="badge {ex}">{"december" if ex == "dec" else "juni"}</span>{lees}</span>'
                      f'<span class="wat">{E(wat)}</span></li>')
        themas.append(f'''<section class="thema" id="t{i+1}">
  <div class="ico"><span data-icoon="{th['icoon']}"></span><span class="nr">{E(th['nr'])}</span></div>
  <div><h2>{E(th['titel'])}</h2><p class="vraag">{E(th['vraag'])}</p></div>
  <div><p class="idee">{E(th['idee'])}</p><p class="kent"><b>Je kent al:</b> {E(th['kent'])}</p></div>
  <ol class="hfd">{rijen}</ol>
</section>''')
    titel = f"{o['vak']} {o['jaar']} · overzicht van het jaar"
    return f'''<!DOCTYPE html>
<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(titel)}</title>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body style="--c:{o['kleur']}"><main>
<a class="terug" href="index.html">‹ Alle tools</a>
<div class="eyebrow">{E(o['vak'])} · {E(o['jaar'])} · {E(o['richting'])}</div>
<h1>Overzicht van het jaar</h1>
<div class="grote"><b>De grote vraag</b><span>{E(o['vraag'])}</span></div>
<div class="kaart">{tegels}</div>
<div class="legende"><span><span class="badge dec">december</span> leerstof voor het examen van december</span><span><span class="badge jun">juni</span> leerstof voor het examen van juni</span></div>
{'<div class="pijl"></div>'.join(themas)}
<section class="gebruik"><h2>Zo gebruik je dit overzicht</h2><ul>
<li>Begin je aan een nieuw hoofdstuk? Kijk hier eerst: bij welk thema hoort het, en wat ken je al?</li>
<li>Lees de grote vraag van het thema. Na het thema kan je ze beantwoorden.</li>
<li>Voor een examen: kijk welke hoofdstukken bij december of juni horen.</li></ul></section>
</main>
<script>
{ICONEN_JS}
document.querySelectorAll('[data-icoon]').forEach(el => {{
  const n = el.dataset.icoon;
  el.innerHTML = `<svg viewBox="0 0 48 48" aria-hidden="true">${{(DEFS + (ICONEN[n] || '')).replaceAll('PIJL', 'pijl-' + n)}}</svg>`;
}});
</script>
</body></html>'''

for o in ORG:
    f = f"overzicht-{o['id']}.html"
    open(R + f, 'w', encoding='utf-8').write(pagina(o))
    print('gemaakt:', f)
