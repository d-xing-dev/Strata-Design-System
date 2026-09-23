# Composition conventions

How the space between components is spent. `USAGE.md` says when each component applies;
`RESOLUTION-MAP.md` says which component renders which semantic pattern; this file says how
composed surfaces stay readable — the rules a per-screen composition spec cites instead of
restating.

**Provenance.** These conventions are `added`, not derived from Carbon — Carbon publishes a
spacing scale and a grid but no rules for spending them, which is part of why two competent
builders working from identical tokens produce products that do not look alike. They derive
instead from Gestalt grouping (proximity and alignment are perceived as belonging, before
thought) and from the readability principles the UX pipeline reasons against. `why`: the token
and component layers guarantee the parts; without stated conventions, every composition re-decides
the grammar, and the products stop looking like siblings.

**What this file is not.** It is not a build check and must not become a fake one. The contrast
audit can composite colours; nothing in a build can see whether the eye lands in the right place.
These conventions are enforced by the pipeline's looking-gate — a person or agent judging a
rendered screen against a composition spec — and documented here so the spec and the judgement
share one vocabulary.

## The gap hierarchy

**The gap inside a group is always at least one visible spacing step smaller than the gap
between groups.** Grouping is the message; spacing is the medium. When within-group and
between-group gaps are equal, the layout asserts that everything is one group, and the viewer's
perceptual system files the screen as noise.

Default pairings from the scale, by density:

| Context | Within a group | Between groups |
|---|---|---|
| Comfortable | `--st-space-05` (16) | `--st-space-06` (24) or `--st-space-07` (32) |
| Comfortable, major page bands | — | `--st-space-08` (40) with `.st-hr` where separation must survive scrolling |
| Compact | `--st-space-04` (12) | `--st-space-06` (24) |

Set gaps with `--gap` on `.st-stack` / `.st-row` / `.st-grid` instances — never with bespoke
margin rules, which is the 24-structural-classes failure arriving through spacing.

## Alignment edges

**Regions on a screen share declared edges; a declared edge is a checkable fact.** A composition
spec states which regions sit on a common left edge and which bands share a top edge; the render
either honours the declaration or records a deviation. Within a horizontal band, components align
to a common text baseline — a stat row beside a table header aligns baselines, not box tops,
because the eye reads type, not boxes.

The grid provides the edges: regions spanning `.st-col` boundaries inherit alignment for free,
which is why a two-up that is "not quite on the grid" (`.st-row` + `.st-fill`) should become a
grid row the moment anything else must align with it.

## One focal point

**One primary per screen.** The anchor region — decided upstream in the composition intent, from
the dominant job or the screen's flow position — is the one place visual weight concentrates:
scale, position, or contrast, applied once. Everything else is secondary or tertiary, and the
discipline is subtractive: the anchor is made primary mostly by *not* emphasising its neighbours.
Two primaries is not double emphasis, it is no emphasis with extra ink — attention is serial, and
a screen that emphasises two things directs the eye to neither.

Status colour does not compete for the focal point: a status is noticed *when present*
(`status-indicator` carries shape and text as well as colour), not enthroned as the page's
subject. Work-waiting is not a status, and neither is the anchor.

## Zoning and disclosure

What is open and what is behind a `disclosure` is decided by the composition intent from the
scale answers, and the split follows one rule: **visible-by-default is for what the screen's
question needs; on-demand is for what a minority of visits need.** A `__meta` line on every
collapsed section states its size, so choosing to open it is informed. Never zone the anchor
behind a disclosure — a screen whose subject is collapsed has no subject.

## Density is not composition

Compact mode changes the values the conventions resolve to (the table above), never the
conventions themselves: the gap hierarchy, the declared edges and the single focal point hold at
every density. Declaring `data-density="compact"` and then also tightening gaps by hand is
double-compression — the 12,000-row failure in its modern form.

## Deviation

A composition may override any default here — a screen's needs outrank a convention — but the
override is **named in the spec's deviation budget with its reason**, and an unnamed override
found at the looking-gate is a finding. The budget is small by nature: polish is the deviation
budget spent deliberately, and a screen deviating everywhere has no baseline left to deviate
from.

## Precedents

The reference page (`reference.html`) is the artefact that transmits composition — worked
examples, not rules. A field composition that passes the looking-gate and reads well may be
submitted as a precedent through the same channel as an invented component: spec, verdict,
consumer count, adjudicated by the system owner, added to the reference build (`build/reference.py`)
rather than hand-edited into dist. Precedents are how these conventions grow evidence without
hardening into page templates — a precedent is an example with provenance, not a prescription.
