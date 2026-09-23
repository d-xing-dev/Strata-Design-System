# Usage rules

For each component: when it applies, when it does not, and **what to do when it almost fits**.

That third column is the one that matters. Design systems erode at the seams, not the centre.
Nobody restyles a button; they need a card that is slightly different, make one, and within a
month half the product runs on the shadow primitive. In one measured engagement a bespoke card
was used **47 times against `.st-tile`'s 4** — inside a single session, by an agent that knew the
risk. That is not carelessness. It is what happens when a real need meets a component that does
not stretch, and nothing tells you which way to bend.

**The standing rule when something almost fits: build what you need, and report it.** The
invention is often correct. What is never correct is it being invisible. Reported, it becomes a
usage rule or a new variant; unreported, it becomes the next project's starting point.

---

## Containers

### `.st-tile` — a record

**Applies to** a bounded record or object you might select, click through, or compare against its
siblings. It enforces `__title` / `__body` because that structure is what makes a row of tiles
scannable.

**Does not apply to** a headed panel containing mixed content — a form section, a chart with a
legend, a table with a toolbar. **This was the 47-use failure.** `.st-tile`'s structure fought
that job, so a shadow card appeared beside it.

**When it almost fits:** you want a headed panel, not a record. Use `.st-section` with
`.st-section__head`, which is the layout primitive for exactly that and carries no card chrome.
If you need the panel to look contained, put `.st-section` inside a `.st-tile` — do not build a
third thing.

### `.st-section` / `.st-page`

**Applies to** every page. `.st-page` owns the vertical rhythm; `.st-section` separates bands of
content within it.

**Does not apply** inside a modal, which owns its own padding.

**When it almost fits:** if you want a section to feel heavier, that is a `--gap` change or a
`.st-hr`, not a new wrapper.

---

## Layout

### `.st-grid` + `.st-col`

**Applies to** any multi-column arrangement. Sixteen columns, spans set with custom properties:

```html
<div class="st-grid">
  <div class="st-col" style="--span:16; --span-lg:10">…</div>
  <div class="st-col" style="--span:16; --span-lg:6">…</div>
</div>
```

**Every child needs `.st-col`** — or at least a `--span`. A child with neither used to auto-place
into one column of sixteen and render as a sliver, which looks like a CSS bug rather than a
missing class. That is now defended: an unclassed child renders full-width, which is obviously
wrong rather than mysteriously wrong. Use `.st-col--half`, `--third`, `--two-thirds` or
`--quarter` for the common splits so the ordinary case needs no inline style at all.

**Does not apply to** a row of controls or a toolbar — that is `.st-row`. The grid is for page
structure, not for putting three things next to each other.

**A page narrower than the shell** is `.st-container--narrow` (45rem), for form-heavy and prose
pages. `.st-container` caps the frame and `.st-page__sub` caps one measure; before this, a page
that wanted to be narrower than the whole shell had to set `max-width` inline.

**When it almost fits:** you want a two-up that is not on the grid. Use `.st-row` with
`.st-fill`, or `.st-compare` if the two things are genuinely being compared.

### `.st-stack` / `.st-row`

**Applies to** everything else. These two cover most bespoke layout CSS people write.

**When it almost fits:** the gap is wrong. Set `--gap` on the instance. Do not write a new class
for a spacing variant — that is how 24 structural classes happen.

---

## Density

**Declare it once on the shell**, never per surface:

```html
<div class="st-shell" data-density="compact">
```

**Never compress by hand.** Components read `--st-density-control`, `--st-density-row` and
`--st-density-pad`. If a surface genuinely differs — one dense table in an otherwise comfortable
product — set `data-density="compact"` on that surface, not on its cells.

**When it almost fits:** if compact is still too loose, that is a finding for the system, not a
local override. Two density modes is a decision; five hand-compressed surfaces is an accident.

---

## Appearance axes

**One `data-appearance` attribute on the shell root is the only mechanical way to vary the
product's look** -- space-separated values: `chrome-coloured` (blue-90 chrome; default is white),
`table-head-tint` | `table-head-strong` (default is grey). Together with the shell variant and
density, these form the product's **appearance config**: chosen ONCE per product at the binding
decision, recorded in the ledger, held on every screen. A product that mixes coloured and light
chrome screen-by-screen has un-chosen the choice. The dot-chip tag is deliberately not an axis --
one tag, everywhere.

**When it almost fits:** a product with a real reason for two chromes (admin vs end-user areas)
declares two zones in its config -- an extension, not a per-screen exception.

---

## Type

