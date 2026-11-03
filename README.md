# 🎯 SICARIO — Tactical Twitter (X) UI Eliminator

> *"Plata o Plomo. Eliminate Twitter UI without mercy."*

A tactical, high-performance **Manifest V3 Chrome Extension** designed to ruthlessly eliminate algorithmic bloatware, AI distractions, and unwanted UI noise from Twitter (X.com).

Built with **Material Design 3**, zero-flicker CSS injection at `document_start`, and zero telemetry.

---

## ⚡ The Inspirations & The Identity

Built at the intersection of 5 legendary pop-culture pillars:

1. **NARCOS (*Sicario / El Patrón*)**: The primary identity. A quiet hitman taking out targets with lethal precision. No negotiations, no clutter.
2. **SILICON VALLEY (*Middle-Out*)**: Lossless feed compression. Compressing Twitter down to only the pure signal and zero bloatware.
3. **BATMAN (*The Dark Knight*)**: Gotham stealth aesthetics, WayneTech HUD, and vigilance against algorithmic noise.
4. **REACHER (*Jack Reacher*)**: "Details matter." Minimalist subtraction. Traveling light with zero baggage.
5. **TVF PITCHERS (*Tu Beer Hai*)**: *"Tu content hai! Flow kar, glass ko ignore kar."* You are the beer; the bloated UI is just an annoying container.

---

## 🚀 Key Features

- **⚡ Zero-Flicker Execution**: Injected directly at `document_start` before React paints the DOM — no awkward UI popping.
- **🛡️ 1-Click "Hide All Noise" Shield**: Master noise switch to vaporize Trends, Who to Follow, Grok AI, and metrics in a single tap.
- **🎯 Point & Click Element Eliminator**: Interactive crosshair tool. Hover over *any* unwanted element on Twitter/X and click to permanently vaporize it.
- **🎛️ Granular Distraction Targets**:
  - **Trends & "What’s Happening"**: Hides viral topic sidebars and trending cards.
  - **"Who to Follow"**: Removes algorithmic suggested accounts.
  - **Notifications**: Hides notification Bell link and unread counter badges.
  - **Chats & Direct Messages**: Hides Messages nav item and the floating bottom-right chat dock.
  - **Audio & Video Calls**: Blocks call buttons and start-a-call prompts across DMs.
  - **Search & Activity History**: Hides recent search dropdown items and history suggestions.
  - **Grok AI**: Blocks navigation drawer, sidebar widgets, and inline tweet prompt buttons.
  - **Premium & Verified Promos**: Blocks subscription upsells and badge prompts.
  - **Tweet View Counts / Impressions**: Hides view count metrics from all tweets.
  - **Explore Tab**: Option to hide the explore magnifying glass from navigation.
- **🚫 Permanent Cleanups**: Jobs tab, Communities tab, and bottom floating signup/cookie banners are permanently removed.
- **✍️ Custom User Rules**: Add any custom CSS selector directly from the popup with 1-click restore.
- **🎭 5 Material Design 3 Themes**:
  - 🔫 **Sicario**: Narcos Gold & Crimson
  - 📉 **Middle-Out**: Pied Piper Emerald & Weissman Blue
  - 🦇 **Dark Knight**: Gotham Stealth Black & Bat-Signal Yellow
  - 🎯 **Reacher**: Tactical Olive & Slate
  - 🍺 **Tu Beer Hai**: Craft Amber Brew & Warm Gold
- **🔒 100% Private & Local**: Zero analytics, zero network requests, zero tracking. All settings are stored locally in Chrome Sync Storage.

---

## 📥 Installation & Setup Instructions

> [!NOTE]
> **Why Manual Installation?**
> Due to the Chrome Web Store developer account publishing limit (5/5 items limit reached), **Sicario** is distributed directly as an open-source, unpacked extension. Manual installation takes under 60 seconds and gives you full control and direct code inspectability.

