<script setup>
const props = defineProps(['usersPermissions'])
</script>

<template>
    <table class="table-auto w-[800px] border-collapse border border-slate-500">
        <thead>
            <tr>
                <th class="border border-slate-600">Пользователь</th>
                <th class="border border-slate-600">Чтение</th>
                <th class="border border-slate-600">Запись</th>
                <th class="border border-slate-600">Передача прав</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(permission, index) in usersPermissions" :key="permission.permission_id">
                <td class="border border-slate-700">{{ permission.user_name }}</td>
                <td class="border border-slate-700">
                    <input v-model="permission.can_read" @change="$emit('updatePermission', permission, index)"
                        class="hover:cursor-pointer" type="checkbox"></input>
                </td>
                <td class="border border-slate-700">
                    <input v-model="permission.can_write" @change="$emit('updatePermission', permission, index)"
                        class="hover:cursor-pointer" type="checkbox"></input>
                </td>
                <td class="border border-slate-700">
                    <input v-model="permission.can_tg" @change="$emit('updatePermission', permission, index)"
                        class="hover:cursor-pointer" type="checkbox"></input>
                </td>
            </tr>
        </tbody>
    </table>
</template>