# IMPLEMENTATION_PLAN — 分階段實作計畫

原則：沿用現有架構，不全面重寫；先統一、再擴充；每一階段都可以獨立交付與回退。

## 1. 差距總表

| 規範要求 | 現況 | 差距 | 優先級 |
|---|---|---|---|
| AM 網點與網角 | ✓（點陣） | 向量版另一套近似 → 需統一 | P0 |
| 網點形狀 | 只有圓 | 缺 6 種 | P0 |
| FM | ✓（孔版顆粒） | 柯式沒有 FM；藍雜訊貼圖周期太小 | P0 |
| 色調曲線 | ✗ | 線性、gamma、自訂 | P0 |
| 網點擴大 | ✓ | 兩套式子 → 統一 | P0 |
| CMYK 分色 | △ | 缺 GCR、TAC | P1 |
| 疊印 | △ | 在 sRGB 相乘 → 改為線性；不透明墨 | P1 |
| 每色版獨立參數 | ✗ | 網角、線數、網點擴大、偏移 | P1 |
| 套印旋轉與縮放 | ✗ | 仿射變換 | P1 |
| 網布物理量 | ✗ | 線徑、開口、開孔率、角度、莫爾 | P2 |
| 紙張吸墨、沉積量 | ✗ | | P3 |
| 匯出與預覽解耦 | ✗ | 分塊、mm 座標 | P0（基礎建設） |

## 2. 值得實作與只做視覺的分界

- **值得實作**（有依據、可驗證）：LPI、網角、網點形狀、覆蓋率曲線、網點擴大、GCR／TAC、線性空間疊印、每色版套印、目數、線徑、開口、開孔率（查表）、目數:LPI 建議、最小網點推導。
- **只做視覺**：孔版顆粒、墨擴散、不均勻、吸墨、紙纖維、沉積量造成的凸起、網布莫爾（用光柵拍頻近似）、謄寫版全部參數、數位碳粉雜訊。
- **不做**：ICC 色彩管理、光譜 Neugebauer 校正、宣稱打樣精度。

## 3. 模組架構

全部是純函式；同一份程式碼同時給主執行緒預覽與 Worker 匯出使用。

```
print-core/（純函式，可丟進 Worker）
  units.js        mm ↔ px ↔ lpi ↔ mesh 換算
  separation.js   RGB → plates[]（CMYK＋GCR／TAC、專色、灰階、sepSolve）
  tone.js         覆蓋率曲線（sRGB／線性／gamma／自訂 LUT）
  dotgain.js      tvi(c, g) 與 Yule–Nielsen 選項（單一來源）
  halftone.js     AM（spot function＋面積校正 LUT）、FM（256² 藍雜訊）、平滑
  mesh.js         開口、開孔率、Vth、網點可保持判斷、莫爾頻率
  registration.js 每色版仿射（dx、dy、θ、s）
  composite.js    線性空間乘法疊印＋不透明度（簡化 K–M）
  paper.js        吸墨 → 網點擴大與擴散係數
render/
  tilePipeline    以 mm 為座標的分塊管線；Worker 池（hardwareConcurrency−1，上限 8）
  previewAdapter  預覽：依縮放倍率決定 px/mm
  exportAdapter   匯出：指定 DPI 分塊，與預覽共用參數與種子
```

向量圖層的網點改成：遮罩先點陣化，再走同一條 `halftone` 管線，取代 CSS `--dots` 近似。這是 P0 的關鍵統一工作。

## 4. 參數資料結構

```js
L.print = {
  v: 2,
  process: 'offset' | 'screen' | 'riso' | 'digital',
  tone:  { curve: 'srgb' | 'linear' | 'gamma', gamma: 1.8, lut: null },
  halftone: { mode: 'am' | 'fm' | 'off', lpi: 175, shape: 'round', dotGain: .12, minDot: .02, maxDot: .95, fmDotUM: 25 },
  plates: [ { ink: 'C', color: '#00aeef', angle: 15, lpi: null, dotGain: null, density: 1, opacity: 0, reg: { dx: 0, dy: 0, rot: 0, scale: 1 } } ],
  separation: { mode: 'cmyk' | 'spot' | 'gray' | 'custom', gcr: .7, tac: 3.2 },
  mesh: { count: 305, unit: 'in', threadUM: 34, angle: 22.5, eomUM: 12 },
  substrate: { type: 'coated' | 'uncoated', absorption: .3 }
}
```

`plates[i]` 的欄位為 null 時繼承 `halftone` 的值。舊的扁平鍵（lpi、dotGain、mesh、scrLpi、regX…）由 `migrateV1()` 轉入新結構。

## 5. 分階段開發

| 階段 | 內容 | 驗收 |
|---|---|---|
| **S0 基礎** | 拆出 print-core 純函式；mm 座標；分塊管線；Worker 池；Uint8／Uint16 平面 | 現有輸出逐像素不變（迴歸截圖）；A4 600dpi 匯出成功 |
| **S1＝P0** | 統一向量與點陣網點；6 種網點形狀＋面積校正；256² FM；色調曲線；統一 `tvi()` | 測試圖 1–5、9、10 通過；覆蓋率誤差 < 1% |
| **S2＝P1** | GCR／TAC；線性空間疊印；不透明度；每色版參數與仿射套印；專色 | 測試圖 6；與 sepSolve 往返誤差 |
| **S3＝P2** | 網布模組（查表＋公式）；最小網點推導取代經驗式；網布莫爾預覽 | 查表數值與型錄一致；莫爾頻率與理論一致 |
| **S4＝P3** | 紙張吸墨、沉積量、纖維、版材特性 | 視覺審核 |
| **S5 UI** | 依規範 A–G 分組；基本模式與進階模式；預設組合匯入匯出 | 符合「不加多餘說明」原則 |

每個階段完成後回報，等確認才進入下一階段。

## 6. 效能風險與對策

| 瓶頸 | 對策 |
|---|---|
| 40 B/px → A4 600dpi 約 1.4 GB | 分塊（如 512²）＋Uint8 平面＋融合成單一像素函式 |
| 單 Worker | Worker 池；網點閾值法可分塊平行；誤差擴散改為每色版一個 Worker |
| data URI 過大 | 預覽直接畫 `<canvas>`；匯出用 `convertToBlob`（不在預覽中顯示）|
| 8192 貼圖上限、iOS 384 MB | 分塊匯出並逐塊編碼 |
| 縮放重算 | 只重算可見範圍＋倍率分級（已有雛形） |
| CSP 擋 Worker 的 blob URL | 偵測後退回分塊同步執行並以 `await` 讓出主執行緒 |
