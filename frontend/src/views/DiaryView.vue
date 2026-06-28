<template>
    <div class="page">
        <header class="hero">
            <div class="hero-topbar">
                <router-link v-if="authenticated" to="/profile" class="hero-auth-btn secondary">
                    Профиль
                </router-link>

                <router-link v-if="authenticated" to="/stats" class="hero-auth-btn secondary">
                    Статистика
                </router-link>

                <router-link v-if="!authenticated" to="/login" class="hero-auth-btn primary">
                    Войти
                </router-link>

                <button v-if="authenticated" class="hero-auth-btn secondary" @click="logout">
                    Выйти
                </button>
            </div>

            <div class="hero-content">
                <div>
                    <h1>NutriLog</h1>
                    <p>Персональный дневник питания с анализом КБЖУ и статистикой</p>
                    <div class="hero-badges">
                        <span>Контроль КБЖУ</span>
                        <span>История питания</span>
                        <span>Умная аналитика</span>
                    </div>
                </div>
                <img src="../assets/hero.png" alt="Hero">
            </div>
        </header>

        <main>
            <section class="card">
                <h2>{{ editingId ? "Редактировать запись" : "Добавить запись питания" }}</h2>

                <div class="date-row">
                    <label for="entryDate">Дата дневника:</label>
                    <input id="entryDate" v-model="entryDate" type="date" @change="loadData">
                </div>

                <div class="form-grid">
                    <div class="form-field">
                        <label>Название блюда</label>
                        <input v-model="entry.name" placeholder="Например: Гречка с курицей">
                    </div>
                    <div class="form-field">
                        <label>Белки, г</label>
                        <input v-model.number="entry.proteins" type="number" placeholder="0">
                    </div>
                    <div class="form-field">
                        <label>Жиры, г</label>
                        <input v-model.number="entry.fats" type="number" placeholder="0">
                    </div>
                    <div class="form-field">
                        <label>Углеводы, г</label>
                        <input v-model.number="entry.carbs" type="number" placeholder="0">
                    </div>
                    <div class="form-field">
                        <label>Калории, ккал</label>
                        <input v-model.number="entry.calories" type="number" placeholder="0">
                    </div>
                </div>

                <div class="form-actions">
                    <button @click="saveEntry" :disabled="loading">
                        {{ loading ? "Сохранение..." : (editingId ? "Сохранить изменения" : "Добавить запись") }}
                    </button>
                    <button v-if="editingId" class="secondary" type="button" @click="cancelEdit">
                        Отмена
                    </button>
                </div>
                <p class="message">{{ message }}</p>
            </section>

            <section class="stats">
                <div class="stat-card">
                    <span>Белки</span>
                    <strong>{{ stats.proteins }} / {{ stats.proteins_norm }}</strong>
                </div>
                <div class="stat-card">
                    <span>Жиры</span>
                    <strong>{{ stats.fats }} / {{ stats.fats_norm }}</strong>
                </div>
                <div class="stat-card">
                    <span>Углеводы</span>
                    <strong>{{ stats.carbs }} / {{ stats.carbs_norm }}</strong>
                </div>
                <div class="stat-card">
                    <span>Калории</span>
                    <strong>{{ stats.calories }} / {{ stats.calories_norm }}</strong>
                </div>
            </section>

            <section class="card">
                <h2>Мои записи</h2>

                <div v-if="!authenticated" class="entries">
                    <p>Для просмотра записей необходимо войти в систему</p>
                </div>

                <div v-else-if="entries.length === 0" class="entries">
                    <p>Записей за выбранную дату пока нет</p>
                </div>

                <div v-else class="entries">
                    <div
                        v-for="item in entries"
                        :key="item.id"
                        class="entry"
                        :class="{ 'entry-editing': editingId === item.id }"
                    >
                        <div><strong class="entry-title">{{ item.name }}</strong></div>
                        <div>Б: {{ item.proteins }} г</div>
                        <div>Ж: {{ item.fats }} г</div>
                        <div>У: {{ item.carbs }} г</div>
                        <div>{{ item.calories }} ккал</div>
                        <div class="entry-actions">
                            <button class="edit" @click="startEdit(item)">Изменить</button>
                            <button class="danger" @click="deleteEntry(item.id)">Удалить</button>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </div>
</template>

<script>
import api from "../api/client";

