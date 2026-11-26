import re, json, html
SRC = 'lesson-bid-ask-spread-pip-point-pipette-gold.html'
OUT = 'lesson-lot-size-pip-value-calculation.html'
URL = 'https://qaziforextips.com/' + OUT
VID = 'szP5-vlipFs'
TITLE = 'How to Calculate Lot Size &amp; Pip Value in Forex (10 Pip Rule) | Lesson 2.2'
TITLE_T = 'How to Calculate Lot Size & Pip Value in Forex (10 Pip Rule) | Lesson 2.2'
DESC = 'How to calculate lot size and pip value in forex: standard, mini and micro lots, the 10 pip rule, USDJPY and gold pip value, MT5 tick value, and lot size from risk.'
H1 = 'How to calculate lot size and pip value in forex: the 10 pip rule, USDJPY, gold and lot size from risk (Lesson 2.2)'
HERO = 'img/forex-basics/lot-size-pip-value-10-pip-rule-3d-lesson-2-2'
HERO_ALT = '3D lot size and pip value: a 10 pip EURUSD move pays $1 on 0.01 lot, $10 on 0.10 lot and $100 on 1.00 lot (Lesson 2.2)'
DATE = '2026-11-26'
LEN = '13:49'; DUR = 'PT13M49S'
CH = [("0:00","Same trade, $2 vs $200 loss"),("1:01","Lesson 2.2 overview"),("1:40","What is lot size in forex (rice shop example)"),("3:51","What is pip value"),("4:41","The 10 pip rule (0.01, 0.10, 1.00 lot)"),("6:27","USDJPY pip value and cross pairs"),("7:33","Gold (XAUUSD) lot size and pip value"),("8:19","Contract size and tick value in MT5"),("9:35","How to calculate lot size from risk"),("10:33","Small account: the 0.01 minimum lot"),("11:26","3 lot size mistakes"),("12:06","Summary"),("12:44","Practical task")]
def sec(t):
    m,s=t.split(':');return int(m)*60+int(s)
