#!/usr/bin/env python3
"""Live Gold / Silver / USD-PKR / BTC rates for qaziforextips.com.

Runs every 30 minutes from .github/workflows/rates.yml. It:
  1. fetches the rates (Twelve Data when the TWELVEDATA_KEY secret is set, free keyless sources otherwise),
  2. writes data/rates.json (read by the home-page chart and boxes) and data/gold-history.json,
  3. writes the numbers straight into gold-rate-pakistan.html and index.html, so Google reads them
     without running JavaScript, and refreshes the page date in sitemap.xml.
If every source fails it changes nothing, so the site never shows empty or wrong numbers.
Only the Python standard library is used.
"""
import datetime as dt
import html
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
KEY = os.environ.get("TWELVEDATA_KEY", "").strip()
UA = "QFT-rates/1.0 (+https://qaziforextips.com)"
OZ = 31.1034768            # grams in a troy ounce
TOLA = 11.6638038          # grams in a tola
KARATS = [("24K", 24), ("22K", 22), ("21K", 21), ("18K", 18)]
PKT = dt.timezone(dt.timedelta(hours=5))
PAGE = "gold-rate-pakistan.html"
URL = "https://qaziforextips.com/" + PAGE


# ------------------------------------------------------------------ fetching
def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def td(path):
    j = get("https://api.twelvedata.com/" + path + "&apikey=" + KEY)
    if isinstance(j, dict) and j.get("status") == "error":
        raise RuntimeError(j.get("message", "Twelve Data error"))
    return j


def currency_api():
    for u in ("https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.min.json",
              "https://latest.currency-api.pages.dev/v1/currencies/usd.min.json"):
        try:
            return get(u)["usd"]
        except Exception as e:
            print("currency-api:", u, e)
    return None


def ok(v, lo, hi):
    return isinstance(v, (int, float)) and lo < v < hi


