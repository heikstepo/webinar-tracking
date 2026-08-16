#!/usr/bin/env python3
"""Erase a prop the matte kept, inside a bounded region.

In this shot a houseplant leaf sits behind his shoulder and rembg includes it.
It cannot be dropped by keeping the largest connected component, because it
touches the body and is part of the same island.

Inside the given box it is trivially separable by colour — the leaf averages
RGB(44, 50, 42) while everything else there is the white shirt at RGB(183, 188,
189) — so "dark and not warm" isolates it. The mask is feathered so the shoulder
edge stays soft.

Coordinates are shot-specific. Check them against a new photo before reusing.

    python3 strip-prop.py assets/face.png assets/face-noprop.png
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

BOX = (870, 1120, 60, 400)   # y0, y1, x0, x1
LUM_MAX = 118                # leaf ~46, shirt ~187
WARMTH_MIN = -4              # (R-G); leaf is faintly green, skin is warm


def strip(src: str, dst: str, box=BOX):
    im = Image.open(src).convert("RGBA")
    arr = np.array(im).astype(np.float32)
    rgb, alpha = arr[:, :, :3], arr[:, :, 3]
    y0, y1, x0, x1 = box

    sub = rgb[y0:y1, x0:x1]
    lum = sub.mean(axis=2)
    warmth = sub[:, :, 0] - sub[:, :, 1]
    hit = ((lum < LUM_MAX) & (warmth <= -WARMTH_MIN)).astype(np.float32)

    mask = np.zeros(alpha.shape, np.float32)
    mask[y0:y1, x0:x1] = hit
    mask = np.array(Image.fromarray((mask * 255).astype(np.uint8))
                    .filter(ImageFilter.GaussianBlur(2.0)), np.float32) / 255.0

    out = np.dstack([rgb, alpha * (1.0 - mask)]).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")
    img = img.crop(img.getbbox())
    img.save(dst)
    print(f"stripped {src} -> {dst}  {img.size}  ({int(hit.sum())} prop px removed)")


if __name__ == "__main__":
    strip(sys.argv[1] if len(sys.argv) > 1 else "assets/face.png",
          sys.argv[2] if len(sys.argv) > 2 else "assets/face-noprop.png")
