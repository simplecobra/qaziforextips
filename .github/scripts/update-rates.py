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
    # Silver: gold-api.com is live and keyless; Currency-API (once a day) is the fallback
    try:
        out["silver"] = float(get("https://api.gold-api.com/price/XAG")["price"])
        src.append("gold-api.com (XAG)")
    except Exception as e:
        print("gold-api silver failed:", e)
        if cur and cur.get("xag"):
            out["silver"] = 1 / cur["xag"]
            src.append("Currency-API (XAG, daily)")
    # Bitcoin
    try:
        c = get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,pkr&include_24hr_change=true")["bitcoin"]
        out["btc"], out["btc_pkr"], out["btc_chg"] = c["usd"], c["pkr"], c.get("usd_24h_change")
        src.append("CoinGecko (BTC)")
        try:
            m = get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=pkr&ids=bitcoin")[0]
            out["btc_hi"], out["btc_lo"] = m.get("high_24h"), m.get("low_24h")
            h = get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=pkr&days=30&interval=daily")
            out["btc_hist"] = [[dt.datetime.fromtimestamp(p[0] / 1000, dt.timezone.utc).strftime("%Y-%m-%d"), round(p[1])]
                               for p in h.get("prices", [])]
        except Exception as e:
            print("CoinGecko extra BTC data failed:", e)
    except Exception as e:
        print("CoinGecko failed:", e)
        try:
            t = get("https://data-api.binance.vision/api/v3/ticker/24hr?symbol=BTCUSDT")
            out["btc"], out["btc_chg"] = float(t["lastPrice"]), float(t["priceChangePercent"])
            if out.get("pkr"):
                out["btc_pkr"] = out["btc"] * out["pkr"]
        except Exception as e2:
            print("Binance BTC failed:", e2)
    if cur:
        out["fx"] = {k: cur["pkr"] / cur[k] for k in ("eur", "gbp", "sar", "aed", "cny", "cad", "aud", "kwd", "qar", "omr", "myr", "jpy")
                     if cur.get(k) and cur.get("pkr")}
    out["sources"] = src
    return out


# ------------------------------------------------------------------ numbers
def per_gram_pkr(usd_oz, pkr):
    return usd_oz * pkr / OZ


def rs(v):
    return "Rs " + f"{round(v):,}"


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
        "fx": {k: round(v, 2) for k, v in (raw.get("fx") or old.get("fx") or {}).items()},
        "sources": raw.get("sources", []),
    }
    if raw.get("silver"):
        sg = per_gram_pkr(raw["silver"], p)
        r["silver"] = {"usd_oz": round(raw["silver"], 2), "tola": round(sg * TOLA), "g10": round(sg * 10),
                       "g1": round(sg, 2), "kg": round(sg * 1000), "oz": round(sg * OZ),
                       "tola925": round(sg * TOLA * 0.925)}
    elif old.get("silver"):
        r["silver"] = old["silver"]
    if raw.get("btc"):
        r["btc"] = {"usd": round(raw["btc"]), "pkr": round(raw.get("btc_pkr") or raw["btc"] * p),
                    "chg24": round(raw["btc_chg"], 2) if raw.get("btc_chg") is not None else None,
                    "hi24": round(raw["btc_hi"]) if raw.get("btc_hi") else None,
                    "lo24": round(raw["btc_lo"]) if raw.get("btc_lo") else None}
    elif old.get("btc"):
        r["btc"] = old["btc"]
    return r


