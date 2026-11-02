import json, re, math
D = json.load(open('/home/claude/cursus/biofig/bio.json'))
def _w(s, w=640):
    s = re.sub(r'<svg ([^>]*?)style="[^"]*"', r'<svg \1', s, count=1)
    return s.replace('<svg ', f'<svg width="{w}" ', 1)
def lab(k, w=640): return _w(D[k], w)
def namen(k):
    return [n for i, n in sorted((int(i), n) for i, n in re.findall(r'<text[^>]*data-i="(\d+)"[^>]*>([^<]*)</text>', D[k]))]
def num(k, w=640):
    s = D[k]
    def f(m):
        tag, i = m.group(0), int(m.group(1))
        x = float(re.search(r' x="([-\d.]+)"', tag).group(1)); y = float(re.search(r' y="([-\d.]+)"', tag).group(1))
        end = 'text-anchor="end"' in tag
        cx = x - 16 if end else x + 16
        return (f'<circle cx="{cx}" cy="{y-7}" r="16" fill="#fff" stroke="#1D2A36" stroke-width="2.5"/>'
                f'<text x="{cx}" y="{y-1}" text-anchor="middle" font-size="19" font-weight="700" fill="#1D2A36" font-family="Inter, sans-serif">{i+1}</text>')
    s = re.sub(r'<text[^>]*data-i="(\d+)"[^>]*>[^<]*</text>', f, s)
    return _w(s, w)
def plat(k, w=640): return _w(D[k], w)
