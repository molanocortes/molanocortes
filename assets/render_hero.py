#!/usr/bin/env python3
"""
render_hero.py - draws the animated hero for the GitHub profile README.

The finger is not an illustration. Its link lengths, standoff, joint limits and
telescopic slide law are the same ones the TAKTO digital twins render from
(Fable/web/app/src/kinematics.js, itself derived from the validated sizing
engine), so the linkage in the animation moves the way the built mechanism does:

    proximal / middle / distal   45 / 28 / 22 mm   (reference middle finger)
    dorsal standoff              h = 8 mm
    knuckle-rail migration       s(t)  = h * tan(t/2)
    telescopic link extension    D(t)  = sqrt(span^2 + 2h^2(1-cos t) + 2*span*h*sin t) - span
    DIP coupling                 DIP   = (2/3) * PIP
    stops                        MCP 90 deg, PIP 110 deg, abduction +-16 deg

The three traces are the three encoder channels of one finger unit. The pose and
the traces are sampled from the same phase, so what the linkage is doing and what
the traces read always agree.

The motion itself is a synthetic grasp cycle, not a bench capture. It is a
kinematic model being exercised.

Output: hero-dark.svg, hero-light.svg (no script, no external refs, SMIL only,
so both animate inside a GitHub <img>).

Usage: python3 render_hero.py
"""

import math
from pathlib import Path

# ---------------------------------------------------------------- mechanism --

SEG = (45.0, 28.0, 22.0)   # proximal, middle, distal (mm)
META = 38.0                # metacarpal drawn back from the MCP (mm)
H_RAIL = 8.0               # dorsal standoff (mm)
DIP_FROM_PIP = 2.0 / 3.0

MCP_MAX, PIP_MAX, AB_MAX = 90.0, 110.0, 16.0

N = 48                     # samples per loop
DUR = "6s"


def smoothstep(a, b, x):
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3.0 - 2.0 * t)


def envelope(t):
    """Grasp cycle: dwell open, close, dwell closed, open."""
    t %= 1.0
    return min(smoothstep(0.05, 0.40, t), 1.0 - smoothstep(0.58, 0.93, t))


def channels(t):
    """The three encoder channels of one finger at phase t, in degrees."""
    # a functional cylindrical grasp, not a closed fist: the range an assistive
    # device actually works over, and the only one that stays legible in a
    # sagittal view (a full fist curls the distal phalanx back into a spiral).
    mcp = 4.0 + 58.0 * envelope(t)
    pip = 6.0 + 72.0 * envelope(t + 0.03)          # PIP leads slightly
    abd = (6.0 * math.cos(2 * math.pi * t)
           - 9.0 * envelope(t)
           + 2.5 * math.sin(6 * math.pi * t + 0.7))
    return abd, mcp, pip


def pose(t):
    """Every point the drawing needs, in millimetres, y up, MCP at the origin."""
    _, mcp, pip = channels(t)
    dip = DIP_FROM_PIP * pip
    a0 = 0.0                                        # metacarpal direction
    a1 = a0 - math.radians(mcp)                     # flexion curls toward -y
    a2 = a1 - math.radians(pip)
    a3 = a2 - math.radians(dip)

    def step(p, ang, L):
        return (p[0] + L * math.cos(ang), p[1] + L * math.sin(ang))

    def normal(ang):                                # dorsal side of a segment
        return (-math.sin(ang), math.cos(ang))

    j1 = (0.0, 0.0)                                 # MCP
    j2 = step(j1, a1, SEG[0])                       # PIP
    j3 = step(j2, a2, SEG[1])                       # DIP
    j4 = step(j3, a3, SEG[2])                       # fingertip
    m0 = step(j1, a0 + math.pi, META)               # back of the palm

    # device pins: each sits the standoff above its joint, on the frame that
    # owns it. The MCP pin also rides the palm-side knuckle rail.
    slide_knuckle = H_RAIL * math.tan(math.radians(mcp) / 2.0)
    n0, n1, n2 = normal(a0), normal(a1), normal(a2)
    pa = (j1[0] + slide_knuckle * math.cos(a0) + H_RAIL * n0[0],
          j1[1] + slide_knuckle * math.sin(a0) + H_RAIL * n0[1])
    pb = (j2[0] + H_RAIL * n1[0], j2[1] + H_RAIL * n1[1])
    pc = (j3[0] + H_RAIL * n2[0], j3[1] + H_RAIL * n2[1])

    return dict(m0=m0, j1=j1, j2=j2, j3=j3, j4=j4, pa=pa, pb=pb, pc=pc)


