# Rotation Study: 10 Oversold Large Caps vs. MSFT / PLTR / TSLA

**Prepared:** Saturday 2026-10-10 (data as of Friday 2026-10-09 close unless noted)
**Scope:** WM, WMT, PEP, AXP, MCD, MGM, LVMUY, NFLX, APP, FICO vs. benchmarks MSFT, PLTR, TSLA
**Status:** Research note. **Not financial advice.** Every number below is from public web sources retrieved via search on 2026-10-10; direct market-data APIs and most quote pages were unreachable from this environment (DNS/proxy blocked), so figures come from search-engine excerpts of aggregator pages and are flagged where they conflict or could not be verified.

**Re-check with live data:** `python scripts/rotation_screener.py --csv rotation.csv` recomputes RSI, moving averages, ATM IV/greeks, put/call ratios, fundamentals, earnings dates and seasonality from Yahoo Finance, with trim scores for MSFT/PLTR and entry scores for the 10 candidates. Run it before each tranche in Section 10.

---

## 0. Executive summary

- **The user's pasted figures check out on price:** MSFT $535.07, PLTR $209.05, TSLA $382.70 are the verified Oct 9 closes. MSFT 30-day IV ~32% is consistent with ApexVol (Oct 2-5). PLTR 30-day IV ~57% is close (AlphaQuery Oct 6: 54.5%). WMT IV ~23% matches (Oct 5-8). The user's drawdown figures are roughly right but several are stale: WMT is ~-18% from high (not -22%), AXP ~-20% (not -27%), WM ~-16%, MGM ~-43%, LVMUY ~-44%, NFLX ~-44%, APP ~-62%, FICO ~-67%, MCD ~-31%, PEP ~-27%.
- **Macro backdrop (Oct 9):** S&P 500 7,811.54 (+0.6%, ~record), Nasdaq 27,366 (+0.64%), VIX 14.84, **10-year Treasury ~5.24% (hit ~5.37% Wednesday, highest in 24 years)**. High long rates are the single biggest common headwind to the dividend/consumer names on this list and the biggest reason the "rotation into defensives" trade has not worked yet.
- **Ranking for rotation (best to worst):** Tier 1 (buy on triggers): **AXP, WMT, PEP**. Tier 2 (accumulate after earnings): **MCD, WM, NFLX**. Tier 3 (small, event-driven): **MGM, LVMUY**. Tier 4 (avoid for now / falling knives): **APP, FICO**.
- **Source positions:** PLTR just printed a new 52-week high on a Goldman upgrade (+5.2% Oct 9, RSI likely >70, IV ~55%, earnings ~Nov 2 unconfirmed): trim into strength or collar now. MSFT is 3% off its high with earnings confirmed Oct 28 (implied move ~7-8%): hold core through earnings with covered calls, trim into post-earnings strength.
- **Key dates:** LVMH Q3 sales Oct 12; NFLX Oct 20; TSLA Oct 21; AXP Oct 23; WM Oct 27; MSFT & MGM Oct 28; PLTR ~Nov 2 (est.); MCD, APP, FICO ~Nov 4 (MCD/FICO unconfirmed); WMT ~Nov 19 (est.).

---

## 1. Data-quality note (read first)

- WebFetch to stockanalysis, finviz, barchart, marketchameleon, optioncharts, investing.com, tradingview, Yahoo, Nasdaq, CNBC, Morningstar, Zacks, SEC, etc. all failed (ENOTFOUND / proxy 403). Only WebSearch worked, which returns excerpts of those pages. Consequently:
  - **Prices/52-week ranges/earnings dates:** mostly cross-checked across 2+ sources; flagged where not.
  - **RSI / moving averages:** aggregator snapshots dated Oct 1-8; values conflict across vendors (different smoothing/dates). I give a range and the most recent reading.
  - **Options data (IV, IV rank, put/call):** mostly Sep 18 - Oct 8 snapshots; several are undated. LVMUY has no usable options data (illiquid ADR chain).
  - **Greeks:** no source showed a live chain, so ATM Greeks are **Black-Scholes estimates computed by me** (Section 4) from the IV estimates, r = 4.0% (assumed), Nov 20, 2026 expiry (41 DTE). Label: *computed estimate*.
  - **Forward P/E and consensus targets:** mostly June-Sept snapshots; "derived" means I rescaled a dated P/E to the current price.
  - **Seasonality:** from tickerleague/chartrow/equityclock/seasonax excerpts; several are my arithmetic on year-by-year tables with 5-16 year samples. Treat as weak priors.

---

## 2. Snapshot table (as of 2026-10-09 close)

