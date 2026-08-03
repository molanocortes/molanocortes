#!/usr/bin/env python3
"""
render_repo_headers.py - the header band that sits at the top of every one of my
public repo READMEs.

One band per repo, in a light and a dark variant, selected by prefers-color-scheme
through a <picture> element. Each band carries the repo name, a one-line spec, and
a motif drawn from that project's actual subject matter: the Protocol 2.0 frame it
parses, the isolation boundary it enforces, the audio graph it builds. The motifs
are meant to survive being read closely, so they carry real field names and real
numbers, never filler.

No script, no external references, no web fonts, so they render anywhere GitHub
puts them.

Usage: python3 render_repo_headers.py [outdir]
       (defaults to writing <repo>-header-{light,dark}.svg into ./repo-headers/)
"""

import sys
from pathlib import Path

W, H = 1000, 150
MOTIF_X = 452                       # motif column starts here
MONO = ('font-family="ui-monospace,SFMono-Regular,SF Mono,Menlo,'
        'Consolas,monospace"')
SANS = ('font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,'
        'Arial,sans-serif"')

THEMES = {
    "light": dict(ink="#191713", muted="#6e6b62", line="#c6c1b2",
                  faint="#dcd6c8", accent="#d94e12", fill="#f1efe9"),
    "dark":  dict(ink="#f0ede6", muted="#8f887c", line="#4a443b",
                  faint="#3d3831", accent="#ff7a3d", fill="#1b1815"),
}


def n(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def txt(x, y, s, fill, size=11, font=MONO, anchor="start", ls=1.2, weight=None):
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{n(x)}" y="{n(y)}" {font} font-size="{size}" '
            f'letter-spacing="{ls}" text-anchor="{anchor}" fill="{fill}"{w}>'
            f'{s}</text>')


def box(x, y, w, h, c, fill="none", sw=1.2, r=2):
    return (f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" '
            f'rx="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>')


def arrow(x1, y1, x2, y2, c, mid):
    return (f'<path d="M{n(x1)} {n(y1)}H{n(x2 - 5)}" stroke="{c}" '
            f'stroke-width="1.2" marker-end="url(#{mid})"/>')


# ------------------------------------------------------------------ motifs ---

def motif_dynamixel(c):
    """The Protocol 2.0 instruction frame, with Fast Sync Read called out."""
    o, x, y, h = [], MOTIF_X, 44, 26
    fields = [("FF FF FD 00", 74), ("ID", 26), ("LEN", 34),
              ("8A", 26), ("PARAMS", 58), ("CRC16", 42)]
    for i, (label, w) in enumerate(fields):
        hot = label == "8A"
        col = c["accent"] if hot else c["line"]
        o.append(box(x, y, w, h, col, c["fill"] if hot else "none",
                     1.6 if hot else 1.2))
        o.append(txt(x + w / 2, y + 17, label,
                     c["accent"] if hot else c["muted"], 9.5, MONO, "middle", 0.9))
        if hot:
            o.append(f'<path d="M{n(x + w / 2)} {n(y + h + 4)}V{n(y + h + 12)}" '
                     f'stroke="{c["accent"]}" stroke-width="1.2"/>')
            o.append(txt(x + w / 2, y + h + 24, "FAST SYNC READ", c["accent"],
                         9, MONO, "middle", 1.1))
        x += w + 4
    o.append(txt(MOTIF_X, y - 10, "INSTRUCTION FRAME", c["faint"], 8.5))
    o.append(txt(MOTIF_X, y + h + 46, "ONE TURNAROUND, EVERY SERVO",
                 c["muted"], 9))
    return "".join(o)


def motif_bno085(c):
    """Two sensors, two independent protocol states, one microcontroller."""
    o, mid = [], f'a{c["accent"][1:]}'
    for i, (addr, tag) in enumerate((("0x4A", "hand"), ("0x4B", "forearm"))):
        y = 38 + i * 44
        o.append(box(MOTIF_X, y, 96, 30, c["line"]))
        o.append(txt(MOTIF_X + 48, y + 13, "BNO085", c["ink"], 10, MONO, "middle"))
        o.append(txt(MOTIF_X + 48, y + 25, f"{addr}  {tag}", c["muted"], 8.5,
                     MONO, "middle", 0.8))
        o.append(arrow(MOTIF_X + 100, y + 15, MOTIF_X + 152, y + 15,
                       c["line"], mid))
        o.append(box(MOTIF_X + 156, y, 118, 30, c["accent"], c["fill"], 1.6))
        o.append(txt(MOTIF_X + 215, y + 19, "TinyBNO085", c["accent"], 10,
                     MONO, "middle"))
        o.append(arrow(MOTIF_X + 278, y + 15, MOTIF_X + 320, y + 15,
                       c["line"], mid))
    o.append(box(MOTIF_X + 324, 38, 92, 74, c["line"]))
    o.append(txt(MOTIF_X + 370, 70, "Teensy", c["ink"], 10, MONO, "middle"))
    o.append(txt(MOTIF_X + 370, 84, "4.1", c["muted"], 9, MONO, "middle"))
    o.append(txt(MOTIF_X, 28, "STATE LIVES IN THE OBJECT, NOT IN A GLOBAL",
                 c["faint"], 8.5))
    o.append(txt(MOTIF_X, 128, "NO SHARED sh2 CONTEXT, SO NOTHING COLLIDES",
                 c["muted"], 9))
    return "".join(o)


