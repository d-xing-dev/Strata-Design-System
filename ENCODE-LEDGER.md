# Encode ledger — every recorded change to Strata's expression

**What this is.** Each decision that changed how Strata looks, recorded in the system's own idiom
— src / value / delta / why. It opens with the visual redesign that converged 19–20 Aug 2026
(E-01…E-20, through the direction board, five pages, type study and variations rounds) and
continues with every event raised since. **The ledger is the record of WHY; `build/` is the
truth.**

**Header corrected 23 Aug 2026, and the correction is itself worth recording.** This file used to
say the device bridge was down, that the transcription into `build/` had not happened, and that
"`build/` and this ledger disagree, and this ledger is the newer truth". All three stopped being
true on **21 Aug**, when the encode was executed directly into `build/tokens.py` and
`build/build.py`. It also pointed at `strata-next-scaffold.css` as the result — that file was the
hand-authored encode *target*, and it was deleted as defect D2c precisely because it looked like a
build output and was not one. Leaving the paragraph up for two days is the same defect class the
whole system argues against: **a stale assertion outlives the condition it described, and it stops
anyone looking.**

**Current state:** both brands build clean at **348 contrast checks, 0 AA failing, 14 advisory
below target**, production check 0 findings, `snapshot.py --check` clean.

---

## The events

