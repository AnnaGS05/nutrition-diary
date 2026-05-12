async function request(url, options = {}) {
    const response = await fetch(url, {
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        },
        ...options
    });

    if (!response.ok) {
        throw new Error(`Ошибка запроса: ${response.status}`);
    }

    return response.json();
}

async function isAuthenticated() {
    const response = await fetch("/auth/me", {
        credentials: "include"
    });

    if (!response.ok) {
        return false;
    }

    const data = await response.json();
    return Boolean(data.authenticated);
}

async function registerUser() {
    const usernameInput = document.getElementById("registerUsername");
    const passwordInput = document.getElementById("registerPassword");
    const message = document.getElementById("authMessage");

    if (!usernameInput || !passwordInput) return;

    const body = new URLSearchParams();
    body.append("username", usernameInput.value);
    body.append("password", passwordInput.value);

    const response = await fetch("/auth/register", {
        method: "POST",
        body,
        credentials: "include"
    });

    const data = await response.json();

    if (message) {
        message.textContent = data.message || data.error || "Регистрация выполнена";
    }

    if (response.ok && data.message) {
        setTimeout(() => {
            window.location.href = "/login";
        }, 700);
    }
}

async function loginUser() {
    const usernameInput = document.getElementById("loginUsername");
    const passwordInput = document.getElementById("loginPassword");
    const message = document.getElementById("authMessage");

    if (!usernameInput || !passwordInput) return;

    const body = new URLSearchParams();
    body.append("username", usernameInput.value);
    body.append("password", passwordInput.value);

    const response = await fetch("/auth/login", {
        method: "POST",
        body,
        credentials: "include"
    });

    const data = await response.json();

    if (response.ok && data.message) {
        if (message) {
            message.textContent = "Вход выполнен";
        }

        setTimeout(() => {
            window.location.href = "/";
        }, 500);
    } else {
        if (message) {
            message.textContent = data.error || "Ошибка входа";
        }
    }
}

async function logoutUser() {
    await fetch("/auth/logout", {
        method: "POST",
        credentials: "include"
    });

    setStatsToZero();

    const entriesList = document.getElementById("entriesList");
    if (entriesList) {
        entriesList.innerHTML = "<p>Для просмотра записей необходимо войти в систему</p>";
    }

    await checkAuth();
}

async function checkAuth() {
    const authenticated = await isAuthenticated();

    const authToggleBtn = document.getElementById("authToggleBtn");
    const logoutBtn = document.getElementById("logoutBtn");
    const entriesList = document.getElementById("entriesList");

    if (authenticated) {
        if (authToggleBtn) authToggleBtn.classList.add("hidden");
        if (logoutBtn) logoutBtn.classList.remove("hidden");

        await loadEntries();
        await loadStats();
    } else {
        if (authToggleBtn) authToggleBtn.classList.remove("hidden");
        if (logoutBtn) logoutBtn.classList.add("hidden");

        setStatsToZero();

        if (entriesList) {
            entriesList.innerHTML = "<p>Для просмотра записей необходимо войти в систему</p>";
        }
    }
}

async function addEntry() {
    const authenticated = await isAuthenticated();
    const entryMessage = document.getElementById("entryMessage");

    if (!authenticated) {
        if (entryMessage) {
            entryMessage.textContent = "Для добавления записи необходимо войти";
        }

        setTimeout(() => {
            window.location.href = "/login";
        }, 700);

        return;
    }

    const nameInput = document.getElementById("entryName");
    const proteinsInput = document.getElementById("entryProteins");
    const fatsInput = document.getElementById("entryFats");
    const carbsInput = document.getElementById("entryCarbs");
    const caloriesInput = document.getElementById("entryCalories");

    const entry = {
        name: nameInput.value,
        proteins: Number(proteinsInput.value || 0),
        fats: Number(fatsInput.value || 0),
        carbs: Number(carbsInput.value || 0),
        calories: Number(caloriesInput.value || 0)
    };

    await request("/api/entries/", {
        method: "POST",
        body: JSON.stringify(entry)
    });

    if (entryMessage) {
        entryMessage.textContent = "Запись добавлена";
    }

    nameInput.value = "";
    proteinsInput.value = "";
    fatsInput.value = "";
    carbsInput.value = "";
    caloriesInput.value = "";

    await loadEntries();
    await loadStats();
}

async function loadEntries() {
    const response = await fetch("/api/entries/", {
        credentials: "include"
    });

    if (!response.ok) {
        return;
    }

    const entries = await response.json();
    const list = document.getElementById("entriesList");

    if (!list) return;

    list.innerHTML = "";

    if (entries.length === 0) {
        list.innerHTML = "<p>Записей пока нет</p>";
        return;
    }

    entries.forEach(entry => {
        const item = document.createElement("div");
        item.className = "entry";

        item.innerHTML = `
            <div>
                <div class="entry-title">${entry.name}</div>
                <small>${entry.created_at}</small>
            </div>
            <div>Б: ${entry.proteins}</div>
            <div>Ж: ${entry.fats}</div>
            <div>У: ${entry.carbs}</div>
            <div>${entry.calories} ккал</div>
            <button class="danger" onclick="deleteEntry(${entry.id})">Удалить</button>
        `;

        list.appendChild(item);
    });
}

async function deleteEntry(id) {
    const authenticated = await isAuthenticated();

    if (!authenticated) {
        window.location.href = "/login";
        return;
    }

    await request(`/api/entries/${id}`, {
        method: "DELETE"
    });

    await loadEntries();
    await loadStats();
}

async function loadStats() {
    const response = await fetch("/api/stats", {
        credentials: "include"
    });

    if (!response.ok) {
        setStatsToZero();
        return;
    }

    const stats = await response.json();

    const totalProteins = document.getElementById("totalProteins");
    const totalFats = document.getElementById("totalFats");
    const totalCarbs = document.getElementById("totalCarbs");
    const totalCalories = document.getElementById("totalCalories");

    if (totalProteins) totalProteins.textContent = stats.proteins || 0;
    if (totalFats) totalFats.textContent = stats.fats || 0;
    if (totalCarbs) totalCarbs.textContent = stats.carbs || 0;
    if (totalCalories) totalCalories.textContent = stats.calories || 0;
}

function setStatsToZero() {
    const totalProteins = document.getElementById("totalProteins");
    const totalFats = document.getElementById("totalFats");
    const totalCarbs = document.getElementById("totalCarbs");
    const totalCalories = document.getElementById("totalCalories");

    if (totalProteins) totalProteins.textContent = 0;
    if (totalFats) totalFats.textContent = 0;
    if (totalCarbs) totalCarbs.textContent = 0;
    if (totalCalories) totalCalories.textContent = 0;
}

const logoutButton = document.getElementById("logoutBtn");

if (logoutButton) {
    logoutButton.addEventListener("click", logoutUser);
}

checkAuth();