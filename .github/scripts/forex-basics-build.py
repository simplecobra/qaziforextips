#!/usr/bin/env python3
"""Forex Basics: Zero to Hero (Urdu/Hindi) section of qaziforextips.com.

Reads data/forex-basics.json and builds:
  - forex-basics-course.html          the course hub (all modules, published lessons linked)
  - one lesson-*.html page per published lesson (video, notes, khulasa, FAQ, schema)
The page shell (head styles, header, footer, scripts) is copied from lesson-forex-trading-basics.html,
so the new pages always match the rest of the site. Comments from YouTube are added later
by .github/scripts/yt-comments.py (it looks for "    <h2>Related lessons</h2>").
Run: python3 .github/scripts/forex-basics-build.py
"""
import os, re, json, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = "https://qaziforextips.com/"
HUB = "forex-basics-course.html"
HUB_NAME = "Forex Basics: Zero to Hero"
D = json.load(open(os.path.join(ROOT, "data", "forex-basics.json"), encoding="utf-8"))
T = open(os.path.join(ROOT, "lesson-forex-trading-basics.html"), encoding="utf-8").read()
e = html.escape

MODULES = [
    ("Start Here", ["Start here: how to use this course", "How money is made and lost in forex (the $50-100 reality)", "Scams, signal groups and guaranteed profit", "Binary options are not forex", "Is forex halal or haram?"]),
    ("What is Forex", ["What is forex trading?", "How the forex market works", "Where does your trade go? (interbank, LP, OTC, CFD)", "Currencies and their codes", "Currency pairs: base and quote", "Major, minor and exotic pairs", "Gold and Silver (XAU/USD, XAG/USD)", "Forex vs stocks, crypto, indices and oil", "Buy and Sell explained", "Why forex is open 24/5"]),
    ("Trading Language and Maths", ["Bid, Ask and Spread", "Pip, point and pipette", "Gold pip, point and tick", "Lot size", "Pip value", "How to calculate profit and loss", "Account currency", "Commission", "Swap and triple swap", "Slippage, requotes and spread widening", "The total cost of a trade", "Risk:Reward introduction"]),
    ("Leverage and Margin", ["What is leverage?", "Margin, free margin and margin level", "Margin call and stop out", "Example: $1,000 at 1:500"]),
    ("Brokers and Accounts", ["What is a forex broker?", "Market maker, STP, ECN and A/B book", "Regulated broker checklist", "IB and affiliate links", "Account types", "How to open a demo account", "Real account and KYC", "Deposits and withdrawals in Pakistan and India", "Legal position in Pakistan and India", "Account security"]),
    ("MT4 and MT5", ["MT4 vs MT5: install and login", "MT5 platform tour", "Charts, chart types and timeframes", "Templates and profiles", "Symbol specification", "Market orders", "Pending orders", "Stop loss and take profit", "Trailing stop, breakeven and partial close", "Hedging vs netting accounts", "Indicators, EAs and alerts", "History and account statement", "MT5 on mobile", "TradingView basics"]),
    ("Reading a Chart", ["What is a price chart?", "Candlesticks: open, high, low, close", "Timeframes and multi-timeframe", "What is a trend?", "Higher highs, higher lows, lower highs, lower lows", "Support and resistance introduction", "Tick volume and volatility", "A 5-minute chart routine", "Trading styles"]),
    ("Market Timings", ["Market open, close and the weekend gap", "Sessions and overlaps", "Timings in PKT and IST (with DST)", "The best time to trade", "Holidays"]),
    ("Risk Management", ["What is risk management?", "Why a stop loss, and where", "Risk in % or in $", "Lot size from your stop loss", "Examples: $100, $500 and $1,000 accounts", "Risk:Reward in depth", "Win rate and expectancy", "Drawdown and recovery", "Daily and weekly loss limits", "Compounding", "Martingale and grid: the danger", "Keep trading money separate"]),
    ("Trading Psychology", ["What is trading psychology?", "Greed, fear and FOMO", "Revenge trading", "Overtrading", "Accepting losses", "Discipline and patience", "A long journey"]),
    ("Fundamentals", ["Three types of analysis", "The economic calendar", "Interest rates, the Fed and FOMC", "CPI (inflation)", "NFP", "GDP", "The dollar index (DXY)", "Gold and the dollar", "Risk-on, risk-off and correlation", "Why not to trade during news"]),
    ("From Demo to Real", ["Your trading plan", "Trading journal", "Backtesting (QFT Replay Simulator)", "Forward testing", "How to use a demo account", "When to move from demo to real", "Your first real account", "Your first trade from A to Z", "Myfxbook"]),
    ("Industry Truths", ["Fake profit screenshots", "Signal groups", "PAMM, MAM and copy trading", "Prop firm basics", "What to check before buying a prop firm challenge", "EA sellers"]),
    ("Wrap-up", ["20 beginner mistakes", "Forex glossary A to Z", "Next step: Price Action Basics"]),
]

