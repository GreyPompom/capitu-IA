const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const chatForm = document.getElementById("chat-form");
const chatHistory = document.getElementById("chat-history");
const inputContainer = document.getElementById("input-container");
const inputError = document.getElementById("input-error");
const newChatBtn = document.getElementById("new-chat-btn");
const appStatusText = document.getElementById("app-status-text");
const sidebarActions = document.querySelectorAll(".sidebar-action");

// O servidor cria a sessão no primeiro turno e devolve seu UUID no contrato.
let currentSessionId = null;
let isSending = false;

function scrollToBottom() {
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function addUserMessage(text) {
    const message = document.createElement("div");
    message.className = "message user-message";
    message.textContent = text;
    chatHistory.appendChild(message);
    scrollToBottom();
}

function addBotMessage(text, results = [], state = "answered") {
    const message = document.createElement("div");
    message.className = "message bot-message";
    message.dataset.state = state;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent = "C";

    const content = document.createElement("div");
    content.className = "message-content";
    const paragraph = document.createElement("p");
    paragraph.textContent = text;
    content.appendChild(paragraph);

    if (Array.isArray(results) && results.length > 0) {
        const list = document.createElement("div");
        list.className = "books-list";
        results.forEach((book, index) => list.appendChild(createBookCard(book, index)));
        content.appendChild(list);
    }

    message.append(avatar, content);
    chatHistory.appendChild(message);
    scrollToBottom();
}

function appendMetadata(container, label, values) {
    if (!Array.isArray(values) || values.length === 0) return;
    const item = document.createElement("span");
    item.textContent = `${label}: ${values.join(", ")}`;
    container.appendChild(item);
}

function createBookCard(book, index) {
    const title = typeof book.title === "string" && book.title.trim()
        ? book.title
        : "Título não informado";
    const card = document.createElement("button");
    card.type = "button";
    card.className = "book-card";
    card.setAttribute("aria-label", `Consultar detalhes de ${title}`);

    const number = document.createElement("span");
    number.className = "book-number";
    number.setAttribute("aria-hidden", "true");
    number.textContent = String(index + 1).padStart(2, "0");

    const info = document.createElement("span");
    info.className = "book-info";
    const titleElement = document.createElement("strong");
    titleElement.textContent = title;
    info.appendChild(titleElement);

    appendMetadata(info, "Autor(es)", book.authors);
    appendMetadata(info, "Assunto(s)", book.subjects);
    if (book.first_publish_year !== null && book.first_publish_year !== undefined) {
        const year = document.createElement("span");
        year.textContent = `Primeira publicação: ${book.first_publish_year}`;
        info.appendChild(year);
    }

    card.append(number, info);
    card.addEventListener("click", () => {
        if (isSending || title === "Título não informado") return;
        userInput.value = `Consultar detalhes do livro: ${title}`;
        chatForm.requestSubmit();
    });
    return card;
}

function showLoading() {
    const message = document.createElement("div");
    message.className = "message bot-message loading-message";
    message.setAttribute("role", "status");
    const avatar = document.createElement("div");
    avatar.className = "loading-avatar";
    avatar.setAttribute("aria-hidden", "true");
    const content = document.createElement("div");
    content.className = "message-content";
    content.textContent = "Consultando acervo...";
    message.append(avatar, content);
    chatHistory.appendChild(message);
    scrollToBottom();
    return message;
}

function setSending(disabled) {
    isSending = disabled;
    userInput.disabled = disabled;
    sendBtn.disabled = disabled;
    newChatBtn.disabled = disabled;
    sidebarActions.forEach((button) => { button.disabled = disabled; });
}

function showInputError(message) {
    inputContainer.classList.toggle("error", Boolean(message));
    inputError.textContent = message;
    inputError.hidden = !message;
}

function isChatResponse(data) {
    return data && typeof data.text === "string" && data.text.length > 0
        && typeof data.session_id === "string"
        && typeof data.state === "string"
        && Array.isArray(data.results);
}

async function handleSend(event) {
    event?.preventDefault();
    if (isSending) return;

    const text = userInput.value.trim();
    if (!text) {
        showInputError("Digite uma mensagem antes de enviar.");
        userInput.focus();
        return;
    }

    showInputError("");
    addUserMessage(text);
    userInput.value = "";
    setSending(true);
    const loadingMessage = showLoading();

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text, session_id: currentSessionId }),
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        if (!isChatResponse(data)) throw new Error("Resposta incompatível com o contrato chat-v1");

        currentSessionId = data.session_id;
        appStatusText.textContent = "Conectada";
        addBotMessage(data.text, data.results, data.state);
    } catch (error) {
        console.error("Falha em POST /api/chat:", error);
        appStatusText.textContent = "Servidor indisponível";
        addBotMessage("Não foi possível comunicar com o servidor. Tente novamente em instantes.", [], "source_unavailable");
    } finally {
        loadingMessage.remove();
        setSending(false);
        userInput.focus();
    }
}

function showWelcomeMessage(isNewConversation = false) {
    const message = document.createElement("div");
    message.className = "message bot-message";
    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent = "C";
    const content = document.createElement("div");
    content.className = "message-content";
    const heading = document.createElement("p");
    const strong = document.createElement("strong");
    strong.textContent = "Olá, sou a Capitu.";
    heading.appendChild(strong);
    const description = document.createElement("p");
    description.textContent = isNewConversation
        ? "Nova conversa iniciada. Ajudo você a encontrar livros e referências para seus estudos. Por onde começamos?"
        : "Ajudo você a encontrar livros e referências para seus estudos. Por onde começamos?";
    content.append(heading, description);
    message.append(avatar, content);
    chatHistory.replaceChildren(message);
}

newChatBtn.addEventListener("click", () => {
    if (isSending) return;
    currentSessionId = null;
    userInput.value = "";
    showInputError("");
    showWelcomeMessage(true);
    userInput.focus();
});

sidebarActions.forEach((button) => {
    button.addEventListener("click", () => {
        const prompts = {
            titulo: "Buscar pelo título: ",
            autor: "Obras do autor: ",
            assunto: "Explorar assunto: ",
            detalhes: "Consultar detalhes do livro: ",
        };
        userInput.value = prompts[button.dataset.action] || "";
        userInput.focus();
    });
});

chatForm.addEventListener("submit", handleSend);
userInput.addEventListener("input", () => {
    if (userInput.value.trim()) showInputError("");
});
