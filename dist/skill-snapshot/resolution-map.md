# Semantic → Strata resolution map

The map from a semantic pattern (committed at **low** fidelity, in the region register) to
the specific Strata component that renders it (resolved at **high** fidelity, once binding is
confirmed).

Without this, resolving semantics to components at high fidelity is a fresh design decision
every time — which is the inconsistency the whole approach exists to prevent. With it,
raising fidelity is a render.

**This map is a property of the bound system, not of the pipeline.** A client's own design
system needs its own map in this format. The semantic vocabulary is the portable part; this
file is Strata's instance of it.

**Changed 21 Aug 2026:** a proposal intake (§Proposals arriving from engagements) — the pipeline's
new `design-structural-precedents` stage runs a resolution check against this map **before** a
structure is chosen, so gaps now arrive here as buildable proposals with an inspiration attached,
early, instead of as refusals at the Bound gate.

**Changed 20 Aug 2026:** fork rules added (§Fork rules) — where one pattern legitimately has
two expressions, the choice is now stated deterministically instead of being a per-screen
judgement; and the shared-expression rule makes "two patterns, one costume" a gate failure.
Expressions updated for the visual-language encode (see ENCODE-LEDGER.md). See PATTERNS.md
for the intent-indexed usage tier that sits above this map.

---

## Fork rules — one pattern, two legitimate expressions

A fork rule exists so that the same input always produces the same expression. If neither
branch of a fork clearly applies, that is a finding for the map, not a local judgement call.

**R1 — `collection`:**
- **R1a → `.st-table`** when the items share comparable fields that the user scans *across*
  (columns are the point: sorting, comparing, totalling).
- **R1b → card list** (`.st-stack` of `.st-tile`) when the items are **few (≤ ~6), heterogeneous,
  and each is acted on individually** (the item is the point; fields differ per item; each
  carries its own action).
- The two may coexist on one screen *because the rule separates them* — a scanned worklist
  table above a parked-items card strip is two different inputs, not one pattern in two
  costumes.

**R2 — the shared-expression rule (the mirror of R1):** no two patterns may share an
expression unless a stated cue separates them. The recorded cues:
- A `record-detail` card **always carries `.st-kv`** (caps keys, E-15); a collection card
  never does. That is how "one thing, expanded" and "several things, listed" stay tellable
  apart when both are `.st-tile`.
- A `summary-tile` (`.st-stat`) carries the display figure + caps label anatomy; nothing else
  may imitate it.

**R3 — undecided content:** a region whose requirement is **Open** renders the shaped skeleton
of its *assigned expression* (`st-skeleton-table` / `st-skeleton-card` / `st-skeleton-stat`),
with the job slot stating what the region will do. Never a filled component with invented
content; never a generic grey block.

Any deviation or looking-gate verdict note that recurs twice becomes a candidate rule for this
section — that is the rule factory, and it is how this map grows from findings rather than
anticipation.

---

## Resolved

