const form = document.getElementById("entry-form");
const entriesList = document.getElementById("entries-list");
const refreshBtn = document.getElementById("refresh-btn");

async function loadEntries() {
    try {
        const response = await fetch("/api/entries/");
        const entries = await response.json();

        entriesList.innerHTML = "";

        if (entries.length === 0) {
            entriesList.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #94a3b8;">
                    <i class="fas fa-clipboard-list" style="font-size: 3rem; opacity: 0.3; margin-bottom: 12px;"></i>
                    <p>Пока нет записей</p>
                    <p style="font-size: 0.95rem;">Добавьте первый продукт через форму выше</p>
                </div>
            `;
            return;
        }

        entries.forEach(entry => {
            const div = document.createElement("div");
            div.className = "entry-card";
            div.innerHTML = `
                <strong>${entry.name}</strong>
                <div class="nutrients">
                    <div class="nutrient">
                        <small>Белки</small>
                        <span>${entry.proteins} г</span>
                    </div>
                    <div class="nutrient">
                        <small>Жиры</small>
                        <span>${entry.fats} г</span>
                    </div>
                    <div class="nutrient">
                        <small>Углеводы</small>
                        <span>${entry.carbs} г</span>
                    </div>
                    <div class="nutrient" style="background: #eff6ff; border-color: #bfdbfe;">
                        <small>Калории</small>
                        <span style="color: #1e40af;">${entry.calories} ккал</span>
                    </div>
                </div>
            `;
            entriesList.appendChild(div);
        });
    } catch (error) {
        console.error("Ошибка загрузки записей:", error);
    }
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        name: document.getElementById("name").value.trim(),
        proteins: parseFloat(document.getElementById("proteins").value) || 0,
        fats: parseFloat(document.getElementById("fats").value) || 0,
        carbs: parseFloat(document.getElementById("carbs").value) || 0,
        calories: parseFloat(document.getElementById("calories").value) || 0
    };

    try {
        const response = await fetch("/api/entries/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            form.reset();
            loadEntries();

            const btn = form.querySelector("button");
            const originalText = btn.innerHTML;
            btn.innerHTML = `<i class="fas fa-check"></i> Добавлено!`;
            btn.style.background = "#10b981";

            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.style.background = "";
            }, 1800);
        } else {
            alert("Ошибка при добавлении записи");
        }
    } catch (error) {
        alert("Ошибка соединения с сервером");
    }
});

refreshBtn.addEventListener("click", loadEntries);

loadEntries();