import { FormEvent, useEffect, useState } from "react";
import "./theme.css";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8787";

type Source = { url: string; title?: string; citation?: string };
type Claim = { id: string; text: string; source_urls?: string[] };
type Evidence = { claims?: Claim[]; sources?: Source[] };
type RunResult = {
  id: string;
  status: string;
  summary: string;
  evidence?: Evidence | null;
  model_events?: { message: string; [key: string]: unknown }[];
};

export default function App() {
  const [task, setTask] = useState("Fix the failing test in the sample project");
  const [log, setLog] = useState("Waiting for a run.\n");
  const [busy, setBusy] = useState(false);
  const [evidence, setEvidence] = useState<Evidence | null>(null);
  const [nemotronReady, setNemotronReady] = useState<boolean | null>(null);

  async function refreshHealth() {
    try {
      const res = await fetch(`${API_URL}/health`);
      const json = await res.json();
      setNemotronReady(Boolean(json.nemotron_configured));
    } catch {
      setNemotronReady(null);
    }
  }

  useEffect(() => {
    refreshHealth();
  }, []);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setEvidence(null);
    setLog((prev) => prev + `\n> ${task}\n`);
    try {
      const res = await fetch(`${API_URL}/runs`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task }),
      });
      const json = (await res.json()) as RunResult;
      setEvidence(json.evidence ?? null);
      const lines =
        json.model_events?.map((ev) => `${ev.message}${ev.tier ? ` (${ev.tier})` : ""}`) ?? [];
      setLog(
        (prev) =>
          prev +
          lines.join("\n") +
          `\n\nStatus: ${json.status}\n\n${json.summary}\n`,
      );
    } catch (err) {
      setLog((prev) => prev + `Error: ${String(err)}\n`);
    } finally {
      setBusy(false);
      refreshHealth();
    }
  }

  return (
    <div className="appShell">
      <header className="hero">
        <h1>GroundTruth</h1>
        <p>
          Research with citations, patch with Nemotron on Nebius Token Factory, prove with tests.
        </p>
        {nemotronReady === false && (
          <p style={{ marginTop: "0.75rem", fontSize: "0.95rem" }}>
            Nemotron pending Token Factory access. Tavily and tests run in fallback mode on the
            sample project.
          </p>
        )}
      </header>

      <main className="layout">
        <section className="panel">
          <span className="badge">Nemotron routing</span>
          <h2>Run</h2>
          <form className="taskForm" onSubmit={onSubmit}>
            <textarea
              value={task}
              onChange={(ev) => setTask(ev.target.value)}
              aria-label="Task"
            />
            <button className="btnPrimary" type="submit" disabled={busy}>
              {busy ? "Running…" : "Run agent"}
            </button>
          </form>
          <h2 style={{ marginTop: "1.5rem" }}>Log</h2>
          <div className="log">{log}</div>
        </section>

        <aside className="panel">
          <span className="badge">Tavily evidence</span>
          <h2>Sources</h2>
          {!evidence && (
            <p className="evidenceEmpty">Run a task to load Tavily claims and sources here.</p>
          )}
          {evidence?.claims?.map((claim) => (
            <div key={claim.id} style={{ marginBottom: "1rem" }}>
              <strong>[{claim.id}]</strong> {claim.text.slice(0, 280)}
              {claim.text.length > 280 ? "…" : ""}
            </div>
          ))}
          <ul style={{ paddingLeft: "1.1rem", margin: 0 }}>
            {evidence?.sources?.map((s) => (
              <li key={s.url} style={{ marginBottom: "0.5rem" }}>
                <a href={s.url} target="_blank" rel="noreferrer">
                  {s.title || s.url}
                </a>
              </li>
            ))}
          </ul>
        </aside>
      </main>

      <footer className="footer">Nebius x NVIDIA Global AI Hackathon · MIT</footer>
    </div>
  );
}
