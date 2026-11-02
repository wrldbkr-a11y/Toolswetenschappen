import sys,hashlib,urllib.request,urllib.parse,re,time,subprocess,os
UA="ToolswetenschappenBot/1.0 (https://github.com/wrldbkr-a11y/Toolswetenschappen; educational)"
def get(u):
    while True:
        try: return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=90).read()
        except urllib.error.HTTPError as e:
            if e.code==429:
                ra=int(e.headers.get('retry-after','120')); print('  429, wacht',ra,flush=True); time.sleep(min(ra,620)+5); continue
            raise
lijst=[l.strip() for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
for naam in lijst:
    n=naam.replace(' ','_'); pad='img/'+n
    if os.path.exists(pad) and os.path.getsize(pad)>1000: continue
    h=hashlib.md5(n.encode()).hexdigest()
    try:
        data=get(f'https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{urllib.parse.quote(n)}')
    except Exception as e: print('FOUT',naam,e,flush=True); continue
    open(pad,'wb').write(data)
    try:
        raw=get('https://commons.wikimedia.org/w/index.php?title=File:'+urllib.parse.quote(n)+'&action=raw').decode('utf8','ignore')
        open(pad+'.raw','w').write(raw)
    except Exception as e: print('lic fout',e)
    prev=pad+'.prev.png'
    if n.lower().endswith('.svg'): subprocess.run(['rsvg-convert','-w','900','-o',prev,pad],capture_output=True)
    else: subprocess.run(['convert',pad+'[0]','-resize','900x900>',prev],capture_output=True)
    print('OK',naam,len(data)//1024,'KB',flush=True); time.sleep(25)
print('KLAAR',flush=True)
