#!/usr/bin/env python3
"""
render_social_cards.py - the 1280x640 social preview card for each public repo.

This is the image link unfurlers show when a repo URL is pasted into Slack, a DM
or a post, so it has one job: say what the thing is, in his voice, at thumbnail
size. Typography-led, one accent, no logos, no screenshots.

Upload the result per repo under Settings -> General -> Social preview. GitHub
does not read it from the repo, so a copy is committed at docs/social-preview.png
purely so it is versioned and easy to find again.

Usage: python3 render_social_cards.py [outdir]
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 640
PAPER, INK, MUTED, LINE, ACCENT = "#f1efe9", "#191713", "#6e6b62", "#c6c1b2", "#d94e12"

HELV = "/System/Library/Fonts/HelveticaNeue.ttc"
MONO = "/System/Library/Fonts/SFNSMono.ttf"

REPOS = {
    "dynamixel-on-device": dict(
        head=["The Dynamixel control loop,", "on the microcontroller."],
        spec="C++17   ·   SINGLE HEADER   ·   AGPL-3.0",
        note="Protocol 2.0 with Fast Sync Read. Allocation-free, bounded waits,\n"
             "and a wire protocol you can unit-test with no hardware attached."),
    "bno085-multi": dict(
        head=["Several BNO085 IMUs,", "one microcontroller."],
        spec="C   ·   SINGLE HEADER   ·   MIT",
        note="A reentrant SHTP driver that keeps every byte of protocol state\n"
             "inside the object, so a second sensor cannot clobber the first."),
    "latex-safe-build": dict(
        head=["LaTeX builds that cannot", "corrupt your tree."],
        spec="POSIX SHELL   ·   AGENT SKILL   ·   MIT",
        note="Compiles in an isolated scratch copy and copies only the PDF back.\n"
             "Auto-detects the root file and engine, triages failing logs."),
    "multi-volume-controller": dict(
        head=["A per-app volume mixer", "for macOS."],
        spec="SWIFT + C   ·   macOS 14.4+   ·   AGPL-3.0",
        note="Built on Core Audio process taps. No driver, no admin install, and\n"
             "it never becomes your default output, so it cannot mute your Mac."),
    "penumbra-screen-dimmer": dict(
        head=["Darker than the", "hardware minimum."],
        spec="PYTHON   ·   PyObjC / APPKIT   ·   MIT",
        note="A click-through software dimmer that covers the menu bar, the Dock\n"
             "and full-screen apps, across every display and Space."),
}


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    f_head = ImageFont.truetype(HELV, 62, index=1)      # Helvetica Neue Bold
    f_note = ImageFont.truetype(HELV, 23, index=0)
    f_kick = ImageFont.truetype(MONO, 17)
    f_spec = ImageFont.truetype(MONO, 18)
    f_repo = ImageFont.truetype(MONO, 20)

    def spaced(d, xy, text, font, fill, tracking):
        """PIL has no letter-spacing, and the mono rows need it."""
        x, y = xy
        for ch in text:
            d.text((x, y), ch, font=font, fill=fill)
            x += d.textlength(ch, font=font) + tracking
        return x

    for repo, m in REPOS.items():
        img = Image.new("RGB", (W, H), PAPER)
        d = ImageDraw.Draw(img)

        # left accent edge: the only piece of pure brand on the card
        d.rectangle([0, 0, 7, H], fill=ACCENT)

        pad = 88
        spaced(d, (pad, 74), "GITHUB.COM/MOLANOCORTES", f_kick, MUTED, 3.4)

        y = 168
        for line in m["head"]:
            d.text((pad - 3, y), line, font=f_head, fill=INK)
            y += 76

        d.line([(pad, y + 34), (pad + 56, y + 34)], fill=ACCENT, width=3)

        d.multiline_text((pad, y + 72), m["note"], font=f_note, fill=MUTED,
                         spacing=10)

        d.line([(pad, H - 118), (W - pad, H - 118)], fill=LINE, width=1)
        spaced(d, (pad, H - 92), m["spec"], f_spec, MUTED, 1.6)

        name = repo
        wname = sum(d.textlength(c, font=f_repo) + 1.4 for c in name)
        spaced(d, (W - pad - wname, H - 92), name, f_repo, INK, 1.4)

        p = out / f"{repo}-social.png"
        img.save(p, optimize=True)
        print(f"{p.name}  {p.stat().st_size / 1024:.0f} KB  {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1
              else Path(__file__).resolve().parent / "social-cards"))
