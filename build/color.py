"""
Strata palette generator.

Method (and why it diverges from Carbon):

Carbon's IBM Design Language palette is hand-authored per hue. Its ten grades are
perceptually even *within* a hue but NOT luminance-matched *across* hues -- which is
why Carbon has to publish a "minimum number of steps apart for ratio R" lookup table
(https://carbondesignsystem.com/elements/color/overview/) instead of a rule.

Strata instead pins every grade to a fixed sRGB relative luminance, identical across
all hues, and solves for OKLCH lightness to hit it. Consequences:
  * Grade N has the same contrast behaviour in every hue. The step table becomes exact.
  * Swapping a hue can never silently break a contrast guarantee.
  * Chroma is capped well below Carbon's (Carbon Blue 60 #0f62fe is OKLCH C~0.25);
    Strata caps at C=0.13 at grade 60. This is the "lighter / less industrial" ask
    expressed numerically rather than by taste.

No third-party deps: sRGB <-> OKLab conversions are implemented inline.
"""

from __future__ import annotations
import math

# ---------------------------------------------------------------------------
# sRGB <-> linear <-> OKLab
# ---------------------------------------------------------------------------


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def oklch_to_linear_rgb(L: float, C: float, h_deg: float):
    h = math.radians(h_deg)
    a, b = C * math.cos(h), C * math.sin(h)

    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l, m, s = l_**3, m_**3, s_**3

    return (
        +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def in_gamut(rgb_lin, eps: float = 1e-4) -> bool:
    return all(-eps <= c <= 1 + eps for c in rgb_lin)


def relative_luminance(rgb_lin) -> float:
    """WCAG 2.x relative luminance. Input is already linear-light sRGB."""
    r, g, b = (min(max(c, 0.0), 1.0) for c in rgb_lin)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def to_hex(rgb_lin) -> str:
    out = []
    for c in rgb_lin:
        v = _linear_to_srgb(min(max(c, 0.0), 1.0))
        out.append(max(0, min(255, round(v * 255))))
    return "#{:02x}{:02x}{:02x}".format(*out)


def hex_to_luminance(hex_str: str) -> float:
    h = hex_str.lstrip("#")
    lin = [_srgb_to_linear(int(h[i : i + 2], 16) / 255) for i in (0, 2, 4)]
    return relative_luminance(lin)


def contrast(hex_a: str, hex_b: str) -> float:
    la, lb = hex_to_luminance(hex_a), hex_to_luminance(hex_b)
    lo, hi = sorted((la, lb))
    return round((hi + 0.05) / (lo + 0.05), 2)


# ---------------------------------------------------------------------------
# The luminance ladder
# ---------------------------------------------------------------------------
# Y is sRGB relative luminance. Chosen so that contrast against pure white is a
# round, memorable number at every grade. Contrast vs white == 1.05 / (Y + 0.05).
#
#   grade   target vs #ffffff        what it buys us
#   10      1.08 : 1                 page tint / subtlest layer
#   20      1.28 : 1                 accent surfaces, zebra rows
#   30      1.62 : 1                 disabled borders
#   40      2.15 : 1                 dark-theme text/accents
#   50      3.05 : 1                 >=3:1 non-text on white  (AA 1.4.11)
#   60      5.00 : 1                 >=4.5:1 body text on white (AA 1.4.3)
#   70      7.10 : 1                 >=4.5:1 on grade-20 surfaces
#   80     10.60 : 1                 inverse surfaces
#   90     14.20 : 1                 dark-theme layer
#   100    17.40 : 1                 dark-theme page background
LUMINANCE_LADDER = {
    10: 0.9222,
    20: 0.7703,
    30: 0.5981,
    40: 0.4384,
    50: 0.2943,
    60: 0.1600,
    70: 0.0979,
    80: 0.0491,
    90: 0.0239,
    100: 0.0103,
}

# Chroma ceiling per grade. Peaks at 60 (the action grade) and tapers to the ends
# so grade 10 reads as a tinted neutral rather than a pastel.
CHROMA_LADDER = {
    10: 0.022,
    20: 0.050,
    30: 0.080,
    40: 0.110,
    50: 0.142,
    60: 0.166,
    70: 0.150,
    80: 0.120,
    90: 0.080,
    100: 0.048,
}

# ---------------------------------------------------------------------------
# BRANDS
# ---------------------------------------------------------------------------
# A brand is four things: hue angles, chroma multipliers, a role map saying which
# ramp carries which semantic job, and any pinned literals that sit outside the
# ramps. Everything else in the system derives.
#
# Select with the STRATA_BRAND environment variable. Default is `scaffold`,
# deliberately -- an unbranded build is the safe default, and a brand should be an
# explicit act.
#
#   scaffold   Unbranded. The MODERATE-fidelity render target. Real spacing, real
#              type, real states, real hierarchy -- and no brand commitment. Exists
#              because raising visual finish must not smuggle in a design-system
#              binding that hasn't been decided yet.
#
#   deloitte   Deloitte. Green 349 #046A38 primary (grade 70 reproduces it to
#              delta-RGB 5), Cool Gray neutrals at 255.5 deg. The HIGH-fidelity
#              target once binding is confirmed.

BRANDS = {
    "scaffold": {
        "hues": {
            # Flatter neutral than a branded build -- a tint reads as a choice, and
            # scaffold should not appear to have made any.
            "neutral": (255.5, 0.030),
            # Interactive accent. Blue at reduced chroma: conventional enough to read
            # as "clickable" without reading as anyone's brand.
            "blue":    (250.0, 0.70),
            "green":   (150.0, 0.85),   # success
            "amber":   (75.0,  0.90),   # warning
            "red":     (28.0,  1.00),   # error -- full chroma, a hesitant error is a bug
            "teal":    (205.0, 0.80),   # info
            "indigo":  (292.0, 0.80),   # visited / categorical
            "orange":  (48.0,  0.85),   # categorical
            "magenta": (352.0, 0.85),   # categorical
        },
        # focus shares the primary hue here, which is legitimate: focus is an action
        # affordance, not a status. The rule the guard enforces is that no action role
        # may share a hue with a *status* role.
        "roles": {"primary": "blue", "focus": "blue", "info": "teal", "success": "green",
                  "warning": "amber", "danger": "red", "visited": "indigo"},
        "pinned": {},
        "anchors": [],
    },

    "deloitte": {
        "hues": {
            "neutral": (255.5, 0.055),   # Deloitte Cool Gray 10/11
            "green":   (153.6, 1.10),    # PRIMARY. Deloitte Green 349 #046A38
            "teal":    (205.1, 0.90),    # categorical. Deloitte Teal 7714
            "blue":    (236.8, 0.95),    # informational. Deloitte Blue 7690
            "indigo":  (292.0, 0.92),    # categorical only -- not a Deloitte colour
            "amber":   (63.1, 1.00),     # warning. Deloitte Orange 144
            "orange":  (48.0, 1.00),     # categorical
            "red":     (29.6, 1.20),     # danger. Deloitte Red 485
            "magenta": (352.0, 1.05),    # categorical only -- not a Deloitte colour
        },
        # A green brand cannot also carry green success. When primary and success
        # resolved to the same hue, `focus` (primary.60) and `support-success`
        # (success.60) became the *same token expression* -- the role indirection
        # collapsed silently. Success moves to Deloitte Teal 7714, focus off the
        # action hue entirely, visited to magenta to keep indigo free for focus.
        "roles": {"primary": "green", "focus": "indigo", "info": "blue", "success": "teal",
                  "warning": "amber", "danger": "red", "visited": "magenta"},
        # Deloitte Green #86BC25 cannot be reproduced by a single-hue ramp: it sits at
        # OKLCH hue 128.3 while the dark green sits at 153.6. Deloitte's green ramp
        # swings ~45 degrees light-to-dark -- a Pantone set, not a computed ramp. It is
        # also 2.27:1 against white, so it can never carry text, an icon, or a control
        # boundary. Mark use only.
        "pinned": {"brand-green": "#86BC25"},
        "anchors": [
            ("Deloitte Green", "#86BC25", "Pantone 368",  "mark only -- 2.27:1, cannot carry text"),
            ("Green 361",      "#43B02A", "Pantone 361",  "off-ramp, same hue-swing reason as #86BC25"),
            ("Green 347",      "#009A44", "Pantone 347",  "success -- nearest grade is 60, delta 29"),
            ("Green 349",      "#046A38", "Pantone 349",  "PRIMARY ACTION"),
            ("Green 350",      "#2C5234", "Pantone 350",  "muted dark green -- genuinely off-ramp, "
                                                          "chroma 0.067 where the ladder carries 0.12 "
                                                          "at that luminance; use literally if needed"),
            ("Cool Gray 10",   "#63666A", "Cool Gray 10", "secondary text, borders"),
            ("Cool Gray 11",   "#53565A", "Cool Gray 11", "Deloitte dark grey"),
            ("Blue 7690",      "#0076A8", "Pantone 7690", "informational"),
            ("Blue 7692",      "#005587", "Pantone 7692", "informational, dark"),
            ("Teal 7714",      "#007680", "Pantone 7714", "categorical"),
            ("Red 485",        "#DA291C", "Pantone 485",  "error / danger"),
            ("Orange 144",     "#ED8B00", "Pantone 144",  "warning"),
        ],
    },
}

import os
ACTIVE_BRAND = os.environ.get("STRATA_BRAND", "scaffold")
assert ACTIVE_BRAND in BRANDS, f"unknown brand {ACTIVE_BRAND!r}; have {list(BRANDS)}"

_B = BRANDS[ACTIVE_BRAND]
HUES = _B["hues"]
ROLES = _B["roles"]
PINNED = _B["pinned"]
BRAND_ANCHORS = _B["anchors"]

GRADES = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]


