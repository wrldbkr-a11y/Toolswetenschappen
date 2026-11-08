"""In vragen schrijven we de volledige naam van een grootheid, niet het symbool.
Niet: "Bereken k" of "met F_z = 20 N". Wel: "Bereken de veerconstante" en "met een zwaartekracht van 20 N".
In uitleg, oplossingen en formules blijven de symbolen staan.

namen_in_vragen(html, bestand) past dit toe op: de opgave van oefeningen (div.tekst), de vraag van denkvragen
en Test jezelf (div.vraag), en de wisbordvragen (span.wb). Wordt aangeroepen door bouw.py.
"""
import re

ALG = {  # symbool (zoals in de html) → (lidwoord, naam)
    'F<sub>w,s,max</sub>': ('de', 'maximale statische wrijvingskracht'), 'F<sub>w,s</sub>': ('de', 'statische wrijvingskracht'),
    'F<sub>w,d</sub>': ('de', 'dynamische wrijvingskracht'), 'F<sub>z</sub>': ('de', 'zwaartekracht'), 'F<sub>N</sub>': ('de', 'normaalkracht'),
    'F<sub>G</sub>': ('het', 'gewicht'), 'F<sub>v</sub>': ('de', 'veerkracht'), 'F<sub>r</sub>': ('de', 'resulterende kracht'),
    'μ<sub>s</sub>': ('de', 'statische wrijvingscoëfficiënt'), 'v<sub>gem</sub>': ('de', 'gemiddelde snelheid'),
    'A<sub>r</sub>': ('de', 'relatieve atoommassa'), 'Δl': ('de', 'uitrekking'), 'Δx': ('de', 'verplaatsing'), 'Δt': ('het', 'tijdsverloop'),
    'k': ('de', 'veerconstante'), 'm': ('de', 'massa'),
}
PER = {  # extra symbolen per soort pagina (alleen waar ze eenduidig zijn)
    'krachten': {'g': ('de', 'zwaarteveldsterkte')}, 'zwaartekracht': {'g': ('de', 'zwaarteveldsterkte')}, 'archimedes': {'g': ('de', 'zwaarteveldsterkte')},
    'licht': {'g': ('de', 'grenshoek'), 'i': ('de', 'invalshoek')}, 'lichtbreking': {'r': ('de', 'brekingshoek')},
    'weerkaatsing': {'i': ('de', 'invalshoek'), 'r': ('de', 'weerkaatsingshoek')},
    'chemie': {'Z': ('het', 'atoomnummer'), 'A': ('het', 'massagetal')},
    'lenzen': {'f': ('de', 'brandpuntsafstand'), 'v': ('de', 'voorwerpsafstand'), 'b': ('de', 'beeldafstand'), 'N': ('de', 'vergrotingsfactor'),
               'B': ('de', 'beeldgrootte'), 'V': ('de', 'voorwerpsgrootte')},
    'schakel': {'R': ('de', 'weerstand'), 'U': ('de', 'spanning'), 'I': ('de', 'stroomsterkte'), 'R<sub>s</sub>': ('de', 'vervangingsweerstand')},
    'snelheid': {'v': ('de', 'snelheid'), 'x₁': ('de', 'beginpositie'), 'x₂': ('de', 'eindpositie')}, 'beweging': {'v': ('de', 'snelheid')},
    'archimedes': {'F<sub>A</sub>': ('de', 'archimedeskracht'), 'V': ('het', 'volume'), 'ρ': ('de', 'massadichtheid'), 'p': ('de', 'druk')},
    'druk': {'V': ('het', 'volume'), 'ρ': ('de', 'massadichtheid'), 'p': ('de', 'druk'), 'A': ('de', 'oppervlakte'), 'h': ('de', 'diepte')},
}

def _kaart(bestand):
    k = dict(ALG)
    for sleutel, extra in PER.items():
        if sleutel in bestand: k.update(extra)
    return k

