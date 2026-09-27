import re
import datetime
import random
import ast
import operator

class BasicChatbot:
    def __init__(self, name="Aura"):
        self.name = name
        self.setup_intents()

    def setup_intents(self):
        self.jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the computer go to the doctor? Because it had a virus!",
            "There are only 10 kinds of people in the world: those who understand binary, and those who don't.",
            "Why was the JavaScript developer sad? Because they didn't Node how to Express themselves.",
            "What is an algorithm? A word used by programmers when they don't want to explain what they did."
        ]

        self.facts = [
            "The first computer programmer was Ada Lovelace in the 1840s.",
            "The term 'bug' in computer science was popularized when a real moth was found inside the Harvard Mark II computer in 1947.",
            "Python was named after the British comedy series 'Monty Python's Flying Circus', not the snake!",
            "More than 90% of the world's currency exists only on computers."
        ]

    def safe_calculate(self, expression_str):
        """Safely evaluates basic arithmetic expressions (+, -, *, /, %, **)."""
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
        }

        def eval_node(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            elif isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                op_type = type(node.op)
                if op_type in operators:
                    if op_type == ast.Div and right == 0:
                        raise ZeroDivisionError("Division by zero")
                    return operators[op_type](left, right)
            elif isinstance(node, ast.UnaryOp):
                operand = eval_node(node.operand)
                op_type = type(node.op)
                if op_type in operators:
                    return operators[op_type](operand)
            raise ValueError("Unsupported expression")

        try:
            # Clean up query
            cleaned = expression_str.replace("^", "**").strip()
            tree = ast.parse(cleaned, mode='eval')
            result = eval_node(tree.body)
            # Format nicely
            if isinstance(result, float) and result.is_integer():
                return int(result)
            return round(result, 4)
        except Exception:
            return None

    def get_response(self, user_message: str) -> dict:
        text = user_message.strip()
        if not text:
            return {
                "reply": "It looks like you sent an empty message. Ask me anything!",
                "intent": "empty"
            }

        lower_text = text.lower().strip()

        # 1. Greetings
        if re.search(r'\b(hello|hi|hey|hiya|greetings|howdy|good\s*(morning|afternoon|evening))\b', lower_text):
            responses = [
                f"Hello! I'm {self.name}, your friendly assistant. How can I help you today?",
                f"Hey there! Great to see you. What's on your mind?",
                f"Hi! How can I assist you today?"
            ]
            return {"reply": random.choice(responses), "intent": "greeting"}

        # 2. Farewells
        if re.search(r'\b(bye|goodbye|see you|cya|farewell|take care|have a good day)\b', lower_text):
            responses = [
                "Goodbye! Have a fantastic day ahead!",
                "See you later! Feel free to return if you have more questions.",
                "Take care! It was a pleasure chatting with you."
            ]
            return {"reply": random.choice(responses), "intent": "farewell"}

        # 3. How are you / status
        if re.search(r'\b(how are you|how do you do|how\'?s it going|what\'?s up|how are things)\b', lower_text):
            responses = [
                "I'm running smoothly and feeling great! How are you doing?",
                "All systems operational! Ready to assist you. How is your day going?",
                "Doing wonderful, thank you for asking! What can I do for you today?"
            ]
            return {"reply": random.choice(responses), "intent": "status"}

        # 4. Identity / About
        if re.search(r'\b(who are you|what is your name|what are you|what can you do|your purpose|who created you|who made you)\b', lower_text):
            reply = (
                f"I am {self.name}, a basic intelligent chatbot!\n\n"
                "Here are a few things I can do for you:\n"
                "• Answer basic conversational questions\n"
                "• Tell the current date and time (`What time is it?`)\n"
                "• Solve math problems (`Calculate 45 * 12 + 8`)\n"
                "• Share funny jokes (`Tell me a joke`)\n"
                "• Share fun tech facts (`Tell me a fact`)\n"
                "• Provide help and guidance (`help`)"
            )
            return {"reply": reply, "intent": "about"}

        # 5. Help
        if re.search(r'\b(help|commands|options|what to ask)\b', lower_text):
            reply = (
                "Here are some example prompts you can try:\n"
                "• 'Hello' or 'Good morning'\n"
                "• 'What time is it?' or 'What is today's date?'\n"
                "• 'Calculate (25 * 4) + 15'\n"
                "• 'Tell me a joke'\n"
                "• 'Tell me a cool fact'\n"
                "• 'Who are you?'"
            )
            return {"reply": reply, "intent": "help"}

        # 6. Current Time & Date
        if re.search(r'\b(time|date|day|clock|current time|today\'?s date)\b', lower_text):
            now = datetime.datetime.now()
            if "time" in lower_text:
                time_str = now.strftime("%I:%M %p")
                return {"reply": f"The current time is **{time_str}**.", "intent": "time"}
            elif "date" in lower_text or "day" in lower_text:
                date_str = now.strftime("%A, %B %d, %Y")
                return {"reply": f"Today is **{date_str}**.", "intent": "date"}
            else:
                formatted = now.strftime("%A, %B %d, %Y at %I:%M %p")
                return {"reply": f"Right now it's **{formatted}**.", "intent": "datetime"}

        # 7. Math & Calculations
        # Check if the user asks to calculate or if message is mostly an arithmetic expression
        calc_match = re.search(r'(?:calculate|what is|solve|evaluate)?\s*([0-9\.\s\+\-\*\/\(\)\^\%]+)', lower_text)
        if calc_match and any(op in calc_match.group(1) for op in ['+', '-', '*', '/', '%', '^']):
            math_candidate = calc_match.group(1).strip()
            # Verify candidate has numbers and at least one operator
            if re.search(r'\d', math_candidate):
                result = self.safe_calculate(math_candidate)
                if result is not None:
                    return {
                        "reply": f"**Result:** `{math_candidate}` = **{result}**",
                        "intent": "math"
                    }

        # 8. Jokes
        if re.search(r'\b(joke|funny|make me laugh|humor)\b', lower_text):
            return {"reply": random.choice(self.jokes), "intent": "joke"}

        # 9. Facts / Trivia
        if re.search(r'\b(fact|trivia|tell me something interesting|cool fact)\b', lower_text):
            return {"reply": random.choice(self.facts), "intent": "fact"}

        # 10. Politeness / Thanks
        if re.search(r'\b(thank|thanks|thank you|awesome|great job|cool|appreciate it)\b', lower_text):
            responses = [
                "You're very welcome! Happy to help anytime.",
                "Glad I could help! Let me know if you need anything else.",
                "Anytime! I'm here if you have more questions."
            ]
            return {"reply": random.choice(responses), "intent": "thanks"}

        # 11. Weather (simulated)
        if re.search(r'\b(weather|temperature|forecast|is it raining)\b', lower_text):
            return {
                "reply": "I don't have live satellite sensors hooked up yet, but I predict 100% chance of smooth coding today! ☀️",
                "intent": "weather"
            }

        # Fallback
        fallback_replies = [
            f"I'm not quite sure how to answer that yet. You can ask me for the **time**, to **solve a math problem**, or to **tell a joke**! Type `help` for more.",
            f"Hmm, I didn't catch that. Try asking me something like 'What can you do?' or 'Tell me a fact'.",
            f"That's an interesting question! As a basic chatbot, I'm still learning. Try typing `help` to see what I can do."
        ]
        return {
            "reply": random.choice(fallback_replies),
            "intent": "fallback"
        }
