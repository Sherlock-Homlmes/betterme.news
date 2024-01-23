
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
                    <v-btn prepend-icon="$vuetify" :loading="updating" @click="onDiscordPreview">
                        <template v-slot:prepend v-if="isDiscordPreviewed">
                <v-icon color="success"></v-icon>
            </template>
                                        Send</v-btn>
                                </center>
        </template>

        <template v-slot:item.3>
            <v-card title="Tạo bài viết mới" flat></v-card>
                                <center class="my-5">
                                    <v-btn v-if="pageInfo?.id" prepend-icon="$vuetify" :disabled="!canSave" :loading="updating" @click="onCreatePost">Create</v-btn>
                                    <v-btn v-else prepend-icon="$vuetify" :disabled="!canSave" :loading="updating" @click="onCreatePost">SAVE(TODO...)</v-btn>
                                </center>
        </template>
        </v-stepper>
    </div>
    <v-progress-circular v-else indeterminate color="green" ></v-progress-circular>
    <v-snackbar
        v-model="snackbar"
        vertical
    >
    <div class="text-subtitle-1 pb-2">View created post</div>
    <template v-slot:actions>
        <v-btn
        color="indigo"
        variant="text"
        :href='"https://betterme.news/posts/somepost_"+pageInfo?.id'
        target="_blank"
        >
        View
        </v-btn>
        <v-btn
        color="indigo"
        variant="text"
        @click="snackbar = false"
        >
        Close
        </v-btn>
    </template>
    </v-snackbar>
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
import type {GetCrawlersIvolunteerDataResponse, PostCrawlersPreviewDiscordDataPayload, PostCrawlersDataPayload, PostCrawlersResponse} from '~/src/types/responses'
import {CrawlerDataResponseTypeEnum, OriginCrawlPagesEnum, IvolunteerPageTagsEnum} from '~/src/types/enums'

const vm = getCurrentInstance().proxy
// TODO: snackbar component
const snackbar = ref<Boolean>(false)
const link = ref<String>(vm.$route.params.postName)
const pageInfo = ref<GetCrawlersIvolunteerDataResponse>()
const tags = ref<IvolunteerPageTagsEnum[]>()
const updating = ref<Boolean>(false)
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
    pageInfo.value = await postResult.json() as GetCrawlersIvolunteerDataResponse
    changeTracker.track(pageInfo.value)
}

const onSaveDraft = async () => {
    updating.value = true
    await fetch( `${fetchLink}/admin/crawlers/${link.value}`, {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(changeTracker.getChange(pageInfo.value))
    })
    updating.value = false
}

const onCreatePost = async () => {
    if(!pageInfo.value) return

    updating.value = true
    const body: PostCrawlersDataPayload = {
        origin: OriginCrawlPagesEnum.IVOLUNTEER_VN,
        post_name: link.value.toString()
    }
    const result = await fetch(`${fetchLink}/admin/crawlers`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body)
    })
    const response_data = await result.json() as PostCrawlersResponse
    pageInfo.value.id = response_data["id"]
    updating.value = false
    snackbar.value = true
}

const onDiscordPreview = async () => {
    updating.value = true
    await onSaveDraft()
    const body: PostCrawlersPreviewDiscordDataPayload = {
        origin: OriginCrawlPagesEnum.IVOLUNTEER_VN,
        preview_source: [CrawlerDataResponseTypeEnum.DISCORD]
    }
    await fetch(`${fetchLink}/admin/crawlers/${link.value}/_preview`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body)
    })
    isDiscordPreviewed.value = true
    updating.value = false
}
const onHtmlPreview = ()=>{
    updating.value = true
    //
    isHtmlPreviewed.value = true
    updating.value = false
}
const onFacebookPreview = ()=>{
    updating.value = true
    //
    isFacebookPreviewed.value = true
    updating.value = false
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