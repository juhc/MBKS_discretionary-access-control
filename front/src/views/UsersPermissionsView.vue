<script setup>
import mbksApiInstance from '@/api';
import { useRoute } from 'vue-router';
import { computed, reactive, ref, watch } from 'vue';
import UsersPermissions from '@/components/UsersPermissions.vue'
import router from '@/router';

const route = useRoute();

const usersPermissions = ref([])
let tempUsersPermissions = []

const getUsersPermissions = async () => {
    await mbksApiInstance.get(`/files/${route.params.file_name}/users/permissions`).then((response) => {
        tempUsersPermissions = JSON.stringify(response.data);
        usersPermissions.value = response.data;
        isChanged.value = false;
    }).catch((error) => {
        if (error.response.data.detail == 'NO TG') {
            router.back();
            alert('Пользователь не может изменять права для этого файла')
        }
    })
}

const updatePermission = (permission, index) => {
    usersPermissions.value[index] = permission;
}

const sendUpdatedPermissions = async () => {
    let data = usersPermissions.value.map((element) => {
        return {
            id: element.permission_id,
            user_name: element.user_name,
            user_id: element.user_id,
            can_read: element.can_read,
            can_write: element.can_write,
            can_tg: element.can_tg
        }
    })
    data.file_name = route.params.file_name;
    await mbksApiInstance.patch(`/files/${data.file_name}/users/permissions/`, data).then((response) => {
        getUsersPermissions()
    })
}

getUsersPermissions();

const isPermissionsChanged = () => {
    return JSON.stringify(usersPermissions.value) !== tempUsersPermissions
}

const isChanged = ref(false)

watch(usersPermissions, (newValue, oldValue) => {
    isChanged.value = isPermissionsChanged();
}, { deep: true })
</script>

<template>
    <div class="flex flex-col">
        <UsersPermissions @updatePermission="updatePermission" :usersPermissions="usersPermissions"></UsersPermissions>
        <button @click="sendUpdatedPermissions" v-show="isChanged">Изменить</button>
    </div>
</template>