#!/usr/bin/env python3
"""Emit the demo screen: one markup source, two brand renders, one self-contained copy.

    python3 demo/build.py        # after dist/scaffold and dist/deloitte have been built

The markup is written once here. A brand render is a different <link>, nothing else --
that is the claim the page exists to show, so the page must not be able to cheat it by
being hand-copied twice.
"""
import pathlib, re, sys

HERE = pathlib.Path(__file__).parent          # strata/demo/
ROOT = HERE.parent                            # strata/
DIST = ROOT / "dist"
OUT = HERE
OUT.mkdir(exist_ok=True)

SPRITE = (DIST / "scaffold" / "strata-icons.svg").read_text()


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 32 32" width="16" height="16" aria-hidden="true"><use href="#st-i-{name}"></use></svg>'


# --- the queue -------------------------------------------------------------
# ref, counterparty, account, value date, amount, approvals, status text, hue, selected
ROWS = [
    ("PMT-4471", "Brightwater Energy",  "EUR · 4471-08", "23 Aug", "2,480,000.00", "1 of 2", "Over limit",      "red",   False),
    ("PMT-4472", "Corran Logistics",    "GBP · 1180-02", "23 Aug",   "184,300.00", "1 of 2", "Needs you",       "amber", True),
    ("PMT-4473", "Brightwater Energy",  "EUR · 4471-08", "23 Aug",   "960,000.00", "1 of 2", "Over limit",      "red",   False),
    ("PMT-4474", "Halden Manufacturing","GBP · 2207-01", "23 Aug",    "76,915.40", "1 of 2", "Needs you",       "amber", True),
    ("PMT-4475", "Ostrand Chemicals",   "USD · 3390-04", "23 Aug", "1,205,000.00", "2 of 2", "Ready to release","green", False),
    ("PMT-4476", "Corran Logistics",    "GBP · 1180-02", "24 Aug",    "42,180.00",  "1 of 2", "Needs you",      "amber", True),
    ("PMT-4477", "Vellmar Freight",     "EUR · 5512-03", "23 Aug",   "318,750.00", "2 of 2", "Ready to release","green", False),
    ("PMT-4478", "Ostrand Chemicals",   "USD · 3390-04", "23 Aug",   "509,400.00", "0 of 2", "Held — cut-off",  "amber", False),
    ("PMT-4479", "Kelso Interiors",     "GBP · 8801-06", "24 Aug",     "9,640.00", "1 of 2", "Second approval", "blue",  False),
    ("PMT-4480", "Vellmar Freight",     "EUR · 5512-03", "24 Aug",   "127,900.00", "2 of 2", "Ready to release","green", False),
    ("PMT-4481", "Halden Manufacturing","GBP · 2207-01", "24 Aug",   "233,050.00", "1 of 2", "Second approval", "blue",  False),
    ("PMT-4482", "Kelso Interiors",     "GBP · 8801-06", "25 Aug",    "18,220.00", "2 of 2", "Ready to release","green", False),
]


def rows_html():
    out = []
    for ref, cp, acct, vd, amt, appr, status, hue, sel in ROWS:
        s = ' aria-selected="true"' if sel else ""
        checked = " checked" if sel else ""
        out.append(f'''            <tr class="st-table__rowlink"{s}>
              <td>
                <label class="st-choice">
                  <input class="st-check" type="checkbox"{checked}>
                  <span class="st-check__box">{icon("check")}</span>
                  <span class="st-visually-hidden">Select payment {ref}</span>
                </label>
              </td>
              <td><a class="st-code" href="#detail">{ref}</a></td>
              <td class="st-truncate">{cp}</td>
              <td class="st-num">{vd}</td>
              <td class="st-num">{amt}</td>
              <td class="st-num">{appr}</td>
              <td><span class="st-tag st-tag--{hue}">{status}</span></td>
            </tr>''')
    return "\n".join(out)


# --- the screen ------------------------------------------------------------

