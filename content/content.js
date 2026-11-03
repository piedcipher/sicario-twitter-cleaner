/**
 * SICARIO — Twitter (X) UI Eliminator
 * Content Script (Injected at document_start for zero-flicker speed)
 */

(() => {
  const STYLE_ID = "sicario-injected-styles";
  let styleEl = document.getElementById(STYLE_ID);

  if (!styleEl) {
    styleEl = document.createElement("style");
    styleEl.id = STYLE_ID;
    const target = document.documentElement || document.head;
    if (target) {
      target.appendChild(styleEl);
    } else {
      document.addEventListener("DOMContentLoaded", () => {
        document.documentElement.appendChild(styleEl);
      });
    }
  }

  // CORE PERMANENT RULES (Always eliminated when extension is active)
  const CORE_PERMANENT_RULES = `
    /* Always eliminate Jobs from nav */
    a[href="/jobs"],
    [data-testid="AppTabBar_Jobs_Link"],
    div:has(> a[href="/jobs"]) {
      display: none !important;
    }

    /* Always eliminate Communities from nav */
    a[href*="/communities"],
    [data-testid="AppTabBar_Communities_Link"],
    div:has(> a[href*="/communities"]) {
      display: none !important;
    }

    /* Always eliminate Bottom floating prompts & signup banners */
    [data-testid="BottomBar"],
    div[data-testid="BottomBar"],
    #layers div:has(> [data-testid="BottomBar"]),
    #layers div:has(> div > [data-testid="BottomBar"]),
    #layers [data-testid="sheetDialog"] {
      display: none !important;
    }
  `;

  // Pre-configured CSS rules mapped to user toggle keys
  const PRESET_RULES = {
    hide_whats_happening: `
      /* Target the trend items & container */
      [aria-label="Timeline: Trending now"],
      [data-testid="trend"],
      /* Target the section containing trending */
      section:has([aria-label="Timeline: Trending now"]),
      section:has([data-testid="trend"]),
      [data-testid="sidebarColumn"] section,
      /* Target the card wrapper div inside the sidebar */
      [data-testid="sidebarColumn"] div:has(> section) {
        display: none !important;
      }
    `,
    hide_who_to_follow: `
      [aria-label="Who to follow"],
      aside[aria-label*="Who to follow"],
      aside[aria-label*="who to follow" i],
      [data-testid="sidebarColumn"] aside:has([data-testid="UserCell"]),
      [data-testid="sidebarColumn"] aside,
      /* Target the card wrapper div inside the sidebar */
      [data-testid="sidebarColumn"] div:has(> aside) {
        display: none !important;
      }
    `,
    hide_grok: `
      a[href="/i/grok"],
      [data-testid="AppTabBar_Grok_Link"],
      [data-testid="GrokDrawer"],
      [data-testid="inlineGrokPrompt"],
      button[aria-label*="Grok"],
      div:has(> a[href="/i/grok"]) {
        display: none !important;
      }
    `,
    hide_premium_promos: `
      a[href="/i/premium_sign_up"],
      a[href="/i/verified-orgs-signup"],
      aside[aria-label="Subscribe to Premium"],
      [data-testid="sidebarColumn"] aside:has(a[href*="premium"]) {
        display: none !important;
      }
    `,
    hide_view_counts: `
      a[href*="/analytics"],
      [data-testid="tweet"] a[href$="/analytics"],
      [aria-label*="views"],
      [aria-label*="View post analytics"] {
        display: none !important;
      }
    `,
    hide_explore_tab: `
      a[href="/explore"],
      [data-testid="AppTabBar_Explore_Link"] {
        display: none !important;
      }
    `,
    hide_notifications: `
      a[href="/notifications"],
      [data-testid="AppTabBar_Notifications_Link"],
      div:has(> a[href="/notifications"]) {
        display: none !important;
      }
    `,
    hide_chats: `
      a[href="/i/chat"],
      a[href="/messages"],
      [data-testid="AppTabBar_DirectMessage_Link"],
      [data-testid="DMDrawer"],
      div[data-testid="DMDrawer"],
      #layers div:has(> [data-testid="DMDrawer"]),
      div:has(> a[href="/i/chat"]),
      div:has(> a[href="/messages"]) {
        display: none !important;
      }
    `,
    hide_calls: `
      [data-testid="callButton"],
      [data-testid="audioCall"],
      [data-testid="videoCall"],
      button[aria-label*="Audio call"],
      button[aria-label*="Video call"],
      button[aria-label*="Call" i],
      button[aria-label*="call" i],
      [aria-label*="Start a call"],
      [data-testid="AppTabBar_Calls_Link"],
      a[href*="/calls"] {
        display: none !important;
      }
    `,
    hide_history: `
      [data-testid="typeaheadRecentSearchesItem"],
      [data-testid="typeaheadRecentSearchesClear"],
      [data-testid="clearRecentSearches"],
      [data-testid="SearchHistory"],
      div:has(> [data-testid="typeaheadRecentSearchesItem"]),
      div[aria-label*="Recent searches" i],
      [data-testid*="history" i],
      a[href*="/history"] {
        display: none !important;
      }
    `
  };

  // Default configuration
  const DEFAULT_SETTINGS = {
    master_active: true,
    theme: "sicario",
    hide_whats_happening: true,
    hide_who_to_follow: true,
    hide_notifications: true,
    hide_chats: true,
    hide_calls: true,
    hide_history: true,
    hide_grok: true,
    hide_premium_promos: true,
    hide_view_counts: true,
    hide_explore_tab: false,
    custom_selectors: []
  };

  let currentSettings = { ...DEFAULT_SETTINGS };

  function compileCSS(settings) {
    if (!settings.master_active) {
      return "";
    }

    let css = "/* SICARIO DYNAMIC RULES */\n";

    // 1. Core permanent rules (Jobs, Communities, Bottom prompts)
    css += `/* Permanent Core Eliminators */\n${CORE_PERMANENT_RULES}\n`;

    // 2. User toggles
    for (const [key, rule] of Object.entries(PRESET_RULES)) {
      if (settings[key]) {
        css += `/* ${key} */\n${rule}\n`;
      }
    }

    // 3. User custom rules
    if (Array.isArray(settings.custom_selectors) && settings.custom_selectors.length > 0) {
      css += "/* Custom User Elimination Rules */\n";
      for (const item of settings.custom_selectors) {
        const sel = typeof item === "string" ? item : item.selector;
        if (sel && sel.trim().length > 0) {
          css += `${sel.trim()} {\n  display: none !important;\n}\n`;
        }
      }
    }

    return css;
  }

  function cleanDOMElements() {
    if (!currentSettings.master_active) return;

    // What's happening / Trends failsafe
    if (currentSettings.hide_whats_happening) {
      const trends = document.querySelectorAll('[aria-label="Timeline: Trending now"], [data-testid="trend"]');
      trends.forEach(el => {
        const section = el.closest('section') || el.closest('[role="region"]');
        if (section) {
          section.style.setProperty('display', 'none', 'important');
          const parent = section.parentElement;
          if (parent && parent.tagName === 'DIV' && parent.getAttribute('data-testid') !== 'sidebarColumn') {
            parent.style.setProperty('display', 'none', 'important');
          }
        }
      });
    }

    // Who to follow failsafe
    if (currentSettings.hide_who_to_follow) {
      const followEls = document.querySelectorAll('[aria-label="Who to follow"], aside[aria-label*="Who to follow"]');
      followEls.forEach(el => {
        const aside = el.closest('aside') || el;
        aside.style.setProperty('display', 'none', 'important');
        const parent = aside.parentElement;
        if (parent && parent.tagName === 'DIV' && parent.getAttribute('data-testid') !== 'sidebarColumn') {
          parent.style.setProperty('display', 'none', 'important');
        }
      });
    }

    // Notifications failsafe
    if (currentSettings.hide_notifications) {
      document.querySelectorAll('a[href="/notifications"], [data-testid="AppTabBar_Notifications_Link"]').forEach(el => {
        el.style.setProperty('display', 'none', 'important');
      });
    } else {
      document.querySelectorAll('a[href="/notifications"], [data-testid="AppTabBar_Notifications_Link"]').forEach(el => {
        el.style.removeProperty('display');
      });
    }

    // Chats / Direct Messages failsafe
    if (currentSettings.hide_chats) {
      document.querySelectorAll('a[href="/i/chat"], a[href="/messages"], [data-testid="AppTabBar_DirectMessage_Link"], [data-testid="DMDrawer"]').forEach(el => {
        el.style.setProperty('display', 'none', 'important');
      });
    } else {
      document.querySelectorAll('a[href="/i/chat"], a[href="/messages"], [data-testid="AppTabBar_DirectMessage_Link"], [data-testid="DMDrawer"]').forEach(el => {
        el.style.removeProperty('display');
      });
    }

    // Audio & Video Calls failsafe
    if (currentSettings.hide_calls) {
      document.querySelectorAll('[data-testid="callButton"], button[aria-label*="call" i], button[aria-label*="Call" i]').forEach(el => {
        el.style.setProperty('display', 'none', 'important');
      });
    } else {
      document.querySelectorAll('[data-testid="callButton"], button[aria-label*="call" i], button[aria-label*="Call" i]').forEach(el => {
        el.style.removeProperty('display');
      });
    }

    // Search History & Recent Searches failsafe
    if (currentSettings.hide_history) {
      document.querySelectorAll('[data-testid="typeaheadRecentSearchesItem"], [data-testid="typeaheadRecentSearchesClear"]').forEach(el => {
        el.style.setProperty('display', 'none', 'important');
      });
    } else {
      document.querySelectorAll('[data-testid="typeaheadRecentSearchesItem"], [data-testid="typeaheadRecentSearchesClear"]').forEach(el => {
        el.style.removeProperty('display');
      });
    }

    // Clean up any residual styles on sidebar/header if previously set
    document.querySelectorAll('[data-testid="sidebarColumn" i], [role="complementary"], header[role="banner"], [data-testid="primaryColumn"]').forEach(el => {
      el.style.removeProperty('display');
      el.style.removeProperty('visibility');
      el.style.removeProperty('width');
      el.style.removeProperty('min-width');
      el.style.removeProperty('max-width');
      el.style.removeProperty('flex-grow');
      el.style.removeProperty('margin');
    });
  }

  function applySettings(settings) {
    currentSettings = { ...DEFAULT_SETTINGS, ...settings };
    if (!styleEl || !styleEl.isConnected) {
      styleEl = document.getElementById(STYLE_ID) || document.createElement("style");
      styleEl.id = STYLE_ID;
      (document.documentElement || document.head).appendChild(styleEl);
    }
    styleEl.textContent = compileCSS(currentSettings);
    cleanDOMElements();
  }

  // Live MutationObserver for dynamically loaded Twitter timeline chunks
  const domObserver = new MutationObserver(() => {
    cleanDOMElements();
  });

  if (document.body) {
    domObserver.observe(document.body, { childList: true, subtree: true });
  } else {
    document.addEventListener("DOMContentLoaded", () => {
      domObserver.observe(document.body, { childList: true, subtree: true });
      cleanDOMElements();
    });
  }

  // Initial load
  chrome.storage.sync.get(DEFAULT_SETTINGS, (items) => {
    applySettings(items);
  });

  // Listen for storage updates in real-time
  chrome.storage.onChanged.addListener((changes, areaName) => {
    if (areaName === "sync") {
      const updated = { ...currentSettings };
      for (const [key, change] of Object.entries(changes)) {
        updated[key] = change.newValue;
      }
      applySettings(updated);
    }
  });

  // ==========================================
  // TACTICAL CROSSHAIR / TARGET PICKER MODE
  // ==========================================
  let isPickerActive = false;
  let hoveredElement = null;
  let hudEl = null;

  function createHUD() {
    if (hudEl) return hudEl;
    hudEl = document.createElement("div");
    hudEl.id = "sicario-picker-hud";
    hudEl.style.display = "none";
    hudEl.innerHTML = `
      <span class="hud-badge">TARGET</span>
      <span class="hud-selector" id="sicario-hud-selector">Ready</span>
      <span style="opacity: 0.6; font-size: 10px;">(Click: Eliminate | ESC: Cancel)</span>
    `;
    document.documentElement.appendChild(hudEl);
    return hudEl;
  }

  function getBestSelector(el) {
    if (!el || el === document.body || el === document.documentElement) return null;

    // Check for major section card containers first (Trends, Who to Follow)
    const trendParent = el.closest('[aria-label="Timeline: Trending now"]');
    if (trendParent) {
      return '[aria-label="Timeline: Trending now"]';
    }

    const followParent = el.closest('[aria-label="Who to follow"]');
    if (followParent) {
      return '[aria-label="Who to follow"]';
    }

    // 1. Check data-testid directly or on close wrapper
    if (el.getAttribute("data-testid")) {
      return `[data-testid="${el.getAttribute("data-testid")}"]`;
    }

    // 2. Check aria-label
    if (el.getAttribute("aria-label")) {
      return `[aria-label="${el.getAttribute("aria-label").replace(/"/g, '\\"')}"]`;
    }

    // 3. Check for specific navigation link
    if (el.tagName === "A" && el.getAttribute("href")) {
      const href = el.getAttribute("href");
      if (href.startsWith("/")) {
        return `a[href="${href}"]`;
      }
    }

    // 4. Check parent with data-testid (often SVGs or text spans inside a widget)
    const testIdParent = el.closest("[data-testid]");
    if (testIdParent && testIdParent !== document.body) {
      return `[data-testid="${testIdParent.getAttribute("data-testid")}"]`;
    }

    // 5. Check role
    const roleParent = el.closest("[role='complementary'], [role='region'], aside, section, nav");
    if (roleParent) {
      const role = roleParent.getAttribute("role");
      const aria = roleParent.getAttribute("aria-label");
      if (aria) {
        return `${roleParent.tagName.toLowerCase()}[aria-label="${aria.replace(/"/g, '\\"')}"]`;
      }
      if (role) {
        return `${roleParent.tagName.toLowerCase()}[role="${role}"]`;
      }
    }

    // 6. ID
    if (el.id) {
      return `#${el.id}`;
    }

    // 7. Structural fallback
    const tag = el.tagName.toLowerCase();
    if (el.className && typeof el.className === "string") {
      const validClass = el.className.split(/\s+/).find(c => c && !c.includes("sicario") && !c.startsWith("r-"));
      if (validClass) return `${tag}.${validClass}`;
    }

    return tag;
  }

  function handleMouseMove(e) {
    if (!isPickerActive) return;

    const el = document.elementFromPoint(e.clientX, e.clientY);
    if (!el || el.closest("#sicario-picker-hud") || el.closest("#sicario-toast")) return;

    if (hoveredElement !== el) {
      if (hoveredElement) {
        hoveredElement.classList.remove("sicario-highlighted-element");
      }
      hoveredElement = el;
      hoveredElement.classList.add("sicario-highlighted-element");

      const selector = getBestSelector(el) || "Element";
      const hud = createHUD();
      const selectorText = document.getElementById("sicario-hud-selector");
      if (selectorText) selectorText.textContent = selector;

      hud.style.display = "flex";
      hud.style.left = `${Math.min(window.innerWidth - 320, e.clientX + 16)}px`;
      hud.style.top = `${Math.min(window.innerHeight - 60, e.clientY + 16)}px`;
    }
  }

  function handleClick(e) {
    if (!isPickerActive) return;

    e.preventDefault();
    e.stopPropagation();

    const targetEl = hoveredElement || e.target;
    const selector = getBestSelector(targetEl);

    if (selector) {
      eliminateSelector(selector, targetEl.tagName.toLowerCase());
    }

    stopPicker();
  }

  function handleKeyDown(e) {
    if (e.key === "Escape" && isPickerActive) {
      stopPicker();
    }
  }

  function startPicker() {
    isPickerActive = true;
    document.documentElement.classList.add("sicario-picker-active");
    createHUD();

    window.addEventListener("mousemove", handleMouseMove, true);
    window.addEventListener("click", handleClick, true);
    window.addEventListener("keydown", handleKeyDown, true);
  }

  function stopPicker() {
    isPickerActive = false;
    document.documentElement.classList.remove("sicario-picker-active");
    if (hoveredElement) {
      hoveredElement.classList.remove("sicario-highlighted-element");
      hoveredElement = null;
    }
    if (hudEl) {
      hudEl.style.display = "none";
    }

    window.removeEventListener("mousemove", handleMouseMove, true);
    window.removeEventListener("click", handleClick, true);
    window.removeEventListener("keydown", handleKeyDown, true);
  }

  function showToast(message) {
    const existing = document.getElementById("sicario-toast");
    if (existing) existing.remove();

    const toast = document.createElement("div");
    toast.id = "sicario-toast";
    toast.innerHTML = `
      <span style="font-size: 15px;">🎯</span>
      <span>${message}</span>
    `;
    document.documentElement.appendChild(toast);
    setTimeout(() => {
      if (toast && toast.parentNode) {
        toast.style.opacity = "0";
        toast.style.transition = "opacity 0.25s ease";
        setTimeout(() => toast.remove(), 250);
      }
    }, 3000);
  }

  function eliminateSelector(selector, label) {
    chrome.storage.sync.get({ custom_selectors: [] }, (res) => {
      const list = res.custom_selectors || [];
      const exists = list.some(item => (typeof item === "string" ? item : item.selector) === selector);
      if (!exists) {
        list.push({
          selector: selector,
          label: label || "Custom Element",
          date: new Date().toISOString()
        });
        chrome.storage.sync.set({ custom_selectors: list }, () => {
          showToast(`Eliminated target: <code style="color: #00E599;">${selector}</code>`);
        });
      } else {
        showToast(`Target already eliminated: <code style="color: #00E599;">${selector}</code>`);
      }
    });
  }

  // Listen for messages from popup
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "SETTINGS_UPDATED" && request.settings) {
      applySettings(request.settings);
      sendResponse({ status: "SETTINGS_APPLIED" });
    } else if (request.action === "START_PICKER") {
      startPicker();
      sendResponse({ status: "PICKER_STARTED" });
    } else if (request.action === "STOP_PICKER") {
      stopPicker();
      sendResponse({ status: "PICKER_STOPPED" });
    }
    return true;
  });

})();
