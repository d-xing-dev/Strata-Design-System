# Bound design systems

What lives here is the **contract plus the renderable stylesheets** — the minimum needed to
render a screen at moderate or high fidelity, plus the attribution that has to travel with
anything rendered from them. The full system (build scripts, token source, living style guide,
contrast audit) lives outside the skill; you only need it to add a brand or change the system.

| File | Used at | What it is |
|---|---|---|
| `resolution-map.md` | Moderate → High gate | Semantic pattern → component. **Read before resolving any region to a specific control.** Also lists what the system does not have |
| `strata-scaffold.css` | **Moderate** | Unbranded. Real spacing, type, states, hierarchy, one non-brand accent. No brand commitment |
| `strata-deloitte.css` | **High**, Deloitte only | Branded. Valid only after the binding question is answered |
| `NOTICE`, `LICENCE-AND-ATTRIBUTION.md` | **Any artefact rendered from either stylesheet** | Strata derives from IBM Carbon under Apache-2.0, which requires the NOTICE to travel with derivative distributions |
| `reference-scaffold.html`, `reference-deloitte.html` | **Before writing any layout CSS** | One assembled screen, laid out entirely with system classes. The only artefact that transmits composition |
| `usage.md` | Whenever a component almost fits | When each applies, when it does not, and what to do when it nearly does |
| `shell-spec.md` | Before adding a shell region | Region set, parameters, the two variants, and what is deliberately absent |
| `strata-icons.svg` | **High and above** | Sixteen icons as a symbol sprite. Inline it once per document, reference with `<use href="#st-i-search">`. A production screen with no icons is not one |

## Read the reference page first

`reference-scaffold.html` (moderate) and `reference-deloitte.html` (high) are one assembled
screen each: full shell, a collection at realistic length, a form with helper text and a
validation state, status, notification, and real body copy. Between them they use every component
in the system, **in composition** rather than in isolation.

This matters more than it sounds. A design system constrains parts, not compositions — tokens fix
the atoms, but page rhythm, chrome weight, heading hierarchy and section separation live in the
grammar, and two competent builders working from identical tokens produce products that do not
look alike. A component gallery cannot transmit that. One real page can.

**Read it before writing any layout CSS. Then re-lay one of your own screens against its rhythm
and diff before propagating.** Everything on it is a system class; the only page-specific CSS is
three declarations in the head, and if you find yourself needing more than that, the layout layer
is the thing to report against.

## Who owns this

**Strata is maintained in its own project.** It is not owned by any consuming engagement, and
no engagement should modify it in place.

**To propose a component or a change**, write a brief and send it to that project. A brief that
gets acted on contains: the semantic pattern it resolves, which regions in your product consume
it and how many, the markup and CSS as built, the rules that matter and why, and an honest
assumptions table — including whether you checked it against the inventory below.

Until a proposal is adopted, the resolution map still reads *not built*, and the next project
rebuilds the same thing differently. That is the erosion mechanism operating at system scale.

## The complete inventory

**Check here before building anything.** A component built because nobody could see the
inventory is a duplicated system, which is worse than the gap it closed.