PAGE_IMAGES = {'gold': [['img/gold-rate-pakistan-24k-gold-bars.webp', 600, 420, 'Gold rate in Pakistan today – 24K gold bars with a rising gold price line', '24K gold bars: the price per tola follows XAUUSD and the dollar rate'], ['img/gold-tola-ounce-karat-purity-infographic.webp', 300, 660, 'Gold infographic: 1 tola = 11.664 grams, 1 ounce = 2.67 tola, and 24K, 22K, 21K, 18K gold purity', 'Gold facts: tola, ounce and karat purity']], 'silver': [['img/silver-rate-pakistan-chandi-bars.webp', 600, 420, 'Silver rate in Pakistan today – chandi bars and a silver coin with a price line', 'Fine silver bars: the chandi rate follows XAGUSD and the dollar rate'], ['img/silver-chandi-tola-kg-nisab-infographic.webp', 300, 660, 'Chandi infographic: 1 kg = 85.7 tola, zakat nisab 52.5 tola of silver, 999 and 925 silver purity', 'Silver facts: tola, kg, nisab and purity']], 'btc': [['img/bitcoin-price-pakistan-btc-coin.webp', 600, 420, 'Bitcoin price in Pakistan – BTC coin in front of a rising crypto chart', 'Bitcoin in PKR: global BTC price × the dollar rate'], ['img/bitcoin-supply-satoshi-facts-infographic.webp', 300, 660, 'Bitcoin facts infographic: 21 million maximum supply, 1 BTC = 100 million satoshis, BTC to PKR formula', 'Bitcoin facts: supply, satoshis and how the PKR price is set']], 'usd': [['img/dollar-rate-pakistan-usd-pkr-notes.webp', 600, 420, 'Dollar rate in Pakistan – 100 US dollar note and 5000 rupee note, USD to PKR', 'US dollar to Pakistani rupee: the interbank rate'], ['img/dollar-rate-interbank-open-market-infographic.webp', 300, 660, 'Dollar rate infographic: interbank vs open market rate and what moves the Pakistani rupee', 'Dollar facts: interbank vs open market and what moves the rupee']]}


def img_objs(key):
    return [{"@type": "ImageObject", "url": "https://qaziforextips.com/" + a, "contentUrl": "https://qaziforextips.com/" + a,
             "width": w * 2, "height": h * 2, "caption": alt, "creator": {"@id": "https://qaziforextips.com/#org"},
             "creditText": "Qazi Forex Tips", "copyrightNotice": "Qazi Forex Tips"} for a, w, h, alt, cap in PAGE_IMAGES[key]]


def save_hist(name, row, keep=400):
    """Upsert today's row (weekdays only unless every_day) in data/<name>.json and return the list."""
    path = os.path.join(ROOT, "data", name + ".json")
    try:
        hist = json.load(open(path, encoding="utf-8"))
    except Exception:
        hist = []
    if row:
        hist = [h for h in hist if h["d"] != row["d"]] + [row]
        hist.sort(key=lambda h: h["d"])
        hist = hist[-keep:]
        json.dump(hist, open(path, "w", encoding="utf-8"), separators=(",", ":"))
    return hist


def set_head(s, title, desc):
    s = re.sub(r"<title>.*?</title>", "<title>" + esc(title) + "</title>", s, count=1, flags=re.S)
    for attr, val in (('name="description"', desc), ('property="og:title"', title),
                      ('property="og:description"', desc), ('name="twitter:title"', title),
                      ('name="twitter:description"', desc)):
        s = re.sub(r'(<meta ' + attr + r' content=")[^"]*(")', lambda m: m.group(1) + esc(val) + m.group(2), s, count=1)
    return s


def set_ld(s, ld):
    return re.sub(r'(<script type="application/ld\+json" id="ld">).*?(</script>)',
                  lambda m: m.group(1) + json.dumps(ld, ensure_ascii=False) + m.group(2), s, count=1, flags=re.S)


def page_ld(url, title, desc, crumb, faq, now, published="2026-11-13", key=None):
    imgs = img_objs(key) if key else []
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc, "inLanguage": "en",
         "datePublished": published, "dateModified": now.strftime("%Y-%m-%dT%H:%M:%S+05:00"),
         **({"primaryImageOfPage": imgs[0], "image": imgs} if imgs else {}),
         "isPartOf": {"@id": "https://qaziforextips.com/#site"}, "publisher": {"@id": "https://qaziforextips.com/#org"}},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://qaziforextips.com/"},
            {"@type": "ListItem", "position": 2, "name": "Forex Guide", "item": "https://qaziforextips.com/forex-guide.html"},
            {"@type": "ListItem", "position": 3, "name": crumb, "item": url}]}]}


