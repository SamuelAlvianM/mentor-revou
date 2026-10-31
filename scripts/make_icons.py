"""Build the round header logo and favicons from the ORIGINAL (undistorted) SAM logo.

Never resize the landscape original to a square: crop a square around the logo instead.
Usage: backend/.venv/Scripts/python scripts/make_icons.py
"""
from pathlib import Path

from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent.parent
src = Image.open(root / "scripts" / "assets" / "logo-sam-original.jpg").convert("RGB")
W, H = src.size

# Square crop centred on the logo (ring centre), wide enough to keep the whole orbit.
CX, CY = int(W * 0.5), int(H * 0.48)
half = 500
box = (CX - half, max(0, CY - half), CX + half, min(H, CY + half))
sq = src.crop(box)
side = min(sq.size)
sq = sq.crop(((sq.width - side) // 2, (sq.height - side) // 2, (sq.width + side) // 2, (sq.height + side) // 2))

pub = root / "frontend" / "public"
sq.resize((512, 512), Image.LANCZOS).save(pub / "logo-sam.jpg", quality=92)


def round_icon(size: int) -> Image.Image:
    im = sq.resize((size, size), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
    im.putalpha(mask.resize((size, size), Image.LANCZOS))
    return im


for name, size in (("favicon-16.png", 16), ("favicon-32.png", 32)):
    round_icon(size).save(pub / name)
ico = round_icon(64)
ico.save(pub / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
ico.save(root / "frontend" / "app" / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
sq.resize((180, 180), Image.LANCZOS).save(pub / "apple-touch-icon.png")  # iOS rounds this itself
print("icons ok", src.size, "crop", box)
