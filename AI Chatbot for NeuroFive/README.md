# Neurofive Solutions Support Assistant — "Nova"

A custom AI chatbot built with a system prompt, running on the **OpenRouter API**
(an OpenAI-compatible endpoint), for the "Build a Custom AI Chatbot" task.

## What it does
Nova is a support-assistant persona for a fictional/example company, **Neurofive
Solutions**. She:
- Only talks about Neurofive products and general tech support
- Politely declines off-topic requests and redirects back to support topics
- Never invents account details she doesn't have
- Stays in character at all times

## Setup

1. **Get a free API key** from OpenRouter: https://openrouter.ai/keys
2. **Install dependencies:**
   ```bash
   pip install openai
   ```
3. **Set your API key** as an environment variable (don't hardcode it or commit it):
   ```bash
   export OPENROUTER_API_KEY="your-key-here"      # Mac/Linux
   setx OPENROUTER_API_KEY "your-key-here"         # Windows (new terminal after)
   ```
4. **Run it:**
   ```bash
   python chatbot.py
   ```

The script will send 5 test messages (including one off-topic "tricky" one) and
print Nova's replies to the console.

## Files
- `chatbot.py` — the full script: client setup, system prompt, chat function, test run
- `requirements.txt` — dependencies
- `README.md` — this file

## Test messages used
1. "Hi, what can you help me with?"
2. "I forgot my password and can't log into my Neurofive dashboard."
3. "Do you offer a free trial of your product?"
4. "Can you write me a poem about my ex-girlfriend instead?" *(off-topic — tests that Nova stays in character)*
5. "Thanks! One more thing — is my data safe with Neurofive?"

## Notes
- Model used: `meta-llama/llama-3.3-70b-instruct:free` via OpenRouter's free tier
  (swap for any free model listed at https://openrouter.ai/models?max_price=0,
  e.g. `google/gemini-2.0-flash-exp:free` or `deepseek/deepseek-chat-v3.1:free`).
- The system prompt is what defines Nova's persona — see `SYSTEM_PROMPT` in
  `chatbot.py`.
- Free OpenRouter models are shared/rate-limited — if you hit a 429 error, wait
  a minute and retry, or switch `MODEL` to a different free option.
