import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
    withCredentials: true
});

function getCookie(name) {
    const match = document.cookie.match(
        new RegExp("(^| )" + name + "=([^;]+)")
    );
    return match ? decodeURIComponent(match[2]) : null;
}

api.interceptors.request.use(config => {
    const csrf = localStorage.getItem("csrf_token") || getCookie("csrf_token");

    if (csrf) {
        config.headers["X-CSRF-Token"] = csrf;
    }

    return config;
});

export default api;