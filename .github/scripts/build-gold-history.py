# -*- coding: utf-8 -*-
"""Builds gold-rate-history-pakistan.html: gold rate history in Pakistan, per tola, 1947 to today.
Data:
  data/gold-monthly.json   world gold price, USD per troy ounce, monthly average (datasets/gold-prices, from 1833).
  data/metals-daily.json   daily XAU and XAG in USD/oz from March 2024 (open currency API reference rates, weekdays,
                           isolated one-day spikes smoothed), extended every weekday by update-rates.py.
  data/usdpkr-annual.json + data/usdpkr-daily.json   dollar rate (see build-usd-history.py).
Tola price = USD per ounce x USD/PKR / 31.1035 x 11.6638. Before March 2024 it is an estimate from the monthly world
price and the yearly average dollar rate; it is not the sarafa (APGJSA) rate, which usually carries a premium.
Layout is taken from the Silver Bullet guide so the page matches the site.
Run: python3 .github/scripts/build-gold-history.py   (called by the rates workflow; safe to run any time)."""
import json, os, re, html, math, datetime as dt, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hx

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SLUG = "gold-rate-history-pakistan.html"
URL = "https://qaziforextips.com/" + SLUG
HERO = "img/guides/hero/gold-rate-history-pakistan-1947-2026"
PKT = dt.timezone(dt.timedelta(hours=5))
OZ, TOLA = 31.1034768, 11.6638038
E = lambda s: html.escape(str(s), quote=True)
MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
UR_MON = ["جنوری", "فروری", "مارچ", "اپریل", "مئی", "جون", "جولائی", "اگست", "ستمبر", "اکتوبر", "نومبر", "دسمبر"]


def load(name):
    return json.load(open(os.path.join(ROOT, "data", name), encoding="utf-8"))


def tola(usd, pkr):
    return usd * pkr / OZ * TOLA


def rs(v, dec=0):
    return f"Rs {v:,.{dec}f}"


