"""
Strata token source of truth.

Every entry carries a `carbon` provenance record:
    src   -- the official Carbon URL the value was taken from
    value -- what Carbon actually specifies
    delta -- same | changed | added | dropped
    why   -- required whenever delta != "same"

Nothing in dist/ is hand-written. tokens.json, strata.css and the style guide are
all emitted from this file, so the documentation cannot drift from the CSS.
(Carbon's own docs *have* drifted, in at least four places verified against the
repos at HEAD: /elements/color/tokens/ prints $button-primary-hover as #0353e9
while the shipped SCSS resolves to #0050e6 -- and @carbon/themes disagrees with
ITSELF at the same version, its JS build exporting #0353e9. It prints
$text-placeholder as Gray 40 while the code ships rgba(22,22,22,0.4). The date
picker style page publishes a raw `0 2px 6px 0 rgba(0,0,0,0.2)` while the code
ships `0 2px 6px $shadow` at 30% alpha. The dropdown publishes 48px right padding
while _dropdown.scss ships 42px. Multiple artefacts, multiple answers. This build
has one.)
"""

from color import ROLES, ACTIVE_BRAND

# Role indirection. Semantic tokens reference a ROLE, and the active brand decides
# which ramp fills it. This is what makes a brand swap a config change rather than a
# find-and-replace through every semantic token -- and it is what lets the unbranded
# `scaffold` build render moderate fidelity without smuggling in a brand commitment.
P = ROLES["primary"]
S = ROLES["success"]
I = ROLES["info"]
W = ROLES["warning"]
D = ROLES["danger"]
V = ROLES["visited"]
# Focus is its own role. It was primary.60, which meant that on any brand where
# primary and success share a hue the focus ring and the success colour became
# the same expression -- see check_role_separation() in color.py.
F = ROLES["focus"]

C = "https://carbondesignsystem.com"

# ---------------------------------------------------------------------------
# TYPE
# ---------------------------------------------------------------------------

TYPEFACE = {
    # [encode 2026-08-20, ledger E-03] REVERSAL of the Inter divergence, eyes open.
    # Plex is SIL OFL-1.1 with 'Plex' as a Reserved Font Name: it may be bundled
    # and shipped commercially; the font FILES (if ever bundled) must carry their
    # own LICENSE.txt and can never be relicensed Apache-2.0; a modified cut must
    # be renamed. Those constraints survive and are accepted. The trade-dress
    # argument that motivated Inter assumed Plex + IBM Blue + IBM densities
    # TOGETHER; Strata's palette is its own OKLCH ladder (chroma ceiling 0.166,
    # not IBM Blue) and its densities diverged, so the face alone does not
    # assemble the IBM look. Inter stays in the stack as first fallback. No font
    # files ship in this repo yet — the stack is a reference until they do.
    "sans": {
        "value": "'IBM Plex Sans', 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif",
        "carbon": {
            "src": f"{C}/elements/typography/overview/",
            "value": "'IBM Plex Sans', system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
            "delta": "same",
            "why": (
                "Re-adopted 20 Aug 2026 (was 'changed' to Inter-first; see the ledger). "
                "OFL-1.1 obligations recorded above and in LICENCE-AND-ATTRIBUTION.md §2."
            ),
        },
    },
    "mono": {
        "value": "'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace",
        "carbon": {
            "src": f"{C}/elements/typography/overview/",
            "value": "'IBM Plex Mono', 'Menlo', 'DejaVu Sans Mono', Courier, monospace",
            "delta": "same",
            "why": "Same reasoning and same obligations as the sans face.",
        },
    },
}

# Carbon's scale formula, retained for provenance:  Yn = Yn-1 + (floor((n-2)/4) + 1) * 2
TYPE_SCALE = [12, 14, 16, 18, 20, 24, 28, 32, 36, 42, 48, 54, 60]

# [encode 2026-08-20, ledger E-02] The T1 ramp replaces the twelve-token scale.
# Four sizes — 12 / 13.5 / 15 / 28 — weight-led: if something needs emphasis,
# change its weight or colour, never its size. Caps labels are 12px + tracking,
# never a smaller size. Eight tokens, eight classes; the one-class-per-token
# invariant holds with a smaller N. Chosen by eye against four alternatives
# (including Carbon's own productive ramp, T2) on identical pages —
# type-system-study, 19–20 Aug 2026. The retired styles (label-md,
# body-compact, heading-compact, heading-xs, heading-lg) are gone, not aliased:
# an alias is a second name for the same decision, and second names are how ten
# font sizes happen. 13.5px is deliberately off Carbon's scale — it is the T1
# body size, sitting between label-01 and body-compact-01.
TYPE_STYLES_RETIRED_20260820 = ["label-sm", "label-md", "body-compact",
                                "heading-compact", "heading-xs", "heading-lg"]

TYPE_STYLES = {
    "label":      dict(size=12, lh=16, weight=500, ls="0.4px",
                       carbon=dict(src=f"{C}/elements/typography/type-sets/",
                                   value="label-01 — 12px / 16px / 400 / 0.32px",
                                   delta="changed",
                                   why=("The caps micro-label of the T1 ramp: weight 500 and "
                                        "wider tracking because it renders uppercase (the "
                                        "class sets text-transform). One label style, not "
                                        "two — label-md retired with the ramp."))),
    "helper":     dict(size=12, lh=16, weight=400, ls="0.32px",
                       carbon=dict(src=f"{C}/elements/typography/type-sets/",
                                   value="helper-text-01 — 12px / 16px / 400 / 0.32px",
                                   delta="same")),
    "body-sm":    dict(size=12, lh=18, weight=400, ls="0.1px",
                       carbon=dict(src=f"{C}/elements/typography/type-sets/",
                                   value="label-01 — 12px / 16px / 400 / 0.32px (nearest)",
                                   delta="changed",
                                   why=("T1's small running text: 12px with a taller line and "
                                        "tighter tracking than a label, because it sets "
                                        "sentences, not tags."))),
    "body-md":    dict(size=13.5, lh=20, weight=400, ls="0px",
                       carbon=dict(src=f"{C}/elements/typography/type-sets/",
                                   value="body-compact-01 14px / body-01 14px (nearest)",
                                   delta="changed",
                                   why=("THE body size. 13.5px is the T1 working-density body "
                                        "— denser than the previous 16px default (that "
                                        "divergence is hereby reversed), calmer than "
                                        "Carbon's 14 at these weights. Off-scale knowingly; "
                                        "the ramp is hand-tuned, not formula-derived."))),
    "heading-sm": dict(size=13.5, lh=20, weight=600, ls="0px",
                       carbon=dict(src=f"{C}/elements/typography/type-sets/",
                                   value="heading-compact-01 — 14px / 18px / 600 / 0.16px (nearest)",
                                   delta="changed",
                                   why=("Body-size heading: inline heads, card titles, table "
                                        "headers. Same size as body-md — weight alone carries "
                                        "the emphasis, which is the T1 rule."))),
    "heading-md": dict(size=15, lh=22, weight=600, ls="-0.1px",
                       carbon=dict(src=f"{C}/elements/typography/type-sets/",
                                   value="heading-compact-02 — 16px / 22px / 600 / 0px (nearest)",
                                   delta="changed",
                                   why=("The section head. One size above body, weight-led, "
                                        "a whisper of negative tracking."))),
    "display":    dict(size=28, lh=32, weight=600, ls="-0.5px",
                       carbon=dict(src=f"{C}/elements/typography/type-sets/",
                                   value="heading-04 — 28px / 36px / 400 / 0px",
                                   delta="changed",
                                   why=("The one display moment: page titles and stat "
                                        "figures. 600 not 300/400 — T1 was chosen over "
                                        "Carbon's light-display treatment by eye, on "
                                        "identical pages. Negative tracking per the "
                                        "large-text rule the old heading-lg established."))),
    "code":       dict(size=12, lh=16, weight=400, ls="0.32px",
                       carbon=dict(src=f"{C}/elements/typography/type-sets/",
                                   value="code-01 — 12px / 16px / 400 / 0.32px",
                                   delta="same",
                                   why=("Every identifier renders mono — the house signature. "
                                        "Drops from code-02 metrics to code-01 with the ramp."))),
}

# ---------------------------------------------------------------------------
# SPACING — Carbon's 8px mini-unit scale, unchanged
# ---------------------------------------------------------------------------

