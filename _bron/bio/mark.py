import sys,json
from PIL import Image,ImageDraw,ImageFont
img,pts,out=sys.argv[1],json.loads(sys.argv[2]),sys.argv[3]
im=Image.open(img).convert('RGB'); d=ImageDraw.Draw(im)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',16)
for k,(x,y) in pts.items():
    d.ellipse((x-6,y-6,x+6,y+6),outline='black',width=3,fill='yellow'); d.text((x+8,y-8),k,fill='black',font=f,stroke_width=2,stroke_fill='white')
im.save(out)
