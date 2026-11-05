#!/usr/bin/env python3
"""YouTube comments on the website.

1. Finds every lesson page (lesson-*.html) and its YouTube video.
2. Downloads the public comments of each video:
   - with the official YouTube Data API when the secret YT_API_KEY is set (recommended),
   - otherwise from the public YouTube watch page.
3. Keeps only good comments (no links, phone numbers, signals, "inbox", money/profit claims,
   no comments by the channel itself, nothing on the block list data/yt-blocklist.txt).
4. Writes data/yt-comments.json and puts the best 4 comments under each lesson
   (between <!--YTC--> markers) and the best 6 on feedback.html.
Comments are shown exactly as written, with name, date and a link to the original comment.
Run: python3 .github/scripts/yt-comments.py [--offline]   (--offline = only rebuild pages from the JSON)
"""
import os, re, json, sys, glob, html, time, datetime, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data", "yt-comments.json")
BLOCK = os.path.join(ROOT, "data", "yt-blocklist.txt")
KEY = os.environ.get("YT_API_KEY", "").strip()
PER_LESSON, ON_FEEDBACK = 4, 6
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

BAD = re.compile(r"(https?://|www\.|wa\.me|\+?\d[\d\s-]{8,}|signal|inbox|dm me|whatsapp|telegram|\$\s?\d|\d+\s?\$|"
                 r"profit|kamaye|earn|income|account manage|join my|number do|contact|\brs\.?\s?\d|\bpkr\b|lakh|crore|"
                 r"\btp\s?hit|\bsl\s?hit|\d+\s?trades?\b|trade open|invest|bitcoin|crypto|passive income|recommend(ed)? (me|by))", re.I)

def get(url, data=None, headers=None):
    h = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

def ago(iso):
    try:
        d = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except Exception:
        return ""
    days = (datetime.datetime.now(datetime.timezone.utc) - d).days
    if days >= 365: n = days // 365; return f"{n} year{'s' if n > 1 else ''} ago"
    if days >= 30:  n = days // 30;  return f"{n} month{'s' if n > 1 else ''} ago"
    if days >= 7:   n = days // 7;   return f"{n} week{'s' if n > 1 else ''} ago"
    if days >= 1:   return f"{days} day{'s' if days > 1 else ''} ago"
    return "today"

def via_api(vid):
    q = urllib.parse.urlencode({"part": "snippet", "videoId": vid, "order": "relevance", "maxResults": 60,
                                "textFormat": "plainText", "key": KEY})
    j = json.loads(get("https://www.googleapis.com/youtube/v3/commentThreads?" + q))
    out = []
    for it in j.get("items", []):
        s = it["snippet"]["topLevelComment"]["snippet"]
        out.append({"a": s.get("authorDisplayName", ""), "t": s.get("textOriginal", ""), "l": int(s.get("likeCount", 0)),
                    "d": ago(s.get("publishedAt", "")), "id": it["snippet"]["topLevelComment"]["id"],
                    "own": s.get("authorChannelId", {}).get("value") == it["snippet"].get("channelId")})
    return out

def via_page(vid):
    page = get("https://www.youtube.com/watch?v=" + vid + "&hl=en")
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", page, re.S)
    ver = re.search(r'"INNERTUBE_CLIENT_VERSION":"([^"]+)"', page)
    if not m or not ver: return []
    toks = re.findall(r'"continuationCommand":\{"token":"([^"]+)","request":"CONTINUATION_REQUEST_TYPE_WATCH_NEXT"', m.group(1))
    if not toks: return []
    body = json.dumps({"context": {"client": {"clientName": "WEB", "clientVersion": ver.group(1), "hl": "en"}},
                       "continuation": toks[-1]}).encode()
    j = json.loads(get("https://www.youtube.com/youtubei/v1/next?prettyPrint=false", body, {"Content-Type": "application/json"}))
    out = []
    for mu in j.get("frameworkUpdates", {}).get("entityBatchUpdate", {}).get("mutations", []):
        p = mu.get("payload", {}).get("commentEntityPayload")
        if not p: continue
        like = str(p.get("toolbar", {}).get("likeCountNotliked", "0")).strip()
        out.append({"a": p["author"]["displayName"], "t": p["properties"]["content"]["content"],
                    "l": int(like) if like.isdigit() else 0, "d": p["properties"].get("publishedTime", "").replace(" (edited)", ""),
                    "id": p["properties"]["commentId"], "own": bool(p["author"].get("isCreator"))})
    return out