def solve_grade(hue_deg: float, chroma: float, target_Y: float):
    """Binary-search OKLCH L for the target luminance; reduce C until in gamut."""
    c = chroma
    for _ in range(64):
        lo, hi = 0.0, 1.0
        rgb = None
        for _ in range(60):
            mid = (lo + hi) / 2
            rgb = oklch_to_linear_rgb(mid, c, hue_deg)
            if relative_luminance(rgb) < target_Y:
                lo = mid
            else:
                hi = mid
        if in_gamut(rgb):
            return rgb, c
        c *= 0.97
    return rgb, c


def build_palette():
    palette = {}
    for name, (hue, cmul) in HUES.items():
        ramp = {}
        for g in GRADES:
            rgb, _ = solve_grade(hue, CHROMA_LADDER[g] * cmul, LUMINANCE_LADDER[g])
            ramp[g] = to_hex(rgb)
        palette[name] = ramp
    palette["white"] = {0: "#ffffff"}
    palette["black"] = {0: "#000000"}
    return palette


def build_hover_spectrum(palette):
    """
    Carbon's interaction rule, ported verbatim as arithmetic:
      hover  = a HALF step (grades 10-60 darker, 70-100 lighter)
      active = TWO full steps
      selected = ONE full step
    Source: https://carbondesignsystem.com/elements/color/overview/  (Interaction states)

    Carbon hand-authored its half-steps into a separate 'hover spectrum' table.
    Because Strata's grades sit on a known luminance ladder, the half-step is
    computable: interpolate the ladder in log-luminance and re-solve. Same rule,
    no second table to maintain.
    """
    hover = {}
    for name, (hue, cmul) in HUES.items():
        ramp = {}
        for g in GRADES:
            nxt = g + 10 if g <= 60 else g - 10
            nxt = max(10, min(100, nxt))
            y1, y2 = LUMINANCE_LADDER[g], LUMINANCE_LADDER[nxt]
            # geometric midpoint -- perceptually centred between the two grades
            y_mid = math.sqrt(y1 * y2)
            rgb, _ = solve_grade(hue, CHROMA_LADDER[g] * cmul, y_mid)
            ramp[g] = to_hex(rgb)
        hover[name] = ramp
    hover["white"] = {0: build_palette()["neutral"][10]}
    return hover


