import sys,hashlib,urllib.request,urllib.parse,re,os,subprocess,time
UA="ToolswetenschappenBot/1.0 (educational; https://github.com/wrldbkr-a11y)"
def get(u):
    for k in range(6):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=60).read()
        except Exception as e:
            if '429' in str(e): time.sleep(25); continue
            raise
    raise Exception('429')
for naam in sys.argv[1:]:
    n=naam.replace(' ','_'); h=hashlib.md5(n.encode()).hexdigest()
    u=f'https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{urllib.parse.quote(n)}'
    try: data=get(u)
    except Exception as e: print('FOUT',naam,e); continue
    pad='img/'+n; open(pad,'wb').write(data)
    raw=get('https://commons.wikimedia.org/w/index.php?title=File:'+urllib.parse.quote(n)+'&action=raw').decode('utf8','ignore')
    lic=re.findall(r'\{\{(?:self\|)?([^{}]*?(?:cc-|PD|pd-|Cc-|GFDL|public domain|CC-)[^{}]*)\}\}',raw,re.I)
    aut=re.findall(r'\|\s*[Aa]uthor\s*=\s*(.*)',raw)
    open(pad+'.lic','w').write('LIC: '+' ; '.join(lic)[:200]+'\nAUTHOR: '+(aut[0][:150] if aut else '?')+'\n')
    prev=pad+'.prev.png'
    if n.lower().endswith('.svg'): subprocess.run(['rsvg-convert','-w','900','-o',prev,pad],capture_output=True)
    else: subprocess.run(['convert',pad,'-resize','900x900>',prev],capture_output=True)
    print('OK',naam,len(data)//1024,'KB |',' ; '.join(lic)[:90],'|',(aut[0][:60] if aut else '?'))
    time.sleep(6)
