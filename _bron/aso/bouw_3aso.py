#!/usr/bin/env python3
"""Maakt de fysicatools voor het 3de jaar 'andere richtingen' (leerplan II-Nat'-d)
uit de tools van 3NW. Eén bron, dus pas altijd de 3NW-tool aan en draai dit script opnieuw:

    python3 _bron/aso/bouw_3aso.py      (vanuit de map van de repo)

Scènes die niet in het leerstofoverzicht 3ASO staan, worden verborgen (niet verwijderd,
zodat de scripts van de tool blijven werken). Thema- en hoofdstuknummers volgen 3ASO.
"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
NOOT = '<!-- GEGENEREERD door _bron/aso/bouw_3aso.py uit {bron}. Pas de bron aan, niet dit bestand. -->\n'

def verberg(s, ids):
    for i in ids:
        s, n = re.subn(r'<section class="scene"( id="%s")' % i, r'<section class="scene-weg" hidden\1', s)
        assert n == 1, i
    return s

def vervang(s, paren):
    for a, b in paren:
        assert a in s, a[:60]
        s = s.replace(a, b)
    return s

def bouw(bron, doel, fn):
    s = (ROOT / bron).read_text(encoding='utf-8')
    s = fn(s)
    s = s.replace('<!DOCTYPE html>\n', '<!DOCTYPE html>\n' + NOOT.format(bron=bron), 1)
    (ROOT / doel).write_text(s, encoding='utf-8')
    print('gemaakt:', doel)


def lesdoelen(sleutel, groepen, breed='1180px', pad='0 24px'):
    """Inklapbaar paneel 'Lesdoelen' met 'Ik kan dit'-vinkjes (bewaard per browser)."""
    li = ''
    for kop, doelen in groepen:
        li += '<li style="list-style:none;margin:8px 0 2px;font-weight:700">%s</li>' % kop
        for d in doelen:
            li += '<li style="list-style:none;margin:2px 0"><label style="display:flex;gap:8px;align-items:flex-start;cursor:pointer"><input type="checkbox" style="margin-top:4px;flex:none">%s</label></li>' % d
    return ('<div style="max-width:%s;margin:14px auto 0;padding:%s"><details id="ld3" style="border:1px solid #c9d6e3;border-radius:10px;padding:8px 14px;background:rgba(127,160,200,.08)">'
            '<summary style="cursor:pointer;font-weight:700">Lesdoelen · Ik kan …</summary><ul style="padding:0;margin:4px 0 6px;font-size:14px;line-height:1.5">%s</ul>'
            '<p style="font-size:12px;opacity:.75;margin:4px 0">Vink aan wat je al kan. Wat je niet kan aanvinken, oefen je nog eens.</p></details></div>\n'
            '<script>(function(){var K="ld3-%s",b=document.querySelectorAll("#ld3 input");var st={};try{st=JSON.parse(localStorage.getItem(K)||"{}")}catch(e){}'
            'b.forEach(function(x,i){x.checked=!!st[i];x.onchange=function(){st[i]=x.checked;try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}})})();</script>\n') % (breed, pad, li, sleutel)

def bijvoeg(naam):
    return (ROOT / '_bron' / 'aso' / naam).read_text(encoding='utf-8')

EY = 'Fysica 3de jaar · andere richtingen · '

bouw('rekenen-fysica.html', 'rekenen-fysica-3aso.html', lambda s: vervang(s, [
    ('Fysica 3de jaar · Thema 2 · Krachten · hoofdstuk 1', EY + 'Thema 1 · Krachten · hoofdstuk 1'),
    ('</header>\n', '</header>\n' + lesdoelen('rekenen', [('1 Rekenen in de fysica', ['Ik geef meetresultaten weer in de SI-eenheid en in de afgeleide eenheid.', 'Ik geef meetresultaten weer met het correcte aantal beduidende cijfers.', 'Ik gebruik de wetenschappelijke notatie om meetresultaten te noteren.'])]))]))

bouw('krachten-beweging.html', 'krachten-beweging-3aso.html', lambda s: vervang(s, [
    ('Fysica 3de jaar · Thema 2 · Krachten · hoofdstuk 2 en 3', EY + 'Thema 1 · Krachten · hoofdstuk 2 en 3'),
    ('<div class="readout" id="s3b-read"></div>', '<div class="readout" id="s3b-read"></div>\n        <div class="note"><strong>Wrijvingskracht</strong> is een kracht die de beweging <strong>tegenwerkt</strong>. Ze ontstaat waar een voorwerp over een ondergrond schuift of rolt, of door de lucht beweegt. Op een ruwe ondergrond (gras, zand) is er veel wrijving, op ijs bijna geen. Wrijving is ook nuttig: zonder wrijving kan je niet stappen, fietsen of remmen.</div>'),
    ('</header>\n', '</header>\n' + lesdoelen('krachtbew', [('2.1 Effect van een kracht', ['Ik toon het statisch en dynamisch effect van een kracht aan in concrete situaties.']), ('2.2 Kracht als vector', ['Ik geef het vectoriële karakter van een kracht weer in concrete situaties.', 'Ik teken krachten als vectoren met behulp van een schaal.']), ('3.1 Verandering van de bewegingstoestand', ['Ik toon aan hoe de bewegingstoestand van een lichaam verandert in concrete situaties.']), ('3.2 Resulterende kracht en beweging', ['Ik leg het traagheidsbeginsel uit in concrete situaties.', 'Ik teken de snelheidsvector bij verschillende bewegingstoestanden van een lichaam.'])])),
    ('  <!-- ===================== DAGELIJKS LEVEN', bijvoeg('snelheidsvector.html') + '\n  <!-- ===================== DAGELIJKS LEVEN')]))

def krachten(s):
    s = verberg(s, ['wr1', 'wr3', 'wr2', 'km1', 'km2', 'km3', 'ev1', 'ev2'])
    s = re.sub(r'(id="ve[12]" data-nr=")6(")', r'\g<1>5\2', s)
    return vervang(s, [
        ('<title>Krachten: zwaartekracht, wrijving, veerkracht en krachtmoment</title>', '<title>Krachten: zwaartekracht en veerkracht</title>'),
        ('Fysica 3de jaar · Thema 2 · Krachten · hoofdstuk 4 tot 7', EY + 'Thema 1 · Krachten · hoofdstuk 4 en 5'),
        ('<strong>Zwaartekracht, normaalkracht, gewicht, wrijving, veerkracht en krachtmoment.</strong>', '<strong>Zwaartekracht, normaalkracht, gewicht en veerkracht.</strong>'),
        ("{id:'zw',label:'4 Zwaartekracht'},{id:'wr',label:'5 Wrijvingskracht'},{id:'ve',label:'6 Veerkracht'},{id:'km',label:'7 Krachtmoment en evenwicht'},",
         "{id:'zw',label:'4 Zwaartekracht'},{id:'ve',label:'5 Veerkracht'},"),
        ("[['alles', 'Door elkaar'], ['zw', '4 Zwaartekracht'], ['wr', '5 Wrijving'], ['ve', '6 Veerkracht'], ['km', '7 Krachtmoment en evenwicht']]",
         "[['alles', 'Door elkaar'], ['zw', '4 Zwaartekracht'], ['ve', '5 Veerkracht']]"),
        ("kies(['zw', 'wr', 've', 'km'])", "kies(['zw', 've'])"),
        ('</header>\n', '</header>\n' + lesdoelen('krachten', [('4.1 Zwaartekracht is overal', ['Ik toon aan dat de zwaartekracht werkzaam is in het zwaarteveld van een hemellichaam.', 'Ik geef het verschil weer tussen het zwaarteveld en de zwaartekracht.']), ('4.2 Zwaartekracht, massa en zwaarteveldsterkte', ['Ik toon de kenmerken van de zwaartekracht als vector aan in concrete situaties.', 'Ik geef in woorden het verband weer tussen de grootte van de zwaartekracht en de massa.', 'Ik gebruik de formule voor het berekenen van de zwaartekracht.', 'Ik vorm de formule van de zwaartekracht om voor het berekenen van de massa en de zwaarteveldsterkte.', 'Ik geef in woorden het verband weer tussen het zwaarteveld en de zwaartekracht.']), ('4.3 en 4.4 Massa, gewicht en normaalkracht', ['Ik geef het verschil weer tussen massa en gewicht.', 'Ik geef het verschil weer tussen zwaartekracht, massa en gewicht.', 'Ik geef het verschil weer tussen normaalkracht, zwaartekracht en gewicht.']), ('5 Veerkracht', ['Ik leg uit wat veerkracht is.', 'Ik geef in woorden het verband weer tussen de grootte van de veerkracht, de veerconstante en de lengteverandering van een elastisch voorwerp.', 'Ik gebruik de omgevormde formules voor de grootte van de veerkracht om vraagstukken op te lossen.'])])),
    ])
bouw('krachten.html', 'krachten-3aso.html', krachten)

bouw('snelheid-afgelegde-weg.html', 'snelheid-3aso.html', lambda s: vervang(s, [
    ('Fysica 3de jaar · Thema 4 · Snelheid · hoofdstuk 1 en 2', EY + 'Thema 2 · Rechtlijnige bewegingen · hoofdstuk 1 en 2'),
    ('<button type="button" id="tab-vt"', '<button type="button" style="display:none" id="tab-vt"'),
    ('<nav class="snav" id="snav"></nav>\n', '<nav class="snav" id="snav"></nav>\n' + lesdoelen('snelheid', [('1 Basisbegrippen', ['Ik geef het verschil weer tussen de begrippen puntmassa, baan, positie, tijdstip, verplaatsing en tijdsverloop.']), ('2.1 Gemiddelde en ogenblikkelijke snelheid', ['Ik leg het begrip snelheid uit.', 'Ik geef het verschil weer tussen de gemiddelde snelheid en de ogenblikkelijke snelheid.']), ('2.2 Eenparig rechtlijnige beweging', ['Ik beschrijf en herken een eenparig rechtlijnige beweging.', 'Ik gebruik de formule voor het berekenen van de gemiddelde snelheid.', 'Ik vorm de formule van de gemiddelde snelheid om voor het berekenen van de verplaatsing en het tijdsverloop.', 'Ik teken de x(t)-grafiek en de v(t)-grafiek van een eenparig rechtlijnige beweging.', 'Ik geef het verband weer tussen de helling van de grafiek en de snelheid van een lichaam.', 'Ik leg het differentiequotiënt Δx/Δt uit.'])], breed='none', pad='0')),
    ('Kijk naar de <b>helling</b> van de x(t)-grafiek en de <b>oppervlakte</b> onder de v(t)-grafiek.', 'Kijk naar de <b>helling</b> van de x(t)-grafiek en naar de v(t)-grafiek.'),
    ('<p>v(t)-grafiek: een horizontale rechte. De oppervlakte eronder is de verplaatsing.</p>', '<p>v(t)-grafiek: een horizontale rechte, want de snelheid verandert niet.</p>'),
    ("if (te > 1) p += t(B.X(te / 2), (B.Y(0) + B.Y(v)) / 2 + 5, 'oppervlakte = Δx', {s: 13, w: 700, c: INK, a: 'middle'});", ''),
    ('fill="\' + (v >= 0 ? \'#2fa36b\' : \'#d9455f\') + \'" opacity=".22"', 'fill="none" opacity="0"'),
    (' De oppervlakte ligt onder de t-as.', ' De v(t)-grafiek ligt onder de t-as.'),
    ('  <!-- 2.2 GRAFIEKEN OEFENEN', bijvoeg('grafiektekenen.html') + '\n  <!-- 2.2 GRAFIEKEN OEFENEN'),
]))
