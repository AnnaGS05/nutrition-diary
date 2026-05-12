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

    if (!response.ok) return false;

    const data = await response.json();
    return Boolean(data.authenticated);
}

window.loginUser = async function () {
    const usernameInput = document.getElementById("loginUsername");
    const passwordInput = document.getElementById("loginPassword");
    const message = document.getElementById("authMessage");

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
        if (message) message.textContent = "Вход выполнен";

        setTimeout(() => {
            window.location.href = "/";
        }, 500);
    } else {
        if (message) message.textContent = data.error || "Ошибка входа";
    }
};

window.registerUser = async function () {
    const usernameInput = document.getElementById("registerUsername");
    const passwordInput = document.getElementById("registerPassword");
    const message = document.getElementById("authMessage");

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
};

window.addEntry = async function () {
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

    const entry = {
        name: document.getElementById("entryName").value,
        proteins: Number(document.getElementById("entryProteins").value || 0),
        fats: Number(document.getElementById("entryFats").value || 0),
        carbs: Number(document.getElementById("entryCarbs").value || 0),
        calories: Number(document.getElementById("entryCalories").value || 0)
    };

    await request("/api/entries/", {
        method: "POST",
        body: JSON.stringify(entry)
    });

    if (entryMessage) {
        entryMessage.textContent = "Запись добавлена";
    }

    document.getElementById("entryName").value = "";
    document.getElementById("entryProteins").value = "";
    document.getElementById("entryFats").value = "";
    document.getElementById("entryCarbs").value = "";
    document.getElementById("entryCalories").value = "";

    await loadEntries();
    await loadStats();
};

async function loadEntries() {
    const response = await fetch("/api/entries/", {
        credentials: "include"
    });

    if (!response.ok) return;

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

window.deleteEntry = async function (id) {
    await request(`/api/entries/${id}`, {
        method: "DELETE"
    });

    await loadEntries();
    await loadStats();
};

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

async function logoutUser() {
    await fetch("/auth/logout", {
        method: "POST",
        credentials: "include"
    });

    window.location.href = "/";
}

async function checkAuth() {
    const authenticated = await isAuthenticated();

    const authToggleBtn = document.getElementById("authToggleBtn");
    const logoutBtn = document.getElementById("logoutBtn");
    const profileBtn = document.getElementById("profileBtn");
    const entriesList = document.getElementById("entriesList");

    if (authenticated) {
        if (authToggleBtn) authToggleBtn.classList.add("hidden");
        if (logoutBtn) logoutBtn.classList.remove("hidden");
        if (profileBtn) profileBtn.classList.remove("hidden");

        await loadEntries();
        await loadStats();
    } else {
        if (authToggleBtn) authToggleBtn.classList.remove("hidden");
        if (logoutBtn) logoutBtn.classList.add("hidden");
        if (profileBtn) profileBtn.classList.add("hidden");

        setStatsToZero();

        if (entriesList) {
            entriesList.innerHTML = "<p>Для просмотра записей необходимо войти в систему</p>";
        }
    }
}

window.saveProfile = async function () {
    const profile = {
        age: document.getElementById("profileAge").value,
        height: document.getElementById("profileHeight").value,
        weight: document.getElementById("profileWeight").value,
        gender: document.getElementById("profileGender").value,
        activity: document.getElementById("profileActivity").value,
        goal: document.getElementById("profileGoal").value
    };

    const response = await fetch("/api/profile/", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(profile)
    });

    const data = await response.json();

    if (!response.ok) {
        document.getElementById("profileMessage").textContent =
            "Необходимо войти в систему";
        return;
    }

    document.getElementById("profileMessage").textContent =
        "Профиль сохранён";

    document.getElementById("normProteins").textContent = data.proteins_norm;
    document.getElementById("normFats").textContent = data.fats_norm;
    document.getElementById("normCarbs").textContent = data.carbs_norm;
    document.getElementById("normCalories").textContent = data.calories_norm;
};

async function loadProfile() {
    const profileAge = document.getElementById("profileAge");

    if (!profileAge) return;

    const response = await fetch("/api/profile/", {
        credentials: "include"
    });

    if (!response.ok) return;

    const data = await response.json();

    if (!data.exists) return;

    document.getElementById("profileAge").value = data.age;
    document.getElementById("profileHeight").value = data.height;
    document.getElementById("profileWeight").value = data.weight;
    document.getElementById("profileGender").value = data.gender;
    document.getElementById("profileActivity").value = data.activity;
    document.getElementById("profileGoal").value = data.goal;

    document.getElementById("normProteins").textContent = data.proteins_norm;
    document.getElementById("normFats").textContent = data.fats_norm;
    document.getElementById("normCarbs").textContent = data.carbs_norm;
    document.getElementById("normCalories").textContent = data.calories_norm;
}

const logoutButton = document.getElementById("logoutBtn");

if (logoutButton) {
    logoutButton.addEventListener("click", logoutUser);
}

checkAuth();
loadProfile();