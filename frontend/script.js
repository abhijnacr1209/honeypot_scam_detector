let chatHistory = "";

// ✅ create / reuse session id
let sessionId = localStorage.getItem("session_id");
if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);
}

async function sendChat() {
    const input = document.getElementById('user-input'); // ✅ fixed ID
    const message = input.value.trim();
    if (!message) return;

    // Show scammer message
    appendBubble(message, 'scammer');
    input.value = "";
    chatHistory += `Scammer: ${message}\n`;

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                session_id: sessionId   // ✅ REQUIRED
            })
        });

        if (!res.ok) throw new Error("Backend error");

        const data = await res.json();

        appendBubble(data.reply, 'sharma');
        chatHistory += `Mr. Sharma: ${data.reply}\n\n`;

    } catch (err) {
        console.error(err);
        appendBubble(
            "Arrey beta… network is very weak today. Can you repeat slowly?",
            "sharma"
        );
    }
}

function appendBubble(text, sender) {
    const chatWindow = document.getElementById('chat-window');
    const bubble = document.createElement('div');
    bubble.className = `bubble ${sender}`;

    const now = new Date();
    const timeStr =
        now.getHours().toString().padStart(2, '0') + ":" +
        now.getMinutes().toString().padStart(2, '0');

    bubble.innerHTML = `${text} <span class="time">${timeStr}</span>`;
    chatWindow.appendChild(bubble);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// ✅ ENTER KEY SUPPORT
document.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendChat();
});

// ---------------- REPORT ----------------

async function generateReport() {
    const modal = document.getElementById('report-modal');
    const overlay = document.getElementById('overlay');
    const reportContent = document.getElementById('report-content');

    reportContent.innerText = "Generating investigation report...";
    modal.style.display = 'block';
    overlay.style.display = 'block';

    try {
        const res = await fetch('/api/report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId }) // ✅ FIXED
        });

        const data = await res.json();

        reportContent.innerHTML = `
            <pre style="white-space: pre-wrap;">${data.report}</pre>
        `;
    } catch (err) {
        reportContent.innerText = "Error generating report.";
        console.error(err);
    }
}

function closeModal() {
    document.getElementById('report-modal').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}
