# Provenance of the TAKTO ONE assets on the profile

The profile shows two TAKTO ONE assets and sends people to the release repository for the
rest. Both are copies of files in `molanocortes/takto-one`, `docs/media/`, taken at commit
`8c8b698` (2026-09-02). Nothing was retouched; the only changes are scale, frame rate and
container. When the source changes, regenerate from it rather than editing these files.

| File here | Source in `takto-one/docs/media/` | What changed |
| --- | --- | --- |
| `hero.png` | `hero.png` (2400 × 1350) | downscaled to 1800 px wide |
| `turntable.webp` | `TAKTO-TURNTABLE.mp4` (1600 × 900, 20 fps, 24 s) | cropped to the device (66 % × 72 % centre), 960 px wide, 12 fps, q 62, loops |

Both are renders from the release CAD, not photographs of the bench.

## Regenerate

`ffmpeg` with `libwebp` (the static build from `pip install imageio-ffmpeg` is enough) and
Pillow. Run from the `takto-one` checkout; write into this folder.

```bash
OUT=../molanocortes/assets/takto
ffmpeg -y -i docs/media/TAKTO-TURNTABLE.mp4 \
  -vf "fps=12,crop=iw*0.66:ih*0.72:(iw-iw*0.66)/2:(ih-ih*0.72)/2,scale=960:-1:flags=lanczos" \
  -c:v libwebp -lossless 0 -q:v 62 -compression_level 6 -loop 0 -an $OUT/turntable.webp
```

```python
from PIL import Image
im = Image.open("docs/media/hero.png").convert("RGB")
im.resize((1800, round(im.height * 1800 / im.width)), Image.LANCZOS).save(f"{OUT}/hero.png", optimize=True)
```

Why WebP and not GIF: the same turntable as a 960 px GIF is over 20 MB; as WebP it is 2.5 MB
at visibly better quality. GitHub renders animated WebP wherever it renders a GIF.
