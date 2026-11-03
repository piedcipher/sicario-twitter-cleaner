import os
import math
from PIL import Image, ImageDraw

def render_crisp_icon(size):
    # Supersample at 4x for crispy antialiased geometry
    scale = 4
    dim = size * scale
    cx = dim / 2.0
    cy = dim / 2.0

    img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background: Ultra-deep luxury jet obsidian (#090A0E)
    # Using squircle with smooth radius
    pad = dim * 0.06
    r_corner = dim * 0.26
    draw.rounded_rectangle(
        [pad, pad, dim - pad, dim - pad],
        radius=r_corner,
        fill=(10, 11, 15, 255),
        outline=(255, 255, 255, 28),
        width=int(max(1, 1.2 * scale))
    )

    # Sleek champagne gold / platinum hairline accent
    hairline_gold = (235, 195, 120, 240)
    crisp_white = (255, 255, 255, 255)
    accent_crimson = (255, 59, 92, 255)

    # Minimal outer precision ring
    ring_radius = dim * 0.32
    draw.ellipse(
        [cx - ring_radius, cy - ring_radius, cx + ring_radius, cy + ring_radius],
        outline=(255, 255, 255, 50),
        width=int(max(1, 1.2 * scale))
    )

    # Minimalist hairline crosshair ticks with surgical gaps
    tick_w = int(max(1.5 * scale, 2))
    inner_gap = dim * 0.14
    outer_edge = dim * 0.34

    # Top & Bottom ticks
    draw.line([(cx, cy - outer_edge), (cx, cy - inner_gap)], fill=hairline_gold, width=tick_w)
    draw.line([(cx, cy + inner_gap), (cx, cy + outer_edge)], fill=hairline_gold, width=tick_w)

    # Left & Right ticks
    draw.line([(cx - outer_edge, cy), (cx - inner_gap, cy)], fill=hairline_gold, width=tick_w)
    draw.line([(cx + inner_gap, cy), (cx + outer_edge, cy)], fill=hairline_gold, width=tick_w)

    # Sleek Minimalist Aperture Chevrons (> <)
    # Scaled down to be classy, integrated micro-accents
    ch_h = dim * 0.12
    ch_w = dim * 0.06
    ch_offset = dim * 0.18

    # Left chevron >
    draw.line(
        [(cx - ch_offset - ch_w, cy - ch_h), (cx - ch_offset, cy), (cx - ch_offset - ch_w, cy + ch_h)],
        fill=crisp_white,
        width=int(max(1.2 * scale, 1))
    )

    # Right chevron <
    draw.line(
        [(cx + ch_offset + ch_w, cy - ch_h), (cx + ch_offset, cy), (cx + ch_offset + ch_w, cy + ch_h)],
        fill=crisp_white,
        width=int(max(1.2 * scale, 1))
    )

    # Central micro precision dot (Single classy ruby/crimson pinpoint)
    dot_r = dim * 0.04
    draw.ellipse(
        [cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r],
        fill=accent_crimson
    )

    # Downsample with Lanczos filter for razor-sharp crispy edges
    return img.resize((size, size), Image.Resampling.LANCZOS)

out_dir = "/Users/tirthpatel/.gemini/antigravity/scratch/sicario-twitter-cleaner/icons"
for s in [16, 48, 128]:
    im = render_crisp_icon(s)
    path = os.path.join(out_dir, f"icon{s}.png")
    im.save(path, "PNG")
    print(f"Generated {path} ({s}x{s})")

# Write minimal vector SVG
svg_minimal = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#141720"/>
      <stop offset="100%" stop-color="#08090C"/>
    </radialGradient>
    <linearGradient id="goldLuxury" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FCE4B8"/>
      <stop offset="100%" stop-color="#D4AF37"/>
    </linearGradient>
  </defs>

  <!-- Base Squircle -->
  <rect x="24" y="24" width="464" height="464" rx="128" fill="url(#bgGlow)" stroke="rgba(255, 255, 255, 0.08)" stroke-width="2"/>
  
  <!-- Outer Precision Sub-Ring -->
  <circle cx="256" cy="256" r="168" fill="none" stroke="rgba(255, 255, 255, 0.06)" stroke-width="1.5"/>

  <!-- Tactical Scope Ring -->
  <circle cx="256" cy="256" r="128" fill="none" stroke="rgba(255, 255, 255, 0.16)" stroke-width="2"/>

  <!-- Minimalist Hairline Crosshair Ticks -->
  <line x1="256" y1="96" x2="256" y2="184" stroke="url(#goldLuxury)" stroke-width="3" stroke-linecap="round"/>
  <line x1="256" y1="328" x2="256" y2="416" stroke="url(#goldLuxury)" stroke-width="3" stroke-linecap="round"/>
  <line x1="96" y1="256" x2="184" y2="256" stroke="url(#goldLuxury)" stroke-width="3" stroke-linecap="round"/>
  <line x1="328" y1="256" x2="416" y2="256" stroke="url(#goldLuxury)" stroke-width="3" stroke-linecap="round"/>

  <!-- Classy Middle-Out Micro-Chevrons -->
  <path d="M 180 208 L 204 256 L 180 304" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>
  <path d="M 332 208 L 308 256 L 332 304" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>

  <!-- Central Surgical Dot -->
  <circle cx="256" cy="256" r="16" fill="#FF3B5C"/>
  <circle cx="256" cy="256" r="6" fill="#FFFFFF"/>
</svg>
"""

with open(os.path.join(out_dir, "logo.svg"), "w") as f:
    f.write(svg_minimal.strip())

print("Classy minimal logo.svg generated!")
