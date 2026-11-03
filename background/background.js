/**
 * SICARIO — Background Service Worker
 */

chrome.runtime.onInstalled.addListener((details) => {
  const DEFAULT_SETTINGS = {
    master_active: true,
    theme: "sicario", // sicario, middle_out, batman, reacher, pitchers
    hide_right_sidebar: true,
    hide_left_nav: false,
    hide_whats_happening: true,
    hide_todays_news: true,
    hide_who_to_follow: true,
    hide_grok: true,
    hide_premium_promos: true,
    hide_view_counts: true,
    hide_explore_tab: false,
    custom_selectors: []
  };

  chrome.storage.sync.get(null, (existing) => {
    if (!existing || Object.keys(existing).length === 0) {
      chrome.storage.sync.set(DEFAULT_SETTINGS);
    }
  });

  // Set initial badge
  updateBadge(true);
});

function updateBadge(active) {
  if (active) {
    chrome.action.setBadgeText({ text: "ON" });
    chrome.action.setBadgeBackgroundColor({ color: "#FF1744" });
  } else {
    chrome.action.setBadgeText({ text: "OFF" });
    chrome.action.setBadgeBackgroundColor({ color: "#666666" });
  }
}

chrome.storage.onChanged.addListener((changes, area) => {
  if (area === "sync" && changes.master_active !== undefined) {
    updateBadge(changes.master_active.newValue);
  }
});
