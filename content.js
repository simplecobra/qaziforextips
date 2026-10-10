/* =====================================================================
   QAZI FOREX TIPS – WEBSITE CONTENT
   ---------------------------------------------------------------------
   Website ki saari likhai, videos aur software ISI AIK FILE mein hain.
   Design ko haath lagane ki zaroorat nahi.

   USOOL:
   - Har cheez  "  "  (double quotes) ke andar likhein.
   - Har item ke baad comma  ,  lagayein (aakhri ke baad bhi chalega).
   - Kuch hatana ho to poori { ... } line(s) delete kar dein.
   - Save karne ke baad 1-2 minute mein website par nazar aata hai.
   ===================================================================== */

window.SITE = {

  /* ---------- 1. AAP KI MALOOMAT ---------- */
  brand: {
    name: "Qazi Forex Tips",
    tagline: "Gold, Price Action & Risk Management – in Urdu",
    whatsapp: "+92-323-6700010",
    youtube: "",          // apne channel ka link, e.g. "https://www.youtube.com/@..."
    facebook: "",         // Facebook group / page ka link
    email: ""             // agar ho
  },

  /* ---------- 2. SHURU KA HISSA (HERO) ---------- */
  hero: {
    title: "Learn to trade like a professional.",
    urdu: "پروفیشنل ٹریڈر کی طرح ٹریڈنگ سیکھیں",
    text: "Price action, Gold (XAUUSD) analysis, risk and money management – explained in Urdu, with tools built for MetaTrader 5."
  },

  /* ---------- 3. SOFTWARE, EA, INDICATORS ----------
     NAYA SOFTWARE DAALNA: neeche wala aik { ... } block copy karein,
     paste karein, aur likhai badal dein.
       type:   "Software" ya "EA" ya "Indicator"
       badge:  "NEW" / "UPDATED" ya "" (khali)
       image:  "naam.jpg" (tasveer bhi isi jagah upload karein) ya "" (khali)
       link:   is ki apni page ka link, ya "" (to button WhatsApp kholega)        */
  tools: [
    {
      name: "QFT Replay Simulator",
      type: "Software",
      badge: "v3.01",
      text: "MT5 market replay and manual backtesting with Prop Firm Challenge mode and a professional backtest report.",
      points: ["Replay any day, candle by candle", "Risk in $ – lot follows your SL", "Money management plan from your results"],
      image: "simulator.jpg",
      link: "simulator.html",
      button: "See the simulator"
    },
    {
      name: "QFT Trade Assistant",
      type: "EA",
      badge: "",
      text: "Risk management trade panel for MT5: set risk in money or %, drag SL / TP lines, the lot size is calculated for you.",
      points: ["Lot size from your risk", "SL / TP lines on the chart", "One-click orders"],
      image: "",
      link: "",
      button: "Ask on WhatsApp"
    },
    {
      name: "QFT Smart DCA EA",
      type: "EA",
      badge: "",
      text: "Dollar-cost averaging EA with hedge-lock protection for MT5. For experienced traders who understand the risk of averaging.",
      points: ["Universal: any symbol", "Hedge-lock protection", "Basket profit target"],
      image: "",
      link: "",
      button: "Ask on WhatsApp"
    }
  ],

  /* ---------- 4. YOUTUBE VIDEOS ----------
     NAYI VIDEO DAALNA: sirf title aur YouTube ka link likhein.
     Tasveer (thumbnail) website khud YouTube se le leti hai.
     Nayi video sab se UPAR likhein.
       topic: "Gold" / "Price Action" / "Risk Management" / "Psychology" / "Tools"   */
  videos: [
    // { title: "QFT Replay Simulator – complete tutorial", link: "https://www.youtube.com/watch?v=XXXXXXXXXXX", topic: "Tools" },
  ],

  /* ---------- 5. HUM KYA SIKHATE HAIN ---------- */
  topics: [
    { name: "Price Action", text: "Support and resistance, market structure, candle behaviour – reading the chart without indicator overload." },
    { name: "Gold (XAUUSD)", text: "How Gold moves around sessions and news, and how to plan trades on it." },
    { name: "Risk & Money Management", text: "Position size, risk per trade, daily stops and building a plan that survives losing streaks." },
    { name: "Trading Psychology", text: "Discipline, patience and the habits that keep an account alive." }
  ],

  /* ---------- 6. NEECHE KI LINE (FOOTER) ---------- */
  disclaimer: "Trading forex and gold involves high risk. Content is for education only and is not financial advice. Past or backtest results do not guarantee future results."
};
