import re, json, html
SRC = 'lesson-xauusd-gold-buy-sell-forex-hours.html'
OUT = 'lesson-bid-ask-spread-pip-point-pipette-gold.html'
URL = 'https://qaziforextips.com/' + OUT
VID = '6_r9hTuMSjo'
TITLE = 'What is Pip in Forex? Bid, Ask, Spread, Point &amp; Gold Pip | Lesson 2.1'
TITLE_T = 'What is Pip in Forex? Bid, Ask, Spread, Point & Gold Pip | Lesson 2.1'
DESC = 'What is a pip in forex? Bid and ask price, spread cost, pip, point and pipette on EURUSD and USDJPY, and how gold (XAUUSD) pips, points and ticks work.'
H1 = 'What is a pip in forex? Bid, ask and spread, pip vs point vs pipette, and the gold pip (Lesson 2.1)'
HERO = 'img/forex-basics/bid-ask-spread-pip-point-mt5-quote-3d-lesson-2-1'
HERO_ALT = '3D MT5 quote tiles: EURUSD sell at bid 1.08450 and buy at ask 1.08462, a 1.2 pip spread (Lesson 2.1)'
DATE = '2026-11-25'
LEN = '12:51'; DUR = 'PT12M51S'
CH = [("0:00","Why a new buy trade starts in loss"),("0:43","Lesson 2.1 intro"),("1:26","Bid and ask price: money changer example"),("2:03","Bid, ask and spread in MT5"),("2:40","Why your trade opens in minus (spread cost)"),("3:26","Bid chart and sell stop loss hit by ask"),("3:58","When spread widens"),("4:41","What is a pip in forex"),("5:29","Pipette (5th digit)"),("5:53","JPY pairs pip"),("6:17","Point in MT5: 10 points = 1 pip"),("6:45","Counting pips: 25 pips example"),("7:35","Gold (XAUUSD) point and tick size"),("8:00","Gold pip: 30 or 300?"),("8:30","Golden rule: count dollars in gold"),("9:16","Gold specification in MT5"),("9:44","2-digit vs 3-digit gold brokers"),("10:51","Gold spread"),("11:15","5 common mistakes"),("12:01","Practical task"),("12:27","Next lesson: lot size")]
def sec(t):
    m,s=t.split(':');return int(m)*60+int(s)
