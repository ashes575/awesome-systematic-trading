#!/usr/bin/env python3
"""Screen a rotation out of extended tech holdings into oversold quality names.

For every ticker it pulls daily candles, the option chain and the fundamentals
from Yahoo Finance, then reports trend and oversold indicators, ATM implied
volatility with Black-Scholes greeks, options volume and put/call ratios,
profitability, analyst sentiment and calendar-month seasonality. Holdings get a
trim score (how stretched they are), candidates get an entry score (how washed
out they are and whether the selling has stopped).

    pip install yfinance pandas numpy
    python scripts/rotation_screener.py                       # defaults below
    python scripts/rotation_screener.py --hold MSFT PLTR --buy WMT PEP NFLX
    python scripts/rotation_screener.py --csv out.csv

The scores are mechanical: a high trim score says a holding is extended, not
that it will fall, and a high entry score says a name is oversold and turning,
not that it is cheap. Check the earnings date column before acting on either.
"""
import argparse
import math
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

HOLDINGS = ["MSFT", "PLTR"]
CANDIDATES = ["WM", "WMT", "PEP", "AXP", "MCD", "MGM", "LVMUY", "NFLX", "APP", "FICO"]
BENCHMARKS = ["TSLA", "SPY"]
RISK_FREE = 0.04
TARGET_DTE = (25, 50)  # window for the "30-day" ATM option


# --- indicators -------------------------------------------------------------

def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + gain / loss.replace(0, np.nan))


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    line = close.ewm(span=fast, adjust=False).mean() - close.ewm(span=slow, adjust=False).mean()
    return line, line.ewm(span=signal, adjust=False).mean()


