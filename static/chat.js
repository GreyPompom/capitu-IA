const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const chatHistory = document.getElementById("chat-history");
const inputContainer = document.getElementById("input-container");

function scrollToBottom() {
    chatHistory.scrollTop = chatHistory.scrollHeight;
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
}

sendBtn.addEventListener("click", handleSend);

userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        handleSend();
    }
});