def hist_rows(hist, key, fmt, extra=None):
    last = list(reversed(hist[-8:]))
    out = []
    for i, h in enumerate(last[:7]):
        nxt = last[i + 1] if i + 1 < len(last) else None
        d = dt.datetime.strptime(h["d"], "%Y-%m-%d").strftime("%a %-d %b")
        if nxt:
            c = h[key] - nxt[key]
            ctxt = f'<span class="{"up" if c >= 0 else "down"}">{"+" if c >= 0 else "−"}{fmt(abs(c))[3:]}</span>'
        else:
            ctxt = "–"
        mid = extra(h) if extra else ""
        out.append(f"<tr><td>{d}</td><td>{fmt(h[key])}</td>{mid}<td>{ctxt}</td></tr>")
    return "".join(out)


SILVER_PAGE, BTC_PAGE = "silver-rate-pakistan.html", "bitcoin-price-pakistan.html"


def silver_page(r, hist):
    url = "https://qaziforextips.com/" + SILVER_PAGE
    path = os.path.join(ROOT, SILVER_PAGE)
    if not os.path.exists(path) or not r.get("silver"):
        return None
    s = open(path, encoding="utf-8").read()
    now = dt.datetime.now(PKT)
    day, day_long = now.strftime("%-d %b %Y"), now.strftime("%-d %B %Y")
    v = r["silver"]
    prev = [h for h in hist if h["d"] < now.strftime("%Y-%m-%d")]
    chg = v["tola"] - prev[-1]["tola"] if prev else 0
    title = f"Silver Rate in Pakistan Today {day} – Chandi Price per Tola"
    desc = (f"Silver (chandi) rate in Pakistan today ({day}): {rs(v['tola'])} per tola, {rs(v['g10'])} per 10 gram, "
            f"{rs(v['kg'])} per kg. Live rate, calculator and 30-day chart.")
    s = set_head(s, title, desc)
    s = put(s, "date", esc(day_long))
    s = put(s, "time", esc(r["updated_pkt"]))
    s = put(s, "big", esc(rs(v["tola"])))
    s = put(s, "chg", f'<span class="gr-chg {"up" if chg >= 0 else "down"}">{"+" if chg >= 0 else "−"}{abs(chg):,} vs previous day</span>' if prev else "")
    s = put(s, "mini",
            f'<div><i>10 gram</i><b>{rs(v["g10"])}</b></div><div><i>1 kg</i><b>{rs(v["kg"])}</b></div>'
            f'<div><i>Silver / ounce</i><b>${v["usd_oz"]:,.2f}</b></div><div><i>USD / PKR</i><b>{r["usdpkr"]:.2f}</b></div>')
    g1 = v["g1"]
    rows = [("Pure silver (999)", 1.0), ("Sterling silver (925)", 0.925)]
    s = put(s, "table", "".join(
        f'<tr><th scope="row">{n}</th><td>{rs(g1 * f * TOLA)}</td><td>{rs(g1 * f * 10)}</td><td>Rs {g1 * f:,.2f}</td>'
        f'<td>{rs(g1 * f * 1000)}</td><td>{rs(g1 * f * OZ)}</td></tr>' for n, f in rows))
    s = put(s, "sent", f"The silver rate in Pakistan today, {esc(day_long)}, is <b>{rs(v['tola'])} per tola</b> and "
                       f"<b>{rs(v['g10'])} per 10 grams</b> for pure (999) silver, based on the international price of "
                       f"${v['usd_oz']:,.2f} per ounce and a dollar rate of {r['usdpkr']:.2f} rupees.")
    s = put(s, "ur", "آج " + f"{now.day} {UR_MONTHS[now.month - 1]} {now.year}" + " کو پاکستان میں چاندی کا ریٹ <b>"
            + f"{v['tola']:,}" + " روپے فی تولہ</b> اور <b>" + f"{v['g10']:,}" + " روپے فی 10 گرام</b> ہے۔")
    s = put(s, "ro", f"Aaj {esc(day_long)} ko Pakistan mein chandi ka rate <b>{rs(v['tola'])} fi tola</b> aur "
                     f"<b>{rs(v['g10'])} fi 10 gram</b> hai.")
    s = put(s, "hist", hist_rows(hist, "tola", rs, lambda h: f'<td>${h["usd"]:,.2f}</td>'))
    nis_s = round(v["tola"] * 52.5)
    nis_g = round(r["gold"]["karats"]["24K"]["tola"] * 7.5)
    s = put(s, "nisab",
            f'<div><i>Silver nisab · 52.5 tola</i><b>{rs(nis_s)}</b><span>612.36 g of pure silver</span></div>'
            f'<div><i>Gold nisab · 7.5 tola</i><b>{rs(nis_g)}</b><span>87.48 g of 24K gold</span></div>'
            f'<div><i>Zakat on the silver nisab (2.5%)</i><b>{rs(nis_s * 0.025)}</b><span>2.5% of {rs(nis_s)}</span></div>')
    s = put(s, "nisabtxt", f"At today's market rate ({esc(day_long)}), <b>52.5 tola of silver = {rs(nis_s)}</b> and "
                           f"<b>7.5 tola of 24K gold = {rs(nis_g)}</b>.")
    s = put(s, "json", esc(json.dumps({"g1": g1, "nisS": nis_s, "nisG": nis_g,
                                         "hist": [[h["d"], h["tola"]] for h in hist[-60:]]}, separators=(",", ":"))))
    faq = [
        ("What is the silver rate in Pakistan today?",
         f"On {day_long} pure (999) silver in Pakistan is {rs(v['tola'])} per tola, {rs(v['g10'])} per 10 grams and "
         f"{rs(v['kg'])} per kilogram, based on ${v['usd_oz']:,.2f} per ounce and USD/PKR {r['usdpkr']:.2f}."),
        ("How is the silver price per tola calculated?",
         "Silver price per tola = international silver price per ounce (USD) × USD/PKR ÷ 31.1035 × 11.6638. "
         "For sterling silver (925) multiply the result by 0.925."),
        ("Why is the sarafa silver rate different?",
         "This page shows the market rate from the international price and the live dollar rate. Local bullion dealers "
         "add their own premium, and jewellers add making charges, so shop prices are usually higher."),
        ("What is the difference between 999 and 925 silver?",
         "999 (fine) silver is 99.9% pure and is sold as bars and coins. 925 (sterling) silver is 92.5% silver mixed with "
         "copper for strength and is common in jewellery."),
        ("Is the silver rate the same in Karachi, Lahore and Islamabad?",
         "The base rate is the same across Pakistan. Small differences come from local dealer premiums and shop spreads."),
        ("How often is this silver rate updated?",
         "Every 30 minutes on trading days, Monday to Friday. On weekends the last Friday rate stays on the page."),
        ("What is the nisab amount in Pakistan today?",
         f"At today's market rate, the silver nisab of 52.5 tola (612.36 grams) is {rs(nis_s)} and the gold nisab of "
         f"7.5 tola (87.48 grams) of 24K gold is {rs(nis_g)}. Zakat is 2.5% of zakatable wealth that stays above the nisab "
         f"for a lunar year."),
    ]
    s = set_ld(s, page_ld(url, title, desc, "Silver Rate in Pakistan", faq, now, key="silver"))
    s = put(s, "faq1", esc(faq[0][1]))
    return path, s


