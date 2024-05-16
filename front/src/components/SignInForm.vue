<script setup>
import { useAuthStore } from '@/stores/auth';
import { ref } from 'vue';
import { useRouter } from 'vue-router';


const authStore = useAuthStore();
const router = useRouter();

const username = ref('');
const password = ref('');

const signIn = async () => {
    await authStore.signIn({ name: username.value, password: password.value });
    router.push('/profile')
}
</script>

<template>
    <div class="flex flex-col items-center">
        <div class="text-2xl">Вход</div>
        <form class="flex flex-col w-96">
            <label for="username">Имя пользователя</label>
            <input name="username" type="text" placeholder="Ivan" v-model="username">
            <label for="password">Пароль</label>
            <input name="password" type="password" placeholder="12345" v-model="password">
            <input @click.prevent="signIn" class="hover:cursor-pointer hover:border border-indigo-500" type="submit"
                value="Войти">
        </form>
    </div>
</template>