def main():
    gm = {r["m"]: r["usd"] for r in load("gold-monthly.json")}
    md = sorted(load("metals-daily.json"), key=lambda h: h["d"])
    ann = {a["y"]: a["pkr"] for a in load("usdpkr-annual.json")}
    upd = {h["d"]: h["pkr"] for h in load("usdpkr-daily.json")}
    bis = {r["m"]: r["pkr"] for r in load("usdpkr-monthly.json")}   # monthly USD/PKR from 1957 (BIS)
    now = dt.datetime.now(PKT)

    # ---- daily rows (gold + silver in PKR) ----
    days, last_pkr = [], None
    for h in md:
        p = upd.get(h["d"])
        if p is None:   # nearest earlier dollar rate
            k = dt.date.fromisoformat(h["d"])
            for _ in range(7):
                k -= dt.timedelta(days=1)
                if k.isoformat() in upd:
                    p = upd[k.isoformat()]
                    break
        if p is None:
            continue
        t24 = tola(h["xau"], p)
        sv = tola(h["xag"], p) if h.get("xag") else None
        days.append({"d": h["d"], "xau": h["xau"], "xag": h.get("xag"), "pkr": p, "t24": t24, "sv": sv})
    last = days[-1]
    ld = dt.date.fromisoformat(last["d"])
    cy = ld.year
    first_d = dt.date.fromisoformat(days[0]["d"])
    dmon = {}
    for x in days:
        dmon.setdefault(x["d"][:7], []).append(x)

    # yearly dollar rate (annual file, current year from daily data)
    def year_pkr(y):
        if y in ann:
            return ann[y]
        v = [p for d, p in upd.items() if d.startswith(str(y))]
        return sum(v) / len(v) if v else None

    # ---- monthly gold series from Aug 1947 ----
    months = []
    y, m = 1947, 8
    while (y, m) <= (ld.year, ld.month):
        k = f"{y}-{m:02d}"
        if k in dmon:
            rows = dmon[k]
            usd = sum(r["xau"] for r in rows) / len(rows)
            t24 = sum(r["t24"] for r in rows) / len(rows)
            pkr = sum(r["pkr"] for r in rows) / len(rows)
            src = "daily"
        elif k in gm and (bis.get(k) or year_pkr(y)):
            usd, pkr = gm[k], bis.get(k) or year_pkr(y)
            t24, src = tola(usd, pkr), "est"
        else:
            usd = None
        if usd:
            months.append({"k": k, "y": y, "m": m, "usd": usd, "pkr": pkr, "t24": t24, "src": src})
        m += 1
        if m == 13:
            y, m = y + 1, 1
    mk = {x["k"]: x for x in months}

    # ---- yearly averages ----
    years = {}
    for x in months:
        years.setdefault(x["y"], []).append(x)
    yrs = sorted(years)
    Y = {y: {"usd": sum(r["usd"] for r in v) / len(v), "pkr": sum(r["pkr"] for r in v) / len(v),
             "t24": sum(r["t24"] for r in v) / len(v), "n": len(v)} for y, v in years.items()}

    # ---- facts ----
    cur = last["t24"]
    t47, t00, t10, t20 = Y[1947]["t24"], Y[2000]["t24"], Y[2010]["t24"], Y[2020]["t24"]
    t24y, t25y = Y[2024]["t24"], Y[2025]["t24"]
    top = max(days, key=lambda r: r["t24"])
    top_usd = max(days, key=lambda r: r["xau"])
    m80 = max((x for x in months if x["y"] in (1979, 1980, 1981)), key=lambda x: x["usd"])
    m01 = min((x for x in months if 1998 <= x["y"] <= 2002), key=lambda x: x["usd"])
    m11 = max((x for x in months if x["y"] in (2011, 2012)), key=lambda x: x["usd"])
    m20 = max((x for x in months if x["y"] == 2020), key=lambda x: x["usd"])
    g_mult = last["xau"] / Y[2000]["usd"]
    d_mult = last["pkr"] / Y[2000]["pkr"]
    lakh00 = 100000 * cur / t00
    fd = lambda d: d.strftime("%-d %B %Y")
    fm = lambda x: f"{MON[x['m'] - 1]} {x['y']}"

    # ---- year-wise table (newest first); each year opens to show its months ----
    rows, prev = [], None
    for y in yrs:
        a = Y[y]
        ch = "–" if prev is None else f"{(a['t24'] / prev - 1) * 100:+.1f}%"
        note = "Aug–Dec" if y == 1947 else (f"Jan–{MON[ld.month - 1][:3]}" if y == cy else "")
        subs = [f'<tr><th scope="row">{MON[x["m"] - 1]} {y}</th><td>{rs(x["t24"])}</td><td>{rs(x["t24"] * 22 / 24)}</td>'
                f'<td>${x["usd"]:,.0f}</td><td>{x["pkr"]:,.2f}</td></tr>' for x in reversed(years[y])]
        rows.append((str(y), [f'<td>{rs(a["t24"])}</td>', f'<td>{rs(a["t24"] * 22 / 24)}</td>', f'<td>${a["usd"]:,.0f}</td>',
                              f'<td>{a["pkr"]:,.2f}</td>', f'<td>{ch}</td>', f'<td>{note}</td>'], subs))
        prev = a["t24"]
    yt = hx.year_table(["Year", "24K tola", "22K tola", "Gold $/oz", "USD/PKR", "Change", "Note"], list(reversed(rows)),
                       ["Month", "24K tola", "22K tola", "Gold $/oz", "USD/PKR"])
    # ---- decades ----
    dec = ""
    for d0 in range(1950, cy + 1, 10):
        a, b = Y.get(d0), Y.get(min(d0 + 9, cy))
        if a and b:
            dec += (f'<tr><th scope="row">{d0}<span class="dec-s">s</span></th><td>{rs(a["t24"])}</td><td>{rs(b["t24"])}</td>'
                    f'<td>{b["t24"] / a["t24"]:.1f}×</td></tr>')
    # ---- daily gold tables, one per month, shown one at a time ----
    dp = []
    for k in sorted(dmon, reverse=True):
        y, m = int(k[:4]), int(k[5:])
        body = "".join(f'<tr><th scope="row">{dt.date.fromisoformat(r["d"]).strftime("%a %-d %b")}</th><td>{rs(r["t24"])}</td>'
                       f'<td>{rs(r["t24"] * 22 / 24)}</td><td>{rs(r["t24"] * 21 / 24)}</td><td>{rs(r["t24"] / TOLA * 10)}</td><td>${r["xau"]:,.0f}</td>'
                       f'<td>{r["pkr"]:,.2f}</td></tr>'
                       for r in reversed(dmon[k]))
        dp.append((k, f"{MON[m - 1]} {y}", f"Gold rate in {MON[m - 1]} {y} (daily)",
                   f'<div class="tbl"><table><thead><tr><th>Date</th><th>24K tola</th><th>22K tola</th><th>21K tola</th><th>24K 10 g</th><th>Gold $/oz</th><th>USD/PKR</th></tr></thead>'
                   f'<tbody>{body}</tbody></table></div>'))
    dd = hx.explorer("Choose a month", dp, groups=True)
    # ---- chart 1: yearly 24K tola, log scale ----
    W, H, L, B = 760, 320, 64, 30
    lo, hi = math.log10(10), math.log10(max(Y[y]["t24"] for y in yrs) * 1.4)
    xs = lambda i: L + i * (W - L - 12) / (len(yrs) - 1)
    yv = lambda v: H - B - (math.log10(v) - lo) / (hi - lo) * (H - B - 12)
    pts = " ".join(f"{xs(i):.1f},{yv(Y[y]['t24']):.1f}" for i, y in enumerate(yrs))
    grid = "".join(f'<line x1="{L}" x2="{W - 12}" y1="{yv(v):.1f}" y2="{yv(v):.1f}"/><text x="4" y="{yv(v) + 4:.1f}">{lab}</text>'
                   for v, lab in ((10, "Rs 10"), (100, "Rs 100"), (1000, "Rs 1k"), (10000, "Rs 10k"), (100000, "Rs 1 lakh"), (1000000, "Rs 10 lakh")) if v < 10 ** hi)
    xl = "".join(f'<text x="{xs(i):.1f}" y="{H - 8}" text-anchor="middle">{y}</text>' for i, y in enumerate(yrs) if y % 10 == 0)
    svg1 = (f'<figure style="margin:18px 0"><svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="ghT1" style="width:100%;height:auto;background:var(--surface);border:1px solid var(--line);border-radius:14px">'
            f'<title id="ghT1">24K gold price per tola in Pakistan, yearly average 1947–{cy} (log scale)</title>'
            f'<g stroke="currentColor" stroke-opacity=".12" font-size="11" fill="currentColor" fill-opacity=".6">{grid}</g>'
            f'<g font-size="11" fill="currentColor" fill-opacity=".6">{xl}</g>'
            f'<polyline points="{pts}" fill="none" stroke="#c9971f" stroke-width="3" stroke-linejoin="round"/></svg>'
            f'<figcaption style="color:var(--muted);font-size:14px;margin-top:6px">Yearly average 24K gold price per tola in Pakistan, 1947–{cy}. '
            f'Log scale: every gridline is 10 times the one below it.</figcaption></figure>')

    # ---- chart 2: daily gold and silver since 2024 ----
    def line_chart(key, color, tid, title, cap, step):
        W2, H2, L2 = 760, 240, 70
        vals = [r[key] for r in days if r[key]]
        dd_ = [r for r in days if r[key]]
        mn, mx = min(vals) * 0.95, max(vals) * 1.03
        x2 = lambda i: L2 + i * (W2 - L2 - 12) / (len(dd_) - 1)
        y2 = lambda v: H2 - 28 - (v - mn) / (mx - mn) * (H2 - 40)
        p2 = " ".join(f"{x2(i):.1f},{y2(r[key]):.1f}" for i, r in enumerate(dd_))
        g0 = math.ceil(mn / step) * step
        gr = "".join(f'<line x1="{L2}" x2="{W2 - 12}" y1="{y2(v):.1f}" y2="{y2(v):.1f}"/><text x="4" y="{y2(v) + 4:.1f}">{rs(v)}</text>'
                     for v in range(int(g0), int(mx), step))
        seen, xl2 = set(), ""
        for i, r in enumerate(dd_):
            if r["d"][5:7] in ("01", "07") and r["d"][:7] not in seen:
                seen.add(r["d"][:7])
                xl2 += f'<text x="{x2(i):.1f}" y="{H2 - 8}" text-anchor="middle">{MON[int(r["d"][5:7]) - 1][:3]} {r["d"][:4]}</text>'
        return (f'<figure style="margin:18px 0"><svg viewBox="0 0 {W2} {H2}" role="img" aria-labelledby="{tid}" style="width:100%;height:auto;background:var(--surface);border:1px solid var(--line);border-radius:14px">'
                f'<title id="{tid}">{E(title)}</title><g stroke="currentColor" stroke-opacity=".12" font-size="11" fill="currentColor" fill-opacity=".6">{gr}</g>'
                f'<g font-size="11" fill="currentColor" fill-opacity=".6">{xl2}</g><polyline points="{p2}" fill="none" stroke="{color}" stroke-width="2.2" stroke-linejoin="round"/></svg>'
                f'<figcaption style="color:var(--muted);font-size:14px;margin-top:6px">{E(cap)}</figcaption></figure>')
    svg2 = line_chart("t24", "#c9971f", "ghT2", f"Daily 24K gold price per tola in Pakistan since {fd(first_d)}",
                      f"Daily 24K gold price per tola in Pakistan, {fd(first_d)} to {fd(ld)}.", 100000)
    title = f"Gold Rate History Pakistan: Year-wise Tola Price 1947–{cy}"
    desc = (f"Gold rate history in Pakistan: 24K tola from about {rs(t47)} in 1947 to {rs(cur)} now. Year-wise and month-wise "
            f"table, daily gold rates since 2024.")
    if len(desc) > 155:
        desc = f"Gold rate history in Pakistan: 24K tola from about {rs(t47)} in 1947 to {rs(cur)} now. Year-wise, monthly and daily gold rates."
    h1 = f"Gold rate history in Pakistan: tola price from 1947 to {cy}"
    faq = [
        ("What was the gold rate in Pakistan in 1947?",
         f"About {rs(t47)} per tola of 24K gold, by our estimate: the world price was fixed at $35 an ounce and one US dollar was Rs 3.31. Local bazaar prices of that time could differ."),
        ("What was the 1 tola gold price in Pakistan in 2000, 2010 and 2020?",
         f"Yearly averages, estimated from the world gold price and the dollar rate: about {rs(t00)} in 2000, {rs(t10)} in 2010 and {rs(t20)} in 2020 for 24K gold per tola."),
        ("What was the gold rate in Pakistan in 2024 and 2025?",
         f"The average 24K price per tola was about {rs(t24y)} in 2024 and {rs(t25y)} in 2025 (international price converted at the daily dollar rate)."),
        ("What is the highest gold rate in Pakistan so far?",
         f"In our daily data the highest 24K reference price was {rs(top['t24'])} per tola on {fd(dt.date.fromisoformat(top['d']))}, when gold was about ${top['xau']:,.0f} an ounce. Sarafa bazaar rates on the same day can be different."),
        ("How is the historical tola price calculated?",
         "Tola price = gold price in US dollars per ounce × USD/PKR ÷ 31.1035 × 11.6638. Before March 2024 we use the monthly world price and the monthly average dollar rate (yearly before 1957), so older figures are estimates. 22K is the 24K price × 22/24."),
        ("Why is the sarafa bazaar rate different from this page?",
         "Sarafa associations add a local premium, duties and dealer margins, and they update at their own times. Jewellery also adds making charges. Use this page for history and trends; check your jeweller for a buying price."),
        ("How much has gold gone up since 2000 in Pakistan?",
         f"From about {rs(t00)} per tola (2000 average) to {rs(cur)} on {fd(ld)}, about {cur / t00:.0f} times. Two things pushed it: gold rose about {g_mult:.1f} times in dollars and the dollar rose about {d_mult:.1f} times in rupees. Past prices do not tell what gold will do next."),
        ("Where can I see the silver (chandi) rate history?",
         "Silver has its own page: the silver rate history in Pakistan, with daily chandi rates per tola, 10 gram and kg since March 2024, monthly averages and a date lookup."),
        ("Pakistan mein sone ka rate 1947 se ab tak kitna barha?",
         f"1947 mein 1 tola 24K sona taqreeban {rs(t47)} ka tha, 2000 mein {rs(t00)}, 2010 mein {rs(t10)}, 2020 mein {rs(t20)} aur aaj taqreeban {rs(cur)} (international qeemat se andaza)."),
    ]
    faq_h = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faq)
    dj = json.dumps([[r["d"], round(r["t24"]), 0] for r in days], separators=(",", ":"))
    mj = json.dumps({x["k"]: round(x["t24"]) for x in months}, separators=(",", ":"))

    body = hx.CSS + hx.YR_CSS + f'''<div class="qa"><b class="k">Quick answer</b><p>One tola of 24K gold in Pakistan was about <b>{rs(t47)} in 1947</b>, <b>{rs(t00)} in 2000</b>, <b>{rs(t10)} in 2010</b>, <b>{rs(t20)} in 2020</b>, <b>{rs(t25y)} in 2025</b> (yearly averages) and <b>{rs(cur)}</b> on {fd(ld)}. Find any date below: daily rates from {fd(first_d)}, and a year-wise table back to 1947 where every year opens to show its 12 months. Looking for chandi? See the <a href="silver-rate-history-pakistan.html">silver rate history</a>.</p></div>
<h2 id="lookup">Gold rate on any date</h2>
<div class="gr-calc" style="border:1px solid var(--line);border-radius:14px;padding:16px;background:var(--surface)"><label for="ghD" style="font-weight:600">Pick a date</label>
<input type="date" id="ghD" min="1947-08-01" max="{last['d']}" value="{last['d']}" style="display:block;margin:8px 0;padding:10px;border:1px solid var(--line);border-radius:10px;font-size:16px;background:var(--bg);color:var(--ink)">
<div id="ghR" aria-live="polite" style="font-size:17px;line-height:1.7;margin:6px 0 0">24K: <b>{rs(cur)}</b> per tola · 22K: <b>{rs(cur * 22 / 24)}</b> · 21K: <b>{rs(cur * 21 / 24)}</b> ({fd(ld)})</div>
<p style="font-size:13.5px;color:var(--muted);margin:6px 0 0">Daily rates from {fd(first_d)}; before that, the monthly average (estimate).</p></div>
<h2 id="price-chart">Gold price per tola from 1947 to {cy}</h2>
<p>Gold in Pakistan has gone from about <b>{rs(t47)}</b> a tola in 1947 to <b>{rs(cur)}</b> in {cy}, about <b>{cur / t47:,.0f} times</b>. Two engines drive it: the world gold price in dollars, and the dollar rate in rupees (see the <a href="usd-to-pkr-history.html">USD to PKR history</a>). When both rise together, the tola rate jumps.</p>
{svg1}
<h2 id="years">Gold rate in Pakistan year-wise (1947–{cy})</h2>
<p>Yearly average price per tola, newest first. Gold $/oz is the world price; USD/PKR is the average dollar rate of that year. Change is against the year before.</p>
<p class="yr-hint"><b>Click any year</b> to open its month-by-month rates right below it; click again to close.</p>
{yt}
<h2 id="decades">Decade by decade</h2>
<p>How many times the 24K tola price grew inside each decade (first year average to last year average).</p>
<div class="tbl"><table><thead><tr><th>Decade</th><th>Start</th><th>End</th><th>Growth</th></tr></thead><tbody>{dec}</tbody></table></div>
<h2 id="moments">Key moments in gold's history</h2>
<ul><li><b>1947–1971:</b> the world price was fixed at about <b>$35 an ounce</b> under the Bretton Woods system, so the tola rate in Pakistan moved mainly with the rupee (Rs 3.31, then Rs 4.76 from 1955).</li>
<li><b>August 1971:</b> the US ended the dollar's convertibility into gold and the price was set free.</li>
<li><b>{fm(m80)}:</b> the first big peak, a monthly average of about <b>${m80['usd']:,.0f}</b> an ounce, after high inflation and the oil shocks.</li>
<li><b>{fm(m01)}:</b> the lowest level in about 20 years, near <b>${m01['usd']:,.0f}</b> an ounce, about {rs(m01['t24'])} a tola in Pakistan.</li>
<li><b>{fm(m11)}:</b> a new high near <b>${m11['usd']:,.0f}</b> after the 2008 crisis, about {rs(m11['t24'])} a tola.</li>
<li><b>{fm(m20)}:</b> the COVID-19 high near <b>${m20['usd']:,.0f}</b>; with the rupee at Rs 160+, the tola passed Rs 1 lakh.</li>
<li><b>2022–2023:</b> the rupee's biggest fall (dollar above Rs 300) pushed the tola rate up much faster than the world price, which rose only modestly.</li>
<li><b>2024–{cy}:</b> central-bank buying, rate cuts and global tension lifted gold above $3,000 and then $4,000 an ounce. The highest daily reference in our data was <b>${top_usd['xau']:,.0f}</b> on {fd(dt.date.fromisoformat(top_usd['d']))}; the highest tola price was <b>{rs(top['t24'])}</b>.</li></ul>
<h2 id="growth">What Rs 1 lakh of gold in 2000 is worth today</h2>
<p>Rs 100,000 (1 lakh) put into 24K gold at the 2000 average price (about {rs(t00)} a tola) would buy about <b>{100000 / t00:.1f} tola</b>. At {fd(ld)}'s rate that gold is worth about <b>{rs(lakh00)}</b>. The same Rs 1 lakh kept in dollars would be worth about {rs(100000 * d_mult)} today. This is a look back, not a forecast: gold also had long flat and falling periods (1980–2001, 2012–2018), and past prices do not tell what it will do next.</p>
<h2 id="daily">Daily gold rate in Pakistan</h2>
<p>Every weekday from {fd(first_d)}. Pick a month (or use ‹ ›). 10 g = 24K price for 10 grams; Gold $/oz and USD/PKR are the two numbers behind that day's rate.</p>
{svg2}
{dd}
<h2 id="why">Why gold keeps rising in rupees</h2>
<p>A tola in Pakistan is priced from the world gold price in dollars. So the local rate rises when gold rises abroad (inflation, interest-rate cuts, wars, central banks buying), <i>and</i> when the rupee falls. Since 2000 gold rose about <b>{g_mult:.1f} times</b> in dollars while the dollar rose about <b>{d_mult:.1f} times</b> in rupees; together that is about {g_mult * d_mult:.0f} times. Traders follow the same driver on charts as XAUUSD: see the <a href="guide-gold-trading.html">gold trading guide</a> and today's <a href="gold-rate-pakistan.html">gold rate in Pakistan</a>.</p>
<div class="khulasa"><h2>Khulasa (Roman Urdu / Hindi)</h2><ul>
<li>1947 mein 1 tola 24K sona taqreeban {rs(t47)} ka tha, 2000 mein {rs(t00)}, 2010 mein {rs(t10)}, 2020 mein {rs(t20)}.</li>
<li>Aaj ({fd(ld)}) 24K sona {rs(cur)} fi tola hai.</li>
<li>Sone ka rate do cheezon se barhta hai: duniya mein gold ki dollar qeemat, aur dollar ka rate.</li>
<li>2024 se pehle ke rate andaza hain; sarafa bazaar ka rate thora mukhtalif hota hai.</li>
<li>Kisi bhi tareekh ka rate upar wale date box se dekhein.</li></ul></div>
<section class="gr-ur" lang="ur" dir="rtl" style="font-family:var(--f-ur);line-height:2.1;margin:18px 0"><h2>پاکستان میں سونے کے ریٹ کی تاریخ</h2><p>1947 میں ایک تولہ سونا تقریباً {t47:,.0f} روپے کا تھا۔ 2000 میں اوسط {t00:,.0f} روپے، 2020 میں {t20:,.0f} روپے، اور آج {ld.day} {UR_MON[ld.month - 1]} {ld.year} کو 24 قیراط سونا {cur:,.0f} روپے فی تولہ ہے۔ پرانے ریٹ انٹرنیشنل قیمت اور ڈالر ریٹ سے نکالا گیا اندازہ ہیں، صرافہ بازار کا ریٹ تھوڑا مختلف ہوتا ہے۔</p></section>
<div class="ls-faq"><h2>Questions</h2>{faq_h}</div>
<h2>Sources and method</h2>
<p style="font-size:14.5px">World gold price, monthly average in US dollars per ounce: the open <i>gold-prices</i> dataset (datasets/gold-prices on GitHub). Daily gold from March 2024: reference rates from an open currency data service (one isolated bad day smoothed), and from 21 November 2026 the prices on our <a href="gold-rate-pakistan.html">live gold rate page</a>. Dollar rate: World Bank yearly averages, BIS monthly averages from 1957 and daily rates, as on our <a href="usd-to-pkr-history.html">USD to PKR history</a>. Formula: USD/oz × USD/PKR ÷ 31.1035 × 11.6638 = price per tola. Figures before March 2024 are estimates, not historical sarafa (APGJSA) rates. Updated {fd(now.date())}.</p>
<nav class="pn" aria-label="Rates"><a href="gold-rate-pakistan.html"><small>‹ Live</small><b>Gold rate in Pakistan today</b></a><a class="nx" href="silver-rate-history-pakistan.html"><small>Next ›</small><b>Silver rate history</b></a></nav>
<p class="ls-disc">For information only; not an offer to buy or sell gold, and not financial advice. Gold prices can fall as well as rise.</p>
''' + hx.JS + hx.YR_JS + f'''<script type="application/json" id="ghData">{{"d":{dj},"m":{mj}}}</script>
<script>(function(){{try{{var D=JSON.parse(document.getElementById('ghData').textContent),m={{}};D.d.forEach(function(r){{m[r[0]]=r}});var i=document.getElementById('ghD'),o=document.getElementById('ghR');function f(n){{return 'Rs '+Math.round(n).toLocaleString('en-US')}}function out(r,t){{o.innerHTML='24K: <b>'+f(r[1])+'</b> per tola · 22K: <b>'+f(r[1]*22/24)+'</b> · 21K: <b>'+f(r[1]*21/24)+'</b> · 10 g 24K: <b>'+f(r[1]/11.6638*10)+'</b>'+' ('+t+')'}}function show(){{var v=i.value;if(!v)return;var d=new Date(v+'T00:00:00'),t=d.toLocaleDateString('en-GB',{{day:'numeric',month:'long',year:'numeric'}});if(m[v]){{out(m[v],t);return}}var k=v;for(var j=0;j<6&&!m[k];j++){{d.setDate(d.getDate()-1);k=d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2)}}if(m[k]){{out(m[k],'nearest earlier rate, '+k);return}}var mk=v.slice(0,7);if(D.m[mk]){{var dd=new Date(v+'T00:00:00');o.innerHTML='24K ≈ <b>'+f(D.m[mk])+'</b> per tola · 22K ≈ <b>'+f(D.m[mk]*22/24)+'</b> (estimated average for '+dd.toLocaleDateString('en-GB',{{month:'long',year:'numeric'}})+')'}}else o.textContent='No data for this date.'}}i.addEventListener('change',show);}}catch(e){{}}}})();</script>'''

    T = open(os.path.join(ROOT, "guide-ict-silver-bullet-time-in-pakistan.html"), encoding="utf-8").read()
    s = T
    a = s.index('<div class="wrap ls-body">'); b = s.index('<aside class="ls-side">')
    s = s[:a] + '<div class="wrap ls-body">\n  <article class="ls-art">\n' + body + '\n  </article>\n  ' + s[b:]
    hs = s.index('<section class="ls-hero">'); he = s.index('</section>', hs) + len('</section>')
    hero = (f'<section class="ls-hero"><div class="wrap gh-grid"><div class="gh-txt">\n'
            f'  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a>›<a href="gold-rate-pakistan.html">Gold Rate</a>›<span>Gold rate history</span></nav>\n'
            f'  <div class="ls-meta">Rates · history 1947–{cy}</div>\n  <h1>{E(h1)}</h1>\n'
            f'  <p class="ur" lang="ur" style="font-family:var(--f-ur);font-size:20px;line-height:2.1;margin:4px 0">پاکستان میں سونے کے ریٹ کی تاریخ: 1947 سے آج تک</p>\n'
            f'  <p class="ls-lead">What a tola of gold cost in Pakistan in every year since independence, every month since 1947 and every weekday since {fd(first_d)}, with a date lookup and the moments that moved the price.</p>\n'
            f'  <div class="byline"><img src="logo-128.webp" alt="Qazi Forex Tips" width="46" height="46"><div>By the <b>Qazi Forex Tips</b> team, led by <a href="about.html"><b>Dr. Qazi Abdul Basit</b></a>, Ph.D<br>Updated {fd(now.date())}</div></div>\n</div>\n'
            f'  <figure class="gh-art"><img src="{HERO}.webp" srcset="{HERO}-800.webp 800w, {HERO}.webp 1600w" sizes="(min-width:1000px) 560px, 100vw" width="1600" height="1280" '
            f'alt="Gold rate history in Pakistan: 3D gold bars rising from about Rs {t47:,.0f} per tola in 1947 to Rs {cur / 1000:,.0f}k in {cy}" fetchpriority="high" decoding="async"></figure>\n</div></section>')
    s = s[:hs] + hero + s[he:]
    s = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", s, count=1)
    for attr, val in (('name="description"', desc), ('property="og:title"', title), ('property="og:description"', desc),
                      ('name="twitter:title"', title), ('name="twitter:description"', desc)):
        s = re.sub(r'(<meta ' + attr + r' content=")[^"]*(")', lambda mm: mm.group(1) + E(val) + mm.group(2), s, count=1)
    s = s.replace("https://qaziforextips.com/guide-ict-silver-bullet-time-in-pakistan.html", URL)
    s = re.sub(r'(<meta property="og:image" content=")[^"]*', r'\g<1>https://qaziforextips.com/' + HERO + '.jpg', s)
    s = re.sub(r'(<meta name="twitter:image" content=")[^"]*', r'\g<1>https://qaziforextips.com/' + HERO + '.jpg', s)
    ldj = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": URL + "#article", "headline": h1, "description": desc, "url": URL, "mainEntityOfPage": URL,
         "image": [{"@type": "ImageObject", "url": "https://qaziforextips.com/" + HERO + ".webp", "width": 1600, "height": 1280,
                    "caption": f"Gold rate history in Pakistan: 24K tola price from 1947 to {cy}"}],
         "datePublished": "2026-11-21T00:00:00+05:00", "dateModified": now.strftime("%Y-%m-%dT%H:%M:%S+05:00"), "inLanguage": "en",
         "keywords": "gold rate history in pakistan, gold price history pakistan, gold rate in pakistan year wise, 1 tola gold price in 2000 in pakistan, gold rate in 1947 in pakistan, gold rate in pakistan month wise",
         "author": {"@type": "Organization", "@id": "https://qaziforextips.com/#org", "name": "Qazi Forex Tips", "url": "https://qaziforextips.com/"},
         "publisher": {"@type": "Organization", "@id": "https://qaziforextips.com/#org", "name": "Qazi Forex Tips", "logo": {"@type": "ImageObject", "url": "https://qaziforextips.com/logo.png"}}},
        {"@type": "Dataset", "name": f"Gold price history in Pakistan (1947–{cy})",
         "description": f"Estimated 24K gold price per tola in Pakistani rupees: yearly and monthly from 1947, daily from {days[0]['d']}.",
         "url": URL, "temporalCoverage": "1947-08/" + last["d"], "creator": {"@type": "Organization", "name": "Qazi Forex Tips", "url": "https://qaziforextips.com/"},
         "isBasedOn": ["https://github.com/datasets/gold-prices", "https://data.worldbank.org/indicator/PA.NUS.FCRF?locations=PK"],
         "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": "https://qaziforextips.com/data/metals-daily.json"},
                          {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": "https://qaziforextips.com/data/gold-monthly.json"}],
         "license": "https://qaziforextips.com/terms.html"},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://qaziforextips.com/"},
                                                        {"@type": "ListItem", "position": 2, "name": "Gold Rate in Pakistan", "item": "https://qaziforextips.com/gold-rate-pakistan.html"},
                                                        {"@type": "ListItem", "position": 3, "name": "Gold rate history", "item": URL}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda mm: '<script type="application/ld+json">' + json.dumps(ldj, ensure_ascii=False) + '</script>', s, count=1, flags=re.S)
    path = os.path.join(ROOT, SLUG)
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    norm = lambda t: re.sub(r"Updated \d+ \w+ \d{4}|\"dateModified\": \"[^\"]*\"", "", t)
    if norm(old) != norm(s):
        open(path, "w", encoding="utf-8").write(s)
        print("gold history page written:", len(days), "days,", len(months), "months, title", len(title), "desc", len(desc))
    else:
        print("gold history page unchanged")


if __name__ == "__main__":
    main()
