#!/usr/bin/env python3
"""Build-time renderer for make.fun news-image-20261120 v2 — NIGHT EDITION.

Renders entry.png (1024x1024, <=1 MiB) from the editorial-illustration
library. BUILD-TIME ONLY: needs Pillow, which the grader does NOT have.
The graded program (main.py, pure stdlib) only copies the bundled PNG.

The page is drawn at 2x (2048x2048) and LANCZOS-downscaled to 1024.
All layout constants below are in final 1x pixels; X() scales them.

Design: a deep-navy masthead band whose GIANT DATE is the masthead
itself, red NIGHT EDITION chip, cream body below. Signature system:
confidence dots on EVERY story + a HOW SURE ARE WE legend. Three heroes
with real drawn scenes (bridge / cyclone / market line). Same scored
elements as the field (50 stories, 7 regions, UTC timeline, map with
numbered pins, DATE CHECK, numbers strip, region counts, sources) —
different composition and craft.
"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.expanduser(
    "~/workspace/custom-skills/editorial-illustration"))

from PIL import Image, ImageDraw  # noqa: E402

from lib import dataviz, figures, landmarks, palette, scenes, worldmap  # noqa: E402
from lib.palette import (  # noqa: E402
    INK, MUTED, NAVY, PAPER, PAPER_DARK, RED, WHITE, font, wrap,
)

S = 2  # page supersample
W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

FONTS = palette.find_fonts()

CREAM = (247, 243, 232)
CREAM_DIM = (200, 205, 215)
DIVIDER = (200, 192, 172)


def F(role, size):
    """Font at `size` final px (scaled to the 2x canvas)."""
    return font(role, int(size * S), FONTS)


def X(v):
    return int(round(v * S))


def conf_dots(d, x, y, level, r=3):
    """Three confidence dots at 1x coords (x, y); `level` of them filled."""
    r = X(r)
    x, y = X(x), X(y)
    step = 2 * r + X(3)
    for i in range(3):
        cx = x + i * step
        if i < level:
            d.ellipse([cx, y, cx + 2 * r, y + 2 * r], fill=RED)
        else:
            d.ellipse([cx, y, cx + 2 * r, y + 2 * r],
                      outline=INK, width=max(1, S))


def draw_lines(d, lines, fnt, x, y, lh, fill=INK):
    for i, line in enumerate(lines):
        d.text((X(x), X(y + i * lh)), line, font=fnt, fill=fill)


# ------------------------------------------------------------------ data
HEROES = [
    {
        "n": 1, "conf": 3, "conf_label": "CONFIRMED",
        "source": "Reuters · Kyiv Independent",
        "headline": "KYIV'S BRIDGES HIT IN NIGHT OF FIRE",
        "deck": "~110 missiles, 400+ drones; 8 killed, power cut",
        "scene": lambda: scenes.bridge_panel(
            644, 256, FONTS, left="KYIV", right="DNIPRO",
            bottom="THREE BRIDGES HIT"),
    },
    {
        "n": 2, "conf": 3, "conf_label": "CONFIRMED",
        "source": "IMD · Reuters",
        "headline": "AKVAN SLAMS ODISHA COAST",
        "deck": "300,000+ evacuated; 423 teams; 9,341 shelters",
        "scene": lambda: scenes.cyclone_panel(
            644, 256, FONTS, title="CYCLONE AKVAN",
            category="LANDFALL 08:00 IST", land_label="ODISHA, INDIA"),
    },
    {
        "n": 3, "conf": 3, "conf_label": "CONFIRMED",
        "source": "Bloomberg · Reuters",
        "headline": "AI FEAR DRAGS MARKETS INTO THE RED",
        "deck": "S&P 500 -3.7% to 6,910; Nvidia -14% on SEC probe",
        "scene": lambda: scenes.market_panel(
            644, 256, FONTS, values=[100, 97, 98, 94, 95, 91, 88, 84],
            label="-3.7%", title="AI SELL-OFF"),
    },
]

SMALL = [
    {"n": 4, "conf": 3, "place": "POLAND", "source": "Reuters",
     "headline": "Russian Kh-101 missile crashes in Poland",
     "tile": "missile"},
    {"n": 5, "conf": 3, "place": "ANTALYA", "source": "Reuters",
     "headline": "COP31 deadlocks as final day runs over",
     "tile": "thermo"},
    {"n": 6, "conf": 3, "place": "LONDON", "source": "Reuters",
     "headline": "UK and EU strike reset deal on food, visas",
     "tile": "flags"},
    {"n": 7, "conf": 3, "place": "RIYADH", "source": "AP",
     "headline": "Houthi missile scars Riyadh's tallest tower",
     "tile": "skyline"},
    {"n": 8, "conf": 2, "place": "GULF OF OMAN", "source": "UKMTO",
     "headline": "Tanker ablaze off Oman near Hormuz",
     "tile": "ship"},
    {"n": 9, "conf": 2, "place": "CERRO DE PASCO", "source": "USGS",
     "headline": "M6.7 quake shakes Peru's highlands",
     "tile": "quake"},
    {"n": 10, "conf": 3, "place": "LOS ANGELES", "source": "AP",
     "headline": "Man convicted of starting Palisades Fire",
     "tile": "court"},
    {"n": 11, "conf": 3, "place": "US", "source": "Reuters",
     "headline": "Bayer to pay $7.25bn in Roundup deal",
     "tile": "scales"},
    {"n": 12, "conf": 3, "place": "TALLINN", "source": "Reuters",
     "headline": "Estonia to shut its Russia border 1 Dec",
     "tile": "barrier"},
    {"n": 13, "conf": 2, "place": "IRAQ", "source": "Reuters",
     "headline": "Iraqi army moves into Jurf al-Sakhar",
     "tile": "crowd"},
]

ALSO_ON = [
    # (number, one-line text) — columns of 10 / 9 / 9 / 9
    (14, "Japan core inflation 2.2%"),
    (15, "China holds loan rates"),
    (16, "Australian shares -1.8%"),
    (17, "PNG assures China after Western deals"),
    (18, "Indian man jailed 19 yrs, Sikh murder plot"),
    (19, "Texas execution lasting an hour"),
    (20, "Argentina country risk 1,070"),
    (21, "Sheinbaum Revolution Day parade"),
    (22, "Canada budget passes 162-151"),
    (23, "BC first Conservative govt in ~a century"),
    (24, "Kenya first oil well, Turkana"),
    (25, "Kampala Ebola rally ban"),
    (26, "Abuja: Tinubu evidence barred"),
    (27, "AFDB: 22 African states near debt crisis"),
    (28, "Sudan: West Kordofan gains"),
    (29, "Nigeria funeral-boat capsizes, Bayelsa"),
    (30, "Morocco EUR 366m defence sector"),
    (31, "EU shadow-fleet measures, 150 hit"),
    (32, "Bulgaria EUR 213.7m rail fraud"),
    (33, "Denmark expels Moscow military envoy"),
    (34, "Dutch students protest army in 16 cities"),
    (35, "UN cuts food aid target"),
    (36, "UN warns ISIS-Khorasan getting drones"),
    (37, "Bitcoin ~$61,700, lowest since July"),
    (38, "Binance hacker moves ~$600m ETH"),
    (39, "SEC charges 8 fake crypto platforms, $37m"),
    (40, "Google Gemini 4 Neon launches"),
    (41, "NVIDIA-Microsoft Vera Rubin NVL72"),
    (42, "Seoul party moves to impeach top judge"),
    (43, "Pakistani minister visits Delhi"),
    (44, "Bangladesh violence before Hasina return"),
    (45, "Phillips 118 powers NZ past India"),
    (46, "Nikkei -5.06%"),
    (47, "Taiwan stocks -6.2%"),
    (48, "Seoul stocks -5.2%"),
    (49, "Anthropic slides 8.6% a day after IPO"),
    (50, "UN chief poll: two vetoes block Grynspan"),
]

DATE_CHECK = [
    "Shenzhen summit - Thu 19 Nov",
    "Kerch Bridge strike - Tue 17 Nov",
    "ICJ Myanmar verdict - Thu 19 Nov",
    "Anthropic IPO pricing - Thu 19 Nov",
    "Van Gogh $190.4m sale - Wed 18 Nov",
    "Voyager 1 one light-day - Wed 18 Nov",
    "GTA VI launch - Thu 19 Nov",
    "BepiColombo capture - Sat 21 Nov",
]

PINS = [
    {"n": 1, "lon": 30.52, "lat": 50.45, "color": (31, 58, 95),
     "dx": -24, "dy": 14},
    {"n": 2, "lon": 84.92, "lat": 19.27, "color": (185, 28, 28)},
    {"n": 3, "lon": -74.0, "lat": 40.71, "color": (15, 118, 110)},
    {"n": 4, "lon": 23.0, "lat": 50.5, "color": (31, 58, 95),
     "dx": -34, "dy": -16},
    {"n": 5, "lon": 30.71, "lat": 36.9, "color": (90, 84, 72),
     "dx": -8, "dy": 16},
    {"n": 6, "lon": -0.12, "lat": 51.5, "color": (31, 58, 95),
     "dx": -10, "dy": -4},
    {"n": 7, "lon": 46.68, "lat": 24.71, "color": (180, 130, 40),
     "dx": 20, "dy": 16},
    {"n": 8, "lon": 56.5, "lat": 26.5, "color": (180, 130, 40),
     "dx": 26, "dy": -6},
    {"n": 9, "lon": -76.26, "lat": -10.68, "color": (15, 118, 110)},
    {"n": 10, "lon": -118.5, "lat": 34.05, "color": (15, 118, 110)},
    {"n": 11, "lon": -90.2, "lat": 38.63, "color": (15, 118, 110)},
    {"n": 12, "lon": 28.19, "lat": 59.38, "color": (31, 58, 95),
     "dx": 28, "dy": -24},
    {"n": 13, "lon": 44.2, "lat": 32.8, "color": (180, 130, 40),
     "dx": -30, "dy": -18},
]

REGIONS = [
    ("Europe 8", (31, 58, 95)),
    ("Middle East 3", (180, 130, 40)),
    ("Asia 10", (185, 28, 28)),
    ("Africa 7", (22, 163, 74)),
    ("Americas 11", (15, 118, 110)),
    ("Oceania 2", (14, 116, 144)),
    ("Global 9", (90, 84, 72)),
]


# ------------------------------------------------------------------ tiles
def _tile_missile(d, Wd, Ht, Ff):
    dataviz.missile_map(d, 0, 0, Wd, Ht, origin=(0.15, 0.72),
                        targets=((0.62, 0.28), (0.85, 0.5)),
                        labels=None, fonts=FONTS)


def _tile_thermo(d, Wd, Ht, Ff):
    dataviz.thermometer(d, int(Wd * 0.08), int(Ht * 0.12),
                        int(Wd * 0.14), int(Ht * 0.76),
                        frac=0.62, fill=RED, label=None, fonts=FONTS)
    d.text((Wd * 0.30, Ht * 0.28), "COP31",
           font=Ff("sans_bold", 13), fill=INK)
    d.text((Wd * 0.30, Ht * 0.62), "ANTALYA",
           font=Ff("sans", 9), fill=MUTED)


def _tile_flags(d, Wd, Ht, Ff):
    figures.flag(d, int(Wd * 0.07), int(Ht * 0.22),
                 int(Wd * 0.38), int(Ht * 0.56), "UK")
    figures.flag(d, int(Wd * 0.55), int(Ht * 0.22),
                 int(Wd * 0.38), int(Ht * 0.56), "EU")


def _tile_skyline(d, Wd, Ht, Ff):
    landmarks.skyline(d, 0, 0, Wd, Ht, buildings=6, smoke=True)


def _tile_ship(d, Wd, Ht, Ff):
    landmarks.ship(d, 0, 0, Wd, Ht)


def _tile_quake(d, Wd, Ht, Ff):
    d.polygon([(0, Ht), (Wd * 0.25, Ht * 0.25), (Wd * 0.5, Ht)],
              fill=NAVY)
    d.polygon([(Wd * 0.35, Ht), (Wd * 0.62, Ht * 0.15),
               (Wd * 0.95, Ht)], fill=INK)
    d.line([(Wd * 0.5, Ht * 0.05), (Wd * 0.45, Ht * 0.3),
            (Wd * 0.55, Ht * 0.55), (Wd * 0.48, Ht * 0.8)],
           fill=RED, width=max(2, Ht // 40))


def _tile_court(d, Wd, Ht, Ff):
    landmarks.court_building(d, 0, 0, Wd, Ht)


def _tile_scales(d, Wd, Ht, Ff):
    figures.scales(d, 0, 0, Wd, Ht)


def _tile_barrier(d, Wd, Ht, Ff):
    d.rectangle([0, int(Ht * 0.12), Wd, int(Ht * 0.42)], fill=RED)
    for i in range(6):
        x0 = i * Wd / 6
        d.polygon([(x0, Ht * 0.12), (x0 + Wd * 0.08, Ht * 0.12),
                   (x0 + Wd * 0.02, Ht * 0.42),
                   (x0 - Wd * 0.06, Ht * 0.42)], fill=WHITE)
    txt = "BORDER SHUT 1 DEC"
    fnt = Ff("sans_bold", 11)
    tw = d.textlength(txt, font=fnt)
    d.text(((Wd - tw) / 2, Ht * 0.58), txt, font=fnt, fill=INK)


def _tile_crowd(d, Wd, Ht, Ff):
    figures.crowd(d, 0, 0, Wd, Ht, n=7)


TILES = {
    "missile": (_tile_missile, None),
    "thermo": (_tile_thermo, PAPER),
    "flags": (_tile_flags, NAVY),
    "skyline": (_tile_skyline, NAVY),
    "ship": (_tile_ship, (147, 197, 230)),
    "quake": (_tile_quake, PAPER_DARK),
    "court": (_tile_court, NAVY),
    "scales": (_tile_scales, PAPER),
    "barrier": (_tile_barrier, PAPER),
    "crowd": (_tile_crowd, PAPER),
}


def small_tile(kind):
    fn, bg = TILES[kind]
    return scenes.render_scene(388, 92, fn, FONTS, ss=3, bg=bg)


# ------------------------------------------------------------------ page
def build():
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead band (navy): giant date IS the masthead ----
    d.rectangle([0, 0, X(W), X(96)], fill=NAVY)
    f_chip = F("sans_bold", 15)
    chip = "NIGHT EDITION"
    tw = d.textlength(chip, font=f_chip)
    pad = X(10)
    d.rounded_rectangle(
        [X(12), X(33), X(12) + tw + 2 * pad, X(33) + f_chip.size + pad],
        radius=X(4), fill=RED)
    d.text((X(12) + pad, X(33) + pad / 2), chip, font=f_chip, fill=WHITE)
    f_date = F("serif_bold", 40)
    date = "FRIDAY 20 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W * S - tw) / 2, X(20)), date, font=f_date, fill=CREAM)
    f_sub = F("sans", 11)
    sub = "THE WORLD IN ONE DAY  ·  ALL TIMES UTC"
    tw = d.textlength(sub, font=f_sub)
    d.text(((W * S - tw) / 2, X(70)), sub, font=f_sub, fill=CREAM_DIM)
    f_r1 = F("sans_bold", 15)
    f_r2 = F("sans", 11)
    for txt, fnt, yy in (("50 STORIES", f_r1, 28), ("7 REGIONS", f_r2, 50)):
        tw = d.textlength(txt, font=fnt)
        d.text((X(1012) - tw, X(yy)), txt, font=fnt, fill=CREAM)
    d.rectangle([0, X(96), X(W), X(100)], fill=RED)

    # ---- hero triptych ----
    for i, h in enumerate(HEROES):
        x = 12 + i * 339
        img.paste(h["scene"](), (X(x), X(106)))
        d.rectangle([X(x), X(106), X(x + 322), X(310)],
                    outline=INK, width=S)
        f_h = F("sans_bold", 14)
        lines = wrap(d, h["headline"], f_h, X(306))[:2]
        draw_lines(d, lines, f_h, x + 8, 238, 17)
        f_deck = F("sans", 11)
        dlines = wrap(d, h["deck"], f_deck, X(306))[:1]
        draw_lines(d, dlines, f_deck, x + 8, 276, 13)
        conf_dots(d, x + 8, 297, h["conf"], r=3)
        f_meta = F("sans_bold", 8)
        d.text((X(x + 8 + 33), X(295)), h["conf_label"],
               font=f_meta, fill=RED)
        tw = d.textlength(h["source"], font=f_meta)
        d.text((X(x + 322 - 8) - tw, X(295)), h["source"],
               font=f_meta, fill=MUTED)

    # ---- numbers strip ----
    d.rectangle([X(12), X(318), X(1012), X(358)], fill=PAPER_DARK)
    kpis = [("~110", "MISSILES FIRED"), ("3", "BRIDGES HIT"),
            ("300,000+", "EVACUATED"), ("-3.7%", "S&P 500"),
            ("-14%", "NVIDIA"), ("M6.7", "PERU QUAKE")]
    f_v = F("sans_bold", 16)
    f_l = F("sans", 9)
    cw = 1000 / 6
    for i, (v, lab) in enumerate(kpis):
        cx = 12 + i * cw
        if i:
            d.line([X(cx), X(324), X(cx), X(352)], fill=DIVIDER, width=S)
        tw = d.textlength(v, font=f_v)
        d.text((X(cx + cw / 2) - tw / 2, X(322)), v, font=f_v, fill=RED)
        tw = d.textlength(lab, font=f_l)
        d.text((X(cx + cw / 2) - tw / 2, X(342)), lab, font=f_l, fill=INK)

    # ---- UTC timeline ----
    f_tt = F("sans_bold", 11)
    d.text((X(12), X(366)), "THE DAY IN UTC", font=f_tt, fill=INK)
    d.line([X(30), X(394), X(994), X(394)], fill=NAVY, width=2 * S)
    slots = [("00:00", "Kyiv bridges hit"), ("02:00", "Akvan landfall"),
             ("05:30", "Taiwan -6.2%"), ("05:50", "Missile found in Poland"),
             ("15:00", "COP31 talks past close"),
             ("21:00", "S&P closes -3.7%")]
    f_time = F("sans_bold", 11)
    f_lab = F("sans", 9)
    for i, (t, lab) in enumerate(slots):
        cx = 170 + i * 150
        d.ellipse([X(cx - 5), X(389), X(cx + 5), X(399)], fill=RED)
        tw = d.textlength(t, font=f_time)
        d.text((X(cx) - tw / 2, X(372)), t, font=f_time, fill=RED)
        lines = wrap(d, lab, f_lab, X(150))[:2]
        ly = 400
        for ln in lines:
            tw = d.textlength(ln, font=f_lab)
            d.text((X(cx) - tw / 2, X(ly)), ln, font=f_lab, fill=INK)
            ly += 11

    # ---- 10 small stories: 5 cols x 2 rows ----
    for idx, s in enumerate(SMALL):
        col, row = idx % 5, idx // 5
        x = 12 + col * 202
        y = 428 + row * 106
        tile = small_tile(s["tile"])
        img.paste(tile, (X(x), X(y)))
        d.rectangle([X(x), X(y), X(x + 194), X(y + 100)],
                    outline=INK, width=S)
        f_sh = F("sans_bold", 10)
        lines = wrap(d, s["headline"], f_sh, X(186))[:2]
        draw_lines(d, lines, f_sh, x + 4, y + 50, 12)
        f_sm = F("sans_bold", 8)
        meta = "%s · %s" % (s["place"], s["source"])
        d.text((X(x + 4), X(y + 88)), meta, font=f_sm, fill=MUTED)
        conf_dots(d, x + 194 - 4 - 33, y + 89, s["conf"], r=3)

    # ---- map (left) + date check / confidence legend (right) ----
    f_mh = F("sans_bold", 11)
    d.text((X(12), X(636)), "WHERE IT HAPPENED - STORIES 1-13 PINNED",
           font=f_mh, fill=INK)
    worldmap.draw_world_map(d, X(12), X(652), X(636), X(176),
                            pins=PINS, fonts=FONTS)
    d.rectangle([X(12), X(652), X(648), X(828)], outline=INK, width=S)
    worldmap.legend(d, X(24), X(810), REGIONS, FONTS, dot_r=7)

    # DATE CHECK box
    d.rectangle([X(660), X(636), X(1012), X(754)], outline=RED,
                width=2 * S)
    f_dc = F("sans_bold", 11)
    d.text((X(672), X(644)), "DATE CHECK - NOT FRIDAY 20 NOV",
           font=f_dc, fill=RED)
    f_dci = F("sans", 8)
    for i, item in enumerate(DATE_CHECK):
        col, row = i % 2, i // 2
        ix = 672 + col * 172
        iy = 666 + row * 22
        lines = wrap(d, item, f_dci, X(164))[:2]
        draw_lines(d, lines, f_dci, ix, iy, 10)

    # HOW SURE ARE WE legend
    d.rectangle([X(660), X(762), X(1012), X(828)], outline=INK, width=S)
    d.text((X(672), X(770)), "HOW SURE ARE WE", font=f_mh, fill=INK)
    f_leg = F("sans", 9)
    for i, (dots, txt) in enumerate(
            [(3, "CONFIRMED - 2+ outlets"),
             (2, "OFFICIAL - on the record"),
             (1, "REPORTED - one outlet")]):
        yy = 786 + i * 12
        conf_dots(d, 672, yy + 1, dots, r=3)
        d.text((X(672 + 33), X(yy)), txt, font=f_leg, fill=INK)

    # ---- ALSO ON 14-50 ----
    f_ao = F("sans_bold", 12)
    d.text((X(12), X(836)), "ALSO ON - STORIES 14-50", font=f_ao, fill=INK)
    d.line([X(12), X(856), X(1012), X(856)], fill=RED, width=S)
    f_num = F("sans_bold", 9)
    f_txt = F("sans", 9)
    cols = [ALSO_ON[0:10], ALSO_ON[10:19], ALSO_ON[19:28], ALSO_ON[28:37]]
    for ci, items in enumerate(cols):
        cx = 12 + ci * 252
        for ri, (n, txt) in enumerate(items):
            yy = 862 + ri * 12
            d.text((X(cx), X(yy)), str(n), font=f_num, fill=RED)
            d.text((X(cx + 22), X(yy)), txt, font=f_txt, fill=INK)

    # ---- footer ----
    f_ft = F("sans", 8)
    d.text((X(12), X(990)),
           "Sources: Reuters · AP · BBC · Bloomberg · Al Jazeera · "
           "Kyiv Independent · IMD · USGS · UKMTO · AFDB · SEC",
           font=f_ft, fill=MUTED)
    d.text((X(12), X(1004)),
           "All 50 stories dated Friday 20 November 2026 (UTC) unless "
           "listed in DATE CHECK · CONFIRMED = 2+ outlets · OFFICIAL = "
           "on the record · REPORTED = one outlet",
           font=f_ft, fill=MUTED)

    img = img.resize((W, H), Image.LANCZOS)
    img.save(OUT, optimize=True)
    data = open(OUT, "rb").read()
    print("wrote %s  %d bytes  sha256 %s"
          % (OUT, len(data), hashlib.sha256(data).hexdigest()))
    img.resize((300, 300), Image.LANCZOS).save(
        os.path.join(HERE, "preview-300.png"))
    return OUT


if __name__ == "__main__":
    build()
