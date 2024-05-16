import { reactive, ref } from "vue"
import mbksApiInstance from "@/api/index.js"
import { defineStore } from "pinia"
import router from "@/router"


export const useAuthStore = defineStore('auth', () => {
    const userInfo = reactive({
        token: '',
        username: '',
        userId: ''
    })

    const authError = ref('')
    const isAuth = ref(false)

    const signIn = async (payload) => {
        try {
            let response = await mbksApiInstance.post("/auth/sign-in", { ...payload });
            userInfo.token = response.data.access_token
            userInfo.username = response.data.username
            userInfo.userId = response.data.user_id

            localStorage.setItem('userTokens', JSON.stringify({
                'access_token': userInfo.token
            }))

            isAuth.value = true
        } catch (err) {
            console.log(err)
        }
    }

    const signUp = async (payload) => {
        try {
            let response = await mbksApiInstance.post("/auth/sign-up", { ...payload });
        } catch (err) {
            console.log(err.response.err.data)
        }
    }

    const checkAuth = async () => {
        await mbksApiInstance.get("/users/me").then((response) => {
                userInfo.userId = response.data.id
                userInfo.username = response.data.name
                isAuth.value = true;
            }).catch((error) => {
                logout();
            })
    }

    const logout = () => {
        userInfo.value = {
            token: '',
            username: '',
            userId: ''
        }

        localStorage.clear();
        isAuth.value = false;
        router.push('/sign-in')
    }

    return { signIn, signUp, userInfo, checkAuth, isAuth, logout }
})