COVERS = ["Bid and ask price with a money changer example","What is spread in forex and why a buy trade opens in minus","Spread cost in dollars on 1 lot and 0.01 lot","Why the MT5 chart shows bid, and how a sell stop loss gets hit by the ask","When spread widens: news, rollover, Monday open","How to see spread in MT5 Market Watch (in points)","What is a pip, a pipette and a point (10 points = 1 pip)","Pips on EURUSD and on JPY pairs","Gold (XAUUSD): point, tick size and tick value","Why one gold move is called 3, 30 or 300 pips","Golden rule: in gold, count dollars","2-digit vs 3-digit gold brokers and the 10x stop loss trap","5 beginner mistakes and a practical task"]
NOTES = """<h2>Bid and ask price: why every symbol has two prices</h2><p>A money changer's board shows two dollar rates: <b>we buy at 279</b> and <b>we sell at 282</b>. If you sell him a dollar you get 279; if you buy one you pay 282. The 3-rupee gap is his earning. Forex works the same way. In MT5 every symbol has two prices: the lower one is the <b>bid</b> and the higher one is the <b>ask</b>. For example, EURUSD bid 1.08450 and ask 1.08462.</p>
<p><b>The rule:</b> a <b>buy</b> always opens at the <b>ask</b> (the higher price) and a <b>sell</b> always opens at the <b>bid</b> (the lower price). You always buy a little expensive and sell a little cheap, just like at the shop.</p>
<h2>What is spread in forex, and why your trade opens in minus</h2><p>The <b>spread</b> is ask minus bid. When you buy at the ask and look at your profit straight away, the trade would close at the bid, so it shows a small minus equal to the spread. That is not a mistake; it is the trade's entry ticket. Profit starts only after price first covers the spread.</p>
<table><tr><th>EURUSD spread 1.2 pips</th><th>Cost</th></tr><tr><td>1 standard lot</td><td>about $12</td></tr><tr><td>0.01 lot</td><td>about $0.12</td></tr></table>
<p>You pay this on every trade, win or lose. Read more in our guide <a href="guide-what-is-spread.html">What is spread in forex?</a></p>
<h2>The MT5 chart shows the bid price</h2><p>A buy trade closes at the bid, so its stop loss and take profit follow the chart. A sell trade closes by buying back at the <b>ask</b>, which sits above the chart line. That is why a sell stop loss can be hit even when the bid candle never touched it. In MT5 open the chart properties and turn on the <b>Ask line</b> to see the gap.</p>
<h2>When spread widens</h2><p>Spread is small when the market is busy (London and New York hours). It can become many times bigger at big news, at the daily rollover around midnight server time, and at the Monday open. New traders should avoid trading at those moments.</p>
<h2>How to see the spread in MT5</h2><p>Right-click <b>Market Watch</b> and turn on the <b>Spread</b> column. The number is in <b>points</b>, not pips: a spread of 12 on EURUSD means 1.2 pips.</p>
<h2>What is a pip, a pipette and a point?</h2><p>A <b>pip</b> is the unit traders use to count price moves. On most pairs it is the 4th digit after the decimal (0.0001). Brokers show a 5th digit, the <b>pipette</b>, which is one tenth of a pip. Think of a ruler: pips are the centimetre marks and pipettes the millimetre marks. In MT5 a <b>point</b> is the smallest digit your broker shows, so on a 5-digit quote <b>10 points = 1 pip</b>.</p>
<ul><li>EURUSD 1.08452 to 1.08462 = 1 pip = 10 points.</li><li>JPY pairs: the pip is the 2nd decimal (0.01). USDJPY 150.250 to 150.750 = 50 pips.</li><li>EURUSD 1.08450 to 1.08700 = 25 pips = 250 points. That is about $250 on 1 lot and $2.50 on 0.01 lot.</li></ul>
<p>Lot size and pip value get their own lessons next. You can also read <a href="guide-what-is-a-pip.html">What is a pip in forex?</a></p>
<h2>Gold pip, point and tick (XAUUSD)</h2><p>Gold is usually quoted with 2 decimals, like 3800.00. The smallest step is 0.01 dollar (one cent): MT5 calls it one point and the specification calls it the <b>tick size</b>. The trouble is that there is no single definition of a gold pip: some people call 0.01 a pip, most traders call 0.10 a pip, and some call a whole dollar a pip. So the same move from 3800 to 3803 can be called 300, 30 or 3 pips.</p>
<p><b>Golden rule:</b> in gold, don't count pips, count dollars. 3800 to 3803 is a $3 move per ounce, with no confusion.</p>
<table><tr><th>Gold lot (100 oz)</th><th>$1 move</th><th>$3 move</th></tr><tr><td>1 lot</td><td>$100</td><td>$300</td></tr><tr><td>0.1 lot</td><td>$10</td><td>$30</td></tr><tr><td>0.01 lot</td><td>$1</td><td>$3</td></tr></table>
<p>Right-click gold in MT5 and open <b>Specification</b>: contract size 100, digits 2, tick size 0.01, tick value $1 (per 1 lot). Contract sizes can differ by broker, so always check yours.</p>
<h2>2-digit vs 3-digit gold brokers</h2><p>Some brokers quote gold with 2 digits after the point and some with 3. On a 2-digit broker, 3800.00 to 3800.10 means one ounce rose by 10 cents. On a 3-digit broker the 3rd digit is a tenth of a cent, so 3800.100 is still 10 cents. The price moved the same; only the writing differs. But MT5 points change ten times: those 10 cents are 10 points on a 2-digit broker and 100 points on a 3-digit broker. A 50-point stop loss copied from a video is 50 cents away on one broker and only 5 cents on the other. Always check <b>Digits</b> in the specification.</p>
<h2>Gold spread</h2><p>If Market Watch shows a gold spread of 20 with 2 digits, that is 20 cents: about $0.20 on 0.01 lot and $20 on 1 lot. Gold spread jumps fast at news time, so know the news times.</p>
<h2>5 beginner mistakes to avoid</h2><ol><li>Panicking at the small minus when a trade opens. That is the spread.</li><li>Taking MT5 points as pips and setting a stop loss or target ten times too big.</li><li>Placing a sell stop loss exactly at the high on a bid-only chart, with no room for the spread.</li><li>Using someone else's gold pips. Count dollars.</li><li>Trading at big news or Monday morning when spreads are wide.</li></ol>
<h2>Practical task</h2><p>On your demo MT5, turn on the Spread column in Market Watch, note the EURUSD and gold spread, convert them into pips and dollars, then open the gold specification and check Digits and Contract size. Share your EURUSD spread in the YouTube comments. Want to plan trades with the spread included? Try the free <a href="trade-assistant.html">QFT Trade Assistant</a> lot size panel for MT5.</p>"""
KHULASA = ["Har symbol ki do qeematein: neeche wali bid, ooper wali ask. Buy ask par, sell bid par hoti hai.","Spread = ask minus bid. Trade khulte hi spread jitna minus is liye dikhta hai: yeh trade ka dakhla ticket hai.","EURUSD par 1.2 pip spread: 1 lot par taqreeban $12, 0.01 lot par $0.12, har trade par.","MT5 chart bid dikhata hai; sell trade ask par band hoti hai, is liye sell ka SL candle pohanche bagair bhi hit ho sakta hai.","Pip = 4th digit (0.0001), JPY pairs mein 2nd digit (0.01). Pipette = pip ka daswan hissa. MT5 point = sab se chhota digit: 10 points = 1 pip.","Gold mein pip ki ek tareef nahi: 3800 se 3803 ko koi 300, koi 30, koi 3 pip kehta hai. Gold mein pip nahi, dollar ginein.","Gold ka 1 lot = 100 oz: $1 move = 1 lot par $100, 0.1 par $10, 0.01 par $1.","2 digit aur 3 digit broker: 3800.10 aur 3800.100 dono 10 cent hain, magar points 10 aur 100. Specification mein Digits zaroor check karein."]
FAQ = [("What is a pip in forex?","A pip is the unit used to count price moves. On most currency pairs it is the 4th decimal (0.0001); on JPY pairs it is the 2nd decimal (0.01). EURUSD moving from 1.08450 to 1.08700 is 25 pips."),
("What is the difference between a pip and a point in MT5?","In MT5 a point is the smallest digit your broker shows. With 5-digit quotes, one point is a pipette (a tenth of a pip), so 10 points = 1 pip. The Market Watch spread column and stop-loss distances are shown in points."),
("What is spread in forex?","Spread is the difference between the ask (buy) price and the bid (sell) price. A buy opens at the ask and closes at the bid, so every new trade starts with a small minus equal to the spread. A 1.2 pip EURUSD spread costs about $12 per lot."),
("How much is a pip in gold (XAUUSD)?","There is no single definition of a gold pip, so count dollars instead. With a 100 oz contract, a $1 move is $100 on 1 lot, $10 on 0.1 lot and $1 on 0.01 lot. Check the contract size and digits in your broker's specification."),
("پِپ اور پوائنٹ میں کیا فرق ہے؟","پِپ زیادہ تر پیئرز میں اعشاریہ کے بعد چوتھا ہندسہ ہے۔ ایم ٹی فائیو کا پوائنٹ قیمت کا سب سے چھوٹا ہندسہ ہے، اس لیے پانچ ڈیجٹ والی قیمت میں دس پوائنٹ ایک پِپ ہیں۔"),
("ٹریڈ کھلتے ہی مائنس کیوں آتا ہے؟","بائے آسک پر کھلتا ہے مگر ابھی بند کریں تو بِڈ پر بند ہو گا۔ یہ فرق اسپریڈ ہے، یعنی ٹریڈ کا داخلہ ٹکٹ۔"),
("Gold mein pip kaise ginein?","Gold mein pip ki ek tareef nahi, is liye dollar ginein: ek ounce par qeemat kitne dollar chali. 1 lot (100 oz) par $1 ka move $100 hai.")]
TAKES = ["A small minus right after you buy is not a loss to fear. It is the spread: the entry ticket of every trade.","In gold, don't count pips, count dollars. Then nobody's 30 or 300 can confuse you.","Before copying anyone's stop loss in points, open the specification and check the digits of your own broker."]

