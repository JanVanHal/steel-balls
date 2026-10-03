#!/usr/bin/env bash
# Commit + push the dashboard/data to GitHub Pages (JanVanHal/steel-balls). Safe no-op if no git repo / no changes.
set -u
cd "$(dirname "$0")/.." || exit 0
[ -d .git ] || { echo "publish: no git repo, skipping push"; exit 0; }
git add index.html portfolio.json trades.csv history.csv opening-plan.md opening-orders.json README.md scripts .gitignore 2>/dev/null
if git diff --cached --quiet; then echo "publish: nothing to commit"; exit 0; fi
git commit -q -m "${1:-update} ($(TZ=Asia/Bangkok date '+%Y-%m-%d %H:%M ICT'))" && git push -q origin main && echo "publish: pushed"
