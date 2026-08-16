#!/usr/bin/env python3
"""Grade the cutout so it survives on a dark thumbnail background.

This is colour work, not generative retouching: an S-curve for contrast, a
saturation lift, a warm/cool split-tone, and an unsharp pass. Alpha is carried
through untouched so the matted hair edge stays soft.

    python3 grade-face.py assets/face.png assets/face-graded.png
"""
import sys
from PIL import Image, ImageEnhance, ImageFilter


def s_curve(strength: float = 0.18):
    """Contrast curve that lifts highlights and drops shadows without clipping."""
    lut = []
    for i in range(256):
        x = i / 255.0
        # smoothstep blended with identity by `strength`
        y = x + strength * (x * x * (3 - 2 * x) - x) * 3.0
        lut.append(max(0, min(255, int(round(y * 255)))))
    return lut


def split_tone(img: Image.Image, warm=(1.045, 1.005, 0.955), cool=(0.975, 0.995, 1.05)):
    """Warm the highlights, cool the shadows — cheap cinematic separation."""
    r, g, b = img.split()
    lum = img.convert("L")
    out = []
    for chan, w, c in zip((r, g, b), warm, cool):
        hi = chan.point(lambda v, w=w: min(255, int(v * w)))
        lo = chan.point(lambda v, c=c: min(255, int(v * c)))
        out.append(Image.composite(hi, lo, lum))
    return Image.merge("RGB", out)


def grade(src: str, dst: str):
    im = Image.open(src).convert("RGBA")
    alpha = im.getchannel("A")
    rgb = im.convert("RGB")

    lut = s_curve(0.20)
    rgb = rgb.point(lut * 3)
    rgb = split_tone(rgb)
    rgb = ImageEnhance.Color(rgb).enhance(1.26)      # saturation
    rgb = ImageEnhance.Brightness(rgb).enhance(1.04)
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=2.2, percent=115, threshold=3))

    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    out.save(dst)
    print(f"graded {src} -> {dst}  {out.size}")


if __name__ == "__main__":
    grade(sys.argv[1] if len(sys.argv) > 1 else "assets/face.png",
          sys.argv[2] if len(sys.argv) > 2 else "assets/face-graded.png")
