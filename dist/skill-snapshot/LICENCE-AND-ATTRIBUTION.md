# Licence and attribution

Strata is a derivative of the IBM Carbon Design System. This is the part to get right before
it goes near a product. Nothing here is legal advice — it is a summary of what the licences
actually say, with sources, so you can brief someone who does give legal advice.

---

## 1. Carbon code and documentation — Apache License 2.0

Both `github.com/carbon-design-system/carbon` and `github.com/carbon-design-system/carbon-website`
carry `LICENSE` = Apache-2.0. Every source file is headed
`Copyright IBM Corp. 2018, 2026 ... licensed under the Apache-2.0 license`.

Note that this covers **the guidance prose too**, not just the code — the accessibility rules,
the token documentation, the content guidelines are all Apache-2.0 licensed, not merely readable.

**What it grants:** use, reproduce, modify, distribute, sublicense and sell derivative works,
including commercially and in closed source. No copyleft.

**What it obliges (§4), all commonly missed:**

1. Give recipients a copy of the licence.
2. **Mark modified files as changed.**
3. Retain all copyright, patent, trademark and attribution notices from the source.
4. If the original carries a `NOTICE` file, reproduce its attribution content. *(No `NOTICE`
   file was found at the root of either repo, so this appears inapplicable — verify at the
   moment you fork.)*

**The clause that constrains you — §6, Trademarks:**

> "This License does not grant permission to use the trade names, trademarks, service marks,
> or product names of the Licensor, except as required for reasonable and customary use in
> describing the origin of the Work and reproducing the content of the NOTICE file."

The code is yours to take. The names are not.

---

## 2. IBM Plex — SIL Open Font License 1.1, with a Reserved Font Name

**This is a different licence from the rest of Carbon**, and it is the most commonly botched
part of forking Carbon.

`github.com/IBM/plex` → `LICENSE.txt`:
> "Copyright © 2017 IBM Corp. with **Reserved Font Name 'Plex'**. This Font Software is
> licensed under the SIL Open Font License, Version 1.1."

- ✅ Bundle it, embed it, self-host it, ship it commercially, modify it.
- ❌ Sell the font on its own.
- ❌ Use "Plex" in the name of any modified version. It is a Reserved Font Name; a fork must
  be renamed.
- ❌ **Relicense the font, or any derivative of it, under anything other than OFL-1.1 —
  including under Apache-2.0.** If you ship Plex inside an Apache-2.0 design system, the font
  files remain OFL-1.1 and must carry their own licence text alongside them.

**Strata's position (revised 20 Aug 2026, ledger E-03):** the font stacks are **Plex-first
with Inter as first fallback**. No font files ship in this repository, so no OFL obligation is
live yet -- the stack is a reference the reader's system resolves. The constraints above become
real the day font files are bundled: ship Plex's `LICENSE.txt` beside them, never relicense
them, and never name a modified cut "Plex". The trade-dress caution below assumed Plex + IBM
Blue + IBM densities assembled together; Strata's palette is its own OKLCH ladder and its
densities diverged, so the face alone does not assemble the IBM look.

---

## 3. The IBM colour palette

`@carbon/colors` sits inside the Apache-2.0 monorepo, so the hex values are Apache-2.0
licensed — and colour values as such are generally not copyrightable in any case. You could
legally copy `#0f62fe`.

**Strata does not**, and the reason is not copyright. The palette is presented throughout
IBM's material as *the IBM Design Language colour palette*, and IBM Blue is a brand signature.
IBM Blue 60 + a Plex-like face + IBM densities produces something a reasonable observer might
take for an IBM product. That is a **trade dress / passing-off** exposure, and it is entirely
separate from the software licence — Apache-2.0 permitting the copy does not make it safe.

What Strata takes instead is the *architecture*: ten grades plus black and white, the half-step
hover rule, the ±2-step active rule, the contrast-steps method. That is the portion with the
engineering value, and it carries no brand risk. Hues are generated independently in
`build/color.py`.

---

## 4. The "Carbon" name

No explicit trademark statement for "Carbon" or "Carbon Design System" was found in either
repo — no `TRADEMARKS.md`, no `NOTICE`, no policy page on naming derivative systems. What is
on record is that IBM's own writing-style guide lists "Carbon" and "the Carbon Design System"
among terms taking a capital letter, i.e. treats it as a proper noun.

Apache-2.0 §6 therefore governs by default: **no trademark licence is granted.**

- ✅ "Derived from IBM's Carbon Design System" — descriptive, customary origin attribution.
- ❌ "<X> Carbon", "Carbon for <X>", or anything implying IBM origin or endorsement.
- Note IBM names its own internal derivatives "Carbon for IBM Products", "Carbon for Cloud",
  "Carbon for AI". That convention is available to IBM and not to you.

---

## 5. Carbon's Figma kits — CC BY 4.0

Resolved. Carbon's publicly distributed Figma kits are **not** covered by the repos' Apache-2.0
licence; they carry their own, and it is permissive.

