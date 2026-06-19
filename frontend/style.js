const BASE_URL = window.location.origin;

let user_id = null;
let currentTopic = "";
let firstMessage = true;
let isGenerating = false;
let activeChatId = null;
let personalExperience = "";

let userGroqKey = ""; // Store user's own Groq key

// ✅ Toggle Groq key input
function toggleGroqKey() {
    const wrapper = document.getElementById("groq-key-input-wrapper");
    const toggle = document.getElementById("groq-toggle");
    if (wrapper.style.display === "none") {
        wrapper.style.display = "block";
        toggle.innerText = "⚡ Using your own Groq key (unlimited) ✓";
        toggle.style.color = "#2ea043";
    } else {
        wrapper.style.display = "none";
        toggle.innerText = "⚡ Have a Groq API key? Use unlimited version →";
        toggle.style.color = "#1f6feb";
        document.getElementById("groq-key-input").value = "";
        userGroqKey = "";
    }
}

// ✅ Login
async function login() {
    const input = document.getElementById("username-input").value.trim();
    const pin = document.getElementById("pin-input").value.trim();
    const groqKey = document.getElementById("groq-key-input").value.trim();

    if (!input) { showToast("⚠️ Please enter your name!"); return; }
    if (!pin || pin.length !== 4 || isNaN(pin)) {
        showToast("⚠️ Please enter a 4-digit PIN!");
        return;
    }

    // Validate Groq key format if provided
    if (groqKey && !groqKey.startsWith("gsk_")) {
        showToast("⚠️ Invalid Groq key format! Should start with gsk_");
        return;
    }

    user_id = "user_" + input.toLowerCase().replace(/\s+/g, "_");
    userGroqKey = groqKey; // Store for use in requests

    try {
        const res = await fetch(`${BASE_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id, pin })
        });

        if (res.status === 401) {
            showToast("❌ Incorrect PIN. Try again!");
            return;
        }

        const data = await res.json();
        localStorage.setItem("blog_user_id", user_id);
        localStorage.setItem("blog_username", input);
        localStorage.setItem("blog_pin", pin);
        if (groqKey) {
            localStorage.setItem("blog_groq_key", groqKey);
        }

        showToast(data.status === "created" ? "✅ Account created!" : "✅ Welcome back!");
        showApp(input);
        loadChats();

    } catch (err) {
        showToast("❌ Login failed. Check connection.");
    }
}

// ✅ Logout
function logout() {
    localStorage.removeItem("blog_user_id");
    localStorage.removeItem("blog_username");
    user_id = null;
    firstMessage = true;
    activeChatId = null;
    currentTopic = "";
    personalExperience = "";
    document.getElementById("chat").innerHTML = "";
    document.getElementById("history").innerHTML = "";
    document.getElementById("app").style.display = "none";
    document.getElementById("login-screen").style.display = "flex";
    document.getElementById("username-input").value = "";
}

// ✅ Show main app
function showApp(username) {
    document.getElementById("login-screen").style.display = "none";
    document.getElementById("app").style.display = "flex";
    document.getElementById("user-label").innerText = "👤 " + username;
    updateGroqKeyStatus();
    loadRemainingRequests();
}

// ✅ Auto login
window.onload = () => {
    const savedId = localStorage.getItem("blog_user_id");
    const savedName = localStorage.getItem("blog_username");
    const savedKey = localStorage.getItem("blog_groq_key");
    if (savedId && savedName) {
        user_id = savedId;
        if (savedKey) {
            userGroqKey = savedKey;
        }
        showApp(savedName);
        loadChats();
    }
};

// ✅ Load remaining requests
async function loadRemainingRequests() {
    try {
        const res = await fetch(`${BASE_URL}/remaining/${user_id}`);
        const data = await res.json();
        updateRemainingLabel(data.remaining, data.limit);
    } catch (err) {
        console.error("Failed to load remaining requests:", err);
    }
}

// ✅ Update remaining label
function updateRemainingLabel(remaining, limit) {
    const label = document.getElementById("remaining-label");
    if (!label) return;
    label.innerText = `📊 ${remaining}/${limit} generations left today`;
    if (remaining <= 2) {
        label.style.color = "#f85149"; // Red when low
    } else if (remaining <= 5) {
        label.style.color = "#d29922"; // Yellow when medium
    } else {
        label.style.color = "#8b949e"; // Grey when plenty
    }
}

// ✅ Load all chats into sidebar
async function loadChats() {
    try {
        const res = await fetch(`${BASE_URL}/chats/${user_id}`);
        const data = await res.json();
        const history = document.getElementById("history");
        history.innerHTML = "";
        data.chats.forEach(chat => {
            addChatToSidebar(chat.chat_id, chat.topic, chat.chat_id === activeChatId);
        });
    } catch (err) {
        console.error("Failed to load chats:", err);
    }
}

// ✅ Add chat item to sidebar
function addChatToSidebar(chat_id, topic, isActive = false) {
    const history = document.getElementById("history");
    const item = document.createElement("div");
    item.className = "history-item" + (isActive ? " active" : "");
    item.innerText = topic;
    item.id = "chat-item-" + chat_id;
    item.onclick = () => switchChat(chat_id, topic, item);
    history.insertBefore(item, history.firstChild);
}

// ✅ Toggle the add-key panel in sidebar
function toggleAddKeyPanel() {
    if (userGroqKey) return; // already has a key, nothing to toggle
    const panel = document.getElementById("add-key-panel");
    panel.style.display = panel.style.display === "none" ? "block" : "none";
}

// ✅ Save key added mid-session from sidebar
function saveGroqKeyFromSidebar() {
    const input = document.getElementById("add-key-input");
    const key = input.value.trim();

    if (!key || !key.startsWith("gsk_")) {
        showToast("⚠️ Invalid Groq key format!");
        return;
    }

    userGroqKey = key;
    localStorage.setItem("blog_groq_key_" + user_id, key);

    document.getElementById("add-key-panel").style.display = "none";
    updateGroqKeyStatus();
    loadRemainingRequests();
    showToast("✅ Groq key added! You now have unlimited generations.");
}

// ✅ Reflect current key status in sidebar
function updateGroqKeyStatus() {
    const status = document.getElementById("groq-key-status");
    if (userGroqKey) {
        status.innerText = "⚡ Using your own key (unlimited)";
        status.classList.add("active");
    } else {
        status.innerText = "⚡ Add Groq key for unlimited";
        status.classList.remove("active");
    }
}

// ✅ Switch to existing chat
async function switchChat(chat_id, topic, element) {
    if (isGenerating) return;
    document.querySelectorAll(".history-item").forEach(el => el.classList.remove("active"));
    element.classList.add("active");
    activeChatId = chat_id;
    currentTopic = topic;
    firstMessage = false;
    clearExperience();

    try {
        const res = await fetch(`${BASE_URL}/switch_chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id, chat_id })
        });
        const data = await res.json();
        document.getElementById("chat").innerHTML = "";
        if (data.blog) addMessage(data.blog, "ai");
        else addMessage("No blog generated yet for this topic.", "ai");
    } catch (err) {
        showToast("❌ Failed to load chat");
    }
}