def blocklist():
    if not os.path.exists(BLOCK): return set()
    ids = set()
    for line in open(BLOCK, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"): continue
        m = re.search(r"lc=([\w-]+)", line)
        ids.add(m.group(1) if m else line)
    return ids

def choose(cs, blocked, n):
    ok = [c for c in cs if not c["own"] and c["id"] not in blocked and len(c["t"]) >= 28 and not BAD.search(c["t"])]
    ok.sort(key=lambda c: c["l"] * 3 + min(len(c["t"]), 160) / 40, reverse=True)
    return ok[:n]

def lessons():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "lesson-*.html"))):
        s = open(f, encoding="utf-8").read()
        m = re.search(r"youtube\.com/embed/([\w-]{11})", s)
        if m: out.append((os.path.basename(f), m.group(1)))
    return out

# ------------------------------------------------------------------ HTML
COL = ["#c23b55", "#2f7fd1", "#0a9d86", "#b8860b", "#7b5cd6", "#d2691e"]
CSS = ("<style>.ytc{margin-top:40px;border:1px solid var(--line);border-radius:16px;background:var(--surface);padding:24px}"
       ".ytc-h{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:12px;margin-bottom:16px}.ytc-h h2{margin:0}"
       ".ytc-h p{margin:4px 0 0;color:var(--muted);font-size:14px}"
       ".ytc-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.ytc-grid.c3{grid-template-columns:repeat(3,minmax(0,1fr))}"
       ".ytc figure.ytc-c{margin:0;border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:var(--bg);display:grid;gap:8px;align-content:start}"
       ".ytc-top{display:flex;align-items:center;gap:10px}"
       ".ytc-av{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;font:700 14px/1 var(--f-body);color:#fff;flex:none}"
       ".ytc-n{font-weight:700;font-size:14px;line-height:1.2;overflow-wrap:anywhere}.ytc-n small{display:block;font-weight:400;color:var(--muted);font-size:12px;margin-top:2px}"
       ".ytc blockquote.ytc-t{margin:0;padding:0;border:0;font-style:normal;quotes:none;font-size:15.5px;line-height:1.6;white-space:pre-line;overflow-wrap:anywhere}"
       ".ytc blockquote.ytc-t[dir=rtl]{font-family:var(--f-ur);font-size:17px;line-height:2.1}"
       ".ytc-f{display:flex;justify-content:space-between;align-items:center;font-size:13px;color:var(--muted)}.ytc-f a{color:var(--muted)}"
       ".ytc-yt{display:inline-flex;align-items:center;gap:6px;font:600 12px/1 var(--f-mono);letter-spacing:.8px;text-transform:uppercase;color:#e04848}"
       "@media (max-width:760px){.ytc-grid,.ytc-grid.c3{grid-template-columns:1fr}.ytc{padding:18px}}</style>")
E = lambda s: html.escape(s, quote=True)

def card(c, vid, i):
    name = c["a"].lstrip("@")
    rtl = bool(re.search(r"[؀-ۿ]", c["t"]))
    url = f"https://www.youtube.com/watch?v={vid}&lc={c['id']}"
    likes = f"👍 {c['l']}" if c["l"] else ""
    return (f'<figure class="ytc-c"><div class="ytc-top"><span class="ytc-av" style="background:{COL[i % len(COL)]}">{E(name[:1].upper())}</span>'
            f'<div class="ytc-n">{E(name)}<small>{E(c["d"])} · YouTube</small></div></div>'
            f'<blockquote class="ytc-t" dir="{"rtl" if rtl else "ltr"}" cite="{url}">{E(c["t"])}</blockquote>'
            f'<div class="ytc-f"><span>{likes}</span><a href="{url}" target="_blank" rel="noopener nofollow">View on YouTube ↗</a></div></figure>')

