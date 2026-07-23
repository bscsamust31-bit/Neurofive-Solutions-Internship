# ResumeForge AI

**AI-powered resume analyzer, ATS optimizer, interview prep engine & cover-letter
generator.** A polished, animated (Three.js) single-page frontend backed by a
Flask API that talks to an LLM through the **BlueMinds** AI gateway.

> Built as the final internship task for **NeuroFive Solutions**.

---

## ✨ Features

- **📊 Deep Resume Scoring** — overall score + 5-axis breakdown (content
  quality, formatting, keyword optimization, impact metrics, company fit).
- **🎯 Company-Tailored Insights** — recommendations shaped around a target
  company's real culture (Google, Amazon, Microsoft, Meta, Apple, Netflix,
  early-stage startups, or generic).
- **🤖 ATS Optimization Report** — a dedicated ATS score plus concrete issues
  and fixes so the resume survives applicant tracking systems.
- **🧠 Interview Prep Engine** — likely interview questions by type
  (behavioral / technical / situational / culture-fit), talking points to
  lean into, and red flags to proactively address.
- **📋 Prioritized Action Plan** — a checklist of next steps with priority
  and time estimates.
- **✉️ AI Cover Letter Generator** — one click turns the resume + job
  description into a tailored, ready-to-send cover letter with a subject
  line, in the tone you choose.
- **📄 Resume Upload** — drag-and-drop or browse to upload `.pdf`, `.docx`,
  or `.txt` resumes; text is auto-extracted into the editable textarea.
- **🟢 Live API status pill** — the navbar shows whether the AI engine is
  actually configured and reachable, in real time.

The frontend (`templates/index.html`) is **unchanged from the original
design** — the same animated hero, glassmorphism cards, scoring rings, and
cover-letter modal. `app.py` simply implements every endpoint the frontend
already expects, so the two "click together" out of the box.

---

## 🧱 Project Structure

```
resumeforge/
├── app.py                # Flask backend — all API logic lives here
├── templates/
│   └── index.html        # Original frontend (untouched), served by Flask
├── requirements.txt       # Python dependencies
├── .env.example           # Copy to .env and fill in your BlueMinds key
└── README.md               # You are here
```

---

## 🔌 How the frontend & backend are connected

`index.html` already calls these relative endpoints via `fetch(...)` — no
frontend code was changed, `app.py` was written to match it exactly:

| Method | Endpoint               | Called by                        | Purpose                                   |
|--------|-------------------------|-----------------------------------|--------------------------------------------|
| GET    | `/`                     | Browser                          | Serves `index.html`                        |
| GET    | `/api/status`           | Navbar status pill               | Reports whether the AI key is configured   |
| GET    | `/api/companies`        | "Target Company" dropdown        | Returns the list of tailorable companies   |
| POST   | `/api/upload-resume`    | Drag-and-drop / file picker      | Extracts text from an uploaded resume      |
| POST   | `/api/analyze`          | "Analyze Resume →" button        | Runs the full AI resume analysis           |
| POST   | `/api/cover-letter`     | "✉️ Generate Cover Letter" button | Generates a tailored cover letter          |

`app.py` renders `templates/index.html` with Flask's `render_template`, and
every JS `fetch()` call in that file hits one of the routes above on the
**same origin** — so once the server is running, opening `http://localhost:5000`
gives you the fully working app with no extra configuration.

---

## 🤖 AI Provider: BlueMinds

This project uses the **BlueMinds API** (`https://api.bluesminds.com/v1`) as
its LLM provider. BlueMinds exposes an **OpenAI-compatible** REST API, so the
backend uses the official `openai` Python SDK and simply points its
`base_url` at BlueMinds instead of OpenAI:

```python
client = OpenAI(api_key=BLUESMINDS_API_KEY, base_url="https://api.bluesminds.com/v1")
```

This means:
- You can swap in **any** OpenAI-compatible provider (OpenAI itself, Groq,
  OpenRouter, etc.) just by changing `BLUESMINDS_BASE_URL` / renaming the env
  vars — no code changes required.