def crore(v):
    return "Rs " + f"{v / 1e7:.2f}" + " Cr"


def btc_page(r, hist):
    url = "https://qaziforextips.com/" + BTC_PAGE
    path = os.path.join(ROOT, BTC_PAGE)
    b = r.get("btc")
    if not os.path.exists(path) or not b:
        return None
    s = open(path, encoding="utf-8").read()
    now = dt.datetime.now(PKT)
    day, day_long = now.strftime("%-d %b %Y"), now.strftime("%-d %B %Y")
    title = f"Bitcoin Price in Pakistan Today {day} – BTC to PKR Live"
    desc = (f"Bitcoin price in Pakistan today ({day}): 1 BTC = {rs(b['pkr'])} ({crore(b['pkr'])}), ${b['usd']:,}. "
            f"Live BTC to PKR rate, converter and 30-day chart.")
    s = set_head(s, title, desc)
    s = put(s, "date", esc(day_long))
    s = put(s, "time", esc(r["updated_pkt"]))
    s = put(s, "big", esc(rs(b["pkr"])))
    c = b.get("chg24") or 0
    s = put(s, "chg", f'<span class="gr-chg {"up" if c >= 0 else "down"}">{pct(c)} in 24 hours · {crore(b["pkr"])}</span>')
    s = put(s, "mini",
            f'<div><i>BTC / USD</i><b>${b["usd"]:,}</b></div>'
            f'<div><i>24h high</i><b>{crore(b["hi24"]) if b.get("hi24") else "–"}</b></div>'
            f'<div><i>24h low</i><b>{crore(b["lo24"]) if b.get("lo24") else "–"}</b></div>'
            f'<div><i>USD / PKR</i><b>{r["usdpkr"]:.2f}</b></div>')
    amts = [0.0001, 0.001, 0.01, 0.1, 0.5, 1]
    s = put(s, "table", "".join(f'<tr><th scope="row">{a:g} BTC</th><td>{rs(a * b["pkr"])}</td><td>${a * b["usd"]:,.2f}</td></tr>' for a in amts))
    s = put(s, "sent", f"The Bitcoin price in Pakistan today, {esc(day_long)}, is <b>{rs(b['pkr'])}</b> "
                       f"({crore(b['pkr'])}) for 1 BTC, which is ${b['usd']:,} at a dollar rate of {r['usdpkr']:.2f} rupees.")
    s = put(s, "ur", "آج " + f"{now.day} {UR_MONTHS[now.month - 1]} {now.year}" + " کو ایک بٹ کوائن کی قیمت <b>"
            + f"{b['pkr']:,}" + " روپے</b> (" + f"{b['pkr'] / 1e7:.2f}" + " کروڑ) ہے۔")
    s = put(s, "ro", f"Aaj {esc(day_long)} ko 1 Bitcoin ki qeemat <b>{rs(b['pkr'])}</b> ({crore(b['pkr'])}) hai.")
    s = put(s, "hist", hist_rows(hist, "pkr", rs))
    s = put(s, "json", esc(json.dumps({"pkr": b["pkr"], "usd": b["usd"], "hist": [[h["d"], h["pkr"]] for h in hist[-31:]]},
                                      separators=(",", ":"))))
    faq = [
        ("What is the Bitcoin price in Pakistan today?",
         f"On {day_long} 1 Bitcoin is about {rs(b['pkr'])} ({crore(b['pkr'])}), or ${b['usd']:,}, at USD/PKR {r['usdpkr']:.2f}."),
        ("How is the BTC to PKR price calculated?",
         "The Bitcoin price in rupees is the global Bitcoin price in US dollars multiplied by the dollar rate. "
         "Local P2P sellers often quote a little more or less than this market rate."),
        ("Is Bitcoin legal in Pakistan?",
         "Pakistan's Parliament passed the Virtual Assets Act in 2026, which made the Pakistan Virtual Assets Regulatory "
         "Authority (PVARA) the regulator that licenses crypto exchanges and service providers. Use licensed platforms "
         "and check PVARA and the State Bank for the latest rules."),
        ("What is a satoshi?",
         "A satoshi (sat) is the smallest unit of Bitcoin: 1 BTC = 100,000,000 satoshis. You can buy a small part of a Bitcoin."),
        ("How often is this Bitcoin price updated?",
         "Every 30 minutes on weekdays. Bitcoin trades 24/7, so the price on exchanges can move between updates."),
    ]
    s = set_ld(s, page_ld(url, title, desc, "Bitcoin Price in Pakistan", faq, now, key="btc"))
    s = put(s, "faq1", esc(faq[0][1]))
    return path, s


