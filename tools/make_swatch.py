#!/usr/bin/env python3
"""產生效果樣本卡 swatch-card.svg（A6 橫式 148×105mm，viewBox 單位 0.1mm）。
每格是一個依「工法 · 顏色 + 加工」命名的 <g>，載入燙印打樣室會自動建立對應效果。
logo.svg 存在時嵌入右上角。"""
import pathlib, re
ROOT=pathlib.Path(__file__).resolve().parent.parent
W,H=1480,1050
CELL,GAP=92,14; SQ_H=62; PITCH=124
COLS=8; GX=(W-(COLS*CELL+(COLS-1)*GAP))//2
PAPER='#141414'

foils=[('銀','#c9cacf'),('金','#d3a84a'),('香檳金','#d9c39a'),('玫瑰金','#d9a091'),('古銅','#b87333'),('紅','#d1202c'),('橘','#e0581c'),('粉','#e56a9a'),
       ('紫','#5b2d8e'),('藍','#2f56b5'),('湖水綠','#1f8f8a'),('綠','#1f7a4d'),('白','#f2f2f4'),('黑','#2b2b30'),('霧銀','#b9bbc2'),('霧金','#c9a75a')]
holos=[('線條','#cfd0d6'),('直條反轉','#d4d4da'),('放射交叉','#d6d6dc'),('彩虹','#dcdce2'),('幻彩流動','#cfd2dc'),('碎片亮粉','#c9c9cf'),('金蔥亮粉','#d4a84a'),
       ('星空宇宙','#aeb2c2'),('星塵線條','#c9ccd6'),('閃鑽 V','#d8d8de'),('碎冰','#d0d2da'),('珍珠箔','#f1eff0'),('透明','#ffffff')]
inks=[('白墨','#f3f1ec'),('185C','#e4002b'),('專色黃','#fedd00'),('877C','#9a9c9e'),('871C','#9b8557'),('806C','#ff3eb5'),('811C','#ff6a39'),('803C','#ffe900')]
fins=[('亮面UV','亮面 UV'),('霧面UV','霧面 UV'),('磨砂UV','磨砂 UV'),('立體UV','立體 UV'),('亮粉UV','亮粉 UV'),('打凸','打凸'),('打凹','打凹')]

def esc(s): return s.replace('&','&amp;').replace('<','&lt;')
def cell(gid, fill, x, y, label, star=True):
    r=[f'  <g id="{esc(gid)}">',
       f'    <rect x="{x}" y="{y}" width="{CELL}" height="{SQ_H}" rx="6" fill="{fill}"/>',
       f'    <line x1="{x+6}" y1="{y+SQ_H+9}" x2="{x+CELL-22}" y2="{y+SQ_H+9}" stroke="{fill}" stroke-width="0.8"/>']
    if star:
        cx,cy,ro,ri=x+CELL-9,y+SQ_H+9,6,2.6
        pts=[]
        import math
        for i in range(10):
            a=-math.pi/2+i*math.pi/5; rad=ro if i%2==0 else ri
            pts.append(f'{cx+rad*math.cos(a):.1f},{cy+rad*math.sin(a):.1f}')
        r.append(f'    <polygon points="{" ".join(pts)}" fill="{fill}"/>')
    r.append('  </g>')
    lab=f'    <text x="{x}" y="{y+SQ_H+30}" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#f3f1ec">{esc(label)}</text>'
    return '\n'.join(r), lab

out=[]; labels=[]; headers=[]
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
out.append(f'  <g id="刀模"><rect x="0" y="0" width="{W}" height="{H}" rx="30" fill="none" stroke="#ff5511" stroke-width="1"/></g>')
out.append(f'  <g id="紙 · 新百代 {PAPER}"><rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/></g>')
y=175
def section(title, items, kind):
    global y
    headers.append(f'    <text x="{GX}" y="{y-8}" font-family="Helvetica, Arial, sans-serif" font-size="13" letter-spacing="2" fill="#f3f1ec">{esc(title)}</text>')
    for i,(name,val) in enumerate(items):
        col=i%COLS; row=i//COLS
        x=GX+col*(CELL+GAP); yy=y+row*PITCH
        if kind=='foil': gid=f'燙箔 · {name}'; fill=val; lab=f'燙{name}'
        elif kind=='holo': gid=f'燙雷射 · {name}'; fill=val; lab=name
        elif kind=='ink': gid=f'印刷 · {name}'; fill=val; lab=name
        else: gid=f'加工 · {name}'; fill=PAPER; lab=val
        g,l=cell(gid,fill,x,yy,lab); out.append(g); labels.append(l)
    rows=(len(items)+COLS-1)//COLS
    y+=rows*PITCH+22
section('燙箔  HOT FOIL', foils, 'foil')
section('燙雷射  HOLOGRAPHIC FOIL', holos, 'holo')
section('油墨  INK · SPOT · METALLIC · FLUO', inks, 'ink')
section('表面處理  FINISHES', fins, 'fin')
# 標題與 logo（燙霧銀）
logo=''
lp=ROOT/'logo.svg'
if lp.exists():
    src=lp.read_text(); vb=re.search(r'viewBox="([^"]+)"',src).group(1).split(); vx,vy,vw,vh=map(float,vb)
    inner=re.sub(r'^.*?<svg[^>]*>','',src,flags=re.S).replace('</svg>','').strip()
    bw,bh=300,70; k=min(bw/vw,bh/vh); lx=W-60-vw*k; ly=60
    logo=f'    <g id="logo" transform="translate({lx:.1f} {ly:.1f}) scale({k:.5f}) translate({-vx} {-vy})" fill="#b9bbc2">{inner}</g>'
title=f'''  <g id="燙箔 · 霧銀">
    <text x="{GX}" y="100" font-family="Georgia, 'Times New Roman', serif" font-size="44" letter-spacing="6" fill="#b9bbc2">FOIL PROOF</text>
    <text x="{GX}" y="128" font-family="Helvetica, Arial, sans-serif" font-size="13" letter-spacing="4" fill="#b9bbc2">效果樣本  EFFECT SWATCHES · 44 FINISHES</text>
    <line x1="{GX}" y1="145" x2="{W-GX}" y2="145" stroke="#b9bbc2" stroke-width="0.8"/>
{logo}
  </g>'''
out.append(title)
out.append('  <g id="印刷 · 白墨 標籤">')
out+=headers; out+=labels
out.append(f'    <text x="{GX}" y="{H-32}" font-family="Helvetica, Arial, sans-serif" font-size="11" letter-spacing="2" fill="#f3f1ec">MMXXVI · FOIL PROOF LAB · NALDO.DESIGN · instagram.com/naldo.design</text>')
out.append('  </g>')
out.append('</svg>')
(ROOT/'swatch-card.svg').write_text('\n'.join(out)+'\n')
print('→ swatch-card.svg', len('\n'.join(out)), 'bytes, grid ends y=', y)
