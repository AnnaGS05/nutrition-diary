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
                <h2>Добавить запись питания</h2>

                <div class="date-row">
                    <label for="entryDate">Дата дневника:</label>
                    <input id="entryDate" v-model="entryDate" type="date" @change="loadData">
                </div>

                <div class="form-grid">
                    <input v-model="entry.name" placeholder="Название блюда">
                    <input v-model.number="entry.proteins" type="number" placeholder="Белки">
                    <input v-model.number="entry.fats" type="number" placeholder="Жиры">
                    <input v-model.number="entry.carbs" type="number" placeholder="Углеводы">
                    <input v-model.number="entry.calories" type="number" placeholder="Калории">
                </div>

                <button @click="addEntry">Добавить запись</button>
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
                    <div v-for="item in entries" :key="item.id" class="entry">
                        <div><strong class="entry-title">{{ item.name }}</strong></div>
                        <div>Б: {{ item.proteins }}</div>
                        <div>Ж: {{ item.fats }}</div>
                        <div>У: {{ item.carbs }}</div>
                        <div>{{ item.calories }} ккал</div>
                        <button class="danger" @click="deleteEntry(item.id)">Удалить</button>
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
            message: ""
        };
    },
    async mounted() {
        await this.checkAuth();
        await this.loadData();
    },
    methods: {
        async checkAuth() {
            const response = await api.get("/auth/me");
            this.authenticated = Boolean(response.data.authenticated);
        },
        async loadData() {
            if (!this.authenticated) return;

            const entriesResponse = await api.get(`/api/entries/?entry_date=${this.entryDate}`);
            this.entries = entriesResponse.data;

            const statsResponse = await api.get(`/api/stats?entry_date=${this.entryDate}`);
            this.stats = statsResponse.data;
        },
        async addEntry() {
            if (!this.authenticated) {
                this.message = "Для добавления записи необходимо войти";
                setTimeout(() => this.$router.push("/login"), 700);
                return;
            }

            await api.post("/api/entries/", {
                ...this.entry,
                entry_date: this.entryDate
            });

            this.message = "Запись добавлена ✓";

            this.entry = {
                name: "",
                proteins: 0,
                fats: 0,
                carbs: 0,
                calories: 0
            };

            await this.loadData();
        },
        async deleteEntry(id) {
            await api.delete(`/api/entries/${id}`);
            await this.loadData();
        },
        async logout() {
            await api.post("/auth/logout");
            this.$router.push("/login");
        }
    }
};
</script>