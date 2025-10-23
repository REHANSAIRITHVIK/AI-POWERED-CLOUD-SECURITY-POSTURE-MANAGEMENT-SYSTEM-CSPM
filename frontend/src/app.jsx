import React, { useEffect, useState } from "react";
import { getFindings, scanResources, remediate } from "./api";

const sample = [
  {"cloud_provider":"aws","resource_type":"s3","resource_id":"bucket-photos-public","config":{"type":"s3","acl":"public-read","encryption":false,"versioning":false}},
  {"cloud_provider":"aws","resource_type":"ec2","resource_id":"web-server-1","config":{"type":"vm","open_ports":[22,80],"public_ip":true,"os":"linux"}}
];

export default function App() {
  const [findings, setFindings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [payload, setPayload] = useState(JSON.stringify(sample, null, 2));

  async function load() {
    setLoading(true);
    try {
      const f = await getFindings();
      setFindings(f);
    } finally { setLoading(false); }
  }

  useEffect(() => { load(); }, []);

  async function handleScan() {
    let parsed;
    try {
      parsed = JSON.parse(payload);
    } catch (e) {
      alert("Invalid JSON payload");
      return;
    }
    setLoading(true);
    try {
      await scanResources(parsed);
      await load();
    } catch (e) {
      alert("Scan failed: " + e.message);
    } finally { setLoading(false); }
  }

  async function handleRemediate(id) {
    setLoading(true);
    try {
      await remediate(id);
      await load();
    } finally { setLoading(false); }
  }

  return (
    <div className="container">
      <div className="header">
        <div>
          <h1 style={{margin:0}}>AI-Powered CSPM</h1>
          <div className="small">Scan cloud resources, view risk findings, remediate</div>
        </div>
        <div className="controls">
          <button className="button" onClick={load}>Refresh</button>
        </div>
      </div>

      <div style={{display:"grid", gridTemplateColumns:"1fr 420px", gap:16}}>
        <div>
          <h3 style={{marginTop:0}}>Findings</h3>
          {loading ? <div className="small">Loading...</div> : null}
          <table className="findings-table" aria-live="polite">
            <thead>
              <tr><th>Title</th><th>Severity</th><th>Score</th><th>Remedied</th><th></th></tr>
            </thead>
            <tbody>
              {findings.length === 0 && <tr><td colSpan="5" className="small">No findings yet.</td></tr>}
              {findings.map(f => (
                <tr key={f.id}>
                  <td>
                    <div style={{fontWeight:700}}>{f.title}</div>
                    <div className="small">{f.description}</div>
                  </td>
                  <td>
                    <span className={`badge ${f.severity.toLowerCase()==="high"?"high":f.severity.toLowerCase()==="medium"?"medium":"low"}`}>
                      {f.severity}
                    </span>
                  </td>
                  <td>{(f.risk_score || 0).toFixed(2)}</td>
                  <td>{f.remedied ? "✅" : "—"}</td>
                  <td>
                    {!f.remedied ? <button className="button secondary" onClick={()=>handleRemediate(f.id)}>Mark Remedied</button>: null}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div>
          <h3>Scan Payload (JSON)</h3>
          <textarea value={payload} onChange={(e)=>setPayload(e.target.value)} />
          <div style={{display:"flex", gap:10, marginTop:8}}>
            <button className="button" onClick={handleScan}>Run Scan</button>
            <button className="button secondary" onClick={()=>setPayload(JSON.stringify(sample, null, 2))}>Load Sample</button>
          </div>

          <div style={{marginTop:18}}>
            <h4 style={{marginBottom:6}}>How to use</h4>
            <div className="small">Paste a JSON array of resource objects and click <strong>Run Scan</strong>.</div>
            <div className="small" style={{marginTop:6}}>Example resource: <code>{"{cloud_provider:'aws',resource_type:'s3',resource_id:'b1',config:{...}}"}</code></div>
          </div>
        </div>
      </div>
    </div>
  );
}
