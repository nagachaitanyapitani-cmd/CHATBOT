document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chatForm");
    const userInput = document.getElementById("userInput");
    const chatBody = document.getElementById("chatBody");
    const typingIndicator = document.getElementById("typingIndicator");
    const clearChatBtn = document.getElementById("clearChatBtn");
    const suggestionsContainer = document.getElementById("suggestionsContainer");
    const initialTime = document.getElementById("initialTime");

    // Format current time
    function getFormattedTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    if (initialTime) {
        initialTime.textContent = getFormattedTime();
    }

    // Scroll chat to the bottom
    function scrollToBottom() {
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Format markdown-style bold and code tags for display
    function formatMessageText(text) {
        // Escape HTML
        let formatted = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");

        // Code backticks: `code`
        formatted = formatted.replace(/`([^`]+)`/g, "<code>$1</code>");

        // Bold: **text**
        formatted = formatted.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

        // Bullet points / newlines
        formatted = formatted.replace(/\n/g, "<br>");

        return formatted;
    }

    // Append a message to the chat
    function appendMessage(sender, text) {
        const messageGroup = document.createElement("div");
        messageGroup.className = `message-group ${sender}`;

        const avatar = document.createElement("div");
        avatar.className = `avatar ${sender === "bot" ? "bot-avatar-small" : "user-avatar-small"}`;
        avatar.textContent = sender === "bot" ? "🤖" : "👤";

        const contentDiv = document.createElement("div");
        contentDiv.className = "message-content";

        const bubble = document.createElement("div");
        bubble.className = `bubble ${sender === "bot" ? "bot-bubble" : "user-bubble"}`;
        bubble.innerHTML = formatMessageText(text);

        const timeSpan = document.createElement("span");
        timeSpan.className = "timestamp";
        timeSpan.textContent = getFormattedTime();

        contentDiv.appendChild(bubble);
        contentDiv.appendChild(timeSpan);

        messageGroup.appendChild(avatar);
        messageGroup.appendChild(contentDiv);

        chatBody.appendChild(messageGroup);
        scrollToBottom();
    }

    // Send user message to server
    async function sendMessage(text) {
        const trimmed = text.trim();
        if (!trimmed) return;

        // Append user message
        appendMessage("user", trimmed);
        userInput.value = "";
        userInput.focus();

        // Show typing indicator
        typingIndicator.classList.add("active");
        scrollToBottom();

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: trimmed })
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();

            // Simulate natural typing delay (400ms)
            setTimeout(() => {
                typingIndicator.classList.remove("active");
                appendMessage("bot", data.reply);
            }, 350);

        } catch (error) {
            console.error("Chat error:", error);
            setTimeout(() => {
                typingIndicator.classList.remove("active");
                appendMessage("bot", "⚠️ Oops! Something went wrong while communicating with the server.");
            }, 300);
        }
    }

    // Event listener: Form submit
    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        sendMessage(userInput.value);
    });

    // Event listener: Quick chips
    if (suggestionsContainer) {
        suggestionsContainer.addEventListener("click", (e) => {
            const chip = e.target.closest(".chip");
            if (chip && chip.dataset.msg) {
                sendMessage(chip.dataset.msg);
            }
        });
    }

    // Event listener: Clear conversation
    if (clearChatBtn) {
        clearChatBtn.addEventListener("click", () => {
            chatBody.innerHTML = `
                <div class="message-group bot">
                    <div class="avatar bot-avatar-small">🤖</div>
                    <div class="message-content">
                        <div class="bubble bot-bubble">
                            Chat cleared! Feel free to ask me anything.
                        </div>
                        <span class="timestamp">${getFormattedTime()}</span>
                    </div>
                </div>
            `;
            userInput.focus();
        });
    }
});
