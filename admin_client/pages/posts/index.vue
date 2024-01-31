
<template>
  <NuxtLayout name="default">
    <center class="mt-5 mb-15">
        <h1>Manage posts</h1>
  <v-data-table
    :headers="headers"
    :items="posts"
    :sort-by="[{ key: 'calories', order: 'asc' }]"
  >
    <template v-slot:top>
      <v-toolbar flat >
        <v-spacer></v-spacer>
        <v-text-field class="w-25" label="Post url" v-model="newPostUrl"></v-text-field>
        <v-btn @click="onClickCreateNewPost">Create new post</v-btn>
      </v-toolbar>
    </template>
    <template v-slot:item.title="{ item }">
        <a :href="`${clientLink}/posts/${item.id}`">{{ item.title }}</a>
    </template>
    <template v-slot:item.banner_img="{ item }">
        <v-img :src="item.banner_img" :alt="item.name" height="150px"></v-img>
    </template>
    <template v-slot:item.actions="{ item }">
        <a
            :href="`/posts/${item.id}`"
            target="_blank"
        >
            <v-icon
                size="small"
                class="me-2"
            >
                mdi-pencil
            </v-icon>
        </a>
        <v-icon
            size="small"
            @click="onClickDeletePost(item)"
        >
            mdi-delete
        </v-icon>

        <!-- Not work -->
    </template>
  </v-data-table>

    <v-dialog v-model="deleteDialog" max-width="500px">
        <v-card>
        <v-card-title class="text-h5">Are you sure you want to delete this post?</v-card-title>
        <v-card-text class="text-h5">Please type: "{{ deletePost.title }}" to confirm</v-card-text>
        <v-card-actions>
            <v-text-field v-model="confirmDeletePostValue" label="postName"></v-text-field>
            <v-spacer></v-spacer>
            <v-btn color="blue-darken-1" variant="text" @click="deleteDialog = false">Cancel</v-btn>
            <v-btn color="blue-darken-1" variant="text" @click="onDeletePostConfirm(deletePost)" :disabled="confirmDeletePostValue != deletePost.title">OK</v-btn>
        </v-card-actions>
        </v-card>
    </v-dialog>

    </center>
    </NuxtLayout>
</template>

<script setup lang="ts">
    // TODO:
    // pagination
    // search
    // filter
    // filter
    import { useRuntimeConfig } from 'nuxt/app';
    import {ref, getCurrentInstance, onMounted } from 'vue';
    import type {GetPostListResponse} from '~/src/types/responses'
    import fetchWithAuth from '~/src/common/betterFetch'
    const config = useRuntimeConfig()
    const { fetchLink, clientLink } = config.public
    // const vm = getCurrentInstance().proxy


    const headers = ref([
        { title: 'Title', align: 'start', key: 'title'},
        { title: 'Banner image', key: 'banner_img', sortable: false},
        { title: 'Description', key: 'description', sortable: false },
        { title: 'View', key: 'view' },
        { title: 'Actions', key: 'actions', sortable: false },
    ])
    const posts = ref<Array<GetPostListResponse>>([])
    const newPostUrl = ref<string>('')

    const deleteDialog = ref<boolean>(false)
    const confirmDeletePostValue = ref<string>('')
    const deletePost = ref<GetPostListResponse>()

    const getPostList = async () => {
        const postsResult = await fetch(
            `${fetchLink}/posts?per_page=10000`

        )
        posts.value = await postsResult.json() as Array<GetPostListResponse>
    }

    const onClickDeletePost = (post: GetPostListResponse) => {
        deletePost.value = post
        deleteDialog.value = true
    }
    const onDeletePostConfirm = async (deletePost: GetPostListResponse) => {
        try{
            await fetchWithAuth(
                `${fetchLink}/admin/posts/${deletePost.id}`,{method: 'DELETE'}
            )
            posts.value = posts.value.filter(post => post.id !== deletePost.id)
        }
        catch(err){
            console.error(err)
        }
        finally{
            deleteDialog.value = false
        }
    }

    const onClickCreateNewPost = () => {
        if(newPostUrl.value === '') return
        window.open(`/crawlers/ivolunteer_vn/${newPostUrl.value}`, '_blank');
        newPostUrl.value = ''
    }

    onMounted(async () => {
        await getPostList()
    })
</script>