BODY = f'''
<a class="st-skip" href="#main">Skip to main content</a>

<div class="st-shell st-shell--task st-shell--norail" data-density="comfortable"
     data-product __SHELL_STYLE__>

  <header class="st-shell__header" data-region="app.identity">
    <a class="st-shell__brand" href="#main">Meridian <small>payment operations</small></a>
    <nav class="st-shell__nav" data-region="app.primary-nav" aria-label="Primary">
      <a class="st-shell__navlink" href="#main" aria-current="page">Release queue</a>
      <a class="st-shell__navlink" href="#main">Counterparties</a>
      <a class="st-shell__navlink" href="#main">Limits</a>
      <a class="st-shell__navlink" href="#main">Audit</a>
    </nav>
    <span class="st-shell__spacer"></span>
    <a class="st-waiting st-waiting--due" href="#main" data-region="app.work-waiting">
      <span class="st-waiting__count">12</span>
      <span class="st-waiting__label">waiting on you</span>
    </a>
    <div class="st-shell__util" data-region="app.utility">
      <button class="st-shell__utilbtn" aria-label="Help">{icon("help")}</button>
      <button class="st-shell__utilbtn" aria-label="Settings">{icon("settings")}</button>
    </div>
    <span class="st-shell__account" data-region="app.account">
      <span class="st-shell__avatar" aria-hidden="true">DX</span>
      <span>D. Xing · Approver</span>
    </span>
  </header>

  <div class="st-statusband" data-region="app.subject-state" role="status">
    <span class="st-statusband__item st-statusband__item--stale">
      <span class="st-statusband__dot" aria-hidden="true"></span>
      Balances are 6 minutes old</span>
    <span class="st-statusband__item">
      <span class="st-statusband__dot" aria-hidden="true"></span>
      Same-day EUR cut-off in 47 minutes</span>
    <span class="st-statusband__item">
      <span class="st-statusband__dot" aria-hidden="true"></span>
      Last release confirmed 09:12</span>
  </div>

  <main class="st-shell__main" id="main" tabindex="-1">
    <div class="st-container">
      <div class="st-page">

        <div class="st-page__head">
          <div>
            <h1 class="st-heading-md st-page__title">Payments awaiting release</h1>
            <p class="st-body-md st-page__sub">Everything approved by a preparer and now waiting
              on a second signature. Payments over a counterparty limit are held here rather than
              hidden, because a payment you cannot see is indistinguishable from one that was
              never raised.</p>
          </div>
          <div class="st-row" style="--gap: var(--st-space-03)">
            <button class="st-btn st-btn--tertiary st-btn--md">Export the queue</button>
            <button class="st-btn st-btn--primary st-btn--md">Release 8 approved</button>
          </div>
        </div>

        <section class="st-section">
          <div class="st-grid">
            <div class="st-col st-col--quarter">
              <div class="st-stat" data-region="queue.needs-me">
                <div class="st-stat__figure">12</div>
                <div class="st-stat__label">awaiting approval</div>
              </div>
            </div>
            <div class="st-col st-col--quarter">
              <div class="st-stat" data-region="queue.ready">
                <div class="st-stat__figure">8</div>
                <div class="st-stat__label">ready to release</div>
              </div>
            </div>
            <div class="st-col st-col--quarter">
              <div class="st-stat" data-region="queue.breached">
                <div class="st-stat__figure">2</div>
                <div class="st-stat__label">held over a limit</div>
              </div>
            </div>
            <div class="st-col st-col--quarter">
              <div class="st-stat" data-region="queue.value">
                <div class="st-stat__figure">48.2m</div>
                <div class="st-stat__label">GBP releasing today</div>
              </div>
            </div>
          </div>
        </section>

        <div class="st-note st-note--warning" role="status" data-region="queue.limit-breach">
          {icon("warning")}
          <div>
            <p class="st-note__title">Two payments exceed the Brightwater Energy limit</p>
            <p class="st-note__body">Together they are 1.02m over the 2.42m daily limit. Neither can
              be released until Treasury raises the limit or the value date moves, and this notice
              stays on the screen until one of those happens —
              <a href="#main">open the limit request</a>.</p>
          </div>
        </div>

        <section class="st-section">
          <div class="st-section__head">
            <h2 class="st-heading-sm">The queue</h2>
            <span class="st-helper">Sorted by value date, then reference</span>
          </div>

          <div class="st-grid">
            <div class="st-col" style="--span:16; --span-lg:8">
              <div class="st-search" data-region="queue.search">
                <label class="st-search__field">
                  <span class="st-search__icon" aria-hidden="true">{icon("search")}</span>
                  <span class="st-visually-hidden">Find a payment</span>
                  <input class="st-field" type="search" placeholder="Reference, counterparty or amount"
                         aria-describedby="queue-count">
                </label>
                <div class="st-search__count" id="queue-count" aria-live="polite">
                  <b>12</b> shown of <b>247</b> in the queue
                </div>
              </div>
            </div>
            <div class="st-col" style="--span:16; --span-md:8; --span-lg:4">
              <div class="st-formitem" data-region="queue.filter-date">
                <label class="st-lbl st-label-sm" for="f-date">Value date</label>
                <div class="st-field-wrap">
                  <select class="st-field" id="f-date">
                    <option>Today and tomorrow</option>
                    <option>Today only</option>
                    <option>This week</option>
                  </select>
                  {icon("chevron-down")}
                </div>
              </div>
            </div>
            <div class="st-col" style="--span:16; --span-md:8; --span-lg:4">
              <div class="st-formitem" data-region="queue.filter-status">
                <label class="st-lbl st-label-sm" for="f-status">Status</label>
                <div class="st-field-wrap">
                  <select class="st-field" id="f-status">
                    <option>Not yet released</option>
                    <option>Needs you</option>
                    <option>Over limit</option>
                  </select>
                  {icon("chevron-down")}
                </div>
              </div>
            </div>
          </div>

          <div class="st-row" style="--gap: var(--st-space-03); margin-bottom: var(--st-space-05)"
               data-region="queue.applied-filters">
            <span class="st-helper">Filters in force</span>
            <span class="st-tag st-tag--interactive">Value date 23–24 Aug
              <button class="st-tag__x" aria-label="Remove the value date filter">{icon("close")}</button></span>
            <span class="st-tag st-tag--interactive">Excludes released
              <button class="st-tag__x" aria-label="Remove the released filter">{icon("close")}</button></span>
          </div>

          <div class="st-table-wrap">
            <div class="st-table__batchbar" data-region="queue.bulk-actions">
              <span><b>3</b> payments selected · 303,395.40 GBP</span>
              <div class="st-btn-group">
                <button class="st-btn st-btn--ghost st-btn--sm">Approve all three</button>
                <button class="st-btn st-btn--ghost st-btn--sm">Return all three</button>
                <button class="st-btn st-btn--ghost st-btn--sm">Clear the selection</button>
              </div>
            </div>
            <table class="st-table" data-region="queue.table">
              <thead>
                <tr>
                  <th scope="col">
                    <label class="st-choice">
                      <input class="st-check" type="checkbox">
                      <span class="st-check__box">{icon("check")}</span>
                      <span class="st-visually-hidden">Select every payment shown</span>
                    </label>
                  </th>
                  <th scope="col">Reference</th>
                  <th scope="col">Counterparty</th>
                  <th scope="col" class="st-num" aria-sort="ascending">
                    <button class="st-table__sort" type="button">Value date
                      {icon("sort", "st-table__sortarrow")}</button></th>
                  <th scope="col" class="st-num">Amount</th>
                  <th scope="col" class="st-num">Approvals</th>
                  <th scope="col">Status</th>
                </tr>
              </thead>
              <tbody>
{rows_html()}
              </tbody>
              <tfoot>
                <tr>
                  <td colspan="7">
                    <span class="st-helper">235 more in this queue, beyond the filters in force.</span>
                    <button class="st-btn st-btn--tertiary st-btn--sm">Show the next 12</button>
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        </section>

      </div>
    </div>
  </main>

  <aside class="st-shell__panel" id="detail" data-region="app.detail" data-open="true"
         aria-label="Payment PMT-4471">
    <div class="st-panel__head">
      <h2 class="st-panel__title">PMT-4471</h2>
      <button class="st-panel__dismiss" aria-label="Close the payment detail">
        {icon("close")}
      </button>
    </div>
    <div class="st-panel__body">
      <div class="st-panel__section">
        <span class="st-tag st-tag--red">Over limit</span>
        <p class="st-body-sm" style="margin: var(--st-space-04) 0 0">Brightwater Energy is 1.02m
          over its daily limit once this payment and PMT-4473 are counted together. Approving one
          of the two clears the other, so the order you take them in changes which one waits.</p>
      </div>
      <div class="st-panel__section">
        <dl class="st-kv">
          <dt>Counterparty</dt><dd>Brightwater Energy</dd>
          <dt>Account</dt><dd class="st-num">EUR · 4471-08</dd>
          <dt>Amount</dt><dd class="st-num">2,480,000.00 EUR</dd>
          <dt>Value date</dt><dd>23 Aug, same day</dd>
          <dt>Raised by</dt><dd>a.okafor · 08:51</dd>
          <dt>Daily limit</dt><dd class="st-num">2,420,000.00 EUR</dd>
        </dl>
      </div>
      <div class="st-panel__section">
        <p class="st-body-sm st-text-secondary" style="margin: 0">Returning this sends it back to
          the preparer with your reason attached. It does not cancel the payment, and the value
          date does not move on its own.</p>
      </div>
    </div>
    <div class="st-panel__foot">
      <div class="st-btn-group">
        <button class="st-btn st-btn--primary st-btn--sm">Approve</button>
        <button class="st-btn st-btn--tertiary st-btn--sm">Return with a question</button>
      </div>
    </div>
  </aside>
</div>
'''


