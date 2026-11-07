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

EY = 'Fysica 3de jaar · andere richtingen · '

bouw('rekenen-fysica.html', 'rekenen-fysica-3aso.html', lambda s: vervang(s, [
    ('Fysica 3de jaar · Thema 2 · Krachten · hoofdstuk 1', EY + 'Thema 1 · Krachten · hoofdstuk 1')]))

bouw('krachten-beweging.html', 'krachten-beweging-3aso.html', lambda s: vervang(s, [
    ('Fysica 3de jaar · Thema 2 · Krachten · hoofdstuk 2 en 3', EY + 'Thema 1 · Krachten · hoofdstuk 2 en 3'),
    ('<div class="readout" id="s3b-read"></div>', '<div class="readout" id="s3b-read"></div>\n        <div class="note"><strong>Wrijvingskracht</strong> is een kracht die de beweging <strong>tegenwerkt</strong>. Ze ontstaat waar een voorwerp over een ondergrond schuift of rolt, of door de lucht beweegt. Op een ruwe ondergrond (gras, zand) is er veel wrijving, op ijs bijna geen. Wrijving is ook nuttig: zonder wrijving kan je niet stappen, fietsen of remmen.</div>')]))

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
    ])
bouw('krachten.html', 'krachten-3aso.html', krachten)

bouw('snelheid-afgelegde-weg.html', 'snelheid-3aso.html', lambda s: vervang(s, [
    ('Fysica 3de jaar · Thema 4 · Snelheid · hoofdstuk 1 en 2', EY + 'Thema 2 · Rechtlijnige bewegingen · hoofdstuk 1 en 2'),
    ('<button type="button" id="tab-vt"', '<button type="button" style="display:none" id="tab-vt"'),
]))
