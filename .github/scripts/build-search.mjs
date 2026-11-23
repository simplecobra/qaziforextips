// Builds the site search index (Pagefind) into /pagefind for qaziforextips.com.
// Every public page is added as one record with its main text (header, menus, sidebars and footer left out),
// a "type" filter (Lessons, SMC course, Sawal Jawab, Guides, Rates, Tools, Courses, Pages) and its title/image.
// All records use one language index so Urdu, Roman Urdu and English pages are searched together.
// Skips: noindex pages, redirect pages, verification files.
// Run (needs: npm i pagefind@1.3.0 node-html-parser@6.1.13 in the folder this script runs from):
//   SITE_ROOT=/path/to/repo node build-search.mjs
import * as pagefind from "pagefind";
import { parse } from "node-html-parser";
import fs from "node:fs";
import path from "node:path";

const ROOT = process.env.SITE_ROOT || process.cwd();
const SKIP = new Set(["404.html", "app.html", "new-home.html", "search.html", "google7ace57b56453d67a.html"]);
const DROP = "script,style,noscript,svg,template,header,footer,nav,aside,.ls-side,.crumbs,.pn,#waFloat,.wa-float,.byline,.share,.ytc-form,iframe,form";

function typeOf(f) {
  if (/^(gold|silver|dollar|bitcoin)-(rate|price)-pakistan|history|^usd-to-pkr/.test(f)) return "Rates";
  if (f.startsWith("lesson-")) return "Lessons";
  if (f.startsWith("smc-")) return "SMC course";
  if (f.startsWith("qa-") || f === "group-qa.html") return "Sawal Jawab";
  if (f.startsWith("guide-") || f === "forex-guide.html" || f === "forex-roadmap.html") return "Guides";
  if (/^(free-|simulator|trade-assistant|mt5-|qft-|tools|lot-size|calculator)|indicator|-mt5|-mt4|journal|calculator|replay|backtest-/.test(f) && !f.startsWith("lesson-")) return "Tools";
  if (f.startsWith("course-") || ["youtube.html", "forex-basics-course.html", "free-forex-course-price-action-batch.html"].includes(f)) return "Courses";
  return "Pages";
}

const clean = (t) => t.replace(/\s+/g, " ").trim();

const { index } = await pagefind.createIndex({ forceLanguage: "en" });
let n = 0;
for (const f of fs.readdirSync(ROOT).filter((x) => x.endsWith(".html")).sort()) {
  if (SKIP.has(f)) continue;
  const html = fs.readFileSync(path.join(ROOT, f), "utf8");
  if (/http-equiv=["']refresh/i.test(html) || /name=["']robots["'][^>]*noindex/i.test(html)) continue;
  const doc = parse(html);
  const tEl = doc.querySelector("title");
  if (!tEl) continue;
  const title = clean(tEl.text).replace(/\s*[|–-]\s*Qazi Forex Tips\s*$/i, "");
  const desc = doc.querySelector('meta[name="description"]')?.getAttribute("content") || "";
  const img = doc.querySelector('meta[property="og:image"]')?.getAttribute("content") || "";
  const body = doc.querySelector("main") || doc.querySelector("body") || doc;
  body.querySelectorAll(DROP).forEach((el) => el.remove());
  const h1 = clean(body.querySelector("h1")?.text || "");
  if (clean(body.text).length < 80) continue;
  body.querySelectorAll("h1").forEach((el) => el.remove());
  const url = f === "index.html" ? "/" : "/" + f;
  const esc = (t) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
  // Pagefind weights headings (h1 strongest), so the page name goes in the h1 and the page's H1 in an h2;
  // sub-headings keep their ids, so results can jump to the right section.
  const page = `<html lang="en"><body><main data-pagefind-body>` +
    `<span data-pagefind-ignore data-pagefind-filter="type">${esc(typeOf(f))}</span>` +
    `<span data-pagefind-ignore data-pagefind-meta="title">${esc(title || h1)}</span>` +
    (h1 ? `<span data-pagefind-ignore data-pagefind-meta="h1">${esc(h1)}</span>` : "") +
    (img ? `<span data-pagefind-ignore data-pagefind-meta="image">${esc(img.replace("https://qaziforextips.com", ""))}</span>` : "") +
    `<h1 data-pagefind-weight="10">${esc(title || h1)}</h1>` + (h1 && h1 !== title ? `<h2 data-pagefind-weight="6">${esc(h1)}</h2>` : "") +
    `<p>${esc(desc)}</p>${body.innerHTML}</main></body></html>`;
  const { errors } = await index.addHTMLFile({ url, content: page });
  if (errors.length) console.error(f, errors);
  n++;
}
await index.writeFiles({ outputPath: path.join(ROOT, "pagefind") });
await pagefind.close();
console.log("search index:", n, "pages");