COVERS = ["Why the same trade lost $2 for one trader and $200 for another","What a lot is: standard (1.00), mini (0.10) and micro (0.01) lots, with a rice shop example","Units are always of the base currency","The Volume box in MT5 is your lot size","Leverage decides margin, lot size decides profit and loss","Pip value formula: pip size × units, in the quote currency","The 10 pip rule: $1, $10 and $100 on EURUSD-type pairs","USDJPY pip value (about $6.3 per lot at 159) and cross pairs like EURGBP","Gold (XAUUSD): $1 move = $1 on 0.01 lot, $100 on 1 lot","Reading contract size, tick size and tick value in the MT5 specification","How professionals calculate lot size from risk and stop loss","Why 0.01 can be too big on a $100 account","3 lot size mistakes and a practical task"]
NOTES = """<h2>Why the same trade can lose $2 or $200</h2><p>Two friends buy EURUSD at the same price with the stop loss 20 pips away. The market falls and both stops are hit. One loses <b>$2</b>, the other <b>$200</b>. Same chart, same entry, same stop: the only difference is the <b>lot size</b>. The first used 0.01 lot and the second 1.00 lot. This lesson shows exactly how that happens and how to choose the right size before every trade.</p>
<h2>What is lot size in forex?</h2><p>A rice shop sells a 100 kg sack, a 10 kg bag and a 1 kg packet. If the rate rises by 10 rupees a kilo, the sack owner gains 1,000 rupees, the bag owner 100 and the packet owner only 10. The rate moved the same for everyone; the gain depends on how much stock you hold. In forex that quantity is the <b>lot</b>: how many units of currency you buy or sell.</p>
<table><tr><th>Lot</th><th>Name</th><th>Units</th><th>Rice shop</th></tr><tr><td>1.00</td><td>Standard lot</td><td>100,000</td><td>Sack</td></tr><tr><td>0.10</td><td>Mini lot</td><td>10,000</td><td>Bag</td></tr><tr><td>0.01</td><td>Micro lot</td><td>1,000</td><td>Packet</td></tr></table>
<p>The units are always of the <b>first (base) currency</b>: one lot of EURUSD is 100,000 euros, paid for in dollars. At most brokers 0.01 is the smallest lot, and each size is ten times the one below it. In MT5 you rarely see the word lot: the <b>Volume</b> box in the order window is your lot size. Typing 1 instead of 0.01 makes the trade a hundred times bigger.</p>
<p>How does a small account open 100,000 euros? Through leverage and margin, which get their own module. For now remember: <b>leverage decides how much money is blocked to open the trade; lot size decides how much you win or lose.</b></p>
<h2>What is pip value?</h2><p>A pip is a distance in price (0.0001 on EURUSD, see <a href="lesson-bid-ask-spread-pip-point-pipette-gold.html">Lesson 2.1</a>). <b>Pip value</b> is how much money changes in your account when price moves one pip. The formula is simple:</p>
<p><b>Pip value = pip size × units</b>, and the answer is in the <b>quote (second) currency</b>. EURUSD, 1 lot: 0.0001 × 100,000 = 10, and the quote currency is the dollar, so <b>1 pip = $10 per lot</b>.</p>
<h2>The 10 pip rule (EURUSD and other pairs with USD second)</h2><table><tr><th>Lot</th><th>Units</th><th>10 pips</th><th>1 pip</th></tr><tr><td>0.01</td><td>1,000</td><td>$1</td><td>$0.10</td></tr><tr><td>0.10</td><td>10,000</td><td>$10</td><td>$1</td></tr><tr><td>1.00</td><td>100,000</td><td>$100</td><td>$10</td></tr></table>
<p>Ten times the lot, ten times the money. Back to the two friends: a 20 pip stop is double 10 pips, so 0.01 lot lost $2 and 1.00 lot lost $200 (0.10 lot would have lost $20). On a $500 account that 1 lot trade took 40% in one go. The rule works on every pair where the dollar comes second, such as GBPUSD and AUDUSD, whatever the price. Remember the line: <b>the pip is distance, the lot is weight; money is the two multiplied.</b></p>
<h2>USDJPY and cross pairs: pip value changes with price</h2><p>On USDJPY a pip is 0.01. 0.01 × 100,000 = 1,000, but that is <b>1,000 yen</b>, not dollars. With USDJPY around 159 (November 2026), 1,000 ÷ 159 ≈ <b>$6.29 per pip per lot</b>, not $10. The higher USDJPY goes, the smaller this value becomes. On pairs without the dollar, such as EURGBP, pip value is first in the quote currency (pounds) and then converted to dollars. MT5 does this conversion for you. The same pips on different pairs are not the same dollars.</p>
<h2>Gold (XAUUSD) lot size and pip value</h2><p>In gold, count dollars, not pips. One lot of gold is usually <b>100 ounces</b>, so a $1 move in the gold price is <b>$100 on 1 lot, $10 on 0.10 lot and $1 on 0.01 lot</b>. Gold often moves $20 to $50 in a normal day, which is $20 to $50 even on 0.01 lot, while EURUSD on the same lot usually moves a few dollars. A lot that feels small on EURUSD is a much bigger risk on gold.</p>
<h2>Check it yourself: contract size and tick value in MT5</h2><p>In Market Watch right-click the symbol and open <b>Specification</b>.</p><ul><li><b>EURUSD:</b> contract size 100,000 (units of 1 lot), minimal volume 0.01, volume step 0.01. On a 5-digit broker the tick size is one pipette and the tick value is $1; ten pipettes make a pip, so $1 × 10 = <b>$10 per pip per lot</b>, the same as the formula.</li><li><b>Gold:</b> contract size 100, tick size 0.01, tick value $1. A $1 move has 100 ticks, so $100 per lot.</li></ul><p>Contract sizes differ between brokers, and on a cent account everything is in cents, so check your own broker once.</p>
<h2>How to calculate lot size from risk (the professional way)</h2><p>A beginner picks a lot first and hopes. A professional works backwards: first the maximum dollars he accepts losing, then the stop loss where the chart says it belongs, and only then the lot.</p>
<p><b>Lot = risk in dollars ÷ (stop loss in pips × pip value of 1 lot)</b></p>
<p>Example: $500 account, 1% risk = $5, stop loss 25 pips on EURUSD. 25 × $10 = $250, and $5 ÷ $250 = <b>0.02 lot</b>. If the stop is hit, you lose only $5. Our free <a href="lot-size-calculator.html">lot size calculator</a> does this maths for forex and gold, and the <a href="trade-assistant.html">QFT Trade Assistant</a> does it inside MT5.</p>
<h2>Small accounts: when even 0.01 lot is too big</h2><p>A $100 account risking 1% ($1) with a 20 pip stop needs 1 ÷ (20 × 10) = <b>0.005 lot</b>, but most brokers' smallest lot is 0.01, which doubles the risk to 2%. Don't shrink the stop loss to fit the lot: the chart decides where the stop goes. Either skip the trade or take the 2% risk knowingly. (A cent account is another way small traders size down; it comes up in the next lessons.) Read more in <a href="guide-risk-management-in-forex.html">risk management in forex</a>.</p>
<h2>3 lot size mistakes to avoid</h2><ol><li>Treating 0.1 and 0.01 as the same: one zero is ten times the risk.</li><li>Using the same lot on every pair and on gold and assuming the risk is the same, when pip value and movement both differ.</li><li>Doubling the lot after a loss to win it all back. This habit blows up more accounts than anything else. Increase the lot by calculation, not emotion.</li></ol>
<h2>Practical task</h2><p>1) In your demo MT5 open the specification of EURUSD, USDJPY and gold, and work out the pip value of each on 0.01 lot. 2) Open the free <a href="lot-size-calculator.html">lot size calculator</a>, enter a $500 account, 1% risk and a 25 pip stop loss. If you get 0.02, today's lesson is locked in. Write your USDJPY pip value in the YouTube comments. Next lesson: profit and loss in dollars, account currency and risk to reward.</p>"""
KHULASA = ["Lot = kitna maal: 1.00 lot = 100,000 units (sack), 0.10 = 10,000 (bag), 0.01 = 1,000 (packet). Units hamesha pehli (base) currency ki.","MT5 mein Volume box hi lot size hai. Leverage margin tay karta hai, nafa nuqsaan lot size tay karta hai.","Pip value = pip size x units, aur jawab doosri (quote) currency mein. EURUSD 1 lot par 1 pip = $10.","10 pip rule: 10 pips par 0.01 lot = $1, 0.10 = $10, 1.00 = $100. Pip doori hai, lot wazan.","USDJPY par 1 lot ka pip 1,000 yen, 159 ke rate par taqreeban $6.3. Cross pairs mein MT5 khud dollar mein badalta hai.","Gold: 1 lot = 100 oz. $1 move = 0.01 lot par $1, 1 lot par $100.","Pehle risk, phir stop loss, phir lot: lot = risk $ / (SL pips x 1 lot ki pip value). $500, 1%, 25 pips = 0.02 lot.","$100 account par 0.01 bhi bara ho sakta hai: SL chhota na karein, trade chhorein ya 2% risk jaan boojh kar lein."]
FAQ = [("How do you calculate pip value in forex?","Multiply the pip size by the number of units: pip value = pip size × units, in the quote currency. On EURUSD one lot is 100,000 units, so 0.0001 × 100,000 = $10 per pip. On 0.10 lot it is $1 and on 0.01 lot $0.10."),
("What is the 10 pip rule?","On EURUSD and other pairs where USD is the second currency, a 10 pip move is worth $1 on 0.01 lot, $10 on 0.10 lot and $100 on 1.00 lot. Ten times the lot means ten times the money."),
("How do I calculate lot size from my risk?","Lot = risk in dollars ÷ (stop loss in pips × pip value of 1 lot). With a $500 account, 1% risk ($5) and a 25 pip EURUSD stop: 5 ÷ (25 × 10) = 0.02 lot."),
("What is the pip value of USDJPY and gold?","USDJPY: 1,000 yen per pip per lot, about $6.29 at a price of 159, and it falls as USDJPY rises. Gold (100 oz contract): a $1 move is $100 on 1 lot, $10 on 0.10 lot and $1 on 0.01 lot."),
("لاٹ سائز کیا ہوتا ہے؟","لاٹ بتاتا ہے کہ آپ کتنی کرنسی خرید یا بیچ رہے ہیں۔ ایک اسٹینڈرڈ لاٹ میں ایک لاکھ یونٹ، منی لاٹ میں دس ہزار اور مائیکرو لاٹ یعنی صفر اعشاریہ صفر ایک میں ایک ہزار یونٹ ہوتے ہیں۔"),
("سو ڈالر کے اکاؤنٹ پر کتنا لاٹ لیں؟","پہلے رسک طے کریں، پھر چارٹ کے مطابق سٹاپ لاس، پھر لاٹ نکالیں۔ اگر حساب صفر اعشاریہ صفر ایک سے بھی کم آئے تو سٹاپ لاس چھوٹا نہ کریں، یا ٹریڈ چھوڑ دیں یا زیادہ رسک جان بوجھ کر لیں۔"),
("0.01 lot par 10 pips ka kitna profit hota hai?","EURUSD jaise pairs par 0.01 lot par 10 pips = $1 profit ya loss. 0.10 lot par $10 aur 1 lot par $100.")]
TAKES = ["The pip is distance and the lot is weight. However small the distance, if the weight is big, the loss will be big.","Lot size is not a guess, it is a calculation: risk first, then stop loss, then lot.","The chart decides where the stop loss goes, not your wish. Never shrink the stop to fit a lot."]

