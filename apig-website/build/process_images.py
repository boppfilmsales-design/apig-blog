# -*- coding: utf-8 -*-
"""Normalise and enhance the legacy product photographs.

The old catalogue images are low-resolution, inconsistently cropped and often
sit on a large white field with the product occupying a small corner.  This
script trims that dead margin, scales the result with LANCZOS, applies a mild
brightness / contrast / sharpness pass and writes a consistent pair of assets:

    assets/img/<id>.jpg      1200 x 900  (product, centred, white canvas)
    assets/thumbs/<id>.jpg    480 x 360  (card thumbnails)

Output manifest: build/images.json
"""
import json
import os
import sys

from PIL import Image, ImageEnhance, ImageFilter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(HERE, "build", "raw_images")
OUT_MAIN = os.path.join(HERE, "assets", "img")
OUT_THUMB = os.path.join(HERE, "assets", "thumbs")

MAIN_SIZE = (1200, 900)
THUMB_SIZE = (480, 360)

# a pixel counts as "background" when it is this close to paper white
WHITE_CUT = 242


def trim_white(img, pad=8):
    """Crop away uniform near-white margins, keeping a small breathing gap."""
    from PIL import ImageChops

    rgb = img.convert("RGB")
    small = rgb.copy()
    small.thumbnail((420, 420))
    w, h = small.size
    corners = [small.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    ref = tuple(sum(c[i] for c in corners) // 4 for i in range(3))
    # only trim when the backdrop really is near-white
    if min(ref) < 228:
        return rgb
    bg = Image.new("RGB", small.size, ref)
    diff = ImageChops.difference(small, bg).convert("L")
    mask = diff.point(lambda p: 255 if p > 14 else 0)
    bbox = mask.getbbox()
    if not bbox:
        return rgb
    scale = w / float(rgb.size[0])
    box = (max(0, int(bbox[0] * scale) - pad), max(0, int(bbox[1] * scale) - pad),
           min(rgb.size[0], int(bbox[2] * scale) + pad),
           min(rgb.size[1], int(bbox[3] * scale) + pad))
    return rgb.crop(box)


def contain(img, size):
    """Scale to fit inside `size` and centre on a white canvas."""
    canvas = Image.new("RGB", size, (255, 255, 255))
    w, h = img.size
    ratio = min(size[0] / float(w), size[1] / float(h))
    new = (max(1, int(w * ratio)), max(1, int(h * ratio)))
    img = img.resize(new, Image.LANCZOS)
    canvas.paste(img, ((size[0] - new[0]) // 2, (size[1] - new[1]) // 2))
    return canvas


def enhance(img):
    img = ImageEnhance.Brightness(img).enhance(1.07)
    img = ImageEnhance.Contrast(img).enhance(1.06)
    img = ImageEnhance.Color(img).enhance(1.04)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.4, percent=75, threshold=3))
    return img


def process(path, name):
    try:
        src = Image.open(path)
    except Exception as exc:  # noqa: BLE001
        print("  [SKIP]", name, exc)
        return None
    src = src.convert("RGB")
    trimmed = trim_white(src)
    enhanced = enhance(trimmed)
    main = contain(enhanced, MAIN_SIZE)
    thumb = contain(enhanced, THUMB_SIZE)
    main_path = os.path.join(OUT_MAIN, name + ".jpg")
    thumb_path = os.path.join(OUT_THUMB, name + ".jpg")
    main.save(main_path, "JPEG", quality=88, optimize=True, progressive=True)
    thumb.save(thumb_path, "JPEG", quality=84, optimize=True, progressive=True)
    return {
        "main": os.path.relpath(main_path, HERE).replace("\\", "/"),
        "thumb": os.path.relpath(thumb_path, HERE).replace("\\", "/"),
        "src_size": list(src.size),
        "out_size": list(trimmed.size),
    }


def main():
    os.makedirs(OUT_MAIN, exist_ok=True)
    os.makedirs(OUT_THUMB, exist_ok=True)
    if not os.path.isdir(RAW):
        print("no raw_images directory")
        return
    files = sorted(os.listdir(RAW))
    manifest = {}
    for i, f in enumerate(files, 1):
        stem, ext = os.path.splitext(f)
        if ext.lower() not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
            continue
        info = process(os.path.join(RAW, f), stem)
        if info:
            manifest[stem] = info
        if i % 10 == 0 or i == len(files):
            print(f"  processed {i}/{len(files)}")
    with open(os.path.join(HERE, "build", "images.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
    print("images processed:", len(manifest))


if __name__ == "__main__":
    main()
