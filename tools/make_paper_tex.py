#!/usr/bin/env python3
"""把實拍紙樣照片做成無縫「高度圖」紙紋，寫成 swatch/paper-tex.json 供 build.py 注入。
用法：python3 tools/make_paper_tex.py [--src ~/Downloads/paper-samples] [--out swatch/paper-tex.json] [--sheet /tmp/paper-sheet.jpg] [--size 512] [--pxmm 22]
流程：找一塊沒有印字的乾淨區域 → 灰階 → 去掉低頻光影 → 正規化 → 十字交叉淡入做成無縫 → WebP data URI；另估計紙色。
純 Pillow（沒有 numpy）。"""
import argparse, base64, io, json, pathlib, sys
from PIL import Image, ImageOps, ImageFilter, ImageChops, ImageDraw, ImageStat

# key: (檔名, crop)；crop='auto' 或 (x, y)＝原圖左上角座標（size 由 --size 決定）
MAP = {
  'sakemat':      ('DSC01423.png','auto'),   # 日本 酒墊紙
  'shinbaidai':   ('DSC01425.png','auto'),   # 英國 新百代 02
  'shinbaidai01': ('DSC01431.png','auto'),   # 英國 新百代 01
  'shinbaidai03': ('DSC01427.png','auto'),   # 英國 新百代 03（奶油色）
  'matisse':      ('DSC01432.png','auto'),   # 德國 馬諦斯 F6150
  'matisseF6149': ('DSC01433.png','auto'),
  'matisseF6107': ('DSC01434.png','auto'),
  'matisseF6146': ('DSC01435.png','auto'),
  'matisseF6172': ('DSC01426.png',(2600,100)),   # 避開壓凸字
  'beercard':     ('DSC01428.png','auto'),   # SS 啤酒卡
  'beercardA':    ('DSC01442.png','auto'),   # 特 A 啤酒卡
  'beerUS':       ('DSC01429.png','auto'),   # 美國 啤酒紙
  'scent':        ('DSC01436.png','auto'),   # 香氛紙
  'vanilla':      ('DSC01437.png','auto'),   # 香草紙
  'country':      ('DSC01438.png','auto'),   # 鄉村紙
  'cotton622':    ('DSC01440.png','auto'),   # 高級查冠純棉紙 622
  'chipboard':    ('DSC01441.png','auto'),   # 黃心模型紙板
}

