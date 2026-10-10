# Daily Rotation Brief

A weekday routine that emails exact buy/sell recommendations for rotating out of MSFT/PLTR
into the oversold names in `research/2026-10-10-rotation-oversold-vs-ai-tech.md`.
Four Sonnet subagents gather data in parallel; one Fable subagent makes the decision; the
result is emailed to you. It never places orders. You execute in Robinhood yourself.

| File | Purpose |
|---|---|
| `portfolio.json` | Your holdings, cash and accounts. The routine treats it as the source of truth. |
| `ROUTINE_PROMPT.md` | The exact prompt the routine runs. Paste it into the routine. |
| `../scripts/rotation_screener.py` | Live indicator/options screener (used when Yahoo is reachable). |

## Set it up (once, about 3 minutes)

1. Connect Gmail at https://claude.ai/customize/connectors (skip if it is already connected).
2. In Claude Code on the web (https://claude.ai/code), open **Routines** and create a new routine:
   - **Repository:** `ashes575/awesome-systematic-trading`
   - **Connectors:** Gmail
   - **Schedule:** weekdays, 7:56 AM, America/New_York (the email lands around 8:15-8:30)
   - **Prompt:** the full text of `ROUTINE_PROMPT.md`
3. Use **Run now** once to confirm an email titled `[Rotation Brief] ...` arrives.

## Keeping it accurate

- After you trade, reply to that morning's email with what filled, e.g. `sold 12 PLTR @ 209.50`.
  The next run reads your replies. Every week or so, fold those trades into `portfolio.json`
  and bump its `as_of` date.
- Fill in `cost_basis_per_share` / `held_over_1y` in `portfolio.json` for better tax-aware sells.
- If you get options approval and reach 100 shares of a name, set `options_trading_enabled: true`.

## Optional: live market data

The cloud sandbox blocks most market-data hosts, so by default the agents fall back to web
search (prices can be stale and the briefs say so). To give them live data, add these hosts
under the environment's **Network access -> Allowed domains**
(https://code.claude.com/docs/en/cloud-environments#network-access):
`query1.finance.yahoo.com`, `query2.finance.yahoo.com`, `fc.yahoo.com`, `guce.yahoo.com`.
`rotation_screener.py` then pulls real candles, option chains and greeks.

Not financial advice. Verify every price before you place an order.
