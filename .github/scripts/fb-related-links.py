#!/usr/bin/env python3
"""Forex Basics (Zero to Hero) lessons: topic links.
1) In-text links: the first mention of a related topic inside the Lesson notes gets a link (data-smcx="1",
   so forex-basics-build.py keeps it on a rebuild). Only text outside existing links, one link per target.
2) "More on this topic" cards under Related lessons, in a <!--RELX--> block (also kept on a rebuild).
Idempotent: run again after adding a lesson. Run from the repo root.
"""
import re, os

T = {  # target: (label, card title)
 "lesson-how-to-start-forex-trading.html": ("Lesson 0.1", "How to start forex trading: the course roadmap"),
 "lesson-how-to-make-money-in-forex.html": ("Lesson 0.2", "How money is made and lost in forex"),
 "lesson-forex-scams-signal-groups.html": ("Lesson 0.3", "Forex scams and fake signal groups"),
 "lesson-binary-options-vs-forex.html": ("Lesson 0.4", "Binary options vs forex"),
 "lesson-what-is-forex-trading.html": ("Lesson 1.1", "What is forex trading?"),
 "lesson-how-forex-market-works.html": ("Lesson 1.2", "How the forex market works"),
 "lesson-how-forex-brokers-work.html": ("Lesson 1.3", "How forex brokers work"),
 "lesson-currency-pairs-explained.html": ("Lesson 1.4", "Currency pairs: base, quote, major, minor"),
 "lesson-xauusd-gold-buy-sell-forex-hours.html": ("Lesson 1.5", "XAUUSD, buy and sell, forex hours"),
 "lesson-bid-ask-spread-pip-point-pipette-gold.html": ("Lesson 2.1", "Pip, point, pipette and the gold pip"),
 "lesson-lot-size-pip-value-calculation.html": ("Lesson 2.2", "Lot size and pip value calculation"),
 "lesson-risk-to-reward-ratio-profit-loss-calculation.html": ("Lesson 2.3", "Risk to reward and profit/loss"),
 "guide-forex-demo-account-in-pakistan.html": ("Guide", "Forex demo account in Pakistan"),
 "guide-risk-reward-ratio.html": ("Guide", "Risk:reward ratio and break-even win rate"),
 "guide-drawdown-in-forex.html": ("Guide", "Drawdown, losing streaks and recovery"),
 "qa-is-forex-a-scam.html": ("Sawal Jawab", "Is forex a scam?"),
 "guide-forex-signals-in-pakistan.html": ("Guide", "The truth about forex signals"),
 "guide-forex-brokers-in-pakistan.html": ("Guide", "How to choose a regulated broker"),
 "guide-what-is-leverage.html": ("Guide", "What is leverage? Margin and risk"),
 "guide-forex-trading-sessions.html": ("Guide", "Forex market timings in Pakistan and India"),
 "guide-what-is-swap-in-forex.html": ("Guide", "What is swap in forex?"),
 "guide-what-is-a-pip.html": ("Guide", "What is a pip? Pip value explained"),
 "guide-what-is-spread.html": ("Guide", "What is spread? Bid, ask and cost"),
 "guide-gold-trading.html": ("Guide", "Gold (XAUUSD) trading for beginners"),
 "gold-rate-pakistan.html": ("Live rates", "Gold rate in Pakistan today"),
 "lot-size-calculator.html": ("Free tool", "Lot size calculator for forex and Gold"),
 "guide-risk-management-in-forex.html": ("Guide", "Risk management: the complete guide"),
 "free-trading-journal-mt5.html": ("Free tool", "Free trading journal for MT5"),
}

