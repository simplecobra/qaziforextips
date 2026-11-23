/* Site search for qaziforextips.com (Pagefind index in /pagefind, rebuilt by .github/workflows/search.yml).
   Adds a search button to the header of every page (next to the light/dark button).
   Click it, or press Ctrl+K or "/", to search every lesson, SMC lesson, Sawal Jawab, guide, rate page and tool,
   in English, Roman Urdu or Urdu. Results are re-ranked so pages whose title or H1 matches the search come first. */
(function () {
  if (window.__qftSearch) return; window.__qftSearch = 1;
  var css = document.createElement("style");
  css.textContent =
    ".qs-btn{width:44px;height:44px;border-radius:8px;border:1px solid var(--line);background:transparent;color:var(--ink);cursor:pointer;display:grid;place-items:center;flex:none;margin-left:6px}" +
    ".qs-btn:hover{border-color:var(--gold)}.qs-btn svg{width:20px;height:20px}" +
    ".qs-ov{position:fixed;inset:0;z-index:9999;background:rgba(5,8,16,.72);backdrop-filter:blur(3px);display:none;align-items:flex-start;justify-content:center;padding:6vh 14px 14px}" +
    ".qs-ov.on{display:flex}" +
    ".qs-box{width:100%;max-width:780px;max-height:86vh;display:flex;flex-direction:column;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:16px;box-shadow:0 30px 80px rgba(0,0,0,.5);overflow:hidden}" +
    ".qs-head{padding:14px 16px 10px;border-bottom:1px solid var(--line)}" +
    ".qs-row{display:flex;gap:8px;align-items:center}" +
    ".qs-in{flex:1;min-width:0;padding:13px 14px 13px 42px;border:1px solid var(--line);border-radius:12px;background:var(--surface) no-repeat 13px 50%/18px url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23c4911f' stroke-width='2.4' stroke-linecap='round'%3E%3Ccircle cx='11' cy='11' r='7'/%3E%3Cpath d='m20 20-3.6-3.6'/%3E%3C/svg%3E\");color:var(--ink);font:500 17px var(--f-body);outline:none}" +
    ".qs-in:focus{border-color:var(--gold)}" +
    ".qs-x{border:1px solid var(--line);background:transparent;color:var(--ink);border-radius:10px;padding:11px 12px;cursor:pointer;font:600 13px var(--f-body);flex:none}" +
    ".qs-chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}" +
    ".qs-chip{border:1px solid var(--line);background:transparent;color:var(--muted);border-radius:999px;padding:5px 11px;font:600 13px var(--f-body);cursor:pointer}" +
    ".qs-chip.on{background:var(--gold);border-color:var(--gold);color:#1c1405}.qs-chip i{font-style:normal;opacity:.7;margin-left:4px}" +
    ".qs-body{overflow:auto;padding:6px 16px 12px}" +
    ".qs-info{font-size:14px;color:var(--muted);margin:10px 2px;line-height:1.6}.qs-info a{color:var(--gold)}" +
    ".qs-r{display:block;padding:12px 10px;border-radius:12px;text-decoration:none;color:var(--ink);border:1px solid transparent}" +
    ".qs-r:hover,.qs-r.sel{background:var(--surface);border-color:var(--line)}" +
    ".qs-t{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap;font:700 16.5px var(--f-body);line-height:1.35}" +
    ".qs-b{font:700 11px var(--f-body);letter-spacing:.6px;text-transform:uppercase;color:var(--gold);border:1px solid var(--line);border-radius:6px;padding:2px 6px;white-space:nowrap}" +
    ".qs-e{font-size:14px;color:var(--muted);line-height:1.6;margin-top:4px;unicode-bidi:plaintext}" +
    ".qs-e mark,.qs-s mark{background:rgba(231,185,79,.32);color:var(--ink);padding:0 2px;border-radius:3px}" +
    ".qs-s{display:block;font-size:13.5px;color:var(--muted);text-decoration:none;padding:3px 0 0 14px;border-left:2px solid var(--line);margin:6px 0 0 2px;unicode-bidi:plaintext}" +
    ".qs-s b{color:var(--ink);font-weight:600}.qs-s:hover b{color:var(--gold)}" +
    ".qs-more{display:block;margin:8px auto 4px;border:1px solid var(--line);background:transparent;color:var(--ink);border-radius:10px;padding:9px 16px;cursor:pointer;font:600 14px var(--f-body)}" +
    "@media(max-width:400px){.qs-btn{width:40px;height:40px;margin-left:0}}" +
    "@media(max-width:600px){.qs-ov{padding:2vh 6px 6px}.qs-box{max-height:94vh}.qs-head{padding:12px 10px 8px}.qs-body{padding:4px 8px 10px}}";
  document.head.appendChild(css);

  var icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/></svg>';
  var btn = document.createElement("button");
  btn.type = "button"; btn.className = "qs-btn"; btn.id = "qsBtn";
  btn.setAttribute("aria-label", "Search the website"); btn.title = "Search (Ctrl+K)"; btn.innerHTML = icon;
  var theme = document.getElementById("themeBtn");
  var wrap = document.querySelector("header .wrap") || document.querySelector("header");
  if (theme && theme.parentNode) theme.parentNode.insertBefore(btn, theme);
  else if (wrap) wrap.appendChild(btn);
  else { btn.style.cssText = "position:fixed;top:14px;right:14px;z-index:999;background:var(--surface,#151d30)"; document.body.appendChild(btn); }

  var TYPES = ["All", "Lessons", "SMC course", "Sawal Jawab", "Guides", "Rates", "Tools", "Courses", "Pages"];
  var ov = document.createElement("div");
  ov.className = "qs-ov"; ov.setAttribute("role", "dialog"); ov.setAttribute("aria-modal", "true"); ov.setAttribute("aria-label", "Search");
  ov.innerHTML = '<div class="qs-box"><div class="qs-head"><div class="qs-row"><input class="qs-in" type="search" autocomplete="off" ' +
    'placeholder="Search lessons, SMC, Sawal Jawab, rates, tools…" aria-label="Search the website"><button type="button" class="qs-x">Close ✕</button></div>' +
    '<div class="qs-chips"></div></div><div class="qs-body" aria-live="polite"></div></div>';
  document.body.appendChild(ov);
  var inp = ov.querySelector(".qs-in"), chips = ov.querySelector(".qs-chips"), out = ov.querySelector(".qs-body");
  var HELP = '<p class="qs-info">Search in English, Roman Urdu or Urdu, e.g. <i>order block</i>, <i>lot size kaise nikalein</i>, <i>آرڈر بلاک</i>, <i>gold rate 2010</i>.<br>' +
    'Tip: press <b>Ctrl+K</b> or <b>/</b> on any page to open search.</p>';
  var NONE = 'Not found? <a href="https://wa.me/923236700010" target="_blank" rel="noopener">Ask on WhatsApp</a> or ask the AI assistant (round button in the corner).';
  out.innerHTML = HELP;

  var pf = null, type = "All", all = [], shown = 0, seq = 0, sel = -1, gaLast = "", gaT = null;
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function words(q) { return q.toLowerCase().split(/[\s,.;:!?()"'\-]+/).filter(function (w) { return w.length > 1; }); }
  function bonus(q, d) {   // title / H1 match first: whole phrase, then all words, then some words
    var t = ((d.meta.title || "") + " " + (d.meta.h1 || "")).toLowerCase(), ql = q.toLowerCase().trim(), w = words(q), hit = 0;
    w.forEach(function (x) { if (t.indexOf(x) >= 0) hit++; });
    var b = 0;
    if (ql.length > 2 && t.indexOf(ql) >= 0) b += 40;
    if (w.length && hit === w.length) b += 20;
    return b + hit * 4;
  }
  function renderChips(counts) {
    chips.innerHTML = TYPES.filter(function (t) { return t === "All" || counts[t]; }).map(function (t) {
      return '<button type="button" class="qs-chip' + (t === type ? " on" : "") + '" data-t="' + t + '">' + t + '<i>' + (t === "All" ? counts.All : counts[t]) + "</i></button>";
    }).join("");
  }
  function item(d) {
    var subs = (d.sub_results || []).filter(function (s) { return s.url !== d.url && s.title !== d.meta.title; }).slice(0, 2);
    return '<a class="qs-r" href="' + esc(d.url) + '"><div class="qs-t">' + esc(d.meta.title || d.url) + '<span class="qs-b">' + esc((d.filters.type || [""])[0]) + "</span></div>" +
      '<div class="qs-e">' + d.excerpt + "</div></a>" +
      subs.map(function (s) { return '<a class="qs-s" href="' + esc(s.url) + '"><b>' + esc(s.title) + "</b> · " + s.excerpt + "</a>"; }).join("");
  }
  function list() { return all.filter(function (d) { return type === "All" || (d.filters.type || [])[0] === type; }); }
  function paint(reset) {
    var L = list();
    if (reset) shown = 0;
    shown = Math.min(L.length, shown + 10);
    out.innerHTML = L.length ? L.slice(0, shown).map(item).join("") + (shown < L.length ? '<button type="button" class="qs-more">Show more (' + (L.length - shown) + ")</button>" : "") +
      '<p class="qs-info">' + NONE + "</p>" : '<p class="qs-info">Nothing found for <b>' + esc(inp.value) + "</b>. " + NONE + "</p>";
    sel = -1;
  }
  async function run() {
    var q = inp.value.trim(), my = ++seq;
    if (q.length < 2) { all = []; chips.innerHTML = ""; out.innerHTML = HELP; return; }
    var r = await pf.debouncedSearch(q, {}, 220);
    if (!r || my !== seq) return;
    var data = await Promise.all(r.results.slice(0, 40).map(function (x, i) { return x.data().then(function (d) { d._s = x.score + bonus(q, d) - i * 0.01; return d; }); }));
    if (my !== seq) return;
    data.sort(function (a, b) { return b._s - a._s; });
    all = data;
    var counts = { All: data.length };
    data.forEach(function (d) { var t = (d.filters.type || ["Pages"])[0]; counts[t] = (counts[t] || 0) + 1; });
    if (type !== "All" && !counts[type]) type = "All";
    renderChips(counts); paint(true);
    clearTimeout(gaT);
    gaT = setTimeout(function () { if (q.length > 2 && q !== gaLast && window.gtag) { gaLast = q; window.gtag("event", "search", { search_term: q, results: data.length }); } }, 1500);
  }
  async function load() {
    if (pf) return;
    pf = await import("/pagefind/pagefind.js");
    await pf.options({ excerptLength: 22, ranking: { termSaturation: 1.2, pageLength: 0.3 } });
    pf.init();
  }
  function open(q) {
    ov.classList.add("on"); document.documentElement.style.overflow = "hidden";
    if (q) inp.value = q;
    setTimeout(function () { inp.focus(); inp.select(); }, 30);
    load().then(function () { if (inp.value.trim()) run(); });
  }
  function close() { ov.classList.remove("on"); document.documentElement.style.overflow = ""; }
  inp.addEventListener("input", function () { if (pf) run(); else load().then(run); });
  chips.addEventListener("click", function (e) { var b = e.target.closest(".qs-chip"); if (!b) return; type = b.getAttribute("data-t"); chips.querySelectorAll(".qs-chip").forEach(function (c) { c.classList.toggle("on", c === b); }); paint(true); });
  out.addEventListener("click", function (e) { if (e.target.closest(".qs-more")) paint(false); });
  btn.addEventListener("click", function () { open(); });
  ov.querySelector(".qs-x").addEventListener("click", close);
  ov.addEventListener("click", function (e) { if (e.target === ov) close(); });
  document.addEventListener("keydown", function (e) {
    var tag = (e.target && e.target.tagName) || "";
    if ((e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K")) { e.preventDefault(); open(); return; }
    if (e.key === "/" && !/INPUT|TEXTAREA|SELECT/.test(tag) && !e.target.isContentEditable) { e.preventDefault(); open(); return; }
    if (!ov.classList.contains("on")) return;
    if (e.key === "Escape") { close(); return; }
    var R = out.querySelectorAll(".qs-r");
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault(); if (!R.length) return;
      sel = e.key === "ArrowDown" ? Math.min(R.length - 1, sel + 1) : Math.max(0, sel - 1);
      R.forEach(function (x, i) { x.classList.toggle("sel", i === sel); }); R[sel].scrollIntoView({ block: "nearest" });
    } else if (e.key === "Enter" && e.target === inp) {
      var t = R[sel >= 0 ? sel : 0]; if (t) location.href = t.href;
    }
  });
  window.QFTSearch = { open: open, close: close };
  try { var q = new URLSearchParams(location.search).get("q"); if (q && document.body.getAttribute("data-search-page") === "1") open(q); } catch (e) {}
})();
