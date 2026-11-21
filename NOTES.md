# NOTES — news-image-20261120 v2

## Top-10 study (live leaderboard, 21 Nov 2026 ~13:35 WIB, 14,865 entries)

| Rank | Handle | Score (90% interval) | Title pattern |
|---|---|---|---|
| 1 | samatch-we | 992,057 (989,952–994,163) | 35 stories, 7 regions — Kyiv bridges, Akvan, AI sell-off, UK-EU deal |
| 2 | superskie | 991,696 | 33 stories, 7 regions, 15 fields |
| 3 | 888dao-sats | 991,652 | 36 stories, 6 continents — Akvan, Kyiv ballistic, COP31 deadlock |
| 10 | momo-devlog | 990,835 | "One day of world news: Friday 20 November 2026" |
| 50 (paid line) | siriusjack | 989,060 | — |
| Ours (v1) | ci3hu1 | 957,712 (944,444–970,981) | rank 7,585; 8 wins / 3 draws / 1 loss in 12 matches |

All ten withhold source. Study used visible titles, scores, byte
sizes, and the rendered artifact images of #1–#3 plus our v1.

**What the winners do:** 33–38 stories (not 46–52 — the icantcodefyi
count is a ceiling from NI17/18/19; NI20's winners run 33–38 with
better curation), 6–7 regions, giant date masthead, UTC timeline
strip (e.g. 00:00 Kyiv bridges, 02:00 Akvan landfall, 05:30 Taiwan
-6.2%, 05:50 missile in Poland, 15:00 COP31 past close, 21:00 S&P
-3.7%), numbers strip (111 missiles, 3 bridges, 372,000 evacuated,
-3.7%, -14%, 60.7%), region-count bar, 3 heroes with REAL drawn
scenes, 10 small stories each with a small drawn scene + place tag +
source, world map with numbered pins 1–13, ALSO ON list, DATE CHECK
box, sources line. Top-3 byte sizes 169–743 KB (rich, detailed
images). icantcodefyi is NOT entered in NI20.

**What our v1 did wrong:** generic masthead with small date; NO hero
scenes (3 text headlines only); NO numbers strip, timeline, date
check, or confidence tags; map with unnumbered dots; led with
non-Friday stories (Shenzhen summit, Kerch bridge); missed core Friday
stories (Poland missile, AI sell-off, UK-EU deal, COP31, Peru quake,
Palisades verdict, Bayer settlement).

**What our v2 does differently:** NIGHT EDITION — navy masthead band
with the giant date as the masthead, red chip, cream body. Confidence
dots on EVERY story + HOW SURE ARE WE legend (only #2 marks
confidence, partially). 50 stories (3 + 10 + 37), all verified Friday.
Real drawn scenes for all 13 featured stories via our own
editorial-illustration library. DATE CHECK with 8 verified exclusions.

## Design decisions

- 1024x1024, <=1 MiB (final: 511,470 bytes). Page drawn at 2x and
  LANCZOS-downscaled; viewed at full size and at 300 px wide.
- Fix round 1: timeline title collided with the 00:00 slot (moved
  slots right, first slot cx 170); map pins in Europe/Middle East
  overlapped (offsets are in tile px — doubled and spread).
- A panel passes when a stranger can name the story from the picture
  alone at 300 px: bridge (broken span + KYIV/DNIPRO), cyclone
  (spiral + ODISHA), market (falling red line + -3.7%).

## Sources (all stories Friday 20 November 2026, UTC)

- Heroes: Reuters + Kyiv Independent (Kyiv bridges, ~110 missiles,
  400+ drones, 8 killed, 28+ hurt, power/water cut, 3 nuclear plants
  cut output); IMD + Reuters (Akvan landfall Gopalpur ~08:00 IST,
  70–80 km/h gusting 90, 300,000+ evacuated, 423 teams, 9,341
  shelters, no deaths); Bloomberg + Reuters (S&P 500 -3.7% to 6,910,
  Nikkei -5.06%, Taiwan -6.2%, Seoul -5.2%, Nvidia -14% on SEC probe).
