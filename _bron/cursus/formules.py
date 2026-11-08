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
        if heeft_is and BEGIN.match(p):
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
