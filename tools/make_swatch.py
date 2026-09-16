#!/usr/bin/env python3
"""產生效果樣本卡（每一類一張，比較省效能）：swatch/swatch-foil.svg、swatch-holo.svg、swatch-ink.svg、swatch-finish.svg。
五張（燙箔金屬色／燙箔純色／燙雷射／油墨／表面處理），每張 105×55mm 橫式（viewBox 單位 0.1mm），每格是一個依「工法_色碼+加工」命名的 <g>，載入燙印打樣室會自動建立對應效果。
logo.svg 存在時嵌入右上角。"""
import pathlib, re, math, json
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/'swatch'; OUT.mkdir(exist_ok=True)
W,H=1050,550
CELL,GAP=92,14; SQ_H=62; PITCH=124
PAPER='#141414'

metals=[('亮金 G-22','#c9a640'),('青口亮金 G-24','#d1c26c'),('紅口亮金 G-31','#c99a34'),('紅口亮金 G-40','#c39b2c'),('亮紅金 RE-90','#c31420'),('亮古銅金 CG-45','#c67c3c'),('玫瑰金 CG-71','#cf9d8a'),('亮黑 CK-11','#2b2b31'),('亮銀 S-01','#c9cbcd'),
        ('青口霧金 MG-22','#e3c463'),('霧金 MG-04','#e2a94a'),('霧淺古銅金 MG-25','#d8a17c'),('霧深古銅金 MG-76','#e28a5f'),('霧黑 8800','#141416'),('霧鐵灰 CK-10','#7b7672'),('霧銀 MS-03','#c7cbcb'),('霧銀 MS-01','#d3d7d8'),('霧白 7801','#f4f4f2')]
pigments=[('亮紅','#d1202c'),('亮橘','#e0581c'),('亮粉','#e56a9a'),('亮紫','#5b2d8e'),('亮藍','#2f56b5'),('亮湖水綠','#1f8f8a'),('亮綠','#1f7a4d'),
          ('霧紅','#c8303a'),('霧橘','#d9602a'),('霧粉','#e07aa3'),('霧紫','#63397f'),('霧藍','#3b5ea8'),('霧湖水綠','#2d8c88'),('霧綠','#2d7a53')]
holos=[('線條','#888888'),('直條反轉','#888888'),('放射交叉','#888888'),('彩虹','#888888'),('幻彩流動','#888888'),('碎片亮粉','#888888'),('金蔥亮粉','#b8924a'),
       ('星空宇宙','#888888'),('星塵線條','#888888'),('閃鑽 V','#888888'),('碎冰','#888888'),('碎鑽','#888888'),('砂點','#888888'),('皺紋','#888888'),('星芒','#888888'),('珍珠箔','#f1eff0'),('透明','#ffffff')]
inks=[('白墨','#f3f1ec'),('黑墨','#161616'),('銀墨','#a9abae'),('金墨','#b8975a'),('古銅墨','#8f6b4d'),('玫瑰金墨','#b48a7f'),('香檳金墨','#c8b48e'),
      ('185C','#e4002b'),('專色黃','#fedd00'),('877C','#9a9c9e'),('871C','#9b8557'),('806C','#ff3eb5'),('811C','#ff6a39'),('803C','#ffe900')]
fins=[('亮面UV','亮面 UV'),('霧面UV','霧面 UV'),('磨砂UV','磨砂 UV'),('立體UV','立體 UV'),('亮粉UV','亮粉 UV'),('打凸','打凸'),('打凹','打凹')]

CARDS=[ # (檔名, 標題, 項目, 類型)
  ('swatch-foil-metal.svg',   '燙箔 · 金屬色  METALLIC FOIL',  metals,   'foil'),
  ('swatch-foil-pigment.svg', '燙箔 · 純色  PIGMENT FOIL',     pigments, 'foil'),
  ('swatch-holo.svg',         '燙雷射  HOLOGRAPHIC FOIL',      holos,    'holo'),
  ('swatch-ink.svg',          '油墨  INK · METALLIC · SPOT · FLUO', inks, 'ink'),
  ('swatch-finish.svg',       '表面處理  FINISHES',            fins,     'fin'),
]

