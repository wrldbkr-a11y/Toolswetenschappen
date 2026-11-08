"""Tussen twee formules (of twee gegevens) staat geen punt "·": dat lijkt op een maalteken.
"B = N · V · V = B / N" wordt "B = N · V      V = B / N" (brede spatie).
Een punt is een scheiding als het stuk erna begint met een symbool en "=" (V = …); anders is het een maalteken (m · g).
Wordt aangeroepen door bouw.py.
"""
import re, html as H

SEP = '&emsp;&emsp;'
PUNT = re.compile(r'(?:&nbsp;|\s)*·(?:&nbsp;|\s)*')
BEGIN = re.compile(r'^\s*(?:[A-Za-zΔρμηθλαωσπ][A-Za-z₀-₉0-9,]*|[A-Za-zΔ]\s?[₀-₉]?)\s*=')

def _plat(s):
    return ' '.join(H.unescape(re.sub(r'<[^>]+>', '', s)).replace('\xa0', ' ').split())

def _blok(inner):
    if '·' not in inner or '=' not in inner: return inner
    delen = PUNT.split(inner); seps = PUNT.findall(inner)
    if len(delen) < 2: return inner
    uit = delen[0]; heeft_is = '=' in _plat(delen[0])
    for sep, deel in zip(seps, delen[1:]):
        p = _plat(deel)
        sinds = _plat(uit).rsplit('=', 1)[-1]
        # in een rekenketen (… = ρ · g · h · A = …) is · een maalteken; een scheiding herken je aan &nbsp;, aan een breuk erna of aan een getal ervoor
        echt = '&nbsp;' in sep or '/' in p or re.search(r'\d', sinds)
        if heeft_is and BEGIN.match(p) and echt and not re.search(r'[−+-]', sinds):
            uit += SEP + deel           # nieuwe formule of nieuw gegeven
        else:
            uit += sep + deel
        heeft_is = heeft_is or '=' in p
        if BEGIN.match(p): heeft_is = True
    return uit

def ruimte_tussen_formules(html):
    def blok(m):
        return m.group(1) + _blok(m.group(2)) + m.group(3)
    hoofd, sep, rest = html.partition('<body')
    if not sep: return html
    # svg en script niet aanraken
    stukken = re.split(r'(<svg.*?</svg>|<script.*?</script>)', rest, flags=re.S)
    for i, st in enumerate(stukken):
        if st.startswith(('<svg', '<script')): continue
        stukken[i] = re.sub(r'(<(?:p|li|td|th)(?:\s[^>]*)?>)(.*?)(</(?:p|li|td|th)>)', blok, st, flags=re.S)
    return hoofd + sep + ''.join(stukken)