def fetch(old):
    out, src = {}, []
    # Gold + USD/PKR + 15-minute candles
    if KEY:
        try:
            qx = td("quote?symbol=XAU/USD")
            qp = td("quote?symbol=USD/PKR")
            ts = td("time_series?symbol=XAU/USD&interval=15min&outputsize=64&timezone=UTC")
            out["gold"], out["gold_prev"] = float(qx["close"]), float(qx["previous_close"])
            out["pkr"], out["pkr_prev"] = float(qp["close"]), float(qp["previous_close"])
            out["market_open"] = bool(qx.get("is_market_open"))
            out["candles"] = [[int(dt.datetime.strptime(v["datetime"], "%Y-%m-%d %H:%M:%S")
                                   .replace(tzinfo=dt.timezone.utc).timestamp()),
                               round(float(v["open"]), 2), round(float(v["high"]), 2),
                               round(float(v["low"]), 2), round(float(v["close"]), 2)]
                              for v in reversed(ts.get("values", []))]
            out["candle_symbol"] = "XAUUSD"
            src.append("Twelve Data (XAU/USD, USD/PKR)")
        except Exception as e:
            print("Twelve Data failed, using free sources:", e)
            out = {}
    cur = currency_api()
    if not out.get("candles"):
        try:   # PAXG is a token backed 1:1 by a troy ounce of gold; its price follows spot gold closely
            k = get("https://data-api.binance.vision/api/v3/klines?symbol=PAXGUSDT&interval=15m&limit=64")
            out["candles"] = [[int(r[0] // 1000), round(float(r[1]), 2), round(float(r[2]), 2),
                               round(float(r[3]), 2), round(float(r[4]), 2)] for r in k]
            out["candle_symbol"] = "PAXGUSDT"
        except Exception as e:
            print("candles fallback failed:", e)
    if "gold" not in out and cur and cur.get("xau") and cur.get("pkr"):
        # Without the Twelve Data key: the live gold price comes from the last PAXG candle when there is
        # one (it updates every minute), otherwise from Currency-API, which updates only once a day.
        live = out["candles"][-1][4] if out.get("candle_symbol") == "PAXGUSDT" and out.get("candles") else None
        out["gold"] = live or 1 / cur["xau"]
        out["pkr"] = cur["pkr"]
        today = dt.datetime.now(PKT).strftime("%Y-%m-%d")
        prev = [h for h in old.get("history", []) if h["d"] < today]
        out["gold_prev"] = prev[-1]["usd"] if prev else out["gold"]
        out["pkr_prev"] = prev[-1]["pkr"] if prev else out["pkr"]
        src.append("Binance PAXG/USDT (live gold)" if live else "Currency-API (daily reference)")
        src.append("Currency-API (USD/PKR, daily)")
    # Silver (daily reference)
    if cur and cur.get("xag"):
        out["silver"] = 1 / cur["xag"]
    # Bitcoin
    try:
        c = get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,pkr&include_24hr_change=true")["bitcoin"]
        out["btc"], out["btc_pkr"], out["btc_chg"] = c["usd"], c["pkr"], c.get("usd_24h_change")
        src.append("CoinGecko (BTC)")
    except Exception as e:
        print("CoinGecko failed:", e)
        try:
            t = get("https://data-api.binance.vision/api/v3/ticker/24hr?symbol=BTCUSDT")
            out["btc"], out["btc_chg"] = float(t["lastPrice"]), float(t["priceChangePercent"])
            if out.get("pkr"):
                out["btc_pkr"] = out["btc"] * out["pkr"]
        except Exception as e2:
            print("Binance BTC failed:", e2)
    out["sources"] = src
    return out


# ------------------------------------------------------------------ numbers
def per_gram_pkr(usd_oz, pkr):
    return usd_oz * pkr / OZ


def rs(v):
    return "Rs " + f"{round(v):,}"


def crore(v):
    return "Rs " + f"{v / 1e7:.2f}" + " Cr"


def pct(v):
    if v is None:
        return ""
    return ("▲ " if v >= 0 else "▼ ") + f"{abs(v):.2f}%"


def build(raw, old):
    now = dt.datetime.now(dt.timezone.utc)
    g, p = raw["gold"], raw["pkr"]
    gp, pp = raw.get("gold_prev") or g, raw.get("pkr_prev") or p
    pg, pg_prev = per_gram_pkr(g, p), per_gram_pkr(gp, pp)
    rows = {}
    for name, k in KARATS:
        f = k / 24
        rows[name] = {"tola": round(pg * f * TOLA), "g10": round(pg * f * 10), "g1": round(pg * f),
                      "oz": round(pg * f * OZ)}
    t24, t24_prev = pg * TOLA, pg_prev * TOLA
    r = {
        "updated": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "updated_pkt": now.astimezone(PKT).strftime("%d %b %Y, %H:%M PKT"),
        "gold": {"usd_oz": round(g, 2), "usd_prev": round(gp, 2), "chg_pct": round((g / gp - 1) * 100, 2) if gp else 0,
                 "tola24_change": round(t24 - t24_prev), "karats": rows},
        "usdpkr": round(p, 2), "usdpkr_prev": round(pp, 2),
        "silver": None, "btc": None,
        "candles": raw.get("candles") or old.get("candles") or [],
        "candle_symbol": raw.get("candle_symbol") or old.get("candle_symbol", "XAUUSD"),
        "market_open": raw.get("market_open"),
        "sources": raw.get("sources", []),
    }
    if raw.get("silver"):
        sg = per_gram_pkr(raw["silver"], p)
        r["silver"] = {"usd_oz": round(raw["silver"], 2), "tola": round(sg * TOLA), "g10": round(sg * 10)}
    elif old.get("silver"):
        r["silver"] = old["silver"]
    if raw.get("btc"):
        r["btc"] = {"usd": round(raw["btc"]), "pkr": round(raw.get("btc_pkr") or raw["btc"] * p),
                    "chg24": round(raw["btc_chg"], 2) if raw.get("btc_chg") is not None else None}
    elif old.get("btc"):
        r["btc"] = old["btc"]
    return r


def update_history(r):
    path = os.path.join(ROOT, "data", "gold-history.json")
    try:
        hist = json.load(open(path, encoding="utf-8"))
    except Exception:
        hist = []
    today = dt.datetime.now(PKT)
    if today.weekday() < 5:            # gold does not trade on Saturday / Sunday
        d = today.strftime("%Y-%m-%d")
        row = {"d": d, "usd": r["gold"]["usd_oz"], "pkr": r["usdpkr"], "tola24": r["gold"]["karats"]["24K"]["tola"]}
        hist = [h for h in hist if h["d"] != d] + [row]
        hist.sort(key=lambda h: h["d"])
        hist = hist[-400:]
        json.dump(hist, open(path, "w", encoding="utf-8"), separators=(",", ":"))
    return hist


# ------------------------------------------------------------------ writing into the HTML
def put(s, name, inner):
    pat = re.compile(r"(<!--R:" + name + r"-->)(.*?)(<!--/R:" + name + r"-->)", re.S)
    if not pat.search(s):
        print("  marker missing:", name)
        return s
    return pat.sub(lambda m: m.group(1) + inner + m.group(3), s, count=1)


def esc(s):
    return html.escape(str(s), quote=True)


UR_MONTHS = ["جنوری", "فروری", "مارچ", "اپریل", "مئی", "جون", "جولائی", "اگست", "ستمبر", "اکتوبر", "نومبر", "دسمبر"]


def gold_page(r, hist):
    path = os.path.join(ROOT, PAGE)
    s = open(path, encoding="utf-8").read()
    now = dt.datetime.now(PKT)
    day = now.strftime("%-d %b %Y")          # 13 Nov 2026
    day_long = now.strftime("%-d %B %Y")     # 13 November 2026
    k = r["gold"]["karats"]
    t24, chg = k["24K"]["tola"], r["gold"]["tola24_change"]
    arrow = "up" if chg >= 0 else "down"
    sign = "+" if chg >= 0 else "−"

    title = f"Gold Rate in Pakistan Today {day} – 24K Tola Price"
    desc = (f"Gold rate in Pakistan today ({day}): 24K {rs(t24)} per tola, {rs(k['24K']['g10'])} per 10 gram. "
            f"22K, 21K, 18K rates, calculator and 30-day chart, updated every 30 minutes.")
    s = re.sub(r"<title>.*?</title>", "<title>" + esc(title) + "</title>", s, count=1, flags=re.S)
    for attr, val in (('name="description"', desc), ('property="og:title"', title),
                      ('property="og:description"', desc), ('name="twitter:title"', title),
                      ('name="twitter:description"', desc)):
        s = re.sub(r'(<meta ' + attr + r' content=")[^"]*(")', lambda m: m.group(1) + esc(val) + m.group(2), s, count=1)

    s = put(s, "date", esc(day_long))
    s = put(s, "time", esc(r["updated_pkt"]))
    s = put(s, "big", esc(rs(t24)))
    s = put(s, "chg", f'<span class="gr-chg {arrow}">{sign}{rs(abs(chg))[3:]} ({pct(r["gold"]["chg_pct"])}) vs previous close</span>')
    s = put(s, "mini",
            f'<div><i>10 gram (24K)</i><b>{rs(k["24K"]["g10"])}</b></div>'
            f'<div><i>1 gram (24K)</i><b>{rs(k["24K"]["g1"])}</b></div>'
            f'<div><i>Gold / ounce</i><b>${r["gold"]["usd_oz"]:,.2f}</b></div>'
            f'<div><i>USD / PKR</i><b>{r["usdpkr"]:.2f}</b></div>')
    body = "".join(
        f'<tr><th scope="row">{name} gold</th><td>{rs(v["tola"])}</td><td>{rs(v["g10"])}</td>'
        f'<td>{rs(v["g1"])}</td><td>{rs(v["oz"])}</td></tr>' for name, v in k.items())
    s = put(s, "table", body)
    s = put(s, "sent",
            f"The gold rate in Pakistan today, {esc(day_long)}, is <b>{rs(t24)} per tola</b> for 24K gold and "
            f"<b>{rs(k['22K']['tola'])} per tola</b> for 22K gold, based on the international price of "
            f"${r['gold']['usd_oz']:,.2f} per ounce and a dollar rate of {r['usdpkr']:.2f} rupees.")
    s = put(s, "ur",
            "آج " + f"{now.day} {UR_MONTHS[now.month - 1]} {now.year}" + " کو پاکستان میں 24 قیراط سونے کا ریٹ <b>" + f"{t24:,}" + " روپے فی تولہ</b> اور "
            "22 قیراط سونا <b>" + f"{k['22K']['tola']:,}" + " روپے فی تولہ</b> ہے۔")
    s = put(s, "ro",
            f"Aaj {esc(day_long)} ko Pakistan mein 24K sone ka rate <b>{rs(t24)} fi tola</b> aur 22K ka "
            f"<b>{rs(k['22K']['tola'])} fi tola</b> hai.")
    # last 7 trading days, newest first
    last = list(reversed(hist[-8:]))
    hrows = []
    for i, h in enumerate(last[:7]):
        nxt = last[i + 1] if i + 1 < len(last) else None
        d = dt.datetime.strptime(h["d"], "%Y-%m-%d").strftime("%a %-d %b")
        if nxt:
            c = h["tola24"] - nxt["tola24"]
            ctxt = f'<span class="{"up" if c >= 0 else "down"}">{"+" if c >= 0 else "−"}{abs(c):,}</span>'
        else:
            ctxt = "–"
        hrows.append(f'<tr><td>{d}</td><td>{rs(h["tola24"])}</td><td>${h["usd"]:,.2f}</td><td>{h["pkr"]:.2f}</td><td>{ctxt}</td></tr>')
    s = put(s, "hist", "".join(hrows))
    s = put(s, "json", esc(json.dumps({"tola24": t24, "g1": {n: v["g1"] for n, v in k.items()},
                                         "hist": [[h["d"], h["tola24"]] for h in hist[-60:]]}, separators=(",", ":"))))
    # structured data, written fresh each run
    faq = [
        ("What is the gold rate in Pakistan today?",
         f"On {day_long} the 24K gold rate in Pakistan is {rs(t24)} per tola and {rs(k['24K']['g10'])} per 10 grams, "
         f"based on the international price of ${r['gold']['usd_oz']:,.2f} per ounce and USD/PKR {r['usdpkr']:.2f}. "
         f"22K gold is {rs(k['22K']['tola'])} per tola."),
        ("How is the gold price per tola calculated?",
         "Gold price per tola = international gold price per ounce (USD) × USD/PKR rate ÷ 31.1035 × 11.6638. "
         "One troy ounce is 31.1035 grams and one tola is 11.6638 grams. For 22K multiply by 22/24, for 21K by 21/24 and for 18K by 18/24."),
        ("Why is the sarafa (jeweller) rate different from this rate?",
         "This page shows the rate from the international market and the live dollar rate. The rate announced by the "
         "sarafa associations in Pakistan is set by local dealers and can be a little higher or lower, and jewellers add "
         "making charges (mazdoori) and their margin on jewellery."),
        ("Is the gold rate the same in Karachi, Lahore and Islamabad?",
         "The base rate is the same across Pakistan because it follows the international price and the dollar rate. "
         "Small differences come from local dealer premiums, making charges and the buy/sell spread of each shop."),
        ("What is the difference between 24K, 22K and 21K gold?",
         "24K is 99.9% pure gold, mostly sold as bars and biscuits. 22K is about 91.7% gold and is the most common "
         "purity for jewellery in Pakistan. 21K is 87.5% gold and 18K is 75% gold."),
        ("How often is this gold rate updated?",
         "Every 30 minutes while the gold market is open, Monday to Friday. On Saturday and Sunday the international "
         "market is closed, so the last Friday price stays on the page."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": URL + "#page", "url": URL, "name": title, "description": desc,
         "inLanguage": "en", "datePublished": "2026-11-13", "dateModified": now.strftime("%Y-%m-%dT%H:%M:%S+05:00"),
         "isPartOf": {"@id": "https://qaziforextips.com/#site"},
         "publisher": {"@id": "https://qaziforextips.com/#org"},
         "about": {"@type": "Thing", "name": "Gold price in Pakistan"},
         "primaryImageOfPage": {"@type": "ImageObject", "url": "https://qaziforextips.com/og-image.jpg"}},
        {"@type": "FAQPage", "@id": URL + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://qaziforextips.com/"},
            {"@type": "ListItem", "position": 2, "name": "Forex Guide", "item": "https://qaziforextips.com/forex-guide.html"},
            {"@type": "ListItem", "position": 3, "name": "Gold Rate in Pakistan", "item": URL}]},
    ]}
    s = re.sub(r'(<script type="application/ld\+json" id="ld">).*?(</script>)',
               lambda m: m.group(1) + json.dumps(ld, ensure_ascii=False) + m.group(2), s, count=1, flags=re.S)
    s = put(s, "faq1", esc(faq[0][1]))
    return path, s


