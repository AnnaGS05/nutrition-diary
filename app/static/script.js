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
    try {
        const response = await fetch("/auth/me", {
            credentials: "include"
        });

        if (!response.ok) return false;

        const data = await response.json();
        return Boolean(data.authenticated);
    } catch {
        return false;
    }
}

function getSelectedDate() {
    const input = document.getElementById("entryDate");

    if (!input) {
        return new Date().toISOString().slice(0, 10);
    }

    if (!input.value) {
        input.value = new Date().toISOString().slice(0, 10);
    }

    return input.value;
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

    if (message) {
        message.textContent = data.message || data.error || "Ошибка входа";
    }

    if (response.ok) {
        setTimeout(() => {
            window.location.href = "/";
        }, 600);
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

    if (response.ok) {
        setTimeout(() => {
            window.location.href = "/login";
        }, 700);
    }
};

window.logoutUser = async function () {
    await fetch("/auth/logout", {
        method: "POST",
        credentials: "include"
    });

    window.location.href = "/";
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
        calories: Number(document.getElementById("entryCalories").value || 0),
        entry_date: getSelectedDate()
    };

    await request("/api/entries/", {
        method: "POST",
        body: JSON.stringify(entry)
    });

    if (entryMessage) {
        entryMessage.textContent = "Запись добавлена ✓";
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
    const entryDate = getSelectedDate();

    const response = await fetch(`/api/entries/?entry_date=${entryDate}`, {
        credentials: "include"
    });

    if (!response.ok) return;

    const entries = await response.json();
    const list = document.getElementById("entriesList");

    if (!list) return;

    list.innerHTML = "";

    if (entries.length === 0) {
        list.innerHTML = "<p>Записей за выбранную дату пока нет</p>";
        return;
    }

    entries.forEach(entry => {
        const item = document.createElement("div");
        item.className = "entry";
        item.innerHTML = `
            <div><strong class="entry-title">${entry.name}</strong></div>
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
    const entryDate = getSelectedDate();

    const response = await fetch(`/api/stats?entry_date=${entryDate}`, {
        credentials: "include"
    });

    if (!response.ok) return;

    const stats = await response.json();

    setStat("totalProteins", stats.proteins, stats.proteins_norm);
    setStat("totalFats", stats.fats, stats.fats_norm);
    setStat("totalCarbs", stats.carbs, stats.carbs_norm);
    setStat("totalCalories", stats.calories, stats.calories_norm);
}

function setStat(elementId, value, norm) {
    const el = document.getElementById(elementId);

    if (el) {
        el.textContent = `${value} / ${norm}`;
    }
}

window.saveProfile = async function () {
    const profile = {
        age: Number(document.getElementById("profileAge").value),
        height: Number(document.getElementById("profileHeight").value),
        weight: Number(document.getElementById("profileWeight").value),
        gender: document.getElementById("profileGender").value,
        activity: parseFloat(document.getElementById("profileActivity").value),
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
    const message = document.getElementById("profileMessage");

    if (message) {
        message.textContent = response.ok ? "Профиль сохранён ✓" : "Ошибка сохранения";
    }

    if (response.ok) {
        setProfileNorms(data);
        await loadProfile();
    }
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

    document.getElementById("profileAge").value = data.age || "";
    document.getElementById("profileHeight").value = data.height || "";
    document.getElementById("profileWeight").value = data.weight || "";
    document.getElementById("profileGender").value = data.gender || "male";
    document.getElementById("profileActivity").value = data.activity || "1.55";
    document.getElementById("profileGoal").value = data.goal || "maintain";

    setProfileNorms(data);
}

function setProfileNorms(data) {
    const proteins = document.getElementById("normProteins");
    const fats = document.getElementById("normFats");
    const carbs = document.getElementById("normCarbs");
    const calories = document.getElementById("normCalories");

    if (proteins) proteins.textContent = data.proteins_norm || 0;
    if (fats) fats.textContent = data.fats_norm || 0;
    if (carbs) carbs.textContent = data.carbs_norm || 0;
    if (calories) calories.textContent = data.calories_norm || 0;
}

async function checkAuth() {
    const authenticated = await isAuthenticated();

    const authToggleBtn = document.getElementById("authToggleBtn");
    const logoutBtn = document.getElementById("logoutBtn");
    const profileBtn = document.getElementById("profileBtn");
    const statsBtn = document.getElementById("statsBtn");

    if (authenticated) {
        if (authToggleBtn) authToggleBtn.classList.add("hidden");
        if (logoutBtn) logoutBtn.classList.remove("hidden");
        if (profileBtn) profileBtn.classList.remove("hidden");
        if (statsBtn) statsBtn.classList.remove("hidden");

        await loadEntries();
        await loadStats();
    } else {
        if (authToggleBtn) authToggleBtn.classList.remove("hidden");
        if (logoutBtn) logoutBtn.classList.add("hidden");
        if (profileBtn) profileBtn.classList.add("hidden");
        if (statsBtn) statsBtn.classList.add("hidden");
    }
}

async function loadWeeklyStats() {
    const response = await fetch("/api/stats/weekly", {
        credentials: "include"
    });

    if (!response.ok) return;

    const data = await response.json();

    const avgCalories = document.getElementById("avgCalories");
    const avgProteins = document.getElementById("avgProteins");
    const avgFats = document.getElementById("avgFats");
    const avgCarbs = document.getElementById("avgCarbs");

    if (avgCalories) avgCalories.textContent = data.average.calories;
    if (avgProteins) avgProteins.textContent = data.average.proteins;
    if (avgFats) avgFats.textContent = data.average.fats;
    if (avgCarbs) avgCarbs.textContent = data.average.carbs;

    setPercent("caloriesPercent", data.average.calories, data.norm.calories);
    setPercent("proteinsPercent", data.average.proteins, data.norm.proteins);
    setPercent("fatsPercent", data.average.fats, data.norm.fats);
    setPercent("carbsPercent", data.average.carbs, data.norm.carbs);

    const bestDayText = document.getElementById("bestDayText");

    if (bestDayText) {
        bestDayText.textContent =
            `${data.best_day.date}: ${data.best_day.calories} ккал`;
    }

    const chart = document.getElementById("caloriesChart");

    if (!chart || typeof Chart === "undefined") return;

    new Chart(chart, {
        type: "line",
        data: {
            labels: data.days.map(day => day.label),
            datasets: [
                {
                    label: "Калории",
                    data: data.days.map(day => day.calories),
                    borderColor: "#4a9c5e",
                    backgroundColor: "rgba(74,156,94,0.18)",
                    fill: true,
                    tension: 0.35
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function setPercent(elementId, value, norm) {
    const element = document.getElementById(elementId);

    if (!element) return;

    if (!norm) {
        element.textContent = "0%";
        return;
    }

    element.textContent = `${Math.round(value / norm * 100)}%`;
}

document.addEventListener("DOMContentLoaded", () => {
    const dateInput = document.getElementById("entryDate");

    if (dateInput) {
        dateInput.value = new Date().toISOString().slice(0, 10);

        dateInput.addEventListener("change", () => {
            loadEntries();
            loadStats();
        });
    }

    checkAuth();
    loadProfile();

    if (location.pathname === "/stats") {
        loadWeeklyStats();
    }
});