| Group | Classes |
|---|---|
| Type | **EIGHT, and only these eight.** `.st-display` `.st-heading-md` `.st-heading-sm` `.st-body-md` `.st-body-sm` `.st-label` `.st-helper` `.st-code`. Ledger E-02 retired `.st-heading-lg` `.st-heading-xs` `.st-heading-compact` `.st-body-compact` `.st-label-md` `.st-label-sm` and did **not** alias them — a retired name styles **nothing**, so `.st-heading-lg` on a page title renders body text. Page titles take `.st-display`; a section head takes `.st-heading-sm`. All eight set `margin-block: 0`, so spacing is the composition layer's and never a type class's |
| Button | `.st-btn` + `--primary` `--secondary` `--tertiary` `--ghost` `--danger` `--sm` `--md`, `.st-btn-group` |
| Field | `.st-field` `.st-field--date` `.st-field-wrap` `.st-formitem` (+ `--full`, which drops the 24rem cap where the control **is** the content) `.st-lbl` `.st-help` `.st-msg` `.st-msg--error` `.st-msg--warning` |
| Choice | `.st-choice` `.st-radio` `.st-check` |
| Toggle | `.st-toggle` `.st-toggle-wrap` |
| Table | `.st-table` `.st-table--zebra` `.st-table-wrap` — the wrap **scrolls** a table wider than itself and keeps its radius; it no longer clips one away |
| Tag | `.st-tag` + `--sm` `--lg` `--outline` `--interactive` and hue modifiers |
| Notification | `.st-note` + `--error` `--success` `--warning` |
| Tile | `.st-tile` `.st-tile--clickable` `.st-tile--selected` (`__title` / `__body`). A tile that acts rather than navigates must be a real `<button>`; `button.st-tile` resets the UA font, alignment and width so it needs no inline style |
| Tabs | `.st-tablist` `.st-tab` — the list scrolls itself when the tabs do not fit; it never widens the page |
| Modal | `.st-modal` + `--xs` `--sm` `--lg`, `.st-modal-scrim` |
| Calendar | `.st-cal` `.st-day` + `--selected` `--start` `--end` `--inrange` `--today` `--muted` |
| Utility | `.st-focusable` |
| **Layout** | `.st-container` `.st-container--full` `.st-grid` `.st-grid--narrow` `.st-grid--condensed` `.st-col` |
| **Composition** | `.st-stack` `.st-row` + `--top` `--between` `--end`, `.st-fill` `.st-page` `.st-page__head` `.st-page__title` `.st-page__sub` `.st-section` `.st-section__head` `.st-hr` |
| **Shell** | `.st-shell` + `--task` `--explorer` `--norail`, `__header` `__brand` `__nav` `__navlink` `__spacer` `__util` `__utilbtn` `__account` `__avatar` `__rail` `__main` `__panel`, `.st-crumb`, `.st-waiting` + `--due` `--none`, `.st-skip` |
| **Rail** | `.st-rail__group` (`[data-open]`) `.st-rail__label` (a `<button>`) `.st-rail__chev` `.st-rail__count` `.st-rail__items` `.st-rail__link` + `--sub` `.st-rail__meta` + `--due` `.st-rail__more` — **one level of nesting only**; a third tier is a drill and belongs to the page |
| **Panel** | `.st-shell__panel` (`[data-open]`, region `app.detail`) `.st-panel__head` `__title` `__dismiss` `__body` `__section` `__foot` — never persistent, dismiss required |
| **Lineage** | `.st-lineage` + `--upstream` `--downstream`, `__origin` `__hop` `__hoplabel` `__hopcount` `__nodes` `__node` (+ `--open` `--restricted`) `__node-toggle` `__desc` `__nest` `__more` `__horizon`. **`--path`** is the second view: `__step` (+ `--origin` `--terminal`) `__via` `__rule` — one route end to end with the formula at each step, where the hop bands answer *what is one step away* |
| Density | `[data-density="compact"]` on the shell or a surface |
| Toast | `.st-toasts` `.st-toast` + `--success` `--warning` `--info`, `__body` `__title` `__close` |
| Search | `.st-search` `__field` `__icon` `__clear` `__count` + `--over` |
| Disclosure | `.st-disclose` + `--empty`, `__chev` `__title` `__meta` `__body` |
| Steps | `.st-steps` `.st-step` + `--done` `--current` `--todo` `--failed`, `__num` `__text` `__pos` |
| Stat | `.st-stat` + `--lead` `--unavailable`, `__figure` `__label` `__delta` (`--up` `--down`) `__meter` (`--warn`) — see **Meter** for the standalone bar |
| Comparison | `.st-compare` `__panel` (`--winning` `--absent`) `__label` `__body` `__attrib`; `.st-cmp-before` `.st-cmp-after` `.st-cmp-same` `.st-cmp-unread` |
| Subject state | `.st-statusband` `__item` (`--stale` `--blocked`) `__dot` |
| Empty state | `.st-empty` + `--error`, `__title` `__body` |
| Key-value | `.st-kv` (`<dl>` / `<dt>` / `<dd>`) |
| Table controls | `.st-table__sort` `.st-table__sortarrow` `.st-table__rowlink` |
| **Utilities** | `.st-num` `.st-nowrap` `.st-truncate` `.st-text-secondary` `.st-text-helper` `.st-visually-hidden` — **bounded set, see below** |
| Grid shortcuts | `.st-col--half` `--third` `--two-thirds` `--quarter`, `.st-container--narrow` |
| Code block | `.st-codeblock` + `--line`, `__head` `__meta`; `<b>` inside marks a key. **`.st-code` is inline only** — a formula or payload on its own line takes this, which brings the surface, the caption and a scroll of its own |
| Pager | `.st-pager` `__nav` `__position` (+ `--counting`) `__of` `__size` — position in a set that cannot be scrolled. States a **range and a total**, never a page number alone, and holds its width so the button you just pressed stays under the cursor |
| Meter | `.st-meter` + `--warn` (`> i` is the fill) — a bare progress bar. `.st-stat__meter` is the same element inside a stat. Needs `role="progressbar"` with aria-valuenow/min/max, or naming by adjacent text |
| Key code | `.st-keycode` + `--sm` |
| Icons | `.st-icon` + `--sm` `--md` `--lg` `--xl`, `.st-icon-btn` (44px target) |
| Loading | `.st-skeleton` + `--text` `--line` `--block` `--circle`, `.st-loading` `__spinner` |
| Motion | `.st-enter` `.st-exit` `.st-page-enter` `.st-settle` — **prototype level only** |
| Review chrome | `.st-review` + `--bar`, `__label` — **never inside the product region** |