if __name__ == "__main__":
    p = build_palette()
    for name, ramp in p.items():
        if name in ("white", "black"):
            continue
        row = "  ".join(f"{g}:{ramp[g]}" for g in GRADES)
        print(f"{name:9s} {row}")
    print()
    print("contrast checks against #ffffff")
    for g in GRADES:
        print(f"  neutral-{g:<3d} {contrast(p['neutral'][g], '#ffffff'):>6.2f}"
              f"   blue-{g:<3d} {contrast(p['blue'][g], '#ffffff'):>6.2f}"
              f"   amber-{g:<3d} {contrast(p['amber'][g], '#ffffff'):>6.2f}")


# ---------------------------------------------------------------------------
# Role separation guard
# ---------------------------------------------------------------------------
# A design system's roles are only meaningful if a person can tell them apart.
# Contrast auditing cannot catch this: two roles can both pass AA against every
# backdrop and still be indistinguishable from each other.
#
# The failure this exists to prevent is not "similar" -- it is *identical*. When
# Deloitte's primary and success both resolved to `green`, the semantic tokens
# `focus` (primary.60) and `support-success` (success.60) became the same
# expression, so the role indirection silently collapsed and a green block could
# mean "do this" or "this worked". It surfaced only at high fidelity, in front of
# a client, six weeks downstream.
#
# The rule is asymmetric on purpose:
#   * Two STATUS roles may never share a hue. Confusing success with danger is
#     the most expensive misread in any interface.
#   * An ACTION role may never share a hue with a status role, for the same
#     reason at one remove.
#   * Two ACTION roles MAY share a hue. A primary button and a focus ring in the
#     same family is conventional and reads correctly -- both mean "interactive".
ACTION_ROLES = ("primary", "focus", "visited")
STATUS_ROLES = ("success", "warning", "danger", "info")

