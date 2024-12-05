import axios from "axios";

// Set up the base API client
const api = axios.create({
    baseURL: "http://localhost:8000", // Backend API URL
});

// Add a request interceptor to include the Bearer token (if available)
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token"); // Retrieve token from localStorage
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;