| Semantic pattern | Strata component | Modifiers / notes |
|---|---|---|
| `collection` | **fork R1**: `.st-table` in `.st-table-wrap` **or** card list | Table: frameless, hairline rows, **no zebra default**; `th.st-num`/`td.st-num` for numerics; header colour is the product's appearance axis, never a per-screen choice |
| `collection-bulk-actions` | `.st-table__batchbar` | Appears above the table on first selection. Row-level actions disable while active |
| `bounded-choice-small` | `.st-choice` + `.st-radio` | Vertical by default. Never a select — hiding three options behind a click costs a click and gains nothing |
| `bounded-choice-large` | `select.st-field` + chevron | 40px right padding to clear the chevron. Menu scrolls at six rows |
| `multi-choice` | `.st-choice` + `.st-check` | Supports indeterminate for parent/child sets |
| `binary-instant` | `.st-toggle` + `.st-toggle__track` | State text required, three words or less, adjectives not verbs |
| `binary-deferred` | `.st-check` + an `action-row` | If there is no commit control on the surface, the pattern is wrong — use `binary-instant` |
| `unbounded-entry` | `.st-field` / `textarea.st-field` | Hairline field, white fill, radius 8, label always present. `--strong` is the accessible-boundary fallback |
| `constrained-entry` | `.st-field` — `.st-field--date` for dates | `tabular-nums` on numeric and date fields |
| `filter-set` | `select.st-field` and/or `.st-tag--interactive` | Applied filters render as dismissible chips |
| `status-indicator` | `.st-tag` with a hue modifier | **The dot-chip** (E-09): neutral bordered chip, 7px hue dot, text carries the meaning. The one expression the appearance axes never vary. `--icon` swaps the dot for a 12px icon |
| `notification-inline` | `.st-note` + status modifier | White card, hairline border, 3px semantic left rule, icon required, persists until dismissed |
| `action-row` | `.st-btn-group` + `.st-btn` variants | Primary right in dialogs and wizards, left on full pages. One primary per surface |
| `navigation-set` | `.st-tablist` + `.st-tab` | Peer surfaces only. Selected carries weight 600 as well as the underline |
| `navigation-set` (stepper) | `.st-steps` + `.st-step` | **Border-top state coding** (E-13): 2px edge + weight; done/current/todo/`--failed` (non-optional). Position stated in text via `__pos`. Never `.st-tablist` |
| `overlay-dialog` | `.st-modal` in `.st-modal-scrim` | `--xs` 320 / `--sm` 480 / default 640 / `--lg` 880. Body scrolls, header and footer fixed |
| `record-detail` | `.st-tile` **+ `.st-kv` (required — R2 cue)** | The kv anatomy is what separates it from a collection card |
| `search` | `.st-search` + `.st-field` | The count is part of the component; idle state carries the total |
| `disclosure` | `.st-disclose` on `<details>` | Whole summary row is the control; `__meta` states size; `--empty` removes the control |
| `reveal-pane` | `.st-shell__panel` (region `app.detail`) + `.st-panel__*`, **`.st-tablist` composed inside (cap of three)** | **Built 23 Aug 2026 from CP-01 (E-26, E-28).** Tabbed: the tabs are how the panel changes shape when the situation does, so a situational facet is a tab carrying `data-attention`, not a class modifier — and the panel **opens on** an unanswered tab. `.st-panel__box` delineates the one fragment that must read as an object; it is recessed where `.st-tile` is raised, because a tile means *a record* and a box means *a fragment*. Opens on row selection, closes on dismiss or Esc; **never persistent** — the column does not exist when nothing is selected. Body scrolls, head and foot hold, same anatomy as `.st-modal`. Below 1056px it becomes a sheet stacked in `grid-area: main`, so it covers the list and leaves header, band and rail reachable. **Never nests.** Not a substitute for `.st-modal`: no scrim, so it cannot demand a decision |
| `lineage` | `.st-lineage` + `--upstream` / `--downstream` | **Built 23 Aug 2026 from brief 6 (ledger E-23).** Distance is the structure, not an inference: each hop is a `<section>` with a real heading and its own count, nodes are a `<ul>`, expansion is a `<button>`. `__more` states within-band overflow and `__horizon` states the beyond-count — both are bands, never helper text. `__node--restricted` and `__horizon` wear `.st-empty`'s dashed `border-strong` edge, so a stated hole cannot read as an error (errors go solid in `support-error`). Empty case resolves to `.st-empty`, not a lineage variant. **Never `.st-truncate` on `__desc`** |
| `notification-transient` | `.st-toast` in `.st-toasts` | Confirmations only. Never an error, never anything actionable |
| `summary-tile` | `.st-stat` | **Now a card** (E-14): hairline surface, caps label, 28/600 figure. Label required; delta sign in CSS content |
| `comparison — tabular` | `.st-cmp-*` cell modifiers | Inside an ordinary `.st-table`. Unchanged rows render; `--unread` exists because a blank cell reads as zero |
| `comparison — prose` | `.st-compare` + `__panel` | Winning panel carries a text tag as well as a border |
| `page-layout` | `.st-container` + `.st-grid` + `.st-col` | 16 columns, Carbon's breakpoints |
| `application-shell` | `.st-shell` + `--task` / `--explorer` | One region set, two prominence configurations. **Chrome colour and table-header colour are appearance axes** — declared once per product in the appearance config (`data-appearance`), chosen at binding, recorded in the ledger |
| `subject-state` | `.st-statusband` | The tenth shell region; present only where such state persists across screens |
| `empty-state` | `.st-empty` + `--error` | Must say what is missing **and** what to do |
| `key-value` | `.st-kv` | Caps keys (E-15). Inside a `record-detail`; also its identifying cue |
| `collection-sort` | `.st-table__sort` + `__sortarrow` | The control inside `th[aria-sort]` |
| `collection-row-navigation` | `.st-table__rowlink` | The row **must** contain a real link |
| `content link` | `.st-link` | Added E-19 for the remembered case. **E-21 (23 Aug) added the base `a` rule**, so an unclassed link is now on-palette instead of `#0000EE` — `.st-link` is emphasis, not the only thing standing between the product and the UA default. Inside semantic surfaces the inherit-and-underline rule still wins |
| **undecided region** | `st-skeleton-table` / `-card` / `-stat` + `__job` | Fork R3. Designed-and-empty, never invented, never broken |

## Not yet built in Strata

| Semantic pattern | Status | Nearest thing today | Carbon has it? |
|---|---|---|---|
| `comparison — variance grammar` | Not built | Shared-axis tie-out with tolerance treatment. **Only planning and finance work needs it** | No |

