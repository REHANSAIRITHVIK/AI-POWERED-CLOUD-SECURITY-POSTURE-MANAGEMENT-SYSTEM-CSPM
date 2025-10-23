const API = import.meta.env.VITE_API || "http://localhost:8000"

export async function getFindings() {
  const r = await fetch(`${API}/findings`);
  return await r.json();
}

export async function scanResources(resources) {
  const r = await fetch(`${API}/scan`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(resources)
  });
  return await r.json();
}

export async function remediate(id) {
  const r = await fetch(`${API}/remediate/${id}`, { method: "POST" });
  return await r.json();
}
