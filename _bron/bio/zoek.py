import sys,json,urllib.request,urllib.parse,re
UA="ToolswetenschappenBot/1.0 (educational use; contact via github wrldbkr-a11y)"
def api(params):
    params.update({'format':'json'})
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
    r=urllib.request.Request(u,headers={'User-Agent':UA}); return json.load(urllib.request.urlopen(r,timeout=30))
def zoek(q,n=12):
    d=api({'action':'query','generator':'search','gsrsearch':q+' filetype:bitmap|drawing','gsrnamespace':6,'gsrlimit':n,'prop':'imageinfo','iiprop':'url|size|extmetadata','iiurlwidth':900})
    out=[]
    for p in sorted(d.get('query',{}).get('pages',{}).values(),key=lambda x:x.get('index',0)):
        ii=p['imageinfo'][0]; m=ii.get('extmetadata',{})
        lic=m.get('LicenseShortName',{}).get('value','?'); art=re.sub('<[^>]+>','',m.get('Artist',{}).get('value','?'))[:50]
        out.append((p['title'],lic,art,ii['width'],ii['height'],ii.get('thumburl')))
    return out
if __name__=='__main__':
    for t in zoek(' '.join(sys.argv[1:])): print(' | '.join(map(str,t[:5])))
