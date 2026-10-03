#!/usr/bin/env python3
"""Embed portfolio.json, trades.csv and history.csv into index.html (single file; works offline and on GitHub Pages)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, load_portfolio, read_csv, TRADES, HISTORY, atomic_write, now_bkk

data = {"portfolio": load_portfolio(), "trades": read_csv(TRADES), "history": read_csv(HISTORY), "built_bkk": now_bkk()}
blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
tpl = open(os.path.join(ROOT, "scripts", "dashboard.template.html")).read()
atomic_write(os.path.join(ROOT, "index.html"), tpl.replace("/*__DATA__*/", blob))
print("built index.html")
