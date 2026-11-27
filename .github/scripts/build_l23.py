import re, json, html
SRC = 'lesson-lot-size-pip-value-calculation.html'
OUT = 'lesson-risk-to-reward-ratio-profit-loss-calculation.html'
URL = 'https://qaziforextips.com/' + OUT
VID = 'DDglYjbFI1M'
TITLE = 'Risk to Reward Ratio in Forex &amp; Profit/Loss Calculation | Lesson 2.3'
DESC = 'Risk to reward ratio in forex explained with examples: how to calculate profit and loss, account currency, cent accounts, equal risk per trade and breakeven win rate.'
H1 = 'Risk to reward ratio in forex trading and how to calculate profit and loss (Lesson 2.3)'
HERO = 'img/forex-basics/risk-to-reward-ratio-profit-loss-calculation-3d-lesson-2-3'
HERO_ALT = '3D risk to reward ratio: $10 risk with a 20 pip stop loss vs $20 reward with a 40 pip take profit, a 1:2 ratio with a 33% breakeven win rate (Lesson 2.3)'
DATE = '2026-11-27'
LEN = '15:34'; DUR = 'PT15M34S'
CH = [("0:00","61% win rate but account blown?"),("1:15","3 parts of this lesson"),("1:36","How to calculate forex profit and loss"),("2:32","Buy example: EURUSD +$50"),("2:53","Sell example with 0.01 lot"),("3:38","Gold profit calculation"),("4:35","Floating P/L, equity and balance in MT5"),("5:08","Account currency explained"),("5:59","USDJPY profit in dollars"),("6:32","Cross pair (EURGBP) conversion"),("7:04","Cent account explained"),("7:45","What is risk to reward ratio"),("8:19","Full example: $1,000 account, 1% risk"),("9:01","Equal risk on every trade"),("10:45","Breakeven win rate formula"),("11:10","10 trades example and the 90% trap"),("12:06","Why the 61% trader lost"),("12:52","3 common mistakes"),("13:22","1-minute summary"),("14:09","Practical task"),("15:08","Next lesson: real trading costs")]
def sec(t):
    m,s=t.split(':');return int(m)*60+int(s)
