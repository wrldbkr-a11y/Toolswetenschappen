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
