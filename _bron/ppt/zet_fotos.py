# zet FOTO_ITEMS in de tool; gebruikt img/sch-<key>.webp als het bestaat
import json,os,re
R='/home/claude/toolswetenschappen/'
D=json.load(open('/home/claude/ppt/foto_data.json'))
bron=json.load(open('/home/claude/ppt/foto_bron.json')) if os.path.exists('/home/claude/ppt/foto_bron.json') else {}
items=[]
for k,t,u in D:
    it={'tekst':t,'antwoord':k,'uitleg':u}
    if os.path.exists(R+f'img/sch-{k}.webp'):
        it['img']=f'img/sch-{k}.webp'; it['bron']=bron.get(k,'')
    items.append(it)
blok='const FOTO_ITEMS = '+json.dumps(items,ensure_ascii=False)+';\n'
p=R+'chemie-scheidingstechnieken.html'; s=open(p).read()
s=re.sub(r'const FOTO_ITEMS = .*?;\n','',s,flags=re.S)
s=s.replace("const TK = Object.keys(TECH)",blok+"const TK = Object.keys(TECH)")
open(p,'w').write(s); print(sum('img' in i for i in items),'met foto')
