import sys
import argparse
from flask import Flask, render_template, request, jsonify
from chatbot_logic import BasicChatbot

app = Flask(__name__)
bot = BasicChatbot(name="Aura")

@app.route("/")
def index():
    return render_template("index.html", bot_name=bot.name)

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"reply": "Please enter a message.", "intent": "empty"}), 400
    
    response = bot.get_response(message)
    return jsonify(response)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_cli():
    print("=" * 55)
    print(f"[*] Welcome to {bot.name} CLI Chatbot!")
    print("Type your message and press Enter.")
    print("Type 'exit' or 'quit' to end the session.")
    print("=" * 55)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print(f"\n{bot.name}: Goodbye! Have a great day!\n")
                break
            
            result = bot.get_response(user_input)
            print(f"\n{bot.name}: {result['reply']}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{bot.name}: Session ended. Bye!")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic Chatbot Server or CLI")
    parser.add_argument("--cli", action="store_true", help="Run the chatbot in CLI / terminal mode")
    parser.add_argument("--port", type=int, default=5000, help="Web server port (default: 5000)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Web server host (default: 127.0.0.1)")
    
    args = parser.parse_args()
    
    if args.cli:
        run_cli()
    else:
        print(f"Starting {bot.name} Web Chatbot on http://{args.host}:{args.port}")
        app.run(host=args.host, port=args.port, debug=False)
