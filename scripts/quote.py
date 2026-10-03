#!/usr/bin/env python3
"""Steel Balls quote fetcher (paper trading only).

Usage:  python3 scripts/quote.py SPY XLE XLF [--json]

Primary source : Yahoo Finance chart API (query1, fallback query2)
                 meta.regularMarketPrice + meta.regularMarketTime
                 During the regular session this is the latest regular-session
                 trade (US equities on Yahoo are normally real-time / a few
                 seconds-to-minutes behind). After 16:00 ET it is the official close.
Fallback source: Nasdaq.com quote API (lastSalePrice; free feed, may be delayed
                 ~15 min and only date-stamped when closed).
Never invents a price: a ticker with no valid quote is reported as an error
and get_quote() raises QuoteError.
"""
import json, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
BKK = ZoneInfo("Asia/Bangkok")
# NOTE: Yahoo returns HTTP 429 to full browser UA strings and to curl/python UAs
# from this box, but 200 to the bare "Mozilla/5.0" UA (tested 2026-10-03).
UA = "Mozilla/5.0"


class QuoteError(Exception):
    pass


def _get(url, timeout=15, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            last = e
            if e.code not in (429, 500, 502, 503, 504):
                raise
            time.sleep(1.5 * (i + 1))
        except Exception as e:
            last = e
            time.sleep(1)
    raise last


def _fmt(ts_utc):
    return {
        "time_utc": ts_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "time_et": ts_utc.astimezone(ET).strftime("%Y-%m-%d %H:%M:%S ET"),
        "time_bkk": ts_utc.astimezone(BKK).strftime("%Y-%m-%d %H:%M:%S ICT"),
    }


def yahoo(ticker):
    last = None
    for host in ("query1", "query2"):
        url = f"https://{host}.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=1d"
        try:
            d = _get(url)
            res = d["chart"]["result"][0]
            m = res["meta"]
            price = m.get("regularMarketPrice")
            ts = m.get("regularMarketTime")
            if not price or not ts or price <= 0:
                raise QuoteError("empty price")
            t = datetime.fromtimestamp(ts, tz=timezone.utc)
            now = int(time.time())
            reg = m.get("currentTradingPeriod", {}).get("regular", {})
            in_session = reg.get("start", 0) <= now < reg.get("end", 0)
            out = {"ticker": ticker.upper(), "price": round(float(price), 4),
                   "currency": m.get("currency"), "exchange": m.get("fullExchangeName"),
                   "source": f"Yahoo Finance chart API ({host})",
                   "source_url": f"https://finance.yahoo.com/quote/{ticker.upper()}",
                   "market_state": "REGULAR (live/near-live)" if in_session else "CLOSED (last regular-session price = official close)",
                   "fetched_bkk": datetime.now(BKK).strftime("%Y-%m-%d %H:%M:%S ICT")}
            out.update(_fmt(t))
            return out
        except Exception as e:  # try next host
            last = e
    raise QuoteError(f"yahoo failed: {last}")


def nasdaq(ticker):
    last = None
    for cls in ("stocks", "etf"):
        try:
            d = _get(f"https://api.nasdaq.com/api/quote/{ticker}/info?assetclass={cls}")
            data = d.get("data") or {}
            p = (data.get("primaryData") or {}).get("lastSalePrice")
            if not p or p == "N/A":
                raise QuoteError("no lastSalePrice")
            price = float(p.replace("$", "").replace(",", ""))
            now = datetime.now(timezone.utc)
            out = {"ticker": ticker.upper(), "price": price, "currency": "USD",
                   "exchange": data.get("exchange"),
                   "source": "Nasdaq.com quote API (may be ~15 min delayed)",
                   "source_url": f"https://www.nasdaq.com/market-activity/{'etf' if cls=='etf' else 'stocks'}/{ticker.lower()}",
                   "market_state": data.get("marketStatus"),
                   "source_timestamp_text": data["primaryData"].get("lastTradeTimestamp"),
                   "fetched_bkk": now.astimezone(BKK).strftime("%Y-%m-%d %H:%M:%S ICT")}
            out.update(_fmt(now))  # Nasdaq only gives a text timestamp -> times below are FETCH times
            out["time_note"] = "fetch time (Nasdaq gives no exact trade time; price may be ~15 min old)"
            return out
        except Exception as e:
            last = e
    raise QuoteError(f"nasdaq failed: {last}")


def get_quote(ticker):
    errs = []
    for fn in (yahoo, nasdaq):
        try:
            return fn(ticker)
        except Exception as e:
            errs.append(str(e))
    raise QuoteError(f"{ticker}: no real price available ({'; '.join(errs)})")


def main(argv):
    as_json = "--json" in argv
    tickers = [a for a in argv if not a.startswith("--")]
    if not tickers:
        print(__doc__); return 2
    results, rc = [], 0
    for t in tickers:
        try:
            results.append(get_quote(t))
        except QuoteError as e:
            results.append({"ticker": t.upper(), "error": str(e)}); rc = 1
    if as_json:
        print(json.dumps(results, indent=2))
    else:
        for q in results:
            if "error" in q:
                print(f"{q['ticker']:6} ERROR {q['error']}")
            else:
                print(f"{q['ticker']:6} {q['price']:>10.2f}  src={q['time_utc']} | {q['time_et']} | {q['time_bkk']}  [{q['market_state']}]  {q['source']}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
