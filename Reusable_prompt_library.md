<p align="center">
  <img src=".\banner.png" width="160" height="160" style="border-radius:50%; object-fit:cover;" alt="NeuroFive Solutions"/>
</p>

# NeuroFive Internship — Task 2
### Build Your First Reusable Prompt Library

![Task](https://img.shields.io/badge/Task-Prompt%20Library-1b4d34?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-2e7d32?style=for-the-badge)
![UseCase](https://img.shields.io/badge/Use%20Case-Customer%20Support%20Replies-123825?style=for-the-badge)

**Submitted by:** Chashman Aslam · Multan University of Science and Technology (MUST)

---

## 📌 Overview

Professional prompt engineers don't rewrite prompts from scratch every time — they build **reusable templates** with placeholders, the same way developers write functions instead of copy-pasting code.

This task documents **Prompt Library v1**: a single reusable prompt template for **Customer Support Replies**, instantiated into 5 real, distinct scenarios, tested live, with actual outputs captured below.

---

## 🎯 Use Case Chosen

**Customer Support Email Replies** — chosen because it's a high-frequency, high-stakes writing task where consistency, tone control, and speed all matter. A well-built template here saves real time in a real job, not just in a classroom exercise.

---

## 🧩 The Reusable Template

Every prompt in this library follows the exact same 5-part skeleton. Only the bracketed variables change between uses — the structure itself never does.

```text
ROLE: You are a [job title] at [company/product].

CONTEXT: [Customer's situation — what happened, relevant background,
their emotional state or urgency]

TASK: [Exactly what to write — e.g., "write a reply that acknowledges
X and offers Y"]

FORMAT: [Length, structure, greeting/sign-off requirements, whether
to use bullet points or numbered steps]

CONSTRAINTS: [Tone rules, what must be included, what must be avoided,
policy limits — e.g., don't promise exact dates, don't sound scripted]
```

**Why this structure works:**
- **Role** anchors the voice and level of authority in the reply
- **Context** feeds in the specific situation so the reply isn't generic
- **Task** removes ambiguity about what output is actually expected
- **Format** controls length and structure so replies are consistent and easy to send as-is
- **Constraints** enforces tone and policy boundaries — the guardrails that keep AI output safe to send without heavy editing

---

## 📚 Prompt Library v1 — 5 Instantiations

Each of the 5 prompts below uses the **exact same template**, with only the Role/Context/Task/Format/Constraints variables swapped for a different real-world scenario. All 5 were run live and the actual outputs are included, unedited.

---

### 1️⃣ Late Delivery — Apology + Goodwill Gesture

**Prompt:**
```text
ROLE: You are a customer support specialist at ShopEase, an online
retail company.

CONTEXT: A customer named Sarah ordered a laptop bag 3 days ago that
was expected to arrive yesterday but hasn't shown up yet. She emailed
frustrated, saying she needs it for a work trip tomorrow.

TASK: Write a reply that acknowledges the delay, apologizes sincerely,
and offers a solution.

FORMAT: Email format, 100-150 words, with a subject line, greeting,
and sign-off.

CONSTRAINTS: Warm and empathetic tone. Do not promise an exact delivery
time unless verified. Offer a discount code or expedited shipping as
a goodwill gesture. No corporate jargon.
```

**Output:**
> **Subject: Following Up on Your Order — We're On It**
>
> Hi Sarah,
>
> I'm really sorry your laptop bag hasn't arrived yet, especially with your trip coming up tomorrow — I know how stressful that timing is.
>
> I've flagged your order for priority tracking right now so we can get you an update as soon as possible. In the meantime, I've added code **RUSH15** for 15% off your next order as an apology for the inconvenience, and I'm looking into expedited shipping options to see if we can get this to you faster.
>
> I'll follow up within the next few hours with a concrete update. Thank you for your patience, Sarah.
>
> Warmly,
> Alex
> ShopEase Customer Support

---

### 2️⃣ Billing Error — Duplicate Charge

**Prompt:**
```text
ROLE: You are a billing support agent at FinTrack, a subscription-based
expense tracking app.

CONTEXT: A customer named Ahmed was charged twice for his monthly
subscription ($9.99 x2) due to a payment processing glitch. He's
worried about being charged again next month.

TASK: Write a reply confirming the duplicate charge, explaining the
refund process, and reassuring him about future billing.

FORMAT: Email format, 100-130 words, clear structure with a short
bullet list of next steps.

CONSTRAINTS: Reassuring, professional tone. Must state the refund
timeline (3-5 business days). Avoid blaming the customer or sounding
overly technical.
```

**Output:**
> **Subject: Your Duplicate Charge — Refund Confirmed**
>
> Hi Ahmed,
>
> Thanks for flagging this, and sorry for the confusion. I checked your account and confirmed you were charged twice ($9.99 x2) due to a processing glitch on our end.
>
> Here's what happens next:
> - The duplicate charge has been refunded to your original payment method
> - You'll see it reflected within 3–5 business days
> - Your subscription itself is unaffected — no action needed from you
>
> I've also flagged your account so this doesn't happen again next billing cycle. If the refund doesn't show up by early next week, just reply here and I'll follow up directly.
>
> Best,
> Layla
> FinTrack Billing Support

---

### 3️⃣ Product Defect — Replacement or Refund

**Prompt:**
```text
ROLE: You are a customer care representative at HomeGlow, a home
appliances brand.

CONTEXT: A customer named Maria received a blender that stopped
working after 2 uses. She's requesting either a replacement or a
full refund and is a repeat customer.

TASK: Write a reply offering both options (replacement or refund),
and outline the return process.

FORMAT: Email format, 120-150 words, with a numbered list for the
return process.

CONSTRAINTS: Empathetic but efficient tone. Must acknowledge her
loyalty as a repeat customer. Include return instructions clearly.
Do not sound scripted.
```

**Output:**
> **Subject: Let's Fix This For You, Maria**
>
> Hi Maria,
>
> I'm sorry to hear your blender stopped working after just two uses — that's not the experience we want for a customer who's been with us as long as you have, and I appreciate you giving us the chance to make it right.
>
> You have two options:
> 1. **Replacement** — we'll ship a new unit right away, at no cost to you
> 2. **Full refund** — processed back to your original payment method
>
> To get started:
> 1. Reply with your preferred option
> 2. We'll email you a prepaid return label
> 3. Once the item ships back, your replacement or refund goes out within 2 business days
>
> Thank you for your continued trust in HomeGlow, Maria — we'll get this sorted quickly.
>
> Best,
> Omar
> HomeGlow Customer Care

---

### 4️⃣ General How-To Question

**Prompt:**
```text
ROLE: You are a friendly support agent at CloudNote, a note-taking app.

CONTEXT: A new user, Jason, emailed asking how to enable dark mode
and sync notes across devices.

TASK: Write a reply with clear step-by-step instructions for both
features.

FORMAT: Email format, 100-140 words, using two short numbered lists
(one per feature).

CONSTRAINTS: Friendly, concise tone. No unnecessary preamble. Assume
the user is not very technical.
```

**Output:**
> **Subject: Dark Mode + Syncing — Here's How!**
>
> Hi Jason,
>
> Great questions — both are easy to set up!
>
> **Dark Mode:**
> 1. Open Settings (gear icon, top right)
> 2. Tap "Appearance"
> 3. Select "Dark"
>
> **Sync Across Devices:**
> 1. Go to Settings > Account
> 2. Sign in with the same email on each device
> 3. Toggle "Auto-Sync" on
>
> Your notes should sync within a few seconds of connecting. Let me know if you run into anything!
>
> Cheers,
> Sam
> CloudNote Support

---

### 5️⃣ Positive Review — Thank You + Soft Referral

**Prompt:**
```text
ROLE: You are a customer engagement specialist at Brewly, a specialty
coffee subscription service.

CONTEXT: A customer named Priya left a 5-star review praising the
flavor variety and fast shipping, and mentioned she's already
recommended Brewly to friends.

TASK: Write a warm thank-you reply that acknowledges her specific
praise and gently encourages her to share her referral code.

FORMAT: Short reply, 60-90 words, casual and appreciative tone, no
formal greeting/sign-off needed (review-reply style).

CONSTRAINTS: Genuine, not salesy. Mention the referral program only
briefly, not pushy. Use her name.
```

**Output:**
> Hi Priya, thank you so much for this — it genuinely made our day! We're so glad the flavor variety hit the mark, and getting it to you quickly is exactly what we aim for. Recommending us to friends means the world to us, truly. If they ever sign up, don't forget you've got a referral code waiting to earn you both a little something extra. Thanks again for being part of the Brewly community! ☕

---

## 📊 Library Summary

| # | Scenario | Tone | Length Target | Special Requirement |
|---|---|---|---|---|
| 1 | Late delivery | Empathetic, urgent | 100–150 words | Goodwill gesture required |
| 2 | Billing error | Reassuring, calm | 100–130 words | Bullet list + refund timeline |
| 3 | Product defect | Empathetic, efficient | 120–150 words | Two clear options + numbered steps |
| 4 | How-to question | Friendly, concise | 100–140 words | Two numbered instruction sets |
| 5 | Positive review | Warm, genuine | 60–90 words | Soft referral mention only |

---

## 💡 Why This Matters

Rewriting a support reply prompt from scratch every time costs time and produces inconsistent tone across a team. This template turns that into a **fill-in-the-blank operation**: swap five variables, get a polished, on-brand reply in seconds — whether the situation is a shipping delay, a billing glitch, or a five-star review. That's the actual promise of "reusable prompts": not saving typing, but **saving judgment calls** by encoding them once into a structure everyone can reuse.

---

## 📁 Deliverables

| File | Description |
|---|---|
| `README.md` | This file — full prompt library write-up |
| `Prompt_Library_v1.pdf` | Polished PDF version of this library |
| Video (LinkedIn) | 2–3 min walkthrough of the template + live demo of 2 of the 5 prompts  |

---

## 🛠️ Tool Used

- **Claude** (Anthropic) — all 5 prompts tested live, outputs captured unedited

---

<sub>NeuroFive Solutions — Internship Program</sub>