def home_page(r):
    path = os.path.join(ROOT, "index.html")
    s = open(path, encoding="utf-8").read()
    k = r["gold"]["karats"]["24K"]
    boxes = [f'<a class="lrate" href="gold-rate-pakistan.html"><i>Gold 24K / tola</i><b>{rs(k["tola"])}</b>'
             f'<span class="{"up" if r["gold"]["chg_pct"] >= 0 else "down"}">{pct(r["gold"]["chg_pct"])}</span></a>']
    sv = r.get("silver")
    boxes.append(f'<div class="lrate"><i>Silver / tola</i><b>{rs(sv["tola"]) if sv else "–"}</b>'
                 f'<span>${sv["usd_oz"]:,.2f}/oz</span></div>' if sv else
                 '<div class="lrate"><i>Silver / tola</i><b>–</b><span></span></div>')
    chg_p = (r["usdpkr"] / r["usdpkr_prev"] - 1) * 100 if r.get("usdpkr_prev") else None
    boxes.append(f'<div class="lrate"><i>USD / PKR</i><b>Rs {r["usdpkr"]:.2f}</b>'
                 f'<span class="{"up" if (chg_p or 0) >= 0 else "down"}">{pct(chg_p)}</span></div>')
    b = r.get("btc")
    boxes.append(f'<div class="lrate"><i>Bitcoin (PKR)</i><b>{crore(b["pkr"])}</b>'
                 f'<span class="{"up" if (b.get("chg24") or 0) >= 0 else "down"}">{pct(b.get("chg24"))}</span></div>' if b else
                 '<div class="lrate"><i>Bitcoin (PKR)</i><b>–</b><span></span></div>')
    s = put(s, "home", "".join(boxes))
    s = put(s, "hometime", esc(r["updated_pkt"]))
    return path, s