s = open(SRC, encoding='utf-8').read()
old_vid = 'RB0wCB3Q9MQ'
# head
s = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', s, 1)
for k in ['description','twitter:title','twitter:description']:
    pass
s = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>'+DESC, s, 1)
s = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>'+TITLE, s, 1)
s = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>'+DESC, s, 1)
s = re.sub(r'(<meta name="twitter:title" content=")[^"]*', r'\g<1>'+TITLE, s, 1)
s = re.sub(r'(<meta name="twitter:description" content=")[^"]*', r'\g<1>'+DESC, s, 1)
s = s.replace('https://qaziforextips.com/lesson-xauusd-gold-buy-sell-forex-hours.html', URL)
# schema
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
g = json.loads(m.group(1))
L = len(CH); tot = sec(LEN)
for n in g['@graph']:
    t = n.get('@type')
    if t == 'VideoObject':
        n['name'] = 'What is Pip in Forex? Spread, Bid Ask, Point & Gold Pip (Urdu/Hindi) | Lesson 2.1'
        n['description'] = DESC; n['uploadDate'] = DATE+'T20:30:00+05:00'; n['duration'] = DUR
        n['hasPart'] = [{"@type":"Clip","name":c[1],"startOffset":sec(c[0]),"endOffset":(sec(CH[i+1][0]) if i+1<L else tot),"url":f"https://www.youtube.com/watch?v={VID}&t={sec(c[0])}s"} for i,c in enumerate(CH)]
    elif t == 'Article':
        n['headline'] = H1; n['description'] = DESC
        n['image'] = [{"@type":"ImageObject","url":"https://qaziforextips.com/"+HERO+".jpg","width":1200,"height":675,"caption":HERO_ALT}, f"https://i.ytimg.com/vi/{VID}/maxresdefault.jpg"]
        n['datePublished'] = n['dateModified'] = DATE+'T20:30:00+05:00'
    elif t == 'FAQPage':
        n['mainEntity'] = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]
    elif t == 'BreadcrumbList':
        n['itemListElement'][-1]['name'] = 'Lesson 2.1: Bid, ask, spread, pip, point and gold pip'
