import sys, math, json, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.environ.get("MEEYE_ROOT", os.path.abspath(os.path.join(HERE, "..", "..")))
from PIL import Image
import meeye_style as ms
from trace import mask_to_path, fit
# refs/ holds traced source art. Output PNGs land in the repo icons/ folder.
R = os.path.join(ROOT, "refs") + os.sep
OUT = os.path.join(ROOT, "icons") + os.sep
def load(f): return Image.open(R+f).convert('RGBA')
def arr(f): return np.array(load(f)).astype(float)
def lum(a): return a[...,:3].mean(-1)
icons={}   # name -> dict(img, glyph_svg, bg, ...)

def capsule(x1,y1,x2,y2,r):
    dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy); nx,ny=-dy/L*r,dx/L*r
    return (f"M{x1+nx:.2f},{y1+ny:.2f}L{x2+nx:.2f},{y2+ny:.2f}A{r},{r} 0 0 0 {x2-nx:.2f},{y2-ny:.2f}"
            f"L{x1-nx:.2f},{y1-ny:.2f}A{r},{r} 0 0 0 {x1+nx:.2f},{y1+ny:.2f}Z")

def add(name, svg=None, bg=None, tint=None, stops=None, colored=None, defs='', art=None, **kw):
    if art is not None:
        img=ms.render_art(art, **kw); gsvg=None
    elif colored is not None:
        rgb,a=ms.glyph_layer(colored,defs); img=ms.render2(a,bg,glyph_rgb=rgb,bg_stops=stops,**kw); gsvg=colored
    else:
        a=ms.glyph_alpha(svg); img=ms.render2(a,bg,gtint=tint,bg_stops=stops,**kw); gsvg=svg
    icons[name]=dict(img=img,glyph=gsvg,bg=bg,tint=tint,stops=stops,defs=defs)

# ---------- 1 Grok ----------
a=arr('play_ai.x.grok.png'); d,bb=mask_to_path(lum(a)>128)
add('grok', fit(d,bb,maxdim=104), ('#3d424b','#17191d'), '#cdd5e3')
# ---------- 2 Grok Bot ----------
gb=f'<path fill-rule="evenodd" d="M96,44 A54,54 0 1 1 95.9,44Z {capsule(70,96,82,121,8.5)} {capsule(110,80,125,105,8.5)}"/>'
add('grok_bot', gb, ('#34373e','#131518'), '#c9cfda')
# ---------- 3 X ----------
xp="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"
s=100/24
add('x_twitter', f'<path d="{xp}" transform="translate({96-12*s*0.97:.2f} {96-12*s:.2f}) scale({s*0.97:.4f} {s:.4f})"/>', ('#383a40','#111215'), '#d0d4db')
# ---------- 4 Feiniu (fnOS) ----------
fn='M190,322 Q190,240 272,240 L640,240 C675,236 705,205 705,172 C705,138 692,108 678,85 C725,112 748,160 748,208 C748,268 710,312 655,314 L265,314 L265,568 Q265,583 280,583 L308,583 Q325,583 325,566 L325,510 Q325,481 354,481 L432,481 L436,455 Q438,382 480,382 L658,382 C610,440 560,458 510,458 L510,515 Q510,552 472,552 L395,552 L395,628 Q395,660 363,660 L250,660 Q190,660 190,590 Z M85,85 C60,112 52,140 57,180 C62,215 100,238 150,240 C130,265 125,290 122,315 C60,312 8,268 8,208 C8,160 40,112 85,85 Z'
add('feiniu', fit(f'{fn}',(8,85,748,660),maxdim=112,dy=2), ('#5b9cff','#2c6fe8'), '#cfe0ff')
# ---------- 5 Sonicare ----------
a=arr('play_com.philips.cdp.ohc.tuscany.png'); m=(a[...,:3].min(-1)>235); m[375:]=False; m[:,:110]=False; m[:,420:]=False
d,bb=mask_to_path(m); add('philips_sonicare', fit(d,bb,maxdim=104), ('#2a93c6','#0b67a0'), '#cfe9f6')
# ---------- 6 Termius ----------
a=arr('play_com.server.auditor.ssh.client.png'); d,bb=mask_to_path(lum(a)>110)
add('termius', fit(d,bb,maxdim=116), ('#33449a','#121d5c'), '#cfd5ee')
# ---------- 7 PiliNara ----------
pn="M56,54L39.78,54l2.22,-10.94h14c3.02,0 5.47,2.45 5.47,5.47 0,3.02 -2.45,5.47 -5.47,5.47zM56,35.77h-9.62l-7.13,36.45h7.51L48.92,61.29h7.08c7.05,0 12.76,-5.71 12.76,-12.76 0,-7.05 -5.71,-12.76 -12.76,-12.76z"
sc=104/36.5
add('pilinara', f'<path fill-rule="evenodd" d="{pn}" transform="translate({96-54*sc:.2f} {96-54*sc:.2f}) scale({sc:.4f})"/>', ('#27b85c','#1b9c45'), '#d4ffe2')
# ---------- 8 Venera ----------
sv=0.31
def vn(): 
    return (f'<g transform="translate({96-256*sv:.1f} {96-270*sv:.1f}) scale({sv})" fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round">'
            '<path stroke-width="30" d="M143,172 L238,366"/><path stroke-width="26" d="M188,172 L257,322 L325,172"/><path stroke-width="30" d="M371,172 L272,366"/></g>')
