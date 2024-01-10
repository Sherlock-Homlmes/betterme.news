<template>
<center class="mt-5 mb-15">
    <div v-if="pageInfo" class="w-75">
        <v-text-field label="Title" v-model="pageInfo.title"></v-text-field>
        <img :src="`http://localhost/api/media/${pageInfo?.banner}`" >
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
        <v-textarea label="Description" variant="solo-filled" v-model="pageInfo.description"></v-textarea>
        <v-card>
                        <editor
                            :init="{
                                height: 1000,
                                menubar: false,
                                plugins: [
                                'advlist autolink lists link image charmap print preview anchor',
                                'searchreplace visualblocks code fullscreen',
                                'insertdatetime media table paste code help wordcount'
                                ],
                                toolbar:
                                'undo redo | formatselect | bold italic backcolor | \
                                alignleft aligncenter alignright alignjustify | \
                                bullist numlist outdent indent | removeformat | help'
                            }"
                            v-model="pageInfo.content"
                            initial-value="Loading..."
                            output-format="html"
                        />
        </v-card>
        <v-stepper :items="['Step 1', 'Step 2', 'Step 3']" class="mt-10">
        <template v-slot:item.1>
            <v-card title="Chỉnh sửa nội dung" flat></v-card>
        </template>

        <template v-slot:item.2>
            <v-card title="Xem trước nội dung đăng lên web" flat></v-card>
                                <center class="my-5" :color='"green"'>
                                    <v-btn prepend-icon="$vuetify" @click="onHtmlPreview">
                                            <template v-slot:prepend v-if="isHtmlPreviewed">
                <v-icon color="success"></v-icon>
            </template>
                                        Preview</v-btn>
                                </center>
            <v-card title="Xem trước bài đăng lên discord" flat></v-card>
                                <center class="my-5">
                                    <v-btn prepend-icon="$vuetify"  @click="onDiscordPreview">
                                            <template v-slot:prepend v-if="isDiscordPreviewed">
                <v-icon color="success"></v-icon>
            </template>
                                        Send</v-btn>
                                </center>
        </template>

        <template v-slot:item.3>
            <v-card title="Tạo bài viết mới" flat></v-card>
                                <center class="my-5">
                                    <v-btn prepend-icon="$vuetify" :disabled="!canSave">Create</v-btn>
                                </center>
        </template>
        </v-stepper>
    </div>
    <v-progress-circular v-else indeterminate color="green" ></v-progress-circular>
</center>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import fetchLink from '~/src/config'
import Editor from '@tinymce/tinymce-vue';
import type {GetCrawlersIvolunteerDataResponse} from '~/src/types/responses'

const pageInfo = ref<GetCrawlersIvolunteerDataResponse>(null)
const tab = ref<Number>()
const isHtmlPreviewed = ref<Boolean>(false)
const isDiscordPreviewed = ref<Boolean>(false)
const canSave = computed<Boolean>(()=>isDiscordPreviewed.value && isHtmlPreviewed.value)

const getPageInfo = async (link: string) => {
    const result = await fetch(
        `${fetchLink}/admin/crawlers/${link}`
    )
    pageInfo.value = await result.json()
}

const onDiscordPreview = ()=>{
    isDiscordPreviewed.value = true
    console.log(pageInfo.value)
}
const onHtmlPreview = ()=>{
    isHtmlPreviewed.value = true
}

watch(()=>pageInfo,
()=>{
    isDiscordPreviewed.value = false
    isHtmlPreviewed.value = false
},{deep:true})

onMounted(async()=>{
    await getPageInfo('du-an-ve-lich-su-ngan-nam-dat-viet-mo-don-tuyen-thanh-vien-the-he-4-0-s23376.html?origin=ivolunteer_vn')
})

</script>

<style style lang="sass">
</style>
