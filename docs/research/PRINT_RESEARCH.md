# PRINT_RESEARCH — 印刷工藝與技術研究報告

> 由四個研究 Worker 平行撰寫，Main Agent 整合與核對。參數標籤：真實工藝參數／理論計算參數／經驗參考參數／純視覺模擬參數。核對結論與跨來源衝突見文末〈整合核對〉與 VALIDATION_REPORT.md。


---

## A. 網版印刷 網布與版膜工程參數（瀏覽器印刷效果模擬器用）

標籤：【真實】真實工藝參數／【理論】理論計算參數／【經驗】經驗參考參數／【視覺】純視覺模擬參數
注意：網頁內容經 WebFetch 小模型擷取，表格列可能錯位（已標示）。表格資料來源為 Sefar PET 1500 經 Schulze 目錄轉載、Saati 型錄 (archiexpo)、Sefar 經 Coates 轉載，非直接下載原廠 PDF，建議實作前人工複核。

## 1. 目數（mesh count）
- 每吋目數 M（/in）與每公分目數 n（/cm）：M = n × 2.54；n = M / 2.54。【理論】單位換算
- Sefar/歐系標示「n-d」：例 Sefar 120-34 = 120 線/cm、線徑 34 μm（約 305 /in）。美系標示 M/d 如 305/34 或 Murakami 180/48 = 180 /in、48 μm。完整 Sefar 命名如 PET 1500 120/305-34Y（/cm，/in，μm，顏色）；Schulze 目錄實列「43/110-80W」「120/305-31W」。【真實】
- 來源：https://www.groener-schulze.com/kataloge/pdf/schulze_siebdruckkatalog10.pdf ；https://www.mrprint.com/blog/828-developing-maximum-color-strength-when-using-four-color-process（「280.34」「305.34」後數字為線徑 μm）
- 常見換算：60/in→423 μm 節距；110/in→231；200/in→127；305/in→83.3；355/in→71.5；400/in→63.5（節距 = 25400/M）。【理論】

## 2. 線徑分級（S/M/T/HD）
- 同目數下常見：S（Small，細線）、M（Medium）、T（Thick）、HD（Heavy duty，Saati 標示用）；線徑愈細→開口、開孔率、墨量愈大。【真實】分類；各廠數值略異。
- 實際列（來源：Schulze/Sefar PET 1500；Saati）【真實】：
  - 43/cm(110/in)：80、90（Sefar）、64（Saati AM）
  - 77/cm(195/in)：55
  - 90/cm(230/in)：40、48（Sefar表）
  - 100/cm(255/in)：40
  - 120/cm(305/in)：31、34（Sefar 120-34 為 T 級）、37（Murakami 文章）
  - 150/cm(380/in)：31、34
  - 165/cm(420/in)：27
  - 355/in：27(S)、31(M)、34(T/HD)；390/in：27/31/34；460/in：27/31（Screenprintingmag Table 1）
  - 粗網 60–110/in（約 24–43/cm）：線徑約 64–120 μm（Saati 32/cm 70、43/cm 64；Sefar 24/cm 120、32/cm 100）
- 來源：https://screenprintingmag.com/rationalizing-screen-fabric-selection/ ；https://pdf.archiexpo.com/pdf/saati/hi-dro-mesh/4630861-444502.html
- 注：S/M/T 在 60–400 /in 全範圍的完整線徑表本次未取得單一原廠對照；以上為抽樣列，不是完整矩陣。

## 3. 網布開口 a 公式（已驗證）
- 公式：a = 25400/M − d（μm；M 每吋目數；d 線徑 μm）。等價每公分版：a = 10000/n − d（n /cm）。兩式互等（25400/M = 10000/n）。【理論】
- 適用：平織、線徑均勻、無變形、未壓延。限制：實際織物線在交織處彎曲、拉伸張力改變節距（張力下經緯距變化）、壓延/塗層（calendering）使開口縮小；M 為名義值（305/in 實為 120/cm = 304.8）。
- 開口驗證（計算 vs 表格；偏差=表−算）：

| 網布 | 計算 a | 表值 a | 偏差 |
|---|---|---|---|
| Sefar PET1500 43/110-80 | 152.6 | 149 | −3.6 |
| PET1500 100/255-40 | 60.0 | 57 | −3.0 |
| PET1500 120/305-31 | 52.3 | 49 | −3.3 |
| PET1500 165/420-27 | 33.6 | 29 | −4.6 |
| PET1500 150/380-31 | 35.7 | 32 | −3.7 |
| PET1500 77/195-55 | 74.9 | 67 | −7.9（疑擷取錯位或表值異常）|
| Saati 90.40 | 71.1 | 68 | −3.1 |
| Saati 120.31 | 52.3 | 53 | +0.7 |
| Saati 43.64 | 168.6 | 170 | +1.4 |
| Saati 78.40 | 88.2 | 85 | −3.2 |
| Saati 32.70 | 242.5 | 245 | +2.5 |

- 結論：公式為一階近似，誤差多在 −8～+3 μm（約 1–10%，細網相對誤差大，165/cm 達 −14%）。Sefar 表值系統性偏小（約 3 μm，可能含測量/張力/壓延因素，此為推測，原廠未在擷取內容說明）；Saati 表值較貼近理論。模擬器：用公式作預設，可加 −3 μm 「經驗修正」。【理論】公式 / 【真實】表值
- Sefar 官網對 mesh opening ω 的定義：相鄰經緯線間的距離（垂直網面量測）。來源 https://www.sefar.com/en/607/Description-of-mesh-opening.htm?Article=6566821&ArticleReturn=606&UniqueName=meshOpening 。同頁指出墨粒徑應小於開口一定倍數（頁面字面為「至少 0.3 倍」）；Dobie 文章則稱「開口應為墨中最大固體粒子的 4 倍」（https://www.printing.org/docs/default-source/journal-docs/dobie_screenmaking_0321.pdf）。**來源衝突**：0.3×（≈3.3 倍）與 4× 不同，皆為【經驗】。

## 4. 開孔率 OA = (a/(a+d))²
- 變數：a、d 同單位 μm；(a+d) = 節距 p。OA 無因次（×100 為 %）。【理論】= 幾何投影面積比，假設方形開口、直線、平織。
- 對照（OA_算(a用公式) / OA_算(a用表) / OA_表）：
  - 43/110-80：43.0 / 42.3 / 40.8
  - 100/255-40：36.0 / 34.5 / 32.5
  - 120/305-31：39.4 / 37.5 / 35.0
  - 165/420-27：30.7 / 26.8 / 22.3
  - 150/380-31：28.6 / 25.8 / 23.3
  - Saati 120.31：39.4 / 39.8 / 40
  - Saati 43.64：52.5 / 52.8 / 53
  - Saati 32.70：60.2 / 60.5 / 61
- 結論：Saati 表值與公式吻合（±1 個百分點）；Sefar（Schulze 轉載）表值低於公式 2–8 個百分點，細網愈明顯（165/cm：理論 30.7 vs 表 22.3）。限制：公式忽略線的橢圓截面與交織處的遮擋、斜織(twill)開孔率較高；Screenprintingmag 稱斜織較平織厚、開孔率較大。細網請以表值為準。
- 衝突：Sefar vs Saati 對同一幾何的開孔率處理不同（疑為量測方法差異，推測）。