a=ms.glyph_alpha(vn()); img=ms.render2(a,('#3f62ff','#1b38e6'),gtint='#d7dfff'); icons['venera']=dict(img=img,glyph=vn(),bg=('#3f62ff','#1b38e6'),tint='#d7dfff',stops=None,defs='')
# ---------- 9 Hail ----------
hs=3.0
hail=(f'<g transform="translate({96-54*hs:.1f} {96-54*hs:.1f}) scale({hs})">'
      '<path d="M45,38.4L63,38.4L54,54Z" fill="#81D4FA"/>'
      '<g stroke="#1d2430" stroke-width="4.5" stroke-linecap="round" fill="none"><path d="M45,38.4L63,69.6M63,38.4L45,69.6M45,38.4L63,38.4M72,54L63,69.6M63,69.6L45,69.6M45,69.6L36,54"/></g></g>')
add('hail', colored=hail, bg=('#ffffff','#e3e7ee'), sh_alpha=0.22)
# ---------- 10/11 games ----------
# Genshin: three clean glyph concepts (a/b/c) - user picks one; packages are mapped to genshin_a
def st4(cx,cy,r,k=0.16): return f'M{cx},{cy-r} Q{cx+r*k},{cy-r*k} {cx+r},{cy} Q{cx+r*k},{cy+r*k} {cx},{cy+r} Q{cx-r*k},{cy+r*k} {cx-r},{cy} Q{cx-r*k},{cy-r*k} {cx},{cy-r}Z'
gdef=('<linearGradient id="wg" gradientUnits="userSpaceOnUse" x1="0" y1="40" x2="0" y2="160"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{T}"/></linearGradient>'
      '<linearGradient id="lg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.35"/><stop offset="1" stop-color="#fff" stop-opacity="0.95"/></linearGradient>'
      '<linearGradient id="fl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.65"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
      '<linearGradient id="gd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6c0"/><stop offset="1" stop-color="#ffcf4d"/></linearGradient>')
# (a) the gate / door of light (start-screen motif)
ga=('<g transform="translate(0 -12)"><path d="M56,150 V92 A40,40 0 0 1 136,92 V150Z" fill="none" stroke="url(#wg)" stroke-width="8" stroke-linejoin="round"/>'
    '<path d="M68,150 V92 A28,28 0 0 1 124,92 V150Z" fill="url(#lg)"/>'
    '<path d="M68,150 L38,176 H154 L124,150Z" fill="url(#fl)"/>'
    f'<path d="{st4(96,112,9,0.2)}" fill="#fff"/></g>')
