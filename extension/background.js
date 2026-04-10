chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg?.type === 'MARK_FORWARD_TO_TAB') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const tab = tabs[0];
      if (!tab?.id) return sendResponse({ ok: false });
      chrome.tabs.sendMessage(tab.id, msg.payload, (resp) => sendResponse(resp || { ok: false }));
    });
    return true;
  }
});
