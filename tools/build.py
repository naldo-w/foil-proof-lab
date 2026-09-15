#!/usr/bin/env python3
"""從 foil-proof.template.html 產出兩個版本：
  index.html        公開版（內建 sample-card.svg，GitHub Pages）
  <private>.html    私人版（內建指定的設計稿，不進 repo）
用法：python3 tools/build.py [私人設計稿.svg] [私人輸出.html]
"""
import pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parent.parent
T=(ROOT/'foil-proof.template.html').read_text()
LINK='原始碼：<a href="https://github.com/naldo-w/foil-proof-lab" target="_blank" rel="noopener">github.com/naldo-w/foil-proof-lab</a>'
def build(svg,name,credit,out,wrap):
    s=T.replace('__SAMPLE_SVG__',pathlib.Path(svg).read_text()).replace('__SAMPLE_NAME__',name).replace('__SAMPLE_CREDIT__',credit).replace('__SOURCE_LINK__',LINK)
    if wrap: s='<!doctype html>\n<html lang="zh-Hant">\n'+s
    pathlib.Path(out).write_text(s); print('→',out)
build(ROOT/'sample-card.svg','sample-card.svg','內建範例卡為本工具自製的示範圖，隨程式碼一併以 MIT 授權釋出。',ROOT/'index.html',True)
if len(sys.argv)>=3:
    svg=pathlib.Path(sys.argv[1]); build(svg,svg.name,'內建的設計稿 © NALDO.DESIGN，保留所有權利，僅供本工具示範，不含在 MIT 授權範圍內，未經許可不得使用、複製或散布。',sys.argv[2],False)
