<template>
    <NuxtPage/>
</template>

<script setup lang="ts">
    import {getCurrentInstance, onMounted } from 'vue';
    import { useRuntimeConfig } from 'nuxt/app';
    import fetchWithAuth from '~/src/common/betterFetch'

    const config = useRuntimeConfig()
    const { fetchLink } = config.public
    const vm = getCurrentInstance().proxy
    onMounted(async ()=>{
        if(vm.$route.name === 'auth-discord-oauth') return
        const response = await fetchWithAuth(`${fetchLink}/auth/self`)
        if(!response.ok) vm.$router.push('/')
    })
</script>