**Eight tokens, eight classes, and never set `font-size` directly.** (The T1 ramp replaced
the twelve-token scale on 20 Aug 2026 -- four sizes, 12 / 13.5 / 15 / 28, weight-led. The
classes are `st-label`, `st-helper`, `st-body-sm`, `st-body-md`, `st-heading-sm`,
`st-heading-md`, `st-display`, `st-code`. If something needs emphasis, change its weight or
colour, never its size -- that rule is what keeps the ramp at four sizes.)

**When it almost fits:** there is no class for the size you want. That is a finding. Do not write
a literal — one literal legitimises the rest, and the measured cost of partial coverage was 109
hardcoded pixel values in a single product.

**The six retired names are gone, not aliased, and a retired name styles NOTHING.**
`.st-heading-lg`, `.st-heading-xs`, `.st-heading-compact`, `.st-body-compact`, `.st-label-md`
and `.st-label-sm` were retired by E-02. An alias is a second name for the same decision and
second names are how twelve sizes happen — so there is no fallback, and `.st-heading-lg` on a
page title renders **body text**. A page title takes `.st-display`; a section head takes
`.st-heading-sm`; a small caps label takes `.st-label`. This is not a preference. An artefact
reached Bound in September using three of the retired names, with every heading on every screen
unstyled, and no check saw it — the class check only ever flagged names that do not begin with
`st-`. `production-check.py` now fails on any `st-` class no stylesheet defines.

**All eight set `margin-block: 0`.** A type class sets a font and never a space: spacing belongs
to the composition layer, `--gap` on a stack or a component's own padding. Before this, the same
class on a `<p>` and on a `<span>` produced different vertical rhythm, and a measured gap
hierarchy inverted — 44px under a table where unrelated blocks sat at 32.

---

## Status and action

### `.st-tag` vs `.st-btn` vs `.st-note`

Roles are separated by **form** as well as colour, and the form is what survives greyscale and a
brand whose action and status colours sit close together:

| Form | Means |
|---|---|
| Filled rectangle with a verb | An action |
| Bordered chip with a hue dot and a state word | A status |
| Left-ruled band with an icon | A notification |
| Outlined panel with an attribution line | A version |

**When it almost fits:** you want a status that is clickable. That is a filter — use
`.st-tag--interactive`. You want an action that looks quiet — that is `.st-btn--ghost`. Do not
make a tag clickable to avoid a button.

### `.st-note` vs `.st-toast`

**`.st-note` is the default.** It persists until dismissed, which is the safe behaviour.

**`.st-toast` is for confirmations of something the person just did**, where the information is
genuinely disposable. **Never an error, never anything actionable.** If it needs a response, it
must not be able to disappear before the response.

**When it almost fits:** it feels too heavy for a confirmation but it does contain an action. It
is not a toast. Keep it inline.

---

## The new components

### `.st-stat` — a figure at a glance

**Applies to** the one number a person reads before anything else. Rows of two to four.

**Does not apply to** a chart, or to a number inside a table. Since 20 Aug 2026 (E-14) the
stat **is** a card -- hairline surface, caps label, display figure -- because on the white canvas
a bare figure floats. The row-of-four-panels risk the old no-border rule guarded against is now
owned by the composition layer's gap hierarchy, not by the component.

**Rules that matter:** the label is required and is not a tooltip; a bare figure is not
information. `--unavailable` renders smaller and italic, because a missing figure must never look
like a zero.

**When it almost fits:** you want five or more. That is a table.

### `.st-search`

**Applies to** narrowing a set too large to scroll. **The count is the component**, not the
field. Idle state carries the total. Put `aria-live="polite"` on `.st-search__count`.

**Does not apply to** filtering by a known dimension — that is `filter-set`.

### `.st-disclose`

**Applies to** content that is available but not always wanted. Native `<details>`, so keyboard
operation and find-in-page come free.

**The whole summary row is the control.** A 12px chevron hit target is a defect. `--empty` means
the control is **absent**, not disabled — a disabled expander implies there is content behind it.

**When it almost fits:** you are using several as a menu. That is legitimate, and `__meta` is
what makes it work: a collapsed section stating its own size lets a person choose without
opening it.

### `.st-steps`

**Applies to** a short ordered sequence a person moves through once.

**Does not apply to** peer surfaces you may revisit freely — that is `.st-tablist`. The two
differ on revisitability, order and what "current" implies, which is why a modifier would have
been wrong.

**`--failed` is not optional.** Sequences fail.

**Expression since 20 Aug 2026 (E-13):** border-top state coding -- a 2px leading edge plus text
weight carries the state; the number circles are retired and `__pos` states position in words,
which was always the accessible channel.

### `.st-lineage` — a directed dependency walk

