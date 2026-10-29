"""Render social cards from the project's J2000 stars and constellations.

Run `py scripts/social_banners.py` with Pillow installed. Fonts and their
OFL licenses are bundled in scripts/assets/fonts. Colors and typography
follow Chulapa's gitdev-dark skin. No network access is needed.
"""

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "scripts/assets/fonts"
BACKGROUND = "#24292f"
BLUE = "#79b8ff"
SCALE = 2


def render(width, height, filename):
    canvas = Image.new("RGB", (width * SCALE, height * SCALE), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    sx, sy = width / 1280 * SCALE, height / 640 * SCALE
    cx, cy, radius = 1000 * sx, 320 * sy, 370 * sy
    center_lon, center_lat = map(math.radians, (65, 25))

    def project(lon, lat):
        lon, lat = math.radians(lon) - center_lon, math.radians(lat)
        depth = (math.sin(center_lat) * math.sin(lat)
                 + math.cos(center_lat) * math.cos(lat) * math.cos(lon))
        if depth < 0:
            return None
        x = math.cos(lat) * math.sin(lon)
        y = (math.cos(center_lat) * math.sin(lat)
             - math.sin(center_lat) * math.cos(lat) * math.cos(lon))
        return cx - radius * x, cy - radius * y

    def line(coords, color, thickness):
        previous = None
        for point in coords:
            current = project(*point)
            if current is not None and previous is not None:
                draw.line((previous, current), fill=color, width=thickness)
            previous = current

    draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius),
                 fill="#20252b", outline="#485460", width=2)
    for latitude in range(-60, 90, 30):
        line([(lon, latitude) for lon in range(-180, 181)], "#373e47", 1)
    for longitude in range(-180, 180, 30):
        line([(longitude, lat) for lat in range(-90, 91)], "#373e47", 1)

    stars = json.loads((ROOT / "data/stars.6.geojson").read_text())
    for feature in stars["features"]:
        point = project(*feature["geometry"]["coordinates"])
        if point is None:
            continue
        magnitude = feature["properties"]["mag"]
        r = max(.55, (6.7 - magnitude) * .36) * SCALE
        x, y = point
        color = "#ffffff" if magnitude < 3 else "#a8b3c1"
        draw.ellipse((x-r, y-r, x+r, y+r), fill=color)

    constellations = json.loads(
        (ROOT / "data/constellations.lines.geojson").read_text())
    for feature in constellations["features"]:
        for segment in feature["geometry"]["coordinates"]:
            line(segment, BLUE, 2 * SCALE)

    # Fade the real celestial chart behind the text, as in the reference cards.
    mask = Image.new("L", canvas.size)
    ramp = [round(255 * (1 - max(0, min(1, (x / canvas.width - .35) / .31))))
            for x in range(canvas.width)]
    mask.putdata(ramp * canvas.height)
    canvas = Image.composite(Image.new("RGB", canvas.size, BACKGROUND),
                             canvas, mask)
    draw = ImageDraw.Draw(canvas)

    def text(x, y, value, size, color="white", heading=False):
        font = ImageFont.truetype(
            str(FONTS / ("InterTight.ttf" if heading else "Inter.ttf")),
            round(size * sx))
        if heading:
            font.set_variation_by_axes([800])
        draw.text((round(x*sx), round(y*sy)), value, font=font,
                  fill=color, anchor="lt")

    text(64, 66, "OPEN DATA · J2000", 20, BLUE)
    text(60, 142, "Celestial", 100, heading=True)
    text(60, 252, "Data", 100, heading=True)
    text(64, 402, "The sky in GeoJSON", 29)
    text(64, 445, "and GeoPackage", 29)
    text(64, 565, "Explore the sky. Download the data.", 20)
    draw.rectangle((960*sx, 596*sy, width*SCALE, height*SCALE),
                   fill=BACKGROUND)
    text(974, 606, "Source: d3-celestial", 13, "#a8b3c1")
    canvas = canvas.resize((width, height), Image.Resampling.LANCZOS)
    destination = ROOT / "assets/img" / filename
    canvas.save(destination, quality=95, subsampling=0, optimize=True)
    print(f"{destination.name}: {width} × {height}")


if __name__ == "__main__":
    render(1200, 630, "social-preview.jpg")
    render(1280, 640, "github-preview.jpg")
