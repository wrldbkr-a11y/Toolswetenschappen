import sys; sys.path.insert(0,'/home/claude/w5'); from bouw import bouw
sch=open('/home/claude/w5/sch.js').read(); nlf=sch[sch.index('const nl='):sch.index('\n',sch.index('const nl='))]
css='.sel{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:8px;font:inherit;background:#fff;}\n.note a{color:var(--accent);font-weight:600;}'
bouw('/home/claude/toolswetenschappen/ladingen.html','Ladingen en elektrostatica',
 '<strong>Waar komt lading vandaan, en hoe laad je een voorwerp?</strong> Ontdek de elementaire lading, het verschil tussen geleiders en isolatoren, laden door wrijving en influentie, en toepassingen zoals bliksem, het kopieerapparaat en het swifferdoekje.',
 [('lading','Lading in materie'),('laden','Voorwerpen laden'),('toep','Toepassingen')],
 open('/home/claude/w5/lad_html.txt').read(), nlf+'\n'+open('/home/claude/w5/lad.js').read(), css)