# page: (in-text links [(regex, target)], extra cards [targets])
P = {
 "lesson-how-to-start-forex-trading.html": (
   [(r"\bdemo account\b", "guide-forex-demo-account-in-pakistan.html"), (r"\bpip\b", "lesson-bid-ask-spread-pip-point-pipette-gold.html")],
   ["lesson-what-is-forex-trading.html", "guide-forex-demo-account-in-pakistan.html", "lesson-lot-size-pip-value-calculation.html", "lesson-risk-to-reward-ratio-profit-loss-calculation.html"]),
 "lesson-how-to-make-money-in-forex.html": (
   [(r"\bwin rate\b", "guide-risk-reward-ratio.html"), (r"\b(?:risk to reward|risk:reward|reward)\b", "lesson-risk-to-reward-ratio-profit-loss-calculation.html"), (r"\bleverage\b", "guide-what-is-leverage.html")],
   ["lesson-risk-to-reward-ratio-profit-loss-calculation.html", "guide-risk-reward-ratio.html", "guide-drawdown-in-forex.html", "lot-size-calculator.html"]),
 "lesson-forex-scams-signal-groups.html": (
   [(r"\bregulat(?:ed|ion|or)\b", "guide-forex-brokers-in-pakistan.html"), (r"\bbrokers?\b", "lesson-how-forex-brokers-work.html")],
   ["qa-is-forex-a-scam.html", "guide-forex-signals-in-pakistan.html", "lesson-how-forex-brokers-work.html", "guide-forex-brokers-in-pakistan.html"]),
 "lesson-binary-options-vs-forex.html": (
   [(r"\bbrokers?\b", "lesson-how-forex-brokers-work.html"), (r"\bmarket\b", "lesson-how-forex-market-works.html")],
   ["lesson-how-forex-market-works.html", "lesson-how-forex-brokers-work.html", "guide-what-is-leverage.html", "qa-is-forex-a-scam.html"]),
 "lesson-what-is-forex-trading.html": (
   [(r"\bcurrency pairs?\b", "lesson-currency-pairs-explained.html"), (r"\bpips?\b", "lesson-bid-ask-spread-pip-point-pipette-gold.html"), (r"\bleverage\b", "guide-what-is-leverage.html")],
   ["lesson-currency-pairs-explained.html", "lesson-xauusd-gold-buy-sell-forex-hours.html", "lesson-bid-ask-spread-pip-point-pipette-gold.html", "guide-forex-trading-sessions.html"]),
 "lesson-how-forex-market-works.html": (
   [(r"\bcurrency pairs?\b", "lesson-currency-pairs-explained.html"), (r"\bspread\b", "lesson-bid-ask-spread-pip-point-pipette-gold.html"), (r"\bleverage\b", "guide-what-is-leverage.html"), (r"\bGold\b", "lesson-xauusd-gold-buy-sell-forex-hours.html")],
   ["lesson-currency-pairs-explained.html", "lesson-bid-ask-spread-pip-point-pipette-gold.html", "guide-forex-trading-sessions.html", "guide-what-is-leverage.html"]),
 "lesson-how-forex-brokers-work.html": (
   [(r"\bspread\b", "lesson-bid-ask-spread-pip-point-pipette-gold.html"), (r"\bswap\b", "guide-what-is-swap-in-forex.html"), (r"\bscams?\b", "lesson-forex-scams-signal-groups.html"), (r"\bcurrency pairs?\b", "lesson-currency-pairs-explained.html")],
   ["lesson-bid-ask-spread-pip-point-pipette-gold.html", "guide-what-is-swap-in-forex.html", "lesson-forex-scams-signal-groups.html", "guide-forex-brokers-in-pakistan.html"]),
 "lesson-currency-pairs-explained.html": (
   [(r"\bpips?\b", "lesson-bid-ask-spread-pip-point-pipette-gold.html"), (r"\bspread\b", "guide-what-is-spread.html"), (r"\bXAUUSD\b", "lesson-xauusd-gold-buy-sell-forex-hours.html"), (r"\bsessions?\b", "guide-forex-trading-sessions.html"), (r"\bmarket\b", "lesson-how-forex-market-works.html")],
   ["lesson-xauusd-gold-buy-sell-forex-hours.html", "lesson-bid-ask-spread-pip-point-pipette-gold.html", "guide-gold-trading.html", "guide-forex-trading-sessions.html"]),
 "lesson-xauusd-gold-buy-sell-forex-hours.html": (
   [(r"\b(?:market hours|trading hours|sessions?|Pakistan time|London)\b", "guide-forex-trading-sessions.html"), (r"\bpips?\b", "lesson-bid-ask-spread-pip-point-pipette-gold.html"), (r"\blot size\b", "lesson-lot-size-pip-value-calculation.html"), (r"\btola\b", "gold-rate-pakistan.html"), (r"\bGold trading\b", "guide-gold-trading.html")],
   ["guide-gold-trading.html", "guide-forex-trading-sessions.html", "lesson-lot-size-pip-value-calculation.html", "gold-rate-pakistan.html"]),
 "lesson-bid-ask-spread-pip-point-pipette-gold.html": (
   [(r"\bcurrency pairs?\b", "lesson-currency-pairs-explained.html"), (r"\blot size\b", "lesson-lot-size-pip-value-calculation.html"), (r"\bleverage\b", "guide-what-is-leverage.html"), (r"\bstop loss\b", "lesson-risk-to-reward-ratio-profit-loss-calculation.html"), (r"\bGold trading\b", "guide-gold-trading.html")],
   ["lesson-currency-pairs-explained.html", "lot-size-calculator.html", "lesson-risk-to-reward-ratio-profit-loss-calculation.html", "guide-gold-trading.html"]),
 "lesson-lot-size-pip-value-calculation.html": (
   [(r"\bleverage\b", "guide-what-is-leverage.html"), (r"\brisk management\b", "guide-risk-management-in-forex.html"), (r"\b(?:XAUUSD|Gold)\b", "lesson-xauusd-gold-buy-sell-forex-hours.html"), (r"\b(?:risk to reward|reward)\b", "lesson-risk-to-reward-ratio-profit-loss-calculation.html")],
   ["guide-what-is-leverage.html", "guide-risk-management-in-forex.html", "lesson-xauusd-gold-buy-sell-forex-hours.html", "guide-gold-trading.html"]),
 "lesson-risk-to-reward-ratio-profit-loss-calculation.html": (
   [(r"\bwin rate\b", "guide-risk-reward-ratio.html"), (r"\bdrawdown\b", "guide-drawdown-in-forex.html"), (r"\bjournal\b", "free-trading-journal-mt5.html"), (r"\blosing streaks?\b", "lesson-how-to-make-money-in-forex.html")],
   ["guide-risk-reward-ratio.html", "guide-drawdown-in-forex.html", "lesson-how-to-make-money-in-forex.html", "free-trading-journal-mt5.html"]),
}

