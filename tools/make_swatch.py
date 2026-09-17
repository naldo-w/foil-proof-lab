#!/usr/bin/env python3
"""產生效果樣本卡（每一類一張）：swatch/swatch-foil-metal.svg、swatch-foil-pigment.svg、swatch-holo.svg、swatch-ink.svg、swatch-finish.svg 與 swatches.json。
版面（單位 px，1px = 1/96 in）：
  上：左 logo、右 樣本卡標題（字高＝logo 高）
  中：樣本 80×80（形狀取自 swatch/sample-shape.svg），一行 4 個、間距 16，名稱 16px 置中在樣本下方
  下：FOIL PROOF LAB 8px 置中
  上中下間距 40；四邊留白 40；圓角 40；卡片依內容決定大小；紙：黑色銅版紙 0.5mm
每格是一個依「工法_色碼+加工」命名的 <g>，載入燙印打樣室會自動建立對應效果。"""
import pathlib, re, json
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/'swatch'; OUT.mkdir(exist_ok=True)
PAD=40; GAP=40; CELL=80; CGAP=16; COLS=4; NAME=16; NAME2=11; NAME_GAP=8; FOOT=8; LOGO_H=24; RADIUS=40
def tw(t,fs): return sum((fs if ord(c)>0x2e7f else fs*0.58) for c in t)  # 估字寬：CJK 1em、拉丁 0.58em
PAPER='#121212'
W=PAD*2+COLS*CELL+(COLS-1)*CGAP   # 448

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

# 樣本形狀：取 sample-shape.svg 裡的 path
shape_src=(OUT/'sample-shape.svg').read_text()
SHAPE_D=re.search(r'<path d="([^"]+)"', shape_src).group(1)
SHAPE_VB=re.search(r'viewBox="([^"]+)"', shape_src).group(1).split(); SHAPE_S=float(SHAPE_VB[2])

logo_inner=None
lp=ROOT/'logo.svg'
if lp.exists():
    src=lp.read_text(); vb=re.search(r'viewBox="([^"]+)"',src).group(1).split(); vx,vy,vw,vh=map(float,vb)
    logo_inner=(re.sub(r'^.*?<svg[^>]*>','',src,flags=re.S).replace('</svg>','').strip(), vx,vy,vw,vh)

def cell(gid, fill, x, y):
    k=CELL/SHAPE_S
    return f'  <g id="{esc(gid)}"><path transform="translate({x} {y}) scale({k:.5f})" d="{SHAPE_D}" fill="{fill}"/></g>'

def make(fname, title, items, kind):
    rows=(len(items)+COLS-1)//COLS
    row_h=CELL+NAME_GAP+NAME+NAME2+2
    grid_h=rows*row_h+(rows-1)*CGAP
    H=PAD+LOGO_H+GAP+grid_h+GAP+FOOT+PAD
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         f'  <g id="刀模"><rect x="0" y="0" width="{W}" height="{H}" rx="{RADIUS}" fill="none" stroke="#ff5511" stroke-width="1"/></g>',
         f'  <g id="紙_銅版紙 {PAPER} 0.5mm"><rect x="0" y="0" width="{W}" height="{H}" rx="{RADIUS}" fill="{PAPER}"/></g>']
    labels=[]
    y0=PAD+LOGO_H+GAP
    for i,(name,val) in enumerate(items):
        col=i%COLS; row=i//COLS; x=PAD+col*(CELL+CGAP); yy=y0+row*(row_h+CGAP)
        if kind=='foil': gid=f'燙箔_{name}'; fill=val; lab=name
        elif kind=='holo': gid=f'燙雷射_{name}'; fill=val; lab=name
        elif kind=='ink': gid=f'印刷_{name}'; fill=val; lab=name
        else: gid=f'加工_{name}'; fill=PAPER; lab=val
        out.append(cell(gid,fill,x,yy))
        # 名稱：有編號就拆兩行（名稱 16px、編號 11px），超寬的名稱自動縮字
        m=re.match(r'^(.*?)\s+([A-Z]{1,3}-?\d+|\d{4})$', lab)
        name, code = (m.group(1), m.group(2)) if m else (lab, '')
        fs=NAME; maxw=CELL+CGAP-4
        while tw(name,fs)>maxw and fs>9: fs-=1
        ty=yy+CELL+NAME_GAP+fs*0.85
        labels.append(f'    <text x="{x+CELL/2}" y="{ty:.1f}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="{fs}" fill="#f3f1ec">{esc(name)}</text>')
        if code: labels.append(f'    <text x="{x+CELL/2}" y="{ty+NAME2+2:.1f}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="{NAME2}" letter-spacing=".5" fill="#c9c7c2">{esc(code)}</text>')
    logo=''
    if logo_inner:
        inner,vx,vy,vw,vh=logo_inner; k=LOGO_H/vh
        logo=f'    <g id="logo" transform="translate({PAD} {PAD}) scale({k:.5f}) translate({-vx} {-vy})" fill="#b9bbc2">{inner}</g>'
    logo_w = LOGO_H*(logo_inner[3]/logo_inner[4]) if logo_inner else 0
    tfs=LOGO_H; avail=W-PAD*2-logo_w-16
    while tw(title,tfs)>avail and tfs>10: tfs-=1
    out.append(f'''  <g id="燙箔_霧銀 MS-03">
{logo}
    <text x="{W-PAD}" y="{PAD+LOGO_H*0.86:.1f}" text-anchor="end" font-family="Helvetica, Arial, sans-serif" font-size="{tfs}" letter-spacing=".5" fill="#b9bbc2">{esc(title)}</text>
  </g>''')
    out.append('  <g id="印刷_白墨 標籤">'); out+=labels
    out.append(f'    <text x="{W/2}" y="{H-PAD:.1f}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="{FOOT}" letter-spacing="2" fill="#f3f1ec">FOIL PROOF LAB</text>')
    out.append('  </g>'); out.append('</svg>')
    s='\n'.join(out)+'\n'; (OUT/fname).write_text(s); print('→',OUT/fname, f'{W}×{H}px', len(items),'cells'); return s

bundle={fname: make(fname,title,items,kind) for fname,title,items,kind in CARDS}
(OUT/'swatches.json').write_text(json.dumps(bundle, ensure_ascii=False))
print('→',OUT/'swatches.json')
