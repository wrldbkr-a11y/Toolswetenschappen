"""Maakt potentiaal.html (5Wet, thema 1, hoofdstuk 4) uit elektrisch-veld.html.

Beide tools delen dezelfde code. Pas altijd elektrisch-veld.html aan en draai daarna:
    python3 _bron/ev/potentiaal.py
    python3 _bron/lesdoelen/nw_lesdoelen.py      (lesdoelen 3.x in elektrisch-veld, 4.x in potentiaal)

Welke tabbladen een hoofdstuk toont, staat in data-hfd op elke tab-knop ("3", "4" of "3 4").
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
s = (ROOT / 'elektrisch-veld.html').read_text(encoding='utf-8')


def vervang(oud, nieuw):
    global s
    assert s.count(oud) == 1, oud
    s = s.replace(oud, nieuw)


vervang('<title>Elektrisch veld en gravitatieveld</title>', '<title>Potentiaal</title>')
vervang('<body data-hfd="3">', '<body data-hfd="4">')
vervang('<h1>Elektrisch veld en gravitatieveld</h1>', '<h1>Potentiaal</h1>')
s = re.sub(r'  <p class="sub">Veldlijnen, veldgrootheden[^\n]*</p>\n',
           '  <p class="sub">Van zwaarteveld naar elektrisch veld: veldsterkte, potentiële energie en potentiaal in een homogeen veld</p>\n',
           s, count=1)
s = re.sub(r'<!--ldnw-->.*?<!--/ldnw-->\n', '', s, flags=re.S)   # nw_lesdoelen.py zet de juiste doelen
(ROOT / 'potentiaal.html').write_text(s, encoding='utf-8')
print('potentiaal.html gemaakt')