def esc(s): return s.replace('&','&amp;').replace('<','&lt;')
def cell(gid, fill, x, y, label):
    r=[f'  <g id="{esc(gid)}">',
       f'    <rect x="{x}" y="{y}" width="{CELL}" height="{SQ_H}" rx="6" fill="{fill}"/>',
       f'    <line x1="{x+6}" y1="{y+SQ_H+9}" x2="{x+CELL-22}" y2="{y+SQ_H+9}" stroke="{fill}" stroke-width="0.8"/>']
    cx,cy,ro,ri=x+CELL-9,y+SQ_H+9,6,2.6; pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; rad=ro if i%2==0 else ri
        pts.append(f'{cx+rad*math.cos(a):.1f},{cy+rad*math.sin(a):.1f}')
    r.append(f'    <polygon points="{" ".join(pts)}" fill="{fill}"/>')
    r.append('  </g>')
    lab=f'    <text x="{x}" y="{y+SQ_H+30}" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#f3f1ec">{esc(label)}</text>'
    return '\n'.join(r), lab

logo_inner=None
lp=ROOT/'logo.svg'
if lp.exists():
    src=lp.read_text(); vb=re.search(r'viewBox="([^"]+)"',src).group(1).split(); vx,vy,vw,vh=map(float,vb)
    logo_inner=(re.sub(r'^.*?<svg[^>]*>','',src,flags=re.S).replace('</svg>','').strip(), vx,vy,vw,vh)

def make(fname, title, items, kind):
    cols = min(9, (len(items)+1)//2)     # 固定兩列
    rows=(len(items)+cols-1)//cols
    gx=(W-(cols*CELL+(cols-1)*GAP))//2
    y0=220                                # 標題線下方置中
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         f'  <g id="刀模"><rect x="0" y="0" width="{W}" height="{H}" rx="24" fill="none" stroke="#ff5511" stroke-width="1"/></g>',
         f'  <g id="紙_新百代 {PAPER}"><rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/></g>']
    labels=[]
    for i,(name,val) in enumerate(items):
        col=i%cols; row=i//cols; x=gx+col*(CELL+GAP); yy=y0+row*PITCH
        if kind=='foil': gid=f'燙箔_{name}'; fill=val; lab=name
        elif kind=='holo': gid=f'燙雷射_{name}'; fill=val; lab=name
        elif kind=='ink': gid=f'印刷_{name}'; fill=val; lab=name
        else: gid=f'加工_{name}'; fill=PAPER; lab=val
        g,l=cell(gid,fill,x,yy,lab); out.append(g); labels.append(l)
    logo=''
    if logo_inner:
        inner,vx,vy,vw,vh=logo_inner; bw,bh=240,56; k=min(bw/vw,bh/vh); lx=W-56-vw*k; ly=44
        logo=f'    <g id="logo" transform="translate({lx:.1f} {ly:.1f}) scale({k:.5f}) translate({-vx} {-vy})" fill="#b9bbc2">{inner}</g>'
    mx=56
    out.append(f'''  <g id="燙箔_霧銀 MS-03">
    <text x="{mx}" y="82" font-family="Georgia, 'Times New Roman', serif" font-size="36" letter-spacing="5" fill="#b9bbc2">FOIL PROOF</text>
    <text x="{mx}" y="106" font-family="Helvetica, Arial, sans-serif" font-size="12" letter-spacing="3" fill="#b9bbc2">{esc(title)} · {len(items)} SWATCHES</text>
    <line x1="{mx}" y1="122" x2="{W-mx}" y2="122" stroke="#b9bbc2" stroke-width="0.8"/>
{logo}
  </g>''')
    out.append('  <g id="印刷_白墨 標籤">'); out+=labels
    out.append(f'    <text x="{mx}" y="{H-22}" font-family="Helvetica, Arial, sans-serif" font-size="10" letter-spacing="2" fill="#f3f1ec">MMXXVI · FOIL PROOF LAB · NALDO.DESIGN · instagram.com/naldo.design</text>')
    out.append('  </g>'); out.append('</svg>')
    s='\n'.join(out)+'\n'; (OUT/fname).write_text(s); print('→',OUT/fname, len(s),'bytes,',len(items),'cells, y0=',y0); return s

bundle={fname: make(fname,title,items,kind) for fname,title,items,kind in CARDS}
(OUT/'swatches.json').write_text(json.dumps(bundle, ensure_ascii=False))
print('→',OUT/'swatches.json')
