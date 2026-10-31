"""Turn raw PNG captures into optimized WebP frames in frontend/public/shots.

Usage: backend/.venv/Scripts/python scripts/make_shots.py <raw_dir> [<more_raw_dirs>...]
"""
import sys
from pathlib import Path

from PIL import Image

raws = [Path(a) for a in sys.argv[1:]]
out = Path(__file__).resolve().parent.parent / "frontend" / "public" / "shots"
out.mkdir(parents=True, exist_ok=True)
for old in out.glob("*.webp"):
    old.unlink()

# output name -> source png (searched in every raw dir)
FRAMES = {
    "penbisa-1": "penbisa-0.png", "penbisa-2": "penbisa-2.png", "penbisa-3": "penbisa-3.png",
    "penbisa-4": "penbisa-layanan-0.png", "penbisa-5": "penbisa-tentang-0.png",
    "orbita-1": "orbita-0.png", "orbita-2": "orbita-1.png", "orbita-3": "orbita-3.png",
    "orbita-4": "orbita-modul-0.png", "orbita-5": "orbita-harga-0.png", "orbita-6": "orbita-cara-0.png",
    "cosmos-1": "cosmos-0.png", "cosmos-2": "cosmos-1.png", "cosmos-3": "cosmos-2.png", "cosmos-4": "cosmos-3.png",
    "cc-1": "cc-0.png", "cc-2": "cc-2.png", "cc-3": "cc-3.png",
    "konsa-1": "konsa-s0.png", "konsa-2": "konsa-s1.png", "konsa-3": "konsa-s2.png",
    "hompimplay-1": "hompimplay-id-0.png", "hompimplay-2": "hompimplay-id-1.png",
    "hompimplay-3": "hompimplay-id-2.png", "hompimplay-4": "hompimplay-id-3.png",
    "cheverse-1": "che-home.png", "cheverse-2": "che-table.png", "cheverse-3": "che-element.png",
    "cheverse-4": "che-mass.png", "cheverse-5": "che-reaction.png",
    "ma-1": "ma-home.png", "ma-2": "ma-list.png", "ma-3": "ma-loans.png", "ma-4": "ma-events.png",
    "sr-1": "sr-home.png", "sr-2": "sr-unit.png",
}

for name, src in FRAMES.items():
    path = next((r / src for r in raws if (r / src).exists()), None)
    if not path:
        print("skip", name, src)
        continue
    Image.open(path).convert("RGB").save(out / f"{name}.webp", "WEBP", quality=82, method=6)
print("done", len(list(out.glob("*.webp"))))
