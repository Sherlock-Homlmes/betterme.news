<template>
<center>
    <div v-if="pageInfo">
        <h1>{{ pageInfo?.html.title }}</h1>
        <img :src="`http://localhost:8008/scrap/data/ivolunteer_vn/media/${pageInfo?.html.banner}`" >
    </div>
    <v-progress-circular v-else indeterminate color="green" ></v-progress-circular>
</center>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import  fetchLink from '~/src/config'

const pageInfo = ref(null)
const getPageInfo = async (link: string) => {
    const result = await fetch(
        `${fetchLink}/crawlers/${link}`
    )
    pageInfo.value = await result.json()
    console.log(pageInfo.value)
}
onMounted(async()=>{
    await getPageInfo('du-an-cham-net-mo-don-tuyen-thanh-vien-the-he-1-s23330.html?origin=ivolunteer_vn')
})

</script>

<style style lang="sass">
</style>
