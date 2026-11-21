import json, os
from PIL import Image, ImageDraw, ImageFont
_HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.environ.get('MEEYE_ROOT', os.path.abspath(os.path.join(_HERE,'..','..')))
m=json.load(open(os.path.join(ROOT,'resmap.json')))
F=lambda n,sz: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf'%n,sz)
def old(k): return Image.open(os.path.join(ROOT,'apk',m[k][0])).convert('RGBA')
def new(k): return Image.open(os.path.join(ROOT,'icons','%s.png'%k)).convert('RGBA')
BG=(236,238,242,255); PAD=20
newn=['grok','grok_bot','x_twitter','feiniu','philips_sonicare','termius','pilinara','venera','hail','senplayer','nrfr','eskimo','samsung_game_booster_plus','deepseek','deepseek_alt','meituan','meituan_alt','disney_plus','disney_plus_wordmark','bilibili_white','genshin_teyvat_sky','genshin_vision','google_gemini']
groups=[('Genshin Impact: pack original (kept as alt)  ->  NEW illustrated: genshin_teyvat_sky (main), genshin_vision (alt)',[('o','genshin_impact','pack original'),('n','genshin_teyvat_sky','NEW teyvat_sky (main)'),('n','genshin_vision','NEW vision (alt)')]),
 ('Honkai: Star Rail: reverted to the pack original (benghuai_huoche, train)',[('o','benghuai_huoche','pack original = used again')]),
 ('Disney+: pack original  ->  NEW castle scene (main) / NEW wordmark+sparkle (alt)',[('o','disney_plus','pack original'),('n','disney_plus','NEW castle (disney_plus)'),('n','disney_plus_wordmark','NEW wordmark (alt)')]),
 ('Nrfr: pack SIM Toolkit icons (left)  vs  NEW Nrfr = SIM + globe/region badge',[('o','samsung_sim_toolkit','pack: SIM toolkit (Samsung)'),('o','stock_sim_toolkit','pack: SIM toolkit (stock)'),('n','nrfr','NEW nrfr')]),
 ('Game Booster+ (com.samsung.android.game.honeyplayplus)  and  SenPlayer (recentred)',[('n','samsung_game_booster_plus','NEW Game Booster+'),('n','senplayer','NEW SenPlayer (recentred)')])]
Z=170; Z2=120; cols=8
W=max(3*(Z+PAD)*1+PAD, cols*(Z2+PAD)+PAD)
W=1250
hdr=34; H=20
for g,items in groups: H+=hdr+Z+PAD+30
H+=hdr+((len(newn)+cols-1)//cols)*(Z2+PAD+22)+20
im=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(im); y=14
for g,items in groups:
    d.text((PAD,y),g,font=F('-Bold',17),fill=(30,30,40)); y+=hdr
    for i,(src,k,l) in enumerate(items):
        x=PAD+i*(Z+PAD+12); im.alpha_composite((old(k) if src=='o' else new(k)).resize((Z,Z),Image.LANCZOS),(x,y))
        d.text((x+Z//2,y+Z+4),l,font=F('',13),fill=(50,50,60),anchor='mt')
    y+=Z+PAD+30
d.text((PAD,y),'All NEW icons (incl. alternates)',font=F('-Bold',17),fill=(30,30,40)); y+=hdr
for i,k in enumerate(newn):
    x=PAD+(i%cols)*(Z2+PAD+12); yy=y+(i//cols)*(Z2+PAD+22)
    im.alpha_composite(new(k).resize((Z2,Z2),Image.LANCZOS),(x,yy)); d.text((x+Z2//2,yy+Z2+3),k,font=F('',11),fill=(60,60,70),anchor='mt')
im.convert('RGB').save('preview_v6.png'); print(im.size)