def cut(s, a, b):
    i = s.index(a); j = s.index(b, i)
    return s[i:j]

# ---- shell parts from the template ----
HEAD_TOP = T[:T.index("<title>")]
HEAD_REST = T[T.index("</script>", T.index("application/ld+json")) + len("</script>"):T.index("<body")]
HEADER = cut(T, "<body", "<main")
FOOTER = T[T.index("</main>"):]
ASIDE_SIM = re.search(r'<div class="box"><h3>Practise this on real charts</h3>.*?</div>', T, re.S).group(0)
ASIDE_GUIDE = re.search(r'<div class="box"><h3>Read the guide</h3>.*?</div>', T, re.S).group(0)
ASIDE_WA = re.search(r'<div class="box"><h3>Questions\?</h3>.*?</div>', T, re.S).group(0)

def head(title, desc, url, image, extra_og, ld):
    return (HEAD_TOP + f"<title>{e(title)}</title>\n"
            f'<meta name="description" content="{e(desc)}">\n'
            f'<link rel="canonical" href="{url}">\n'
            '<meta name="robots" content="index, follow, max-image-preview:large, max-video-preview:-1">\n'
            '<meta name="author" content="Dr. Qazi Abdul Basit">\n<meta name="theme-color" content="#0d1220">\n'
            + extra_og +
            '<meta property="og:site_name" content="Qazi Forex Tips">\n'
            f'<meta property="og:title" content="{e(title)}">\n<meta property="og:description" content="{e(desc)}">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:image" content="{image}">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="{e(title)}">\n'
            f'<meta name="twitter:description" content="{e(desc)}">\n<meta name="twitter:image" content="{image}">\n'
            '<link rel="preconnect" href="https://www.youtube.com">\n<link rel="preconnect" href="https://i.ytimg.com">\n'
            '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'
            + HEAD_REST)

PERSON = {"@type": "Person", "@id": SITE + "#qazi", "name": "Dr. Qazi Abdul Basit", "url": SITE + "about.html",
          "jobTitle": "Forex and Gold trader, founder of Qazi Forex Tips"}
ORG = {"@type": "Organization", "@id": SITE + "#org", "name": "Qazi Forex Tips", "logo": {"@type": "ImageObject", "url": SITE + "logo.png"}}

def nice_date(d):
    x = datetime.date.fromisoformat(d)
    return f"{x.day} {x.strftime('%B %Y')}"

def secs(t):
    p = [int(v) for v in t.split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]

LESSONS = D["lessons"]

