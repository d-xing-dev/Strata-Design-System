#!/usr/bin/env python3
"""The construction floor, executed. Runs at every render, and it is the Bound gate.

THIS FILE IS THE SOURCE OF TRUTH, 21 Aug 2026. It used to say an identical copy lived
here in the repo and that the build ran it against the reference page. Neither was
true: the file did not exist and the reference page had never faced its own gate. It
does now -- `make.py` runs this against the generated reference page every build, and
`snapshot.py` emits it into `dist/skill-snapshot/`, which is how the UX skills receive
it. One copy, generated outward. "If you change one, copy it to the other" was the
instruction that produced the drift; there is nothing to copy any more.

Bound means the screen is the product: good enough to put in front of a client or an
end user, with nothing expected to change afterwards except copy. That is a strong
claim, and a claim is only worth the check behind it. A weak gate under a strong
promise is worse than no promise -- it ships artefacts labelled production-ready that
are not. The floor itself is not Bound-only: one construction standard applies from
the first Draft, so this runs at every render and the gate is the same check with
`--require-full`.

    python3 production-check.py screen.html [more.html ...]
    python3 production-check.py --allow=my-harness-class screens/*.html
    python3 production-check.py --system-css=dist/deloitte/strata.css screen.html
    python3 production-check.py --allow-override=st-tablist,st-table-wrap screen.html
    python3 production-check.py --screenshots=shots/ --require-full screens/*.html

Exit 0 clean, 1 with findings.

`--screenshots=DIR` (full mode only) captures every screen at every declared width in both
themes into DIR. The captures exist to serve the LOOKING-GATE: this script checks correctness,
and no script can check composition -- whether the eye lands on the anchor, whether declared
groups read as groups, whether declared edges align. Those are judged by a reviewer looking at
these captures against the screen's composition spec, per
`design-screen-compositions/references/composition-contract.md`. The capture is automated so the
looking never silently stops happening; the judgement is not automated because it cannot be.

TWO MODES, AND IT ALWAYS TELLS YOU WHICH IT RAN
-----------------------------------------------
  full    Playwright is importable. Renders each screen at every declared desktop
          width in both themes. Adds overflow detection and proves the stylesheet
          actually resolved.
  static  Playwright is not available. Parses the markup with the standard library.
          Catches six of the eight conditions; cannot see layout.

**A partial check reported as a full one is the exact failure this gate exists to
stop**, so the mode is printed every run and `--require-full` refuses to pass in
static mode. Use that flag when the result is going on an artefact.

    pip install playwright && playwright install chromium

WHAT IT CHECKS
--------------
  both modes:  placeholder copy · accessible names · keyboard reachability ·
               `.st-table__rowlink` with no <a> inside · classes outside the
               system · the stylesheet <link> resolves to a file that exists ·
               the embedded generated stylesheet is byte-identical to the built
               one · a local rule redefining a system class is declared
  full only:   horizontal overflow at each width · the stylesheet actually
               applied (a token resolves in the computed style) · every `st-`
               class in the rendered DOM is defined by some stylesheet
  neither:     axe-core. Run it separately -- see the note at the bottom.

THE PRODUCT REGION
------------------
An artefact is a production-built screen inside a review document. The collapsed
bar, region codes and popovers, the review panel, assumption lists and any harness
control are review affordances: they belong in the file and not in the product.

  `.st-review` or `data-review`  -> review chrome. Skipped here, deleted on build.
  `[data-product]`               -> the product. Nothing inside it may be chrome.

If nothing carries `[data-product]`, everything outside review chrome is treated
as product.
"""
from __future__ import annotations
import sys, pathlib, json, re
from html.parser import HTMLParser

PLACEHOLDER_MARKERS = ["lorem ipsum", "todo", "tbc", "tbd", "xxx", "placeholder",
                       "dummy text", "sample text", "foo bar", "asdf"]

