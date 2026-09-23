#!/usr/bin/env python3
"""Emit dist/index.html — the living style guide, rendered from the same tokens
the components use. Run via build/make.py."""

from __future__ import annotations
import html, os
from color import GRADES, contrast, PINNED, BRAND_ANCHORS, HUES, ROLES, ACTIVE_BRAND
import tokens as T
import build as B

E = html.escape

ICONS = {
    "check": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M6.2 11.5 3 8.3l1-1 2.2 2.2L12 3.7l1 1z"/></svg>',
    "chevron": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 11 3.5 6.5 4.6 5.4 8 8.8l3.4-3.4 1.1 1.1z"/></svg>',
    "left": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M10 13 5 8l5-5 1.1 1.1L7.2 8l3.9 3.9z"/></svg>',
    "right": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M6 3l5 5-5 5-1.1-1.1L8.8 8 4.9 4.1z"/></svg>',
    "calendar": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M13 2h-1V0h-1v2H5V0H4v2H3a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1zm0 12H3V6h10zm0-9H3V3h10z"/></svg>',
    "error": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M10 1a9 9 0 1 0 0 18 9 9 0 0 0 0-18zm-.75 4h1.5v7h-1.5zm.75 11a1.1 1.1 0 1 1 0-2.2 1.1 1.1 0 0 1 0 2.2z"/></svg>',
    "warning": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M10 1 0 19h20zm-.75 6h1.5v6h-1.5zm.75 9.4a1.05 1.05 0 1 1 0-2.1 1.05 1.05 0 0 1 0 2.1z"/></svg>',
    "success": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M10 1a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM8.6 14 4.8 10.2l1.1-1.1 2.7 2.7 5.5-5.5 1.1 1.1z"/></svg>',
    "info": '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M10 1a9 9 0 1 0 0 18 9 9 0 0 0 0-18zm.75 14h-1.5V8h1.5zM10 6.2A1.1 1.1 0 1 1 10 4a1.1 1.1 0 0 1 0 2.2z"/></svg>',
    "close": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="m12 4.7-.7-.7L8 7.3 4.7 4l-.7.7L7.3 8 4 11.3l.7.7L8 8.7l3.3 3.3.7-.7L8.7 8z"/></svg>',
    "sort": '<svg viewBox="0 0 16 16" fill="currentColor" width="14" height="14"><path d="M8 3.5 11.5 8h-7zM8 12.5 4.5 8h7z" opacity=".45"/></svg>',
    "arrow": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M9 3 8 4l3.3 3.3H2v1.4h9.3L8 12l1 1 5-5z"/></svg>',
}

DELTA_LABEL = {
    "same": ("Adopted", "adopt"),
    "changed": ("Changed", "chg"),
    "added": ("Added", "add"),
    "dropped": ("Dropped", "drop"),
}


def cite(prov, inline=True):
    """Render a Carbon provenance record."""
    label, cls = DELTA_LABEL[prov.get("delta", "same")]
    src = prov.get("src", "")
    why = prov.get("why")
    out = [f'<div class="cite cite--{cls}">']
    out.append(f'<span class="cite__tag">{label}</span>')
    out.append(f'<span class="cite__val"><b>Carbon:</b> {E(prov["value"])}</span>')
    if why:
        out.append(f'<span class="cite__why">{E(why)}</span>')
    if src:
        out.append(f'<a class="cite__src" href="{E(src)}" target="_blank" rel="noopener">{E(src.replace("https://carbondesignsystem.com", "").replace("https://", ""))}</a>')
    out.append("</div>")
    return "".join(out)


def swatch_row(ramp_name, ramp):
    cells = []
    for g in GRADES:
        hexv = ramp[g]
        # 4.5:1, not 3.0 — these labels are body text sitting on the swatch, and an
        # accessibility audit that fails inside the accessibility documentation is a
        # bad look. Grades 10-50 take dark type, 60-100 take white.
        cr = contrast(hexv, "#ffffff")
        fg = "#ffffff" if cr >= 4.5 else "#131416"
        cells.append(
            f'<div class="sw" style="background:{hexv};color:{fg}">'
            f'<span class="sw__g">{g}</span><span class="sw__h">{hexv}</span></div>')
    return (f'<div class="ramp"><div class="ramp__name">{E(ramp_name)}</div>'
            f'<div class="ramp__cells">{"".join(cells)}</div></div>')


