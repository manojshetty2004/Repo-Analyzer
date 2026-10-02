document.addEventListener("DOMContentLoaded", () => {
    const repoUrlInput = document.getElementById("repo-url");
    const indexBtn = document.getElementById("index-btn");
    const indexProgress = document.getElementById("index-progress");
    const progressText = document.getElementById("progress-text");
    const activeRepoName = document.getElementById("active-repo-name");
    const messagesContainer = document.getElementById("messages-container");
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const suggestionsBox = document.getElementById("suggestions-box");

    let isIndexing = false;
    let isWaitingForReply = false;

    // Expand input height dynamically
    chatInput.addEventListener("input", () => {
        chatInput.style.height = "auto";
        chatInput.style.height = `${chatInput.scrollHeight}px`;
        sendBtn.disabled = !chatInput.value.trim();
    });

    // Keypress listener for send on Enter
    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Send click listener
    sendBtn.addEventListener("click", () => {
        sendMessage();
    });

    // Index button listener
    indexBtn.addEventListener("click", () => {
        indexRepository();
    });

    const clearBtn = document.getElementById("clear-btn");
    clearBtn.addEventListener("click", async () => {
        clearBtn.disabled = true;
        try {
            const res = await fetch("/clear", { method: "POST" });
            if (res.ok) {
                document.getElementById("stat-modules").textContent = "-";
                document.getElementById("stat-classes").textContent = "-";
                document.getElementById("stat-functions").textContent = "-";
                document.getElementById("stat-methods").textContent = "-";
                document.getElementById("stat-imports").textContent = "-";
                document.getElementById("stat-nodes").textContent = "-";
                activeRepoName.textContent = "No codebase indexed yet";
                repoUrlInput.value = "";
                appendMessage("system", "Database cleared successfully.");
            } else {
                throw new Error("Failed to clear database.");
            }
        } catch (e) {
            appendMessage("system", `Error: ${e.message}`);
        } finally {
            clearBtn.disabled = false;
        }
    });

    // Suggestions listener
    suggestionsBox.addEventListener("click", (e) => {
        const btn = e.target.closest(".suggestion-tag");
        if (btn) {
            const query = btn.getAttribute("data-query");
            chatInput.value = query;
            sendMessage();
        }
    });

    // Parse statistics response
    const parseStatistics = (text) => {
        const modulesMatch = text.match(/Modules\s*:\s*(\d+)/i);
        const classesMatch = text.match(/Classes\s*:\s*(\d+)/i);
        const functionsMatch = text.match(/Functions\s*:\s*(\d+)/i);
        const methodsMatch = text.match(/Methods\s*:\s*(\d+)/i);
        const importsMatch = text.match(/Imports\s*:\s*(\d+)/i);
        const nodesMatch = text.match(/Graph Nodes\s*:\s*(\d+)/i);

        if (modulesMatch) document.getElementById("stat-modules").textContent = modulesMatch[1];
        if (classesMatch) document.getElementById("stat-classes").textContent = classesMatch[1];
        if (functionsMatch) document.getElementById("stat-functions").textContent = functionsMatch[1];
        if (methodsMatch) document.getElementById("stat-methods").textContent = methodsMatch[1];
        if (importsMatch) document.getElementById("stat-imports").textContent = importsMatch[1];
        if (nodesMatch) document.getElementById("stat-nodes").textContent = nodesMatch[1];
    };

    // Index action
    async function indexRepository() {
        const repo = repoUrlInput.value.trim();
        if (!repo) return;

        isIndexing = true;
        indexBtn.disabled = true;
        indexProgress.classList.remove("hidden");
        progressText.textContent = "Cloning and parsing repository...";

        try {
            const res = await fetch("/index", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ repository_url: repo })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Failed to index repository.");
            }

            const data = await res.json();
            progressText.textContent = "Indexing and generating embeddings...";
            
            // Set active codebase text
            let repoDisplayName = repo;
            try {
                if (repo.includes("github.com")) {
                    const parts = repo.split("github.com/")[1].split("/");
                    repoDisplayName = `${parts[0]}/${parts[1]}`;
                } else {
                    repoDisplayName = repo.split(/[\\/]/).pop();
                }
            } catch (e) {}
            activeRepoName.textContent = `Codebase: ${repoDisplayName}`;

            appendMessage("system", `Successfully indexed codebase: ${repoDisplayName}`);

            // Fetch statistics silently to populate the sidebar stats grid
            progressText.textContent = "Retrieving codebase statistics...";
            const statsRes = await fetch("/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: "Show statistics of the repository" })
            });

            if (statsRes.ok) {
                const statsData = await statsRes.json();
                parseStatistics(statsData.answer);
            }
        } catch (e) {
            appendMessage("system", `Error indexing: ${e.message}`);
        } finally {
            isIndexing = false;
            indexBtn.disabled = false;
            indexProgress.classList.add("hidden");
        }
    }

    // Send message action
    async function sendMessage() {
        const question = chatInput.value.trim();
        if (!question || isWaitingForReply) return;

        appendMessage("user", question);
        chatInput.value = "";
        chatInput.style.height = "auto";
        sendBtn.disabled = true;

        isWaitingForReply = true;
        const thinkingBubble = appendThinkingIndicator();

        try {
            const res = await fetch("/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: question })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Server error.");
            }

            const data = await res.json();
            removeThinkingIndicator(thinkingBubble);
            appendMessage("assistant", data.answer);
        } catch (e) {
            removeThinkingIndicator(thinkingBubble);
            appendMessage("assistant", `Error: ${e.message}`);
        } finally {
            isWaitingForReply = false;
        }
    }

    // Render basic markdown tags safely
    function renderContent(text) {
        let escaped = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");

        // Code blocks: ```python ... ```
        escaped = escaped.replace(/```(?:[a-zA-Z0-9]+)?\n([\s\S]*?)```/g, (match, code) => {
            return `<pre><code>${code.trim()}</code></pre>`;
        });

        // Inline code blocks: `code`
        escaped = escaped.replace(/`([^`]+)`/g, "<code>$1</code>");

        // Bold text: **text**
        escaped = escaped.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

        // Bullet lists
        escaped = escaped.replace(/^\s*[-*]\s+(.*)$/gm, "<li>$1</li>");
        // Wrap <li> elements in a <ul> tag
        escaped = escaped.replace(/(<li>.*<\/li>)/s, "<ul>$1</ul>");

        // Section Headers
        escaped = escaped.replace(/^### (.*)$/gm, "<h3>$1</h3>");
        escaped = escaped.replace(/^## (.*)$/gm, "<h2>$1</h2>");
        escaped = escaped.replace(/^# (.*)$/gm, "<h1>$1</h1>");

        // Line breaks
        escaped = escaped.replace(/\n/g, "<br>");

        return escaped;
    }

    // Append standard message card to DOM
    function appendMessage(sender, text) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${sender}-message`;

        const bubble = document.createElement("div");
        bubble.className = "message-bubble";

        if (sender === "system") {
            bubble.innerHTML = `<i class="fa-solid fa-circle-info system-icon"></i> <p>${text}</p>`;
        } else if (sender === "user") {
            bubble.textContent = text;
        } else {
            bubble.innerHTML = renderContent(text);
        }

        messageDiv.appendChild(bubble);
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Append thinking dot pulsing loader to DOM
    function appendThinkingIndicator() {
        const messageDiv = document.createElement("div");
        messageDiv.className = "message assistant-message";

        const bubble = document.createElement("div");
        bubble.className = "message-bubble thinking-bubble";
        bubble.innerHTML = `<span class="dot"></span><span class="dot"></span><span class="dot"></span>`;

        messageDiv.appendChild(bubble);
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return messageDiv;
    }

    function removeThinkingIndicator(indicatorEl) {
        if (indicatorEl) {
            messagesContainer.removeChild(indicatorEl);
        }
    }
});