**The layout and shell layer now exists**, so a Strata binding covers composition as well as
components. That was not true before: the absence cost one measured engagement 24 structural
classes and 90 rules, with roughly half its finished class uses bespoke. If you are binding to a
**client's** system instead, check whether theirs ships a layout layer — many do not — and if it
does not, say on the artefact that the binding is component-level only.

**Bound is the product, and its gate is executed.** `production-check.py` sits in this directory,
emitted here by Strata's build from `build/production_check.py` — one copy, so the floor cannot mean
one thing at the Draft and another at the gate, and all three design skills run this same file. It
checks placeholder copy, keyboard reachability, accessible names, overflow at every declared desktop
width, and classes outside the system. Since 6 Sep it also checks three conditions that exist
because an artefact reached Bound carrying three retired type classes and four workarounds for
components this system had already shipped, and **nothing caught any of it**: the old class check
only ever flagged names that do *not* start with `st-`, so a retired name read as a system one.

  - **every `st-` class in the rendered DOM is defined by some stylesheet.** A retired or
    mistyped name styles nothing and is invisible to any check that reads markup alone.
  - **the embedded generated stylesheet is byte-identical to the built one** (`--system-css=`).
    Appending a proposal to the generated block is how four hand-written components came to read
    as system ones.
  - **a local rule redefining a system class is declared** (`--allow-override=`). A workaround
    pending a system fix is legitimate; an undeclared duplicate of a rule the system already has
    is a stale copy nobody noticed.

The governing rule behind all three, from `patterns.md`: *a document that asserts a capability or
a condition must be checkable, and an assertion that outlives its condition is a defect rather
than stale prose.* A proposal that says "the system does not have this yet" names a class, and a
name is checkable. It runs on the **product region** only —
review chrome carries `.st-review` or `data-review` and is skipped; the product carries
`[data-product]`.

**Desktop web only.** Mobile is a recorded out-of-scope rather than a silence: the shell hides the
rail below 672px and puts nothing in its place, so a product claiming production-readiness on a
phone would be claiming something untrue.

**Links inside coloured surfaces inherit and underline.** Handled by the system for
`.st-statusband`, `.st-note`, `.st-toast`, `.st-empty`, `.st-step__text` and `.st-tag` — an
unstyled anchor takes the link colour, which on a green-primary brand makes a *blocked* status
render in the action hue.

**Utilities are bounded and the bound is the rule:** a utility may only express something the
token layer already contains. No new values, no new colours. Four exist, all from measured field
use — `.st-num` alone replaced 86 bespoke class uses. A utility you want that is not there is a
finding, not a licence to write it locally.

**One pattern remains unresolvable:** `comparison — variance grammar`. Shared-axis tie-out with
tolerance treatment, needed only by planning and finance work. If a region needs it, stop, reopen
the region at Moderate, or propose — do not substitute the tabular comparison for it.

## Rules

**Moderate renders against `strata-scaffold.css`. Always.** Never a branded stylesheet, however
convenient — that is the visual-finish guardrail, and using a brand file at moderate is the exact
smuggling the ladder exists to prevent.

**High renders against a branded file, and only after binding is confirmed.** If the client has
their own design system, neither of these files applies: use theirs, and it needs its own
resolution map in the same format.

**A pattern with no component in the map cannot be resolved.** Stop, reopen the region at
Moderate, or build a flagged proposal and brief it back — never substitute the closest thing
silently. See the fidelity contract.

**Never set `font-size` directly.** Twelve type tokens, twelve classes, no exceptions. The gap
between those two numbers is what produced 109 hardcoded pixel values in one engagement.

**Declare density once, on the shell.** `data-density="compact"` — components read
`--st-density-*` and never the raw size scale. Compressing surface by surface is how correct
component usage still ends up looking wrong.

**Do not write layout CSS.** `.st-grid`, `.st-stack`, `.st-row` and `.st-page` cover it. If they
do not, that is a finding for the system, not a local class.

**Ship the NOTICE with any artefact rendered from these stylesheets.**

## Adding a brand

Add an entry to `BRANDS` in the full system's `build/color.py` — hue angles, chroma multipliers,
a role map, any pinned literals — then `STRATA_BRAND=<name> python3 build/make.py` and copy the
resulting `dist/<name>/strata.css` in here as `strata-<name>.css`.

Two things fail the build rather than being caught in review: any AA contrast guarantee
breaking, and a **role wheel that cannot be read** — two status roles on one hue, an action role
sharing a hue with a status role, or any checked pair under 20° apart. A brand that ships is a
brand that passed both.

`focus` is a role in its own right. Do not point it at the primary hue on a brand where primary
and success are close; that is precisely how the Deloitte build ended up rendering its focus
ring and its success colour as the same literal.


<!-- SNAPSHOT-STATE:BEGIN -- generated by build/snapshot.py, do not edit -->
<!-- SNAPSHOT-STATE:END -->
