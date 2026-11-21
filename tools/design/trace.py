import numpy as np, potrace
from PIL import Image, ImageFilter
def mask_to_path(mask, up=2, blur=1.0, thresh=0.5):
    """mask: 2D float/bool array (1=fill). Returns (svg path d in mask pixel coords, bbox)"""
    im=Image.fromarray((np.asarray(mask,float)*255).astype(np.uint8))
    if up!=1: im=im.resize((im.width*up,im.height*up),Image.BICUBIC)
    if blur: im=im.filter(ImageFilter.GaussianBlur(blur*up/2))
    a=np.array(im)>thresh*255
    bm=potrace.Bitmap(~a)
    pl=bm.trace(turdsize=4,turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,alphamax=1.0,opticurve=True,opttolerance=0.3)
    d=[]
    f=lambda p:f"{p.x/up:.2f},{p.y/up:.2f}"
    for c in pl.curves:
        d.append("M"+f(c.start_point))
        for s in c.segments:
            if s.is_corner: d.append("L"+f(s.c)+"L"+f(s.end_point))
            else: d.append("C"+f(s.c1)+" "+f(s.c2)+" "+f(s.end_point))
        d.append("Z")
    ys,xs=np.where(a); 
    return "".join(d),(xs.min()/up,ys.min()/up,(xs.max()+1)/up,(ys.max()+1)/up)
def fit(d,bbox,cx=96,cy=96,maxdim=108,dy=0,dx=0):
    x0,y0,x1,y1=bbox; w,h=x1-x0,y1-y0; s=maxdim/max(w,h)
    tx=cx+dx-(x0+w/2)*s; ty=cy+dy-(y0+h/2)*s
    return f'<path d="{d}" fill-rule="evenodd" transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})"/>'
