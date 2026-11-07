#!/usr/bin/env python3
"""Vaste soorten vakken in alle tools, zodat leerlingen zien wat leerstof is en wat extra is.

  data-vak="ken"    groen   'Ken dit'    definities, regels, formules (de leerstof)
  data-vak="letop"  oranje  'Let op'     typische fouten en verwarringen
  data-vak="vb"     grijs   'Voorbeeld'  leefwereld, weetjes, toepassingen
  data-vak="vk"     blauw   (eigen titel) voorkennis

Elk vak .kader / .tip / .note / .info / .noteer krijgt automatisch een soort op basis van de
eerste woorden. Een vak dat al data-vak heeft, blijft zoals het is (zo kan je met de hand kiezen).
Vakken die leeg zijn (gevuld door JavaScript) krijgen niets, tenzij je data-vak zelf zet.
Wordt aangeroepen door vinkjes.voeg_toe(), dus door alle bouwscripts.
"""
import re, html

LETOP = ('Let op', 'Onthoud: traagheid', 'Opgelet', 'Je rekenmachine', 'Zwaarteveld ≠', 'Wrijving is nodig')
VB = ('Rekenen met de wet', 'In Brussel', 'Waterzuiveringsstation', 'Kraantjeswater', 'Muntthee', 'Nog een analyse', 'Voorbeeld', 'Ook planten')
NIETS = ('Sleep om', 'Gemaakt door', 'Atoomsoorten')

BEGIN, EINDE = '<!--vakken-->', '<!--/vakken-->'
CSS = BEGIN + '''<style>
[data-vak]{position:relative}
[data-vak="ken"]{background:#E8F5EC!important;border:0!important;border-left:4px solid #1F7A4A!important;border-radius:0 10px 10px 0!important}
[data-vak="letop"]{background:#FFF7ED!important;border:0!important;border-left:4px solid #D97706!important;border-radius:0 10px 10px 0!important;color:inherit}
[data-vak="vb"]{background:transparent!important;border:1.5px dashed #94A3B8!important;border-radius:10px!important}
[data-vak="vk"]{background:#EEF4FB!important;border:0!important;border-left:4px solid #64748B!important;border-radius:0 10px 10px 0!important}
[data-vak]:not(.kader)::before,.kader[data-vak] .kop::before{display:block;font-size:11.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;margin-bottom:2px}
.kader[data-vak] .kop::before{display:inline}
[data-vak="ken"]:not(.kader)::before{content:"Ken dit";color:#1F7A4A}
.kader[data-vak="ken"] .kop::before{content:"Ken dit · ";color:#1F7A4A}
[data-vak="letop"]:not(.kader)::before{content:"Let op";color:#B45309}
[data-vak][data-label="nee"]::before{content:none!important}
[data-vak="vb"]:not(.kader)::before{content:"Voorbeeld";color:#64748B}
[data-vak="vk"]::before{content:none!important}
.lpd{font-size:12px!important;opacity:.7}
.lpd::before{content:"Leerplandoel (voor de leerkracht): ";font-weight:700}
</style>''' + EINDE + '\n'

def _tekst(s, i):
    t = html.unescape(re.sub(r'<[^>]+>', ' ', s[i:i + 600]))
    return ' '.join(t.split())

def soort(t, klas):
    if not t or t.startswith(NIETS) or t.startswith('${'):
        return None
    if t.startswith('Voorkennis'):
        return 'vk'
    if t.startswith(LETOP):
        return 'letop'
    if t.startswith(VB):
        return 'vb'
    return 'ken'

def toepassen(s):
    s = re.sub(re.escape(BEGIN) + r'.*?' + re.escape(EINDE) + r'\n?', '', s, flags=re.S)
    s = re.sub(r' data-vak="\w+"(?: data-label="nee")? data-auto', '', s)
    uit, pos, n = [], 0, 0
    for m in re.finditer(r'<(div|p|aside)\b([^>]*?)class="(kader|tip|note|info|noteer|def)\b([^"]*)"([^>]*)>', s):
        tag = m.group(0)
        if 'data-vak=' in tag:
            continue
        t = _tekst(s, m.end())
        k = soort(t, m.group(3))
        if not k:
            continue
        extra = ' data-label="nee"' if (k == 'letop' and t.startswith(('Let op', 'Opgelet'))) or m.group(3) == 'def' else ''
        uit.append(s[pos:m.end() - 1] + ' data-vak="%s"%s data-auto>' % (k, extra)); pos = m.end(); n += 1
    s = ''.join(uit) + s[pos:]
    if n or 'data-vak=' in s or 'class="lpd"' in s:
        i = s.find('</head>')
        s = s[:i] + CSS + s[i:] if i >= 0 else CSS + s
    return s