SPACING = {
    "01": 2, "02": 4, "03": 8, "04": 12, "05": 16, "06": 24, "07": 32,
    "08": 40, "09": 48, "10": 64, "11": 80, "12": 96, "13": 160,
}
SPACING_CARBON = dict(
    src=f"{C}/elements/spacing/overview/",
    value="spacing-01..13 = 2, 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96, 160px. Carbon's own "
          "wording: the scale uses 'multiples of two, four, and eight'. Note the 8px mini unit "
          "is a 2x GRID concept, not the basis of the spacing scale — 2, 4 and 12 are not "
          "multiples of 8. The two are complementary, not the same rule.",
    delta="same",
    why=("Adopted wholesale, all 13 values. This is the single strongest part of Carbon: "
         "a 13-step scale on multiples of 2/4/8 covers everything from icon insets to page "
         "gutters without anyone reaching for an arbitrary number."),
)

# ---------------------------------------------------------------------------
# CONTROL SIZES
# ---------------------------------------------------------------------------

SIZES = {
    "xs": 24, "sm": 32, "md": 40, "lg": 48, "xl": 64,
}
SIZES_CARBON = dict(
    src=f"{C}/components/button/usage/",
    value="Carbon control heights: xs 24, sm 32, md 40, lg 48, xl 64, 2xl 80. "
          "Default for product UI is large-productive (48) for buttons, medium (40) for fields.",
    delta="changed",
    why=("The scale is kept 1:1 so anything ported from Carbon maps without arithmetic. "
         "What changes is the DEFAULT: Strata defaults every interactive control to lg "
         "(48px), fields included. Carbon's own accessibility guidance requires "
         "'all touch targets for interactive icons need to be 44px or larger' "
         "(/elements/icons/usage/) yet its default field is 40px -- an internal "
         "inconsistency. Defaulting to 48 clears the 44px floor for every control, "
         "not just icons. 32px remains available for data-dense surfaces. "
         "xs (24) is carried because Carbon carries it and the resolution map cites "
         "it for table row height -- but it is a ROW height only. It is below the "
         "44px touch floor and must never size an interactive control."),
)

# ---------------------------------------------------------------------------
# RADIUS — the clearest expression of "lighter, less industrial"
# ---------------------------------------------------------------------------

# [encode 2026-08-20, ledger E-01] xl re-cut 12 -> 10: the unified 6-10 radius
# stance of the locked language — chips 6, controls 8, surfaces 10.
RADIUS = {
    "none": 0, "xs": 2, "sm": 4, "md": 6, "lg": 8, "xl": 10, "full": 9999,
}
RADIUS_CARBON = dict(
    src=f"{C}/components/popover/style/",
    value=("Carbon has no radius scale, no radius token in @carbon/layout or @carbon/themes, "
           "and no published square-corner rule or rationale anywhere on the site. Four "
           "component pages do publish a radius — Tag 16px, Content switcher 4px, Code "
           "snippet 2px, Popover 2px — while 23 component SCSS files set border-radius "
           "in shipped code (button, checkbox, toggle, tile, tooltip, slider, list-box...)."),
    delta="added",
    why=("Worth being precise, because 'Carbon is square-cornered' is folklore. It is not "
         "a documented rule. What Carbon actually has is radius applied ad hoc in 23 files "
         "with only four values ever documented — which is the definition of a scale that "
         "should exist and doesn't. Strata makes it explicit and moves the control default "
         "from 0 to 6px. Because it is a token, reverting the whole system to square is a "
         "one-line change."),
)

# ---------------------------------------------------------------------------
# ELEVATION
# ---------------------------------------------------------------------------

ELEVATION = {
    "00": "none",
    # [encode 2026-08-20, ledger E-06] 01 re-tuned to the whisper shadow that
    # hairline surfaces (cards, fields, stats) carry at rest. 02/03 unchanged.
    "01": "0 1px 2px rgba(16,18,20,0.04)",
    "02": "0 2px 6px rgba(16,18,20,0.08), 0 4px 12px rgba(16,18,20,0.08)",
    "03": "0 8px 16px rgba(16,18,20,0.10), 0 16px 32px rgba(16,18,20,0.12)",
}
ELEVATION_CARBON = dict(
    src=f"{C}/components/tile/usage/",
    value=("One shadow mixin: `box-shadow: 0 2px 6px $shadow` where $shadow is black "
           "@30% (light themes) / @80% (dark). Plus a hardcoded 0 2px 2px rgba(0,0,0,.2) "
           "on Popover. Carbon states: 'Tiles reside on the same plane as the page "
           "background layer and do not have elevation... Do not add a drop shadow to tiles.'"),
    delta="changed",
    why=("Strata keeps the layering model as the primary depth mechanism for in-flow "
         "surfaces -- that part of Carbon is excellent and is why Carbon reads calm. "
         "But a single 30%-black shadow is blunt: it is too heavy for a dropdown and "
         "too weak for a modal, which is exactly why Carbon had to hardcode a different "
         "one on Popover. Strata publishes three levels, all two-layer (tight contact "
         "shadow + diffuse ambient) and all tinted with the neutral hue rather than pure "
         "black, which is the single biggest contributor to a 'softer' surface read."),
)

# ---------------------------------------------------------------------------
# MOTION — adopted from Carbon essentially unchanged
# ---------------------------------------------------------------------------

MOTION = {
    "ease-standard": dict(value="cubic-bezier(0.2, 0, 0.38, 0.9)",
                          carbon=dict(src=f"{C}/elements/motion/overview/",
                                      value="productive standard — cubic-bezier(0.2, 0, 0.38, 0.9)",
                                      delta="same")),
    "ease-entrance": dict(value="cubic-bezier(0, 0, 0.38, 0.9)",
                          carbon=dict(src=f"{C}/elements/motion/overview/",
                                      value="productive entrance — cubic-bezier(0, 0, 0.38, 0.9)",
                                      delta="same")),
    "ease-exit":     dict(value="cubic-bezier(0.2, 0, 1, 0.9)",
                          carbon=dict(src=f"{C}/elements/motion/overview/",
                                      value="productive exit — cubic-bezier(0.2, 0, 1, 0.9)",
                                      delta="same")),
    "ease-expressive": dict(value="cubic-bezier(0.4, 0.14, 0.3, 1)",
                            carbon=dict(src=f"{C}/elements/motion/overview/",
                                        value="expressive standard — cubic-bezier(0.4, 0.14, 0.3, 1)",
                                        delta="same")),
    "duration-fast":     dict(value="110ms", carbon=dict(src=f"{C}/elements/motion/overview/",
                                                         value="duration-fast-02 = 110ms", delta="same")),
    "duration-moderate": dict(value="150ms", carbon=dict(src=f"{C}/elements/motion/overview/",
                                                         value="duration-moderate-01 = 150ms", delta="same")),
    "duration-slow":     dict(value="240ms", carbon=dict(src=f"{C}/elements/motion/overview/",
                                                         value="duration-moderate-02 = 240ms", delta="same")),
    # [encode 2026-08-20] Was emitted in dist but had dropped out of the token
    # source — the motion patterns (shimmer, spinner, settle) reference it, and
    # an undefined duration var silently disables the animation. Restored with
    # its Carbon provenance.
    "duration-slower":   dict(value="700ms", carbon=dict(src=f"{C}/elements/motion/overview/",
                                                         value="duration-slow-02 = 700ms", delta="same")),
}

# ---------------------------------------------------------------------------
# BREAKPOINTS
# ---------------------------------------------------------------------------

BREAKPOINTS = {"sm": 320, "md": 672, "lg": 1056, "xlg": 1312, "max": 1584}
BREAKPOINTS_CARBON = dict(
    src=f"{C}/elements/2x-grid/overview/",
    value="sm 320 (4 col), md 672 (8), lg 1056 (16), xlg 1312 (16), max 1584 (16); "
          "wide gutter 32px, narrow 16px, condensed 1px",
    delta="same",
    why="Adopted unchanged, including the 16-column 2x Grid and the three gutter modes.",
)

# ---------------------------------------------------------------------------
# LAYOUT  (added -- Carbon has a 2x Grid and a UI Shell; neither was extracted
#          when Strata was derived, and the omission was never recorded. It cost
#          one measured engagement 24 structural classes and 90 rules, with
#          roughly half its finished class uses bespoke rather than system.)
#
# Derived, not copied. The 16-column responsive grid is a shared convention and
# Strata implements it on CSS Grid rather than reproducing Carbon's float/flex
# column classes. Nothing here reproduces IBM product chrome.
# ---------------------------------------------------------------------------

BREAKPOINTS = {"sm": 320, "md": 672, "lg": 1056, "xlg": 1312, "max": 1584}
BREAKPOINTS_CARBON = dict(
    src=f"{C}/elements/2x-grid/overview/",
    value="Carbon breakpoints: sm 320, md 672, lg 1056, xlg 1312, max 1584.",
    delta="same",
    why=None,
)

