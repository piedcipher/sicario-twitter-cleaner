import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_icon(size):
    # Use 4x supersampling for ultra-crisp antialiased rendering
    scale = 4
    canvas_size = size * scale
    img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx = canvas_size / 2.0
    cy = canvas_size / 2.0
    r = canvas_size * 0.44

    # Outer squircle / rounded tactical shield background
    bg_pad = canvas_size * 0.04
    rect_box = [bg_pad, bg_pad, canvas_size - bg_pad, canvas_size - bg_pad]
    corner_radius = canvas_size * 0.22
    
    # Shadow/Glow under base
    shadow_pad = bg_pad * 0.8
    draw.rounded_rectangle(
        [shadow_pad, shadow_pad + canvas_size * 0.02, canvas_size - shadow_pad, canvas_size - shadow_pad + canvas_size * 0.02],
        radius=corner_radius,
        fill=(10, 14, 20, 180)
    )

    # Base shield - Dark tactical obsidian
    draw.rounded_rectangle(rect_box, radius=corner_radius, fill=(13, 17, 23, 255), outline=(218, 165, 32, 200), width=int(max(1, 2 * scale)))

    # Inner subtle border (Wayne Tech / Reacher tactical HUD)
    inner_pad = canvas_size * 0.09
    draw.rounded_rectangle(
        [inner_pad, inner_pad, canvas_size - inner_pad, canvas_size - inner_pad],
        radius=corner_radius * 0.75,
        fill=None,
        outline=(35, 45, 60, 255),
        width=int(max(1, 1 * scale))
    )

    # Crosshair Reticle Ring (Sicario / Narcos hitman precision)
    ring_r = r * 0.65
    ring_box = [cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r]
    draw.ellipse(ring_box, outline=(229, 169, 60, 180), width=int(max(1, 1.8 * scale)))

    # Crosshair tick marks (North, South, East, West)
    tick_len = r * 0.32
    tick_w = int(max(1, 2.2 * scale))
    gap = r * 0.22

    gold_bright = (255, 200, 70, 255)
    red_accent = (255, 60, 80, 240)

    # Top line
    draw.line([(cx, cy - gap), (cx, cy - gap - tick_len)], fill=gold_bright, width=tick_w)
    # Bottom line
    draw.line([(cx, cy + gap), (cx, cy + gap + tick_len)], fill=gold_bright, width=tick_w)
    # Left line
    draw.line([(cx - gap, cy), (cx - gap - tick_len, cy)], fill=gold_bright, width=tick_w)
    # Right line
    draw.line([(cx + gap, cy), (cx + gap + tick_len, cy)], fill=gold_bright, width=tick_w)

    # Silicon Valley "Middle-Out" Compression Chevrons (> <)
    chev_h = r * 0.45
    chev_w = r * 0.25
    chev_dist = r * 0.52

    # Left chevron pointing right: >
    p1 = (cx - chev_dist - chev_w, cy - chev_h)
    p2 = (cx - chev_dist, cy)
    p3 = (cx - chev_dist - chev_w, cy + chev_h)
    draw.line([p1, p2, p3], fill=(0, 230, 150, 220), width=int(max(1, 2.5 * scale)), joint="miter")

    # Right chevron pointing left: <
    p4 = (cx + chev_dist + chev_w, cy - chev_h)
    p5 = (cx + chev_dist, cy)
    p6 = (cx + chev_dist + chev_w, cy + chev_h)
    draw.line([p4, p5, p6], fill=(0, 230, 150, 220), width=int(max(1, 2.5 * scale)), joint="miter")

    # Center elimination dot (Red Laser Dot / Hitman crosshair center / Pitcher core spark)
    dot_r = r * 0.12
    draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=red_accent, outline=(255, 255, 255, 255), width=int(max(1, 1 * scale)))

    # Downscale with high quality Lanczos filter
    final_img = img.resize((size, size), Image.Resampling.LANCZOS)
    return final_img

out_dir = "/Users/tirthpatel/.gemini/antigravity/scratch/sicario-twitter-cleaner/icons"
for s in [16, 48, 128]:
    im = create_icon(s)
    path = os.path.join(out_dir, f"icon{s}.png")
    im.save(path, "PNG")
    print(f"Generated {path} ({s}x{s})")

# Also write a rich vector SVG version
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#161B22"/>
      <stop offset="50%" stop-color="#0E1218"/>
      <stop offset="100%" stop-color="#07090C"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFE082"/>
      <stop offset="50%" stop-color="#FFB300"/>
      <stop offset="100%" stop-color="#FF8F00"/>
    </linearGradient>
    <linearGradient id="neonGreen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00FFA3"/>
      <stop offset="100%" stop-color="#00B0FF"/>
    </linearGradient>
    <radialGradient id="laserGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FF3366" stop-opacity="1"/>
      <stop offset="60%" stop-color="#FF0044" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#FF0044" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="16" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
  </defs>

  <!-- Base Tactical Shield (Wayne Tech / Reacher Armor) -->
  <rect x="24" y="24" width="464" height="464" rx="112" fill="url(#bgGrad)" stroke="url(#goldGrad)" stroke-width="8" filter="url(#shadow)"/>
  
  <!-- Subtle Internal HUD Ring -->
  <circle cx="256" cy="256" r="160" fill="none" stroke="#2B3545" stroke-width="4" stroke-dasharray="8 6"/>

  <!-- Sicario Sniper Crosshair Ring (Narcos Gold) -->
  <circle cx="256" cy="256" r="120" fill="none" stroke="url(#goldGrad)" stroke-width="7" opacity="0.9"/>
  
  <!-- Crosshair Reticle Axes -->
  <line x1="256" y1="84" x2="256" y2="176" stroke="url(#goldGrad)" stroke-width="7" stroke-linecap="round"/>
  <line x1="256" y1="336" x2="256" y2="428" stroke="url(#goldGrad)" stroke-width="7" stroke-linecap="round"/>
  <line x1="84" y1="256" x2="176" y2="256" stroke="url(#goldGrad)" stroke-width="7" stroke-linecap="round"/>
  <line x1="336" y1="256" x2="428" y2="256" stroke="url(#goldGrad)" stroke-width="7" stroke-linecap="round"/>

  <!-- Silicon Valley Middle-Out Compression Chevrons (> <) -->
  <path d="M 172 170 L 214 256 L 172 342" fill="none" stroke="url(#neonGreen)" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 340 170 L 298 256 L 340 342" fill="none" stroke="url(#neonGreen)" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Central Laser Eliminator Point (The Sicario / Bat-signal focus / Pitcher clarity) -->
  <circle cx="256" cy="256" r="28" fill="url(#laserGlow)"/>
  <circle cx="256" cy="256" r="14" fill="#FF1744" stroke="#FFFFFF" stroke-width="4"/>
</svg>
"""

with open(os.path.join(out_dir, "logo.svg"), "w") as f:
    f.write(svg_content.strip())
print("Saved logo.svg successfully!")
