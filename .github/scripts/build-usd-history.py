# -*- coding: utf-8 -*-
"""Builds usd-to-pkr-history.html: dollar rate history in Pakistan (USD to PKR) from 1947 to today.
Data:
  data/usdpkr-annual.json  yearly averages. 1960-2025: World Bank, official exchange rate (PA.NUS.FCRF, period average);
                           1950-1959: Penn World Table 11.0 (FRED XRNCUSPKA618NRUG); 1947-1949: par value Rs 3.31.
  data/usdpkr-daily.json   daily reference rate from 2 March 2024 (open currency API, mid-market; isolated spikes smoothed),
                           extended every weekday by update-rates.py with the site's own USD/PKR rate.
Layout (header, footer, sidebar, scripts) is taken from the Silver Bullet guide, so the page matches the site.
Run: python3 .github/scripts/build-usd-history.py   (called by the rates workflow; safe to run any time)."""
import json, os, re, html, datetime as dt, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hx

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SLUG = "usd-to-pkr-history.html"
URL = "https://qaziforextips.com/" + SLUG
HERO = "img/guides/hero/usd-to-pkr-history-1947-2026"
PKT = dt.timezone(dt.timedelta(hours=5))
E = lambda s: html.escape(str(s), quote=True)
MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
UR_MON = ["جنوری", "فروری", "مارچ", "اپریل", "مئی", "جون", "جولائی", "اگست", "ستمبر", "اکتوبر", "نومبر", "دسمبر"]


def load(name):
    return json.load(open(os.path.join(ROOT, "data", name), encoding="utf-8"))