- You choose the underlying model via `BLUESMINDS_MODEL` (defaults to
  `gpt-4o-mini`; BlueMinds also offers Claude and Gemini family models —
  check your BlueMinds dashboard for exactly which model IDs your key can
  access).

The backend asks the model to return **strict JSON** matching the schema the
frontend already expects (`overall_score`, `score_breakdown`, `strengths`,
`weaknesses`, `interview_prep`, `ats_optimization`, `action_plan`, etc.), so
results render directly into the existing UI components — score ring,
breakdown bars, before/after improvement cards, interview question cards,
and the action plan checklist.

---

## ⚙️ Setup & Installation

### 1. Clone / copy the project and enter the folder
```bash
cd resumeforge
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your BlueMinds API key
```bash
cp .env.example .env
```
Then edit `.env`:
```env
BLUESMINDS_API_KEY=your_bluesminds_api_key_here
BLUESMINDS_BASE_URL=https://api.bluesminds.com/v1
BLUESMINDS_MODEL=gpt-4o-mini
PORT=5000
FLASK_DEBUG=true
```
Get a BlueMinds API key from your BlueMinds account/dashboard
(`https://api.bluesminds.com`).

### 5. Run the app
```bash
python app.py
```
Then open **http://localhost:5000** in your browser.

If `BLUESMINDS_API_KEY` isn't set, the app still runs and the UI still
loads — the status pill will show **"API key not configured"** and
`/api/analyze` / `/api/cover-letter` will return a clear 503 error instead
of crashing, so you can demo the frontend even without a key.

---

## 🧪 API Reference

### `GET /api/status`
```json
{ "api_configured": true, "model": "gpt-4o-mini" }
```

### `GET /api/companies`
```json
[{ "id": "google", "name": "Google" }, { "id": "amazon", "name": "Amazon" }, ...]
```

### `POST /api/upload-resume` — `multipart/form-data`, field `file`
Accepts `.pdf`, `.docx`, `.txt` (max 8 MB).
```json
{ "resume_text": "extracted plain text...", "filename": "resume.pdf" }
```

### `POST /api/analyze`
Request:
```json
{
  "resume_text": "...",
  "job_description": "optional",
  "company_name": "google",
  "experience_level": "Mid-Level"
}
```
Response: a JSON object with `overall_score`, `score_breakdown`,
`executive_summary`, `strengths`, `weaknesses`, `missing_keywords`,
`suggested_improvements`, `tailored_recommendations`, `interview_prep`,
`ats_optimization`, and `action_plan` — matching exactly what
`renderResults()` in `index.html` expects.

### `POST /api/cover-letter`
Request:
```json
{
  "resume_text": "...",
  "job_description": "optional",
  "company_name": "netflix",
  "experience_level": "Senior",
  "tone": "Professional and confident"
}
```
Response:
```json
{ "subject_line": "...", "cover_letter": "..." }
```

---

## 🛠️ Tech Stack

- **Backend:** Flask, `openai` SDK (pointed at BlueMinds), `pypdf`,
  `python-docx`, `python-dotenv`
- **Frontend:** Vanilla HTML/CSS/JS + Three.js (unchanged, original design)
- **AI Provider:** BlueMinds (OpenAI-compatible gateway)

---

## 📝 Notes

- All resume/job-description text is sent to the configured AI provider for
  analysis only — the app itself does not persist uploaded resumes to disk;
  extracted text is returned directly to the browser and kept in memory for
  the current session.
- `MAX_CONTENT_LENGTH` is capped at 8 MB per upload to keep things fast.
- The company list in `COMPANIES` (inside `app.py`) is easy to extend — add
  a new `id: {"name": ..., "profile": ...}` entry and it automatically shows
  up in the "Target Company" dropdown and steers the AI's tailored output.

---

## 👩‍💻 Author

Built as the final task of the **NeuroFive Solutions internship program**.