COVERS = ["Why a trader can win 61% of trades and still lose money (43 million trade study)","Profit or loss = pips moved × pip value, and which direction is profit for buy and sell","Worked examples: EURUSD buy +$50, EURUSD sell 0.01 lot, gold at 0.01, 0.10 and 1 lot","Floating profit, equity and balance in MT5, and why a new trade starts slightly negative","Account currency: why a USDJPY or EURGBP profit arrives in dollars","Cent accounts: why 100 on screen is only $1","What risk to reward ratio means (1:1, 1:2, 1:3) with a $1,000 account and 1% risk","Equal risk on every trade: changing the lot with the stop loss","Breakeven win rate formula 1 ÷ (1 + R) and the 10 trade example","The 90% win-rate trap, 3 common mistakes and a practical task"]
NOTES = """<h2>Why a 61% win rate can still lose money</h2><p>A study by a large broker of more than <b>43 million real trades</b> (2014–2015) found that on EURUSD traders closed about <b>61%</b> of their trades in profit. Yet the average winning trade was about <b>48 pips</b> and the average losing trade about <b>83 pips</b>. Do the maths: 0.61 × 48 − 0.39 × 83 ≈ <b>−3 pips per trade</b>. They won more often, but every loss was bigger than a win. By the end of this lesson you will be able to work out the profit or loss of any trade before you open it, and see why risk to reward matters more than win rate.</p>
<h2>How to calculate profit and loss in forex</h2><p>You need three things: the <b>entry</b> price, the <b>exit</b> price and the <b>lot size</b>. The formula is one line:</p><p><b>Profit or loss = pips moved × pip value</b></p><p>Remember the line from <a href="lesson-lot-size-pip-value-calculation.html">Lesson 2.2</a>: the pip is distance, the lot is weight, and money is the two multiplied. First check the direction: in a <b>buy</b>, price going up is profit and down is loss; in a <b>sell</b> it is the opposite, price going down is profit.</p>
<table><tr><th>Trade</th><th>Move</th><th>Pip value</th><th>Result</th></tr><tr><td>EURUSD buy 1.1000 → 1.1050, 0.10 lot</td><td>+50 pips</td><td>$1</td><td>+$50</td></tr><tr><td>EURUSD sell 1.1000 → 1.0980, 0.01 lot</td><td>20 pips down</td><td>$0.10</td><td>+$2 (−$2 if price went up)</td></tr><tr><td>Gold buy 3,570 → 3,590, 0.01 lot</td><td>$20 move</td><td>$1 per $1</td><td>+$20</td></tr><tr><td>Same gold move, 0.10 lot</td><td>$20 move</td><td>$10 per $1</td><td>±$200</td></tr><tr><td>Same gold move, 1.00 lot</td><td>$20 move</td><td>$100 per $1</td><td>±$2,000</td></tr></table>
<p>In gold, count dollars, not pips. The same $20 move is $20, $200 or $2,000 depending only on the lot, which is why a beginner always starts with 0.01. Check your numbers with the free <a href="lot-size-calculator.html">lot size calculator</a>.</p>
<h2>Floating profit, equity and balance in MT5</h2><p>While a trade is open its profit or loss is <b>floating</b>: it changes every second and shows in your <b>equity</b>. Only when the trade closes does it become real money and your <b>balance</b> changes. Right after opening, every trade shows a small minus because of the spread, explained in <a href="lesson-bid-ask-spread-pip-point-pipette-gold.html">Lesson 2.1</a>.</p>
<h2>Account currency: why your profit comes in dollars</h2><p>Your <b>account currency</b> is the currency your balance is written in, usually US dollars. The rule: <b>profit is born in the pair's second (quote) currency and comes home in your account currency</b>. MT5 converts it for you.</p><ul><li><b>EURUSD, dollar account:</b> the quote currency is already USD, so nothing is converted (the +$50 example).</li><li><b>USDJPY, dollar account:</b> 1 lot bought at 159.00 and closed at 159.50 is 50 pips = <b>¥50,000</b>. 50,000 ÷ 159 ≈ <b>$314</b>.</li><li><b>EURGBP (cross pair), dollar account:</b> 40 pips on 1 lot = <b>£400</b>. With GBPUSD around 1.31 that is about <b>$524</b>. On screen you only see the final dollar number.</li></ul>
<h2>Cent account explained</h2><p>On a <b>cent account</b> the balance is written in cents: $1 = 100 cents. Deposit $10 and the account shows 1,000. The money is the same, only the way it is written changes. So a profit of 100 on screen is 100 cents, <b>just $1</b>. Cent accounts differ between brokers, so check your account currency once.</p>
<h2>What is risk to reward ratio?</h2><p>Every trade has two distances. Entry to <b>stop loss</b> is your <b>risk</b>; entry to <b>take profit</b> is your <b>reward</b>. A 20 pip stop loss and a 40 pip take profit is a <b>1:2 risk to reward ratio</b>: one part risk, two parts reward.</p>
<p><b>Full example:</b> a $1,000 account risking 1% per trade risks $10. With a 20 pip EURUSD stop loss, 0.05 lot makes 20 pips worth exactly $10. Then 1:1 is a $10 target, 1:2 is $20 and 1:3 (60 pips) is $30. Before you open the trade you already know the most you can lose and what can come in. This is the foundation of <a href="guide-risk-management-in-forex.html">risk management in forex</a>.</p>
<h2>Equal risk on every trade</h2><p>If you want to succeed in forex, take the <b>same risk on every trade</b>: the lot changes, the risk does not. With a $1,000 account and $10 (1%) risk, first see on the chart how many pips the stop loss needs, then size the lot:</p>
<table><tr><th>Stop loss</th><th>Lot</th><th>Loss if hit</th></tr><tr><td>10 pips</td><td>0.10</td><td>$10</td></tr><tr><td>50 pips</td><td>0.02</td><td>$10</td></tr><tr><td>100 pips</td><td>0.01</td><td>$10</td></tr></table>
<p>With a fixed lot, the trade with the bigger stop loss also has the bigger loss, and that is exactly how "small wins, big losses" begins. If the maths gives 0.033 lot (30 pip stop), always round <b>down</b> to 0.03 so the risk stays at or below $10 ($9). Practise lot sizing every day.</p>
<h2>Breakeven win rate: 1 ÷ (1 + R)</h2><table><tr><th>Risk to reward</th><th>Win rate needed to break even</th></tr><tr><td>1:1</td><td>50%</td></tr><tr><td>1:1.5</td><td>40%</td></tr><tr><td>1:2</td><td>33% (one in three)</td></tr><tr><td>1:3</td><td>25% (one in four)</td></tr></table>
<p><b>10 trades at 1:2:</b> $10 risk and a $20 target. Win only 4: +$80. Lose 6: −$60. Result <b>+$20</b>, with less than half the trades won. <b>The 90% trap:</b> win 9 trades at $5 each (+$45) and lose one with a far stop loss (−$60): a 90% win rate and still <b>−$15</b>. Counting wins is only a feeling; real money is made by risk to reward. One professional caution: set the stop loss from the chart first, then put the take profit at a real level. Don't push the target far just to make the ratio look bigger, or price will never reach it.</p>
<h2>3 common mistakes</h2><ol><li>Doing the sell trade maths backwards and calling price going up a profit.</li><li>Seeing 100 profit on a cent account and thinking it is $100.</li><li>Closing winners early and leaving losers open, the habit that builds an account that loses while winning.</li></ol>
<h2>Practical task</h2><p>On paper write a trade: EURUSD buy at 1.1000, stop loss 20 pips below, take profit 40 pips above, 0.01 lot. Work out the risk in dollars, the reward in dollars and the risk to reward ratio. Then answer in the YouTube comments: with a $1,000 account, 1% risk and 1:3, how many dollars is one winning trade? Next lesson: the real cost of a trade (spread, commission, swap, triple swap and slippage).</p>"""
KHULASA = ["Profit/loss = kitne pips chale x pip value. Buy mein price upar = profit, sell mein price neeche = profit.","Gold mein pips nahi, dollar ginein: $20 move = 0.01 lot par $20, 0.10 par $200, 1 lot par $2,000.","Trade khuli ho to profit floating hai (equity mein). Band hone par hi balance badalta hai.","Profit pair ki doosri currency mein banta hai aur account currency mein aata hai: USDJPY 50 pips 1 lot = ¥50,000 ≈ $314.","Cent account mein 100 ka matlab $1 hai, $100 nahi.","Risk to reward: SL 20 pips, TP 40 pips = 1:2. $1,000 account, 1% = $10 risk.","Har trade par barabar risk: SL 10 pips = 0.10 lot, 50 pips = 0.02, 100 pips = 0.01, nuqsaan har baar $10. Lot hamesha neeche round karein.","Breakeven jeet = 1 / (1 + R): 1:2 par sirf 33% jeet kaafi hai. 90% jeet ke saath bhi bara loss account dubo deta hai."]
FAQ = [("What is risk to reward ratio in forex?","It compares how much you can lose to how much you aim to gain on a trade. Entry to stop loss is the risk and entry to take profit is the reward. A 20 pip stop loss with a 40 pip take profit is a 1:2 risk to reward ratio."),
("How do you calculate profit and loss in forex?","Profit or loss = pips moved × pip value. On EURUSD 0.10 lot (pip value $1), a 50 pip move is $50. On 0.01 lot (pip value $0.10), 20 pips is $2. In a buy, price going up is profit; in a sell, price going down is profit."),
("What win rate do I need with a 1:2 risk to reward?","Breakeven win rate = 1 ÷ (1 + R). At 1:2 it is 1 ÷ 3 = 33%, so winning one trade in three covers the losses. At 1:1 you need 50% and at 1:3 only 25%."),
("Why does my EURGBP or USDJPY profit show in dollars?","Profit is made in the pair's second currency (pounds or yen) and MT5 converts it into your account currency. For example ¥50,000 at USDJPY 159 is about $314."),
("رسک ٹو ریوارڈ کیا ہوتا ہے؟","انٹری سے سٹاپ لاس تک کا فاصلہ رسک ہے اور انٹری سے ٹیک پرافٹ تک کا فاصلہ ریوارڈ۔ اگر سٹاپ لاس بیس پِپ اور ٹیک پرافٹ چالیس پِپ ہو تو رسک ٹو ریوارڈ ایک اور دو ہے۔"),
("ہر ٹریڈ پر برابر رسک کیسے لیں؟","پہلے رسک ڈالر میں طے کریں، پھر چارٹ سے سٹاپ لاس کے پِپ دیکھیں اور لاٹ اس کے حساب سے بدلیں۔ ایک ہزار ڈالر اور دس ڈالر رسک پر دس پِپ سٹاپ لاس کے لیے صفر اعشاریہ ایک لاٹ اور سو پِپ کے لیے صفر اعشاریہ صفر ایک لاٹ۔"),
("Cent account mein 100 profit ka matlab kya hai?","Cent account mein balance cents mein hota hai, is liye 100 profit sirf 100 cents yani $1 hai.")]
TAKES = ["Counting wins is only a feeling. Real money is made by risk to reward.","The lot changes with the stop loss; the risk stays the same on every trade.","Set the stop loss from the chart first, then the take profit at a real level. Never push the target far just to make the ratio look bigger."]

