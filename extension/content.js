const BACKEND_URL = localStorage.getItem('markBackendUrl') || 'http://127.0.0.1:8787';

function collectMessages() {
  const nodes = document.querySelectorAll('[data-testid="msg-container"]');
  const out = [];
  nodes.forEach((node) => {
    const text = node.innerText || '';
    if (!text.trim()) return;
    out.push({ text, timestamp: new Date().toISOString(), groupName: document.title });
  });
  return out.slice(-10);
}

async function pushMessages() {
  const messages = collectMessages();
  if (!messages.length) return;
  try {
    await fetch(`${BACKEND_URL}/api/integrations/whatsapp-intake`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source: 'extension', messages })
    });
  } catch (e) {}
}

function sendReply(text) {
  const box = document.querySelector('[contenteditable="true"][data-tab]');
  if (!box) return false;
  box.focus();
  document.execCommand('insertText', false, text);
  const sendBtn = document.querySelector('[data-testid="send"]');
  if (sendBtn) { sendBtn.click(); return true; }
  return false;
}

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg?.type === 'MARK_SEND_WHATSAPP') {
    const ok = sendReply(msg.text || '');
    sendResponse({ ok });
  }
  if (msg?.type === 'MARK_SCAN') {
    sendResponse({ messages: collectMessages() });
  }
  return true;
});

setInterval(pushMessages, 15000);
