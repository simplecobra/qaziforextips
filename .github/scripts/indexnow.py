"""Tell Bing (and the other IndexNow search engines) which pages changed.
Used by .github/workflows/indexnow.yml. Usage: indexnow.py <changed files...>  or  indexnow.py --all
The key file (80eaa78f37d87a1bc12da0f27579d2c2.txt in the site root) must stay on the website."""
import json, re, sys, urllib.request

HOST = "qaziforextips.com"
KEY = "80eaa78f37d87a1bc12da0f27579d2c2"
SKIP = {"404.html", "google7ace57b56453d67a.html", "app.html"}

def page_urls(files):
    out = []
    for f in files:
        f = f.strip()
        if not f.endswith(".html") or "/" in f or f in SKIP:
            continue
        out.append(f"https://{HOST}/" if f == "index.html" else f"https://{HOST}/{f}")
    return out

if sys.argv[1:] == ["--all"]:
    xml = open("sitemap.xml", encoding="utf-8").read()
    urls = [u for u in re.findall(r"<loc>([^<]+)</loc>", xml) if not re.search(r"\.(png|jpe?g|webp)$", u)]
else:
    urls = page_urls(sys.argv[1:])
if "sitemap.xml" in sys.argv[1:]:
    urls.append(f"https://{HOST}/sitemap.xml")
urls = sorted(set(urls))
if not urls:
    print("IndexNow: no pages changed"); sys.exit(0)

body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("IndexNow:", r.status, "-", len(urls), "URLs"); print("\n".join(urls))
except urllib.error.HTTPError as e:
    print("IndexNow error:", e.code, e.read()[:300]); sys.exit(1)
