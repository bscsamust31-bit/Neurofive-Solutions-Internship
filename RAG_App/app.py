"""
RAG Mini-Project — Chat With Your Own Document
------------------------------------------------
A polished Streamlit app that lets you upload a document (PDF / TXT / DOCX),
builds a real retrieval pipeline (chunking + embeddings + FAISS vector search),
and answers your questions grounded in that document — with source snippets,
hallucination flagging, and an auto-generated summary report for your writeup.

Run:
    pip install -r requirements.txt
    streamlit run app.py
"""

import os
import io
import time
import textwrap
import datetime
import numpy as np
import streamlit as st

# ----------------------------- API Key --------------------------------------
# Paste your Bluesmind API key here
BLUESMIND_API_KEY = "your key"
BLUESMIND_BASE_URL = "https://api.bluesminds.com/v1"

# Model used for all answers (fixed — no dropdown in the UI)
MODEL = "gpt-4o"

# ----------------------------- Page config ---------------------------------
st.set_page_config(
    page_title="ChatDoc — RAG Mini Project",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------- Theme / CSS ----------------------------------
CUSTOM_CSS = """
<style>
:root{
    --bg:#06100c;
    --panel:#0c1a13;
    --panel2:#0f2118;
    --green:#22c55e;
    --green-soft:#16a34a33;
    --green-glow: 0 0 24px #22c55e55;
    --text:#e6f4ea;
    --muted:#7fa38c;
    --border:#1c3325;
}
html, body, [class*="css"]  {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
#MainMenu, footer, header {visibility: hidden;}
.stApp { background: radial-gradient(circle at 20% 0%, #0d1f14 0%, #06100c 55%); }

/* Landing hero */
.hero-wrap{
    padding: 64px 24px 32px 24px;
    text-align:center;
}
.hero-badge{
    display:inline-block;
    padding:6px 16px;
    border:1px solid var(--border);
    border-radius:999px;
    color:var(--green);
    font-size:13px;
    letter-spacing:1.5px;
    text-transform:uppercase;
    background:var(--panel2);
    margin-bottom:22px;
}
.hero-title{
    font-size:56px;
    font-weight:800;
    line-height:1.08;
    background:linear-gradient(180deg,#eafff1 0%, #9ef0b8 60%, #22c55e 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:14px;
}
.hero-sub{
    max-width:680px;
    margin:0 auto 34px auto;
    color:var(--muted);
    font-size:18px;
    line-height:1.6;
}
.feature-card{
    background:var(--panel);
    border:1px solid var(--border);
    border-radius:16px;
    padding:22px 20px;
    height:100%;
    transition: all .2s ease;
}
.feature-card:hover{
    border-color:var(--green);
    box-shadow:var(--green-glow);
    transform:translateY(-2px);
}
.feature-icon{font-size:26px;margin-bottom:10px;}
.feature-title{font-weight:700;font-size:16px;margin-bottom:6px;color:#eafff1;}
.feature-desc{color:var(--muted);font-size:13.5px;line-height:1.5;}

.step-pill{
    display:flex;align-items:center;gap:12px;
    background:var(--panel2);
    border:1px solid var(--border);
    border-radius:12px;
    padding:12px 16px;
    margin-bottom:10px;
}
.step-num{
    background:var(--green);color:#06100c;font-weight:800;
    width:26px;height:26px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;
}

/* Chat area */
.chat-bubble-user{
    background:var(--green-soft);
    border:1px solid var(--green);
    border-radius:14px 14px 2px 14px;
    padding:12px 16px;margin:8px 0;color:#eafff1;
}
.chat-bubble-ai{
    background:var(--panel);
    border:1px solid var(--border);
    border-radius:14px 14px 14px 2px;
    padding:12px 16px;margin:8px 0;color:var(--text);
}
.source-box{
    background:#081209;
    border:1px dashed var(--border);
    border-radius:10px;
    padding:10px 12px;
    font-size:12.5px;
    color:var(--muted);
    margin-top:6px;
}
.flag-tag{
    display:inline-block;background:#5b1d1d;color:#ffb4b4;
    border-radius:6px;padding:2px 8px;font-size:11.5px;margin-left:8px;
}
.section-title{
    color:var(--green);font-size:13px;letter-spacing:1.5px;
    text-transform:uppercase;margin-bottom:6px;font-weight:700;
}
div.stButton > button{
    background:var(--green);
    color:#06100c;
    font-weight:700;
    border-radius:10px;
    border:none;
    padding:10px 22px;
}
div.stButton > button:hover{
    background:#39e37a;
    box-shadow:var(--green-glow);
}
[data-testid="stSidebar"]{
    background:var(--panel);
    border-right:1px solid var(--border);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------------------- Session state --------------------------------
defaults = {
    "started": False,
    "doc_chunks": [],
    "doc_embeddings": None,
    "doc_name": None,
    "chat_history": [],   # list of dicts: question, answer, sources, flagged, plain_answer
    "embedder_ready": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ----------------------------- Landing page ---------------------------------
def render_landing():
    st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="hero-badge">Week 3 · Generative AI &amp; Prompt Engineering</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Chat With Your<br>Own Document</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">A real Retrieval-Augmented Generation pipeline — chunking, '
        'embeddings, vector search, and grounded answers. Upload a PDF, resume, or notes, '
        'and ask it anything. No hallucinated guesses, just answers pulled from your file.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown(
            '<div class="feature-card"><div class="feature-icon">📄</div>'
            '<div class="feature-title">Real Chunking + Embeddings</div>'
            '<div class="feature-desc">Your document is split into overlapping chunks and embedded '
            'with sentence-transformers, then indexed in FAISS for fast semantic search.</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="feature-card"><div class="feature-icon">🎯</div>'
            '<div class="feature-title">Grounded Answers + Sources</div>'
            '<div class="feature-desc">Every answer shows the exact chunks it was built from, '
            'so you can verify it against the source instead of trusting it blindly.</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="feature-card"><div class="feature-icon">🚩</div>'
            '<div class="feature-title">Hallucination Flagging</div>'
            '<div class="feature-desc">Flag any answer that isn\'t really in the document, and '
            'compare it side-by-side against a plain prompt with no retrieval.</div></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown('<div class="section-title">How it works</div>', unsafe_allow_html=True)
    steps = [
        "Upload a PDF, DOCX, or TXT file — 3 to 10 pages works best",
        "The app chunks the text and builds a local FAISS vector index",
        "Ask at least 5 questions — the app retrieves relevant chunks and answers from them",
        "Flag any hallucinated answers, then export a summary report for your submission",
    ]
    for i, s in enumerate(steps, 1):
        st.markdown(
            f'<div class="step-pill"><div class="step-num">{i}</div><div>{s}</div></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    _, mid, _ = st.columns([1, 1, 1])
    with mid:
        if st.button("Get Started →", use_container_width=True):
            st.session_state.started = True
            st.rerun()


# ----------------------------- RAG utilities --------------------------------
@st.cache_resource(show_spinner=False)
def load_embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


def extract_text(uploaded_file):
    name = uploaded_file.name.lower()
    data = uploaded_file.read()
    if name.endswith(".pdf"):
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif name.endswith(".docx"):
        import docx
        doc = docx.Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        return data.decode("utf-8", errors="ignore")


def chunk_text(text, chunk_size=800, overlap=150):
    text = " ".join(text.split())
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c for c in chunks if len(c.strip()) > 30]


def build_index(chunks):
    import faiss
    embedder = load_embedder()
    embeddings = embedder.encode(chunks, show_progress_bar=False, normalize_embeddings=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index, embeddings


def retrieve(query, chunks, index, k=4):
    embedder = load_embedder()
    q_emb = embedder.encode([query], normalize_embeddings=True).astype("float32")
    scores, idxs = index.search(q_emb, k)
    results = []
    for score, idx in zip(scores[0], idxs[0]):
        if idx == -1:
            continue
        results.append((chunks[idx], float(score)))
    return results


def call_llm(api_key, system_prompt, user_prompt, model=MODEL):
    import requests
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
    }
    resp = requests.post(
        f"{BLUESMIND_BASE_URL}/chat/completions",
        headers=headers, json=payload, timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


# ----------------------------- Main app --------------------------------------
def render_app():
    st.markdown(
        '<div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0 18px 0;">'
        '<div style="font-size:22px;font-weight:800;color:#eafff1;">📖 ChatDoc <span style="color:#22c55e;">RAG</span></div>'
        '</div>', unsafe_allow_html=True
    )

    api_key = BLUESMIND_API_KEY

    with st.sidebar:
        st.markdown('<div class="section-title">Document</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload PDF / DOCX / TXT", type=["pdf", "docx", "txt"])
        if uploaded and st.button("⚡ Process document", use_container_width=True):
            with st.spinner("Chunking and embedding your document..."):
                text = extract_text(uploaded)
                if not text.strip():
                    st.error("Couldn't extract any text from this file.")
                else:
                    chunks = chunk_text(text)
                    index, embeddings = build_index(chunks)
                    st.session_state.doc_chunks = chunks
                    st.session_state.doc_index = index
                    st.session_state.doc_name = uploaded.name
                    st.session_state.chat_history = []
            st.success(f"Indexed {len(st.session_state.doc_chunks)} chunks from {uploaded.name}")

        if st.session_state.doc_name:
            st.info(f"📄 Active doc: **{st.session_state.doc_name}**\n\n{len(st.session_state.doc_chunks)} chunks indexed")

        st.markdown("---")
        compare_mode = st.checkbox("Also generate a plain (no-RAG) answer for comparison", value=True)

        st.markdown("---")
        if st.button("⬅ Back to landing"):
            st.session_state.started = False
            st.rerun()

    if not st.session_state.doc_name:
        st.markdown(
            '<div class="feature-card" style="text-align:center;padding:60px 20px;">'
            '<div style="font-size:40px;">📤</div>'
            '<div class="feature-title" style="margin-top:10px;">Upload a document in the sidebar to begin</div>'
            '<div class="feature-desc">PDF, DOCX, or TXT — 3 to 10 pages works best.</div>'
            '</div>', unsafe_allow_html=True
        )
        return

    if not api_key or "PASTE-YOUR-BLUESMIND-KEY-HERE" in api_key:
        st.warning("⚠️ Set your Bluesmind API key in the BLUESMIND_API_KEY variable near the top of app.py.")

    st.markdown('<div class="section-title">Ask a question about your document</div>', unsafe_allow_html=True)
    with st.form("qa_form", clear_on_submit=True):
        question = st.text_input("Your question", placeholder="e.g. What does section 2 say about eligibility?")
        submitted = st.form_submit_button("Ask →")

    if submitted and question.strip() and api_key:
        with st.spinner("Retrieving relevant chunks and generating an answer..."):
            hits = retrieve(question, st.session_state.doc_chunks, st.session_state.doc_index, k=4)
            context = "\n\n---\n\n".join(f"[Chunk {i+1}] {c}" for i, (c, s) in enumerate(hits))
            system_prompt = (
                "You are a careful assistant that answers ONLY using the provided document "
                "context. If the answer isn't in the context, say clearly that the document "
                "doesn't contain that information — do not make anything up."
            )
            user_prompt = f"Document context:\n{context}\n\nQuestion: {question}\n\nAnswer using only the context above."
            try:
                answer = call_llm(api_key, system_prompt, user_prompt, model=MODEL)
            except Exception as e:
                answer = f"⚠️ Error calling the model: {e}"

            plain_answer = None
            if compare_mode:
                try:
                    plain_answer = call_llm(
                        api_key,
                        "You are a helpful assistant.",
                        question,
                        model=MODEL,
                    )
                except Exception as e:
                    plain_answer = f"⚠️ Error calling the model: {e}"

            st.session_state.chat_history.append({
                "question": question,
                "answer": answer,
                "plain_answer": plain_answer,
                "sources": hits,
                "flagged": False,
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
            })

    # ---- Chat history ----
    for i, turn in enumerate(reversed(st.session_state.chat_history)):
        real_i = len(st.session_state.chat_history) - 1 - i
        st.markdown(f'<div class="chat-bubble-user"><b>You:</b> {turn["question"]}</div>', unsafe_allow_html=True)
        flag_html = '<span class="flag-tag">⚑ flagged as hallucinated</span>' if turn["flagged"] else ""
        st.markdown(f'<div class="chat-bubble-ai"><b>RAG answer:</b> {turn["answer"]}{flag_html}</div>', unsafe_allow_html=True)

        cols = st.columns([1, 3])
        with cols[0]:
            flagged = st.checkbox("Flag as hallucinated", value=turn["flagged"], key=f"flag_{real_i}")
            if flagged != turn["flagged"]:
                st.session_state.chat_history[real_i]["flagged"] = flagged
                st.rerun()
        with cols[1]:
            with st.expander("Show retrieved sources"):
                for j, (chunk, score) in enumerate(turn["sources"]):
                    st.markdown(
                        f'<div class="source-box"><b>Chunk {j+1}</b> (similarity {score:.2f})<br>{textwrap.shorten(chunk, 300)}</div>',
                        unsafe_allow_html=True,
                    )

        if turn["plain_answer"]:
            with st.expander("Compare: plain prompt (no document context)"):
                st.markdown(f'<div class="chat-bubble-ai">{turn["plain_answer"]}</div>', unsafe_allow_html=True)
        st.markdown("---")

    # ---- Summary / export ----
    if st.session_state.chat_history:
        st.markdown('<div class="section-title">Summary &amp; Export</div>', unsafe_allow_html=True)
        reflection = st.text_area(
            "Your reflection: how did grounding in your own data change answer quality vs a plain prompt?",
            placeholder="e.g. The RAG answers cited specific figures from page 3 that the plain prompt just guessed at...",
            height=100,
        )
        if st.button("📥 Generate summary report"):
            n_flagged = sum(1 for t in st.session_state.chat_history if t["flagged"])
            lines = [
                f"# RAG Mini-Project Summary\n",
                f"**Document:** {st.session_state.doc_name}",
                f"**Date:** {datetime.date.today().isoformat()}",
                f"**Total questions asked:** {len(st.session_state.chat_history)}",
                f"**Flagged as hallucinated:** {n_flagged}\n",
                "## Q&A Log\n",
            ]
            for idx, t in enumerate(st.session_state.chat_history, 1):
                lines.append(f"### Q{idx}: {t['question']}")
                lines.append(f"**RAG Answer:** {t['answer']}")
                if t["flagged"]:
                    lines.append("**⚑ Flagged as hallucinated / not actually in document**")
                if t["plain_answer"]:
                    lines.append(f"**Plain prompt answer (no context):** {t['plain_answer']}")
                lines.append("")
            lines.append("## Reflection\n")
            lines.append(reflection or "_(not yet written)_")
            report = "\n".join(lines)
            st.download_button(
                "Download report (Markdown)",
                data=report,
                file_name="rag_project_summary.md",
                mime="text/markdown",
            )
            st.code(report, language="markdown")


# ----------------------------- Router ----------------------------------------
if st.session_state.started:
    render_app()
else:
    render_landing()
