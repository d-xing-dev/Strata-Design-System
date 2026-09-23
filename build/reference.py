#!/usr/bin/env python3
"""Emit dist/<brand>/reference.html — the assembled reference page.

This is the only artefact that transmits *composition*. Prose cannot. A component
gallery cannot either: it shows every part correctly and still leaves page rhythm,
chrome weight, heading hierarchy, section separation and density undetermined —
which is where two competent builders working from identical tokens diverge.

It must contain, or it does not do its job:
  - a full application shell
  - a collection at realistic length, not three demo rows
  - a form with helper text and a validation state
  - a status treatment and a notification
  - real body copy at real length
  - **at least one region in a FAILURE state, carrying a link**

That last one was added after a field engagement pointed out that the band on this
page showed three items all reading "fine" -- demonstrating the component on the
day nothing is wrong, when the shell spec's own warning is that a band which
always says everything is fine is a band nobody reads on the day it says
otherwise. It also hid a real defect: an unstyled <a> inside a blocked status took
the action colour, so a failure rendered in the action hue.

The rule that follows: **the reference page teaches the harder case.** A component
shown only in its happy state teaches half of itself and hides the half where the
mistakes are.

Consuming agents: read this before writing any layout CSS. Re-lay one screen
against its rhythm and diff before propagating.
"""

from __future__ import annotations
import os
import build as B

DIST = B.DIST

ROWS = [
    ("SAL03.uplift_pct",     "Sales",      "Uplift %",             "2.5%",  "3.1%",  "up",   "0.6pp", "Reviewed"),
    ("SAL03.base_volume",    "Sales",      "Base volume",          "1,204", "1,204", "same", "",      "Reviewed"),
    ("SAL07.channel_mix",    "Sales",      "Channel mix",          "44.0%", "51.2%", "up",   "7.2pp", "Needs you"),
    ("OPX11.headcount",      "Operations", "Headcount",            "318",   "302",   "down", "16",    "Needs you"),
    ("OPX11.overtime_rate",  "Operations", "Overtime rate",        "6.4%",  "9.8%",  "up",   "3.4pp", "Needs you"),
    ("OPX14.site_capacity",  "Operations", "Site capacity",        "—",     "88.0%", "",     "",      "Blocked"),
    ("FIN02.fx_eur",         "Finance",    "FX rate EUR",          "1.084", "1.084", "same", "",      "Reviewed"),
    ("FIN02.fx_gbp",         "Finance",    "FX rate GBP",          "0.842", "0.851", "up",   "0.9%",  "Reviewed"),
    ("FIN09.accrual_basis",  "Finance",    "Accrual basis",        "Q-end", "M-end", "",     "",      "Needs you"),
    ("FIN09.tax_rate",       "Finance",    "Effective tax rate",   "24.0%", "24.0%", "same", "",      "Reviewed"),
    ("MKT04.spend_ceiling",  "Marketing",  "Spend ceiling",        "4.2m",  "3.8m",  "down", "9.5%",  "Reviewed"),
    ("MKT04.attribution",    "Marketing",  "Attribution window",   "28d",   "14d",   "down", "14d",   "Needs you"),
    ("MKT08.cpa_target",     "Marketing",  "CPA target",           "£31.40","£29.10","down", "7.3%",  "Reviewed"),
    ("SUP01.lead_time",      "Supply",     "Lead time",            "21d",   "26d",   "up",   "5d",    "Needs you"),
    ("SUP01.safety_stock",   "Supply",     "Safety stock",         "12.0%", "12.0%", "same", "",      "Reviewed"),
    ("SUP06.supplier_split", "Supply",     "Supplier split",       "—",     "60/40", "",     "",      "Blocked"),
    ("HRP02.attrition",      "People",     "Attrition",            "11.2%", "13.9%", "up",   "2.7pp", "Needs you"),
    ("HRP02.backfill_lag",   "People",     "Backfill lag",         "34d",   "34d",   "same", "",      "Reviewed"),
    ("HRP05.grade_bands",    "People",     "Grade bands",          "7",     "9",     "up",   "2",     "Reviewed"),
    ("TRE01.hedge_ratio",    "Treasury",   "Hedge ratio",          "75.0%", "80.0%", "up",   "5.0pp", "Needs you"),
    ("TRE01.liquidity_floor","Treasury",   "Liquidity floor",      "18.0m", "18.0m", "same", "",      "Reviewed"),
    ("TRE04.counterparty",   "Treasury",   "Counterparty limit",   "9.0m",  "7.5m",  "down", "16.7%", "Reviewed"),
]

