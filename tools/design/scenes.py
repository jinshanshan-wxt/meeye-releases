"""Hand-drawn SVG scenes (176x176 viewBox, placed full-bleed in the Meeye squircle via render_art).

Offline art regeneration only. Not used by CI. Writes into $MEEYE_ROOT/refs (default: repo root).
"""
import os
import cairosvg
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("MEEYE_ROOT", os.path.abspath(os.path.join(_HERE, "..", "..")))
R = os.path.join(ROOT, "refs") + os.sep
def star(cx,cy,r,fill='#fff',op=1,k=0.18):
    return (f'<path fill="{fill}" opacity="{op}" d="M{cx},{cy-r} Q{cx+r*k},{cy-r*k} {cx+r},{cy} Q{cx+r*k},{cy+r*k} {cx},{cy+r} Q{cx-r*k},{cy+r*k} {cx-r},{cy} Q{cx-r*k},{cy-r*k} {cx},{cy-r}Z"/>')
def cloud(cx,cy,w,fill='#fff',op=0.95):
    h=w*0.28
    return (f'<g fill="{fill}" opacity="{op}"><ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{h/2}"/>'
            f'<ellipse cx="{cx-w*0.18}" cy="{cy-h*0.35}" rx="{w*0.22}" ry="{h*0.6}"/><ellipse cx="{cx+w*0.1}" cy="{cy-h*0.55}" rx="{w*0.27}" ry="{h*0.75}"/></g>')
def render(svg,name,size=704):
    s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 176 176" width="{size}" height="{size}">{svg}</svg>'
    open(R+name+'.svg','w').write(s); cairosvg.svg2png(bytestring=s.encode(),write_to=R+name+'.png',output_width=size,output_height=size)

# ---- Genshin v1: floating island over Teyvat sky -------------------------------------
def genshin_island():
    d=('<defs>'
       '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a73dc"/><stop offset="0.5" stop-color="#6cbcff"/><stop offset="0.85" stop-color="#d8efff"/><stop offset="1" stop-color="#ffe6b8"/></linearGradient>'
       '<radialGradient id="sun" cx="0.78" cy="0.2" r="0.5"><stop offset="0" stop-color="#fffbe0" stop-opacity="0.95"/><stop offset="0.35" stop-color="#fff2b8" stop-opacity="0.45"/><stop offset="1" stop-color="#fff2b8" stop-opacity="0"/></radialGradient>'
       '<linearGradient id="rock" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c79a6a"/><stop offset="0.6" stop-color="#8a5f3f"/><stop offset="1" stop-color="#5b3b2a"/></linearGradient>'
       '<linearGradient id="grass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9be86a"/><stop offset="1" stop-color="#3fae4e"/></linearGradient>'
       '<linearGradient id="fall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8fbff"/><stop offset="1" stop-color="#e8fbff" stop-opacity="0"/></linearGradient></defs>'
       '<rect width="176" height="176" fill="url(#sky)"/><rect width="176" height="176" fill="url(#sun)"/>')
    # distant small island
    d+=('<g opacity="0.9"><path d="M20,52 Q34,48 48,52 Q46,60 36,66 Q30,72 28,66 Q22,60 20,52Z" fill="#a98262"/>'
        '<path d="M18,52 Q34,44 50,52 Q34,57 18,52Z" fill="#8ad866"/></g>')
    d+=cloud(140,70,44,op=0.9)+cloud(26,112,50,op=0.85)
    # waterfall
    d+='<path d="M104,92 L110,92 L108,128 L106,128Z" fill="url(#fall)"/>'
    # main island rock (inverted cone, wobbly)
    d+=('<path d="M42,86 Q88,98 134,86 Q132,104 122,114 Q116,128 106,136 Q98,150 90,156 Q84,146 78,138 Q64,128 58,114 Q46,104 42,86Z" fill="url(#rock)"/>'
        '<path d="M60,100 Q70,112 74,128" stroke="#5b3b2a" stroke-opacity="0.35" stroke-width="2" fill="none" stroke-linecap="round"/>'
        '<path d="M100,104 Q96,120 92,140" stroke="#f2cf9e" stroke-opacity="0.35" stroke-width="2" fill="none" stroke-linecap="round"/>')
    # grass top
    d+=('<path d="M38,82 Q40,70 62,68 Q88,62 116,68 Q138,70 138,82 Q134,92 88,95 Q44,92 38,82Z" fill="url(#grass)"/>'
        '<path d="M38,82 Q44,92 88,95 Q134,92 138,82 Q130,86 88,87 Q46,86 38,82Z" fill="#2c8a3e" opacity="0.55"/>')
    # Statue-of-the-Seven-like pedestal + figure
    d+=('<g><rect x="76" y="60" width="24" height="8" rx="1.5" fill="#e9eef2"/><rect x="80" y="54" width="16" height="7" rx="1.5" fill="#cfd8de"/>'
        '<path d="M88,32 C84,36 84,42 86,46 L84,54 L92,54 L90,46 C92,42 92,36 88,32Z" fill="#f4f7f9"/><circle cx="88" cy="30" r="3.6" fill="#f4f7f9"/>'
        '<path d="M82,44 Q74,40 70,46 Q76,46 83,49Z M94,44 Q102,40 106,46 Q100,46 93,49Z" fill="#fff" opacity="0.95"/></g>')
    # trees
    for x,y,s in [(50,76,1),(124,77,1.1),(112,72,0.8)]:
        d+=f'<g transform="translate({x} {y}) scale({s})"><rect x="-1" y="0" width="2" height="6" fill="#7a4e2c"/><circle cx="0" cy="-3" r="6" fill="#2f9a47"/><circle cx="-2" cy="-5" r="3.5" fill="#5bcf62"/></g>'
    # wind swirls + sparkles
    d+=('<g fill="none" stroke="#fff" stroke-linecap="round" opacity="0.8"><path d="M10,142 Q40,128 64,138 Q80,144 72,152" stroke-width="2.2"/>'
        '<path d="M150,118 Q166,110 168,98 Q168,90 160,92" stroke-width="2"/><path d="M130,38 Q150,30 160,40" stroke-width="1.8" opacity="0.7"/></g>')
    d+=star(150,28,9,'#fffbe0')+star(30,30,6,'#fff')+star(158,150,5,'#fff',0.9)+star(14,84,4,'#fff',0.9)
    d+=cloud(96,176,100,op=0.95)+cloud(14,174,48,op=0.9)+cloud(166,168,44,op=0.9)
    return d