The kit pages state it explicitly. https://www.figma.com/community/file/1157761560874207208
("(v11) Carbon Design System", by IBM and Lauren Rice) carries "Licensed under CC BY 4.0", as do
the sibling IBM Design Language kits the Carbon docs point external users at — the UI Icon Library
(`1089055340263947620`) and the Pictogram Library (`1089047716352012639`). This matches Figma's
own documented default: "Free files are published under an Attribution 4.0 International (CC BY
4.0) license," granting both Share and Adapt rights.

**A trap worth naming:** Figma's separate *Community Free Resource License* does forbid
derivatives and redistribution — but it governs **plugins and widgets**, not files. Carbon's kits
are files. Do not cite that instrument.

Corroborating: IBM's own precedent for distributing kit binaries is permissive.
`github.com/carbon-design-system/carbon-design-kit` ships the actual Sketch files under a full
Apache 2.0 `LICENSE`, as does `carbon-for-products-design-kit`.

**So: yes, you can republish a derivative of the public Carbon Figma kit**, subject to two
conditions that are the real work:

1. **Attribution (CC BY 4.0 §3(a)).** Credit IBM and the named creators, link to the CC BY 4.0
   deed, and state that you modified the file. Put it in the Figma file description and in your docs.
2. **Trademarks are excluded from both grants.** CC BY 4.0 §2(b)(2) says expressly that "Patent and
   trademark rights are not licensed under this Public License"; Apache-2.0 §6 is the parallel
   exclusion for the code. Strip IBM word marks, the 8-bar logo, "Carbon" as a product name, and
   the `logo--*` / `ibm-*` icons from anything you ship.

**One honest limit.** The CC BY 4.0 statement was read from the Figma-rendered file page; Figma
serves no raw equivalent. It reproduced identically across three separate IBM kit files and matches
Figma's platform default, so it is verified for practical purposes — but Figma lets a creator change
a file's licence at any time with no citable version history. **If this is going to legal, take your
own dated screenshot of the licence line before relying on it.**

## 5b. Carbon's icon library — Apache-2.0, no carve-out

`@carbon/icons` v11.85.0 ships **2,734 icons** (2,711 non-deprecated, which is what the website
library page renders) across 2,828 SVG assets. `package.json` declares `"license": "Apache-2.0"`;
the published tarball ships a full Apache 2.0 `LICENSE`; there is no `NOTICE` file and no
icon-specific restriction anywhere on carbondesignsystem.com or ibm.com/design/language.

The one caveat is trademarks again, and it is a real one: the library contains several hundred
`logo--*` and `ibm-*` marks (IBM, watsonx, and third-party brand logos). Apache-2.0 licenses the
*files*; it grants no rights in the *marks they depict*. If you take the set, filter those out.

## 6. Summary

| Asset | Licence | Use it? | Rename/rebrand? | Watch out |
|---|---|---|---|---|
| Carbon code (`@carbon/*`) | Apache-2.0 | Yes, incl. commercial & closed source | Yes — mark modified files, retain notices | §6: no trademark grant |
| Carbon docs prose | Apache-2.0 | Yes | Yes, with attribution | Same §6 |
| Token architecture, layering model, contrast method | Apache-2.0 as code; ideas unprotectable | Yes | Yes | — |
| IBM palette hexes | Apache-2.0 | Legally yes | Yes | Trade dress if combined with Plex + IBM Blue. **Strata declines.** |
| IBM Plex font files | **SIL OFL-1.1** | Yes — bundle, embed, ship, modify | **Must rename any fork** | **Cannot relicense under Apache-2.0.** Cannot sell standalone. **Strata references the face in its stacks (20 Aug 2026) but ships no files; obligations activate if files are ever bundled.** |
| "Carbon" / "IBM" / "IBM Plex" names | Trademark, **not licensed** | Descriptive attribution only | No | Naming the system after Carbon is out |
| Carbon Figma kits | **Unverified** | Verify per file | Verify | Not covered by the repo LICENSE |

---

## 7. Required notice

Ship this alongside the system (it is also in `NOTICE`):

```
Strata is derived from the IBM Carbon Design System, Copyright IBM Corp.,
licensed under the Apache License, Version 2.0. A copy of the licence is
available at http://www.apache.org/licenses/LICENSE-2.0

Files derived from Carbon have been modified. See LICENCE-AND-ATTRIBUTION.md
and the divergence ledger in dist/index.html for the nature of the changes.

Strata is not affiliated with, sponsored by, or endorsed by IBM.
"Carbon", "IBM" and "IBM Plex" are trademarks of IBM Corp.
```

---

## Sources

- https://github.com/carbon-design-system/carbon — `LICENSE`
- https://github.com/carbon-design-system/carbon-website — `LICENSE`
- https://github.com/IBM/plex — `LICENSE.txt`
- https://www.apache.org/licenses/LICENSE-2.0 — §4 Redistribution, §6 Trademarks
- https://scripts.sil.org/OFL — SIL Open Font License 1.1
- https://carbondesignsystem.com/guidelines/content/writing-style/ — capitalisation of "Carbon"
- https://carbondesignsystem.com/designing/kits/figma/ — Figma kit distribution
