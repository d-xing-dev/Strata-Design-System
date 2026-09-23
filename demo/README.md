# demo/ — one ordinary screen

**Generated, 23 Aug 2026.** `demo/build.py` writes everything else in this folder. Edit the
script and re-run it; a hand-edit to the HTML is lost on the next run, and it also breaks the one
thing this folder is for.

```
python3 demo/build.py        # after dist/scaffold and dist/deloitte have both been built
```

## What this is, and how it differs from reference.html

`dist/*/reference.html` is deliberately **maximal** — every component on one surface, so a builder
can see the whole vocabulary and copy the construction. It answers *what exists*.

This answers a different question: **what does an ordinary screen look like when it only uses what
it needs?** A payment release queue, task shell, no rail. Roughly a third of the system appears on
it, and the components that are absent are absent because the screen has no job for them. That
distinction is the point — a system is judged by its restraint as much as its inventory.

## The construction, and why it is built this way

**One markup source, two renders.** `BODY` in `build.py` is written once. A brand render is a
different `<link>` and nothing else. Two hand-copied files could drift into looking alike by
accident, which would demonstrate nothing; generating both from one source means the swap either
holds or visibly does not.

**No page-specific CSS in the product.** The only rules either file adds are the review strip
across the top, which carries `data-review` and is skipped by the gate and deleted on build. If a
demo screen needs bespoke layout CSS, the layout layer does not work — the same test
`reference.html` applies to itself.

**`--st-shell-offset` is set, not overridden.** The review strip pushes the sticky header down
through the system's own documented hook. Note that the strip must also take flow space
(`position: sticky`, not `fixed`): the offset moves the sticky *threshold*, it does not move the
shell, so a `fixed` bar leaves the header stuck 44px down over the status band. See the findings
below.

## What the screen exercises

| Region / pattern | Rendered as | Why it is here |
|---|---|---|
| `application-shell` | `.st-shell--task .st-shell--norail` | Work arrives and is cleared. Depth is 1 — the flows produce drill paths, not navigable sections, so no rail and no locator |
| `app.work-waiting` | `.st-waiting--due` | The queue crosses personas: a preparer hands to an approver |
| `app.subject-state` | `.st-statusband` | Balance staleness and the same-day cut-off persist across screens and change what to trust |
| `app.detail` | `.st-shell__panel` | 247 rows; losing your place is a real cost |
| `collection` | fork **R1a** → `.st-table` | Shared comparable fields, scanned across |
| `collection-bulk-actions` | `.st-table__batchbar` | Three rows selected |
| `summary-tile` | `.st-stat` ×4, none `--lead` | The **table** is the anchor. A lead stat plus a full-width table is two primaries, which is no primary |
| `notification-inline` | `.st-note--warning` | It persists and needs a response, so it must not be able to vanish — never a toast |
| `search` + `filter-set` | `.st-search`, `select.st-field`, dismissible chips | The count is part of the component |
| `status-indicator` | `.st-tag` dot-chips | Five states, each carrying its meaning in words |
| staged view | `<tfoot>`: *235 more in this queue* | The staged-view rule: the beyond-count lives **inside** the component |

## Appearance axes: default, deliberately

No `data-appearance` is declared. Both axes (`chrome-coloured`, `table-head-tint` /
`table-head-strong`) resolve through the **blue ramp** — `--st-blue-20`, `--st-blue-80` — rather
than through a role. On the deloitte brand that draws a blue header above a green batch bar and a
green primary button. That is the E-25 rail defect one layer up, and shipping the demo wearing it
would teach the wrong thing. Recorded here rather than worked around silently.

## Findings raised by building this

1. **`--st-shell-offset` needs a companion note in `SHELL-SPEC.md`.** The offset alone does not
   clear a harness bar. A `position: fixed` bar takes no flow space, so the shell still starts at
   y=0, the header sticks 44px down, and it paints over `app.subject-state` — the band is invisible
   and nothing errors. The bar must also occupy flow.
2. **`.st-shell--task .st-crumb { display: none }` is unconditional.** SHELL-SPEC's drill rule says
   a depth-1 task product puts the locator *in the page* as `.st-crumb`. That rule and this
   selector contradict each other: an in-page breadcrumb on a task shell renders as nothing.
3. **The gate passes this screen clean** — `production_check.py --require-full`, both brands, both
   themes, three widths, 0 findings.