| # | Event | Delta | Why |
|---|---|---|---|
| E-01 | `radius.xl` changed | 12px → 10px | Unified 6–10 radius stance: chips 6, controls 8, surfaces 10. Tonal Precision structure, Dong's locked pick |
| E-02 | Type scale **replaced** | 12 tokens → 8 (T1 ramp: 12/13.5/15/28, weight-led) | type-system-study; T1 chosen by eye over Carbon's productive ramp on identical pages. Retired classes are gone, not aliased |
| E-03 | Font stacks changed | Inter-first → **IBM Plex Sans / Plex Mono first**, Inter fallback | Locked language. Plex is OFL-1.1: bundle-able; font files (when bundled) carry their own LICENSE.txt; never relicensed Apache-2.0; no fork named "Plex". LICENCE-AND-ATTRIBUTION §2 re-read 20 Aug — the caution survives, the adoption is clean because Strata's palette is not IBM's |
| E-04 | `border-subtle` ramp lightened | subtle-00 #e3e3e4→#ececef, subtle-01 #cacbcd→#e3e3e4 (dark: #3d3f41→#333436, #57585b→#3d3f41) | The whisper hairline is the surface language. border-strong unchanged, stays the fallback |
| E-05 | Density defaults re-cut | control 48→40, row 48→40, pad 16→12 (compact: 32/32/8) | B-language reads premium at working density; 48px controls read as marketing. `.st-icon-btn` keeps the 44px floor |
| E-06 | `elevation-01` re-tuned | two-layer → single whisper `0 1px 2px rgba(16,18,20,.04)` | Resting shadow for hairline surfaces; 02/03 unchanged |
| E-07 | Button re-cut | radius 6→8; tertiary → white fill + `border-interactive-subtle` + wash hover | B buttons in Strata blue. Centred-symmetric label divergence from Carbon **re-affirmed** — gains a second why. The tertiary fill-on-hover dark-theme trap disappears with the fill |
| E-08 | Field re-cut | strong full border → **hairline** (subtle-01) + white fill + whisper shadow, radius 8; hover/focus restore strong/focus border | Knowing trade, recorded: rest-state boundary is decorative-grade (1.28:1, advisory). `.st-field--strong` is the accessible fallback ONE CLASS away. Carbon's underline-only was NOT adopted — the boundary stays full |
| E-09 | Tag **replaced** — dot-chip | tinted pills → neutral bordered chip (layer-01, subtle-01 border, radius 6) + 7px hue dot (grade 60 light / 40 dark) + icon slot (`--icon`) | Dong's locked pick, and **the one element the appearance axes never vary**. Hue modifier class names unchanged — only the expression moved. Never-colour-alone holds: the word carries meaning, the dot is affordance. All 12 dot pairs clear 3:1 by ladder construction |
| E-10 | Tile re-cut | layer-01 + subtle-01 + radius 8 → **white + whisper hairline + radius 10 + elevation-01** | The hairline card. Canvas stays white; separation is the hairline, not tone |
| E-11 | Notification quieted | tinted surface → white card + hairline + 3px semantic rule + coloured icon | The tinted note shouted on every screen. Tint tokens remain in the palette |
| E-12 | Table re-cut + **axis** | frameless: white in whisper wrap (radius 10), hairline rows, **no zebra default**, th 12/600 on accent grey; `th.st-num`/`td.st-num` right-align (P-1). Axis: `table-head-tint` (blue-20/blue-80) and `table-head-strong` (blue-80/white), dark-resolved | Locked language + the coloured-header variation Dong asked for, product-constant via appearance config |
| E-13 | Steps **replaced** | boxed stepper + number circles → **border-top state coding** (2px edge + weight; done=ink, current=interactive, failed=error). `__num` display:none (markup-compatible retirement); `__pos` text stays — it was always the accessible channel | Locked language. `--failed` remains non-optional |
| E-14 | Stat **REVERSAL** | "not a card, no border" → **the stat IS a card** (white, hairline, radius 10, caps label, 28/600 figure) | The no-border rule assumed a tonal canvas doing the separating; on the locked white canvas a bare figure floats. Row-of-panels risk now owned by the composition gap hierarchy |
| E-15 | kv keys wear the caps label | dt: 12 secondary → 12/500/.4px uppercase | Also the separating cue of fork rule R2 (record card vs collection card) |
| E-16 | Explorer rail re-cut | border-left selection → rounded row items, icon slot (16px stroke icons, always sized), selection = blue-10 wash + weight + icon colour | The side-menu variant Dong asked for, from variations V5 |
| E-17 | **Appearance config** added | one `data-appearance` attr on the shell root; space-separated axes: `chrome-coloured` (blue-90 chrome), `table-head-tint` / `table-head-strong`; shell task/explorer and density stay the existing mechanisms. Light chrome default is now WHITE header + hairline | Variation lives BETWEEN products: each axis chosen once, at binding, recorded in the ledger, held on every screen. The dot-chip is deliberately NOT an axis |
| E-18 | **Shaped skeletons** added | `st-skeleton-card` / `st-skeleton-stat` / `st-skeleton-table` (+`__head`/`__row`) + required `st-skeleton__job` slot | Every stage renders at one construction standard, so the undecided-content state is a load-bearing production component: designed-and-empty, never invented, never broken. Never fill a skeleton whose requirement is Open |
| E-19 | **Content link** added | `.st-link` (link-primary, 600, hover underline) | Bare content links took UA colours and failed dark-theme contrast — found by axe on the acceptance render. The audit working as designed |
| P-1..P-4 | Construction-floor rules | `.st-num` alignment on table cells; `.st-tag` nowrap; `.st-nowrap` utility; `[hidden]{display:none !important}` | Each from a verified field defect (the invisible-scrim click blocker is P-4's origin) |
| E-20 | Icons extended | 5 stroke symbols added: `st-i-grid`, `st-i-mail`, `st-i-box`, `st-i-clock`, `st-i-star` (16-grid, 1.4 stroke, matching set) | The explorer rail needs them; drawn to the existing construction rules |
| E-21 | **Default anchor** added | base `a { color: link-primary }` + underline/hover/focus scoped to `a:not([class])` | Raised three times from engagements, and the file argued with itself: one comment claimed an unstyled `<a>` takes `--st-link-primary`, E-19's comment thirty lines later recorded that it took the UA default and failed dark contrast. E-19 was right. `.st-link` fixed the remembered case; this is the unremembered one. `#0000EE` was the only saturated blue in the system. Executed directly into `build/build.py` 23 Aug 2026 |
| E-22 | **`.st-visually-hidden`** added | one utility; `.st-shell--explorer .st-waiting__label` now JOINS its selector instead of repeating the declarations | The technique existed exactly once, hardcoded in the shell, so a checkbox or actions column header had no way to carry a name that is read and not drawn. The Utilities block's own bound says a missing utility is a finding, not a licence to write it locally — this is that finding, answered. One expression, so it cannot drift from itself |
| E-23 | **`.st-lineage`** added | 13 classes + `__node-toggle`; sticky `__origin`, `__hop` bands with `__hoplabel`/`__hopcount`, `__nodes`/`__node`, `--open`/`--restricted`, `__nest`, `__more`, `__horizon` | From brief 6, Anaplan Semantic Layer engagement, 23 Aug 2026. A confirmed requirement had no expression and the workaround read as compliant. Three near-fits fail on three different axes — `.st-disclose` loses direction, `.st-table` loses distance, `.st-steps` assumes a known end. Every rule resolves to existing tokens; the role wheel is untouched. Declared absence reuses `.st-empty`'s dashed `border-strong` edge, which is what keeps a restricted node from reading as an error. **9 audit pairs added, all passing** — 312 → 330 checks, still 0 AA failing. The reference page's `review.lineage` region now renders the component instead of the two-disclosure workaround it was demonstrating |
| E-24 | **Rail counts, collapses, nests** | `.st-rail__label` becomes a `<button>` + leading `.st-rail__chev` + trailing `.st-rail__count`; `.st-rail__group[data-open]` / `.st-rail__items`; `.st-rail__link--sub`; `.st-rail__more` | Brief 6 R1 and R5, adjudicated against the **confirmed F4 frame** rather than the brief's description. The nesting was not asked for and was the real gap: SHELL-SPEC asserted "the rail supports one level of nesting" and no CSS expressed it — the second document-versus-code contradiction found this day. R2, R3 and R4 declined, R4 because the confirmed frame does not re-root the rail at all. 4 audit pairs added, 330 → 334 checks, still 0 AA failing |
| E-25 | **Rail selection de-blued** | `blue-10` wash + `blue-80` text + `link-primary` icon → `--st-layer-selected-01` wash + `--st-text-primary` + weight 600, icon on `--st-border-interactive` | E-16 wrote the wash on the scaffold brand, where blue IS primary. On deloitte it rendered a blue wash with blue text and a GREEN icon — three channels, two hues, on a green brand. **The contrast audit passed it every build**, because contrast measures legibility and cannot see a hue that is wrong for the brand. `.st-table tbody tr[aria-selected]` already washed with the neutral `--st-layer-selected-01`; selection is now one expression across both surfaces. E-16's wash-not-rule decision is preserved — only the hue changed |
| E-26 | **`app.detail` region + `.st-shell__panel`** | New shell region and `--st-shell-panel: 320`; `.st-panel__head`/`__title`/`__dismiss`/`__body`/`__section`/`__foot`; grid column via `:has()`, sheet below 1056px | Proposal **CP-01** from the engagement, 8 fields complete, 6 regions / 3 flows of consumers. SHELL-SPEC said "No right panel" — but its stated reason was that a **persistent empty** panel is an invitation, and this one does not exist unless a row is selected, so the refusal never covered it. Spec and `SHELL_CARBON` provenance both amended to say what they meant. The persistent Carbon panel is still declined |
| E-27 | **Rail sectioned, group headers sticky** | `.st-rail__group` gap → hairline between groups; `.st-rail__label` full-bleed, opaque and `position: sticky` within the rail's scroll; row padding one step roomier | Chosen by eye from five rendered options, 23 Aug 2026. Fixes the biggest failure of a long rail — at 312 modules the group you are inside scrolls away and you are reading names with no idea which group owns them. A sticky header costs nothing horizontally, which is the currency this frame is short of. **Cost, recorded rather than discovered:** the roomier rhythm shows fewer rows at once, so more scrolling in exactly the product that has the most to scroll |
| E-28 | **Panel tabbed; boxed fragments; the scroll-container fix** | `.st-tablist` composed into `.st-shell__panel` (**cap of three tabs**); `.st-tab[data-attention]` dot for a situational tab; `.st-panel__box` + `__boxlabel`; rail **and** panel given `align-self: start` + viewport-relative height; toasts move clear of an open panel | Dong's pick, 23 Aug 2026: option 2 as the base, option 3's box for the one fragment that must read as an object, option 5 arriving **as a tab rather than a class modifier** — one anatomy, and the situation adds a tab. A panel with an unanswered tab opens on it, else the decision is behind a click, which was the whole objection to tabbing it. `__box` is separated from `.st-tile` on three cues (recessed `layer-accent-01`, no elevation, radius-md vs the tile's raised white card at radius-xl). **Latent defect closed:** neither the rail nor the panel had ever been a scroll container — both stretched to the grid row's height, so `overflow` never engaged, sticky headers would have been inert and `__foot` sat at the bottom of the page. 6 audit pairs added, 342 → 348 checks, still 0 AA failing |

**Deliberately unchanged:** the palette (all ten ramps — the language is carried by structure,
not new colours), the luminance ladder, role separation and `check_role_separation()`, the focus
mechanism, the shell region set and derivation rules, the semantic pattern vocabulary, motion
patterns, forced-colors coverage (extended to the new anatomy), reduced-motion, the review-layer
boundary. Nothing about becoming beautiful required becoming less governed.

---

## Transcription map — where each event lands in `build/`

The encode was executed against the generated output because the bridge was down. Transcribe as
follows; then `python3 build/make.py` and `STRATA_BRAND=deloitte python3 build/make.py`, and
diff each `dist/*/strata.css` against `strata-next-scaffold.css` — structural intent should
match exactly; brand-resolved values will differ for deloitte, which is correct.

1. **`build/tokens.py`** — E-01 (radius xl), E-02 (the eight type tokens replace the twelve;
   provenance row per token: `changed`, why = type-system-study), E-03 (font stacks), E-04
   (border-subtle values, both themes), E-05 (density defaults), E-06 (elevation-01), and the
   new semantic token `border-interactive-subtle` (blue-30 light / blue-70 dark) from E-07.
2. **`build/build.py`** (component CSS emitters) — E-07…E-19 component blocks and the
   `[data-appearance~=…]` rules, plus P-1…P-4. The comments in `strata-next-scaffold.css`
   carry the whys verbatim — lift them with the code.
3. **`build/build.py` `AUDIT_PAIRS`** — add the new pairs (all verified passing): th-tint
   text/border, th-strong text, chrome-coloured navlink/brand/account/waiting/count/avatar,
   rail-current (light+dark), tag text (light+dark), tertiary label; and as advisory: the six
   dot hues × both themes, field hairline border, card hairline, tag border.
4. **`build/color.py`** — no change. The role wheel is untouched; the guard re-runs as-is.
5. **`dist/*/strata-icons.svg`** source (`build/icons.py` or equivalent) — E-20's five symbols.
6. **Reference page (`build/guide.py`)** — regenerates itself; the tag, steps, stat and
   skeleton sections will re-render in the new expressions with the provenance rows above.

## What was verified here, and what only the real rebuild can verify

Verified: both themes, both exemplar screens, axe 0 violations; production-check full-mode
clean; 25 enforced contrast pairs pass computationally; forced-colors rules extended.
Only the rebuild can verify: the full 262-check audit across every existing pair against the
re-cut border tokens (three old advisory pairs will report new values), the deloitte brand
under the new component anatomy (green primary buttons at radius 8 etc. — the role guard and
audit will catch anything), and the regenerated reference page.
