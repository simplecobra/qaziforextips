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
.dec-s{text-transform:lowercase;color:var(--ink);opacity:.75}
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


# ---------------- year rows that open to show their months (same table) ----------------
YR_CSS = """<style>
.tbl.hx-s{max-height:600px}
.tbl.hx-s>table>thead th{position:sticky;top:0;z-index:2;background:var(--surface)}
.tbl.hx-s .yr-m thead th{position:static}
tr.yr{cursor:pointer}
tr.yr:hover>th,tr.yr:hover>td{background:rgba(201,151,31,.08)}
tr.yr.open>th,tr.yr.open>td{background:rgba(201,151,31,.14)}
.yr-b{all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:8px;font:inherit;color:inherit;letter-spacing:inherit}
.yr-b:focus-visible{outline:2px solid var(--gold);outline-offset:3px;border-radius:4px}
.yr-c{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:50%;border:1px solid currentColor;font-size:10px;transition:transform .2s}
tr.yr.open .yr-c{transform:rotate(180deg)}
tr.yr-sub>td{padding:4px 10px 14px !important;background:var(--bg)}
.yr-m{width:100%;margin:6px 0 0;font-size:14.5px}
.yr-m th,.yr-m td{padding:7px 10px !important}
.yr-hint{font-size:14px;color:var(--muted);margin:-4px 0 8px}
</style>"""

YR_JS = """<script>(function(){document.querySelectorAll('tr.yr').forEach(function(tr){var s=tr.nextElementSibling,b=tr.querySelector('.yr-b');
tr.addEventListener('click',function(){var o=s.hidden;s.hidden=!o;tr.classList.toggle('open',o);b.setAttribute('aria-expanded',o?'true':'false')})})})();</script>"""


def year_table(head, rows, sub_head):
    """head: list of column names (first is the year column).
    rows: list of (year_key, [td html strings], [sub row html strings]) in display order.
    sub_head: column names for the monthly table that opens under a year."""
    n = len(head)
    th = "".join(f"<th>{h}</th>" for h in head)
    sh = "".join(f"<th>{h}</th>" for h in sub_head)
    body = ""
    for k, cells, subs in rows:
        body += (f'<tr class="yr"><th scope="row"><button type="button" class="yr-b" aria-expanded="false" aria-controls="yr-{k}">{k}'
                 f'<span class="yr-c" aria-hidden="true">▼</span></button></th>{"".join(cells)}</tr>'
                 f'<tr class="yr-sub" id="yr-{k}" hidden><td colspan="{n}"><table class="yr-m"><thead><tr>{sh}</tr></thead>'
                 f'<tbody>{"".join(subs)}</tbody></table></td></tr>')
    return f'<div class="tbl hx-s"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'