# Desktop only, and that is a recorded scope decision rather than an oversight:
# the shell hides the rail below 672px and puts nothing in its place, so a product
# claiming production-readiness on a phone would be claiming something untrue.
WIDTHS = [1024, 1280, 1584]

# [6 Sep 2026] The two conditions below were added after an artefact reached BOUND
# carrying three retired type classes and four workarounds for components the system had
# already shipped. Neither was caught, and the reason is worth stating: the bespoke-class
# check only ever flagged classes that do NOT start with `st-`, so `.st-heading-lg` --
# retired months earlier and resolving to nothing at all -- read as a system class and
# passed every gate. Every page title in that artefact rendered as body text.
#
# The governing rule, from PATTERNS.md: a document that asserts a capability or a
# condition must be CHECKABLE, and an assertion that outlives its condition is a defect
# rather than stale prose. A proposal that says "the system does not have this yet" is
# exactly such an assertion, and it is mechanically checkable, because it names a class.
#
#   SYSTEM_MARKER    the first line the generator writes. A <style> block carrying it
#                    claims to BE the generated stylesheet, so with --system-css it is
#                    compared against the real one. Appending a proposal to that block --
#                    which is how those four survived -- fails here.
#   dead classes     an `st-` class in the rendered DOM that no stylesheet defines.
#                    Needs the DOM, so it is full mode only: a screen whose markup is
#                    built by script has almost no static markup to read.
#   overrides        a local rule redefining a class the system already defines. Not
#                    forbidden -- a workaround pending a system fix is legitimate -- but
#                    it must be DECLARED with --allow-override, so it is a decision
#                    somebody made rather than a duplicate nobody noticed.
SYSTEM_MARKER = "Strata — generated by build/build.py"
CLASS_RE = re.compile(r"\.(st-[A-Za-z0-9_-]+)")
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


def css_classes(text: str) -> set[str]:
    """Every `st-` class a stylesheet DEFINES, comments excluded.

    Excluding comments is not tidiness. This system documents a retired class by NAMING
    it -- the type-utility block says in prose that `.st-heading-lg` and `.st-label-sm`
    are gone -- so a regex over the raw text counts the retired names as defined and the
    check silently passes the exact defect it was written to catch. Caught by running the
    new check against a fixture rather than by trusting that it worked.
    """
    return set(CLASS_RE.findall(COMMENT_RE.sub(" ", text)))

