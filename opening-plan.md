# Steel Balls: opening plan (DRAFT, filled Mon 5 Oct 2026)

> **Paper trading only.** Virtual 500 USD. No brokerage and no real orders.
> **Prices and share counts below are NOT final.** Every position gets filled at the first real
> regular-session price fetched on **Mon 5 Oct 2026, just after 09:30 ET (20:30 Bangkok)**, via
> `scripts/quote.py` (Yahoo chart API, Nasdaq fallback). The 500 USD SPY baseline is bought in the same run.
> Friday 2 Oct closes are listed for sizing reference only.

## Market backdrop (as of Fri 2 Oct 2026 close)
- S&P 500 closed at 7,722.72 (+0.73%), about 1% below its mid-August record and up ~13% YTD. The Nasdaq closed near a record after a weak September jobs report (+29k payrolls, 4.2% unemployment) cut the odds of an October hike to ~22%, down from 64% a week earlier. Sources: [WSJ](https://www.wsj.com/finance/stocks/u-s-stocks-rise-as-jobs-report-tempers-rate-outlook-fde051d1), [Reuters via LSE](https://www.lse.co.uk/news/us-stocks-equities-close-higher-as-softer-jobs-data-quiets-rate-hike-expectations-asxmwpmbeyprqb8.html)
- The Fed hiked to 3.75–4.00% on 16 Sep (its first hike since 2023) and the dots point to one more. The next FOMC is **27–28 Oct**. Sources: [Fed statement](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm), [Fed calendar](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)
- The 10-year Treasury hit 5.34% on Thu 1 Oct, a 24-year high. Midterms are on 3 Nov. Source: [Reuters via Kitco](https://www.kitco.com/news/off-the-wire/2026-10-02/wall-st-week-ahead-spiking-bond-yields-midterms-earnings-test-us)
- Brent is around $100–102 with the US-Iran war in its 8th month: a third US carrier is heading to the region and China has halted fuel exports. SPR loans and better Saudi flows are offsetting that. Sources: [Moneyweb/Bloomberg](https://www.moneyweb.co.za/news/markets/oil-holds-gain-as-us-sends-third-aircraft-carrier-to-middle-east/), [The National](https://www.thenationalnews.com/business/energy/2026/10/02/oil-prices-stable-amid-mixed-supply-signals-from-the-middle-east/)
- Breadth is very narrow. RSP lagged SPY by 4.6 pp in September (Bespoke), and only 12% of S&P 1500 sub-industries trade above both their 50- and 200-day averages (CFRA). Source: [CNBC week ahead](https://www.cnbc.com/2026/10/02/stock-market-next-week-outlook-for-oct-5-9-2026-.html)

## Calendar (ET)
| Date | Event |
|---|---|
| Mon 5 Oct 10:00 | ISM Services PMI (Sep) |
| Wed 7 Oct 14:00 | FOMC minutes (Sep meeting); 10y auction |
| Thu 8 Oct | Jobless claims; PepsiCo earnings; 30y auction |
| Fri 9 Oct | UMich sentiment (prelim); Delta earnings |
| Tue 13 Oct | JPM, C, GS, WFC, JNJ, UNH earnings ([JPM IR](https://www.jpmorganchase.com/ir/news/2026/jpmc-to-host-third-quarter-2026-earnings-call), [MarketBeat](https://www.marketbeat.com/earnings/reports/2026-10-13-jpmorgan-chase-co-stock/)) |
| Wed 14 Oct 08:30 | CPI (Sep); BAC earnings ([Fazen](https://fazen.markets/en/ism-services-fed-minutes-canadian-jobs-week-ahead-calendar)) |
| Tue–Wed 27–28 Oct | FOMC decision |
| Tue 3 Nov | US midterm elections |

## Target allocation (500 USD)
| Ticker | What | Target | ~USD | Fri 2 Oct close (ref only) |
|---|---|---|---|---|
| SMH | VanEck Semiconductor ETF | 20% | 100 | 630.60 |
| XLE | Energy Select Sector SPDR | 20% | 100 | 62.82 |
| XLF | Financial Select Sector SPDR | 20% | 100 | 53.49 |
| RSP | Invesco S&P 500 Equal Weight | 20% | 100 | 209.73 |
| SGOV | iShares 0-3 Month Treasury Bond ETF | 15% | 75 | 100.44 |
| Cash | | 5% | 25 | |

The idea: hold about 60% in tilts that differ from SPY (energy, banks, equal-weight breadth) and keep one AI/semis leg so we don't fall far behind if the narrow rally continues. About 20% sits in T-bills and cash as dry powder ahead of CPI, the FOMC and the midterms.

## Draft reasons (finalised with real fill prices on Monday)
**SMH (20%).** Thesis: AI capex is still what's leading this market, and the Nasdaq closed near a record on 2 Oct even with the 10-year above 5%. Catalyst: Q3 earnings season and continued AI spend. Risk: high yields hurt long-duration tech, and leadership is crowded. Exit: sell if it falls 12% below entry, or trim if the position grows past 30% of the portfolio. Sources: [WSJ](https://www.wsj.com/finance/stocks/u-s-stocks-rise-as-jobs-report-tempers-rate-outlook-fde051d1), [Kitco/Reuters](https://www.kitco.com/news/off-the-wire/2026-10-02/wall-st-week-ahead-spiking-bond-yields-midterms-earnings-test-us)

**XLE (20%).** Thesis: Brent near $100 supports producer cash flows, and the market also tilts toward an energy shock. Catalyst: Gulf escalation (third carrier) and China's fuel-export halt. Risk: de-escalation, SPR releases, demand slowdown. Exit: sell if Brent closes below $90 for 3 sessions or XLE falls 10% below entry. Sources: [Moneyweb](https://www.moneyweb.co.za/news/markets/oil-holds-gain-as-us-sends-third-aircraft-carrier-to-middle-east/), [The National](https://www.thenationalnews.com/business/energy/2026/10/02/oil-prices-stable-amid-mixed-supply-signals-from-the-middle-east/)

**XLF (20%).** Thesis: higher policy rates support bank net interest income, and big banks report first in the season. Catalyst: JPM/C/GS/WFC report on 13 Oct and BAC on 14 Oct. Risk: credit stress from 5%+ long yields and a softening labour market. Exit: review after bank earnings; sell if XLF falls 10% below entry. Sources: [JPM IR](https://www.jpmorganchase.com/ir/news/2026/jpmc-to-host-third-quarter-2026-earnings-call), [MarketBeat](https://www.marketbeat.com/earnings/reports/2026-10-13-jpmorgan-chase-co-stock/)

**RSP (20%).** Thesis: breadth looks washed out (RSP lagged SPY by 4.6 pp in September; 12% of sub-industries are above their 50/200-day averages), which historically has set up catch-up rallies. Catalyst: softer jobs data cut October hike odds to ~22%, and rate-sensitive names and small caps rallied on 2 Oct. Risk: a hike on 28 Oct or yields at new highs. Exit: sell if it falls 8% below entry or if the Fed hikes and the 10-year makes a new high. Sources: [CNBC](https://www.cnbc.com/2026/10/02/stock-market-next-week-outlook-for-oct-5-9-2026-.html), [Reuters via LSE](https://www.lse.co.uk/news/us-stocks-equities-close-higher-as-softer-jobs-data-quiets-rate-hike-expectations-asxmwpmbeyprqb8.html)

**SGOV (15%).** Thesis: 0–3 month T-bills earn roughly the policy rate (fed funds 3.75–4.00%) with minimal price risk. They're dry powder for after CPI (14 Oct), the FOMC (28 Oct) or the midterms (3 Nov). Risk: lags the market if equities rip. Exit: rotate into equities on a pullback or a confirmed thesis. Sources: [Fed statement](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm), [Fed calendar](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)

**Cash (5%).** Buffer, no yield. Not a trade.

## Monday execution checklist
1. After 09:30 ET (20:30 BKK), confirm `python3 scripts/quote.py SPY` shows `REGULAR` and a timestamp from today's session.
2. Review the reasons in `opening-orders.json`, adding anything material from the weekend or premarket. Do not invent facts.
3. `python3 scripts/trade.py open opening-orders.json` fetches all prices plus SPY in one run, fills the orders, sets the SPY baseline, rebuilds the dashboard and pushes it.
