/**
 * SICARIO — Chrome Extension Popup Logic
 * Material Design 3 + Expandable Panels + Single Noise Shield Toggle
 */

document.addEventListener("DOMContentLoaded", () => {
  const THEME_DATA = {
    sicario: {
      title: "SICARIO",
      tagline: '"Plata o Plomo. Eliminate UI without mercy."'
    },
    middle_out: {
      title: "MIDDLE-OUT",
      tagline: '"Lossless Twitter compression. 5.2 Weissman."'
    },
    batman: {
      title: "DARK KNIGHT",
      tagline: '"Purging the shadows of X."'
    },
    reacher: {
      title: "REACHER",
      tagline: '"Details matter. Zero baggage."'
    },
    pitchers: {
      title: "TU BEER HAI",
      tagline: '"Tu content hai! Flow kar, glass ko ignore kar."'
    }
  };

  // Noise keys grouped under "Hide All Noise"
  const NOISE_KEYS = [
    "hide_whats_happening",
    "hide_todays_news",
    "hide_who_to_follow",
    "hide_notifications",
    "hide_chats",
    "hide_calls",
    "hide_history",
    "hide_grok",
    "hide_premium_promos",
    "hide_view_counts"
  ];

  // All granular toggle keys
  const TOGGLE_KEYS = [
    "hide_whats_happening",
    "hide_todays_news",
    "hide_who_to_follow",
    "hide_notifications",
    "hide_chats",
    "hide_calls",
    "hide_history",
    "hide_grok",
    "hide_premium_promos",
    "hide_view_counts",
    "hide_explore_tab"
  ];

  const DEFAULT_SETTINGS = {
    master_active: true,
    theme: "sicario",
    hide_whats_happening: true,
    hide_todays_news: true,
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

  // DOM Elements
  const masterToggle = document.getElementById("master-toggle");
  const masterStatus = document.getElementById("master-status");
  const displayTitle = document.getElementById("display-title");
  const displayTagline = document.getElementById("display-tagline");
  const themeButtons = document.querySelectorAll(".m3-segment-btn, .theme-btn");
  const hideAllNoiseToggle = document.getElementById("hide_all_noise");
  const startPickerBtn = document.getElementById("start-picker-btn");
  const activeCountBadge = document.getElementById("active-count-badge");
  const customSelectorInput = document.getElementById("custom-selector-input");
  const addCustomBtn = document.getElementById("add-custom-btn");
  const customRulesList = document.getElementById("custom-rules-list");
  const customCountBadge = document.getElementById("custom-count-badge");
  const resetDefaultsBtn = document.getElementById("reset-defaults-btn");

  // Accordion Elements
  const granularTrigger = document.getElementById("granular-accordion-trigger");
  const granularCollapse = document.getElementById("granular-accordion-collapse");
  const granularCard = document.getElementById("granular-accordion");

  const customTrigger = document.getElementById("custom-accordion-trigger");
  const customCollapse = document.getElementById("custom-accordion-collapse");
  const customCard = document.getElementById("custom-accordion");

  let currentSettings = { ...DEFAULT_SETTINGS };

  // Set Theme UI
  function applyThemeUI(themeKey) {
    const data = THEME_DATA[themeKey] || THEME_DATA.sicario;
    document.body.setAttribute("data-theme", themeKey);
    displayTitle.textContent = data.title;
    displayTagline.textContent = data.tagline;

    themeButtons.forEach(btn => {
      btn.classList.toggle("active", btn.dataset.theme === themeKey);
    });
  }

  // Update Active Counts and Noise Toggle State
  function syncNoiseState() {
    let activeCount = 0;
    TOGGLE_KEYS.forEach(key => {
      if (currentSettings[key]) activeCount++;
    });

    if (activeCountBadge) {
      activeCountBadge.textContent = `${activeCount} ACTIVE`;
    }

    // Check if any primary noise key is active
    const anyNoiseActive = NOISE_KEYS.some(key => currentSettings[key]);
    if (hideAllNoiseToggle) {
      hideAllNoiseToggle.checked = anyNoiseActive;
    }
  }

  // Setup Accordion Toggle Logic
  function setupAccordion(trigger, collapse, card) {
    if (!trigger || !collapse || !card) return;

    trigger.addEventListener("click", () => {
      const isExpanded = trigger.getAttribute("aria-expanded") === "true";
      const nextState = !isExpanded;

      trigger.setAttribute("aria-expanded", String(nextState));
      collapse.classList.toggle("open", nextState);
      card.classList.toggle("is-expanded", nextState);

      if (nextState) {
        setTimeout(() => {
          card.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }, 120);
      }
    });
  }

  setupAccordion(granularTrigger, granularCollapse, granularCard);
  setupAccordion(customTrigger, customCollapse, customCard);

  // Render Custom Rules List
  function renderCustomRules(list) {
    customRulesList.innerHTML = "";
    customCountBadge.textContent = `${list.length} ${list.length === 1 ? "RULE" : "RULES"}`;

    if (!list || list.length === 0) {
      customRulesList.innerHTML = `<div class="m3-empty-state">No custom rules yet. Point & click or type a selector above.</div>`;
      return;
    }

    list.forEach((item, index) => {
      const selector = typeof item === "string" ? item : item.selector;

      const row = document.createElement("div");
      row.className = "m3-chip";
      row.innerHTML = `
        <span class="m3-chip-text" title="${selector}">${selector}</span>
        <button class="m3-chip-delete" data-index="${index}" title="Restore this element">✕</button>
      `;
      customRulesList.appendChild(row);
    });

    // Attach delete listeners
    customRulesList.querySelectorAll(".m3-chip-delete").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const idx = parseInt(e.currentTarget.dataset.index, 10);
        deleteCustomRule(idx);
      });
    });
  }

  function deleteCustomRule(index) {
    const list = [...(currentSettings.custom_selectors || [])];
    if (index >= 0 && index < list.length) {
      list.splice(index, 1);
      chrome.storage.sync.set({ custom_selectors: list }, () => {
        currentSettings.custom_selectors = list;
        renderCustomRules(list);
      });
    }
  }

  function addCustomRule(selector) {
    if (!selector || selector.trim().length === 0) return;
    const cleanSel = selector.trim();
    const list = [...(currentSettings.custom_selectors || [])];

    const exists = list.some(item => (typeof item === "string" ? item : item.selector) === cleanSel);
    if (!exists) {
      list.push({
        selector: cleanSel,
        label: "Manual Rule",
        date: new Date().toISOString()
      });
      chrome.storage.sync.set({ custom_selectors: list }, () => {
        currentSettings.custom_selectors = list;
        renderCustomRules(list);
        customSelectorInput.value = "";
      });
    }
  }

  // Load Initial Settings
  chrome.storage.sync.get(DEFAULT_SETTINGS, (items) => {
    currentSettings = { ...DEFAULT_SETTINGS, ...items };

    // Master Switch
    masterToggle.checked = currentSettings.master_active;
    masterStatus.textContent = currentSettings.master_active ? "ON" : "OFF";

    // Theme
    applyThemeUI(currentSettings.theme || "sicario");

    // Presets
    TOGGLE_KEYS.forEach(key => {
      const el = document.getElementById(key);
      if (el) {
        el.checked = !!currentSettings[key];
      }
    });

    // Sync Noise state & count badge
    syncNoiseState();

    // Custom Rules
    renderCustomRules(currentSettings.custom_selectors || []);
  });

  // Live Broadcast to open Twitter tabs for zero-delay instant updates
  function broadcastSettings(newSettings) {
    chrome.tabs.query({}, (tabs) => {
      if (tabs && tabs.length > 0) {
        tabs.forEach(tab => {
          const url = tab.url || "";
          if (url.includes("twitter.com") || url.includes("x.com")) {
            chrome.tabs.sendMessage(tab.id, { action: "SETTINGS_UPDATED", settings: newSettings }, () => {
              if (chrome.runtime.lastError) { /* ignore tabs without content script */ }
            });
          }
        });
      }
    });
  }

  // Master Switch Change
  masterToggle.addEventListener("change", (e) => {
    const active = e.target.checked;
    masterStatus.textContent = active ? "ON" : "OFF";
    currentSettings.master_active = active;
    chrome.storage.sync.set({ master_active: active }, () => {
      broadcastSettings(currentSettings);
    });
  });

  // ONE TOGGLE TO HIDE NOISE
  if (hideAllNoiseToggle) {
    hideAllNoiseToggle.addEventListener("change", (e) => {
      const active = e.target.checked;
      const updates = {};

      NOISE_KEYS.forEach(key => {
        updates[key] = active;
        currentSettings[key] = active;
        const el = document.getElementById(key);
        if (el) el.checked = active;
      });

      chrome.storage.sync.set(updates, () => {
        syncNoiseState();
        broadcastSettings(currentSettings);
      });
    });
  }

  // Theme Button Clicks
  themeButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const themeKey = btn.dataset.theme;
      applyThemeUI(themeKey);
      currentSettings.theme = themeKey;
      chrome.storage.sync.set({ theme: themeKey }, () => {
        broadcastSettings(currentSettings);
      });
    });
  });

  // Granular Presets Change (Includes Right Sidebar Entirely)
  TOGGLE_KEYS.forEach(key => {
    const el = document.getElementById(key);
    if (el) {
      el.addEventListener("change", (e) => {
        const update = {};
        update[key] = e.target.checked;
        currentSettings[key] = e.target.checked;
        chrome.storage.sync.set(update, () => {
          syncNoiseState();
          broadcastSettings(currentSettings);
        });
      });
    }
  });

  // Add Custom Rule Button
  addCustomBtn.addEventListener("click", () => {
    addCustomRule(customSelectorInput.value);
  });

  customSelectorInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      addCustomRule(customSelectorInput.value);
    }
  });

  // Start Picker (Point & Click)
  startPickerBtn.addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs && tabs[0]) {
        const activeTab = tabs[0];
        const url = activeTab.url || "";
        if (url.includes("twitter.com") || url.includes("x.com")) {
          chrome.tabs.sendMessage(activeTab.id, { action: "START_PICKER" }, () => {
            window.close(); // Close popup so user can target elements
          });
        } else {
          alert("Please navigate to twitter.com or x.com to use the Point & Click element eliminator!");
        }
      }
    });
  });

  // Reset to Defaults
  resetDefaultsBtn.addEventListener("click", () => {
    if (confirm("Reset all Sicario settings and rules to default?")) {
      chrome.storage.sync.set(DEFAULT_SETTINGS, () => {
        window.location.reload();
      });
    }
  });
});
