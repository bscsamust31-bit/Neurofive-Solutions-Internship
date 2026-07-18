"""
Chain-of-Thought + Persona Prompting — Before/After Demo
-----------------------------------------------------------
Runs the SAME reasoning problem two different ways against the same model:

  RUN A ("Before"): a plain, direct prompt — no reasoning instruction, no persona.
  RUN B ("After"):  the same question + "think step-by-step before answering"
                     + a relevant expert persona.

Both answers are printed to the terminal AND saved to comparison_results.md
so you can drop that straight into your write-up / LinkedIn post.

Setup:
    1. Get a free API key: https://openrouter.ai/keys
    2. pip install openai
    3. export OPENROUTER_API_KEY="your-key-here"   (Mac/Linux)
       setx OPENROUTER_API_KEY "your-key-here"      (Windows)
    4. Run:  python cot_vs_plain.py
"""

import os
from datetime import datetime
from openai import OpenAI

# ---------------------------------------------------------------------------
# 1. Client setup (OpenRouter, OpenAI-compatible)
# ---------------------------------------------------------------------------
client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY", "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"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://github.com/",
        "X-Title": "CoT vs Plain Prompting Demo",
    },
)

# Use a free-tier model. Pick a plain/standard chat model on purpose (NOT an
# already-reasoning model like o1 or a "thinking" model) so the difference
# between the two prompting styles is visible and fair.
MODEL = "openrouter/auto-beta"

# ---------------------------------------------------------------------------
# 2. The reasoning problem
# ---------------------------------------------------------------------------
# This is a classic "cognitive reflection" style word problem. It has an
# intuitive-but-WRONG answer that a model (or a person) tends to blurt out
# immediately without thinking, and a correct answer that only shows up if
# you actually work through the algebra step by step. That makes it a great
# stress-test for CoT prompting.

PROBLEM = (
    "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the "
    "ball. How much does the ball cost?"
)
CORRECT_ANSWER = "$0.05 (five cents)"

# ---------------------------------------------------------------------------
# 3. RUN A — plain, direct prompt (no reasoning instruction, no persona)
# ---------------------------------------------------------------------------
PLAIN_PROMPT = PROBLEM

# ---------------------------------------------------------------------------
# 4. RUN B — Chain-of-Thought + Persona prompt
# ---------------------------------------------------------------------------
PERSONA_SYSTEM_PROMPT = (
    "You are a senior data analyst who is meticulous about arithmetic and "
    "never skips a step when solving a quantitative problem."
)

COT_PROMPT = (
    f"{PROBLEM}\n\n"
    "Think step-by-step before answering. Show your reasoning first, then "
    "clearly state your final answer on the last line as 'Final Answer: ...'"
)


def call_model(user_prompt, system_prompt=None):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=500,
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# 5. Run both, print + save a side-by-side comparison
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("CHAIN-OF-THOUGHT + PERSONA PROMPTING — BEFORE / AFTER DEMO")
    print("=" * 70)
    print(f"\nProblem:\n{PROBLEM}")
    print(f"\nKnown correct answer: {CORRECT_ANSWER}")

    print("\n" + "-" * 70)
    print("RUN A — 'BEFORE': plain prompt, no persona, no reasoning instruction")
    print("-" * 70)
    answer_a = call_model(PLAIN_PROMPT)
    print(answer_a)

    print("\n" + "-" * 70)
    print("RUN B — 'AFTER': Chain-of-Thought + Persona prompt")
    print("-" * 70)
    answer_b = call_model(COT_PROMPT, system_prompt=PERSONA_SYSTEM_PROMPT)
    print(answer_b)

    # Save both to a markdown file for your README / LinkedIn post
    with open("comparison_results.md", "w", encoding="utf-8") as f:
        f.write("# Chain-of-Thought + Persona Prompting — Comparison Results\n\n")
        f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
        f.write(f"**Model used:** `{MODEL}`\n\n")
        f.write(f"## Problem\n\n{PROBLEM}\n\n")
        f.write(f"**Known correct answer:** {CORRECT_ANSWER}\n\n")
        f.write("## Run A — Plain Prompt (Before)\n\n")
        f.write(f"**Prompt sent:**\n```\n{PLAIN_PROMPT}\n```\n\n")
        f.write(f"**Model response:**\n\n{answer_a}\n\n")
        f.write("## Run B — Chain-of-Thought + Persona Prompt (After)\n\n")
        f.write(f"**System prompt (persona):**\n```\n{PERSONA_SYSTEM_PROMPT}\n```\n\n")
        f.write(f"**User prompt:**\n```\n{COT_PROMPT}\n```\n\n")
        f.write(f"**Model response:**\n\n{answer_b}\n\n")

    print("\n" + "=" * 70)
    print("Saved full comparison to comparison_results.md")
    print("=" * 70)
