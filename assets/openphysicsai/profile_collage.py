"""The profile's OpenPhysicsAI picture: six of the front page's gallery films in a 3 x 2 grid, each played over one loop
at its own pace (time-stretched by its frame durations), labelled, rounded, transparent between the tiles."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageSequence

SRC = Path(sys.argv[1]) / "docs" / "media"  # an OpenPhysicsAI checkout
OUT = Path(sys.argv[2])
TILES = [("drone-print", "A drone frame, 3D printed"), ("sailplane", "The wake of a sailplane"),
         ("dam-break", "A dam breaks"), ("concert-hall", "Sound fills a concert hall"),
         ("heat-sink", "A heat sink warms up"), ("black-hole", "Light near a black hole")]
COLS, TW, TH, GAP, R = 3, 420, 315, 10, 14
FRAMES, MS = 75, 80

f = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 20)
f.set_variation_by_name("Semibold")
shade = Image.new("L", (1, 70))
for y in range(70):
    shade.putpixel((0, y), int(160 * (y / 69) ** 1.6))
shade = shade.resize((TW, 70))
mask = Image.new("L", (TW, TH), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, TW - 1, TH - 1), R, fill=255)
films = []
for name, label in TILES:
    im = Image.open(SRC / ("tile-%s.gif" % name))
    frames, ends, t = [], [], 0
    for fr in ImageSequence.Iterator(im):
        frames.append(fr.convert("RGB").resize((TW, TH), Image.LANCZOS))
        t += min(fr.info.get("duration", 80) or 80, 300)  # long holds (a title card, an empty plate) shortened
        ends.append(t)
    films.append((frames, ends, label))
W, H = COLS * TW + (COLS - 1) * GAP, 2 * TH + GAP
out = []
for k in range(FRAMES):
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i, (frames, ends, label) in enumerate(films):
        t = (k + 0.5) / FRAMES * ends[-1]
        j = next(n for n, e in enumerate(ends) if e > t)
        tile = frames[j].copy()
        tile.paste(Image.new("RGB", (TW, 70)), (0, TH - 70), shade)
        ImageDraw.Draw(tile).text((16, TH - 16), label, font=f, fill=(245, 245, 247), anchor="ls")
        canvas.paste(tile, ((i % COLS) * (TW + GAP), (i // COLS) * (TH + GAP)), mask)
    out.append(canvas)
out[FRAMES * 2 // 3].save(OUT.with_suffix(".png"))
out[0].save(OUT, save_all=True, append_images=out[1:], duration=MS, loop=0, quality=74, method=6)
print("wrote %s, %dx%d, %.1f MB" % (OUT, W, H, OUT.stat().st_size / 1e6))
