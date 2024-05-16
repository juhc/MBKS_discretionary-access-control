<script setup>
const props = defineProps({
    fileName: String,
    fileData: String
})

const show = defineModel('show')
</script>

<template>
    <div @click.stop="show = !show" v-if="show" class="fixed flex bg-black/50 inset-0">
        <div @click.stop class="p-2 flex flex-col m-auto bg-white min-h-[50px] min-w-[300px] py-5">
            <span class="font-bold italic">Название файла</span>
            <span>{{ fileName }}</span>
            <span class="font-bold italic">Содержимое</span>
            <span> {{ fileData }}</span>
            <button class="border-2 border-black hover:bg-slate-500/25" @click ="show = !show">Закрыть</button>
        </div>
    </div>
</template>