"""Meeye-style icon compositor. Reuses the pack's own shape mask, rim overlay and outer shadow (extracted from the APK).

Offline art regeneration only. Not used by CI.
MEEYE_ROOT points at a local workspace with resmap.json and apk/ (default: repo root).
"""
import json, io, os, numpy as np
from PIL import Image, ImageFilter
import cairosvg
S=192; SS=4
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("MEEYE_ROOT", os.path.abspath(os.path.join(_HERE, "..", "..")))
_m=json.load(open(os.path.join(ROOT, "resmap.json")))
def _L(k): return np.array(Image.open(os.path.join(ROOT, "apk", _m[k][0])).convert('RGBA')).astype(float)
_mask=_L('icon_mask')[...,3]/255.0
UPON=_L('icon_upon')                # white rim highlight (alpha<=64)
_tw=_L('twitter')
def _outer_shadow():
    out=_mask>=0.98
    a=np.where(out,_tw[...,3],np.nan)
    # propagate into AA band / inside by iterative neighbour mean
    a2=a.copy()
    for _ in range(4):
        pad=np.pad(a2,1,constant_values=np.nan)
        stack=np.stack([pad[1+dy:1+dy+S,1+dx:1+dx+S] for dy in(-1,0,1) for dx in(-1,0,1)])
        mean=np.nanmean(np.where(np.isnan(stack),np.nan,stack),axis=0)
        a2=np.where(np.isnan(a2),mean,a2)
    return np.nan_to_num(a2,nan=0.0)/255.0
SHADOW=_outer_shadow()
_a=_tw[...,3]/255.0
SHAPE=np.where(_mask>=0.999,0.0,np.clip((_a-SHADOW)/np.maximum(1-SHADOW,1e-6),0,1))

def lerp(c0,c1,t): return c0+(c1-c0)*t[...,None]
def hexc(h): h=h.lstrip('#'); return np.array([int(h[i:i+2],16) for i in (0,2,4)],float)

def glyph_alpha(svg_body, extra_defs=''):
    """svg_body: SVG markup in a 192x192 user space (white shapes; use fill-rule/evenodd for holes). Returns float alpha 192x192."""
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{S*SS}" height="{S*SS}" viewBox="0 0 {S} {S}">{extra_defs}<g fill="#fff">{svg_body}</g></svg>'
    png=cairosvg.svg2png(bytestring=svg.encode())
    im=Image.open(io.BytesIO(png)).convert('RGBA').split()[3]
    im=im.resize((S,S),Image.LANCZOS)
    return np.array(im).astype(float)/255.0

def render(galpha, top, bottom, gtint, gtop='#ffffff', grad_y=(8,146), sh_off=4, sh_sigma=5, sh_alpha=0.25, glyph_extra=None):
    """top/bottom: bg gradient hex; gtint: glyph bottom tint hex"""
    yy=np.repeat(np.arange(S)[:,None],S,1).astype(float)
    t=np.clip((yy-grad_y[0])/(grad_y[1]-grad_y[0]),0,1)
    bg=lerp(hexc(top),hexc(bottom),t)
    # glyph shadow
    ga=Image.fromarray((galpha*255).astype(np.uint8))
    ga=ga.transform(ga.size,Image.AFFINE,(1,0,0,0,1,-sh_off))
    ga=ga.filter(ImageFilter.GaussianBlur(sh_sigma))
    sh=np.array(ga).astype(float)/255*sh_alpha
    col=bg*(1-sh[...,None])
    # glyph fill (vertical gradient across glyph bbox)
    ys=np.where(galpha.max(1)>0.5)[0]; y0,y1=ys.min(),ys.max()
    tg=np.clip((yy-y0)/max(1,(y1-y0)),0,1)
    gc=lerp(hexc(gtop),hexc(gtint),tg)
    col=col*(1-galpha[...,None])+gc*galpha[...,None]
    # rim overlay
    ua=UPON[...,3:4]/255.0
    col=col*(1-ua)+UPON[...,:3]*ua
    A=SHAPE
    out_a=A+(1-A)*SHADOW
    rgb=np.where(out_a[...,None]>0,(col*A[...,None])/np.maximum(out_a[...,None],1e-6),0)
    rgba=np.dstack([np.clip(rgb,0,255),np.clip(out_a*255,0,255)])
    return Image.fromarray(rgba.round().astype(np.uint8),'RGBA')

