#!/usr/bin/env python3
"""The shipping icon sprite -- `st-i-*` symbols, inlined once per document and referenced
with <use href="#st-i-name">.

RECOVERED SOURCE, 21 Aug 2026. build.py has always pointed here ("see build/icons.py for
why extraction was declined") but the file did not exist: the sprite's only copy was the
generated artefact in dist/, so it was unreproducible -- wipe dist/ and the drawings were
gone. Every path below was recovered verbatim from that artefact; nothing was redrawn. The
regenerated sprite is four bytes shorter than the recovered one, and the four bytes are
newlines that were left between hand-appended symbols. SVG ignores whitespace between
elements, so the render is unchanged; equivalence is verified symbol-by-symbol rather than
byte-by-byte, which is the check that actually means something.

This is a different set from guide.ICONS, the 16-grid filled set the documentation page
uses. Construction rules from Carbon: 32 grid, 2px padding, 16/20/24/32 sizes, stroke-based
rather than filled. Every icon is aria-hidden -- an icon carrying meaning alone is a defect,
and every component in this system pairs one with text.

KNOWN INCONSISTENCY, reported by odd_constructions() and not yet resolved: five symbols
added during the 20 Aug encode (grid, mail, box, clock, star) are drawn on a 16 viewBox with
stroke-width 1.4, where the rest of the set is a 32 viewBox with stroke-width 2. Rendered at
16px the standard set strokes at 1px and these five stroke at 1.4px -- roughly 40% heavier.
They do not look like the same family at small sizes. Redrawing them on the 32 grid is a
ledger event nobody has raised yet.
"""

from __future__ import annotations

WRAPPER = '<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true" data-strata-icons="1">'
STROKE_ATTRS = ' viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'

# (name, attrs_override_or_None, path markup) in sprite order.
ICONS: list[tuple[str, str | None, str]] = [
    ('chevron-right', None, '<path d="M12 7l9 9-9 9"/>'),
    ('chevron-down', None, '<path d="M7 12l9 9 9-9"/>'),
    ('close', None, '<path d="M8 8l16 16M24 8L8 24"/>'),
    ('check', None, '<path d="M6 17l7 7L26 9"/>'),
    ('search', None, '<circle cx="14" cy="14" r="8"/><path d="M20 20l6.5 6.5"/>'),
    ('sort', None, '<path d="M16 8l7 9H9z" fill="currentColor" stroke="none"/>'),
    ('success', None, '<circle cx="16" cy="16" r="12"/><path d="M10 16.5l4 4L22 12"/>'),
    ('warning', None, '<path d="M16 5l13 22H3z"/><path d="M16 13v6"/><path d="M16 22.5v.5"/>'),
    ('error', None, '<circle cx="16" cy="16" r="12"/><path d="M11 11l10 10M21 11L11 21"/>'),
    ('info', None, '<circle cx="16" cy="16" r="12"/><path d="M16 14v9"/><path d="M16 9.5v.5"/>'),
    ('menu', None, '<path d="M5 9h22M5 16h22M5 23h22"/>'),
    ('help', None, '<circle cx="16" cy="16" r="12"/><path d="M12.5 12.5a3.5 3.5 0 1 1 3.5 3.5V19"/><path d="M16 23v.5"/>'),
    ('settings', None, '<path d="M4 10h9M19 10h9M4 22h5M15 22h13"/><circle cx="16" cy="10" r="3"/><circle cx="12" cy="22" r="3"/>'),
    ('external', None, '<path d="M14 6h12v12"/><path d="M26 6L14 18"/><path d="M22 20v6H6V10h6"/>'),
    ('filter', None, '<path d="M4 7h24l-9 10v9l-6-3v-6z"/>'),
    ('more', None, '<circle cx="8" cy="16" r="1.6" fill="currentColor" stroke="none"/><circle cx="16" cy="16" r="1.6" fill="currentColor" stroke="none"/><circle cx="24" cy="16" r="1.6" fill="currentColor" stroke="none"/>'),
    ('grid', ' viewBox="0 0 16 16"', '<path d="M2.5 2.5h4.4v4.4H2.5zM9.1 2.5h4.4v4.4H9.1zM2.5 9.1h4.4v4.4H2.5zM9.1 9.1h4.4v4.4H9.1z" fill="none" stroke="currentColor" stroke-width="1.4"/>'),
    ('mail', ' viewBox="0 0 16 16"', '<path d="M2 3.5h12v9H2zM2 4.5l6 4.5 6-4.5" fill="none" stroke="currentColor" stroke-width="1.4"/>'),
    ('box', ' viewBox="0 0 16 16"', '<path d="M2 5l6-2.8L14 5v6l-6 2.8L2 11zM2 5l6 2.7L14 5M8 7.7v6" fill="none" stroke="currentColor" stroke-width="1.4"/>'),
    ('clock', ' viewBox="0 0 16 16"', '<circle cx="8" cy="8" r="5.6" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M8 4.8V8l2.4 1.6" fill="none" stroke="currentColor" stroke-width="1.4"/>'),
    ('star', ' viewBox="0 0 16 16"', '<path d="M8 2.4l1.7 3.5 3.8.6-2.8 2.7.7 3.8L8 11.2 4.6 13l.7-3.8L2.5 6.5l3.8-.6z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>'),
]


def sprite() -> str:
    """The full sprite document, generated from ICONS so the file in dist/ cannot drift
    from the definitions the components reference."""
    parts = [WRAPPER]
    for name, attrs, inner in ICONS:
        parts.append(f'<symbol id="st-i-{name}"{attrs or STROKE_ATTRS}>{inner}</symbol>')
    parts.append("</svg>")
    return "".join(parts)


def odd_constructions() -> list[str]:
    """Symbols off the standard 32-grid stroke construction. Reported rather than silently
    tolerated: a mixed grid is how an icon set stops reading as one set."""
    return [n for n, a, _ in ICONS if a is not None]


if __name__ == "__main__":
    print(f"{len(ICONS)} symbols, {len(sprite())} bytes")
    odd = odd_constructions()
    if odd:
        print("off-standard construction: " + ", ".join(odd))
