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

            if (password.length < 6 || password.length > 50) {
                this.message = "Пароль должен содержать от 6 до 50 символов";
                return;
            }

            const body = new URLSearchParams();
            body.append("username", username);
            body.append("password", password);
>>>>>>> 3ddcdb1

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