def lesson_page(i, L):
    url = SITE + L["slug"]; vid = L["vid"]
    img = f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"
    num = L["n"]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "VideoObject", "@id": url + "#video", "name": L["title"], "description": L["desc"],
         "thumbnailUrl": [img, f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"], "uploadDate": L["date"] + "T00:00:00+05:00",
         "duration": L["duration"], "embedUrl": f"https://www.youtube.com/embed/{vid}", "contentUrl": f"https://www.youtube.com/watch?v={vid}",
         "url": url, "inLanguage": "ur", "publisher": {"@id": SITE + "#org"}, "author": {"@id": SITE + "#qazi"},
         "hasPart": [{"@type": "Clip", "name": n, "startOffset": secs(t),
                      **({"endOffset": secs(L["chapters"][k + 1][0])} if k + 1 < len(L["chapters"]) else {"endOffset": secs(L["len"])}),
                      "url": f"https://www.youtube.com/watch?v={vid}&t={secs(t)}s"} for k, (t, n) in enumerate(L["chapters"])]},
        {"@type": "Article", "@id": url + "#article", "headline": L["h1"], "description": L["desc"], "url": url,
         "mainEntityOfPage": url, "image": img, "datePublished": L["date"] + "T00:00:00+05:00",
         "dateModified": L.get("modified", L["date"]) + "T00:00:00+05:00", "inLanguage": "en",
         "articleSection": HUB_NAME, "keywords": L["keywords"], "video": {"@id": url + "#video"},
         "isPartOf": {"@id": SITE + HUB + "#course"}, "author": PERSON, "publisher": ORG},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Courses", "item": SITE + "youtube.html"},
            {"@type": "ListItem", "position": 3, "name": HUB_NAME, "item": SITE + HUB},
            {"@type": "ListItem", "position": 4, "name": f"Lesson {num}: {L['short']}", "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in L["faq"]]}]}
    og = ('<meta property="og:type" content="video.other">\n'
          f'<meta property="og:video" content="https://www.youtube.com/embed/{vid}">\n')
    prev_l = LESSONS[i - 1] if i > 0 else None
    next_l = LESSONS[i + 1] if i + 1 < len(LESSONS) else None
    chap = "".join(f'<li><a href="https://www.youtube.com/watch?v={vid}&amp;t={secs(t)}s" target="_blank" rel="noopener">{t}</a> {e(n)}</li>' for t, n in L["chapters"])
    takes = "".join(f"<blockquote><p>{e(x)}</p><cite>From this lesson</cite></blockquote>" for x in L["takes"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in L["faq"])
    kh = "".join(f"<li>{e(x)}</li>" for x in L["khulasa"])
    side_list = "".join(f'<li><a href="{x["slug"]}"' + (' aria-current="page"' if x is L else "") + f'>Lesson {x["n"]}: {e(x["short"])}</a></li>' for x in LESSONS)
    pn = '<nav class="pn" aria-label="Lessons">'
    pn += (f'<a href="{prev_l["slug"]}"><small>‹ Previous lesson</small><b>{e(prev_l["short"])}</b></a>' if prev_l
           else f'<a href="{HUB}"><small>‹ Course page</small><b>{HUB_NAME}: all lessons</b></a>')
    pn += (f'<a class="nx" href="{next_l["slug"]}"><small>Next lesson ›</small><b>{e(next_l["short"])}</b></a>' if next_l
           else f'<a class="nx" href="{HUB}"><small>Next lesson ›</small><b>{e(L.get("next", "Coming soon: see the course page"))}</b></a>')
    pn += "</nav>"
    rel = ('<div class="rel"><a href="guide-forex-trading-in-pakistan-and-india.html"><small>Guide</small><span>Forex trading in Pakistan and India: rules, brokers, scams, Gold and hours</span></a>'
           '<a href="lesson-forex-trading-basics.html"><small>Price Action Basics</small><img src="https://i.ytimg.com/vi/9JfvsIfslCg/mqdefault.jpg" alt="" loading="lazy" width="320" height="180"><span>Forex trading for beginners: risk, demo or real account, and your broker</span></a>'
           '<a href="lesson-forex-myths.html"><small>Price Action Basics</small><img src="https://i.ytimg.com/vi/UnSphPChym8/mqdefault.jpg" alt="" loading="lazy" width="320" height="180"><span>Forex trading myths vs reality</span></a></div>')
    body = (f'''<main id="top">
<section class="ls-hero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a>›<a href="youtube.html">Courses</a>›<a href="{HUB}">{HUB_NAME}</a>›<span>Lesson {num}</span></nav>
  <div class="ls-meta">{HUB_NAME} · Module {L["module"]} · Lesson {num} · {L["len"]} video · Urdu / Hindi</div>
  <h1>{e(L["h1"])}</h1>
  <p class="ls-lead">{e(L["lead"])}</p>
  <div class="byline"><img src="dr-qazi-120.webp" alt="Dr. Qazi Abdul Basit" width="46" height="46"><div>Video lesson by <a href="about.html"><b>Dr. Qazi Abdul Basit</b></a>, Ph.D · Forex &amp; Gold trader since 2013<br>Notes by the Qazi Forex Tips team · Updated {nice_date(L.get("modified", L["date"]))}</div></div>
  <div class="ls-video"><iframe src="https://www.youtube.com/embed/{vid}?rel=0" title="{e(L["h1"])} – video lesson" loading="eager" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
  <div class="ls-vbar"><span>Watch in Urdu / Hindi · {L["len"]}</span><span>·</span><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener" style="color:var(--ink)">Open on YouTube</a></div>
</div></section>

<div class="wrap ls-body">
  <article class="ls-art">
    <div class="covers"><h2>In this lesson</h2><ul>{"".join(f"<li>{e(c)}</li>" for c in L["covers"])}</ul></div>
    <div class="take"><div class="th"><img src="dr-qazi-120.webp" alt="Dr. Qazi Abdul Basit" width="48" height="48" loading="lazy"><div><b>Dr. Qazi's take</b><span>In his own words, from this lesson</span></div></div>{takes}</div>
    <h2>Video chapters</h2><ul>{chap}</ul>
    <h2>Lesson notes</h2>
    {L["notes"]}
    <div class="urdu"><h2>Khulasa (Roman Urdu / Hindi)</h2><ul>{kh}</ul></div>
    <div class="ls-faq"><h2>Questions</h2>{faq}</div>
    <h2>Related lessons</h2>
    {rel}
    {pn}
    <p class="ls-disc">Education only, not financial advice. Trading forex, Gold and CFDs carries a high risk of loss. Examples are for learning; check the rules of your country and practise on a demo account before using real money.</p>
  </article>
  <aside class="ls-side">
    <div class="box"><h3>{HUB_NAME}</h3><p>A free beginner course in Urdu/Hindi, from zero. New lessons every day.</p><ol>{side_list}</ol><a class="btn gold" href="{HUB}">All lessons and the full syllabus</a></div>
    {ASIDE_SIM}
    {ASIDE_GUIDE}
    {ASIDE_WA}
  </aside>
</div>
''')
    title = L["seo_title"] + " | Lesson " + num
    return head(title, L["desc"], url, img, og, ld) + HEADER + body + FOOTER

def hub_page():
    url = SITE + HUB
    first = LESSONS[0]
    img = f"https://i.ytimg.com/vi/{first['vid']}/maxresdefault.jpg"
    title = "Free Forex Course for Beginners in Urdu/Hindi: Zero to Hero"
    desc = (f"Free forex trading course for beginners in Urdu/Hindi: {sum(len(m[1]) for m in MODULES)} short video lessons, "
            "from what forex is to pips, lots, leverage, MT5 and risk management.")
    pub = {x["short"].split("?")[0].lower(): x for x in LESSONS}
    by_mod = {}
    for x in LESSONS: by_mod.setdefault(x["module"], []).append(x)
    total = sum(len(m[1]) for m in MODULES)
    mods = ""
    for mi, (mname, topics) in enumerate(MODULES):
        done = by_mod.get(mi, [])
        cards = "".join(f'<a class="lnc" href="{x["slug"]}"><img src="https://i.ytimg.com/vi/{x["vid"]}/mqdefault.jpg" alt="" loading="lazy" width="320" height="180"><span><b>Lesson {x["n"]}: {e(x["short"])}</b><small>{x["len"]} video + notes</small></span></a>' for x in done)
        rest = topics[len(done):]
        soon = "".join(f"<li>{e(t)}</li>" for t in rest)
        mods += (f'<div class="fbm" id="module-{mi}"><h3><span>Module {mi}</span> {e(mname)}</h3>'
                 + (f'<div class="lngrid">{cards}</div>' if cards else "")
                 + (f'<details{" open" if mi == 0 or (cards and mi == max(by_mod)) else ""}><summary>{"Coming next" if cards else "Lessons in this module"} ({len(rest)})</summary><ol start="{len(done) + 1}">{soon}</ol></details>' if rest else "")
                 + "</div>")
    css = ('<style>.fbm{border:1px solid var(--line);border-radius:16px;background:var(--surface);padding:20px 22px;margin:0 0 16px}'
           '.fbm h3{margin:0 0 12px;font-size:22px}.fbm h3 span{display:inline-block;font:600 12px/1 var(--f-mono);letter-spacing:.8px;text-transform:uppercase;'
           'color:var(--gold,#e9b949);border:1px solid var(--line);border-radius:999px;padding:6px 10px;margin-right:8px;vertical-align:middle}'
           '.fbm details summary{cursor:pointer;color:var(--muted);font-size:15px;margin-top:6px}.ls-art .fbm ol{margin:10px 0 0;padding-left:22px;color:var(--muted);columns:2;column-gap:28px}'
           '.ls-art .fbm ol li{break-inside:avoid;margin:0 0 4px;font-size:16px;line-height:1.45}.lngrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px;margin-bottom:6px}'
           '.lnc{display:grid;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:var(--bg);color:var(--ink);text-decoration:none}'
           '.lnc img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}.lnc span{padding:10px 12px;display:grid;gap:4px}.lnc small{color:var(--muted)}'
           '.fbsteps{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:18px 0 26px}.fbsteps div{border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:var(--surface)}'
           '.fbsteps b{display:block;margin-bottom:4px}@media (max-width:640px){.ls-art .fbm ol{columns:1}}</style>')
    items = [{"@type": "ListItem", "position": k + 1, "url": SITE + x["slug"], "name": f"Lesson {x['n']}: {x['short']}"} for k, x in enumerate(LESSONS)]
    faq = [["Is this forex course really free?", "Yes. Every lesson is free on YouTube with free written notes on this website. There is no paid upgrade inside the course."],
           ["Which language is the course in?", "The videos are in simple Urdu/Hindi with English trading words (pip, lot, spread), and every video has English subtitles. The notes are in English with a Roman Urdu / Hindi summary."],
           ["I know nothing about trading. Where do I start?", "Start with Lesson 1, What is forex trading?, and watch the lessons in order. Each lesson is 5 to 15 minutes and ends with a 10-minute practical task."],
           ["Will this course teach me to make money quickly?", "No. Nobody can promise profit. The course teaches how the market works, how to manage risk and how to practise on a demo account first, so you can decide for yourself."],
           ["What comes after Forex Basics?", "After the basics, continue with the free Price Action Mastery course (Basic, then Advanced) and the strategy lessons on the Courses page."]]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Course", "@id": url + "#course", "name": f"{HUB_NAME} – Free Forex Course for Beginners (Urdu/Hindi)", "description": desc, "url": url,
         "inLanguage": ["ur", "hi"], "isAccessibleForFree": True, "educationalLevel": "Beginner", "image": img,
         "provider": ORG, "author": PERSON, "teaches": "Forex trading basics, pips, lots, leverage, margin, MT5, risk management, trading psychology",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "category": "Free"},
         "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Online", "courseWorkload": "PT20H", "instructor": PERSON}},
        {"@type": "ItemList", "@id": url + "#lessons", "name": f"{HUB_NAME} lessons", "itemListElement": items},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Courses", "item": SITE + "youtube.html"},
            {"@type": "ListItem", "position": 3, "name": HUB_NAME, "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    og = '<meta property="og:type" content="website">\n'
    pl = D.get("playlist") or ""
    pl_btn = (f'<a href="https://www.youtube.com/playlist?list={pl}" target="_blank" rel="noopener" style="color:var(--ink)">Open the playlist on YouTube</a>'
              if pl else '<a href="https://www.youtube.com/@QaziForexTips" target="_blank" rel="noopener" style="color:var(--ink)">Watch on YouTube @QaziForexTips</a>')
    faqh = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)
    body = (f'''<main id="top">
<section class="ls-hero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a>›<a href="youtube.html">Courses</a>›<span>{HUB_NAME}</span></nav>
  <div class="ls-meta">Free course · {total} lessons · {len(LESSONS)} published · Urdu / Hindi · English subtitles</div>
  <h1>Forex Basics: Zero to Hero – free forex course for beginners in Urdu/Hindi</h1>
  <p class="ls-lead">Never traded before? Start here. Short lessons of 5 to 15 minutes take you step by step from "what is forex?" to pips, lots, leverage, MT5, risk management and your first trade on a demo account. Each lesson has a video, written notes, a Roman Urdu summary and a 10-minute practical task. New lessons are added every day.</p>
  <div class="byline"><img src="dr-qazi-120.webp" alt="Dr. Qazi Abdul Basit" width="46" height="46"><div>Course by <a href="about.html"><b>Dr. Qazi Abdul Basit</b></a>, Ph.D · Forex &amp; Gold trader since 2013<br>Updated {nice_date(max(x.get("modified", x["date"]) for x in LESSONS))}</div></div>
  <div class="ls-vbar"><a class="btn gold" href="{first["slug"]}">Start with Lesson 1</a><span>·</span>{pl_btn}</div>
</div></section>

<div class="wrap ls-body">
  <article class="ls-art">
    {css}
    <h2>How this course works</h2>
    <div class="fbsteps"><div><b>1. Watch in order</b>Each lesson builds on the one before. Begin with Module 0 and Lesson 1.</div><div><b>2. Read the notes</b>Every lesson page has notes, examples, chapters and a Roman Urdu khulasa.</div><div><b>3. Do the task</b>A 10-minute practical task after every lesson, on paper or on a demo account.</div><div><b>4. Then Price Action</b>After the basics, move on to the free Price Action Mastery course.</div></div>
    <h2>Course syllabus</h2>
    {mods}
    <div class="ls-faq"><h2>Questions</h2>{faqh}</div>
    <h2>After the basics</h2>
    <p>Finished the basics? Continue with <a href="course-price-action-basic.html">Price Action Mastery – Basic</a>, then <a href="course-price-action-advanced.html">Advanced</a> and the <a href="course-trading-strategies.html">trading strategies</a>. The <a href="forex-roadmap.html">forex learning roadmap</a> shows the whole path, and the <a href="forex-guide.html">Forex Guide</a> explains every term in writing.</p>
    <p class="ls-disc">Education only, not financial advice. Trading forex, Gold and CFDs carries a high risk of loss. Check the rules of your country and practise on a demo account before using real money.</p>
  </article>
  <aside class="ls-side">
    <div class="box"><h3>Start here</h3><p>Lesson 1: {e(first["short"])} ({first["len"]}).</p><a class="btn gold" href="{first["slug"]}">Watch Lesson 1</a></div>
    {ASIDE_SIM}
    {ASIDE_GUIDE}
    {ASIDE_WA}
  </aside>
</div>
''')
    return head(title, desc, url, img, og, ld) + HEADER + body + FOOTER

def main():
    for i, L in enumerate(LESSONS):
        open(os.path.join(ROOT, L["slug"]), "w", encoding="utf-8").write(lesson_page(i, L))
        print("wrote", L["slug"])
    open(os.path.join(ROOT, HUB), "w", encoding="utf-8").write(hub_page())
    print("wrote", HUB)

if __name__ == "__main__":
    main()