add('genshin_a', colored=ga, defs=gdef.replace('{T}','#d6efff'), bg=('#62cbff','#2b86ee'), sh_alpha=0.25)
# (b) Paimon-inspired: floating head with crown + cape
gb_=('<g transform="translate(0 -2)"><path fill-rule="evenodd" fill="url(#wg)" d="M96,52 a30,30 0 1 0 0.1,0Z M84,81 a4.2,5.6 0 1 0 0.1,0Z M108,81 a4.2,5.6 0 1 0 0.1,0Z"/>'
     '<path fill="#bfe1ff" d="M68,108 Q96,120 124,108 L134,146 Q118,138 110,152 Q96,142 82,152 Q74,138 58,146Z"/><path fill="#fff" d="M80,108 Q96,114 112,108 L112,114 Q96,121 80,114Z"/><circle cx="64" cy="86" r="8" fill="url(#wg)"/><circle cx="128" cy="86" r="8" fill="url(#wg)"/>'
     '<path fill="url(#gd)" stroke="url(#gd)" stroke-width="2" stroke-linejoin="round" d="M80,54 L83,38 L90,47 L96,32 L102,47 L109,38 L112,54Z"/>'
     f'<path fill="#fff" d="{st4(140,58,9)}"/><path fill="#fff" d="{st4(52,116,6)}"/></g>')
add('genshin_b', colored=gb_, defs=gdef.replace('{T}','#cfd2ff'), bg=('#7d82f2','#3a3cc4'), sh_alpha=0.25)
# (c) celestia island + logo star
gc=('<g><path fill="url(#gd)" d="'+st4(96,64,34,0.15)+'"/>'
    '<path fill="url(#wg)" d="M52,120 Q96,132 140,120 Q134,134 120,144 Q108,154 96,170 Q84,154 72,144 Q58,134 52,120Z"/>'
    '<path fill="url(#wg)" d="M76,108 H116 L96,92Z"/><g fill="url(#wg)"><rect x="80" y="109" width="6" height="12" rx="1"/><rect x="93" y="109" width="6" height="12" rx="1"/><rect x="106" y="109" width="6" height="12" rx="1"/></g></g>')
add('genshin_c', colored=gc, defs=gdef.replace('{T}','#d4fff2'), bg=('#4fe0bd','#1c96bd'), sh_alpha=0.25)
# ---------- 12 SenPlayer ----------
defs=('<linearGradient id="o" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffd27d"/><stop offset="1" stop-color="#f58a6e"/></linearGradient>'
      '<linearGradient id="m" x1="0" y1="0" x2="0.4" y2="1"><stop offset="0" stop-color="#f20a64"/><stop offset="1" stop-color="#a0306e"/></linearGradient>'
      '<linearGradient id="p" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a4fb0"/><stop offset="1" stop-color="#a98ac8"/></linearGradient>'
      '<clipPath id="c"><path d="M52,58 Q52,48 62,48 Q70,48 78,52 L134,84 Q150,96 134,108 L78,140 Q68,146 62,146 Q52,146 52,136Z"/></clipPath>')
sen=('<g transform="translate(-19 -24) scale(1.25)"><g clip-path="url(#c)"><rect x="40" y="40" width="120" height="120" fill="url(#o)"/>'
     '<path d="M40,40 L96,40 C118,60 122,96 108,120 C100,134 90,142 80,150 L40,150Z" fill="url(#m)"/>'
     '<path d="M40,64 C70,76 84,100 84,118 C84,132 80,142 76,150 L40,150Z" fill="#5c2a90"/>'
     '<path d="M40,104 C62,96 82,100 82,126 C82,140 76,148 70,152 L40,152Z" fill="url(#p)"/></g></g>')
add('senplayer', colored=sen, defs=defs, bg=('#f7f9fa','#e1e6eb'), sh_alpha=0.2)
# ---------- 13 Disney+ (original composition = official logo: wordmark + arc, recoloured to the Meeye look) ----------
a=arr('disney_ios.png'); m=(a[...,:3].min(-1)>200); m[:230]=False; m[830:]=False
d,bb=mask_to_path(m,up=1,blur=0.8)
add('disney_plus', fit(d,bb,maxdim=114,dy=0), ('#2f86d6','#0b2c82'), '#dcecff')
# ---------- 14 bilibili white ----------
a=arr('bili/r2.png'); pink=np.clip((255-a[...,1])/150,0,1)*(a[...,0]>200)
d,bb=mask_to_path(pink,up=3,blur=0.8)
tvm=(1-pink)*np.clip((252-a[...,0])/14,0,1)*(np.abs(a[...,0]-a[...,1])<8)
d2,bb2=mask_to_path(tvm,up=3,blur=1.2)
x0,y0,x1,y1=bb2; sc=122/ (bb[2]-bb[0])
def place(dd,b,cx,cy,fill):
    return f'<path d="{dd}" fill="{fill}" fill-rule="evenodd" transform="translate({cx-sc*(b[0]+b[2])/2:.2f} {cy-sc*(b[1]+b[3])/2:.2f}) scale({sc:.4f})"/>'