| Ticker | Close | 1-day | 52w Low | 52w High | % from High | Mkt cap | Next earnings | Verified? |
|---|---|---|---|---|---|---|---|---|
| **MSFT** | 535.07 | +2.38% | 349.20 | 553.72 | -3.4% | ~$3.97T | **Oct 28 AMC (company-confirmed Oct 7)** | Yes (multiple) |
| **PLTR** | 209.05 | +5.17% | 106.37 | 209.58 (set Oct 9) | -0.3% (new 52w high) | ~$502B | Nov 2 AMC (**unconfirmed**, calendars) | Yes (Yahoo/Investing/Google) |
| **TSLA** | 382.70 | +2.05% | 297.38 | 498.83 | -23.3% | ~$1.51T | **Oct 21 AMC (company 8-K)** | Yes |
| **WM** | 208.83 | -0.6% | 194.11 | 248.13 | -15.8% | ~$83B | **Oct 27 AMC (company PR Sep 24)** | Yes (Yahoo) |
| **WMT** | 111.35 | +0.71% | 98.88 (Nov 14 '25) | 135.16 (May 19 '26) | -17.6% | ~$890B (derived) | ~Nov 19 BMO (**est.**) | Yes (Yahoo/MarketBeat/CNBC) |
| **PEP** | 125.97 | ~flat | 123.47 (Oct 7 '26) | 171.48 (Feb 12 '26) | -26.5% | ~$173B (derived) | Reported Q3 on Oct 8; next ~early Feb 2027 | Yes (Morningstar/CNBC) |
| **AXP** | 308.17 | +0.33% | 290.97 (Mar 20 '26) | 387.49 (Dec '25) | -20.5% | ~$214B (derived) | **Oct 23 BMO** | Yes (Yahoo) |
| **MCD** | 235.23 | -0.70% | 229.20 (Oct 5 '26) | 341.75 | -31.2% | ~$168B (derived) | ~Nov 4 BMO (CNBC/Trefis; **not company-confirmed**; one calendar says Oct 28) | Yes (CNBC/Macrotrends/CNN) |
| **MGM** | ~29.4-29.7 (**unconfirmed**; Oct 8 close 30.01) | ~-1 to -2% | 29.19 | 51.59 | ~-43% | ~$8B (derived) | **Oct 28 AMC (confirmed)** | Partial |
| **LVMUY** | 85.20 (Morningstar, delayed) | -0.77% | 84.62 | 152.95 | -44.3% | ~€190B / ~$210B (derived from Paris line €381) | **Q3 sales Oct 12 after Paris close** | Partial (ADR); Paris line €381.45 on Oct 7 vs 52w low €376 |
| **NFLX** | 70.30 | -1.77% | 65.08 (Jul 17 '26) | 124.86 | -43.7% | ~$291B (derived) | **Oct 20 AMC** | Yes |
| **APP** | 277.04 | -1.10% | 266.84 (Oct 2-3 '26) | 738.01 | -62.5% | $92.7B | **Nov 4 AMC (company-confirmed)** | Yes (Morningstar/CNN) |
| **FICO** | 667.58 | **-5.63%** (prev 707.43) | ~588-617 (intraday ~Oct 1; **unverified**) | ~1,998 | -66.6% | ~$14.5B | ~Nov 4 AMC (**est.**, not announced) | Yes (StockAnalysis/Finviz/MarketBeat) |

---

## 3. Technicals and recent price action (last 2-4 weeks)

| Ticker | RSI(14) (date, source) | vs 20/50/200-day SMA | MACD / read | Recent action & levels |
|---|---|---|---|---|
| MSFT | 44 (Oct 8, Investing.com) vs 62.6 (Oct 5, Trendlyne) - **conflict** | Above 50d (~522.6) and 200d (~506) per Investing.com | Investing.com "Strong Sell" summary vs price above both MAs - mixed | Choppy near highs: -1.35% Oct 8 on tech selloff, +2.38% Oct 9 rebound. Resistance 553.72 (52w high). Support ~522 (50d) then ~506 (200d). Not overbought. |
| PLTR | 66.1 (Oct 7, pre-jump); likely ~70-75 after +5.2% | Above 20d (~183) and 50d (~174); 200d not found (~150-160 est.) | Stochastics 97/88 overbought (Oct 7) | Broke out to new 52w high $209.58 on Oct 8 Goldman upgrade to Buy ($230 PT). Parabolic short-term: ~+14% from Oct 3 ($188.75). First support ~$198 (Oct 9 low), then $183 (20d). |
| TSLA | 58.8 (Oct 4, Financhill); ~64 (Oct 2, Investing) | Above 50d (~349), **below 200d (~393)** | 11/12 indicators bullish (Financhill) | +2% on Oct 2 delivery beat; grinding higher pre-earnings. Resistance 393 (200d) then ~400. Support ~375/349. |
| WM | 41.7 (Oct 6, Gotrade); one vendor shows 75 (likely wrong) | **Below 50d (218.6) and 200d (224.7)** | MACD -3.97, bearish | Range-bound 205-210 since late Sept after Sept slide from ~228. Support 194-199 (52w low zone); resistance 214-218 (Aug range floor / 50d). |
| WMT | 52.9 (Oct 8); 43.3 (Oct 6) | Reclaimed 20d (~107) and 50d (~108.6) on Oct 7-9; **below 200d (~120)** | Stochastic turning up from oversold | Recovering: 105 (Oct 6) -> 111.35. Three up days. Support 105-107; resistance 115-118, then 120 (200d). |
| PEP | ~25 (Oct 4, TradingKey); 16 (Oct 2, StockInvest) - oversold pre-earnings | Below all MAs; 200d ~147 | Descending channel | New 52w low 123.47 on Oct 7 (analyst downgrades), then Oct 8 earnings: beat + guidance cut, +3% intraday, faded to ~flat. Support 123.5; resistance 129.2 / 132.3 / 135.5. |
| AXP | 25.5 (Investing, undated) to ~45 (Financhill) - **conflict**; likely 35-45 | **Below 50d (~317) and 200d (~330-337)**; 50d < 200d (death cross) | Bearish | -7.3% past month. $350M AML penalty Oct 8 (guidance unchanged) absorbed with +0.33% Oct 9. Support 300 then 291 (Mar low); resistance 317 (50d), 330. |
| MCD | 17-40 (Oct 5, vendors disagree); 23.6 (Oct 1, ChartMill) - oversold | Below 50d (~234-255) and 200d (~251-275); death cross | MACD negative | New 52w low 229.20 Oct 5 after Investor Day ("tough conditions are the baseline"). Bounced to 235-237. Support 229; resistance 246 (prior low), 250 (200d). |
| MGM | **11.7 (Oct 2, Financhill) - extreme oversold** | Far below 50d (~41) and 200d (~39.75) | Sell signal since Sep 11 (-23%) | Gapped -10% Sep 24 on People Inc. withdrawal of $48.30 bid; drifted to 29.19 52w low. Support 29.2; resistance 32.6 (Sep 26) then 34-36. |
| LVMUY | 31.0 (Oct 8, WallStreetBuys) | 12.8% below 50d; below 200d | Vendor "Strong Sell" | Sitting ~1% above 52w low into Oct 12 Q3 sales. Paris: €381 vs €376 low; 52w high €654.70. Support 84.6 (ADR); resistance ~92-95. |
| NFLX | 32.9 (Oct 5, SwingTradeBot) | Below 50d (75.5) and 200d (83.9); ADX 27 (strong downtrend) | Down across all horizons | Grinding down toward Jul low 65.08; -1.8% Oct 9. Support 65-68; resistance 75.5 (50d). |
| APP | 15.6-29 (Oct 1-2) - oversold | Below 20d (~315), 50d (~333), 200d (~458) | Bearish; 9 straight down days to Oct 5 (-19%) | New 52w low 266.84 Oct 2-3 (court denied APP's bid vs Unity). Support 267 then ~220 (technical); resistance 300, 315 (20d). |
| FICO | 21.8 (Oct 7, StockRSI); 26 (StockScan) | Far below all MAs; death cross | Stochastic exited oversold Oct 7 then **broke down again Oct 9 (-5.6%)** | -27% on FHFA single-grid announcement (~Sep 29-30), -40% in 30 days. Oct 9 broke $673 floor. Next support ~617 (close on crash day) / ~588; resistance 706. |

---

## 4. Options: IV, positioning, implied moves and estimated Greeks

### 4a. Sourced options data

| Ticker | 30d ATM IV (date/source) | IV rank / percentile | Put/Call (vol / OI) | Notable flow / implied earnings move |
|---|---|---|---|---|
| MSFT | **32.0%** (Oct 2-5, ApexVol) | IV rank 32, 1y pct 32 (ApexVol) | ~0.55-0.68 (OptionVisualizer / ApexVol range) | Implied move into Oct 30 weekly **~7.9%** (OptionSlam); avg historical earnings move ±5.3%. |
| PLTR | **54.5%** (Oct 6, AlphaQuery) | 19-37 (sources conflict) | 0.76 / 1.03 (Oct 6, AlphaQuery) | Front-expiry expected move ±8.8% (Sept snapshot). Last earnings reaction +29.5%. No current earnings-specific implied move found. |
| TSLA | 38-44% (Sep 10 opti-view 38.1%; Barchart 43.9% undated) | 13-29 | 0.60-0.92 / 0.74-0.78 | Expected front-month move ±6.6% (Sept). Earnings Oct 21. |
| WM | ~20% (Sep 18, OptionSamurai) | IV rank ~25 (Sep 18); 19 (Barchart undated) | 0.63 / 0.58-1.03 | Low-vol name; premiums cheap. |
| WMT | **23.0%** (Oct 5) / 23.1% calls (Oct 8, AlphaQuery) | IV rank ~23 (Oct 5) | **0.31 / 0.40 (Oct 8) - very call-heavy (bullish)** | Max pain $110; expected move 6.6% (Oct 5 snapshot). |
| PEP | 24.4% (Sep 18, pre-earnings; likely lower now) | IV rank ~52 (Sep 18) | 0.47-0.93 OI (conflicting dates) | Earnings passed (Oct 8). |
| AXP | ~30% (Sep 30, AlphaQuery) | not found (Oct 2025 snapshot showed 25) | **OI P/C 1.71 (Sep 30) - put-heavy/hedged** | Historical implied earnings move ~3.5% (July). Earnings Oct 23. |
| MCD | 23.7% 3-mo (Sep 23); ~31% Nov-expiry (Macroaxis) | 39-54 (conflicting) | Call-heavy: call/put 1.64x on Sep 23 52w-low day (contrarian signal) | Nov expiry max pain ~$260 (stale). |
| MGM | ~56% (Barchart, undated) | ~59 (undated) | 0.35 / 1.12 | Call volume +143% vs avg on Sep 21 (pre-withdrawal); TipRanks noted P/C ~1.87 spike post-withdrawal. |
| LVMUY | **No usable data** (ADR options chain essentially empty) | n/a | n/a | Trade exposure via Paris line or basket if options needed. |
| NFLX | **45.2%** (Oct 7, OptionsAnalysisSuite) | **IV rank 74** (Oct 7) | 0.54 / 0.65 (Oct 5) | **Expected move through Oct 20 earnings ~12-13%**; historical avg earnings move ~11%. Premium rich - sell, don't buy. |
| APP | **65.7% 3-mo** (Oct 2, Investing.com) | not found | ~1.09 vol (43.6k puts vs 40k calls, Oct 2); OI 0.73 (Fintel, undated) | Nov 20 $270/$280 put spread; Oct 16 $300 calls 4x OI; Jun 2027 $600 call. Skew flat (no crash premium). |
| FICO | 52-57% (Jul-Sept Barchart snapshots; **stale**; 52w IV range 33-75%) | ~45-62 (stale) | 0.91 vol (Jul) | Zacks Strong Sell (Oct 9-10). No current snapshot; IV likely near the top of range after -40%/30d. |

### 4b. Black-Scholes ATM Greeks - **computed estimates, not sourced** (r = 4.0% assumed, expiry Nov 20 2026 = 41 DTE, strike = spot)

| Ticker | Spot | IV used | Call Δ | Put Δ | Γ | Θ/day (call, $) | Vega ($ per 1 vol pt) | ATM straddle ≈ | 1σ 30-day move |
|---|---|---|---|---|---|---|---|---|---|
| MSFT | 535.07 | 32% | 0.54 | -0.46 | 0.0069 | -0.31 | 0.71 | $45.70 (8.5%) | ±$49 (±9.2%) |
| PLTR | 209.05 | 55% | 0.55 | -0.45 | 0.0103 | -0.20 | 0.28 | $30.64 (14.7%) | ±$33 (±15.8%) |
| TSLA | 382.70 | 42% | 0.54 | -0.46 | 0.0074 | -0.28 | 0.51 | $42.87 (11.2%) | ±$46 (±12.0%) |
| WM | 208.83 | 21% | 0.54 | -0.46 | 0.0270 | -0.08 | 0.28 | $11.72 (5.6%) | ±$12.6 (±6.0%) |
| WMT | 111.35 | 23% | 0.54 | -0.46 | 0.0463 | -0.05 | 0.15 | $6.84 (6.1%) | ±$7.3 (±6.6%) |
| PEP | 125.97 | 22% | 0.54 | -0.46 | 0.0427 | -0.05 | 0.17 | $7.41 (5.9%) | ±$8.0 (±6.3%) |
| AXP | 308.17 | 30% | 0.54 | -0.46 | 0.0128 | -0.17 | 0.41 | $24.68 (8.0%) | ±$26.5 (±8.6%) |
| MCD | 235.23 | 25% | 0.54 | -0.46 | 0.0201 | -0.11 | 0.31 | $15.71 (6.7%) | ±$16.9 (±7.2%) |
| MGM | 29.50 | 55% | 0.55 | -0.45 | 0.0729 | -0.03 | 0.04 | $4.32 (14.7%) | ±$4.65 (±15.8%) |
| LVMUY | 85.20 | 32% (assumed from HV; no IV data) | 0.54 | -0.46 | 0.0435 | -0.05 | 0.11 | $7.28 (8.5%) | ±$7.8 (±9.2%) |
| NFLX | 70.30 | 45% | 0.54 | -0.46 | 0.0374 | -0.05 | 0.09 | $8.44 (12.0%) | ±$9.1 (±12.9%) |
| APP | 277.04 | 66% | 0.55 | -0.45 | 0.0065 | -0.31 | 0.37 | $48.70 (17.6%) | ±$52 (±18.9%) |
| FICO | 667.58 | 60% (assumed; stale sources) | 0.55 | -0.45 | 0.0029 | -0.68 | 0.89 | $106.72 (16.0%) | ±$115 (±17.2%) |

Reading: a ~45-delta put bought on MSFT costs roughly 4%+ of notional for 41 days; a 25-delta covered call on PLTR (roughly the $240 strike) should fetch several percent of notional given 55% IV. These are planning magnitudes only; pull a live chain before trading.

---

## 5. Fundamentals and profitability

| Ticker | Last quarter (date) | Revenue growth | Margin | FCF | Fwd P/E (quality) | Div. yield | Consensus / targets |
|---|---|---|---|---|---|---|---|
| **MSFT** | FQ4'26 (Jul 29) | Rev $90.0B **+18%**; Azure +43% (guided +45% cc for FQ1) | GM 67.2%; op income +18% | Not retrieved (FY26 10-K) | ~27-30x FY27 (**derived/unverified**; one July source implied ~38x at $465) | ~0.7% | Targets: MarketBeat $579 (48 analysts), Yahoo $588; Wells $725 (Oct 1), Evercore $635 (Oct 7). FQ1 guide rev $89.85-90.95B; calendar-2026 capex ~$175B. |
| **PLTR** | Q2'26 (Aug 3) | Rev $1.935B **+93%**; US commercial +149% | GAAP op margin 47%; adj 62% | Adj FCF $1.22B (63% margin) | **~85-90x fwd** (GuruFocus 90x; TradingKey ~85x) | 0 | Consensus ~$196-208; Goldman upgrade to Buy $230 (Oct 8). FY26 guide $8.15B (+82%). Q3 guide $2.160-2.164B. |
| **TSLA** | Q2'26 (Jul); Q3 deliveries Oct 2 | Q3 deliveries 486,532 (-2.1% y/y, beat cons. ~462k); Q2 rev $28.2B | Q2 GAAP GM 16.8%, **op margin 1.4%** | n/a | >100x (mid-2026 source cited 167x; **stale**) | 0 | Mean PT ~$402-425, consensus Hold. |
| **WM** | Q2'26 (Jul 28) | Rev $6.68B +4% (slight miss); FY rev guide cut to $26.3-26.5B | Adj EBITDA margin 30.9% (+40bp); GAAP op margin 18.7% | **$1.10B (+34.5%)**; FY FCF guide $3.75-3.85B kept | ~22x (derived from stockhub 25.4x at $245) | ~1.6% | Consensus Moderate Buy, PT ~$253-263 (stale); UBS $270. Leverage 2.96x. |
| **WMT** | FQ2'27 (Aug 20) | Rev $187.9B **+5.9%**; US comps +2.6% (6-yr low; drug-price caps cost ~80-90bp; >$2B fuel costs) | Op margin 5.0% (flattered by tariff refunds) | H1 FCF $5.5B (down $1.4B on capex) | ~38x FY27 EPS ~$2.92 (**derived**) | ~0.85% | Argus Buy $130; "Buy, avg $130.35" (one source); stock fell 9% on weak Q3 op-income guide; Q3 guide adj EPS $0.62-0.64. |
| **PEP** | Q3'26 (Oct 8) | Rev $25.27B +5.6%; organic +3.1% | Op margin 16.9%; core margin ~flat | n/a | **~15x** (derived: $126 / FY26 core EPS ~$8.35-8.42) | **~4.7%** ($5.92) | FY26 core EPS growth cut to +2.5-3.5% (CNBC) / +1-2% cc (other) - **conflict**. Targets being cut: RBC $150, MS $145; consensus Hold ~$150-158. |
| **AXP** | Q2'26 (Jul 24) | Rev $19.6B **+10%**; FY guide raised to 10% | Net margin ~15.8%; EPS $4.53 +11% | n/a (financial) | **~17-18x** (derived from 19.4x at $351) | ~1.2% ($3.80) | Consensus ~$371-375 (July, stale); recent cuts TD Cowen $335, UBS $345. $350M AML penalty (Oct 8): guidance 2026/2027 unchanged, no asset cap. |
| **MCD** | Q2'26 (Aug 4) | Rev $7.10B +3.7%; **global comps +1.3%, US +0.8%** | Op margin ~46-47% (franchise model) | n/a | **~16.5x** (derived: $235 / FY1 EPS $14.19) | **~3.2%** ($7.44; Oct dividend raise likely) | Consensus was Moderate Buy $336 (June); now cuts: Wells $270, Guggenheim $250; Citi Buy maintained. Investor Day: "high inflation / flat traffic is the baseline"; $8.5B investment plan; AI-pricing concerns. |
| **MGM** | Q2'26 (Jul 29) | Rev $4.5B +1%; Vegas +3%, digital +20%, regional -4% (asset sales) | Op margin 11.3%; adj EPS $0.59 (vs $0.79) | ~$317M/qtr (OCF $559M - capex $241M); cash $2.5B | **~15x** FY26 adj EPS ~$2.00 (derived) | 0 (buybacks) | Post-withdrawal: BofA Neutral $40, Mizuho Outperform $55, UBS $46, Truist Buy; consensus ~$49 (stale). People Inc. (27% holder) pulled $48.30 bid Sep 23; WSJ: MGM may bid for People Inc. (unconfirmed). |
| **LVMUY** | H1'26 (Jul 27) | Rev €38.6B -2.9% reported, **+2% organic**; Q2 +3% organic; F&LG -1% organic; W&J +9% | Op margin 22.5% (-10bp) | Op FCF €4.1B | ~16x (**derived**; Barclays cited ~18x earlier) | ~3.4% (derived at €381) | Consensus €570 (Aug, stale; range €420-660); Bernstein trimmed on China; RBC downgrade. **Q3 sales Oct 12** - no consensus found; Q2 run-rate +3% organic is the bar. |
| **NFLX** | Q2'26 (Jul 16) | Rev $12.6B **+13%**; Q3 guide $12.86B (< $13B cons.) | **Op margin 33.4%**; Q3 guide 33.2%; FY 31.5% | **FY26 FCF guide ~$12.5B** | ~19-20x (derived; trailing P/E 21.6) | 0 | Consensus $93-114 (conflicting dates); 71% Buy. Sarandos Oct 1: subscriber growth "not as fast as we want". Reed Hastings departure; Warner deal abandoned; $2.8B termination fee distorting accounts. |
| **APP** | Q2'26 (Aug 5) | Rev $1.924B **+53%** (just below guide midpoint) | Adj EBITDA $1.614B (84%); **net margin ~66%** | $863M (conversion to normalize ~75% of EBITDA) | ~17-18x (derived; EPS run-rate ~$15) | 0 (buybacks $551M/qtr) | BofA Neutral $400 (Aug 11, 2027 growth cut to 23%); Wells EW; BTIG Buy $396; stale consensus ~$497. SEC inquiry closed with no action. Lawsuit vs Unity: court denied APP's bid (Oct 2). |
| **FICO** | FQ3'26 (Jul 29) | Rev $674M **+26%**; Scores +41%; Software +2% | **Non-GAAP op margin 62%** | $370M qtr; TTM $961M | **~15.7x** FY26 non-GAAP EPS guide $42.43 (**but FY27 estimates not yet reset**) | 0 | Goldman Buy $1,322; RBC Outperform; Barclays $935; Baird $1,070; BofA cut target in half; Huber Underweight; Zacks Strong Sell. |

---

## 6. Sentiment and drawdown thesis (cyclical vs. structural)

| Ticker | Why it is down | My read |
|---|---|---|
| WM | Volume softness, FY revenue guide cut, rates at 24-yr high hitting bond-proxy/defensive multiples; technically weak since Sept. | **Cyclical/valuation reset.** Business intact (margins expanding, FCF +34%). Modest -16% drawdown; not a bargain at ~22x but a quality compounder. |
| WMT | Weak Q3 operating-income guide, drug-price caps (80-90bp comp drag), $2B fuel costs, Target's holiday discounting, rising yields vs defensives. | **Cyclical/mostly temporary** (policy drag is known and annualizes), but multiple (~38x) still rich. Momentum has turned up; options flow bullish. |
| PEP | Volume declines in snacks (Frito-Lay), GLP-1 narrative, cost inflation, guidance cut, downgrades. | **Mostly cyclical with a slow structural overhang** (snack volumes). At 15x and 4.7% yield the bad news is largely priced; earnings catalyst is behind it. |
| AXP | Spend-growth deceleration worries, target cuts, premium-card competition, AML consent orders, financials de-rating with the curve. | **Cyclical/sentiment.** 10% revenue growth, 17x, buyback machine. Oct 23 print is the catalyst; put/call 1.7 shows heavy hedging (contrarian-positive if it holds). |
| MCD | US traffic flat, value-menu execution, CEO "tough conditions are the baseline", AI/dynamic-pricing backlash, GLP-1, downgrades. | **Half cyclical, half structural (US traffic).** Franchise model keeps margins ~46% and dividend safe; 16.5x and 3.2% yield is the cheapest MCD has been in years. Needs comps to stabilize. |
| MGM | Takeover bid withdrawn (premium collapse), Vegas/Macau softness, adj EPS down y/y, leverage. | **Event-driven, cyclical.** No fundamental break; RSI 11 says forced selling. But it is a levered consumer-discretionary casino into a 5.2% 10-year. Small size only. |
| LVMUY | Luxury demand slowdown (China, aspirational US consumer), F&LG organic -1%, margin squeeze, FX, downgrades. | **Cyclical trough with a long duration.** Organic growth has already turned positive (+3% Q2). Oct 12 is binary. Buy only on evidence. |
| NFLX | Growth deceleration (13% -> ~12%), Q3 guide miss, abandoned Warner deal + $2.8B fee, Hastings departure, Sarandos "sub growth slower than we want". | **Deceleration de-rating, not a broken model** (33% op margin, $12.5B FCF). ~19-20x is the cheapest in years. Oct 20 is a ±13% event with IV rank 74. |
| APP | Growth decel from 30%+, BofA/Wells downgrades, Unity litigation loss, class actions, earlier short reports, 9-day slide. | **Structural questions unresolved** (ad-tech durability, Unity dispute). Cheap on paper (~17x) but estimates still falling. Falling knife until Nov 4. |
| FICO | FHFA removed prior-approval for VantageScore 4.0 (Sep 9), then announced a **single LLPA grid putting VantageScore on parity with Classic FICO** (~Sep 29-30): -27% in a day, -40% in 30 days. VantageScore 5.5% of GSE originations in Sept (KBW). Zacks Strong Sell. | **Structural.** The mortgage-score pricing monopoly, which drove Scores +41%, is being dismantled. ~16x FY26 looks cheap only because FY27+ estimates have not been cut. Avoid until FY27 guidance resets (Nov 4). |

Benchmarks: **MSFT** - sentiment strongly bullish into Oct 28 (Wells $725, Evercore $635, new segment disclosure). **PLTR** - euphoric (Goldman upgrade, new high, 85-90x). **TSLA** - delivery beat, 23% below high, 1.4% op margin, >100x; sentiment mixed/Hold.

---

## 7. Seasonality (Oct / Nov / Dec / Jan) - weak priors, small samples

| Ticker | Oct | Nov | Dec | Jan | Source / sample |
|---|---|---|---|---|---|
| MSFT | +3.8% (5y) / +7.2% Oct 3-Nov 8 window (15y, Seasonax) | +4.4% (5y) | -1.5% (5y) | +4.3% (38y, 66% win) | tickerleague 2021-25; Seasonax; TrendSpider |
| PLTR | +6.1% (83% win) | +35.6% (outlier-driven: +168% '20, +61% '24; median +10%) | +5.9% (median +12.5%) | +5.2% (sign issues in table) | tickerleague 2020-26 (6y) |
| TSLA | historically weak (36% win thru 2021); +2.7% '25 | -5.8% '25 | +4.5% '25 | n/a | TrendSpider 2021; chartrow |
| WM | -9.5% '25 (single yr) | +9.1% '25 | -11.3% '24 | +9.2% '25 | Equity Clock: **Nov 8-Mar 19 window +2.54%/yr vs SPX, 16/20 yrs** |
| WMT | n/a | +9.2% '25, +12.9% '24 | n/a | n/a | Equity Clock: **Aug 22-Nov 14 window +2.62% vs SPX (20y)** |
| PEP | +3.3% (5y avg) | +1.0% | -0.1% | **-3.0% (5 straight negative Jans)** | tickerleague 2021-25 |
| AXP | **+4.7%** | **+7.6%** | +4.2% | **+7.7%** | my means from tickerleague 2010-25 (16y; outliers inflate) |
| MCD | +2.8% | +2.9% (82% win) | +2.3% | -0.4% | tickerleague 2020-26; Seasonax: late-Oct to mid-Dec strong (20y) |
| MGM | sign conflict ('25: ±7.6%) | n/a | n/a | sign conflict | Equity Clock: **Oct 28-Jan 16 window +9.92%/yr vs SPX (20y)** |
| LVMUY | n/a | n/a | n/a | n/a | Equity Clock: Dec 25-Mar 31 window +2.57% vs SPX (17y); consumer-disc. strength Oct 17-Apr 12 |
| NFLX | +7.5% (my mean, 2012-25) | +3.0% | ~0% | **+14.7% (20y, 71% win)** | tickerleague; Benzinga/Finviz |
| APP | +2.2% to +6.5% | +9.0% to +14.7% (Nov '24 +99% outlier) | +1.7% to +2.3% | -7.6% / +4.7% (**conflict**) | Frenzy Capital / tickerleague (5-6y) |
| FICO | +2.5% | +9.7% | +1.1% | +3.5% | my means from tickerleague 2012-25 |

Takeaway: Nov-Jan is seasonally the best stretch for AXP, MGM (window), WM (window), NFLX (Jan), and MCD (late-Oct to mid-Dec). PEP's January is historically poor. PLTR's November looks huge but is two outlier years.

---

## 8. Comparison: the 10 vs. MSFT / PLTR / TSLA

| | Valuation (fwd P/E) | Growth | Quality (margin, FCF) | Momentum (RSI / vs 200d) | Volatility (IV) | Yield | Next catalyst |
|---|---|---|---|---|---|---|---|
| MSFT | ~27-30x | +18% rev, Azure +43% | Excellent | Neutral (44-63), above 200d | 32% | 0.7% | Oct 28 |
| PLTR | ~85-90x | +93% rev | Excellent margins, extreme multiple | Overbought (~70+), new high | 55% | 0 | ~Nov 2 |
| TSLA | >100x | deliveries -2% y/y | Weak (1.4% op margin) | Neutral-bullish (59), below 200d | ~42% | 0 | Oct 21 |
| AXP | ~17x | +10% rev | High (ROE franchise) | Oversold-ish (25-45), below 200d | 30% | 1.2% | Oct 23 |
| WMT | ~38x | +6% rev | High | Recovering (53), above 20/50d | 23% | 0.85% | ~Nov 19 |
| PEP | ~15x | +3% organic | Good | Oversold (~25), post-earnings | ~22% | 4.7% | done |
| MCD | ~16.5x | +1.3% comps | Very high margins | Oversold (17-40) | ~25% | 3.2% | ~Nov 4 |
| WM | ~22x | +4% rev | High, FCF +34% | Weak (42), below 200d | 21% | 1.6% | Oct 27 |
| NFLX | ~19-20x | +12-13% rev | High (33% op margin, $12.5B FCF) | Downtrend (33) | 45% (IV rank 74) | 0 | Oct 20 |
| MGM | ~15x | +1% rev | Medium, levered | Extreme oversold (12) | ~55% | 0 | Oct 28 |
| LVMUY | ~16x | +2-3% organic | High | Oversold (31) | n/a (~32% HV) | ~3.4% | Oct 12 |
| APP | ~17x | +53% rev (decelerating) | Extraordinary margins, legal risk | Extreme oversold (16-29) | 66% | 0 | Nov 4 |
| FICO | ~16x (FY26 only) | +26% rev (Scores +41%, at risk) | Very high, structurally threatened | Oversold, broke support again | ~60% (assumed) | 0 | ~Nov 4 |

Relative view: the three source names have the best growth and the richest multiples; PLTR in particular is pricing near-perfection (90x) with momentum stretched. The best risk/reward in the oversold list is in names where (a) the thesis is cyclical, (b) the earnings catalyst is imminent and expectations are already cut, and (c) seasonality helps: **AXP, WMT, PEP, then MCD/WM/NFLX**.

---

## 9. Tiered ranking for rotation

**Tier 1 - Buy on triggers (core rotation destinations)**
1. **AXP** - 10% growth at 17x, buybacks, oversold, Oct 23 catalyst, strongest Nov-Jan seasonality of the group. Risk: credit/spend deceleration; AML consent-order costs.
2. **WMT** - momentum has already turned (above 20/50d), options flow very bullish (P/C 0.3-0.4), seasonal window (to Nov 14) and Nov 19 print. Risk: multiple (~38x) leaves no room for another guide-down.
3. **PEP** - catalyst behind it, 15x, 4.7% yield, consensus already cut. Risk: snack-volume secular decline; weak January seasonality; rates.

**Tier 2 - Accumulate after the catalyst**
4. **MCD** - cheapest in years (16.5x, 3.2% yield) but management told you conditions are not improving; wait for the Nov 4 comps print or a reclaim of $246.
5. **WM** - quality defensive, small drawdown, not cheap; buy post Oct 27 if FCF guide holds; seasonal window from Nov 8.
6. **NFLX** - de-rated to ~19-20x with 33% margins; Oct 20 is a ±13% coin flip with IV rank 74. Preferred: sell cash-secured puts into earnings or buy after the print. January seasonality is the best on the list.

**Tier 3 - Small, event-driven only**
7. **MGM** - RSI 11, bid-collapse selling exhausted, 20-yr Oct 28-Jan 16 seasonal window, Oct 28 print, possible corporate action with People Inc. Levered casino into 5.2% yields: cap at 1-2% of portfolio.
8. **LVMUY** - trough cycle, 3.4% yield, but Oct 12 is binary and ADR options are illiquid. Buy only if Q3 organic growth >= Q2's +3% and the stock does not make a new low.

**Tier 4 - Avoid for now (falling knives)**
9. **APP** - estimates still falling, litigation, no floor yet; 66% IV. Revisit only after Nov 4 and a reclaim of the 20-day (~$315).
10. **FICO** - structural regulatory dismantling of its mortgage-score pricing power; broke support again Friday on a Strong Sell; FY27 numbers not reset. Do not buy before Nov 4 guidance; even then wait for a base.

---

## 10. Dated rotation plan (best-guess dates and levels; not financial advice)

### 10a. Source positions: how/when to trim MSFT and PLTR

**PLTR (trim first; most extended)**
- **Now / Mon Oct 12 - Fri Oct 16:** Sell 20-25% of the position into the post-upgrade spike (stock +14% in a week, new high, RSI ~70+, 85-90x). Use limit orders $205-215. Rationale: the Goldman upgrade is a sell-side catalyst already in the price; implied 30-day 1σ is ±16%.
- **Alternative to selling (tax-aware):** sell Nov 20 covered calls ~$240-250 (roughly 25-delta) on the shares you would otherwise trim; or collar: buy Nov 20 ~$185 put / sell ~$245 call (near zero-cost given 55% IV). This caps upside through the ~Nov 2 print but protects a ±16% move.
- **Fri Oct 30 (pre-earnings check):** if PLTR > $215 and RSI > 70, sell a second 15-20% tranche. If it has pulled back to the 20-day (~$183-190) and held, do nothing and reassess post-earnings.
- **Nov 3-6 (post-earnings):** finish trims into strength if guidance raise is "only" in line (the Aug reaction was +29.5%, so expectations are high). Invalidation of the trim thesis: a > +15% post-earnings gap with FY27 guide implying > 60% growth - then keep a larger core.

**MSFT (hold core through earnings; monetize vol)**
- **Oct 12-16:** sell Nov 20 covered calls on 25-50% of the position at ~$575-580 (just above the 52w high; ~25-delta at 32% IV). Premium offsets a ±8% event. Do NOT sell shares pre-earnings unless price > $553 with RSI > 70 (then trim 10%).
- **Oct 28 AMC earnings (confirmed):** implied move ~7.9%. Street has Azure +45% cc guided; new segment disclosure (Agents & Infra / Devices & Consumer).
- **Oct 29 - Nov 6:** trim 15-25% into post-earnings strength (target zone $560-585 if it gaps up), or hold and let calls get assigned. If it gaps down and holds the 50-day (~$522), trim nothing; if it closes below the 200-day (~$506) on volume, reduce 20% regardless (trend break).
- Target end-state (illustrative): MSFT reduced ~20-25%, PLTR reduced ~35-45%, funding the Tier 1-2 buys below over Oct 13 - Dec 15.

**Tax note (generic, not advice):** check holding periods per lot (long-term vs short-term), use specific-lot identification, and be aware of wash-sale rules (30 days) if you re-buy either name or substantially identical positions; covered calls that are deep ITM can affect holding period. Consult a tax professional.

### 10b. Destination buys: tranches, triggers, stops

| Ticker | Tranche 1 (when / level / trigger) | Tranche 2 (when / level / trigger) | Tranche 3 | Stop / invalidation |
|---|---|---|---|---|
| **AXP** | Oct 19-22 (pre-earnings), $300-310, 1/3 size. Trigger: holds > $300 and RSI >= 35. | Oct 23-27 post-earnings, 1/3, if print shows billed-business growth >= ~7% and stock holds > $300 (even on a dip). | Nov 10-20 on reclaim of 50-day (~$317), final 1/3. | Close < $288 (below Mar 20 low $290.97). |
| **WMT** | Oct 13-16, $108-112, 1/3. Trigger: already above 20/50-day; stay in if > $105. | Nov 3-13, 1/3 on hold of $108 or break > $115. | Nov 20-24 post-earnings (Nov 19 est.), 1/3, if Q3 op income within guide and stock > $110. | Close < $103 (below Oct 6 low and 20-day). |
| **PEP** | Oct 13-17, $123.5-128, 1/2. Trigger: RSI reclaim > 30 (likely already) and no new low below $123.47 for 3 sessions. | Nov 3-14, 1/2 on reclaim of $129.2 (first resistance) or on any retest of $124-125 that holds. | - | Close < $118. Also exit if January seasonality + rates push it through $120 on volume. |
| **MCD** | Nov 2-3 (pre-earnings), $230-238, 1/3, small. Trigger: holds above $229.20 low; RSI > 30. | Nov 4-6 post-earnings, 1/3, only if US comps >= +1.5% and stock closes > $240. | Dec 1-15 on reclaim of $250 (200-day), final 1/3. | Close < $222. |
| **WM** | Oct 28-30 post-earnings (Oct 27 AMC), $200-212, 1/2. Trigger: FCF guide $3.75-3.85B maintained. | Nov 10-21 on reclaim of $218 (50-day), 1/2. Seasonal window opens Nov 8. | - | Close < $190 (below 52w low $194.11). |
| **NFLX** | Prefer: Oct 19-20 sell Nov 20 cash-secured puts ~$62-63 (below Jul low) to harvest IV rank 74. Or Oct 21-23 post-earnings, 1/2, if close > $75.5 (50-day) or a gap-down holds > $65.08 for 3 days. | Nov 10-Dec 15, 1/2, on reclaim of $84 (200-day) or late-Dec ahead of January seasonality. | - | Close < $62. |
| **MGM** | Oct 29-30 post-earnings (Oct 28 AMC), $28-32, 1/2 of a small (1-2%) position. Trigger: holds > $29.19 low, RSI > 30. Seasonal window starts Oct 28. | Nov 10-20 on reclaim of $34, 1/2. | - | Close < $26.5. |
| **LVMUY** | Oct 13 (US session after Oct 12 Q3 sales), $83-90, 1/2 of a small position. Trigger: Q3 organic >= +3% and no close below $84.62. | Nov-Dec on reclaim of ~$95 (50-day region), 1/2. | - | Close < $78. Skip entirely if Q3 organic growth is negative. |
| **APP** | No buy before Nov 4. After earnings: only if close > $315 (20-day) within 5 sessions and guide is reaffirmed. Starter 1/3. | On reclaim of $333 (50-day). | - | Close < $240 (invalidation of "floor at $267"). |
| **FICO** | No buy before Nov 4. After earnings: require FY27 guide, a 10+ session base, and reclaim of $706. | - | - | Close < $560. Reassess the structural thesis only on FHFA clarity (effective date/pricing grid). |

### 10c. Calendar

| Date | Event / action |
|---|---|
| Mon Oct 12 | LVMH Q3 sales (after Paris close). PLTR trim tranche 1 window opens. MSFT covered-call entry. |
| Tue Oct 13 | LVMUY decision (post-print). WMT tranche 1; PEP tranche 1 window (Oct 13-17). |
| Mon Oct 19-Tue Oct 20 | NFLX cash-secured puts (optional); NFLX earnings Oct 20 AMC. |
| Wed Oct 21 | TSLA earnings AMC (benchmark only). AXP tranche 1 window (Oct 19-22). |
| Fri Oct 23 | AXP earnings BMO; AXP tranche 2 decision. |
| Tue Oct 27 | WM earnings AMC. |
| Wed Oct 28 | **MSFT earnings AMC; MGM earnings AMC.** |
| Thu Oct 29-Fri Oct 30 | WM tranche 1; MGM tranche 1; MSFT post-earnings trim window; PLTR pre-earnings check (Oct 30). |
| ~Mon Nov 2 | PLTR earnings AMC (unconfirmed). MCD tranche 1 (Nov 2-3, small). |
| ~Wed Nov 4 | MCD (BMO, unconfirmed), APP (AMC, confirmed), FICO (AMC, est.) earnings. |
| Nov 3-6 | PLTR post-earnings trims; MCD tranche 2. |
| Nov 10-21 | Second tranches (AXP, WMT, WM, MGM, NFLX). |
| ~Thu Nov 19 | WMT earnings (est.); WMT tranche 3 Nov 20-24. |
| Dec 1-15 | Final tranches (MCD, NFLX); review stops; year-end tax-lot housekeeping. |

---

## 11. Risks and what would invalidate the plan

1. **Rates.** The 10-year is at ~5.24% after touching 5.37% (24-year high). Every Tier 1-2 name is a rate-sensitive consumer/dividend/financial stock. A further leg to 5.5%+ would keep compressing their multiples regardless of earnings. Invalidation: 10-year > 5.5% with the dollar rising - halt new buys, keep MSFT.
2. **AI trade does not roll over.** The premise of trimming MSFT/PLTR is mean reversion of extended multiples. If MSFT prints Azure > 45% and PLTR raises FY26 to > $8.5B, the source names may keep outperforming the rotation targets for another quarter. Mitigation: trims are partial and staged; covered calls rather than outright sales keep upside participation.
3. **Earnings-specific binaries:** NFLX (±13%), AXP (credit/spend), WM (volume), MGM (Vegas/Macau), LVMH (Oct 12). Each tranche is sized so a stop-out costs < 0.5% of portfolio.
4. **Structural names re-rating lower:** FICO and APP are excluded for this reason; MCD and PEP carry partial structural risk (traffic, GLP-1). If MCD US comps go negative or PEP cuts again, stops will trigger.
5. **Consumer recession.** WMT's six-year-low comps, MCD's flat traffic, PEP volume declines and MGM softness could all be early signs of a broader slowdown rather than idiosyncratic issues. A rising unemployment rate / falling Conference Board confidence would argue for holding more MSFT and skipping MGM/LVMUY entirely.
6. **Data risk.** Many technical and options inputs here are 2-10 days old and vendor-inconsistent; verify RSI, IV, put/call and exact support levels on a live platform before executing any order. The MGM Oct 9 close and FICO 52-week low were not confirmed. Earnings dates for PLTR, MCD, FICO and WMT are estimates.
7. **Tax drag.** Realized gains on MSFT/PLTR could be large; the after-tax hurdle for the rotation is higher than the pre-tax comparison suggests. Prefer collars/covered calls on lots with the largest embedded gains.

---

## 12. Sources (retrieved via web search 2026-10-10)

Prices / 52-week / market cap: Yahoo Finance quote pages (MSFT, WM, WMT, AXP, TSLA, PLTR, MGM), Google Finance (PLTR, TSLA, NFLX, WMT), Morningstar (PEP, LVMUY, APP, MGM), CNBC (WMT, PEP, MCD, AXP), Macrotrends (MCD, MGM, NFLX, AXP), CNN Markets (FICO, APP, MCD), MarketBeat (MSFT, FICO, PEP, MCD), StockAnalysis (FICO), Investing.com (MGM, FICO, LVMH news), heygotrade (TSLA, WMT, MGM, NFLX, WM), Upstox (MSFT), ad-hoc-news.de (LVMH Paris line, WM, WMT), Robinhood, Pluang (PLTR, WM).
- https://finance.yahoo.com/quote/MSFT/ ; https://www.marketbeat.com/stocks/NASDAQ/MSFT/ ; https://upstox.com/us-stocks/msft-share-price/
- https://www.google.com/finance/beta/quote/PLTR:NASDAQ ; https://www.investing.com/equities/palantir-technologies-inc ; https://www.gurufocus.com/news/9117902/
- https://finance.yahoo.com/quote/TSLA/ ; https://www.google.com/finance/quote/TSLA:NASDAQ ; https://www.heygotrade.com/en/us-stock/tsla/
- https://finance.yahoo.com/quote/WM/ ; https://www.morningstar.com/stocks/xnys/wm/quote ; https://stockinvest.us/stock/WM
- https://finance.yahoo.com/quote/WMT/ ; https://www.cnbc.com/quotes/WMT ; https://www.marketbeat.com/stocks/NASDAQ/WMT/
- https://www.morningstar.com/stocks/xnas/pep/quote ; https://www.cnbc.com/quotes/PEP ; https://www.marketbeat.com/instant-alerts/price-pepsico-nasdaq-pep-sets-new-52-week-low-on-analyst-downgrade-2026-10-07/
- https://finance.yahoo.com/quote/AXP/ ; https://www.cnbc.com/quotes/AXP ; https://www.cnn.com/markets/stocks/AXP ; https://simplywall.st/stocks/us/diversified-financials/nyse-axp/american-express
- https://www.cnbc.com/quotes/MCD ; https://www.macrotrends.net/stocks/charts/MCD/mcdonalds/stock-price-history ; https://www.marketbeat.com/instant-alerts/price-mcdonalds-nyse-mcd-sets-new-1-year-low-time-to-sell-2026-10-05/
- https://www.macrotrends.net/stocks/charts/MGM/mgm-resorts/stock-price-history ; https://www.investing.com/equities/mgm-mirage ; https://finance.yahoo.com/quote/MGM/ ; https://www.heygotrade.com/en/us-stock/mgm/
- https://www.morningstar.com/stocks/otcm/lvmuy/quote ; https://www.benzinga.com/quote/LVMUY ; https://www.ad-hoc-news.de/boerse/news/corporate-news/lvmh-mo-t-hennessy-louis-vuitton-stock-heads-into-october-12-results/70255215
- https://www.heygotrade.com/en/us-stock/nflx/ ; https://www.macrotrends.net/stocks/charts/NFLX/netflix/stock-price-history ; https://www.google.com/finance/labs/quote/NFLX:NASDAQ
- https://www.morningstar.com/stocks/xnas/app/quote ; https://www.cnn.com/markets/stocks/APP ; https://www.trefis.com/stock/app/articles/617511/applovin-stock-slides-19-over-9-straight-down-days/2026-10-05
- https://stockanalysis.com/stocks/fico/ ; https://www.marketbeat.com/instant-alerts/price-fair-isaac-nyse-fico-stock-price-down-59-should-you-sell-2026-10-09/ ; https://finviz.com/stock?t=FICO

Earnings dates: Microsoft IR press release (Oct 7, via finviz/days.to) ; Tesla 8-K https://www.sec.gov/Archives/edgar/data/0001318605/000162828026064366/exhibit991111111.htm ; WM BusinessWire https://secure.businesswire.com/news/home/20260924859097/en/ ; AppLovin IR https://investors.applovin.com/news/news-details/2026/AppLovin-to-Announce-Third-Quarter-2026-Results/default.aspx ; MGM https://www.ad-hoc-news.de/boerse/news/corporate-news/mgm-resorts-stock-sets-october-28-earnings-date/70223798 ; NFLX https://www.ad-hoc-news.de/boerse/news/corporate-news/netflix-stock-enters-a-key-earnings-phase-as-growth-slows/70256652 ; LVMH https://www.ad-hoc-news.de/boerse/news/nachboerse/lvmh-stock-company-schedules-third-quarter-sales-release-for-october-12/70244303 ; AXP https://www.investing.com/equities/american-express-historical-data ; PLTR est. https://www.benzinga.com/quote/PLTR/earnings ; MCD est. https://beta.earningswhispers.com/go/w/MCD , https://www.trefis.com/stock/mcd/articles/618171/ ; WMT est. https://beta.earningswhispers.com/go/w/WMT ; FICO est. https://www.marketbeat.com/stocks/NYSE/FICO/earnings/

Technicals: https://www.investing.com/equities/microsoft-corp-technical ; https://us.trendlyne.com/us/equity/technical-analysis/MSFT/1554053/microsoft-corporation/ ; https://journalarta.com/en/2026/10/08/pltr-stock-analysis-gains-1-07-testing-key-resistance/ ; https://financhill.com/stock-price-chart/tsla-technical-analysis ; https://www.heygotrade.com/en/us-stock/wm/ ; https://journalarta.com/en/2026/10/08/momentum-gains-wmt-stock-gains-0-90-on-wednesday/ ; https://www.tradingkey.com/analysis/stocks/us-stocks/262197698-pepsico-pep-stock-forecast-october-4-2026 ; https://stockinvest.us/stock/PEP ; https://www.investing.com/equities/american-express-technical ; https://www.investing.com/equities/mcdonalds-technical ; https://www.chartmill.com/stock/quote/MCD/technical-analysis ; https://financhill.com/stock-price-chart/mgm-technical-analysis ; https://wallstreetbuys.com/stocks/lvmuy.us ; https://swingtradebot.com/equities/NFLX ; https://in.investing.com/equities/applovin-technical ; https://tradersunion.com/news/stocks/show/3636557-applovin-slides-3-75percent-today-on/ ; https://www.stockrsi.com/fico/ ; https://tradersunion.com/news/stocks/show/3748100-fico-slides-4-53percent-today-on/ ; https://tickeron.com/ticker/FICO/

Options / IV: https://apexvol.com/options/msft ; https://www.optionslam.com/earnings/stocks/MSFT ; https://www.alphaquery.com/stock/PLTR/volatility-option-statistics/30-day/iv-mean ; https://opti-view.com/underlying/TSLA/implied-volatility ; https://optionsamurai.com/ticker/wm/implied-volatility ; https://www.alphaquery.com/stock/WMT/volatility-option-statistics/30-day/put-call-ratio-oi ; https://www.optionsanalysissuite.com/stocks/wmt ; https://optionsamurai.com/ticker/pep/option-chain ; https://www.alphaquery.com/stock/AXP/volatility-option-statistics/30-day/put-call-ratio-oi ; https://www.investing.com/news/stock-market-news/mcdonalds-options-activity-call-surge-on-a-52week-low-day-93CH-4913533 ; https://www.barchart.com/stocks/quotes/MGM/put-call-ratios ; https://www.optionsanalysissuite.com/stocks/nflx ; https://www.alphaquery.com/stock/NFLX/volatility-option-statistics/30-day/iv-mean ; https://www.investing.com/news/stock-market-news/applovin-options-flow-puts-edge-out-calls-as-shares-slip-273-93CH-4928116 ; https://www.barchart.com/etfs-funds/quotes/FICO ; https://www.tipranks.com/news/catalyst/fico-stock-slammed-as-mortgage-monopoly-crumbles

Fundamentals / news: https://www.cnbc.com/2026/07/29/microsoft-msft-q4-earnings-report-2026.html ; https://www.sec.gov/Archives/edgar/data/0001321655/000132165526000039/a2026q2ex991pressrelease.htm ; https://electrek.co/2026/10/02/tesla-q3-2026-deliveries-486532/ ; https://www.sec.gov/Archives/edgar/data/0000823768/000110465926087575/tm2621414d1_ex99-1.htm ; https://corporate.walmart.com/news/2026/08/20/walmart-releases-q2-fy27-earnings ; https://www.cnbc.com/2026/08/20/walmart-wmt-q2-2027-earnings.html ; https://www.axios.com/2026/08/20/walmart-earnings-sales-revenue ; https://www.cnbc.com/2026/10/08/pepsico-pep-q3-2026-earnings.html ; https://www.sec.gov/Archives/edgar/data/0000077476/000007747626000050/q320268-kxexhibit991.htm ; https://www.sec.gov/Archives/edgar/data/0000004962/000000496226000318/q226exhibit991.htm ; https://www.sec.gov/Archives/edgar/data/0000004962/000000496226000376/axp-20261008.htm ; https://www.bankingdive.com/news/amex-dinged-by-fed-occ-must-pay-350m-for-aml-failures/832570/ ; https://www.investing.com/news/transcripts/earnings-call-transcript-mcdonalds-q2-2026-beats-eps-misses-sales-93CH-4834709 ; https://247wallst.com/investing/2026/09/24/mcdonalds-breaks-to-a-new-52-week-low-after-the-ceo-says-things-are-not-getting-better/ ; https://www.prnewswire.com/news-releases/mgm-resorts-international-reports-second-quarter-2026-financial-and-operating-results-302838122.html ; https://www.cnbc.com/2026/09/24/barry-diller-people-mgm-resorts.html ; https://stocktwits.com/news-articles/markets/equity/mgm-stock-tumbles-after-barry-diller-s-people-scraps-takeover-bid-mizuho-says-withdrawal-was-not-terribly-surprising/cZMJIPBRB9V ; https://www.investing.com/news/transcripts/earnings-call-transcript-lvmh-posts-solid-h1-2026-growth-as-margins-hold-firm-93CH-4814843 ; https://www.sec.gov/Archives/edgar/data/0001065280/000106528026000211/ex991_q226.htm ; https://variety.com/2026/tv/news/netflix-q2-2026-earnings-1236812558/ ; https://investors.applovin.com/news/news-details/2026/AppLovin-Announces-Second-Quarter-2026-Financial-Results/default.aspx ; https://ca.finance.yahoo.com/news/applovin-shares-drop-bank-america-173500523.html ; https://www.benzinga.com/markets/tech/26/10/62130241/applovin-stock-sinks-to-52-week-low-heres-why ; https://www.sec.gov/Archives/edgar/data/0000814547/000081454726000031/exhibit991erq32026.htm ; https://www.housingwire.com/articles/fhfa-unified-llpa-grid-fico-vantagescore/ ; https://www.tikr.com/blog/fico-sinks-27-as-trump-admin-announces-plans-to-end-its-mortgage-scoring-monopoly ; https://www.investing.com/news/stock-market-news/why-is-fair-isaac-stock-sliding-today-93CH-4921272 ; https://247wallst.com/investing/2026/10/09/goldman-sachs-upgrades-palantir-to-buy-sees-18-upside-and-further-outperformance-into-2027/ ; https://finance.yahoo.com/markets/stocks/articles/microsoft-stock-gets-flashy-price-170430954.html

Macro (Oct 9): https://finance.yahoo.com/markets/stocks/articles/markets-news-oct-9-2026-105547352.html ; https://fred.stlouisfed.org/series/sp500 ; https://investrade.com/market-review-october-09-2026/ ; https://finance.yahoo.com/quote/%5EVIX/

Seasonality: https://www.seasonax.com/?p=20746 ; https://tickerleague.com/companies/MSFT/seasonality ; https://tickerleague.com/companies/PLTR/seasonality ; https://chartrow.com/quote/tsla/monthly-returns ; https://charts.equityclock.com/waste-management-inc-nysewm-seasonal-chart ; https://charts.equityclock.com/?p=1453 ; https://tickerleague.com/companies/PEP/seasonality ; https://tickerleague.com/companies/AXP/seasonality ; https://tickerleague.com/companies/MCD/seasonality ; https://seasonax.com/?p=17700 ; https://charts.equityclock.com/mgm-resorts-international-nysemgm-seasonal-chart ; https://charts.equityclock.com/?p=6452 ; https://tickerleague.com/companies/NFLX/seasonality ; https://finviz.com/news/270262/netflix-stock-has-a-january-superpower-and-the-numbers-prove-it ; https://www.frenzycap.com/quote/APP ; https://tickerleague.com/companies/APP/seasonality ; https://tickerleague.com/companies/FICO/seasonality

---
*Not financial advice. Prepared for research purposes only. All figures should be re-verified against a live data source before any trade.*