INTERACTIVE = {"a", "button", "input", "select", "textarea", "summary"}
NAMEABLE = {"button", "a", "input", "select", "textarea"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


# ---------------------------------------------------------------------------
# static mode
# ---------------------------------------------------------------------------

class _Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []            # [(tag, attrs, is_review, is_product)]
        self.findings_raw = {"placeholders": [], "unreachable": [], "unlabelled": [],
                             "bespoke": set()}
        self.stylesheets = []
        self.styles = []            # text of each <style> block, in document order
        self.labels_for = set()
        self.has_product_marker = False
        self._text_owner = None
        self._text = []
        self._pending = []          # (tag, attrs, path) awaiting text

    # -- helpers
    def _is_review(self, attrs):
        cls = attrs.get("class", "")
        return "st-review" in cls.split() or "data-review" in attrs

    def _in_review(self):
        return any(r for (_t, _a, r, _p) in self.stack)

    def _in_product(self):
        if not self.has_product_marker:
            return True
        return any(p for (_t, _a, _r, p) in self.stack)

    def handle_starttag(self, tag, attrs_list):
        attrs = {k: (v or "") for k, v in attrs_list}
        if "data-product" in attrs:
            self.has_product_marker = True
        review = self._is_review(attrs) or self._in_review()
        product = "data-product" in attrs or self._in_product()
        if tag not in VOID:
            self.stack.append((tag, attrs, review, product))

        if tag == "link" and "stylesheet" in attrs.get("rel", ""):
            self.stylesheets.append(attrs.get("href", ""))
        if tag == "label" and attrs.get("for"):
            self.labels_for.add(attrs["for"])

        if review or not product:
            return

        for c in attrs.get("class", "").split():
            if c and not c.startswith("st-"):
                self.findings_raw["bespoke"].add(c)

        if tag in INTERACTIVE:
            ti = attrs.get("tabindex")
            if ti and ti.lstrip("-").isdigit() and int(ti) < 0:
                self.findings_raw["unreachable"].append((tag, attrs.get("class", "")))

        if tag in NAMEABLE:
            self._pending.append((tag, attrs, len(self.stack)))
            self._text = []

    def handle_data(self, data):
        txt = data.strip()
        # style/script text is code, not copy: '.st-step--todo' is a class name,
        # not a TODO. Placeholder markers apply to rendered text only.
        if self.stack and self.stack[-1][0] == "style":
            self.styles.append(data)
        if any(t == "style" or t == "script" for (t, _a, _r, _p) in self.stack):
            return
        if not txt or self._in_review() or not self._in_product():
            return
        self._text.append(txt)
        low = txt.lower()
        for m in PLACEHOLDER_MARKERS:
            if m in low:
                self.findings_raw["placeholders"].append((m, txt[:60]))
                break

    def handle_endtag(self, tag):
        while self.stack and self.stack[-1][0] != tag:
            self.stack.pop()
        if self._pending and self._pending[-1][0] == tag:
            t, attrs, _d = self._pending.pop()
            name = (attrs.get("aria-label") or attrs.get("title") or
                    " ".join(self._text)).strip()
            labelled = attrs.get("aria-labelledby") or (attrs.get("id") in self.labels_for) \
                or any(s[0] == "label" for s in self.stack)
            if not name and not labelled and t != "a":
                self.findings_raw["unlabelled"].append((t, attrs.get("class", "")))
            self._text = []
        if self.stack:
            self.stack.pop()


def _defined_classes(path: pathlib.Path, system_css=None):
    """Every `st-` class defined by any stylesheet this document can actually reach.

    Read from disk rather than from the CSSOM, for the reason given in PROBE. Returns
    None when nothing could be read at all, which is a different answer from "nothing is
    defined" and must not be reported as a clean result.
    """
    texts = []
    if system_css:
        try:
            texts.append(pathlib.Path(system_css).read_text(errors="replace"))
        except OSError:
            pass
    src = path.read_text(errors="replace")
    sc = _Scan()
    sc.feed(src)
    texts.extend(sc.styles)
    for href in sc.stylesheets:
        if href.startswith(("http://", "https://", "data:")):
            continue
        f = path.parent / href
        if f.exists():
            texts.append(f.read_text(errors="replace"))
    if not any(t.strip() for t in texts):
        return None
    return css_classes("\n".join(texts))


def _static(path: pathlib.Path, allow, system_css=None,
            allow_override=()) -> list[str]:
    src = path.read_text(errors="replace")
    s = _Scan()
    s.feed(src)
    out = []
    for m, txt in s.findings_raw["placeholders"]:
        out.append(f"placeholder copy ({m!r}) — {txt!r}")
    for t, c in s.findings_raw["unreachable"]:
        out.append(f"not keyboard-reachable — <{t}> class={c!r}")
    for t, c in s.findings_raw["unlabelled"]:
        out.append(f"no accessible name — <{t}> class={c!r}")
    extra = sorted(c for c in s.findings_raw["bespoke"] if c not in allow)
    if extra:
        out.append(f"{len(extra)} classes outside the system and outside review "
                   f"chrome: {extra[:10]}")
    # a row styled as navigating with no link inside is unreachable AND invisible
    for row in re.findall(r'<tr[^>]*class="[^"]*st-table__rowlink[^"]*"[^>]*>(.*?)</tr>',
                          src, re.S):
        if not re.search(r"<a\s[^>]*href=", row):
            out.append("`.st-table__rowlink` with no <a> inside — unreachable by "
                       "keyboard, invisible to a screen reader, looks correct")
            break
    for href in s.stylesheets:
        if href.startswith(("http://", "https://", "data:")):
            continue
        if not (path.parent / href).exists():
            out.append(f"stylesheet <link href={href!r}> does not exist next to this "
                       f"file — the screen renders unstyled")

    system_blocks = [b for b in s.styles if SYSTEM_MARKER in b]
    local_blocks = [b for b in s.styles if SYSTEM_MARKER not in b]

    if system_css:
        want = pathlib.Path(system_css).read_text(errors="replace")
        for b in system_blocks:
            if b.strip() != want.strip():
                extra = len(b.strip()) - len(want.strip())
                out.append(
                    "the embedded generated stylesheet is not the generated stylesheet "
                    f"({extra:+d} bytes against {system_css}) — anything added to that "
                    "block inherits the authority of generated CSS, which is how four "
                    "hand-written components once read as system ones")
        if not system_blocks and not s.stylesheets:
            out.append("no generated stylesheet found in this document — it carries no "
                       "<style> with the build marker and no <link>")

    if system_blocks or system_css:
        system_css_text = (pathlib.Path(system_css).read_text(errors="replace")
                           if system_css else "\n".join(system_blocks))
        system_classes = css_classes(system_css_text)
        redefined = set()
        for b in local_blocks:
            redefined |= css_classes(b) & system_classes
        undeclared = sorted(c for c in redefined if c not in allow_override)
        if undeclared:
            out.append(
                f"{len(undeclared)} local rule(s) redefine a class the system already "
                f"defines, undeclared: {undeclared[:10]} — either the system rule is "
                "wrong and this is a finding, or the local copy is stale. Declare it "
                "with --allow-override= if it is a workaround you have decided to keep")
    return out


# ---------------------------------------------------------------------------
# full mode
# ---------------------------------------------------------------------------

PROBE = r"""
() => {
  const REVIEW = '.st-review, [data-review]';
  const scope = document.querySelector('[data-product]') || document.body;
  const inReview = el => el.closest(REVIEW) !== null;
  const vis = el => { const s = getComputedStyle(el);
    return s.display !== 'none' && s.visibility !== 'hidden' && el.offsetParent !== null; };
  const all = [...scope.querySelectorAll('*')].filter(e => !inReview(e));
  const out = {overflow: [], styled: null, used: []};

  // What the product markup USES. The browser is asked ONLY this, because it is the half
  // the browser alone can answer -- a screen whose markup is built by script has almost
  // no static markup to read, and this is the only place the rendered classes exist.
  // What the stylesheets DEFINE is read from disk in Python instead: Chromium refuses
  // `cssRules` on any sheet loaded over file://, so asking the CSSOM here reported every
  // class in the document as undefined, all 164 of them, every one of them correct.
  const used = new Set();
  for (const el of all) for (const c of el.classList) if (c.startsWith('st-')) used.add(c);
  out.used = [...used].sort();
  out.styled = getComputedStyle(document.documentElement)
                 .getPropertyValue('--st-grid-columns').trim();
  for (const el of all) {
    if (!vis(el)) continue;
    if (el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflowX === 'visible')
      out.overflow.push({sel: el.tagName.toLowerCase() + '.' +
        ((el.className || '').toString().split(' ')[0] || ''), over: el.scrollWidth - el.clientWidth});
  }
  return out;
}
"""


def _full(paths, allow, shots_dir=None, system_css=None, allow_override=()):
    from playwright.sync_api import sync_playwright
    findings = []
    captured = 0
    if shots_dir:
        shots_dir = pathlib.Path(shots_dir)
        shots_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for path in paths:
            p = pathlib.Path(path)
            for f in _static(p, allow, system_css, allow_override):
                findings.append(f"{p.name}: {f}")
            used = set()
            for theme in ("light", "dark"):
                for w in WIDTHS:
                    pg = b.new_page(viewport={"width": w, "height": 900})
                    pg.goto("file://" + str(p.resolve()))
                    pg.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}')")
                    r = pg.evaluate(PROBE)
                    if theme == "light" and w == WIDTHS[0] and not r["styled"]:
                        findings.append(f"{p.name}: stylesheet did not apply "
                                        f"(--st-grid-columns is empty) — check the <link>")
                    used.update(r.get("used") or ())
                    for x in r["overflow"]:
                        findings.append(f"{p.name} [{theme} {w}px]: horizontal overflow "
                                        f"{x['over']}px on {x['sel']}")
                    if shots_dir is not None:
                        pg.screenshot(path=str(shots_dir / f"{p.stem}--{theme}--{w}.png"),
                                      full_page=True)
                        captured += 1
                    pg.close()
            # Reported once per file rather than once per width and theme: a dead class
            # is a property of the document, and six identical lines read as six defects.
            defined = _defined_classes(p, system_css)
            if defined is None:
                findings.append(f"{p.name}: no stylesheet could be read from disk, so "
                                f"whether its classes resolve was NOT checked — say so "
                                f"rather than reporting this screen as clean")
            else:
                dead = sorted(c for c in used if c not in defined)
                if dead:
                    findings.append(
                        f"{p.name}: {len(dead)} class(es) used in the product markup that "
                        f"no stylesheet defines — they style nothing: {dead[:10]}")
        b.close()
    if shots_dir is not None:
        findings_note = (f"captured {captured} screenshots into {shots_dir}/ for the "
                         f"looking-gate — judge them against each screen's composition spec")
        print("  SCREENSHOTS:", findings_note)
    return findings


