# The shell spec

The application frame: what persists across every screen. Read this before adding a region.

## The test

**Every region must be answerable from an artefact the pipeline already produces.** If a
region's presence cannot be derived from the screen set, the flows, the personas or the scale
answers, it is not fit for purpose — it is decoration, and it will fill with whatever nobody else
had a home for.

This is the difference between this shell and Carbon's. Carbon's has a notification bell and a
product switcher because IBM has notifications and a product portfolio. Neither is derived from
anything about the product being built. A shell copied the same way inherits IBM's org chart.

## What a shell is for

Three questions the screens cannot answer, because the answer has to be true everywhere:

1. **Where am I** — in the product, and in the hierarchy.
2. **What needs me** — work that has arrived since I last looked.
3. **How do I get to what's next.**

That is the same list the wireframe skill gives for a landing page. **A shell is the landing-page
job made persistent.** Useful as a check: a region not serving orientation, attention or routing
should be cut.

## Regions

Region classes carry the same codes the region register uses, so a functional requirement written
elsewhere can point at one.

| Region | Class | Job | Present when |
|---|---|---|---|
| `app.identity` | `.st-shell__brand` | Whose product this is, which product | Always |
| `app.primary-nav` | `.st-shell__nav` | Top-level routes | Always |
| `app.locator` | `.st-crumb` | Where in the hierarchy I am now | Always |
| `app.content` | `.st-shell__main` | The page | Always |
| `app.account` | `.st-shell__account` | Who I am acting as, and how to leave | Always |
| `app.work-waiting` | `.st-waiting` | What has been handed to me | **Any flow crosses personas** |
| `app.secondary-nav` | `.st-shell__rail` | Within-section routes | **Nav depth ≥ 2** |
| `app.transient` | `.st-toasts` | System messages that pass | A `notification-transient` region exists |
| `app.subject-state` | `.st-statusband` | The state of the thing being worked on | **Product state persists across screens and changes what to trust** |
| `app.utility` | `.st-shell__util` | Search, help, settings | **Cap of four.** Each needs a named reason |
| `app.detail` | `.st-shell__panel` | What a selected row could not carry | **A list and its detail are read together.** Opens on selection, closes on dismiss — never persistent |

### `app.work-waiting` is the one that justifies the whole approach

It has no Carbon equivalent, and it is derived rather than borrowed. `design-interaction-flows`
forces three answers at every persona handoff: *what tells the next person there is something
waiting, what do they see when they arrive, what happens if they never act.* The first has
nowhere to live except the shell, because it is the only region that persists across screens.

So this renders **only if a flow actually crosses personas.** Carbon gives you a bell because IBM
has notifications; this gives you a handoff surface because your flows have handoffs — and when
they do not, it is absent rather than empty. An empty bell is the thing nobody looks at.

Work waiting is **not a status**. It is neither good nor bad, it is yours. Rendering it in a
status colour spends the alert budget on routine work. `--due` adds a warning border only when
something has actually aged past its point.

### `app.subject-state` — the tenth region, and how it was found

The first nine covered the product, the work, the worker and the page. They did not cover **the
state of the thing being worked on**: how stale the extracted copy is, whether writing is
currently barred, whether the last write verified. A field engagement reported three such regions,
correctly argued they were none of `app.work-waiting` (nothing is waiting on the person),
`app.utility` (not navigation) or `app.account` (not the worker) — and noted that they *passed*
this spec's own derivation test while having no slot to pass into.

That is a hole in the region set, not a misuse of it, so the region exists now.

**It belongs in the frame, not in content.** The engagement put it at the top of `app.content`,
which works and uses only system classes. But the test is: if a fact must be true on every screen
*and changes what a person should trust about what they are reading*, a per-screen home is the
wrong home. Staleness is exactly that — the number on the page is not wrong, it is old, and that
is not a property of the number.

**Most products have none of this and should render nothing.** Present only where such state
exists, persists, and changes how the content should be read. A band that always says "everything
is fine" is a band nobody reads on the day it says otherwise.

Never colour alone: the dot is an affordance and the words carry the meaning.

## Parameters

A shell that fits is configured, not chosen. Each parameter has an owner upstream.

| Parameter | Answered by | Default |
|---|---|---|
| Nav depth (1 / 2 / 3) | `clarify-nonfunctional-scale` | 2 |
| Persona handoffs exist | `design-interaction-flows` | derived |
| Density (comfortable / compact) | `clarify-nonfunctional-scale` | comfortable |
| Multi-product switcher | Commercial | **off, and not built** |
| Themes | Binding | light + dark |

