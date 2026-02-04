const chatBox = document.getElementById("messages");
const input = document.getElementById("user-input");

// Create or reuse session id
let sessionId = localStorage.getItem("session_id");
if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);
}

function addMessage(text, className) {
    const div = document.createElement("div");
    div.className = `msg ${className}`;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "scammer");
    input.value = "";

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });

        if (!res.ok) throw new Error("Backend error");

        const data = await res.json();
        addMessage(data.reply, "sharma");

    } catch (err) {
        addMessage("[Backend not responding]", "sharma");
        console.error(err);
    }
}

function handleKey(e) {
    if (e.key === "Enter") sendMessage();
}