## 5. 理論墨量 Vth 與網厚
- 公式：Vth (cm³/m²) = OA × 網布厚度 t。單位換算：OA(%)/100 × t(μm) 得數值 = cm³/m²（1 μm × 1 m² = 1 cm³）。例 t=49 μm、OA=35% → 17.2。【理論】
- 驗證：Schulze/Sefar：43/110-80：40.8%×130=53.0（表53.0 ✓）；100/255-40：32.5×64=20.8 ✓；165/420-27：22.3×43=9.6 ✓；Screenprintingmag 355/27 PW：36%×42=15.1（表15 ✓）；Saati 120.31：40×48=19.2（表19 ✓）。公式與廠表完全一致（表本來就以此計算）。
- 良率：Yield (m²/L) = 1000 / Vth（Sefar/Coates，估算）；Coates 稱「沒有通用公式」，須依現場調整。來源 https://coates.de/images/AScharrer0524/Calculation_of_Screen_Inks_Consumption24.pdf 。
- Sefar 數值（經 Coates）：43/cm-80 Vth 53.0；77-55 23.0；90-48 19.9；100-40 21.1；120-34 16.3；150-31 10.9；165-27 9.6（150-34 列 6.6 疑為表格錯位或不同織法，未採用）。
- 網厚典型（μm）：110/in 約 130–150；195/in 約 87；255/in 約 64；305/in 約 49；420/in 約 43；355/in 42–60（PW 比 TW 薄）；460/in 43–56。【真實】
- 實際濕墨膜（Dobie/PRINTING United）：WIFT = (Mt × OA) + EOM，Mt 為張力下網厚。即實際墨厚 = Vth + 版膜在網上的厚度 EOM（注意此式是 EOM 加算，是否有轉印效率係數未說明）。實際轉移約為理論的某一比例（因墨膜分裂、刮刀、離網），數值本次未取得可信來源，故模擬器列【視覺】參數。

## 6. 版膜厚度、EOM、Rz
- EOM（emulsion over mesh）：網布印刷面上方版膜厚度。Dobie 圖 2（針對細網）：280/in 10–13 μm；325/in 8–10；400/in 8；≥500/in 6–7。【真實/經驗】
- 每次塗佈（印刷面）增厚：100-40 約 7 μm；120-37 約 5；140-37 約 3（Murakami/PRINTING United）。S 級細線每次增厚較多；固含量高 → 增厚多。https://www.printing.org/detail/resource/Value-A-Concept-in-Screen-Quality-Evaluation
- Rz：4 mm 內分 5 段，各段最大+最小（見原文定義）取平均，單位 μm。Rz<10 μm 可在光滑面印好；3–7 μm 極佳；傳統重氮約 9、光聚合重氮約 7 μm。【真實】
- 對細線：120/cm 網上 EOM 約 15 μm 可印細線，>20 μm 幾乎不可能。EOM 愈厚 → 墨量增加、邊緣定義變差（墨沿版膜壁流動、陰影）；Rz 愈低 → 版面平整、邊緣銳利、密封好。
- 網線徑 vs 最小影像（Dobie 圖 1，【經驗】）：200 μm 影像：325/28 μm；150 μm：325/23；100 μm：400/18；≤50 μm：≥500/16；建議線徑不超過最小影像寬度 25–30%。
- 衝突：Dobie 的 EOM 為細網值，Murakami 的 5 μm/次為 120-37；兩者不矛盾但量級不同（網目不同）。

## 7. 網目與 LPI 比
- 常見規則：網目 ÷ LPI = 3～5（5 最常見）。Solutions for Screen Printers：廠商用 3、4、5，不確定先用 5；230 目 → 最高 46 LPI；LPI × 因子 = 所需網目，只往上取不往下取。https://support.solutionsforscreenprinters.com/hc/en-us/articles/26412588963604-From-Theory-to-Practice-Simplifying-Halftone-to-Mesh-Moir%C3%A9-Control-for-Screen-Printers 【經驗】
- Screenprinting.com：÷5 為理想，÷4 細節多但網點更難保持（160 目→32 或 40 LPI）。https://www.screenprinting.com/blogs/news/a-crash-course-in-halftones-for-screen-printing 【經驗】
- Impressions（Coudray 等）：LPI × 4（55 LPI→220→取 230）；實例 230/45 ≈ 5.1，305/45 ≈ 6.8。https://impressionsmagazine.com/process-technique/halftone-printing-on-textiles/16499/
- 衝突：因子 3–5 vs 4 vs 5 vs 6.8（高比值實例）；皆非物理，為經驗。本次未找到 SGIA/FESPA/原廠的正式比值出處（搜尋未直達）。
- 最小保持網點（我自己的推導，【理論】）：網點週期 P = 25400/LPI (μm)；圓點面積比 t 時直徑 D = P·√(4t/π)；跨越網線數 k ≈ D / 節距，節距 p = 25400/M。則 k = (M/LPI)·√(4t/π)。例：5% 點、比值 5 → k = 5×0.252 = 1.26 個節距；比值 3 → 0.76 個節距（不到一格，印不上）。即「5% 點至少要跨越約 1–2 個網格」是推論，不是原廠規格；實際最小可印點還受 EOM、網線徑、乳劑解析度、曝光影響。

## 8. 網角與網點角度、莫爾紋
- Solutions for Screen Printers：所有半色調用 22.5° 以避免與網紋莫爾。Screenprinting.com：22.5°，避開 0/90/180/270（與網線對齊）及 45°（對角打在網交點）。【經驗】
- Print Wear & Promotion：CMYK 參考角 C15/M75/Y0/K45；單色漸層用 22.5°；角度由輸出菲林設定，不是旋轉網布。https://printwearandpromotion.co.uk/solving-the-mystery-of-moire/
- Impressions 作者用 45 LPI、61° 橢圓點。
- 網布 bias 繃網：網布相對框旋轉角度（常見 22.5° 或 15–22.5°）用於減少莫爾，但本次來源未找到明確 22.5° bias 數值的原廠出處；標【經驗】，需另證。
- 莫爾頻率（理論）：兩光柵的拍頻 f_b = |f1 − f2|（含角度：|f1 − f2| 向量差）。以 f_mesh = n(/cm) 與 f_halftone = LPI/2.54 (/cm) 向量相減（方向由角度差決定）即可預測莫爾週期 Λ = 1/|f⃗1 − f⃗2|；此為標準光柵拍頻光學，非印刷來源。【理論】模擬器可直接實作。
- 莫爾傾向：圓點最耐莫爾，方點次之，菱形/橢圓最易（Screenprintingmag p=2146，Impressions）。
- 衝突：22.5° 通行 vs 傳統 CMYK 15/75/0/45（45 在網上最差）。

## 9. 絲印 LPI、網點擴大、可印範圍
- LPI：Impressions：45 LPI 作者標準、55 LPI 常用；最高 110 LPI（蠟 CTS 1200 dpi 輸出）；Coudray：最小點 5% 於 65 LPI。紡織常 35–55 LPI（本次來源 45–65），圖像/海報類可更高（網目 ≥ 305 目，Dobie 稱 ≥500 目可至很細）。LPI 因紡織與圖像而不同的區分【經驗】，出處不全面。
- 網點擴大：Screenprintingmag（p=2146）：紡織常 ≥35%、圖像印刷約 20%（為 50% 點的增加量，如 30% 擴大 → 80%）；中間調 40–60% 最大；中間調跳躍可超過 20%；方點理想下自增 10–12%。Coudray：實測約 28%–>45%，另加現實約 5%；Photoshop 設 38%；Screenprinting.com：「常選 30%」。【經驗】衝突：20%（圖像）/ 28–45%（紡織）/ 30%（常選）/ 38%（Photoshop 設定）。
- 可印範圍：Coudray：5% 點擴大至約 20–25%（淺色丟失）；>70–75% 點擴大至實底（暗部壓縮）。→ 實際可印約 10–70% 輸入（紡織）。菱形/橢圓點約 40% 連角、60% 對角連（p=2146）。【經驗】
- 降低點擴大：基底含約 2% 透明高密度基底（Coudray 示範）；加稀釋劑導致大量擴大；離網過大放大網點。

## 模擬器參數建議表
- 網目、線徑、網厚、開孔率、Vth：【真實／理論】用上表；a、OA 用公式 + Sefar 修正（−3 μm）【理論+經驗】。
- EOM、Rz：【真實】範圍 3–15 μm / 3–10 μm。
- 墨轉移率：【視覺】。
- 網點擴大曲線：【經驗】20–45%。
- 莫爾：用向量拍頻公式【理論】；視覺強度【視覺】。

