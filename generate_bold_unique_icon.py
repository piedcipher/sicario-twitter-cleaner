import os
import math
from PIL import Image, ImageDraw

def render_bold_unique_icon(size):
    # 4x supersampling for razor-sharp antialiasing
    scale = 4
    dim = size * scale
    cx = dim / 2.0
    cy = dim / 2.0

    img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Outer Squircle Base (Deep obsidian black with gold rim)
    pad = dim * 0.04
    r_corner = dim * 0.28
    
    # Outer Glow / Soft Edge
    draw.rounded_rectangle(
        [pad, pad, dim - pad, dim - pad],
        radius=r_corner,
        fill=(10, 12, 18, 255)
    )

    # Vibrant, saturated gold rim (High contrast against dark and light browser toolbars!)
    rim_w = int(max(2 * scale, 2))
    draw.rounded_rectangle(
        [pad, pad, dim - pad, dim - pad],
        radius=r_corner,
        fill=None,
        outline=(255, 184, 0, 255),
        width=rim_w
    )

    # Inner subtle tactical dark bezel
    bezel_pad = pad + dim * 0.06
    draw.rounded_rectangle(
        [bezel_pad, bezel_pad, dim - bezel_pad, dim - bezel_pad],
        radius=r_corner * 0.75,
        fill=(15, 18, 26, 255),
        outline=(255, 255, 255, 25),
        width=int(max(1 * scale, 1))
    )

    # 2. BOLD TARGET RETICLE RING
    ring_r = dim * 0.30
    ring_w = int(max(2.2 * scale, 2))
    draw.ellipse(
        [cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
        outline=(255, 195, 30, 230),
        width=ring_w
    )

    # 3. ICONIC TACTICAL "S" CHEVRONS (Middle-Out + Bat-wing angles)
    # Bold white/gold wings that form a stylized "S" reticle
    wing_w = int(max(2.8 * scale, 2))
    gold_bright = (255, 220, 80, 255)
    white_bright = (255, 255, 255, 255)

    # Upper wing (Left to Center-top): >
    uw_p1 = (cx - dim * 0.22, cy - dim * 0.22)
    uw_p2 = (cx, cy - dim * 0.26)
    uw_p3 = (cx + dim * 0.18, cy - dim * 0.12)
    draw.line([uw_p1, uw_p2, uw_p3], fill=gold_bright, width=wing_w, joint="round")

    # Lower wing (Right to Center-bottom): <
    lw_p1 = (cx + dim * 0.22, cy + dim * 0.22)
    lw_p2 = (cx, cy + dim * 0.26)
    lw_p3 = (cx - dim * 0.18, cy + dim * 0.12)
    draw.line([lw_p1, lw_p2, lw_p3], fill=gold_bright, width=wing_w, joint="round")

    # 4. CROSSHAIR TICK SPIKES (North, South, East, West)
    tick_w = int(max(2.5 * scale, 2))
    gap = dim * 0.10
    tick_len = dim * 0.18

    # North
    draw.line([(cx, cy - gap), (cx, cy - gap - tick_len)], fill=white_bright, width=tick_w)
    # South
    draw.line([(cx, cy + gap), (cx, cy + gap + tick_len)], fill=white_bright, width=tick_w)
    # West
    draw.line([(cx - gap, cy), (cx - gap - tick_len, cy)], fill=white_bright, width=tick_w)
    # East
    draw.line([(cx + gap, cy), (cx + gap + tick_len, cy)], fill=white_bright, width=tick_w)

    # 5. HIGH-VISIBILITY LASER CORE (Electric Ruby / Crimson)
    # Large, glowing center that pops immediately at 16x16!
    core_r = dim * 0.08
    draw.ellipse(
        [cx - core_r, cy - core_r, cx + core_r, cy + core_r],
        fill=(255, 23, 68, 255),
        outline=(255, 255, 255, 255),
        width=int(max(1.2 * scale, 1))
    )

    # Center white specular spark
    spark_r = dim * 0.03
    draw.ellipse(
        [cx - spark_r, cy - spark_r, cx + spark_r, cy + spark_r],
        fill=(255, 255, 255, 255)
    )

    return img.resize((size, size), Image.Resampling.LANCZOS)

out_dir = "/Users/tirthpatel/.gemini/antigravity/scratch/sicario-twitter-cleaner/icons"
for s in [16, 48, 128]:
    im = render_bold_unique_icon(s)
    path = os.path.join(out_dir, f"icon{s}.png")
    im.save(path, "PNG")
    print(f"Generated {path} ({s}x{s})")

# Also write the master SVG vector version
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#141824"/>
      <stop offset="50%" stop-color="#0A0D14"/>
      <stop offset="100%" stop-color="#05070A"/>
    </linearGradient>

    <!-- Electric Amber Gold Gradient -->
    <linearGradient id="goldGlow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFE082"/>
      <stop offset="50%" stop-color="#FFB300"/>
      <stop offset="100%" stop-color="#FF8F00"/>
    </linearGradient>

    <!-- Hot Laser Crimson -->
    <radialGradient id="laserCore" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="35%" stop-color="#FF3366"/>
      <stop offset="85%" stop-color="#FF1744"/>
      <stop offset="100%" stop-color="#D50000"/>
    </radialGradient>

    <!-- Drop Shadow -->
    <filter id="neonShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="12" flood-color="#FFB300" flood-opacity="0.35"/>
    </filter>
  </defs>

  <!-- 1. High-Contrast Obsidian Squircle Base -->
  <rect x="20" y="20" width="472" height="472" rx="140" fill="url(#bgGrad)" stroke="url(#goldGlow)" stroke-width="12" filter="url(#neonShadow)"/>
  
  <!-- 2. Inner Tactical Shield Bezel -->
  <rect x="52" y="52" width="408" height="408" rx="112" fill="#0E121B" stroke="rgba(255, 255, 255, 0.12)" stroke-width="3"/>

  <!-- 3. Glowing Tactical Reticle Ring -->
  <circle cx="256" cy="256" r="148" fill="none" stroke="url(#goldGlow)" stroke-width="10" stroke-dasharray="14 8" opacity="0.85"/>
  <circle cx="256" cy="256" r="110" fill="none" stroke="url(#goldGlow)" stroke-width="6" opacity="0.6"/>

  <!-- 4. Iconic Tactical 'S' Chevrons (Middle-Out + Batman Cowl Wings) -->
  <path d="M 148 144 L 256 124 L 348 196" fill="none" stroke="url(#goldGlow)" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 364 368 L 256 388 L 164 316" fill="none" stroke="url(#goldGlow)" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- 5. Razor-Sharp Crosshair Ticks (White Hot Contrast) -->
  <line x1="256" y1="92" x2="256" y2="192" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
  <line x1="256" y1="320" x2="256" y2="420" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
  <line x1="92" y1="256" x2="192" y2="256" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
  <line x1="320" y1="256" x2="420" y2="256" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>

  <!-- 6. Glowing Electric Laser Pinpoint Core -->
  <circle cx="256" cy="256" r="36" fill="url(#laserCore)"/>
  <circle cx="256" cy="256" r="14" fill="#FFFFFF"/>
</svg>
"""

with open(os.path.join(out_dir, "logo.svg"), "w") as f:
    f.write(svg_content.strip())

print("Saved bold unique logo.svg!")
