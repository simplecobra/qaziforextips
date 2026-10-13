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
    youtube: "https://www.youtube.com/@QaziForexTips",
    facebook: "https://www.facebook.com/groups/qaziforextips",
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
      badge: "v3.11",
      text: "Risk management trade panel for MT5: set risk in money or %, drag Entry / SL / TP lines, the lot size is calculated for you.",
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

  /* ---------- 3a. DOWNLOADS (simulator.html + trade-assistant.html) ----------
     Zip files GitHub ke "downloads" folder mein hain. Naya version aaye to:
     1) nayi zip ISI NAAM se downloads folder mein upload karein (purani replace ho jayegi),
     2) yahan version aur size badal dein. Link kabhi nahi badalta.            */
  downloads: {
    simulator:      { file: "downloads/QFT-Replay-Simulator.zip", version: "3.01", size: "5.3 MB" },
    tradeAssistant: { file: "downloads/QFT-Trade-Assistant.zip",  version: "3.11", size: "3.9 MB" }
  },

  /* ---------- 3b. QFT TRADE ASSISTANT (trade-assistant.html + Home showcase) ----------
     version: naya version aaye to sirf yahan number badlein.
     shots:   screenshots ke naam. Tasveer GitHub par isi naam se upload karein,
              website khud dikha degi. Jo tasveer nahi mili woh khud chhup jati hai.
     video:   YouTube video ka link jab video ban jaye (abhi khali).            */
  tradeAssistant: {
    version: "3.11",
    video: "",
    shots: [
      { file: "ta-1.png", caption: "Main panel: risk, lot size and one-click orders" },
      { file: "ta-2.png", caption: "Entry, SL and TP lines on the chart" },
      { file: "ta-3.png", caption: "Close tab: manage open trades" },
      { file: "ta-4.png", caption: "Info tab: account, symbol and statistics" },
      { file: "ta-5.png", caption: "Patterns & Strategies tabs" },
      { file: "ta-6.png", caption: "License & Updates screen" }
    ],
    features: [
      { title: "Risk in money or %", text: "Set risk in $ or as % of balance, equity, free margin, a custom amount, or the previous day, week or month. No hidden risk cap: you decide." },
      { title: "Automatic lot size", text: "Move your SL and the lot size follows your risk. The lot turns red if the broker would not accept it." },
      { title: "Drag Entry, SL and TP", text: "Compact lines at the right edge of the chart. Drag the entry to make a pending order, lock SL or TP with L, flip Buy/Sell with R." },
      { title: "One-click orders", text: "Market and pending orders go straight in, with no confirmation popup. Clear English messages only when something is wrong, such as margin." },
      { title: "Manage open trades", text: "Close tab for partial and full closes. SL and TP stay draggable on the chart after entry." },
      { title: "Patterns & Strategies", text: "Toggle buttons mark chart patterns and strategy signals with Entry, SL and TP, each with a history score so you can judge it yourself." },
      { title: "News on the panel", text: "Upcoming high-impact news shown in your own PC time, so you are not caught by NFP or CPI." },
      { title: "Remembers everything", text: "Risk, RR and other settings survive an MT5 restart. Hotkeys for the main buttons and selectable panel themes." },
      { title: "Online updates & licence", text: "Update to the newest version from inside the panel. Licence key tied to your account number." }
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
    featured: "https://youtu.be/U1bCUislVJ4",   // hero mein bari video (aam tor par sab se nayi)

    latest: [
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
        text: "Practical guides: brokers, deposits & withdrawals, TradingView, backtesting software, lot size, news and the best time to trade.",
        course: false,
        link: "https://www.youtube.com/playlist?list=PLae00y7sDib7ZXxHWIHzlkcmcAU992IUw",
        videos: [
          { title: "Tradingview Tutorial: How to Use Tradingview for Technical Analysis (Urdu/Hindi)", link: "https://youtu.be/d4U5FhM6NLU", time: "20:34" },
          { title: "Weekly Analysis 21 June to 25 June EURUSD, EURGBP, EURJPY. EURCAD, EURCHF", link: "https://youtu.be/oBldQaYHb6k", time: "12:37" },
          { title: "Weekly Analysis Gold, Oil, Silver, XRPUSD, BTCUSD from 21 June to 25 June Urdu Hindi", link: "https://youtu.be/4G3RaAzSbkI", time: "10:57" },
          { title: "Weekly Analysis GBPUSD, GBPAUD, GBPNZD, GBPCHF. GBPCAD for 21 June to 25 June 2021", link: "https://youtu.be/bGJysA4XgT8", time: "14:33" },
          { title: "Simple method to Read and Analyze NFP News Data in Urdu/Hindi", link: "https://youtu.be/jU96IJBXrSE", time: "13:10" },
          { title: "Thinktrader Tutorial + Download Link: Best Free Software for Backtesting Forex/ Stock Market", link: "https://youtu.be/PwWmz-5S4qE", time: "13:01" },
          { title: "IC Markets Broker Review and Account Opening", link: "https://youtu.be/H4KgkxaiKSQ", time: "36:46" },
          { title: "Best Broker Selection Guide. very simple steps in Urdu & Hindi I How to Select Top Broker for Forex", link: "https://youtu.be/JeUpNZjti5Q", time: "15:28" },
          { title: "Chart Pattern Dashboard: Autochartist: Get Daily Forex/Stock Chart Pattern Signals on Mobile", link: "https://youtu.be/dOYz8pONVa0", time: "12:10" },
          { title: "Must Watch this Video before Starting Forex Trading l Trading Myths VS Realities", link: "https://youtu.be/UnSphPChym8", time: "12:19" },
          { title: "Strategy Optimization Tips – Improve Your Strategy Step by Step", link: "https://youtu.be/o0KRYx2WOmw", time: "13:06" },
          { title: "IC Markets Account Opening & Verification – Step by Step", link: "https://youtu.be/Ud6u5BLeKt0", time: "16:57" },
          { title: "Best time to trade Forex/Gold for Scalping in Pakistan/ India", link: "https://youtu.be/ULqqAMzAKhg", time: "12:35" },
          { title: "Soft4FX Tutorial: FOREX, Stock, Crypto Best Backtesting Software (Bar Reply Forex Simulator for MT4)", link: "https://youtu.be/wHBg7w9ws-Y", time: "24:07" },
          { title: "IC Markets | How to deposit and withdraw from IC Markets | Local Bank | Skrill l Pakistan & India", link: "https://youtu.be/0aYu58CE4Fo", time: "12:04" },
          { title: "Trade Assistant for mt4 : Automatic Risk/Lot Size calculator: Manage your trades with just 1 click", link: "https://youtu.be/1uMbc43V_tk", time: "16:18" },
          { title: "FP Markets Account Opening & Verification – Step by Step", link: "https://youtu.be/KBmSAZsrRa0", time: "9:36" },
          { title: "Managing Lot Size in Forex – The Right Lot Size on Every Trade", link: "https://youtu.be/4c9gtnO5_48", time: "9:39" },
          { title: "Best MT5 Replay Tool for Backtesting | Prop Firm Challenge Mode | Practice Like Real Market", link: "https://youtu.be/U1bCUislVJ4", time: "28:40" }
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
    { title: "Learn the basics", text: "Price Action Mastery – Basic Level. 11 lectures, from support & resistance to multi-timeframe analysis.", link: "youtube.html#pl-1", button: "Start Lecture 1" },
    { title: "Go advanced", text: "Price Action Mastery – Advance Level. Market structure, swing levels and chart patterns with entry, SL and TP rules.", link: "youtube.html#pl-2", button: "Open the course" },
    { title: "Pick a strategy", text: "Complete strategies with rules: divergence, breakout, price action scalping and Gold scalping.", link: "youtube.html#pl-3", button: "See strategies" },
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
  testimonials: [
  ],

  /* Feedback ka automatic system (Google Form + Google Sheet). Inhein na chheren.
     Website ka form har feedback Google Sheet "QFT Student Feedback (Responses)" mein bhejta hai.
     Jis student ne ijazat di (YES), us ka feedback ~5 minute mein website par khud aa jata hai.
     Kisi feedback ko chhupana ho: Sheet mein us line ke "Hide" khane mein YES likh dein.      */
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
