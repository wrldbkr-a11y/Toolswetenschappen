"""Formules met een horizontale breukstreep, en voldoende ruimte tussen formules die naast elkaar staan.
"ρ = p_h / (g · h)" wordt een gestapelde breuk: <span class="fr"><span>p_h</span><span>g · h</span></span>.
Alleen in symbolische formules (geen kommagetallen, geen gewone woorden): rekenwerk met getallen blijft zoals het is.
Formules naast elkaar (gescheiden door brede spaties, meerdere &nbsp; of " en ") krijgen een brede tussenruimte.
Wordt aangeroepen door bouw.py, na ruimte_tussen_formules().
"""
import re, html as H

GAP = '&emsp;&emsp;&emsp;'
CSS = ('<style>.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1.2;margin:0 .12em;font-size:.95em}'
       '.fr>span{padding:0 .25em;white-space:nowrap}.fr>span:first-child{border-bottom:1.3px solid currentColor}'
       '.fm{white-space:nowrap;display:inline-block;margin:3px 0}</style>')
WOORD_OK = {'cos', 'sin', 'tan'}
_TAGS = []
SCHEID = re.compile(r'(&emsp;(?:&emsp;)+|(?:&nbsp;\s*){2,}|\s*<br\s*/?>\s*|\s+en\s+|;\s+|:\s+|\.\s+(?=[A-Z<])|,\s+(?=[A-Za-zΔρμ<|√]))')

def _mask(s):
    tags = []
    def f(m):
        tags.append(m.group(0)); return chr(0xE000 + len(tags) - 1)
    return re.sub(r'<[^>]+>', f, s), tags
def _unmask(s, tags):
    return re.sub('[-]', lambda m: tags[ord(m.group(0)) - 0xE000], s)

def symbolisch(piece):
    s = re.sub(r'<sub>.*?</sub>|<sup>.*?</sup>', '', piece)
    p = ' '.join(H.unescape(re.sub(r'<[^>]+>', '', s)).replace('\xa0', ' ').split())
    if '=' not in p or '/' not in p: return False
    if re.search(r'\d,\d|\d\.\d|[%°]', p): return False
    if not re.fullmatch(r'[A-Za-zΑ-ωΔ0-9₀-₉²³½ ·()√|=/+\-−,]+', p): return False
    for w in re.findall(r'[A-Za-zΑ-ω]{2,}', p):
        if w not in WOORD_OK and not w.startswith('Δ'): return False
    # getallen alleen als 1/… of 2 · … (bv. 1/R, 2 · E); rekenwerk met getallen blijft gewoon staan
    if re.search(r'\d', re.sub(r'(?<!\d)1(?=\s*/)|(?<!\d)2(?=\s*·)', '', p)): return False
    # links van het eerste = staat een grootheid, geen getal
    return not re.match(r'\s*\d', p)

def _top(s, ch):
    """posities van ch op diepte 0 (niet tussen haakjes)"""
    d, uit = 0, []
    for i, c in enumerate(s):
        if c == '(': d += 1
        elif c == ')': d -= 1
        elif c == ch and d == 0: uit.append(i)
    return uit

def _ontbloot(s):
    t = s.strip()
    if t.startswith('(') and t.endswith(')'):
        d = 0
        for i, c in enumerate(t):
            d += c == '('; d -= c == ')'
            if d == 0 and i < len(t) - 1: return t
        return t[1:-1].strip()
    return t

def _term(s):
    """één term (zonder + of − op diepte 0): breuk maken als er precies één / op diepte 0 staat"""
    m = re.match(r'^(\s*)(.*?)(\s*)$', s, re.S); voor, kern, na = m.groups()
    # √( … / … )
    w = re.match(r'^√\(\s*(.*)\s*\)$', kern, re.S)
    if w and '/' in w.group(1) and not _top(kern, '/'):
        return voor + '√(' + _zijde(w.group(1)) + ')' + na
    e = re.match(r'^(.*\S)(\s+\([^()·]*\))$', kern, re.S)   # eenheid tussen haakjes achteraan, bv. (N/C)
    if e and '/' in e.group(1): return voor + _term(e.group(1)) + e.group(2) + na
    sl = [i for i in _top(kern, '/') if not (i > 0 and kern[i - 1] == '<')]
    if len(sl) != 1: return s
    a, b = kern[:sl[0]], kern[sl[0] + 1:]
    if not (_balans(a, _TAGS) and _balans(b, _TAGS)): return s
    # een kwadraat of macht hoort bij de noemer; een getal of symbool ervoor blijft ervoor als het tussen haakjes staat? nee: alles links is teller
    return voor + f'<span class="fr"><span>{_ontbloot(a)}</span><span>{_ontbloot(b)}</span></span>' + na

