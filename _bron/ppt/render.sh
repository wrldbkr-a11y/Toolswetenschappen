#!/bin/bash
# $1 = pptx basename zonder extensie, $2 = prefix
S=/root/.claude/skills/synced/1fe33a63-f4ea-4cfc-950e-0e79e049737b_a8573341-fcc3-4e00-a94c-615572386dea/pptx/scripts
python3 $S/office/validate.py $1.pptx && python3 $S/office/soffice.py --headless --convert-to pdf $1.pptx >/dev/null 2>&1
rm -f slide-*.jpg; pdftoppm -jpeg -r 50 $1.pdf slide
python3 -c "
from PIL import Image;import glob
fs=sorted(glob.glob('slide-*.jpg'));ims=[Image.open(f) for f in fs];w,h=ims[0].size
for g in range(0,len(ims),6):
  c=Image.new('RGB',(2*w,3*h),'white')
  for i,im in enumerate(ims[g:g+6]):c.paste(im,((i%2)*w,(i//2)*h))
  c.save(f'$2{g//6}.jpg',quality=80)
print(len(fs))"