s = open(SRC, encoding='utf-8').read()
old_vid = '6_r9hTuMSjo'
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
        n['name'] = 'How to Calculate Lot Size & Pip Value in Forex | EURUSD & Gold (Urdu/Hindi) | Lesson 2.2'
        n['description'] = DESC; n['uploadDate'] = DATE+'T20:30:00+05:00'; n['duration'] = DUR
        n['hasPart'] = [{"@type":"Clip","name":c[1],"startOffset":sec(c[0]),"endOffset":(sec(CH[i+1][0]) if i+1<L else tot),"url":f"https://www.youtube.com/watch?v={VID}&t={sec(c[0])}s"} for i,c in enumerate(CH)]
    elif t == 'Article':
        n['headline'] = H1; n['description'] = DESC
        n['image'] = [{"@type":"ImageObject","url":"https://qaziforextips.com/"+HERO+".jpg","width":1200,"height":1200,"caption":HERO_ALT}, f"https://i.ytimg.com/vi/{VID}/maxresdefault.jpg"]
        n['datePublished'] = n['dateModified'] = DATE+'T20:30:00+05:00'
    elif t == 'FAQPage':
        n['mainEntity'] = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]
    elif t == 'BreadcrumbList':
        n['itemListElement'][-1]['name'] = 'Lesson 2.2: Lot size and pip value'
