/* =====================================================================
   QFT STUDENT FEEDBACK – shared code for index.html and feedback.html
   Reads approved feedback from the published Google Sheet ("Public" tab)
   plus any manual entries in content.js → testimonials, and sends the
   feedback form to the Google Form. Settings live in content.js →
   feedbackSystem. Nothing to edit here.
   ===================================================================== */
(function () {
  var MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

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

  function card(t) {
    return '<figure class="tst" style="margin:0">' + stars(t.rating) + "<p>" + esc(t.text) + '</p><figcaption class="who"><b>' + esc(t.name) + "</b>" +
      esc([t.city, t.batch ? "Batch " + t.batch : "", t.date].filter(Boolean).join(" · ")) + "</figcaption></figure>";
  }

  /* cb(list) is called once with manual entries, then again when the Sheet arrives */
  function load(S, cb) {
    var F = S.feedbackSystem || {};
    var manual = (S.testimonials || []).filter(function (t) { return t && t.text; }).map(function (t) {
      return { name: t.name || "", city: t.city || "", batch: cleanBatch(t.batch), rating: t.rating, text: t.text, date: t.date || "", sort: 0 };
    });
    cb(manual.slice(), false);
    if (!F.publicCsv) return;
    fetch(F.publicCsv + "&t=" + Math.floor(Date.now() / 60000), { cache: "no-store" })
      .then(function (r) { return r.ok ? r.text() : ""; })
      .then(function (txt) {
        var rows = parseCSV(txt || ""); if (rows.length < 2) { cb(manual.slice(), true); return; }
        var h = rows[0].map(function (x) { return x.trim().toLowerCase(); }), ix = function (n) { return h.indexOf(n); };
        var live = rows.slice(1).map(function (r) {
          var d = parseDate(r[ix("timestamp")]);
          return { name: (r[ix("name")] || "").trim(), city: (r[ix("city")] || "").trim(), batch: cleanBatch(r[ix("batch")]), rating: r[ix("rating")],
                   text: (r[ix("feedback")] || "").trim(), date: d ? d.label : "", sort: d ? d.sort : 0 };
        }).filter(function (t) { return t.name && t.text.length >= 3; });
        live.sort(function (a, b) { return b.sort - a.sort; });
        cb(live.concat(manual), true);
      })
      .catch(function () { cb(manual.slice(), true); });
  }

  function summary(list) {
    var rated = list.map(function (t) { return parseInt(t.rating, 10); }).filter(function (n) { return n >= 1 && n <= 5; });
    var avg = rated.length ? rated.reduce(function (a, b) { return a + b; }, 0) / rated.length : 0;
    return { count: list.length, rated: rated.length, avg: avg };
  }

  /* ids: { form, name, city, batch, text, allow, hp, send, err, ok }  */
  function attachForm(S, ids, waUrl) {
    var F = S.feedbackSystem || {}, $ = function (k) { return document.getElementById(ids[k]); }, f = $("form");
    if (!f) return;
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if ($("hp") && $("hp").value) return;
      var name = $("name").value.trim(), text = $("text").value.trim(), rating = (f.querySelector('input[name="rating"]:checked') || {}).value || "";
      var err = !name ? "Please write your name." : !rating ? "Please choose a star rating." : text.length < 10 ? "Please write a few words of feedback." : "";
      $("err").textContent = err; $("err").hidden = !err; $("ok").hidden = true;
      if (err) return;
      var allow = $("allow").checked, k = F.fields || {}, body = new URLSearchParams();
      body.append(k.name, name.slice(0, 80)); body.append(k.city, $("city").value.trim().slice(0, 60)); body.append(k.batch, $("batch").value.trim().slice(0, 20));
      body.append(k.rating, rating); body.append(k.text, text.slice(0, 1500)); body.append(k.allow, allow ? "YES" : "No");
      var btn = $("send"); btn.disabled = true; btn.textContent = "Sending…";
      fetch(F.formAction, { method: "POST", mode: "no-cors", body: body }).then(function () {
        $("ok").textContent = allow ? "Thank you, " + name + "! Your feedback has been received and will appear on the website in a few minutes."
                                    : "Thank you, " + name + "! Your feedback has been received. Only our team will see it.";
        $("ok").hidden = false; f.reset();
      }).catch(function () {
        $("err").innerHTML = 'Could not send right now. Please check your internet, or <a href="' + esc(waUrl) + '" target="_blank" rel="noopener">send it on WhatsApp</a>.'; $("err").hidden = false;
      }).then(function () { btn.disabled = false; btn.textContent = "Send feedback"; });
    });
  }

  window.QFTFeedback = { load: load, card: card, stars: stars, summary: summary, attachForm: attachForm, esc: esc };
})();