bw=place(d2,bb2,96,92,'#e3e5ea')+place(d,bb,96,110-0,'#fb6f9c')
bw=place(d2,bb2,96,96,'#e1e3e8')+f'<path d="{d}" fill="#ff6699" fill-rule="evenodd" transform="translate({96-sc*(bb2[0]+bb2[2])/2:.2f} {96-sc*(bb2[1]+bb2[3])/2:.2f}) scale({sc:.4f})"/>'
add('bilibili_white', colored=bw, bg=('#ffffff','#e9ecf0'), sh_alpha=0.2)
# ---------- 15 Nrfr (SIM card outline with the globe centred on the card body) ----------
def nrfr_svg():
    # card body bbox (stroke centre-line) x 60..132 -> centre 96; y 41..147 -> centre 94 (1-2px above optical middle, Meeye habit)
    # chamfer is cut INTO the right-top corner only, body bbox stays symmetric about x=96. Globe centred on the body (96,94).
    cx,cy=96,94
    return ('<g fill="none" stroke="url(#wg)" stroke-linecap="round" stroke-linejoin="round">'
            '<path stroke-width="6.5" d="M72,41 H110 L132,63 V135 Q132,147 120,147 H72 Q60,147 60,135 V53 Q60,41 72,41Z"/>'
            f'<circle stroke-width="5" cx="{cx}" cy="{cy}" r="25"/><ellipse stroke-width="4.2" cx="{cx}" cy="{cy}" rx="10.5" ry="25"/>'
            f'<path stroke-width="4.2" d="M{cx-25},{cy} H{cx+25} M{cx-21},{cy-12} H{cx+21} M{cx-21},{cy+12} H{cx+21}"/></g>')
nk_defs='<linearGradient id="wg" gradientUnits="userSpaceOnUse" x1="0" y1="40" x2="0" y2="150"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e3cfff"/></linearGradient>'
add('nrfr', colored=nrfr_svg(), defs=nk_defs, bg=('#a24bff','#6a05e8'))
# ---------- 16 Eskimo ----------
a=arr('eskimo_ios.png'); d,bb=mask_to_path(a[...,0]>150,up=1,blur=0.8)
add('eskimo', fit(d,bb,maxdim=112), ('#2f8dff','#0462e6'), '#d4e8ff')
# ---------- 17 Game Booster+ / honeyplay+ (traced from the Galaxy Store icon) ----------
from scipy import ndimage as ndi
h4=np.array(Image.open(R+'hp/gb512.png').convert('RGBA')).astype(float); hr,hg,hb=h4[...,0],h4[...,1],h4[...,2]; hop=h4[...,3]>200
yy_,xx_=np.mgrid[0:512,0:512]
Xm=hop&(hg>hr+30)&(hg>hb+15)&(xx_>345)
reg=(xx_<345)&(yy_>150)&(yy_<350)
cap=reg&hop&(((hb>hg+12)&(hg>135))|(h4[...,:3].min(-1)>225))&~Xm
cap=ndi.binary_opening(cap,iterations=1); cap=ndi.binary_fill_holes(cap)
wh=reg&(h4[...,:3].min(-1)>238)&ndi.binary_erosion(cap,iterations=6)
dc,bc=mask_to_path(cap,up=2,blur=0.8); dwh,bwh=mask_to_path(wh,up=2,blur=0.8); dx_,bx_=mask_to_path(Xm,up=2,blur=0.8)
bb_all=(min(bc[0],bx_[0]),min(bc[1],bx_[1]),max(bc[2],bx_[2]),max(bc[3],bx_[3]))
def pl(dp_,fill): return fit(dp_,bb_all,maxdim=124).replace('<path ',f'<path fill="{fill}" ')
gdefs=('<linearGradient id="gc" gradientUnits="userSpaceOnUse" x1="0" y1="70" x2="0" y2="120"><stop offset="0" stop-color="#d9dbff"/><stop offset="1" stop-color="#a2a6fa"/></linearGradient>'
       '<linearGradient id="gx" gradientUnits="userSpaceOnUse" x1="0" y1="70" x2="0" y2="120"><stop offset="0" stop-color="#b6ffd2"/><stop offset="1" stop-color="#4fdc92"/></linearGradient>')