USD_PAGE = "dollar-rate-pakistan.html"
FX_NAMES = [("eur", "Euro (EUR)"), ("gbp", "British Pound (GBP)"), ("sar", "Saudi Riyal (SAR)"), ("aed", "UAE Dirham (AED)"),
            ("qar", "Qatari Riyal (QAR)"), ("kwd", "Kuwaiti Dinar (KWD)"), ("omr", "Omani Rial (OMR)"), ("cny", "Chinese Yuan (CNY)"),
            ("cad", "Canadian Dollar (CAD)"), ("aud", "Australian Dollar (AUD)"), ("myr", "Malaysian Ringgit (MYR)"), ("jpy", "Japanese Yen (JPY)")]


def usd_page(r, hist):
    url = "https://qaziforextips.com/" + USD_PAGE
    path = os.path.join(ROOT, USD_PAGE)
    if not os.path.exists(path):
        return None
    s = open(path, encoding="utf-8").read()
    now = dt.datetime.now(PKT)
    day, day_long = now.strftime("%-d %b %Y"), now.strftime("%-d %B %Y")
    u, up = r["usdpkr"], r.get("usdpkr_prev") or r["usdpkr"]
    chg = u - up
    title = f"Dollar Rate in Pakistan Today {day} – USD to PKR Live"
    desc = (f"Dollar rate in Pakistan today ({day}): 1 US dollar = Rs {u:.2f}. Live USD to PKR rate, converter, "
            f"30-day chart and Riyal, Dirham, Pound and Euro rates in rupees.")
    s = set_head(s, title, desc)
    s = put(s, "date", esc(day_long))
    s = put(s, "time", esc(r["updated_pkt"]))
    s = put(s, "big", f"Rs {u:.2f}")
    s = put(s, "chg", f'<span class="gr-chg {"up" if chg >= 0 else "down"}">{"+" if chg >= 0 else "−"}{abs(chg):.2f} '
                      f'({pct((u / up - 1) * 100 if up else 0)}) vs previous close</span>')
    fx = r.get("fx") or {}
    s = put(s, "mini",
            f'<div><i>100 USD</i><b>{rs(u * 100)}</b></div><div><i>1,000 USD</i><b>{rs(u * 1000)}</b></div>'
            f'<div><i>Saudi Riyal</i><b>Rs {fx.get("sar", 0):.2f}</b></div><div><i>UAE Dirham</i><b>Rs {fx.get("aed", 0):.2f}</b></div>')
    amts = [1, 10, 50, 100, 500, 1000, 5000, 10000]
    s = put(s, "table", "".join(f'<tr><th scope="row">${a:,}</th><td>{rs(a * u)}</td><td>Rs {a * u:,.2f}</td></tr>' for a in amts))
    s = put(s, "fx", "".join(f'<tr><th scope="row">{n}</th><td>Rs {fx[k]:,.2f}</td><td>{rs(fx[k] * 100)}</td></tr>'
                              for k, n in FX_NAMES if k in fx))
    s = put(s, "sent", f"The dollar rate in Pakistan today, {esc(day_long)}, is <b>Rs {u:.2f}</b> for 1 US dollar, so "
                       f"<b>100 dollars = {rs(u * 100)}</b>.")
    s = put(s, "ur", "آج " + f"{now.day} {UR_MONTHS[now.month - 1]} {now.year}" + " کو ایک امریکی ڈالر <b>"
            + f"{u:.2f}" + " روپے</b> کا ہے، یعنی 100 ڈالر <b>" + f"{round(u * 100):,}" + " روپے</b>۔")
    s = put(s, "ro", f"Aaj {esc(day_long)} ko 1 dollar <b>Rs {u:.2f}</b> ka hai, yaani 100 dollar <b>{rs(u * 100)}</b>.")
    s = put(s, "hist", hist_rows(hist, "pkr", lambda x: f"Rs {x:,.2f}"))
    s = put(s, "json", esc(json.dumps({"u": u, "fx": fx, "hist": [[h["d"], h["pkr"]] for h in hist[-31:]]}, separators=(",", ":"))))
    faq = [
        ("What is the dollar rate in Pakistan today?",
         f"On {day_long} one US dollar is Rs {u:.2f} in the market (interbank) rate, so 100 dollars is {rs(u * 100)}."),
        ("What is the difference between the interbank and open market dollar rate?",
         "The interbank rate is the rate banks trade at with each other and is the rate shown here. The open market rate is what "
         "exchange companies charge in cash; it is usually a little higher and has separate buying and selling prices."),
        ("Why does the dollar rate change in Pakistan?",
         "The rupee moves with Pakistan's imports and exports, remittances from overseas Pakistanis, foreign exchange reserves, "
         "IMF and loan inflows, and the State Bank's interest rate policy."),
        ("How much is 100 dollars in Pakistani rupees?",
         f"At today's rate of Rs {u:.2f}, 100 US dollars is {rs(u * 100)} and 1,000 dollars is {rs(u * 1000)}."),
        ("How often is this dollar rate updated?",
         "Every 30 minutes on weekdays. Other currencies in the table are daily reference rates."),
    ]
    s = set_ld(s, page_ld(url, title, desc, "Dollar Rate in Pakistan", faq, now, key="usd"))
    s = put(s, "faq1", esc(faq[0][1]))
    return path, s


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
         "primaryImageOfPage": img_objs("gold")[0], "image": img_objs("gold")},
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
    boxes.append(f'<a class="lrate" href="silver-rate-pakistan.html"><i>Silver / tola</i><b>{rs(sv["tola"])}</b>'
                 f'<span>${sv["usd_oz"]:,.2f}/oz</span></a>' if sv else
                 '<div class="lrate"><i>Silver / tola</i><b>–</b><span></span></div>')
    chg_p = (r["usdpkr"] / r["usdpkr_prev"] - 1) * 100 if r.get("usdpkr_prev") else None
    boxes.append(f'<a class="lrate" href="dollar-rate-pakistan.html"><i>USD / PKR</i><b>Rs {r["usdpkr"]:.2f}</b>'
                 f'<span class="{"up" if (chg_p or 0) >= 0 else "down"}">{pct(chg_p)}</span></a>')
    b = r.get("btc")
    boxes.append(f'<a class="lrate" href="bitcoin-price-pakistan.html"><i>Bitcoin (PKR)</i><b>{crore(b["pkr"])}</b>'
                 f'<span class="{"up" if (b.get("chg24") or 0) >= 0 else "down"}">{pct(b.get("chg24"))}</span></a>' if b else
                 '<div class="lrate"><i>Bitcoin (PKR)</i><b>–</b><span></span></div>')
    s = put(s, "home", "".join(boxes))
    s = put(s, "hometime", esc(r["updated_pkt"]))
    return path, s