s = open(SRC, encoding='utf-8').read()
old_vid = 'szP5-vlipFs'
# head
s = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', s, 1)
for k in ['description','twitter:title','twitter:description']:
    pass
s = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>'+DESC, s, 1)
s = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>'+TITLE, s, 1)
s = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>'+DESC, s, 1)
s = re.sub(r'(<meta name="twitter:title" content=")[^"]*', r'\g<1>'+TITLE, s, 1)
s = re.sub(r'(<meta name="twitter:description" content=")[^"]*', r'\g<1>'+DESC, s, 1)
s = s.replace('https://qaziforextips.com/lesson-bid-ask-spread-pip-point-pipette-gold.html', URL)
# schema
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
g = json.loads(m.group(1))
L = len(CH); tot = sec(LEN)
for n in g['@graph']:
    t = n.get('@type')
    if t == 'VideoObject':
        n['name'] = 'Risk to Reward Ratio in Forex Trading Explained | Profit & Loss Calculation (Urdu/Hindi) Lesson 2.3'
        n['description'] = DESC; n['uploadDate'] = DATE+'T20:30:00+05:00'; n['duration'] = DUR
        n['hasPart'] = [{"@type":"Clip","name":c[1],"startOffset":sec(c[0]),"endOffset":(sec(CH[i+1][0]) if i+1<L else tot),"url":f"https://www.youtube.com/watch?v={VID}&t={sec(c[0])}s"} for i,c in enumerate(CH)]
    elif t == 'Article':
        n['headline'] = H1; n['description'] = DESC
        n['image'] = [{"@type":"ImageObject","url":"https://qaziforextips.com/"+HERO+".jpg","width":1200,"height":1200,"caption":HERO_ALT}, f"https://i.ytimg.com/vi/{VID}/maxresdefault.jpg"]
        n['datePublished'] = n['dateModified'] = DATE+'T20:30:00+05:00'
    elif t == 'FAQPage':
        n['mainEntity'] = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]
    elif t == 'BreadcrumbList':
        n['itemListElement'][-1]['name'] = 'Lesson 2.3: Risk to reward ratio and profit/loss'
