import { useState } from "react";
import "./App.css";

export default function App() {
  const API = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8001";
  const [text, setText] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const save = async (e) => {
    e.preventDefault();
    const payload = text.trim();
    if (!payload) return;
    setLoading(true);
    setStatus("");
    try {
      const res = await fetch(`${API}/items`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: payload }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }
      const data = await res.json();
      setStatus(`✅ Saved! id=${data.id}`);
      setText("");
    } catch (err) {
      setStatus(`❌ ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 560, margin: "3rem auto", fontFamily: "system-ui" }}>
      <h1>Microservice Demo</h1>
      <form onSubmit={save}>
        <label htmlFor="text">Enter something to save:</label>
        <textarea
          id="text"
          rows={4}
          style={{ width: "100%", marginTop: 8 }}
          placeholder="Hello, database!"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button
          type="submit"
          disabled={loading || !text.trim()}
          style={{ marginTop: 10, padding: "8px 14px" }}
        >
          {loading ? "Saving..." : "Save"}
        </button>
      </form>
      {status && <p style={{ marginTop: 10 }}>{status}</p>}
      <p style={{ color: "#666", marginTop: 16, fontSize: 12 }}>
        Using API: {API}
      </p>
    </div>
  );
}