**Depth is a recorded answer, not a hardcoded limit.** The rail supports one level of nesting.
Depth 3 requires a named override and almost always means the answer is page-level tabs or a
different screen split. Carbon hardcodes its two-tier maximum, which means the first client with
a four-level hierarchy fights the shell and re-invents it — the erosion mechanism, at frame
scale.

**Drill-downs are not nav depth.** Depth counts distinct navigable *sections* — routes a person
chooses between — not how far they can drill into a record from within a screen. Drilling is
progressive disclosure and belongs to the page: `.st-crumb` in-page, detail panels, `disclosure`.
A depth answer derived only from drill paths is depth 1, renders `--task` with no rail, and the
locator lives in the page rather than the frame. This is a field finding: a scale answer of
"two levels" that meant drill levels once produced a rail with nothing to hold, caught when the
flows showed no second navigable section. When recording the depth parameter, state which kind
of level was counted.

**A region that scrolls independently must opt out of the row's stretch.** A shell region is a
grid item in a `1fr` row, so it stretches to the row's height: on a 3,600px page the rail was
3,600px tall and `overflow-y: auto` never engaged. **"It has `overflow: auto`" is not evidence
that anything scrolls.** Such a region needs `align-self: start`, `position: sticky` below the
header, and an explicit `calc(100vh - offset - header)` height. Found 23 Aug 2026 in **both**
`app.secondary-nav` and `app.detail` — the rail's sticky group headers would have been inert and
the panel's footer sat at the bottom of the page rather than the pane. Measure
`scrollHeight > clientHeight` before believing a scroll container exists.

**The shell owns density.** One attribute on the root; components read `--st-density-control`,
`--st-density-row` and `--st-density-pad` and never the raw size scale. This is the fix for
correct component usage that still looks wrong: a product rendering 12,000 rows was compressed by
hand throughout because there was nowhere to declare that it was dense.

```html
<div class="st-shell st-shell--explorer" data-density="compact">
```

## Two variants, one region set

The products differ on which of the three jobs dominates.

| | `.st-shell--task` | `.st-shell--explorer` |
|---|---|---|
| Shape of work | Work arrives, you clear it | You navigate a structure |
| `app.work-waiting` | Prominent — full pill, count and label | Badge — count only, label to screen readers |
| `app.locator` | Hidden — there is no hierarchy to be lost in | Prominent |
| `app.secondary-nav` | Usually absent | Usually present |
| Typical products | Approval, review, exception handling | Planning models, registries, hierarchies |

Same regions, different prominence. One shell trying to serve both gives you a rail nobody uses
and a queue nobody finds.

## What is deliberately absent

**No product switcher.** It answers a multi-product portfolio, and it is the single most
identifying element of Carbon's header.

**No *persistent* right panel.** Carbon's exists for system-level content most engagements do not
have, and a persistent empty panel is an invitation. **Amended 23 Aug 2026 (E-26):** this was
written as "No right panel", which is wider than the reason given for it. A panel that opens on
row selection and closes on dismiss is never empty, because it does not exist unless a row is
selected — so the reason never covered it. `app.detail` is now a region for the dismissible case.
The persistent Carbon panel is still declined, for the reason originally given.

**No global search unless a `search` region exists in the register.** Search in the shell is a
claim that search works across the whole product. Make it when it is true.

**No IBM chrome.** Anatomy taken, identity not. Apache-2.0 grants no trademark rights, and the
header is the most trade-dress-loaded part of Carbon.

## The erosion guard

The shell is the most attractive dumping ground in any product — it is persistent, so everything
wants to live there. Two hard rules:

**`app.utility` is capped at four, each with a named reason.** No cap means it fills.

**A project adding a class to the shell is a reportable finding**, not a local fix. One
engagement did exactly this — `.st-shell__header { top: 44px }`, to clear a review harness bar —
reported it, and the answer was that a harness offset should never have needed an override.
`--st-shell-offset` now exists for it. That is the loop working: the override was legitimate, the
need for it was not. That is the
`.tile`-used-47-times mechanism at frame scale, and reporting it is how you find out the shell is
wrong rather than watching it get quietly replaced.

## Accessibility floor

- `.st-skip` is present and **visible on focus**. A skip link that stays hidden when focused is
  worse than none, because it steals a tab stop and gives nothing back.
- `app.primary-nav` and `app.secondary-nav` mark the current item with `aria-current="page"`, and
  carry weight and a border as well as colour so the state survives greyscale.
- `.st-crumb` states position in text, not only by highlight.
- The rail is hidden below 672px and opened with `data-open="true"`; the header nav must remain
  reachable at that width.