js = json.dumps(g, ensure_ascii=False).replace(old_vid, VID)
s = s[:m.start(1)] + js + s[m.end(1):]
s = s.replace(old_vid, VID)
# hero
s = re.sub(r'<span>Lesson 2\.2</span>', '<span>Lesson 2.3</span>', s, 1)
s = re.sub(r'<div class="ls-meta">.*?</div>', f'<div class="ls-meta">Forex Basics: Zero to Hero · Module 2 · Lesson 2.3 · {LEN} video · Urdu / Hindi</div>', s, 1)
s = re.sub(r'<h1>.*?</h1>', f'<h1>{H1}</h1>', s, 1, flags=re.S)
LEAD = "A trader won 61% of his trades and still lost money: in a study of 43 million real trades, the average EURUSD win was 48 pips and the average loss 83 pips. This lesson of Forex Basics: Zero to Hero shows how to calculate the profit or loss of any trade (EURUSD, USDJPY, EURGBP and gold), why your profit arrives in your account currency, what a cent account really shows, and how the risk to reward ratio, equal risk per trade and the breakeven win rate decide whether an account grows or sinks."
s = re.sub(r'<p class="ls-lead">.*?</p>', f'<p class="ls-lead">{LEAD}</p>', s, 1, flags=re.S)
s = s.replace('Updated 26 November 2026', 'Updated 27 November 2026')
s = re.sub(r'img/forex-basics/lot-size-pip-value-10-pip-rule-3d-lesson-2-2', HERO, s)
s = s.replace('width="1200" height="675" alt="'+HERO_ALT, 'width="1200" height="1200" alt="'+HERO_ALT)
s = re.sub(r'(<figure class="fb-art ls-art3d">.*?alt=")[^"]*', r'\g<1>'+HERO_ALT, s, 1, flags=re.S)
s = re.sub(r'(<iframe src="https://www.youtube.com/embed/'+VID+r'\?rel=0" title=")[^"]*', r'\g<1>'+H1+' – video lesson', s, 1)
s = s.replace('Watch in Urdu / Hindi · 13:49', 'Watch in Urdu / Hindi · '+LEN)
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
s = re.sub(r'<div class="rel">.*?</div>', '<div class="rel"><a href="lot-size-calculator.html"><small>Free tool</small><span>Lot size calculator for forex and gold (XAUUSD)</span></a><a href="guide-risk-management-in-forex.html"><small>Guide</small><span>Risk management in forex: the complete guide</span></a><a href="trade-assistant.html"><small>Free MT5 tool</small><span>QFT Trade Assistant: risk-based lot size in MT5</span></a><a href="lesson-lot-size-pip-value-calculation.html"><small>Forex Basics</small><img src="https://i.ytimg.com/vi/szP5-vlipFs/mqdefault.jpg" alt="" loading="lazy" width="320" height="180"><span>Lesson 2.2: Lot size and pip value (10 pip rule)</span></a></div>', s, 1, flags=re.S)
s = re.sub(r'<nav class="pn" aria-label="Lessons">.*?</nav>', '<nav class="pn" aria-label="Lessons"><a href="lesson-lot-size-pip-value-calculation.html"><small>‹ Previous lesson</small><b>Lot size and pip value (10 pip rule)</b></a><a class="nx" href="forex-basics-course.html"><small>Next lesson ›</small><b>Trade costs: commission, swap and slippage (Lesson 2.4)</b></a></nav>', s, 1, flags=re.S)
open(OUT, 'w', encoding='utf-8').write(s)
print('ok', len(s), s.count(VID), s.count(old_vid))