def glyph_layer(svg_body, defs=''):
    """Colored glyph: svg_body in 192 space with its own fills. Returns (rgb float HxWx3, alpha HxW) premultiplication-safe."""
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{S*SS}" height="{S*SS}" viewBox="0 0 {S} {S}"><defs>{defs}</defs>{svg_body}</svg>'
    png=cairosvg.svg2png(bytestring=svg.encode())
    im=np.array(Image.open(io.BytesIO(png)).convert('RGBA')).astype(float)/255
    a=im[...,3]; pm=im[...,:3]*a[...,None]
    n=S*SS
    pm=pm.reshape(S,SS,S,SS,3).mean((1,3)); a=a.reshape(S,SS,S,SS).mean((1,3))
    rgb=np.where(a[...,None]>1e-6,pm/np.maximum(a[...,None],1e-6),0)*255
    return rgb,a

def render2(galpha, bg, glyph_rgb=None, gtint=None, gtop='#ffffff', grad_y=(8,146), sh_off=4, sh_sigma=5, sh_alpha=0.25, bg_stops=None):
    """bg=(top,bottom) hex or bg_stops=[(t,hex),...]; glyph_rgb optional colored glyph; else white->gtint gradient."""
    yy=np.repeat(np.arange(S)[:,None],S,1).astype(float)
    t=np.clip((yy-grad_y[0])/(grad_y[1]-grad_y[0]),0,1)
    if bg_stops:
        ts=[s[0] for s in bg_stops]; cols=np.array([hexc(s[1]) for s in bg_stops])
        bgc=np.stack([np.interp(t,ts,cols[:,c]) for c in range(3)],-1)
    else: bgc=lerp(hexc(bg[0]),hexc(bg[1]),t)
    ga=Image.fromarray((galpha*255).astype(np.uint8))
    ga=ga.transform(ga.size,Image.AFFINE,(1,0,0,0,1,-sh_off)).filter(ImageFilter.GaussianBlur(sh_sigma))
    sh=np.array(ga).astype(float)/255*sh_alpha
    col=bgc*(1-sh[...,None])
    if glyph_rgb is None:
        ys=np.where(galpha.max(1)>0.5)[0]; y0,y1=ys.min(),ys.max()
        tg=np.clip((yy-y0)/max(1,(y1-y0)),0,1)
        glyph_rgb=lerp(hexc(gtop),hexc(gtint),tg)
    col=col*(1-galpha[...,None])+glyph_rgb*galpha[...,None]
    ua=UPON[...,3:4]/255.0
    col=col*(1-ua)+UPON[...,:3]*ua
    return _finish(col)

def _finish(col):
    A=SHAPE; out_a=A+(1-A)*SHADOW
    rgb=np.where(out_a[...,None]>0,(col*A[...,None])/np.maximum(out_a[...,None],1e-6),0)
    return Image.fromarray(np.dstack([np.clip(rgb,0,255),np.clip(out_a*255,0,255)]).round().astype(np.uint8),'RGBA')

def render_art(img, scale=1.0, dx=0, dy=0, cut=None):
    """Official raster art placed full-bleed in the Meeye squircle (keeps pack's rim + shadow)."""
    im=img.convert('RGBA'); side=int(round(176*scale))
    im=im.resize((side,side),Image.LANCZOS)
    canvas=Image.new('RGBA',(S,S),(0,0,0,0)); canvas.alpha_composite(im,(8+dx-(side-176)//2,8+dy-(side-176)//2))
    c=np.array(canvas).astype(float)
    col=c[...,:3]*c[...,3:4]/255+np.array([128,128,128])*(1-c[...,3:4]/255)
    ua=UPON[...,3:4]/255.0
    col=col*(1-ua)+UPON[...,:3]*ua
    return _finish(col)