gbp=pl(dc,'url(#gc)')+pl(dwh,'#ffffff')+pl(dx_,'url(#gx)')
add('samsung_game_booster_plus', colored=gbp, defs=gdefs, bg=('#b24dfb','#5f10d4'), sh_alpha=0.28)
# ---------- 18 DeepSeek ----------
a=arr('play_deepseek.png'); d,bb=mask_to_path(a[...,0]<170,up=1,blur=0.8)
add('deepseek_alt', fit(d,bb,maxdim=112), ('#6784ff','#3a55ee'), '#d6ddff')   # inverted (blue bg / white whale) - kept as extra option
wh=fit(d,bb,maxdim=112).replace('<path ','<path fill="url(#dsg)" ')
dsdefs='<linearGradient id="dsg" gradientUnits="userSpaceOnUse" x1="0" y1="40" x2="0" y2="150"><stop offset="0" stop-color="#6683ff"/><stop offset="1" stop-color="#3d58f0"/></linearGradient>'
add('deepseek', colored=wh, defs=dsdefs, bg=('#ffffff','#e4e8f0'), sh_alpha=0.22)
# ---------- 19 Meituan ----------
a=arr('meituan_ios.png'); d,bb=mask_to_path(lum(a)<90,up=1,blur=0.8)
add('meituan_alt', colored=fit(d,bb,maxdim=122).replace('<path ','<path fill="#161616" '), bg=('#ffe23c','#ffc700'), sh_alpha=0.16, sh_off=3, sh_sigma=4)  # official black-on-yellow, extra option
add('meituan', fit(d,bb,maxdim=118), ('#ffcb2e','#f49800'), '#fff1c9')

# ---------- 20 Gemini (current multicolor sparkle) ----------
import base64
cut=Image.open(R+'gemini_cutout.png'); _b=__import__('io').BytesIO(); cut.save(_b,'PNG')
gm=f'<image x="{96-56:.1f}" y="{96-56:.1f}" width="112" height="112" xlink:href="data:image/png;base64,{base64.b64encode(_b.getvalue()).decode()}" xmlns:xlink="http://www.w3.org/1999/xlink"/>'
add('google_gemini', colored=gm, bg=('#ffffff','#e4e8f0'), sh_alpha=0.2)


# =================== batch 8 (v2rayNG, Expert RAW, Nothing X, Canta, Droid-ify, Resplash, TikTok) ===================
from scipy import ndimage as ndi
def cutout(name, rgb, alpha, maxdim, dy=0, up=3, dx=0):
    """rgb HxWx3 (0-255), alpha HxW (0-1) -> raster glyph <image> (interior colours pushed out to the edge: no halo)"""
    H,W=alpha.shape
    im=Image.fromarray(rgb.astype(np.uint8)).resize((W*up,H*up),Image.LANCZOS); rgb=np.array(im).astype(float)
    a=np.array(Image.fromarray((alpha*255).astype(np.uint8)).resize((W*up,H*up),Image.BICUBIC)).astype(float)/255
    solid=a>0.9; idx=ndi.distance_transform_edt(~solid,return_distances=False,return_indices=True)
    rgb=rgb[idx[0],idx[1]]
    ys,xs=np.where(a>0.02); x0,x1,y0,y1=xs.min()-2,xs.max()+3,ys.min()-2,ys.max()+3
    out=np.dstack([rgb,a*255]).astype(np.uint8)[y0:y1,x0:x1]; Image.fromarray(out,'RGBA').save(R+'cut_'+name+'.png')
    w,h=x1-x0,y1-y0; s=maxdim/max(w,h); bio=__import__('io').BytesIO(); Image.fromarray(out,'RGBA').save(bio,'PNG')
    ax,ay=(x0+x1)/2,(y0+y1)/2   # bbox centre of the visible art
    return (f'<image x="{96+dx-w*s/2:.2f}" y="{96+dy-h*s/2:.2f}" width="{w*s:.2f}" height="{h*s:.2f}" '
            f'xlink:href="data:image/png;base64,{base64.b64encode(bio.getvalue()).decode()}" xmlns:xlink="http://www.w3.org/1999/xlink"/>')