def _vervang(tekst, kaart):
    syms = sorted(kaart, key=len, reverse=True)
    alt = '|'.join(re.escape(x) for x in syms)
    S = r'(?<![\w;/])(' + alt + r')(?![\w<(])'          # symbool, niet in een woord en niet "v(t)"
    W = r'(\d+(?:[,.]\d+)?(?: · 10[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)?(?:\s?(?:N/kg|N/m|kg/m³|km/h|m/s|cm³|m³|kg|cm|mm|Pa|N|g|m|s|J|W|°|%)(?![\w]))?|…)'
    N = lambda m, i=1: kaart[m.group(i)][1]
    L = lambda m, i=1: kaart[m.group(i)][0]
    zin = lambda pre: pre == '' or pre.rstrip().endswith(('.', '?', '!', '>'))
    # 0. "naam SYM" (symbool achter zijn eigen naam) → naam
    for sym, (lw, naam) in kaart.items():
        tekst = re.sub(re.escape(naam) + r' ' + re.escape(sym) + r'(?![\w<(])', naam, tekst)
    # 1. "met/heeft/bij SYM = waarde" → "met een NAAM van waarde"
    tekst = re.sub(r'\b(met|heeft|bij|Bij|Met) (?:een )?' + S + r' = ' + W, lambda m: f'{m.group(1)} een {N(m, 2)} van {m.group(3)}', tekst)
    tekst = re.sub(r'(van ' + W + r') en ' + S + r' = ' + W, lambda m: f'{m.group(1)} en een {N(m, 3)} van {m.group(4)}', tekst)
    # 2. "Wat betekent SYM = waarde" → "Wat betekent een NAAM van waarde"
    tekst = re.sub(r'(Wat betekent) ' + S + r' = ' + W, lambda m: f'{m.group(1)} een {N(m, 2)} van {m.group(3)}', tekst)
    # 3. "(neem SYM ≈ waarde" / "(SYM = waarde" → "(neem een NAAM van waarde" / "(NAAM: waarde"
    tekst = re.sub(r'\(neem ' + S + r' [=≈] ' + W, lambda m: f'(neem een {N(m)} van {m.group(2)}', tekst)
    tekst = re.sub(r'\(' + S + r' ([=≈]) ' + W, lambda m: f'({N(m)} {m.group(2)} {m.group(3)}', tekst)
    # 4. "is SYM = waarde" → "is de NAAM waarde"; "Als SYM = waarde" → "Als de NAAM waarde is"
    tekst = re.sub(r'\bis ' + S + r' = ', lambda m: f'is {L(m)} {N(m)} ', tekst)
    tekst = re.sub(r'\b(Als|als) ' + S + r' = ' + W, lambda m: f'{m.group(1)} {L(m, 2)} {N(m, 2)} {m.group(3)} is', tekst)
    # 5. overige "SYM = waarde" → "de NAAM is waarde" (met hoofdletter aan het begin van een zin)
    def is_(m):
        lw = L(m, 2).capitalize() if zin(m.group(1)) else L(m, 2)
        return f'{m.group(1)}{lw} {N(m, 2)} is {m.group(3)}'
    tekst = re.sub(r'(^|[.?!>]\s*|\s|,\s)' + S + r' = ' + W, is_, tekst)
    # 6. "een SYM" → "een NAAM"
    tekst = re.sub(r'\been ' + S, lambda m: f'een {N(m)}', tekst)
    # 7. lange symbolen (F_z, Δl, μ_s ...) overal → "de NAAM"
    lang = '|'.join(re.escape(x) for x in syms if len(x) > 1)
    def los(m):
        lw = L(m, 2); pre = m.group(1)
        if m.group(0)[len(pre):].startswith(('de ', 'het ')): return m.group(0)
        if zin(pre): lw = lw.capitalize()
        return f'{pre}{lw} {N(m, 2)}'
    tekst = re.sub(r'(^|[.?!>]\s*|[\s(,/:])(?<![\w;])(' + lang + r')(?![\w<(])', los, tekst)
    # 8. losse letters (k, g, B ...) alleen na een werkwoord of als "k?"
    kort = '|'.join(re.escape(x) for x in syms if len(x) == 1)
    if kort:
        tekst = re.sub(r'\b((?:Bereken|Bepaal|Zoek|Meet|bereken|bepaal|meet)(?: telkens)?) (' + kort + r')\b(?![<(])', lambda m: f'{m.group(1)} {L(m, 2)} {N(m, 2)}', tekst)
        tekst = re.sub(r'\b(met|op) (' + kort + r')(?=[:.,?])', lambda m: f'{m.group(1)} {L(m, 2)} {N(m, 2)}', tekst)
        kort2 = '|'.join(re.escape(x) for x in syms if len(x) == 1 and x not in ('m', 'g', 's'))   # m, g, s kunnen eenheden zijn
        if kort2: tekst = re.sub(r'(^|[.!>:]\s*|(?<!…)\s)(' + kort2 + r')\?', lambda m: los(m) + '?', tekst)
        tekst = re.sub(r'\b(Is|is) (' + kort + r') (?=\w)', lambda m: f'{m.group(1)} {L(m, 2)} {N(m, 2)} ', tekst)
        tekst = re.sub(r'\b(over|van|voor) (' + kort + r') (?=(?:en|of)\b)', lambda m: f'{m.group(1)} {L(m, 2)} {N(m, 2)} ', tekst)
        tekst = re.sub(r'\bje (' + kort + r') van\b', lambda m: f'je {L(m)} {N(m)} van', tekst)
        tekst = re.sub(r'\bis (' + kort + r')\?', lambda m: f'is {L(m)} {N(m)}?', tekst)
        tekst = re.sub(r'(: | en )m\?', lambda m: m.group(1) + 'de massa?', tekst) if 'm' in kaart else tekst
        tekst = re.sub(r'\b([Dd]uid) (' + kort + r') en (' + kort + r') aan', lambda m: f'{m.group(1)} {L(m, 2)} {N(m, 2)} en {L(m, 3)} {N(m, 3)} aan', tekst)
        tekst = re.sub(r'(?<=, )(' + kort + r')(?=,| en )', lambda m: f'{L(m)} {N(m)}', tekst)
        tekst = re.sub(r'(^|[>\s])(' + kort + r') in functie van', lambda m: los(m) + ' in functie van', tekst)
        tekst = re.sub(r'\b((?:Meet|Bereken|Bepaal|meet|bereken|bepaal) (?:de|het) [a-zë]+) en (' + kort + r')\b(?![<(])', lambda m: f'{m.group(1)} en {L(m, 2)} {N(m, 2)}', tekst)
        tekst = re.sub(r'\bin functie van (' + kort + r')\b(?![<(])', lambda m: f'in functie van {L(m)} {N(m)}', tekst)
    tekst = re.sub(r'\b(de|het) (de|het) ', r'\2 ', tekst, flags=re.I)
    return re.sub(r'\b(is (?:de|het) [\w ]+?) is ', r'\1 ', tekst)

def _in_tags(html, open_re, sluit, kaart):
    uit, pos = [], 0
    for m in re.finditer(open_re, html):
        if m.start() < pos: continue
        einde = html.find(sluit, m.end())
        if einde < 0: break
        uit.append(html[pos:m.end()]); binnen = html[m.end():einde]
        # figuren (svg) en de stappen in een opgave niet aanraken
        delen = re.split(r'(<svg.*?</svg>|<figure.*?</figure>)', binnen, flags=re.S)
        uit.append(''.join(d if d.startswith(('<svg', '<figure')) else _vervang(d, kaart) for d in delen))
        pos = einde
    uit.append(html[pos:])
    return ''.join(uit)

def namen_in_vragen(html, bestand=''):
    if 'biologie' in bestand: return html
    kaart = _kaart(bestand)
    html = _in_tags(html, r'<div class="tekst">', '<div class="onder"', kaart)
    html = _in_tags(html, r'<div class="vraag"><div class="kop">Denkvraag</div><p>', '</p></div>', kaart)
    html = _in_tags(html, r'<span class="wb">', '</span> <span class="antw">', kaart)
    return html