## 來源衝突彙整
1. 開口/開孔率：Sefar 表值 < 公式（至 −14%/−8 個百分點），Saati 吻合。
2. 墨粒 vs 開口：0.3 倍（Sefar 頁面字面）vs 開口≥4 倍粒徑（Dobie）。
3. 網目:LPI 比 3/4/5（5 最常）/6.8 實例。
4. 網點擴大 20% vs 28–45% vs 30% vs 38%。
5. 半色調角度 22.5° vs 傳統 15/75/0/45。
6. Sefar 77/195-55 與 150-34 列疑為擷取錯位（開口 67 vs 預期 75；Vth 6.6 vs 預期約 10），未納入結論。

## 缺口
- 未取得 Sefar/Saati 原廠 PDF 直接對照全 S/M/T/HD 矩陣；SGIA/FESPA 正式 mesh:LPI 比值；明確 bias 繃網角度出處；墨轉移效率係數。

---

## B. 網點（Halftone）研究：瀏覽器印刷效果模擬器

標記：【真】真實工藝參數／【理】理論計算參數／【驗】經驗參考參數／【視】純視覺模擬參數。
查證狀態：ISO 12647-2:2013 公開樣本僅取得 Table 1（紙型→曲線對應）、網線數、網角、非週期網點尺寸；TVI 40%/80% 數值表（Table 9）未能取得，下列數值為經驗範圍，使用前須對照標準或 FOGRA/GRACoL 特性資料。其餘公式為標準文獻推導，並以 Python 驗算過部分數值。

## 1. AM 網點
- 網線數 LPI（lines/inch）；ISO 用 cm⁻¹（L/cm）。換算：lpi = L/cm × 2.54。【理】
- 網格週期（cell pitch）= 25.4 / LPI mm（150 lpi → 0.1693 mm；60 L/cm → 0.1667 mm）。【理】
- 設定器解析度 DPI，網格邊長（device pixels）n = DPI / LPI；每網格 n² 個 device pixel，灰階層數 = n² + 1（PostScript 經典 (DPI/LPI)²+1；2400 dpi／150 lpi → 16² + 1 = 257）。【理】
- 瀏覽器：螢幕 DPR×96 dpi，網點週期若只有數 px，層數遠低於 256，會出現階調斷層；需用超取樣（thresholding 在高解析度，或 smoothstep 反鋸齒）。【視】
- 網角旋轉：(u,v) = ( x·cosθ + y·sinθ , −x·sinθ + y·cosθ )，再取 u' = frac(u/p)·2 − 1，v' = frac(v/p)·2 − 1（domain [-1,1]），p = 週期。【理】
- 有理正切角（tanθ = m/n，如 0°、45°、18.43°=atan(1/3)、26.57°=atan(1/2)）可得週期重複的超格（supercell），輸出完全週期、無 moiré 漂移，但 15°/75° 非有理。傳統（Hell/類比網屏）用 15°/75°；PostScript Level 2 之前的有理正切（RT）與後來 Accurate Screening/IS 無理正切（IT）為近似。取捨：無理角更接近理想角、層數多，但無法精確週期、不同色版間 rosette 有細微漂移。【理】
- 衝突：ISO 12647-2:2013 §4.2.5 的描述（無主軸網點，C/M/K 差 30°、Y 與其他色相差 15°、主色 45°）與常見業界口訣 C75°/M15°/Y0°/K45° 並不矛盾，但標準給的是「差值規則」而非唯一組合。有主軸網點（橢圓）C/M/K 差 60°，主色 45° 或 135°。【真】

## 2. Spot function（PostScript，x,y ∈ [-1,1]，值域 [-1,1]）
PostScript 規則：對 cell 內每個像素算 S(x,y)，由小到大排序，依序開啟；「值小者先黑（含墨）」。設閾值方式（網點「黑」為墨）：
- Round：S = 1 − (x² + y²)（PLRM 範例：`{360 mul sin 2 div exch 360 mul sin 2 div add}` 是 Euclidean 預設的另一種寫法，不是 round）。PLRM 內建預設 spot 為 `{abs exch abs 2 copy add 1 gt {1 sub dup mul exch 1 sub dup mul add 1 sub} {dup mul exch dup mul add 1 exch sub} ifelse}`，即 inverted-round 與 round-square 結合（<50% 時圓點，>50% 時圓洞）。
- Euclidean（PLRM 常見）：|x|+|y| ≤ 1 時 S = 1 − (x²+y²)，否則 S = (|x|−1)² + (|y|−1)² − 1。亦即中間調為「圓角方形 → 洞」。
- Ellipse（PLRM 標準）：w = 3|x| + 4|y| − 3；若 w < 0 → 1 − (x² + (|y|/0.75)²)/... ，w > 1 → 1 − ((1−|x|)² + ((1−|y|)/0.75)²)，否則 0.5 − w。此為 PLRM 圖例的「ellipse」實作。（細節各 RIP 略異，【驗】）
- Square：S = 1 − max(|x|, |y|)。【理】（方形網點；50% 處棋盤接觸）
- Diamond：S = 1 − (|x|+|y|)/... 簡式：S = 1 − (|x|+|y|)（|x|+|y|≤1 時）；PLRM 版用 1−|x|−|y| 在內、(|x|−1)+(|y|−1) 在外，連續。
- Line：S = |y|（或 1 − |y|）。【理】
- Cross：S = −min(|x|, |y|)（或 1 − ... 取反）。
說明：以上「簡式」為本文歸納；PLRM 原文為 Euclidean/ellipse 之分段式，實作前請對照 Adobe PostScript Language Reference 3rd ed. §7.4。我未能全文取得該頁，故標【驗】。

閾值法：對每個像素算 S 後在 cell 內排序，得 rank∈[0,N−1]；覆蓋率 a 時，rank < a·N 的像素有墨。這使「S 值」≠「面積」：例如 round 的 S=1−r² 為二次函數，S>t 的面積比例是 π r²（圓面積）而非線性；因此直接用 `S < threshold(a)` 會讓實際墨面積隨 a 非線性。校準法：(1) 離線排序（rank/N 即累積面積分佈，CDF）；(2) 或建 LUT：area(t) = P(S < t)，再以 t = area⁻¹(a) 查表；(3) shader 內解析反函數：round 時 r = sqrt(a/π)（週期內）。結果：實際面積 = a（對 Murray–Davies 而言的「幾何覆蓋率」）。【理】

## 3. 覆蓋率 C = 1 − L/255 是否正確？
不嚴謹。
- 若 L 為 sRGB 編碼值（gamma ≈ 2.2，分段曲線）：線性亮度 Y = ((v+0.055)/1.055)^2.4，v=L/255。
- 「覆蓋率」有兩種意義：(a) 想要的視覺明度 → 網點面積（印刷網點是在線性反射率空間混合，Murray–Davies），應 a = (Y_paper − Y)/(Y_paper − Y_solid) 於線性空間；(b) 保持影像看起來一樣（RIP 的 TRC）。
- 驗算：sRGB 128（v=0.502）：1−v = 0.498（如直接當覆蓋率）；1−Y_lin = 0.784。若 halftone 在螢幕以 gamma 空間顯示、而人眼/螢幕平均後是線性，則 a = 0.498 的網點平均後只會呈現 Y_lin = 0.502 → 對應 sRGB 約 188（較亮），發生「中間調變淡」。正確作法：先 sRGB→線性 Y，再 a = 1−Y（紙白=1、墨=0 的理想模型），或加入 TVI 後反推（見 §4）。【理】
- L* 路徑：L* 與感知均勻，但面積混合是線性反射率（Y）；用 L* 當覆蓋率只在簡化視覺時使用。【視】
- Tone curve：RIP 的轉移曲線（transfer function）將輸入 a_in → 輸出 a_out 以補償 TVI：a_out = TVI⁻¹(a_in)。見 §4。【真】