def main():
    ann = load("usdpkr-annual.json")
    daily = sorted(load("usdpkr-daily.json"), key=lambda h: h["d"])
    now = dt.datetime.now(PKT)
    last = daily[-1]
    ld_last = dt.date.fromisoformat(last["d"])
    # yearly rows: annual file + current-year average from daily data
    years = {a["y"]: a for a in ann}
    cy = ld_last.year
    if cy not in years:
        vals = [h["pkr"] for h in daily if h["d"].startswith(str(cy))]
        years[cy] = {"y": cy, "pkr": round(sum(vals) / len(vals), 2), "src": "ytd"}
    ys = sorted(years)
    # monthly averages from daily data
    months = {}
    for h in daily:
        months.setdefault(h["d"][:7], []).append(h["pkr"])
    mrows = sorted(months.items(), reverse=True)

    def rs(v):
        return f"Rs {v:,.2f}"

    # ---- year-wise table ----
    yt = ""
    prev = None
    for y in ys:
        a = years[y]
        ch = "–" if prev is None else (f'{(a["pkr"] / prev - 1) * 100:+.1f}%')
        note = {"par": "par value", "pwt": "", "wb": "", "ytd": f"Jan–{MON[ld_last.month - 1][:3]} average"}[a["src"]]
        yt = f'<tr><th scope="row">{y}</th><td>{rs(a["pkr"])}</td><td>{ch}</td><td>{note}</td></tr>' + yt
        prev = a["pkr"]
    # ---- decade summary ----
    dec = ""
    for d0 in range(1950, cy + 1, 10):
        a, b = years.get(d0), years.get(min(d0 + 9, cy))
        if a and b:
            dec += f"<tr><th scope=\"row\">{d0}s</th><td>{rs(a['pkr'])}</td><td>{rs(b['pkr'])}</td><td>{(b['pkr'] / a['pkr'] - 1) * 100:+.0f}%</td></tr>"
    # ---- monthly table ----
    mt = ""
    for k, v in mrows:
        y, m = int(k[:4]), int(k[5:])
        mt += f'<tr><th scope="row">{MON[m - 1]} {y}</th><td>{rs(sum(v) / len(v))}</td><td>{rs(min(v))}</td><td>{rs(max(v))}</td></tr>'
    # ---- daily tables by month, shown one at a time ----
    dp = []
    for k, v in mrows:
        y, m = int(k[:4]), int(k[5:])
        rows = [h for h in daily if h["d"].startswith(k)]
        body = "".join(f'<tr id="d{h["d"]}"><th scope="row">{dt.date.fromisoformat(h["d"]).strftime("%a %-d %b %Y")}</th><td>{rs(h["pkr"])}</td><td>{rs(h["pkr"] * 100)}</td></tr>'
                       for h in reversed(rows))
        dp.append((k, f"{MON[m - 1]} {y}", f"USD to PKR in {MON[m - 1]} {y} (daily)",
                   f'<div class="tbl"><table><thead><tr><th>Date</th><th>1 USD</th><th>100 USD</th></tr></thead><tbody>{body}</tbody></table></div>'))
    dd = hx.explorer("Choose a month", dp, groups=True)
    # ---- chart (annual, inline SVG) ----
    W, H, L, B = 760, 300, 46, 30
    mx = max(years[y]["pkr"] for y in ys)
    xs = lambda i: L + i * (W - L - 10) / (len(ys) - 1)
    yv = lambda v: H - B - v / (mx * 1.05) * (H - B - 12)
    pts = " ".join(f"{xs(i):.1f},{yv(years[y]['pkr']):.1f}" for i, y in enumerate(ys))
    grid = "".join(f'<line x1="{L}" x2="{W-10}" y1="{yv(v):.1f}" y2="{yv(v):.1f}"/><text x="4" y="{yv(v)+4:.1f}">{v}</text>' for v in (0, 50, 100, 150, 200, 250, 300))
    lab = "".join(f'<text x="{xs(i):.1f}" y="{H-8}" text-anchor="middle">{y}</text>' for i, y in enumerate(ys) if y % 10 == 0)
    svg = (f'<figure style="margin:18px 0"><svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="usdT" style="width:100%;height:auto;background:var(--surface);border:1px solid var(--line);border-radius:14px">'
           f'<title id="usdT">USD to PKR yearly average from 1947 ({rs(years[ys[0]]["pkr"])}) to {cy} ({rs(years[cy]["pkr"])})</title>'
           f'<g stroke="currentColor" stroke-opacity=".12" font-size="11" fill="currentColor" fill-opacity=".6">{grid}</g>'
           f'<g font-size="11" fill="currentColor" fill-opacity=".6">{lab}</g>'
           f'<polyline points="{pts}" fill="none" stroke="#c9971f" stroke-width="3" stroke-linejoin="round"/></svg>'
           f'<figcaption style="color:var(--muted);font-size:14px;margin-top:6px">Yearly average dollar rate in Pakistan, 1947–{cy} (rupees per US dollar).</figcaption></figure>')

    # ---- facts for text ----
    peak_m = max(months.items(), key=lambda kv: sum(kv[1]) / len(kv[1]))
    low_m = min(months.items(), key=lambda kv: sum(kv[1]) / len(kv[1]))
    a47, a00, a10, a18, a23 = (years[y]["pkr"] for y in (1947, 2000, 2010, 2018, 2023))
    cur = last["pkr"]
    first_d = dt.date.fromisoformat(daily[0]["d"])
    fd = lambda d: d.strftime("%-d %B %Y")
    title = f"USD to PKR History: Dollar Rate in Pakistan 1947–{cy}"
    desc = (f"Dollar rate history in Pakistan: Rs 3.31 in 1947 to {rs(cur)} today. Year-wise table 1947–{cy}, monthly averages "
            f"and daily USD to PKR rates since 2024.")
    if len(desc) > 155:
        desc = f"Dollar rate history in Pakistan: Rs 3.31 in 1947 to {rs(cur)} today. Year-wise table, monthly averages and daily USD to PKR since 2024."
    h1 = f"Dollar rate history in Pakistan: USD to PKR from 1947 to {cy}"
    faq = [
        ("What was the dollar rate in Pakistan in 1947?", "At independence one US dollar was about Rs 3.31. Pakistan kept that rate until August 1955, when the rupee was devalued to Rs 4.76."),
        ("What was the dollar rate in Pakistan in 2000, 2010 and 2018?", f"Yearly averages: {rs(a00)} in 2000, {rs(a10)} in 2010 and {rs(a18)} in 2018 (World Bank official rate)."),
        ("What was the dollar rate in Pakistan in 2023?", f"The 2023 average was {rs(a23)}. It was the sharpest fall of the rupee in its history; the dollar briefly went above Rs 300 in early September 2023."),
        (f"What is the dollar rate in Pakistan today?", f"On {fd(ld_last)} one US dollar was {rs(cur)}. For the live rate, updated every 30 minutes on weekdays, see the dollar rate page."),
        ("How do I find the dollar rate on a specific date?", f"Use the date lookup on this page or open the month in the daily tables. Daily rates are available from {fd(first_d)}; for earlier dates the yearly average is shown."),
        ("How much has the rupee fallen against the dollar since 1947?", f"From Rs 3.31 to about {rs(cur)}: the dollar now buys about {cur / 3.31:.0f} times as many rupees as in 1947."),
        ("Pakistan mein dollar ka rate 1947 se ab tak kitna barha?", f"1947 mein 1 dollar taqreeban Rs 3.31 ka tha, 2000 mein {rs(a00)}, 2023 mein {rs(a23)} aur aaj taqreeban {rs(cur)}."),
    ]
    faq_h = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faq)
    dj = json.dumps([[h["d"], h["pkr"]] for h in daily], separators=(",", ":"))
    aj = json.dumps({str(y): years[y]["pkr"] for y in ys}, separators=(",", ":"))

    body = hx.CSS + f'''<div class="qa"><b class="k">Quick answer</b><p>One US dollar was <b>Rs 3.31 in 1947</b>, <b>{rs(a00)} in 2000</b>, <b>{rs(a18)} in 2018</b>, <b>{rs(a23)} in 2023</b> (yearly averages) and <b>{rs(cur)}</b> on {fd(ld_last)}. Find any date below: daily rates from {fd(first_d)}, monthly averages, and a year-wise table back to 1947.</p></div>
<h2 id="lookup">Dollar rate on any date</h2>
<div class="gr-calc" style="border:1px solid var(--line);border-radius:14px;padding:16px;background:var(--surface)"><label for="uhD" style="font-weight:600">Pick a date</label>
<input type="date" id="uhD" min="1947-08-14" max="{last['d']}" value="{last['d']}" style="display:block;margin:8px 0;padding:10px;border:1px solid var(--line);border-radius:10px;font-size:16px;background:var(--bg);color:var(--ink)">
<p id="uhR" aria-live="polite" style="font-size:18px;margin:6px 0 0">1 USD = <b>{rs(cur)}</b> on {fd(ld_last)}</p><p style="font-size:13.5px;color:var(--muted);margin:6px 0 0">Daily reference rate from {fd(first_d)}; before that, the yearly average.</p></div>
<h2 id="price-chart">USD to PKR from 1947 to {cy}</h2>
<p>The Pakistani rupee started at <b>Rs 3.31</b> per dollar in 1947. It stayed fixed for long periods, then fell in steps after 1972 and much faster after 2018. By {cy} a dollar costs about <b>{cur / 3.31:.0f} times</b> as many rupees as at independence.</p>
{svg}
<h2 id="years">Dollar rate in Pakistan year-wise (1947–{cy})</h2>
<p>Yearly average rate of 1 US dollar in Pakistani rupees, newest first. The change column is against the year before.</p>
<div class="tbl hx-s"><table><thead><tr><th>Year</th><th>1 USD (average)</th><th>Change</th><th>Note</th></tr></thead><tbody>{yt}</tbody></table></div>
<h2 id="decades">Decade by decade</h2>
<div class="tbl"><table><thead><tr><th>Decade</th><th>Start</th><th>End</th><th>Change</th></tr></thead><tbody>{dec}</tbody></table></div>
<h2 id="moments">Key moments in the rupee's history</h2>
<ul><li><b>1947–1955:</b> Rs 3.31 per dollar. In 1949 Pakistan did not follow the sterling devaluation that India made.</li>
<li><b>August 1955:</b> devalued to <b>Rs 4.76</b>, a rate that held until 1971.</li>
<li><b>May 1972:</b> devalued to Rs 11, then set at <b>Rs 9.90</b> from February 1973 until 1981.</li>
<li><b>January 1982:</b> the fixed link to the dollar ended and a managed float began; the rupee fell steadily through the 1980s and 1990s.</li>
<li><b>2008:</b> a balance-of-payments crisis took the dollar from about Rs 62 to near Rs 80 within a year.</li>
<li><b>2018–2019:</b> from about Rs 110 to Rs 160 under the IMF programme and a market-based rate.</li>
<li><b>2022–2023:</b> the biggest fall in history, from about Rs 180 to above Rs 300 at the start of September 2023.</li>
<li><b>2024–{cy}:</b> a calmer period, mostly between Rs 276 and Rs 285 (highest monthly average {rs(sum(peak_m[1]) / len(peak_m[1]))} in {MON[int(peak_m[0][5:]) - 1]} {peak_m[0][:4]}, lowest {rs(sum(low_m[1]) / len(low_m[1]))} in {MON[int(low_m[0][5:]) - 1]} {low_m[0][:4]}).</li></ul>
<h2 id="monthly">Monthly average USD to PKR (since March 2024)</h2>
<div class="tbl hx-s"><table><thead><tr><th>Month</th><th>Average</th><th>Low</th><th>High</th></tr></thead><tbody>{mt}</tbody></table></div>
<h2 id="daily">Daily dollar rate in Pakistan</h2>
<p>Every day from {fd(first_d)}, Pick a month (or use ‹ ›) to see each day.</p>
{dd}
<h2 id="why">Why the rupee keeps falling</h2>
<p>The rupee weakens when Pakistan needs more dollars than it earns: imports (especially fuel) larger than exports, debt repayments, and low foreign exchange reserves. It steadies when remittances, exports, IMF and other inflows rise, and when inflation and interest rates are under control. For traders this matters because Gold in Pakistan is priced through the dollar: see the <a href="gold-rate-pakistan.html">gold rate in Pakistan</a>, which moves with both the world gold price and USD/PKR, and the <a href="gold-rate-history-pakistan.html">gold rate history since 1947</a>.</p>
<div class="khulasa"><h2>Khulasa (Roman Urdu / Hindi)</h2><ul>
<li>1947 mein 1 dollar Rs 3.31 ka tha, 1955 mein Rs 4.76, 1973 se 1981 tak Rs 9.90.</li>
<li>2000 mein average {rs(a00)}, 2018 mein {rs(a18)}, 2023 mein {rs(a23)}.</li>
<li>Aaj ({fd(ld_last)}) 1 dollar taqreeban {rs(cur)} ka hai.</li>
<li>Kisi bhi tareekh ka rate upar wale date box se dekhein; 2024 se rozana rate maujood hai.</li></ul></div>
<section class="gr-ur" lang="ur" dir="rtl" style="font-family:var(--f-ur);line-height:2.1;margin:18px 0"><h2>پاکستان میں ڈالر کی تاریخ</h2><p>1947 میں ایک ڈالر 3.31 روپے کا تھا۔ 2023 میں اوسط ریٹ {years[2023]['pkr']:.2f} روپے رہا، اور آج {ld_last.day} {UR_MON[ld_last.month - 1]} {ld_last.year} کو ایک ڈالر {cur:.2f} روپے کا ہے۔</p></section>
<div class="ls-faq"><h2>Questions</h2>{faq_h}</div>
<h2>Sources and method</h2>
<p style="font-size:14.5px">Yearly averages 1960–2025: World Bank, official exchange rate (LCU per US$, period average). 1950–1959: Penn World Table 11.0 via FRED. 1947–1949: the par value of Rs 3.31. Daily rates from March 2024: mid-market reference rates from an open currency data service, with single-day spikes smoothed, and from 21 November 2026 the interbank rate shown on our <a href="dollar-rate-pakistan.html">live dollar rate page</a>. Open-market (cash) rates are usually a little higher. Updated {fd(now.date())}.</p>
<nav class="pn" aria-label="Rates"><a href="dollar-rate-pakistan.html"><small>‹ Live</small><b>Dollar rate in Pakistan today</b></a><a class="nx" href="gold-rate-pakistan.html"><small>Next ›</small><b>Gold rate in Pakistan today</b></a></nav>
<p class="ls-disc">For information only; not an offer to buy or sell currency, and not financial advice.</p>
''' + hx.JS + f'''<script type="application/json" id="uhData">{{"d":{dj},"y":{aj}}}</script>
<script>(function(){{try{{var D=JSON.parse(document.getElementById('uhData').textContent),m={{}};D.d.forEach(function(r){{m[r[0]]=r[1]}});var i=document.getElementById('uhD'),o=document.getElementById('uhR');function f(n){{return 'Rs '+n.toLocaleString('en-US',{{minimumFractionDigits:2,maximumFractionDigits:2}})}}function show(){{var v=i.value;if(!v)return;var d=new Date(v+'T00:00:00'),t=d.toLocaleDateString('en-GB',{{day:'numeric',month:'long',year:'numeric'}});if(m[v]){{o.innerHTML='1 USD = <b>'+f(m[v])+'</b> on '+t+' (100 USD = '+f(m[v]*100)+')';return}}var k=v;for(var j=0;j<6&&!m[k];j++){{d.setDate(d.getDate()-1);k=d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2)}}if(m[k]){{o.innerHTML='1 USD = <b>'+f(m[k])+'</b> (nearest earlier rate, '+k+')';return}}var y=v.slice(0,4);if(D.y[y]){{o.innerHTML='1 USD ≈ <b>'+f(D.y[y])+'</b> (average for '+y+')'}}else o.textContent='No data for this date.'}}i.addEventListener('change',show);}}catch(e){{}}}})();</script>'''

    T = open(os.path.join(ROOT, "guide-ict-silver-bullet-time-in-pakistan.html"), encoding="utf-8").read()
    s = T
    a = s.index('<div class="wrap ls-body">'); b = s.index('<aside class="ls-side">')
    s = s[:a] + '<div class="wrap ls-body">\n  <article class="ls-art">\n' + body + '\n  </article>\n  ' + s[b:]
    hs = s.index('<section class="ls-hero">'); he = s.index('</section>', hs) + len('</section>')
    hero = (f'<section class="ls-hero"><div class="wrap gh-grid"><div class="gh-txt">\n'
            f'  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a>›<a href="dollar-rate-pakistan.html">Dollar Rate</a>›<span>USD to PKR history</span></nav>\n'
            f'  <div class="ls-meta">Rates · history 1947–{cy}</div>\n  <h1>{E(h1)}</h1>\n'
            f'  <p class="ur" lang="ur" style="font-family:var(--f-ur);font-size:20px;line-height:2.1;margin:4px 0">پاکستان میں ڈالر ریٹ کی تاریخ: 1947 سے آج تک</p>\n'
            f'  <p class="ls-lead">How many rupees a US dollar cost in every year since independence, every month since 2024 and every day since {fd(first_d)}, with a date lookup and the key moments behind each fall.</p>\n'
            f'  <div class="byline"><img src="logo-128.webp" alt="Qazi Forex Tips" width="46" height="46"><div>By the <b>Qazi Forex Tips</b> team, led by <a href="about.html"><b>Dr. Qazi Abdul Basit</b></a>, Ph.D<br>Updated {fd(now.date())}</div></div>\n</div>\n'
            f'  <figure class="gh-art"><img src="{HERO}.webp" srcset="{HERO}-800.webp 800w, {HERO}.webp 1600w" sizes="(min-width:1000px) 560px, 100vw" width="1600" height="1280" '
            f'alt="Dollar rate history in Pakistan: 3D bar chart of USD to PKR from Rs 3.31 in 1947 to about Rs 277 in 2026" fetchpriority="high" decoding="async"></figure>\n</div></section>')
    s = s[:hs] + hero + s[he:]
    s = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", s, count=1)
    for attr, val in (('name="description"', desc), ('property="og:title"', title), ('property="og:description"', desc),
                      ('name="twitter:title"', title), ('name="twitter:description"', desc)):
        s = re.sub(r'(<meta ' + attr + r' content=")[^"]*(")', lambda m: m.group(1) + E(val) + m.group(2), s, count=1)
    s = s.replace("https://qaziforextips.com/guide-ict-silver-bullet-time-in-pakistan.html", URL)
    s = re.sub(r'(<meta property="og:image" content=")[^"]*', r'\g<1>https://qaziforextips.com/' + HERO + '.jpg', s)
    s = re.sub(r'(<meta name="twitter:image" content=")[^"]*', r'\g<1>https://qaziforextips.com/' + HERO + '.jpg', s)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": URL + "#article", "headline": h1, "description": desc, "url": URL, "mainEntityOfPage": URL,
         "image": [{"@type": "ImageObject", "url": "https://qaziforextips.com/" + HERO + ".webp", "width": 1600, "height": 1280,
                    "caption": "Dollar rate history in Pakistan: USD to PKR from 1947 to " + str(cy)}],
         "datePublished": "2026-11-21T00:00:00+05:00", "dateModified": now.strftime("%Y-%m-%dT%H:%M:%S+05:00"), "inLanguage": "en",
         "keywords": "dollar rate history in pakistan, usd to pkr history, dollar rate in pakistan year wise, usd to pkr historical rates, dollar rate in 2023 in pakistan, dollar rate 1947 pakistan",
         "author": {"@type": "Organization", "@id": "https://qaziforextips.com/#org", "name": "Qazi Forex Tips", "url": "https://qaziforextips.com/"},
         "publisher": {"@type": "Organization", "@id": "https://qaziforextips.com/#org", "name": "Qazi Forex Tips", "logo": {"@type": "ImageObject", "url": "https://qaziforextips.com/logo.png"}}},
        {"@type": "Dataset", "name": "USD to PKR exchange rate history (1947–" + str(cy) + ")", "description": "Yearly averages from 1947, monthly averages and daily rates from " + daily[0]["d"] + " of the US dollar in Pakistani rupees.",
         "url": URL, "temporalCoverage": "1947/" + last["d"], "creator": {"@type": "Organization", "name": "Qazi Forex Tips", "url": "https://qaziforextips.com/"},
         "isBasedOn": ["https://data.worldbank.org/indicator/PA.NUS.FCRF?locations=PK", "https://fred.stlouisfed.org/series/XRNCUSPKA618NRUG"],
         "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": "https://qaziforextips.com/data/usdpkr-daily.json"},
                          {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": "https://qaziforextips.com/data/usdpkr-annual.json"}],
         "license": "https://qaziforextips.com/terms.html"},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://qaziforextips.com/"},
                                                        {"@type": "ListItem", "position": 2, "name": "Dollar Rate in Pakistan", "item": "https://qaziforextips.com/dollar-rate-pakistan.html"},
                                                        {"@type": "ListItem", "position": 3, "name": "USD to PKR history", "item": URL}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>', s, count=1, flags=re.S)
    path = os.path.join(ROOT, SLUG)
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    # do not rewrite the file when only the "Updated" date would change
    norm = lambda t: re.sub(r"Updated \d+ \w+ \d{4}|\"dateModified\": \"[^\"]*\"", "", t)
    if norm(old) != norm(s):
        open(path, "w", encoding="utf-8").write(s)
        print("usd history page written:", len(daily), "days,", len(ys), "years")
    else:
        print("usd history page unchanged")


if __name__ == "__main__":
    main()