def _zijde(s):
    pos = [i for i in _top(s, '+')] + [i for i in _top(s, '−')]
    if not pos: return _term(s)
    pos = sorted(pos); uit, vorig = '', 0
    for p in pos:
        uit += _term(s[vorig:p]) + s[p]; vorig = p + 1
    return uit + _term(s[vorig:])

def _balans(deel, tags):
    stap = []
    for c in deel:
        o = ord(c) - 0xE000
        if 0 <= o < len(tags):
            t = tags[o]
            m = re.match(r'<(/?)(\w+)', t)
            if not m or t.endswith('/>'): continue
            if m.group(1):
                if not stap or stap[-1] != m.group(2): return False
                stap.pop()
            else: stap.append(m.group(2))
    return not stap

def formule(piece):
    m, tags = _mask(piece)
    # buitenste tags rond de hele formule (bv. <b>…</b>) erbuiten houden
    voor, na = '', ''
    while True:
        k = m.strip()
        if len(k) >= 2 and 0xE000 <= ord(k[0]) < 0xE000 + len(tags) and 0xE000 <= ord(k[-1]) < 0xE000 + len(tags):
            t1, t2 = tags[ord(k[0]) - 0xE000], tags[ord(k[-1]) - 0xE000]
            m1 = re.match(r'<(\w+)', t1)
            if m1 and t2 == f'</{m1.group(1)}>' and _balans(k[1:-1], tags):
                voor += k[0]; na = k[-1] + na; m = k[1:-1]; continue
        break
    global _TAGS
    _TAGS = tags
    zijden = m.split('=')
    m2 = '='.join(_zijde(z) if '/' in z else z for z in zijden)
    return _unmask(voor + m2 + na, tags)

def _inhoud(inner):
    if '/' not in inner or '=' not in inner: return inner
    delen = SCHEID.split(inner)
    uit, n_form = [], 0
    for i, d in enumerate(delen):
        if i % 2 == 1: uit.append(d); continue
        if symbolisch(d):
            uit.append('<span class="fm">' + formule(d) + '</span>'); n_form += 1
        else:
            uit.append(d)
    # brede ruimte tussen twee formules die naast elkaar staan
    for i in range(1, len(uit) - 1, 2):
        if uit[i - 1].endswith('</span>') and '<span class="fm">' in uit[i - 1] and '<span class="fm">' in uit[i + 1] and re.fullmatch(r'(&emsp;)+|(?:&nbsp;\s*)+|\s+', uit[i]):
            uit[i] = GAP
    return ''.join(uit)

def breuken(html):
    hoofd, sep, rest = html.partition('<body')
    if not sep: return html
    stukken = re.split(r'(<svg.*?</svg>|<script.*?</script>|<style.*?</style>)', rest, flags=re.S)
    for i, st in enumerate(stukken):
        if st.startswith(('<svg', '<script', '<style')): continue
        st = re.sub(r'(<(?:p|li|td|th)(?:\s[^>]*)?>)(.*?)(</(?:p|li|td|th)>)', lambda m: m.group(1) + _inhoud(m.group(2)) + m.group(3), st, flags=re.S)
        st = re.sub(r'(<div class="formule">)(.*?)(</div>)', lambda m: m.group(1) + _inhoud(m.group(2)) + m.group(3), st, flags=re.S)
        st = re.sub(r'(<span class="f">)(.*?)(</span></div>)', lambda m: m.group(1) + _inhoud(m.group(2)) + m.group(3), st, flags=re.S)
        stukken[i] = st
    return hoofd.replace('</head>', CSS + '</head>', 1) + sep + ''.join(stukken)
