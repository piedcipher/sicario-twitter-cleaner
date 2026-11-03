# 🎯 SICARIO — Tactical Twitter (X) UI Eliminator

> *"Plata o Plomo. Eliminate Twitter UI without mercy."*

A tactical, high-performance Manifest V3 Chrome Extension designed to ruthlessly eliminate unwanted UI elements, bloatware, and distractions from Twitter (X.com).

---

## ⚡ The Inspirations & The Identity

Built at the intersection of 5 legendary pop-culture pillars:

1. **NARCOS (*Sicario / El Patrón*)**: The primary identity. A quiet hitman taking out targets with lethal precision. No negotiations, no clutter.
2. **SILICON VALLEY (*Middle-Out*)**: Lossless feed compression. Compressing Twitter down to only the pure signal and zero bloatware.
3. **BATMAN (*The Dark Knight*)**: Gotham stealth aesthetics, WayneTech HUD, and vigilance against algorithmic noise.
4. **REACHER (*Jack Reacher*)**: "Details matter." Minimalist subtraction. Traveling light with zero baggage.
5. **TVF PITCHERS (*Tu Beer Hai*)**: *"Tu content hai! Flow kar, glass ko ignore kar."* You are the beer; the bloated UI is just an annoying container.

---

## 🎨 The Logo Design

The emblem in `icons/logo.svg` synthesizes elements from all 5 inspirations:
- **WayneTech / Reacher Outer Plate**: Angular dark obsidian tactical shield with drop shadow.
- **Narcos Gold Reticle**: The circular sniper crosshair marking targets for elimination.
- **Silicon Valley Chevrons (`> <`)**: The Middle-Out compression brackets focusing inwards.
- **Laser Eliminator Point**: The glowing central focal point of pure signal.

Icons are included in `16x16`, `48x48`, and `128x128` PNG formats, plus raw vector SVG.

---

## 🚀 Key Features

- **⚡ Zero-Flicker Execution**: Injected directly at `document_start` before React paints the DOM.
- **🎯 Point & Click Element Eliminator**: Click the crosshair tool in the popup, hover over *any* element on Twitter/X, and click to permanently vaporize it!
- **🎛️ Pre-Baked Distraction Targets**:
  - Right Sidebar column (and auto-centers the main timeline feed)
  - "What's Happening" / Viral trending topics
  - "Who to Follow" recommendation modules
  - Grok AI navigation links & in-feed prompts
  - Premium & Verified subscription upsell banners
  - Tweet view counts / analytics impressions
  - Explore, Jobs, and Communities tabs
  - Bottom signup & cookie floating bars
- **✍️ "Tell Me What To Hide" (Custom Rules)**:
  - Add any CSS selector (e.g. `[data-testid="chat-drawer"]`, `#layers`, etc.)
  - Real-time rule management with one-click restore (🗑️)
- **🎭 5 Switchable Tactical Themes**:
  - 🔫 **Sicario** (Narcos Gold & Crimson)
  - 📉 **Middle-Out** (Pied Piper Emerald & Electric Blue)
  - 🦇 **Dark Knight** (Gotham Stealth Black & Bat-Signal Yellow)
  - 🎯 **Reacher** (Tactical Olive & Slate)
  - 🍺 **Tu Beer Hai** (Craft Amber Brew & Warm Gold)

---

## 📦 How to Install in Chrome

1. Open Google Chrome.
2. Navigate to `chrome://extensions`.
3. In the top-right corner, enable **Developer mode**.
4. Click **Load unpacked** in the top-left corner.
5. Select this directory:
   ```
   /Users/tirthpatel/.gemini/antigravity/scratch/sicario-twitter-cleaner
   ```
6. Pin the **Sicario** icon to your Chrome toolbar.
7. Open [x.com](https://x.com) or [twitter.com](https://twitter.com) and enjoy a distraction-free feed!

---

## 🛠️ Project Structure

```
sicario-twitter-cleaner/
├── manifest.json            # Manifest V3 configuration
├── icons/
│   ├── icon16.png           # 16x16 extension icon
│   ├── icon48.png           # 48x48 extension icon
│   ├── icon128.png          # 128x128 extension icon
│   └── logo.svg             # High-res vector emblem
├── popup/
│   ├── popup.html           # Popup interface
│   ├── popup.css            # Multi-theme HUD stylesheet
│   └── popup.js             # State management & theme switcher
├── content/
│   ├── content.js           # Zero-flicker CSS injector & target picker
│   └── content.css          # Target reticle & HUD styles
├── background/
│   └── background.js        # Service worker & extension badge
└── generate_icons.py        # Icon generator script
```
