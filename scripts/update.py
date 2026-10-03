#!/usr/bin/env python3
"""Refresh prices, append/replace today's history row (keyed by ET date), rebuild, publish.

  update.py [--no-push]
Run after the US close (16:00 ET = 03:00 Bangkok next day) for the official close.
Before the opening trades there is no SPY baseline, so it only rebuilds.
"""
import argparse, os, sys
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa
from quote import get_quote, QuoteError


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()
    with lock():
        p = load_portfolio()
        base = p.get("spy_baseline")
        if not base:
            print("No SPY baseline yet (pre-launch). Rebuilding dashboard only.")
        else:
            tickers = [x["ticker"] for x in p["positions"]] + ["SPY"]
            quotes = {}
            for t in tickers:
                try:
                    quotes[t] = get_quote(t)
                except QuoteError as e:
                    sys.exit(f"ABORT: {e} (no history row written; never guessing prices)")
            for t, q in quotes.items():
                p["last_prices"][t] = {"price": q["price"], "time_et": q["time_et"], "source": q["source"]}
            value = p["cash"] + sum(x["shares"] * quotes[x["ticker"]]["price"] for x in p["positions"])
            spy_px = quotes["SPY"]["price"]
            spy_val = base["shares"] * spy_px + (base["usd"] - base["shares"] * base["price"])
            value = round(value, 2) + 0.0
            pp = round((value / p["start_cash"] - 1) * 100, 3) + 0.0
            spy_val = round(spy_val, 2) + 0.0
            sp = round((spy_val / base["usd"] - 1) * 100, 3) + 0.0
            date_et = quotes["SPY"]["time_et"][:10]
            row = {"date_et": date_et, "portfolio_value": f"{value:.2f}", "cash": f"{p['cash']:.2f}",
                   "spy_shares": f"{base['shares']:.6f}", "spy_price": f"{spy_px:.4f}",
                   "spy_value": f"{spy_val:.2f}", "portfolio_pct": f"{pp:.3f}",
                   "spy_pct": f"{sp:.3f}", "diff_pct": f"{round(pp - sp, 3) + 0.0:.3f}"}
            rows = [r for r in read_csv(HISTORY) if r["date_et"] != date_et] + [row]
            rows.sort(key=lambda r: r["date_et"])
            atomic_write(HISTORY, csv_text(HIST_FIELDS, rows))
            print(f"{date_et}: portfolio {value:.2f} ({pp:+.2f}%) | SPY baseline {spy_val:.2f} ({sp:+.2f}%) | diff {pp - sp:+.2f} pp")
        p["last_update_bkk"] = now_bkk()
        atomic_write(PORTFOLIO, portfolio_text(p))
    rebuild_and_publish(push=not a.no_push, msg="Daily update")


if __name__ == "__main__":
    main()
