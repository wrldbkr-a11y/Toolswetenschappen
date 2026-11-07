"""Leest lesdoelen uit een leerstofoverzicht (.docx) -> nw_overzichten.json.
Gebruik: python3 overzicht.py sleutel=pad.docx ...  (sleutels: 3dec 3jun 4dec 4jun 5dec 5jun)"""
import subprocess, re, sys, json, html as H
from pathlib import Path

def items(path):
    h = subprocess.run(['pandoc', path, '-t', 'html', '--wrap=none'], capture_output=True, text=True).stdout
    h = re.sub(r'<(td|th)[^>]*>', '\n<P>', h); h = re.sub(r'</?(p|li|br)[^>]*>', '\n<P>', h)
    return [t for t in (' '.join(H.unescape(re.sub(r'<[^>]+>', ' ', p)).split()) for p in h.split('<P>')) if t]

def niveau(k):
    """Lager = beter als kop: 1.2 voor 1.2.3; daarna 'N titel', HOOFDSTUK, Hoofdstuk N, Thema."""
    m = re.match(r'^\d+(\.\d+)+', k)
    if m: return m.group(0).count('.')
    if re.match(r'^\d+\.?\s', k): return 5
    if re.match(r'^HOOFDSTUK', k): return 6
    if re.match(r'^Hoofdstuk', k): return 7
    return 8

def parse(path):
    res, koppen, cur = [], [], None
    for t in items(path):
        t2 = re.sub(r'^[☐\-–•\s]+', '', t)
        if re.match(r'^(Ik|Je)\b', t2):
            if koppen:   # eerste doel na nieuwe koppen: kies de hoogste kop (minste punten)
                cur = [min(koppen, key=niveau), []]; res.append(cur); koppen = []
            if cur is None: cur = ['(zonder kop)', []]; res.append(cur)
            rest = re.sub(r'^(Ik|Je)\s+(kan\s+)?', '', t2).lower()
            if not any(re.sub(r'^(Ik|Je)\s+(kan\s+)?', '', d).lower() == rest for d in cur[1]):
                cur[1].append(t2)
        elif re.match(r'^(\d+(\.\d+)*\.?\s+\S|HOOFDSTUK|Hoofdstuk|Thema)', t) and len(t) < 110:
            koppen.append(t)
    return [r for r in res if r[1]]

if __name__ == '__main__':
    uit = Path(__file__).with_name('nw_overzichten.json')
    data = json.loads(uit.read_text(encoding='utf-8')) if uit.exists() else {}
    for a in sys.argv[1:]:
        k, p = a.split('=', 1); data[k] = parse(p)
    uit.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
