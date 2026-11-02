import re
src=open('/home/claude/cursus/bio_cursus.py',encoding='utf-8').read()
src=src.split("voorkennis = f")[0]
ns={}; exec(src,ns)
F={'plant':ns['fig_plant']('naam'),'blad':ns['fig_blad']('naam'),'stengel':ns['fig_stengel']('naam'),'wortel':ns['fig_wortel']('naam'),
'vaten':ns['fig_vaten'],'transport':ns['fig_transport'].split('</svg>')[0]+'</svg>','feedback':ns['fig_feedback'](),'cel':ns['fig_cel'](),'osmose':ns['fig_osmose'](),
'stoma':ns['fig_stoma']}
html='<html><body style="margin:0;background:#fff">'+''.join(f'<div id="{k}" style="display:inline-block;padding:6px;background:#fff">{v}</div><br>' for k,v in F.items())+'</body></html>'
open('/home/claude/toolswetenschappen/_figs.html','w').write(html)
