"""Turn raw PNG captures into optimized WebP frames in frontend/public/shots.

Usage: backend/.venv/Scripts/python scripts/make_shots.py <raw_dir>
"""
import sys
from pathlib import Path

from PIL import Image

raw = Path(sys.argv[1])
out = Path(__file__).resolve().parent.parent / "frontend" / "public" / "shots"
out.mkdir(parents=True, exist_ok=True)

# name -> (source file, optional crop box)
FRAMES = {
    "penbisa-home": ("penbisa-home.png", None),
    "penbisa-karya": ("penbisa-karya.png", None),
    "orbita-home": ("orbita-home.png", None),
    "orbita-modul": ("orbita-modul.png", None),
    "orbita-parts": ("orbita-tall.png", (0, 1170, 1440, 2070)),
    "orbita-start": ("orbita-tall.png", (0, 1990, 1440, 2890)),
    "cosmos-home": ("cosmos-home.png", None),
    "cosmos-products": ("cosmos-products.png", None),
    "cc-home": ("cc-home.png", None),
    "cheverse": ("cheverse.png", None),
    "konsa-1": ("konsa-s0.png", None),
    "konsa-2": ("konsa-s1.png", None),
    "sr-home": ("sr-home.png", None),
    "sr-unit": ("sr-unit.png", None),
    "ma-home": ("ma-home.png", None),
    "ma-list": ("ma-list.png", None),
    "ma-loans": ("ma-loans.png", None),
    "ma-events": ("ma-events.png", None),
}

for name, (src, box) in FRAMES.items():
    path = raw / src
    if not path.exists():
        print("skip", name)
        continue
    im = Image.open(path).convert("RGB")
    if box:
        im = im.crop(box)
    im.save(out / f"{name}.webp", "WEBP", quality=82, method=6)
    print("ok", name, im.size)
