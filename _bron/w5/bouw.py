import sys,re,json
def bouw(uit,titel,intro,cats,html,js,extra_css=''):
    css=open('/home/claude/w5/base.css').read()
    nav=open('/home/claude/w5/nav.js').read()
    nav=re.sub(r"const categories=\[.*?\];","const categories="+json.dumps([{'id':a,'label':b} for a,b in cats],ensure_ascii=False)+";",nav,flags=re.S)
    helpers=open('/home/claude/w5/helpers.js').read()
    doc=f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titel}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
{css}
{extra_css}
</style>
</head>
<body>

<header class="top">
  <h1>{titel}</h1>
  <p class="intro">{intro}</p>
  <nav id="catnav" class="catnav"></nav>
  <nav id="nav"></nav>
</header>

<main>
{html}
</main>

<script>
{nav}
{helpers}
{js}
</script>
</body>
</html>
'''
    open(uit,'w').write(doc)
