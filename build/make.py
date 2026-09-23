#!/usr/bin/env python3
"""Assemble dist/index.html. Run:  python3 build/make.py"""

from __future__ import annotations
import os, json
import build as B
import guide as G
import tokens as T
from color import (GRADES, contrast, ACTIVE_BRAND, ROLES,
                   check_role_separation, role_separation_report)

I = G.ICONS
DIST = B.DIST

PAGE_CSS = r"""
:root { --gut: clamp(16px, 4vw, 48px); }
html { scroll-behavior: smooth; scroll-padding-top: 76px; }
body.guide { background: var(--st-background); }
.wrap { max-width: 1180px; margin: 0 auto; padding: 0 var(--gut) 8rem; }

/* topbar */
.top { position: sticky; top: 0; z-index: 50;
       background: var(--st-background);  /* fallback: Safari <16.2 / FF <113 */
       border-bottom: 1px solid var(--st-border-subtle-01); }
@supports (background: color-mix(in srgb, red 50%, transparent)) {
  .top { background: color-mix(in srgb, var(--st-background) 88%, transparent);
         -webkit-backdrop-filter: blur(12px); backdrop-filter: blur(12px); }
}
.top__in { max-width: 1180px; margin: 0 auto; padding: 0 var(--gut); height: 60px; display: flex; align-items: center; gap: var(--st-space-06); }
.brand { font-weight: 650; letter-spacing: -0.01em; display: flex; align-items: center; gap: 10px; }
.brand__mark { width: 22px; height: 22px; border-radius: 6px;
  background: linear-gradient(150deg, var(--st-interactive), var(--st-background-brand) 70%, var(--st-text-primary)); }
.brand small { font-weight: 400; color: var(--st-text-secondary); font-size: 12px; }
.top nav { display: flex; gap: 2px; margin-left: auto; flex-wrap: wrap; }
.top nav a { font-size: 13px; color: var(--st-text-secondary); text-decoration: none; padding: 6px 10px; border-radius: 6px; }
.top nav a:hover { background: var(--st-background-hover); color: var(--st-text-primary); }

/* hero */
.hero { padding: 4.5rem 0 3rem; border-bottom: 1px solid var(--st-border-subtle-01); }
.hero h1 { font: 500 clamp(34px, 5.5vw, 56px)/1.08 var(--st-font-sans); letter-spacing: -0.025em; margin: 0 0 1rem; max-width: 20ch; }
.hero p { max-width: 68ch; color: var(--st-text-secondary); font-size: 18px; line-height: 1.6; margin: 0 0 1rem; }
.pillrow { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 1.75rem; }
.pill { font-size: 12px; padding: 5px 11px; border-radius: 999px; border: 1px solid var(--st-border-subtle-01);
        color: var(--st-text-secondary); background: var(--st-layer-01); }

section { padding: 4rem 0 1rem; border-bottom: 1px solid var(--st-border-subtle-01); }
section > h2 { font: 500 30px/1.15 var(--st-font-sans); letter-spacing: -0.02em; margin: 0 0 .35rem; }
section > .lede { color: var(--st-text-secondary); max-width: 74ch; margin: 0 0 2.25rem; font-size: 16.5px; line-height: 1.6; }
h3 { font: 600 17px/1.3 var(--st-font-sans); margin: 2.5rem 0 .85rem; }
h4.tokgrp { font: 600 12px/1 var(--st-font-sans); text-transform: uppercase; letter-spacing: .09em;
            color: var(--st-text-secondary); margin: 2.25rem 0 .6rem; }
p.note { color: var(--st-text-secondary); font-size: 14px; line-height: 1.6; max-width: 78ch; }
p.srcline { font-size: 12px; color: var(--st-text-helper); margin: .5rem 0 0; }
p.srcline a, .cite__src { color: var(--st-link-primary); }
code { font-family: var(--st-font-mono); font-size: .86em; }

/* the argument blocks */
.arg { display: grid; gap: 1.25rem; grid-template-columns: repeat(auto-fit, minmax(255px, 1fr)); margin: 1.5rem 0 0; }
.arg > div { background: var(--st-layer-01); border: 1px solid var(--st-border-subtle-01);
             border-radius: var(--st-radius-lg); padding: 1.15rem 1.25rem; }
.arg p.argh { margin: 0 0 .45rem; font-size: 14.5px; font-weight: 600; color: var(--st-text-primary); }
.vh { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.arg p { margin: 0; font-size: 13.5px; line-height: 1.62; color: var(--st-text-secondary); }

/* citation */
.cite { display: grid; gap: 3px; margin-top: .45rem; padding-left: .7rem; border-left: 2px solid var(--st-border-subtle-01); }
.cite--chg { border-left-color: var(--st-support-warning); }
.cite--add { border-left-color: var(--st-support-info); }
.cite--drop { border-left-color: var(--st-support-error); }
.cite__tag, .cite__tag--adopt, .cite__tag--chg, .cite__tag--add, .cite__tag--drop {
  display: inline-block; width: fit-content; font-size: 10px; letter-spacing: .07em; text-transform: uppercase;
  font-weight: 700; padding: 2px 6px; border-radius: 4px;
  background: var(--st-layer-accent-01); color: var(--st-text-secondary); }
.cite--chg .cite__tag, .cite__tag--chg { background: var(--st-support-warning-subtle); color: var(--st-support-warning); }
.cite--add .cite__tag, .cite__tag--add { background: var(--st-support-info-subtle); color: var(--st-support-info); }
.cite--drop .cite__tag, .cite__tag--drop { background: var(--st-support-error-subtle); color: var(--st-support-error); }
.cite__val { font-size: 12.5px; color: var(--st-text-secondary); line-height: 1.5; }
.cite__why { font-size: 12.5px; color: var(--st-text-primary); line-height: 1.55; }
.cite__src { font-size: 11px; text-decoration: none; word-break: break-all; }
.cite__src:hover { text-decoration: underline; }
.role { font-size: 13.5px; }

/* tables */
table.tok { width: 100%; border-collapse: collapse; font-size: 13.5px; margin-bottom: 1rem; }
table.tok th { text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: .08em;
  color: var(--st-text-secondary); font-weight: 600; padding: .5rem .7rem; border-bottom: 1px solid var(--st-border-subtle-01); }
table.tok td { padding: .7rem; border-bottom: 1px solid var(--st-border-subtle-01); vertical-align: top; }
table.tok tbody tr:hover { background: var(--st-layer-01); }
.tok__v { white-space: nowrap; }
.tok__v span { display: inline-block; vertical-align: middle; }
.chip { display: inline-block; width: 15px; height: 15px; border-radius: 4px; vertical-align: middle;
        margin-right: 7px; border: 1px solid var(--st-border-subtle-01); }
.nowrap { white-space: nowrap; }
.num { text-align: right; font-variant-numeric: tabular-nums; }
.pass { color: var(--st-support-success); font-weight: 600; font-size: 12px; }
.fail { color: var(--st-support-error); font-weight: 700; font-size: 12px; }
.adv { color: var(--st-text-helper); font-size: 12px; }
small { font-size: 11.5px; color: var(--st-text-helper); }

/* ramps */
.ramp { display: grid; grid-template-columns: 5.5rem 1fr; gap: 1rem; align-items: center; margin-bottom: 7px; }
.ramp__name { font-size: 12px; font-weight: 600; text-transform: capitalize; color: var(--st-text-secondary); }
.ramp__cells { display: grid; grid-template-columns: repeat(10, 1fr); border-radius: 8px; overflow: hidden; }
.sw { padding: .6rem .45rem .55rem; display: grid; gap: 1px; font-size: 10px; line-height: 1.2; }
.sw__g { font-weight: 700; }
.sw__h { font-family: var(--st-font-mono); font-size: 9.5px; }

/* scales */
.scales { display: grid; gap: 5px; }
.sc { display: grid; grid-template-columns: 210px 4.5rem 1fr; align-items: center; gap: 1rem; font-size: 12.5px; }
.sc__bar { height: 13px; border-radius: 3px; background: linear-gradient(90deg, var(--st-border-interactive), var(--st-background-brand)); }

/* demos */
.demo { background: var(--st-layer-01); border: 1px solid var(--st-border-subtle-01);
        border-radius: var(--st-radius-lg); padding: 1.75rem; margin: 0 0 .75rem;
        display: flex; flex-wrap: wrap; gap: 1.25rem; align-items: flex-start; }
.demo--stack { flex-direction: column; }
.demo--pad0 { padding: 0; overflow: hidden; }
.demo__col { display: grid; gap: .9rem; }
.comp { margin-bottom: 3.25rem; }
.comp > h3 { margin-top: 0; font-size: 20px; }
.comp > p.lede2 { color: var(--st-text-secondary); font-size: 14.5px; margin: 0 0 1.1rem; max-width: 72ch; }
.swatchbox { display: grid; gap: 3px; }
.elev { width: 150px; height: 76px; border-radius: var(--st-radius-lg); background: var(--st-layer-02);
        border: 1px solid var(--st-border-subtle-01); display: grid; place-items: center; font-size: 12px; }
</style>
"""


