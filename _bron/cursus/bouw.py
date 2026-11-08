import json, html

SJABLOON = open('/home/claude/cursus/sjabloon.html', encoding='utf-8').read()

def denk(id, vraag, stappen, besluit):
    lis = ''.join(f'<li><span class="stap">{s[0]}</span> {s[1]}</li>' for s in stappen)
    return f'''<div class="denk" data-vrij="{id}">
  <div class="vraag"><div class="kop">Denkvraag</div><p>{vraag}</p></div>
  <div class="onder"><div class="redenering"><ol>{lis}</ol><div class="besluit">{besluit}</div></div></div>
</div>'''

def oef(id, nr, titel, tekst, stappen, besluit):
    lis = ''.join(f'<li><span class="stap">{s[0]}</span> {s[1]}</li>' for s in stappen)
    return f'''<div class="oef" data-vrij="{id}">
  <div class="titel"><span class="nr">{nr}</span>{titel}</div>
  <div class="tekst">{tekst}</div>
  <div class="onder" style="margin-top:8px"></div>
  <div class="redenering"><ol>{lis}</ol><div class="besluit">{besluit}</div></div>
</div>'''

def blok(id, nr, titel, inhoud, vrij=None):
    v = f' data-vrij="{vrij}"' if vrij else ''
    n = f'<span class="nr">{nr}</span>' if nr else ''
    return f'<section class="blok" id="{id}"{v}>\n<h2>{n}{titel}</h2>\n{inhoud}\n</section>\n'

def tool(href, tekst):
    return f'<a class="toolknop" href="{href}" target="_blank" rel="noopener">▶ {tekst}</a>'

def kader(kop, tekst):
    return f'<div class="kader"><div class="kop">{kop}</div>{tekst}</div>'

def figuur(svg, onderschrift=''):
    return f'<figure class="figuur">{svg}<figcaption>{onderschrift}</figcaption></figure>'

def bouw(bestand, eyebrow, titel, intro, blokken, vrijgave, cornell):
    vr = '\n'.join(f'  {k}: {"true" if v else "false"},' + ' '*(24-len(k)-len(str(v))) + f'// {uitleg}' for k, v, uitleg in vrijgave)
    s = (SJABLOON.replace('{{TITEL}}', titel).replace('{{EYEBROW}}', eyebrow).replace('{{INTRO}}', intro)
         .replace('{{INHOUD}}', ''.join(blokken)).replace('{{VRIJGAVE}}', vr)
         .replace('{{CORNELL}}', json.dumps(cornell, ensure_ascii=False)).replace('{{BESTAND}}', bestand).replace('{{FOOTER}}', FOOTER))
    import sys; sys.path.insert(0, '/home/claude/toolswetenschappen/_bron'); from vinkjes import voeg_toe
    sys.path.insert(0, '/home/claude/toolswetenschappen/_bron/cursus'); from namen import namen_in_vragen
    s = namen_in_vragen(s, bestand)   # in vragen: volledige namen, geen symbolen
    from tabellen import koppen_toevoegen
    s = koppen_toevoegen(s, bestand)   # elke tabel een titel per kolom
    from formules import ruimte_tussen_formules
    s = ruimte_tussen_formules(s)   # geen punt tussen twee formules (lijkt op een maalteken)
    from breuken import breuken
    s = breuken(s)   # horizontale breukstreep en brede ruimte tussen formules
    from vectoren import vectortekens
    s = vectortekens(s, bestand)   # vectorteken boven elk krachtsymbool in figuren
    open('/home/claude/toolswetenschappen/' + bestand, 'w', encoding='utf-8').write(voeg_toe(s))

FOOTER = 'Cursus fysica — gemaakt voor klasgebruik, bij de tools op Oefentools wetenschappen.'
STAP = '<div class="stappenplan"><span>1 · gegeven</span><span>2 · gevraagd</span><span>3 · formule</span><span>4 · oplossing</span><span>5 · antwoord met eenheid</span></div>'

