#!/usr/bin/env python3
"""從 foil-proof.template.html 產出 index.html（注入效果樣本卡；沒有內建設計稿，啟動時顯示上傳／樣本卡）。
用法：python3 tools/build.py [額外輸出.html]
"""
import pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parent.parent
T=(ROOT/'foil-proof.template.html').read_text()
LINK='原始碼：<a href="https://github.com/naldo-w/foil-proof-lab" target="_blank" rel="noopener">github.com/naldo-w/foil-proof-lab</a>'
def build(svg,name,credit,out,wrap):
    sw=ROOT/'swatch'/'swatches.json'; swatch=sw.read_text() if sw.exists() else '{}'  # 每類一張的樣本卡（tools/make_swatch.py）
    s=T.replace('__SWATCH_SVG__',swatch).replace('__SAMPLE_CREDIT__',credit).replace('__SOURCE_LINK__',LINK)
    if wrap: s='<!doctype html>\n<html lang="zh-Hant">\n'+s
    pathlib.Path(out).write_text(s); print('→',out)
build(None,'','效果樣本卡（swatch/*.svg）為本工具自製的示範圖，隨程式碼一併以 MIT 授權釋出。',ROOT/'index.html',True)
if len(sys.argv)>=2: build(None,'','效果樣本卡（swatch/*.svg）為本工具自製的示範圖，隨程式碼一併以 MIT 授權釋出。',sys.argv[1],False)
