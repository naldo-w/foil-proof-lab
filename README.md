# 燙印打樣室 · Foil Proof Lab

**線上使用：https://naldo-w.github.io/foil-proof-lab/**

在瀏覽器裡把 SVG 設計稿模擬成紙本印刷打樣：燙銀、燙金、燙紅、燙玫瑰金、全息銀、專色油墨、白墨、局部上光、打凹／打凸，
再平鋪多張、換視角，匯出 IG／FB 尺寸的 mockup PNG。純前端單一 HTML，不需要安裝、不需要伺服器。

## 功能

- **上傳 SVG**（拖放或選檔），自動偵測顏色：預設「相同顏色 → 相同效果」，滿版底色矩形自動當成紙色
- **三種指派方式**：依顏色、依 SVG 圖層（具名 `<g>`）、直接在畫面上點（元素／群組／圖層／同色）
- **紙張**：15 種紙質（銅版、雪銅、珠光、象牙卡、蛋殼紋、水彩紙、雲彩紙、萊妮、條紋、麻布、皮紋、鎚目、牛皮、再生、毛氈），紋理以 feTurbulence 高度圖＋feDiffuseLighting 打光生成；可調紋理強度、凹凸深度、顆粒、尺寸、光源角度、混合模式、光澤
- **效果參數**：箔色、亮度、全息、髮絲紋、光澤；油墨濃度與混合模式；打凹深度
- **版面 Mockup**：1080×1080 / 1080×1350 / 1080×1440 / 1080×1920 / 16:9 / A4 或自訂；
  單張、整齊、錯開、隨機、扇形、階梯六種鋪法；正上方／俯 30°／俯 45°／左右前 45°／等角等視角；
  光源跟著滑鼠走，每張卡片各自反光與投影
- **匯出 PNG**（1× / 2×），設定自動存在瀏覽器 localStorage

## 原理

每個效果圖層是一個 `div`：箔面漸層 + 全息 + glare 多層 `mix-blend-mode`，
再用「只保留該圖層元素、全部填白」的 SVG 當 CSS `mask-image`，所以任何路徑、文字、描邊都能套用。

## 建議

- 文字請先在 Illustrator／Affinity **建立外框**再上傳，否則會以系統字型顯示
- 匯出請用 Chrome／Edge；Safari 對 `foreignObject` + `mask` 支援不完整
- 畫面效果為視覺近似，實際成品以印刷廠打樣為準

## 版權與授權

- 程式碼 © 2026 n_do（[naldo-w](https://github.com/naldo-w)），以 [MIT License](LICENSE) 釋出。
- 內建範例卡 `sample-card.svg` 為本工具自製示範圖，同樣以 MIT 授權釋出。
- 卡片傾斜、反光與全息效果的手法參考 [pokemon-cards-css](https://github.com/simeydotme/pokemon-cards-css)（© simeydotme，MIT License）。
- 介面字型 IBM Plex、Noto Sans TC（SIL Open Font License），由 Google Fonts 載入。
- 使用者上傳的 SVG 只在本機瀏覽器處理，不會傳送到任何伺服器；其著作權仍屬原設計者所有。