// ✅ Start new chat
function startNewChat() {
    firstMessage = true;
    currentTopic = "";
    activeChatId = null;
    document.getElementById("chat").innerHTML = "";
    document.querySelectorAll(".history-item").forEach(el => el.classList.remove("active"));
    clearExperience();
    showToast("New chat started!");
}

// ✅ Send message
async function send(e) {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    if (isGenerating) return;

    const inputBox = document.getElementById("input");
    const text = inputBox.value.trim();
    if (!text) { showToast("⚠️ Message is empty!"); return; }

    isGenerating = true;
    setSendButtonState(true);
    addMessage(text, "user");
    inputBox.value = "";
    inputBox.style.height = "44px";

    let body = { user_id };

    // Replace with this:
    if (firstMessage) {
        const chatRes = await fetch(`${BASE_URL}/new_chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id, topic: text })
        });
        const chatData = await chatRes.json();
        activeChatId = chatData.chat_id;
        currentTopic = text;
        body.topic = text;
        body.instruction = "";
        body.personal_experience = personalExperience;
        body.groq_api_key = userGroqKey; // ← Added
        firstMessage = false;
        addChatToSidebar(activeChatId, text, true);
    } else {
        body.topic = currentTopic;
        body.instruction = text;
        body.personal_experience = personalExperience;
        body.groq_api_key = userGroqKey; // ← Added
    }


    // Show thinking dots
    const thinkingMsg = addThinkingIndicator();

    try {
        const res = await fetch(`${BASE_URL}/generate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        // ── Rate limit hit
        if (res.status === 429) {
            const data = await res.json();
            thinkingMsg.remove();
            addMessage("⚠️ " + data.detail, "ai");
            isGenerating = false;
            setSendButtonState(false);
            updateRemainingLabel(0, MAX_REQUESTS_PER_USER_PER_DAY);
            document.getElementById("add-key-panel").style.display = "block"; // ← surface it right when they hit the wall
            return;
        }

        // ── Bad input
        if (res.status === 400) {
            const data = await res.json();
            thinkingMsg.remove();
            addMessage("⚠️ " + data.detail, "ai");
            isGenerating = false;
            setSendButtonState(false);
            return;
        }

        // ── Server error
        if (!res.ok) {
            thinkingMsg.remove();
            addMessage("❌ Server error. Please try again.", "ai");
            isGenerating = false;
            setSendButtonState(false);
            return;
        }

        thinkingMsg.remove();

        // Create AI message bubble for streaming
        const aiMsg = document.createElement("div");
        aiMsg.className = "message ai";
        document.getElementById("chat").appendChild(aiMsg);

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split("\n");
            buffer = lines.pop();

            for (const line of lines) {
                if (line.startsWith("data: ")) {
                    try {
                        const parsed = JSON.parse(line.slice(6));
                        if (parsed.token) {
                            aiMsg._raw = (aiMsg._raw || "") + parsed.token;
                            aiMsg.innerHTML = marked.parse(aiMsg._raw);
                            document.getElementById("chat").scrollTop = document.getElementById("chat").scrollHeight;
                        }
                        if (parsed.error) {
                            aiMsg.innerHTML = "❌ Error: " + parsed.error;
                        }
                        if (parsed.done) {
                            // Refresh remaining count after successful generation
                            loadRemainingRequests();
                        }
                    } catch {}
                }
            }
        }

    } catch (err) {
        thinkingMsg?.remove();
        addMessage("❌ Server error. Check backend.", "ai");
        showToast("Server error ❌");
    } finally {
        isGenerating = false;
        setSendButtonState(false);
    }
}