def motif_latex(c):
    """The isolation boundary: the working tree is read, never written."""
    o, mid = [], f'a{c["accent"][1:]}'
    o.append(box(MOTIF_X, 44, 104, 40, c["line"]))
    o.append(txt(MOTIF_X + 52, 60, "working", c["ink"], 10, MONO, "middle"))
    o.append(txt(MOTIF_X + 52, 74, "tree", c["ink"], 10, MONO, "middle"))
    o.append(arrow(MOTIF_X + 108, 64, MOTIF_X + 152, 64, c["line"], mid))
    o.append(txt(MOTIF_X + 130, 56, "rsync", c["muted"], 8.5, MONO, "middle", 0.8))
    # the isolated scratch copy
    o.append(f'<rect x="{MOTIF_X + 152}" y="30" width="228" height="70" rx="3" '
             f'fill="none" stroke="{c["accent"]}" stroke-width="1.4" '
             f'stroke-dasharray="4 3"/>')
    o.append(txt(MOTIF_X + 266, 26, "ISOLATED SCRATCH COPY", c["accent"], 8.5,
                 MONO, "middle", 1.1))
    o.append(box(MOTIF_X + 166, 44, 90, 40, c["line"], c["fill"]))
    o.append(txt(MOTIF_X + 211, 68, "latexmk", c["ink"], 10, MONO, "middle"))
    o.append(arrow(MOTIF_X + 260, 64, MOTIF_X + 296, 64, c["line"], mid))
    o.append(box(MOTIF_X + 300, 44, 64, 40, c["line"]))
    o.append(txt(MOTIF_X + 332, 68, "PDF", c["ink"], 10, MONO, "middle"))
    o.append(f'<path d="M{MOTIF_X + 332} 100V116H{MOTIF_X + 52}V88" '
             f'stroke="{c["accent"]}" stroke-width="1.2" '
             f'marker-end="url(#{mid}v)"/>')
    o.append(txt(MOTIF_X + 200, 130, "ONLY THE PDF COMES BACK", c["muted"], 9,
                 MONO, "middle"))
    return "".join(o)


def motif_volume(c):
    """The Core Audio graph: per-app taps, one aggregate, one real-time IOProc."""
    o, mid = [], f'a{c["accent"][1:]}'
    for i in range(3):
        y = 30 + i * 30
        o.append(box(MOTIF_X, y, 78, 22, c["line"]))
        o.append(txt(MOTIF_X + 39, y + 15, ["app A", "app B", "app C"][i],
                     c["muted"], 9, MONO, "middle", 0.8))
        o.append(f'<path d="M{MOTIF_X + 82} {n(y + 11)}H{MOTIF_X + 116}" '
                 f'stroke="{c["line"]}" stroke-width="1.2"/>')
    o.append(txt(MOTIF_X, 22, "PROCESS TAPS", c["faint"], 8.5))
    o.append(f'<path d="M{MOTIF_X + 116} 41V101" stroke="{c["line"]}" '
             f'stroke-width="1.2"/>')
    o.append(arrow(MOTIF_X + 116, 71, MOTIF_X + 152, 71, c["line"], mid))
    o.append(box(MOTIF_X + 156, 50, 128, 42, c["accent"], c["fill"], 1.6))
    o.append(txt(MOTIF_X + 220, 66, "RT IOProc", c["accent"], 10, MONO, "middle"))
    o.append(txt(MOTIF_X + 220, 80, "x gain, sum", c["muted"], 8.5, MONO,
                 "middle", 0.8))
    o.append(arrow(MOTIF_X + 288, 71, MOTIF_X + 328, 71, c["line"], mid))
    o.append(box(MOTIF_X + 332, 50, 84, 42, c["line"]))
    o.append(txt(MOTIF_X + 374, 68, "output", c["ink"], 10, MONO, "middle"))
    o.append(txt(MOTIF_X + 374, 82, "device", c["muted"], 8.5, MONO, "middle", 0.8))
    o.append(txt(MOTIF_X, 128, "NO ALLOCATION, NO LOCKS, NO MESSAGES IN THE "
                 "CALLBACK", c["muted"], 9))
    return "".join(o)


