import { createRouter, createWebHistory } from "vue-router";

import DiaryView from "../views/DiaryView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import ProfileView from "../views/ProfileView.vue";
import StatsView from "../views/StatsView.vue";

const routes = [
    { path: "/", component: DiaryView },
    { path: "/login", component: LoginView },
    { path: "/register", component: RegisterView },
    { path: "/profile", component: ProfileView },
    { path: "/stats", component: StatsView }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;