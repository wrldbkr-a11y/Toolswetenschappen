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

## Lesdoelen NW-tools (afvinkbaar)
- `_bron/lesdoelen/overzicht.py` leest de leerstofoverzichten (.docx) naar `nw_overzichten.json`.
- `_bron/lesdoelen/nw_lesdoelen.py` zet per tool een dicht paneel (`<!--ldnw-->…<!--/ldnw-->`) met de lesdoelen; de koppeling tool → paragrafen staat in `KAART`.
- `aso/bouw_3aso.py` haalt dit blok weg, zodat de 3ASO-versies alleen hun eigen lesdoelen tonen. Volgorde: eerst `nw_lesdoelen.py`, dan `bouw_3aso.py`.

## Cursus biologie 3de jaar (thema 1–3) in het nieuwe formaat
- `cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/bio3_nieuw.py`
- Bestaande inhoud en figuren uit `bio_cursus.py` en `bio2_cursus.py`; nieuwe inhoud (idee, uitgewerkt voorbeeld, Let op, Test jezelf, wisbordvragen, uitdagingen, begrippen) in `bio3_inhoud.py`.
- Word: `Cursus_Biologie_3.docx` (leerling, zonder bijlage) en `Cursus_Biologie_3_leerkracht.docx` (EDI=1), zie `_bron/word/bouw_word.sh`.

## Cursus chemie 3de jaar (thema 1–2) in het nieuwe formaat
- `cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/chemie3_nieuw.py`
- Gedeelde bouwstenen voor bio en chemie: `_bron/cursus/nieuw_formaat.py`. Nieuwe inhoud: `chemie3_inhoud.py`.
- Word: `Cursus_Chemie_3.docx` (leerling, zonder bijlage) en `Cursus_Chemie_3_leerkracht.docx`.

## Cursus snelheid 3ASO (thema 2, hoofdstuk 1–2)
- `cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/snelheid_3aso.py` → `cursus-snelheid-3aso.html`
- Volledig nieuw geschreven (figuren, inhoud en oefeningen in één bestand); gebruikt `nieuw_formaat.py`.
- Word: `Cursus_Snelheid_3ASO.docx` en `Cursus_Snelheid_3ASO_leerkracht.docx`.

## Cursussen 3NW (optica + krachten) in het nieuwe formaat
- `cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/nw3_nieuw.py`
- Leest `optica_cursus.py` (de oude maak()-aanroepen worden opgevangen) en `derde_krachten.py` (tot `delen = [`); nieuwe inhoud in `nw3_inhoud.py`.
- Stappenplannen (`<h3>Stappenplan: …</h3><ol>`) worden automatisch kaders "Denkstappen · …"; nieuwe denkstappen en geheugensteunen via `stappen=` en `steun=` in `D(...)`.
- Word: `Cursus_Fysica_3NW.docx` (zonder bijlage) en `Cursus_Fysica_3NW_leerkracht.docx`.

## Cursus 3NW deel 2: zwaartekracht, wrijving en veerkracht (thema 2, hoofdstuk 1, 3, 5, 6)
- `cd /home/claude/cursus && python3 /home/claude/toolswetenschappen/_bron/cursus/nw3_krachten2.py` → `cursus-zwaartekracht-wrijving-veer.html`
- Hergebruikt figuren en oefeningen uit de 3ASO-cursus (aso_krachten.py tot aso_extra), links naar de NW-tools; wrijving is nieuw.
- Word: `Cursus_Fysica_3NW_deel2.docx` en `..._leerkracht.docx`.

## Afspraken in vragen en tekeningen (automatisch)
- `_bron/cursus/namen.py`: in vragen (opgaven, denkvragen, Test jezelf, wisbordvragen) staan volledige namen, geen symbolen ("Bereken de veerconstante", niet "Bereken k"). bouw.py past dit toe bij het bouwen. Per soort pagina een eigen woordenlijst (bv. g = grenshoek in optica, zwaarteveldsterkte bij krachten).
- Vectorpijlen hebben een dunne lijn (pijl() in derde_krachten.py en vierde_cursus.py: lijndikte b × 0,5; ac_help/ladingen: 1,8).
- Krachten in tekenoefeningen zijn minstens 3 hokjes lang (kies de schaal zo).

## Oefening "Van pijlen naar zinnen"
- `_bron/cursus/zinnen_inhoud.py`: per cursuspagina twee redeneringen met pijlen + modelantwoord, en het kader met verbindingswoorden (VERBIND).
- nieuw_formaat.pagina() voegt de oefening toe vóór de uitdagingen (kader alleen op de eerste pagina van een reeks; anders een korte geheugensteun). aso_krachten.py en snelheid_3aso.py doen het zelf.

## 4NW en 5Wet in het nieuwe formaat
- `nw4_nieuw.py` + `nw4_inhoud.py`: druk (H1-H4) en energie/vermogen. Vangt de oude inhoud op uit `druk_vast.py` (vroeger in bouw.py) en `vierde_cursus.py`.
- `nw5_nieuw.py` + `nw5_inhoud.py`: ladingen, coulomb, elektrisch veld, potentiaal (sjabloon_ac, met nummering) en gemengde schakelingen.
- Tekenoefeningen op ruitjes (2 per hoofdstuk) staan in de builders. `pagina(..., nrs=[...])` zet eigen deelnummers (bv. 1.1).
- bouw.py is nu een pure bibliotheek: importeren bouwt geen pagina meer.

## Formules en vectortekens (nabewerking in bouw.py)
- `breuken.py`: symbolische formules met / krijgen een horizontale breukstreep (span.fr); formules naast elkaar een brede tussenruimte. Rekenwerk met getallen blijft gewoon.
- `formules.py`: "·" is alleen een scheiding tussen formules bij &nbsp;, een breuk erna of een getal ervoor (niet in een rekenketen).
- `vectoren.py`: vectorteken boven F…/E…-labels in figuren (niet in grafieken en optica); pijlen met marker dunner.
- Word: extract.js geeft breuken door als {frac}; maak_docx.js maakt er OMML-breuken van (recht, via toc_bijwerken.py). Brede spaties blijven bewaard.

## Advance organizers (overzicht van het jaar)
- `_bron/organizer/organizer_inhoud.py`: per vak en jaar de thema's (grote vraag, idee, je kent al) en hoofdstukken (examen dec/jun, link naar de cursus). Bron: leerstofoverzichten.
- `_bron/organizer/bouw_organizer.py` maakt `overzicht-<vak>-<klas>.html` (iconen uit index.html). Tegels op de startpagina; elke cursuspagina linkt bovenaan naar haar overzicht (bouw.py, overzicht_link).
- Een nieuwe cursuspagina? Zet de link bij het hoofdstuk in organizer_inhoud.py en bouw opnieuw.

- Word-versie van de overzichten: `_bron/word/maak_org.js` (leest org.json + iconen-PNG uit /home/claude/word/org).