FRAMES = [pose(i / N) for i in range(N)] + [pose(0.0)]
SERIES = [channels(i / N) for i in range(N)] + [channels(0.0)]

# The metacarpal never moves, so the palm-side knuckle rail the MCP block rides
# is static geometry: one line at the standoff height, with end stops.
RAIL = ((-13.0, H_RAIL), (21.0, H_RAIL))

# ------------------------------------------------------------------ canvas ---

W, HGT = 1000, 258
MECH_BOX = (30, 26, 384, 178)      # x, y, w, h  (SVG coords, y down)
TRACE_X, TRACE_W = 470, 470
ROW_H, ROW_GAP, ROW_TOP = 52, 14, 30
CAPTION_Y = 242


def _fit():
    """Uniform scale + offset fitting every frame of the mechanism in its box."""
    keys = ("m0", "j1", "j2", "j3", "j4", "pa", "pb", "pc")
    pts = [f[k] for f in FRAMES for k in keys] + list(RAIL)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    bx, by, bw, bh = MECH_BOX
    s = min(bw / (x1 - x0), bh / (y1 - y0))
    ox = bx + (bw - (x1 - x0) * s) / 2.0 - x0 * s
    oy = by + (bh - (y1 - y0) * s) / 2.0 + y1 * s   # y flip
    return s, ox, oy


SCALE, OX, OY = _fit()


def P(p):
    """millimetres (y up) -> SVG user units (y down)."""
    return (p[0] * SCALE + OX, OY - p[1] * SCALE)


