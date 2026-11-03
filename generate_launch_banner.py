#!/usr/bin/env python3
"""
Generate a 1200x675 high-impact Twitter / X launch post banner.
Outputs to assets/twitter_launch_banner.png
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH, HEIGHT = 1200, 675
IMG_PATH = os.path.join(os.path.dirname(__file__), "assets", "twitter_launch_banner.png")
ICON_PATH = os.path.join(os.path.dirname(__file__), "icons", "icon128.png")

os.makedirs(os.path.dirname(IMG_PATH), exist_ok=True)

# 1. Base canvas
im = Image.new("RGBA", (WIDTH, HEIGHT), (10, 13, 18, 255))
draw = ImageDraw.Draw(im)

# 2. Draw subtle tactical grid
grid_color = (255, 255, 255, 8)
for x in range(0, WIDTH, 40):
    draw.line([(x, 0), (x, HEIGHT)], fill=(20, 26, 36, 255), width=1)
for y in range(0, HEIGHT, 40):
    draw.line([(0, y), (WIDTH, y)], fill=(20, 26, 36, 255), width=1)

# Subtle crosshair dots at intersections
for x in range(80, WIDTH, 160):
    for y in range(80, HEIGHT, 160):
        draw.line([(x-3, y), (x+3, y)], fill=(255, 184, 0, 40), width=1)
        draw.line([(x, y-3), (x, y+3)], fill=(255, 184, 0, 40), width=1)

# 3. Ambient Glow Effects
glow_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_layer)

# Crimson radial glow on the right (behind card)
glow_draw.ellipse([700, 100, 1200, 600], fill=(255, 23, 68, 30))
# Amber radial glow on top-left
glow_draw.ellipse([50, -50, 450, 350], fill=(255, 184, 0, 20))
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(80))
im = Image.alpha_composite(im, glow_layer)
draw = ImageDraw.Draw(im)

# 4. Fonts
font_huge = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 76, index=1)
font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32, index=1)
font_mid_bold = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20, index=1)
font_regular = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18, index=0)
font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14, index=0)
font_mono = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14, index=1)
font_mono_small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12, index=0)

# 5. LEFT COLUMN: Branding & Value Props
LEFT_X = 80

# Top Pill: OPEN SOURCE • MANIFEST V3
pill_box = [LEFT_X, 75, LEFT_X + 260, 105]
draw.rounded_rectangle(pill_box, radius=6, fill=(255, 184, 0, 25), outline=(255, 184, 0, 120), width=1)
draw.text((LEFT_X + 16, 82), "OPEN SOURCE • MANIFEST V3", font=font_mono, fill=(255, 184, 0, 255))

# Brand Title: SICARIO
draw.text((LEFT_X, 125), "SICARIO", font=font_huge, fill=(255, 255, 255, 255))
# Laser Red accent bar under title
draw.rounded_rectangle([LEFT_X, 222, LEFT_X + 140, 228], radius=3, fill=(255, 23, 68, 255))

# Tagline
draw.text((LEFT_X, 248), "Eliminate Twitter UI Without Mercy.", font=font_large, fill=(240, 243, 246, 255))

desc_text = "A tactical, zero-flicker Chrome extension designed to ruthlessly\nvaporize algorithmic noise, Grok AI, Trends, and ads from X.com."
draw.text((LEFT_X, 298), desc_text, font=font_regular, fill=(160, 175, 195, 255), spacing=6)

# Feature Badges (Pills)
features = [
    ("🛡️ 1-Click 'Hide All Noise'", (255, 23, 68)),
    ("🎯 Point & Click Eliminator", (255, 184, 0)),
    ("⚡ Zero-Flicker Injection", (0, 230, 118)),
    ("🎭 5 Material Design 3 Themes", (0, 229, 255)),
]

pill_y = 385
for label, col in features:
    # Pill box
    bbox = draw.textbbox((0, 0), label, font=font_mid_bold)
    pw = bbox[2] - bbox[0] + 32
    draw.rounded_rectangle([LEFT_X, pill_y, LEFT_X + pw, pill_y + 38], radius=8, fill=(18, 23, 32, 220), outline=(col[0], col[1], col[2], 90), width=1)
    draw.text((LEFT_X + 16, pill_y + 8), label, font=font_mid_bold, fill=(245, 247, 250, 255))
    pill_y += 48

# Bottom GitHub link
git_box = [LEFT_X, 580, LEFT_X + 440, 620]
draw.rounded_rectangle(git_box, radius=8, fill=(20, 26, 36, 255), outline=(50, 65, 85, 255), width=1)
draw.text((LEFT_X + 16, 591), "github.com/piedcipher/sicario-twitter-cleaner", font=font_mono, fill=(120, 210, 255, 255))


# 6. RIGHT COLUMN: Tactical HUD Card
CARD_X = 640
CARD_Y = 80
CARD_W = 480
CARD_H = 515

# Card background with glassmorphism border
card_box = [CARD_X, CARD_Y, CARD_X + CARD_W, CARD_Y + CARD_H]
draw.rounded_rectangle(card_box, radius=16, fill=(14, 18, 25, 240), outline=(255, 23, 68, 120), width=2)

# Card Header Bar
draw.rounded_rectangle([CARD_X, CARD_Y, CARD_X + CARD_W, CARD_Y + 54], radius=16, fill=(20, 25, 35, 255))
# Fix bottom radius of header
draw.rectangle([CARD_X, CARD_Y + 40, CARD_X + CARD_W, CARD_Y + 54], fill=(20, 25, 35, 255))
draw.line([(CARD_X, CARD_Y + 54), (CARD_X + CARD_W, CARD_Y + 54)], fill=(40, 50, 70, 255), width=1)

# Window dots
draw.ellipse([CARD_X + 20, CARD_Y + 22, CARD_X + 32, CARD_Y + 34], fill=(255, 23, 68, 255))
draw.ellipse([CARD_X + 40, CARD_Y + 22, CARD_X + 52, CARD_Y + 34], fill=(255, 184, 0, 255))
draw.ellipse([CARD_X + 60, CARD_Y + 22, CARD_X + 72, CARD_Y + 34], fill=(0, 230, 118, 255))

draw.text((CARD_X + 90, CARD_Y + 18), "SICARIO TACTICAL HUD // v1.2", font=font_mono, fill=(200, 215, 230, 255))
draw.text((CARD_X + CARD_W - 95, CARD_Y + 18), "[ ACTIVE ]", font=font_mono, fill=(0, 230, 118, 255))

# Reticle icon emblem inside HUD
if os.path.exists(ICON_PATH):
    icon_img = Image.open(ICON_PATH).convert("RGBA")
    icon_resized = icon_img.resize((84, 84), Image.Resampling.LANCZOS)
    im.paste(icon_resized, (CARD_X + 30, CARD_Y + 75), icon_resized)

draw.text((CARD_X + 130, CARD_Y + 85), "STATUS: ELIMINATION ACTIVE", font=font_mono, fill=(255, 184, 0, 255))
draw.text((CARD_X + 130, CARD_Y + 115), "TARGET RADAR: 6 THREATS NEUTRALIZED", font=font_mono_small, fill=(130, 150, 175, 255))

# Target List Items
targets = [
    ("TRENDS & 'WHAT’S HAPPENING'", "VAPORIZED", (255, 23, 68)),
    ("TODAY'S NEWS SIDEBAR CARD", "PURGED", (255, 23, 68)),
    ("GROK AI PROMPTS & DRAWER", "TERMINATED", (255, 23, 68)),
    ("WHO TO FOLLOW SUGGESTIONS", "ELIMINATED", (255, 23, 68)),
    ("PREMIUM & VERIFIED UPSELLS", "BLOCKED", (255, 184, 0)),
    ("TWEET VIEW COUNT METRICS", "HIDDEN", (0, 230, 118)),
]

ty = CARD_Y + 185
for label, status, status_col in targets:
    # Row background
    row_box = [CARD_X + 24, ty, CARD_X + CARD_W - 24, ty + 44]
    draw.rounded_rectangle(row_box, radius=8, fill=(18, 23, 33, 220), outline=(32, 42, 58, 255), width=1)
    
    # Crosshair mark
    draw.text((CARD_X + 38, ty + 12), "✕", font=font_mono, fill=(255, 23, 68, 255))
    draw.text((CARD_X + 62, ty + 13), label, font=font_mono, fill=(220, 230, 240, 255))
    
    # Status badge
    sbox = draw.textbbox((0, 0), status, font=font_mono_small)
    sw = sbox[2] - sbox[0] + 16
    draw.rounded_rectangle([CARD_X + CARD_W - 36 - sw, ty + 10, CARD_X + CARD_W - 36, ty + 34], radius=4, fill=(status_col[0], status_col[1], status_col[2], 30), outline=(status_col[0], status_col[1], status_col[2], 120), width=1)
    draw.text((CARD_X + CARD_W - 28 - sw, ty + 13), status, font=font_mono_small, fill=status_col)
    
    ty += 52

# Save Banner
im = im.convert("RGB")
im.save(IMG_PATH, "PNG", quality=95)
print(f"Successfully generated launch banner at: {IMG_PATH}")
