const chatBox = document.getElementById("chatBox");
const input = document.getElementById("messageInput");

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

    const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await res.json();
    addMessage(data.reply || "No response", "sharma");
}

input.addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
});
