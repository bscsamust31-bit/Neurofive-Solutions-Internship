<p align="center">
  <img src="./banner.png" width="160" height="160" style="border-radius:50%; object-fit:cover;" alt="NeuroFive Solutions"/>
</p>

# NeuroFive Internship — Task 1
### Prompt Basics: Zero-Shot vs Few-Shot Showdown

![Task](https://img.shields.io/badge/Task-Prompt%20Engineering-1b4d34?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-2e7d32?style=for-the-badge)
![Tools](https://img.shields.io/badge/Tools-ChatGPT%20%7C%20Claude%20%7C%20Gemini-123825?style=for-the-badge)

**Submitted by:** Chashman Aslam · Multan University of Science and Technology (MUST)

---

## 📌 Overview

This repository documents **Task 1** of the NeuroFive Solutions internship: a hands-on comparison of **zero-shot** vs **few-shot** prompting for a real classification problem — sorting customer support messages into `Complaint`, `Question`, or `Praise`.

The goal was to *feel* how much prompt wording changes model behavior by running the **same 10 messages** through **the same instruction**, once with no examples and once with three labeled examples, across **three different AI tools**: ChatGPT, Claude, and Gemini.

---

## 🎯 Objective

- Pick a real classification problem (customer support triage)
- Write a zero-shot prompt and run it across multiple LLMs
- Write a few-shot prompt (instruction + labeled examples) and run the same messages again
- Compare accuracy in a results table
- Draw a conclusion on *why* one approach outperformed the other

---

## 🗂️ Test Dataset

Ten realistic customer messages were curated to cover all three categories, including **two deliberately mixed-tone messages** (#7 and #10) designed to stress-test whether a model judges *overall intent* or just grabs onto surface keywords.

| # | Message | Intended Label |
|---|---|---|
| 1 | "My order arrived 3 days late and the box was crushed." | 🔴 Complaint |
| 2 | "How do I reset my password?" | 🔵 Question |
| 3 | "Absolutely love this product, best purchase this year!" | 🟢 Praise |
| 4 | "This is the second time my payment failed, very frustrating." | 🔴 Complaint |
| 5 | "Do you ship to Pakistan?" | 🔵 Question |
| 6 | "Your support team fixed my issue in 5 minutes, amazing!" | 🟢 Praise |
| 7 | "I was charged twice for the same order — can someone explain why?" | 🔴 Complaint |
| 8 | "What's your return policy?" | 🔵 Question |
| 9 | "The app keeps crashing every time I open it." | 🔴 Complaint |
| 10 | "Just wanted to say your customer service is top notch, though I wish response times were a bit faster." | 🟢 Praise |

> Messages #7 and #10 mix sentiment on purpose — one is a complaint phrased as a question, the other is praise with a minor gripe — to see whether each prompting style captures the *dominant* intent.

---

## 🧪 Methodology

### 1️⃣ Zero-Shot Prompt

Instruction only — no examples given:

```text
Classify each of the following customer messages as "Complaint", "Question", or "Praise".
Just give the label for each one.

1. My order arrived 3 days late and the box was crushed.
2. How do I reset my password?
3. Absolutely love this product, best purchase this year!
4. This is the second time my payment failed, very frustrating.
5. Do you ship to Pakistan?
6. Your support team fixed my issue in 5 minutes, amazing!
7. I was charged twice for the same order — can someone explain why?
8. What's your return policy?
9. The app keeps crashing every time I open it.
10. Just wanted to say your customer service is top notch, though I wish response times were a bit faster.
```

### 2️⃣ Few-Shot Prompt

Instruction + 3 labeled examples (plus 2 extra examples showing how to resolve mixed tone):

```text
Classify each customer message as "Complaint", "Question", or "Praise".
Use the PRIMARY tone/intent of the message, even if it's mixed.

Examples:
"My package never arrived." → Complaint
"What time does support open?" → Question
"You guys are amazing, thank you!" → Praise
"I love the product, but shipping was a bit slow." → Praise (mostly positive, minor complaint)
"Why was I charged twice? This needs fixing." → Complaint (question is secondary to the frustration)

Now classify these:
[same 10 messages as above]
```

Both prompts were run **as-is**, with no follow-up corrections, on **ChatGPT**, **Claude**, and **Gemini**.

---

## 📊 Results

### Claude — Detailed Output

| # | Zero-Shot Output | Few-Shot Output |
|---|---|---|
| 1 | Complaint | Complaint |
| 2 | Question | Question |
| 3 | Praise | Praise |
| 4 | Complaint | Complaint |
| 5 | Question | Question |
| 6 | Praise | Praise |
| 7 | ❌ Question *(expected Complaint)* | ✅ Complaint |
| 8 | Question | Question |
| 9 | Complaint | Complaint |
| 10 | ❌ Complaint *(expected Praise)* | ✅ Praise |

**Claude score:** Zero-shot `8/10` → Few-shot `10/10`

Claude's zero-shot mistakes both happened on the mixed-tone messages. Without examples, it leaned on surface cues — the trailing question mark in #7 pulled it toward "Question," and the word *"wish"* in #10 pulled it toward "Complaint." Once given examples that explicitly modeled how to resolve mixed sentiment, it corrected both.

### ChatGPT & Gemini — Detailed Output

Both tools were tested identically and scored a **perfect 10/10 in both conditions** — correctly resolving the mixed-tone messages even without any examples.

| # | ChatGPT Zero-Shot | ChatGPT Few-Shot | Gemini Zero-Shot | Gemini Few-Shot |
|---|---|---|---|---|
| 1–10 | ✅ All correct | ✅ All correct | ✅ All correct | ✅ All correct |

---

## 🏆 Final Accuracy Table

| Tool | Zero-Shot Accuracy | Few-Shot Accuracy |
|---|:---:|:---:|
| **ChatGPT** | 10/10 | 10/10 |
| **Claude** | 8/10 | 10/10 |
| **Gemini** | 10/10 | 10/10 |

---

## 💡 Takeaway

> Across ChatGPT, Claude, and Gemini, **few-shot prompting matched or beat zero-shot in every single case** — it never made results worse. ChatGPT and Gemini were strong enough to correctly resolve the two ambiguous, mixed-tone messages even with zero guidance, scoring 10/10 in both conditions. Claude, however, misread both mixed-tone messages in the zero-shot run, defaulting to surface-level cues like a trailing question mark or the word "wish" rather than judging overall intent — but jumped to a perfect 10/10 once given three labeled examples, including one that explicitly modeled how to resolve mixed sentiment.
>
> This shows that few-shot examples act as an **implicit decision rule**: they don't just repeat the instruction, they teach the model *how* to weigh conflicting signals in a message. This benefit shows up most clearly on the model that needed it — proving few-shot prompting is most valuable exactly where a model's zero-shot judgment is weakest.

---

## 📁 Deliverables

| File | Description |
|---|---|
| `README.md` | This file — full task write-up |
| `Prompt_Basics_Zero-Shot_vs_Few-Shot.pdf` | Polished PDF report with cover page, dataset, prompts, results, and takeaway |
| Video (LinkedIn) | 2–3 min walkthrough of prompts, results, and takeaway  |

---

## 🛠️ Tools Used

- **ChatGPT** (OpenAI)
- **Claude** (Anthropic)
- **Gemini** (Google)

---

<sub>NeuroFive Solutions — Internship Program</sub>
