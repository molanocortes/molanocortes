# Provenance of the TAKTO ONE assets on the profile

The profile shows two TAKTO ONE assets and sends people to the release repository for the
rest. Both are copies of files in `molanocortes/takto-one`, `docs/media/`, taken at commit
`8c8b698` (2026-09-02). Nothing was retouched; the only changes are scale, frame rate and
container. When the source changes, regenerate from it rather than editing these files.

| File here | Source in `takto-one/docs/media/` | What changed |
| --- | --- | --- |
| `hero.webp` | `hero.png` (2400 × 1350) | 1600 px wide, lossy WebP q 82 (31 KB against 1.3 MB) |
| `turntable.webp` | `TAKTO-TURNTABLE.mp4` (1600 × 900, 20 fps, 24 s) | cropped to the device (66 % × 72 % centre), 800 px wide, played at 2× so one turn is 12 s, 12 fps, q 58, loops (1.0 MB) |

Both are renders from the release CAD, not photographs of the bench. The sizes are chosen
for a phone on mobile data: the whole page is about 1 MB.

## Regenerate

`ffmpeg` with `libwebp` (the static build from `pip install imageio-ffmpeg` is enough) and
Pillow. Run from the `takto-one` checkout; write into this folder.

```bash
OUT=../molanocortes/assets/takto
ffmpeg -y -i docs/media/TAKTO-TURNTABLE.mp4 \
  -vf "setpts=0.5*PTS,fps=12,crop=iw*0.66:ih*0.72:(iw-iw*0.66)/2:(ih-ih*0.72)/2,scale=800:-1:flags=lanczos" \
  -c:v libwebp -lossless 0 -q:v 58 -compression_level 6 -loop 0 -an $OUT/turntable.webp
```

```python
from PIL import Image
im = Image.open("docs/media/hero.png").convert("RGB")
im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
im.save(f"{OUT}/hero.webp", "WEBP", quality=82, method=6)
```

Why WebP and not GIF or PNG: the same turntable as a GIF is over 20 MB; the hero as PNG is
over 800 KB at this size and 31 KB as WebP, because the render's white ground compresses to
almost nothing. GitHub renders WebP, still and animated, wherever it renders a PNG or GIF.
