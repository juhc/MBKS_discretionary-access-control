import axios from "axios";
import { useAuthStore } from "@/stores/auth";

const mbksApiInstance = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 1000
})

mbksApiInstance.interceptors.request.use((config) => {
    if (localStorage.getItem('userTokens')) {
        config.headers.Authorization = `Bearer ${JSON.parse(localStorage.getItem('userTokens')).access_token}`
    }

    return config
})

export default mbksApiInstance