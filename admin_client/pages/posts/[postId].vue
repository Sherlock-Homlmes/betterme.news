<template>
<center class="mt-5 mb-15">
    <div v-if="postInfo" class="w-75">
        <v-text-field label="Title" v-model="postInfo.title"></v-text-field>
        <img :src="postInfo?.banner_img" >
        <v-file-input clearable label="To do..." variant="solo-filled" class="w-50" :disabled='true'></v-file-input>
        <v-autocomplete
            v-model="postInfo.tags"
            class="w-50"
            clearable
            chips
            label="Tags"
            :items="tags"
            multiple
            variant="solo-filled"
        ></v-autocomplete>
        <v-combobox
            v-model="postInfo.keywords"
            clearable
            chips
            multiple
            label="Keyword"
        ></v-combobox>
        <v-textarea label="Description" variant="solo-filled" v-model="postInfo.description"></v-textarea>
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
                v-model="postInfo.content"
                initial-value="Loading..."
                output-format="html"
            />
        </v-card>
        <center class="my-5">
            <v-btn prepend-icon="$vuetify" :loading="updating" @click="onSavePost">SAVE</v-btn>
        </center>
    </div>
    <v-progress-circular v-else indeterminate color="green" ></v-progress-circular>
    <v-snackbar
        v-model="snackbar"
        vertical
    >
    <div class="text-subtitle-1 pb-2">Post saved</div>
    <template v-slot:actions>
        <v-btn
        color="indigo"
        variant="text"
        :href='`${clientLink}/posts/${postInfo?.id}`'
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
import { useRuntimeConfig } from 'nuxt/app';
import { changeTracker } from '~/src/func'
import Editor from '@tinymce/tinymce-vue';
import type {GetPostResponse} from '~/src/types/responses'
import {IvolunteerPageTagsEnum} from '~/src/types/enums'

const config = useRuntimeConfig()
const { fetchLink, clientLink } = config.public

const vm = getCurrentInstance().proxy
// TODO: snackbar component
const snackbar = ref<Boolean>(false)
const postInfo = ref<GetPostResponse>()
const tags = ref<IvolunteerPageTagsEnum[]>()
const updating = ref<Boolean>(false)
// TODO: add conditions

const getPostInfo = async () => {
    const tagsResult = await fetch(
        `${fetchLink}/tags?origin=ivolunteer_vn`
    )
    tags.value = await tagsResult.json()

    const postResult = await fetch(
        `${fetchLink}/posts/${vm.$route.params.postId}`
    )
    postInfo.value = await postResult.json() as GetPostResponse
    changeTracker.track(postInfo.value)
}

const onSavePost = async () => {
    if(!postInfo.value) return
    updating.value = true
    await fetch( `${fetchLink}/admin/posts/${vm.$route.params.postId}`, {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(changeTracker.getChange(postInfo.value))
    })
    updating.value = false
}

onMounted(async()=>{
    await getPostInfo()
})

</script>

<style style lang="sass">
</style>