js = json.dumps(g, ensure_ascii=False).replace(old_vid, VID)
s = s[:m.start(1)] + js + s[m.end(1):]
s = s.replace(old_vid, VID)
# hero
s = re.sub(r'<span>Lesson 1\.5</span>', '<span>Lesson 2.1</span>', s, 1)
s = re.sub(r'<div class="ls-meta">.*?</div>', f'<div class="ls-meta">Forex Basics: Zero to Hero · Module 2 · Lesson 2.1 · {LEN} video · Urdu / Hindi</div>', s, 1)
s = re.sub(r'<h1>.*?</h1>', f'<h1>{H1}</h1>', s, 1, flags=re.S)
LEAD = "You buy EURUSD on a demo account and before the market moves a single point your profit shows minus 12 cents. And one friend says gold moved 30 pips today while another says 300 pips, looking at the same chart. This first lesson of Module 2 of Forex Basics: Zero to Hero clears up both puzzles: bid and ask price, what spread really costs you, why the MT5 chart shows the bid and how a sell stop loss gets hit by the ask, what a pip, a pipette and an MT5 point are, and how the gold (XAUUSD) pip, point and tick work, including the 2-digit vs 3-digit broker trap."
s = re.sub(r'<p class="ls-lead">.*?</p>', f'<p class="ls-lead">{LEAD}</p>', s, 1, flags=re.S)
s = s.replace('Updated 24 November 2026', 'Updated 25 November 2026')
s = re.sub(r'img/forex-basics/xauusd-gold-chart-vs-jeweller-tola-3d-lesson-1-5', HERO, s)
s = re.sub(r'(<figure class="fb-art ls-art3d">.*?alt=")[^"]*', r'\g<1>'+HERO_ALT, s, 1, flags=re.S)
s = re.sub(r'(<iframe src="https://www.youtube.com/embed/'+VID+r'\?rel=0" title=")[^"]*', r'\g<1>'+H1+' – video lesson', s, 1)
s = s.replace('Watch in Urdu / Hindi · 17:44', 'Watch in Urdu / Hindi · '+LEN)
# covers
s = re.sub(r'<div class="covers"><h2>In this lesson</h2><ul>.*?</ul>', '<div class="covers"><h2>In this lesson</h2><ul>'+''.join(f'<li>{html.escape(c)}</li>' for c in COVERS)+'</ul>', s, 1, flags=re.S)
# chapters
s = re.sub(r'<h2>Video chapters</h2><ul>.*?</ul>', '<h2>Video chapters</h2><ul>'+''.join(f'<li><a href="https://www.youtube.com/watch?v={VID}&amp;t={sec(a)}s" target="_blank" rel="noopener">{a}</a> {html.escape(b)}</li>' for a,b in CH)+'</ul>', s, 1, flags=re.S)
# notes: between "<h2>Lesson notes</h2>" and '<div class="urdu">'
i = s.index('<h2>Lesson notes</h2>')+len('<h2>Lesson notes</h2>'); j = s.index('    <div class="urdu">', i)
s = s[:i] + '\n' + NOTES + '\n' + s[j:]
# takes
s = re.sub(r'(<div class="take">.*?</div></div>)(<blockquote>.*?)(</div>)', lambda mm: mm.group(1)+''.join(f'<blockquote><p>{html.escape(t)}</p><cite>From this lesson</cite></blockquote>' for t in TAKES)+mm.group(3), s, 1, flags=re.S)
s = re.sub(r'<div class="urdu"><h2>Khulasa \(Roman Urdu / Hindi\)</h2><ul>.*?</ul>', '<div class="urdu"><h2>Khulasa (Roman Urdu / Hindi)</h2><ul>'+''.join(f'<li>{html.escape(k)}</li>' for k in KHULASA)+'</ul>', s, 1, flags=re.S)
s = re.sub(r'<div class="ls-faq"><h2>Questions</h2>.*?</div>', '<div class="ls-faq"><h2>Questions</h2>'+''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q,a in FAQ)+'</div>', s, 1, flags=re.S)
s = re.sub(r'<figure class="ls-summary".*?</figure>\n', '', s, 1, flags=re.S)
s = re.sub(r'<div class="rel">.*?</div>', '<div class="rel"><a href="guide-what-is-a-pip.html"><small>Guide</small><span>What is a pip in forex? Pip value and how to count pips</span></a><a href="guide-what-is-spread.html"><small>Guide</small><span>What is spread in forex? Bid, ask and the cost of a trade</span></a><a href="lesson-xauusd-gold-buy-sell-forex-hours.html"><small>Forex Basics</small><img src="https://i.ytimg.com/vi/RB0wCB3Q9MQ/mqdefault.jpg" alt="" loading="lazy" width="320" height="180"><span>Lesson 1.5: XAUUSD, gold, buy and sell, forex hours</span></a></div>', s, 1, flags=re.S)
s = re.sub(r'<nav class="pn" aria-label="Lessons">.*?</nav>', '<nav class="pn" aria-label="Lessons"><a href="lesson-xauusd-gold-buy-sell-forex-hours.html"><small>‹ Previous lesson</small><b>XAUUSD, gold, buy and sell, forex 24/5</b></a><a class="nx" href="forex-basics-course.html"><small>Next lesson ›</small><b>Lot size (Lesson 2.2)</b></a></nav>', s, 1, flags=re.S)
open(OUT, 'w', encoding='utf-8').write(s)
print('ok', len(s), s.count(VID), s.count(old_vid))
