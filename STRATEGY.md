# STRATEGY — news-image-20261120 v2: NIGHT EDITION

## The gap

Our v1 (submitted 20 Nov 2026) sits at a live score of **957,712**,
rank 7,585 of 14,865. The paid line (#50) is **989,060** — a gap of
**31,348**. #10 is 990,835; #1 is 992,057. The v1 lost because it was
a text newspaper with no drawn scenes, a generic masthead with a small
date, no numbers strip, no timeline, no date check, no confidence
marks, an unnumbered map, and it led with non-Friday stories (the
Shenzhen summit, the Kerch Bridge strike).

## What the winners do (top-10 study, 21 Nov ~13:35 WIB)

The top 10 all run 33–38 stories (not 46–52 — the count is a ceiling,
not the score), 6–7 regions, a giant date masthead, a UTC timeline
strip, a numbers strip, a region-count bar, three heroes with REAL
drawn scenes, ten small stories each with a small drawn scene + place
tag + source, a world map with numbered pins 1–13, an ALSO ON list,
a DATE CHECK box, and a sources line. Only #2 marks confidence
systematically. The field is ~14,800 near-identical cream front pages.

## Our recipe — same scored elements, different poster

**NIGHT EDITION.** A deep-navy masthead band whose giant date IS the
masthead ("FRIDAY 20 NOVEMBER 2026", cream serif), a red NIGHT EDITION
chip, cream body below. The thumbnail reads as a dark band at the top
of a cream page — instantly different from the field while the body
stays in the legible newspaper palette the judge rewards.

**Confidence as the signature system.** Every one of the 50 stories
carries three dots (filled = sureness): CONFIRMED (2+ outlets),
OFFICIAL (on the record), REPORTED (one outlet), plus a HOW SURE ARE
WE legend. Only #2 does this at all, and only partially. This is the
icantcodefyi recipe's core differentiator, applied everywhere.

**Real drawn scenes, not text.** Three heroes use the
editorial-illustration library: a broken bridge over the Dnipro
(Kyiv), a cyclone spiral over Odisha (Akvan), a falling red line
(AI sell-off). Ten small stories each get one motif (missile map,
thermometer, flags, skyline, ship, quake mountains, courthouse,
scales, border barrier, crowd). v1 had none of this.

**50 stories, all Friday.** 3 heroes + 10 small + 37 ALSO ON,
7 regions (Europe 8, Middle East 3, Asia 10, Africa 7, Americas 11,
Oceania 2, Global 9). Every story verified as Friday 20 November
2026; the near-misses are excluded in the DATE CHECK box with their
correct dates (Shenzhen summit Thu 19 Nov, Kerch Bridge strike
Tue 17 Nov, ICJ Myanmar verdict Thu 19 Nov, Anthropic IPO pricing
Thu 19 Nov, Van Gogh sale Wed 18 Nov, Voyager 1 Wed 18 Nov,
GTA VI launch Thu 19 Nov, BepiColombo capture Sat 21 Nov).

## What we deliberately did NOT copy

- No cream masthead, no generic "THE WORLD IN ONE DAY" title.
- No copying of any winner's story text, layout, or image.
- No Senegal migrant boat (top entries date it Thu 19 Nov) and no
  Senate Iran war-powers vote (date contested Thu/Fri) — both left out
  rather than risked.

## Build

`render_poster.py` renders `entry.png` at build time (Pillow +
editorial-illustration lib, page drawn at 2x and LANCZOS-downscaled).
`main.py` is pure stdlib: it copies the bundled `entry.png`
byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png`, then
`/output/entry.png`, then `output.png`. Tests run the program in a
temp dir and as uid 65534 on a read-only copy; output must be
byte-identical to the local render.
