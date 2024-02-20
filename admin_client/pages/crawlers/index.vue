<template>
  <NuxtLayout name="default">
    <center class="mt-5 mb-15">
      <h1>Crawlers</h1>
      <v-select
        v-model="crawlContentType"
        class="w-50"
        label="Content type"
        :items="contentTypes"
        variant="outlined"
      ></v-select>
      <div class="d-flex justify-center align-center w-25">
        <v-text-field
          label="Post url"
          v-model="newPostUrl"
          variant="outlined"
          hide-details
        ></v-text-field>
        <v-btn class="ml-2" @click="onClickCreateNewPost">Crawl</v-btn>
      </div>
      <v-data-table
        items-per-page="100"
        :headers="draftPostHeaders"
        :items="draftPosts"
        :loading="loadingDraftPosts"
      >
        <template v-slot:top>
          <h1>Draft posts</h1>
        </template>
        <template v-slot:item.name="{ item }">
          {{ item.title }}
        </template>
        <template v-slot:item.actions="{ item }">
          <a :href="`/crawlers/${item.source}/${item.slug}`" target="_blank">
            <v-icon size="small" class="me-2"> mdi-pencil </v-icon>
          </a>
          <v-icon size="small" @click="deleteDraftPost(item)">
            mdi-delete
          </v-icon>

          <!-- Not work -->
        </template>
      </v-data-table>
      <v-data-table
        items-per-page="100"
        :headers="postHeaders"
        :items="posts"
        :loading="loadingPosts"
      >
        <template v-slot:top>
          <h1>Crawlers</h1>
        </template>
        <template v-slot:item.url="{ item }">
          <a
            :href="`/crawlers/ivolunteer_vn/${item}?content_type=${crawlContentType}`"
            target="_blank"
          >
            {{ item }}
          </a>
        </template>
      </v-data-table>

      <!-- <v-dialog v-model="deleteDialog" max-width="500px">
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
    </v-dialog> -->
    </center>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { useRuntimeConfig } from "nuxt/app";
import { ref, onMounted, watch } from "vue";
import type {} from "~/src/types/enum";
import fetchWithAuth from "~/src/common/betterFetch";
import { IvolunteerPageContentTypeEnum } from "~/src/types/enums";
const config = useRuntimeConfig();
const { fetchLink, clientLink } = config.public;
// const vm = getCurrentInstance().proxy

const postHeaders = ref([{ title: "URL", key: "url", sortable: false }]);
const draftPostHeaders = ref([
  { title: "Name", key: "name", sortable: false },
  { title: "Actions", key: "actions", sortable: false },
]);
const posts = ref<string[]>([]);
const draftPosts = ref([]);
const newPostUrl = ref<string>("");
const loadingDraftPosts = ref(false);
const loadingPosts = ref(false);
const contentTypes = [...new Set(Object.values(IvolunteerPageContentTypeEnum))];
const crawlContentType = ref<IvolunteerPageContentTypeEnum>(contentTypes[0]);

const getDraftPosts = async () => {
  loadingDraftPosts.value = true;
  const draftPostsResult = await fetchWithAuth(
    `${fetchLink}/admin/draft_posts`,
  );
  draftPosts.value = (await draftPostsResult.json()).map((draftPost) => {
    return {
      id: draftPost.id,
      title: draftPost.draft_data.title,
      slug: draftPost.name,
      source: draftPost.source,
    };
  });
  loadingDraftPosts.value = false;
};

const getPostList = async () => {
  loadingPosts.value = true;
  const postsResult = await fetchWithAuth(
    `${fetchLink}/admin/crawlers?origin=ivolunteer_vn&content_type=${crawlContentType.value}`,
  );
  posts.value = (await postsResult.json()) as string[];
  loadingPosts.value = false;
};

const onClickCreateNewPost = () => {
  if (newPostUrl.value === "") return;
  window.open(`/crawlers/ivolunteer_vn/${newPostUrl.value}`, "_blank");
  newPostUrl.value = "";
};

const deleteDraftPost = async (deleteDraftPost) => {
  try {
    await fetchWithAuth(
      `${fetchLink}/admin/draft_posts/${deleteDraftPost.id}`,
      { method: "DELETE" },
    );
    draftPosts.value = draftPosts.value.filter(
      (draftPost) => draftPost.id !== deleteDraftPost.id,
    );
    window.alert("Delete success");
  } catch (err) {
    window.alert("Delete fail");
  }
};

watch(
  crawlContentType,
  async () => {
    await getPostList();
  },
  { deep: true },
);

onMounted(async () => {
  await getDraftPosts();
  await getPostList();
});
</script>