def link_text(seg, rx, target):
    """Link the first match of rx in plain text (outside tags and existing links)."""
    out, pos, depth = [], 0, 0
    for m in re.finditer(r"<[^>]+>", seg):
        txt = seg[pos:m.start()]
        if depth == 0 and txt:
            mm = re.search(rx, txt, re.I)
            if mm:
                new = txt[:mm.start()] + f'<a href="{target}" data-smcx="1">{mm.group(0)}</a>' + txt[mm.end():]
                return seg[:pos] + new + seg[m.start():], True
        tag = m.group(0).lower()
        if tag.startswith("<a ") or tag == "<a>": depth += 1
        elif tag.startswith("</a"): depth = max(0, depth - 1)
        pos = m.end()
    txt = seg[pos:]
    if depth == 0 and txt:
        mm = re.search(rx, txt, re.I)
        if mm:
            return seg[:pos] + txt[:mm.start()] + f'<a href="{target}" data-smcx="1">{mm.group(0)}</a>' + txt[mm.end():], True
    return seg, False

def card(t):
    lab, title = T[t]
    return f'<a href="{t}"><small>{lab}</small><span>{title}</span></a>'

def process(f, inline, cards):
    h = open(f, encoding="utf-8").read(); o = h
    a = h.find("<h2>Lesson notes</h2>"); b = h.find("<h2>Khulasa", a)
    added = []
    if a > 0 and b > a:
        notes = h[a:b]
        for rx, tgt in inline:
            if tgt == f or f'href="{tgt}"' in notes or not os.path.exists(tgt):
                continue
            # only inside paragraphs and list items
            for pm in re.finditer(r"<(p|li|td)(?:\s[^>]*)?>(.*?)</\1>", notes, re.S):
                seg, ok = link_text(pm.group(2), rx, tgt)
                if ok:
                    notes = notes[:pm.start(2)] + seg + notes[pm.end(2):]
                    added.append(tgt); break
        h = h[:a] + notes + h[b:]
    # cards block
    h = re.sub(r"\n?\s*<!--RELX-->.*?<!--/RELX-->", "", h, flags=re.S)
    rel = h.find("<h2>Related lessons</h2>")
    have = set(re.findall(r'href="([^"#]+)"', h[rel:rel + 2500])) if rel > 0 else set()
    cs = [c for c in cards if c != f and os.path.exists(c) and c not in have]
    blk = ('<!--RELX--><h3 class="relx-h" style="margin:18px 0 8px;font-size:17px">More on this topic</h3>'
           '<div class="rel">' + "".join(card(c) for c in cs) + '</div><!--/RELX-->')
    if rel > 0 and cs:
        end = h.find("</div>", h.find('<div class="rel">', h.find("<h2>Related lessons</h2>"))) + 6
        h = h[:end] + "\n    " + blk + h[end:]
    if h != o:
        open(f, "w", encoding="utf-8").write(h)
    return added, cs

if __name__ == "__main__":
    for f, (inl, cards) in P.items():
        if os.path.exists(f):
            added, cs = process(f, inl, cards)
            print(f, "| in-text:", len(added), added, "| cards:", len(cs))
