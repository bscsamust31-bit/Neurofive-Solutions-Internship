# Sample Illustrative Run (for reference only)

> ⚠️ This file shows the **typical pattern** this experiment is designed to surface,
> based on how models commonly answer this well-studied problem. It is here so you
> understand what to look for. **Your actual submission must use the real output
> from running `cot_vs_plain.py` against a live OpenRouter model** — paste those
> real results into `comparison_results.md` (auto-generated when you run the script).

## The Problem

> A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball.
> How much does the ball cost?

**Correct answer:** $0.05

---

## Run A — Plain Prompt (Before)

**Prompt:**
```
A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball.
How much does the ball cost?
```

**Typical response pattern:**
> The ball costs $0.10.

This is the classic *intuitive-but-wrong* answer. $0.10 + $1.00 = $1.10 "feels"
right at a glance, but it violates the actual condition: if the ball is $0.10,
the bat (at "$1.00 more") would be $1.10, making the total $1.20 — not $1.10.
Weaker or free-tier models answering in a single fast pass are prone to
reproducing this exact error because it's the statistically "obvious" answer
seen constantly in training data discussions of this puzzle.

---

## Run B — Chain-of-Thought + Persona (After)

**Persona (system prompt):**
```
You are a senior data analyst who is meticulous about arithmetic and never
skips a step when solving a quantitative problem.
```

**Prompt:**
```
A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball.
How much does the ball cost?

Think step-by-step before answering. Show your reasoning first, then clearly
state your final answer on the last line as 'Final Answer: ...'
```

**Typical response pattern:**
```
Let the ball's price = x
Then the bat's price = x + 1.00

Total: x + (x + 1.00) = 1.10
2x + 1.00 = 1.10
2x = 0.10
x = 0.05

Check: ball = $0.05, bat = $1.05, total = $1.10 ✓

Final Answer: The ball costs $0.05.
```

By being forced to set up the algebra explicitly instead of pattern-matching
to the "obvious" number, the model self-corrects and lands on the right answer.

---

## Why CoT + Persona Changed the Result (write-up)

Direct prompting invites the model to pattern-match against the most
statistically common association for this well-known puzzle, producing the
tempting-but-incorrect $0.10 answer without any verification step. Adding
"think step-by-step" forces the model to externalize intermediate reasoning —
setting up variables and an equation — rather than jumping straight to a
final number, which surfaces the arithmetic error before it becomes the
answer. The persona ("senior data analyst... meticulous about arithmetic")
reinforces this by priming the model toward a checking, detail-oriented
behavior pattern rather than a quick conversational one. Together, the two
techniques shift the model from fast, intuitive "System 1" pattern completion
toward slower, structured "System 2" reasoning — which is exactly why CoT
improves correctness on problems with a plausible-but-wrong shortcut answer.
