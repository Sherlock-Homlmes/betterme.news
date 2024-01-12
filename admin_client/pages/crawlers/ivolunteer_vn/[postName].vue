
<template>
<center class="mt-5 mb-15">
    <div v-if="pageInfo" class="w-75">
        <v-text-field label="Title" v-model="pageInfo.title"></v-text-field>
        <img :src="`http://localhost/api/media/${pageInfo?.banner}`" >
        <v-file-input clearable label="To do..." variant="solo-filled" class="w-50" :disabled='true'></v-file-input>
        <v-autocomplete
        v-model="pageInfo.tags"
        class="w-50"
        clearable
        chips
        label="Tags"
        :items="tags"
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
                <center class="my-5" :color='"green"'>
                    <v-btn prepend-icon="$vuetify" @click="onSaveDraft" :disabled="true">
                        <template v-slot:prepend v-if="isHtmlPreviewed">
                            <v-icon color="success"></v-icon>
                        </template>
                        Save draft(Coming soon...)
                    </v-btn>
                </center>
        </template>

        <template v-slot:item.2>
            <v-card title="Xem trước nội dung đăng lên web" flat></v-card>
                <center class="my-5" :color='"green"'>
                    <v-btn prepend-icon="$vuetify" @click="onHtmlPreview" :disabled="true">
                        <template v-slot:prepend v-if="isHtmlPreviewed">
                            <v-icon color="success"></v-icon>
                        </template>
                        TO DO...
                    </v-btn>
                </center>
            <v-card title="Xem trước nội dung đăng lên facebook" flat></v-card>
                <center class="my-5" :color='"green"'>
                    <v-btn prepend-icon="$vuetify" @click="onFacebookPreview" :disabled="true">
                        <template v-slot:prepend v-if="isFacebookPreviewed">
                            <v-icon color="success"></v-icon>
                        </template>
                        TO DO...
                    </v-btn>
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
// TODO:
// web preview
// to store
// facebook preview
// vue use
import { ref, onMounted, watch, computed, getCurrentInstance } from 'vue';
import fetchLink from '~/src/config'
import { changeTracker } from '~/src/func'
import Editor from '@tinymce/tinymce-vue';
import type {GetCrawlersIvolunteerDataResponse, PostCrawlersPreviewDiscordDataPayload} from '~/src/types/responses'
import {CrawlerDataResponseTypeEnum, OriginCrawlPagesEnum, IvolunteerPageTagsEnum} from '~/src/types/enums'

const vm = getCurrentInstance().proxy
const link = ref<String>(vm.$route.params.postName)
const pageInfo = ref<GetCrawlersIvolunteerDataResponse>()
const tags = ref<IvolunteerPageTagsEnum[]>()
const isFacebookPreviewed = ref<Boolean>(false)
const isHtmlPreviewed = ref<Boolean>(false)
const isDiscordPreviewed = ref<Boolean>(false)
// TODO: add conditions
const canSave = computed<Boolean>(()=>isDiscordPreviewed.value)

const getPageInfo = async () => {
    const tagsResult = await fetch(
        `${fetchLink}/admin/tags?origin=ivolunteer_vn`
    )
    tags.value = await tagsResult.json()

    const postResult = await fetch(
        `${fetchLink}/admin/crawlers/${link.value}?origin=ivolunteer_vn`
    )
    pageInfo.value = await postResult.json()
    changeTracker.track(pageInfo.value)
}

const onSaveDraft = async () => {
    await fetch( `${fetchLink}/admin/crawlers/${link.value}`, {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(changeTracker.getChange(pageInfo.value))
    })
}
const onDiscordPreview = async () => {
    await onSaveDraft()
    const body: PostCrawlersPreviewDiscordDataPayload = {
        origin: OriginCrawlPagesEnum.IVOLUNTEER_VN,
        preview_source: [CrawlerDataResponseTypeEnum.DISCORD]
    }
    await fetch(`${fetchLink}/admin/crawlers/${link.value}/preview`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body)
    })
    isDiscordPreviewed.value = true
}
const onHtmlPreview = ()=>{
    isHtmlPreviewed.value = true
}
const onFacebookPreview = ()=>{
    isFacebookPreviewed.value = true
}

watch(()=>pageInfo,
()=>{
    isDiscordPreviewed.value = false
    isHtmlPreviewed.value = false
    isFacebookPreviewed.value = false
},{deep:true})

onMounted(async()=>{
    await getPageInfo()
})

</script>

<style style lang="sass">
</style>
