# Steel Balls: paper-trading bot (simulation)

Virtual **500 USD**, US-listed stocks/ETFs, long only, no leverage/options/shorts, fractional shares allowed, no fees.
**No real money. No brokerage connection. No real orders.** It's benchmarked against a virtual 500 USD in SPY bought at the same moment as the opening trades.

Dashboard: `index.html` (single file, data embedded). Live: https://janvanhal.github.io/steel-balls/

## Files
| File | What |
|---|---|
| `portfolio.json` | cash, positions, SPY baseline, last prices, start dates |
| `trades.csv` | every fill: Bangkok + ET time, ticker, shares, price, total, cash after, reason, source links |
| `history.csv` | one row per US trading day (ET date): portfolio vs SPY baseline |
| `opening-plan.md` | research + target allocation for the opening trades |
| `opening-orders.json` | the opening batch fed to `trade.py open` |
| `scripts/quote.py` | real quote fetcher (Yahoo chart API; Nasdaq.com fallback) |
| `scripts/trade.py` | paper-trade executor (fetches the real price, refuses if none) |
| `scripts/update.py` | refresh prices, write the daily history row, rebuild, push |
| `scripts/build.py` | embeds data into `index.html` from `scripts/dashboard.template.html` |
| `scripts/publish.sh` | git commit + push (no-op without a repo or changes) |

## Commands (run from this folder)
```bash
python3 scripts/quote.py SPY XLE XLF            # live/near-live in session, official close after
python3 scripts/trade.py open opening-orders.json   # Mon 5 Oct after 09:30 ET: opening batch + SPY baseline
python3 scripts/trade.py buy  XLE --usd 50 --reason "thesis, catalyst, risk, exit" --sources URL1 URL2
python3 scripts/trade.py sell XLE --shares 0.5 --reason "..." --sources URL   # or --usd N / --all
python3 scripts/update.py                         # daily after the close (16:00 ET = 03:00 Bangkok)
python3 scripts/build.py                          # rebuild index.html only
```
Flags: `--no-push` skips the git push. `--allow-closed` lets a trade fill at the last close outside the regular session (off by default).

## Price sources (tested Sat 3 Oct 2026 from this box)
- **Yahoo Finance chart API** `query1/query2.finance.yahoo.com/v8/finance/chart/<T>`: works, but **only with the bare `User-Agent: Mozilla/5.0`**. Full browser UAs and curl/python UAs get HTTP 429. `regularMarketPrice` + `regularMarketTime` give the latest regular-session trade during market hours (near-real-time for US listings) and the official close (16:00 ET stamp) afterwards. The script retries on 429/5xx.
- **Nasdaq.com API** `api.nasdaq.com/api/quote/<T>/info?assetclass=etf|stocks`: works as a fallback. The free feed is not real-time (`isRealTime:false`, about 15 min delay possible) and gives only a text timestamp, so the recorded time is the fetch time.
- **Stooq CSV**: does not work from here (the `q/l` endpoint returns "page does not exist", and `q/d/l` serves a JS proof-of-work challenge).

## Guarantees in the scripts
- No price, no trade. A missing quote aborts the whole opening batch, and `update.py` writes no row rather than guessing.
- Trades are refused outside the regular session unless `--allow-closed` is passed.
- Cash can't go negative (no leverage), and you can't sell more than you hold (no shorts).
- Files are written atomically (temp file + rename) under a file lock.
