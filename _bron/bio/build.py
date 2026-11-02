import sys,json,base64
sys.path.insert(0,'/home/claude/w5'); from bouw import bouw
b64=lambda f,m:'data:'+m+';base64,'+base64.b64encode(open(f,'rb').read()).decode()
st=json.load(open('stengel.json'))
data='const IMG='+json.dumps({'blad':b64('blad.webp','image/webp'),'oog':b64('oog.webp','image/webp')})+';\n'
data+='const STENGEL='+json.dumps({'svg':open('stengel.svg').read().split('>',1)[1].rsplit('</svg>',1)[0],'bundels':st['bundels']})+';\n'
data+='const WORTEL='+json.dumps({'svg':open('wortel.svg').read().split('>',1)[1].rsplit('</svg>',1)[0]})+';\n'
data+='const EPI='+open('epidermis.json').read()+';\n'
css='''
.figwrap{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;}
.chips{display:flex;flex-wrap:wrap;gap:6px;}
.chip{font-family:var(--font);font-size:13px;padding:5px 10px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--text);cursor:pointer;}
.chip:hover{border-color:var(--accent);} .chip.on{background:#fef3c7;border-color:#d97706;font-weight:700;}
.stappenlijst{margin:0;padding-left:22px;font-size:14px;line-height:1.9;color:var(--text-dim);}
.stappenlijst li{cursor:pointer;} .stappenlijst li.on{color:#b45309;font-weight:700;} .stappenlijst li.gedaan{color:var(--text);}
table.vgl{width:100%;border-collapse:collapse;font-size:14px;margin-top:12px;background:#fff;}
table.vgl th,table.vgl td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;}
table.vgl tr:first-child th{background:var(--accent-soft);}
table.kruis td{text-align:center;} table.kruis input{width:20px;height:20px;accent-color:var(--accent);}
td.ok-cel{background:var(--ok-bg);} td.fout-cel{background:var(--flag-bg);}
.tag.paars{background:#ede9fe;color:#6d28d9;} .tag.groen{background:var(--ok-bg);color:var(--ok-text);}
.card svg{max-height:90px;}
.schema{display:grid;gap:12px;margin:10px 0;}
.schema-k{font-weight:600;font-size:14px;margin-bottom:6px;}
.bron{font-size:12px;color:var(--text-dim);margin-top:30px;line-height:1.6;}
'''
js=data+open('bio1.js').read()+'\n'+open('bio2.js').read()+'\n'+open('bio3.js').read()
html=open('bio_html.txt').read()+'''
  <p class="bron"><b>Bronnen van de afbeeldingen.</b> Bladdoorsnede: Zephyris (Richard Wheeler), Wikimedia Commons, CC BY-SA 3.0. Doorsnede van het oog: Rhcastilhos en Jmarchn, Wikimedia Commons, publiek domein. Beide aangepast: Engelse namen verwijderd, Nederlandse namen toegevoegd. Alle andere tekeningen zijn voor deze tool gemaakt.</p>'''
bouw('/home/claude/toolswetenschappen/biologie-prikkels.html','Biologie: water, prikkels en reacties',
 '<strong>Hoe houden planten en dieren hun binnenmilieu in evenwicht?</strong> Ontdek de waterhuishouding van planten, feedbacksystemen, receptoren en het oog, en hoe spieren reageren op prikkels.',
 [('water','Waterhuishouding plant'),('feedback','Homeostase en feedback'),('receptor','Receptoren en het oog'),('effector','Effectoren en spieren')],html,js,css)
print('ok')
