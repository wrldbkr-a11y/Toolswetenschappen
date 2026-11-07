"""Afvinkbaar lesdoelenpaneel in de NW-tools (3NW, 4NW, 5Wet).

Bron: nw_overzichten.json (lesdoelen per paragraaf, uit de leerstofoverzichten).
Het paneel staat tussen <!--ldnw--> en <!--/ldnw-->, dus opnieuw draaien is veilig.
bouw_3aso.py haalt dit blok weg voor de 3ASO-versies.

Gebruik:  python3 _bron/lesdoelen/nw_lesdoelen.py   (daarna eventueel aso/bouw_3aso.py)
"""
import json, re, sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
ROOT = HIER.parent.parent
sys.path.insert(0, str(HIER.parent))
from vinkjes import voeg_toe

OV = json.loads((HIER / 'nw_overzichten.json').read_text(encoding='utf-8'))

# vaste titels voor koppen die in het overzicht algemeen zijn
TITEL = {('3dec', 12): '2 Effect van een kracht', ('3jun', 0): '1 Rekenen in de fysica',
         ('4dec', 0): '1 Druk bij vaste stoffen', ('5dec', 13): 'Wet van Ohm in gemengde schakelingen'}

# tool: (anker, [(overzicht, [indexen])])
KAART = {
    'optica.html': ('</header>\n', [('3dec', range(0, 12))]),
    'krachten-construeren.html': ('</header>\n', [('3dec', [12, 13, 14, 15]), ('3jun', [1])]),
    'rekenen-fysica.html': ('</header>\n', [('3jun', [0])]),
    'krachten-beweging.html': ('</header>\n', [('3jun', [2, 3])]),
    'krachten.html': ('</header>\n', [('3jun', range(4, 13))]),
    'snelheid-afgelegde-weg.html': ('<nav class="snav" id="snav"></nav>\n', [('3jun', [13, 14, 15])]),
    'druk.html': ('</header>\n', [('4dec', range(0, 7))]),
    'energie-vermogen.html': ('</header>\n', [('4dec', range(7, 11)), ('4jun', [0, 1])]),
    'warmte-gassen.html': ('</header>\n', [('4jun', range(2, 11))]),
    'elektriciteit.html': ('</header>\n', [('4jun', range(11, 19))]),
    'ladingen.html': ('</header>\n', [('5dec', [0, 1, 2])]),
    'elektrostatica.html': ('</header>\n', [('5dec', [2])]),
    'krachten-op-ladingen.html': ('</header>\n', [('5dec', [3, 4])]),
    'elektrisch-veld.html': ('de Aarde</p>\n', [('5dec', range(5, 13))]),
    'schakelingen.html': ('</header>\n', [('5dec', [13])]),
    'elektromagnetisme.html': ('</header>\n', [('5jun', range(0, 8))]),
    'kernfysica.html': ('</header>\n', [('5jun', range(8, 23))]),
}


def kop_schoon(k):
    k = re.sub(r'\s*\(?\s*(p\.?\s*)?\d+\s*([-–,]|en)\s*\d+.*$', '', k)    # (p12-14), (28-33), p 125 en 127
    k = re.sub(r'\s*\(?\s*p\.?\s*\d+.*$', '', k)                           # p 24, (p. 195)
    k = re.sub(r'\s*\(\s*p\.?\s*$', '', k)
    k = re.sub(r'^HOOFDSTUK\s+(\d+)\s*:\s*(.*)$', lambda m: m.group(1) + ' ' + m.group(2).capitalize(), k)
    k = re.sub(r'^(\d+(\.\d+)*)\.\s', r'\1 ', k)
    k = k.strip(' .').replace('Gezichtveld', 'Gezichtsveld')
    return re.sub(r'^([\d.]+ )(\w)', lambda m: m.group(1) + m.group(2).upper(), k)


def doel_schoon(d):
    d = d.strip()
    return d if d.endswith(('.', '?', '!', ')')) else d + '.'


def paneel(groepen):
    li = ''.join('<p class="ldk">%s</p><ul class="doelen">%s</ul>' % (k, ''.join('<li>%s</li>' % doel_schoon(d) for d in ds))
                 for k, ds in groepen)
    return ('<!--ldnw--><div class="ldnw-wrap"><details id="ldnw">'
            '<style>.ldnw-wrap{max-width:1180px;margin:14px auto 0;padding:0 24px}'
            '#ldnw{border:1px solid #c9d6e3;border-radius:10px;padding:8px 14px;background:rgba(127,160,200,.08)}'
            '#ldnw>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:10px;font-weight:700}#ldnw>summary::-webkit-details-marker{display:none}'
            '#ldnw .pijl{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:50%;background:#2F6FB0;color:#fff;font-size:13px;transition:transform .2s}'
            '#ldnw[open] .pijl{transform:rotate(90deg)}#ldnw .hint{font-weight:500;font-size:13px;opacity:.75}#ldnw[open] .hint{display:none}'
            '#ldnw .ldk{margin:10px 0 2px;font-weight:700}#ldnw ul.doelen{margin:0;font-size:14px;line-height:1.5}</style>'
            '<summary><span class="pijl">▶</span>Lesdoelen · Ik kan … <span class="hint">klik om te openen en af te vinken</span></summary>%s'
            '<p style="font-size:12px;opacity:.75;margin:8px 0 4px">Vink aan wat je al kan. Wat je niet kan aanvinken, oefen je nog eens.</p></details></div><!--/ldnw-->\n').replace('%s', li)


def main():
    for naam, (anker, delen) in KAART.items():
        p = ROOT / naam
        s = p.read_text(encoding='utf-8')
        s = re.sub(r'<!--ldnw-->.*?<!--/ldnw-->\n', '', s, flags=re.S)
        groepen = []
        for ov, idx in delen:
            for i in idx:
                k, ds = OV[ov][i]
                groepen.append((TITEL.get((ov, i)) or kop_schoon(k), ds))
        assert s.count(anker) >= 1, (naam, anker)
        s = s.replace(anker, anker + paneel(groepen), 1)
        p.write_text(voeg_toe(s, naam), encoding='utf-8')
        print('%-28s %d groepen, %d doelen' % (naam, len(groepen), sum(len(d) for _, d in groepen)))


if __name__ == '__main__':
    main()
