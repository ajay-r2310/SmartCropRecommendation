// ===============================
// Agro AI Chatbot
// ===============================

const chatToggle = document.getElementById("chat-toggle");
const chatContainer = document.getElementById("chat-container");
const chatClose = document.getElementById("chat-close");

const chatInput = document.getElementById("chat-input");
const chatSend = document.getElementById("chat-send");

const chatMessages = document.getElementById("chat-messages");
const typingIndicator = document.getElementById("typing-indicator");

// ----------------------------
// Open Chat
// ----------------------------

chatToggle.addEventListener("click", () => {
    chatContainer.classList.add("active");
});

// ----------------------------
// Close Chat
// ----------------------------

chatClose.addEventListener("click", () => {
    chatContainer.classList.remove("active");
});

// ----------------------------
// Send on Button Click
// ----------------------------

chatSend.addEventListener("click", sendMessage);

// ----------------------------
// Send on Enter Key
// ----------------------------

chatInput.addEventListener("keypress", function (e) {

    if (e.key === "Enter") {

        e.preventDefault();

        sendMessage();

    }

});

// ----------------------------
// Main Function
// ----------------------------

async function sendMessage() {

    const message = chatInput.value.trim();

    if (message === "") return;

    addUserMessage(message);

    chatInput.value = "";

    showTyping();

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        hideTyping();

        if (data.success) {

            addBotMessage(data.response);

        } else {

            addBotMessage(data.message);

        }

    }

    catch (error) {

        hideTyping();

        addBotMessage(
            "Sorry! Unable to connect to Agro AI."
        );

        console.error(error);

    }

}

// ----------------------------
// User Message
// ----------------------------

function addUserMessage(message) {

    const div = document.createElement("div");

    div.className = "user-message";

    div.innerHTML = `

        <div class="message-content">

            ${escapeHtml(message)}

        </div>

        <div class="message-icon">

            👨‍🌾

        </div>

    `;

    chatMessages.appendChild(div);

    scrollBottom();

}

// ----------------------------
// Bot Message
// ----------------------------

function addBotMessage(message) {

    const div = document.createElement("div");

    div.className = "bot-message";

    div.innerHTML = `

        <div class="message-icon">

            🌾

        </div>

        <div class="message-content">

            ${formatMessage(message)}

        </div>

    `;

    chatMessages.appendChild(div);

    scrollBottom();

}

// ----------------------------
// Typing
// ----------------------------

function showTyping() {

    typingIndicator.style.display = "flex";

    scrollBottom();

}

function hideTyping() {

    typingIndicator.style.display = "none";

}

// ----------------------------
// Scroll
// ----------------------------

function scrollBottom() {

    chatMessages.scrollTop = chatMessages.scrollHeight;

}

// ----------------------------
// Format Response
// ----------------------------

function formatMessage(text) {

    if (!text) return "";

    return escapeHtml(text)
        .replace(/\n/g, "<br>");

}

// ----------------------------
// Escape HTML
// ----------------------------

function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}
