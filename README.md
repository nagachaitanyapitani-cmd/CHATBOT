# 🤖 Aura - Basic Chatbot

A clean, responsive, and extensible chatbot built with **Python (Flask)** and modern web technologies (HTML5, CSS3, JavaScript). It works out of the box both as a **web application** and as a **command-line interface (CLI)**.

---

## ✨ Features

- **Web Chat Interface**: Modern, dark-themed UI with smooth animations and responsive mobile layout.
- **CLI Mode**: Run directly in your terminal with `python app.py --cli`.
- **Natural Intent Recognition**:
  - 👋 **Greetings & Farewells**: Responds naturally to hellos and goodbyes.
  - ⏰ **Date & Time**: Gives real-time clock and calendar updates.
  - 🧮 **Math & Calculations**: Evaluates arithmetic expressions safely (e.g. `(25 * 4) + 15`).
  - 😄 **Jokes & Tech Facts**: Random programmer jokes and computer history facts.
  - ❓ **Help & Guidance**: Tells you what it can do and lists sample queries.
- **Interactive UX**:
  - Quick-reply suggestion chips.
  - Simulated typing indicator.
  - One-click clear conversation history.
  - Auto-scroll and formatted markdown preview (bold text & inline code).

---

## 🚀 Getting Started

### 1. Installation

Make sure you have Python 3 installed. Install the dependencies (Flask):

```bash
pip install -r requirements.txt
```

### 2. Run the Web Chatbot

Start the Flask server:

```bash
python app.py
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

### 3. Run in Terminal (CLI Mode)

If you prefer using the terminal directly:

```bash
python app.py --cli
```

Type `exit` or `quit` when you're done.

---

## 📁 Project Structure

```
Chatbot/
├── app.py                 # Flask server and CLI runner
├── chatbot_logic.py       # Core intent matching and logic engine
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
├── templates/
│   └── index.html         # Web chat interface
└── static/
    ├── style.css          # Modern dark styling
    └── script.js          # Interactive chat UI script
```

---

## 🛠️ How to Customize

- **Add custom intents & responses**: Open [chatbot_logic.py](file:///c:/Users/yadav/Desktop/Chatbot/chatbot_logic.py) and add new keyword patterns or responses in `get_response()`.
- **Change Bot Name**: Change `name="Aura"` in `BasicChatbot(name="...")` inside [app.py](file:///c:/Users/yadav/Desktop/Chatbot/app.py).
- **Styling**: Modify [style.css](file:///c:/Users/yadav/Desktop/Chatbot/static/style.css) to customize the color palette or UI components.
