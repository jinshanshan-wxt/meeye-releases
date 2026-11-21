import sys, os
from PIL import Image
_HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.environ.get('MEEYE_ROOT', os.path.abspath(os.path.join(_HERE,'..','..')))
names=sys.argv[2:]; out=sys.argv[1]
cols=6; W=2
rows=(len(names)+cols-1)//cols
s=Image.new('RGBA',(cols*(192*W+8)+8,rows*(192*W+8)+8),(128,128,128,255))
for i,n in enumerate(names):
    im=Image.open(os.path.join(ROOT,'icons',f'{n}.png')).convert('RGBA').resize((192*W,192*W),Image.LANCZOS)
    s.alpha_composite(im,(8+(i%cols)*(192*W+8),8+(i//cols)*(192*W+8)))
s.save(out)
