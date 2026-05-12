<template>
    <div class="page">
        <nav class="navbar">
            <router-link to="/" class="logo-text">NutriLog</router-link>

            <div class="nav-actions">
                <router-link to="/">Дневник</router-link>
                <router-link to="/profile">Профиль</router-link>
                <button @click="logout">Выйти</button>
            </div>
        </nav>

        <section class="card">
            <h2>Статистика питания</h2>
            <p class="message">Анализ потребления КБЖУ за последние 7 дней.</p>
        </section>

        <section class="stats">
            <div class="stat-card">
                <span>Средние калории</span>
                <strong>{{ average.calories }}</strong>
            </div>

            <div class="stat-card">
                <span>Средние белки</span>
                <strong>{{ average.proteins }}</strong>
            </div>

            <div class="stat-card">
                <span>Средние жиры</span>
                <strong>{{ average.fats }}</strong>
            </div>

            <div class="stat-card">
                <span>Средние углеводы</span>
                <strong>{{ average.carbs }}</strong>
            </div>
        </section>

        <section class="card">
            <h2>Калории за последние 7 дней</h2>
            <canvas id="caloriesChart"></canvas>
        </section>

        <section class="card">
            <h2>Лучший день по калориям</h2>
            <p class="message">{{ bestDayText }}</p>
        </section>
    </div>
</template>

<script>
import api from "../api/client";
import Chart from "chart.js/auto";

export default {
    data() {
        return {
            average: {
                calories: 0,
                proteins: 0,
                fats: 0,
                carbs: 0
            },
            bestDayText: "Данные пока не загружены",
            chart: null
        };
    },
    async mounted() {
        await this.loadStats();
    },
    methods: {
        async loadStats() {
            const response = await api.get("/api/stats/weekly");
            const data = response.data;

            this.average = data.average;
            this.bestDayText = `${data.best_day.date}: ${data.best_day.calories} ккал`;

            const canvas = document.getElementById("caloriesChart");

            this.chart = new Chart(canvas, {
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
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        },
        async logout() {
            await api.post("/auth/logout");
            this.$router.push("/login");
        }
    }
};
</script>