## 4. 網點擴大（Dot gain／TVI）
- 定義：TVI（tone value increase）= a_eff − a_nom（百分點）。ISO 12647 用 TVI；「dot gain」同義，常見於舊稱。【真】
- Murray–Davies（1943）：a_eff = (1 − 10^(−D_t)) / (1 − 10^(−D_s))，D_t 為網點區密度（含紙），D_s 為實地密度，皆減去紙白（紙白密度視為 0）。等價以反射率：a_eff = (R_p − R_t)/(R_p − R_s)。【真/理】
- Yule–Nielsen（1951）：R_t^(1/n) = a·R_s^(1/n) + (1−a)·R_p^(1/n)；n=1 即 Murray–Davies。有效面積：a_eff(YN) = (1 − 10^(−D_t/n))/(1 − 10^(−D_s/n))。n 取 1.5–2.5（【驗】；網線數越高、紙越粗／散射越大 n 越大）。驗算（R_p=0.85, R_s=0.03，真實面積=50%）：用 n=1 的 Murray–Davies 解讀的 a_eff：n=1 → 50%、1.5 → 61%、2 → 67%、2.5 → 71%、3 → 73%，即光學擴大 ≈ +11…+23 點。這顯示 n 與擴大量高度耦合；n=2 對應的光學部分已和 ISO 的 12–16% TVI 同數量級。
- 機械增益（mechanical）：製版、壓力使墨點實際變大（印刷機、橡皮布、紙吸墨）；光學增益（optical）：光散射於紙內（Yule–Nielsen 效應）。量測 TVI = 兩者之和。【真】
- 模型（參數化，供模擬器用）：
  1. 拋物線：TVI(a) = 4·g·a·(1−a)，g = 50% 處 TVI（0.12–0.22），峰值在 50%，兩端為 0。【經驗】驗算：g=0.15 → a=.1:5.4%, .2:9.6%, .4:14.4%, .5:15%, .6:14.4%, .8:9.6%, .9:5.4%，與 ISO 曲線「近似 50% 峰值對稱」相符；真實曲線峰值略偏 40–50%，高光側升降較快。
  2. 周長模型：Δ ∝ 邊界長度 × 擴張距離 δ（以半徑擴大）。圓點 a = πr²/p²，a' = π(r+δ)²/p² → 低調時 a' = (√a + δ√π/p)²；>50% 轉為洞（以 1−a 對稱）。可得 TVI 在 a→0 與 √a 成比例（最初陡），在 50% 附近連續。【理】δ 與 p 之比（約 δ ≈ 5–12 µm 於 150 lpi，p=169 µm）為擬合參數。【驗】
  3. 實務：RIP 轉移曲線以 ISO 曲線 A–G 內插（40% 與 80% 兩點加 0、100 兩點，以樣條）。【真】
- ISO 12647-2 對應：PC1（優質塗佈）→ 曲線 A；PC2/PC3/PC4 → 曲線 B；PC5（非塗佈）→ 曲線 C（Table 1，已由公開樣本確認）。40% TVI 約 12–16（塗佈）、約 18–22（非塗佈）——此數為【驗】，非逐字核對標準。K 版常較 CMY 多 1–2 點。
- 衝突：不同來源對「dot gain」「TVI」「optical dot area」混用；GRACoL 用 TVI（A 曲線族），ISO 用曲線 A–G（A=最小），兩者以 40%/80% 兩點定義（ISO 12647-2 為 40%/80%；SWOP/GRACoL 傳統量 50%）。

## 5. 最小／最大可印網點
- ISO 12647-2:2013 公開樣本：非週期（FM）網點 20–40 µm（塗佈偏 20–30，非塗佈偏 30–40）；週期網線 48–80 cm⁻¹（非塗佈偏 48–70）。【真】
- 常見經驗：AM 150 lpi 高光最小網點約 1–2%，低於此在印版／印刷上掉點；暗部 98–99% 開孔會堵（高光「斷」、暗部「閉」）。具體百分比視製版／機台，【驗】。模擬器可做 a<a_min → 0（或機率式掉點）、a>1−a_min → 1。【視】
- 最小網點直徑 d_min ≈ 20 µm 對應 a_min = π(d/2)²/p² = π·100²/169² ≈ 1.1%（150 lpi）。【理】

## 6. FM／隨機網點
- 白雜訊：每像素 > 隨機閾值；顆粒粗、低頻團塊；無結構但品質差。
- Bayer 有序抖動：遞迴矩陣（2×2：[[0,2],[3,1]]/4，倍增）；確定、可平鋪、可平行（shader 友善）；有規則十字紋。
- 誤差擴散：Floyd–Steinberg（1976；7/16, 3/16, 5/16, 1/16）；Jarvis–Judice–Ninke（12 格，/48）；Stucki（12 格，/42）。品質高、顆粒細，但順序相依（序列）、不易 GPU 平行、動畫時圖案「游動」/閃爍。
- 藍雜訊（Ulichney 1993 void-and-cluster）：離線生成閾值矩陣（如 64×64）；頻譜在低頻有缺口（無低頻能量），平鋪，shader 一次查表；確定、可動畫（以固定矩陣+平移或時間偏移）。品質接近誤差擴散。【理】
- 1 階 FM（點大小固定，頻率調變）vs 2 階 FM（點成簇，大小也變；如 Agfa Crystal Raster）：2 階較穩定於印刷擴大，因為單點太小時 TVI 不穩（見 §5）。
- 比較（瀏覽器）：| 方法 | 品質 | 成本 | 確定性／平鋪 | 動畫穩定 |
  Bayer：中、極低、是、是；藍雜訊 texture：高、低、是、是（推薦）；FS：高、高（序列）、否（依輸入）、差；白雜訊：低、極低、是（hash）、閃爍除非固定種子。
- 真實 FM 印刷：TVI 比 AM 高（周長大），ISO 另有 FM 專用曲線，【真】。

## 7. CMYK 網角
- 常用：C 15°、M 75°、Y 0°（或 90°）、K 45°（K 45° 因人眼對 45° 最不敏感）。另一組：C 105°、M 75°、K 45°、Y 90°（歐洲）。ISO：差 30°（無主軸），Y 與他色差 15°。【真】
- 為何 Y = 0°：黃明度最高、可見度最低，故放在僅剩 15° 間隔的位置；其網紋干涉最難被注意。
- 30° 間隔使三色（C/M/K）形成最細緻的玫瑰花紋（rosette）；差異誤差產生 moiré（週期 ≈ 1/ (|f1 − f2|)）。 
- 無理角度（IT）使 rosette 品質更佳，有理角度（RT）可預測。【理】
- 瀏覽器：旋轉用 θ 的 sin/cos 即可；為避免 moiré 於縮放，以 fwidth 做抗鋸齒（smoothstep 寬度 ≈ 0.7/pixels-per-cell）。【視】

## 參數表
| 參數 | 值 | 類別 |
|---|---|---|
| LPI | 100–200（ISO 48–80 L/cm=122–203 lpi） | 真 |
| 週期 | 25.4/LPI mm | 理 |
| 層數 | (DPI/LPI)²+1 | 理 |
| 網角 | 15/75/0/45 | 真 |
| 50% TVI g | 0.12–0.22 | 經驗 |
| YN n | 1.5–2.5 | 經驗 |
| a_min | 1–2% | 經驗 |
| FM 點徑 | 20–40 µm | 真 |
| 抗鋸齒寬度 | ≈ 0.7 px | 視 |
| 藍雜訊矩陣大小 | 64×64 | 視 |

## 來源／不確定項
ISO 12647-2:2013 公開樣本（iTeh）；X-Rite、Wikipedia「Dot gain」；Ulichney, "Void-and-cluster method for dither array generation," 1993；Floyd & Steinberg 1976；Yule & Nielsen 1951；Murray 1936／Davies。未驗：PLRM 的 spot function 原文、ISO Table 9 TVI 數字、GRACoL 曲線。§2 之部分 spot function 以簡式列出，需對照 PLRM 後再用作「真實」。

---

## C. 分色、油墨疊印與套準（瀏覽器印刷模擬器）研究報告

標籤：【真】真實工藝參數／【理】理論計算參數／【經】經驗參考參數／【視】純視覺模擬參數
資料來源說明：本次實際抓取到 RISO 官網規格頁（us.riso.com SF5450、riso.com.hk MZ970、riso.co.uk compare）與 SAIC EverythingRiso 2024；Neugebauer / Yule–Nielsen / Kubelka–Munk / ICC 部分為教科書與 EPFL LSP（Hersch 團隊）文獻之標準公式，由我整理，未逐篇重新核對頁碼。「未查得」者已明示。

