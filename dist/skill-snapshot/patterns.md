# Strata patterns — the intent tier

**New file, 20 Aug 2026.** This is the third tier of the system's documentation, and it
completes the three-tier shape the governance research argued for:

1. **Parts** — tokens and components. What exists. (`dist/*/index.html`, the reference.)
2. **Usage** — how each part behaves and when a *part* is right or wrong. (`usage.md`.)
3. **Patterns** — this file: solutions indexed by **what the user needs to do**, GOV.UK-shaped
   (every entry says *when to use* and *when NOT to use*), resolving through RESOLUTION-MAP.md.

The boundary this tier respects: **the system owns the decidable rules; the pipeline owns the
contextual selection.** A pattern entry tells you which pattern answers an intent and when it
doesn't; the composition layer still decides anchor, zoning and reading order per screen. Where
a choice inside a pattern is decidable, it is a fork rule in the map, not prose here.

Each entry: intent → pattern → when / when not / resolution. Evidence notes are kept short;
recurring findings feed rules back into the map (the rule factory).

---

### Help users to work through a queue of items
**Pattern:** `collection` (scanned) + `subject-state` + `work-waiting`.
**When:** items arrive and are cleared; order is the priority; the user compares across items.
**When not:** if each item is a long-lived thing the user *navigates to* rather than clears,
that is an explorer structure — different shell variant, breadcrumb on, queue affordances off.
**Resolves:** fork R1a → table. Age/value right-aligned (`st-num`); every row states its
blocking reason in words (a status chip, never colour alone).

### Help users to act on one item in depth
**Pattern:** `record-detail` + `navigation-set` (stepper) + `action-row`.
**When:** one subject, several facts, a sequence with a current position.
**When not:** don't use a stepper for peer surfaces you may revisit freely — that is tabs;
steps have an order and things you cannot yet reach. Never both for the same question.
**Resolves:** `.st-tile` + `.st-kv` (the kv is required — it is the R2 cue), `.st-steps`
border-top coding, one primary action per surface.

### Help users to keep a small set of stalled things visible
**Pattern:** `collection` (attended) — the strip of stuck items that must stay louder than flow.
**When:** few, heterogeneous, each individually acted on (chase, view, open).
**When not:** the moment the set grows comparable and scanned (≥ ~7, shared fields), it is a
table again — move it, don't grow the cards.
**Resolves:** fork R1b → card list. Each card: identifier (`st-code`), name, status chip, one
`.st-link` action.

### Help users to enter details
**Pattern:** `unbounded-entry` / `constrained-entry` in a `.st-formitem`.
**When not:** never collect what the flow doesn't consume; never a placeholder as a label.
**Resolves:** hairline field; `--strong` fallback if boundary legibility is questioned in
testing — one class, not a redesign.

### Help users to choose
**Patterns:** `bounded-choice-small` (radios) / `bounded-choice-large` (select) /
`multi-choice` (checkboxes) / `binary-instant` (toggle) / `binary-deferred` (checkbox + commit).
**When not:** never a select for three options; never a toggle for anything that isn't applied
instantly; never a checkbox pretending to be a commit.

### Help users to commit, and to trust what committing did
**Pattern:** `action-row` + `notification-transient` (confirmation) or `notification-inline`
(anything that persists or needs response).
**When not:** never carry an error or anything actionable in a toast — if it needs a response
it must not be able to vanish.

### Help users to notice the state of the thing they're working on
**Pattern:** `subject-state` (statusband) for state that persists across screens (staleness,
locks, write-back); `status-indicator` (dot-chip) for state of one item.
**When not:** a per-screen fact does not go in the frame; an item status does not go in the
band. An empty band is the bell nobody looks at — render it only when the product has such
state at all.

### Help users to find a thing
**Pattern:** `search` (+ `filter-set`).
**When not:** three filters the user always uses beat a search box that hides them.
**Resolves:** the count is part of the component — idle carries the total.

### Help users to compare
**Patterns:** `comparison — tabular` (numbers against numbers, in a table) /
`comparison — prose` (two whole versions, pick one).
**When not:** variance-with-tolerance grammar is **not built** — the gate must say so rather
than substituting something approximate.

### Help users to read a list and one item at once
**Pattern:** `reveal-pane`.
**When:** the person compares across rows AND needs more than a row can carry — and losing their
place in the list is a real cost, not an inconvenience. A queue of 247 is the case that names it.
**When not:** if the detail demands a decision before anything else can happen, that is
`overlay-dialog` — a panel has no scrim and cannot compel. If the list is short enough to re-find
your place in, drill to a page and keep the width. Below 1056px the pane becomes a sheet over the
list, so a product whose users work narrow is choosing to cover the thing they were comparing.
**Resolves:** `.st-shell__panel` in region `app.detail`; the dismiss control is required, because
a pane that opens on selection and cannot be closed is a third column wearing a panel's clothes.

### Help users to see how far a consequence reaches
**Pattern:** `lineage`.
**When:** a change to one element propagates to others and **distance changes the decision** —
the person needs to know how far away the consequences are before they act. Data lineage, formula
auditing, build dependencies, permission inheritance, supply chains.
**When not:** a flat neighbour list (`collection`) is right when the set is small and distance is
irrelevant. A `disclosure` answers what is *inside* something; a walk answers what a change *reaches*.
Never a node-link canvas as the only view — it has no linear reading order, cannot be pasted into a
message and cannot be cited in a chat answer. Legitimate second view, poor only view.
**Resolves:** `.st-lineage` + direction modifier. N hops by default with each band counted and the
horizon stated as its own band; `.st-empty` for "nothing depends on this", which is a real and
useful answer rather than a failure.

### Help users when there is nothing, or something failed
**Pattern:** `empty-state` — every flow has a non-success terminal, and this is the surface it
lands on. Must say what is missing AND what to do.

### Show what is not yet decided
**Pattern:** the shaped skeleton (fork R3) — `st-skeleton-table` / `-card` / `-stat` with the
job slot.
**When:** the region's requirement is Open.
**When not — both directions:** never invented content wearing production finish (a guess in
good clothes is the failure this whole process exists to prevent, and it gets more dangerous
as artefacts get prettier); and never a loading shimmer for something that is *undecided*
rather than *loading* — the job slot's words are what tell those apart.

---

## Governing rules that sit above every entry

- **Appearance axes are product-constant.** Chrome, table-header treatment, shell variant,
  density, register: chosen once per product at binding, in the appearance config, recorded in
  the ledger. Screens never re-choose.
- **The dot-chip is the one non-variable element.** One tag expression, everywhere, every
  product.
- **Expression consistency is gated.** The looking-gate's fifth question: does every instance
  of the same pattern wear the same expression, and do any two patterns share one without a
  separating cue? Judged against the map's fork rules.
- **A staged view must state what it staged.** Any component that shows part of a set carries
  the count of what it did not show **inside the component**, not in helper text beside it. A
  truncation the person cannot see is indistinguishable from an empty set, so a view that stages
  silently is not a smaller answer — it is a wrong one. This generalises a rule the system
  already held in one place (`search`: "the count is part of the component; idle carries the
  total") to every other place it applies: paging tables, fan-out cuts, top-N lists, and any
  horizon on a walk. Raised from an engagement 23 Aug 2026, where a workaround carried a
  beyond-count as **text** with no structure behind it and passed every review that scanned for
  the requirement's vocabulary.

- **The rule factory.** Any deviation note or verdict note that appears twice across
  engagements is a candidate fork rule or cue. The map grows from findings, not anticipation —
  the system's founding habit, applied to its own governance.