**Applies to** a set where a change to one element propagates to others and **distance changes
the decision.** Data lineage, formula auditing, build dependencies, permission inheritance.

**Distance is the structure, not an inference from indentation.** Each hop is a `<section>` with
a real heading and its own count, so a screen-reader user gets "Hop 2, 7 items" as a landmark.
Nodes are a `<ul>`, so the count is announced. Expansion is a `<button>`, not a click handler.

**`__horizon` is a band, not a footnote.** The chain always exists; only the view is staged. Same
for `__more` within a band — a band that shows part of a set states the rest, inside the
component. See the governing rule in `patterns.md`.

**`__node--restricted` and `__horizon` wear `.st-empty`'s dashed `border-strong` edge**, because
they are the same semantic: a stated hole. That is what keeps them from reading as an error,
since `.st-empty--error` separates failure by going solid in `support-error`.

**Never `.st-truncate` on `__desc`.** The description is what makes the chain meaningful rather
than structural. Above 672px it shares the row; below it takes its own line and wraps.

**When it almost fits:** the set is small and distance is irrelevant. That is a flat neighbour
list — a `collection`. A `.st-disclose` answers what is *inside* something; a walk answers what a
change *reaches*.

### `.st-lineage--path` — one route, end to end

**Applies to** tracing a single value through the calculations that produce it: this line item,
into that formula, into that total, out to the number somebody reads. The hop bands answer *what
is one step away and how far does this reach*; the path answers *how does this number get made*.
A dependency trace says what is connected, and only a calculation trace explains a figure.

**Each `__step` carries its `__rule` — the formula, verbatim — and its `__via`**, which names how
the value enters the next one. "Summed into" and "multiplied by the monthly rate into" are
different facts, and a chain that says only "connected to" has not explained anything.

**Both ends are marked, and both are findings.** `--terminal` downstream is an output nothing
consumes; `--origin` upstream is an input nothing feeds. Say so in words as well — the dot is a
second channel, never the only one.

**When it almost fits:** you want `.st-steps`. It has the same shape and the wrong meaning — a
stepper encodes *your progress through a task*, with things done, current and not yet reachable,
where every node in a route is equally settled and none is current. Wearing it would inherit
revisit semantics that are false here.

### `.st-codeblock` — machine text, as a block

**Applies to** a formula, a payload, a config fragment, an error response quoted verbatim —
anything monospaced that occupies its own line or more.

**`.st-code` is the inline one and does not substitute.** It sets a font, a size and a letter
spacing, and nothing else: no surface, no gutter, no scroll. A six-line payload wearing it reads
as prose in a monospace font, which was measured as the least readable thing in an artefact.

**Caption it with `__head`.** Machine text with no label is a puzzle — the reader has to work out
what they are looking at before they can begin reading it. `__meta` takes the size or the count.

**Keys inside a payload take `<b>` and get weight, never colour.** A syntax palette inside a
product that also uses colour for meaning is two vocabularies competing for one channel.

**`--line` for a single expression**, which wraps rather than scrolls, because one line has
nowhere to scroll to.

### `.st-pager` — position in a set that cannot be scrolled

**Applies to** any collection too large to scroll through: 312 modules, 68,402 list members. A
scroll bar is not a position — you cannot return to "about two thirds down", quote it to a
colleague, or tell whether the set ended or the fetch did.

**State a RANGE and a total, never a page number alone.** "1–5 of 312" answers a question that
"page 1 of 63" does not. `__position` is the anchor: it is the middle of the row, it is centred,
and it reserves its width so the row cannot reflow as the numbers change — the whole point is
that Next is still under the cursor when you go to press it again.

**A set still being counted is a real state**, not an error. `__position--counting` says the
position is known and the total is not yet.

**When it almost fits:** the list has forty rows. Then it scrolls, and a pager is furniture.

### `.st-shell__panel` — the dismissible reveal pane

**Applies to** a list whose rows carry more than a row can hold, where **losing your place in the
list is a real cost.** A queue of 247 is the case that names it.

**Region `app.detail`. Never persistent** — the grid column does not exist unless a row is
selected, which is the whole difference between this and the right panel the shell spec declines.

**The dismiss control is required.** A pane that opens on selection and cannot be closed is a
third column wearing a panel's clothes.

**Body scrolls, head and foot hold** — the same anatomy `.st-modal` uses, because it is the same
problem: a fixed-height surface whose middle grows.

**Below 1056px it becomes a sheet stacked in `grid-area: main`**, so it covers the list and leaves
the header, status band and rail reachable. A product whose users habitually work narrow is
therefore choosing to cover the thing they were comparing — that is a frame decision, not a
component one.

