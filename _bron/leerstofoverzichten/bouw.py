"""Bouwt leerstofoverzichten.html uit de bestanden in deze map.

Gebruik:  python3 _bron/leerstofoverzichten/bouw.py

Een nieuw of aangepast overzicht:
1. Zet het Word-bestand in deze map en zet het om:  pandoc bestand.docx -t gfm -o 4nw-jun.md
   (of plak de tekst in een .md-bestand).
2. Voeg een regel toe in OVERZICHTEN hieronder (id = bestandsnaam zonder .md).
3. Draai dit script en publiceer (git add, commit, push).
"""
import re, subprocess, html
from pathlib import Path

MAP = Path(__file__).parent
REPO = MAP.parent.parent

# (id, klas, examen, richting)  — volgorde = volgorde op de pagina
OVERZICHTEN = [
    ("3nw-dec",   "3NW",  "PW december",               "wet"),
    ("3nw-jun",   "3NW",  "2de en 3de trimester",      "wet"),
    ("4nw-dec",   "4NW",  "PW december",               "wet"),
    ("4nw-pasen", "4NW",  "2de en 3de trimester",      "wet"),
    ("5wet-dec",  "5Wet", "PW december",               "wet"),
    ("5wet-jun",  "5Wet", "PW juni",                   "wet"),
    ("3aso-dec",  "3ASO", "PW december",               "andere"),
    ("3aso-jun",  "3ASO", "PW juni",                   "andere"),
]

DOEL = re.compile(r'(?:(?<=\s)|(?<=\|))\s*(?:[-–☐•]\s*(?=(?:Ik|Je|ik|je)\b)|[-☐•]\s+(?=[A-Z(]))')
SUBNR = re.compile(r'(?<=[^\s|])\s+(?=\d+\.\d+(?:\.\d+)?\.?\s+[A-ZÀ-Ý])')


def vet(regel):
    """De omzetting uit Word zet elk vet stukje tussen ** **. Zet om naar <b>, ook als de
    sterretjes niet netjes sluiten (Word knipt vet tekst soms midden in een woord)."""
    stukken = regel.split('**')
    uit, aan = [], False
    for i, s in enumerate(stukken):
        if i:
            aan = not aan
        if aan and s.strip():
            lead = s[:len(s) - len(s.lstrip())]; trail = s[len(s.rstrip()):]
            uit.append(f'{lead}<b>{s.strip()}</b>{trail}')
        elif not aan:
            uit.append(s)
        else:
            uit.append(s)  # leeg vet stuk: alleen spaties
    return ''.join(uit).replace('</b><b>', '').replace('</b> <b>', ' ')


def cel_regels(regel):
    """Lesdoelen die in één cel achter elkaar staan, krijgen elk een eigen regel."""
    if not regel.lstrip().startswith('|'):
        return regel
    regel = re.sub(r'\|\s*-\s+(?=\d)', '| ', regel)
    regel = DOEL.sub(' <br>• ', regel)
    regel = re.sub(r'(?<=[.)!])\s+(?=(?:Ik|Je)\b)', ' <br>• ', regel)
    regel = SUBNR.sub(' <br>', regel)
    regel = re.sub(r'(Lesdoelen\s*:?)\s+(?!\|)', r'<b>\1</b><br>', regel)
    regel = re.sub(r'\|\s*<br>', '| ', regel)
    regel = re.sub(r'(<br>\s*)+<br>', '<br>', regel)
    return regel


def omzetten(md):
    regels = []
    for r in md.splitlines():
        r = r.lstrip('\t')
        r = vet(r)
        r = cel_regels(r)
        regels.append(r)
    tekst = '\n'.join(regels)
    h = subprocess.run(['pandoc', '-f', 'markdown+pipe_tables+raw_html-tex_math_dollars', '-t', 'html', '--wrap=none'],
                       input=tekst, capture_output=True, text=True, check=True).stdout
    h = re.sub(r'<colgroup>.*?</colgroup>', '', h, flags=re.S)
    h = re.sub(r'<(table|thead|tbody|tr|td|th)\b[^>]*>', r'<\1>', h)
    # paragraaftitels in een cel vet
    h = re.sub(r'(<td>|<br>)\s*(\d+\.\d+(?:\.\d+)?\.?\s[^<•]*?)\s*(?=<br>|</td>)', r'\1<b>\2</b>', h)
    # rij met lege rechtercel: één brede cel
    h = re.sub(r'<(td|th)>((?:(?!</\1>).)*?\S(?:(?!</\1>).)*?)</\1>\s*<\1>\s*</\1>', r'<\1 colspan="2">\2</\1>', h, flags=re.S)
    h = re.sub(r'<th>\s*</th>', '<th></th>', h)
    # lege rijen weg
    h = re.sub(r'<tr>\s*(<td>\s*</td>\s*)+</tr>', '', h)
    return h


def titel_en_inhoud(h):
    m = re.match(r'\s*<p>(.*?)</p>', h, flags=re.S)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip(), h[m.end():]
    return '', h


def bouw():
    secties, knoppen = [], []
    klassen = []
    for oid, klas, examen, richting in OVERZICHTEN:
        bron = MAP / f'{oid}.md'
        titel, inhoud = titel_en_inhoud(omzetten(bron.read_text(encoding='utf-8')))
        secties.append(f'<section class="lso" id="lso-{oid}" data-id="{oid}" data-klas="{klas}" hidden>\n'
                       f'<h2>{html.escape(klas)} · {html.escape(examen)}</h2>\n'
                       f'<p class="bron">{html.escape(titel)}</p>\n{inhoud}</section>')
        if klas not in klassen:
            klassen.append(klas)
        knoppen.append((klas, oid, examen))
    nav = []
    for k in klassen:
        items = ''.join(f'<button type="button" data-id="{oid}">{html.escape(ex)}</button>'
                        for kk, oid, ex in knoppen if kk == k)
        nav.append(f'<div class="groep"><span class="klas">{k}</span>{items}</div>')
    sjabloon = (MAP / 'sjabloon.html').read_text(encoding='utf-8')
    pagina = sjabloon.replace('<!--NAV-->', '\n'.join(nav)).replace('<!--INHOUD-->', '\n'.join(secties))
    (REPO / 'leerstofoverzichten.html').write_text(pagina, encoding='utf-8')
    print('leerstofoverzichten.html:', len(pagina), 'tekens,', len(secties), 'overzichten')


if __name__ == '__main__':
    bouw()
