import json, os
from PIL import Image, ImageDraw, ImageFont
_HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.environ.get('MEEYE_ROOT', os.path.abspath(os.path.join(_HERE,'..','..')))
m=json.load(open(os.path.join(ROOT,'resmap.json')))
F=lambda n,sz: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf'%n,sz)
def old(k): return Image.open(os.path.join(ROOT,'apk',m[k][0])).convert('RGBA')
def new(k): return Image.open(os.path.join(ROOT,'icons','%s.png'%k)).convert('RGBA')
BG=(236,238,242,255); Z=144; PAD=18
existing=['chatgpt','claude','google_gemini','telegram','github','youtube','microsoft_copilot','nikke','pilipala','twitter']
newn_unused=['grok','grok_bot','x_twitter','feiniu','philips_sonicare','termius','pilinara','venera','hail','senplayer','nrfr','eskimo','samsung_game_booster_plus','deepseek','meituan','disney_plus','bilibili_white','hsr','genshin']
newn=['grok','grok_bot','x_twitter','feiniu','philips_sonicare','termius','pilinara','venera','hail','senplayer','nrfr','eskimo','samsung_game_booster_plus','deepseek','deepseek_alt','meituan','meituan_alt','disney_plus','bilibili_white','benghuai_huoche_official','genshin_impact_official','google_gemini']
pairs=[('google_gemini','google_gemini','Gemini (old kept as google_gemini_old)'),('twitter','x_twitter','X (was bird)'),('disney_plus','disney_plus','Disney+'),('benghuai_huoche','benghuai_huoche_official','HSR (old kept as alt)'),('genshin_impact','genshin_impact_official','Genshin (old kept as alt)'),('meituan','meituan','Meituan'),('meituan','meituan_alt','Meituan: old -> alt (official look)'),('bilibili','bilibili_white','bilibili intl (com.bilibili.app.in)'),('terminus','termius','Termius'),('pilipala','pilinara','PiliPala -> PiliNara')]
cols=10
W=cols*(Z+PAD)+PAD
def rows(n): return (n+cols-1)//cols
H=40+rows(len(existing))*(Z+PAD+22)+40+rows(len(newn))*(Z+PAD+22)+40+((len(pairs)+3)//4)*(Z+PAD+40)+20
im=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(im); y=14
def title(t):
    global y; d.text((PAD,y),t,font=F('-Bold',20),fill=(30,30,40)); y+=34
def put(img,x,yy,label=None):
    im.alpha_composite(img.resize((Z,Z),Image.LANCZOS),(x,yy))
    if label: d.text((x+Z//2,yy+Z+3),label,font=F('',12),fill=(60,60,70),anchor='mt')
title('Existing Meeye icons (reference, same size)')
for i,k in enumerate(existing): put(old(k),PAD+(i%cols)*(Z+PAD),y+(i//cols)*(Z+PAD+22),k)
y+=rows(len(existing))*(Z+PAD+22)+8
title('NEW icons (21 incl. alternates) - native 192px renders, shown at the same size')
for i,k in enumerate(newn): put(new(k),PAD+(i%cols)*(Z+PAD),y+(i//cols)*(Z+PAD+22),k)
y+=rows(len(newn))*(Z+PAD+22)+8
title('Before (existing Meeye)  ->  After (new)')
for i,(o,n,l) in enumerate(pairs):
    x=PAD+(i%4)*(2*Z+PAD*2+10); yy=y+(i//4)*(Z+PAD+40)
    put(old(o),x,yy); put(new(n),x+Z+8,yy)
    d.text((x+Z+4,yy+Z+3),l,font=F('',12),fill=(60,60,70),anchor='mt')
im.convert('RGB').save('preview.png'); print(im.size)