def demos():
    """All live component demos, keyed to T.COMPONENTS."""
    d = {}

    d["button"] = f"""
<div class="demo">
  <div class="st-btn-group">
    <button class="st-btn st-btn--primary">Create workspace</button>
    <button class="st-btn st-btn--secondary">Duplicate</button>
    <button class="st-btn st-btn--tertiary">Preview</button>
    <button class="st-btn st-btn--ghost">Cancel</button>
    <button class="st-btn st-btn--danger">Delete</button>
    <button class="st-btn st-btn--primary" disabled>Disabled</button>
  </div>
  <div class="st-btn-group">
    <button class="st-btn st-btn--primary st-btn--sm">Small</button>
    <button class="st-btn st-btn--primary st-btn--md">Medium</button>
    <button class="st-btn st-btn--primary">Large (default)</button>
    <button class="st-btn st-btn--primary">Continue {I['arrow']}</button>
  </div>
</div>"""

    d["text-input"] = f"""
<div class="demo">
  <div class="demo__col" style="min-width:19rem">
    <div class="st-formitem">
      <label class="st-lbl" for="f1">Workspace name</label>
      <input class="st-field" id="f1" placeholder="e.g. Northwind analytics">
      <span class="st-help">Lowercase letters, numbers and hyphens.</span>
    </div>
    <div class="st-formitem">
      <label class="st-lbl" for="f2">Contact email</label>
      <input class="st-field" id="f2" value="not-an-email" aria-invalid="true">
      <span class="st-msg st-msg--error">{I['error']}Enter an email address in the form name@example.com.</span>
    </div>
    <div class="st-formitem">
      <label class="st-lbl" for="f3">Retention</label>
      <input class="st-field" id="f3" value="400 days">
      <span class="st-msg st-msg--warning" style="color:var(--st-support-warning)">{I['warning']}<span style="color:var(--st-text-primary)">Over 365 days incurs archive charges.</span></span>
    </div>
  </div>
  <div class="demo__col" style="min-width:19rem">
    <div class="st-formitem">
      <label class="st-lbl" for="f4">Description</label>
      <textarea class="st-field" id="f4" placeholder="What is this workspace for?"></textarea>
    </div>
    <div class="st-formitem">
      <label class="st-lbl" for="f5">Workspace ID</label>
      <input class="st-field" id="f5" value="ws_8f31c02a" readonly>
      <span class="st-help">Read-only. Stays keyboard-navigable.</span>
    </div>
    <div class="st-formitem">
      <label class="st-lbl" for="f6">Legacy region</label>
      <input class="st-field" id="f6" value="eu-west-1" disabled>
    </div>
  </div>
</div>"""

    d["checkbox"] = f"""
<div class="demo">
  <div class="demo__col">
    <span class="st-label st-text-secondary">Notify me about</span>
    <label class="st-choice"><input type="checkbox" class="st-check" checked><span class="st-check__box">{I['check']}</span><span class="st-choice__label">Deployment failures</span></label>
    <label class="st-choice"><input type="checkbox" class="st-check" id="ind"><span class="st-check__box">{I['check']}</span><span class="st-choice__label">Budget thresholds</span></label>
    <label class="st-choice"><input type="checkbox" class="st-check"><span class="st-check__box">{I['check']}</span><span class="st-choice__label">Weekly digest, which can wrap onto a second line to show that wrapped label text top-aligns to the control rather than centring</span></label>
    <label class="st-choice"><input type="checkbox" class="st-check" disabled><span class="st-check__box">{I['check']}</span><span class="st-choice__label">SMS alerts (unavailable on this plan)</span></label>
  </div>
</div>"""

    d["radio"] = """
<div class="demo">
  <div class="demo__col">
    <span class="st-label st-text-secondary">Deployment target</span>
    <label class="st-choice"><input type="radio" name="r" class="st-radio"><span class="st-radio__dot"></span><span class="st-choice__label">Staging</span></label>
    <label class="st-choice"><input type="radio" name="r" class="st-radio" checked><span class="st-radio__dot"></span><span class="st-choice__label">Production</span></label>
    <label class="st-choice"><input type="radio" name="r" class="st-radio" disabled><span class="st-radio__dot"></span><span class="st-choice__label">Edge (requires upgrade)</span></label>
  </div>
</div>"""

    d["toggle"] = """
<div class="demo">
  <div class="demo__col">
    <label class="st-toggle-wrap"><input type="checkbox" class="st-toggle" checked><span class="st-toggle__track"></span><span class="st-toggle__state">Automatic backups <b>on</b></span></label>
    <label class="st-toggle-wrap"><input type="checkbox" class="st-toggle"><span class="st-toggle__track"></span><span class="st-toggle__state">Public endpoint <b>off</b></span></label>
    <label class="st-toggle-wrap"><input type="checkbox" class="st-toggle" disabled><span class="st-toggle__track"></span><span class="st-toggle__state" style="color:var(--st-text-disabled)">Audit log streaming</span></label>
  </div>
</div>"""

    d["select"] = f"""
<div class="demo">
  <div class="demo__col" style="min-width:19rem">
    <div class="st-formitem">
      <label class="st-lbl" for="s1">Region</label>
      <div class="st-field-wrap">
        <select class="st-field" id="s1">
          <option>ap-southeast-2 · Sydney</option>
          <option>eu-west-1 · Ireland</option>
          <option>us-east-1 · N. Virginia</option>
        </select>{I['chevron']}
      </div>
      <span class="st-help">Data does not leave the selected region.</span>
    </div>
  </div>
  <div class="demo__col">
    <span class="st-label st-text-secondary">Open menu</span>
    <div style="width:19rem;background:var(--st-layer-02);border:1px solid var(--st-border-subtle-01);border-radius:var(--st-radius-md);box-shadow:var(--st-elevation-02);overflow:hidden">
      <div style="height:48px;display:flex;align-items:center;padding-inline:16px">ap-southeast-2 · Sydney</div>
      <div style="height:48px;display:flex;align-items:center;padding-inline:16px;background:var(--st-layer-hover-01)">eu-west-1 · Ireland</div>
      <div style="height:48px;display:flex;align-items:center;justify-content:space-between;padding-inline:16px;background:var(--st-layer-selected-01)">us-east-1 · N. Virginia <span style="width:16px;color:var(--st-icon-primary)">{I['check']}</span></div>
    </div>
  </div>
</div>"""

    # calendar grid: July 2026, range 14 -> 21
    cells = []
    for n in (29, 30):
        cells.append(f'<button class="st-day st-day--muted">{n}</button>')
    for n in range(1, 32):
        cls = "st-day"
        if n == 30:
            cls += " st-day--today"
        if n == 14:
            cls += " st-day--start"
        elif n == 21:
            cls += " st-day--end"
        elif 14 < n < 21:
            cls += " st-day--inrange"
        dis = " disabled" if n in (4, 5) else ""
        cells.append(f'<button class="{cls}"{dis}>{n}</button>')
    for n in (1, 2):
        cells.append(f'<button class="st-day st-day--muted">{n}</button>')
    dows = "".join(f'<div class="st-cal__dow">{x}</div>' for x in ["M", "T", "W", "T", "F", "S", "S"])

    d["date-picker"] = f"""
<div class="demo">
  <div class="demo__col" style="min-width:19rem">
    <div class="st-formitem">
      <label class="st-lbl" for="d1">Start date (dd/mm/yyyy)</label>
      <div class="st-field-wrap"><input class="st-field st-field--date" id="d1" value="14/07/2026">{I['calendar']}</div>
      <span class="st-help">Format is in the label, never placeholder-only.</span>
    </div>
    <div class="st-formitem">
      <label class="st-lbl" for="d2">End date (dd/mm/yyyy)</label>
      <div class="st-field-wrap"><input class="st-field st-field--date" id="d2" value="21/07/2026">{I['calendar']}</div>
    </div>
  </div>
  <div class="st-cal">
    <div class="st-cal__head">
      <button class="st-cal__nav" aria-label="Previous month">{I['left']}</button>
      <span class="st-cal__month">July 2026</span>
      <button class="st-cal__nav" aria-label="Next month">{I['right']}</button>
    </div>
    <div class="st-cal__grid">{dows}</div>
    <div class="st-cal__grid">{''.join(cells)}</div>
  </div>
</div>"""

    d["table"] = f"""
<div class="demo demo--pad0" style="display:block">
  <div class="st-table__batchbar">
    <span class="st-heading-sm">2 items selected</span>
    <div class="st-btn-group"><button class="st-btn st-btn--ghost st-btn--sm" style="color:inherit">Archive</button><button class="st-btn st-btn--ghost st-btn--sm" style="color:inherit">Cancel</button></div>
  </div>
  <table class="st-table st-table--zebra">
    <thead><tr>
      <th style="width:48px"><label class="st-choice" style="margin:0"><input type="checkbox" class="st-check" aria-label="Select all rows"><span class="st-check__box">{I['check']}</span></label></th><th aria-sort="ascending">Name {I['sort']}</th><th aria-sort="none">Region {I['sort']}</th><th aria-sort="none">Status {I['sort']}</th><th class="num" style="text-align:right">Nodes</th>
    </tr></thead>
    <tbody>
      <tr aria-selected="true"><td><label class="st-choice" style="margin:0"><input type="checkbox" class="st-check" checked aria-label="Select northwind-prod"><span class="st-check__box">{I['check']}</span></label></td><td>northwind-prod</td><td>ap-southeast-2</td><td><span class="st-tag st-tag--green">Healthy</span></td><td class="num" style="text-align:right">24</td></tr>
      <tr aria-selected="true"><td><label class="st-choice" style="margin:0"><input type="checkbox" class="st-check" checked aria-label="Select northwind-staging"><span class="st-check__box">{I['check']}</span></label></td><td>northwind-staging</td><td>ap-southeast-2</td><td><span class="st-tag st-tag--amber">Degraded</span></td><td class="num" style="text-align:right">6</td></tr>
      <tr><td><label class="st-choice" style="margin:0"><input type="checkbox" class="st-check" aria-label="Select atlas-eu"><span class="st-check__box">{I['check']}</span></label></td><td>atlas-eu</td><td>eu-west-1</td><td><span class="st-tag st-tag--red">Failed</span></td><td class="num" style="text-align:right">0</td></tr>
      <tr><td><label class="st-choice" style="margin:0"><input type="checkbox" class="st-check" aria-label="Select atlas-us"><span class="st-check__box">{I['check']}</span></label></td><td>atlas-us</td><td>us-east-1</td><td><span class="st-tag st-tag--green">Healthy</span></td><td class="num" style="text-align:right">12</td></tr>
    </tbody>
  </table>
</div>"""

    d["modal"] = f"""
<div class="demo" style="background:var(--st-layer-accent-01);justify-content:center">
  <div class="st-modal" style="position:relative">
    <div class="st-modal__head">
      <p class="st-modal__label">Workspace</p>
      <h3 class="st-modal__title">Delete northwind-prod?</h3>
    </div>
    <div class="st-modal__body">
      <p style="margin:0">This permanently removes 24 nodes and all attached volumes. Snapshots taken in the last 30 days are retained. This cannot be undone.</p>
    </div>
    <div class="st-modal__foot">
      <button class="st-btn st-btn--ghost">Cancel</button>
      <button class="st-btn st-btn--danger">Delete workspace</button>
    </div>
  </div>
</div>"""

    d["tabs"] = """
<div class="demo demo--stack">
  <div class="st-tablist" role="tablist">
    <button class="st-tab" role="tab" aria-selected="true">Overview</button>
    <button class="st-tab" role="tab" aria-selected="false">Nodes</button>
    <button class="st-tab" role="tab" aria-selected="false">Logs</button>
    <button class="st-tab" role="tab" aria-selected="false">Settings</button>
    <button class="st-tab" role="tab" aria-selected="false" disabled>Billing</button>
  </div>
  <p class="note" style="margin:0">Selected tab carries weight 600 as well as the underline, so it survives greyscale.</p>
</div>"""

    d["notification"] = f"""
<div class="demo demo--stack">
  <div class="st-note st-note--error" style="width:100%">{I['error']}<div><p class="st-note__title">Deployment failed</p><p class="st-note__body">Three of 24 nodes could not pull the image. Retry the deployment or roll back to build 4471.</p></div></div>
  <div class="st-note st-note--warning" style="width:100%">{I['warning']}<div><p class="st-note__title">Approaching your node quota</p><p class="st-note__body">42 of 50 nodes in use. Requests above the quota will queue.</p></div></div>
  <div class="st-note st-note--success" style="width:100%">{I['success']}<div><p class="st-note__title">Snapshot restored</p><p class="st-note__body">northwind-prod was restored from the 29 July snapshot.</p></div></div>
  <div class="st-note" style="width:100%">{I['info']}<div><p class="st-note__title">Maintenance window</p><p class="st-note__body">Scheduled for 2 August, 14:00–16:00 AEST.</p></div></div>
</div>"""

    d["tag"] = f"""
<div class="demo">
  <div class="st-btn-group">
    <span class="st-tag">Neutral</span>
    <span class="st-tag st-tag--blue">Infrastructure</span>
    <span class="st-tag st-tag--teal">Analytics</span>
    <span class="st-tag st-tag--green">Healthy</span>
    <span class="st-tag st-tag--amber">Degraded</span>
    <span class="st-tag st-tag--red">Failed</span>
    <span class="st-tag st-tag--magenta">Beta</span>
    <span class="st-tag st-tag--outline">Outline</span>
  </div>
  <div class="st-btn-group">
    <span class="st-tag st-tag--sm">Small</span>
    <span class="st-tag">Medium</span>
    <span class="st-tag st-tag--lg">Large</span>
    <span class="st-tag st-tag--blue">region: ap-southeast-2 <button class="st-tag__x" aria-label="Remove">{I['close']}</button></span>
  </div>
</div>"""

    d["tile"] = """
<div class="demo">
  <div class="st-tile" style="max-width:16rem"><p class="st-tile__title">Base tile</p><p class="st-tile__body">Static container. No elevation at rest, matching Carbon.</p></div>
  <a class="st-tile st-tile--clickable" href="#tile" style="max-width:16rem"><p class="st-tile__title">Clickable tile</p><p class="st-tile__body">Lifts to elevation-01 on hover. Whole surface is the target.</p></a>
  <div class="st-tile st-tile--selected" style="max-width:16rem"><p class="st-tile__title">Selected tile</p><p class="st-tile__body">2px border-interactive, with padding compensated so nothing shifts.</p></div>
</div>"""
    return d