## 1. RGB→CMYK：樸素法 vs ICC

### 1.1 樸素法（理）
C' = 1−R, M' = 1−G, Y' = 1−B（R,G,B ∈ [0,1]）
K = min(C',M',Y') = 1−max(R,G,B)
C = (C'−K)/(1−K)，M、Y 同理（K=1 時設 0）。
- 這是設備無關的數學轉換，沒有油墨物理，色域與色彩準確度與真實印刷差距大（純青 C=1 實際約 sRGB (0,174,239)，而非 (0,255,255)）。
- GCR（灰成分替代）：K = γ·min(C',M',Y')，γ∈[0,1] 為替代量（0=無 GCR，1=全 GCR）；曲線式 GCR 常用 K = γ(m)·m，m=min。UCR 則僅在中性暗部以 K 取代 CMY。【理，γ 取值為經】
- TAC（總墨量）限制 = C+M+Y+K（%）：【真】常見規範值——FOGRA39 / ISO Coated v2 約 330%（部分 ECI 文件 300–330），GRACoL 2006 Coated #1 約 330%，SWOP 約 300%，新聞紙（SNAP/ISO Newspaper）約 240%，無塗佈紙（PSO Uncoated）約 300%。數值在不同文件略有出入（ISO Coated v2 常被引為 330，而 ISO Coated v2 300% 是另一個設定檔），**來源衝突**：做 UI 預設時建議提供 300／330／340 選項並註明「依 profile」。超限處理：K 增加（GCR）後按比例縮 CMY，或 clip。

### 1.2 ICC 分色
ICC 設備連結流程：RGB → (sRGB 轉 XYZ/Lab，PCS D50) → 色域映射（渲染意圖：感知／相對色度＋黑點補償）→ CMYK 的 A2B/B2A LUT（通常 4D→3D 的 CLUT，17^4 節點）。B2A 表中已內含 GCR/TAC 決策。【真】
- 瀏覽器原生：Canvas/CSS 無 ICC 引擎做 RGB→CMYK（CSS Color 4 的 `color()` 只涵蓋 RGB/Lab/Lch 等，`device-cmyk()` 僅在規格中、無瀏覽器實作；Safari 對 ICC 內嵌圖片做 RGB profile 管理，但不輸出 CMYK）。可行的近似（經）：
  1. 在 JS/WebGL/WebGPU 自行實作 4D CLUT 三線性/四面體插值（可載入裁剪後的 .icc A2B 表或預烘焙 LUT PNG）；
  2. 用 Neugebauer/Yule–Nielsen 前向模型（下節）配一組「油墨 Lab/XYZ」常數，反向用最小二乘或查表；
  3. 多項式回歸 RGB→CMYK（較粗略）。
- 預覽方向（CMYK→螢幕）才是模擬器核心：前向模型比反向分色重要。

## 2. 專色分色與自訂通道

- 模型（理）：把圖像視為光學密度加成（≈CSS multiply 的對數形式）。每通道 i 有墨色 RGB 透射 t_i∈(0,1]³，覆蓋率 a_i∈[0,1]；乘法模型：R_out = R_paper · Π_i (1 − a_i(1 − t_i))。
- 最小二乘解混（unmixing）：取 −ln(R_out/R_paper) = Σ a_i·(−ln t_i)（近似「有效密度 d_i」加成），形成 3×N 矩陣 D（N=通道數），解 min ‖D a − d_target‖²，約束 0≤a≤1（NNLS / 投影梯度 / WebGPU compute 逐像素）。
- 限制：N>3 時病態（metamerism，解不唯一，需正則化／GCR 式偏好）；N=2 時只能覆蓋色域的曲面；乘法模型忽略不透明墨、網點擴張、散射（KM）、墨與墨之間的不獨立；目標色超出色域需 clip 或 gamut mapping。【理】

## 3. 疊印模型

### 3.1 Demichel（理）
獨立隨機網點放置，三墨（有效網點覆蓋率 c,m,y）八個 Neugebauer 原色面積：
a_w=(1−c)(1−m)(1−y)；a_c=c(1−m)(1−y)；a_m=(1−c)m(1−y)；a_y=(1−c)(1−m)y；
a_cm=cm(1−y)；a_cy=c(1−m)y；a_my=(1−c)my；a_cmy=cmy。
一般 k 墨：2^k 項，面積 a_p = Π_i [a_i 若墨 i 在 p 中，否則 1−a_i]。Σa_p=1。
注意：c,m,y 為**有效**面積（含網點擴張）；若網點為規則角度網屏（非隨機），Demichel 為近似，Hersch 等（EPFL）用「網屏相位」修正。獨立假設在 riso 的隨機（FM/grain）網點最合理，在角度 AM 網屏下大致成立。

### 3.2 Neugebauer（理）
R(λ) = Σ_p a_p · R_p(λ)（反射率線性混合，Murray–Davies 的多色推廣）。單色：R = (1−a)R_paper + a·R_ink。
Murray–Davies 網點面積：a_eff = (R_paper − R_t)/(R_paper − R_solid)（以密度算的 MD 用 D）。缺陷：未計光在紙內橫向散射 → 低估暗化（網點擴張的光學成分）。

### 3.3 Yule–Nielsen 修正（理）
R^{1/n} = Σ_p a_p · R_p^{1/n}。n 為經驗光學網點擴張因子，n=1 退化為 Neugebauer；【經】典型 n≈1.7–2.5（膠印塗佈紙約 1.7–2.2；無塗佈紙更大、約 2–3，視網屏線數而定；網屏越細 n 越大，因橫向散射相對越大）。需用實測色塊擬合 n 與機械網點擴張（物理 a_geom → a_eff）。
Yule–Nielsen modified Spectral Neugebauer（YNSN）：以光譜 R_p(λ) 逐波長計算，再積分到 XYZ。**不需光譜時的簡化**：RGB 三通道（或線性 RGB）上直接套用，誤差可接受（視）。
網點擴張（dot gain）曲線：a_eff = a_nom + g(a_nom)；常見 FOGRA39：50% 網點約 +13–15%（約 CMYK 塗佈紙，ISO 12647-2 的 TVI 曲線 A：中間調 ≈ 13%、曲線 B/C 無塗佈約 18–20%）；【真】ISO 12647-2 數值；riso 無公開標準。

### 3.4 Kubelka–Munk（理）
單層：R_∞ = 1 + K/S − √((K/S)² + 2K/S)；K/S = (1−R_∞)²/(2R_∞)。
有限厚度層（厚度 X，背景反射率 R_g）：
R = [1 − R_g(a − b·coth(bSX))]/[a − R_g + b·coth(bSX)]，a = 1+K/S，b=√(a²−1)。
- 透明墨（S≈0）：T = exp(−K·X)（Beer–Lambert），多層即相乘 → 對應 CSS multiply。
- 不透明墨：高 S，覆蓋下層，疊印結果 ≈「上層取代」；中間為半透明（riso 墨多為此類，但偏透明）。
- 需要的參數：每墨 K(λ)、S(λ)、厚度 X；單一 RGB 近似時可取 per-channel K,S（視）。Saunderson 修正（表面界面反射 ≈ 4–5% 外加內反射 ≈ 0.4–0.6）用於準確量測轉換，視覺模擬可略。
- 為何 CSS multiply ≈ 理想透明減色：multiply 計算 Cs·Cb，等價於兩透明層透射相乘，且忽略表面反射、散射（網點擴張光學成分）、墨不透明度與墨/紙交互；因此 (a) 不能表現白墨/不透明墨覆蓋（需 normal 混合或 KM），(b) 沒有紙白色以外的基底光學，(c) 色域永遠比真實疊印暗得更乾淨。
- 光學密度 D = −log10 R（R 為反射率，0..1，需參考白＝紙白或絕對白，須註明）；透射密度 D = −log10 T。「不透明度」(opacity) 在製墨業定義為（黑背景 vs 白背景的反射率比 R_b/R_w，即 contrast ratio）；與密度不是同一回事：密度是吸收量，不透明度是遮蓋力。UI 不宜把「墨量%」與「密度」混用。【理】

## 4. Risograph

### 4.1 製版與機械（真，來自 RISO 官網規格頁）
- 熱感穿孔：ThermalHead 掃描製版 → 感熱蠟孔穿孔母版，貼合滾筒（drum）；墨由滾筒內部經穿孔滲出至紙。無網版框，一色一滾筒。
- 解析度（rev. 官網）：SF5450：掃描 600×600 dpi、印刷 **300×600 dpi**，快速製版模式 **300×400 dpi**；MZ970：**600×600 dpi**；SF9350／MH9350／SJ9390（riso.co.uk）：600×600；SF5350、SF5030：300×600。→ 模擬器預設：300、400、600 dpi 皆有真實機型對應【真】。
- 印刷面積：SF5450 最大 291×425 mm；MH/SJ/SF9350 291×413 mm；SF5030 204×290 mm。紙重：46–210 gsm（SF/MH 9xxx 系列，riso.co.uk）。**來源衝突**：SAIC 服務中心因自有設備限制僅收 ≤80 gsm（經，非機器規格）。
- 位置調整範圍：SF5450 水平 ±15 mm、垂直 ±10 mm（MZ970 頁寫垂直 ±15、水平 ±10，與 SF5450 相反——**兩頁方向定義衝突**，可能是進紙方向命名差異）。【真】這是「調位範圍」不是「套準精度」。
- 套準精度（registration accuracy）：RISO 官網頁**未查得**公開 ± mm 數值。業界/使用者文獻：SAIC「misregistration WILL happen」，以切紙容差 1/16 in（≈1.6 mm）作留白參考；社群與工作室指南常見經驗值：**約 ±0.5–1 mm 每次重覆，進紙／紙張伸縮造成最大約 1–2 mm**。【經】請在 UI 標「經驗值」，不要引為 RISO 保證值。
- 墨：大豆油基油墨（乳化油墨 W/O），靠紙吸收滲透乾燥（不是揮發固化）→ 僅適合無塗佈紙（SAIC 指引：禁用塗佈紙）。【真】
- 墨透明度：RISO 墨多為半透明（SAIC：「ink is translucent」，疊印取決於紙色與層序）；有少數不透明/金屬墨（如 Metallic Gold、Silver，需另購、效果有限）【經】。
- 抗墨轉印（set-off）與墨層：SAIC 指引：重覆印 ≤4 次，大面積深色 ≤2 次，因進紙輪會吸墨弄髒；大面積實心建議降到 70–85% 覆蓋，且避開進紙邊。【真，工作室指引】
- 圖像模式（MZ/SF 系列，官網僅列）：Line、Photo（Standard / Portrait）、Duo、Pencil；另有「Dot Process」功能。**RISO 官網規格頁未給出 lpi 數字**；「Grain Touch」是 RISO 自家 FM（隨機/顆粒狀）加網名稱，常被使用者用於 ComColor/RISO 驅動；網屏 lpi 選項（常見：Screen 為 ~71 lpi–約 106 lpi 之類）**未能由官方來源驗證，不要寫進模擬器作為官方值**。【經：僅作為「可調 lpi 預設 50–106」的視覺範圍】
- 使用者文獻：300 dpi 灰階 PDF（SAIC 指引）建置每色版；RISO 不適合照片，需半色調或抖色。
- 不均勻性（視/經）：滾筒墨量不均、進紙處「ghost」、實心區斑駁、紙纖維決定吸收（顆粒感）、先印色對後印色的 set-off、乾燥前碰觸髒污。模擬為低頻噪聲（紙纖維 + 墨層）乘到墨密度上；參數屬【視】。
- 紙吸收：無塗佈紙吸收墨→ dot gain 大、密度低、顏色偏暗/暈；紙色直接決定結果（透明墨乘上色紙）。

## 5. 謄寫版（mimeograph，簡）
- 蠟紙（wax stencil）以鐵筆/打字機打穿或電子製版，墨由軟質滾筒擠壓穿過孔洞；墨為油墨（早期為 油溶性），在無塗佈吸收性紙上。
- 特徵：邊緣不規則（紙纖維、蠟紙破口）、墨斑與滲透暈、實心區不均、墨量隨使用遞減、側邊較粗的 spread。無公開量化標準【無真實標準值，全部為【視】】。可由 riso 模型加大邊緣噪聲、降低解析度（≈有效 100–200 dpi）、增加 gain 來近似。

## 6. 套準誤差建模

仿射模型（理）：對每個色版 i，位置 p' = s_i · R(θ_i) · (p − c) + c + t_i
- t_i = (dx, dy)（mm）；θ_i（度或 mrad，繞紙中心 c）；s_i = 1 + ε（紙伸縮，無量綱；以 ppm 或 % 表示）。
- 紙張吸濕伸縮：【經】無塗佈紙濕度變化 ~1% RH 約 0.01–0.03% 尺寸變化；平版多色印刷中紙伸縮約 0.05–0.2%（A3 約 0.15–0.6 mm）；riso 先印再回家重印，因吸墨/吸濕伸縮可更大（0.1–0.3%）。【經，非精確】
- 典型容差：【經／部份真】膠印（sheetfed offset）多色套準 ≈ ±0.02–0.05 mm（高品質機器 ≤0.01–0.02 mm 重複）；網版印刷（手工/半自動）≈ ±0.1–0.3 mm（精密 ±0.05 mm）；riso：見上，±0.5–1 mm 經驗值，RISO 官方未列。【數字為產業慣用值，未能於此次查得標準文件，標「經」】
- 取樣：每個版以高斯隨機 σ(x,y)=0.3–0.5 mm（riso）＋整批 systematic 偏移（調位的人為誤差）＋同一滾筒歪斜 θ~±0.05–0.2°。
- 實作：分別在 WebGPU 以每色版獨立 2D 仿射變換重採樣，再套用疊印模型；偏移 < 1 px 需 subpixel（雙線性）重採樣，會讓網點微弱模糊，註記為視覺副作用。

## 7. 紙張

- 塗佈紙：墨留表面，dot gain 小（FOGRA39 約 +13%）、密度高、色域大；紙白（FOGRA39 紙白 Lab ≈ 95/0/−2；PSO Uncoated FOGRA47 ≈ 95/0/−2 之類，未驗證）。【真，但具體 Lab 值請以 profile 為準】
- 無塗佈紙：吸收 → dot gain 大（+18–25%）、密度低、色域縮小、色偏暖、吸墨造成顆粒；ISO 12647-2 紙型 4（無塗佈白）數值為參考。
- 紙白（paper white）：模擬時基底 RGB（如 Lab 95,0,−2 → 約 sRGB 242,242,240），對透明墨（riso、減色）尤為關鍵——整個畫面 = paper_color × Π(ink transmittance)。有色紙需照樣乘上。 【理】
- 紙吸收參數（視）：吸收度 → (a) gain 增量 Δa = k_abs·a(1−a)（在 50% 最大，仿 TVI 曲線形狀），(b) 墨密度縮放 ρ = 1−α·k_abs，(c) 邊緣暈/輕微模糊半徑 r ≈ 0.02–0.08 mm（視）。

## 8. 參數分類表（摘要）

| 參數 | 值/公式 | 標籤 |
|---|---|---|
| Riso 製版解析度 | 300×600/300×400/600×600 dpi | 真 |
| Riso 印刷面積 | 291×413 或 291×425 mm | 真 |
| Riso 紙重 | 46–210 gsm（機器），80 gsm（SAIC 限制） | 真／經（衝突） |
| Riso 位置調整 | ±10/±15 mm（兩頁方向互換） | 真（衝突） |
| Riso 套準精度 | ±0.5–1 mm | 經 |
| Riso lpi/grain 數值 | 官方未公開 | 經/視 |
| TAC | 300/330/340% | 真（依 profile） |
| Yule–Nielsen n | 1.7–2.5 | 經 |
| 網點擴張 50% | 塗佈 +13%，無塗佈 +18–20%（ISO 12647-2） | 真 |
| Demichel / Neugebauer / KM 公式 | 見 §3 | 理 |
| 套準偏移 σ、旋轉、紙伸縮 | 見 §6 | 經 |
| 墨不均、紙纖維噪聲、謄寫版邊緣 | — | 視 |

## 9. 來源與衝突備註
- RISO 規格頁：us.riso.com/products/digital-duplicators/sf-series/sf5450/；riso.com.hk/eng/products/mz970.php；riso.co.uk/compare-duplicators/。
- SAIC：sites.saic.edu/servicebureau/.../EverythingRiso_2024.pdf。
- Yule–Nielsen / YNSN：EPFL LSP（lspwww.epfl.ch/publications/colour/），Hersch 等（未逐篇通讀）。
- 衝突：(1) SF5450 vs MZ970 位置調整 H/V 互換；(2) 80 gsm 限制 vs 機器 210 gsm；(3) TAC 300 vs 330（ISO Coated v2 不同變體）；(4) riso 套準精度官方無數值。
- 需補查（未完成）：RISO 官方 lpi 清單、ComColor 與 MZ 的 Grain Touch 說明、ISO 12647-2/FOGRA39 TAC 原文、GRACoL TVI 表。

---

## D. 瀏覽器原生影像處理效能研究（印刷模擬器：網點、分色、合成）

測試環境：Playwright Chromium（headless、軟體 WebGL、僅 2 核心、無 WebGPU）。數字為單執行緒、取 2-3 次最佳值，僅供量級參考；真機（桌機 Chrome/Safari）通常快 1.5-3 倍。腳本在 /root/work/research/bench/b.js、c.js。

## 1. 資料型別與每百萬像素成本（4096×4096 = 16.8 MP，單通道）

| 操作 | 時間 | 每 MP |
|---|---|---|
| 門檻/有序網點，Uint8 來源→Uint8 輸出 | 41 ms | 2.4 ms |
| 同上，Float32 來源（需 /255 比較） | 71 ms | 4.2 ms |
| 輸出 RGBA 用 Uint32Array 單次寫入 | 56 ms | 3.3 ms |
| 輸出 RGBA 用 Uint8ClampedArray 逐通道寫 4 次 | 72 ms | 4.3 ms |
| Floyd-Steinberg，Float32 全幅緩衝 | 202 ms | 12 ms |
| Floyd-Steinberg，整數定點 + 兩行滾動緩衝 | 114 ms | 6.8 ms |
| putImageData 4k×4k | 8.6 ms | 0.5 ms |
| getImageData 4k×4k | 64 ms | 3.8 ms |

結論：
- 整數（Uint8/定點）比 Float32 快約 1.7 倍，且記憶體是 1/4。僅在色彩管理/混色階段才需要 Float32。
- 寫 RGBA 時用 `new Uint32Array(imageData.data.buffer)` 一次寫一個像素，比四次逐通道寫快約 25%（注意位元組序：小端，0xAABBGGRR，現今所有目標平台皆小端）。
- 誤差擴散用「兩行滾動緩衝」比整幅 Float32 快且省記憶體。
- getImageData 比 putImageData 貴 7 倍（GPU 回讀/反預乘）。建議整條管線留在 TypedArray，只在最後一次 putImageData；避免反覆 getImageData。並用 `getContext('2d',{willReadFrequently:true})` 若必須回讀。
- 注意 ImageData 是預乘 alpha 之前的非預乘資料，但 canvas 內部預乘，半透明像素 round-trip 會損失精度；分色/網點通道請用不透明 alpha=255 或自行維護獨立 Uint8 平面，不要經由 canvas 往返。

## 2. OffscreenCanvas、ImageBitmap、傳輸

- OffscreenCanvas：MDN 標為 Baseline Widely available，自 2023 年 3 月起各主流瀏覽器可用（Safari 16.4 為首個支援版本，與 Safari 16.4 發佈時間吻合；MDN 頁面本身未在文字中列出各子功能版本，請以 caniuse/MDN 相容表再確認 WebGL-in-worker 與 `transferControlToOffscreen`）。Firefox 105+、Chrome 69+。
- 不要把 OffscreenCanvas 當作必須：純 TypedArray 運算在 Worker 內不需要它。只有「在 Worker 內編碼 PNG（convertToBlob）」或「Worker 內 WebGL」才需要。需做功能偵測並退回主執行緒 canvas。
- Transferable vs structured clone（64 MB ArrayBuffer，實測）：transfer 1.2 ms；clone 48 ms（約 40 倍）。大型平面一律 transfer（`postMessage(buf,[buf])`），傳出後原端 detach。若要共享讀取可用 SharedArrayBuffer，但需 cross-origin isolation（COOP/COEP），在嵌入式環境通常拿不到，不要依賴。
- createImageBitmap（2048² PNG blob 解碼）28 ms；可在 Worker 使用，ImageBitmap 可 transfer。
- 編碼（2048² 含少量內容）：toDataURL PNG 26 ms、toDataURL JPEG 46 ms、OffscreenCanvas.convertToBlob PNG 19 ms。convertToBlob 非同步、不阻塞主執行緒，且不經 base64（base64 實測膨脹 1.3334 倍，即 +33%）。
- 4096² 高熵雜訊 PNG：toDataURL 906 ms，字串 85.7 MB；以 data URI 餵給 Image 解碼 1410 ms。4096² 網點（稀疏黑點）PNG：100 ms，0.5 MB，所以印刷用 1-bit 內容 PNG 很小，data URI 負擔可忽略；真正貴的是連續調/雜訊內容。
- 嚴格 CSP（blob: 被擋）：只能 data:。策略：Worker 回傳 ArrayBuffer（PNG 位元組或原始平面），主執行緒用 `btoa` 分塊或 FileReader.readAsDataURL（對 Blob 仍可用，不需要 blob: URL）轉 data URI；預覽盡量直接畫進顯示用 `<canvas>`（canvas 本身不受 img-src 影響），僅在必須成為 `<img>`/CSS mask 時才轉 data URI。注意 `img-src` 要含 `data:`；Worker 本身若從 blob: 建立也可能被 `worker-src`/`script-src` 擋，需要 data: Worker 或同源檔案（請確認嵌入環境 CSP 的 worker-src）。

## 3. Worker 池與並行

- `navigator.hardwareConcurrency`：本機測試環境回報 2。Safari 回報值被上限/粗化（歷史上 iOS 回報偏低）。建議 `n = clamp(hardwareConcurrency - 1, 1, 8)`，並保留 1 核給 UI。（本沙箱僅 2 核，無法實測多核擴展，下為理論/經驗推估，未量測。）
- 可平行（逐像素獨立）：門檻、有序（Bayer/clustered-dot）、藍噪音遮罩查表、AM/FM 網點由座標計算的旋轉網屏、分色矩陣、混合模式合成。以水平條帶（行數 / worker 數）切分；條帶高度為 L2 友善（例如 64-256 行）並用工作佇列動態分派以平衡。理論加速接近核心數。
- 網屏旋轉：網點角度由座標變換決定，不依賴鄰域，因此切 tile 時只需傳全域座標偏移（tile 原點 x0,y0），結果與整圖相同。
- 誤差擴散（Floyd-Steinberg 等）：依賴左與上方鄰居，嚴格序列。選項：(a) 每色版一個 worker（4 版 CMYK 天然 4 路並行，最實際）；(b) wavefront/斜線並行（Floyd-Steinberg 依賴 (x-1,y)、(x-1,y+1)、(x,y+1)... 沿 x+2y 的反對角線可並行，但需 SharedArrayBuffer + 同步，在無 cross-origin isolation 時不可行）；(c) 切成帶狀並在帶邊界重疊 ~16-32 行再丟棄（近似，邊界有輕微不連續，與序列結果非位元一致，預覽可用、輸出不建議）；(d) 改用藍噪音/有序抖動取代，以得到可平行且 deterministic 的 FM 效果。建議：輸出用 (a)+(d)，預覽用 (d)。
- 單核誤差擴散成本：整數版 ~7 ms/MP，A4@600dpi 單版（約 35 MP）≈ 240 ms（本機）— 對匯出完全可接受，並不一定需要平行化。

## 4. 記憶體（A4 @ 600 dpi = 4961 × 7016 ≈ 34.8 MP）

| 表示 | 單版 | 4 版 CMYK | 6 版（含專色/白/燙箔） |
|---|---|---|---|
| Uint8 連續調 | 34.8 MB | 139 MB | 209 MB |
| Float32 | 139 MB | 557 MB | 835 MB |
| 1-bit 打包 | 4.35 MB | 17.4 MB | 26 MB |
| RGBA 預覽 canvas（每張） | 139 MB | | |

- 一張 A4@600dpi 的 RGBA canvas 就是 139 MB；多張 canvas 在 iOS Safari 很快撞牆（pqina 報告 iOS 15 總 canvas 記憶體上限約 384 MB，4096×4096=64 MB 為其單張上限；舊 iOS 單張面積上限約 16,777,216 像素；桌機 Chrome 約 16384 邊長 / 268 M 像素面積；Firefox 單邊 32767。數字隨版本/裝置變動，請用 canvas-size 函式庫在執行時探測）。
- 策略：(1) 不為每版建立 canvas，用 Uint8Array 平面；(2) 以 tile（如 512×512 或 1024×1024，1 MB/4 MB）逐塊處理：讀來源→分色→網點→合成→編碼，不產生整頁中間圖；(3) 匯出 PNG 時每色版以 1-bit/8-bit 灰階 PNG 逐 tile 編碼會較複雜（PNG 需串流 IDAT），可行做法是自寫 PNG 容器 + CompressionStream('deflate')（Chrome/Safari 16.4+/Firefox 113+）逐行壓縮；(4) 可重用緩衝（pool），避免 GC 抖動；(5) 大陣列 transfer 後立即釋放引用。
- 避免中間圖：把「分色→網點→著色→合成」融合成單一每像素函式，對每個輸出 tile 只讀一次來源，寫一次輸出。

## 5. WebGL2 / WebGPU 作為選配加速

- 網點（門檻、有序、旋轉網屏、藍噪音查表）本質是逐像素函式，非常適合 fragment shader：GPU 上 16 MP 通常 < 5 ms（推估，沙箱僅軟體渲染，不量測）。誤差擴散不適合。
- 限制：MAX_TEXTURE_SIZE 沙箱為 8192（桌機常 16384，行動裝置常 4096-8192），A4@600dpi 長邊 7016 在某些裝置會超限，必須 tile 渲染。readPixels 同步回讀會卡頓；GPU 結果浮點精度（mediump）可能與 CPU 不一致，影響「預覽 == 匯出」的位元一致性。
- WebGPU：Chrome 113+、Safari 26、Firefox 較晚（Windows 141），覆蓋仍不完整，且嵌入式 Chromium 可能關閉。本沙箱 `navigator.gpu` 為 false。
- 建議：CPU（TypedArray + Worker）為唯一的「真值」實作，保證 deterministic 且在所有環境（含嚴格 CSP、無 GPU）可跑；WebGL2 僅作為互動預覽的可選加速，並在啟動時做小型自檢（對固定測試圖與 CPU 結果比對），不一致或不支援就退回 CPU。匯出一律走 CPU。

## 6. 預覽/匯出解析度獨立與確定性

- 把場景定義在「物理單位」（mm 或 1/600 inch 座標）上，網點用世界座標（x_mm, y_mm）計算網屏相位，而非像素索引。預覽只是以不同取樣密度評估同一函式；匯出為 600 dpi 評估。預覽低解析度時，網點週期（例如 150 lpi ≈ 0.17 mm）會小於預覽像素而產生 aliasing/moiré，所以預覽應：(a) 放大到實際像素密度檢視時才運行真實網點；(b) 縮小檢視時顯示以網點覆蓋率（連續調）近似的結果。
- 確定性隨機：不使用 Math.random。使用種子化 PRNG（mulberry32 / sfc32 / xoshiro128**），或更好的「無狀態雜湊」h(seed, x, y)（如 PCG / 整數 hash，以 Math.imul 實作），使每個像素的隨機值只取決於世界座標與種子，與 tile 順序、worker 切分無關。這樣預覽 tile、匯出 tile 與整圖結果一致。避免 Math.sin 式雜湊（跨 GPU/引擎精度不同）；浮點運算要避免 fused-multiply-add 差異，儘量用整數運算。藍噪音遮罩以固定資產（內嵌 data URI 的 64×64 或 128×128 Uint8）tile 取用，取樣座標 = 世界座標 mod 遮罩尺寸。
- CSS mask-image：尺寸沒有明確規範上限，實務受限於圖片解碼上限與 GPU 紋理大小；大 mask 會被降採樣或以 tile 方式處理。SVG 作為 mask-image（含 data: URI）在 Chrome/Safari 中通常是先光柵化到「元素的設計尺寸 × device pixel ratio」，之後 CSS transform: scale()（縮放）只是縮放已光柵化的紋理，因此放大會模糊；瀏覽器不一定在 transform 變更後重新光柵化（Chrome 的 will-change: transform 會明確鎖定紋理，沒有它時 Chrome 可能在縮放動畫結束後重新光柵化）。Safari 通常較容易保持模糊。這部分我未在沙箱以三引擎實測，屬經驗性說明，建議以小測試頁驗證。
  對策：(1) 縮放用改變元素實際寬高（或 mask-size）而不是 transform: scale；(2) 或不用 CSS mask，直接在 `<canvas>` 以目前縮放比用 `destination-in`/`globalCompositeOperation` 繪製，並在縮放停止後以 devicePixelRatio × zoom 重繪（debounce）；(3) 避免 mask 用位圖 PNG data URI（放大一定糊），優先向量 SVG 並在縮放後重新設置 mask-size。

## 7. 大型 data URI 上限（MDN Data URLs 頁面）

- Chromium 512 MB；Firefox 512 MB（136 起；97 起 32 MB，之前 256 KB）；Safari（WebKit）2048 MB。皆指 URL 字串長度，二進位有效載荷約其 75%（base64 +33%，實測 1.3334）。
- 實測 Chromium：85.7 MB 的 data URI PNG 可解碼（1.4 s）。200 MB 的字串可建立並嘗試載入（未在此判斷渲染成功）。
- 實務限制並非 URL 上限，而是：字串記憶體（UTF-16 時最多加倍）、解碼時間、以及 CSS 中嵌入 data URI 對樣式解析的負擔。建議單一 data URI 控制在 < 10 MB；較大資源分塊或改用 canvas 直接繪製。
- 嵌入環境若 CSP 禁 blob:，確認 img-src 含 data:，且 style-src 允許 CSS 內 data: URL（由 img-src 管轄）。

## 建議摘要

1. CPU 為真值：Uint8 平面 + 整數運算 + Uint32 寫入，Worker 池（核心數-1，上限 8），條帶/tile 動態分派，transfer ArrayBuffer。
2. 網屏用世界座標與無狀態整數雜湊，預覽與匯出共用同一函式 → 位元一致。
3. 誤差擴散以「每色版一 worker」平行；需大量平行時改用藍噪音或有序抖動。
4. 匯出 tile 化、1-bit 打包 PNG 串流；避免整頁 RGBA canvas（A4@600dpi 139 MB/張）。
5. 嚴格 CSP：不依賴 blob:，用 canvas 直接顯示，必要時 data URI，大小 < 10 MB。
6. WebGL2/WebGPU 僅選配預覽，附啟動自檢與 CPU 退回。
7. 縮放預覽避免 CSS transform 放大 mask；改用實際尺寸或 canvas 重繪。

## 來源
- MDN OffscreenCanvas：https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas
- MDN Data URLs：https://developer.mozilla.org/docs/Web/HTTP/Basics_of_HTTP/Data_URLs
- pqina Safari canvas 記憶體：https://pqina.nl/blog/total-canvas-memory-use-exceeds-the-maximum-limit/
- canvas-size：https://github.com/jhildenbiddle/canvas-size
- 本機 benchmark：/root/work/research/bench/b.js、c.js