def semantic_table():
    groups = {}
    for name, (lt, dk, role, prov) in T.SEMANTIC.items():
        grp = name.split("-")[0]
        groups.setdefault(grp, []).append((name, lt, dk, role, prov))
    out = []
    for grp, rows in groups.items():
        out.append(f'<h4 class="tokgrp">{E(grp)}</h4>')
        out.append('<table class="tok"><thead><tr>'
                   '<th>Token</th><th>Light</th><th>Dark</th><th>Role &amp; provenance</th>'
                   '</tr></thead><tbody>')
        for name, lt, dk, role, prov in rows:
            lv, dv = B.resolve(lt), B.resolve(dk)
            out.append(
                f'<tr><td><code>--st-{E(name)}</code></td>'
                f'<td class="tok__v"><i class="chip" style="background:{lv}"></i>'
                f'<span><code>{E(lt)}</code><br><small>{E(lv)}</small></span></td>'
                f'<td class="tok__v"><i class="chip chip--dk" style="background:{dv}"></i>'
                f'<span><code>{E(dk)}</code><br><small>{E(dv)}</small></span></td>'
                f'<td><div class="role">{E(role)}</div>{cite(prov)}</td></tr>')
        out.append("</tbody></table>")
    return "".join(out)


def type_table():
    out = ['<table class="tok"><thead><tr><th>Token</th><th>Specimen</th>'
           '<th>Metrics</th><th>Provenance</th></tr></thead><tbody>']
    for name, s in T.TYPE_STYLES.items():
        style = (f"font-size:{s['size']}px;line-height:{s['lh']}px;"
                 f"font-weight:{s['weight']};letter-spacing:{s['ls']};"
                 f"font-family:{'var(--st-font-mono)' if name=='code' else 'var(--st-font-sans)'}")
        out.append(
            f'<tr><td><code>--st-type-{E(name)}</code></td>'
            f'<td><div style="{style}">Grid systems for everyone</div></td>'
            f'<td class="nowrap"><small>{s["size"]}px / {s["lh"]}px<br>'
            f'{s["weight"]} · {E(s["ls"])}</small></td>'
            f'<td>{cite(s["carbon"])}</td></tr>')
    out.append("</tbody></table>")
    return "".join(out)


def scale_strip(title, values, unit="px", prov=None, note=None):
    cells = "".join(
        f'<div class="sc"><div class="sc__bar" style="width:{min(v,200)}px"></div>'
        f'<code>{E(str(k))}</code><small>{v}{unit}</small></div>'
        for k, v in values.items())
    body = f'<div class="scales">{cells}</div>'
    if note:
        body += f'<p class="note">{E(note)}</p>'
    if prov:
        body += cite(prov)
    return f'<h3>{E(title)}</h3>{body}'


def component_spec(key, comp):
    rows = []
    for name, ours, carbon_val, delta, why in comp["spec"]:
        label, cls = DELTA_LABEL[delta]
        rows.append(
            f'<tr><td class="nowrap"><b>{E(name)}</b></td>'
            f'<td>{E(ours)}</td>'
            f'<td><div class="cite cite--{cls}" style="margin:0">'
            f'<span class="cite__tag">{label}</span>'
            f'<span class="cite__val">{E(carbon_val)}</span>'
            + (f'<span class="cite__why">{E(why)}</span>' if why else "")
            + "</div></td></tr>")
    return (f'<table class="tok spec"><thead><tr><th style="width:9rem">Property</th>'
            f'<th style="width:26%">Strata</th><th>Against official Carbon</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>'
            f'<p class="srcline">Source: <a href="{E(comp["carbon_src"])}" target="_blank" '
            f'rel="noopener">{E(comp["carbon_src"])}</a></p>')


