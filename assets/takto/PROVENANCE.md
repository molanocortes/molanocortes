# Provenance of the TAKTO ONE assets on the profile

Every file here is a copy or a re-encode of a file in the TAKTO ONE release repository
(`molanocortes/takto-one`, `docs/media/`), taken at commit `8c8b698` (2026-09-02). Nothing
was retouched; the only changes are scale, frame rate and container. When the source
changes, regenerate from it with the commands below rather than editing these files.

| File here | Source in `takto-one/docs/media/` | What changed |
| --- | --- | --- |
| `hero.png` | `hero.png` (2400 × 1350) | downscaled to 1800 px wide |
| `film.webp` | `TAKTO-ONE.mp4` (1920 × 1080, 24 fps, 30 s, v057 master) | animated WebP, 1080 px wide, 12 fps, q 55, loops |
| `turntable.webp` | `TAKTO-TURNTABLE.mp4` (1600 × 900, 20 fps, 24 s) | cropped to the device (66 % × 72 % centre), 960 px wide, 12 fps, q 62, loops |
| `replay.webp` | `ui-replay.gif` (1120 × 700) | animated WebP, 880 px wide, 10 fps |
| `ar-modes.webp` | `ar-modes-live.gif` (1200 × 310) | animated WebP, 900 px wide, 10 fps |
| `watch-faces.webp` | `watch-faces-live.gif` (832 × 326) | animated WebP, same size, 10 fps |
| `app-screens.png` | `app-screens.png` (2441 × 1713) | downscaled to 1600 px wide |
| `pcbs.png` | `pcb-encoder-board.png` + `pcb-palm-carrier.png` | the two KiCad renders composed side by side on white at 1600 × 1127 |

All of them are renders or captures of the release software running on its simulator, not
photographs of the bench. The film and the turntable are rendered from the release CAD.

## Regenerate

`ffmpeg` with `libwebp` (the static build from `pip install imageio-ffmpeg` is enough) and
Pillow. Run from the `takto-one` checkout; write into this folder.

```bash
OUT=../molanocortes/assets/takto
ffmpeg -y -i docs/media/TAKTO-ONE.mp4 -vf "fps=12,scale=1080:-1:flags=lanczos" \
  -c:v libwebp -lossless 0 -q:v 55 -compression_level 6 -loop 0 -an $OUT/film.webp
ffmpeg -y -i docs/media/TAKTO-TURNTABLE.mp4 \
  -vf "fps=12,crop=iw*0.66:ih*0.72:(iw-iw*0.66)/2:(ih-ih*0.72)/2,scale=960:-1:flags=lanczos" \
  -c:v libwebp -lossless 0 -q:v 62 -compression_level 6 -loop 0 -an $OUT/turntable.webp
ffmpeg -y -i docs/media/ui-replay.gif -vf "fps=10,scale=880:-1:flags=lanczos" \
  -c:v libwebp -lossless 0 -q:v 60 -compression_level 6 -loop 0 -an $OUT/replay.webp
ffmpeg -y -i docs/media/ar-modes-live.gif -vf "fps=10,scale=900:-1:flags=lanczos" \
  -c:v libwebp -lossless 0 -q:v 60 -compression_level 6 -loop 0 -an $OUT/ar-modes.webp
ffmpeg -y -i docs/media/watch-faces-live.gif -vf "fps=10" \
  -c:v libwebp -lossless 0 -q:v 62 -compression_level 6 -loop 0 -an $OUT/watch-faces.webp
```

```python
from PIL import Image
def down(src, dst, w):
    im = Image.open(src).convert("RGB")
    im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(dst, optimize=True)
down("docs/media/hero.png", f"{OUT}/hero.png", 1800)
down("docs/media/app-screens.png", f"{OUT}/app-screens.png", 1600)
```

Why WebP and not GIF: the same turntable as a 960 px GIF is over 20 MB; as WebP it is 2.5 MB
at visibly better quality. GitHub renders animated WebP wherever it renders a GIF. The real
MP4 can only play on GitHub from a `user-attachments` URL minted by hand in a public repo;
the README carries the instructions in a comment.
