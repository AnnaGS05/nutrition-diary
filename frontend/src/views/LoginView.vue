<template>
    <div class="page">
        <section class="card auth-page">
            <h1>NutriLog</h1>
            <h2>Вход в аккаунт</h2>

            <input v-model="username" type="text" placeholder="Логин">
            <input v-model="password" type="password" placeholder="Пароль">

            <button @click="login">Войти</button>

            <p class="message">{{ message }}</p>

            <div class="auth-links">
                <p>Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link></p>
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
        async login() {
<<<<<<< HEAD
            const body = new URLSearchParams();
            body.append("username", this.username);
            body.append("password", this.password);
=======
            const username = this.username.trim();
            const password = this.password.trim();

            if (!username || !password) {
                this.message = "Введите логин и пароль";
                return;
            }

            if (username.length < 3 || username.length > 30) {
                this.message = "Логин должен содержать от 3 до 30 символов";
                return;
            }

            const body = new URLSearchParams();
            body.append("username", username);
            body.append("password", password);
>>>>>>> 3ddcdb1

            const response = await api.post("/auth/login", body, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            });

            this.message = response.data.message || response.data.error || "Ошибка входа";

            if (response.data.message) {
                setTimeout(() => {
                    this.$router.push("/");
                }, 500);
            }
        }
    }
};
</script>