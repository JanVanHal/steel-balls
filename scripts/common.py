"""Shared helpers: file paths, locking, atomic writes, timestamps."""
import csv, fcntl, json, os, subprocess, sys, tempfile
from contextlib import contextmanager
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORTFOLIO = os.path.join(ROOT, "portfolio.json")
TRADES = os.path.join(ROOT, "trades.csv")
HISTORY = os.path.join(ROOT, "history.csv")
ET = ZoneInfo("America/New_York")
BKK = ZoneInfo("Asia/Bangkok")
TRADE_FIELDS = ["trade_id", "datetime_bkk", "datetime_et", "action", "ticker", "shares", "price",
                "total", "cash_after", "reason", "sources"]
HIST_FIELDS = ["date_et", "portfolio_value", "cash", "spy_shares", "spy_price", "spy_value",
               "portfolio_pct", "spy_pct", "diff_pct"]


@contextmanager
def lock():
    with open(os.path.join(ROOT, ".lock"), "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def atomic_write(path, text):
    d = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp-")
    with os.fdopen(fd, "w", newline="") as f:
        f.write(text)
    os.replace(tmp, path)


def load_portfolio():
    with open(PORTFOLIO) as f:
        return json.load(f)


def portfolio_text(p):
    return json.dumps(p, indent=2) + "\n"


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def csv_text(fields, rows):
    import io
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in fields})
    return buf.getvalue()


def stamp(dt_utc):
    return (dt_utc.astimezone(BKK).strftime("%Y-%m-%d %H:%M:%S ICT"),
            dt_utc.astimezone(ET).strftime("%Y-%m-%d %H:%M:%S %Z"))


def now_bkk():
    return datetime.now(BKK).strftime("%Y-%m-%d %H:%M:%S ICT")


def rebuild_and_publish(push=True, msg="update"):
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py")], check=True)
    if push:
        subprocess.run(["bash", os.path.join(ROOT, "scripts", "publish.sh"), msg], check=False)