def sitemap():
    path = os.path.join(ROOT, "sitemap.xml")
    s = open(path, encoding="utf-8").read()
    today = dt.datetime.now(PKT).strftime("%Y-%m-%d")
    for page in (PAGE, SILVER_PAGE, BTC_PAGE, USD_PAGE):
        u = "https://qaziforextips.com/" + page
        s = re.sub(r"(<loc>" + re.escape(u) + r"</loc>\s*<lastmod>)[^<]*(</lastmod>)",
                   lambda m: m.group(1) + today + m.group(2), s, count=1)
    return path, s


def main():
    rates_path = os.path.join(ROOT, "data", "rates.json")
    try:
        old = json.load(open(rates_path, encoding="utf-8"))
        old_flat = {"gold": old.get("gold", {}), "usdpkr_prev": old.get("usdpkr"),
                    "silver": old.get("silver"), "btc": old.get("btc"),
                    "candles": old.get("candles"), "candle_symbol": old.get("candle_symbol"), "fx": old.get("fx")}
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
    today = dt.datetime.now(PKT)
    srow = None
    if r.get("silver") and today.weekday() < 5:
        srow = {"d": today.strftime("%Y-%m-%d"), "usd": r["silver"]["usd_oz"], "pkr": r["usdpkr"], "tola": r["silver"]["tola"]}
    shist = save_hist("silver-history", srow)
    bhist = None
    if raw.get("btc_hist"):
        bhist = [{"d": d, "pkr": v} for d, v in raw["btc_hist"]]
        dedup = {}
        for h in bhist:
            dedup[h["d"]] = h            # the last point of a day is the newest
        bhist = sorted(dedup.values(), key=lambda h: h["d"])
        json.dump(bhist, open(os.path.join(ROOT, "data", "btc-history.json"), "w", encoding="utf-8"), separators=(",", ":"))
    else:
        brow = {"d": today.strftime("%Y-%m-%d"), "pkr": r["btc"]["pkr"]} if r.get("btc") else None
        bhist = save_hist("btc-history", brow, keep=60)
    urow = {"d": today.strftime("%Y-%m-%d"), "pkr": r["usdpkr"]} if today.weekday() < 5 else None
    uhist = save_hist("usdpkr-history", urow)
    jobs = [gold_page(r, hist), silver_page(r, shist), btc_page(r, bhist), usd_page(r, uhist), home_page(r), sitemap()]
    for job in jobs:
        if job:
            open(job[0], "w", encoding="utf-8").write(job[1])
    print("Gold 24K tola:", r["gold"]["karats"]["24K"]["tola"], "| USD/PKR:", r["usdpkr"], "| sources:", r["sources"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
