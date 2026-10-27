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
    tagline: "Gold, Price Action & Risk Management – in Urdu & Hindi",
    whatsapp: "+92-323-6700010",
    youtube: "https://www.youtube.com/@QaziForexTips",
    facebook: "https://www.facebook.com/groups/qaziforextips",
    email: ""             // agar ho
  },

  /* ---------- 2. SHURU KA HISSA (HERO) ---------- */
  hero: {
    title: "Free Forex & Gold Trading Course in Urdu & Hindi",
    urdu: "پروفیشنل ٹریڈر کی طرح ٹریڈنگ سیکھیں",
    text: "Price action, Gold (XAUUSD) analysis, risk and money management – explained in Urdu and Hindi, with tools built for MetaTrader 5 and 4."
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
      badge: "v3.04",
      text: "MT5 market replay and manual backtesting with Prop Firm Challenge mode and a professional backtest report.",
      points: ["Replay any day, candle by candle", "Risk in $ – lot follows your SL", "Money management plan from your results"],
      image: "simulator.jpg",
      link: "simulator.html",
      button: "See the simulator"
    },
    {
      name: "QFT Trade Assistant",
      type: "EA",
      badge: "v3.13",
      text: "Risk management trade panel for MT5 and MT4: set risk in money or %, drag Entry / SL / TP lines, the lot size is calculated for you.",
      points: ["Lot size from your risk", "Drag Entry / SL / TP on the chart", "One-click market & pending orders"],
      image: "",
      link: "trade-assistant.html",
      button: "See the Trade Assistant"
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

  /* ---------- WHAT'S NEW (updates.html + home patti + software pages) ----------
     updates:  sab se NAYI sab se UPAR. date "2026-10-14" (pata ho) ya "" (na pata ho, tab version dikhta hai).
               type: "new" / "improved" / "fixed".   products: "simulator", "trade-assistant", "courses", "website".
     announce: home page ki chhoti patti. Sirf 1 khabar. "until" ke baad khud chhup jati hai.
               Nayi khabar par "id" zaroor badlein (warna jis ne band ki thi usay nazar nahi aayegi).
     versions: Simulator / Trade Assistant pages par "Version history". Naya version = list mein sab se upar 1 line. */
  announce: {
    id: "sim-304",
    text: "QFT Replay Simulator 3.04: start a prop firm challenge at any moment, indicators on all charts, Save as.",
    link: "simulator.html#new", linkText: "See what's new",
    until: "2026-12-31"
  },

  updates: [
    { date: "2026-10-27", type: "new", products: ["simulator"],
      title: "Replay Simulator 3.04: Prop Firm Challenge from the simulator window",
      text: "Start a prop firm challenge at any moment of the replay with the new Prop Firm button, using ready rules (2-Step Phase 1 and 2, 1-Step, Instant funding) or your own, and show, hide, stop or restart it without leaving the replay. Indicators added on one replay chart now appear on all replay charts (MT5). Save Simulation lets you pick the folder and name, and Load opens a .qsim file from any folder, so you can share a replay with students. New BUY / SELL buttons with the price. Installed simulators update from Main Menu; your licence, data and saved simulations stay.",
      link: "simulator.html#new", linkText: "See what's new" },
    { date: "2026-10-23", type: "new", products: ["trade-assistant"],
      title: "Trade Assistant 3.13: compact view, Start here help and 2 ICT strategies",
      text: "Version 3.13 for MT5 and MT4 adds a compact view (only risk, lot, Lines and Sell / Buy, made for scalping and small screens), a 3-step Start here help for new users, a risk box that turns yellow above 2% and red above 5% of your balance, and two ICT strategies in Signals: ICT OTE 79% and the ICT 2022 Model. New Best button keeps only the strategies that beat break-even on your chart, and Use setup copies a signal's Entry, SL and TP to the Trade tab for you to check. Navy Blue is the new default theme. Installed panels update themselves; new users can download 3.13.",
      link: "trade-assistant.html#new", linkText: "See what's new" },
    { date: "2026-10-22", type: "new", products: ["courses", "website"],
      title: "Free course pages and the Forex Guide (Urdu & Hindi)",
      text: "Each free course now has its own page with every lecture in order: Price Action Mastery Basic (11 lectures), Advance (9) and Trading Strategies (10). The new Forex Guide explains pips, leverage, spread, risk:reward, Smart Money Concepts, Gold, MT4 vs MT5 and prop firm challenges, with diagrams and a Roman Urdu / Hindi summary.",
      link: "course-price-action-basic.html", linkText: "Start the basic course" },
    { date: "2026-10-21", type: "new", products: ["simulator"],
      title: "Replay Simulator for MetaTrader 4 is released (version 3.03)",
      text: "The QFT Replay Simulator now runs on MetaTrader 4 too, with the same tools as MT5 3.03: market replay with Prev Bar, Prop Firm Challenge mode and dashboard, lot size from your $ risk, the Smart Panel, sessions and killzones, drawings sync and the full backtest report. Download the MT4 zip from the Simulator page. MT4 differences: the replay runs on an offline chart, data comes from M1 history (History Center) or a CSV file because MT4 has no tick history, and there are no news lines because MT4 has no economic calendar. Each MT4 account needs its own licence key.",
      link: "simulator.html#download", linkText: "Download for MT4" },
    { date: "2026-10-20", type: "new", products: ["website"],
      title: "Lesson notes: 54 lessons with video, written notes and questions",
      text: "54 of our lectures now have their own page with the video, the rules in writing, common mistakes, a short Roman Urdu summary and the questions traders ask most: price action basics, market analysis, chart patterns, strategies, risk and lot size, and platform and broker guides.",
      link: "youtube.html#lessons", linkText: "Read the lessons" },
    { date: "2026-10-18", type: "fixed", products: ["simulator"],
      title: "Replay Simulator 3.03 is out: please download or update now",
      text: "Version 3.03 fixes a problem in 3.02: the simulator window could open empty after the simulator was attached to a chart again, the chart timeframe was changed or a template was applied. It keeps everything new in 3.02 (Smart Panel, clean start, zoomed-out charts). Download the new version from the Simulator page, or in the simulator open Main Menu → Updates → Update now, then restart MetaTrader 5. Your licence, data and settings stay.",
      link: "simulator.html#download", linkText: "Download 3.03" },
    { date: "2026-10-18", type: "new", products: ["simulator"],
      title: "Replay Simulator 3.02: the Smart Panel",
      text: "The big simulator window now shrinks into one slim bar with Prev, Play, Next, speed, lot, Buy, Sell, Close All, floating P/L and the replay time, so the chart stays clear. The chart that runs the simulator steps aside when the replay starts, and replay charts open zoomed out with more candles. Your licence, data and settings stay when you update.",
      link: "simulator.html#new", linkText: "See the Smart Panel" },
    { date: "2026-10-17", type: "new", products: ["trade-assistant"],
      title: "Trade Assistant 3.12, now also for MetaTrader 4",
      text: "The full panel now runs on MT4 too, with the same licence rules. Version 3.12 adds an About page (licence, key, updates, theme, size, website and WhatsApp in one place), panel size from 75% to 150%, every tradeable symbol of your broker in the symbol list with a scroll bar, and clearer messages for DLL, connection and broker problems.",
      link: "trade-assistant.html#download", linkText: "Download MT5 or MT4" },
    { date: "2026-10-14", type: "new", products: ["trade-assistant", "simulator", "courses"],
      title: "New video tutorials: Trade Assistant and Replay Simulator",
      text: "A full 28-minute Trade Assistant tutorial (setup, chart patterns, signals, lot calculator and Prop Firm Guard), now playing on the Trade Assistant page, and a new video on practising like the real market with the Replay Simulator's Prop Firm Challenge mode.",
      link: "trade-assistant.html#video", linkText: "Watch the tutorial" },
    { date: "2026-10-14", type: "new", products: ["website"],
      title: "Meet the team behind Qazi Forex Tips",
      text: "A new About page with Dr. Qazi Abdul Basit's story, how we teach, and the four team members who work with him on analysis, education and our MT5 tools.",
      link: "about.html", linkText: "Meet the team" },
    { date: "2026-10-13", type: "new", products: ["simulator", "trade-assistant"],
      title: "Download the Simulator and the Trade Assistant from the website",
      text: "Both tools now download in one click, with the version, file size and three install steps on their pages. The licence key for a live account comes on WhatsApp.",
      link: "trade-assistant.html#download", linkText: "Go to downloads" },
    { date: "2026-10-13", type: "new", products: ["website", "courses"],
      title: "Student feedback page",
      text: "Read real feedback from our students and from traders who use our tools, filter it by course, batch or tool, and write your own in one minute.",
      link: "feedback.html", linkText: "Read the feedback" },
    { date: "", version: "Trade Assistant 3.10 – 3.11", type: "improved", products: ["trade-assistant"],
      title: "The Trade Assistant now updates itself",
      text: "Open the License page and press Update: the new version downloads and installs, and your settings and licence stay the same. Every problem now shows a clear message (DLL off, internet, antivirus, file in use).",
      link: "trade-assistant.html#download", linkText: "Get v3.11" },
    { date: "", version: "Trade Assistant 3.05 – 3.09", type: "new", products: ["trade-assistant"],
      title: "Professional trading journal report",
      text: "An HTML report with equity curve, day journal, streaks, setups and feelings, a money management plan and a Monte Carlo test, for any period you choose. Plus a full week of news with a scrollbar, a 'Candle closes in' countdown and one folder for all screenshots." },
    { date: "", version: "Replay Simulator 3.00", type: "new", products: ["simulator"],
      title: "Prop Firm Challenge mode and a new pro report",
      text: "Practise the exact rules of your prop firm (profit target, daily loss, max loss) with a live dashboard that shows PASSED or FAILED. The new report adds a trading journal, streaks, R-multiple statistics, a Monte Carlo test and your own money plan. Keyboard shortcuts: Space, N / P, B / S.",
      link: "simulator.html#challenge", linkText: "See the challenge mode" },
    { date: "", version: "Replay Simulator 2.99", type: "new", products: ["simulator"],
      title: "Risk in $: the lot size is calculated for you",
      text: "Type your risk in dollars and drag the SL line. The lot follows the SL distance, so the loss at the stop never goes above your risk. Also: import years of M1 data from HistData or Dukascopy CSV files.",
      link: "simulator.html#features", linkText: "See all features" },
    { date: "2026-10-10", type: "new", products: ["website", "courses"],
      title: "The new Qazi Forex Tips website",
      text: "A new home for our free Urdu and Hindi courses: every YouTube playlist on one page with the videos playing right here, our MT5 tools, and a light and a dark theme.",
      link: "youtube.html", linkText: "Open the courses" }
  ],

  versions: {
    simulator: [
      { v: "3.04", current: true, items: ["Prop Firm Challenge from the simulator window: start, hide, stop or restart a challenge at any moment of the replay", "Ready challenge types: 2-Step Phase 1 and 2, 1-Step, Instant funding, or Custom rules", "Indicators added on one replay chart appear on all replay charts (MT5)", "Save Simulation: choose your own folder and name; Load: open a .qsim file from any folder", "New BUY / SELL buttons with the price, compact Smart Panel and Prop Firm buttons", "Taller footer and a shorter New Simulation window"] },
      { v: "3.03", items: ["Now also available for MetaTrader 4 (separate download, own licence key per MT4 account)", "Fix: the simulator window could be empty after the simulator was attached again, the chart timeframe was changed or a template was applied", "Includes everything from 3.02: Smart Panel, clean start, zoomed-out replay charts, website links"] },
      { v: "3.02", items: ["Smart Panel: Prev / Play / Next, speed, lot, Buy, Sell, Close All, P/L and time in one slim bar", "SMART PANEL button next to Buy / Sell, or minimize the window during a replay", "The chart that runs the simulator is minimized during the replay and comes back after", "Replay charts open one zoom step further out (more candles, better structure)", "Website and WhatsApp links in every window and in the backtest report"] },
      { v: "3.00", items: ["Prop Firm Challenge mode: target, daily loss and max loss with a live dashboard", "New pro report: journal, streaks, money plan, charts", "R-multiple statistics and Monte Carlo risk test", "Keyboard shortcuts: Space, N / P, B / S, + / −", "Online licence check"] },
      { v: "2.99", items: ["Risk in $: the lot size is calculated from your SL", "Moving the SL line re-sizes the lot, the loss never goes above your risk", "Import CSV: M1 data from HistData or Dukascopy", "Clearer messages for tick downloads"] }
    ],
    tradeAssistant: [
      { v: "3.13", current: true, items: ["Compact view: one button shrinks the panel to risk, lot, Lines and Sell / R / Buy", "Start here: 3 short steps guide a new user through risk, SL / TP and the order", "Risk box turns yellow above 2% and red above 5% of the balance", "2 new ICT strategies in Signals: ICT OTE 79% and ICT 2022 Model (11 strategies)", "Best button: keeps only the strategies that beat break-even on your chart", "Use setup: copies a signal's Entry, SL and TP to the Trade tab (you place the order)", "Navy Blue default theme, cleaner panel without the bottom box"] },
      { v: "3.12", items: ["First MetaTrader 4 version (same panel and licence rules)", "Info > About page: licence, key, updates, theme, panel size, website and WhatsApp; new users start here", "Panel size 75% – 150%, and the panel shrinks itself to stay above indicator windows", "Symbol list: every tradeable symbol of your broker, with a scroll bar", "Symbol details moved to Market > Symbol", "Lines close after an order (Lines button brings them back)", "Update progress in %, restart prompt and What's new after an update", "Clear messages: DLL missing, old MetaTrader, connection, broker EA trading off"] },
      { v: "3.11", items: ["Online self-update tested and working: Update on the License page installs the new version"] },
      { v: "3.10", items: ["A clear message for every problem: DLL off, internet, antivirus, file in use"] },
      { v: "3.09", items: ["Clock shows your country (e.g. PK time)", "'Candle closes in' countdown"] },
      { v: "3.08", items: ["All screenshots in one folder, with a Folder button"] },
      { v: "3.07", items: ["Journal report for any period: 7 / 30 days, 3 / 6 months, this year, all history"] },
      { v: "3.06", items: ["News for the whole week and the next 7 days, with a scrollbar"] },
      { v: "3.05", items: ["Professional HTML journal report: equity, streaks, setups, money plan, Monte Carlo"] },
      { v: "3.04", items: ["Smoother panel while dragging lines"] },
      { v: "3.03", items: ["ATR on / off with SL / TP restore", "News filter (High / Medium / Low) and news lines on the chart"] },
      { v: "3.01 – 3.02", items: ["5 panel themes", "News, clock and journal in your PC time", "Order retry"] }
    ]
  },

  /* ---------- 3a. DOWNLOADS (simulator.html + trade-assistant.html) ----------
     Zip files GitHub ke "downloads" folder mein hain. Naya version aaye to:
     1) nayi zip ISI NAAM se downloads folder mein upload karein (purani replace ho jayegi),
     2) yahan version aur size badal dein. Link kabhi nahi badalta.            */
  downloads: {
    simulator:      { file: "downloads/QFT-Replay-Simulator.zip", version: "3.04", size: "4.6 MB" },
    simulatorMT4:   { file: "downloads/QFT-Replay-Simulator-MT4.zip", version: "3.03", size: "6.3 MB" },
    tradeAssistant: { file: "downloads/QFT-Trade-Assistant.zip",  version: "3.13", size: "3.9 MB" },
    tradeAssistantMT4: { file: "downloads/QFT-Trade-Assistant-MT4.zip", version: "3.13", size: "3.8 MB" }
  },

  /* ---------- 3b. QFT TRADE ASSISTANT (trade-assistant.html + Home showcase) ----------
     version: naya version aaye to sirf yahan number badlein.
     shots:   screenshots ke naam. Tasveer GitHub par isi naam se upload karein,
              website khud dikha degi. Jo tasveer nahi mili woh khud chhup jati hai.
     video:   YouTube tutorial ka link (Trade Assistant page par chalti hai).    */
  tradeAssistant: {
    version: "3.13",
    video: "https://youtu.be/lAOFQHaCszA",
    shots: [
      { file: "ta-hero.png", caption: "QFT Trade Assistant 3.13 on a Gold (XAUUSD) M5 chart in the Navy Blue theme: risk 1,000 USD, lot 1.24 calculated, Entry, SL and TP lines with money at risk and reward" },
      { file: "ta-1.png", caption: "Trade tab: risk in USD or %, R/TP and R/SL ratio, ATR stop, lot calculator, market, stop and limit orders" },
      { file: "ta-2.png", caption: "Chart lines: drag Entry, SL and TP and see the loss and profit in USD; L locks a line, R flips Buy and Sell" },
      { file: "ta-3.png", caption: "Close tab: close buys, sells, profits or losses, delete pending orders, auto close by profit, loss or time (e.g. Friday 23:30)" },
      { file: "ta-8.png", caption: "Protect tab: Prop Firm Guard with daily loss and max drawdown limits, news lock, open risk and the maximum lot" },
      { file: "ta-5.png", caption: "Market tab: economic calendar for the whole week with high, medium and low impact news and a countdown, in your PC time" },
      { file: "ta-6.png", caption: "Signals, Patterns: chart and candlestick patterns plus Smart Money zones (FVG, order block, BOS/CHoCH, liquidity sweep) with history scores" },
      { file: "ta-7.png", caption: "Signals, Strategies: 11 strategies including ICT OTE 79% and the ICT 2022 Model, with the Best and Use setup buttons; no auto trading" },
      { file: "ta-9.png", caption: "Journal tab: every trade with its setup, feeling and note, report period, screenshots and a full HTML report (amounts blurred)" },
      { file: "ta-4.png", caption: "Info, About: licence status, version 3.13 up to date, check for updates, Navy Blue theme and panel size 75–150%" }
    ],
    features: [
      { title: "Exact lot from your risk", text: "8 risk modes: $, % of balance, equity, free margin or a custom value, or % of the day, week or month start. Commission included, rounded to your broker's lot step. The lot turns red if the broker would not accept it." },
      { title: "Drag Entry, SL and TP", text: "See the loss and profit in USD and points before you click. L locks SL or TP, R flips Buy and Sell, and dragging the entry turns it into a Stop or Limit order by itself." },
      { title: "One click, always with SL and TP", text: "Buy, Sell, Buy/Sell Stop and Buy/Sell Limit, sent with SL and TP at once, no confirmation popup. ATR stop loss button, Risk:Reward auto TP, spread limit and split orders." },
      { title: "Prop Firm Guard", text: "Set your daily loss limit, max drawdown, daily target and trades per day. The panel blocks new trades before a rule is broken, the way FTMO-style firms check you." },
      { title: "News lock and calendar", text: "The whole week of high, medium and low impact news in your own PC time, with a countdown and news lines on the chart. Lock trading around big events like NFP and CPI." },
      { title: "Partial close, break-even, trailing", text: "Up to 10 TP and 10 SL levels, break-even with offset, 6 trailing methods (points, Fractals, MA, Parabolic SAR, ATR, High/Low bar), profit lock, OCO and hidden SL/TP." },
      { title: "Close everything in one click", text: "Close Buy, Sell, Profit, Loss or All, delete pending orders by type, and auto-close at a profit or loss target or at a set time, such as Friday close." },
      { title: "Patterns, Smart Money and strategies", text: "18 patterns including FVG, Order Blocks, BOS/CHoCH and liquidity sweeps, plus 11 strategies including ICT OTE 79% and the ICT 2022 Model, with Entry, SL and TP. Each has a history score on your own chart, a Best button keeps only the ones that beat break-even there, and Use setup copies a signal to the Trade tab. Closed candles only, no repainting." },
      { title: "Journal and professional report", text: "Note the setup, feeling and lesson for every trade, then open a colourful report with equity curve, win rate, drawdown and Monte Carlo, so you see what to repeat and what to stop." },
      { title: "Sessions and market info", text: "Sydney, Tokyo, London and New York coloured on the chart with daylight saving handled. Account, symbol and trading statistics in one tab." },
      { title: "Push alerts to your phone", text: "Alerts on the MT5 app when a trade opens or closes, break-even is set, a guard limit or news lock is hit, a signal appears or a price is reached." },
      { title: "Compact view, your way", text: "One button shrinks the panel to risk, lot, Lines and Sell / Buy for scalping. The risk box turns yellow above 2% and red above 5% of your balance. 5 themes (Navy Blue default), size 75–150%, hotkeys, presets, a Start here help for new users, and one-click updates. One licence key works on MT5 and MT4." }
    ]
  },

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

  /* ---------- 6. YOUTUBE PAGE (youtube.html) ----------
     Yeh poora YouTube page isi hisse se banta hai.
     Thumbnail (tasveer) website khud YouTube se le leti hai.

     NAYI VIDEO DAALNA (sirf 2 kaam):
       1) "latest" mein SAB SE UPAR aik line daalein.
       2) Jis playlist mein video hai, us ki "videos" list mein bhi aik line daalein
          (playlist mein jis number par video hai, usi jagah).
       Line aisi hoti hai:
       { title: "Video ka naam", link: "https://youtu.be/XXXXXXXXXXX", time: "12:34" },
       - link: YouTube par "Share" > "Copy" se jo link milta hai, woh paste karein.
       - time: video ki lambai (khali "" bhi chal jata hai).

     NAYI PLAYLIST: neeche wala aik poora { name: ... } block copy/paste karein.
       link: YouTube playlist ka link (button "Play all on YouTube" ke liye)          */
  youtube: {
    title: "Free forex lessons in Urdu & Hindi",
    urdu: "فاریکس ٹریڈنگ مفت سیکھیں – اردو اور ہندی میں",
    text: "Complete Price Action courses, tested strategies, live sessions and practical guides. Start from Lecture 1 and go step by step.",
    featured: "https://youtu.be/lAOFQHaCszA",   // hero mein bari video (aam tor par sab se nayi)

    latest: [
      { title: "Trade Assistant MT5 Tutorial | Setup, Chart Patterns, Signals, Lot Calculator & Prop Firm Guard", link: "https://youtu.be/lAOFQHaCszA", time: "28:10" },
      { title: "Best MT5 Replay Tool for Backtesting | Prop Firm Challenge Mode | Practice Like Real Market", link: "https://youtu.be/U1bCUislVJ4", time: "28:40" },
      { title: "High Probability TREND REVERSAL Technique | Simplest and Easiest steps", link: "https://youtu.be/Npav87jvsgE", time: "55:21" },
      { title: "Master the Fibonacci Retracement Technique: A Step-by-Step Guide. Expert Tips & Strategies", link: "https://youtu.be/3bVuDuiWMvE", time: "26:18" },
      { title: "Rule-Based Multi-Timeframe Analysis for Forex & Stocks", link: "https://youtu.be/uVsJgH40mz4", time: "32:31" },
      { title: "How to BACKTEST any Strategy like a PRO! (The main Reason behind Failure of a Trader)", link: "https://youtu.be/LXhMQmasz7Y", time: "24:00" },
      { title: "When to Trade Against the Trend – A Simple Method (Urdu & Hindi)", link: "https://youtu.be/4WyfWJpBXSQ", time: "43:52" }
    ],

    playlists: [
      {
        name: "Price Action Mastery – Basic Level",
        text: "Complete beginner course in Urdu & Hindi. Start here: support & resistance, trendlines, Fibonacci, SL / TP and multi-timeframe analysis.",
        course: true,   // true = cards par "Lecture 1, 2, 3..." likha aata hai
        link: "https://www.youtube.com/playlist?list=PLae00y7sDib6oCTqRtajkeN43LT7pQvNQ",
        videos: [
          { title: "Some important Points about Forex Trading (Price Action Mastery Course lecture 01)", link: "https://youtu.be/9JfvsIfslCg", time: "19:38" },
          { title: "Importance of Price Action and Technical Analysis (Lecture 02)", link: "https://youtu.be/787D9bivMGA", time: "18:26" },
          { title: "Why Support and Resistance Fails? Important rules to Draw Support and Resistance", link: "https://youtu.be/DDaEQcAJIEA", time: "40:35" },
          { title: "Easiest and Important Rules to Draw Trendlines in Urdu/Hindi", link: "https://youtu.be/oj6VV-aQyHo", time: "35:32" },
          { title: "Where to set Take Profit and Stop Loss? How to Close half trade in Profit", link: "https://youtu.be/P4WlWt2Tmjs", time: "18:38" },
          { title: "How to Identify False Breakouts and How to Avoid them. Tips and Detailed Video in Urdu and Hindi", link: "https://youtu.be/7aLG1XgfSYA", time: "22:49" },
          { title: "Simple Fibonacci retracement Strategy explain in Urdu Hindi (The Secret of Fibonacci)", link: "https://youtu.be/qLNsCRwyQp0", time: "14:59" },
          { title: "Simple and Easy method to use Trend Based Fibonacci Extensions for Profit Levels", link: "https://youtu.be/wQ5GxVGwxww", time: "17:32" },
          { title: "Most Important Lecture Don't Skip any Second. Use of Rejection and Momentum Candle for Perfect Entry", link: "https://youtu.be/jwOwHVb1nIU", time: "39:13" },
          { title: "Money Management Plan – How to Grow a Small Account Step by Step (Forex, Crypto, Stock)", link: "https://youtu.be/558_ymM-hCg", time: "33:42" },
          { title: "Become An Expert With Multiple Time Frame Analysis || Top Down Analysis ||", link: "https://youtu.be/DSXZkL9ygfE", time: "33:14" }
        ]
      },
      {
        name: "Price Action Mastery – Advance Level",
        text: "After the basic course: market structure, swing levels and the chart patterns professionals trade – with entry, SL and TP rules.",
        course: true,
        link: "https://www.youtube.com/playlist?list=PLae00y7sDib4LJZQrca7Icna4_D1lxnZU",
        videos: [
          { title: "Price Channel Detailed Video: Types, Drawing and Channel Trading Strategy in Simple words", link: "https://youtu.be/53hlwsaW3og", time: "31:10" },
          { title: "More simple! can't possible: Master these Chart Pattern Symmetrical, Ascending & Descending Triangle", link: "https://youtu.be/kCiq33-i7nk", time: "30:18" },
          { title: "How to Spot and Trade Rising & Falling Wedges", link: "https://youtu.be/rWSzRoAk0m4", time: "35:05" },
          { title: "How Professionals Trade Head & Shoulders Patters l How to Confirm, Recognize and Trade it URDU Hindi", link: "https://youtu.be/UXq228TiW6c", time: "26:36" },
          { title: "Best method to trade Inverse Head & Shoulder Pattern with complete Rules of Entry,TP & SL urdu/hindi", link: "https://youtu.be/qF7NSlS-lYU", time: "21:36" },
          { title: "Mastering Forex/ Stock Market Structure (Advanced). Key to Success in Forex/ Stock Urdu/Hindi", link: "https://youtu.be/VFo2qCSMPuU", time: "25:34" },
          { title: "How To Identify Swing Highs & Lows (Major Swing Levels) All you Need to Know", link: "https://youtu.be/-RVBo8qiJ1Q", time: "17:36" },
          { title: "Quasimodo Pattern for Scalpers and Day Traders", link: "https://youtu.be/vqC4EwSmtPE", time: "17:16" },
          { title: "The Only Flag Pattern Video You Will Ever Need I Simple But Powerful Flag Pattern Trading Strategy", link: "https://youtu.be/oQZz8Ng78XM", time: "18:24" }
        ]
      },
      {
        name: "Trading Strategies",
        text: "Complete strategies with rules: divergence, MACD, breakout, price action scalping and Gold scalping.",
        course: false,
        link: "https://www.youtube.com/playlist?list=PLae00y7sDib5m4Tmn2g_3enubmXc65Zja",
        videos: [
          { title: "Trade Divergence like a PRO – Complete Divergence Strategy", link: "https://youtu.be/ZCPiVFEoryw", time: "43:30" },
          { title: "MACD Crossover Trading Strategy in Urdu & Hindi", link: "https://youtu.be/O1sffgWvmwg", time: "17:17" },
          { title: "How to Trade Hidden Divergence – Complete Rules", link: "https://youtu.be/rRvvmwV_Km0", time: "23:48" },
          { title: "Price Action Trading Strategy for Day Traders & Scalpers", link: "https://youtu.be/6ktztQxlCk4", time: "20:41" },
          { title: "Breakout Trading Strategy – Price Action Method for Intraday Traders", link: "https://youtu.be/gsIRSLb1B8Q", time: "22:51" },
          { title: "Dominant Breakout Method – Breakout Strategy for Forex & Stocks", link: "https://youtu.be/xHuF_uWFaww", time: "25:50" },
          { title: "Dominant Plus – Scalping Strategy for Gold, Indices & Crypto (M5 / M15)", link: "https://youtu.be/vNwv4ZwHVMA", time: "12:03" },
          { title: "QFT Price Action Scalping Strategy – Gold, Indices, Stocks & Forex", link: "https://youtu.be/jDDa-sa8X1E", time: "28:47" },
          { title: "Gold Scalping Strategy on the 5-Minute Chart – Stochastic RSI", link: "https://youtu.be/5vrDSC08ox0", time: "22:30" },
          { title: "Gold Scalping Strategy GSS-2 – Complete Rules", link: "https://youtu.be/4QHH5V2gsEQ", time: "33:25" }
        ]
      },
      {
        name: "Weekly Live Sessions",
        text: "Full-length live session recordings: market recap, weekly analysis, market structure and Q&A.",
        course: false,
        link: "https://www.youtube.com/playlist?list=PLae00y7sDib4YBRj3X0qmwkgPtEUpFnuW",
        videos: [
          { title: "Weekly Live Session: Market Recap, Weekly Analysis, Types of Levels, Tips & Tricks and Much More", link: "https://youtu.be/P3G1W3-Y_oI", time: "59:50" },
          { title: "Unknown Facts About Forex Trading Every Trader Should Know (Urdu / Hindi)", link: "https://youtu.be/0uPnOhdFIW8", time: "1:04:39" },
          { title: "Weekly Live Session Recording : Forex Market Recap plus weekly Analysis GOLD GBPUSD", link: "https://youtu.be/bLVgD208gJg", time: "1:09:01" },
          { title: "Most Important Points for Price Action Trader in Urdu and Hindi live session 22 Jan 2023", link: "https://youtu.be/wFTDiXOnfN4", time: "1:09:20" },
          { title: "It's Time to Open Up About classic trading method. The Ultimate Guide to Forex Market Structure.", link: "https://youtu.be/eXbRWN-g8gI", time: "55:34" },
          { title: "Increase Accuracy of Classic Trading Method. The Ultimate Guide to Forex Market Structure (Part-2)", link: "https://youtu.be/o1Y-bcvP5mU", time: "58:06" },
          { title: "When to Trade Against the Trend – A Simple Method (Urdu & Hindi)", link: "https://youtu.be/4WyfWJpBXSQ", time: "43:52" },
          { title: "How to BACKTEST any Strategy like a PRO! (The main Reason behind Failure of a Trader)", link: "https://youtu.be/LXhMQmasz7Y", time: "24:00" },
          { title: "Rule-Based Multi-Timeframe Analysis for Forex & Stocks", link: "https://youtu.be/uVsJgH40mz4", time: "32:31" },
          { title: "Master the Fibonacci Retracement Technique: A Step-by-Step Guide. Expert Tips & Strategies", link: "https://youtu.be/3bVuDuiWMvE", time: "26:18" }
        ]
      },
      {
        name: "Important Forex Videos",
        text: "Practical guides: TradingView, backtesting software, broker selection, lot size, news and the best time to trade.",
        course: false,
        link: "https://www.youtube.com/playlist?list=PLae00y7sDib7ZXxHWIHzlkcmcAU992IUw",
        videos: [
          { title: "Tradingview Tutorial: How to Use Tradingview for Technical Analysis (Urdu/Hindi)", link: "https://youtu.be/d4U5FhM6NLU", time: "20:34" },
          { title: "Weekly Analysis 21 June to 25 June EURUSD, EURGBP, EURJPY. EURCAD, EURCHF", link: "https://youtu.be/oBldQaYHb6k", time: "12:37" },
          { title: "Weekly Analysis Gold, Oil, Silver, XRPUSD, BTCUSD from 21 June to 25 June Urdu Hindi", link: "https://youtu.be/4G3RaAzSbkI", time: "10:57" },
          { title: "Weekly Analysis GBPUSD, GBPAUD, GBPNZD, GBPCHF. GBPCAD for 21 June to 25 June 2021", link: "https://youtu.be/bGJysA4XgT8", time: "14:33" },
          { title: "Simple method to Read and Analyze NFP News Data in Urdu/Hindi", link: "https://youtu.be/jU96IJBXrSE", time: "13:10" },
          { title: "Thinktrader Tutorial + Download Link: Best Free Software for Backtesting Forex/ Stock Market", link: "https://youtu.be/PwWmz-5S4qE", time: "13:01" },
          { title: "Best Broker Selection Guide. very simple steps in Urdu & Hindi I How to Select Top Broker for Forex", link: "https://youtu.be/JeUpNZjti5Q", time: "15:28" },
          { title: "Chart Pattern Dashboard: Autochartist: Get Daily Forex/Stock Chart Pattern Signals on Mobile", link: "https://youtu.be/dOYz8pONVa0", time: "12:10" },
          { title: "Must Watch this Video before Starting Forex Trading l Trading Myths VS Realities", link: "https://youtu.be/UnSphPChym8", time: "12:19" },
          { title: "Strategy Optimization Tips – Improve Your Strategy Step by Step", link: "https://youtu.be/o0KRYx2WOmw", time: "13:06" },
          { title: "Best time to trade Forex/Gold for Scalping in Pakistan/ India", link: "https://youtu.be/ULqqAMzAKhg", time: "12:35" },
          { title: "Soft4FX Tutorial: FOREX, Stock, Crypto Best Backtesting Software (Bar Reply Forex Simulator for MT4)", link: "https://youtu.be/wHBg7w9ws-Y", time: "24:07" },
          { title: "Trade Assistant for mt4 : Automatic Risk/Lot Size calculator: Manage your trades with just 1 click", link: "https://youtu.be/1uMbc43V_tk", time: "16:18" },
          { title: "Managing Lot Size in Forex – The Right Lot Size on Every Trade", link: "https://youtu.be/4c9gtnO5_48", time: "9:39" },
          { title: "Best MT5 Replay Tool for Backtesting | Prop Firm Challenge Mode | Practice Like Real Market", link: "https://youtu.be/U1bCUislVJ4", time: "28:40" },
          { title: "Trade Assistant MT5 Tutorial | Setup, Chart Patterns, Signals, Lot Calculator & Prop Firm Guard", link: "https://youtu.be/lAOFQHaCszA", time: "28:10" }
        ]
      },
      {
        name: "More videos",
        text: "Videos from the channel that are not in a playlist yet.",
        course: false,
        link: "",
        videos: [
          { title: "High Probability TREND REVERSAL Technique | Simplest and Easiest steps", link: "https://youtu.be/Npav87jvsgE", time: "55:21" },
          { title: "How Do I Analyze the Forex Market & Take Entries. Last Week Analysis with Explanation.", link: "https://youtu.be/Qh16-yMyp2A", time: "42:39" },
          { title: "Qazi Forex Tips Live Stream", link: "https://youtu.be/0T4pGece544", time: "1:09:19" }
        ]
      }
    ]
  },

  /* ---------- 7. NUMBERS (sirf SACH figures likhein) ---------- */
  stats: [
    { value: "2013", label: "Trading since" },
    { value: "64th", label: "Student batch running" },
    { value: "14K+", label: "YouTube subscribers" },
    { value: "60+",  label: "Free video lessons" }
  ],

  /* ---------- 8. YAHAN SE SHURU KAREIN (learning path) ---------- */
  path: [
    { title: "Learn the basics", text: "Price Action Mastery – Basic Level. 11 lectures, from support & resistance to multi-timeframe analysis.", link: "course-price-action-basic.html", button: "Open the course" },
    { title: "Go advanced", text: "Price Action Mastery – Advance Level. Market structure, swing levels and chart patterns with entry, SL and TP rules.", link: "course-price-action-advanced.html", button: "Open the course" },
    { title: "Pick a strategy", text: "Complete strategies with rules: divergence, breakout, price action scalping and Gold scalping.", link: "course-trading-strategies.html", button: "See strategies" },
    { title: "Practise before you risk money", text: "Replay past markets candle by candle in the QFT Replay Simulator and build your own track record.", link: "simulator.html", button: "See the simulator" }
  ],

  /* ---------- 9. ABOUT (photo: tasveer ka naam, e.g. "qazi.jpg") ---------- */
  about: {
    name: "Dr. Qazi Abdul Basit",
    role: "Ph.D in Business Administration · Forex & Gold trader since 2013 · Founder, Qazi Forex Tips",
    photo: "dr-qazi-2.jpg",
    story: [
      "I have been trading forex and Gold since 2013. Like every trader I went through the ups and downs, and those years taught me what keeps an account alive: clear price action, a fixed risk on every trade, and the discipline to follow a plan.",
      "I started Qazi Forex Tips so traders in Pakistan and India can learn this in their own language. The YouTube channel has complete free courses in Urdu and Hindi, and our 64th student batch is running now.",
      "I also build MetaTrader 5 tools for my own trading and teaching, like the QFT Replay Simulator for honest backtesting and the QFT Trade Assistant for risk-based lot sizes."
    ],
    skills: ["Price Action", "Gold (XAUUSD)", "Risk & Money Management", "Trading Psychology"]
  },

  /* ---------- 9b. STUDENTS KI FEEDBACK (website par dikhane ke liye) ----------
     Jab koi student WhatsApp par feedback bheje AUR "website par dikhane ki ijazat"
     di ho, to yahan aik line daal dein. Sirf ASLI feedback, student ki ijazat se.
     Jab tak yeh list khali hai, website par yeh section chhupa rahega.
       rating: 1 se 5 tak (stars)
       batch:  batch number ya "" (khali)
     Misaal (shuru mein // hata kar chalu karein):
     { name: "Ali Raza", city: "Lahore", batch: "62", rating: 5, text: "Price action course ne meri trading badal di.", date: "Oct 2026" },  */
  /* ---------- TEAM (home page, About ke neeche) ----------
     photo: tasveer ka naam (GitHub par upload). Khali "" = initials dikhenge.
     Tarteeb wahi jo yahan hai. Har shakhs ki ijazat se.                      */
  team: [
    { name: "Faham Shabeer", role: "EA Developer & Trader", photo: "team-faham.jpg",
      text: "Faham builds and tests Expert Advisors (EAs) for MetaTrader 5 and trades Gold (XAUUSD) himself. In more than two years of trading he has focused on Smart Money Concepts, price action and liquidity, with short-term setups and a fixed risk plan. He believes discipline, patience and control of emotions matter more than any single trade.",
      quote: "Protect your capital, trust your analysis, master your emotions.",
      tags: ["MT5 EAs", "Gold", "SMC", "Price Action"] },
    { name: "Irfan Ahmed Bhutto", role: "Instructor · Price Action", photo: "team-irfan.jpg",
      text: "Irfan began his own trading education under Dr. Qazi Abdul Basit in June 2024 and now teaches as an instructor at Qazi Forex Tips. He helps students read market structure, liquidity, supply and demand zones and shifts in trend (BOS and CHoCH) across several timeframes, and plan every trade with a clear exit and a fixed risk.",
      quote: "",
      tags: ["Teaching", "Price Action", "Market Structure", "Risk Management"] },
    { name: "Muhammad Anas", role: "SMC & ICT Trader", photo: "",
      text: "Anas trades with Smart Money Concepts (SMC) and ICT methods, reading market structure and liquidity to plan his entries. He believes good trading is not about predicting every move, but about following a clear plan, respecting risk and staying consistent. At Qazi Forex Tips he keeps building his skills and shares what he learns with our community.",
      quote: "Learn the market, respect risk, follow the strategy, and stay disciplined.",
      tags: ["SMC", "ICT", "Liquidity", "Market Structure"] },
    { name: "Muhammad Hassan Mohsin", role: "Education Team", photo: "",
      text: "Hassan works on the education side of Qazi Forex Tips. He helps beginners and developing traders understand how the market works through structured learning material on technical analysis, risk management and trading psychology, and helps keep our community focused on a disciplined approach to trading.",
      quote: "Learn the market. Manage your risk. Trade with discipline.",
      tags: ["Education", "Technical Analysis", "Risk Management", "Psychology"] }
  ],

  testimonials: [
  ],

  /* Feedback ka automatic system (Google Form + Google Sheet). Inhein na chheren.
     Website ka form har feedback Google Sheet "QFT Student Feedback (Responses)" mein bhejta hai.
     Jis student ne ijazat di (YES), us ka feedback ~5 minute mein website par khud aa jata hai.
     Kisi feedback ko chhupana ho: Sheet mein us line ke "Hide" khane mein YES likh dein.      */
  /* Team members ki feedback par saaf note (imaandari ke liye).
     Naam bilkul wahi likhein jo feedback mein hai. */
  feedbackNotes: {
    "Faham Shabeer": "Batch 5 student · now part of the QFT team"
  },

  feedbackSystem: {
    formAction: "https://docs.google.com/forms/d/e/1FAIpQLSeJIBUyRHfxqj0Kn7ijzCE-GEE_zv3YM3HeMmuEOqKGXOkv7g/formResponse",
    fields: { name: "entry.1097635637", city: "entry.1320651867", batch: "entry.1167245964", rating: "entry.1558484287", text: "entry.145154759", allow: "entry.1668224544", product: "entry.1090851567" },
    publicCsv: "https://docs.google.com/spreadsheets/d/e/2PACX-1vSARWCOQMDXkUfVVPxDncWD_8huG0N58l7UAVHNayn_2UeGDAZaiXH2G-YFNbsV1oUsvBk0ZSOUamk9/pub?gid=423830435&single=true&output=csv"
  },

  /* ---------- 10. SAWAL JAWAB (FAQ) ---------- */
  faq: [
    { q: "I am completely new. Where should I start?", a: "Start with Price Action Mastery – Basic Level on our YouTube page and watch it in order from Lecture 1. Practise on a demo account while you learn." },
    { q: "Are the YouTube courses free?", a: "Yes. Every course on the YouTube channel is free to watch, in Urdu and Hindi." },
    { q: "How do I join the next student batch?", a: "Send us a message on WhatsApp at +92-323-6700010 and we will share the details of the next batch." },
    { q: "How much money do I need to start trading?", a: "Learn and practise on a demo account first. When you go live, use only money you can afford to lose and keep the risk on each trade small, for example 1% of the account." },
    { q: "How can I get the QFT Replay Simulator or an EA?", a: "Message us on WhatsApp. We will help you choose the right tool and guide you through setup and the licence." },
    { q: "Do you give signals or guaranteed profits?", a: "No. We teach you to read the market and manage risk yourself. Trading carries high risk and nobody can guarantee profit." }
  ],

  /* ---------- 11. NEECHE KI LINE (FOOTER) ---------- */
  disclaimer: "Trading forex and gold involves high risk. Content is for education only and is not financial advice. Past or backtest results do not guarantee future results."
};