// ✅ Thinking indicator with animated dots
function addThinkingIndicator() {
    const chat = document.getElementById("chat");
    const msg = document.createElement("div");
    msg.className = "message ai thinking-msg";
    msg.innerHTML = `
        <div class="thinking-dots">
            <span></span><span></span><span></span>
        </div>
    `;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
    return msg;
}

// ✅ Toggle send button state
function setSendButtonState(loading) {
    const btn = document.getElementById("send-btn");
    btn.disabled = loading;
    btn.innerHTML = loading
        ? `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>`
        : `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>`;
}

// ✅ Accept blog
async function accept(e) {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    if (!activeChatId) { showToast("⚠️ No blog to accept yet!"); return; }

    try {
        await fetch(`${BASE_URL}/accept`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id, topic: currentTopic })
        });
        showToast("✅ Blog saved as your style example!");
    } catch (err) {
        showToast("❌ Failed to save blog");
    }
}

// ✅ Add message
function addMessage(text, sender) {
    const chat = document.getElementById("chat");
    const msg = document.createElement("div");
    msg.className = "message " + sender;
    msg.innerHTML = sender === "ai" ? marked.parse(text) : text;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
    return msg;
}

// ✅ Toggle experience panel
function toggleExperience() {
    const panel = document.getElementById("experience-panel");
    const btn = document.getElementById("experience-btn");
    panel.classList.toggle("visible");
    btn.classList.toggle("active");
}

// ✅ Save experience
function saveExperience() {
    const text = document.getElementById("experience-input").value.trim();
    const status = document.getElementById("experience-status");
    const btn = document.getElementById("experience-btn");

    if (!text) {
        showToast("⚠️ Please write your experience first!");
        return;
    }

    personalExperience = text;
    status.innerText = "✓ Experience added";
    status.classList.add("saved");
    btn.classList.add("active");

    document.getElementById("experience-panel").classList.remove("visible");
    showToast("✅ Personal experience added!");
}

// ✅ Clear experience
function clearExperience() {
    personalExperience = "";
    const input = document.getElementById("experience-input");
    const status = document.getElementById("experience-status");
    const btn = document.getElementById("experience-btn");
    const panel = document.getElementById("experience-panel");

    if (input) input.value = "";
    if (status) { status.innerText = "No experience added"; status.classList.remove("saved"); }
    if (btn) btn.classList.remove("active");
    if (panel) panel.classList.remove("visible");
}

// ✅ Auto resize input
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("input");

    input.addEventListener("input", function() {
        this.style.height = "44px";
        this.style.height = Math.min(this.scrollHeight, 150) + "px";
    });

    input.addEventListener("keypress", function(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            send(e);
        }
    });
});