def motif_penumbra(c):
    """The brightness ramp, and the part of it the backlight cannot reach."""
    o = []
    x0, x1, y = MOTIF_X, MOTIF_X + 420, 78
    o.append(txt(x0, 34, "PERCEIVED BRIGHTNESS", c["faint"], 8.5))
    # the ramp itself, as a ramp
    gid = f'g{c["accent"][1:]}'
    o.append(f'<defs><linearGradient id="{gid}" x1="0" x2="1">'
             f'<stop offset="0" stop-color="{c["ink"]}" stop-opacity="0.30"/>'
             f'<stop offset="1" stop-color="{c["ink"]}" stop-opacity="0.02"/>'
             f'</linearGradient></defs>')
    o.append(f'<rect x="{x0}" y="{y - 40}" width="{n(x1 - x0)}" height="40" '
             f'fill="url(#{gid})"/>')
    o.append(f'<path d="M{x0} {y}H{x1}" stroke="{c["line"]}" stroke-width="1.2"/>')
    for i in range(9):
        xx = x0 + i * (x1 - x0) / 8
        o.append(f'<path d="M{n(xx)} {y}V{y + 5}" stroke="{c["line"]}" '
                 f'stroke-width="1"/>')
    # hardware floor marker at 55 % of the ramp
    xf = x0 + (x1 - x0) * 0.55
    o.append(f'<path d="M{n(xf)} {y - 34}V{y + 14}" stroke="{c["muted"]}" '
             f'stroke-width="1.2" stroke-dasharray="3 3"/>')
    o.append(txt(xf - 8, y - 24, "hardware minimum", c["muted"], 9, MONO, "end"))
    # the region Penumbra adds
    o.append(f'<rect x="{n(xf)}" y="{y - 18}" width="{n(x1 - xf)}" height="18" '
             f'fill="{c["accent"]}" opacity="0.16"/>')
    o.append(f'<path d="M{n(xf)} {y - 9}H{n(x1)}" stroke="{c["accent"]}" '
             f'stroke-width="1.6"/>')
    o.append(txt(xf + 10, y - 24, "Penumbra continues here", c["accent"], 9))
    o.append(txt(x0, y + 26, "BRIGHT", c["muted"], 8.5))
    o.append(txt(x1, y + 26, "NEAR BLACK", c["muted"], 8.5, MONO, "end"))
    o.append(txt(x0, 128, "SOFTWARE DIMMING ON TOP OF THE BACKLIGHT",
                 c["muted"], 9))
    return "".join(o)


REPOS = {
    "dynamixel-on-device": dict(
        spec="C++17  ·  single header  ·  AGPL-3.0",
        tag="The Dynamixel control loop,<br/>on the microcontroller.",
        motif=motif_dynamixel),
    "bno085-multi": dict(
        spec="C  ·  single header  ·  MIT",
        tag="Several BNO085 IMUs,<br/>one microcontroller.",
        motif=motif_bno085),
    "latex-safe-build": dict(
        spec="POSIX shell  ·  agent skill  ·  MIT",
        tag="LaTeX builds that cannot<br/>corrupt your tree.",
        motif=motif_latex),
    "multi-volume-controller": dict(
        spec="Swift + C  ·  macOS 14.4+  ·  AGPL-3.0",
        tag="A per-app volume mixer<br/>for macOS.",
        motif=motif_volume),
    "penumbra-screen-dimmer": dict(
        spec="Python  ·  PyObjC / AppKit  ·  MIT",
        tag="Darker than the hardware<br/>minimum.",
        motif=motif_penumbra),
}


def build(repo, theme_name):
    c, meta = THEMES[theme_name], REPOS[repo]
    mid = f'a{c["accent"][1:]}'
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" fill="none" role="img" '
         f'aria-label="{repo}: {meta["tag"].replace("<br/>", " ")}">',
         f'<defs>'
         f'<marker id="{mid}" viewBox="0 0 8 8" refX="7" refY="4" '
         f'markerWidth="6" markerHeight="6" orient="auto">'
         f'<path d="M0 1L7 4L0 7z" fill="{c["line"]}"/></marker>'
         f'<marker id="{mid}v" viewBox="0 0 8 8" refX="7" refY="4" '
         f'markerWidth="6" markerHeight="6" orient="auto">'
         f'<path d="M0 1L7 4L0 7z" fill="{c["accent"]}"/></marker>'
         f'</defs>']

    # identity column
    o.append(txt(0, 26, "MOLANOCORTES", c["faint"], 9, MONO, "start", 2.2))
    line1, line2 = meta["tag"].split("<br/>")
    o.append(txt(-2, 62, line1, c["ink"], 25, SANS, "start", -0.4, 600))
    o.append(txt(-2, 90, line2, c["ink"], 25, SANS, "start", -0.4, 600))
    o.append(f'<path d="M0 108H36" stroke="{c["accent"]}" stroke-width="2"/>')
    o.append(txt(0, 128, meta["spec"], c["muted"], 9.5))

    o.append(meta["motif"](c))
    o.append('</svg>')
    return "".join(o)


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1
               else Path(__file__).resolve().parent / "repo-headers")
    out.mkdir(parents=True, exist_ok=True)
    for repo in REPOS:
        for theme in ("light", "dark"):
            f = out / f"{repo}-header-{theme}.svg"
            f.write_text(build(repo, theme), encoding="utf-8")
    print(f"wrote {len(REPOS) * 2} headers to {out}")
