#!/usr/bin/env python3
"""從 foil-proof.template.html 產出兩個版本：
  index.html        公開版（無內建設計稿，啟動顯示上傳／樣本卡；GitHub Pages）
  <private>.html    私人版（內建指定的設計稿，不進 repo）
用法：python3 tools/build.py [私人設計稿.svg] [私人輸出.html]
"""
import pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parent.parent
T=(ROOT/'foil-proof.template.html').read_text()
LINK='原始碼：<a href="https://github.com/naldo-w/foil-proof-lab" target="_blank" rel="noopener">github.com/naldo-w/foil-proof-lab</a>'
def build(svg,name,credit,out,wrap):
    sw=ROOT/'swatch'/'swatches.json'; swatch=sw.read_text() if sw.exists() else '{}'  # 每類一張的樣本卡（tools/make_swatch.py）
    sample=pathlib.Path(svg).read_text() if svg else ''  # 沒有內建設計稿 → 啟動時顯示空狀態（上傳／樣本卡）
    s=T.replace('__SAMPLE_SVG__',sample).replace('__SWATCH_SVG__',swatch).replace('__SAMPLE_NAME__',name).replace('__SAMPLE_CREDIT__',credit).replace('__SOURCE_LINK__',LINK)
    if wrap: s='<!doctype html>\n<html lang="zh-Hant">\n'+s
    pathlib.Path(out).write_text(s); print('→',out)
build(None,'','效果樣本卡（swatch/*.svg）為本工具自製的示範圖，隨程式碼一併以 MIT 授權釋出。',ROOT/'index.html',True)
if len(sys.argv)>=3:
    svg=pathlib.Path(sys.argv[1]); build(svg,svg.name,'內建的設計稿 © NALDO.DESIGN，保留所有權利，僅供本工具示範，不含在 MIT 授權範圍內，未經許可不得使用、複製或散布。',sys.argv[2],False)