**One gap left, and it is the right one to have left.** (History unchanged — see the previous
revision for the full account of how `comparison` was split and costed.)

## Proposals arriving from engagements

Adjudicating these is what this project is for. A gap found in an engagement arrives as a
**component proposal**, and the pipeline raises it in one canonical format defined at
`design-structural-precedents/references/precedent-contract.md`. Three stages can raise one and all
three use that format: the precedent stage's resolution check (earliest, and the only one that runs
before anything is drawn), `design-screen-compositions` when a composition needs an expression
nothing here covers, and `raise-design-fidelity` at the Bound re-resolution (latest, and the most
expensive place to find out).

**A proposal this project will act on carries eight things.** Anything missing them is a request for
a conversation, not a proposal:

| Field | Why the system owner needs it |
|---|---|
| ID `CP-nn` | So the same gap accumulates consumers instead of being re-raised under new names |
| Proposed name | In `st-` vocabulary, not the source product's |
| The job it does | The semantic pattern, solution-agnostic — this is what gets a row in the map |
| Why nothing existing serves | **The nearest component named** and what it specifically fails at. "There isn't one" is not a finding, it is an unfinished search |
| Behaviour required | States, interactions, responsive behaviour. The buildable part |
| **Inspiration** | The external precedent with resolvable sources, and the option render if one was drawn. **This is what makes a proposal a brief rather than a complaint** — it is the difference between "we need a panel" and something that can be built without a second conversation |
| Consumers | By region code. A count of one is a different decision from a count of nine |
| Workaround in force | What ships until it exists, what that costs, and whether it blocks |

**Three verdicts, and all three are recorded here.** *Build it* — the pattern gets a row in
§Resolved and the component gets a ledger event with its `why`. *Compose it* — existing parts do the
job, and the composition becomes a fork rule or a `PATTERNS.md` entry rather than a component.
*Decline it* — recorded with the reason and with the engagement's workaround and cost, because the
next engagement will hit the same wall and should not have to rediscover the decision.

**A proposal is never a licence to substitute.** The engagement's honest position while a proposal is
open is the recorded workaround or a shaped skeleton (R3), not a region rendered as though it
resolved. What the map cannot express, the artefact should not pretend to.

**Two rules confirmed 23 Aug 2026, and one finding parked under the rule factory.**

- **A panel opens on an unanswered tab.** A situational tab carrying `data-attention` is selected
  when the panel opens. Without it the decision sits behind a click, which is the whole objection
  to expressing a decision as a tab rather than an arrangement. Confirmed by Dong.
- **`data-attention` stays scoped to `.st-shell__panel .st-tab`.** It is not a system-wide tab
  state. **Occurrence one, recorded as a finding rather than generalised** — the habit is to wait
  for the pattern. If a second tablist needs an attention state, that is the second occurrence and
  it becomes a `.st-tab` rule; a third would be the links-inside-coloured-surfaces mistake repeated.
- **Working assumption, not confirmed:** where a subject has more than one unanswered question, the
  dot means *one or more* and the count lives in the panel body ("Question 1 of 247"), matching how
  the queue already reads. The dot is a state, not a counter. **Raise this with the engagement**
  before a screen depends on it.

**The rule factory applies here too.** A workaround that appears in two proposals is evidence the map
is missing a rule, not just a component.

### Adjudicated 23 Aug 2026 — the Anaplan Semantic Layer rail (brief 6, section 2)

Judged against the **confirmed F4 frame**, not against the brief's description of it. Three of the
five were declined, and two of those three were declined because the confirmed frame chose an
architecture that removes the need rather than because the need was unreal.

| Item | Verdict | Reason |
|---|---|---|
| **R1** group label counts and collapses | **Built** (E-24) | The frame's sidebar is five counted, collapsible groups. Confirmed need |
| **R5** overflow row | **Built** (E-24) | The frame shows "11 more" and "2 more". At 312 modules truncation is the default state, so this is the staged-view rule applied to the rail |
| *(not raised)* one level of nesting | **Built** (E-24) | SHELL-SPEC said "the rail supports one level of nesting" and **no CSS expressed it**. The frame needs area → module. Found while adjudicating the five |
| **R2** second trailing slot | **Declined** | The frame does not fuse two meanings into one slot — it puts the collapse caret **leading** and keeps the count trailing. The second meaning goes to the other end of the row, which is a position, not a second slot |
| **R3** control belonging to one group | **Declined — no consumer** | The frame's search is sidebar-wide ("Find anything — 12,456 points"), not group-scoped, and it is a text search, so `select.st-field`'s 40px chevron padding never arises. `.st-search` fits the rail. Re-raise if a group-scoped filter appears |
| **R4** `.st-rail__scope` | **Declined — the frame removes the need** | The confirmed frame **does not re-root the rail**. It stops at area → module and sends depth beyond that to a detail panel, which is what SHELL-SPEC's drill rule already says. Scope stays in `.st-crumb`, and the frame's own correction note agrees: *the model is scope, so it sits in the breadcrumb, not in the nav*. This reverses the maintainer's earlier recommendation to build it |

