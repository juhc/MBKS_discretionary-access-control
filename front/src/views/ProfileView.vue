<script setup>
import FilesList from "@/components/FilesList.vue";
import FileMod from "@/components/FileMod.vue"
import { reactive, ref } from "vue";
import mbksApiInstance from "@/api";


const showFileDialog = ref(false)
const fileInfo = reactive({
    name: '',
    data: ''
})

const createFile = async () => {
    await mbksApiInstance.post('/files/', { data: fileInfo.data, name: fileInfo.name }).then((response) => {
        console.log(response)
    })
}
</script>

<template>
    <FileMod v-model:fileData="fileInfo.data" v-model:fileName="fileInfo.name" v-model:show="showFileDialog">
        <button @click="async () => await createFile()" class="bg-white border-2 border-black hover:bg-slate-500/25">
            Создать файл
        </button>
    </FileMod>
    <div>
        <button class="border-2 p-2 border-black" @click="showFileDialog = !showFileDialog">Добавиь файл</button>
        <div class="mt-[20px]">
            <FilesList/>
        </div>
    </div>
</template>