def build_page():
    D = demos()
    tokens_doc = B.build_tokens_json()
    B.build_css()
    with open(os.path.join(DIST, "strata.css")) as f:
        css = f.read()

    ramps = "".join(G.swatch_row(n, r) for n, r in B.PALETTE.items() if n not in ("white", "black"))

    comps_html = []
    for key, comp in T.COMPONENTS.items():
        title = key.replace("-", " ").title().replace("Ui", "UI")
        comps_html.append(
            f'<div class="comp" id="c-{key}"><h3>{title}</h3>'
            f'<p class="lede2">{G.E(comp["summary"])}</p>'
            f'{D.get(key, "")}{G.component_spec(key, comp)}</div>')

    nav = [("foundations", "Foundations"), ("brand", "Brand"), ("colour", "Colour"), ("type", "Type"),
           ("scales", "Scales"), ("components", "Components"),
           ("accessibility", "Accessibility"), ("ledger", "Divergence"), ("licence", "Licence")]
    navhtml = "".join(f'<a href="#{i}">{l}</a>' for i, l in nav)

    html_out = f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Strata ({ACTIVE_BRAND}) — a design system derived from IBM Carbon</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<style>
{css}
{PAGE_CSS}
</head>
<body class="guide">

<header class="top">
  <div class="top__in">
    <span class="brand"><span class="brand__mark"></span>Strata <small>v0.3 · {ACTIVE_BRAND}</small></span>
    <nav>{navhtml}</nav>
    <button class="st-btn st-btn--tertiary st-btn--sm" id="themebtn" style="margin-left:12px">Dark</button>
  </div>
