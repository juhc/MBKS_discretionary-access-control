<script setup>
import { useAuthStore } from "@/stores/auth"
import { ref } from "vue"
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const username = ref('');
const password = ref('');
const password_repeat = ref('');

const signUp = async() => {
    await authStore.signUp({name:username.value, password:password.value});
    router.push('/sign-in');
}

</script>

<template>
    <div class="flex flex-col items-center">
        <div class="text-2xl">Регистрация</div>
        <form class="flex flex-col w-96">
            <label for="username">Имя пользователя</label>
            <input name="username" v-model="username" type="text" placeholder="Ivan">
            <label for="password">Пароль</label>
            <input name="password" v-model="password" type="password" placeholder="12345">
            <label for="password_repeat">Повторите пароль</label>
            <input name="password_repeat" v-model="password_repeat" type="password" placeholder="12345">
            <input @click.prevent="signUp" class="hover:cursor-pointer hover:border border-indigo-500" type="submit" value="Зарегистрироваться">
        </form>
    </div>
</template>