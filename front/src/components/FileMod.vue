<script setup>
const show = defineModel('show')
const fileName = defineModel('fileName');
const fileData = defineModel('fileData');
</script>

<template>
    <div @click.stop="show = !show" v-if="show" class="fixed flex bg-black/50 inset-0">
        <div @click.stop class="p-2 flex flex-col m-auto bg-white min-h-[50px] min-w-[300px] py-5">
            <label class="font-bold italic">Название</label>
            <input v-model="fileName" placeholder="Название файла...">
            <label class="font-bold italic">Содержимое</label>
            <textarea v-model="fileData" placeholder="Введите текст..."></textarea>
            <slot></slot>
        </div>
    </div>
</template>