/* =====================================================================
   QFT FEEDBACK & REVIEWS – shared code for index.html, feedback.html,
   simulator.html and trade-assistant.html
   Reads approved feedback from the published Google Sheet ("Public" tab)
   plus any manual entries in content.js → testimonials, and sends the
   forms to the Google Form. Settings live in content.js → feedbackSystem.
   Each feedback belongs to one product: course, simulator or
   trade-assistant (empty = course). Nothing to edit here.
   ===================================================================== */
(function () {
  var MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

  /* products: key → short label (chips) and full name (cards, Sheet) */
  var PROD = {
    "course":          { label: "Courses",          name: "Course" },
    "simulator":       { label: "Replay Simulator", name: "QFT Replay Simulator" },
    "trade-assistant": { label: "Trade Assistant",  name: "QFT Trade Assistant" }
  };
  function prodKey(v) {
    v = String(v || "").toLowerCase();
    if (/simul|replay/.test(v)) return "simulator";
    if (/assist/.test(v)) return "trade-assistant";
    return "course";
  }

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function parseCSV(txt) {
    var rows = [], row = [], f = "", q = false;
    for (var i = 0; i < txt.length; i++) {
      var c = txt[i];
      if (q) { if (c === '"') { if (txt[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
      else if (c === '"') q = true;
      else if (c === ",") { row.push(f); f = ""; }
      else if (c === "\n" || c === "\r") { if (c === "\r" && txt[i + 1] === "\n") i++; row.push(f); rows.push(row); row = []; f = ""; }
      else f += c;
    }
    if (f !== "" || row.length) { row.push(f); rows.push(row); }
    return rows;
  }

  /* the Sheet writes M/D/YYYY h:mm:ss */
  function parseDate(ts) {
    var m = String(ts || "").match(/(\d{1,4})[\/\-.](\d{1,2})[\/\-.](\d{2,4})/); if (!m) return null;
    var a = +m[1], b = +m[2], c = +m[3], y, mo, d;
    if (m[1].length === 4) { y = a; mo = b; d = c; } else { y = c < 100 ? 2000 + c : c; if (a > 12) { d = a; mo = b; } else { mo = a; d = b; } }
    return { y: y, m: mo, d: d, label: MON[mo - 1] ? MON[mo - 1] + " " + y : "", sort: y * 10000 + mo * 100 + d };
  }

  function cleanBatch(b) { return String(b || "").replace(/^\s*batch\s*/i, "").trim(); }

  function stars(r) {
    r = Math.max(0, Math.min(5, parseInt(r, 10) || 0));
    return r ? '<div class="stars" aria-label="' + r + ' out of 5">' + "★★★★★".slice(0, r) + '<span style="opacity:.25">' + "★★★★★".slice(r) + "</span></div>" : "";
  }

  /* long feedback: show ~6 lines + "Read more" */
  var LONG = 280;
  if (!window.__qftMore) {
    window.__qftMore = 1;
    var st = document.createElement("style");
    st.textContent = ".tst p.clamp{display:-webkit-box;-webkit-line-clamp:6;-webkit-box-orient:vertical;overflow:hidden}" +
      ".tst .more{justify-self:start;background:none;border:0;padding:0;margin:-6px 0 0;color:var(--gold);font:inherit;font-weight:600;cursor:pointer}" +
      ".tst .who .note{display:block;margin-top:4px;color:var(--gold);font-weight:600}" +
      ".tst .tag{justify-self:start;font:600 11px/1 var(--f-mono);letter-spacing:1px;text-transform:uppercase;color:var(--gold);border:1px solid color-mix(in srgb,var(--gold) 45%,transparent);border-radius:20px;padding:5px 9px}";
    document.head.appendChild(st);
    document.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest(".tst .more"); if (!b) return;
      var p = b.previousElementSibling, open = p.classList.toggle("clamp");
      b.textContent = open ? "Read more" : "Show less"; b.setAttribute("aria-expanded", String(!open));
    });
  }

  /* card(t) shows a product tag for tool reviews; card(t, {noTag:true}) hides it (used on the product's own page) */
  function card(t, opt) {
    opt = opt && typeof opt === "object" && !Array.isArray(opt) ? opt : {};
    var long = String(t.text || "").length > LONG, tool = t.product && t.product !== "course";
    return '<figure class="tst" style="margin:0">' + (tool && !opt.noTag ? '<span class="tag">' + esc(PROD[t.product].name) + "</span>" : "") +
      stars(t.rating) + "<p" + (long ? ' class="clamp"' : "") + ">" + esc(t.text) + "</p>" +
      (long ? '<button type="button" class="more" aria-expanded="false">Read more</button>' : "") + '<figcaption class="who"><b>' + esc(t.name) + "</b>" +
      esc([t.city, !tool && t.batch && !t.note ? "Batch " + t.batch : "", t.date].filter(Boolean).join(" · ")) +
      (t.note ? '<span class="note">' + esc(t.note) + "</span>" : "") + "</figcaption></figure>";
  }

  /* cb(list, final) is called once with manual entries, then again when the Sheet arrives.
     product (optional) keeps only that product's feedback. */
  function load(S, cb, product) {
    var F = S.feedbackSystem || {}, notes = {};
    Object.keys(S.feedbackNotes || {}).forEach(function (n) { notes[n.trim().toLowerCase()] = S.feedbackNotes[n]; });
    var addNote = function (t) { t.note = notes[String(t.name || "").trim().toLowerCase()] || ""; return t; };
    var only = function (list) { list.forEach(addNote); return product ? list.filter(function (t) { return t.product === product; }) : list; };
    var manual = (S.testimonials || []).filter(function (t) { return t && t.text; }).map(function (t) {
      return { name: t.name || "", city: t.city || "", batch: cleanBatch(t.batch), rating: t.rating, text: t.text, date: t.date || "", product: prodKey(t.product), sort: 0 };
    });
    cb(only(manual.slice()), false);
    if (!F.publicCsv) return;
    fetch(F.publicCsv + "&t=" + Math.floor(Date.now() / 60000), { cache: "no-store" })
      .then(function (r) { return r.ok ? r.text() : ""; })
      .then(function (txt) {
        var rows = parseCSV(txt || ""); if (rows.length < 2) { cb(only(manual.slice()), true); return; }
        var h = rows[0].map(function (x) { return x.trim().toLowerCase(); }), ix = function (n) { return h.indexOf(n); };
        var live = rows.slice(1).map(function (r) {
          var d = parseDate(r[ix("timestamp")]);
          return { name: (r[ix("name")] || "").trim(), city: (r[ix("city")] || "").trim(), batch: cleanBatch(r[ix("batch")]), rating: r[ix("rating")],
                   text: (r[ix("feedback")] || "").trim(), date: d ? d.label : "", product: prodKey(r[ix("product")]), sort: d ? d.sort : 0 };
        }).filter(function (t) { return t.name && t.text.length >= 3; });
        live.sort(function (a, b) { return b.sort - a.sort; });
        cb(only(live.concat(manual)), true);
      })
      .catch(function () { cb(only(manual.slice()), true); });
  }

  function summary(list) {
    var rated = list.map(function (t) { return parseInt(t.rating, 10); }).filter(function (n) { return n >= 1 && n <= 5; });
    var avg = rated.length ? rated.reduce(function (a, b) { return a + b; }, 0) / rated.length : 0;
    return { count: list.length, rated: rated.length, avg: avg };
  }

  /* ids: { form, name, city, batch?, product? (select), text, allow, hp, send, err, ok }
     fixedProduct: product key when the form belongs to one product page */
  function attachForm(S, ids, waUrl, fixedProduct) {
    var F = S.feedbackSystem || {}, $ = function (k) { return ids[k] ? document.getElementById(ids[k]) : null; }, f = $("form");
    if (!f) return;
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if ($("hp") && $("hp").value) return;
      var name = $("name").value.trim(), text = $("text").value.trim(), rating = (f.querySelector('input[name="rating"]:checked') || {}).value || "";
      var err = !name ? "Please write your name." : !rating ? "Please choose a star rating." : text.length < 10 ? "Please write a few words of feedback." : "";
      $("err").textContent = err; $("err").hidden = !err; $("ok").hidden = true;
      if (err) return;
      var prod = fixedProduct || ($("product") ? $("product").value : "course");
      var allow = $("allow").checked, k = F.fields || {}, body = new URLSearchParams();
      body.append(k.name, name.slice(0, 80)); body.append(k.city, $("city").value.trim().slice(0, 60));
      body.append(k.batch, prod === "course" && $("batch") ? $("batch").value.trim().slice(0, 20) : "");
      body.append(k.rating, rating); body.append(k.text, text.slice(0, 1500)); body.append(k.allow, allow ? "YES" : "No");
      if (k.product) body.append(k.product, (PROD[prod] || PROD.course).name);
      var btn = $("send"), label = btn.textContent; btn.disabled = true; btn.textContent = "Sending…";
      fetch(F.formAction, { method: "POST", mode: "no-cors", body: body }).then(function () {
        $("ok").textContent = allow ? "Thank you, " + name + "! Your feedback has been received and will appear on the website in a few minutes."
                                    : "Thank you, " + name + "! Your feedback has been received. Only our team will see it.";
        $("ok").hidden = false; f.reset();
      }).catch(function () {
        $("err").innerHTML = 'Could not send right now. Please check your internet, or <a href="' + esc(waUrl) + '" target="_blank" rel="noopener">send it on WhatsApp</a>.'; $("err").hidden = false;
      }).then(function () { btn.disabled = false; btn.textContent = label; });
    });
  }

  /* Reviews section for a product page (simulator / trade-assistant).
     opt: { mount: element id, product: key, title, waUrl, max (default 6) } */
  function mountReviews(S, opt) {
    var box = document.getElementById(opt.mount); if (!box) return;
    var p = opt.product, P = PROD[p], max = opt.max || 6;
    box.innerHTML =
      '<div class="rv-head"><div class="rv-intro"><div class="eyebrow">User reviews</div><h2>' + esc(opt.title) + '</h2>' +
      '<p class="rv-sum" id="rvSum">Real reviews from traders who use the ' + esc(P.name) + ', shared with their permission.</p></div>' +
      '<div class="rv-actions"><button class="btn gold" type="button" id="rvOpen" aria-expanded="false" aria-controls="rvBox">Write a review</button>' +
      '<a class="btn" id="rvAll" href="feedback.html?about=' + p + '">All feedback</a></div></div>' +
      '<div class="rv-grid" id="rvList" hidden></div>' +
      '<p class="rv-empty" id="rvEmpty" hidden>No reviews yet. Already using the ' + esc(P.name) + '? Be the first to share your experience.</p>' +
      '<div class="rv-box" id="rvBox" hidden><form id="rvForm" novalidate>' +
        '<div class="rv-note full">Tell other traders how the software works for you: what helps, what could be better. Please do not write profit amounts or results.</div>' +
        '<div class="fld"><label for="rvName">Your name</label><input id="rvName" autocomplete="name" required></div>' +
        '<div class="fld"><label for="rvCity">City</label><input id="rvCity" autocomplete="address-level2"></div>' +
        '<fieldset class="fld rate full"><legend>Your rating</legend><div class="row">' +
          [5, 4, 3, 2, 1].map(function (n) { return '<input type="radio" name="rating" id="rv' + n + '" value="' + n + '"><label for="rv' + n + '" title="' + n + (n > 1 ? " stars" : " star") + '">★</label>'; }).join("") +
        '</div></fieldset>' +
        '<div class="fld full"><label for="rvText">Your review (English, Urdu or Roman Urdu)</label><textarea id="rvText" required></textarea></div>' +
        '<label class="chk full"><input type="checkbox" id="rvAllow"> I allow Qazi Forex Tips to show my name, city and review on the website.</label>' +
        '<p class="fb-err full" id="rvErr" role="alert" hidden></p>' +
        '<input type="text" id="rvHp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">' +
        '<div class="full"><button class="btn gold" type="submit" id="rvSend">Send review</button></div>' +
        '<p class="full fb-ok" id="rvOk" role="status" hidden></p>' +
      '</form></div>';
    var $ = function (id) { return document.getElementById(id); }, openB = $("rvOpen");
    function open(scroll) {
      $("rvBox").hidden = false; openB.setAttribute("aria-expanded", "true"); openB.hidden = true;
      if (scroll) $("rvBox").scrollIntoView({ behavior: "smooth", block: "start" });
      setTimeout(function () { $("rvName").focus({ preventScroll: true }); }, scroll ? 400 : 0);
    }
    openB.addEventListener("click", function () { open(false); });
    box.addEventListener("click", function (e) { if (e.target.closest && e.target.closest("[data-rv-open]")) { e.preventDefault(); open(true); } });
    if (/^#(review|reviews)$/.test(location.hash)) setTimeout(function () { box.scrollIntoView(); open(true); }, 300);

    load(S, function (list, final) {
      $("rvList").innerHTML = list.slice(0, max).map(function (t) { return card(t, { noTag: true }); }).join("");
      $("rvList").hidden = !list.length;
      $("rvEmpty").hidden = !(final && !list.length);
      var s = summary(list);
      if (s.rated) $("rvSum").textContent = s.avg.toFixed(1) + " ★ average from " + s.count + (s.count === 1 ? " review" : " reviews") + ". Real reviews, shared with permission.";
      $("rvAll").textContent = list.length > max ? "See all " + list.length + " reviews" : "All feedback";
    }, p);
    attachForm(S, { form: "rvForm", name: "rvName", city: "rvCity", text: "rvText", allow: "rvAllow", hp: "rvHp", send: "rvSend", err: "rvErr", ok: "rvOk" }, opt.waUrl || "", p);
  }

  window.QFTFeedback = { load: load, card: card, stars: stars, summary: summary, attachForm: attachForm, mountReviews: mountReviews, products: PROD, prodKey: prodKey, esc: esc };
})();
