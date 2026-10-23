/* Writes the approved feedback (Google Sheet "Public" tab) into feedback.html as plain HTML,
   so Google can read the reviews without running JavaScript. The page's own script still
   loads the live list on top of it. Uses the same code as the page (feedback.js).
   Run: node .github/scripts/bake-feedback.js   (FB_CSV_FILE=path to test with a local CSV) */
const fs = require("fs"), path = require("path");
const ROOT = path.resolve(__dirname, "..", "..");
global.window = global; global.__qftMore = 1;           // skip the browser-only style/click setup
if (process.env.FB_CSV_FILE) global.fetch = async () => ({ ok: true, text: async () => fs.readFileSync(process.env.FB_CSV_FILE, "utf8") });
require(path.join(ROOT, "content.js")); require(path.join(ROOT, "feedback.js"));
const S = window.SITE, Q = window.QFTFeedback, FILE = path.join(ROOT, "feedback.html");

Q.load(S, (list, final) => {
  if (!final) return;
  if (!list.length) { console.log("No feedback rows (or the Sheet could not be read). Page left unchanged."); return; }
  const s = Q.summary(list);
  const cards = list.map(t => Q.card(t)).join("");
  const score = s.rated ? '<span>Overall rating</span><b>' + s.avg.toFixed(1) + '</b>' + Q.stars(Math.round(s.avg)) +
    '<span>' + s.count + (s.count === 1 ? " review" : " reviews") + " from students &amp; users</span>" : "";
  let html = fs.readFileSync(FILE, "utf8"), before = html;
  html = html.replace(/<!--FB-STATIC-->[\s\S]*?<!--\/FB-STATIC-->/, "<!--FB-STATIC-->" + cards + "<!--/FB-STATIC-->");
  if (score) html = html.replace(/<!--FB-SCORE-->[\s\S]*?<!--\/FB-SCORE-->/, "<!--FB-SCORE-->" + score + "<!--/FB-SCORE-->");
  if (html === before) console.log("feedback.html: no change (" + list.length + " reviews).");
  else { fs.writeFileSync(FILE, html); console.log("feedback.html updated: " + list.length + " reviews, average " + s.avg.toFixed(1)); }

  /* star rating in Google: AggregateRating on each tool's SoftwareApplication, from that tool's real reviews
     (shown on the same page). Allowed for software; never added to the Organization. */
  [["simulator", "simulator.html"], ["trade-assistant", "trade-assistant.html"]].forEach(([key, file]) => {
    const own = list.filter(t => t.product === key), r = Q.summary(own), fp = path.join(ROOT, file);
    let page = fs.readFileSync(fp, "utf8"); const old = page;
    const m = page.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/); if (!m) return;
    const d = JSON.parse(m[1]), nodes = d["@graph"] || [d];
    const app = nodes.find(n => n["@type"] === "SoftwareApplication"); if (!app) return;
    if (r.rated >= 3) app.aggregateRating = { "@type": "AggregateRating", ratingValue: Number(r.avg.toFixed(1)), ratingCount: r.rated, bestRating: 5, worstRating: 1 };
    else delete app.aggregateRating;
    page = page.replace(m[1], JSON.stringify(d));
    if (page !== old) { fs.writeFileSync(fp, page); console.log(file + ": rating " + (app.aggregateRating ? r.avg.toFixed(1) + " from " + r.rated : "removed")); }
  });
});
