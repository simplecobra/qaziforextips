/* =====================================================================
   QFT AI Assistant – website chat widget
   ---------------------------------------------------------------------
   - Pehle aap ki file "qft-bot-answers.txt" mein jawab dhoondta hai
     (muft, foran).
   - Na mile to Cloudflare Worker ke zariye Claude Haiku 5.5 se poochta hai.
   - WORKER_URL khali ho to sirf custom answers chalte hain, baqi sawal
     WhatsApp pe bhej diye jate hain.
   ===================================================================== */
(function () {
  "use strict";

  // ↓↓↓ Cloudflare Worker banne ke baad us ka link yahan paste karein ↓↓↓
  var WORKER_URL = "https://qft-bot.qazi-basit1.workers.dev/";
  // ↑↑↑

  var ANSWERS_FILE = "qft-bot-answers.txt";
  var MAX_WORDS_FOR_CUSTOM = 25;   // is se lambe sawal seedha AI ko jate hain
  var STORE_KEY = "qft-bot-chat";

  var WA = "923236700010";
  try { if (window.SITE && SITE.brand && SITE.brand.whatsapp) WA = SITE.brand.whatsapp.replace(/\D/g, ""); } catch (e) {}

  var WELCOME = "Assalam o Alaikum! Main **QFT Assistant** hoon.\nForex, Gold, Price Action, Risk Management ya hamare **free course** ke baare mein koi bhi sawal poochein.";
  var CHIPS = ["Course mein kya sikhaya jata hai?", "Naya batch kab shuru hoga?", "Kahan se shuru karun?", "Order Block kya hai?"];

  if (document.getElementById("qftBot")) return;

  /* ---------------- styles (site ke colors khud le leta hai) ---------------- */
  var css = document.createElement("style");
  css.textContent = [
    ".qb-btn{position:fixed;left:18px;bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:32;width:58px;height:58px;padding:0;border-radius:50%;border:0;cursor:pointer;",
    "background:var(--gold,#e7b94f);color:var(--gold-ink,#1c1405);display:grid;place-items:center;box-shadow:0 10px 30px rgba(0,0,0,.4);transition:transform .15s}",
    ".qb-btn:hover{transform:scale(1.07)}.qb-btn svg{width:28px;height:28px}",
    ".qb-btn .qb-ai{position:absolute;top:-4px;right:-6px;font:700 10px/1 var(--f-mono,monospace);background:var(--gold-ink,#1c1405);color:var(--gold,#e7b94f);padding:3px 5px;border-radius:5px;border:1.5px solid var(--gold,#e7b94f)}",
    ".qb-btn .qb-lbl{position:absolute;left:68px;top:50%;transform:translateY(-50%);white-space:nowrap;background:var(--surface,#151d30);color:var(--ink,#eef1f7);border:1px solid var(--line,#26304a);font:600 14px/1 var(--f-body,'Segoe UI',sans-serif);padding:8px 11px;border-radius:8px;opacity:0;pointer-events:none;transition:opacity .15s}",
    ".qb-btn:hover .qb-lbl,.qb-btn:focus-visible .qb-lbl{opacity:1}",
    ".qb-panel{position:fixed;left:18px;bottom:calc(88px + env(safe-area-inset-bottom,0px));z-index:33;width:min(390px,calc(100vw - 36px));height:min(580px,calc(100vh - 120px));",
    "display:flex;flex-direction:column;background:var(--surface,#151d30);color:var(--ink,#eef1f7);border:1px solid var(--line,#26304a);border-radius:16px;overflow:hidden;",
    "box-shadow:0 24px 70px rgba(0,0,0,.5);font-family:var(--f-body,'Segoe UI',sans-serif)}",
    ".qb-panel[hidden]{display:none}",
    "@media(max-width:560px){.qb-panel{left:8px;right:8px;width:auto;bottom:calc(8px + env(safe-area-inset-bottom,0px));height:min(82vh,calc(100vh - 16px))}}",
    ".qb-head{display:flex;align-items:center;gap:11px;padding:14px 14px 13px 16px;border-bottom:1px solid var(--line,#26304a);background:var(--bg2,#111829)}",
    ".qb-av{width:38px;height:38px;border-radius:50%;flex:none;display:grid;place-items:center;background:var(--gold,#e7b94f);color:var(--gold-ink,#1c1405);font:800 18px/1 var(--f-display,sans-serif)}",
    ".qb-ttl{flex:1;min-width:0}.qb-ttl b{display:block;font-size:16px;letter-spacing:.2px}.qb-ttl small{display:block;font-size:12.5px;color:var(--muted,#9aa4ba);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}",
    ".qb-x{background:none;border:0;color:var(--muted,#9aa4ba);font-size:26px;line-height:1;cursor:pointer;padding:4px 6px;border-radius:6px}.qb-x:hover{color:var(--ink,#eef1f7)}",
    ".qb-log{flex:1;overflow-y:auto;padding:16px 14px 6px;display:flex;flex-direction:column;gap:10px;scroll-behavior:smooth}",
    ".qb-m{max-width:88%;padding:10px 13px;border-radius:13px;font-size:15px;line-height:1.5;word-wrap:break-word;overflow-wrap:anywhere}",
    ".qb-m.bot{align-self:flex-start;background:var(--bg2,#111829);border:1px solid var(--line,#26304a);border-bottom-left-radius:4px}",
    ".qb-m.me{align-self:flex-end;background:var(--gold,#e7b94f);color:var(--gold-ink,#1c1405);border-bottom-right-radius:4px}",
    ".qb-m a{color:var(--gold,#e7b94f);font-weight:600;text-decoration:underline;text-underline-offset:2px}",
    ":root[data-theme=light] .qb-m.bot a{color:#7d5806}",
    ".qb-m ul{margin:4px 0;padding-left:20px}.qb-m li{margin:2px 0}.qb-m p{margin:0 0 6px}.qb-m p:last-child{margin:0}",
    ".qb-wa{display:inline-flex;align-items:center;gap:7px;margin-top:8px;padding:7px 12px;border-radius:8px;background:#25d366;color:#fff!important;text-decoration:none!important;font-weight:700;font-size:14px}",
    ".qb-dots{display:inline-flex;gap:4px;padding:4px 2px}.qb-dots i{width:7px;height:7px;border-radius:50%;background:var(--muted,#9aa4ba);animation:qbd 1s infinite}",
    ".qb-dots i:nth-child(2){animation-delay:.15s}.qb-dots i:nth-child(3){animation-delay:.3s}@keyframes qbd{0%,80%,100%{opacity:.25}40%{opacity:1}}",
    ".qb-chips{display:flex;flex-wrap:wrap;gap:7px;padding:2px 14px 10px}",
    ".qb-chip{border:1px solid var(--line,#26304a);background:transparent;color:var(--ink,#eef1f7);border-radius:16px;padding:7px 12px;font:14px/1.2 var(--f-body,sans-serif);cursor:pointer}",
    ".qb-chip:hover{border-color:var(--gold,#e7b94f);color:var(--gold,#e7b94f)}",
    ".qb-form{display:flex;gap:8px;align-items:flex-end;padding:10px 12px;border-top:1px solid var(--line,#26304a)}",
    ".qb-in{flex:1;resize:none;max-height:110px;min-height:44px;padding:11px 13px;border-radius:11px;border:1px solid var(--line,#26304a);background:var(--bg,#0d1220);color:var(--ink,#eef1f7);font:15px/1.4 var(--f-body,sans-serif);outline:none}",
    ".qb-in:focus{border-color:var(--gold,#e7b94f)}",
    ".qb-send{width:44px;height:44px;flex:none;border:0;border-radius:11px;background:var(--gold,#e7b94f);color:var(--gold-ink,#1c1405);cursor:pointer;display:grid;place-items:center}",
    ".qb-send:disabled{opacity:.45;cursor:default}.qb-send svg{width:20px;height:20px}",
    ".qb-foot{padding:0 14px 10px;font-size:11.5px;color:var(--muted,#9aa4ba);text-align:center}",
    ".qb-foot a{color:inherit}"
  ].join("");
  document.head.appendChild(css);

  /* ---------------- HTML ---------------- */
  var CHAT_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.4-4.9A8 8 0 1 1 21 12Z"/><path d="M8.5 11h.01M12 11h.01M15.5 11h.01" stroke-width="2.6"/></svg>';
  var SEND_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3.4 20.4 21 12 3.4 3.6 3.4 10l12.6 2-12.6 2z"/></svg>';

  var btn = document.createElement("button");
  btn.className = "qb-btn"; btn.id = "qftBot"; btn.type = "button";
  btn.setAttribute("aria-label", "Open QFT AI Assistant"); btn.setAttribute("aria-expanded", "false");
  btn.innerHTML = CHAT_ICON + '<span class="qb-lbl">Ask Qazi – AI se poochein</span><span class="qb-ai">AI</span>';

  var panel = document.createElement("div");
  panel.className = "qb-panel"; panel.hidden = true;
  panel.setAttribute("role", "dialog"); panel.setAttribute("aria-label", "QFT AI Assistant");
  panel.innerHTML =
    '<div class="qb-head"><div class="qb-av">Q</div><div class="qb-ttl"><b>QFT AI Assistant</b><small>Forex · Gold · Price Action · Free Course</small></div>' +
    '<button class="qb-x" type="button" aria-label="Close">&times;</button></div>' +
    '<div class="qb-log" aria-live="polite"></div>' +
    '<div class="qb-chips"></div>' +
    '<form class="qb-form"><textarea class="qb-in" rows="1" maxlength="1000" placeholder="Apna sawal likhein…" aria-label="Your question"></textarea>' +
    '<button class="qb-send" type="submit" aria-label="Send">' + SEND_ICON + '</button></form>' +
    '<div class="qb-foot">Sirf taleem ke liye · signals nahi · <a href="https://wa.me/' + WA + '" target="_blank" rel="noopener">Team se WhatsApp</a></div>';

  document.body.appendChild(panel);
  document.body.appendChild(btn);

  var log = panel.querySelector(".qb-log"), chips = panel.querySelector(".qb-chips");
  var form = panel.querySelector(".qb-form"), input = panel.querySelector(".qb-in"), send = panel.querySelector(".qb-send");

  /* ---------------- state ---------------- */
  var history = [];   // [{role, content}]
  try { history = JSON.parse(sessionStorage.getItem(STORE_KEY) || "[]") || []; } catch (e) { history = []; }
  function save() { try { sessionStorage.setItem(STORE_KEY, JSON.stringify(history.slice(-20))); } catch (e) {} }

  var answers = null, answersLoading = null;
  function loadAnswers() {
    if (answers) return Promise.resolve(answers);
    if (!answersLoading) {
      answersLoading = fetch(ANSWERS_FILE + "?v=" + Math.floor(Date.now() / 300000))
        .then(function (r) { return r.ok ? r.text() : ""; })
        .then(function (t) { answers = parseAnswers(fill(t)); return answers; })
        .catch(function () { answers = []; return answers; });
    }
    return answersLoading;
  }

  /* ---------------- batch schedule (har mahine khud update) ----------------
     Admission har mahine 25 ko khulte hain, agle mahine 1 tareekh shaam 5 baje band,
     naya batch 1 tareekh se. BATCH_BASE = jo batch 1 December 2026 ko shuru hua. */
  var BATCH_BASE = { num: 66, year: 2026, month: 11 };   // month: 0 = Jan … 11 = Dec
  var MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"];
  function batchInfo(ms) {
    var d = new Date(ms + 5 * 3600000);                       // Pakistan time (UTC+5)
    var y = d.getUTCFullYear(), m = d.getUTCMonth(), day = d.getUTCDate(), h = d.getUTCHours();
    var sy = y, sm = m, open;
    if (day === 1 && h < 17) { open = true; }                  // 1 tareekh, shaam 5 se pehle
    else { sm = m + 1; if (sm > 11) { sm = 0; sy++; } open = day >= 25; }
    var num = BATCH_BASE.num + (sy - BATCH_BASE.year) * 12 + (sm - BATCH_BASE.month);
    var om = sm === 0 ? 11 : sm - 1;
    var info = { BATCH: num, RUNNING: num - 1, START: "1 " + MONTHS[sm] + " " + sy,
      OPEN_DATE: "25 " + MONTHS[om], CLOSE: "1 " + MONTHS[sm] + " shaam 5 baje" };
    info.STATUS = open
      ? "Is waqt Batch-" + num + " ke admission **khule hain** – " + info.CLOSE + " tak, ya seats poori hone tak."
      : "Is waqt admission **band hain**. Batch-" + num + " ke admission **" + info.OPEN_DATE + "** ko khulenge aur " + info.CLOSE + " tak khule rahenge.";
    return info;
  }
  function fill(text) {
    var b = batchInfo(Date.now());
    return text.replace(/\{(BATCH|RUNNING|START|OPEN_DATE|CLOSE|STATUS)\}/g, function (_, k) { return b[k]; });
  }

  /* ---------------- custom answers ---------------- */
  function norm(s) {
    try { return (" " + s.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").replace(/\s+/g, " ").trim() + " "); }
    catch (e) { return (" " + s.toLowerCase().replace(/[^a-z0-9\u0600-\u06ff\u0900-\u097f]+/g, " ").replace(/\s+/g, " ").trim() + " "); }
  }
  function parseAnswers(text) {
    var out = [], cur = null, inA = false;
    text.split(/\r?\n/).forEach(function (line) {
      var t = line.trim();
      if (t.charAt(0) === "#") return;
      if (/^Q:/i.test(t)) {
        if (cur && cur.answer) out.push(cur);
        cur = { keys: t.slice(2).split("|").map(function (k) { return norm(k).trim(); }).filter(function (k) { return k.length >= 4; }), answer: "" };
        inA = false; return;
      }
      if (/^LINK:/i.test(t)) { inA = false; return; }
      if (cur && /^A:/i.test(t)) { cur.answer = t.slice(2).trim(); inA = true; return; }
      if (cur && inA) {
        if (!t) { inA = false; return; }
        cur.answer += "\n" + t;
      }
    });
    if (cur && cur.answer) out.push(cur);
    return out;
  }
  function findCustom(q) {
    if (!answers || !answers.length) return null;
    if (q.split(/\s+/).length > MAX_WORDS_FOR_CUSTOM) return null;
    var nq = norm(q), best = null, bestScore = 0;
    answers.forEach(function (a) {
      a.keys.forEach(function (k) {
        if (nq.indexOf(" " + k + " ") !== -1 && k.length > bestScore) { best = a; bestScore = k.length; }
      });
    });
    return best ? best.answer : null;
  }

  /* ---------------- safe text → HTML ---------------- */
  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function inline(s) {
    s = esc(s);
    s = s.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, function (_, t, u) {
      var ext = u.indexOf("qaziforextips.com") === -1;
      return '<a href="' + u + '"' + (ext ? ' target="_blank" rel="noopener"' : "") + ">" + t + "</a>";
    });
    s = s.replace(/(^|[\s(])(https?:\/\/[^\s<)]+)/g, '$1<a href="$2" target="_blank" rel="noopener">$2</a>');
    s = s.replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");
    return s;
  }
  function render(text) {
    var html = "", list = false;
    text.split(/\n/).forEach(function (line) {
      var m = line.match(/^\s*(?:[-*•]|\d+[.)])\s+(.*)$/);
      if (m) { if (!list) { html += "<ul>"; list = true; } html += "<li>" + inline(m[1]) + "</li>"; return; }
      if (list) { html += "</ul>"; list = false; }
      if (line.trim()) html += "<p>" + inline(line.trim()) + "</p>";
    });
    if (list) html += "</ul>";
    return html;
  }

  /* ---------------- UI helpers ---------------- */
  function bubble(role, text, extraHtml) {
    var d = document.createElement("div");
    d.className = "qb-m " + (role === "user" ? "me" : "bot");
    if (role === "user") d.textContent = text; else d.innerHTML = render(text) + (extraHtml || "");
    log.appendChild(d); log.scrollTop = log.scrollHeight;
    return d;
  }
  function waButton(question) {
    var msg = "Assalam o Alaikum, mera sawal hai: " + (question || "");
    return '<a class="qb-wa" href="https://wa.me/' + WA + "?text=" + encodeURIComponent(msg) + '" target="_blank" rel="noopener">WhatsApp pe poochein</a>';
  }
  function typing() {
    var d = document.createElement("div");
    d.className = "qb-m bot"; d.innerHTML = '<span class="qb-dots"><i></i><i></i><i></i></span>';
    log.appendChild(d); log.scrollTop = log.scrollHeight; return d;
  }
  function drawChips() {
    chips.innerHTML = "";
    if (history.some(function (m) { return m.role === "user"; })) { chips.hidden = true; return; }
    chips.hidden = false;
    CHIPS.forEach(function (c) {
      var b = document.createElement("button"); b.type = "button"; b.className = "qb-chip"; b.textContent = c;
      b.onclick = function () { ask(c); }; chips.appendChild(b);
    });
  }
  function drawAll() {
    log.innerHTML = ""; bubble("assistant", WELCOME);
    history.forEach(function (m) { bubble(m.role, m.content); });
    drawChips();
  }

  /* ---------------- ask ---------------- */
  var busy = false;
  function ask(q) {
    q = (q || "").trim(); if (!q || busy) return;
    busy = true; send.disabled = true; chips.hidden = true;
    bubble("user", q); history.push({ role: "user", content: q }); save();
    input.value = ""; autosize();
    var t = typing();

    loadAnswers().then(function () {
      var custom = findCustom(q);
      if (custom) {
        if (WORKER_URL) {   // sirf record ke liye – is ka koi API kharcha nahi
          try { fetch(WORKER_URL, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ log: "custom", q: q }), keepalive: true }).catch(function () {}); } catch (e) {}
        }
        return { text: custom };
      }
      if (!WORKER_URL) return { text: "Is sawal ka behtar jawab hamari team WhatsApp pe degi.", wa: true };
      return fetch(WORKER_URL, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: history.slice(-10) })
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (d) {
          if (r.ok && d.reply) {
            var needWa = /\[WA\]/.test(d.reply);                     // AI ne kaha: team se rabta behtar hai
            return { text: d.reply.replace(/\s*\[WA\]\s*/g, " ").trim(), wa: needWa };
          }
          if (r.status === 429) return { text: d.code === "site_limit"
            ? "Aaj AI Assistant ki limit poori ho gayi hai. Apna sawal WhatsApp pe bhej dein."
            : "Aaj ke aap ke AI sawalon ki limit poori ho gayi hai. Kal dobara poochein, ya abhi WhatsApp pe rabta karein.", wa: true };
          return { text: "Maazrat, abhi jawab nahi aa saka. Thori dair baad try karein ya WhatsApp pe poochein.", wa: true, fail: true };
        });
      }).catch(function () {
        return { text: "Internet ka masla lag raha hai. Dobara try karein ya WhatsApp pe poochein.", wa: true, fail: true };
      });
    }).then(function (res) {
      t.remove();
      bubble("assistant", res.text, res.wa ? waButton(q) : "");
      if (!res.fail) { history.push({ role: "assistant", content: res.text }); }
      else { history.pop(); }   // fail hua sawal history se nikal dein taake agla sawal theek jaye
      save();
    }).then(function () { busy = false; send.disabled = false; input.focus(); });
  }

  function autosize() { input.style.height = "auto"; input.style.height = Math.min(input.scrollHeight, 110) + "px"; }

  /* ---------------- events ---------------- */
  function open() {
    panel.hidden = false; btn.setAttribute("aria-expanded", "true");
    if (!log.childNodes.length) drawAll();
    loadAnswers();
    setTimeout(function () { input.focus(); }, 50);
  }
  function close() { panel.hidden = true; btn.setAttribute("aria-expanded", "false"); btn.focus(); }

  btn.addEventListener("click", function () { panel.hidden ? open() : close(); });
  panel.querySelector(".qb-x").addEventListener("click", close);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) close(); });
  form.addEventListener("submit", function (e) { e.preventDefault(); ask(input.value); });
  input.addEventListener("input", autosize);
  input.addEventListener("keydown", function (e) { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); ask(input.value); } });

  // WhatsApp menu ke saath takraao na ho: chat khulay to WA menu band
  btn.addEventListener("click", function () { var w = document.querySelector(".wam"); if (w) w.hidden = true; });

  // test ke liye
  window.QFTBot = { parse: parseAnswers, find: function (q) { return findCustom(q); }, render: render, batch: batchInfo, fill: fill };
})();