- Small: Reuters (Kh-101 in Poland, Nowy Lipowiec, NATO "grave
  violation"; COP31 Antalya deadlock, draft omits fossil fuels,
  $120bn adaptation finance unresolved; UK-EU reset — food trade,
  carbon markets, 100,000 youth visas; Bayer $7.25bn Roundup;
  Estonia border shut 1 Dec; Iraqi army in Jurf al-Sakhar); AP
  (Houthi missile, Riyadh's tallest tower, 7–8 floors of windows,
  no injuries; Palisades Fire conviction); UKMTO (tanker ablaze off
  Oman, no casualties); USGS (Peru M6.7, Cerro de Pasco/Junin).
- ALSO ON 14–50: Reuters/AP/BBC/Bloomberg/Al Jazeera/USGS/AFDB/SEC
  reporting of 20 Nov 2026 (see footer of the poster for the outlet
  list). Story 50 (UN chief poll: two veto powers reject Costa
  Rica's Grynspan) verified via Reuters, 20 Nov 2026.
- DATE CHECK exclusions verified 21 Nov ~13:35–13:40 WIB: Shenzhen
  summit Thu 19 Nov; Kerch Bridge 3rd strike Tue 17 Nov; ICJ Myanmar
  genocide verdict Thu 19 Nov (Le Monde/HRW — first time a state held
  responsible for genocide, 9–6, reparations ordered); Anthropic $83
  IPO pricing Thu 19 Nov (Friday's story is the day-two -8.6% slide,
  used as story 49); Van Gogh $190.4m sale Wed 18 Nov; Voyager 1
  one-light-day mark Wed 18 Nov; GTA VI midnight launch Thu 19 Nov;
  BepiColombo Mercury orbit capture Sat 21 Nov (not yet happened).
- NOT used: Senegal migrant boat (top entries date it Thu 19 Nov);
  Senate Iran war-powers vote (date contested Thu/Fri).

## Build log

- Fresh kit downloaded 21 Nov ~13:45 WIB (news-image-20261120-v2-kit).
- Rendered with render_poster.py (Pillow 10.2.0 + editorial-illustration
  lib). Two view rounds (full size + 300 px); one fix round applied.
- main.py is pure stdlib (copy bundled entry.png). Tests: 3/3 pass,
  including a run as uid 65534 on a read-only copy (byte-identical).
- Local judge-test (pairwise criteria check vs current top 3): see
  report to parent; the entry wins on the brief's scored criteria
  (story count, regions, date check, confidence, timeline, map,
  scenes) and loses only on raw leaderboard momentum it cannot have
  before submission.

## Submission (21 Nov 2026, Joni "Setuju" 14:01 WIB)

- Submission 01a1fce9-b44d-71e8-aa0e-44b1a4542d3a, HTTP 202,
  server 2026-11-21T07:02:16Z (14:02:16 WIB). Title: "NIGHT EDITION —
  Friday 20 November 2026 in one image". Signed by payout wallet
  h7aEYozd3ouRt11uqdJC8cQ42hHRckuFotiEvuJbuhE.
- Submitted commit aee0b63670e48d385fb896ab373ac60c0a665804 (repo
  Ci3hu1/news-image-20261120-v2). This NOTES.md update is a later
  docs commit; the graded commit is aee0b636.
- Bundle news-image-20261120-v2-kit.tar.gz: 3,240,059 bytes, sha256
  3c0f785e6ae58dc6f72894c8f3a2e6f882172e8a63c82fc2525ae4c19a2ad7fb,
  18 sessions, usage 200 rows (parent 183 x v3 + 17 subagents x v2).
- Kit check on aee0b636: 13 pass / 6 skip / 5 submission / 0 failed,
  ok=true. First check (commit 6afd4a6) failed 1 item, license_osi:
  root LICENSE needed an SPDX-License-Identifier line; added
  "SPDX-License-Identifier: MIT" and committed as aee0b636.
- Repo About set: description (NIGHT EDITION...), homepage
  https://make.fun/bounty/news-image-20261120, topics makefun,
  ai-agents, bounties, growth.
- Claim code stored ONLY in ~/.config/makefun/
  news-image-20261120-v2-submission.json (0600). v1's code stays in
  news-image-20261120-submission.json (untouched). This v2 submission
  supersedes v1 as the standing entry (last submit wins).
- Entries close 22 Nov 2026 07:00 WIB; results 6 Dec 2026. Live
  score to be read after judging starts; v1's live score was
  957,712 (rank 7,585), paid line #50 989,060.
