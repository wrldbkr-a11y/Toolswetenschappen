"""Vult de inhoudstafel van .docx-bestanden (gemaakt met docx-js) in met de juiste paginanummers.
Werkwijze: koppen uit het document halen, inhoudstafel invullen, met LibreOffice naar pdf omzetten, de pagina van elke kop
opzoeken, opnieuw invullen ... tot de nummers niet meer veranderen. Het veld blijft een echte inhoudstafel.
Gebruik: python3 toc_bijwerken.py bestand1.docx [bestand2.docx ...]"""
import sys, os, re, subprocess, tempfile, zipfile, html, shutil

def lees(pad):
    return zipfile.ZipFile(pad).read('word/document.xml').decode('utf-8')

def koppen(xml):
    m = re.search(r'TOC \\h \\o &quot;1-(\d)&quot;', xml) or re.search(r'TOC[^<]*\\o &quot;1-(\d)&quot;', xml)
    maxlv = int(m.group(1)) if m else 2
    uit = []
    for p in re.finditer(r'<w:p>(?:(?!</w:p>).)*?</w:p>', xml, re.S):
        s = p.group(0)
        h = re.search(r'<w:pStyle w:val="Heading(\d)"/>', s)
        if h and int(h.group(1)) <= maxlv:
            tekst = html.unescape(''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', s))).strip()
            if tekst: uit.append([int(h.group(1)), tekst, '0'])
    return uit

def invullen(pad, entries):
    tmp = pad + '.tmp'
    with zipfile.ZipFile(pad) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zuit:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'word/document.xml':
                s = data.decode('utf-8')
                par = ''.join(
                    f'<w:p data-toc="1"><w:pPr><w:pStyle w:val="TOC{lv}"/><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9020"/></w:tabs>'
                    f'<w:spacing w:before="{80 if lv == 1 else 0}" w:after="20"/><w:ind w:left="{(lv - 1) * 360}"/></w:pPr>'
                    f'<w:r>{"<w:rPr><w:b/></w:rPr>" if lv == 1 else ""}<w:t xml:space="preserve">{html.escape(t)}</w:t></w:r>'
                    f'<w:r>{"<w:rPr><w:b/></w:rPr>" if lv == 1 else ""}<w:tab/><w:t>{p}</w:t></w:r></w:p>' for lv, t, p in entries).replace(' data-toc="1"', '')
                i = s.find('<w:instrText xml:space="preserve">TOC'); assert i > 0, 'geen inhoudstafel'
                sep = s.find('<w:fldChar w:fldCharType="separate"/></w:r></w:p>', i); assert sep > 0
                sep_end = sep + len('<w:fldChar w:fldCharType="separate"/></w:r></w:p>')
                end = s.find('<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>', sep_end); assert end > 0
                s = s[:sep_end] + par + s[end:]
                data = s.encode('utf-8')
            zuit.writestr(item, data)
    os.replace(tmp, pad)

def norm(x):
    return re.sub(r'\s+', ' ', x).strip()

def paginas(pad, entries):
    tmp = tempfile.mkdtemp()
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp, pad], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    pdf = os.path.join(tmp, os.path.splitext(os.path.basename(pad))[0] + '.pdf')
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    lijnen = []
    for k in range(1, n + 1):
        txt = subprocess.run(['pdftotext', '-f', str(k), '-l', str(k), '-layout', pdf, '-'], capture_output=True, text=True).stdout
        lijnen.append([norm(l) for l in txt.splitlines() if l.strip()])
    shutil.rmtree(tmp)
    # eerste pagina na de inhoudstafel: de pagina waar de eerste kop als losse regel staat zonder puntjes
    start = 0
    res = []
    for lv, t, _ in entries:
        doel = norm(t); gevonden = None
        for k in range(start, n):
            L = lijnen[k]
            if any(l == doel for l in L) or any(norm(L[j] + ' ' + L[j + 1]) == doel or norm(L[j] + L[j + 1]) == doel for j in range(len(L) - 1)):
                gevonden = k; break
        if gevonden is None:
            res.append('?'); continue
        res.append(str(gevonden + 1)); start = gevonden
    return res

def bijwerken(pad):
    entries = koppen(lees(pad))
    vorige = None
    for ronde in range(4):
        invullen(pad, entries)
        p = paginas(pad, entries)
        for e, x in zip(entries, p): e[2] = x
        if p == vorige: break
        vorige = p
    invullen(pad, entries)
    onbekend = sum(1 for e in entries if e[2] == '?')
    print(f'inhoudstafel ingevuld: {os.path.basename(pad)} · {len(entries)} regels · {ronde + 1} rondes' + (f' · {onbekend} niet gevonden' if onbekend else ''))

if __name__ == '__main__':
    for pad in sys.argv[1:]:
        bijwerken(pad)