def n(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def pt(p):
    q = P(p)
    return f"{n(q[0])} {n(q[1])}"


def lerp(p, q, u):
    return (p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u)


# ------------------------------------------------------------------ themes ---

THEMES = {
    "light": dict(ink="#191713", muted="#6e6b62", line="#c6c1b2",
                  faint="#dcd6c8", accent="#d94e12", bone="#191713"),
    "dark":  dict(ink="#f0ede6", muted="#8f887c", line="#4a443b",
                  faint="#3d3831", accent="#ff7a3d", bone="#f0ede6"),
}

CHANNELS = [
    ("ABD", 0, -AB_MAX, AB_MAX),
    ("MCP", 1, -10.0, MCP_MAX),
    ("PIP", 2, -10.0, PIP_MAX),
]


def anim(attr, values, extra=""):
    return (f'<animate attributeName="{attr}" dur="{DUR}" '
            f'repeatCount="indefinite" values="{values}"{extra}/>')


def anim_xform(values):
    return (f'<animateTransform attributeName="transform" type="translate" '
            f'dur="{DUR}" repeatCount="indefinite" values="{values}"/>')


def build(theme_name):
    c = THEMES[theme_name]
    o = []
    a = o.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {HGT}" '
      f'width="{W}" height="{HGT}" fill="none" role="img" '
      f'aria-label="An animated line drawing of the TAKTO finger linkage '
      f'flexing, beside three scrolling joint-angle traces for its abduction, '
      f'MCP and PIP encoder channels.">')
    a('<title>TAKTO finger unit, kinematic model</title>')

    mono = ('font-family="ui-monospace,SFMono-Regular,SF Mono,Menlo,'
            'Consolas,monospace"')

    # ---- mechanism ----------------------------------------------------------
    # cuff ties: each device pin down to the joint it stands off from
    ties = ";".join(
        f"M{pt(f['pa'])}L{pt(f['j1'])}M{pt(f['pb'])}L{pt(f['j2'])}"
        f"M{pt(f['pc'])}L{pt(f['j3'])}" for f in FRAMES)
    # anatomical chain
    bone = ";".join(
        f"M{pt(f['m0'])}L{pt(f['j1'])}L{pt(f['j2'])}L{pt(f['j3'])}L{pt(f['j4'])}"
        for f in FRAMES)
    # telescopic members, drawn as two overlapping stages per link
    l1o = ";".join(f"M{pt(f['pa'])}L{pt(lerp(f['pa'], f['pb'], 0.62))}"
                   for f in FRAMES)
    l1i = ";".join(f"M{pt(f['pb'])}L{pt(lerp(f['pb'], f['pa'], 0.62))}"
                   for f in FRAMES)
    l2o = ";".join(f"M{pt(f['pb'])}L{pt(lerp(f['pb'], f['pc'], 0.6))}"
                   for f in FRAMES)
    l2i = ";".join(f"M{pt(f['pc'])}L{pt(lerp(f['pc'], f['pb'], 0.6))}"
                   for f in FRAMES)

    # fingertip locus: where the tip travels over the whole grasp cycle. Static,
    # and it is the reason the panel reads as composed at every phase.
    locus = "M" + "L".join(pt(f["j4"]) for f in FRAMES[:N + 1])
    a(f'<path d="{locus}" stroke="{c["faint"]}" stroke-width="1.2" '
      f'stroke-dasharray="1 4" stroke-linecap="round"/>')

    # knuckle rail: static, because the metacarpal does not move
    r0, r1 = P(RAIL[0]), P(RAIL[1])
    tick = 3.2
    a(f'<g stroke="{c["line"]}" stroke-width="1.4" stroke-linecap="round">'
      f'<path d="M{n(r0[0])} {n(r0[1])}H{n(r1[0])}'
      f'M{n(r0[0])} {n(r0[1] - tick)}V{n(r0[1] + tick)}'
      f'M{n(r1[0])} {n(r1[1] - tick)}V{n(r1[1] + tick)}"/></g>')

    a(f'<g stroke="{c["faint"]}" stroke-width="1" stroke-dasharray="2 2.5">'
      f'<path>{anim("d", ties)}</path></g>')
    a(f'<g stroke="{c["bone"]}" stroke-width="4.4" stroke-linecap="round" '
      f'stroke-linejoin="round" opacity="0.45">'
      f'<path>{anim("d", bone)}</path></g>')
    a(f'<g stroke="{c["accent"]}" stroke-width="6.5" stroke-linecap="round">'
      f'<path>{anim("d", l1o)}</path><path>{anim("d", l2o)}</path></g>')
    a(f'<g stroke="{c["accent"]}" stroke-width="3" stroke-linecap="round" '
      f'opacity="0.72">'
      f'<path>{anim("d", l1i)}</path><path>{anim("d", l2i)}</path></g>')

    # anatomical joints, then the device pins on top
    for key, r in (("j1", 3.1), ("j2", 2.8), ("j3", 2.4), ("j4", 2.0)):
        vals = ";".join(pt(f[key]) for f in FRAMES)
        a(f'<g opacity="0.62"><circle r="{r}" fill="{c["bone"]}">'
          f'</circle>{anim_xform(vals)}</g>')
    for key, r in (("pa", 3.6), ("pb", 3.6), ("pc", 3.1)):
        vals = ";".join(pt(f[key]) for f in FRAMES)
        a(f'<g><circle r="{r}" fill="{c["accent"]}">'
          f'</circle>{anim_xform(vals)}</g>')

    a(f'<text x="30" y="{CAPTION_Y}" {mono} font-size="9.5" '
      f'letter-spacing="1.3" fill="{c["muted"]}">'
      f'FINGER UNIT &#183; 45 / 28 / 22 mm &#183; STANDOFF 8 mm</text>')

    # ---- divider ------------------------------------------------------------
    a(f'<path d="M436 30V214" stroke="{c["faint"]}" stroke-width="1"/>')

    # ---- traces -------------------------------------------------------------
    for label, idx, lo, hi in CHANNELS:
        top = ROW_TOP + idx * (ROW_H + ROW_GAP)
        mid = top + ROW_H
        cid = f"clip{label.lower()}-{theme_name}"

        def y_of(v):
            return mid - (v - lo) / (hi - lo) * ROW_H

        a(f'<defs><clipPath id="{cid}"><rect x="{TRACE_X}" y="{top - 4}" '
          f'width="{TRACE_W}" height="{ROW_H + 8}"/></clipPath></defs>')
        # time graticule
        ticks = "".join(f'M{n(TRACE_X + k * TRACE_W / 6)} {n(mid)}'
                        f'V{n(mid - 4)}' for k in range(7))
        a(f'<path d="{ticks}" stroke="{c["faint"]}" stroke-width="1"/>')
        # zero line
        a(f'<path d="M{TRACE_X} {n(y_of(0))}H{TRACE_X + TRACE_W}" '
          f'stroke="{c["faint"]}" stroke-width="1"/>')
        # scrolling trace, two periods wide, translated by exactly one period
        step = TRACE_W / N
        pts = " ".join(f"{n(j * step)},{n(y_of(SERIES[j % N][idx]))}"
                       for j in range(2 * N + 1))
        stroke = c["accent"] if idx else c["muted"]
        width = 1.9 if idx else 1.5
        fade = "" if idx else ' opacity="0.85"'
        scroll = anim_xform(";".join(f"{n(-u * TRACE_W / N)} 0"
                                     for u in range(N + 1)))
        a(f'<g clip-path="url(#{cid})"><g transform="translate({TRACE_X},0)">'
          f'<polyline points="{pts}" stroke="{stroke}" '
          f'stroke-width="{width}" stroke-linejoin="round" '
          f'stroke-linecap="round"{fade}>{scroll}</polyline></g></g>')
        # label and range
        a(f'<text x="{TRACE_X - 22}" y="{n(mid - ROW_H / 2 + 3.5)}" {mono} '
          f'font-size="10" letter-spacing="1.3" text-anchor="end" '
          f'fill="{c["muted"]}">{label}</text>')
        a(f'<text x="{TRACE_X + TRACE_W + 8}" y="{n(top + 4)}" {mono} '
          f'font-size="8.5" fill="{c["faint"]}">{n(hi)}</text>')
        # live cursor dot at the newest sample
        cvals = ";".join(f"0 {n(y_of(s[idx]))}" for s in SERIES)
        a(f'<g>{anim_xform(cvals)}<circle cx="{TRACE_X + TRACE_W}" cy="0" '
          f'r="{2.8 if idx else 2.2}" fill="{c["accent"] if idx else c["muted"]}"/>'
          f'</g>')

    a(f'<path d="M{TRACE_X + TRACE_W} {ROW_TOP - 4}V{ROW_TOP + 3 * ROW_H + 2 * ROW_GAP + 4}" '
      f'stroke="{c["line"]}" stroke-width="1"/>')
    a(f'<text x="{TRACE_X}" y="{CAPTION_Y}" {mono} font-size="9.5" '
      f'letter-spacing="1.3" fill="{c["muted"]}">'
      f'3 ENCODERS PER FINGER &#183; DEGREES</text>')

    a('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    for name in ("dark", "light"):
        out = here / f"hero-{name}.svg"
        out.write_text(build(name), encoding="utf-8")
        print(f"{out.name}  {out.stat().st_size / 1024:.1f} KB")
