#!/usr/bin/env python3
"""Steel Balls paper-trade executor. PAPER TRADING ONLY: no broker, no real orders.

  trade.py buy  TICKER (--usd N | --shares N) --reason "..." --sources URL [URL ...]
  trade.py sell TICKER (--usd N | --shares N | --all) --reason "..." --sources URL [URL ...]
  trade.py open opening-orders.json      # opening batch + 500 USD SPY baseline, one price snapshot
  common flags: --allow-closed (trade at last close outside the session), --no-push

Every fill uses a real price fetched right now (scripts/quote.py). No price means no trade.
portfolio.json and trades.csv are written atomically under a file lock.
"""
import argparse, json, math, os, sys
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa
from quote import get_quote, QuoteError


def fetch(ticker, allow_closed):
    q = get_quote(ticker)  # raises QuoteError -> no trade
    if not q["market_state"].startswith("REGULAR") and not allow_closed:
        raise QuoteError(f"{ticker}: market not in regular session ({q['market_state']}); "
                         "refusing to trade (use --allow-closed to fill at last close)")
    return q


def fill_shares(price, usd=None, shares=None):
    if shares is None:
        shares = math.floor(usd / price * 1e6) / 1e6
    shares = round(float(shares), 6)
    if shares <= 0:
        raise ValueError("share count must be > 0")
    return shares, round(shares * price, 2)


def apply(p, rows, action, ticker, q, usd=None, shares=None, sell_all=False, reason="", sources=()):
    ticker = ticker.upper()
    if not reason.strip():
        raise ValueError("a reason is required")
    price = float(q["price"])
    pos = next((x for x in p["positions"] if x["ticker"] == ticker), None)
    if action == "sell":
        if not pos:
            raise ValueError(f"no position in {ticker} (long only, no shorts)")
        if sell_all:
            shares = pos["shares"]
    shares, total = fill_shares(price, usd, shares)
    if action == "buy":
        if total > p["cash"] + 1e-9:
            raise ValueError(f"insufficient cash: need {total:.2f}, have {p['cash']:.2f} (no leverage)")
        p["cash"] = round(p["cash"] - total, 2)
        if pos:
            pos["cost_basis"] = round(pos["cost_basis"] + total, 2)
            pos["shares"] = round(pos["shares"] + shares, 6)
            pos["avg_cost"] = round(pos["cost_basis"] / pos["shares"], 4)
        else:
            p["positions"].append({"ticker": ticker, "shares": shares, "avg_cost": price,
                                   "cost_basis": total, "opened_et": q["time_et"]})
    else:
        if shares > pos["shares"] + 1e-9:
            raise ValueError(f"cannot sell {shares} {ticker}; hold {pos['shares']} (no shorts)")
        frac = shares / pos["shares"]
        p["cash"] = round(p["cash"] + total, 2)
        pos["cost_basis"] = round(pos["cost_basis"] * (1 - frac), 2)
        pos["shares"] = round(pos["shares"] - shares, 6)
        if pos["shares"] <= 1e-6:
            p["positions"].remove(pos)
    p["last_prices"][ticker] = {"price": price, "time_et": q["time_et"], "source": q["source"]}
    tid = f"T{len(rows) + 1:04d}"
    rows.append({"trade_id": tid, "datetime_bkk": q["time_bkk"], "datetime_et": q["time_et"],
                 "action": action.upper(), "ticker": ticker, "shares": f"{shares:.6f}",
                 "price": f"{price:.4f}", "total": f"{total:.2f}", "cash_after": f"{p['cash']:.2f}",
                 "reason": reason.strip(),
                 "sources": " ".join(list(sources) + [q["source_url"]])})
    print(f"{tid} {action.upper()} {shares:.6f} {ticker} @ {price:.4f} = {total:.2f} USD | cash {p['cash']:.2f} "
          f"| {q['time_et']} / {q['time_bkk']} | {q['source']}")


def save(p, rows):
    p["last_update_bkk"] = now_bkk()
    atomic_write(TRADES, csv_text(TRADE_FIELDS, rows))
    atomic_write(PORTFOLIO, portfolio_text(p))


def cmd_open(path, allow_closed):
    plan = json.load(open(path))
    orders = plan["orders"]
    with lock():
        p = load_portfolio()
        if p["spy_baseline"] is not None:
            sys.exit("SPY baseline already set: opening batch was already executed.")
        # snapshot ALL prices first; abort everything if any is missing
        tickers = [o["ticker"] for o in orders] + ["SPY"]
        quotes = {}
        for t in tickers:
            quotes[t] = fetch(t, allow_closed)
        spend = sum(o["usd"] for o in orders)
        if spend > p["cash"]:
            sys.exit(f"orders total {spend} > cash {p['cash']}")
        rows = read_csv(TRADES)
        for o in orders:
            apply(p, rows, "buy", o["ticker"], quotes[o["ticker"]], usd=o["usd"],
                  reason=o["reason"], sources=o.get("sources", []))
        spy = quotes["SPY"]
        base_usd = float(plan.get("spy_baseline_usd", p["start_cash"]))
        sh = math.floor(base_usd / spy["price"] * 1e6) / 1e6
        p["spy_baseline"] = {"usd": base_usd, "shares": sh, "price": spy["price"],
                             "datetime_et": spy["time_et"], "datetime_bkk": spy["time_bkk"],
                             "source": spy["source"], "source_url": spy["source_url"]}
        p["last_prices"]["SPY"] = {"price": spy["price"], "time_et": spy["time_et"], "source": spy["source"]}
        p["start_date_et"], p["start_date_bkk"] = spy["time_et"], spy["time_bkk"]
        save(p, rows)
        print(f"SPY baseline: {sh:.6f} SPY @ {spy['price']:.4f} ({base_usd:.2f} USD) at {spy['time_et']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["buy", "sell", "open"])
    ap.add_argument("target", help="ticker, or orders JSON for 'open'")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--usd", type=float)
    g.add_argument("--shares", type=float)
    g.add_argument("--all", action="store_true")
    ap.add_argument("--reason", default="")
    ap.add_argument("--sources", nargs="*", default=[])
    ap.add_argument("--allow-closed", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()
    try:
        if a.action == "open":
            cmd_open(a.target, a.allow_closed)
            msg = "Opening trades + SPY baseline"
        else:
            if a.usd is None and a.shares is None and not a.all:
                sys.exit("give --usd, --shares or --all")
            if a.all and a.action != "sell":
                sys.exit("--all only for sell")
            with lock():
                p = load_portfolio()
                q = fetch(a.target, a.allow_closed)
                rows = read_csv(TRADES)
                apply(p, rows, a.action, a.target, q, usd=a.usd, shares=a.shares, sell_all=a.all,
                      reason=a.reason, sources=a.sources)
                save(p, rows)
            msg = f"{a.action.upper()} {a.target.upper()}"
    except (QuoteError, ValueError) as e:
        sys.exit(f"REFUSED: {e}")
    rebuild_and_publish(push=not a.no_push, msg=msg)


if __name__ == "__main__":
    main()
