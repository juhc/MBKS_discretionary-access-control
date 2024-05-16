import { createRouter, createWebHistory } from "vue-router";
import SignInView from "@/views/SignInView.vue";
import SignUpView from "@/views/SignUpView.vue";
import ProfileView from "@/views/ProfileView.vue";
import UsersPermissionsView from "@/views/UsersPermissionsView.vue";
import { useAuthStore } from "@/stores/auth";


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/sign-in",
            name: "sign-in",
            component: SignInView,
            meta: {
                auth: false
            }
        },
        {
            path: "/sign-up",
            name: "sign-up",
            component: SignUpView,
            meta: {
                auth: false
            }
        },
        {
            path: "/profile",
            name: "profile",
            component: ProfileView,
            meta: {
                auth: true
            }
        },
        {
            path: "/permissions/:file_name",
            name: "users-permissions",
            component: UsersPermissionsView,
            meta: {
                auth: true
            }
        }
    ]
})

router.beforeEach((to, from, next) => {
    const tokens = JSON.parse(localStorage.getItem('userTokens'))
    let token = null
    if (tokens) {
        token = tokens.access_token
    }

    if (to.meta.auth && !token) {
        next('/sign-in')
    }
    else if (!to.meta.auth && token) {
        next('/profile')
    }
    else {
        next()
    }
})

export default router