MIN_ROLE_HUE_SEPARATION = 20.0   # degrees; below this two roles are not tellable apart


def _hue_gap(a: float, b: float) -> float:
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


def check_role_separation(brand: str):
    """Return a list of violations. Empty list means the wheel is legible."""
    b = BRANDS[brand]
    roles, hues = b["roles"], b["hues"]
    problems = []
    checked = set()
    for r1 in ACTION_ROLES + STATUS_ROLES:
        for r2 in ACTION_ROLES + STATUS_ROLES:
            if r1 == r2 or (r2, r1) in checked:
                continue
            checked.add((r1, r2))
            if r1 not in roles or r2 not in roles:
                continue
            # two action roles sharing a hue is allowed
            if r1 in ACTION_ROLES and r2 in ACTION_ROLES:
                continue
            h1, h2 = roles[r1], roles[r2]
            if h1 == h2:
                problems.append(
                    f"{brand}: roles {r1!r} and {r2!r} both resolve to hue {h1!r} -- "
                    f"their semantic tokens are the same expression, not merely similar")
                continue
            gap = _hue_gap(hues[h1][0], hues[h2][0])
            if gap < MIN_ROLE_HUE_SEPARATION:
                problems.append(
                    f"{brand}: roles {r1!r} ({h1}) and {r2!r} ({h2}) are {gap:.1f} deg apart, "
                    f"below the {MIN_ROLE_HUE_SEPARATION:.0f} deg minimum")
    return problems


def role_separation_report(brand: str):
    """Every checked pair and its separation -- for the style guide."""
    b = BRANDS[brand]
    roles, hues = b["roles"], b["hues"]
    rows, checked = [], set()
    for r1 in ACTION_ROLES + STATUS_ROLES:
        for r2 in ACTION_ROLES + STATUS_ROLES:
            if r1 == r2 or (r2, r1) in checked or r1 not in roles or r2 not in roles:
                continue
            checked.add((r1, r2))
            allowed = r1 in ACTION_ROLES and r2 in ACTION_ROLES
            h1, h2 = roles[r1], roles[r2]
            gap = 0.0 if h1 == h2 else _hue_gap(hues[h1][0], hues[h2][0])
            rows.append((r1, h1, r2, h2, gap, allowed))
    return sorted(rows, key=lambda r: r[4])
