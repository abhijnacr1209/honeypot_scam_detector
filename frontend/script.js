let chatHistory = "";

async function sendChat() {
    const input = document.getElementById('userMsg');
    const message = input.value.trim();
    if (!message) return;

    // 1. Show Scammer's Message in Bubble
    appendBubble(message, 'scammer');
    input.value = "";
    chatHistory += `Scammer: ${message}\n`;

    try {
        // 2. Call the FastAPI /api/chat endpoint
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        
        const data = await res.json();
        
        // 3. Show Mr. Sharma's Reply
        appendBubble(data.reply, 'sharma');
        chatHistory += `Mr. Sharma: ${data.reply}\n\n`;
        
    } catch (err) {
        console.error("Error:", err);
        appendBubble("Beta, my phone is acting up... signal is very weak today.", "sharma");
    }
}

function appendBubble(text, sender) {
    const chatWindow = document.getElementById('chat-window');
    const bubble = document.createElement('div');
    bubble.className = `bubble ${sender}`;
    
    const now = new Date();
    const timeStr = now.getHours() + ":" + now.getMinutes().toString().padStart(2, '0');
    
    bubble.innerHTML = `${text} <span class="time">${timeStr}</span>`;
    chatWindow.appendChild(bubble);
    
    // Auto-scroll to the bottom
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function generateReport() {
    if (!chatHistory) {
        alert("Please chat with the scammer first before filing a report!");
        return;
    }
    
    const reportContent = document.getElementById('report-content');
    const modal = document.getElementById('report-modal');
    const overlay = document.getElementById('overlay');

    reportContent.innerText = "Analyzing scam patterns... Generating official document...";
    modal.style.display = 'block';
    overlay.style.display = 'block';

    try {
        const res = await fetch('/api/report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ history: chatHistory })
        });
        
        const data = await res.json();
        
        // Format the report for the modal
        reportContent.innerHTML = `
            <div style="background: #f9f9f9; border: 1px solid #ddd; padding: 10px;">
                <strong>Case Reference: ${data.ref_id}</strong><br><br>
                ${data.report.replace(/\n/g, '<br>')}
            </div>
        `;
    } catch (err) {
        reportContent.innerText = "Error generating report. Please try again later.";
    }
}

function closeModal() {
    document.getElementById('report-modal').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}