def lesson_block(vid, cs):
    return ('<!--YTC-->' + CSS + '<section class="ytc" aria-label="Comments from YouTube"><div class="ytc-h"><div>'
            '<span class="ytc-yt">▶ From our YouTube channel</span><h2>What students said about this lecture</h2>'
            '<p>Public comments on this video, shown as written. Updated automatically.</p></div>'
            f'<a class="btn" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">Read all comments</a></div>'
            '<div class="ytc-grid">' + "".join(card(c, vid, i) for i, c in enumerate(cs)) + '</div></section><!--/YTC-->')

def feedback_block(items):
    return ('<!--YTC-->' + CSS + '<div class="wrap" style="padding-top:30px"><section class="ytc" aria-label="Comments from YouTube"><div class="ytc-h"><div>'
            '<span class="ytc-yt">▶ From our YouTube channel</span><h2>Comments from our YouTube lectures</h2>'
            '<p>Public comments from students on our free lectures, shown as written.</p></div>'
            '<a class="btn" href="https://www.youtube.com/@QaziForexTips" target="_blank" rel="noopener">Visit the channel</a></div>'
            '<div class="ytc-grid c3">' + "".join(card(c, v, i) for i, (c, v) in enumerate(items)) + '</div></section></div><!--/YTC-->')

def put(s, block, anchor_re, where="before"):
    s = re.sub(r"<!--YTC-->.*?<!--/YTC-->\n?", "", s, flags=re.S)
    if not block: return s
    m = re.search(anchor_re, s)
    if not m: return s
    i = m.start() if where == "before" else m.end()
    return s[:i] + block + "\n" + s[i:]

def build_pages(data):
    blocked = blocklist()
    changed = 0
    pool = []
    for fname, vid in lessons():
        cs = choose(data.get(vid, []), blocked, PER_LESSON)
        pool += [(c, vid) for c in choose(data.get(vid, []), blocked, 2)]
        p = os.path.join(ROOT, fname); s = open(p, encoding="utf-8").read()
        n = put(s, lesson_block(vid, cs) if cs else "", r"    <h2>Related lessons</h2>")
        if n != s: open(p, "w", encoding="utf-8").write(n); changed += 1
    pool.sort(key=lambda x: x[0]["l"] * 3 + min(len(x[0]["t"]), 160) / 40, reverse=True)
    seen, top = set(), []
    for c, v in pool:                                   # one comment per person on the feedback page
        if c["a"] in seen: continue
        seen.add(c["a"]); top.append((c, v))
        if len(top) >= ON_FEEDBACK: break
    p = os.path.join(ROOT, "feedback.html"); s = open(p, encoding="utf-8").read()
    n = put(s, feedback_block(top) if top else "", r"<main[^>]*>", "after")
    if n != s: open(p, "w", encoding="utf-8").write(n); changed += 1
    print("pages updated:", changed)

def main():
    data = json.load(open(DATA, encoding="utf-8")) if os.path.exists(DATA) else {}
    if "--offline" not in sys.argv:
        src = "YouTube Data API" if KEY else "public watch page"
        ok = 0
        for _, vid in lessons():
            try:
                cs = via_api(vid) if KEY else via_page(vid)
                if cs: data[vid] = cs; ok += 1          # keep the last good copy if a fetch fails
            except Exception as e:
                print("skip", vid, e)
            time.sleep(1.0)
        print(f"fetched {ok} videos via {src}")
        os.makedirs(os.path.dirname(DATA), exist_ok=True)
        json.dump(data, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
    build_pages(data)

if __name__ == "__main__":
    main()
