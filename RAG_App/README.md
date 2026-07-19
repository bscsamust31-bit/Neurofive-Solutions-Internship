# 📖 RAG Mini-Project — Chat With Your Own Document

**Week 3 · Generative AI & Prompt Engineering**

A complete Retrieval-Augmented Generation pipeline with a polished dark/green landing page — upload a document, ask it real questions, and get answers grounded in the actual content instead of a guess.

---

## 📌 Task Description

LLMs don't know your private data — that's where **Retrieval-Augmented Generation (RAG)** comes in. It's the technique behind almost every "chat with your PDF" tool out there. This project builds a small pipeline that lets an AI answer questions using a document you give it, instead of guessing from its training data.

**Tech / concepts covered:** RAG, embeddings, vector search, chunking, LangChain-style retrieval pipeline (built with `sentence-transformers` + FAISS), LLM generation via Bluesmind (gpt-4o).

### ✅ Requirements checklist
- [x] Pick a document (PDF, resume, class notes — 3–10 pages)
- [x] Coded approach: chunking + embeddings + FAISS vector search (no-code tools not needed)
- [x] Upload/ingest the document and ask ≥5 questions requiring the actual content
- [x] Flag any answer that seems hallucinated (not actually in the document)
- [x] Written summary: grounding vs plain prompt quality
- [x] Built-in comparison mode to demo grounded vs ungrounded answers side-by-side
- [ ] Record a 2–3 min demo video of 2–3 Q&A exchanges *(do this after running the app — see below)*
- [ ] Upload video to LinkedIn, tag Neurofive Solutions, share the link

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎨 **Landing page** | Dark/green themed hero page explaining the project before you jump into the app |
| ✂️ **Chunking** | Splits your document into overlapping ~800-character chunks so context isn't lost at boundaries |
| 🧠 **Local embeddings** | Uses `sentence-transformers` (`all-MiniLM-L6-v2`) — runs on your machine, no API cost |
| 🔍 **Vector search** | FAISS index retrieves the top-4 most relevant chunks per question |
| 💬 **Grounded chat** | Sends retrieved chunks as context to an LLM (via Bluesmind) so answers are grounded, not guessed |
| 📎 **Source transparency** | Every answer shows exactly which chunks it was built from, with similarity scores |
| 🚩 **Hallucination flagging** | One-click checkbox to flag any answer that isn't actually supported by the document |
| ⚖️ **Plain-prompt comparison** | Optional side-by-side answer with zero document context, to see the difference retrieval makes |
| 📥 **Auto summary export** | Generates a downloadable Markdown report of your full Q&A log + written reflection |

---

## 🛠️ Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

### Setting your API key
The app calls the LLM through **Bluesmind** (OpenAI-compatible endpoint), and the key is set directly in the code (no input field in the UI):
1. Open **`app.py`**, find these lines near the top:
   ```python
   BLUESMIND_API_KEY = "PASTE-YOUR-BLUESMIND-KEY-HERE"
   BLUESMIND_BASE_URL = "https://api.bluesminds.com/v1"
   ```
2. Replace `"PASTE-YOUR-BLUESMIND-KEY-HERE"` with your real Bluesmind key, save, and rerun the app

The model is fixed to **`gpt-4o`** (set via the `MODEL` constant, no dropdown in the UI).

> ⚠️ **Security note:** since the key now lives in the code, don't upload `app.py` publicly (e.g. to a public GitHub repo) with your real key still in it. Keep it private, or swap it back to an environment variable before sharing.

> **Note:** the first run downloads the embedding model (~90MB) — needs internet once, then embedding runs fully offline. Only your question + the relevant retrieved chunks are sent to Bluesmind per query — your full document never leaves your machine.

---

## 🚀 How to use it (step by step)

1. Set your Bluesmind key in `app.py` (see above) before launching
2. Click **Get Started** on the landing page
3. Upload a 3–10 page PDF / DOCX / TXT and click **⚡ Process document**
4. Ask **at least 5 questions** that require reading the actual content
5. For any answer that seems made up, tick **Flag as hallucinated**
6. Expand **Compare: plain prompt** under any answer to see the non-RAG version
7. Scroll down, write your reflection in the text box
8. Click **📥 Generate summary report** and download the `.md` file
9. Screen-record 2–3 of your Q&A exchanges, upload to LinkedIn tagging Neurofive Solutions

---

## 📝 Project Summary — Grounding vs Plain Prompting

*(This is a starting template — swap in your own document's specifics once you've run your test questions, then paste your final version into the in-app report.)*

**What changed with RAG:**
Answers pulled directly from the uploaded document were noticeably more specific and verifiable — they referenced exact figures, names, dates, or clauses that only exist in that file, and each one came with the retrieved source chunk attached so it could be checked against the original text. Because the model was explicitly instructed to answer *only* from the provided context, it would say when something wasn't covered instead of inventing an answer.

**What the plain prompt did instead:**
Without retrieval, the same questions got answered from the model's general training knowledge. On anything generic the answers sounded fine on the surface, but they had no connection to the actual document — dates, numbers, and specifics were either generic placeholders or plausible-sounding guesses that didn't match the source at all. There was no way to trace *where* an answer came from, which is exactly the hallucination risk RAG is meant to solve.

**Key takeaway:**
Grounding doesn't just change the *wording* of an answer — it changes whether the answer is *checkable*. The retrieved-source panel turned every RAG answer into something verifiable in one click, while the plain prompt answers had to be taken on faith. For any use case involving private, recent, or authoritative data, retrieval is what separates a trustworthy assistant from a confident-sounding guesser.

---

## 📂 Project structure

```
rag_app/
├── app.py              # Full Streamlit app — landing page + RAG pipeline + chat UI
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## ⚙️ Tech Stack

- **Frontend/App:** Streamlit, custom dark/green CSS theme
- **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`, local & free)
- **Vector store:** FAISS (`IndexFlatIP`, cosine similarity via normalized vectors)
- **LLM:** Bluesmind API (OpenAI-compatible), model fixed to `gpt-4o`
- **Document parsing:** `pypdf`, `python-docx`
