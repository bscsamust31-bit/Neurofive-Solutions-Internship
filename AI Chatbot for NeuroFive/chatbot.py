"""
Neurofive Solutions Support Assistant — Flask Backend
------------------------------------------------------
Run:  python chatbot.py
Then open:  http://localhost:5000
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI

# ---------------------------------------------------------------------------
# 1. Flask app setup
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder=".")
CORS(app)  # allow the HTML frontend to talk to this server

# ---------------------------------------------------------------------------
# 2. OpenRouter client setup (same as original chatbot.py)
# ---------------------------------------------------------------------------
client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY", "Enter your Key here"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://github.com/",
        "X-Title": "Neurofive Solutions Support Assistant",
    },
)

MODEL = "anthropic/claude-sonnet-5"

SYSTEM_PROMPT = """You are Nova, the official virtual support assistant for Neurofive Solutions,
a company that builds AI-powered software products.

Your personality and rules:
1. You are friendly, upbeat, and concise — you sound like a helpful teammate, not a corporate script.
2. You ONLY discuss topics related to Neurofive Solutions: its products, general
   tech support (software issues, account questions, "how do I..." questions),
   and basic AI/tech concepts a customer might ask about.
3. If a user asks something completely unrelated to Neurofive Solutions or tech
   support (e.g. politics, celebrity gossip, medical advice, "write my essay"),
   politely decline and steer the conversation back to how you can help with
   Neurofive Solutions or their tech questions. Never pretend to be a general-purpose assistant.
4. You never make up specific account details, order numbers, or pricing you don't
   actually have — if you don't know something, say so and offer to connect the
   user with a human support agent at support@neurofivesolutions.com.
5. Keep replies short: 2-4 sentences unless the user asks for a detailed walkthrough.
6. Always stay in character as Nova. Never say you are an AI language model or break
   the fourth wall about being built on an underlying LLM.
"""

# ---------------------------------------------------------------------------
# 3. Core function — same logic as original ask_nova()
# ---------------------------------------------------------------------------
def ask_nova(user_message, history=None):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=300,
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# 4. API Routes
# ---------------------------------------------------------------------------

# Serve the HTML frontend
@app.route("/")
def index():
    return send_from_directory(".", "neurofive_chatbot.html")

# Chat endpoint — called by the frontend
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    history = data.get("history", [])  # list of {role, content} dicts

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        reply = ask_nova(user_message, history=history)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------
# 5. Optional: terminal test (same 5 messages as original chatbot.py)
# ---------------------------------------------------------------------------
def run_terminal_test():
    test_messages = [
        "Hi, what can you help me with?",
        "I forgot my password and can't log into my Neurofive dashboard.",
        "Do you offer a free trial of your product?",
        "Can you write me a poem about my ex-girlfriend instead?",
        "Thanks! One more thing — is my data safe with Neurofive?",
    ]
    conversation_history = []
    print("=" * 60)
    print("NEUROFIVE SOLUTIONS SUPPORT ASSISTANT — TERMINAL TEST")
    print("=" * 60)
    for i, msg in enumerate(test_messages, start=1):
        print(f"\n[Test {i}] User: {msg}")
        reply = ask_nova(msg, history=conversation_history)
        print(f"Nova: {reply}")
        conversation_history.append({"role": "user", "content": msg})
        conversation_history.append({"role": "assistant", "content": reply})


# ---------------------------------------------------------------------------
# 6. Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        # python chatbot.py --test  →  runs terminal demo like original
        run_terminal_test()
    else:
        # python chatbot.py  →  starts web server
        print("\n🟢 Nova is running at: http://localhost:5000")
        print("   Open that URL in your browser to use the chatbot.\n")
        app.run(debug=True, port=5000)
