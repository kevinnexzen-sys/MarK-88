const input = document.getElementById("api");
chrome.storage.local.get(["mark_api_url"]).then((r) => { input.value = r.mark_api_url || "http://127.0.0.1:8787"; });
document.getElementById("save").onclick = async () => {
  await chrome.storage.local.set({ mark_api_url: input.value });
  alert("Saved");
};
