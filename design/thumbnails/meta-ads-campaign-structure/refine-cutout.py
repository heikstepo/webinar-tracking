#!/usr/bin/env python3
"""Neutralise retained-background spill in the matted cutout.

rembg keeps the wall that shows through the gaps between hair strands. It is
invisible on a light thumbnail and glaring on a dark one.

The wall in this shot is neutral and very slightly cool (R141 G142 B144, chroma
~3, B>=R). Hair, skin and the cream sweater are all warm (R>B, chroma >=16), so
"low chroma AND not warm" isolates the spill without eating the subject. Rather than
punching holes through the strands, the spill is sunk toward hair tone and alpha
is only partly reduced, then feathered — on a dark background that reads as hair
shadow instead of a ragged cutout edge.

    python3 refine-cutout.py assets/face.png assets/face-clean.png
"""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

# Only refine the head region — the wall behind the shoulders is already handled
# by the matte, and the sweater's cool shadows would otherwise get nibbled.
HEAD_ROWS = 1150
CHROMA_MAX = 19.0      # wall ~3, sweater ~16
WARMTH_MAX = 9.0       # (R-B); wall ~ -3, blown wall ~ +6, sweater ~ +16
LUM_RANGE = (48, 252)
EDGE_PX = 34           # spill only happens within this far of the matte edge


def refine(src: str, dst: str):
    im = Image.open(src).convert("RGBA")
    arr = np.array(im).astype(np.float32)
    rgb, alpha = arr[:, :, :3], arr[:, :, 3]

    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    lum = rgb.mean(axis=2)
    warmth = r - b

    # each term ramps 0..1 so the mask has soft shoulders instead of hard edges
    t_chroma = np.clip((CHROMA_MAX - chroma) / CHROMA_MAX, 0, 1)
    t_warm = np.clip((WARMTH_MAX - warmth) / 10.0, 0, 1)
    t_lum = np.clip((lum - LUM_RANGE[0]) / 25.0, 0, 1) * \
            np.clip((LUM_RANGE[1] - lum) / 25.0, 0, 1)
    spill = t_chroma * t_warm * t_lum

    # Spill is a boundary artefact, so gate on distance from the matte edge.
    # This is what keeps eye whites and other low-chroma interior detail safe
    # while allowing much looser colour thresholds at the silhouette.
    inside = alpha > 200
    dist = ndimage.distance_transform_edt(inside)
    spill *= np.clip((EDGE_PX - dist) / EDGE_PX, 0, 1)

    region = np.zeros_like(spill)
    region[:HEAD_ROWS] = 1.0
    region[HEAD_ROWS:HEAD_ROWS + 120] = np.linspace(1, 0, 120)[:, None]
    spill *= region

    removed = float((spill > 0.5).sum())

    # On a dark background, sinking the spill toward hair tone reads better than
    # punching holes through the strands. Alpha only drops where spill is strong.
    hair = np.array([38.0, 28.0, 22.0])
    k = spill[:, :, None]
    new_rgb = rgb * (1.0 - k) + hair * k
    new_alpha = alpha * (1.0 - 0.45 * spill)

    out = np.dstack([new_rgb, new_alpha]).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")

    # feather only the alpha, so colour detail is untouched
    a = img.getchannel("A").filter(ImageFilter.GaussianBlur(0.8))
    img.putalpha(a)
    img = img.crop(img.getbbox())
    img.save(dst)
    print(f"refined {src} -> {dst}  {img.size}  ({int(removed)} spill px removed)")


if __name__ == "__main__":
    refine(sys.argv[1] if len(sys.argv) > 1 else "assets/face.png",
           sys.argv[2] if len(sys.argv) > 2 else "assets/face-clean.png")
