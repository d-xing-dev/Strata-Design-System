# Strata — v0.3

A design system extracted from **IBM Carbon**, justified line by line against the official
Carbon documentation, diverged deliberately toward something lighter, and built to bind to a brand as a config
change. Ships two builds: **`scaffold`** (unbranded) and **`deloitte`**.

> **Visual-language encode, 20 Aug 2026.** The system's expression layer was redesigned and
> re-encoded in one recorded pass: the T1 type ramp (four sizes 12/13.5/15/28, weight-led, eight
> tokens eight classes), the dot-chip tag as the sole tag expression, hairline surfaces at radius
> 6-10, frameless tables with header variants, 40px default density, Plex-first font stacks, and
> a per-product **appearance config** (`data-appearance`: chrome, table-header, shell axes --
> chosen once at binding, never per screen). Every event with its why: **`ENCODE-LEDGER.md`**.
> The intent-indexed usage tier is **`PATTERNS.md`**; fork rules live in **`RESOLUTION-MAP.md`**.
> Where a sentence below and the ledger disagree, the ledger is newer and wins.

*"Strata" is a working name. Pick your own before this goes near a product — it must not
reference "Carbon" or "IBM" (see `LICENCE-AND-ATTRIBUTION.md`).*

> **Brand assumption.** The `deloitte` build assumes you are working for or with Deloitte and are licensed
> to use their palette. Deloitte Green is a registered trademark (USPTO Reg. 5959457, "the mark
> consists of a green dot (Pantone 368)"), and Acorns Grow Inc. separately holds US Reg. 6176921
> over Pantone 368 C *as applied to the background of a software application*. If the assumption
> is wrong, this is not a design question — stop and check.

## Two builds, two fidelity levels

`dist/scaffold/` is **unbranded** and is the render target for **moderate** fidelity — real
spacing, type, states and hierarchy with no design-system commitment. `dist/deloitte/` is the
**high**-fidelity target and is only valid once binding has been confirmed. Scaffold is the
default because a brand should be an explicit act.

What scaffold deliberately cannot show: how it looks on brand, whether the brand palette passes
contrast in context, and any collision a brand creates between roles. A brand-specific role
collision is a high-fidelity finding and must not be assumed absent because moderate looked
fine. The build now refuses a wheel where two roles collapse onto one hue (see *Role
separation* below), but that guard checks hue assignment, not how a specific pair reads in
context.

## Changing brand

The whole brand is one entry in the `BRANDS` block in `build/color.py` — hue angles, chroma
multipliers, a role map saying which ramp carries which semantic job, and any pinned literals
that sit outside the ramps. Everything else derives — semantic tokens reference the *role*, so a
brand swap touches no semantic token at all. Add an entry, run `STRATA_BRAND=<name> python3
build/make.py`, and the palette, both themes, every component, the
312 contrast checks and the documentation all regenerate together. The luminance ladder guarantees
that a hue swap cannot silently break a contrast guarantee; the audit catches the cases where a
*role* assignment breaks one, which is what actually happens.

---

## Open this first

**`dist/scaffold/index.html`** — the living style guide. Every token, every component, both themes,
with the official Carbon value and source URL inline against each one. It is generated from
the same files the components consume, so it cannot drift from what ships.

---

## What's here

```
strata/
├─ dist/
│  ├─ scaffold/       UNBRANDED build — the moderate-fidelity render target (default)
│  │  ├─ index.html   living style guide (open this)
│  │  ├─ tokens.json  the source of record — DTCG-shaped, every token carries provenance
│  │  └─ strata.css   primitives + light/dark semantic layer + every component
│  └─ deloitte/       BRANDED build — the high-fidelity target, once binding is confirmed
├─ RESOLUTION-MAP.md  semantic pattern → Strata component, fork rules, plus the one gap
├─ PATTERNS.md        the intent tier — when to use / when not, GOV.UK-shaped
├─ ENCODE-LEDGER.md   the 20 Aug 2026 visual-language encode, event by event
├─ build/
│  ├─ color.py        palette generator: OKLCH solver + WCAG contrast maths, no deps
│  ├─ tokens.py       the token source of truth, with Carbon provenance per entry
│  ├─ build.py        emits tokens.json and strata.css; runs the contrast audit
│  ├─ guide.py        renders the documentation tables from the same data
│  ├─ icons.py        the shipping `st-i-*` sprite; emits dist/<brand>/strata-icons.svg
│  ├─ snapshot.py     emits dist/skill-snapshot/ — the flattened copy the UX skill ships
│  ├─ snapshot/       the one authored file that copy needs (its own README)
│  └─ make.py         `python3 build/make.py` rebuilds everything
├─ LICENCE-AND-ATTRIBUTION.md
└─ NOTICE
```

Rebuild: `cd build && python3 make.py` (scaffold, the default) or
`STRATA_BRAND=deloitte python3 make.py`. No dependencies beyond the Python standard library.
The build asserts on any failing contrast check, so a token edit that breaks an accessibility
guarantee fails rather than shipping.

**Run both brands.** `dist/skill-snapshot/` — the flattened copy that ships inside the
`raise-design-fidelity` UX skill — needs every brand's CSS, so it is emitted on the run that
completes the set and skipped with a named reason otherwise. `python3 build/snapshot.py --check`
verifies it against its sources and exits non-zero on any drift. It exists because that copy was
assembled by hand for a fortnight and accumulated three invisible defects: a `usage.md` teaching
twelve type tokens against a CSS defining eight, a superseded licence position, and a
"stylesheet" that was actually the hand-authored encode target spec, differing from the real
build in the hairline token. `build/snapshot.py`'s docstring has the full account.

---

## The four architectural decisions

**1. Tokens are the deliverable, not the CSS.** `tokens.json` is the artefact of record;
CSS, component styles and the style guide are generated from it. Carbon shows exactly why
this matters — its published token table prints `$button-primary-hover` as `#0353e9` while the
shipped SCSS resolves to `#0050e6`, and `@carbon/themes` disagrees with *itself* at the same
version, its JS build exporting `#0353e9`. It prints `$text-placeholder` as Gray 40 while the code
ships `rgba(22,22,22,0.4)`. The date picker page publishes a shadow at 20% alpha while the code
ships 30%. `_dropdown.scss` ships 42px right padding against a published 48px. Four artefacts,
four answers.

**2. A living style guide, not a spec document.** A written spec cannot show you that a
warning icon has 2.8:1 against its own background. This one renders every component from the
shipped CSS and recomputes 312 contrast pairs at build time — with alpha tokens genuinely
composited, which is what surfaced three failures that the eye and the approximation both missed.
It also passes axe-core with 0 violations in both themes.

**3. Framework-agnostic CSS custom properties.** No React dependency in the base. Mirrors
Carbon's own `@carbon/colors` / `@carbon/type` / `@carbon/layout` split, which is why Carbon
survived its own v10→v11 migration.

**4. The semantic tier is the contract.** Components reference `--st-layer-01`, never
`--st-neutral-10`. That one rule makes light/dark a data change and lets the whole palette be
re-hued without touching a component file.

---

## Adopted from Carbon unchanged

The spacing scale, all 13 steps (multiples of 2, 4 and 8 — note the 8px mini unit is a 2x Grid
concept, not the spacing scale's basis). The 16-column 2x Grid and its five breakpoints.
The productive motion curves and durations. The layering model, including the off-by-one field
rule (a field on `layer-02` uses `field-03`; borders pair with their own number). The two-tone
focus ring drawn inset at `outline-offset: -2px`. The `group-role-state-index` token grammar.
The interaction-state arithmetic — hover is a half step, selected one, active two. Warning does
not recolour a field border. Placeholder never replaces a label. Tags are not navigation.
Toggles are only for instantly-applied settings. Data table row heights. Notification anatomy.
Tab selected-state weight change.

## The main divergences

| | Carbon | Strata | Because |
|---|---|---|---|
| Corner radius | No scale, no token, no published rationale — four values documented across 22 SCSS files that set one | Explicit 0→10px scale: chips 6, controls 8, surfaces 10 | "Carbon is square" is folklore, not a published rule. Re-cut 20 Aug 2026 (E-01) to the unified hairline stance. |
| Field border | Bottom edge only | Full 1px border — hairline at rest, strong on hover/focus (E-08) | The boundary stays full (Carbon's underline-only was not adopted); its rest weight is a recorded trade with `.st-field--strong` one class away. |
| Button padding | 16px left, **64px right** — but only on a button with no icon | 16px symmetric, label centred | Carbon is already symmetric in four of five cases. It publishes a rationale for the 16, none for the 64, and needs a separate left-align rule to cope with the result. |
| Default body | 14px | 13.5px (was 16px; reversed 20 Aug 2026, E-02) | The T1 working-density body — the 16px argument lost to how the language actually reads on dense product screens. |
| Default control | 40px | 40px (was 48px; re-cut 20 Aug 2026, E-05) | Back to Carbon's default; the 44px floor holds for bare-icon controls via `.st-icon-btn`, and `lg` is one declaration away for touch-first products. |
| Palette | Hand-authored per hue; contrast is a lookup table | Grades pinned to fixed luminance; contrast is a rule | A hue swap can never silently break a guarantee. |
| Chroma peak | ~0.25 OKLCH (Blue 60 `#0f62fe`) | ~0.166 | Lower saturation, plus trade-dress distance from IBM Blue. |
| `text-placeholder` | Fails 4.5:1 in both of its two conflicting official values (2.53:1 and 2.16:1) | 4.62:1 on `field-01` | Placeholder is text. WCAG 1.4.3 applies. |
| `support-warning` | Yellow 30 held constant across all four themes; ~1.6:1 on white | Resolves per theme; 4.6:1 on its own surface | The status that most needs to be noticed was the one that disappeared. |
| `support-info` | Blue — the same family as *Carbon's* primary action | Deloitte Blue 7690 | With a green primary, blue is free. This divergence reversed itself on rebrand — it was contingent on the brand, not on Carbon being wrong. |
| Modal width | % of grid per breakpoint | Fixed max-widths, viewport-capped | Percentage widths let dialog copy run to 90+ characters on a wide monitor. |
| Modal buttons | 50% each, full-bleed | Right-aligned, natural width | Full-bleed makes Cancel exactly as heavy as the primary action. |
| Date field type | `$code-02` (mono) | `body-md` + `tabular-nums` | The only Carbon field set in mono, with no published reason. |
| `prefers-reduced-motion` | Advisory prose only; implemented per-component in 12 SCSS files; no token, no requirement | One global rule | Coverage that depends on someone remembering is partial by construction. |
| Elevation | One shadow, pure black | Three levels, two-layer, hue-tinted | Carbon already had to hardcode a second shadow for Popover. |

The full ledger — roughly 60 decisions adopted, 40 diverged, each with its argument — is the
last section of `dist/index.html`.

---

## What's deliberately not here yet

- **Fluid typography.** Carbon's eleven fluid tokens interpolating across five breakpoints is a
  large surface for a base layer, and Carbon itself concedes the productive/expressive split
  "is no longer neatly divided". Add it when a marketing surface needs it.
- **The remaining ~27 Carbon components.** This is foundations plus 13 core components, per scope.
- **Framework bindings.** The CSS is deliberately framework-free; React/Vue/Web Component
  wrappers sit on top without forking values.
- **Icon set.** The guide uses eleven inline SVGs as placeholders. Carbon's construction rules
  (32px grid, 2px padding, 2px stroke, 2px radius, 45°/15° angles) are adopted and documented in
  the guide. `@carbon/icons` itself is 2,734 icons under Apache-2.0 and can be taken directly —
  filter out the several hundred `logo--*` / `ibm-*` marks first, since the licence covers the
  files but not the trademarks they depict.
- **An `alpha` / opacity scale**, a **z-index scale**, and **focus-order documentation**
  (Carbon has no central composite-widget keyboard spec — it is per-component, and consolidating
  it is a real piece of work).

## Verification status — closed out

Every Carbon citation in this system was extracted from official sources. **All of them have now
been independently re-checked** against the repos at HEAD (raw MDX, shipped SCSS, published npm
tarballs) — 28 foundation-level claims plus roughly 90 component spec rows. Nothing in the
"still to check" list remains open.

**Result: 27 corrections applied.** The pattern is worth noting — none were fabrications, all were
overstatements, truncated quotes, or paraphrases presented as quotes. That is the failure mode to
watch for in a system like this, because each one reads as authoritative.

### Corrections, by kind

**Paraphrase presented as a verbatim quote (8).** Select's "fewer than three options" rule, the
toggle's "applies changes instantly" line (which does not exist in Carbon at all — the real
sentences are "Ideal for settings or preferences that can be immediately applied" and the
checkbox-plus-button alternative), the button left-align caption, the date picker's placeholder-
format warning, the data table's column-header rule, the tabs label rule, the notification title
rule (two separate bullets compressed into one), and the tag "not for navigation" rule. All now
carry Carbon's exact sentences.

**Claim was true but too broad (9).**
- Button padding is 16/64 only on a button with *no icon*; buttons with icons, icon-only buttons
  and all ghost buttons are already 16/16. Strata changes one case, not five.
- "Carbon gives no rationale for the padding" — it gives one for the 16 (nothing within 16px of a
  border), just not the 64.
- Checkbox focus inset is documented on two component pages, not one (button is the other).
- Tag is one of four components publishing a radius, against 22 SCSS files that set one — not the
  only one.
- Carbon *does* publish a dropdown scroll threshold ("start a scroll at the sixth option", shipped
  as 220px). Strata's 320px is that rule restated at a 48px row height, not a value Carbon lacks.
- Carbon *does* give advisory reduced-motion prose and implements the media query in 12 component
  files; what it lacks is a token and a requirement.
- The 8px mini unit is a 2x Grid concept, not the spacing scale's basis.
- Tile's `$border-tile` sits behind an `enable-tile-contrast` feature flag, off by default.
- Tag's group limit applies to selectable tags only and is a threshold plus a soft "consider", not
  a hard per-row cap.

**Wrong value (4).**
- Tabs' resting underline is **2px** `$border-subtle`, not an unstated width — so Strata's 1px is a
  change, and is now recorded as one with its reasoning.
- Modal widths are percentages **of the browser viewport**, not of the grid.
- The date picker's raw `rgba(0,0,0,0.2)` shadow *is* tokenised in shipped code, at 30% not 20% —
  the docs and the code disagree, which is a different (and more interesting) defect than the one
  originally claimed.
- Button focus is a 1px border plus two inset shadows, not a 2px border.

**Numbers restated correctly (3).** `$text-placeholder` measures 2.53:1 composited and 2.16:1 as
Gray 40, not the ~2.35/2.32 first stated. Button has seven documented sizes across two variants.
`@carbon/icons` ships 2,734 icons.

**Findings that came back worse than claimed (3).** `@carbon/themes` contradicts *itself* at the
same version — its JS build exports `$button-primary-hover` as `#0353e9` while its SCSS build ships
`#0050e6`. `_dropdown.scss` ships 42px right padding against a published 48px. `$code-02` appears
exactly once across Carbon's entire component documentation set, and `$link-01` exactly once — both
on the date picker page.

### The four open source-availability questions, now answered

| Was | Now |
|---|---|
| "Date picker Do/Don't may exist as image captions" | **Verified absent.** The raw MDX contains zero `DoDont` / `DoDontRow` components and four purely descriptive `<Caption>` elements. Sibling pages (tag, tile) do contain them, so this is a real gap, not a converter artefact. The date picker's prescriptive guidance is all prose. |
| "Icon library count and licence not retrievable" | **2,734 icons** (2,711 non-deprecated), **Apache-2.0**, no icon-specific restriction. Caveat: several hundred `logo--*` / `ibm-*` marks are in the set — the files are licensed, the marks are not. |
| "Aspect-ratio class names not retrievable" | **Nine classes**, `.cds--aspect-ratio--{W}x{H}` plus a required base class, exposed as the overridable `$aspect-ratios` variable. The file is under `scss/components/`, not `scss/utilities/`, which is why it was not found. The docs publish six ratios; the code makes the three portrait inversions explicit. |
| "Figma kit licensing unverified" | **CC BY 4.0**, stated on the Figma Community file pages, matching Figma's platform default for free files. A derivative *can* be republished with attribution and a statement of changes. See `LICENCE-AND-ATTRIBUTION.md` §5 — including the trap that Figma's Community Free Resource License governs plugins, not files. |

### Audit and rendering, now closed

**Contrast audit — the approximation is gone.** Alpha tokens were previously checked against their
base colour rather than the composite, which over-reported contrast for every alpha token in the
system. The build now does a real source-over composite, and the coverage went from 66 hand-listed
pairs to **168** (now **312**, after the 20 Aug 2026 encode added the dot-chip and
appearance-axis pairs) including the tag palette and every button state. That immediately surfaced **three
failures that had been invisible**: a dark-theme placeholder at 3.48:1, a dark secondary button
label at 3.04:1, and a dark toggle handle at 2.16:1. All three are fixed, and all three exist in
Carbon at the corresponding tokens. Checks are now split — **142 enforced** (a failure aborts the
build) and 26 advisory (disabled states, which WCAG explicitly exempts, and decorative boundaries
not required to identify a component; 14 of those sit below their advisory target, which is
correct — a table row divider that hit 3:1 would be a worse table).

**axe-core: 0 violations**, both themes, whole document including every live demo. Getting there
caught a real bug: the calendar's out-of-month days were using `--st-text-disabled` at 1.83:1.
They are selectable, so the exemption does not apply — Carbon specifies `$text-secondary` there
and had it right where this build had it wrong.

**Forced-colors / Windows High Contrast Mode added.** Carbon handles `prefers-contrast` and never
addresses `forced-colors`, where the OS strips every background. Without handling, all five button
variants collapse into one identical box and selected rows, status tags and toggle tracks vanish.
Strata now restates each in a channel HCM preserves — system-colour borders, the
`Highlight`/`HighlightText` pair for the primary action, a doubled border for danger, `GrayText`
for disabled, `Highlight` outlines on selection. Verified under emulation.

**Cross-browser — partially closed, honestly.** Chromium 141 at 1× and 2×, light and dark, plus
emulated `forced-colors`, `prefers-contrast: more` and `prefers-reduced-motion: reduce` (verified
to actually collapse transitions to 1ms). **Safari and Firefox were not executable in this
environment.** In place of running them, the stylesheet's feature surface was audited by hand:
nothing in `strata.css` requires anything newer than Safari 15.4 / Firefox 85, `appearance` now
carries its `-webkit-` prefix, and the only two modern features used anywhere (`color-mix()` and
`backdrop-filter`) appear solely in the style guide's own chrome, behind an `@supports` guard with
a solid fallback. That is a reasoned argument, not a test — **run it in Safari before you ship.**

### The one thing that genuinely cannot be closed here

A screen-reader pass. No JAWS, NVDA or VoiceOver in this environment. axe-core catches structural
and contrast problems but says nothing about whether the experience *announces* sensibly. Carbon's
own definition of done requires manual testing in all three, and that bar has not been met here.

## The Deloitte brand pass — what changed and why

| | Before | After | Reasoning |
|---|---|---|---|
| **Primary action** | Generic blue, grade 60 | **Deloitte Green 349 `#046A38`**, `green.70` | Grade 70 reproduces it to ΔRGB 5. Grade 70 not 60 because the brand's green *is* a 7:1 colour, and it leaves 80/90 free for hover and active. |
| **Deloitte Green `#86BC25`** | — | **Pinned, outside the ramps** | 2.27:1 against white. It cannot carry text, an icon, or a control boundary under the WCAG AA that Deloitte's own accessibility statement commits to. It is a mark colour. |
| **Neutrals** | hue 255.0° | hue **255.5°** (Cool Gray 10/11) | Effectively a no-op. `--st-neutral-70` was `#55595d` against Cool Gray 11's `#53565A` — ΔRGB 4. The brief was already satisfied; the config now says so. |
| **Dark-theme primary** | grade 60 both themes | `green.70` light / **`green.60` dark** | A grade-70 fill on a grade-100 page is 2.45:1 — it barely reads as a surface, and the near-black focus-inset ring inside it fell to 2.46:1. A blue primary never hits this because Carbon's Blue 60 stays dark in both themes. |
| **`support-info`** | Teal | **Deloitte Blue 7690** (ΔRGB 3) | Reversal — see above. |
| **`support-error`** | generic red hue 25° | Deloitte Red 485, hue **29.6°** (ΔRGB 13) | — |
| **`support-warning`** | generic amber hue 78° | Deloitte Orange 144, hue **63.1°** (ΔRGB 45) | The largest error in the brand mapping. Deloitte Orange is more chromatic than the ladder's ceiling allows at that luminance. Acceptable for a status fill; pin it literally if it matters. |
| **`link-visited`** | Purple | Purple, **flagged off-brand** | The one deliberately non-Deloitte token. Every Deloitte hue is spoken for; substituting one would make "visited" collide with a live signal. Drop visited styling if that trade is unacceptable. |
| **Tertiary button hover** | filled with `link-primary` | filled with `button-primary` | A real bug the rebrand exposed: `link-primary` is grade 40 in dark — a *light* green — so filling with it and keeping a white label gave 2.1:1. |

### The one decision worth arguing about

**This was got wrong once, and the correction is worth reading before touching a brand.**

The original call was that a green brand puts primary and success one grade apart in the same
hue (`green.70` and `green.60`), and that form separation resolved it — success only ever
renders as a toggle track, a status icon or a 3px banner rule, never as a filled action-shaped
surface, and every status carries an icon under the never-colour-alone rule. Moving success to
teal was rejected as breaking *green = good* to solve a problem the form language already
handled.

That reasoning had a hole in it. Semantic tokens reference **roles**, so `focus` was
`primary.60` and `support-success` was `success.60` — and when primary and success both resolve
to `green`, those are not adjacent values, they are **the same expression**. The role
indirection collapsed silently. Form separation cannot rescue a focus ring, because a focus
ring renders transiently on top of every other role and has no form of its own.

Field evidence confirmed it: an engagement taking a product to high fidelity measured
`--st-focus` and `--st-support-success` as one literal and reported three surfaces where a green
block could mean *do this* or *this worked*. It was not a contrast failure — every pair passes
AA — it was a **role identification** failure, which no contrast audit can see.

The wheel now separates by hue:

| Role | Hue | Light |
|---|---|---|
| `primary` | Deloitte Green 349 | `#076636` |
| `success` | Deloitte Teal 7714 | `#0b7b85` |
| `info` | Deloitte Blue 7690 | `#0377a9` |
| `focus` | indigo — deliberately no role, no brand | `#775ec4` |
| `visited` | magenta | `#9b2c67` |
| `warning` | Deloitte Orange 144 | `#a35f0a` |
| `danger` | Deloitte Red 485 | `#d23123` |

Minimum separation across every checked pair went from 0.0° to 31.7°, and the rebuild is
contrast-identical: 170 checks at the time, 0 AA failures, 14 advisory (the suite has since grown to 312). The fix was free.

Teal success is mildly unconventional. That is the price, and it is a much smaller one than
*"is this green thing a button or a confirmation"* on three surfaces of a live product.

**`focus` is now its own role and should stay that way.** A focus ring is a system affordance,
not a brand expression and not a status. Binding it to the primary hue is what created the
collapse.

### The guard

`check_role_separation()` in `build/color.py` runs before anything else and **fails the build**
on a role wheel that cannot be read. The rule is asymmetric on purpose:

- Two **status** roles may never share a hue. Confusing success with danger is the most
  expensive misread in any interface.
- An **action** role may never share a hue with a status role.
- Two **action** roles *may* share a hue — a primary button and a focus ring in the same family
  is conventional and reads correctly, because both mean "interactive". Scaffold does exactly
  this.
- Anything closer than 20° fails even without sharing a ramp.

This is the same philosophy as the contrast audit. A class of bug that surfaces in front of a
client six weeks downstream should be caught by the build, and any future brand with a green or
blue identity walks straight into it.

### What a computed palette cannot promise

Deloitte's green ramp **is not one hue** — it swings from 109° at the light end to 153° at the
dark end. It is a Pantone set, not a computed ramp. A single-hue luminance ladder can hit one end
or the other, not both. Anchoring on the dark end (the interactive colour) is the right trade
because that is the end that has to carry text and pass contrast; the light end is carried as a
pinned literal. The Brand section of the guide reports ΔRGB for every official Deloitte value so
this is auditable rather than asserted — 4 of 12 land within ΔRGB 10, 2 more within 25, and the
rest are honestly labelled *not reproduced*.

## Suggested next steps

1. Rename the system. The palette is already Deloitte's.
2. Review the divergence ledger and reverse anything you disagree with. Each is one edit
   in `build/tokens.py`.
3. ~~Decide the typeface.~~ Decided 20 Aug 2026 (E-03): stacks are Plex-first with Inter
   fallback; no font files ship yet. If you ever bundle the files, ship their `LICENSE.txt`
   beside them and never relicense — `LICENCE-AND-ATTRIBUTION.md` §2 has the constraints.
4. Extend the contrast audit list in `build/build.py` (`AUDIT_PAIRS`) as you add components.
