#!/usr/bin/env python3
"""Shrink one of the owner's own photos for the web. Needs Pillow (pip install pillow).

  python3 optimize_image.py <input> <out_dir> <base-name> [--width 1600] [--og]

Writes <base-name>.webp (never wider than --width, never enlarged, orientation fixed, metadata
such as GPS location removed). With --og also writes <base-name>-1200x630.webp, a centred crop
for the featured / social image. Prints a JSON summary. The original is never touched.
"""
import json
import os
import re
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    print("ERROR: Pillow is not installed. Install it with:  pip install pillow")
    sys.exit(1)


def main(argv):
    args = argv[1:]
    og = "--og" in args
    args = [a for a in args if a != "--og"]
    width = 1600
    if "--width" in args:
        i = args.index("--width")
        width = int(args[i + 1])
        del args[i:i + 2]
    if len(args) < 3:
        print(__doc__)
        return 2
    src, out_dir, base = args[:3]
    if not os.path.isfile(src):
        print(f"ERROR: file not found: {src}")
        return 1
    safe = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-") or "image"
    os.makedirs(out_dir, exist_ok=True)
    img = ImageOps.exif_transpose(Image.open(src))
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    results = []

    def save(im, name):
        path = os.path.join(out_dir, name)
        im.save(path, "WEBP", quality=82, method=4)          # no exif argument: metadata is dropped
        results.append({"file": path, "width": im.width, "height": im.height, "kb": round(os.path.getsize(path) / 1024, 1)})

    main_img = img.copy()
    if main_img.width > width:
        main_img = main_img.resize((width, round(main_img.height * width / main_img.width)), Image.LANCZOS)
    save(main_img, f"{safe}.webp")
    if og:
        save(ImageOps.fit(img, (1200, 630), Image.LANCZOS, centering=(0.5, 0.5)), f"{safe}-1200x630.webp")
    print(json.dumps({"original": src, "outputs": results}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
