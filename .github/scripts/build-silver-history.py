# -*- coding: utf-8 -*-
"""Builds silver-rate-history-pakistan.html: silver (chandi) rate history in Pakistan per tola, 10 gram and kg.
Data: data/metals-daily.json (daily XAG in USD/oz from March 2024, weekdays; extended every weekday by update-rates.py)
and data/usdpkr-daily.json (dollar rate). Price per tola = USD/oz x USD/PKR / 31.1035 x 11.6638 (pure 999 silver).
This is the international-price reference, not the sarafa rate. Layout from the Silver Bullet guide, like the gold page.
Run: python3 .github/scripts/build-silver-history.py   (called by the rates workflow)."""
import json, os, re, html, math, datetime as dt, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hx

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SLUG = "silver-rate-history-pakistan.html"
URL = "https://qaziforextips.com/" + SLUG
HERO = "img/guides/hero/silver-rate-history-pakistan"
PKT = dt.timezone(dt.timedelta(hours=5))
OZ, TOLA = 31.1034768, 11.6638038
NISAB = 52.5
E = lambda s: html.escape(str(s), quote=True)
MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
UR_MON = ["جنوری", "فروری", "مارچ", "اپریل", "مئی", "جون", "جولائی", "اگست", "ستمبر", "اکتوبر", "نومبر", "دسمبر"]


def load(name):
    return json.load(open(os.path.join(ROOT, "data", name), encoding="utf-8"))


def rs(v, dec=0):
    return f"Rs {v:,.{dec}f}"


