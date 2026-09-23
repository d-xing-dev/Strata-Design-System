#!/usr/bin/env python3
"""Assert that the reference pages actually render styled.

A reference page whose stylesheet link does not resolve fails in the direction
where nobody notices: it renders as unstyled HTML, and a reader concludes the
system looks like that. Both pages shipped that way once -- they linked
`strata.css` into a folder that only contained `strata-<brand>.css`.

So this does not check that the file exists. It opens the page and asserts a
computed style that can only be true if the stylesheet loaded.
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

CHECKS = [
    (".st-shell__header", "position", "sticky"),
    (".st-table th",      "height",   lambda v: v not in ("auto", "0px")),
    (".st-statusband",    "display",  "flex"),
]


def check(paths) -> int:
    failures = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for path in paths:
            pg = b.new_page()
            pg.goto("file://" + str(pathlib.Path(path).resolve()))
            # Probe a custom property that only the external stylesheet defines.
            # cssRules is unreadable for file:// sheets, so ask the cascade instead.
            token = pg.evaluate(
                "getComputedStyle(document.documentElement)"
                ".getPropertyValue('--st-grid-columns').trim()")
            if token != "16":
                failures.append(f"{path}: stylesheet did not load "
                                f"(--st-grid-columns read {token!r}) — check the <link href>")
                pg.close()
                continue
            for sel, prop, want in CHECKS:
                got = pg.evaluate(
                    "([s,p]) => { const e = document.querySelector(s); "
                    "return e ? getComputedStyle(e)[p] : null }", [sel, prop])
                ok = want(got) if callable(want) else got == want
                if not ok:
                    failures.append(f"{path}: {sel} {prop} = {got!r}, expected {want!r}")
            pg.close()
        b.close()
    for f in failures:
        print("  RENDER CHECK FAILED:", f)
    return len(failures)


if __name__ == "__main__":
    n = check(sys.argv[1:])
    print(f"render check {len(sys.argv)-1} pages, {n} failures")
    sys.exit(1 if n else 0)
