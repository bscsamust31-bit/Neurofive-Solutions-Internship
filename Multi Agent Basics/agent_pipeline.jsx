import { useState } from "react";
import { PenLine, Wand2, ArrowRight, Loader2, CheckCircle2 } from "lucide-react";

const FONT_IMPORT = `@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap');`;

const PALETTE = {
  paper: "#f7f5ee",
  card: "#fffdf9",
  ink: "#1c1c18",
  inkSoft: "#5c5a51",
  deep: "#123825",
  deepDark: "#0b2117",
  gold: "#c9a24b",
  goldSoft: "#e4cd8f",
  editorBlue: "#3c6e91",
  editorBlueSoft: "#dce9ef",
  line: "#dfdac9",
};

const TOPICS = [
  { id: "remote", label: "Why remote work is here to stay" },
  { id: "photosynthesis", label: "How photosynthesis works" },
];

const WRITER_SYSTEM =
  "You are the Writer agent in a two-agent content pipeline. Your job is to produce a solid FIRST DRAFT on the given topic — clear ideas, reasonable structure, roughly 120-180 words. Don't over-polish; focus on getting the substance right. Write in plain prose, no headers.";

const EDITOR_SYSTEM =
  "You are the Editor/Critic agent in a two-agent content pipeline. You receive a draft written by the Writer agent. Improve it: tighten language, strengthen the opening and closing, fix weak transitions, cut redundancy, improve structure — without changing the core facts or claims. " +
  "Respond with ONLY valid JSON, no markdown fences, no preamble, in this exact shape: " +
  '{"revised": "the improved version as plain prose", "notes": ["short bullet describing one specific change", "another short bullet", "a third short bullet"]}';

async function callAgent(system, userContent) {
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "claude-sonnet-4-6",
      max_tokens: 1000,
      system,
      messages: [{ role: "user", content: userContent }],
    }),
  });
  const data = await response.json();
  return (data.content || [])
    .map((b) => (b.type === "text" ? b.text : ""))
    .filter(Boolean)
    .join("\n");
}

