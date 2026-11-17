# TECHNICAL_ANALYSIS — 現有程式碼與架構分析

分析對象：`index.html`（commit `ab7dfa7`，約 1.87 MB）。行號以該版為準。

## 1. 結論先行

- 網點系統其實有**兩套互相獨立的實作**，演算法、參數與外觀都不一致：
  - 向量圖層：CSS mask 加 `--dots` 貼圖，濃度由 `printTone()` 計算。
  - 點陣圖層：`rasterKernel()` 逐像素運算。
  - 這是「預覽與匯出一致」以外，更根本的「同一參數、兩種結果」問題。
- 點陣核心 `rasterKernel` 的品質不錯：
  - 網點用幾何 AM 圓點並做解析面積校正（r = p·√(c/π)），超過 50% 時反轉成白點，呈棋盤式過渡。
  - 網角旋轉以座標變換實作。
  - 網點擴大作用在等效覆蓋率上，不是作用在濃度上，符合規範 4.4。
  - 亂數用確定性整數雜湊，預覽與匯出可重現。
- 需要修正的數學模型共 6 項，見第 4 節。
- 網版的網布物理量完全未實作：
  - `mesh` 只用來換算「目數÷線數」比值，沒有線徑、開口、開孔率，也沒有網布角度。
- 效能上的主要問題有三：
  - 只有一個 Worker。
  - 每像素用掉 8 個 Float32 平面，約 32 B/px。
  - 沒有分塊處理；匯出解析度受預覽尺寸限制，上一段已改為依縮放倍率加倍。

## 2. 現況盤點

| 功能 | 位置 | 現況 | 評估 |
|---|---|---|---|
| 印刷模式 | `PRINT_MODES` L2484 | offset、offsetSpot、digital；screen 只在內部使用（單色或孔版） | 可沿用 |
| AM 網點（點陣） | `rasterKernel` L2948 | 圓點、面積校正、網角、box 平均取樣 | 品質佳，缺網點形狀 |
| AM 網點（向量） | `printTone` L2156 加 CSS `--dots` | 貼圖濃度近似，minDot、fillAt、gain 為自訂經驗式 | **與點陣版不一致** |
| FM／顆粒 | `genBN` L2143、`toneGrain` | 自寫 void-and-cluster，64×64 貼圖 | 正確；64² 的周期在大圖可見 |
| 數位碳粉 | `rasterKernel` digital 分支 | 雜訊幅度 ∝ t(1−t) | 純視覺 |
| 分色 | `rasterKernel` 內 | K = 1−max(R,G,B)，100% GCR，無 TAC | 需修正 |
| 專色抽取 | offsetSpot 分支 | 以 RGB 距離加 smoothstep 抽出 | 視覺近似 |
| 自動分色（孔版） | `sepSolve` L1934 | 線性 RGB 乘法模型，座標下降法 | 正確（理想透明墨） |
| 疊印 | `OR *= 1 − ink·(1 − col)` | 在 sRGB 數值上相乘 | 需修正（應在線性空間） |
| 孔版不透明度 | `.riso-cover` 雙層 | 主層 multiply·tr ＋ 覆蓋層 normal·(1−tr) | 屬 Kubelka–Munk 的合理近似 |
| 套印 | regX、regY 乘以每版固定方向係數 | 只有平移，無旋轉、縮放 | 需擴充 |
| 墨擴散 | 向量：SVG dilate＋blur；點陣孔版：三次 box blur | 兩套 | 已修正為外擴 |
| 網布 | `mesh` 選單 80–300 | 只取比值 | 缺物理量 |
| Worker | `getRasterWorker` | 單一 Worker，由 `toString()` 建立 blob URL | CSP 下可能被擋（已有同步退回） |
| 匯出 | SVG → Canvas，遮罩點陣化上限 4096 | 點陣圖層依預覽 DPR | 解析度與預覽綁定 |

## 3. 資料結構

- 圖層參數是扁平物件 `L`。點陣參數鍵列在 `RASTER_KEYS`（20 個）。
- 預設值分散在三處：`FIN_DEFAULTS`、點陣分支的 `D`、新增圖層時。
- 單位混用：
  - `spread`：viewBox 單位。
  - `risoSpread`、`grainMM`：mm。
  - `regX`、`regY`：卡片比例（%）。
  - `lpi`：線／英吋。
- 建議改為分組 schema（`halftone`、`ink`、`plate[]`、`registration`、`substrate`），並帶 `version` 欄位做遷移。現有扁平鍵由 migrate 函式讀入，保持向下相容。

## 4. 需要修正的數學模型

| # | 位置 | 現況 | 問題 | 建議 |
|---|---|---|---|---|
| M1 | 覆蓋率 | c = 1 − Rec.601 luma（gamma 編碼值） | 規範 C = 1 − L/255 只在 L 為線性反射率時才代表等反射率。sRGB 128 → 0.498，但等反射率應為 0.784 | 提供 Tone Curve：「sRGB 數值（現況，相容 Photoshop 慣例）／線性反射率／自訂」，預設維持現況並標示差異 |
| M2 | 疊印 | sRGB 數值相乘 | 乘法減色應在線性反射率空間進行，sRGB 相乘偏暗、偏飽和 | 轉線性後相乘再回 sRGB（使用 LUT，成本極低） |
| M3 | 網點擴大 | 4g·c(1−c)，g 為單一常數 | 形式合理（峰值 50%），但與向量版 `printTone` 的另一套式子不一致 | 兩邊共用同一個 `tvi(c, g)`；進階可用 Yule–Nielsen n |
| M4 | 分色 | K = 1−max，100% GCR | 暗部只有 K、沒有豐富黑，也沒有 TAC 限制 | 加 GCR 量 γ（K = γ·min(C′,M′,Y′)）與 TAC 上限 |
| M5 | 網版 minDot／fillAt | 自訂經驗式 | 沒有依據 | 改由「網點直徑 ÷ 網孔開口」推導：點徑小於開口約 1–2 倍時無法保持 |
| M6 | 孔版顆粒 | 64² 藍雜訊貼圖 | 大面積會出現周期 | 改用 256²，或兩張貼圖做旋轉與位移混合 |

## 5. 效能瓶頸

1. **記憶體**：`rasterKernel` 的 R、G、B、A、OR、OG、OB、cov 共 8 個 Float32 平面，再加 Float64 SAT，約 40 B/px。A4 600dpi（35 MP）約需 1.4 GB，**必定失敗**。需要分塊處理並改用 Uint8 或 Uint16 平面。
2. **單一 Worker、序列處理**：多張圖或多個圖層會排隊。
3. **data URI**：點陣結果用 `toDataURL('webp')` 回填。高熵的顆粒圖可達數十 MB，解碼要數秒。
4. **向量遮罩**：每次參數變動都重建 SVG data URI 並交由瀏覽器點陣化；放大時遮罩會以舊尺寸重新取樣。
5. **SAT 每版重建**：4 版需要 4 次 O(n) 的 Float64 運算，可以共用。

## 6. 相容性

- 內建瀏覽器的 CSP 擋 blob 圖片（已改用 data: 退回）。Worker 的 blob URL 也可能受 `worker-src` 限制；現有同步退回會卡住 UI，需要分塊後 `await` 讓出主執行緒。
- 各平台都有 OffscreenCanvas（Safari 16.4 起），但匯出流程目前沒有用到。
- `MAX_TEXTURE_SIZE`（實測 8192）與 iOS canvas 記憶體上限（約 384 MB）會讓 A4 600dpi 單張 canvas 失敗，需要分塊匯出。