# ---- Genshin v2: Anemo Vision emblem --------------------------------------------------
def genshin_vision():
    d=('<defs>'
       '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14245c"/><stop offset="0.55" stop-color="#2b63b8"/><stop offset="1" stop-color="#58c4d8"/></linearGradient>'
       '<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#9ffff0" stop-opacity="0.85"/><stop offset="0.5" stop-color="#5de6d6" stop-opacity="0.28"/><stop offset="1" stop-color="#5de6d6" stop-opacity="0"/></radialGradient>'
       '<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0b0"/><stop offset="0.5" stop-color="#e9b84a"/><stop offset="1" stop-color="#a8741f"/></linearGradient>'
       '<linearGradient id="gold2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff6c8"/><stop offset="1" stop-color="#c58d2c"/></linearGradient>'
       '<radialGradient id="gem" cx="0.4" cy="0.3" r="0.8"><stop offset="0" stop-color="#b9fff0"/><stop offset="0.5" stop-color="#3fd6bd"/><stop offset="1" stop-color="#128e8c"/></radialGradient></defs>'
       '<rect width="176" height="176" fill="url(#sky)"/>')
    # soft wind ribbons in background
    d+=('<g fill="none" stroke="#c9fff6" stroke-linecap="round" opacity="0.35"><path d="M-4,60 Q40,40 80,66 T176,52" stroke-width="3"/>'
        '<path d="M-4,130 Q50,150 96,128 T180,140" stroke-width="3"/><path d="M0,98 Q30,86 60,100" stroke-width="2"/><path d="M120,24 Q146,12 170,28" stroke-width="2"/></g>')
    d+='<circle cx="88" cy="88" r="74" fill="url(#glow)"/>'
    # gold frame: 4-point star with concave sides, plus lower pendant
    d+=('<g><path d="M88,22 Q96,76 150,88 Q96,100 88,154 Q80,100 26,88 Q80,76 88,22Z" fill="url(#gold)"/>'
        '<path d="M88,32 Q95,78 138,88 Q95,98 88,144 Q81,98 38,88 Q81,78 88,32Z" fill="none" stroke="#fff6c8" stroke-width="1.2" opacity="0.7"/>'
        '<circle cx="88" cy="88" r="33" fill="url(#gold2)"/><circle cx="88" cy="88" r="29.5" fill="#8a5a14" opacity="0.55"/>'
        '<circle cx="88" cy="88" r="28" fill="url(#gem)"/>'
        '<path d="M70,78 Q80,66 96,68" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity="0.55"/></g>')
    # Anemo wind spiral
    d+=('<g fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M86,90 C83,84 91,79 96,84 C102,90 94,100 85,98 C75,96 73,83 80,77 C87,71 99,72 104,79" stroke-width="3.6"/>'
        '<path d="M104,79 C106,82 106,85 105,87" stroke-width="3.6"/></g>')
    d+=star(30,36,7,'#fff',0.95)+star(150,40,5,'#e8fffb',0.9)+star(144,138,8,'#fff',0.9)+star(34,142,4.5,'#e8fffb',0.85)
    return d

