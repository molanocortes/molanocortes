# Provenance of the OpenPhysicsAI asset on the profile

`lab.webp` tiles six of the gallery films on the front page of `molanocortes/OpenPhysicsAI` (`docs/media/tile-*.gif`
at its first public commit `7592af9`, 2026-09-27): a drone frame 3D printed, the wake of a sailplane, a dam breaking,
sound filling a concert hall, a heat sink warming up, light near a black hole. Each is a solver's own output filmed in
the lab's native app. Nothing inside a film was retouched: each is scaled to 420 x 315, played over one 6 s loop at its
own pace (holds longer than 0.3 s, such as the empty build plate before the print, shortened), labelled on a soft shade
and tiled 3 x 2 with transparent gaps. 1280 x 640, 75 frames of 80 ms, WebP q 74, 2.2 MB.

## Regenerate

`python3 profile_collage.py <OpenPhysicsAI checkout> assets/openphysicsai/lab.webp` with Pillow; the script is kept
beside this file.