def find_clean(im, size):
    """縮小 1/8，把彩色油墨／深色文字／陰影標成污染，掃方窗找最乾淨且亮度最平的區塊（偏好右下）。回傳原圖座標 (x,y)。"""
    s=8; sm=im.resize((im.width//s, im.height//s), Image.BILINEAR)
    W,H=sm.size; px=sm.load()
    L=ImageOps.grayscale(sm); med=ImageStat.Stat(L).median[0]
    bad=Image.new('L',(W,H),0); bp=bad.load(); lp=L.load()
    for y in range(H):
        for x in range(W):
            r,g,b=px[x,y]; sat=max(r,g,b)-min(r,g,b)
            if sat>18 or abs(lp[x,y]-med)>28: bp[x,y]=255
    bad=bad.filter(ImageFilter.MaxFilter(9))
    low=L.filter(ImageFilter.GaussianBlur(6))
    win=max(4,size//s); m=max(2,int(W*0.03))
    bp=bad.load(); lo=low.load()
    best=None
    step=max(1,win//4)
    for y in range(m, H-win-m, step):
        for x in range(m, W-win-m, step):
            cnt=0; vals=[]
            for yy in range(y,y+win,2):
                for xx in range(x,x+win,2):
                    if bp[xx,yy]: cnt+=1
                    vals.append(lo[xx,yy])
            mean=sum(vals)/len(vals); var=sum((v-mean)**2 for v in vals)/len(vals)
            cost=cnt*1e6+var*100 - (x+y)*0.01   # 同分偏右下
            if best is None or cost<best[0]: best=(cost,x,y)
    return best[1]*s, best[2]*s

def smoothstep(t): t=max(0.0,min(1.0,t)); return t*t*(3-2*t)

def seamless(v, band=48):
    """十字交叉淡入：把圖位移一半，接縫落到中線，再在中線 ±band 內與原圖交叉淡入。"""
    size=v.width; sh=ImageChops.offset(v, size//2, size//2)
    mask=Image.new('L',(size,size),0); mp=mask.load()
    for y in range(size):
        dy=abs(y-size//2)
        for x in range(size):
            dx=abs(x-size//2); d=min(dx,dy)
            mp[x,y]=int(255*(1-smoothstep(d/band)))
    # 中線附近用「原圖」（原圖在中線處是連續的），其餘用位移圖（位移圖在邊緣連續）
    return Image.composite(v, sh, mask)

def height_map(crop, blur=40, target_sigma=40):
    g8=ImageOps.grayscale(crop)
    low=g8.filter(ImageFilter.GaussianBlur(blur)); low=low.filter(ImageFilter.GaussianBlur(blur))  # 兩次 ≈ 大半徑
    gp=g8.load(); lp=low.load(); W,H=g8.size
    vals=[gp[x,y]-lp[x,y] for y in range(0,H,2) for x in range(0,W,2)]
    mean=sum(vals)/len(vals); sigma=(sum((v-mean)**2 for v in vals)/len(vals))**0.5 or 1
    k=target_sigma/sigma
    out=Image.new('L',(W,H)); op=out.load()
    for y in range(H):
        for x in range(W):
            op[x,y]=int(max(0,min(255, 128+(gp[x,y]-lp[x,y]-mean)*k)))
    return out, sigma

def encode(im, limit=56000):
    for q in (78,68,58,50,42):
        buf=io.BytesIO(); im.convert('RGB').save(buf,'WEBP',quality=q,method=6); b=buf.getvalue()
        if len(b)<=limit: return 'data:image/webp;base64,'+base64.b64encode(b).decode(), len(b), f'webp q{q}'
    buf=io.BytesIO(); im.save(buf,'PNG',optimize=True); b=buf.getvalue()
    return 'data:image/png;base64,'+base64.b64encode(b).decode(), len(b), 'png'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--src',default=str(pathlib.Path.home()/'Downloads'/'paper-samples')); ap.add_argument('--out',default=str(pathlib.Path(__file__).resolve().parent.parent/'swatch'/'paper-tex.json'))
    ap.add_argument('--sheet',default=None); ap.add_argument('--size',type=int,default=512); ap.add_argument('--pxmm',type=float,default=22.0); ap.add_argument('--only',default=None)
    a=ap.parse_args(); src=pathlib.Path(a.src)
    if a.sheet:
        fs=sorted(src.glob('*.png'))+sorted(src.glob('*.jpg')); W=480; tiles=[]
        for f in fs:
            im=ImageOps.exif_transpose(Image.open(f)).convert('RGB'); im.thumbnail((W,W)); tiles.append((f.name,im))
        cols=4; rows=(len(tiles)+cols-1)//cols; h=max(t.height for _,t in tiles)+18
        sheet=Image.new('RGB',(cols*W,rows*h),(30,30,30)); d=ImageDraw.Draw(sheet)
        for i,(n,t) in enumerate(tiles): x=(i%cols)*W; y=(i//cols)*h; sheet.paste(t,(x,y+18)); d.text((x+4,y+3),n,fill=(255,255,255))
        sheet.save(a.sheet,quality=85); print('→',a.sheet); return
    out={}; old={}
    op=pathlib.Path(a.out)
    if op.exists():
        try: old=json.loads(op.read_text())
        except Exception: old={}
    print(f'{"key":14} {"file":14} {"crop":>14} {"color":8} {"KB":>6}  fmt   sigma')
    for key,(fname,crop) in MAP.items():
        if a.only and key not in a.only.split(','): 
            if key in old: out[key]=old[key]
            continue
        f=src/fname
        if not f.exists(): print(key,'缺檔案',f); continue
        im=ImageOps.exif_transpose(Image.open(f)).convert('RGB')
        if crop=='auto': x,y=find_clean(im,a.size)
        else: x,y=crop
        x=max(0,min(im.width-a.size,x)); y=max(0,min(im.height-a.size,y))
        c=im.crop((x,y,x+a.size,y+a.size))
        hm,sigma=height_map(c); hm=seamless(hm)
        uri,nbytes,fmt=encode(hm)
        small=c.resize((64,64),Image.BOX); med=ImageStat.Stat(small).median; color='#%02x%02x%02x'%tuple(med[:3])
        out[key]={'uri':uri,'mm':round(a.size/a.pxmm,1),'color':color,'src':fname,'crop':[x,y,a.size],'sigma':round(sigma,1)}
        print(f'{key:14} {fname:14} {str((x,y)):>14} {color:8} {nbytes/1024:6.1f}  {fmt}  {sigma:.1f}')
    op.write_text(json.dumps(out,ensure_ascii=False))
    print('→',op, f'{op.stat().st_size/1024:.0f} KB')

if __name__=='__main__': main()
