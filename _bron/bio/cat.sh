#!/bin/bash
UA="ToolswetenschappenBot/1.0 (https://github.com/wrldbkr-a11y/Toolswetenschappen; educational)"
c=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1].replace(' ','_')))" "$1")
curl -sS -A "$UA" "https://commons.wikimedia.org/wiki/Category:$c" | grep -o 'href="/wiki/\(File\|Category\):[^"#]*"' | sed 's/href="\/wiki\///;s/"$//' | python3 -c "import sys,urllib.parse;[print(urllib.parse.unquote(l.strip())) for l in sys.stdin]" | sort -u
