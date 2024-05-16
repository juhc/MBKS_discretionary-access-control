<script setup>
import { useAuthStore } from "@/stores/auth";
import { computed } from "vue"
import { useRouter } from "vue-router";


const authStore = useAuthStore();
const router = useRouter();

const isAuth = computed(() => authStore.isAuth);

const logout = () => {
    authStore.logout();
    router.push('/sign-in')
}
</script>


<template>
    <div class="flex flex-row gap-x-4 justify-end" v-if="isAuth">
        <RouterLink to="/profile">Профиль</RouterLink>
        <div @click="logout" class="hover:cursor-pointer">Выход</div>
    </div>
    <div class="flex flex-row gap-x-4 justify-end" v-else>
        <RouterLink to="/sign-in">Вход</RouterLink>
        <RouterLink to="/sign-up">Регистрация</RouterLink>
    </div>

</template>