def rd(f): return np.array(Image.open(R+'r8/'+f).convert('RGBA')).astype(float)
WHITEBG=('#ffffff','#e4e8f0')
# ---- 1 v2rayNG_new: the OFFICIAL logo shape, untouched (traced from 2dust/v2rayNG ic_launcher_foreground), only positioned.
# The pack's own v2rayng (reference, visually centred) has bbox centre (99.0, 101.0) and mass centroid (91.2, 93.3);
# its visual centre = mean of the two = (95.1, 97.2). Same rule here: place the logo so (bbox centre + centroid)/2 == (95.1, 97.2).
f=rd('v2_fg.png'); d,bb=mask_to_path(f[...,3]/255>0.5,up=2,blur=0.8)
vg='<linearGradient id="vg" gradientUnits="userSpaceOnUse" x1="0" y1="48" x2="0" y2="146"><stop offset="0" stop-color="#2a2f3a"/><stop offset="1" stop-color="#0b0d12"/></linearGradient>'
def _v2(dx,dy): return fit(d,bb,maxdim=100,dx=dx,dy=dy).replace('<path ','<path fill="url(#vg)" ')
def _vis(dx,dy):
    _,a=ms.glyph_layer(_v2(dx,dy),vg); m=a>0.5; ys,xs=np.where(m)
    return ((xs.min()+xs.max())/2+xs.mean())/2, ((ys.min()+ys.max())/2+ys.mean())/2
_dx=_dy=0.0
for _ in range(4):
    _vx,_vy=_vis(_dx,_dy); _dx+=95.1-_vx; _dy+=97.2-_vy
add('v2rayng_new', colored=_v2(_dx,_dy), defs=vg, bg=WHITEBG, sh_alpha=0.22)
# ---- 2 Samsung Expert RAW: Galaxy Store icon (grey camera on silver) ----
f=rd('raw512.png'); lum_=f[...,:3].mean(-1); yy,xx=np.mgrid[0:512,0:512]
m=(lum_<150)&(f[...,3]>200)&(((xx-256)**2+(yy-290)**2)<230**2); m=ndi.binary_closing(m,iterations=2); m=ndi.binary_fill_holes(m)
_l,_n=ndi.label(m); m=_l==(np.argmax(np.bincount(_l.ravel())[1:])+1)   # keep only the camera (drops faint squircle-edge shading)
add('samsung_expert_raw', colored=cutout('raw',f[...,:3],ndi.gaussian_filter(m.astype(float),0.8),maxdim=116), bg=('#eceff5','#b9bfce'), sh_alpha=0.25)
# ---- 3 Nothing X: official capsule+cross+red dot (Play icon) ----
f=rd('nothing_play.png'); a=np.clip((255-f[...,:3].min(-1))/35,0,1)*(f[...,3]>200)*(((xx-256)**2+(yy-256)**2)<235**2)
add('nothing_x', colored=cutout('nothingx',f[...,:3],a,maxdim=112), bg=('#ffffff','#eef0f5'), sh_alpha=0.22)
# ---- 4 Canta: white bin+arrow (samolego/Canta ic_launcher_foreground) ----
f=rd('canta_ic_launcher_foreground.png'); d,bb=mask_to_path(f[...,3]/255>0.5,up=2,blur=0.8)
add('canta', fit(d,bb,maxdim=92), ('#f04a43','#b30f12'), '#ffdede')
# ---- 5 Droid-ify: green arc + orange arrow on charcoal (Droid-ify/client) ----
f=rd('droid_ic.png'); yy2,xx2=np.mgrid[0:192,0:192]; mx=f[...,:3].max(-1)
a=np.clip((mx-75)/70,0,1)*(((xx2-96)**2+(yy2-96)**2)<80**2)
add('droid_ify_alt', colored=cutout('droid',f[...,:3],a,maxdim=104,up=4), bg=('#323a38','#111514'), sh_alpha=0.3)
# ---- 6 Resplash: ring + disc (b-lam/Resplash ic_launcher_foreground) ----
f=rd('resp_ic_launcher_foreground.png'); d,bb=mask_to_path(f[...,3]/255>0.5,up=2,blur=0.8)
add('resplash', fit(d,bb,maxdim=104).replace('<path ','<path fill="url(#vg)" '), None, defs=None) if False else None
a_=f[...,3]/255; d,bb=mask_to_path(a_>0.5,up=2,blur=0.8)
add('resplash', colored=fit(d,bb,maxdim=104).replace('<path ','<path fill="url(#vg)" '), defs=vg.replace('#2a2f3a','#37444c').replace('#0b0d12','#182127'), bg=WHITEBG, sh_alpha=0.22)
# ---- 7 TikTok: current official note with the cyan/red offsets, near-white on dark gradient ----
t=np.array(Image.open(R+'r8/tt_ios.jpg').convert('RGB')).astype(float); mxt=t.max(-1)
a=np.clip((mxt-40)/160,0,1)*(((xx-256)**2+(yy-256)**2)<215**2)
add('tiktok', colored=cutout('tiktok',t,a,maxdim=108), bg=('#3b3c42','#0b0b0d'), sh_alpha=0.3)

