<template>
    <div class="page">
        <nav class="navbar">
            <router-link to="/" class="logo-text">NutriLog</router-link>

            <div class="nav-actions">
                <router-link to="/">Дневник</router-link>
                <router-link to="/stats">Статистика</router-link>
                <button @click="logout">Выйти</button>
            </div>
        </nav>

        <section class="card">
            <h2>Профиль пользователя</h2>

            <div class="profile-grid">
                <div>
                    <label>Возраст</label>
                    <input v-model.number="profile.age" type="number" placeholder="Возраст">
                </div>

                <div>
                    <label>Рост, см</label>
                    <input v-model.number="profile.height" type="number" placeholder="Рост">
                </div>

                <div>
                    <label>Вес, кг</label>
                    <input v-model.number="profile.weight" type="number" placeholder="Вес">
                </div>

                <div>
                    <label>Пол</label>
                    <select v-model="profile.gender">
                        <option value="male">Мужской</option>
                        <option value="female">Женский</option>
                    </select>
                </div>

                <div>
                    <label>Активность</label>
                    <select v-model.number="profile.activity">
                        <option :value="1.2">Минимальная</option>
                        <option :value="1.375">Лёгкая</option>
                        <option :value="1.55">Средняя</option>
                        <option :value="1.725">Высокая</option>
                    </select>
                </div>

                <div>
                    <label>Цель</label>
                    <select v-model="profile.goal">
                        <option value="loss">Похудение</option>
                        <option value="maintain">Поддержание веса</option>
                        <option value="gain">Набор массы</option>
                    </select>
                </div>
            </div>

            <button @click="saveProfile">Сохранить профиль</button>
            <p class="message">{{ message }}</p>
        </section>

        <section class="stats">
            <div class="stat-card">
                <span>Норма белков</span>
                <strong>{{ norms.proteins_norm }}</strong>
            </div>
            <div class="stat-card">
                <span>Норма жиров</span>
                <strong>{{ norms.fats_norm }}</strong>
            </div>
            <div class="stat-card">
                <span>Норма углеводов</span>
                <strong>{{ norms.carbs_norm }}</strong>
            </div>
            <div class="stat-card">
                <span>Норма калорий</span>
                <strong>{{ norms.calories_norm }}</strong>
            </div>
        </section>
    </div>
</template>

<script>
import api from "../api/client";

export default {
    data() {
        return {
            profile: {
                age: "",
                height: "",
                weight: "",
                gender: "male",
                activity: 1.55,
                goal: "maintain"
            },
            norms: {
                proteins_norm: 0,
                fats_norm: 0,
                carbs_norm: 0,
                calories_norm: 0
            },
            message: ""
        };
    },
    async mounted() {
        await this.loadProfile();
    },
    methods: {
        async loadProfile() {
            const response = await api.get("/api/profile/");

            if (!response.data.exists) return;

            this.profile = {
                age: response.data.age,
                height: response.data.height,
                weight: response.data.weight,
                gender: response.data.gender,
                activity: response.data.activity,
                goal: response.data.goal
            };

            this.norms = {
                proteins_norm: response.data.proteins_norm,
                fats_norm: response.data.fats_norm,
                carbs_norm: response.data.carbs_norm,
                calories_norm: response.data.calories_norm
            };
        },
        async saveProfile() {
            const response = await api.post("/api/profile/", this.profile);

            this.message = "Профиль сохранён ✓";

            this.norms = {
                proteins_norm: response.data.proteins_norm,
                fats_norm: response.data.fats_norm,
                carbs_norm: response.data.carbs_norm,
                calories_norm: response.data.calories_norm
            };

            await this.loadProfile();
        },
        async logout() {
            await api.post("/auth/logout");
            this.$router.push("/login");
        }
    }
};
</script>