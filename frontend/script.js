// Function to add message to chat box
function addMessage(text, sender) {
    const chatBox = document.getElementById("chatBox");
    const msgDiv = document.createElement("div");

    // Use consistent class names for styling
    msgDiv.className = sender === "user" ? "user-message" : "bot-message";
    msgDiv.innerText = text;

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to send message to backend
async function sendMessage() {
    const input = document.getElementById("messageInput");
    const message = input.value.trim();
    if (!message) return;

    // Show user message
    addMessage(message, "user");
    input.value = "";

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        // Show Mr. Sharma reply
        addMessage(data.reply || "[No reply from backend]", "bot");

    } catch (error) {
        addMessage("[Backend not responding]", "bot");
        console.error(error);
    }
}

// Press Enter to send message
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("messageInput");
    const sendBtn = document.getElementById("sendBtn"); // Make sure your button has this ID

    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    sendBtn.addEventListener("click", sendMessage);
});
