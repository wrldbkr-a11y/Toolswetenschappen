// Fysica 4de en 5de jaar + algemeen
module.exports = [
{ tool: 'Druk', bestand: 'druk.html', jaar: '4de jaar', items: [
 { t: 'Druk bij vaste stoffen', doel: 'Druk definiëren, p = F/A gebruiken en omvormen, drukverhogende en drukverlagende toepassingen verklaren.', w: [
  ['Bakstenen in zand of plasticine', '15 min', 'G', 'baksteen of houten blok, bak met zand of plasticine, lat', [
   'Groepjes leggen het blok plat, op de zijkant en rechtop en meten de indrukking.',
   'Ze berekenen telkens p = F/A en zetten de resultaten in een tabel.',
   'Ze vergelijken met de tool en formuleren het verband tussen A en p.']],
  ['Toepassingen sorteren', '10 min', 'D', 'foto’s: mes, punaise, sneeuwschoen, rupsband, naaldhak, ski', [
   'Duo’s sorteren in drukverhogend en drukverlagend en schrijven telkens: "… is …, want de oppervlakte is …".']] ] },
 { t: 'Redeneren met druk', doel: 'Beredeneren wat er met de druk gebeurt als F en/of A met een factor veranderen.', w: [
  ['Kaartenspel: wat gebeurt er met p?', '10 min', 'D', 'kaarten met "F × 2", "A ÷ 3" …', [
   'A trekt een kaart voor F en een voor A. B voorspelt wat er met p gebeurt.',
   'Ze controleren met de redeneertool in de tool en wisselen.']] ] },
 { t: 'Gasdruk, luchtdruk, overdruk en onderdruk', doel: 'Gasdruk verklaren met botsende deeltjes; luchtdruk, overdruk en onderdruk uitleggen; druk en kracht correct onderscheiden.', w: [
  ['Proefjes met luchtdruk', '20 min', 'G', 'glas met kaartje, zuignap, rietje, spuit, plastic fles met warm water', [
   'Groepjes doen drie proefjes: het kaartje onder het omgekeerde glas, de zuignap, een fles met warm water die afkoelt en indeukt.',
   'Ze verklaren met de juiste woorden: "De lucht oefent een kracht uit …", niet "de luchtdruk duwt".',
   'Ze vergelijken met de kaarten in de tool.']],
  ['Deeltjesrollenspel', '10 min', 'K', 'afgebakende ruimte op de speelplaats', [
   'Leerlingen zijn gasdeeltjes en lopen kriskras in een afgebakend vak. Ze tikken de grens aan bij elke "botsing".',
   'Maak het vak kleiner of laat ze sneller lopen (warmer): wat gebeurt er met het aantal botsingen?']] ] },
 { t: 'Hydrostatische druk', doel: 'p = ρ · g · h toepassen en uitleggen dat de druk niet van de vorm van het vat afhangt.', w: [
  ['Fles met gaatjes', '10 min', 'G', 'plastic fles met drie gaatjes boven elkaar, plakband, bak', [
   'Groepjes vullen de fles, trekken de plakband weg en kijken hoe ver de straaltjes spuiten.',
   'Ze verklaren met de diepte h en controleren met de druksonde in de tool.']],
  ['Vormen van vaten', '10 min', 'D', 'tool, deel "Vorm van het vat"', [
   'Duo’s voorspellen eerst in welk vat de druk op de bodem het grootst is.',
   'Ze controleren in de tool en schrijven de conclusie in één zin.']] ] },
 { t: 'Beginsel van Pascal en hydraulica', doel: 'Het beginsel van Pascal uitleggen en toepassen bij een hydraulisch systeem.', w: [
  ['Spuitjes-hydraulica', '20 min', 'G', 'twee spuiten van verschillende diameter, slangetje, water', [
   'Groepjes verbinden de spuiten en duwen op de kleine en de grote zuiger.',
   'Ze voelen het verschil in kracht en meten hoe ver elke zuiger beweegt.',
   'Ze rekenen na met F₁/A₁ = F₂/A₂ in de tool.']] ] },
 { t: 'Archimedeskracht in vloeistoffen en gassen', doel: 'De oorsprong van de archimedeskracht verklaren; zinken, zweven, stijgen en drijven voorspellen; toepassen bij de vis en de heteluchtballon.', w: [
  ['Wegen in lucht en in water', '20 min', 'G', 'dynamometer, steen of metalen blokje, maatbeker met water', [
   'Groepjes wegen het blokje in lucht en ondergedompeld en berekenen F_A.',
   'Ze meten het verplaatste volume en berekenen ρ · g · V. Komt het overeen?']],
  ['Cartesiaans duikertje', '15 min', 'G', 'plastic fles, pipet of ketchupzakje, water', [
   'Groepjes maken een duikertje dat zweeft. Als ze in de fles knijpen, zakt het.',
   'Ze verklaren met het volume van de luchtbel en F_A, en vergelijken met de zwemblaas van de vis in de tool.']],
  ['Expertgroepen met PhET Buoyancy', '30 min', 'G', 'laptops of tablets, PhET-simulatie Buoyancy (phet.colorado.edu/nl/simulations/buoyancy)', [
   'Vier expertgroepen onderzoeken elk één factor in de simulatie, met de krachten en hun waarde zichtbaar: A de massadichtheid van de vloeistof, B het ondergedompelde volume, C de zwaarteveldsterkte, D de massa van het voorwerp en de diepte.',
   'Ze veranderen telkens enkel hun factor, noteren de metingen in een tabel en kijken of F_A recht evenredig is (factor × 2 → F_A × 2?).',
   'In thuisgroepen met één expert van elke groep legt elke expert zijn besluit uit met zijn tabel.',
   'Samen stellen ze F_A = ρ_vl · g · V_ond op en besluiten ze wat géén invloed heeft (massa van het voorwerp, diepte eenmaal volledig ondergedompeld).',
   'Uitbreiding: ze vergelijken ρ_voorwerp met ρ_vloeistof en voorspellen of een blok zinkt, zweeft of drijft voor ze het loslaten.']] ] },
]},
{ tool: 'Energie, vermogen en rendement', bestand: 'energie-vermogen.html', jaar: '4de jaar', items: [
 { t: 'Open, gesloten en geïsoleerd systeem', doel: 'Open, gesloten en geïsoleerde systemen herkennen aan de uitwisseling van energie en materie.', w: [
  ['Drie potjes', '10 min', 'G', 'potje zonder deksel, potje met deksel, thermosfles, warm water, thermometer', [
   'Groepjes vullen de drie met warm water en meten na 10 minuten de temperatuur en de hoeveelheid water.',
   'Ze vullen de tabel in: energie uitgewisseld? materie uitgewisseld?']],
  ['Systeemkaarten', '10 min', 'D', 'kaarten met voorbeelden (mens, kampvuur, frisdrankblikje, aarde)', [
   'Duo’s sorteren en verantwoorden. Daarna oefenen ze in de tool.']] ] },
 { t: 'Vormen van energie en energieomzettingen', doel: 'Energievormen benoemen en energieomzettingen beschrijven in een energieketen.', w: [
  ['Energieketen met voorwerpen', '15 min', 'G', 'zaklamp, opwindspeeltje, dynamo-lamp, zonnecel met motortje', [
   'Groepjes zoeken voor elk toestel de energieomzetting en tekenen de keten met pijlen.',
   'Ze duiden de nuttige en de niet-nuttige energie aan.']],
  ['Potentiële energie: het waterreservoir', '10 min', 'D', 'tool, deel "Waterreservoir op een heuvel"', [
   'Duo’s voorspellen wat er gebeurt met E_pot en E_kin als het water naar beneden stroomt.',
   'Ze controleren in de tool.']] ] },
 { t: 'Vermogen', doel: 'Vermogen definiëren en berekenen met P = E/t of P = W/t.', w: [
  ['De trap op', '20 min', 'G', 'trap, meetlint, chronometer, weegschaal of gekende massa', [
   'Leerlingen lopen de trap op, eerst rustig, dan snel. De groep meet de tijd en de hoogte.',
   'Ze berekenen m · g · h en het vermogen in watt.',
   'Vergelijk met toestellen in de tool: hoeveel lampen kan je laten branden?']],
  ['Typeplaatjes lezen', '10 min', 'D', 'foto’s van typeplaatjes (waterkoker, föhn, gsm-lader)', [
   'Duo’s zoeken het vermogen en berekenen de energie voor 5 minuten gebruik.']] ] },
 { t: 'Rendement', doel: 'Rendement berekenen en het energiestroomdiagram tekenen.', w: [
  ['Lampen vergelijken', '15 min', 'G', 'gloeilamp en ledlamp met hetzelfde licht, thermometer of hand op afstand', [
   'Groepjes voelen de warmte van beide lampen.',
   'Ze tekenen voor elke lamp een energiestroomdiagram en berekenen het rendement met de gegevens uit de tool.']] ] },
]},
{ tool: 'Ladingen en elektrostatica', bestand: 'ladingen.html', jaar: '5de jaar', items: [
 { t: 'Elementaire lading, geleiders en isolatoren, aarding', doel: 'Verklaren waarom een voorwerp geladen is; geleiders en isolatoren onderscheiden; aarding uitleggen.', w: [
  ['Ballon en waterstraal', '10 min', 'D', 'ballon, wollen trui, kraan met dun straaltje', [
   'Duo’s wrijven de ballon en houden hem bij de waterstraal.',
   'Ze verklaren met elektronen en tekenen de ladingen.']],
  ['Geleider of isolator testen', '15 min', 'G', 'batterij, lampje, draadjes, voorwerpen (sleutel, potlood, gom, aluminiumfolie)', [
   'Groepjes testen welke voorwerpen het lampje doen branden.',
   'Ze verbinden met vrije elektronen en met de animatie in de tool.']] ] },
 { t: 'Laden door wrijving, contact en influentie; polarisatie', doel: 'Laden door wrijving, contact en influentie uitleggen en tekenen; de tribo-elektrische reeks toepassen; polarisatie uitleggen.', w: [
  ['Tribo-elektrische reeks testen', '20 min', 'G', 'staven van PVC en glas, wol, zijde, papiersnippers, een opgehangen geladen staaf', [
   'Groepjes wrijven telkens twee materialen en testen of de staaf de opgehangen staaf aantrekt of afstoot.',
   'Ze bepalen welke stof positief en welke negatief wordt en vergelijken met de reeks in de tool.']],
  ['Papiersnippers en polarisatie', '10 min', 'D', 'geladen ballon of staaf, papiersnippers', [
   'Duo’s laten de snippers aantrekken. Ze tekenen de verschoven ladingen in één snipper.',
   'Vergelijk met "Influentie en polarisatie" in de tool.']] ] },
 { t: 'Toepassingen: bliksem, kopieerapparaat, swiffer', doel: 'De bliksem, het kopieerapparaat en een swifferdoekje uitleggen met de juiste terminologie.', w: [
  ['Expertgroepen', '25 min', 'G', 'tool, drie toepassingen', [
   'Elke leerling in een groepje kiest één toepassing en werkt die uit met de tool.',
   'Daarna legt elke expert zijn toepassing uit aan de groep met een tekening.']] ] },
 { t: 'Elektroscoop en bollen (elektrostatische inductie)', doel: 'De ladingsverdeling op een elektroscoop en op bollen voorspellen bij laden door contact en influentie.', w: [
  ['Echte elektroscoop', '15 min', 'G', 'elektroscoop, geladen staaf', [
   'Groepjes laden de elektroscoop door contact en door influentie met aarding.',
   'Ze tekenen telkens de ladingen en vergelijken met de tool "Elektrostatische inductie".']] ] },
]},
{ tool: 'Krachten op ladingen', bestand: 'krachten-op-ladingen.html', jaar: '5de jaar', items: [
 { t: 'Coulombkracht tussen twee en meerdere ladingen', doel: 'Richting, zin en grootte van de coulombkracht bepalen bij twee ladingen, ladingen op één lijn en in een driehoek; de formule omvormen.', w: [
  ['Redeneerkaarten', '15 min', 'D', 'kaarten: "Q₁ × 2", "r × 3" …', [
   'A trekt een kaart, B voorspelt hoe de kracht verandert en legt uit met de formule.',
   'Ze controleren met de oefening "vergelijken" in de tool.']],
  ['Krachten tekenen op de lijn', '15 min', 'I → D', 'werkblad met drie ladingen op een lijn', [
   'Leerlingen tekenen de krachten op de middelste lading en bepalen F_r.',
   'In duo vergelijken ze en controleren met de stappen in de tool.']] ] },
]},
{ tool: 'Elektrisch veld', bestand: 'elektrisch-veld.html', jaar: '5de jaar', items: [
 { t: 'Veldsterkte en veldvector', doel: 'De veldvector tekenen bij een positieve en negatieve bronlading; E = F/q en E = k·Q/r² gebruiken; verwarring met de coulombkracht vermijden.', w: [
  ['Analogie met het zwaarteveld', '10 min', 'D', 'tool, tabbladen "Zwaartekracht" en "Bron- en proeflading"', [
   'Duo’s vullen een tabel in: g en E, m en q, F_z en F.',
   'Ze leggen uit waarom E niet afhangt van de proeflading.']] ] },
 { t: 'Veldlijnen bij één en meerdere ladingen', doel: 'De kenmerken van veldlijnen toepassen; veldlijnen tekenen bij één of meerdere puntladingen.', w: [
  ['Griesmeel in olie (demo)', '10 min', 'K', 'petrischaal met olie en griesmeel, twee elektroden, hoogspanningsbron of geladen staafjes', [
   'Toon hoe de korreltjes zich langs de veldlijnen richten bij één en twee ladingen.',
   'Leerlingen vergelijken met de 2D- en 3D-weergave in de tool.']],
  ['Veldlijnen schetsen en controleren', '15 min', 'D', 'werkblad, tool "Meerdere ladingen"', [
   'Duo’s schetsen de veldlijnen voor twee positieve ladingen en voor + en −.',
   'Ze controleren in de tool en duiden de kenmerken aan die ze gebruikten.']] ] },
 { t: 'Geleidende bol, homogeen veld en kooi van Faraday', doel: 'Het veld bij een geleidende bol en tussen platen tekenen; de grafieken van E(r) tekenen; de kooi van Faraday uitleggen.', w: [
  ['Gsm in aluminiumfolie', '10 min', 'G', 'gsm, aluminiumfolie, metalen trommel', [
   'Groepjes wikkelen een gsm in folie en bellen ernaar. Werkt het nog?',
   'Ze verklaren met de kooi van Faraday en zoeken twee voorbeelden uit het dagelijks leven.']],
  ['Grafiek-matching', '10 min', 'D', 'kaarten met situaties en grafieken E(r)', [
   'Duo’s koppelen elke situatie (puntlading, bol binnen/buiten, platen) aan de juiste grafiek.',
   'Controle met de grafieken in de tool.']] ] },
 { t: 'Potentiële energie, potentiaal en spanning', doel: 'E_pot = Q·E·d en V = E·d berekenen; equipotentiaalvlakken tekenen; het verband met ΔE_kin en de eenheid elektronvolt uitleggen.', w: [
  ['Analogie met de knikkerbaan', '15 min', 'D', 'tool, tab "Energie en potentiaal"; schets van een knikkerbaan', [
   'Duo’s vergelijken m·g·h met Q·E·d in een tabel.',
   'Ze laten in de tool een proton en een elektron los en verklaren de richting.',
   'Ze berekenen de eindsnelheid en ΔE_kin in eV.']] ] },
]},
{ tool: 'Gemengde schakelingen', bestand: 'schakelingen.html', jaar: '5de jaar', items: [
 { t: 'Wet van Ohm', doel: 'De wet van Ohm gebruiken en de U(I)-grafiek interpreteren.', w: [
  ['Meten aan een weerstand', '20 min', 'G', 'spanningsbron, weerstanden (100 Ω, 220 Ω), multimeters', [
   'Groepjes meten I bij vijf spanningen en tekenen de U(I)-grafiek.',
   'Ze bepalen R uit de richtingscoëfficiënt en vergelijken met de tool.']] ] },
 { t: 'Serie, parallel en gemengde schakelingen', doel: 'De substitutieweerstand en de stroom- en spanningsverdeling bepalen in serie-, parallel- en gemengde schakelingen.', w: [
  ['Lampjes-puzzel', '20 min', 'G', 'batterij, drie gelijke lampjes, draadjes', [
   'Groepjes bouwen serie, parallel en een gemengde schakeling en vergelijken de helderheid.',
   'Ze voorspellen eerst en verklaren daarna met U en I.']],
  ['Stappenplan als tweetal', '15 min', 'D', 'opgave, tool "Gemengde schakeling stap voor stap"', [
   'A vervangt één deel door een substitutieweerstand, B controleert. Ze wisselen bij elke stap.',
   'Daarna verdelen ze U en I terug en controleren met de tool.']] ] },
]},
{ tool: 'Formules omvormen', bestand: 'formuleredeneertool.html', jaar: '3de tot 5de jaar', items: [
 { t: 'Inzicht, berekenen, twee toestanden, omvormen, eenheden', doel: 'Redeneren met formules, formules omvormen en eenheden omzetten naar SI.', w: [
  ['Formuledriehoek of balans', '10 min', 'I → D', 'kaartjes met formules', [
   'Leerlingen vormen een formule om met de "balans": wat aan de ene kant gebeurt, gebeurt ook aan de andere kant.',
   'Ze controleren in de tool, deel Omvormen.']],
  ['Twee toestanden voorspellen', '10 min', 'D', 'tool, deel "Twee toestanden"', [
   'A verandert één grootheid, B voorspelt het effect op de andere. Ze wisselen na drie vragen.']] ] },
]},
];