def sitemap():
    path = os.path.join(ROOT, "sitemap.xml")
    s = open(path, encoding="utf-8").read()
    today = dt.datetime.now(PKT).strftime("%Y-%m-%d")
    s2 = re.sub(r"(<loc>" + re.escape(URL) + r"</loc>\s*<lastmod>)[^<]*(</lastmod>)",
                lambda m: m.group(1) + today + m.group(2), s, count=1)
    return path, s2


def main():
    rates_path = os.path.join(ROOT, "data", "rates.json")
    try:
        old = json.load(open(rates_path, encoding="utf-8"))
        old_flat = {"gold": old.get("gold", {}), "usdpkr_prev": old.get("usdpkr"),
                    "silver": old.get("silver"), "btc": old.get("btc"),
                    "candles": old.get("candles"), "candle_symbol": old.get("candle_symbol")}
    except Exception:
        old, old_flat = {}, {}
    try:
        old_flat["history"] = json.load(open(os.path.join(ROOT, "data", "gold-history.json"), encoding="utf-8"))
    except Exception:
        old_flat["history"] = []
    seed = os.environ.get("QFT_SEED")          # local testing only: a JSON file with the raw numbers
    raw = json.load(open(seed, encoding="utf-8")) if seed else fetch(old_flat)
    if not (ok(raw.get("gold"), 500, 50000) and ok(raw.get("pkr"), 50, 2000)):
        print("No trustworthy gold / dollar rate this run. Nothing changed.")
        return 0
    r = build(raw, old_flat)
    os.makedirs(os.path.dirname(rates_path), exist_ok=True)
    json.dump(r, open(rates_path, "w", encoding="utf-8"), separators=(",", ":"))
    hist = update_history(r)
    for path, text in (gold_page(r, hist), home_page(r), sitemap()):
        open(path, "w", encoding="utf-8").write(text)
    print("Gold 24K tola:", r["gold"]["karats"]["24K"]["tola"], "| USD/PKR:", r["usdpkr"], "| sources:", r["sources"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