js = json.dumps(g, ensure_ascii=False).replace(old_vid, VID)
s = s[:m.start(1)] + js + s[m.end(1):]
s = s.replace(old_vid, VID)
# hero
s = re.sub(r'<span>Lesson 2\.1</span>', '<span>Lesson 2.2</span>', s, 1)
s = re.sub(r'<div class="ls-meta">.*?</div>', f'<div class="ls-meta">Forex Basics: Zero to Hero · Module 2 · Lesson 2.2 · {LEN} video · Urdu / Hindi</div>', s, 1)
s = re.sub(r'<h1>.*?</h1>', f'<h1>{H1}</h1>', s, 1, flags=re.S)
LEAD = "Two friends take exactly the same EURUSD trade with the same 20 pip stop loss. Both stops are hit: one loses $2, the other $200. The only difference is the lot size. This lesson of Forex Basics: Zero to Hero explains what a lot is (standard, mini and micro) with a rice shop example, how to calculate pip value, the 10 pip rule that makes the money side easy, why USDJPY, cross pairs and gold pay differently, how to read contract size and tick value in MT5, and how professionals calculate lot size from their risk, including why even 0.01 lot can be too big on a $100 account."
s = re.sub(r'<p class="ls-lead">.*?</p>', f'<p class="ls-lead">{LEAD}</p>', s, 1, flags=re.S)
s = s.replace('Updated 25 November 2026', 'Updated 26 November 2026')
s = re.sub(r'img/forex-basics/bid-ask-spread-pip-point-mt5-quote-3d-lesson-2-1', HERO, s)
s = s.replace('width="1200" height="675" alt="'+HERO_ALT, 'width="1200" height="1200" alt="'+HERO_ALT)
s = re.sub(r'(<figure class="fb-art ls-art3d">.*?alt=")[^"]*', r'\g<1>'+HERO_ALT, s, 1, flags=re.S)
s = re.sub(r'(<iframe src="https://www.youtube.com/embed/'+VID+r'\?rel=0" title=")[^"]*', r'\g<1>'+H1+' – video lesson', s, 1)
s = s.replace('Watch in Urdu / Hindi · 12:51', 'Watch in Urdu / Hindi · '+LEN)
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
s = re.sub(r'<div class="rel">.*?</div>', '<div class="rel"><a href="lot-size-calculator.html"><small>Free tool</small><span>Lot size calculator for forex and gold (XAUUSD)</span></a><a href="lesson-lot-size.html"><small>Price Action course</small><span>What is lot size in forex? 0.01 lot and pip value</span></a><a href="guide-what-is-a-pip.html"><small>Guide</small><span>What is a pip in forex? Pip value explained</span></a><a href="lesson-bid-ask-spread-pip-point-pipette-gold.html"><small>Forex Basics</small><img src="https://i.ytimg.com/vi/6_r9hTuMSjo/mqdefault.jpg" alt="" loading="lazy" width="320" height="180"><span>Lesson 2.1: Bid, ask, spread, pip, point and gold pip</span></a></div>', s, 1, flags=re.S)
s = re.sub(r'<nav class="pn" aria-label="Lessons">.*?</nav>', '<nav class="pn" aria-label="Lessons"><a href="lesson-bid-ask-spread-pip-point-pipette-gold.html"><small>‹ Previous lesson</small><b>Bid, ask, spread, pip, point and gold pip</b></a><a class="nx" href="forex-basics-course.html"><small>Next lesson ›</small><b>Profit/loss, account currency, risk:reward (Lesson 2.3)</b></a></nav>', s, 1, flags=re.S)
open(OUT, 'w', encoding='utf-8').write(s)
print('ok', len(s), s.count(VID), s.count(old_vid))
