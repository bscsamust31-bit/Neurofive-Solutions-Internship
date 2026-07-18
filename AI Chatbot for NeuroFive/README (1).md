<div align="center">

<img src="https://placehold.co/1200x300/0a5c36/ffffff?text=NEUROFIVE+SOLUTIONS&font=montserrat" alt="Neurofive Solutions Banner" width="100%"/>

# 🤖 Nova — Neurofive Solutions Support Assistant

### A custom AI chatbot powered by a system prompt, OpenRouter, and Flask

<img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
<img src="https://img.shields.io/badge/OpenRouter-API-6C5CE7?style=for-the-badge&logo=openai&logoColor=white" alt="OpenRouter"/>
<img src="https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge" alt="License"/>
<img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status"/>

</div>

<br/>

## 📖 Overview

**Nova** is a custom-built AI support assistant for **Neurofive Solutions**, created as part of the *"Build a Custom AI Chatbot with a System Prompt"* task. It connects to a real LLM through the **OpenRouter API** (OpenAI-compatible), uses a carefully written **system prompt** to lock Nova into a specific persona, and is served through a lightweight **Flask backend** with a simple HTML chat frontend.

Unlike a generic AI chatbot, Nova:

- Only talks about **Neurofive Solutions** products and tech support
- **Politely declines** off-topic requests (politics, essays, personal advice, etc.) and redirects back on-topic
- Never invents account details, order numbers, or pricing it doesn't actually have
- Stays fully in character — it never breaks the fourth wall by saying *"I'm an AI language model"*

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Configure Your API Key](#-configure-your-api-key)
- [Running the App](#-running-the-app)
- [API Reference](#-api-reference)
- [The System Prompt](#-the-system-prompt)
- [Test Messages](#-test-messages)
- [Troubleshooting](#-troubleshooting)
- [Security Notes](#-security-notes)
- [Roadmap](#-roadmap)
- [License](#-license)

<br/>

## ✨ Features

| Feature | Description |
|---|---|
| 🎭 **Custom Persona** | System prompt locks the bot into "Nova," a Neurofive support agent |
| 🌐 **Web Chat UI** | Simple HTML frontend served directly by Flask |
| 🔌 **REST API** | `POST /chat` endpoint — easy to plug into any frontend |
| 🧠 **Conversation Memory** | Full chat history sent with each request for contextual replies |
| 🚫 **Off-topic Guardrails** | Politely redirects unrelated questions instead of answering them |
| 🖥️ **Terminal Test Mode** | Run `python chatbot.py --test` for a quick 5-message CLI demo |
| 🆓 **Free-tier LLM** | Runs on OpenRouter's free models — no paid API key required |

<br/>

## 🛠️ Tech Stack

<div align="left">
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask"/>
<img src="https://img.shields.io/badge/Flask--CORS-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask-CORS"/>
<img src="https://img.shields.io/badge/OpenAI_SDK-412991?style=flat-square&logo=openai&logoColor=white" alt="OpenAI SDK"/>
<img src="https://img.shields.io/badge/OpenRouter-6C5CE7?style=flat-square" alt="OpenRouter"/>
<img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white" alt="HTML5"/>
</div>

<br/>

## 📂 Project Structure

```
neurofive-chatbot/
│
├── chatbot.py              # Flask backend + Nova's system prompt + API logic
├── neurofive_chatbot.html  # Frontend chat UI (served at "/")
├── requirements.txt        # Python dependencies
└── README.md                # You are here
```

<br/>

## ⚙️ Setup & Installation

### 1️⃣ Check Python is installed

```bash
python3 --version
```

Need Python 3.9+? Grab it free from [python.org](https://www.python.org/downloads/) — no download link needed here, just visit and install.

### 2️⃣ Clone or download this repo

```bash
git clone https://github.com/your-username/neurofive-chatbot.git
cd neurofive-chatbot
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install flask flask-cors openai
```

<br/>

## 🔑 Configure Your API Key

> ⚠️ **Never hardcode your API key in the script.** Always use an environment variable — see [Security Notes](#-security-notes) below for why.

### Step 1 — Get a free OpenRouter API key
Go to **https://openrouter.ai/keys**, sign in, and click **Create Key**.

### Step 2 — Set it as an environment variable

<table>
<tr><th>OS</th><th>Command</th></tr>
<tr>
<td>🍎 macOS / 🐧 Linux</td>
<td>

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-real-key-here"
```

</td>
</tr>
<tr>
<td>🪟 Windows (CMD)</td>
<td>

```cmd
set OPENROUTER_API_KEY=sk-or-v1-your-real-key-here
```

</td>
</tr>
<tr>
<td>🪟 Windows (PowerShell)</td>
<td>

```powershell
$env:OPENROUTER_API_KEY="sk-or-v1-your-real-key-here"
```

</td>
</tr>
</table>

This only lasts for the current terminal session — set it again next time you open a new terminal, or use `setx` (Windows) / add it to your shell profile (Mac/Linux) to make it permanent.

<br/>

## ▶️ Running the App

### Option A — Full web app (chat UI in browser)

```bash
python chatbot.py
```

Then open your browser to:

```
http://localhost:5000
```

<div align="center">
<img src="https://placehold.co/700x120/0a5c36/ffffff?text=%F0%9F%9F%A2+Nova+is+running+at%3A+http%3A%2F%2Flocalhost%3A5000&font=montserrat" alt="Terminal output example" width="70%"/>
</div>

### Option B — Quick terminal test (no browser needed)

```bash
python chatbot.py --test
```

This runs Nova through 5 pre-written test messages (including one off-topic "tricky" one) directly in your terminal — perfect for a fast sanity check or a demo recording.

<br/>

## 🔌 API Reference

### `POST /chat`

Send a user message (and optional conversation history) to Nova.

**Request body:**
```json
{
  "message": "Do you offer a free trial of your product?",
  "history": [
    { "role": "user", "content": "Hi, what can you help me with?" },
    { "role": "assistant", "content": "Hey! I'm Nova from Neurofive Solutions..." }
  ]
}
```

**Success response — `200 OK`:**
```json
{
  "reply": "Great question! We do offer a free trial — I don't have the exact terms in front of me, but you can check the Pricing page or email support@neurofivesolutions.com for details."
}
```

**Error response — `400` / `500`:**
```json
{ "error": "Empty message" }
```

<br/>

## 🧬 The System Prompt

Nova's entire personality lives in one system prompt inside `chatbot.py`. This is what makes her a *Neurofive support assistant* instead of a generic chatbot:

```text
You are Nova, the official virtual support assistant for Neurofive Solutions...

1. Friendly, upbeat, concise
2. ONLY discusses Neurofive Solutions & tech support topics
3. Politely declines and redirects off-topic requests
4. Never invents account/order/pricing details
5. Keeps replies short (2-4 sentences)
6. Always stays in character as Nova
```

<br/>

## 🧪 Test Messages

These are the 5 messages used to validate that Nova stays in character:

| # | Test Message | Purpose |
|---|---|---|
| 1 | "Hi, what can you help me with?" | Baseline greeting |
| 2 | "I forgot my password and can't log into my Neurofive dashboard." | Common support scenario |
| 3 | "Do you offer a free trial of your product?" | Product question, no fabricated details |
| 4 | "Can you write me a poem about my ex-girlfriend instead?" | 🎯 **Off-topic trap** — tests redirect behavior |
| 5 | "Thanks! One more thing — is my data safe with Neurofive?" | Trust/security follow-up |

<br/>

## 🩹 Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Dependencies not installed | Run `pip install -r requirements.txt` |
| `AuthenticationError` / `401` | API key missing or wrong | Re-check [Configure Your API Key](#-configure-your-api-key) |
| `429 Too Many Requests` | Free model rate-limited | Wait a minute, or swap `MODEL` in `chatbot.py` |
| Browser shows "Not Found" at `/` | `neurofive_chatbot.html` missing from folder | Make sure the HTML frontend file sits next to `chatbot.py` |
| CORS errors in browser console | Frontend/backend origin mismatch | Confirm `flask-cors` is installed and `CORS(app)` is active |

<br/>

## 🔒 Security Notes

- **Never commit real API keys to GitHub.** Always load them via `os.environ.get(...)` with no real key as the fallback — use a placeholder string instead, like `"PASTE-YOUR-KEY-HERE"`.
- If a key is ever accidentally pushed, **revoke it immediately** at [openrouter.ai/keys](https://openrouter.ai/keys) and generate a new one.
- Add a `.gitignore` entry for any `.env` file if you switch to using one.

<br/>

## 🗺️ Roadmap

- [ ] Add streaming responses for a typing-effect feel
- [ ] Persist conversation history per user session
- [ ] Add a typing indicator in the frontend UI
- [ ] Swap in a paid model for higher rate limits in production

<br/>

## 📄 License

Released under the **MIT License** — free to use, modify, and build on.

<br/>

<div align="center">

<img src="https://placehold.co/1200x150/0a5c36/ffffff?text=Built+for+Neurofive+Solutions&font=montserrat" alt="Neurofive Footer Banner" width="100%"/>

</div>