**It is tabbed, and the tabs are the modifier.** When the situation changes, the panel gains or
loses a tab rather than changing arrangement — one anatomy, every situation. **The cap is three**:
three fit a 320px column, four are cramped, and a fourth is the point at which a panel is being
asked to be a page. A situational tab counts toward the three.

**A tab holding something unanswered carries `data-attention`, and the panel opens on it.** The
amber dot is the second channel; the tab's own label is the first, which is why the label must name
the thing ("Decision") rather than being a glyph. Opening on some other tab would put the decision
behind a click, which is the whole objection to tabbing it in the first place.

**`.st-panel__box` is for the ONE fragment that must read as an object** — a formula, a quoted
definition under review, a withheld value. Not every section: three borders in a 320px column is
what makes a panel unreadable. It is **recessed** (`layer-accent-01`, no elevation, radius-md)
where `.st-tile` is **raised** (white, `elevation-01`, radius-xl), because a tile means *a record*
and a box means *a fragment*. If you want a title on it rather than a caps label, you wanted a tile.

**When it almost fits:** the detail must be decided before anything else can happen. A panel has
no scrim and cannot compel, so that is `.st-modal`.

### `.st-keycode`

**Applies to** a machine-readable string a person has to read aloud or transcribe — a pairing
code, a one-time passcode, a short reference ID. Monospace, wide tracking, slashed zero,
tabular figures, because the requirement is that it survives being read down a phone line.

**Does not apply to** an identifier the person only ever copies. That is `.st-code`.

### `.st-compare` / `.st-cmp-*`

**Prose** (`.st-compare`) for two whole versions where a person picks one. The attribution line —
who wrote it, when, against which version — is what makes it a comparison rather than two cards.

**Tabular** (`.st-cmp-*`) for before-and-after on a shared key, inside an ordinary `.st-table`.
Cell modifiers rather than a component, because the table already carries sorting, striping and
row height.

**An unchanged row renders.** Hiding it makes "no change" and "not included" look identical.
`--unread` exists because a blank cell reads as zero.

---

## Links inside coloured surfaces

**Inside any surface that already carries its own semantic colour, a link inherits that colour
and carries an underline.** The system does this for you on `.st-statusband`, `.st-note`,
`.st-toast`, `.st-empty`, `.st-step__text` and `.st-tag`.

The reason is worth knowing, because it is the third time one bug appeared in three different
places. An unstyled `<a>` takes `--st-link-primary`. On a green-primary brand, a link inside a
*blocked* status therefore renders in the action hue — a failure that reads as an action. That
is the role collision the token layer was fixed to remove, walking back in at composition level.

**When it almost fits:** you want the link to stand out inside a notification. It should not.
The surface is already carrying the emphasis; a second emphasis competes with it, and on a
status surface the competition is with meaning rather than with attention.

---

## Utilities

Five, and the number is the point: **a utility may only express something the token layer already
contains.** No new values, no new colours, nothing that is a design decision wearing a utility's
clothes. Every one came from measured field use rather than from anticipation.

| Class | Use it for |
|---|---|
| `.st-num` | Tabular numerals on any cell or figure. Columns of numbers that do not align are the most common way a dense product stops looking like a system |
| `.st-truncate` | Single-line truncation with an ellipsis |
| `.st-text-secondary` | Secondary emphasis **inside** a sentence — the eight type classes set size and weight, never colour |
| `.st-text-helper` | The same, one step quieter |
| `.st-visually-hidden` | A name that is read and not drawn — a checkbox or actions column header. Added 23 Aug 2026 (E-22) after the technique was found hardcoded in exactly one place |

**When it almost fits:** the utility you want is not here. That is a finding, not a licence.
An open-ended colour-utility set is how a token system becomes a class soup, which is why there
are two text colours and not six.

## Tables that navigate

`.st-table__rowlink` styles a row that navigates — cursor, focus ring, and a full-row hit area
from the link inside it.

**It styles the pattern; it does not create it.** The row must contain a real `<a>`. A row made
clickable with a JavaScript handler and no link is unreachable by keyboard and invisible to a
screen reader, and the class will happily make it *look* correct, which is worse than it looking
broken.

`.st-table__sort` is the button inside `th[aria-sort]`. Without it, native button chrome shows
through a styled header cell.

---

## Reporting an invention

When you build something beside a component that almost fit, send it to the Strata project with:
the semantic pattern it resolves, which regions consume it and how many, the markup and CSS as
built, the rules that matter and why, and an honest assumptions table — including whether you
checked the inventory first.

Price it knowing the CSS is the small half. Every component needs contrast pairs, dark-theme
verification, `forced-colors` handling, an axe pass, a resolution-map row and a provenance block.
Budget 2–3× the CSS.