Works on **Google Chrome**, **Brave**, **Microsoft Edge**, **Arc**, and any Chromium-based browser.

### Option A: Clone with Git (Recommended)

1. Open your terminal and clone the repository:
   ```bash
   git clone https://github.com/piedcipher/sicario-twitter-cleaner.git
   ```
2. Open your browser and navigate to:
   - **Chrome**: `chrome://extensions`
   - **Brave**: `brave://extensions`
   - **Edge**: `edge://extensions`
3. Toggle on **Developer mode** in the top-right corner.
4. Click the **Load unpacked** button in the top-left toolbar.
5. In the file dialog, select the `sicario-twitter-cleaner` folder that you just cloned.
6. Done! Click the puzzle icon 🧩 in your browser toolbar and pin **Sicario**.

---

### Option B: Download ZIP (No Git Required)

1. Go to [https://github.com/piedcipher/sicario-twitter-cleaner](https://github.com/piedcipher/sicario-twitter-cleaner).
2. Click the green **Code** button and select **Download ZIP**.
3. Extract the downloaded ZIP file to a folder on your computer (e.g. in your `Documents` or `Developer` folder).
   > *Note: Do not delete or move this folder after installing, as Chrome loads the extension directly from it.*
4. Open Chrome and go to `chrome://extensions`.
5. Enable **Developer mode** (top-right toggle).
6. Click **Load unpacked** (top-left).
7. Select the extracted `sicario-twitter-cleaner` folder.
8. Pin **Sicario** to your extensions bar and visit [x.com](https://x.com).

---

## 🔄 How to Update to the Latest Version

### If you installed via Git:
```bash
cd sicario-twitter-cleaner
git pull origin main
```
Then visit `chrome://extensions` and click the 🔄 **Reload** icon on the **Sicario** extension card.

### If you downloaded as a ZIP:
1. Download and extract the newest ZIP from GitHub, replacing the existing files.
2. Visit `chrome://extensions` and click the 🔄 **Reload** icon on the Sicario card.

---

## 🛠️ Project Structure

```
sicario-twitter-cleaner/
├── manifest.json            # Manifest V3 extension configuration
├── .gitignore               # Ignored system & cache files
├── README.md                # Documentation & setup guide
├── background/
│   └── background.js        # Service worker managing badge status & lifecycle
├── content/
│   ├── content.js           # Zero-flicker CSS engine, DOM failsafes & picker
│   └── content.css          # Tactical HUD reticle & picker highlights
├── popup/
│   ├── popup.html           # Material Design 3 interface with expandable accordions
│   ├── popup.css            # Multi-theme stylesheet & fluid typography
│   └── popup.js             # Live settings broadcaster & theme switcher
└── icons/
    ├── icon16.png           # 16x16 toolbar icon
    ├── icon48.png           # 48x48 extension manager icon
    ├── icon128.png          # 128x128 store/retina icon
    └── logo.svg             # High-res vector emblem
```

---

## ❓ Troubleshooting & FAQ

#### 1. The extension isn't hiding a new section Twitter just rolled out.
Twitter frequently changes internal class names. Sicario uses stable attribute selectors (`data-testid`, `aria-label`, semantic roles) and parent-relative queries. If an element persists:
- Click the **Point & Click to Eliminate** crosshair in the Sicario popup.
- Hover over the offending element and click it to vaporize it instantly. It will be saved into your **Custom Rules**.

#### 2. How do I turn elements back on?
Click the extension icon, open **Granular Target Toggles**, and toggle the switch back to active. Changes take effect across your Twitter tabs in real time without refreshing.

#### 3. Does this slow down Twitter?
No! Sicario injects plain CSS rules at `document_start` before the DOM renders. It actually makes Twitter **faster** by preventing the browser from rendering heavy sidebar videos, carousels, and ads.

---

## 📄 License

MIT License — free for personal and commercial use. Feel free to fork, customize, or contribute!