GRID = {
    "columns": 16,
    "gutter": 32,          # default
    "gutter-narrow": 16,
    "gutter-condensed": 1,
    "container-max": 1584,
    "margin": 16,
}
GRID_CARBON = dict(
    src=f"{C}/elements/2x-grid/overview/",
    value="16 columns; 32px default gutter, 16px narrow, 1px condensed; 1584px max width.",
    delta="changed",
    why=("Values kept 1:1 so anything laid out against Carbon maps without arithmetic. "
         "The implementation differs: CSS Grid with a 16-track template and a gap, "
         "rather than Carbon's per-breakpoint column-width classes. One `.st-col` "
         "with a span attribute replaces 80 generated classes, and subgrid-style "
         "nesting works without a wrapper row."),
)

SHELL = {
    "header": 48,
    "rail": 256,
    "rail-collapsed": 48,
    # [E-26, 2026-08-23] The reveal pane. 320 is the top of the 240-320 range the
    # proposal asked for; below it the kv anatomy inside starts wrapping keys.
    "panel": 320,
    "content-max": 1584,
}
SHELL_CARBON = dict(
    src=f"{C}/components/UI-shell-header/usage/",
    value=("Carbon UI Shell: 48px header, 256px side nav, optional right panel, "
           "product switcher, prescribed header utility order "
           "(search, utilities, notifications, help, account, switcher)."),
    delta="changed",
    why=("Dimensions adopted; identity deliberately not. Strata ships no product "
         "switcher and no right panel -- both answer IBM's multi-product portfolio "
         "rather than any structural need, and the header is the most trade-dress-"
         "loaded part of Carbon. Apache-2.0 grants no trademark rights. What is "
         "taken is the anatomy: a persistent header, an optional single-depth rail, "
         "a content region, a skip link. What is added is `app.work-waiting`, a "
         "region with no Carbon equivalent, because every flow this system serves "
         "has explicit persona handoffs that need somewhere to surface. "
         "[E-26, 2026-08-23] The right-panel refusal is now narrower than it was "
         "written. It said `no right panel`; what it meant, and what the shell spec "
         "gave as its reason, was that a PERSISTENT EMPTY panel is an invitation. A "
         "panel that opens on selection and closes on dismiss is not that, and the "
         "refusal never covered it. `app.detail` is added for the dismissible case "
         "only; the persistent Carbon panel is still declined, for the reason "
         "originally given."),
)

# Density is declared once on the shell and inherited. Components read the density
# variables, never the raw size scale.
#
# This exists because component defaults encode an assumed information density. A
# product rendering 12,000 rows with provenance glyphs was compressed by hand
# throughout -- correct component usage that still looked wrong, because there was
# nowhere to declare "this product is dense".
# [encode 2026-08-20, ledger E-05] Defaults one step denser: control 48 -> 40,
# row 48 -> 40, pad 16 -> 12. The B-language reads premium at working density;
# 48px controls made every rendering read as a marketing page. This partially
# reverses the 48px-default divergence recorded in SIZES_CARBON above — the
# 44px touch floor still holds for bare-icon controls (.st-icon-btn), and lg
# remains one declaration away for touch-first products.
DENSITY = {
    "comfortable": {"control": "md", "row": 40, "pad": "04"},
    "compact":     {"control": "sm", "row": 32, "pad": "03"},
}
DENSITY_CARBON = dict(
    src=f"{C}/elements/spacing/overview/",
    value=("Carbon has no global density mode. Size variants are set per component "
           "instance (Data table xs/sm/md/lg/xl, Button sm/md/lg/xl)."),
    delta="added",
    why=("Per-instance sizing means density is re-decided on every surface and "
         "drifts within one product. One declaration on the shell that components "
         "inherit makes it a recorded decision instead of an accumulation of local "
         "ones. Per-component overrides remain available where a surface genuinely "
         "differs."),
)

# ---------------------------------------------------------------------------
# ICONS  (no asset set shipped yet — these are the adopted construction rules)
# ---------------------------------------------------------------------------

ICON_SIZES = {"sm": 16, "md": 20, "lg": 24, "xl": 32}
ICON_RULES = {
    "grid": "32 x 32px master grid",
    "padding": "2px on all four sides (28 x 28px live area)",
    "stroke": "2px, uniform",
    "corner radius": "2px, increased in multiples of two where needed",
    "angles": "45 degrees primary; 15-degree increments elsewhere",
    "touch target": "44px minimum, padded up in CSS where the glyph is smaller",
    "colour": "solid and monochromatic; must pass 4.5:1, same as type",
    "alignment": "centre-aligned to adjacent text, never baseline-aligned",
}
ICONS_CARBON = dict(
    src="https://www.ibm.com/design/language/iconography/ui-icons/design",
    value=("Verbatim from IBM Design Language: 'IBM icons are drawn on a pixel-based grid of "
           "32px x 32px'; 'The grid contains 2px padding'; 'Use a 2px stroke for all icons to "
           "maintain uniformity'; 'Use a consistent corner radius of 2px for rounded shapes'; "
           "'Use 45 degree angles for even anti-aliasing. Use increments of 15 degrees whenever "
           "possible'. Artboard sizes 16/20/24/32 come from /elements/icons/usage/. "
           "@carbon/icons v11.85.0 ships 2,734 icons (2,711 non-deprecated) across 2,828 SVG "
           "assets, licensed Apache-2.0 with no icon-specific restriction."),
    delta="same",
    why=("Construction rules adopted wholesale — they are well-reasoned and independently "
         "verifiable. No asset set is shipped here; the guide uses eleven placeholder glyphs. "
         "One caveat if you take Carbon's icons directly: the library contains several hundred "
         "logo--* and ibm-* marks, and Apache-2.0 SS6 licenses the files but grants no rights in "
         "the trademarks they depict."),
)

ASPECT_RATIOS = ["1x1", "2x1", "1x2", "3x2", "2x3", "4x3", "3x4", "16x9", "9x16"]
ASPECT_CARBON = dict(
    src="https://carbondesignsystem.com/elements/2x-grid/overview/",
    value=("The 2x Grid page publishes six ratios (1:1, 2:1, 2:3, 3:2, 4:3, 16:9) 'in either "
           "portrait or landscape'. The shipped code makes the inversions explicit: nine classes "
           "on the pattern .cds--aspect-ratio--{W}x{H} plus a required .cds--aspect-ratio base "
           "class, exposed as the overridable $aspect-ratios variable. Note this lives in "
           "scss/components/aspect-ratio/, not scss/utilities/."),
    delta="same",
    why="Nine ratios adopted verbatim, including the three portrait inversions the docs imply "
        "but do not enumerate.",
)

# ---------------------------------------------------------------------------
# SEMANTIC COLOUR
# ---------------------------------------------------------------------------
# Format:  token -> (light_ref, dark_ref, role, carbon_provenance)
# refs are "ramp.grade", "ramp.grade@alpha", "white", "black", or "transparent".

def cb(value, delta="same", why=None, src=f"{C}/elements/color/tokens/"):
    d = dict(src=src, value=value, delta=delta)
    if why:
        d["why"] = why
    return d


