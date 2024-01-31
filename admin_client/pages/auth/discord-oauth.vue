<template>
    <p>something</p>

</template>

<script setup lang="ts">
    import { getCurrentInstance, onMounted } from 'vue';
    import { useRuntimeConfig } from 'nuxt/app';
    import { useStorage } from '@vueuse/core'


    const config = useRuntimeConfig()
    const { fetchLink } = config.public

    const vm = getCurrentInstance().proxy
    onMounted(async ()=>{
        const code = vm.$route.query?.code
        if(code){
            const response = await fetch(`${fetchLink}/auth/discord-oauth?code=${code}`)
            const data = await response.json()
            if(data?.token){
                useStorage('Authorization', data?.token)
                vm.$router.push('/posts')
            }
            else{
                vm.$router.push('/')
            }
        }
        else{
            vm.$router.push('/')
        }
    })
</script>