# ---- Disney+ castle night scene -----------------------------------------------------
def disney_castle():
    d=('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#071f4e"/><stop offset="0.5" stop-color="#0b4f86"/><stop offset="1" stop-color="#17b6c4"/></linearGradient>'
       '<linearGradient id="cs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#bfe9ef"/></linearGradient>'
       '<radialGradient id="mg" cx="0.5" cy="0.6" r="0.55"><stop offset="0" stop-color="#7fe8f2" stop-opacity="0.55"/><stop offset="1" stop-color="#7fe8f2" stop-opacity="0"/></radialGradient></defs>'
       '<rect width="176" height="176" fill="url(#sky)"/><circle cx="88" cy="112" r="84" fill="url(#mg)"/>')
    # fireworks arc (like logo arc) + sparkles
    d+='<path d="M30,86 A62,62 0 0 1 146,82" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity="0.92"/>'
    d+=star(146,80,0.1,'#fff',0)  # placeholder keeps order
    # castle silhouette
    c=('<g fill="url(#cs)">'
       '<rect x="20" y="118" width="136" height="40"/>'
       # central tall tower
       '<rect x="80" y="62" width="16" height="64"/><path d="M78,64 L88,22 L98,64Z"/>'
       # side towers
       '<rect x="52" y="84" width="12" height="44"/><path d="M50,86 L58,56 L66,86Z"/>'
       '<rect x="112" y="84" width="12" height="44"/><path d="M110,86 L118,56 L126,86Z"/>'
       '<rect x="30" y="100" width="10" height="30"/><path d="M28,102 L35,78 L42,102Z"/>'
       '<rect x="136" y="100" width="10" height="30"/><path d="M134,102 L141,78 L148,102Z"/>'
       '<rect x="68" y="98" width="40" height="30"/>'
       '</g>')
    d+=c
    # gate + windows (cut-outs in sky/teal colour)
    d+=('<path d="M80,158 L80,138 Q88,126 96,138 L96,158Z" fill="#0f6f97"/>'
        '<g fill="#0f6f97"><rect x="85" y="76" width="6" height="10" rx="3"/><rect x="55" y="98" width="6" height="9" rx="3"/><rect x="115" y="98" width="6" height="9" rx="3"/></g>')
    d+=star(88,14,7,'#fff')+star(150,48,6,'#e8fcff',0.95)+star(26,50,5,'#e8fcff',0.9)+star(42,22,3.2,'#fff',0.8)+star(134,24,3.2,'#fff',0.8)
    d+='<rect x="0" y="158" width="176" height="18" fill="#0a5f86"/>'
    return d
if __name__=='__main__':
    render(genshin_island(),'scene_genshin_island'); render(genshin_vision(),'scene_genshin_vision'); render(disney_castle(),'scene_disney_castle')
