let token = localStorage.getItem("token") || "";
const headers = () => ({"Content-Type":"application/json", ...(token ? {"Authorization": `Bearer ${token}`} : {})});
async function login(){ const r = await fetch('/api/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:username.value,password:password.value})}); const d=await r.json(); if(d.token){ token=d.token; localStorage.setItem('token', token); loginStatus.innerText='Logged in'; await refreshAll(); } else { loginStatus.innerText='Login failed'; }}
async function refreshAll(){
  const [s,f,d,a,w,dev,rt,cmds] = await Promise.all([
    fetch('/api/dashboard/summary',{headers:headers()}),
    fetch('/api/dashboard/financials',{headers:headers()}),
    fetch('/api/dashboard/drafts',{headers:headers()}),
    fetch('/api/dashboard/approvals',{headers:headers()}),
    fetch('/api/workers',{headers:headers()}),
    fetch('/api/devices',{headers:headers()}),
    fetch('/api/dashboard/runtime',{headers:headers()}),
    fetch('/api/dashboard/commands',{headers:headers()})
  ]);
  summary.textContent = JSON.stringify(await s.json(), null, 2);
  financials.textContent = JSON.stringify(await f.json(), null, 2);
  runtime.textContent = JSON.stringify(await rt.json(), null, 2);
  commands.textContent = JSON.stringify(await cmds.json(), null, 2);
  const draftsData = await d.json();
  drafts.innerHTML = draftsData.map(x => `<div class="draft"><h3>${x.title}</h3><p><b>Status:</b> ${x.status}</p><p><b>Location:</b> ${x.location}</p><p><b>Confidence:</b> ${(x.evaluation||{}).confidence ?? 'n/a'}</p><p><b>Issues:</b> ${((x.evaluation||{}).issues||[]).join('; ')}</p><p><b>Runtime:</b> ${x.runtime_note || ''}</p><pre>${x.final_output || x.draft_output || ''}</pre><p><b>Value:</b> $${x.estimated_value_usd||0} / ${x.estimated_time_saved_minutes||0} min</p></div>`).join('');
  const approvalsData = await a.json();
  approvals.innerHTML = approvalsData.map(x => `<div class="draft"><h3>#${x.id} ${x.summary}</h3><p>Status: ${x.status}</p><button onclick="approvalAction(${x.id}, 'approved')">Approve & Run</button><button onclick="approvalAction(${x.id}, 'rejected')">Reject</button></div>`).join('');
  workers.textContent = JSON.stringify(await w.json(), null, 2);
  devices.textContent = JSON.stringify(await dev.json(), null, 2);
}
async function createTask(){
 const r = await fetch('/api/tasks',{method:'POST',headers:headers(),body:JSON.stringify({title:taskTitle.value,description:taskDescription.value,requires_online:requiresOnline.checked,requires_worker:requiresWorker.checked})});
 const d = await r.json(); await refreshAll(); alert(`Draft task created: #${d.id}`);
}
async function approvalAction(id, status){
 await fetch(`/api/approvals/${id}`,{method:'POST',headers:headers(),body:JSON.stringify({status, response_note:''})}); await refreshAll();
}
if(token) refreshAll();
setInterval(()=>{ if(token) refreshAll(); }, 15000);
