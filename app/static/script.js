const form = document.getElementById("entry-form");
const entriesList = document.getElementById("entries-list");

async function loadEntries() {
    const response = await fetch("/api/entries/");
    const entries = await response.json();

    entriesList.innerHTML = "";

    if (entries.length === 0) {
        entriesList.innerHTML = "<p>Пока нет записей</p>";
        return;
    }

    entries.forEach(entry => {
        const card = document.createElement("div");
        card.className = "entry-card";

        card.innerHTML = `
            <h3>${entry.name}</h3>
            <p>Белки: ${entry.proteins} г</p>
            <p>Жиры: ${entry.fats} г</p>
            <p>Углеводы: ${entry.carbs} г</p>
            <p>Калории: ${entry.calories} ккал</p>
        `;

        entriesList.appendChild(card);
    });
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = {
        name: document.getElementById("name").value,
        proteins: Number(document.getElementById("proteins").value),
        fats: Number(document.getElementById("fats").value),
        carbs: Number(document.getElementById("carbs").value),
        calories: Number(document.getElementById("calories").value)
    };

    await fetch("/api/entries/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    form.reset();
    loadEntries();
});

loadEntries();