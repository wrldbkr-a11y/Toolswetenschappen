"""Elke tabel krijgt een titel per kolom (een kopregel met <th>).
- Een eerste rij met alleen vetgedrukte cellen (zoals ttabel() maakt) wordt een echte kopregel.
- Tabellen zonder kopregel krijgen er een uit KOPPEN (op basis van de tekst in de eerste cel).
- Staat een tabel niet in KOPPEN, dan kiest koppen_toevoegen een algemene kop en meldt dat (zodat je KOPPEN aanvult).
Wordt aangeroepen door bouw.py.
"""
import re, html as H

KOPPEN = {  # eerste cel van de eerste rij → titels van de kolommen
    'W': ['Symbool', 'Betekenis en eenheid'], 'P': ['Symbool', 'Betekenis en eenheid'], 'FA': ['Symbool', 'Betekenis en eenheid'],
    'F': ['Symbool', 'Betekenis en eenheid'], 'p': ['Symbool', 'Betekenis en eenheid'], 'ph': ['Symbool', 'Betekenis en eenheid'],
    'Q': ['Symbool', 'Betekenis en eenheid'],
    'Groep A': ['Groep', 'Wat onderzoeken ze?', 'Opstelling'],
    'ρv > ρvl': ['Massadichtheden', 'Krachten', 'Gevolg'],
    'kurk': ['Stof', 'Massadichtheid', 'Vloeistof', 'Massadichtheid'],
    'FA < Fz': ['Krachten', 'Gevolg'],
    'Barometer': ['Toestel', 'Wat meet het?'],
    'Gegeven': ['Stap', 'Uitwerking'],
    'wel': ['Hangt af van?', 'Factor'],
    'Open systeem': ['Soort systeem', 'Wat wisselt het uit?', 'Voorbeeld'],
    'gravitationele potentiële energie': ['Soort energie', 'Waar komt ze vandaan?', 'Voorbeeld'],
    'Gravitationele potentiële energie': ['Soort energie', 'Formule', 'Eenheden'],
    'Statisch effect': ['Effect', 'Wat gebeurt er?'],
    'gewicht aan een veer': ['Situatie', 'Effect', 'Uitleg'],
    'Fr = 0': ['Resulterende kracht', 'Gevolg voor de snelheid'],
    'Een grasmaaier duwen': ['Situatie', 'Ontbinden'],
    'Hoofdas': ['Begrip', 'Betekenis'],
    'Van ijl naar dicht': ['Overgang', 'Breking', 'Hoeken'],
    'zwaarteveld': ['Zwaarteveld', 'Homogeen elektrisch veld'],
    'celwand': ['Deel van de cel', 'Functie'], 'wortel': ['Orgaan', 'Functie'], 'dekweefsel': ['Weefsel', 'Kenmerk en functie'],
    'licht en genoeg water': ['Situatie', 'Huidmondjes'], 'wortelhaartjes': ['Deel', 'Kenmerk en functie'],
    'Lichtbron zien': ['Wat zie je?', 'Weg van het licht'], 'Invalspunt': ['Begrip', 'Betekenis'],
    'Regelmatige weerkaatsing': ['Soort weerkaatsing', 'Wat gebeurt er?', 'Voorbeelden'],
    'Lichtbron': ['Soort', 'Betekenis', 'Voorbeelden'], 'Divergerend': ['Soort bundel', 'Wat doen de stralen?', 'Voorbeelden'],
    'Zonsverduistering': ['Verduistering', 'Volgorde', 'Wat gebeurt er?'],
}
GEMIST = []

def _plat(c):
    return ' '.join(H.unescape(re.sub(r'<[^>]+>', '', c)).split())

def _tabel(m, bestand):
    open_tag, binnen = m.group(1), m.group(2)
    if 'cornell' in open_tag: return m.group(0)   # afdruksjabloon voor notities: geen kop
    rijen = re.findall(r'<tr[^>]*>.*?</tr>', binnen, re.S)
    if not rijen: return m.group(0)
    eerste = rijen[0]
    if '<th' in eerste: return m.group(0)
    cellen = re.findall(r'<td[^>]*>(.*?)</td>', eerste, re.S)
    if cellen and all(re.fullmatch(r'\s*(<b>.*?</b>)?\s*', c, re.S) for c in cellen):   # vette eerste rij = kopregel
        kop = '<tr>' + ''.join(f'<th>{re.sub(r"</?b>", "", c)}</th>' for c in cellen) + '</tr>'
        return open_tag + binnen.replace(eerste, kop, 1) + '</table>'
    sleutel = _plat(cellen[0]) if cellen else ''
    titels = KOPPEN.get(sleutel)
    if not titels or len(titels) != len(cellen):
        titels = (['Begrip', 'Betekenis'] if len(cellen) == 2 else ['Begrip', 'Betekenis', 'Voorbeeld'] if len(cellen) == 3 else [''] * len(cellen))
        GEMIST.append((bestand, sleutel, len(cellen)))
    kop = '<tr>' + ''.join(f'<th>{x}</th>' for x in titels) + '</tr>'
    i = binnen.find('<tr')
    return open_tag + binnen[:i] + kop + binnen[i:] + '</table>'

CSS = '<style>.vb th{text-align:left;font-weight:700;padding:4px 12px 4px 0;border-bottom:2px solid var(--line,#cbd5e1);color:var(--text,#1D2A36)}</style>'

def koppen_toevoegen(html, bestand=''):
    hoofd, _, rest = html.partition('<body')
    if not rest: hoofd, rest = '', html
    rest = re.sub(r'(<table[^>]*>)(.*?)</table>', lambda m: _tabel(m, bestand), rest, flags=re.S)
    if CSS not in hoofd: hoofd = hoofd.replace('</head>', CSS + '</head>', 1)
    for g in [x for x in GEMIST if x[0] == bestand]: print('  tabel zonder vaste kop:', g)
    GEMIST.clear()
    return hoofd + ('<body' + rest if _ else rest)
