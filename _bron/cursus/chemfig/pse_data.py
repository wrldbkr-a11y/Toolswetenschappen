# volledig PSE: Z, symbool, naam, Ar (None = radioactief, massagetal tussen haakjes), EN (Pauling, 1 decimaal)
R = """1 H waterstof 1.0 2.1|2 He helium 4.0 -|3 Li lithium 6.9 1.0|4 Be beryllium 9.0 1.5|5 B boor 10.8 2.0|6 C koolstof 12.0 2.5|7 N stikstof 14.0 3.0|8 O zuurstof 16.0 3.5|9 F fluor 19.0 4.0|10 Ne neon 20.2 -
11 Na natrium 23.0 0.9|12 Mg magnesium 24.3 1.2|13 Al aluminium 27.0 1.5|14 Si silicium 28.1 1.8|15 P fosfor 31.0 2.1|16 S zwavel 32.1 2.5|17 Cl chloor 35.5 3.0|18 Ar argon 39.9 -
19 K kalium 39.1 0.8|20 Ca calcium 40.1 1.0|21 Sc scandium 45.0 1.3|22 Ti titaan 47.9 1.5|23 V vanadium 50.9 1.6|24 Cr chroom 52.0 1.6|25 Mn mangaan 54.9 1.5|26 Fe ijzer 55.8 1.8|27 Co kobalt 58.9 1.8|28 Ni nikkel 58.7 1.8|29 Cu koper 63.5 1.9|30 Zn zink 65.4 1.6
31 Ga gallium 69.7 1.6|32 Ge germanium 72.6 1.8|33 As arseen 74.9 2.0|34 Se seleen 79.0 2.4|35 Br broom 79.9 2.8|36 Kr krypton 83.8 -
37 Rb rubidium 85.5 0.8|38 Sr strontium 87.6 1.0|39 Y yttrium 88.9 1.2|40 Zr zirkonium 91.2 1.4|41 Nb niobium 92.9 1.6|42 Mo molybdeen 96.0 1.8|43 Tc technetium (98) 1.9|44 Ru ruthenium 101.1 2.2|45 Rh rodium 102.9 2.2|46 Pd palladium 106.4 2.2|47 Ag zilver 107.9 1.9|48 Cd cadmium 112.4 1.7
49 In indium 114.8 1.7|50 Sn tin 118.7 1.8|51 Sb antimoon 121.8 1.9|52 Te telluur 127.6 2.1|53 I jood 126.9 2.5|54 Xe xenon 131.3 -
55 Cs cesium 132.9 0.7|56 Ba barium 137.3 0.9|57 La lanthaan 138.9 1.1|58 Ce cerium 140.1 1.1|59 Pr praseodymium 140.9 1.1|60 Nd neodymium 144.2 1.1|61 Pm promethium (145) 1.1|62 Sm samarium 150.4 1.2|63 Eu europium 152.0 1.2|64 Gd gadolinium 157.3 1.1|65 Tb terbium 158.9 1.2|66 Dy dysprosium 162.5 1.2|67 Ho holmium 164.9 1.2|68 Er erbium 167.3 1.2|69 Tm thulium 168.9 1.2|70 Yb ytterbium 173.0 1.1|71 Lu lutetium 175.0 1.2
72 Hf hafnium 178.5 1.3|73 Ta tantaal 180.9 1.5|74 W wolfraam 183.8 1.7|75 Re renium 186.2 1.9|76 Os osmium 190.2 2.2|77 Ir iridium 192.2 2.2|78 Pt platina 195.1 2.2|79 Au goud 197.0 2.4|80 Hg kwik 200.6 1.9|81 Tl thallium 204.4 1.8|82 Pb lood 207.2 1.8|83 Bi bismut 209.0 1.9|84 Po polonium (209) 2.0|85 At astaat (210) 2.2|86 Rn radon (222) -
87 Fr francium (223) 0.7|88 Ra radium (226) 0.9|89 Ac actinium (227) 1.1|90 Th thorium 232.0 1.3|91 Pa protactinium 231.0 1.5|92 U uraan 238.0 1.7|93 Np neptunium (237) 1.3|94 Pu plutonium (244) 1.3|95 Am americium (243) 1.3|96 Cm curium (247) 1.3|97 Bk berkelium (247) 1.3|98 Cf californium (251) 1.3|99 Es einsteinium (252) 1.3|100 Fm fermium (257) 1.3|101 Md mendelevium (258) 1.3|102 No nobelium (259) 1.3|103 Lr lawrencium (262) -
104 Rf rutherfordium (267) -|105 Db dubnium (268) -|106 Sg seaborgium (269) -|107 Bh bohrium (270) -|108 Hs hassium (277) -|109 Mt meitnerium (278) -|110 Ds darmstadtium (281) -|111 Rg roentgenium (282) -|112 Cn copernicium (285) -|113 Nh nihonium (286) -|114 Fl flerovium (289) -|115 Mc moscovium (290) -|116 Lv livermorium (293) -|117 Ts tennessine (294) -|118 Og oganesson (294) -"""
NM = set('H B C N O F Si P S Cl As Se Br Te I At'.split())
EG = set('He Ne Ar Kr Xe Rn Og'.split())
def plaats(z):
    """(periode, groep 1-18) of ('f', rij, kolom) voor lanthaniden/actiniden"""
    if 58 <= z <= 71: return ('f', 0, z - 58)
    if 90 <= z <= 103: return ('f', 1, z - 90)
    grenzen = [(1, 1), (2, 3), (10, 11), (18, 19), (36, 37), (54, 55), (86, 87)]
    starts = [1, 3, 11, 19, 37, 55, 87]
    p = max(i for i, s in enumerate(starts) if z >= s) + 1
    n = z - starts[p - 1]          # positie in de periode
    if p == 1: return (1, 1 if z == 1 else 18)
    if p in (2, 3): return (p, n + 1 if n < 2 else n + 11)
    if p in (4, 5): return (p, n + 1)
    # periode 6/7: 0,1 = groep 1,2; 2 = La/Ac (groep 3); dan 14 f-elementen overslaan
    if n <= 2: return (p, n + 1)
    return (p, n - 14 + 1)
ALLE = []
for tok in R.replace('\n', '|').split('|'):
    z, s, naam, ar, en = tok.split()
    z = int(z)
    ALLE.append(dict(Z=z, s=s, naam=naam, ar=ar, en=None if en == '-' else float(en),
                     cat='eg' if s in EG else 'nm' if s in NM else 'm', pos=plaats(z)))
assert len(ALLE) == 118 and [e['Z'] for e in ALLE] == list(range(1, 119))