**Two ID namespaces, settled 23 Aug 2026.** `CP-nn` is the engagement's, assigned by the raising
stage. `MP-nn` is the maintainer's, used only when a brief arrives without an ID — it never
overwrites or renumbers a `CP-nn`, and it is dropped the moment the engagement supplies one.

**R2, R3 and R4 are one decision, not three.** They were raised as three items and adjudicated
above as three rows, which understates them. All three are consequences of a single architectural
question — **does the rail re-root when you step into a container?** If it does, you need all
three at once: a scope row to state the exit and the parent (R4), a *trailing* step-in chevron
distinct from the count because stepping in is not the same act as expanding in place (R2), and a
filter scoped to the re-rooted set rather than the whole rail (R3). If it does not, you need none
of them. F4 does not, so none were built.

**The revival trigger, stated so the next engagement does not have to rediscover it.** Re-raise
all three together, as one proposal, when any of these becomes true: the product's users work
below 1056px habitually, where the panel becomes a sheet and covers the list it was meant to
preserve; or the centre must hold something other than a list — an editing surface — while the
person still navigates; or a third genuinely *navigable* tier appears, as opposed to a third
drill level. Until then the honest position is that the frame chose a different architecture,
not that the problem was unreal.

**Proposal ID collision, recorded rather than quietly fixed.** The maintainer assigned `CP-01` to
`st-lineage` because brief 6 omitted the ID field. The engagement independently raised `CP-01` for
`st-panel`. **The raising stage owns the numbering, so the maintainer's ID was never valid** —
`st-lineage` is built and carries its ledger event (E-23) rather than a proposal ID, and `CP-01`
means `st-panel`. A system-side prefix for maintainer-assigned IDs is an open governance question.

## Layout and shell

Unchanged in structure from the previous revision: grid (`.st-container` `.st-grid` `.st-col`),
composition (`.st-stack` `.st-row` `.st-fill` `.st-page` `.st-section` `.st-hr`), shell
(`.st-shell` + regions), density (`[data-density]`). **New:** the appearance config —
`data-appearance` on the shell root, space-separated axes (`chrome-coloured`,
`table-head-tint` | `table-head-strong`), one declaration per product, exactly like a `BRANDS`
entry. Within a product each axis is chosen once and holds everywhere; a product that mixes
chromes screen-by-screen has un-chosen the choice. A product with a real reason for two
chromes (admin vs end-user areas) declares two zones in its config — an extension, not a
violation.

**Utilities remain a bounded set:** `.st-num`, `.st-truncate`, `.st-text-secondary`,
`.st-text-helper`, `.st-nowrap` (P-3, from a measured wrap defect), and now
`.st-visually-hidden` (E-22). The bound is unchanged: a utility may only express something the
token layer already contains.

**The rail counts, collapses and nests (E-24, 23 Aug 2026).** `.st-rail__label` is a `<button>`
carrying a leading `.st-rail__chev` and a trailing `.st-rail__count`; `.st-rail__group[data-open]`
holds the state and `.st-rail__items` is what folds; `.st-rail__link--sub` is the **one** level of
nesting SHELL-SPEC allows, and there is deliberately no `--sub` under a `--sub`, because a third
tier is a drill and drills belong to the page; `.st-rail__more` states within-group overflow.
`.st-disclose` is **not** the substitute for a rail group — it is a bordered card with its own
background, so five in a 256px rail draws five boxes inside a box.

**Read `usage.md` before laying anything out, `PATTERNS.md` before assigning a pattern, and
`shell-spec.md` before adding a region.**

---

## Which build to render against

| Fidelity | Build | Why |
|---|---|---|
| **Draft** | `dist/scaffold/` | One construction standard from the first render. Undecided regions are shaped skeletons, not roughness. **No brand** — polish must not smuggle in a binding that hasn't been decided |
| **Bound** | `dist/<brand>/` | Only after binding is confirmed at the gate; the appearance config is chosen at the same moment and recorded |
| **Motion** | `dist/<brand>/` | The prototype level |

`scaffold` is the default build (`STRATA_BRAND` unset). A brand should be an explicit act.

The build refuses a wheel where two roles collapse onto one hue — `check_role_separation()`
fails before contrast is audited. That guard checks hue *assignment*; how a pair reads in a
composition is still a Bound-gate judgement.