export default {
    data() {
        return {
            authenticated: false,
            entryDate: new Date().toISOString().slice(0, 10),
            entries: [],
            stats: {
                proteins: 0,
                fats: 0,
                carbs: 0,
                calories: 0,
                proteins_norm: 0,
                fats_norm: 0,
                carbs_norm: 0,
                calories_norm: 0
            },
            entry: {
                name: "",
                proteins: 0,
                fats: 0,
                carbs: 0,
                calories: 0
            },
            editingId: null,
            message: "",
            loading: false
        };
    },
    async mounted() {
        await this.checkAuth();
        await this.loadData();
    },
    methods: {
        async checkAuth() {
            try {
                const response = await api.get("/auth/me");
                this.authenticated = Boolean(response.data.authenticated);
            } catch {
                this.authenticated = false;
            }
        },
        async loadData() {
            if (!this.authenticated) return;
            try {
                const entriesResponse = await api.get(`/api/entries/?entry_date=${this.entryDate}`);
                this.entries = entriesResponse.data;

                const statsResponse = await api.get(`/api/stats?entry_date=${this.entryDate}`);
                this.stats = statsResponse.data;
            } catch {
                this.message = "Не удалось загрузить данные";
            }
        },
        startEdit(item) {
            this.editingId = item.id;
            this.entry = {
                name: item.name,
                proteins: item.proteins,
                fats: item.fats,
                carbs: item.carbs,
                calories: item.calories
            };
            this.message = "";
        },
        cancelEdit() {
            this.editingId = null;
            this.entry = { name: "", proteins: 0, fats: 0, carbs: 0, calories: 0 };
            this.message = "";
        },
        validateEntry(name, proteins, fats, carbs, calories) {
            if (!name) {
                this.message = "Введите название блюда";
                return false;
            }
            if (name.length > 100) {
                this.message = "Название блюда не должно превышать 100 символов";
                return false;
            }
            if ([proteins, fats, carbs, calories].some(v => v < 0)) {
                this.message = "Значения КБЖУ не могут быть отрицательными";
                return false;
            }
            if (calories > 10000) {
                this.message = "Калорийность одной записи не должна превышать 10000";
                return false;
            }
            return true;
        },
        async saveEntry() {
            if (!this.authenticated) {
                this.message = "Для добавления записи необходимо войти";
                setTimeout(() => this.$router.push("/login"), 700);
                return;
            }

            const name = this.entry.name.trim();
            const proteins = Number(this.entry.proteins || 0);
            const fats = Number(this.entry.fats || 0);
            const carbs = Number(this.entry.carbs || 0);
            const calories = Number(this.entry.calories || 0);

            if (!this.validateEntry(name, proteins, fats, carbs, calories)) return;

            this.loading = true;
            try {
                if (this.editingId) {
                    await api.put(`/api/entries/${this.editingId}`, {
                        name, proteins, fats, carbs, calories,
                        entry_date: this.entryDate
                    });
                    this.message = "Запись обновлена ✓";
                } else {
                    await api.post("/api/entries/", {
                        name, proteins, fats, carbs, calories,
                        entry_date: this.entryDate
                    });
                    this.message = "Запись добавлена ✓";
                }

                this.cancelEdit();
                await this.loadData();
            } catch {
                this.message = this.editingId
                    ? "Не удалось обновить запись"
                    : "Не удалось добавить запись";
            } finally {
                this.loading = false;
            }
        },
        async deleteEntry(id) {
            try {
                await api.delete(`/api/entries/${id}`);
                if (this.editingId === id) this.cancelEdit();
                await this.loadData();
            } catch {
                this.message = "Не удалось удалить запись";
            }
        },
        async logout() {
            try {
                await api.post("/auth/logout");
            } finally {
                localStorage.removeItem("csrf_token");
                this.$router.push("/login");
            }
        }
    }
};
</script>

<style scoped>
.form-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
}

.form-field {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.form-field label {
    font-size: 13px;
    color: #666;
    font-weight: 500;
}

.form-field input {
    width: 100%;
}

.form-actions {
    display: flex;
    gap: 10px;
    align-items: center;
}

.form-actions button.secondary {
    background: transparent;
    border: 1px solid #ccc;
    color: #555;
}

.entry-editing {
    outline: 2px solid #4a9c5e;
    background: rgba(74, 156, 94, 0.06);
}

.entry-actions {
    display: flex;
    gap: 8px;
}

.entry-actions button.edit {
    background: #f0f4f1;
    color: #2f6e44;
    border: 1px solid #c9ddcd;
}

@media (max-width: 700px) {
    .form-grid {
        grid-template-columns: 1fr 1fr;
    }
}
</style>