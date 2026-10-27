/* Writes the text that the pages build with JavaScript (from content.js and the reviews Sheet)
   into the HTML itself, so Google and other crawlers see it without running JavaScript.
   The page scripts still run and replace these parts with the live version, so nothing changes
   for visitors. Run from the repo root while a local server serves the site on PORT.
   Usage: PORT=8765 node .github/scripts/bake-static.js                                      */
const fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..", ".."), PORT = process.env.PORT || 8765;

/* page → ids whose inner HTML is written in; "#id" = only copy its hidden/visible state */
const PAGES = {
  "about.html":           ["photo", "abRole", "abStory", "abSkills", "stats", "teamList", "#team", "fname", "disc"],
  "index.html":           ["ann", "stats", "path", "photo", "story", "vids", "fbSum", "tstList", "fname", "disc", "waNum"],
  "updates.html":         ["ufil", "latest", "tl", "fname", "disc"],
  "trade-assistant.html": ["taVisual", "gallery", "#screens", "videoBox", "#video", "vhList", "#versions", "rvMount", "fname", "disc"],
  "simulator.html":       ["vhList", "#versions", "rvMount"],
};

function patch(html, id, inner, hidden) {
  const open = new RegExp('<([a-zA-Z][a-zA-Z0-9]*)(\\s[^>]*?\\bid="' + id + '"[^>]*)>');
  const m = open.exec(html); if (!m) { console.warn("  missing #" + id); return html; }
  const tag = m[1], start = m.index + m[0].length;
  const re = new RegExp("<(/?)" + tag + "\\b[^>]*>", "g"); re.lastIndex = start;
  let depth = 1, end = -1, t;
  while ((t = re.exec(html))) { if (t[1]) { if (--depth === 0) { end = t.index; break; } } else if (!t[0].endsWith("/>")) depth++; }
  if (end < 0) { console.warn("  no close for #" + id); return html; }
  let attrs = m[2].replace(/\s+hidden(?=[\s>]|$)(="[^"]*")?/g, "");
  if (hidden) attrs += " hidden";
  return html.slice(0, m.index) + "<" + tag + attrs + ">" + (inner === null ? html.slice(start, end) : inner) + html.slice(end);
}

(async () => {
  const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  let changed = 0;
  for (const [file, ids] of Object.entries(PAGES)) {
    await page.goto(`http://localhost:${PORT}/${file}`, { waitUntil: "networkidle", timeout: 60000 });
    await page.waitForTimeout(2500);                       // reviews arrive from the Sheet
    const got = await page.evaluate(list => list.map(raw => {
      const only = raw[0] === "#", id = only ? raw.slice(1) : raw, el = document.getElementById(id);
      return el ? { id, only, html: el.innerHTML, hidden: el.hidden } : { id, missing: true };
    }), ids);
    const src = path.join(ROOT, file); let html = fs.readFileSync(src, "utf8"), before = html;
    for (const g of got) {
      if (g.missing) { console.warn("  " + file + ": #" + g.id + " not on page"); continue; }
      if (!g.only && !g.html.trim()) continue;              // nothing rendered (e.g. Sheet offline): keep what is there
      if ((g.id === "rvMount" || g.id === "tstList") && !g.html.includes('class="tst"')) continue;   // reviews did not load: keep the last written ones
      html = patch(html, g.id, g.only ? null : g.html, g.hidden);
    }
    if (html !== before) { fs.writeFileSync(src, html); changed++; console.log("updated " + file); } else console.log("no change " + file);
  }
  await browser.close();
  console.log(changed + " file(s) updated");
})().catch(e => { console.error(e); process.exit(1); });