# =================== batch 10 (ChatGPT, 什么值得买): current OFFICIAL art (Google Play icons), glyph shape untouched, only restyled + visually centred ===================
# Visual centre rule (same as v2rayng): mean(bbox centre, mass centroid) placed on the pack's centre (96.0, 95.5) -- the pack's own ChatGPT glyph sits at bbox (96.0, 95.5).
TGT=(96.0,95.5)
def _vcentre(alpha):
    m=alpha>0.5; ys,xs=np.where(m)
    return ((xs.min()+xs.max()+1)/2+xs.mean()+.5)/2, ((ys.min()+ys.max()+1)/2+ys.mean()+.5)/2
def centred(make, defs='', tgt=TGT, it=4):
    dx=dy=0.0
    for _ in range(it):
        s=make(dx,dy)
        a=ms.glyph_layer(s,defs)[1] if defs else ms.glyph_alpha(s)
        vx,vy=_vcentre(a); dx+=tgt[0]-vx; dy+=tgt[1]-vy
    return make(dx,dy),(dx,dy)
# ---- ChatGPT: black blossom on white (official Android/Play icon), traced as-is ----
g=np.array(Image.open(R+'r10/gpt_1024.png').convert('RGBA')).astype(float)
gm=1-(g[...,:3].mean(-1)/255)
gd,gbb=mask_to_path(gm>0.5,up=2,blur=0.8)
gvg='<linearGradient id="gv" gradientUnits="userSpaceOnUse" x1="0" y1="40" x2="0" y2="152"><stop offset="0" stop-color="#2a2f3a"/><stop offset="1" stop-color="#0b0d12"/></linearGradient>'
gsvg,_gd=centred(lambda dx,dy: fit(gd,gbb,maxdim=112,dx=dx,dy=dy).replace('<path ','<path fill="url(#gv)" '), gvg)
add('chatgpt', colored=gsvg, defs=gvg, bg=WHITEBG, sh_alpha=0.22)
# ---- 什么值得买: white brush 值 on the official red (Play icon = red disc + white 值; the disc becomes the Meeye squircle) ----
s_=np.array(Image.open(R+'r10/smzdm_1024.png').convert('RGBA')).astype(float)
red=(s_[...,0]>200)&(s_[...,1]<90)&(s_[...,3]>250); ys_,xs_=np.where(red); ccx,ccy=(xs_.min()+xs_.max()+1)/2,(ys_.min()+ys_.max()+1)/2; rr=(xs_.max()-xs_.min()+1)/2
yy_,xx_=np.mgrid[:s_.shape[0],:s_.shape[1]]
sm=(s_[...,2]/255)*(((xx_-ccx)**2+(yy_-ccy)**2)<(rr-6)**2)       # blue channel: white=1, red=0
sd,sbb=mask_to_path(sm>0.5,up=2,blur=0.8)
srg='<linearGradient id="sg" gradientUnits="userSpaceOnUse" x1="0" y1="40" x2="0" y2="152"><stop offset="0" stop-color="#ff3320"/><stop offset="1" stop-color="#d40a00"/></linearGradient>'
ssvg,_sd=centred(lambda dx,dy: fit(sd,sbb,maxdim=100,dx=dx,dy=dy).replace('<path ','<path fill="url(#sg)" '), srg)
add('shenmezhidemai', colored=ssvg, defs=srg, bg=WHITEBG, sh_alpha=0.22)   # v11: white base + official-red 值 (no disc)

if __name__=='__main__':
    import os; os.makedirs(OUT,exist_ok=True)
    for n,v in icons.items(): v['img'].save(OUT+n+'.png')
    print(list(icons))
