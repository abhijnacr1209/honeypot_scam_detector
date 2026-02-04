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
    div.className = `message ${className}`;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    // Show scammer message
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

        if (data.reply && data.reply.trim() !== "") {
            addMessage(data.reply, "sharma");
        } else {
            addMessage("[No reply from backend]", "sharma");
        }

    } catch (err) {
        addMessage("[Backend not responding]", "sharma");
        console.error(err);
    }
}

// Press Enter to send
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});
