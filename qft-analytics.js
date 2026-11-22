/* QFT Analytics: Google Analytics 4 + Microsoft Clarity (dono free).
   Yeh file qft-bot.js ke zariye har page par load hoti hai.
   GA4: analytics.google.com (account "Qazi Forex Tips")
   Clarity: clarity.microsoft.com (project "Qazi Forex Tips") */
(function () {
  if (window.__qftAnalytics) return;
  window.__qftAnalytics = true;
  if (/^(localhost|127\.|192\.168\.)/.test(location.hostname)) return;

  var GA_ID = "G-NZRYDEN9JM";
  var CLARITY_ID = "zhjlwnp031";

  // Google Analytics 4
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag("js", new Date());
  window.gtag("config", GA_ID);
  var g = document.createElement("script");
  g.async = true;
  g.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
  document.head.appendChild(g);

  // Microsoft Clarity (heatmaps + recordings)
  window.clarity = window.clarity || function () {
    (window.clarity.q = window.clarity.q || []).push(arguments);
  };
  var c = document.createElement("script");
  c.async = true;
  c.src = "https://www.clarity.ms/tag/" + CLARITY_ID;
  document.head.appendChild(c);

  // WhatsApp aur download clicks ko "lead" / "download" event ke taur par count karo
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
    if (!a) return;
    var href = a.getAttribute("href") || "";
    if (/wa\.me|whatsapp/i.test(href)) {
      window.gtag("event", "generate_lead", { method: "whatsapp", link_url: a.href });
      // qualify_lead pehle se GA4 mein "key event" hai, is liye WhatsApp leads Conversions mein foran dikhenge
      window.gtag("event", "qualify_lead", { method: "whatsapp", link_url: a.href });
    } else if (/\.(zip|ex5|ex4|mq5|mq4|exe|pdf)(\?|$)/i.test(href)) {
      window.gtag("event", "file_download_click", { link_url: a.href });
    }
  }, true);
})();