# --- emit ------------------------------------------------------------------

LINKED = '''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Payments awaiting release — Strata demo ({brand})</title>
<link rel="stylesheet" href="../dist/{brand}/strata.css">
<style>
  /* Review chrome only. The product below carries no page-specific CSS at all. */
  body {{ margin: 0; font-family: var(--st-font-sans); color: var(--st-text-primary); }}
  .demo-bar {{ position: sticky; top: 0; height: 44px; z-index: 60;
               display: flex; align-items: center; gap: 16px; padding-inline: 16px;
               background: var(--st-layer-accent-01);
               border-bottom: 1px solid var(--st-border-subtle-01);
               font: 400 12px/1 var(--st-font-sans); color: var(--st-text-secondary); }}
  .demo-bar b {{ color: var(--st-text-primary); }}
  .demo-bar a {{ color: var(--st-link-primary); }}
</style>
</head>
<body>
<div class="demo-bar" data-review>
  <b>Strata demo — payment release queue</b>
  <span>brand <b>{brand}</b> · shell <b>--task --norail</b> · density comfortable · appearance default</span>
  <span>· the other render: <a href="approval-queue-{other}.html">{other}</a></span>
</div>
{sprite}
{body}
</body>
</html>
'''

for brand, other in (("scaffold", "deloitte"), ("deloitte", "scaffold")):
    html = LINKED.format(
        brand=brand, other=other, sprite=SPRITE,
        body=BODY.replace("__SHELL_STYLE__", 'style="--st-shell-offset: 44px"'),
    )
    (OUT / f"approval-queue-{brand}.html").write_text(html)
    print("wrote", OUT / f"approval-queue-{brand}.html")

# The self-contained copy for the hosted artifact: same body, both stylesheets inlined,
# brand chosen at runtime. No <html>/<head>/<body> — the artifact host supplies those.
css = {b: (DIST / b / "strata.css").read_text() for b in ("scaffold", "deloitte")}
ART = HERE / "artifact.html"
ART.write_text((HERE / "artifact_template.html").read_text()
               .replace("__SPRITE__", SPRITE)
               .replace("__CSS_SCAFFOLD__", css["scaffold"])
               .replace("__CSS_DELOITTE__", css["deloitte"])
               .replace("__BODY__", BODY.replace("__SHELL_STYLE__",
                                                 'style="--st-shell-offset: 48px"')))
print("wrote", ART)
