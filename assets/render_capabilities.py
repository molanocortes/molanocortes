#!/usr/bin/env python3
"""
render_capabilities.py - draws the capability strip on the GitHub profile README.

One strip, five layers, one signal path. Each layer of the TAKTO ONE stack that I
designed, built or programmed myself, with the specifics that are true of the shipped
design. The hairline is the data path through the same five layers, joint to twin, with
a pulse that travels it: the layers are not a skills list, they are one machine.

Two layouts, because a README has no CSS: a wide strip with five columns for the
desktop column (896 px), and a stacked one for phones, chosen by the README's <picture>
element on (max-width: 600px). Each in light and dark.

Palette is the TAKTO one: warm ink, sapphire accent (the colour of the device's own
display ring). No fill, so the strip floats on whatever GitHub paints behind it. No
script, no web fonts, SMIL only, so it animates inside a GitHub <img>.

Output: capabilities-{light,dark}.svg, capabilities-{light,dark}-mobile.svg
Usage:  python3 render_capabilities.py
"""

from pathlib import Path

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
KICKER_RIGHT = "JOINT TO MODEL, ONE DATA PATH"

# label, four specifics (short, so they never wrap), path node.
# First line is the TAKTO ONE fact; the rest widen it with work from elsewhere.
COLUMNS = [
    ("MECHANISM",
     ["Tendon-driven hand", "4 fingers, 12 joints",
      "71 printed parts", "LPBF metal, FEM, DfAM"], "joint"),
    ("ELECTRONICS",
     ["2 custom PCBs, KiCad", "12 × AS5600 encoders",
      "IMUs, EMG front end", "CAN, EtherCAT, FPGA"], "encoder"),
    ("FIRMWARE",
     ["Teensy 4.1, C++", "2 kHz control loop",
      "Motor bus on the MCU", "RTOS, ROS 2, Linux"], "teensy"),
    ("CONTROL",
     ["Series-elastic drive", "Transparent / assist",
      "Impedance control", "Hand-to-hand teleop"], "tendon"),
    ("SOFTWARE",
     ["Live 3D twin, WebXR", "iOS + Android app",
      "Python, FastAPI", "Session replay in 4D"], "twin"),
    ("ML · SIGNALS",
     ["EMG acquisition, DSP", "TensorFlow, Conv1D",
      "Hyperspectral, F1 0.93", "Grad-CAM, sklearn"], "model"),
]

TITLE = ("What I build: mechanism, electronics, firmware, control, software and "
         "machine learning, one data path")
DESC = ("Six layers I work across, each opening with a TAKTO ONE fact and widening "
        "to work from elsewhere. A hairline traces the data path from a finger joint "
        "to a trained model.")


def n(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pulse(t, axis, a, b):
    """An accent dot travelling from a to b along one axis every 6 s."""
    fixed = 'cy="{y}"' if axis == "cx" else 'cx="{x}"'
    return (f'<circle r="4.5" fill="{t["accent"]}" opacity="0.95" FIXED>'
            f'<animate attributeName="{axis}" values="{n(a)};{n(b)}" dur="6s" '
            f'calcMode="spline" keySplines="0.4 0 0.2 1" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.95;0.95;0" '
            f'keyTimes="0;0.06;0.94;1" dur="6s" repeatCount="indefinite"/>'
            f'</circle>')


def head(w, h):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">',
            f'<title id="t">{esc(TITLE)}</title>',
            f'<desc id="d">{esc(DESC)}</desc>']