def audit_table():
    rows = B.audit()
    out = ['<table class="tok audit"><thead><tr><th>Pair</th><th>Theme</th>'
           '<th>Foreground</th><th>Background</th><th>Ratio</th><th>Target</th>'
           '<th><span class="vh">Result</span></th></tr></thead><tbody>']
    for r in rows:
        if r["sev"] == "advisory":
            badge = ('<span class="pass">meets</span>' if r["ok"]
                     else '<span class="adv">advisory</span>')
        else:
            badge = ('<span class="pass">pass</span>' if r["ok"]
                     else '<span class="fail">FAIL</span>')
        out.append(
            f'<tr><td>{E(r["label"])}</td><td>{r["theme"]}</td>'
            f'<td><i class="chip" style="background:{r["fg_hex"]}"></i><code>{E(r["fg"])}</code>'
            f'<br><small>{r["fg_hex"]}</small></td>'
            f'<td><i class="chip" style="background:{r["bg_hex"]}"></i><code>{E(r["bg"])}</code>'
            f'<br><small>{r["bg_hex"]}</small></td>'
            f'<td class="num"><b>{r["ratio"]}</b></td><td class="num">{r["need"]}</td>'
            f'<td>{badge}</td></tr>')
    out.append("</tbody></table>")
    aa = [r for r in rows if r["sev"] == "AA"]
    adv = [r for r in rows if r["sev"] == "advisory"]
    n_fail = sum(1 for r in aa if not r["ok"])
    return (f'<p class="note"><b>{len(rows)} programmatic checks — {len(aa)} enforced, '
            f'{n_fail} failing.</b> Recomputed on every build from the emitted token values; '
            'an AA failure aborts the build rather than shipping. The remaining '
            f'{len(adv)} are marked <em>advisory</em>: disabled states, which WCAG explicitly '
            'exempts, and decorative boundaries not required to identify a component. They are '
            'reported so the number is visible, not enforced — a table row divider that hit '
            '3:1 would be a worse table.</p>'
            '<p class="note"><b>Alpha tokens are genuinely composited.</b> A token like '
            '<code>--st-background-active</code> is a wash at 40% opacity; checking its base '
            'colour instead of the composite over-reports contrast for every alpha token in the '
            'system. Adding the real source-over composite to this build immediately surfaced '
            'three failures that had been invisible — a dark-theme placeholder at 3.48:1, a '
            'dark secondary button label at 3.04:1, and a dark toggle handle at 2.16:1. All '
            'three are now fixed, and all three exist in Carbon at the corresponding '
            'tokens.</p>'
            + "".join(out))


def divergence_ledger():
    items = []

    def push(area, token, prov):
        if prov.get("delta", "same") == "same" and not prov.get("why"):
            return
        if prov.get("delta") == "same":
            return
        items.append((area, token, prov))

    for name, (lt, dk, role, prov) in T.SEMANTIC.items():
        push("Colour", f"--st-{name}", prov)
    for name, s in T.TYPE_STYLES.items():
        push("Type", f"--st-type-{name}", s["carbon"])
    for k, v in T.TYPEFACE.items():
        push("Type", f"--st-font-{k}", v["carbon"])
    for label, prov in (("Spacing", T.SPACING_CARBON), ("Sizing", T.SIZES_CARBON),
                        ("Radius", T.RADIUS_CARBON), ("Elevation", T.ELEVATION_CARBON),
                        ("Grid", T.BREAKPOINTS_CARBON)):
        push("Foundation", label, prov)
    for key, comp in T.COMPONENTS.items():
        for name, ours, carbon_val, delta, why in comp["spec"]:
            if delta != "same":
                push("Component", f"{key} · {name}",
                     dict(delta=delta, value=carbon_val, why=why or "", src=comp["carbon_src"]))

    out = ['<table class="tok"><thead><tr><th>Area</th><th>Token / property</th>'
           '<th>Change</th><th>Carbon says</th><th>Why we diverge</th></tr></thead><tbody>']
    for area, token, prov in items:
        label, cls = DELTA_LABEL[prov["delta"]]
        out.append(
            f'<tr><td class="nowrap"><small>{E(area)}</small></td>'
            f'<td><code>{E(token)}</code></td>'
            f'<td><span class="cite__tag cite__tag--{cls}">{label}</span></td>'
            f'<td><small>{E(prov["value"])}</small></td>'
            f'<td><small>{E(prov.get("why",""))}</small></td></tr>')
    out.append("</tbody></table>")
    n_same = (len(T.SEMANTIC) + len(T.TYPE_STYLES) + len(T.MOTION) + 5 +
              sum(len(c["spec"]) for c in T.COMPONENTS.values())) - len(items)
    return (f'<p class="note">Roughly <b>{n_same} decisions adopted from Carbon unchanged</b>, '
            f'<b>{len(items)} deliberately diverged</b>. Every row below is a decision someone '
            f'can argue with — which is the point of writing them down.</p>' + "".join(out))


def icons_and_ratios():
    rows = "".join(
        f'<tr><td class="nowrap"><b>{E(k.title())}</b></td><td>{E(v)}</td></tr>'
        for k, v in T.ICON_RULES.items())
    sizes = " · ".join(f"<code>{k}</code> {v}px" for k, v in T.ICON_SIZES.items())
    ratios = " ".join(f'<span class="pill">{r.replace("x", ":")}</span>' for r in T.ASPECT_RATIOS)
    return (f'<h3>Icons</h3>'
            f'<table class="tok"><tbody>{rows}</tbody></table>'
            f'<p class="note">Artboard sizes: {sizes}. No asset set ships with this base — the '
            f'guide uses eleven placeholder glyphs.</p>'
            + cite(T.ICONS_CARBON) +
            f'<h3>Aspect ratios</h3><div class="pillrow">{ratios}</div>'
            + cite(T.ASPECT_CARBON))


