const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const chatHistory = document.getElementById("chat-history");
const inputContainer = document.getElementById("input-container");

function scrollToBottom() {
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function createBotMessage(contentHtml) {
    const msgDiv = document.createElement("div");
    msgDiv.className = "message bot-message";
    msgDiv.innerHTML = `
        <div class="avatar">C</div>
        <div class="message-content">${contentHtml}</div>
    `;
    return msgDiv;
}

function simulateResponse(text) {
    const lowerText = text.toLowerCase();
    let responseHtml = `<p>Vou buscar referências bibliográficas relacionadas a "${text}". Você também pode informar um título, autor ou assunto para refinar a descoberta.</p>`;

    if (lowerText.includes("machado de assis")) {
        responseHtml = `
            <p>Encontrei algumas obras de Machado de Assis para sua pesquisa. Você pode pedir os detalhes de qualquer título.</p>
            <div style="margin-top: 20px; display: flex; flex-direction: column; gap: 12px;">
                <div style="background: #fff; border: 1px solid #eaeaea; padding: 16px; border-radius: 8px; display: flex; align-items: center;">
                    <span style="font-size: 18px; color: #ccc; margin-right: 16px; font-weight: 500;">01</span>
                    <div>
                        <strong style="display: block; color: #333; margin-bottom: 4px;">Dom Casmurro</strong>
                        <span style="font-size: 13px; color: #666;">Machado de Assis • Romance</span>
                    </div>
                </div>
                <div style="background: #fff; border: 1px solid #eaeaea; padding: 16px; border-radius: 8px; display: flex; align-items: center;">
                    <span style="font-size: 18px; color: #ccc; margin-right: 16px; font-weight: 500;">02</span>
                    <div>
                        <strong style="display: block; color: #333; margin-bottom: 4px;">Memórias Póstumas de Brás Cubas</strong>
                        <span style="font-size: 13px; color: #666;">Machado de Assis • Romance</span>
                    </div>
                </div>
            </div>
        `;
    }

    chatHistory.appendChild(createBotMessage(responseHtml));
    scrollToBottom();
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

    setTimeout(() => {
        removeElement(loadId);
        simulateResponse(text);
    }, 1200);
}

sendBtn.addEventListener("click", handleSend);

userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        handleSend();
    }
});