STATUS_TAG = {
    "Reviewed":  "st-tag--green",
    "Needs you": "st-tag--amber",
    "Blocked":   "st-tag--red",
}


def _rows_html() -> str:
    out = []
    for code, area, name, before, after, dirn, delta, status in ROWS:
        if before == "—":
            bcell = '<td class="st-cmp-unread"></td>'
        elif dirn == "same":
            bcell = f'<td class="st-cmp-before st-num">{before}</td>'
        else:
            bcell = f'<td class="st-cmp-before st-num">{before}</td>'
        if dirn == "same":
            acell = f'<td class="st-cmp-same">unchanged</td>'
        elif dirn:
            acell = (f'<td class="st-cmp-after st-num">{after}'
                     f'<span class="st-stat__delta st-stat__delta--{dirn}">{delta}</span></td>')
        else:
            acell = f'<td class="st-cmp-after">{after}</td>'
        out.append(
            f'    <tr class="st-table__rowlink">\n'
            f'      <td><a href="#" class="st-code">{code}</a></td>\n'
            f'      <td>{area}</td>\n'
            f'      <td class="st-truncate">{name}</td>\n'
            f'      {bcell}\n'
            f'      {acell}\n'
            f'      <td><span class="st-tag {STATUS_TAG[status]}">{status}</span></td>\n'
            f'    </tr>'
        )
    return "\n".join(out)


def build_page(css_href: str = "strata.css") -> str:
    needs = sum(1 for r in ROWS if r[7] == "Needs you")
    blocked = sum(1 for r in ROWS if r[7] == "Blocked")
    reviewed = sum(1 for r in ROWS if r[7] == "Reviewed")
    total = len(ROWS)

    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reference page — Strata ({B.ACTIVE_BRAND})</title>
<link rel="stylesheet" href="{css_href}">
<style>
  /* The ONLY page-specific CSS on this file, and it is three declarations.
     That is the point of the page: if a reference page needs bespoke layout CSS,
     the layout layer it is meant to demonstrate does not work. */
  body {{ margin: 0; font-family: var(--st-font-sans); color: var(--st-text-primary); }}
  .ref-note {{ background: var(--st-layer-accent-01); border-bottom: 1px solid var(--st-border-subtle-01);
               padding: var(--st-space-04) var(--st-space-05); font-size: var(--st-type-body-sm-size); }}
</style>
</head>
<body>
<a class="st-skip" href="#main">Skip to main content</a>

<p class="ref-note" data-review><strong>Strata reference page — {B.ACTIVE_BRAND} build.</strong>
One assembled screen, laid out entirely with system classes. Read it before writing layout CSS,
then re-lay one of your own screens against its rhythm and diff before propagating. Nothing on
this page is bespoke except three declarations in the head.</p>