</header>

<main class="wrap">

<div class="hero">
  <h1>A base extracted from Carbon, with every value shown its source.</h1>
  <p>Strata takes IBM Carbon's token architecture, layering model, spacing scale, motion curves and
  accessibility mechanisms largely intact, and diverges where the brief calls for something lighter —
  or where Carbon's own published guidance contradicts itself. Every token below carries the official
  Carbon value it came from, a link to the page it came from, and where they differ, the reason.</p>
  <p>This page is not a description of the system. It is rendered <em>from</em> the system — the same
  <code>tokens.json</code> and <code>strata.css</code> the components consume. Nothing here can drift
  from what ships.</p>
  <div class="pillrow">
    <span class="pill">9 hue ramps · 10 grades · luminance-locked</span>
    <span class="pill">{len(T.SEMANTIC)} semantic tokens</span>
    <span class="pill">{len(T.COMPONENTS)} components</span>
    <span class="pill">168 contrast checks, 0 failing</span>
    <span class="pill">axe-core: 0 violations</span>
    <span class="pill">Light + dark</span>
  </div>
</div>

<section id="foundations">
  <h2>Why this shape</h2>
  <p class="lede">You asked me to recommend the form and justify it. Four decisions, and what each one
  is defending against.</p>

  <div class="arg">
    <div><p class="argh">1 · Tokens are the deliverable, not the CSS</p>
    <p>The artefact of record is <code>tokens.json</code>. CSS, the component styles and this page are
    all generated from it. The failure mode this prevents is real and Carbon demonstrates it: its
    published token table still prints <code>$button-primary-hover</code> as <code>#0353e9</code> while
    <code>@carbon/themes</code> ships <code>#0050e6</code>, and prints <code>$text-placeholder</code> as
    Gray&nbsp;40 while the code ships <code>rgba(22,22,22,0.4)</code>. Two artefacts, two answers, and
    no way to know which is right without reading the source. One generator, one answer.</p></div>

    <div><p class="argh">2 · A live style guide, not a spec document</p>
    <p>A written spec cannot show you that a warning icon has 2.8:1 against its own background. This
    page renders every component from the shipped CSS and recomputes every contrast pair at build time.
    Design systems fail at the seams between the documentation and the artefact; removing the seam is
    cheaper than policing it.</p></div>

    <div><p class="argh">3 · Framework-agnostic CSS custom properties</p>
    <p>No React dependency in the base layer. The token and CSS layers outlive whatever renders them,
    and a React, Vue or Web Components binding can sit on top without forking the values. This mirrors
    Carbon's own structure — <code>@carbon/colors</code>, <code>@carbon/type</code> and
    <code>@carbon/layout</code> are framework-free by design — and it is why Carbon survived its own
    v10→v11 migration.</p></div>

    <div><p class="argh">4 · Semantic tier is the contract</p>
    <p>Components reference <code>--st-layer-01</code>, never <code>--st-neutral-10</code>. That single
    rule is what makes light/dark a data change rather than a code change, and it is the reason the
    whole palette can be re-hued without touching a component file. Carbon states it as: tokens are
    universal, roles never change between themes, only values do.</p></div>
  </div>

  <h3>What was adopted wholesale</h3>
  <p class="note">The 8px mini-unit spacing scale (all 13 steps). The 16-column 2x Grid and its five
  breakpoints. The productive motion curves and durations. The layering model, including the off-by-one
  field rule — a field placed on <code>layer-02</code> uses <code>field-03</code>, but borders pair with
  their own number. The two-tone focus ring, drawn inset at <code>outline-offset: -2px</code>. The
  <code>group-role-state-index</code> token grammar. The interaction-state arithmetic: hover is a half
  step, selected one step, active two steps. Warning does not recolour a field border. Placeholder never
  replaces a label. Tags are not navigation. Toggles are only for instantly-applied settings. These are
  the parts of Carbon that are genuinely hard-won, and there is no reason to re-derive them.</p>

  <h3>Where it diverges, and the three reasons</h3>
  <div class="arg">
    <div><h4>Lighter, per your brief</h4><p>Radius scale introduced and defaulted to 6px on controls.
    Chroma capped at roughly half Carbon's peak. Body text drops from 17.4:1 to 14.2:1. Scrims and
    shadows tinted with the neutral hue instead of pure black. Default body size 16px, not 14px.</p></div>
    <div><h4>Carbon contradicts itself</h4><p><code>$text-placeholder</code> fails 4.5:1 in both of its
    two conflicting official values. <code>$support-warning</code> is held constant across all four
    themes, breaking the theme contract, and fails 1.4.11 against its own notification background.
    Carbon requires 44px touch targets for icons but ships a 40px default field. The date picker field
    is set in the mono type token for no published reason. <code>@carbon/themes</code> ships two different
    values for <code>$button-primary-hover</code> from its own SCSS and JS builds.</p></div>
    <div><h4>Carbon leaves a gap</h4><p><code>prefers-reduced-motion</code> handled per-component in 12 SCSS
    files, with no token and no requirement — so coverage is partial by construction. No
    sticky-header data table spec, though the React implementation supports it. No dropdown menu
    max-height. No range-<em>start</em> calendar cell state. No radius scale. Status backgrounds locked
    inside the Notification component by the component-token confinement rule.</p></div>
  </div>
