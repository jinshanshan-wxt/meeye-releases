import sys, base64, io, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_icons as B, meeye_style as ms
from trace import mask_to_path
sq,_=mask_to_path(ms.SHAPE>0.5,up=4,blur=0.6)
def svg_for(name,v):
    head='<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="192" height="192" viewBox="0 0 192 192">'
    defs=['<filter id="sh" x="-10%" y="-10%" width="120%" height="125%"><feGaussianBlur in="SourceAlpha" stdDeviation="3.5"/><feOffset dy="2"/><feComponentTransfer><feFuncA type="linear" slope="0.32"/></feComponentTransfer></filter>',
          '<filter id="gs" x="-20%" y="-20%" width="140%" height="150%"><feGaussianBlur in="SourceAlpha" stdDeviation="5"/><feOffset dy="4"/><feComponentTransfer><feFuncA type="linear" slope="0.25"/></feComponentTransfer></filter>',
          f'<clipPath id="sq"><path d="{sq}"/></clipPath>']
    body=[f'<path d="{sq}" filter="url(#sh)"/>']
    if v['glyph'] is None:   # art icon: embed raster
        b=io.BytesIO(); 
        src=None
        im=B.load(src).resize((176,176)); im.save(b,'PNG')
        body.append(f'<g clip-path="url(#sq)"><image x="8" y="8" width="176" height="176" xlink:href="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}"/></g>')
    else:
        if v['stops']:
            stops=''.join(f'<stop offset="{t}" stop-color="{c}"/>' for t,c in v['stops']); y2=176
        else:
            stops=f'<stop offset="0" stop-color="{v["bg"][0]}"/><stop offset="1" stop-color="{v["bg"][1]}"/>'; y2=146
        defs.append(f'<linearGradient id="bg" gradientUnits="userSpaceOnUse" x1="0" y1="8" x2="0" y2="{y2}">{stops}</linearGradient>')
        body.append(f'<path d="{sq}" fill="url(#bg)"/>')
        g=v['glyph']
        if v['tint']:
            a=ms.glyph_alpha(g) if 'url(' not in g else None
            ys=np.where(ms.glyph_alpha(g).max(1)>0.5)[0]
            defs.append(f'<linearGradient id="gg" gradientUnits="userSpaceOnUse" x1="0" y1="{ys.min()}" x2="0" y2="{ys.max()}"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="{v["tint"]}"/></linearGradient>')
            body.append(f'<g filter="url(#gs)" fill="#000" clip-path="url(#sq)">{g}</g><g fill="url(#gg)">{g}</g>')
        else:
            body.append(f'<g filter="url(#gs)" clip-path="url(#sq)">{g}</g>{g}')
        if v['defs']: defs.append(v['defs'])
    body.append(f'<path d="{sq}" fill="none" stroke="#fff" stroke-opacity="0.22" stroke-width="1.2"/>')
    return head+'<defs>'+''.join(defs)+'</defs>'+''.join(body)+'</svg>'
if __name__=='__main__':
    import cairosvg
    for n,v in B.icons.items():
        s=svg_for(n,v); open(B.OUT+n+'.svg','w').write(s)
        check_dir=os.path.join(B.OUT, "svg_render_check")
        os.makedirs(check_dir, exist_ok=True)
        cairosvg.svg2png(bytestring=s.encode(),write_to=os.path.join(check_dir, n+'_svgcheck.png'),output_width=192,output_height=192)
    print('svgs ok')