// ✅ Toast
function showToast(message) {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerText = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2500);
}

// ✅ Max requests constant for frontend display
const MAX_REQUESTS_PER_USER_PER_DAY = 10;


// ✅ Switch between signin and signup tabs
function switchTab(tab) {
    const signinForm = document.getElementById("signin-form");
    const signupForm = document.getElementById("signup-form");
    const signinTab = document.getElementById("signin-tab");
    const signupTab = document.getElementById("signup-tab");
    const hint = document.getElementById("login-hint");

    if (tab === "signin") {
        signinForm.style.display = "block";
        signupForm.style.display = "none";
        signinTab.classList.add("active");
        signupTab.classList.remove("active");
        hint.innerText = "Welcome back! Enter your username and PIN.";
    } else {
        signinForm.style.display = "none";
        signupForm.style.display = "block";
        signinTab.classList.remove("active");
        signupTab.classList.add("active");
        hint.innerText = "Create your account. Username must be unique.";
    }
}

// ✅ Sign In
async function signIn() {
    const username = document.getElementById("signin-username").value.trim();
    const pin = document.getElementById("signin-pin").value.trim();

    if (!username) { showToast("⚠️ Please enter your username!"); return; }
    if (!pin || pin.length !== 4 || isNaN(pin)) {
        showToast("⚠️ Please enter your 4-digit PIN!");
        return;
    }

    user_id = "user_" + username.toLowerCase().replace(/\s+/g, "_");

    try {
        const res = await fetch(`${BASE_URL}/signin`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id, pin })
        });

        if (res.status === 404) {
            showToast("❌ Username not found. Please sign up first!");
            switchTab("signup");
            return;
        }

        if (res.status === 401) {
            showToast("❌ Incorrect PIN. Try again!");
            return;
        }

        const data = await res.json();
        const savedKey = localStorage.getItem("blog_groq_key_" + user_id);
        if (savedKey) userGroqKey = savedKey;

        localStorage.setItem("blog_user_id", user_id);
        localStorage.setItem("blog_username", username);

        showToast("✅ Welcome back, " + username + "!");
        showApp(username);
        loadChats();

    } catch (err) {
        showToast("❌ Sign in failed. Check connection.");
    }
}

// ✅ Sign Up
async function signUp() {
    const username = document.getElementById("signup-username").value.trim();
    const pin = document.getElementById("signup-pin").value.trim();
    const pinConfirm = document.getElementById("signup-pin-confirm").value.trim();
    const groqKey = document.getElementById("groq-key-input").value.trim();

    if (!username) { showToast("⚠️ Please choose a username!"); return; }
    if (username.length < 3) { showToast("⚠️ Username must be at least 3 characters!"); return; }
    if (!pin || pin.length !== 4 || isNaN(pin)) {
        showToast("⚠️ Please choose a 4-digit PIN!");
        return;
    }
    if (pin !== pinConfirm) {
        showToast("⚠️ PINs don't match!");
        return;
    }
    if (groqKey && !groqKey.startsWith("gsk_")) {
        showToast("⚠️ Invalid Groq key format!");
        return;
    }

    user_id = "user_" + username.toLowerCase().replace(/\s+/g, "_");
    userGroqKey = groqKey;

    try {
        const res = await fetch(`${BASE_URL}/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id, pin })
        });

        if (res.status === 409) {
            showToast("❌ Username already taken! Try a different one.");
            return;
        }

        const data = await res.json();

        localStorage.setItem("blog_user_id", user_id);
        localStorage.setItem("blog_username", username);
        if (groqKey) {
            localStorage.setItem("blog_groq_key_" + user_id, groqKey);
        }

        showToast("✅ Account created! Welcome, " + username + "!");
        showApp(username);
        loadChats();

    } catch (err) {
        showToast("❌ Sign up failed. Check connection.");
    }
}

// ✅ Toggle Groq key input
function toggleGroqKey() {
    const wrapper = document.getElementById("groq-key-input-wrapper");
    const toggle = document.getElementById("groq-toggle");
    if (wrapper.style.display === "none") {
        wrapper.style.display = "block";
        toggle.innerText = "⚡ Using your own Groq key (unlimited) ✓";
        toggle.style.color = "#2ea043";
    } else {
        wrapper.style.display = "none";
        toggle.innerText = "⚡ Have a Groq API key? Use unlimited version →";
        toggle.style.color = "#1f6feb";
        document.getElementById("groq-key-input").value = "";
        userGroqKey = "";
    }
}