def main():
    md = sorted(load("metals-daily.json"), key=lambda h: h["d"])
    upd = {h["d"]: h["pkr"] for h in load("usdpkr-daily.json")}
    now = dt.datetime.now(PKT)
    days = []
    for h in md:
        if not h.get("xag"):
            continue
        p, k = upd.get(h["d"]), dt.date.fromisoformat(h["d"])
        for _ in range(7):
            if p is not None:
                break
            k -= dt.timedelta(days=1)
            p = upd.get(k.isoformat())
        if p is None:
            continue
        t = h["xag"] * p / OZ * TOLA
        days.append({"d": h["d"], "xag": h["xag"], "xau": h["xau"], "pkr": p, "t": t, "g10": t / TOLA * 10, "kg": t / TOLA * 1000})
    last, first = days[-1], days[0]
    ld, fdt = dt.date.fromisoformat(last["d"]), dt.date.fromisoformat(first["d"])
    cy = ld.year
    fd = lambda d: d.strftime("%-d %B %Y")
    fdi = lambda s: fd(dt.date.fromisoformat(s))
    dmon = {}
    for x in days:
        dmon.setdefault(x["d"][:7], []).append(x)
    mon = {k: {"t": sum(r["t"] for r in v) / len(v), "lo": min(r["t"] for r in v), "hi": max(r["t"] for r in v),
               "usd": sum(r["xag"] for r in v) / len(v), "pkr": sum(r["pkr"] for r in v) / len(v),
               "ratio": sum(r["xau"] / r["xag"] for r in v) / len(v)} for k, v in dmon.items()}
    yrs = sorted({int(k[:4]) for k in dmon})
    Y = {}
    for y in yrs:
        v = [r for r in days if r["d"].startswith(str(y))]
        Y[y] = {"t": sum(r["t"] for r in v) / len(v), "lo": min(v, key=lambda r: r["t"]), "hi": max(v, key=lambda r: r["t"]),
                "usd": sum(r["xag"] for r in v) / len(v), "pkr": sum(r["pkr"] for r in v) / len(v),
                "from": v[0]["d"], "to": v[-1]["d"]}
    cur = last["t"]
    top = max(days, key=lambda r: r["t"])
    low = min(days, key=lambda r: r["t"])
    after = [r for r in days if r["d"] > top["d"]]
    low_after = min(after, key=lambda r: r["t"]) if after else None
    if low_after and low_after["d"] == last["d"]:
        low_after = None
    ratio = last["xau"] / last["xag"]
    ch_first = (cur / first["t"] - 1) * 100

    # ---- year rows that open to months ----
    rows, prev = [], None
    for y in yrs:
        a = Y[y]
        ch = "–" if prev is None else f"{(a['t'] / prev - 1) * 100:+.1f}%"
        note = f"from {MON[int(a['from'][5:7]) - 1][:3]}" if y == yrs[0] else (f"to {MON[ld.month - 1][:3]}" if y == cy else "")
        subs = []
        for k in sorted((k for k in dmon if k.startswith(str(y))), reverse=True):
            m = mon[k]
            subs.append(f'<tr><th scope="row">{MON[int(k[5:]) - 1]} {y}</th><td>{rs(m["t"])}</td><td>{rs(m["lo"])}</td><td>{rs(m["hi"])}</td>'
                        f'<td>{rs(m["t"] * 1000 / TOLA)}</td><td>${m["usd"]:,.2f}</td><td>{m["ratio"]:.0f}</td></tr>')
        rows.append((str(y), [f'<td>{rs(a["t"])}</td>', f'<td>{rs(a["lo"]["t"])}</td>', f'<td>{rs(a["hi"]["t"])}</td>',
                              f'<td>{rs(a["t"] * NISAB)}</td>', f'<td>${a["usd"]:,.2f}</td>', f'<td>{ch}</td>', f'<td>{note}</td>'], subs))
        prev = a["t"]
    yt = hx.year_table(["Year", "Average tola", "Lowest", "Highest", "52.5 tola", "Silver $/oz", "Change", "Note"], list(reversed(rows)),
                       ["Month", "Average tola", "Low", "High", "1 kg", "Silver $/oz", "Gold/silver ratio"])
    # ---- daily tables, one month at a time ----
    dp = []
    for k in sorted(dmon, reverse=True):
        y, m = int(k[:4]), int(k[5:])
        body = "".join(f'<tr><th scope="row">{dt.date.fromisoformat(r["d"]).strftime("%a %-d %b")}</th><td>{rs(r["t"])}</td><td>{rs(r["g10"])}</td>'
                       f'<td>{rs(r["kg"])}</td><td>${r["xag"]:,.2f}</td><td>{r["pkr"]:,.2f}</td></tr>' for r in reversed(dmon[k]))
        dp.append((k, f"{MON[m - 1]} {y}", f"Silver rate in {MON[m - 1]} {y} (daily)",
                   f'<div class="tbl"><table><thead><tr><th>Date</th><th>Tola</th><th>10 gram</th><th>1 kg</th><th>Silver $/oz</th><th>USD/PKR</th></tr></thead>'
                   f'<tbody>{body}</tbody></table></div>'))
    dd = hx.explorer("Choose a month", dp, groups=True)
    # ---- chart ----
    W2, H2, L2 = 760, 260, 70
    vals = [r["t"] for r in days]
    mn, mx = min(vals) * 0.92, max(vals) * 1.04
    x2 = lambda i: L2 + i * (W2 - L2 - 12) / (len(days) - 1)
    y2 = lambda v: H2 - 28 - (v - mn) / (mx - mn) * (H2 - 40)
    pts = " ".join(f"{x2(i):.1f},{y2(r['t']):.1f}" for i, r in enumerate(days))
    gr = "".join(f'<line x1="{L2}" x2="{W2 - 12}" y1="{y2(v):.1f}" y2="{y2(v):.1f}"/><text x="4" y="{y2(v) + 4:.1f}">{rs(v)}</text>'
                 for v in range(int(math.ceil(mn / 2000) * 2000), int(mx), 2000))
    seen, xl = set(), ""
    for i, r in enumerate(days):
        if r["d"][5:7] in ("01", "07") and r["d"][:7] not in seen:
            seen.add(r["d"][:7])
            xl += f'<text x="{x2(i):.1f}" y="{H2 - 8}" text-anchor="middle">{MON[int(r["d"][5:7]) - 1][:3]} {r["d"][:4]}</text>'
    ti = days.index(top)
    svg = (f'<figure style="margin:18px 0"><svg viewBox="0 0 {W2} {H2}" role="img" aria-labelledby="shT" style="width:100%;height:auto;background:var(--surface);border:1px solid var(--line);border-radius:14px">'
           f'<title id="shT">Daily silver price per tola in Pakistan, {fd(fdt)} to {fd(ld)}</title>'
           f'<g stroke="currentColor" stroke-opacity=".12" font-size="11" fill="currentColor" fill-opacity=".6">{gr}</g>'
           f'<g font-size="11" fill="currentColor" fill-opacity=".6">{xl}</g>'
           f'<polyline points="{pts}" fill="none" stroke="#8a96a8" stroke-width="2.2" stroke-linejoin="round"/>'
           f'<circle cx="{x2(ti):.1f}" cy="{y2(top["t"]):.1f}" r="4" fill="#c9971f"/><text x="{x2(ti) - 8:.1f}" y="{y2(top["t"]) - 2:.1f}" text-anchor="end" font-size="11.5" fill="currentColor">Peak {rs(top["t"])}</text></svg>'
           f'<figcaption style="color:var(--muted);font-size:14px;margin-top:6px">Daily pure silver (999) price per tola in Pakistan, {fd(fdt)} to {fd(ld)}.</figcaption></figure>')

    y24, y25 = Y.get(2024), Y.get(2025)
    title = f"Silver Rate History in Pakistan: Chandi Tola Price 2024–{cy}"
    desc = (f"Silver rate history in Pakistan: chandi per tola, 10 gram and kg every day since March 2024. Year and month "
            f"tables, highs and lows, date lookup.")
    if len(desc) > 155:
        desc = "Silver rate history in Pakistan: daily chandi rate per tola, 10 gram and kg since March 2024, with month tables, highs, lows and a date lookup."
    h1 = f"Silver rate history in Pakistan: chandi price per tola, 2024–{cy}"
    faq = [
        ("What was the silver rate in Pakistan in 2024?",
         f"Pure (999) silver averaged about {rs(y24['t'])} per tola in 2024 (from March), between {rs(y24['lo']['t'])} and {rs(y24['hi']['t'])}." if y24 else ""),
        ("What was the silver rate in Pakistan in 2025?",
         f"The 2025 average was about {rs(y25['t'])} per tola; the low was {rs(y25['lo']['t'])} on {fdi(y25['lo']['d'])} and the high {rs(y25['hi']['t'])} on {fdi(y25['hi']['d'])}." if y25 else ""),
        ("What is the highest silver rate in Pakistan so far?",
         f"In our daily data the highest reference was {rs(top['t'])} per tola on {fdi(top['d'])}, when silver was about ${top['xag']:,.2f} an ounce."
         + (f" It then fell to {rs(low_after['t'])} by {fdi(low_after['d'])}." if low_after else "")),
        ("What is the silver rate per tola today?",
         f"On {fd(ld)} pure silver was {rs(cur)} per tola, {rs(last['g10'])} per 10 gram and {rs(last['kg'])} per kg. For the live rate see the silver rate in Pakistan page."),
        ("What was the value of 52.5 tola silver (nisab) in past years?",
         "At the yearly average rate: " + ", ".join(f"{y}: about {rs(Y[y]['t'] * NISAB)}" for y in yrs)
         + ". This is only the rupee value of 52.5 tola at the market rate; ask a scholar about zakat rules."),
        ("How is the silver rate per tola calculated?",
         "Price per tola = silver price in US dollars per ounce × USD/PKR ÷ 31.1035 × 11.6638. 10 gram = tola ÷ 11.6638 × 10; 1 kg = tola ÷ 11.6638 × 1,000. Sarafa rates add a local premium."),
        ("Why does silver move more than gold?",
         f"Silver is a smaller market and half of it goes into industry (solar panels, electronics), so both buying waves and sell-offs are sharper. Since {fd(fdt)} silver changed {ch_first:+.0f}% in rupees per tola."),
        ("Pakistan mein chandi ka rate 2024 se ab tak kitna badla?",
         f"March 2024 mein 1 tola chandi taqreeban {rs(first['t'])} ki thi, sab se zyada {rs(top['t'])} ({fdi(top['d'])}) gayi, aur {fd(ld)} ko {rs(cur)} thi."),
    ]
    faq = [(q, a) for q, a in faq if a]
    faq_h = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faq)
    dj = json.dumps([[r["d"], round(r["t"])] for r in days], separators=(",", ":"))

    body = hx.CSS + hx.YR_CSS + f'''<div class="qa"><b class="k">Quick answer</b><p>One tola of pure (999) silver in Pakistan was about <b>{rs(first['t'])}</b> on {fd(fdt)}{f", averaged <b>{rs(y24['t'])}</b> in 2024" if y24 else ""}{f" and <b>{rs(y25['t'])}</b> in 2025" if y25 else ""}, reached a high of <b>{rs(top['t'])}</b> on {fdi(top['d'])} and was <b>{rs(cur)}</b> on {fd(ld)} ({rs(last['g10'])} per 10 gram, {rs(last['kg'])} per kg). Daily rates, month tables and a date lookup are below.</p></div>
<h2 id="lookup">Silver rate on any date</h2>
<div class="gr-calc" style="border:1px solid var(--line);border-radius:14px;padding:16px;background:var(--surface)"><label for="shD" style="font-weight:600">Pick a date</label>
<input type="date" id="shD" min="{first['d']}" max="{last['d']}" value="{last['d']}" style="display:block;margin:8px 0;padding:10px;border:1px solid var(--line);border-radius:10px;font-size:16px;background:var(--bg);color:var(--ink)">
<div id="shR" aria-live="polite" style="font-size:17px;line-height:1.7;margin:6px 0 0">Tola: <b>{rs(cur)}</b> · 10 gram: <b>{rs(last['g10'])}</b> · 1 kg: <b>{rs(last['kg'])}</b> ({fd(ld)})</div>
<p style="font-size:13.5px;color:var(--muted);margin:6px 0 0">Daily rates from {fd(fdt)}. On a weekend or holiday the nearest earlier rate is shown.</p></div>
<h2 id="price-chart">Silver price per tola since {fdt.year}</h2>
<p>Silver went from about <b>{rs(first['t'])}</b> a tola in {MON[fdt.month - 1]} {fdt.year} to a peak of <b>{rs(top['t'])}</b> on {fdi(top['d'])}, and was <b>{rs(cur)}</b> on {fd(ld)}. The rupee rate follows two numbers: the world silver price in dollars and the <a href="usd-to-pkr-history.html">dollar rate</a>.</p>
{svg}
<h2 id="years">Silver rate in Pakistan year-wise and month-wise</h2>
<p>Average, lowest and highest price per tola for each year, with the rupee value of 52.5 tola (the silver nisab weight). Change is against the year before.</p>
<p class="yr-hint"><b>Click any year</b> to open its month-by-month rates right below it; click again to close.</p>
{yt}
<h2 id="daily">Daily silver rate in Pakistan</h2>
<p>Every weekday from {fd(fdt)}. Pick a month (or use ‹ ›).</p>
{dd}
<h2 id="moments">Key moments for silver since {fdt.year}</h2>
<ul><li><b>{fdi(low['d'])}:</b> the lowest rate in our data, <b>{rs(low['t'])}</b> per tola (silver about ${low['xag']:,.2f} an ounce).</li>
<li><b>2025:</b> silver broke out with gold; the yearly average rose to {rs(y25['t']) if y25 else "–"} a tola.</li>
<li><b>{fdi(top['d'])}:</b> the record so far, <b>{rs(top['t'])}</b> per tola (about ${top['xag']:,.2f} an ounce).</li>
{f"<li><b>{fdi(low_after['d'])}:</b> after the peak it fell to <b>{rs(low_after['t'])}</b>, a drop of {(1 - low_after['t'] / top['t']) * 100:.0f}%: silver falls as fast as it rises.</li>" if low_after else ""}
<li><b>{fd(ld)}:</b> <b>{rs(cur)}</b> per tola{f", {(1 - cur / top['t']) * 100:.0f}% below the peak" if cur < top['t'] else ""}; one ounce of gold buys about <b>{ratio:.0f} ounces</b> of silver (the gold/silver ratio).</li></ul>
<h2 id="why">Why silver moves faster than gold</h2>
<p>Silver is priced the same way as gold, from the world price in dollars and the rupee rate, but the market is much smaller and about half of the metal is used by industry (solar panels, electronics, batteries). So news about the economy, interest rates and factory demand moves it harder in both directions. Compare it with the <a href="gold-rate-history-pakistan.html">gold rate history since 1947</a>, and see today's <a href="silver-rate-pakistan.html">silver rate in Pakistan</a> for the live price and zakat nisab.</p>
<div class="khulasa"><h2>Khulasa (Roman Urdu / Hindi)</h2><ul>
<li>March 2024 mein 1 tola chandi taqreeban {rs(first['t'])} ki thi.</li>
<li>Sab se zyada rate {rs(top['t'])} fi tola {fdi(top['d'])} ko tha.</li>
<li>Aaj ({fd(ld)}) chandi {rs(cur)} fi tola, {rs(last['g10'])} fi 10 gram aur {rs(last['kg'])} fi kg hai.</li>
<li>Chandi sone se zyada tezi se upar neeche hoti hai.</li>
<li>Kisi bhi tareekh ka rate upar wale date box se dekhein; saal par click karein to us ke mahine khul jaate hain.</li></ul></div>
<section class="gr-ur" lang="ur" dir="rtl" style="font-family:var(--f-ur);line-height:2.1;margin:18px 0"><h2>پاکستان میں چاندی کے ریٹ کی تاریخ</h2><p>مارچ 2024 میں ایک تولہ چاندی تقریباً {first['t']:,.0f} روپے کی تھی۔ سب سے زیادہ ریٹ {top['t']:,.0f} روپے فی تولہ رہا، اور آج {ld.day} {UR_MON[ld.month - 1]} {ld.year} کو خالص چاندی {cur:,.0f} روپے فی تولہ ہے۔ یہ ریٹ انٹرنیشنل قیمت اور ڈالر ریٹ سے نکالے گئے ہیں، صرافہ بازار کا ریٹ تھوڑا مختلف ہوتا ہے۔</p></section>
<div class="ls-faq"><h2>Questions</h2>{faq_h}</div>
<h2>Sources and method</h2>
<p style="font-size:14.5px">Daily silver price in US dollars per ounce from March 2024: reference rates from an open currency data service (one isolated bad day smoothed), and from 21 November 2026 the prices on our <a href="silver-rate-pakistan.html">live silver rate page</a>. Dollar rate: daily rates as on our <a href="usd-to-pkr-history.html">USD to PKR history</a>. Formula: USD/oz × USD/PKR ÷ 31.1035 × 11.6638 = price per tola of pure (999) silver. These are market reference rates, not sarafa (APGJSA) rates. Updated {fd(now.date())}.</p>
<nav class="pn" aria-label="Rates"><a href="silver-rate-pakistan.html"><small>‹ Live</small><b>Silver rate in Pakistan today</b></a><a class="nx" href="gold-rate-history-pakistan.html"><small>Next ›</small><b>Gold rate history</b></a></nav>
<p class="ls-disc">For information only; not an offer to buy or sell silver, and not financial advice. Silver prices can fall as well as rise.</p>
''' + hx.JS + hx.YR_JS + f'''<script type="application/json" id="shData">{dj}</script>
<script>(function(){{try{{var D=JSON.parse(document.getElementById('shData').textContent),m={{}};D.forEach(function(r){{m[r[0]]=r[1]}});var i=document.getElementById('shD'),o=document.getElementById('shR');function f(n){{return 'Rs '+Math.round(n).toLocaleString('en-US')}}function out(v,t){{o.innerHTML='Tola: <b>'+f(v)+'</b> · 10 gram: <b>'+f(v/11.6638*10)+'</b> · 1 kg: <b>'+f(v/11.6638*1000)+'</b> ('+t+')'}}function key(d){{return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2)}}function show(){{var v=i.value;if(!v)return;var d=new Date(v+'T00:00:00'),t=d.toLocaleDateString('en-GB',{{day:'numeric',month:'long',year:'numeric'}});if(m[v]){{out(m[v],t);return}}var k=v;for(var j=0;j<6&&!m[k];j++){{d.setDate(d.getDate()-1);k=key(d)}}if(m[k])out(m[k],'nearest earlier rate, '+k);else o.textContent='No data for this date (daily data starts {first['d']}).'}}i.addEventListener('change',show);}}catch(e){{}}}})();</script>'''

    T = open(os.path.join(ROOT, "guide-ict-silver-bullet-time-in-pakistan.html"), encoding="utf-8").read()
    s = T
    a = s.index('<div class="wrap ls-body">'); b = s.index('<aside class="ls-side">')
    s = s[:a] + '<div class="wrap ls-body">\n  <article class="ls-art">\n' + body + '\n  </article>\n  ' + s[b:]
    hs = s.index('<section class="ls-hero">'); he = s.index('</section>', hs) + len('</section>')
    hero = (f'<section class="ls-hero"><div class="wrap gh-grid"><div class="gh-txt">\n'
            f'  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a>›<a href="silver-rate-pakistan.html">Silver Rate</a>›<span>Silver rate history</span></nav>\n'
            f'  <div class="ls-meta">Rates · history {fdt.year}–{cy}</div>\n  <h1>{E(h1)}</h1>\n'
            f'  <p class="ur" lang="ur" style="font-family:var(--f-ur);font-size:20px;line-height:2.1;margin:4px 0">پاکستان میں چاندی کے ریٹ کی تاریخ: ہر دن، ہر مہینہ</p>\n'
            f'  <p class="ls-lead">What a tola, 10 grams and a kilo of pure silver cost in Pakistan on every weekday since {fd(fdt)}, with month-by-month tables, highs and lows, nisab values and a date lookup.</p>\n'
            f'  <div class="byline"><img src="logo-128.webp" alt="Qazi Forex Tips" width="46" height="46"><div>By the <b>Qazi Forex Tips</b> team, led by <a href="about.html"><b>Dr. Qazi Abdul Basit</b></a>, Ph.D<br>Updated {fd(now.date())}</div></div>\n</div>\n'
            f'  <figure class="gh-art"><img src="{HERO}.webp" srcset="{HERO}-800.webp 800w, {HERO}.webp 1600w" sizes="(min-width:1000px) 560px, 100vw" width="1600" height="1280" '
            f'alt="Silver rate history in Pakistan: 3D silver bars showing the chandi price per tola from {fdt.year} to {cy}" fetchpriority="high" decoding="async"></figure>\n</div></section>')
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
                    "caption": f"Silver rate history in Pakistan, {fdt.year}–{cy}"}],
         "datePublished": "2026-11-22T00:00:00+05:00", "dateModified": now.strftime("%Y-%m-%dT%H:%M:%S+05:00"), "inLanguage": "en",
         "keywords": "silver rate history in pakistan, chandi rate history, silver price history pakistan, silver rate in 2024 pakistan, silver rate in 2025 pakistan, chandi ka rate",
         "author": {"@type": "Organization", "@id": "https://qaziforextips.com/#org", "name": "Qazi Forex Tips", "url": "https://qaziforextips.com/"},
         "publisher": {"@type": "Organization", "@id": "https://qaziforextips.com/#org", "name": "Qazi Forex Tips", "logo": {"@type": "ImageObject", "url": "https://qaziforextips.com/logo.png"}}},
        {"@type": "Dataset", "name": f"Silver price history in Pakistan ({fdt.year}–{cy})",
         "description": f"Daily pure silver price per tola, 10 gram and kg in Pakistani rupees from {first['d']}.",
         "url": URL, "temporalCoverage": first["d"] + "/" + last["d"], "creator": {"@type": "Organization", "name": "Qazi Forex Tips", "url": "https://qaziforextips.com/"},
         "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": "https://qaziforextips.com/data/metals-daily.json"}],
         "license": "https://qaziforextips.com/terms.html"},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://qaziforextips.com/"},
                                                        {"@type": "ListItem", "position": 2, "name": "Silver Rate in Pakistan", "item": "https://qaziforextips.com/silver-rate-pakistan.html"},
                                                        {"@type": "ListItem", "position": 3, "name": "Silver rate history", "item": URL}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda mm: '<script type="application/ld+json">' + json.dumps(ldj, ensure_ascii=False) + '</script>', s, count=1, flags=re.S)
    path = os.path.join(ROOT, SLUG)
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    norm = lambda t: re.sub(r"Updated \d+ \w+ \d{4}|\"dateModified\": \"[^\"]*\"", "", t)
    if norm(old) != norm(s):
        open(path, "w", encoding="utf-8").write(s)
        print("silver history page written:", len(days), "days, title", len(title), "desc", len(desc))
    else:
        print("silver history page unchanged")


if __name__ == "__main__":
    main()