export default function AgentPipeline() {
  const [topicId, setTopicId] = useState(TOPICS[0].id);
  const [customTopic, setCustomTopic] = useState("");
  const [stage, setStage] = useState("idle"); // idle | writing | editing | done | error
  const [draft, setDraft] = useState("");
  const [finalText, setFinalText] = useState("");
  const [notes, setNotes] = useState([]);
  const [tab, setTab] = useState("final");
  const [error, setError] = useState("");

  const activeTopic =
    customTopic.trim() || TOPICS.find((t) => t.id === topicId)?.label || "";

  async function runPipeline() {
    if (!activeTopic) return;
    setError("");
    setDraft("");
    setFinalText("");
    setNotes([]);
    setTab("final");
    setStage("writing");

    try {
      const writerOutput = await callAgent(
        WRITER_SYSTEM,
        `Topic: ${activeTopic}`
      );
      setDraft(writerOutput);
      setStage("editing");

      const editorRaw = await callAgent(
        EDITOR_SYSTEM,
        `Here is the Writer agent's draft:\n\n${writerOutput}`
      );
      const cleaned = editorRaw.replace(/```json|```/g, "").trim();
      let parsed;
      try {
        parsed = JSON.parse(cleaned);
      } catch {
        parsed = { revised: editorRaw, notes: [] };
      }
      setFinalText(parsed.revised || editorRaw);
      setNotes(Array.isArray(parsed.notes) ? parsed.notes : []);
      setStage("done");
    } catch (e) {
      setError("The pipeline hit an error. Please try again.");
      setStage("error");
    }
  }

  const isBusy = stage === "writing" || stage === "editing";

  return (
    <div
      style={{
        fontFamily: "'Inter', sans-serif",
        background: `radial-gradient(1200px 500px at 10% -10%, #16432a 0%, ${PALETTE.deepDark} 55%)`,
        minHeight: "100%",
        color: PALETTE.ink,
      }}
    >
      <style>{FONT_IMPORT}</style>

      {/* Header */}
      <div style={{ padding: "36px 32px 26px 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
          <div
            style={{
              width: 30,
              height: 30,
              borderRadius: "50%",
              border: `1.5px solid ${PALETTE.gold}`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontFamily: "'IBM Plex Mono', monospace",
              fontSize: 12,
              fontWeight: 600,
              color: PALETTE.goldSoft,
            }}
          >
            N5
          </div>
          <span
            style={{
              fontFamily: "'IBM Plex Mono', monospace",
              fontSize: 11,
              letterSpacing: "2.5px",
              textTransform: "uppercase",
              color: "#a9c9b3",
            }}
          >
            NeuroFive Internship · Task 3
          </span>
        </div>
        <h1
          style={{
            fontFamily: "'Fraunces', serif",
            fontWeight: 500,
            fontSize: "clamp(28px, 4vw, 38px)",
            color: "#f2ede3",
            margin: "0 0 8px 0",
            letterSpacing: "-0.5px",
          }}
        >
          Two Agents, <span style={{ color: PALETTE.gold }}>One Pipeline</span>
        </h1>
        <p style={{ color: "#cddccf", fontSize: 14.5, maxWidth: 580, lineHeight: 1.6, margin: 0 }}>
          Agent 1 (Writer) drafts. Agent 2 (Editor/Critic) reviews and refines
          it. Agent 1's output becomes Agent 2's input — no human in between.
        </p>
      </div>

      {/* Main panel */}
      <div
        style={{
          background: PALETTE.paper,
          borderTopLeftRadius: 22,
          borderTopRightRadius: 22,
          padding: "30px 32px 40px 32px",
        }}
      >
        {/* Topic controls */}
        <div style={{ marginBottom: 26 }}>
          <div
            style={{
              fontFamily: "'IBM Plex Mono', monospace",
              fontSize: 10.5,
              letterSpacing: "1.5px",
              textTransform: "uppercase",
              color: PALETTE.deep,
              fontWeight: 600,
              marginBottom: 10,
            }}
          >
            Topic
          </div>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 10 }}>
            {TOPICS.map((t) => (
              <button
                key={t.id}
                onClick={() => {
                  setTopicId(t.id);
                  setCustomTopic("");
                }}
                style={{
                  fontFamily: "'Inter', sans-serif",
                  fontSize: 13,
                  fontWeight: 600,
                  padding: "9px 16px",
                  borderRadius: 999,
                  border:
                    topicId === t.id && !customTopic
                      ? `1.5px solid ${PALETTE.deep}`
                      : `1.5px solid ${PALETTE.line}`,
                  background: topicId === t.id && !customTopic ? PALETTE.deep : "transparent",
                  color: topicId === t.id && !customTopic ? "#f2ede3" : PALETTE.inkSoft,
                  cursor: "pointer",
                }}
              >
                {t.label}
              </button>
            ))}
          </div>
          <input
            value={customTopic}
            onChange={(e) => setCustomTopic(e.target.value)}
            placeholder="...or type your own topic"
            style={{
              width: "100%",
              fontFamily: "'Inter', sans-serif",
              fontSize: 13.5,
              padding: "11px 14px",
              borderRadius: 10,
              border: `1px solid ${PALETTE.line}`,
              background: PALETTE.card,
              outline: "none",
              color: PALETTE.ink,
            }}
          />
        </div>

        {/* Pipeline visual */}
        <div
          style={{
            display: "flex",
            alignItems: "stretch",
            gap: 14,
            marginBottom: 28,
          }}
        >
          <AgentNode
            icon={<PenLine size={16} />}
            label="Agent 1"
            name="Writer"
            color={PALETTE.gold}
            status={
              stage === "writing" ? "running" : draft ? "done" : "idle"
            }
          />
          <div style={{ display: "flex", alignItems: "center", color: PALETTE.inkSoft }}>
            <ArrowRight size={20} />
          </div>
          <AgentNode
            icon={<Wand2 size={16} />}
            label="Agent 2"
            name="Editor / Critic"
            color={PALETTE.editorBlue}
            status={
              stage === "editing" ? "running" : finalText ? "done" : "idle"
            }
          />
          <div style={{ flex: 1 }} />
          <button
            onClick={runPipeline}
            disabled={isBusy || !activeTopic}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              fontFamily: "'Inter', sans-serif",
              fontWeight: 600,
              fontSize: 14,
              padding: "0 22px",
              borderRadius: 10,
              border: "none",
              background: isBusy ? "#2c4d3a" : PALETTE.deep,
              color: "#f2ede3",
              cursor: isBusy || !activeTopic ? "default" : "pointer",
            }}
          >
            {isBusy ? (
              <>
                <Loader2 size={16} className="spin" />
                {stage === "writing" ? "Writer drafting…" : "Editor refining…"}
              </>
            ) : (
              <>Run Pipeline</>
            )}
          </button>
          <style>{`.spin { animation: spin 0.9s linear infinite; } @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
        </div>

        {error && (
          <div style={{ color: "#9a2f2f", fontSize: 13.5, marginBottom: 16 }}>{error}</div>
        )}

        {/* Results */}
        {(draft || finalText) && (
          <div
            style={{
              background: PALETTE.card,
              border: `1px solid ${PALETTE.line}`,
              borderRadius: 14,
              overflow: "hidden",
            }}
          >
            {/* Tabs */}
            <div style={{ display: "flex", borderBottom: `1px solid ${PALETTE.line}` }}>
              <TabButton
                active={tab === "draft"}
                onClick={() => setTab("draft")}
                label="Agent 1 Draft"
                disabled={!draft}
              />
              <TabButton
                active={tab === "final"}
                onClick={() => setTab("final")}
                label="Agent 2 Final"
                disabled={!finalText}
              />
              <TabButton
                active={tab === "notes"}
                onClick={() => setTab("notes")}
                label={`What Changed${notes.length ? ` (${notes.length})` : ""}`}
                disabled={!notes.length}
              />
            </div>

            <div style={{ padding: "22px 24px" }}>
              {tab === "draft" && (
                <div style={{ fontSize: 14, lineHeight: 1.8, color: PALETTE.ink, whiteSpace: "pre-wrap" }}>
                  {draft || "Waiting on Agent 1…"}
                </div>
              )}
              {tab === "final" && (
                <div
                  style={{
                    fontSize: 14,
                    lineHeight: 1.8,
                    color: PALETTE.ink,
                    whiteSpace: "pre-wrap",
                    background: PALETTE.editorBlueSoft,
                    borderLeft: `3px solid ${PALETTE.editorBlue}`,
                    borderRadius: 6,
                    padding: "16px 18px",
                  }}
                >
                  {finalText || "Waiting on Agent 2…"}
                </div>
              )}
              {tab === "notes" && (
                <ul style={{ margin: 0, paddingLeft: 18, fontSize: 13.5, lineHeight: 1.9, color: PALETTE.ink }}>
                  {notes.map((n, i) => (
                    <li key={i} style={{ marginBottom: 6 }}>
                      <CheckCircle2
                        size={13}
                        style={{ display: "inline", marginRight: 6, marginBottom: -1, color: PALETTE.editorBlue }}
                      />
                      {n}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        )}

        {!draft && !finalText && !error && (
          <p
            style={{
              fontFamily: "'IBM Plex Mono', monospace",
              fontSize: 11.5,
              color: PALETTE.inkSoft,
              textAlign: "center",
              marginTop: 40,
            }}
          >
            Pick a topic and run the pipeline — Agent 1's raw draft and Agent 2's refined final will appear here.
          </p>
        )}
      </div>
    </div>
  );
}

function AgentNode({ icon, label, name, color, status }) {
  return (
    <div
      style={{
        background: "#fffdf9",
        border: `1.5px solid ${status === "idle" ? "#dfdac9" : color}`,
        borderRadius: 12,
        padding: "12px 16px",
        minWidth: 150,
        display: "flex",
        flexDirection: "column",
        gap: 4,
        position: "relative",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
        <div style={{ color }}>{icon}</div>
        <span
          style={{
            fontFamily: "'IBM Plex Mono', monospace",
            fontSize: 10,
            letterSpacing: "1px",
            textTransform: "uppercase",
            color: "#5c5a51",
          }}
        >
          {label}
        </span>
        {status === "running" && (
          <Loader2 size={12} className="spin" style={{ marginLeft: "auto", color }} />
        )}
        {status === "done" && (
          <CheckCircle2 size={13} style={{ marginLeft: "auto", color: "#16512c" }} />
        )}
      </div>
      <span style={{ fontFamily: "'Fraunces', serif", fontSize: 16, color: "#1c1c18" }}>{name}</span>
    </div>
  );
}

function TabButton({ active, onClick, label, disabled }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        flex: 1,
        padding: "12px 10px",
        fontFamily: "'Inter', sans-serif",
        fontSize: 12.5,
        fontWeight: 600,
        border: "none",
        borderBottom: active ? `2px solid ${PALETTE.deep}` : "2px solid transparent",
        background: "transparent",
        color: disabled ? "#b8b4a5" : active ? PALETTE.deep : PALETTE.inkSoft,
        cursor: disabled ? "default" : "pointer",
      }}
    >
      {label}
    </button>
  );
}
