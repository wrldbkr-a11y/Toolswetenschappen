#!/usr/bin/env python3
"""Maakt de lesdoelen in alle tools en cursussen afvinkbaar: een vierkantje met een klikbaar vinkje.

Werkt op lijsten  .doel ul > li  (lessites),  ul.doelen > li  (cursussen en 3ASO-fysica).
De vinkjes worden per pagina in de browser bewaard (localStorage). Afgedrukt blijft het vierkantje leeg.

    python3 _bron/vinkjes.py        (vanuit de map van de repo; veilig om opnieuw te draaien)

De bouwscripts roepen voeg_toe() zelf aan, dus na het bouwen hoef je dit niet apart te draaien.
"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
BEGIN, EINDE = '<!--vinkjes-->', '<!--/vinkjes-->'

BLOK = BEGIN + r'''
<style>
.doel ul:has(.vk-li),ul.doelen:has(.vk-li){list-style:none;padding-left:0}
.vk-li{display:flex;gap:10px;align-items:flex-start;cursor:pointer;margin:4px 0;list-style:none}
.vk{flex:none;width:22px;height:22px;margin-top:1px;border:2px solid #64748b;border-radius:5px;background:#fff;display:inline-grid;place-items:center;cursor:pointer;padding:0}
.vk:focus-visible{outline:3px solid #60a5fa;outline-offset:2px}
.vk.aan{background:#16a34a;border-color:#16a34a}
.vk.aan::after{content:"";width:6px;height:11px;border:solid #fff;border-width:0 3px 3px 0;transform:translateY(-1px) rotate(45deg)}
.vk-li.aan .vk-t{color:#15803d}
@media print{.vk{background:#fff!important;border-color:#000!important}.vk.aan::after{border-color:#000}}
</style>
<script>
(function(){
  var K='vinkjes:'+location.pathname.split('/').pop();
  var st={}; try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
  function bewaar(){try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
  var lis=document.querySelectorAll('.doel ul > li, ul.doelen > li');
  [].forEach.call(lis,function(li,i){
    if(li.querySelector('.vk')) return;
    var b=document.createElement('button'); b.type='button'; b.className='vk'; b.setAttribute('role','checkbox');
    b.setAttribute('aria-label','Ik kan dit');
    var t=document.createElement('span'); t.className='vk-t';
    while(li.firstChild) t.appendChild(li.firstChild);
    li.appendChild(b); li.appendChild(t); li.classList.add('vk-li');
    function zet(a){ st[i]=a; b.classList.toggle('aan',a); li.classList.toggle('aan',a); b.setAttribute('aria-checked',a?'true':'false'); }
    zet(!!st[i]);
    li.addEventListener('click',function(e){ if(e.target.closest('a')) return; zet(!st[i]); bewaar(); });
  });
})();
</script>
''' + EINDE + '\n'

def heeft_doelen(s):
    return 'class="doel"' in s or 'class="doelen"' in s

def voeg_toe(s):
    s = re.sub(re.escape(BEGIN) + r'.*?' + re.escape(EINDE) + r'\n?', '', s, flags=re.S)
    if not heeft_doelen(s):
        return s
    i = s.rfind('</body>')
    return s[:i] + BLOK + s[i:] if i >= 0 else s + BLOK

if __name__ == '__main__':
    n = 0
    for f in sorted(ROOT.glob('*.html')):
        s = f.read_text(encoding='utf-8'); t = voeg_toe(s)
        if t != s:
            f.write_text(t, encoding='utf-8'); n += 1
    print('vinkjes in', n, 'bestanden')
