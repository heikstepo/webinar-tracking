#!/usr/bin/env python3
"""Retouch the cutout: even the lighting, lift the shadows, calm the skin.

This is classic frequency-separation retouching, not generative editing — there
is no image model in this pipeline. Concretely it can:

  * lift crushed shadows and even out the key light across the face
  * attenuate skin texture and blemishes while keeping edges (eyes, brows, lips)
  * reduce the *appearance* of neck stubble by pulling dark low-contrast pixels
    in the neck region toward the surrounding skin tone

What it cannot do is genuinely remove a beard. That needs inpainting — inventing
skin that was never photographed. NECK_STRENGTH is capped low on purpose;
pushing it further smears the jawline into plastic instead of looking clean.

    python3 retouch-face.py assets/face-clean.png assets/face-retouched.png
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

SKIN_SMOOTH = 0.72      # keep this fraction of skin texture (lower = smoother)
NECK_SMOOTH = 0.52      # neck gets flattened harder than the face
NECK_STRENGTH = 0.34    # how far neck darks are pulled toward local skin tone
SHADOW_LIFT = 0.15      # 0..1
RELIGHT = 0.07          # strength of the soft key light


def gauss(a: np.ndarray, r: float) -> np.ndarray:
    return np.array(
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(r)), dtype=np.float32)


def skin_mask(rgb: np.ndarray) -> np.ndarray:
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    lum = rgb.mean(axis=2)
    m = ((r > 70) & (g > 30) & (b > 15) & (mx - mn > 12) &
         (r > g + 8) & (r > b + 12) &
         (lum > 95) &            # brows, lashes, beard stay sharp
         (mx - mn < 82))         # lips are far more saturated than cheeks
    return np.clip(gauss(m.astype(np.float32) * 255, 9) / 255.0, 0, 1)


def retouch(src: str, dst: str):
    im = Image.open(src).convert("RGBA")
    arr = np.array(im).astype(np.float32)
    rgb, alpha = arr[:, :, :3].copy(), arr[:, :, 3]
    h, w = rgb.shape[:2]

    skin = skin_mask(rgb)

    # ---- locate face and neck from the silhouette ------------------------
    # A skin-colour centroid is useless here: a forearm is as "skin" as a face.
    # The alpha width profile is unambiguous — head, then a pinch at the neck,
    # then the shoulders flare out.
    solid = alpha > 128
    widths = solid.sum(axis=1).astype(np.float32)
    widths = np.convolve(widths, np.ones(31) / 31, "same")
    top = int(np.argmax(solid.any(axis=1)))
    hi = int(np.argmax(widths[top:top + int(h * 0.35)])) + top      # widest head row
    search = widths[hi:hi + int(h * 0.30)]
    neck = hi + int(np.argmin(search))                              # the pinch
    face_top, face_bot = top, neck
    chin = max(face_top + 1, neck - int((neck - top) * 0.06))
    head = solid[face_top:face_bot]
    xs = np.where(head.any(axis=0))[0]
    cx = int((xs[0] + xs[-1]) / 2)

    # ---- frequency separation -------------------------------------------
    lo = gauss(rgb, 6.0)
    detail = rgb - lo

    keep = SKIN_SMOOTH + (1.0 - skin[:, :, None]) * (1.0 - SKIN_SMOOTH)

    neck = np.zeros((h, w), np.float32)
    n0, n1 = chin, min(h, chin + int((face_bot - face_top) * 0.42))
    neck[n0:n1] = 1.0
    neck = gauss(neck * 255, 26) / 255.0
    band = np.zeros((h, w), np.float32)
    half = int((face_bot - face_top) * 0.46)
    band[:, max(0, cx - half):min(w, cx + half)] = 1.0
    neck = neck * gauss(band * 255, 26) / 255.0 * skin
    keep = keep * (1 - neck[:, :, None]) + NECK_SMOOTH * neck[:, :, None]

    out = lo + detail * keep

    # ---- pull neck darks toward the local skin tone ----------------------
    lo_neck = gauss(out, 26.0)
    lum = out.mean(axis=2)
    lum_lo = lo_neck.mean(axis=2)
    darker = np.clip((lum_lo - lum) / 42.0, 0, 1)          # stubble is darker
    pull = (neck * darker * NECK_STRENGTH)[:, :, None]
    out = out * (1 - pull) + lo_neck * pull

    # ---- lift shadows ----------------------------------------------------
    l = out.mean(axis=2, keepdims=True) / 255.0
    out = out + (1.0 - l) ** 2.2 * 255.0 * SHADOW_LIFT * skin[:, :, None]

    # ---- soft key light on the face --------------------------------------
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rad = np.sqrt(((xx - cx) / (w * 0.55)) ** 2 +
                  ((yy - (face_top + face_bot) / 2) / (h * 0.42)) ** 2)
    key = np.clip(1.0 - rad, 0, 1) ** 1.6
    out = out * (1.0 + RELIGHT * key[:, :, None])

    out = np.clip(out, 0, 255)
    res = Image.fromarray(np.dstack([out, alpha]).astype(np.uint8), "RGBA")
    res.save(dst)
    print(f"retouched {src} -> {dst}  {res.size}  "
          f"(face rows {face_top}-{face_bot}, chin {chin}, centre x {cx})")


if __name__ == "__main__":
    retouch(sys.argv[1] if len(sys.argv) > 1 else "assets/face-clean.png",
            sys.argv[2] if len(sys.argv) > 2 else "assets/face-retouched.png")
