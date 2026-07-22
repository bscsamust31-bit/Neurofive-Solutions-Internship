<p align="center">
  <img src=".\banner.png" width="160" height="160" style="border-radius:50%; object-fit:cover;" alt="NeuroFive Solutions"/>
</p>

# NeuroFive Internship — Task 3
### Multi-Agent Basics — Two AIs Working Together

![Task](https://img.shields.io/badge/Task-Multi--Agent%20Orchestration-1b4d34?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-2e7d32?style=for-the-badge)
![Pipeline](https://img.shields.io/badge/Pipeline-Writer%20→%20Editor-123825?style=for-the-badge)
![Tool](https://img.shields.io/badge/Tool-Claude%20API-c9a24b?style=for-the-badge)

**Submitted by:** Chashman Aslam · Multan University of Science and Technology (MUST)

---

## 📋 Task Checklist

| # | Requirement | Status |
|---|---|:---:|
| 1 | Design a 2-agent pipeline (Writer → Editor/Critic) | ✅ Done |
| 2 | Build it (manual two-step API chain) | ✅ Live interactive tool built |
| 3 | Give each agent a distinct system prompt/persona | ✅ Done |
| 4 | Run on 2 different topics | ✅ Both run live below |
| 5 | Compare final (post-Editor) vs raw Agent 1 draft | ✅ Side-by-side below |
| 6 | Note what the Editor agent actually improved | ✅ Editor's Notes per run |

---

## 📌 Overview

2026's biggest shift in AI is moving from "one prompt, one answer" to **teams of specialized agents collaborating on a task** — agentic / multi-agent orchestration. This task builds a small two-agent system: **Agent 1 (Writer)** drafts content on a topic, and **Agent 2 (Editor/Critic)** reviews and refines that draft — with Agent 1's output becoming Agent 2's input, no human editing in between.

Built as a **manual two-step API chain** (rather than a LangChain framework) to keep the mechanics fully transparent: one API call produces the draft, its raw output is passed directly into a second API call with a different system prompt.

---

## 🧩 Pipeline Design

```
   ┌─────────────┐        draft        ┌──────────────────┐
   │   AGENT 1   │  ─────────────────▶ │      AGENT 2      │
   │   Writer    │                      │  Editor / Critic  │
   └─────────────┘                      └──────────────────┘
         │                                        │
    first-pass draft                    refined final + notes
```

### Agent 1 — Writer

**System prompt / persona:**
```text
You are the Writer agent in a two-agent content pipeline. Your job is
to produce a solid FIRST DRAFT on the given topic — clear ideas,
reasonable structure, roughly 120-180 words. Don't over-polish; focus
on getting the substance right. Write in plain prose, no headers.
```

**Responsibility:** Get the ideas down fast and correctly. Not expected to be polished — that's the next agent's job.

### Agent 2 — Editor / Critic

**System prompt / persona:**
```text
You are the Editor/Critic agent in a two-agent content pipeline. You
receive a draft written by the Writer agent. Improve it: tighten
language, strengthen the opening and closing, fix weak transitions,
cut redundancy, improve structure — without changing the core facts
or claims. Respond with ONLY valid JSON: {"revised": "...", "notes":
["change 1", "change 2", "change 3"]}
```

**Responsibility:** Never just validate — genuinely improve structure, tone, and clarity while preserving the facts Agent 1 established. Also required to self-report what it changed, via the `notes` field.

**How the handoff works:** Agent 1's raw text output is inserted directly into Agent 2's user message ("Here is the Writer agent's draft: ...") — no human touches it in between. Agent 2's structured JSON response is parsed to separate the revised text from its change notes.

---

## 🧪 Run 1 — Topic: "Why remote work is here to stay"

### Agent 1 Draft (raw, unedited)

> Remote work isn't just a pandemic trend anymore — it's actually stuck around because it works for a lot of people. Companies figured out that productivity didn't really drop when people worked from home, and in some cases it went up. Employees like it because they save time and money not commuting, and they have more control over their schedule. Also company can hire from anywhere now, not just people who live near the office, which is a big win for finding good talent. Sure there are downsides like less spontaneous collaboration and some people feel isolated, but companies are adapting by doing hybrid setups and better tools for staying connected. Bottom line, remote work solved real problems for both sides so it's not going away.

### Agent 2 Final (post-Editor)

> Remote work isn't a pandemic-era relic — it has staying power because it solves real problems for both employers and employees.
>
> For companies, the data settled the debate: productivity didn't drop when people left the office, and in many cases it rose. Remote hiring also opened access to talent far beyond commuting distance, letting businesses hire the best person for the job rather than the best person nearby.
>
> For employees, the appeal is just as concrete — no commute, more schedule control, and better work-life balance.
>
> Yes, remote work has real trade-offs: less spontaneous collaboration, and isolation for some. But hybrid models and better connection tools are closing that gap, not eliminating remote work.
>
> The reason remote work is here to stay isn't sentiment — it's that it solved genuine problems for both sides of the table.

### 📝 What the Editor Actually Improved

- Reordered points into **employer benefits vs. employee benefits** for a clearer, scannable structure (the draft mixed both together)
- Cut casual filler ("Sure there are downsides," "Bottom line") for a more polished, professional tone
- Strengthened the opening and closing lines so they bookend the same argument — the draft's ending felt tacked-on
- Preserved every factual claim — no new information added, nothing removed

---

## 🧪 Run 2 — Topic: "How photosynthesis works"

### Agent 1 Draft (raw, unedited)

> Photosynthesis is how plants make their own food using sunlight. It happens mostly in the leaves, in little structures called chloroplasts. The plant takes in carbon dioxide from the air through tiny holes called stomata, and absorbs water through its roots. Using sunlight energy, the plant converts the CO2 and water into glucose, which is basically sugar the plant uses for energy, and it also releases oxygen as a byproduct which is important for us to breathe. This whole process depends on a green pigment called chlorophyll which is what actually captures the sunlight. Photosynthesis is important because it's basically the base of almost every food chain on earth.

### Agent 2 Final (post-Editor)

> Photosynthesis is how plants make their own food using sunlight — a process that quietly powers nearly every food chain on Earth.
>
> It happens mainly in the leaves, inside structures called chloroplasts, where a green pigment called chlorophyll captures light energy. The plant draws in carbon dioxide through tiny pores called stomata and pulls water up through its roots. Using the captured sunlight, it converts these two ingredients — CO2 and water — into glucose, the sugar that fuels the plant, releasing oxygen as a byproduct in the process.
>
> That oxygen is the same oxygen we breathe, which is what makes photosynthesis foundational not just for plants, but for nearly all life on the planet.

### 📝 What the Editor Actually Improved

- Moved the "base of the food chain" significance to the **opening line**, so the reader knows why this matters before the mechanism (the draft buried this at the very end)
- Tied chlorophyll's role directly to light capture at the point it's first mentioned, instead of tacking it on as an afterthought
- Connected "oxygen as byproduct" to "oxygen we breathe" more explicitly, landing the human-relevance point instead of leaving it implicit
- Trimmed repetitive filler phrasing ("which is important," "which is basically") for tighter, more confident prose

---

## 📊 Comparison Summary

| | Run 1: Remote Work | Run 2: Photosynthesis |
|---|---|---|
| **Draft length** | ~130 words | ~125 words |
| **Final length** | ~140 words | ~120 words |
| **Structural change** | Reordered into two clear categories | Moved key significance to the opening |
| **Tone change** | Casual → professional | Explanatory → confident/precise |
| **Facts altered?** | No — same claims, better organized | No — same facts, better flow |

**Consistent pattern across both runs:** the Editor agent never invented new content — it reorganized for clarity, moved the most important point earlier, and cut casual/redundant phrasing. That's a meaningfully different job from Agent 1's, which is exactly the point of splitting them into two agents rather than asking one model to draft-and-polish in a single pass.

---

## 📁 Deliverables

| File | Description |
|---|---|
| `README.md` | This file — pipeline design, both full runs, and comparison |
| `agent_pipeline.jsx` | Interactive live version — pick a topic, watch both agents run in sequence |

---

## 🛠️ Tool Used

- **Claude** (Anthropic) — both agents run as chained API calls with distinct system prompts

---

<sub>NeuroFive Solutions — Internship Program</sub>
