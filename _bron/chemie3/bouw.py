"""Gemeenschappelijke bouwsteen voor de chemie-lessites (3de jaar, andere richtingen).
Gebruikt de stijl en de oefenfuncties van chemie-pse.html (kop.html, helpers.js)."""
import pathlib
HIER = pathlib.Path(__file__).parent
REPO = HIER.parents[1]
KOP = (HIER / 'kop.html').read_text()
HELP = (HIER / 'helpers.js').read_text()

def pagina(bestand, titel, eyebrow, intro, lpd, voorkennis, doelen, tabs, body, css='', js=''):
    kop = KOP.replace('<title>Periodiek systeem</title>', f'<title>{titel}</title>')
    nav = ''.join(f'<button class="lestab" role="tab" aria-controls="{i}" aria-selected="{"true" if k==0 else "false"}"><span class="nr">{l}</span><span class="t"><b>{t}</b>{f"<small>{s}</small>" if s else ""}</span></button>'
                  for k,(i,l,t,s) in enumerate(tabs))
    html = f'''{kop}
.lesnav{{--tabs:{len(tabs)}}}
.credit{{font-size:.85rem;color:var(--muted)}}
.fig{{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px}}
.fig svg{{width:100%;height:auto;display:block;margin:0 auto}}
.fig text{{font-family:var(--f-body);fill:var(--ink)}}
{css}
</style>
</head>
<body>
<div class="wrap">
  <a href="index.html#andere" style="align-self:flex-start;font-weight:700;color:var(--accent);text-decoration:none">← Alle tools</a>
  <header class="hero">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{titel}</h1>
    <p>{intro}</p>
    <p class="lpd">{lpd}</p>
  </header>
  <div class="tip"><b>Voorkennis: dit moet je al kennen</b><ul style="margin:4px 0 0;padding-left:20px">{''.join(f'<li>{v}</li>' for v in voorkennis)}</ul></div>
  <div class="doel"><span class="eyebrow">{doelen[0]}</span><ul>{''.join(f'<li>{d}</li>' for d in doelen[1])}</ul></div>
  <nav class="lesnav" role="tablist" aria-label="Onderdelen">{nav}</nav>
{body}
  <p class="credit">Gemaakt door de vakgroep wetenschappen · Maria Assumpta Lyceum · ontwikkeld met hulp van AI · <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.nl">CC BY-NC-SA 4.0</a></p>
</div>
<script>
(function(){{
{HELP}
{js}
tabs();
}})();
</script>
</body>
</html>
'''
    import sys; sys.path.insert(0, str(REPO / '_bron')); from vinkjes import voeg_toe
    (REPO / bestand).write_text(voeg_toe(html, bestand), encoding='utf-8')
    print('gemaakt:', bestand)