SEMANTIC = {
    # ---- background -------------------------------------------------------
    "background":            ("white", "neutral.100", "Page background",
                              cb("White theme #ffffff / Gray 100 #161616")),
    "background-hover":      ("neutral.50@0.12", "neutral.50@0.16", "Hover on transparent surfaces",
                              cb("$background-hover — Gray 50 @12% light / @16% dark")),
    "background-active":     ("neutral.50@0.40", "neutral.50@0.36", "Active on transparent surfaces",
                              cb("$background-active — Gray 50 @50% light / @40% dark", "changed",
                                 "Carbon's 50% active wash on light themes drops the underlying "
                                 "label to roughly 2.4:1 mid-press. 40% keeps the state legible "
                                 "for the whole duration of the interaction.")),
    "background-selected":   ("neutral.50@0.20", "neutral.50@0.24", "Selected on transparent surfaces",
                              cb("$background-selected — Gray 50 @20% / @24%")),
    "background-inverse":    ("neutral.80", "neutral.10", "High-contrast surfaces: tooltips, toasts",
                              cb("$background-inverse — Gray 80 / Gray 10")),
    "background-brand":      (f"{P}.70", f"{P}.60", "Brand fill: batch action bars, selected dates",
                              cb("$background-brand — Blue 60 #0f62fe in all four themes", "changed",
                                 "Deloitte Green 349 #046A38. Grade 70 reproduces it to within "
                                 "delta-RGB 5 in the light theme. NOT held constant across themes, "
                                 "which is where Carbon does hold it constant: a grade-70 fill on a "
                                 "grade-100 page measures 2.45:1 and barely reads as a surface at "
                                 "all. Dark drops to grade 60 for 3.48:1.")),

    # ---- layer ------------------------------------------------------------
    "layer-01":              ("neutral.10", "neutral.90", "Container on the page background",
                              cb("$layer-01 — Gray 10 (White theme) / Gray 90 (Gray 100 theme)")),
    "layer-02":              ("white", "neutral.80", "Container on layer-01",
                              cb("$layer-02 — White / Gray 80")),
    "layer-03":              ("neutral.10", "neutral.70", "Container on layer-02",
                              cb("$layer-03 — Gray 10 / Gray 70")),
    "layer-hover-01":        ("neutral.20", "neutral.80", "Hover for layer-01",
                              cb("$layer-hover-01 — Gray 10 hover #e8e8e8 / Gray 90 hover #333333")),
    "layer-active-01":       ("neutral.30", "neutral.70", "Active for layer-01",
                              cb("$layer-active-01 — Gray 30 / Gray 70")),
    "layer-selected-01":     ("neutral.20", "neutral.80", "Selected for layer-01",
                              cb("$layer-selected-01 — Gray 20 / Gray 80")),
    "layer-accent-01":       ("neutral.20", "neutral.80", "Tertiary surface: table headers, zebra rows",
                              cb("$layer-accent-01 — Gray 20 / Gray 80")),
    "layer-accent-hover-01": ("neutral.30", "neutral.70", "Hover for layer-accent-01",
                              cb("$layer-accent-hover-01 — Gray 20 hover #d1d1d1 / Gray 80 hover #474747")),

    # ---- field ------------------------------------------------------------
    # Carbon's off-by-one rule is preserved: a field is a layer above the surface
    # it sits on, so field-01 is used on `background`, field-02 on layer-01.
    "field-01":              ("neutral.10", "neutral.90", "Input on the page background",
                              cb("$field-01 — Gray 10 / Gray 90. 'A field is considered a layer "
                                 "on top of the background it is placed on' — /elements/color/usage/",
                                 src=f"{C}/elements/color/usage/")),
    "field-02":              ("white", "neutral.80", "Input on layer-01",
                              cb("$field-02 — White / Gray 80", src=f"{C}/elements/color/usage/")),
    "field-hover-01":        ("neutral.20", "neutral.80", "Hover for field-01",
                              cb("$field-hover-01 — Gray 10 hover / Gray 90 hover")),

    # ---- border -----------------------------------------------------------
    # [encode 2026-08-20, ledger E-04] The border ramp lightened one stance:
    # subtle-00 is now the WHISPER hairline for large surfaces (cards, table
    # frames) — an alpha ref so it composites correctly on any layer — and
    # subtle-01 (the old subtle-00 value) is the standard hairline for controls
    # and dividers. Grade 30/70 retires from rest states; border-strong is
    # unchanged and remains the accessible fallback (.st-field--strong).
    # Decorative boundaries below 3:1 stay advisory-exempt, as before.
    "border-subtle-00":      ("neutral.60@0.13", "neutral.60@0.30", "Whisper hairline for surfaces",
                              cb("$border-subtle-00 — Gray 20 / Gray 80", "changed",
                                 "Lightened to the whisper hairline of the 20 Aug 2026 visual "
                                 "language (composites to ~#ececed on white). Separation is "
                                 "carried by the hairline plus the resting shadow, not tone.")),
    "border-subtle-01":      ("neutral.20", "neutral.80", "Standard hairline on controls and dividers",
                              cb("$border-subtle-01 — Gray 30 / Gray 70", "changed",
                                 "One step lighter than Carbon's: grade 20/80 (the old "
                                 "subtle-00 values). Part of the same E-04 re-cut.")),
    "border-strong-01":      ("neutral.60", "neutral.50", "Field underline; >=3:1 non-text",
                              cb("$border-strong-01 — Gray 50 #8d8d8d in both light themes", "changed",
                                 "Carbon uses Gray 50 for border-strong on every light layer. "
                                 "Against layer-01 (#f4f4f4) that measures 3.02:1 — it passes "
                                 "1.4.11, but by 0.02. Strata uses neutral-60, which measures "
                                 "4.62:1 on layer-01 and 4.99:1 on the page background, so the "
                                 "guarantee survives a hue swap or a rounding change.")),
    "border-inverse":        ("neutral.100", "neutral.10", "Highest-contrast border",
                              cb("$border-inverse — Gray 100 / Gray 10")),
    "border-interactive":    (f"{P}.70", f"{P}.40", "Selected / active borders; >=3:1",
                              cb("$border-interactive — Blue 60 / Blue 50", "changed",
                                 "Moved to grade 70 rather than 60 so it sits with the primary "
                                 "action and opens a clear gap to $support-success at grade 60. "
                                 "7.1:1 on the page background.")),
    # [encode 2026-08-20, ledger E-07] Added for the hairline tertiary button:
    # a quiet interactive boundary that says "actionable" without the weight of
    # border-interactive. Decorative-adjacent; the label carries the 4.5:1.
    "border-interactive-subtle": (f"{P}.30", f"{P}.70", "Quiet interactive border (tertiary button)",
                              cb("No Carbon counterpart — Carbon's tertiary uses a full-strength "
                                 "$button-tertiary border", "added",
                                 "The 20 Aug 2026 language draws tertiary as a white surface "
                                 "with a tinted hairline; grade 30 light / 70 dark keeps it "
                                 "recognisably interactive without competing with primary.")),
    "border-disabled":       ("neutral.30", "neutral.70", "Disabled border",
                              cb("$border-disabled — Gray 30 / Gray 50 @50%")),

    # ---- text -------------------------------------------------------------
    "text-primary":          ("neutral.90", "neutral.10", "Body copy and headings",
                              cb("$text-primary — Gray 100 #161616 / Gray 10 #f4f4f4", "changed",
                                 "Carbon's light-theme body text is Gray 100 at 17.4:1 on white. "
                                 "That is far past AAA and is a large part of why Carbon reads "
                                 "hard-edged. neutral-90 gives 14.2:1 — still comfortably AAA, "
                                 "measurably softer. Note this is a deliberate reduction in "
                                 "contrast and is the one divergence to revisit if the product "
                                 "targets low-vision users or bright-sunlight field use.")),
    "text-secondary":        ("neutral.70", "neutral.30", "Input labels, supporting copy",
                              cb("$text-secondary — Gray 70 / Gray 30")),
    "text-placeholder":      ("neutral.60", "neutral.40", "Placeholder text",
                              cb("$text-placeholder — rgba(22,22,22,0.4) in shipped @carbon/styles; "
                                 "Gray 40 #a8a8a8 in the /elements/color/tokens/ table. The two "
                                 "official sources disagree.", "changed",
                                 "Both Carbon values fail 4.5:1 against their own field background "
                                 "(#f4f4f4): the composited rgba value measures 2.53:1, Gray 40 "
                                 "measures 2.16:1. Placeholder is text and WCAG 1.4.3 applies. "
                                 "neutral-60 gives 4.62:1 on field-01 in light; dark uses "
                                 "grade 40, because grade 50 measures only 3.48:1 against "
                                 "field-02 (a field nested on layer-01) — the composited "
                                 "contrast audit caught that, the eye would not have. "
                                 "Carbon's own rule that placeholder must never replace a "
                                 "persistent label is kept and enforced in the component CSS.")),
    "text-helper":           ("neutral.70", "neutral.30", "Helper text under fields",
                              cb("$text-helper — Gray 60 / Gray 40")),
    "text-on-color":         ("white", "white", "Text on a filled interactive surface",
                              cb("$text-on-color — White in all themes")),
    "text-inverse":          ("white", "neutral.90", "Text on background-inverse",
                              cb("$text-inverse — White / Gray 100")),
    "text-disabled":         ("neutral.90@0.30", "neutral.10@0.28", "Disabled text",
                              cb("$text-disabled — text-primary @25%", "changed",
                                 "25% of Carbon's Gray 100 lands near 1.9:1. Disabled text is "
                                 "exempt from contrast minimums, but 'exempt' is not 'illegible'. "
                                 "30% reads as clearly-off without becoming invisible.")),
    "text-error":            (f"{D}.70", f"{D}.30", "Error message text",
                              cb("$text-error — Red 60 #da1e28 / Red 40", "changed",
                                 "Red 60 on a Gray 10 field measures ~4.3:1 in Carbon. Grade 70 "
                                 "clears 4.5:1 against every light surface in the system.")),

    # ---- link -------------------------------------------------------------
    "link-primary":          (f"{P}.70", f"{P}.40", "Links",
                              cb("$link-primary — Blue 60 / Blue 40", "changed",
                                 "Green, matching the interactive colour — a system with two "
                                 "different 'this is clickable' hues teaches nothing. Grade 70 "
                                 "so a link still clears 4.5:1 on layer-01 and inside a filled "
                                 "table row, not only on white.")),
    "link-hover":            (f"{P}.80", f"{P}.30", "Link hover",
                              cb("$link-primary-hover — Blue 70 / Blue 30", "changed",
                                 "Follows link-primary.")),
    "link-visited":          (f"{V}.70", f"{V}.40", "Visited link",
                              cb("$link-visited — Purple 60 / Purple 40", "changed",
                                 "The one deliberately off-brand token in the system. Deloitte's "
                                 "palette has no purple, and visited-link needs a hue that carries "
                                 "no other meaning here — green is interactive, blue is "
                                 "informational, teal and orange are categorical, red and amber "
                                 "are status. Every Deloitte hue is spoken for. Substituting one "
                                 "would make 'visited' collide with a live signal, which is worse "
                                 "than an off-brand link. Drop visited styling entirely if that "
                                 "trade is unacceptable.")),

    # ---- icon -------------------------------------------------------------
    "icon-primary":          ("neutral.90", "neutral.10", "Primary icons",
                              cb("$icon-primary — Gray 100 / Gray 10")),
    "icon-secondary":        ("neutral.70", "neutral.30", "Secondary icons",
                              cb("$icon-secondary — Gray 70 / Gray 30")),
    "icon-on-color":         ("white", "white", "Icons on a filled surface",
                              cb("$icon-on-color — White")),
    "icon-disabled":         ("neutral.90@0.30", "neutral.10@0.28", "Disabled icons",
                              cb("$icon-disabled — icon-primary @25%", "changed",
                                 "Matched to text-disabled for the same reason.")),
    "icon-interactive":      (f"{P}.60", f"{P}.40", "Icons that signal operability",
                              cb("$icon-interactive — Blue 60 / White", "changed", "Brand green.")),

    # ---- support ----------------------------------------------------------
    "support-error":         (f"{D}.60", f"{D}.40", "Error",
                              cb("$support-error — Red 60 / Red 50")),
    "support-success":       (f"{S}.60", f"{S}.40", "Success",
                              cb("$support-success — Green 50 / Green 40", "changed",
                                 "Value unchanged, but the RELATIONSHIP changed and this is the "
                                 "one token to argue about. With a green brand, success and the "
                                 "primary action are now one grade apart in the same hue "
                                 "(green.60 vs green.70). They are kept apart by form, not by "
                                 "colour: support-success only ever renders as a toggle track, a "
                                 "status icon or a 3px banner rule, never as a filled "
                                 "action-shaped surface, and every status carries an icon under "
                                 "the never-colour-alone rule. The alternative — moving success "
                                 "to teal — breaks the strongest colour convention in UI "
                                 "(green = good) to solve a collision the form language already "
                                 "resolves, and would push info off Deloitte Blue. If user "
                                 "testing says otherwise it is one line: change this to "
                                 "teal.60 / teal.30 and move the tag palette with it.")),
    "support-warning":       (f"{W}.60", f"{W}.30", "Warning",
                              cb("$support-warning — Yellow 30 #f1c21b in ALL FOUR themes", "changed",
                                 "Two problems fixed at once. (1) Carbon holds Yellow 30 constant "
                                 "across light and dark, breaking the contract that every semantic "
                                 "token re-resolves per theme. (2) Yellow 30 measures ~1.6:1 on "
                                 "white, so a Carbon warning icon fails 1.4.11 against its own "
                                 "notification background — the status that most needs to be "
                                 "noticed is the one that disappears. Strata resolves per theme "
                                 "and drops to grade 60 in light, which measures 4.6:1 on the "
                                 "warning surface. It reads as ochre rather than school-bus "
                                 "yellow; that is the cost of making it visible.")),
    "support-info":          (f"{I}.60", f"{I}.40", "Information",
                              cb("$support-info — Blue 70 / Blue 50", "same",
                                 "Deloitte Blue 7690 #0076A8, which grade 60 reproduces to within "
                                 "delta-RGB 3. Note this REVERSES a pre-brand divergence: Strata "
                                 "previously moved info to teal because Carbon's blue info "
                                 "collided with Carbon's blue primary action. With a green "
                                 "primary that objection disappears and blue is free, so info "
                                 "returns to Carbon's value. The divergence was contingent on the "
                                 "brand, not on Carbon being wrong — which is the argument for "
                                 "semantic tokens in one example.")),
    "support-error-subtle":   (f"{D}.10", f"{D}.100", "Error notification background", cb(
        "Component tokens $notification-error-background-color. Values not published on the docs "
        "page for dark themes.", "added",
        "Promoted from a Notification-only component token to a core token. Status backgrounds "
        "are needed by banners, table cells, form sections and inline validation, not just the "
        "Notification component, and Carbon's component-token confinement rule ('should never be "
        "used for anything other than their own component') would otherwise force a duplicate.",
        src=f"{C}/components/notification/style/")),
    "support-success-subtle": (f"{S}.10", f"{S}.100", "Success notification background",
                               cb("as above", "added", "as above", src=f"{C}/components/notification/style/")),
    "support-warning-subtle": (f"{W}.10", f"{W}.100", "Warning notification background",
                               cb("as above", "added", "as above", src=f"{C}/components/notification/style/")),
    "support-info-subtle":    (f"{I}.10", f"{I}.100", "Info notification background",
                               cb("as above", "added", "as above", src=f"{C}/components/notification/style/")),

    # ---- interactive / focus ---------------------------------------------
    "interactive":           (f"{P}.70", f"{P}.40", "Selected and active elements",
                              cb("$interactive — Blue 60 / Blue 50", "changed", "Brand green.")),
    "focus":                 (f"{F}.60", f"{F}.40", "Focus ring",
                              cb("$focus — Blue 60 light / White dark; 2px, outline-offset -2px "
                                 "(inset) per @carbon/styles _focus-outline.scss",
                                 src=f"{C}/elements/color/overview/")),
    "focus-inset":           ("white", "neutral.100", "Inner ring, paired with focus",
                              cb("$focus-inset — White / Gray 100. Carbon: 'Often times to achieve "
                                 "proper 3:1 contrast a $focus-inset border is used between the "
                                 "focus border and the element itself.'",
                                 src=f"{C}/elements/color/overview/")),

    # ---- button -----------------------------------------------------------
    "button-primary":        (f"{P}.70", f"{P}.60", "Primary button fill",
                              cb("$button-primary — Blue 60 in all themes", "changed",
                                 "Deloitte Green 349. Grade 70, not 60: the brand's dark green is "
                                 "a 7.1:1 colour, and it leaves grades 80 and 90 free for hover "
                                 "and active. A grade-60 green would have run out of room. The "
                                 "dark theme uses grade 60 instead: at grade 70 the button barely "
                                 "separates from the page (2.45:1), and the near-black "
                                 "$focus-inset ring inside it fell to 2.46:1 — the composited "
                                 "audit caught that, and it is a failure mode a blue primary "
                                 "never had because Carbon's Blue 60 is a lighter colour than "
                                 "Deloitte's dark green.",
                                 src=f"{C}/components/button/style/")),
    "button-primary-hover":  (f"{P}.80", f"{P}.70", "Primary hover",
                              cb("$button-primary-hover — #0050e6 shipped / #0353e9 documented",
                                 src=f"{C}/components/button/style/")),
    "button-primary-active": (f"{P}.90", f"{P}.80", "Primary active",
                              cb("$button-primary-active — Blue 80", src=f"{C}/components/button/style/")),
    "button-secondary":      ("neutral.80", "neutral.70", "Secondary button fill",
                              cb("$button-secondary — Gray 80 / Gray 60", "changed",
                                 "Dark theme drops a grade. Carbon's dark secondary button is "
                                 "Gray 60 with $text-on-color (white) on it, which measures "
                                 "about 3.5:1 — under 4.5:1 for a button label. Grade 70 gives "
                                 "7.1:1 and leaves room for the hover to lighten without "
                                 "crossing the threshold.",
                                 src=f"{C}/components/button/style/")),
    "button-secondary-hover":("neutral.90", "neutral.60", "Secondary hover",
                              cb("$button-secondary-hover — Gray 80 hover / Gray 60 hover",
                                 "changed",
                                 "Follows the base grade. Carbon's dark hover lightens toward "
                                 "Gray 50, where a white label falls to roughly 3.0:1 — the "
                                 "hover state is where the label becomes least readable, which "
                                 "is backwards.",
                                 src=f"{C}/components/button/style/")),
    "button-danger":         (f"{D}.60", f"{D}.60", "Danger button fill",
                              cb("$button-danger-primary — Red 60", src=f"{C}/components/button/style/")),
    "button-danger-hover":   (f"{D}.70", f"{D}.70", "Danger hover",
                              cb("$button-danger-hover — #b81921 hardcoded (note: @carbon/colors "
                                 "red60Hover is #b81922 — the two official values differ by one digit)",
                                 src=f"{C}/components/button/style/")),
    "button-disabled":       ("neutral.20", "neutral.80", "Disabled button fill",
                              cb("$button-disabled — Gray 30 / Gray 50 @30%", "changed",
                                 "Gray 30 against a white page is a loud disabled state. Grade 20 "
                                 "recedes; the disabled label still reads at ~3.4:1 against it.")),

    # ---- misc -------------------------------------------------------------
    "overlay":               ("neutral.100@0.55", "neutral.100@0.70", "Modal scrim",
                              cb("$overlay — Black @60% in all four themes", "changed",
                                 "Tinted with the neutral hue instead of pure black, and lightened "
                                 "in light themes. Pure black scrims are the other half of why "
                                 "Carbon reads industrial.")),
    "highlight":             (f"{P}.20", f"{P}.90", "Range fills, text highlight",
                              cb("$highlight — Blue 20 / Blue 90", "changed", "Brand green.")),
    "toggle-off":            ("neutral.60", "neutral.50", "Toggle track, off; >=3:1",
                              cb("$toggle-off — Gray 50 / Gray 60")),
    "toggle-handle":         ("white", "neutral.90", "Toggle handle, both states",
                              cb("$icon-on-color — White in every theme", "changed",
                                 "A white handle on Carbon's dark-theme $support-success "
                                 "(Green 40) measures about 2.2:1 — the handle, which is the "
                                 "only thing communicating the toggle's position, is the least "
                                 "visible part of it in dark mode. Strata inverts the handle "
                                 "with the theme: 5.0:1 and 4.7:1 in light, 6.6:1 and 4.7:1 in "
                                 "dark, on the on and off tracks respectively.")),
    "skeleton-background":   ("neutral.20", "neutral.90", "Skeleton container",
                              cb("$skeleton-background — Gray 10 hover / Gray 100 hover")),
    "skeleton-element":      ("neutral.30", "neutral.80", "Skeleton text/element",
                              cb("$skeleton-element — Gray 30 / Gray 80")),
}