def render_wide(theme):
    t = THEMES[theme]
    W, H, M = 1000, 236, 28
    col_w = (W - 2 * M) / len(COLUMNS)
    o = head(W, H)
    o.append(f'<text x="{M}" y="22" {MONO} font-size="11" letter-spacing="2" '
             f'fill="{t["faint"]}">{esc(KICKER_LEFT)}</text>')
    o.append(f'<text x="{W - M}" y="22" {MONO} font-size="11" letter-spacing="2" '
             f'text-anchor="end" fill="{t["faint"]}">{esc(KICKER_RIGHT)}</text>')
    o.append(f'<line x1="{M}" y1="34" x2="{W - M}" y2="34" stroke="{t["line"]}" '
             f'stroke-width="1"/>')
    label_y, rule_y, body_y0, body_dy = 66, 78, 104, 21
    for i, (label, lines, _) in enumerate(COLUMNS):
        x = M + i * col_w
        o.append(f'<text x="{n(x)}" y="{label_y}" {MONO} font-size="12" '
                 f'letter-spacing="1.6" font-weight="600" fill="{t["ink"]}">'
                 f'{esc(label)}</text>')
        o.append(f'<line x1="{n(x)}" y1="{rule_y}" x2="{n(x + 22)}" y2="{rule_y}" '
                 f'stroke="{t["accent"]}" stroke-width="2"/>')
        o.append(f'<line x1="{n(x + 22)}" y1="{rule_y}" x2="{n(x + col_w - 18)}" '
                 f'y2="{rule_y}" stroke="{t["line"]}" stroke-width="1"/>')
        for k, line in enumerate(lines):
            fill = t["ink"] if k == 0 else t["muted"]
            o.append(f'<text x="{n(x)}" y="{body_y0 + k * body_dy}" {SANS} '
                     f'font-size="13" fill="{fill}">{esc(line)}</text>')
    py, x0, x1 = 212, M + 6, W - M - 6
    o.append(f'<line x1="{x0}" y1="{py}" x2="{x1}" y2="{py}" stroke="{t["line"]}" '
             f'stroke-width="1"/>')
    for i, (_, _, node) in enumerate(COLUMNS):
        cx = M + i * col_w + 6
        o.append(f'<circle cx="{n(cx)}" cy="{py}" r="3.2" fill="{t["accent"]}"/>')
        o.append(f'<text x="{n(cx + 10)}" y="{py + 4}" {MONO} font-size="10" '
                 f'letter-spacing="1.4" fill="{t["faint"]}">{esc(node.upper())}</text>')
    o.append(pulse(t, "cx", x0, x1).replace("FIXED", f'cy="{py}"'))
    o.append('</svg>')
    return "\n".join(o) + "\n"


def render_mobile(theme):
    t = THEMES[theme]
    W, M = 420, 22
    block_h, y0 = 78, 64
    H = y0 + block_h * len(COLUMNS) + 26
    path_x, text_x = M + 4, M + 22
    o = head(W, H)
    o.append(f'<text x="{M}" y="20" {MONO} font-size="10.5" letter-spacing="1.6" '
             f'fill="{t["faint"]}">{esc(KICKER_LEFT)}</text>')
    o.append(f'<line x1="{M}" y1="32" x2="{W - M}" y2="32" stroke="{t["line"]}" '
             f'stroke-width="1"/>')
    first_y = y0 - 4
    last_y = y0 + block_h * (len(COLUMNS) - 1) - 4
    o.append(f'<line x1="{path_x}" y1="{first_y}" x2="{path_x}" y2="{last_y}" '
             f'stroke="{t["line"]}" stroke-width="1"/>')
    for i, (label, lines, node) in enumerate(COLUMNS):
        y = y0 + i * block_h
        o.append(f'<circle cx="{path_x}" cy="{y - 4}" r="3.2" fill="{t["accent"]}"/>')
        o.append(f'<text x="{text_x}" y="{y}" {MONO} font-size="12" letter-spacing="1.8" '
                 f'font-weight="600" fill="{t["ink"]}">{esc(label)}</text>')
        o.append(f'<text x="{W - M}" y="{y}" {MONO} font-size="9.5" letter-spacing="1.4" '
                 f'text-anchor="end" fill="{t["faint"]}">{esc(node.upper())}</text>')
        o.append(f'<line x1="{text_x}" y1="{y + 10}" x2="{text_x + 20}" y2="{y + 10}" '
                 f'stroke="{t["accent"]}" stroke-width="2"/>')
        o.append(f'<line x1="{text_x + 20}" y1="{y + 10}" x2="{W - M}" y2="{y + 10}" '
                 f'stroke="{t["line"]}" stroke-width="1"/>')
        o.append(f'<text x="{text_x}" y="{y + 32}" {SANS} font-size="13" fill="{t["ink"]}">'
                 f'{esc(lines[0])}<tspan fill="{t["faint"]}"> · </tspan>'
                 f'<tspan fill="{t["muted"]}">{esc(lines[1])}</tspan></text>')
        o.append(f'<text x="{text_x}" y="{y + 51}" {SANS} font-size="13" '
                 f'fill="{t["muted"]}">{esc(lines[2])}<tspan fill="{t["faint"]}"> · '
                 f'</tspan>{esc(lines[3])}</text>')
    o.append(f'<text x="{W - M}" y="{H - 8}" {MONO} font-size="10.5" letter-spacing="1.6" '
             f'text-anchor="end" fill="{t["faint"]}">{esc(KICKER_RIGHT)}</text>')
    o.append(pulse(t, "cy", first_y, last_y).replace("FIXED", f'cx="{path_x}"'))
    o.append('</svg>')
    return "\n".join(o) + "\n"


def main():
    here = Path(__file__).resolve().parent
    for theme in THEMES:
        for suffix, fn in (("", render_wide), ("-mobile", render_mobile)):
            out = here / f"capabilities-{theme}{suffix}.svg"
            out.write_text(fn(theme), encoding="utf-8")
            print(f"wrote {out.name} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
