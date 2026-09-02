#!/usr/bin/env python3
"""
render_capabilities.py - draws the capability strip on the GitHub profile README.

One strip, five columns, one signal path. Each column is a layer of the TAKTO ONE
stack that I designed, built or programmed myself, with three or four specifics
underneath that are true of the shipped design. The hairline along the bottom is
the data path through the same five layers, joint to screen, with a pulse that
travels it: a reminder that the columns are not a skills list, they are one
machine read left to right.

Palette is the TAKTO one: warm ink and paper, sapphire accent (the colour of the
device's own display ring). No fill, so the strip floats on whatever GitHub
paints behind it. No script, no web fonts, SMIL only, so it animates inside a
GitHub <img>.

Output: capabilities-light.svg, capabilities-dark.svg
Usage:  python3 render_capabilities.py
"""

from pathlib import Path

W, H = 1000, 236
MARGIN = 28
COLS = 5
COL_W = (W - 2 * MARGIN) / COLS

SANS = ('font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,'
        'Arial,sans-serif"')
MONO = ('font-family="ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,'
        'monospace"')

THEMES = {
    "light": dict(ink="#23201A", muted="#5C564A", faint="#8B8474",
                  line="#D8D2C4", accent="#2F76BF"),
    "dark":  dict(ink="#F1F6FC", muted="#BAC7D6", faint="#77879A",
                  line="#2B3542", accent="#5BA8F5"),
}

KICKER_LEFT = "ONE ENGINEER, THE WHOLE STACK"
KICKER_RIGHT = "JOINT TO TWIN, ONE DATA PATH"

# label, body lines (kept short so they never wrap at README width), path node
COLUMNS = [
    ("MECHANISM",
     ["Tendon-driven fingers",
      "4 fingers, 12 joints",
      "Series-elastic spools",
      "71 printed parts"],
     "joint"),
    ("ELECTRONICS",
     ["2 custom PCBs, KiCad",
      "12 × AS5600 encoders",
      "3 IMUs, EMG front end",
      "8 Dynamixel servos"],
     "encoder"),
    ("FIRMWARE",
     ["Teensy 4.1, C++",
      "Control loop to 2 kHz",
      "Motor bus on the MCU",
      "SD log, round display"],
     "teensy"),
    ("CONTROL",
     ["Series-elastic tendons",
      "Transparent to assist",
      "Current-limited motors",
      "Hand-to-hand teleop"],
     "tendon"),
    ("SOFTWARE",
     ["Browser console, 3D twin",
      "WebXR AR layer",
      "Expo app, iOS + Android",
      "Session replay in 4D"],
     "twin"),
]


def n(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(theme):
    t = THEMES[theme]
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">')
    o.append('<title id="t">What I build: mechanism, electronics, firmware, '
             'control and software, one data path</title>')
    o.append('<desc id="d">Five columns, one per layer of the TAKTO ONE stack, '
             'each with the specifics of the shipped design. A hairline along the '
             'bottom traces the data path from a finger joint to the 3D twin.</desc>')

    # kickers
    o.append(f'<text x="{MARGIN}" y="22" {MONO} font-size="11" letter-spacing="2" '
             f'fill="{t["faint"]}">{esc(KICKER_LEFT)}</text>')
    o.append(f'<text x="{W - MARGIN}" y="22" {MONO} font-size="11" letter-spacing="2" '
             f'text-anchor="end" fill="{t["faint"]}">{esc(KICKER_RIGHT)}</text>')
    o.append(f'<line x1="{MARGIN}" y1="34" x2="{W - MARGIN}" y2="34" '
             f'stroke="{t["line"]}" stroke-width="1"/>')

    # columns
    label_y, rule_y, body_y0, body_dy = 66, 78, 104, 21
    for i, (label, lines, _) in enumerate(COLUMNS):
        x = MARGIN + i * COL_W
        o.append(f'<text x="{n(x)}" y="{label_y}" {MONO} font-size="12.5" '
                 f'letter-spacing="1.8" font-weight="600" fill="{t["ink"]}">'
                 f'{esc(label)}</text>')
        # accent tick + hairline
        o.append(f'<line x1="{n(x)}" y1="{rule_y}" x2="{n(x + 22)}" y2="{rule_y}" '
                 f'stroke="{t["accent"]}" stroke-width="2"/>')
        o.append(f'<line x1="{n(x + 22)}" y1="{rule_y}" x2="{n(x + COL_W - 18)}" '
                 f'y2="{rule_y}" stroke="{t["line"]}" stroke-width="1"/>')
        for k, line in enumerate(lines):
            fill = t["ink"] if k == 0 else t["muted"]
            o.append(f'<text x="{n(x)}" y="{body_y0 + k * body_dy}" {SANS} '
                     f'font-size="13.5" fill="{fill}">{esc(line)}</text>')

    # signal path along the bottom: joint -> encoder -> teensy -> tendon -> twin
    py = 212
    x0 = MARGIN + 6
    x1 = W - MARGIN - 6
    o.append(f'<line x1="{x0}" y1="{py}" x2="{x1}" y2="{py}" '
             f'stroke="{t["line"]}" stroke-width="1"/>')
    nodes = []
    for i, (_, _, node) in enumerate(COLUMNS):
        cx = MARGIN + i * COL_W + 6
        nodes.append(cx)
        o.append(f'<circle cx="{n(cx)}" cy="{py}" r="3.2" fill="{t["accent"]}"/>')
        o.append(f'<text x="{n(cx + 10)}" y="{py + 4}" {MONO} font-size="10" '
                 f'letter-spacing="1.4" fill="{t["faint"]}">{esc(node.upper())}</text>')
    # the pulse: one packet travelling the path every 6 s, then a return in the
    # tendon direction is implied by the loop restarting at the joint.
    o.append(f'<circle cy="{py}" r="4.5" fill="{t["accent"]}" opacity="0.95">'
             f'<animate attributeName="cx" values="{n(x0)};{n(x1)}" dur="6s" '
             f'calcMode="spline" keySplines="0.4 0 0.2 1" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;0.95;0.95;0" '
             f'keyTimes="0;0.06;0.94;1" dur="6s" repeatCount="indefinite"/>'
             f'</circle>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


def main():
    here = Path(__file__).resolve().parent
    for theme in THEMES:
        out = here / f"capabilities-{theme}.svg"
        out.write_text(render(theme), encoding="utf-8")
        print(f"wrote {out.name} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
