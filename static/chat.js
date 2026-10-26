const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const chatHistory = document.getElementById("chat-history");
const inputContainer = document.getElementById("input-container");
const newChatBtn = document.getElementById("new-chat-btn");
const sidebarMenuItems = document.querySelectorAll(".sidebar-menu li");

let currentSessionId = generateSessionId();

function generateSessionId() {
    return "session-" + Date.now() + "-" + Math.random().toString(36).substr(2, 9);
}

function scrollToBottom() {
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function addUserMessage(text) {
    const msgDiv = document.createElement("div");
    msgDiv.className = "message bot-message";
    msgDiv.textContent = text;
    chatHistory.appendChild(msgDiv);
    scrollToBottom();
}

function addBotMessage(text, results = []) {
    const msgDiv = document.createElement("div");
    msgDiv.className = "message bot-message";

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = "C";

    const content = document.createElement("div");
    content.className = "message-content";

    const textPara = document.createElement("p");
    textPara.textContent = text;
    content.appendChild(textPara);

    if (Array.isArray(results) && results.length > 0) {
        const listDiv = document.createElement("div");
        listDiv.className = "books-list";

        results.forEach((item, index) => {
            const card = document.createElement("div");
            card.className = "book-card";

            const numSpan = document.createElement("span");
            numSpan.className = "book-number";
            numSpan.textContent = String(index + 1).padStart(2, '0');

            const infoDiv = document.createElement("div");
            infoDiv.className = "book-info";

            const titleStrong = document.createElement("strong");
            titleStrong.textContent = item.title || item.titulo || "Título não informado";

            const authorSpan = document.createElement("span");
            const author = item.author || item.autor || "Autor não informado";
            const genre = item.genre || item.genero || item.subject || "";
            authorSpan.textContent = genre ? `${author} • ${genre}` : author;

            infoDiv.appendChild(titleStrong);
            infoDiv.appendChild(authorSpan);

            card.appendChild(numSpan);
            card.appendChild(infoDiv);

            card.addEventListener("click", () => {
                const bookTitle = item.title || item.titulo;
                if (bookTitle) {
                    userInput.value = `Consultar detalhes de "${bookTitle}"`;
                    handleSend();
                }
            });

            listDiv.appendChild(card);
        });

        content.appendChild(listDiv);
    }

    msgDiv.appendChild(avatar);
    msgDiv.appendChild(content);
    chatHistory.appendChild(msgDiv);
    scrollToBottom();
}

function showLoading() {
    const id = "loading-" + Date.now();
    const loadingDiv = document.createElement("div");
    loadingDiv.className = "message bot-message";
    loadingDiv.id = id;

    const avatar = document.createElement("div");
    avatar.className = "loading-avatar";

    const content = document.createElement("div");
    content.className = "message-content";
    content.style.color = "#888";
    content.style.fontStyle = "italic";
    content.textContent = "Consultando acervo...";

    loadingDiv.appendChild(avatar);
    loadingDiv.appendChild(content);
    chatHistory.appendChild(loadingDiv);
    scrollToBottom();
    return id;
}

function removeElement(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function setInputState(disabled) {
    userInput.disabled = disabled;
    sendBtn.disabled = disabled;
    if (disabled) {
        sendBtn.style.opacity = "0.6";
        sendBtn.style.cursor = "not-allowed";
    } else {
        sendBtn.style.opacity = "1";
        sendBtn.style.cursor = "pointer";
        userInput.focus();
    }
}

async function handleSend() {
    const text = userInput.value.trim();

    if (!text) {
        inputContainer.classList.add("error");
        setTimeout(() => inputContainer.classList.remove("error"), 400);
        return;
    }
    
    addUserMessage(text);
    userInput.value = "";
    setInputState(true);
    const loadId = showLoading();

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: text,
                session_id: currentSessionId
            })
        });

        removeElement(loadId);

        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
        }

        const data = await response.json();

        const responseText = data.response || data.message || "Não foi possível obter uma resposta adequada.";
        const results = data.results || data.items || data.books || [];

        addBotMessage(responseText, results);

    } catch (error) {
        removeElement(loadId);
        console.error("Erro ao chamar API /api/chat:", error);
        addBotMessage("Ocorreu um erro ao comunicar com o servidor. Por favor, tente novamente em instantes.");
    } finally {
        setInputState(false);
    }
}

newChatBtn.addEventListener("click", () => {
    currentSessionId = generateSessionId();
    chatHistory.innerHTML = `
        <div class="message bot-message">
            <div class="avatar">C</div>
            <div class="message-content">
                <p><strong>Olá, sou a Capitu.</strong></p>
                <p>Nova conversa iniciada. Ajudo você a encontrar livros e referências para seus estudos.<br>Por onde começamos?</p>
            </div>
        </div>
    `;
    userInput.value = "";
    userInput.focus();
});

sidebarMenuItems.forEach(item => {
    item.addEventListener("click", () => {
        const action = item.getAttribute("data-action");
        switch (action) {
            case "titulo":
                userInput.value = "Buscar pelo título: ";
                break;
            case "autor":
                userInput.value = "Obras do autor: ";
                break;
            case "assunto":
                userInput.value = "Explorar assunto: ";
                break;
            case "detalhes":
                userInput.value = "Consultar detalhes do livro: ";
                break;
        }
        userInput.focus();
    });
});

sendBtn.addEventListener("click", handleSend);

userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        handleSend();
    }
});