# ---------------------------------------------------------------------------

def check(paths, allow=(), require_full=False, shots_dir=None,
          system_css=None, allow_override=()):
    try:
        import playwright  # noqa: F401
        mode = "full"
    except ImportError:
        mode = "static"
    if mode == "full":
        findings = _full(paths, allow, shots_dir, system_css, allow_override)
    else:
        if shots_dir:
            print("  SCREENSHOTS: not captured — static mode has no browser. The "
                  "looking-gate cannot run on this invocation; do not report it as run.")
        findings = [f"{pathlib.Path(p).name}: {f}"
                    for p in paths
                    for f in _static(pathlib.Path(p), allow, system_css, allow_override)]
    return mode, findings


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    allow = tuple(x for a in sys.argv[1:] if a.startswith("--allow=")
                  for x in a[len("--allow="):].split(",") if x)
    require_full = "--require-full" in sys.argv
    system_css = next((a[len("--system-css="):] for a in sys.argv[1:]
                       if a.startswith("--system-css=")), None)
    allow_override = tuple(x for a in sys.argv[1:] if a.startswith("--allow-override=")
                           for x in a[len("--allow-override="):].split(",") if x)
    shots_dir = next((a[len("--screenshots="):] for a in sys.argv[1:]
                      if a.startswith("--screenshots=")), None)
    if not args:
        print(__doc__)
        sys.exit(2)

    mode, findings = check(args, allow, require_full, shots_dir,
                           system_css, allow_override)
    for f in findings:
        print("  PRODUCTION CHECK:", f)

    print(f"\nproduction check [{mode}] — {len(args)} screens, {len(findings)} findings")
    if mode == "static":
        print("  NOT CHECKED in static mode: horizontal overflow, and whether the "
              "stylesheet actually applied.")
        print("  Install playwright for the full gate, or state on the artefact that "
              "the gate ran partially.")
    print("  NOT CHECKED in either mode: axe-core. It needs a browser and a copy of "
          "axe.min.js; run it")
    print("  separately against every screen in both themes. It is a gate condition, "
          "not an optional extra —")
    print("  three real defects in this system were found by axe and by nothing else.")

    failed = bool(findings) or (require_full and mode != "full")
    if require_full and mode != "full":
        print("\n  --require-full was set and the full gate could not run. Not a pass.")
    sys.exit(1 if failed else 0)
