<div align="center">

<img src="https://placehold.co/1200x300/0a5c36/ffffff?text=NEUROFIVE+SOLUTIONS&font=montserrat" alt="Neurofive Solutions Banner" width="100%"/>

# 🧠 Think Step-by-Step — Chain-of-Thought & Persona Prompting

### Proving CoT + Persona prompting improves reasoning, with a real before/after comparison

<img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/OpenRouter-API-6C5CE7?style=for-the-badge&logo=openai&logoColor=white" alt="OpenRouter"/>
<img src="https://img.shields.io/badge/Concept-Chain--of--Thought-orange?style=for-the-badge" alt="CoT"/>
<img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status"/>

</div>

<br/>

## 📖 Overview

This task tests a simple but powerful idea: **how you ask an LLM a question changes whether it gets the question right.** Same model, same problem, two prompting styles:

- **Run A ("Before"):** a plain, direct prompt — no reasoning instruction, no persona
- **Run B ("After"):** the same problem + **"think step-by-step before answering"** + a relevant expert persona

One script (`cot_vs_plain.py`) fires both prompts at the same model back-to-back and saves the full output to `comparison_results.md` for your write-up and demo video.

<br/>

## 📑 Table of Contents

- [The Problem Chosen](#-the-problem-chosen)
- [Why This Problem](#-why-this-problem)
- [Setup & Installation](#-setup--installation)
- [Configure Your API Key](#-configure-your-api-key)
- [Running the Comparison](#-running-the-comparison)
- [The Two Prompts](#-the-two-prompts)
- [Comparing the Results](#-comparing-the-results)
- [Why CoT + Persona Changed the Result](#-why-cot--persona-changed-the-result)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

<br/>

## 🧩 The Problem Chosen

> *A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?*

**Correct answer:** $0.05

This is a classic **math word problem that requires reasoning**, not recall. It's well-suited for this task because it has a well-documented *intuitive-but-wrong* shortcut answer ($0.10) that models and people alike tend to blurt out instantly — making it an excellent stress-test for whether a prompting technique actually forces real reasoning instead of pattern-matching.

<br/>

## 🎯 Why This Problem

| Requirement from task brief | How this problem satisfies it |
|---|---|
| Needs reasoning | Requires setting up and solving a simple algebraic equation |
| Has a clear correct/incorrect answer | $0.05 is correct; $0.10 is the common wrong answer |
| Reveals a difference between prompting styles | Plain prompting invites pattern-matching to the "obvious" wrong answer; CoT forces step-by-step verification |

<br/>

## ⚙️ Setup & Installation

### 1️⃣ Check Python is installed

```bash
python3 --version
```

Need it? Install free from [python.org](https://www.python.org/downloads/).

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install openai
```

<br/>

## 🔑 Configure Your API Key

> ⚠️ Never hardcode your API key in the script — always use an environment variable.

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

<br/>

## ▶️ Running the Comparison

```bash
python cot_vs_plain.py
```

This will:
1. Send **Run A** (plain prompt) to the model and print the response
2. Send **Run B** (CoT + persona prompt) to the same model and print the response
3. Save both, side by side, into **`comparison_results.md`**

Record your screen while this runs — this terminal output *is* your before/after demo for the video.

<br/>

## 🔀 The Two Prompts

### Run A — Plain Prompt (Before)
```
A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball.
How much does the ball cost?
```
*No persona. No reasoning instruction. Direct question in, direct answer out.*

### Run B — Chain-of-Thought + Persona (After)

**Persona (system prompt):**
```
You are a senior data analyst who is meticulous about arithmetic and never
skips a step when solving a quantitative problem.
```

**User prompt:**
```
A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball.
How much does the ball cost?

Think step-by-step before answering. Show your reasoning first, then clearly
state your final answer on the last line as 'Final Answer: ...'
```

<br/>

## 📊 Comparing the Results

After running the script, fill this in with your **actual** output from `comparison_results.md`:

| | Run A (Plain) | Run B (CoT + Persona) |
|---|---|---|
| **Final answer given** | *(paste actual output)* | *(paste actual output)* |
| **Correct?** | *(Yes/No)* | *(Yes/No)* |
| **Shows reasoning steps?** | *(Yes/No)* | *(Yes/No)* |
| **Response length** | *(short/long)* | *(short/long)* |

A worked illustrative example of what this typically looks like is in [`sample_illustrative_run.md`](./sample_illustrative_run.md) — use it as a reference for what to expect, but your submission should reflect your **actual** script output.

<br/>

## 💡 Why CoT + Persona Changed the Result

Direct prompting invites the model to pattern-match against the most statistically common association for a well-known puzzle, producing a tempting-but-incorrect answer with no verification step. Adding "think step-by-step" forces the model to externalize intermediate reasoning — setting up variables and an equation — rather than jumping straight to a final number, which surfaces arithmetic errors before they become the answer. The persona ("senior data analyst... meticulous about arithmetic") reinforces this by priming the model toward careful, detail-checking behavior instead of a quick conversational reply. Together, the two techniques shift the model from fast, intuitive pattern completion toward slower, structured reasoning — which is exactly why CoT improves correctness on problems with a plausible-but-wrong shortcut answer.

<br/>

## 📂 Project Structure

```
cot-persona-demo/
│
├── cot_vs_plain.py            # Runs both prompts, saves comparison_results.md
├── sample_illustrative_run.md  # Reference example of expected before/after pattern
├── comparison_results.md       # Auto-generated after running the script (your real results)
├── requirements.txt
└── README.md
```

<br/>

## 🩹 Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'openai'` | `pip install -r requirements.txt` |
| `AuthenticationError` / `401` | Re-check your `OPENROUTER_API_KEY` env variable |
| `429 Too Many Requests` | Free model rate-limited — wait a minute and retry |
| Both runs give the same correct answer | Try a smaller/weaker free model — stronger models sometimes get this right even without CoT, which is itself worth noting in your write-up |

<br/>

## 📄 License

Released under the **MIT License**.

<br/>

<div align="center">
<img src="https://placehold.co/1200x150/0a5c36/ffffff?text=Built+for+Neurofive+Solutions&font=montserrat" alt="Neurofive Footer Banner" width="100%"/>
</div>
