#!/usr/bin/env python3
"""Site theme: light "Brand Maroon & Gold" (Sample E, chosen 27 Nov 2026) is the default; dark is optional via the
sun/moon button and remembered per visitor (localStorage "qft-theme").

Run from the repo root:  python3 .github/scripts/apply-theme.py
Idempotent: it rewrites the theme init script, the theme-color meta, the toggle's light colour and the
<style id="qft-theme-e"> block in every page, so pages made by any builder get the theme on the next run
(the theme.yml workflow runs it on every push).
"""
import glob, re, sys

OLD_INIT = ('<script>try{var t=localStorage.getItem("qft-theme");if(t!=="light"&&t!=="dark")t=window.matchMedia&&'
            'matchMedia("(prefers-color-scheme: light)").matches?"light":"";if(t)document.documentElement.setAttribute("data-theme",t);}catch(e){}</script>')
NEW_INIT = ('<script>try{var t=localStorage.getItem("qft-theme");if(t!=="dark")t="light";'
            'document.documentElement.setAttribute("data-theme",t);}catch(e){document.documentElement.setAttribute("data-theme","light");}</script>')
MAROON = "#7a1426"

CSS = """<style id="qft-theme-e">
/* Default light theme "Brand Maroon & Gold": white page, logo maroon header/footer, gold buttons */
:root[data-theme="light"]{--bg:#ffffff;--bg2:#fbf6f0;--surface:#ffffff;--line:#eadfd3;--ink:#1a1214;--muted:#5e5457;--gold:#d4a017;--gold-t:#8a6100;--gold-ink:#1a1214;--wine:#8e1b2e}
:root[data-theme="light"] .ann{background:#fbf3df}
:root[data-theme="light"] .top{background:#7a1426;color:#fff;border-bottom:3px solid #d4a017;--ink:#fff;--muted:rgba(255,255,255,.86);--line:rgba(255,255,255,.22);--bg2:#6a1121;backdrop-filter:none;-webkit-backdrop-filter:none}
:root[data-theme="light"] .top .nav a:hover{color:#ffd76a}
:root[data-theme="light"] .top .theme-btn,:root[data-theme="light"] .top .menu,:root[data-theme="light"] .top button{color:#fff;border-color:rgba(255,255,255,.3)}
:root[data-theme="light"] .top .btn.gold{background:#d4a017;border-color:#d4a017;color:#1a1214}
:root[data-theme="light"] h1 em,:root[data-theme="light"] h1 span{color:#8e1b2e}
:root[data-theme="light"] .panel,:root[data-theme="light"] .shot{box-shadow:0 20px 50px rgba(122,20,38,.12);border-color:#eadfd3}
:root[data-theme="light"] .btn.gold{background:#d4a017;border-color:#d4a017;color:#1a1214}
:root[data-theme="light"] .btn:not(.gold){border-color:#7a1426;color:#7a1426}
:root[data-theme="light"] .step,:root[data-theme="light"] .tool,:root[data-theme="light"] .rl-card,:root[data-theme="light"] .stat,:root[data-theme="light"] .path{box-shadow:0 6px 20px rgba(122,20,38,.06)}
:root[data-theme="light"] .cta-band{background:linear-gradient(135deg,#7a1426,#4a0c17);color:#fff;--ink:#fff;--muted:#e9c9cf;--line:#5c1020}
:root[data-theme="light"] .cta-band .btn:not(.gold){border-color:#fff;color:#fff}
:root[data-theme="light"] footer{background:#2a0a10;color:#d9b9be;--ink:#fff;--muted:#d9b9be;--line:#4a1a22}
:root[data-theme="light"] footer a{color:#fff}
</style>"""

# simulator.html uses another variable scheme (--ink = page background, --text = text, --panel = cards)
CSS_ALT = """
:root[data-theme="light"]{--ink:#ffffff;--panel:#ffffff;--text:#1a1214}
:root[data-theme="light"] .top{--text:#fff;--ink:#7a1426}
:root[data-theme="light"] .top .brand,:root[data-theme="light"] .top .brand *{color:#fff}
:root[data-theme="light"] footer{--text:#fff;--ink:#2a0a10}
"""

def apply(html):
    h = html
    css = CSS
    if 'body{background:var(--ink)' in h:
        css = CSS.replace('</style>', CSS_ALT.strip() + '\n</style>')
    h = h.replace(OLD_INIT, NEW_INIT)
    h = re.sub(r'(<meta name="theme-color" content=")#0d1220(">)', r'\g<1>' + MAROON + r'\2', h, count=1)
    h = h.replace('light ? "#f5f3ee" : "#0d1220"', 'light ? "' + MAROON + '" : "#0d1220"')
    if 'id="qft-theme-e"' in h:
        h = re.sub(r'<style id="qft-theme-e">.*?</style>', lambda m: css, h, count=1, flags=re.S)
    elif NEW_INIT in h and '</head>' in h:
        h = h.replace('</head>', css + '\n</head>', 1)
    return h

if __name__ == "__main__":
    changed = 0
    for f in sorted(glob.glob("*.html")):
        s = open(f, encoding="utf-8").read()
        n = apply(s)
        if n != s:
            open(f, "w", encoding="utf-8").write(n); changed += 1
    print("theme applied, pages changed:", changed)
