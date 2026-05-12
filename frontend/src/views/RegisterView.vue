<template>
    <div class="page">
        <section class="card auth-page">
            <h1>NutriLog</h1>
            <h2>Создать аккаунт</h2>

            <input v-model="username" type="text" placeholder="Придумайте логин">
            <input v-model="password" type="password" placeholder="Придумайте пароль">

            <button @click="register">Зарегистрироваться</button>

            <p class="message">{{ message }}</p>

            <div class="auth-links">
                <p>Уже есть аккаунт? <router-link to="/login">Войти</router-link></p>
                <p><router-link to="/">На главную</router-link></p>
            </div>
        </section>
    </div>
</template>

<script>
import api from "../api/client";

export default {
    data() {
        return {
            username: "",
            password: "",
            message: ""
        };
    },
    methods: {
        async register() {
            const body = new URLSearchParams();
            body.append("username", this.username);
            body.append("password", this.password);

            const response = await api.post("/auth/register", body, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            });

            this.message = response.data.message || response.data.error || "Ошибка регистрации";

            if (response.data.message) {
                setTimeout(() => {
                    this.$router.push("/login");
                }, 600);
            }
        }
    }
};
</script>