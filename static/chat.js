const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const chatHistory = document.getElementById("chat-history");
const inputContainer = document.getElementById("input-container");

function scrollToBottom() {
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function showLoading() {
    const id = "loading-" + Date.now();
    const loadingDiv = document.createElement("div");
    loadingDiv.className = "message bot-message";
    loadingDiv.id = id;
    loadingDiv.innerHTML = `
        <div class="loading-avatar"></div>
        <div class="message-content" style="color: #888; font-style: italic;">Consultando acervo...</div>
    `;
    chatHistory.appendChild(loadingDiv);
    scrollToBottom();
    return id;
}

function removeElement(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function handleSend() {
    const text = userInput.value.trim();

    if (!text) {
        inputContainer.classList.add("error");
        setTimeout(() => inputContainer.classList.remove("error"), 400);
        return;
    }

    const msgDiv = document.createElement("div");
    msgDiv.className = "message user-message";
    msgDiv.textContent = text;
    chatHistory.appendChild(msgDiv);
    
    userInput.value = "";
    scrollToBottom();

    const loadId = showLoading();
}

sendBtn.addEventListener("click", handleSend);

userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        handleSend();
    }
});