<div class="st-shell st-shell--explorer" data-density="comfortable">

  <header class="st-shell__header" data-region="app.identity">
    <a class="st-shell__brand" href="#">Meridian <small>model governance</small></a>
    <nav class="st-shell__nav" data-region="app.primary-nav" aria-label="Primary">
      <a class="st-shell__navlink" href="#">Overview</a>
      <a class="st-shell__navlink" href="#" aria-current="page">Changes</a>
      <a class="st-shell__navlink" href="#">Registry</a>
      <a class="st-shell__navlink" href="#">Audit</a>
    </nav>
    <span class="st-shell__spacer"></span>
    <a class="st-waiting st-waiting--due" href="#" data-region="app.work-waiting">
      <span class="st-waiting__count">7</span>
      <span class="st-waiting__label">waiting on you</span>
    </a>
    <div class="st-shell__util" data-region="app.utility">
      <button class="st-shell__utilbtn" aria-label="Help">?</button>
      <button class="st-shell__utilbtn" aria-label="Settings">&#9881;</button>
    </div>
    <span class="st-shell__account" data-region="app.account">
      <span class="st-shell__avatar" aria-hidden="true">DX</span>
      <span>D. Xing</span>
    </span>
  </header>

  <div class="st-statusband" data-region="app.subject-state" role="status">
    <span class="st-statusband__item st-statusband__item--stale">
      <span class="st-statusband__dot" aria-hidden="true"></span>
      Extract is 41 minutes old</span>
    <span class="st-statusband__item st-statusband__item--blocked">
      <span class="st-statusband__dot" aria-hidden="true"></span>
      Writing blocked — <a href="#">see why</a></span>
    <span class="st-statusband__item">
      <span class="st-statusband__dot" aria-hidden="true"></span>
      Last write verified 09:38</span>
  </div>

  <nav class="st-shell__rail" data-region="app.secondary-nav" aria-label="Sections">
    <div class="st-rail__group">
      <div class="st-rail__label">This cycle</div>
      <a class="st-rail__link" href="#" aria-current="page">All changes <span class="st-rail__meta">22</span></a>
      <a class="st-rail__link" href="#">Needs you <span class="st-rail__meta st-rail__meta--due">{needs}</span></a>
      <a class="st-rail__link" href="#">Blocked <span class="st-rail__meta">{blocked}</span></a>
      <a class="st-rail__link" href="#">Reviewed <span class="st-rail__meta">{reviewed}</span></a>
    </div>
    <div class="st-rail__group" data-open="true">
      <button class="st-rail__label" aria-expanded="true" aria-controls="rail-areas">
        <svg class="st-rail__chev" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path fill="currentColor" d="M6 3l5 5-5 5z"/></svg>Business areas <span class="st-rail__count">14</span></button>
      <div class="st-rail__items" id="rail-areas">
        <a class="st-rail__link st-rail__link--sub" href="#">Salary and cost <span class="st-rail__meta">34</span></a>
        <a class="st-rail__link st-rail__link--sub" href="#">Employee data <span class="st-rail__meta">18</span></a>
        <a class="st-rail__link st-rail__link--sub" href="#">FX and rates <span class="st-rail__meta">8</span></a>
        <button class="st-rail__more">11 more</button>
      </div>
    </div>
    <div class="st-rail__group" data-open="false">
      <button class="st-rail__label" aria-expanded="false" aria-controls="rail-ref">
        <svg class="st-rail__chev" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path fill="currentColor" d="M6 3l5 5-5 5z"/></svg>Reference <span class="st-rail__count">3</span></button>
      <div class="st-rail__items" id="rail-ref">
        <a class="st-rail__link st-rail__link--sub" href="#">Definitions</a>
        <a class="st-rail__link st-rail__link--sub" href="#">Tolerances</a>
        <a class="st-rail__link st-rail__link--sub" href="#">Sign-off history</a>
      </div>
    </div>
  </nav>

  <main class="st-shell__main" id="main" tabindex="-1">
    <div class="st-container">

      <nav aria-label="Breadcrumb">
        <ol class="st-crumb" data-region="app.locator">
          <li><a href="#">Meridian</a></li>
          <li><a href="#">Q3 close</a></li>
          <li aria-current="page">Changes</li>
        </ol>
      </nav>

      <div class="st-page">

        <div class="st-page__head">
          <div>
            <h1 class="st-heading-md st-page__title">Changes awaiting review</h1>
            <p class="st-body-md st-page__sub">Every value that moved between the last published
              version and the current draft. Anything above its tolerance is flagged for you;
              everything else is shown so that "no change" and "not included" cannot be mistaken
              for each other.</p>
          </div>
          <div class="st-row" style="--gap: var(--st-space-03)">
            <button class="st-btn st-btn--tertiary st-btn--md">Export</button>
            <button class="st-btn st-btn--primary st-btn--md">Publish {reviewed} reviewed</button>
          </div>
        </div>

        <div class="st-steps" data-region="review.progress">
          <div class="st-step st-step--done"><span class="st-step__num">&#10003;</span>
            <span class="st-step__text">Extract<span class="st-step__pos">step 1 of 4</span></span></div>
          <div class="st-step st-step--done"><span class="st-step__num">&#10003;</span>
            <span class="st-step__text">Reconcile<span class="st-step__pos">step 2 of 4</span></span></div>
          <div class="st-step st-step--current"><span class="st-step__num">3</span>
            <span class="st-step__text">Review<span class="st-step__pos">step 3 of 4</span></span></div>
          <div class="st-step st-step--todo"><span class="st-step__num">4</span>
            <span class="st-step__text">Publish<span class="st-step__pos">step 4 of 4</span></span></div>
        </div>

        <section class="st-section">
          <div class="st-grid">
            <div class="st-col" style="--span:16; --span-md:8; --span-lg:4">
              <div class="st-stat st-stat--lead" data-region="review.needs-me">
                <div class="st-stat__figure">{needs}
                  <span class="st-stat__delta st-stat__delta--down">2</span></div>
                <div class="st-stat__label">need your judgement</div>
                <div class="st-stat__meter st-stat__meter--warn"><i style="width:32%"></i></div>
              </div>
            </div>
            <div class="st-col" style="--span:16; --span-md:8; --span-lg:4">
              <div class="st-stat">
                <div class="st-stat__figure">{reviewed}</div>
                <div class="st-stat__label">reviewed and ready</div>
                <div class="st-stat__meter"><i style="width:50%"></i></div>
              </div>
            </div>
            <div class="st-col" style="--span:16; --span-md:8; --span-lg:4">
              <div class="st-stat">
                <div class="st-stat__figure">{blocked}</div>
                <div class="st-stat__label">blocked upstream</div>
              </div>
            </div>
            <div class="st-col" style="--span:16; --span-md:8; --span-lg:4">
              <div class="st-stat st-stat--unavailable">
                <div class="st-stat__figure">not yet run</div>
                <div class="st-stat__label">tolerance breach count</div>
              </div>
            </div>
          </div>
        </section>

        <div class="st-note st-note--warning" role="status" data-region="review.upstream-notice">
          <div>
            <strong>Two values could not be read from the source model.</strong>
            They are shown as unread rather than zero, and they cannot be reviewed until the
            upstream extract completes. The owning team has been notified automatically.
          </div>
        </div>

        <section class="st-section">
          <div class="st-section__head">
            <h2 class="st-heading-sm">All changes</h2>
            <span class="st-helper">Sorted by area, then code</span>
          </div>

          <div class="st-search" data-region="review.search">
            <label class="st-search__field">
              <span class="st-search__icon" aria-hidden="true">&#9906;</span>
              <span class="st-lbl">Find a value</span>
              <input class="st-field" type="search" placeholder="Search {total} changed values"
                     aria-describedby="ref-count">
            </label>
            <div class="st-search__count" id="ref-count" aria-live="polite">
              <b>{total}</b> in scope
            </div>
          </div>

          <div class="st-table-wrap" style="margin-top: var(--st-space-05)">
          <table class="st-table st-table--zebra" data-region="review.change-table">
            <caption class="st-helper" style="text-align:left; padding: var(--st-space-04)">
              Before and after on a shared key. Unchanged rows are shown, not hidden.
            </caption>
            <thead>
              <tr>
                <th scope="col" aria-sort="ascending">
                  <button class="st-table__sort" type="button">Code
                    <svg class="st-table__sortarrow" viewBox="0 0 12 12" aria-hidden="true">
                      <path fill="currentColor" d="M6 2l4 6H2z"/></svg></button></th>
                <th scope="col"><button class="st-table__sort" type="button">Area
                    <svg class="st-table__sortarrow" viewBox="0 0 12 12" aria-hidden="true">
                      <path fill="currentColor" d="M6 2l4 6H2z"/></svg></button></th>
                <th scope="col">Value</th>
                <th scope="col">Published</th><th scope="col">Draft</th><th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
{_rows_html()}
            </tbody>
          </table>
          </div>
        </section>

        <section class="st-section">
          <div class="st-section__head"><h2 class="st-heading-sm">Two versions of the definition</h2></div>
          <div class="st-compare" data-region="review.definition-conflict">
            <div class="st-compare__panel">
              <div class="st-compare__label">Yours
                <span class="st-tag st-tag--outline st-tag--sm">unsaved</span></div>
              <p class="st-compare__body st-body-sm">Uplift is applied to the base volume after
                seasonality but before channel mix, so a change to the mix does not compound into
                the uplift. This matches how the planning team has always described it in
                workshops, and it is the reading the current spreadsheet implements.</p>
              <p class="st-compare__attrib">d.xing · edited 09:41 · against version 7</p>
            </div>
            <div class="st-compare__panel st-compare__panel--winning">
              <div class="st-compare__label">Published
                <span class="st-tag st-tag--green st-tag--sm">in force</span></div>
              <p class="st-compare__body st-body-sm">Uplift is applied after channel mix, so the
                two interact. This is what the model actually computes today, and it is why the
                Q2 reforecast moved when the mix was corrected. If the definition above is the
                intended behaviour, the model is wrong rather than the definition.</p>
              <p class="st-compare__attrib">a.okafor · published 12 Jun · version 7</p>
            </div>
          </div>
        </section>

        <section class="st-section">
          <div class="st-section__head"><h2 class="st-heading-sm">Detail on demand</h2></div>
          <p class="st-body-sm st-text-secondary" style="margin:0 0 var(--st-space-04)">The walk
            answers how far a consequence reaches; the disclosures below it answer what is inside
            something. Distance is the reason they are different components.</p>
          <div class="st-lineage st-lineage--upstream" data-region="review.lineage">
            <div class="st-lineage__origin">
              <span class="st-code">CST02</span>
              <span>Salary Cost GBP</span>
              <span class="st-lineage__desc">What feeds this value, three hops upstream</span>
            </div>
            <section class="st-lineage__hop" aria-labelledby="ref-hop-1">
              <h3 class="st-lineage__hoplabel" id="ref-hop-1">Hop 1
                <span class="st-lineage__hopcount">2 items</span></h3>
              <ul class="st-lineage__nodes">
                <li class="st-lineage__node">
                  <a class="st-code" href="#ref-hop-1">FIN02</a>
                  <span class="st-lineage__desc">Exchange rates, published monthly by Finance</span>
                </li>
                <li class="st-lineage__node st-lineage__node--open">
                  <button class="st-lineage__node-toggle" aria-expanded="true" aria-controls="ref-nest-sup06">
                    <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path fill="currentColor" d="M6 3l5 5-5 5z"/></svg><span class="st-visually-hidden">Hide what feeds SUP06</span>
                  </button>
                  <a class="st-code" href="#ref-hop-1">SUP06</a>
                  <span class="st-tag st-tag--amber st-tag--sm">last run Tuesday</span>
                  <span class="st-lineage__desc">Supplier split, which is why the published value
                    reads as unread rather than zero</span>
                  <div class="st-lineage__nest" id="ref-nest-sup06">
                    <h4 class="st-lineage__hoplabel">Feeding SUP06
                      <span class="st-lineage__hopcount">2 items</span></h4>
                    <ul class="st-lineage__nodes">
                      <li class="st-lineage__node">
                        <a class="st-code" href="#ref-hop-1">SUP01</a>
                        <span class="st-lineage__desc">Supplier master, refreshed nightly</span>
                      </li>
                      <li class="st-lineage__node st-lineage__node--restricted">
                        <span class="st-code">PAY09</span>
                        <span class="st-lineage__desc">Restricted — the reference is visible and the
                          content is withheld. This is a declared hole, not a missing record.</span>
                      </li>
                    </ul>
                  </div>
                </li>
              </ul>
            </section>
            <section class="st-lineage__hop" aria-labelledby="ref-hop-2">
              <h3 class="st-lineage__hoplabel" id="ref-hop-2">Hop 2
                <span class="st-lineage__hopcount">7 items</span></h3>
              <ul class="st-lineage__nodes">
                <li class="st-lineage__node">
                  <a class="st-code" href="#ref-hop-2">FIN09</a>
                  <span class="st-lineage__desc">Accrual basis, published monthly</span>
                </li>
                <li class="st-lineage__node">
                  <a class="st-code" href="#ref-hop-2">OVR04</a>
                  <span class="st-lineage__desc">Manual override, expires 30 Sep</span>
                </li>
              </ul>
              <button class="st-lineage__more st-btn st-btn--tertiary st-btn--sm">5 more at this hop</button>
            </section>
            <div class="st-lineage__horizon">
              <h3 class="st-lineage__hoplabel">Beyond the horizon
                <span class="st-lineage__hopcount">41 items</span></h3>
              <button class="st-btn st-btn--tertiary st-btn--sm">41 more, 4 hops and further</button>
            </div>
          </div>
          <details class="st-disclose" data-region="review.history">
            <summary>
              <svg class="st-disclose__chev" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true">
                <path fill="currentColor" d="M6 3l5 5-5 5z"/></svg>
              <span class="st-disclose__title">Change history</span>
              <span class="st-disclose__meta">18 entries</span>
            </summary>
            <div class="st-disclose__body st-body-sm">Every edit since the last publication, with
              who made it and what it replaced.</div>
          </details>
          <details class="st-disclose st-disclose--empty" data-region="review.attachments">
            <summary>
              <svg class="st-disclose__chev" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true">
                <path fill="currentColor" d="M6 3l5 5-5 5z"/></svg>
              <span class="st-disclose__title">Attachments</span>
              <span class="st-disclose__meta">none</span>
            </summary>
          </details>
        </section>

        <section class="st-section">
          <div class="st-section__head"><h2 class="st-heading-sm">Record your decision</h2></div>
          <div class="st-grid">
            <div class="st-col" style="--span:16; --span-lg:8">
              <div class="st-stack">
                <div class="st-formitem">
                  <label class="st-lbl" for="ref-reason">Reason for accepting</label>
                  <input class="st-field" id="ref-reason" aria-describedby="ref-reason-help">
                  <div class="st-help st-helper" id="ref-reason-help">Visible to whoever reviews this
                    after you. One sentence is enough.</div>
                </div>
                <div class="st-formitem">
                  <label class="st-lbl" for="ref-tol">Tolerance applied</label>
                  <input class="st-field" id="ref-tol" value="0" aria-invalid="true"
                         aria-describedby="ref-tol-err">
                  <div class="st-msg st-msg--error st-helper" id="ref-tol-err">
                    A tolerance of zero flags every rounding difference. Enter a value above 0, or
                    choose "no tolerance" to state that deliberately.</div>
                </div>
                <fieldset style="border:0;padding:0;margin:0">
                  <legend class="st-lbl">Then</legend>
                  <div class="st-choice">
                    <label class="st-row" style="--gap: var(--st-space-03)">
                      <input class="st-radio" type="radio" name="ref-next" checked>
                      <span class="st-radio__dot" aria-hidden="true"></span>
                      <span class="st-body-sm">Return to the preparer</span></label>
                    <label class="st-row" style="--gap: var(--st-space-03)">
                      <input class="st-radio" type="radio" name="ref-next">
                      <span class="st-radio__dot" aria-hidden="true"></span>
                      <span class="st-body-sm">Send straight to publish</span></label>
                  </div>
                </fieldset>
                <div class="st-btn-group">
                  <button class="st-btn st-btn--primary">Accept change</button>
                  <button class="st-btn st-btn--secondary">Return with a question</button>
                </div>
              </div>
            </div>
            <div class="st-col" style="--span:16; --span-lg:8">
              <div class="st-tile">
                <div class="st-tile__title">This line</div>
                <dl class="st-kv">
                  <dt>Code</dt><dd class="st-num">FIN02.fx_gbp</dd>
                  <dt>Owner</dt><dd>Finance · a.okafor</dd>
                  <dt>Tolerance</dt><dd class="st-num">0.5%</dd>
                  <dt>Last published</dt><dd>12 Jun, version 7</dd>
                  <dt>Session code</dt><dd><span class="st-keycode st-keycode--sm">KHDR-2F9Q</span></dd>
                </dl>
              </div>
              <div class="st-empty" style="margin-top: var(--st-space-05)">
                <p class="st-empty__title">No questions raised yet</p>
                <p class="st-empty__body">When someone returns a line with a question it appears
                  here, alongside who asked and what they were looking at. Nothing is waiting on
                  you right now.</p>
                <button class="st-btn st-btn--tertiary st-btn--sm">Ask about this line</button>
              </div>
              <div class="st-tile" style="margin-top: var(--st-space-05)">
                <div class="st-tile__title">What happens next</div>
                <div class="st-tile__body">Accepting moves this line to <em>reviewed</em> and adds it
                  to the publish batch. It does not publish on its own — publishing is a separate,
                  deliberate act at step 4, and until then the preparer can still withdraw the
                  change. If you return it instead, the preparer sees your reason and the line goes
                  back to <em>needs preparer</em>; if nobody acts on it within five working days it
                  escalates to the area owner.</div>
              </div>
            </div>
          </div>
        </section>

      </div>
    </div>

    <div class="st-toasts" data-region="app.transient">
      <div class="st-toast st-toast--success" role="status">
        <div class="st-toast__body">
          <div class="st-toast__title">Saved</div>
          Your reason was recorded against FIN02.fx_gbp.
        </div>
        <button class="st-toast__close" aria-label="Dismiss">&#10005;</button>
      </div>
    </div>
  </main>

  <aside class="st-shell__panel" data-region="app.detail" data-open="true"
         aria-label="Salary Cost LC">
    <div class="st-panel__head">
      <div style="flex:1;min-width:0">
        <span class="st-label st-text-secondary">SAL03 &middot; line item</span>
        <h2 class="st-panel__title">Salary Cost LC</h2>
      </div>
      <button class="st-panel__dismiss" aria-label="Close panel">
        <svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true">
          <path fill="currentColor" d="M4 3l9 9-1 1-9-9zM13 4l-9 9-1-1 9-9z"/></svg>
      </button>
    </div>
    <div class="st-tablist" role="tablist" aria-label="Panel sections">
      <button class="st-tab" role="tab" id="pt-dec" aria-controls="pp-dec"
              aria-selected="true" data-attention="true">Decision</button>
      <button class="st-tab" role="tab" id="pt-det" aria-controls="pp-det" aria-selected="false">Detail</button>
      <button class="st-tab" role="tab" id="pt-mea" aria-controls="pp-mea" aria-selected="false">Meaning</button>
    </div>
    <div class="st-panel__body">
      <div role="tabpanel" id="pp-dec" aria-labelledby="pt-dec">
        <div class="st-note st-note--warning" style="margin-bottom:var(--st-space-04)">
          <div class="st-body-sm"><b>Formula changed.</b> Uplift now applies inside the bracket.</div>
        </div>
        <div class="st-panel__box">
          <span class="st-panel__boxlabel">Agreed by james.t, 26 July</span>
          <span class="st-body-sm">Base salary multiplied by the uplift percentage.</span>
        </div>
        <div class="st-panel__box">
          <span class="st-panel__boxlabel">A starting point &mdash; not yet yours</span>
          <span class="st-body-sm">Base salary multiplied by one plus the uplift percentage.</span>
        </div>
      </div>
      <div role="tabpanel" id="pp-det" aria-labelledby="pt-det" hidden>
        <dl class="st-kv">
          <dt>Grain</dt><dd>Employee &times; Month &times; Legal Entity</dd>
          <dt>Cells</dt><dd class="st-num">4,118,400</dd>
          <dt>Owner</dt><dd>james.t</dd>
        </dl>
        <div class="st-panel__box" style="margin-top:var(--st-space-04)">
          <span class="st-panel__boxlabel">Formula</span>
          <span class="st-code">Base Salary Cost * (1 + Uplift %)</span>
        </div>
      </div>
      <div role="tabpanel" id="pp-mea" aria-labelledby="pt-mea" hidden>
        <p class="st-body-sm" style="margin:0">Base salary multiplied by the uplift
          percentage, before on-costs and before any regional adjustment.</p>
      </div>
    </div>
    <div class="st-panel__foot">
      <div class="st-btn-group">
        <button class="st-btn st-btn--primary st-btn--sm">Confirm</button>
        <button class="st-btn st-btn--tertiary st-btn--sm">Rewrite</button>
      </div>
    </div>
  </aside>
</div>
</body>
</html>
"""


# The skill package flattens both brands into one folder, so a page linking the
# generic `strata.css` cannot resolve there -- and BOTH pages linking it means
# there is no arrangement of that folder in which both render. Emit a second copy
# with the brand-qualified href for packaging. Reported from the field: as shipped,
# both reference pages rendered as unstyled HTML.
def skill_href() -> str:
    return f"strata-{B.ACTIVE_BRAND}.css"


if __name__ == "__main__":
    html = build_page()
    with open(os.path.join(DIST, "reference.html"), "w") as f:
        f.write(html)
    print(f"reference.html {len(html)/1024:.1f} KB  ({B.ACTIVE_BRAND})")