def brand_table():
    if not BRAND_ANCHORS:
        role_rows = "".join(
            f'<tr><td><code>{E(k)}</code></td><td><code>{E(v)}</code></td></tr>'
            for k, v in ROLES.items())
        hue_rows = "".join(
            f'<tr><td><code>{E(k)}</code></td><td class="num">{v[0]}&deg;</td>'
            f'<td class="num">{v[1]}</td></tr>' for k, v in HUES.items())
        return (
            '<h3>This build is unbranded, on purpose</h3>'
            '<p class="note">No brand is bound. Every value here is structural \u2014 the spacing '
            'scale, the type scale, control sizes, radius, elevation, motion, the state '
            'definitions and the accessibility rules \u2014 rendered with a neutral palette and a '
            'single non-brand accent. That is what makes it the right target for '
            '<b>moderate fidelity</b>: visual finish high enough that a person engages with it '
            'as a real thing, with no design-system commitment smuggled in.</p>'
            '<p class="note"><b>What this build deliberately cannot show you:</b> how it looks '
            'on brand, whether the brand palette passes contrast in context, and any collision '
            'a specific brand creates between roles \u2014 for instance a brand whose primary '
            'and success sit in the same hue family. Those are high-fidelity questions and this '
            'artefact is not evidence about them.</p>'
            '<h3>Role map</h3>'
            '<table class="tok"><thead><tr><th>Role</th><th>Ramp</th></tr></thead><tbody>'
            + role_rows + '</tbody></table>'
            '<h3>The brand config</h3>'
            '<table class="tok"><thead><tr><th>Family</th><th>OKLCH hue</th>'
            '<th>Chroma multiplier</th></tr></thead><tbody>' + hue_rows + '</tbody></table>')
    rows = []
    for name, hexv, pantone, role in BRAND_ANCHORS:
        a = B.brand_anchor(hexv)
        d = a["deltaRGB"]
        verdict = ("<span class='pass'>exact</span>" if d <= 10 else
                   "<span class='adv'>close</span>" if d <= 25 else
                   "<span class='fail'>not reproduced</span>")
        rows.append(
            f'<tr><td><b>{E(name)}</b><br><small>{E(pantone)}</small></td>'
            f'<td class="tok__v"><i class="chip" style="background:{hexv}"></i><code>{hexv}</code></td>'
            f'<td class="num">{a["contrastVsWhite"]}</td>'
            f'<td class="tok__v"><i class="chip" style="background:{a["hex"]}"></i>'
            f'<code>--st-{a["token"].replace(".", "-")}</code><br><small>{a["hex"]}</small></td>'
            f'<td class="num">{d}</td><td>{verdict}</td><td><small>{E(role)}</small></td></tr>')
    hue_rows = "".join(
        f'<tr><td><code>{E(k)}</code></td><td class="num">{v[0]}&deg;</td>'
        f'<td class="num">{v[1]}</td></tr>' for k, v in HUES.items())
    pinned = "".join(
        f'<tr><td><code>--st-{E(k)}</code></td>'
        f'<td class="tok__v"><i class="chip" style="background:{v}"></i><code>{v}</code></td>'
        f'<td class="num">{contrast(v, "#ffffff")}</td></tr>' for k, v in PINNED.items())
    return (
        '<h3>Where each official Deloitte value lands</h3>'
        '<p class="note">A computed palette cannot promise to reproduce a hand-authored Pantone '
        'set. The honest thing is to state the mapping and the error rather than claim a match. '
        '&Delta;RGB is Euclidean distance in sRGB — under 10 is indistinguishable side by side, '
        'under 25 is a rounding difference, above that is a different colour.</p>'
        '<table class="tok"><thead><tr><th>Deloitte value</th><th>Official</th>'
        '<th>vs&nbsp;white</th><th>Resolves to</th><th>&Delta;RGB</th>'
        '<th><span class="vh">Match quality</span></th><th>Role here</th>'
        '</tr></thead><tbody>' + "".join(rows) + '</tbody></table>'
        '<h3>Pinned — outside the ramps</h3>'
        '<table class="tok"><thead><tr><th>Token</th><th>Value</th><th>vs white</th></tr></thead>'
        '<tbody>' + pinned + '</tbody></table>'
        '<h3>The brand config itself</h3>'
        '<p class="note">This is the whole brand. Nine hue angles and nine chroma multipliers in '
        '<code>build/color.py</code>; everything else is derived.</p>'
        '<table class="tok"><thead><tr><th>Family</th><th>OKLCH hue</th><th>Chroma multiplier</th>'
        '</tr></thead><tbody>' + hue_rows + '</tbody></table>')
