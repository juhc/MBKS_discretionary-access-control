<script setup>
import Header from "@/components/Header.vue"
import { useAuthStore } from "./stores/auth";

const authStore = useAuthStore()
authStore.checkAuth();

</script>

<template>
  <div class="px-8">
  <Header />
    <RouterView />
  </div>
</template>
