<template>
<center class="mb-15">
    <div v-if="pageInfo">
        <h1>{{ pageInfo?.html.title }}</h1>
        <img :src="`http://localhost/api/media/${pageInfo?.html.banner}`" >
        <v-file-input clearable label="File input" variant="solo-filled" class="w-50" ></v-file-input>
        <v-autocomplete
        class="w-50"
        clearable
        chips
        label="Tags"
        :items="['CLB', 'Tinh nguyen', 'somethign 1', 'something 2', 'something 3']"
        multiple
        variant="solo-filled"
        ></v-autocomplete>
        <v-textarea class="w-75" label="Description" variant="solo-filled" v-model="description"></v-textarea>
        <v-card class="w-75" >
            <v-tabs
            v-model="tab"
            color="blue"
            align-tabs="center"
            >
                <v-tab :value="1">Web</v-tab>
                <v-tab :value="2">Discord</v-tab>
            </v-tabs>
            <v-window v-model="tab">

                <!-- html -->
                <v-window-item
                    :key="1"
                    :value="1"
                >
                    <v-container fluid>
                        <editor
                        v-model="pageInfo.html.content"
                        initial-value="Loading..."
                        output-format="html"
                        />
                        <h2></h2>
                    </v-container>
                </v-window-item>

                <!-- discord -->
                <v-window-item
                    :key="2"
                    :value="2"
                >
                    <v-container fluid>
                        {{ pageInfo.discord.content }}
                        <center>
                            <v-btn prepend-icon="$vuetify">Preview</v-btn>
                        </center>
                    </v-container>
                </v-window-item>

            </v-window>
        </v-card>
    </div>


    <v-progress-circular v-else indeterminate color="green" ></v-progress-circular>
</center>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import fetchLink from '~/src/config'
import Editor from '@tinymce/tinymce-vue';
import type {GetCrawlersDataResponse} from '~/src/types/responses'

const pageInfo = ref<GetCrawlersDataResponse>()
const tab = ref<Number>()
const description = ref<String>('')
const isPreviewed = ref<Boolean>(false)

const getPageInfo = async (link: string) => {
    const result = await fetch(
        `${fetchLink}/admin/crawlers/${link}`
    )
    pageInfo.value = await result.json()
    console.log(pageInfo.value)
}
onMounted(async()=>{
    await getPageInfo('du-an-ve-lich-su-ngan-nam-dat-viet-mo-don-tuyen-thanh-vien-the-he-4-0-s23376.html?origin=ivolunteer_vn')
})

</script>

<style style lang="sass">
</style>
