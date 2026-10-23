/* WhatsApp menu: the round WhatsApp button opens a short "What do you need?" list.
   Each choice opens WhatsApp with a ready message, so the team knows at once what the visitor wants.
   To change the choices or messages, edit the list below. Without JavaScript the button still opens WhatsApp. */
(function () {
  var btn = document.getElementById("waFloat"); if (!btn) return;
  var num = "923236700010";
  try { if (window.SITE && SITE.brand && SITE.brand.whatsapp) num = SITE.brand.whatsapp.replace(/\D/g, ""); } catch (e) {}
  var page = (document.querySelector("h1") || {}).textContent || document.title;
  var ITEMS = [
    ["Join a student batch", "Assalam o Alaikum, I want to join the next student batch. Please share the details."],
    ["QFT Trade Assistant (MT5 / MT4)", "Assalam o Alaikum, I want to know about QFT Trade Assistant for MT5 / MT4."],
    ["QFT Replay Simulator", "Assalam o Alaikum, I want to know about QFT Replay Simulator."],
    ["Expert Advisor (EA)", "Assalam o Alaikum, I want to ask about an Expert Advisor (EA)."],
    ["A question about this page", "Assalam o Alaikum, I have a question about: " + page.trim().slice(0, 90) + " (" + location.href.split("#")[0] + ")"],
    ["Something else", "Assalam o Alaikum, I need help with: "]
  ];
  var css = document.createElement("style");
  css.textContent =
    ".wam{position:fixed;right:18px;bottom:calc(88px + env(safe-area-inset-bottom,0px));z-index:31;width:min(320px,calc(100vw - 36px));" +
    "background:var(--surface,#151d30);color:var(--ink,#eef1f7);border:1px solid var(--line,#26304a);border-radius:14px;" +
    "box-shadow:0 18px 50px rgba(0,0,0,.45);padding:14px;font-family:var(--f-body,sans-serif)}" +
    ".wam[hidden]{display:none}" +
    ".wam .wh{margin:2px 4px 10px;font:700 17px/1.2 var(--f-body,sans-serif);color:var(--ink,#eef1f7)}" +
    ".wam .wh small{display:block;font-weight:400;font-size:13px;color:var(--muted,#9aa4ba);margin-top:3px}" +
    ".wam a{display:flex;align-items:center;gap:10px;padding:11px 12px;border-radius:9px;text-decoration:none;color:inherit;font-size:16px;border:1px solid transparent}" +
    ".wam a:hover,.wam a:focus-visible{border-color:#25d366;background:rgba(37,211,102,.08);outline:none}" +
    ".wam a::before{content:'';flex:0 0 8px;height:8px;border-radius:50%;background:#25d366}" +
    ".wam .wx{position:absolute;top:8px;right:10px;background:none;border:0;color:var(--muted,#9aa4ba);font-size:22px;line-height:1;cursor:pointer;padding:4px}";
  document.head.appendChild(css);
  var box = document.createElement("div");
  box.className = "wam"; box.id = "waMenu"; box.hidden = true;
  box.setAttribute("role", "dialog"); box.setAttribute("aria-label", "Chat on WhatsApp");
  box.innerHTML = '<button class="wx" type="button" aria-label="Close">×</button><p class="wh">What do you need?<small>Our team replies on WhatsApp in Urdu, Hindi or English.</small></p>';
  ITEMS.forEach(function (it) {
    var a = document.createElement("a");
    a.href = "https://wa.me/" + num + "?text=" + encodeURIComponent(it[1]);
    a.target = "_blank"; a.rel = "noopener"; a.textContent = it[0];
    a.addEventListener("click", close);
    box.appendChild(a);
  });
  document.body.appendChild(box);
  btn.setAttribute("aria-haspopup", "dialog"); btn.setAttribute("aria-expanded", "false"); btn.setAttribute("aria-controls", "waMenu");
  function open() { box.hidden = false; btn.setAttribute("aria-expanded", "true"); box.querySelector("a").focus(); }
  function close() { box.hidden = true; btn.setAttribute("aria-expanded", "false"); }
  btn.addEventListener("click", function (e) { e.preventDefault(); box.hidden ? open() : close(); });
  box.querySelector(".wx").addEventListener("click", function () { close(); btn.focus(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !box.hidden) { close(); btn.focus(); } });
  document.addEventListener("click", function (e) { if (!box.hidden && !box.contains(e.target) && !btn.contains(e.target)) close(); });
})();
