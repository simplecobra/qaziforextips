# -*- coding: utf-8 -*-
"""Shared "history explorer" block for the rate-history pages (gold, USD/PKR).
One table visible at a time with a year/month picker and older/newer buttons, instead of dozens of
<details> rows. Every panel stays in the HTML (hidden attribute), so Google still reads all the data;
without JavaScript the first (newest) panel shows."""

CSS = """<style>
.hx{border:1px solid var(--line);border-radius:14px;background:var(--surface);padding:14px 14px 4px;margin:16px 0}
.hx-bar{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.hx-bar select{flex:1 1 180px;min-width:0;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink);font:inherit;font-size:16px;font-weight:600}
.hx-b{width:44px;height:44px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink);font-size:22px;line-height:1;cursor:pointer}
.hx-b:disabled{opacity:.35;cursor:default}
.hx-b:not(:disabled):hover{border-color:var(--gold)}
.hx-n{font-size:13.5px;color:var(--muted);white-space:nowrap}
.hx-p h3{font-size:18px;margin:14px 0 4px}
.hx-p .tbl{margin:8px 0 10px}
.tbl.hx-s{max-height:470px;overflow:auto;border:1px solid var(--line);border-radius:12px}
.tbl.hx-s table{margin:0}
.tbl.hx-s thead th{position:sticky;top:0;z-index:1;background:var(--surface)}
.hx td,.hx th,.hx-s td,.hx-s th{white-space:nowrap}
@media(max-width:600px){.hx td,.hx th,.hx-s td,.hx-s th{font-size:14px;padding:8px 10px}.hx{padding:10px 8px 2px}}
.hx-chips{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0 0}
.hx-chips button{border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:999px;padding:5px 11px;font:inherit;font-size:13.5px;cursor:pointer}
.hx-chips button:hover{border-color:var(--gold)}
</style>"""

JS = """<script>(function(){document.querySelectorAll('.hx').forEach(function(h){var s=h.querySelector('select'),P=h.querySelectorAll('.hx-p'),n=h.querySelector('.hx-n'),B=h.querySelectorAll('.hx-b');
function go(i){if(i<0||i>=P.length)return;s.selectedIndex=i;for(var j=0;j<P.length;j++)P[j].hidden=j!==i;if(n)n.textContent=(i+1)+' / '+P.length;B[0].disabled=i>=P.length-1;B[1].disabled=i<=0}
s.addEventListener('change',function(){go(s.selectedIndex)});B[0].addEventListener('click',function(){go(s.selectedIndex+1)});B[1].addEventListener('click',function(){go(s.selectedIndex-1)});
h.querySelectorAll('.hx-chips button').forEach(function(c){c.addEventListener('click',function(){for(var j=0;j<s.options.length;j++)if(s.options[j].value===c.dataset.k){go(j);break}})});go(0)})})();</script>"""


def explorer(label, panels, chips=None, groups=False):
    """panels: list of (key, option_text, heading, table_html), newest first.
    groups=True puts options into <optgroup> by the first 4 characters of the key (year)."""
    opts, cur = "", None
    for k, t, _, _ in panels:
        if groups and k[:4] != cur:
            opts += ("</optgroup>" if cur else "") + f'<optgroup label="{k[:4]}">'
            cur = k[:4]
        opts += f'<option value="{k}">{t}</option>'
    if groups and cur:
        opts += "</optgroup>"
    body = "".join(f'<div class="hx-p" data-k="{k}"{" hidden" if i else ""}><h3>{h}</h3>{tb}</div>'
                   for i, (k, _, h, tb) in enumerate(panels))
    ch = ""
    if chips:
        ch = '<div class="hx-chips">' + "".join(f'<button type="button" data-k="{k}">{t}</button>' for k, t in chips) + "</div>"
    return (f'<div class="hx"><div class="hx-bar"><button type="button" class="hx-b" aria-label="Older">‹</button>'
            f'<select aria-label="{label}">{opts}</select><button type="button" class="hx-b" aria-label="Newer">›</button>'
            f'<span class="hx-n">1 / {len(panels)}</span></div>{ch}{body}</div>')
