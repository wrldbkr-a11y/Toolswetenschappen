# Bronbestanden van Oefentools wetenschappen

Deze map bevat de scripts waarmee de cursussen, de remediëring en de Word-versies gemaakt worden. De website zelf (de HTML-bestanden één map hoger) werkt zonder deze map. De map begint met `_`, daardoor toont GitHub Pages ze niet op de site.

## Wat zit waar

| Map | Wat het maakt |
| --- | --- |
| `cursus/` | De cursushoofdstukken (`cursus-*.html`). Eén script per vak of thema, bv. `chemie_cursus.py`, `bio2_cursus.py`, `vierde_cursus.py`. `bouw.py` en `sjabloon.html` zijn de gemeenschappelijke bouwstenen. `chemfig/` en `biofig/` bevatten figuren die uit de tools gehaald zijn. |
| `remediering/` | `remediering.html`. `vragen.py` bevat de DOK-vragen, `vaktaal.json` de woordenlijsten, `bouw_rem.py` bouwt de pagina. |
| `word/` | De Word-versies van de cursussen. `extract.js` leest de cursuspagina's, `maak_docx.js` maakt het .docx-bestand, `toc_bijwerken.py` vult de inhoudstafel in. `bouw_word.sh` maakt alle vijf de cursussen opnieuw. |
| `blad3d/` | Het 3D-blad in `biologie-prikkels.html`. |
| `ppt/`, `wv/` | De PowerPoints en de werkvormenbundel. |
| `bio/`, `w5/`, `work/`, `bord/`, `ev/` | Oudere bouwscripts en figuren van tools. |

## Opnieuw bouwen

De scripts verwachten deze mappen naast elkaar in `/home/claude/`:

```
/home/claude/toolswetenschappen   (deze repo)
/home/claude/cursus               (kopie van _bron/cursus)
/home/claude/remediering          (kopie van _bron/remediering)
/home/claude/word                 (kopie van _bron/word)
```

Nodig: Python 3, Node.js met de pakketten `docx` en `playwright`.

1. Een hoofdstuk aanpassen: wijzig het script in `cursus/` en voer het uit, bv. `python3 chemie_cursus.py`. Het schrijft de HTML rechtstreeks in de repo.
2. Remediëring bijwerken (haalt titels en doelen uit de cursus): `cd remediering && python3 bouw_rem.py`.
3. Word-versies: `bash word/bouw_word.sh`.
4. Publiceren: `git add -A && git commit && git push` in de repo.

Een nieuwe sessie met Claude kan dit opnieuw opzetten: vraag om de repo te klonen en de mappen uit `_bron` naar `/home/claude/` te kopiëren.

## 3de jaar, andere richtingen (leerplan II-Nat'-d)

- `aso/bouw_3aso.py` maakt de fysicatools `*-3aso.html` uit de 3NW-tools. Pas altijd de 3NW-tool aan en draai daarna dit script opnieuw.
- `chemie3/` bevat de lessites ionvorming, samenstelling en reactie: `python3 _bron/chemie3/ionvorming.py` (en `samenstelling.py`, `reactie.py`). Ze gebruiken de stijl van chemie-pse.html (`kop.html`, `helpers.js`).
- `bio3/` bevat de lessites klieren en zenuwstelsel: `python3 _bron/bio3/klieren.py` en `zenuwstelsel.py`. De afbeeldingen in `bio3/img` komen van Wikimedia Commons, met de Engelse namen weggehaald. De bronnen en licenties staan onderaan elke lessite. `organisch.js` tekent de eigen figuren.

## Afvinkbare lesdoelen (`_bron/vinkjes.py`)
Elke lijst `.doel ul > li` (lessites) of `ul.doelen > li` (cursussen, 3ASO-fysica) krijgt een vierkantje met een klikbaar vinkje. De vinkjes worden per pagina in de browser bewaard. De bouwscripts (`chemie3/bouw.py`, `cursus/bouw.py`, `aso/bouw_3aso.py`) voegen dit zelf toe. Pagina's die je met de hand aanpast: draai `python3 _bron/vinkjes.py`.

## Cursus Krachten 3ASO (`_bron/cursus/aso_krachten.py`)
Bouwen: `cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/aso_krachten.py` → `cursus-krachten-3aso.html`.
Hergebruikt effect, vector, traagheid en beweging uit `derde_krachten.py` (3NW; die leest `oud_krachten.py`). Links wijzen naar de 3ASO-tools.
Leerlingen krijgen een ingevulde naslag; wisbordvragen per deel (`aso_wisbord.py`, `aso_veer.py`) staan in `.edi`-blokken die enkel met `?leerkracht` zichtbaar zijn. Word: `EDI=1 node extract.js …` neemt ze mee (leerkrachtversie), zonder EDI niet.