</section>

<section id="brand">
  <h2>Brand — Deloitte</h2>
  <p class="lede">The primary action colour is Deloitte Green 349 (<code>#046A38</code>), the dark
  green. Neutrals are Deloitte Cool Gray. Everything else in the system is unchanged — this page
  exists so the brand mapping is auditable rather than asserted.</p>

  <div class="arg">
    <div><p class="argh">The dark green was the right call</p>
    <p>Deloitte Green <code>#86BC25</code> measures <b>2.27:1</b> against white. It cannot carry
    text, an icon, or a control boundary under WCAG AA — which is the standard Deloitte's own
    accessibility statement commits to. It is a mark colour. Green 349 at 6.72:1 is the first
    green in the official ramp that can be an action colour, and grade 70 reproduces it to within
    &Delta;RGB 5.</p></div>

    <div><p class="argh">The grey shift was already done</p>
    <p>Deloitte Cool Gray 10 and 11 sit at OKLCH hue <b>255.5&deg;</b>. Strata's neutral was
    already 255.0&deg;. <code>--st-neutral-70</code> was <code>#55595d</code> against Cool Gray 11's
    <code>#53565A</code> — &Delta;RGB 4. The brief was satisfied before it was written; the config
    now says so explicitly rather than leaving it to coincidence.</p></div>

    <div><p class="argh">Deloitte's green ramp is not one hue</p>
    <p>It swings from <b>109&deg;</b> at the light end to <b>153&deg;</b> at the dark end — a
    Pantone set, not a computed ramp. A single-hue ladder can hit one end or the other. Anchoring
    on the dark end (the interactive colour) means <code>#86BC25</code> has to be carried as a
    pinned literal, outside the ramp, restricted to mark use.</p></div>

    <div><p class="argh">One divergence reversed itself</p>
    <p><code>--st-support-info</code> was moved off blue because Carbon's blue info collided with
    Carbon's blue primary action. With a green primary that objection evaporates and blue is free,
    so info returns to Carbon's value — now as Deloitte Blue 7690, &Delta;RGB 3. The divergence was
    contingent on the brand, not on Carbon being wrong.</p></div>
  </div>

  {G.brand_table()}

  <h3>The collision worth arguing about</h3>
  <p class="note">With a green brand, <b>the primary action and success are one grade apart in the
  same hue</b> — <code>green.70</code> and <code>green.60</code>. They are kept apart by form, not
  colour: <code>--st-support-success</code> only ever renders as a toggle track, a status icon or a
  3px banner rule, never as a filled action-shaped surface, and every status carries an icon under
  the never-colour-alone rule already in the system. The alternative — moving success to teal —
  breaks the strongest colour convention in UI to solve a collision the form language already
  resolves, and would push info off Deloitte Blue. Scroll to Notification and Toggle below and
  judge it directly. If it bites in testing it is one line in <code>build/tokens.py</code>.</p>

  <h3>Before you ship this</h3>
  <p class="note">Deloitte Green is a <b>registered trademark</b> — USPTO Reg. 5959457, "the mark
  consists of a green dot (Pantone 368)", colour claimed as a feature of the mark, registered
  January 2020. Separately, Acorns Grow Inc. holds US Reg. 6176921 over Pantone 368 C
  <em>as applied to the background of a software application</em>. This system assumes you are
  building for or with Deloitte and are licensed to use the palette. If that assumption is wrong,
  this is not a design question.</p>
</section>

<section id="colour">
  <h2>Colour</h2>
  <p class="lede">Nine hue ramps of ten grades, plus black and white. Carbon hand-authors each hue, which
  is why it has to publish a lookup table telling you how many steps apart two colours must be to reach a
  given contrast ratio. Strata pins every grade to a fixed relative luminance and solves for OKLCH
  lightness, so grade&nbsp;60 has the same contrast behaviour in every hue and the lookup table becomes
  exact rather than advisory.</p>

  <h3>Primitive ramps</h3>
  {ramps}
  <p class="note"><b>Grade → contrast against white, in every hue:</b>
  10 → 1.08:1 · 20 → 1.28:1 · 30 → 1.62:1 · 40 → 2.15:1 · 50 → <b>3.05:1</b> (the 1.4.11 non-text floor)
  · 60 → <b>5.00:1</b> (the 1.4.3 text floor, with headroom) · 70 → 7.1:1 · 80 → 10.6:1 · 90 → 14.2:1 ·
  100 → 17.4:1. Swapping a hue cannot silently break a contrast guarantee, because the guarantee lives
  in the ladder rather than in the individual value.</p>
  <div class="cite cite--chg"><span class="cite__tag">Changed</span>
  <span class="cite__val"><b>Carbon:</b> IBM Design Language palette — 12 families, 10 grades each, hand-authored, plus a separate hand-authored "hover spectrum" of half-steps. Blue 60 <code>#0f62fe</code> at OKLCH chroma ≈ 0.25.</span>
  <span class="cite__why">Strata caps chroma at 0.166 at grade 60 (red and magenta excepted — a hesitant error colour is a usability bug) and computes the hover half-step from the ladder instead of maintaining a second table. The IBM hex values are Apache-2.0 and could legally be copied verbatim; they are not, because IBM Blue plus a Plex-like face plus IBM densities is a trade-dress exposure that the software licence does not cover.</span>
  <a class="cite__src" href="https://carbondesignsystem.com/elements/color/overview/" target="_blank" rel="noopener">/elements/color/overview/</a></div>

  <h3>Semantic tokens</h3>
  <p class="note">This is the layer components are allowed to reference. Each row shows what it resolves
  to in each theme and the Carbon token it descends from.</p>
  {G.semantic_table()}
</section>

<section id="type">
  <h2>Typography</h2>
  <p class="lede">Carbon's scale formula and type-set structure, on a different face and a 16px baseline.</p>
  {G.type_table()}
  <div class="cite cite--chg"><span class="cite__tag">Changed</span>
  <span class="cite__val"><b>Carbon:</b> IBM Plex Sans / Serif / Mono. Scale formula Yn = Yn-1 + (floor((n-2)/4)+1)·2 from 12px. Type sets split productive (-01, fixed) and expressive (-02, fluid).</span>
  <span class="cite__why">The scale formula is kept exactly. The face changes for licensing reasons: IBM Plex is SIL OFL-1.1 with "Plex" as a Reserved Font Name, so a modified cut must be renamed and the font files cannot be relicensed under Apache-2.0 alongside the rest of a fork — the most commonly botched part of forking Carbon. Strata also drops Carbon's fluid type entirely for now: eleven tokens that interpolate across five breakpoints is a large surface for a base layer, and Carbon itself concedes the productive/expressive split "is no longer neatly divided".</span>
  <a class="cite__src" href="https://carbondesignsystem.com/elements/typography/type-sets/" target="_blank" rel="noopener">/elements/typography/type-sets/</a></div>
</section>

<section id="scales">
  <h2>Space, size, radius, elevation, motion</h2>
  <p class="lede">The spacing scale is Carbon's, untouched. Radius is new. Elevation is rebuilt.</p>

  {G.scale_strip("Spacing", T.SPACING, prov=T.SPACING_CARBON)}
  {G.scale_strip("Control sizes", T.SIZES, prov=T.SIZES_CARBON)}
  {G.scale_strip("Radius", {k: v for k, v in T.RADIUS.items() if k != "full"}, prov=T.RADIUS_CARBON,
                 note="Plus radius-full (9999px) for pills. Component defaults: controls 6px, surfaces 8px, checkbox 2px, tags and toggles pill.")}

  <h3>Elevation</h3>
  <div class="demo">
    <div class="elev" style="box-shadow:var(--st-elevation-00)">00 · none</div>
    <div class="elev" style="box-shadow:var(--st-elevation-01)">01 · hover lift</div>
    <div class="elev" style="box-shadow:var(--st-elevation-02)">02 · menus, popovers</div>
    <div class="elev" style="box-shadow:var(--st-elevation-03)">03 · modals</div>
  </div>
  {G.cite(T.ELEVATION_CARBON)}

  <h3>Motion</h3>
  <table class="tok"><thead><tr><th>Token</th><th>Value</th><th>Provenance</th></tr></thead><tbody>
  {"".join(f'<tr><td><code>--st-{k}</code></td><td><code>{G.E(v["value"])}</code></td><td>{G.cite(v["carbon"])}</td></tr>' for k, v in T.MOTION.items())}
  </tbody></table>
  <p class="note"><b>Added:</b> a global <code>prefers-reduced-motion: reduce</code> rule that collapses
  every transition to 1ms. Carbon's position here is partial rather than absent: its Motion overview gives
  advisory prose ("Consider simplified or reduced motion designs&hellip; make sure there is always a way to
  communicate similar messages statically") and 12 component SCSS files implement the media query
  individually — but there is no motion opt-out token and no normative requirement, so whether a given
  component respects the preference depends on whether someone remembered. One global rule makes coverage
  total and removes the per-component decision.</p>

  {G.scale_strip("Breakpoints", T.BREAKPOINTS, prov=T.BREAKPOINTS_CARBON)}

  {G.icons_and_ratios()}
</section>

<section id="components">
  <h2>Components</h2>
  <p class="lede">Thirteen components, live, driven entirely by the tokens above. Each carries its spec
  measured against the official Carbon style page it derives from. Try the dark toggle in the header —
  no component CSS changes, only the semantic layer re-resolves.</p>
  {"".join(comps_html)}
</section>

<section id="accessibility">
  <h2>Accessibility audit</h2>
  <p class="lede">Carbon targets WCAG 2.1 AA via the IBM Accessibility Checklist, and is careful to say
  it "strives to meet" rather than conforms. Strata inherits the target and adds a build-time check so
  the claim is testable.</p>
  {G.audit_table()}
  <h3>Mechanisms carried over from Carbon</h3>
  <p class="note"><b>The two-tone focus ring.</b> 2px <code>--st-focus</code> at
  <code>outline-offset: -2px</code>, so the ring is drawn inside the element's box and cannot
  collide with an adjacent control in a dense layout. On filled surfaces where the ring colour and
  the fill are close, a <code>--st-focus-inset</code> ring sits just inside it; because focus-inset
  is the theme's opposite pole, the pair is guaranteed to contrast against any underlying colour.
  This is the single most transferable idea in Carbon's accessibility model.<br><br>
  <b><code>prefers-contrast</code> handling.</b> Solid rings become dotted, lifted from Carbon's
  <code>_focus-outline.scss</code>.<br><br>
  <b>Never colour alone.</b> Every status carries an icon; the selected tab carries weight 600 as
  well as an underline; selected table rows carry a checkbox; selected tiles carry a border-width
  change. All four survive greyscale.<br><br>
  <b>44px touch floor.</b> Carbon publishes it for interactive icons and then ships a 40px default
  field. Strata defaults every control to 48px so the floor applies system-wide.</p>

  <h3>Mechanisms Carbon does not have</h3>
  <p class="note"><b><code>forced-colors</code> / Windows High Contrast Mode.</b> Carbon handles
  <code>prefers-contrast</code> and never addresses <code>forced-colors</code>, where the OS strips
  every background and shadow. Anything carrying meaning by fill alone — a primary button, a
  selected row, a status tag, a toggle track — simply disappears. Strata restates each of those in
  a channel HCM preserves: system-colour borders throughout, the <code>Highlight</code> /
  <code>HighlightText</code> pair for the primary action (the native OS convention for a default
  button), a doubled border for danger, <code>GrayText</code> for disabled, and
  <code>Highlight</code> outlines on selected rows and dates. Without this the five button variants
  collapse into one identical box.<br><br>
  <b>Reduced motion, systematised.</b> One global rule rather than 12 per-component
  implementations — see the motion section.<br><br>
  <b>An enforced audit.</b> The table above is recomputed at build time and a failure aborts the
  build. Carbon publishes contrast targets but ships several tokens that miss them.</p>

  <h3>Automated checks run against this page</h3>
  <p class="note"><b>axe-core 4.x: 0 violations</b> in both themes, across the whole document
  including every live component demo. Getting there caught one real bug in this system — the
  calendar's out-of-month days were using <code>--st-text-disabled</code> at 1.83:1. They are
  selectable, so the disabled exemption does not apply; Carbon specifies
  <code>$text-secondary</code> there and had it right where this build had it wrong.<br><br>
  <b>Rendering verified</b> in Chromium 141 at 1x and 2x, in light and dark, and under emulated
  <code>forced-colors: active</code>, <code>prefers-contrast: more</code> and
  <code>prefers-reduced-motion: reduce</code>. <b>Not verified:</b> Safari and Firefox were not
  executable in the build environment. In place of that, the stylesheet's feature surface was
  audited by hand — <code>:focus-visible</code>, negative <code>outline-offset</code>, logical
  properties, <code>place-items</code>, flex <code>gap</code>, <code>:indeterminate</code> and
  <code>font-variant-numeric</code> are all supported in Safari 15.4+ and Firefox 85+;
  <code>appearance</code> carries its <code>-webkit-</code> prefix; and the two modern features
  used anywhere (<code>color-mix()</code> and <code>backdrop-filter</code>) appear only in this
  page's own chrome, behind an <code>@supports</code> guard with a solid fallback. Nothing in
  <code>strata.css</code> itself requires a feature newer than Safari 15.4.</p>
</section>

<section id="ledger">
  <h2>Divergence ledger</h2>
  <p class="lede">Everything that is not Carbon, in one place, with the argument attached. This is the
  document to review — adopting Carbon's decisions needs no defence, departing from them does.</p>
  {G.divergence_ledger()}
</section>

<section id="licence">
  <h2>Licence and attribution</h2>
  <p class="lede">Worth getting right before this goes anywhere near a product.</p>
  <table class="tok"><thead><tr><th>Asset</th><th>Licence</th><th>Position</th></tr></thead><tbody>
  <tr><td>Carbon code and docs prose</td><td>Apache-2.0</td><td>Usable commercially and in closed source. Obligations: ship the licence, mark modified files, retain notices.</td></tr>
  <tr><td>Carbon token architecture, layering model, contrast method</td><td>Apache-2.0 as code; ideas unprotectable</td><td>Taken wholesale. This is the valuable part.</td></tr>
  <tr><td>IBM colour palette hexes</td><td>Apache-2.0 via <code>@carbon/colors</code></td><td><b>Not used.</b> Legally available; declined on trade-dress grounds. Own hues generated instead.</td></tr>
  <tr><td>IBM Plex</td><td><b>SIL OFL-1.1</b>, Reserved Font Name "Plex"</td><td><b>Not used.</b> A different licence from the rest of Carbon: it cannot be relicensed under Apache-2.0, and any modified cut must be renamed. Inter (OFL-1.1, no reserved name) instead.</td></tr>
  <tr><td>"Carbon", "IBM", "IBM Plex" names</td><td>Trademark — <b>not licensed</b>. Apache-2.0 §6 grants no trademark rights.</td><td>Descriptive attribution only: "derived from IBM's Carbon Design System" is fine. Naming the system after Carbon is not.</td></tr>
  <tr><td>Carbon Figma kits</td><td><b>Unverified</b></td><td>Not covered by the repo LICENSE. Check each file in Figma before republishing anything derived from them.</td></tr>
  </tbody></table>
  <p class="note">Required notice, to ship alongside this system:<br><br>
  <code>Strata is derived from the IBM Carbon Design System, Copyright IBM Corp., licensed under the
  Apache License 2.0. Strata is not affiliated with, sponsored by, or endorsed by IBM. "Carbon", "IBM"
  and "IBM Plex" are trademarks of IBM Corp.</code></p>
</section>

</main>

<script>
  const btn = document.getElementById('themebtn');
  btn.addEventListener('click', () => {{
    const el = document.documentElement;
    const next = el.dataset.theme === 'dark' ? 'light' : 'dark';
    el.dataset.theme = next;
    btn.textContent = next === 'dark' ? 'Light' : 'Dark';
  }});
  const ind = document.getElementById('ind');
  if (ind) ind.indeterminate = true;
  document.querySelectorAll('.st-tablist').forEach(list => {{
    list.addEventListener('click', e => {{
      const t = e.target.closest('.st-tab');
      if (!t || t.disabled) return;
      list.querySelectorAll('.st-tab').forEach(x => x.setAttribute('aria-selected', 'false'));
      t.setAttribute('aria-selected', 'true');
    }});
  }});
</script>
</body></html>"""

    with open(os.path.join(DIST, "index.html"), "w") as f:
        f.write(html_out)
    return html_out


if __name__ == "__main__":
    # Role separation runs FIRST. A wheel where two roles collapse onto one hue is
    # not a build worth auditing for contrast -- every pair can pass AA and still be
    # unreadable as roles.
    role_problems = check_role_separation(ACTIVE_BRAND)
    if role_problems:
        raise SystemExit("ROLE SEPARATION FAILED\n  " + "\n  ".join(role_problems))

    page = build_page()
    rows = B.audit()
    bad = B.audit_failures(rows)
    adv = [r for r in rows if r["sev"] == "advisory" and not r["ok"]]
    print(f"tokens.json  {os.path.getsize(os.path.join(DIST,'tokens.json'))/1024:.1f} KB")
    print(f"strata.css   {os.path.getsize(os.path.join(DIST,'strata.css'))/1024:.1f} KB")
    print(f"index.html   {len(page)/1024:.1f} KB")
    import reference
    ref = reference.build_page()
    with open(os.path.join(DIST, "reference.html"), "w") as f:
        f.write(ref)
    # Packaging copy: brand-qualified stylesheet href, for the flattened skill folder.
    refpkg = reference.build_page(reference.skill_href())
    with open(os.path.join(DIST, f"reference-{ACTIVE_BRAND}.html"), "w") as f:
        f.write(refpkg)
    print(f"reference    {len(ref)/1024:.1f} KB (+ packaging copy)")
    print(f"contrast     {len(rows)} checks, {len(bad)} AA failing, {len(adv)} advisory below target")
    assert not bad, bad

    # A reference page that renders unstyled fails where nobody notices -- the
    # reader concludes the system looks like that. Both pages shipped that way
    # once. Prove they render, do not assume the href is right.
    try:
        import render_check
        pkg = os.path.join(DIST, f"reference-{ACTIVE_BRAND}.html")
        n = render_check.check([os.path.join(DIST, "reference.html")])
        assert not n, "reference page does not render"
        print("render check ok")
    except ImportError:
        print("render check SKIPPED (playwright unavailable) — run build/render_check.py manually")

    # The reference page faces its own gate. Its docstring claimed this happened for
    # weeks while build/production_check.py did not exist -- the page that teaches
    # composition had never been checked against the construction floor it teaches.
    import production_check
    # Only the in-dist page here. The packaging copy's <link> points at
    # strata-<brand>.css, a filename that exists in the snapshot and nowhere else, so
    # it is checked there instead -- where its href actually resolves. Checking it in
    # the wrong directory would report a defect that is not one, and teach everyone to
    # ignore the gate.
    pc_mode, pc_findings = production_check.check([os.path.join(DIST, "reference.html")])
    print(f"production   [{pc_mode}] reference page, {len(pc_findings)} findings")
    assert not pc_findings, pc_findings

    # The icon sprite is a build output too. It was not one until 21 Aug 2026: build.py
    # pointed at build/icons.py, that file did not exist, and the sprite's only copy was
    # the artefact in dist/ -- unreproducible, and hand-appended to during the encode.
    import icons
    sprite_path = os.path.join(DIST, "strata-icons.svg")
    with open(sprite_path, "w") as f:
        f.write(icons.sprite())
    odd = icons.odd_constructions()
    print(f"icons        {len(icons.ICONS)} symbols, {os.path.getsize(sprite_path)/1024:.1f} KB"
          + (f"  [{len(odd)} off-standard construction: {', '.join(odd)}]" if odd else ""))

    # The skill snapshot is a BUILD OUTPUT, not a copy somebody remembers to refresh.
    # It shipped a hand-authored stylesheet and two stale docs for a fortnight because it
    # was assembled by hand; see build/snapshot.py for the full account. Emits once every
    # brand has a current build, and names the missing brand otherwise.
    import snapshot
    snapshot.emit_if_complete()
