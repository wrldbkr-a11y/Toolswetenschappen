#!/bin/bash
# zoek op Commons via Special:Search (HTML) en toon bestandsnamen
UA="ToolswetenschappenBot/1.0 (educational; https://github.com/wrldbkr-a11y)"
q=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$1")
curl -sS -A "$UA" "https://commons.wikimedia.org/w/index.php?search=$q&title=Special:MediaSearch&type=image&limit=40" -o /tmp/s.html
curl -sS -A "$UA" "https://commons.wikimedia.org/w/index.php?search=$q&title=Special:Search&ns6=1&limit=30&fulltext=1" | grep -o 'title="File:[^"]*"' | sort -u | head -30