def stochastic(df: pd.DataFrame, n: int = 14) -> pd.Series:
    low, high = df["Low"].rolling(n).min(), df["High"].rolling(n).max()
    return 100 * (df["Close"] - low) / (high - low)


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    prev = df["Close"].shift()
    tr = pd.concat([df["High"] - df["Low"], (df["High"] - prev).abs(), (df["Low"] - prev).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def technicals(df: pd.DataFrame, bench: pd.Series | None = None) -> dict:
    """Snapshot of the latest bar. Needs about a year of daily OHLCV."""
    c = df["Close"]
    r = rsi(c)
    line, sig = macd(c)
    sma = {n: c.rolling(n).mean().iloc[-1] for n in (20, 50, 200)}
    mid, sd = c.rolling(20).mean(), c.rolling(20).std()
    window = c.iloc[-252:]
    last = c.iloc[-1]
    out = {
        "date": df.index[-1].date().isoformat(),
        "close": last,
        "chg_1d_%": 100 * (last / c.iloc[-2] - 1),
        "ret_1m_%": 100 * (last / c.iloc[-22] - 1),
        "ret_3m_%": 100 * (last / c.iloc[-64] - 1),
        "ret_6m_%": 100 * (last / c.iloc[-127] - 1),
        "off_52w_high_%": 100 * (last / window.max() - 1),
        "above_52w_low_%": 100 * (last / window.min() - 1),
        "rsi14": r.iloc[-1],
        "rsi14_5d_min": r.iloc[-5:].min(),
        "stoch14": stochastic(df).iloc[-1],
        "bb_pctb": ((c - (mid - 2 * sd)) / (4 * sd)).iloc[-1],
        "vs_sma20_%": 100 * (last / sma[20] - 1),
        "vs_sma50_%": 100 * (last / sma[50] - 1),
        "vs_sma200_%": 100 * (last / sma[200] - 1),
        "macd_hist": (line - sig).iloc[-1],
        "macd_cross_up": bool(line.iloc[-1] > sig.iloc[-1] and line.iloc[-2] <= sig.iloc[-2]),
        "atr_%": 100 * atr(df).iloc[-1] / last,
        "vol_20d_ann_%": 100 * np.log(c).diff().iloc[-20:].std() * math.sqrt(252),
        "volume_vs_50d": df["Volume"].iloc[-1] / df["Volume"].iloc[-50:].mean(),
        "candle": candle(df.iloc[-1], df.iloc[-2]),
    }
    if bench is not None:
        b = bench.reindex(c.index).ffill()
        out["rel_3m_vs_spy_%"] = 100 * ((last / c.iloc[-64]) / (b.iloc[-1] / b.iloc[-64]) - 1)
    return out


def candle(bar: pd.Series, prev: pd.Series) -> str:
    """Name the last daily candle when it is one of the common reversal shapes."""
    body = bar["Close"] - bar["Open"]
    rng = bar["High"] - bar["Low"]
    if rng <= 0:
        return "flat"
    lower = min(bar["Open"], bar["Close"]) - bar["Low"]
    upper = bar["High"] - max(bar["Open"], bar["Close"])
    prev_body = prev["Close"] - prev["Open"]
    if abs(body) < 0.1 * rng:
        return "doji"
    if lower > 2 * abs(body) and upper < abs(body):
        return "hammer" if body > 0 else "hanging-man/hammer"
    if upper > 2 * abs(body) and lower < abs(body):
        return "shooting-star"
    if body > 0 and prev_body < 0 and bar["Close"] > prev["Open"] and bar["Open"] < prev["Close"]:
        return "bullish-engulfing"
    if body < 0 and prev_body > 0 and bar["Close"] < prev["Open"] and bar["Open"] > prev["Close"]:
        return "bearish-engulfing"
    return "up" if body > 0 else "down"


def seasonality(close: pd.Series, years: int = 15) -> pd.DataFrame:
    """Mean return and hit rate by calendar month over the trailing `years`."""
    monthly = close.resample("ME").last().pct_change().dropna()
    monthly = monthly[monthly.index >= monthly.index[-1] - pd.DateOffset(years=years)]
    grouped = monthly.groupby(monthly.index.month)
    return pd.DataFrame({"mean_%": 100 * grouped.mean(), "hit_%": 100 * grouped.apply(lambda s: (s > 0).mean()),
                         "n": grouped.size()})


# --- options ----------------------------------------------------------------

def _ncdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def bs_greeks(spot: float, strike: float, years: float, iv: float, call: bool, r: float = RISK_FREE) -> dict:
    """Black-Scholes greeks; theta per calendar day, vega per vol point."""
    if years <= 0 or iv <= 0:
        return {"delta": np.nan, "gamma": np.nan, "theta": np.nan, "vega": np.nan}
    sq = iv * math.sqrt(years)
    d1 = (math.log(spot / strike) + (r + iv * iv / 2) * years) / sq
    d2 = d1 - sq
    pdf = math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi)
    disc = math.exp(-r * years)
    decay = -spot * pdf * iv / (2 * math.sqrt(years))
    if call:
        delta, theta = _ncdf(d1), decay - r * strike * disc * _ncdf(d2)
    else:
        delta, theta = _ncdf(d1) - 1, decay + r * strike * disc * _ncdf(-d2)
    return {"delta": delta, "gamma": pdf / (spot * sq), "theta": theta / 365, "vega": spot * pdf * math.sqrt(years) / 100}


def options_snapshot(tk, spot: float, today: datetime) -> dict:
    expiries = list(tk.options or [])
    if not expiries:
        return {}
    dte = {e: (datetime.strptime(e, "%Y-%m-%d").replace(tzinfo=timezone.utc) - today).days for e in expiries}
    in_window = [e for e in expiries if TARGET_DTE[0] <= dte[e] <= TARGET_DTE[1]]
    target = in_window[0] if in_window else min(expiries, key=lambda e: abs(dte[e] - 30))

    call_vol = put_vol = call_oi = put_oi = 0.0
    for e in expiries[:4]:  # near-dated expiries carry most of the flow
        ch = tk.option_chain(e)
        call_vol += ch.calls["volume"].fillna(0).sum()
        put_vol += ch.puts["volume"].fillna(0).sum()
        call_oi += ch.calls["openInterest"].fillna(0).sum()
        put_oi += ch.puts["openInterest"].fillna(0).sum()

    ch = tk.option_chain(target)
    call = ch.calls.iloc[(ch.calls["strike"] - spot).abs().argmin()]
    put = ch.puts.iloc[(ch.puts["strike"] - spot).abs().argmin()]
    iv = np.nanmean([call["impliedVolatility"], put["impliedVolatility"]])
    years = max(dte[target], 1) / 365
    # 25-delta-ish skew: 10% OTM put IV minus 10% OTM call IV
    otm_put = ch.puts.iloc[(ch.puts["strike"] - 0.9 * spot).abs().argmin()]["impliedVolatility"]
    otm_call = ch.calls.iloc[(ch.calls["strike"] - 1.1 * spot).abs().argmin()]["impliedVolatility"]
    cg = bs_greeks(spot, call["strike"], years, call["impliedVolatility"], call=True)
    pg = bs_greeks(spot, put["strike"], years, put["impliedVolatility"], call=False)
    return {
        "opt_expiry": target,
        "opt_dte": dte[target],
        "atm_iv_%": 100 * iv,
        "exp_move_%": 100 * iv * math.sqrt(years),
        "skew_10pct_pts": 100 * (otm_put - otm_call),
        "call_delta": cg["delta"], "call_gamma": cg["gamma"], "call_theta": cg["theta"], "call_vega": cg["vega"],
        "put_delta": pg["delta"], "put_theta": pg["theta"],
        "atm_call_mid": (call["bid"] + call["ask"]) / 2,
        "atm_put_mid": (put["bid"] + put["ask"]) / 2,
        "opt_volume": call_vol + put_vol,
        "pc_volume": put_vol / call_vol if call_vol else np.nan,
        "pc_oi": put_oi / call_oi if call_oi else np.nan,
        "vol_oi_ratio": (call_vol + put_vol) / (call_oi + put_oi) if call_oi + put_oi else np.nan,
    }


# --- fundamentals -----------------------------------------------------------

def fundamentals(tk) -> dict:
    info = tk.info or {}
    out = {
        "mkt_cap_bn": (info.get("marketCap") or np.nan) / 1e9,
        "fwd_pe": info.get("forwardPE"),
        "trail_pe": info.get("trailingPE"),
        "ps": info.get("priceToSalesTrailing12Months"),
        "rev_growth_%": 100 * (info.get("revenueGrowth") or np.nan),
        "op_margin_%": 100 * (info.get("operatingMargins") or np.nan),
        "net_margin_%": 100 * (info.get("profitMargins") or np.nan),
        "fcf_yield_%": 100 * (info.get("freeCashflow") or np.nan) / (info.get("marketCap") or np.nan),
        "div_yield_%": info.get("dividendYield"),
        "beta": info.get("beta"),
        "analyst_rec": info.get("recommendationKey"),
        "target_upside_%": 100 * ((info.get("targetMeanPrice") or np.nan) / (info.get("currentPrice") or np.nan) - 1),
        "short_float_%": 100 * (info.get("shortPercentOfFloat") or np.nan),
    }
    try:
        dates = tk.calendar.get("Earnings Date") or []
        out["next_earnings"] = str(dates[0]) if dates else ""
    except Exception:
        out["next_earnings"] = ""
    return out


# --- scoring ----------------------------------------------------------------

def trim_score(row: pd.Series) -> float:
    """0-100: how stretched a holding is. Above ~60 favours trimming into strength."""
    s = 0.0
    s += np.clip((row["rsi14"] - 50) / 30, 0, 1) * 30          # RSI 80 -> full marks
    s += np.clip(row["vs_sma200_%"] / 40, 0, 1) * 25           # 40% over the 200-day
    s += np.clip(row["vs_sma50_%"] / 15, 0, 1) * 15
    s += np.clip(row["bb_pctb"] - 0.8, 0, 0.4) / 0.4 * 10
    s += 10 if row["macd_hist"] < 0 else 0                     # momentum already rolling over
    s += 10 if row["candle"] in ("shooting-star", "bearish-engulfing", "doji") else 0
    return round(s, 1)


def entry_score(row: pd.Series) -> float:
    """0-100: washed out (first half) and turning (second half)."""
    s = 0.0
    s += np.clip((45 - row["rsi14_5d_min"]) / 20, 0, 1) * 20   # recently oversold
    s += np.clip(-row["off_52w_high_%"] / 50, 0, 1) * 15
    s += np.clip((0.2 - row["bb_pctb"]) / 0.4, 0, 1) * 10 if row["bb_pctb"] < 0.2 else 0
    s += 5 if row["above_52w_low_%"] < 8 else 0
    # turning
    s += 15 if row["rsi14"] > row["rsi14_5d_min"] + 5 else 0
    s += 10 if row["macd_cross_up"] or row["macd_hist"] > 0 else 0
    s += 10 if row["vs_sma20_%"] > 0 else 0
    s += 10 if row["candle"] in ("hammer", "bullish-engulfing", "doji") else 0
    s += 5 if row.get("volume_vs_50d", 0) > 1.5 and row["chg_1d_%"] > 0 else 0
    return round(s, 1)


# --- main -------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hold", nargs="+", default=HOLDINGS)
    ap.add_argument("--buy", nargs="+", default=CANDIDATES)
    ap.add_argument("--bench", nargs="+", default=BENCHMARKS)
    ap.add_argument("--no-options", action="store_true", help="skip option chains (faster)")
    ap.add_argument("--csv", help="write the full table here")
    args = ap.parse_args()

    import yfinance as yf

    today = datetime.now(timezone.utc)
    spy = yf.Ticker("SPY").history(period="2y", auto_adjust=True)["Close"]
    spy.index = spy.index.tz_localize(None)
    rows, seas = [], {}
    for role, tickers in (("hold", args.hold), ("buy", args.buy), ("bench", args.bench)):
        for sym in tickers:
            print(f"fetching {sym}...", file=sys.stderr)
            tk = yf.Ticker(sym)
            daily = tk.history(period="2y", auto_adjust=True)
            if len(daily) < 210:
                print(f"  {sym}: not enough history, skipped", file=sys.stderr)
                continue
            daily.index = daily.index.tz_localize(None)
            row = {"ticker": sym, "role": role, **technicals(daily, spy)}
            if not args.no_options:
                try:
                    row.update(options_snapshot(tk, row["close"], today))
                except Exception as exc:  # thin ADR chains (LVMUY) often fail
                    print(f"  {sym}: options unavailable ({exc})", file=sys.stderr)
            try:
                row.update(fundamentals(tk))
            except Exception as exc:
                print(f"  {sym}: fundamentals unavailable ({exc})", file=sys.stderr)
            monthly = tk.history(period="max", interval="1mo", auto_adjust=True)["Close"]
            monthly.index = monthly.index.tz_localize(None)
            seas[sym] = seasonality(monthly)
            rows.append(row)

    df = pd.DataFrame(rows).set_index("ticker")
    df["trim_score"] = df.apply(trim_score, axis=1)
    df["entry_score"] = df.apply(entry_score, axis=1)
    months = [(today.month + k - 1) % 12 + 1 for k in range(4)]
    for m in months:
        df[f"seas_{m:02d}_%"] = [seas[t]["mean_%"].get(m, np.nan) for t in df.index]

    pd.set_option("display.width", 200, "display.max_columns", 50, "display.float_format", "{:.2f}".format)
    tech = ["close", "rsi14", "stoch14", "bb_pctb", "vs_sma50_%", "vs_sma200_%", "off_52w_high_%",
            "ret_3m_%", "rel_3m_vs_spy_%", "candle"]
    opts = [c for c in ["atm_iv_%", "exp_move_%", "skew_10pct_pts", "call_delta", "call_gamma",
                        "call_theta", "call_vega", "opt_volume", "pc_volume", "pc_oi"] if c in df]
    fund = [c for c in ["fwd_pe", "rev_growth_%", "op_margin_%", "fcf_yield_%", "div_yield_%",
                        "analyst_rec", "target_upside_%", "next_earnings"] if c in df]
    print(f"\n== Technicals (as of {df['date'].max()}) ==\n{df[tech]}")
    if opts:
        print(f"\n== Options (ATM ~30-45 DTE; greeks are Black-Scholes from chain IV) ==\n{df[opts]}")
    print(f"\n== Fundamentals & sentiment ==\n{df[fund]}")
    print(f"\n== Seasonality: mean monthly return %, trailing 15y ==\n{df[[c for c in df if c.startswith('seas_')]]}")

    hold = df[df.role == "hold"].sort_values("trim_score", ascending=False)
    buy = df[df.role == "buy"].sort_values("entry_score", ascending=False)
    print("\n== Trim signals (holdings) ==")
    for t, r in hold.iterrows():
        verdict = "TRIM into strength" if r.trim_score >= 60 else "HOLD / collar" if r.trim_score >= 40 else "HOLD"
        print(f"  {t:6s} trim={r.trim_score:5.1f}  RSI={r.rsi14:5.1f}  vs200d={r['vs_sma200_%']:+6.1f}%  "
              f"earnings={r.get('next_earnings', '')}  -> {verdict}")
    print("\n== Entry signals (candidates) ==")
    for t, r in buy.iterrows():
        verdict = ("BUY tranche" if r.entry_score >= 60 else "WATCH: oversold, not turned" if r.entry_score >= 40
                   else "WAIT")
        print(f"  {t:6s} entry={r.entry_score:5.1f}  RSI={r.rsi14:5.1f} (5d min {r.rsi14_5d_min:5.1f})  "
              f"off-high={r['off_52w_high_%']:+6.1f}%  earnings={r.get('next_earnings', '')}  -> {verdict}")
    print("\nMechanical screen, not advice. Avoid opening full positions inside the week before earnings.")

    if args.csv:
        df.to_csv(args.csv)
        print(f"wrote {args.csv}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
