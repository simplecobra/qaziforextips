/* Live rates in the visitor's browser.
   The pages already carry the numbers written by the GitHub job (data/rates.json, for Google).
   This script fetches the newest Gold / Silver (gold-api.com) and Bitcoin (CoinGecko) prices when the
   page opens and every 2 minutes, and rewrites the numbers on the page. USD/PKR comes from data/rates.json
   (Twelve Data). If a source fails, the written numbers simply stay. */
(function () {
  var OZ = 31.1034768, TOLA = 11.6638038, KAR = [["24K", 24], ["22K", 22], ["21K", 21], ["18K", 18]];
  var page = (location.pathname.split("/").pop() || "index.html");
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var rs = function (v) { return "Rs " + Math.round(v).toLocaleString("en-US"); };
  var rs2 = function (v) { return "Rs " + v.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  var usd = function (v) { return "$" + v.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  var cr = function (v) { return "Rs " + (v / 1e7).toFixed(2) + " Cr"; };
  var pct = function (v) { return v == null || !isFinite(v) ? "" : (v >= 0 ? "▲ " : "▼ ") + Math.abs(v).toFixed(2) + "%"; };
  var cls = function (v) { return v >= 0 ? "up" : "down"; };
  var pkt = function (d) { return d.toLocaleString("en-GB", { timeZone: "Asia/Karachi", day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit", hour12: false }).replace(",", ",") + " PKT"; };
  function get(url) { return fetch(url, { cache: "no-store" }).then(function (r) { if (!r.ok) throw 0; return r.json(); }); }
  function cached(key, url) {
    try { var c = JSON.parse(sessionStorage.getItem(key) || "null"); if (c && Date.now() - c.t < 90000) return Promise.resolve(c.v); } catch (e) {}
    return get(url).then(function (v) { try { sessionStorage.setItem(key, JSON.stringify({ t: Date.now(), v: v })); } catch (e) {} return v; });
  }
  function ok(v, lo, hi) { return typeof v === "number" && v > lo && v < hi; }
  function setTime(when) {
    var t = $(".gr-time");
    if (t) t.innerHTML = t.innerHTML.replace(/Last update:[^·]*·/, "Last update: " + pkt(when) + " (live) ·");
  }
  function rows(html) { var tb = $(".gr-tbl tbody"); if (tb) tb.innerHTML = html; }

  function gold(R, g) {
    var pkr = R.usdpkr, pg = g * pkr / OZ, prevPg = (R.gold.usd_prev || g) * (R.usdpkr_prev || pkr) / OZ;
    var t24 = pg * TOLA, chg = t24 - prevPg * TOLA, chgP = R.gold.usd_prev ? (g / R.gold.usd_prev - 1) * 100 : 0;
    var big = $(".gr-big"); if (big) big.textContent = rs(t24);
    var c = $(".gr-card .gr-chg");
    if (c) { c.className = "gr-chg " + cls(chg); c.textContent = (chg >= 0 ? "+" : "−") + Math.abs(Math.round(chg)).toLocaleString("en-US") + " (" + pct(chgP) + ") vs previous close"; }
    var m = $(".gr-mini");
    if (m) m.innerHTML = '<div><i>10 gram (24K)</i><b>' + rs(pg * 10) + '</b></div><div><i>1 gram (24K)</i><b>' + rs(pg) + '</b></div><div><i>Gold / ounce</i><b>' + usd(g) + '</b></div><div><i>USD / PKR</i><b>' + pkr.toFixed(2) + '</b></div>';
    rows(KAR.map(function (k) { var f = k[1] / 24; return '<tr><th scope="row">' + k[0] + ' gold</th><td>' + rs(pg * f * TOLA) + '</td><td>' + rs(pg * f * 10) + '</td><td>' + rs(pg * f) + '</td><td>' + rs(pg * f * OZ) + '</td></tr>'; }).join(""));
    if (window.QFT_D) { window.QFT_D.g1 = {}; KAR.forEach(function (k) { window.QFT_D.g1[k[0]] = Math.round(pg * k[1] / 24); }); }
  }
  function silver(R, s) {
    var pkr = R.usdpkr, sg = s * pkr / OZ, tola = sg * TOLA;
    var big = $(".gr-big"); if (big) big.textContent = rs(tola);
    var c = $(".gr-card .gr-chg");
    if (c && R.silver && R.silver.tola) {
      var mm = /([+−-])([\d,]+)/.exec(c.textContent);
      if (mm) { var base = R.silver.tola - (mm[1] === "+" ? 1 : -1) * +mm[2].replace(/,/g, ""), d = Math.round(tola - base);
        c.className = "gr-chg " + cls(d); c.textContent = (d >= 0 ? "+" : "−") + Math.abs(d).toLocaleString("en-US") + " vs previous day"; }
    }
    var m = $(".gr-mini");
    if (m) m.innerHTML = '<div><i>10 gram</i><b>' + rs(sg * 10) + '</b></div><div><i>1 kg</i><b>' + rs(sg * 1000) + '</b></div><div><i>Silver / ounce</i><b>' + usd(s) + '</b></div><div><i>USD / PKR</i><b>' + pkr.toFixed(2) + '</b></div>';
    rows([["Pure silver (999)", 1], ["Sterling silver (925)", .925]].map(function (r) { var g = sg * r[1]; return '<tr><th scope="row">' + r[0] + '</th><td>' + rs(g * TOLA) + '</td><td>' + rs(g * 10) + '</td><td>' + rs2(g) + '</td><td>' + rs(g * 1000) + '</td><td>' + rs(g * OZ) + '</td></tr>'; }).join(""));
    var nisS = Math.round(tola * 52.5), nisG = Math.round(R.gold.karats["24K"].tola * 7.5);
    var n = $(".gr-nis");
    if (n) n.innerHTML = '<div><i>Silver nisab · 52.5 tola</i><b>' + rs(nisS) + '</b><span>612.36 g of pure silver</span></div><div><i>Gold nisab · 7.5 tola</i><b>' + rs(nisG) + '</b><span>87.48 g of 24K gold</span></div><div><i>Zakat on the silver nisab (2.5%)</i><b>' + rs(nisS * .025) + '</b><span>2.5% of ' + rs(nisS) + '</span></div>';
    if (window.QFT_D) { window.QFT_D.g1 = sg; window.QFT_D.nisS = nisS; }
  }
  function btc(R, b) {
    var p = b.pkr, big = $(".gr-big"); if (big) big.textContent = rs(p);
    var c = $(".gr-card .gr-chg");
    if (c && b.usd_24h_change != null) { c.className = "gr-chg " + cls(b.usd_24h_change); c.textContent = pct(b.usd_24h_change) + " in 24 hours · " + cr(p); }
    var cells = document.querySelectorAll(".gr-mini b"); if (cells[0]) cells[0].textContent = "$" + Math.round(b.usd).toLocaleString("en-US");
    rows([0.0001, 0.001, 0.01, 0.1, 0.5, 1].map(function (a) { return '<tr><th scope="row">' + a + ' BTC</th><td>' + rs(a * p) + '</td><td>' + usd(a * b.usd) + '</td></tr>'; }).join(""));
    if (window.QFT_D) { window.QFT_D.pkr = p; window.QFT_D.usd = b.usd; }
  }
  function home(R, g, s, b) {
    var box = document.querySelectorAll("#rates .lrate b"), sp = document.querySelectorAll("#rates .lrate span");
    if (g && box[0]) { box[0].textContent = rs(g * R.usdpkr / OZ * TOLA); if (R.gold.usd_prev && sp[0]) { var cp = (g / R.gold.usd_prev - 1) * 100; sp[0].className = cls(cp); sp[0].textContent = pct(cp); } }
    if (s && box[1]) { box[1].textContent = rs(s * R.usdpkr / OZ * TOLA); if (sp[1]) sp[1].textContent = usd(s) + "/oz"; }
    if (b && box[3]) { box[3].textContent = cr(b.pkr); if (sp[3] && b.usd_24h_change != null) { sp[3].className = cls(b.usd_24h_change); sp[3].textContent = pct(b.usd_24h_change); } }
  }
  function refire() { ["cW", "zW"].forEach(function (id) { var e = document.getElementById(id); if (e) e.dispatchEvent(new Event("input")); }); }

  function run() {
    var isGold = page === "gold-rate-pakistan.html", isSilver = page === "silver-rate-pakistan.html",
        isBtc = page === "bitcoin-price-pakistan.html", isHome = page === "index.html" || page === "";
    if (!(isGold || isSilver || isBtc || isHome)) return;
    get("data/rates.json?t=" + Math.floor(Date.now() / 120000)).then(function (R) {
      if (!R || !ok(R.usdpkr, 50, 2000)) return;
      var jobs = [
        (isGold || isSilver || isHome) ? cached("qftXAU", "https://api.gold-api.com/price/XAU").catch(function () { return null; }) : null,
        (isSilver || isHome) ? cached("qftXAG", "https://api.gold-api.com/price/XAG").catch(function () { return null; }) : null,
        (isBtc || isHome) ? cached("qftBTC", "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,pkr&include_24hr_change=true").catch(function () { return null; }) : null
      ];
      return Promise.all(jobs).then(function (a) {
        var g = a[0] && ok(+a[0].price, 500, 50000) ? +a[0].price : null;
        var s = a[1] && ok(+a[1].price, 1, 1000) ? +a[1].price : null;
        var b = a[2] && a[2].bitcoin && ok(a[2].bitcoin.pkr, 1e5, 1e11) ? a[2].bitcoin : null;
        var now = new Date(), done = false;
        if (isGold && g) { gold(R, g); done = true; }
        if (isSilver && s) { silver(R, s); done = true; }
        if (isBtc && b) { btc(R, b); done = true; }
        if (isHome) home(R, g, s, b);
        if (done) { setTime(now); refire(); }
      });
    }).catch(function () {});
  }
  run();
  setInterval(function () { if (!document.hidden) run(); }, 120000);
})();
