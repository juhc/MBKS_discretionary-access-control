<script setup>
import mbksApiInstance from '@/api';
import { computed, reactive, ref, watch } from 'vue';
import FileMod from "@/components/FileMod.vue"
import FileInfo from "@/components/FileInfo.vue"
import { useAuthStore } from '@/stores/auth';

const files = ref([])
const isShowFileInfo = ref(false)
const isShowFileMod = ref(false)
const authStore = useAuthStore();

const fileName = ref('')
const fileData = ref('')

const isError = ref(false)

const textGreenClass = ref('text-green-500')
const textRedClass = ref('text-red-500')

let oldFileName = '';

const showFileInfo = () => {
    if (isError.value) {
        alert('У пользователя нет прав для чтения файла')
        getUserFiles
    }
    else {
        isShowFileInfo.value = !isShowFileInfo.value;
    }
}

const showFileMod = (file_name) => {
    isShowFileMod.value = !isShowFileMod.value
    oldFileName = file_name;
    if (!isError.value) {
        fileName.value = file_name;
        fileData.value = '';
    }
}

const modifyUserFile = async () => {
    await mbksApiInstance.patch(`/files/${oldFileName}`, {
        name: fileName.value, data: fileData.value
    }).then(async (response) => {
        alert('Файл изменен');
        await getUserFiles();
    }).catch(async (error) => {
        if (error.response.data.detail == 'NO WRITE') {
            alert('У пользователя нет прав на изменение файла')
            await getUserFiles();
        }
    })
}

const getUserFile = async (file_name) => {
    isError.value = false
    await mbksApiInstance.get(`/files/${file_name}`).then((response) => {
        fileName.value = response.data.name;
        fileData.value = response.data.data;
    }).catch((error) => {
        isError.value = true;
        let errorMessage = error.response.data.detail;
    })
}

const getUserFiles = async () => {
    await mbksApiInstance.get('/files/permissions/me').then((response) => {
        files.value = response.data
        console.log(response)
    }).catch((error) => {
        console.log(error)
    })
}

const isUserOwner = computed(() => {
    return authStore.userInfo.username
})

getUserFiles()

watch(files, (newFiles, oldFiles) => {

})
</script>

<template>
    <FileInfo v-model:show="isShowFileInfo" :fileData="fileData" :fileName="fileName"></FileInfo>
    <FileMod v-model:fileData="fileData" v-model:fileName="fileName" v-model:show="isShowFileMod">
        <button class="border-2 border-black hover:bg-slate-500/25" @click="modifyUserFile()">Изменить файл</button>
    </FileMod>
    <table class="table-auto w-[800px] border-collapse border border-slate-500">
        <thead>
            <tr>
                <th class="border border-slate-600">Имя файла</th>
                <th class="border border-slate-600">Владелец</th>
                <th class="border border-slate-600">Чтение</th>
                <th class="border border-slate-600">Запись</th>
                <th class="border border-slate-600">Передача прав</th>
                <th class="border border-slate-600">Содержимое</th>
                <th class="border border-slate-600">Редактирование</th>
                <th class="border border-slate-600">Права пользователей</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="file in  files " :key="file.id">
                <td class="border border-slate-700">{{ file.file_name }}</td>
                <td class="border border-slate-700">{{ file.user_name }}</td>
                <td class="border font-bold border-slate-700" :class="[file.can_read ? textGreenClass : textRedClass]">
                    {{
        file.can_read ? '+' : '-' }}
                </td>
                <td class="border font-bold border-slate-700" :class="[file.can_write ? textGreenClass : textRedClass]">
                    {{
        file.can_write ? '+' : '-' }}</td>
                <td class="border font-bold border-slate-700" :class="[file.can_tg ? textGreenClass : textRedClass]">{{
        file.can_tg ? '+' : '-' }}</td>
                <td class="border border-slate-700">
                    <button v-if="file.can_read" class="border-2 border-black hover:bg-slate-500/25"
                        @click="async () => { await getUserFile(file.file_name); showFileInfo(); }">
                        Прочитать
                    </button>
                </td>
                <td class="border border-slate-700">
                    <button v-if="file.can_write" class="border-2 border-black hover:bg-slate-500/25"
                        @click="() => { getUserFile(file.file_name); showFileMod(file.file_name) }">
                        Изменить
                    </button>
                </td>
                <td class="border border-slate-700">
                    <RouterLink v-if="file.can_tg"
                        :to="{ name: 'users-permissions', params: { file_name: file.file_name } }">Права пользователей
                    </RouterLink>
                </td>
                <td v-if="isUserOwner == file.user_name">
                    <button class="border-2 border-black hover:bg-slate-500/25">Изменить владельца</button>
                </td>
            </tr>
        </tbody>
    </table>
</template>