# ---------------------------------------------------------------------------
# COMPONENT SPECS  (values consumed by the emitted CSS and shown in the guide)
# ---------------------------------------------------------------------------

COMPONENTS = {
    "button": dict(
        summary="Primary, secondary, tertiary, ghost and danger, in three sizes.",
        carbon_src=f"{C}/components/button/usage/",
        spec=[
            ("Heights", "sm 32 / md 40 / lg 48 (default)",
             "Carbon: seven sizes across two variants — button xs 24, sm 32, md 40, "
             "large-productive 48, large-expressive 48; full-bleed button xl 64, 2xl 80",
             "changed", "Same scale, default moved to 48 to clear the 44px touch floor. The two "
             "48s and the full-bleed-only 64/80 are collapsed: a size scale with two entries at "
             "the same height is a naming artefact, not a size."),
            ("Padding", "16px both sides; label centred",
             "Carbon: 16px left / 64px right on a button with NO icon. Buttons with icons, "
             "icon-only buttons and all ghost buttons are already 16/16. Carbon's stated basis: "
             "'When we say \"fixed,\" there is a fixed padding of 16px to the left and a 64px "
             "padding to the right of the button label. The button label determines the "
             "button\'s width.' Paired with the Do caption 'Do left-align the label in a "
             "button, even if the button is wide.'",
             "changed",
             "Narrower than it first looks — Carbon is already symmetric in four of five cases, "
             "so this changes one. Carbon does publish a rationale for the 16 (nothing within "
             "16px of a border; >=16px between label and icon so adjacent icon buttons stay "
             "separable) but none for the 64. The result is a button whose visual centre of "
             "mass sits left of its geometric centre, which is why a separate left-align rule "
             "is needed to keep it consistent. Strata centres the label instead."),
            ("Radius", "6px (radius-md)", "Carbon: not published on the style page, and "
             "_button.scss sets no border-radius", "changed", "See the radius scale."),
            ("Icon", "16px, 8px gap",
             "Carbon: 16x16 icon (20x20 expressive); 32px label-to-icon gap on filled buttons, "
             "8px on ghost",
             "changed", "One gap value. The 32px filled-button gap is a consequence of the 64px "
             "right pad, not an independent decision."),
            ("Focus", "2px focus ring, inset, + 1px focus-inset ring on filled variants",
             "Carbon: the style page publishes only colours ($focus border, $focus-inset inset) "
             "plus 'box-shadow: inset | 1px'. Shipped code is a 1px border that turns $focus, "
             "with box-shadow inset 1px $focus AND inset 2px in the button's own background "
             "colour — so the visible double ring is 1px+2px, not 2px+1px.",
             "changed",
             "Strata uses the generic 2px/-2px geometry from Carbon's own focus-outline mixin "
             "for every control including buttons, rather than button's bespoke 1px "
             "border-plus-two-shadows construction. Same two-tone mechanism, one implementation."),
            ("Ordering", "Primary right in dialogs and wizards; primary left on full pages",
             "Carbon: identical rule", "same", None),
            ("Label", "Sentence case, {verb} + {noun}", "Carbon: identical rule", "same", None),
        ],
    ),
    "text-input": dict(
        summary="Text input, textarea and the shared field chrome.",
        carbon_src=f"{C}/components/text-input/style/",
        spec=[
            ("Heights", "sm 32 / md 40 / lg 48 (default)", "Carbon: 32 / 40 (default) / 48",
             "changed", "Default moved to lg, as with buttons."),
            ("Border", "1px full border, all four sides",
             "Carbon: border-bottom 1px $border-strong only; no side or top border",
             "changed",
             "Carbon's underline-only field is the strongest single signal of its visual "
             "identity, and the hardest to defend. A field with no left, right or top edge "
             "does not read as a container, its click target is ambiguous, and adjacent "
             "fields in a row visually merge. Carbon then has to switch to a full 2px border "
             "on focus and on error — so the boxed form already exists in the system, it is "
             "just withheld from the resting state. A full 1px border makes the resting, "
             "focus and error states the same shape."),
            ("Radius", "6px (radius-md)", "Not published", "changed", "See the radius scale."),
            ("Label", "text-secondary, label-sm, 8px above the field",
             "Carbon: $text-secondary, $label-01, margin-bottom 8px ($spacing-03)", "same", None),
            ("Helper", "text-helper, helper, 4px below",
             "Carbon: $text-helper, $helper-text-01, margin-top 4px ($spacing-02)", "same", None),
            ("Error", "2px support-error border, icon, message replaces helper text",
             "Carbon: border 2px $support-error, message $text-error at $label-01, replaces helper",
             "same", None),
            ("Warning", "amber icon; message in text-primary; border unchanged",
             "Carbon: identical — warning icon $support-warning, warning message $text-primary "
             "at $label-01, and no border row at all for the warning state. Carbon publishes no "
             "rationale for the asymmetry with error.",
             "same", None),
            ("Field stack", "24px between fields; 48px before the button row",
             "Carbon (forms pattern page, not the text-input style page): 'we recommend a 32px "
             "spacer between input fields' on dedicated pages, 'designers can revert to 24px or "
             "even 16px' in contained forms, and 'a 48px spacer between the last input and the "
             "button or button group'. The Form style page gives a partly different set again.",
             "changed",
             "One value instead of three. 32px at a 14px body was proportionate; at a 16px "
             "body with taller controls it over-separates."),
        ],
    ),
    "checkbox": dict(
        summary="Checkbox with indeterminate state.",
        carbon_src=f"{C}/components/checkbox/style/",
        spec=[
            ("Control", "18x18px, 1px border, 2px radius",
             "Carbon: 16x16px, 1px border. Radius is not published on the style page, but "
             "_checkbox.scss ships border-radius: 2px — the 2px is Carbon's own value, just "
             "undocumented.",
             "changed",
             "Size only: 18px to sit better against a 16px body line, and to narrow Carbon's "
             "own unexplained gap between its 16px checkbox and 20px radio. The 2px radius is "
             "adopted, not invented."),
            ("Item gap", "8px", "Carbon: checkbox items 4px apart, radio items 8px apart",
             "changed", "Carbon states both values on its two style pages. Unified at 8px."),
            ("Label", "body-md, 8px to the left of the label",
             "Carbon: $body-compact-01, padding-left 8px ($spacing-03)", "changed",
             "Body token only; spacing identical."),
            ("Focus", "2px focus ring, 1px inset",
             "Carbon: border 2px, inset 1px — one of only two component style pages that "
             "publish the focus inset (button is the other, as 'box-shadow: inset | 1px')",
             "same", None),
            ("Wrapping", "Wrapped label text top-aligns to the control",
             "Carbon: identical rule; ellipsis truncation explicitly prohibited", "same", None),
        ],
    ),
    "radio": dict(
        summary="Radio button.",
        carbon_src=f"{C}/components/radio-button/style/",
        spec=[
            ("Control", "18x18px, 8px dot", "Carbon: 20x20px control, 8px dot",
             "changed", "Matched to the checkbox at 18px."),
            ("Item gap", "8px", "Carbon: 8px", "same", None),
            ("Default state", "Nothing preselected",
             "Carbon: 'The default view of a radio button is having no radio button preselected.'",
             "same", None),
        ],
    ),
    "toggle": dict(
        summary="Binary switch that applies instantly.",
        carbon_src=f"{C}/components/toggle/style/",
        spec=[
            ("Track", "48x24 (default), 32x16 (small)", "Carbon: 48x24 and 32x16", "same", None),
            ("Handle", "18px / 10px", "Carbon: 18px (published as '18/1.25' — the rem value is "
             "wrong, 18px is 1.125rem) / 10px", "same", "Value adopted; the docs typo noted."),
            ("On colour", "support-success", "Carbon: $support-success", "same", None),
            ("Off colour", "toggle-off, >=3:1", "Carbon: $toggle-off", "same", None),
            ("State text", "Required, three words or less, adjectives not verbs",
             "Carbon: 'It must be three words or less' and 'Use adjectives rather than verbs to "
             "describe actions and the state of the object affected.' Required on the default "
             "toggle only — on the small toggle both label and state text are optional.",
             "same", None),
            ("Use", "Only for instantly-applied binary settings",
             "Carbon: 'Ideal for settings or preferences that can be immediately applied.' and "
             "'Avoid using toggles for settings that aren\'t binary in nature or don\'t provide "
             "instant application; instead use a different UI component, like a checkbox, in "
             "combination with a button.'", "same", None),
        ],
    ),
    "select": dict(
        summary="Select and dropdown, sharing the field chrome.",
        carbon_src=f"{C}/components/dropdown/style/",
        spec=[
            ("Heights", "Matches text input", "Carbon: matches; menu item height matches field height",
             "same", None),
            ("Right padding", "40px to clear the chevron",
             "Carbon: 48px ($spacing-09) on both the dropdown and select structure tables — "
             "though _dropdown.scss actually ships 42px, so Carbon's own code disagrees with "
             "its published value",
             "changed", "40px clears a 16px chevron with 16px of inset at 48px tall, and it is "
             "one value rather than two."),
            ("Menu", "layer-02 surface, elevation-02, 6px radius, max-height 320px",
             "Carbon: $layer surface, box-shadow 0 2px 6px 0 rgba(0,0,0,.2), border-radius 0. "
             "A scroll threshold IS published: 'We recommend starting a scroll at the sixth "
             "option in the menu list' while 'showing 50% of the last option\'s container "
             "height to indicate there is more to see'. Shipped as max-block-size 220px "
             "(40px item x 5.5).",
             "changed", "Carbon's rule restated at Strata's row height — 320px is six 48px rows, "
             "the same intent as Carbon's 220px at 40px rows. Strata publishes the px value as "
             "well as the rule, so it can be a token."),
            ("Option states", "hover layer-hover-01, selected layer-selected-01 + checkmark",
             "Carbon: $layer-hover, $layer-selected, checkmark $icon-primary", "same", None),
            ("Under three options", "Use radio buttons instead",
             "Carbon (select usage page, not dropdown): 'It is best practice not to use a "
             "select if there are fewer than three options for selection. In this case, use a "
             "radio button group instead.'", "same", None),
        ],
    ),
    "date-picker": dict(
        summary="Simple, single and range date input with calendar flyout.",
        carbon_src=f"{C}/components/date-picker/usage/",
        spec=[
            ("Field text", "body-md — the same token as every other field",
             "Carbon: $code-02 (!). Every other Carbon field uses $body-compact-01",
             "changed",
             "Carbon's date field is the only one set in the mono type token. There is no "
             "published rationale; the plausible one is tabular figure alignment, which is "
             "better served by font-variant-numeric: tabular-nums on the normal face. Strata "
             "does that instead."),
            ("Helper text", "helper token", "Carbon: $label-01 — again the only field that "
             "does not use $helper-text-01", "changed", "Normalised to the shared field pattern."),
            ("Calendar", "288x336px, fixed; left-aligned to the field",
             "Carbon: 288x336px, fixed width, 'should always be aligned to the left edge of "
             "its assigned text field'", "same", None),
            ("Day cell", "40x40px at every field size", "Carbon: 40x40px at every field size",
             "same", "Adopted; the calendar deliberately does not scale with the field."),
            ("Shadow", "elevation-02 token",
             "Carbon: the style page publishes a raw '0 2px 6px 0 rgba(0, 0, 0, 0.2)'; the "
             "shipped _flatpickr.scss calls @include box-shadow, which is '0 2px 6px $shadow' "
             "with $shadow at 30% alpha. The docs and the code disagree on the alpha, and only "
             "the docs are untokenised.",
             "changed", "A documentation defect rather than an implementation one — but it is "
                        "the kind that propagates, because a designer redlining from the style "
                        "page will specify 20% and get 30%."),
            ("Range states", "start / in range / end each explicitly specified",
             "Carbon: the calendar interactive-state table lists Hover, Focus, Disabled, "
             "Selected, In range, End range and Next month — there is no range-START row",
             "changed", "The gap is filled: range start uses the same treatment as Selected. "
                        "Carbon's spellings 'In range' and 'End range' are kept."),
            ("Today", "link-primary text + a 4px dot",
             "Carbon: $link-01 + a 4px dot. $link-01 is a v10 token name that appears exactly "
             "once across every page in the site repo — this row. Every other component uses "
             "$link-primary.", "changed", "Retokenised to link-primary."),
            ("Out-of-month days", "text-secondary — selectable, above 4.5:1",
             "Carbon: 'Next month | Day | text-color | $text-secondary'", "same",
             "Adopted after an axe run caught this build using text-disabled here. "
             "Out-of-month days are selectable, so the disabled exemption does not apply to "
             "them; Carbon had it right and this build had it wrong."),
            ("Format", "Shown in the label or helper text, never placeholder-only",
             "Carbon: 'When using a simple date input, include the date format in parentheses "
             "inline with the label or as helper text below the label.' and 'Only including the "
             "date format as placeholder text inside the field is problematic because it will "
             "disappear from view once the user begins typing.'", "same", None),
        ],
    ),
    "table": dict(
        summary="Data table with sorting, selection, zebra and expansion.",
        carbon_src=f"{C}/components/data-table/style/",
        spec=[
            ("Row heights", "xs 24 / sm 32 / md 40 / lg 48 / xl 64", "Carbon: identical five sizes",
             "same", None),
            ("Header", "Matches row height; heading-compact; layer-accent-01",
             "Carbon: 'The column header row should always match the row size of the table.'; "
             "$heading-compact-01; $layer-accent", "same", None),
            ("Row border", "1px border-subtle-01 bottom", "Carbon: border-bottom $border-subtle, "
             "width not published", "same", "Width made explicit."),
            ("Zebra", "layer-accent-01 on alternate rows", "Carbon: $layer-accent", "same", None),
            ("Selected row", "layer-selected-01 + border-subtle-selected",
             "Carbon: $layer-selected, $border-subtle-selected", "same", None),
            ("Batch bar", "background-brand, text-on-color, at the top of the table",
             "Carbon: $background-brand, $text-on-color, top of table, row actions disabled "
             "while batch mode is active", "same", None),
            ("Sort icon", "Visible on hover when unsorted; persistent on the sorted column",
             "Carbon: identical rule", "same", None),
            ("Sticky header", "Specified: header sticks, body scrolls, max-height set by the caller",
             "Carbon: no sticky-header design spec exists anywhere. Zero matches for sticky / "
             "frozen / pinned across all four data-table pages (usage, style, code, "
             "accessibility) — while DataTable.tsx declares stickyHeader?: boolean in three "
             "interfaces.",
             "added", "A real gap in Carbon — the React implementation supports it, the design "
                      "system never specified it."),
        ],
    ),
    "modal": dict(
        summary="Passive, transactional and danger dialogs.",
        carbon_src=f"{C}/components/modal/style/",
        spec=[
            ("Widths", "xs 320 / sm 480 / md 640 / lg 880px, capped at calc(100vw - 32px)",
             "Carbon: 'Modal widths are defined as percentages of the browser but will still "
             "align to columns on the 2x grid' — xs 24%, sm 36%, md 48%, lg 72% at 1584, with "
             "column spans (4/6/8/12 of 16) but no px values published anywhere",
             "changed",
             "Percentage-of-viewport widths mean a dialog's measure changes with the browser, so "
             "body copy runs to 90+ characters on a wide monitor. Fixed max-widths with a "
             "viewport cap hold the measure constant, which is what dialog copy needs."),
            ("Buttons", "Right-aligned, natural width, 8px apart",
             "Carbon: buttons span 50% of the modal each and bleed to its edges; three buttons "
             "are 25% each", "changed",
             "Full-bleed 50% buttons make Cancel exactly as visually heavy as the primary "
             "action, which is the opposite of what a confirmation dialog should do."),
            ("Radius", "8px (radius-lg)", "Carbon: not published, and _modal.scss contains no "
             "border-radius declaration at all", "changed", "See the radius scale."),
            ("Scrim", "overlay token", "Carbon: $overlay, black @60%, identical in all four "
             "themes", "changed", "Tinted and lightened."),
            ("Scrolling", "Body scrolls; header and footer stay fixed. No horizontal scroll.",
             "Carbon: identical rule", "same", None),
            ("Focus", "First field, or the primary button if there is no field. Esc closes.",
             "Carbon: identical rule", "same", None),
        ],
    ),
    "tabs": dict(
        summary="Line tabs.",
        carbon_src=f"{C}/components/tabs/style/",
        spec=[
            ("Height", "40px", "Carbon: 40px for both line and contained", "same", None),
            ("Selected", "2px border-interactive underline + weight 600",
             "Carbon: border-bottom 2px $border-interactive; label switches from "
             "$body-compact-01 to $heading-compact-01 (400 -> 600)", "same",
             "Adopted including the weight change — it is what makes the selected tab survive "
             "greyscale, satisfying 'don't rely on colour alone'."),
            ("Rest", "1px border-subtle-01 underline across the whole tab list",
             "Carbon: border-bottom 2px $border-subtle ($tab-underline-color) — the same width "
             "as the selected state, only the colour changes",
             "changed",
             "1px at rest, 2px selected. Carbon's equal-width treatment means the resting "
             "underline carries as much visual weight as the selection indicator, so the "
             "selected tab has to rely on colour plus weight to separate itself. Halving the "
             "rest state lets the 2px selected rule read as an indicator rather than a recolour."),
            ("Labels", "One or two words",
             "Carbon: 'Use short tab labels that are clear and specific. Labels should be one to "
             "two words, as these are easier to scan.' Note the style page contradicts this — "
             "'should not exceed three words'.", "same", None),
            ("Not for", "Filtering the same content, or linear steps",
             "Carbon: use a content switcher for filtering, a progress indicator for steps",
             "same", None),
        ],
    ),
    "notification": dict(
        summary="Inline status banner.",
        carbon_src=f"{C}/components/notification/style/",
        spec=[
            ("Left border", "3px in the status colour", "Carbon: border-left 3px $support-*",
             "same", None),
            ("Min height", "48px", "Carbon: 48px ($spacing-09) on inline and callout; the "
             "toast has no min-height, only width 288px", "same", None),
            ("Background", "support-*-subtle core token",
             "Carbon: $notification-*-background-color component tokens", "changed",
             "Promoted to a core token — see support-*-subtle."),
            ("Title", "heading-compact, no full stop",
             "Carbon: $heading-compact-01, plus two separate rules — 'The title should be short "
             "and descriptive, explaining the most important piece of information.' and "
             "'Don\'t use a period to end a title.'", "same", None),
            ("Body", "body-sm, one or two sentences, max two lines",
             "Carbon: identical rule", "same", None),
            ("Icon", "Required, per status",
             "Carbon: a filled status icon per status (information / checkmark / warning / error "
             "filled) with no opt-out in the React implementation — but Carbon never writes "
             "'required' and never states a rationale. Its nearest statement is 'Each status is "
             "associated with a specific color and icon, ensuring a consistent and universal "
             "user experience'.",
             "same", "Value adopted; the 'don't rely on colour alone' justification is Strata's, "
                     "not a Carbon quote."),
            ("Dismissal", "Inline notifications persist until dismissed",
             "Carbon: identical rule; toasts may auto-dismiss after 5s", "same", None),
        ],
    ),
    "tag": dict(
        summary="Read-only, dismissible and selectable tags.",
        carbon_src=f"{C}/components/tag/style/",
        spec=[
            ("Heights", "sm 20 / md 24 / lg 32", "Carbon: sm 18 / md 24 / lg 32", "changed",
             "18px is below the 20px minimum where a 12px label still has breathing room."),
            ("Radius", "md (6px) — the dot-chip", "Carbon: 16px at every size — one of only four radii "
             "Carbon publishes on a component page (Tag 16px, Content switcher 4px, Code "
             "snippet 2px, Popover 2px), against 22 component SCSS files that set one", "changed",
             "[encode 2026-08-20, E-09] The tag is the dot-chip: neutral bordered chip on "
             "layer-01, a 7px hue dot (grade 60 light / 40 dark) or icon in its place, and the "
             "WORD carrying the meaning. Tinted pills retired; hue modifier class names kept. "
             "The one element the appearance axes never vary."),
            ("Type", "label", "Carbon: $label-01", "changed",
             "The T1 caps label (12/500/.4px). Chip text stays sentence-case via the component."),
            ("Group limit", "Six per row, wrapping to at most five lines",
             "Carbon (selectable tags in groups only): 'Keep groups of tags horizontally on one "
             "line when there are six tags or less.' and 'If the number of tags exceeds five "
             "lines of wrapping, consider using a different component for your use case, like a "
             "multi-select dropdown.' — a threshold and a soft 'consider', not a hard per-row cap.",
             "changed", "Applied to all tag variants rather than selectable groups only, and "
                        "treated as a limit rather than a suggestion."),
            ("Not for", "Navigation",
             "Carbon: 'Do not use tags as links that direct you to an entirely different page or "
             "launch you from a current experience to a separate tab'", "same", None),
        ],
    ),
    "tile": dict(
        summary="Base, clickable and selectable tiles.",
        carbon_src=f"{C}/components/tile/style/",
        spec=[
            ("Min size", "64px tall, 128px wide", "Carbon: min-height 64px, min-width 128px",
             "same", None),
            ("Padding", "16px", "Carbon: 16px ($spacing-05)", "same", None),
            ("Surface", "layer-02 (white) with a 1px border-subtle-00 whisper hairline, radius-xl (10px)",
             "Carbon: $layer, and NO border row at all on the base tile — its colour table has "
             "exactly two rows, background and text. Clickable, selectable and expandable tiles "
             "do get $border-tile, but the style page labels it 'Border (feature flag)' and "
             "_tile.scss gates it behind enable-tile-contrast, so it is off by default.",
             "changed",
             "Border on all variants, unconditionally. A White-theme tile on layer-02 is "
             "otherwise invisible — which is presumably why the contrast feature flag exists at "
             "all. Strata takes the flagged behaviour as the default."),
            ("Elevation", "elevation-01 (whisper) at rest; elevation-02 on a clickable tile's hover — [encode E-10]",
             "Carbon: 'Tiles reside on the same plane as the page background layer and do not "
             "have elevation.' and 'Do not add a drop shadow to tiles and use them to reveal "
             "secondary information, actions, or notifications.' Carbon's own AI tile variant "
             "is an exception — it ships $ai-drop-shadow and $ai-inner-shadow.", "changed",
             "Carbon's no-shadow rule is right at rest and is kept. A hover lift on a "
             "clickable tile is a state change, not decoration, and it is the cheapest way "
             "to distinguish a clickable tile from a base one before the pointer commits."),
            ("Radius", "8px (radius-lg)", "Carbon: not published; _tile.scss sets a radius only "
             "on the AI decorator variants, never on base, clickable or selectable",
             "changed", "See the radius scale."),
            ("Mixing", "Do not mix tile variants within one group",
             "Carbon: 'Do match the tile variants in groups.' / 'Do not mix different variants "
             "of tiles in groups.'", "same", None),
        ],
    ),
}
