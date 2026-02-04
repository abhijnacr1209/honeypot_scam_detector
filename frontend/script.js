const chatBox = document.getElementById("chatBox");
const input = document.getElementById("messageInput");

// Create or reuse session id
let sessionId = localStorage.getItem("session_id");
if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);
}

function addMessage(text, className) {
    const div = document.createElement("div");
    div.className = `message ${className}`;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "scammer");
    input.value = "";

    const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message: message,
            session_id: sessionId
        })
    });

    const data = await res.json();
    addMessage(data.reply || "No response", "sharma");
}

input.addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
});
