<template>
  <center class="mt-5 mb-15">
    <div v-if="pageInfo" class="w-75">
      <div class="d-flex justify-center align-center mb-4">
        <v-text-field
          label="Title"
          v-model="pageInfo.title"
          ref="title"
          :rules="[
            (val) => val.length >= 1 || `Hãy điền title`,
            (val) =>
              val.length <= 100 ||
              `Chỉnh title ít hơn 100 chữ. Hiện tại: ${val.length} chữ`,
          ]"
          hide-details
        ></v-text-field>
        <v-btn
          class="ml-4 bg-teal-lighten-1"
          @click="onAIPromptGenerate(pageInfo.title, AIPromtTypeEnum.TITLE)"
          :loading="aiPrompt.loading"
          >AI</v-btn
        >
      </div>
      <v-card
        v-if="aiPrompt.title"
        variant="elevated"
        class="w-75 bg-teal-lighten-1"
        color="surface-variant"
        title="Title được đề xuất bởi AI"
        >{{ aiPrompt.title }}</v-card
      >
      <br />
      <img :src="`${fetchLink}/media/${pageInfo?.banner}`" />
      <v-file-input
        clearable
        label="To do..."
        variant="solo-filled"
        class="w-50"
        :disabled="true"
      ></v-file-input>
      <v-chip variant="flat" color="primary" size="x-large" class="mb-5">
        Deadline: {{ pageInfo.deadline || "ASAP" }}
      </v-chip>
      <v-autocomplete
        v-model="pageInfo.tags"
        class="w-50"
        clearable
        chips
        label="Tags"
        :items="tags"
        multiple
        variant="solo-filled"
        :rules="[(val) => !!(val && val.length) || `Hãy chọn tags`]"
      ></v-autocomplete>
      <v-combobox
        v-model="pageInfo.keywords"
        clearable
        chips
        multiple
        label="Keyword"
      ></v-combobox>
      <div class="d-flex justify-center align-center mb-4">
        <v-textarea
          label="Description"
          variant="solo-filled"
          v-model="pageInfo.description"
        ></v-textarea>
        <v-btn
          class="ml-4 bg-teal-lighten-1"
          @click="
            onAIPromptGenerate(
              pageInfo.description,
              AIPromtTypeEnum.DESCRIPTION,
            )
          "
          :loading="aiPrompt.loading"
          >AI</v-btn
        >
      </div>
      <v-card
        v-if="aiPrompt.description"
        variant="elevated"
        class="w-75 bg-teal-lighten-1"
        color="surface-variant"
        title="Description được đề xuất bởi AI"
        >{{ aiPrompt.description }}</v-card
      >
      <br />
      <v-card>
        <editor
          api-key="xidtifz02mui7lrdh7iq49zlrykxh4o1lqbdcrxy9zsfpnwi"
          :init="{
            height: 1000,
            menubar: false,
            plugins: [
              'advlist autolink lists link image charmap print preview anchor',
              'searchreplace visualblocks code fullscreen',
              'insertdatetime media table paste code help wordcount',
            ],
            toolbar:
              'undo redo | formatselect | bold italic backcolor | \
                                alignleft aligncenter alignright alignjustify | \
                                bullist numlist outdent indent | removeformat | help',
          }"
          v-model="pageInfo.content"
          initial-value="Loading..."
          output-format="html"
        />
      </v-card>
      <v-stepper :items="['Step 1', 'Step 2', 'Step 3']" class="mt-10">
        <template v-slot:item.1>
          <v-card title="Chỉnh sửa nội dung" flat></v-card>
          <center class="my-5" :color="'green'">
            <v-btn
              prepend-icon="$vuetify"
              @click="onSaveDraft(true)"
              :disabled="!canSave"
            >
              <template v-slot:prepend v-if="isHtmlPreviewed">
                <v-icon color="success"></v-icon>
              </template>
              Save draft
            </v-btn>
          </center>
        </template>

        <template v-slot:item.2>
          <v-card title="Xem trước nội dung đăng lên web" flat></v-card>
          <center class="my-5" :color="'green'">
            <v-btn
              prepend-icon="$vuetify"
              @click="onHtmlPreview"
              :disabled="true"
            >
              <template v-slot:prepend v-if="isHtmlPreviewed">
                <v-icon color="success"></v-icon>
              </template>
              TO DO...
            </v-btn>
          </center>
          <v-card title="Xem trước nội dung đăng lên facebook" flat></v-card>
          <center class="my-5" :color="'green'">
            <v-btn
              prepend-icon="$vuetify"
              @click="onFacebookPreview"
              :disabled="true"
            >
              <template v-slot:prepend v-if="isFacebookPreviewed">
                <v-icon color="success"></v-icon>
              </template>
              TO DO...
            </v-btn>
          </center>
          <v-card title="Xem trước bài đăng lên discord" flat></v-card>
          <center class="my-5">
            <v-btn
              prepend-icon="$vuetify"
              :loading="updating"
              @click="onDiscordPreview"
              :disabled="!canSave"
            >
              <template v-slot:prepend v-if="isDiscordPreviewed">
                <v-icon color="success"></v-icon>
              </template>
              Send</v-btn
            >
          </center>
        </template>

        <template v-slot:item.3>
          <v-card title="Tạo bài viết mới" flat></v-card>
          <center class="my-5">
            <v-btn
              prepend-icon="$vuetify"
              :disabled="!canCreatePost"
              :loading="updating"
              @click="onCreatePost"
              >CREATE</v-btn
            >
          </center>
        </template>
      </v-stepper>
    </div>
    <v-progress-circular
      v-else
      indeterminate
      color="green"
    ></v-progress-circular>
    <v-snackbar v-model="snackbar" vertical :timeout="-1">
      <div class="text-subtitle-1 pb-2">View created post</div>
      <template v-slot:actions>
        <v-btn
          color="green"
          variant="text"
          :href="`${clientLink}/posts/${pageInfo?.id}`"
          target="_blank"
        >
          View
        </v-btn>
        <v-btn
          color="green"
          variant="text"
          :href="`/posts/${pageInfo?.id}`"
          target="_blank"
        >
          Edit
        </v-btn>
        <v-btn color="green" variant="text" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </center>
</template>

<script setup lang="ts">
// TODO:
// web preview
// to store - component
// facebook preview
// vue use
import { ref, onMounted, watch, computed, getCurrentInstance } from "vue";
import { useRuntimeConfig } from "nuxt/app";
import { changeTracker } from "@utils/func";
import { fetchWithAuth } from "@utils/betterFetch";
import Editor from "@tinymce/tinymce-vue";
import type {
  GetCrawlersIvolunteerDataResponse,
  PostCrawlersPreviewDiscordDataPayload,
  PostCrawlersDataPayload,
  PostCrawlersResponse,
  PostAIPromtPayload,
} from "@types/responses";
import {
  CrawlerDataResponseTypeEnum,
  OriginCrawlPagesEnum,
  IvolunteerPageTagsEnum,
  IvolunteerPageContentTypeEnum,
  AIPromtTypeEnum,
} from "@types/enums";

const contentTypeMap = {
  // [IvolunteerPageContentTypeEnum.CLUB]: IvolunteerPageTagsEnum.CLUB,
  [IvolunteerPageContentTypeEnum.VOLUNTEER]: IvolunteerPageTagsEnum.VOLUNTEER,
  [IvolunteerPageContentTypeEnum.SCHORLARSHIP]:
    IvolunteerPageTagsEnum.SCHORLARSHIP,
  [IvolunteerPageContentTypeEnum.COURSE]: IvolunteerPageTagsEnum.COURSE,
  [IvolunteerPageContentTypeEnum.EVENT]: IvolunteerPageTagsEnum.EVENT,
};
const config = useRuntimeConfig();
const { fetchLink, clientLink } = config.public;

const vm = getCurrentInstance().proxy as any;
// TODO: snackbar component
const snackbar = ref<Boolean>(false);
const link = ref<String>(vm.$route.params.postName);
const pageInfo = ref<GetCrawlersIvolunteerDataResponse>();
const tags = ref<IvolunteerPageTagsEnum[]>(
  Object.values(IvolunteerPageTagsEnum),
);
const updating = ref<Boolean>(false);
const aiPrompt = ref({
  title: null,
  description: null,
  loading: false,
});
const isFacebookPreviewed = ref<Boolean>(false);
const isHtmlPreviewed = ref<Boolean>(false);
const isDiscordPreviewed = ref<Boolean>(false);
const created = ref<Boolean>(false);
// TODO: add conditions
const canSave = computed<Boolean>(
  () =>
    !created.value &&
    !updating.value &&
    pageInfo.value &&
    !pageInfo.value.id &&
    pageInfo.value.title.length &&
    pageInfo.value.description.length &&
    pageInfo.value.content.length &&
    pageInfo.value.tags.length,
);
const canCreatePost = computed<Boolean>(
  () => canSave.value && isDiscordPreviewed.value,
);

const getPageInfo = async () => {
  try {
    const postResult = await fetchWithAuth(
      `${fetchLink}/admin/crawlers/${link.value}?origin=ivolunteer_vn`,
    );
    pageInfo.value =
      (await postResult.json()) as GetCrawlersIvolunteerDataResponse;
    if (pageInfo.value.id) vm.$router.push(`/posts/${pageInfo.value.id}`);
    changeTracker.track(pageInfo.value);
    pageInfo.value.tags = [
      contentTypeMap[
        vm.$route.query.content_type as IvolunteerPageContentTypeEnum
      ],
    ];
  } catch {
    window.alert("Crawler fail");
  } finally {
    // pass
  }
  eview;
};

const onSaveDraft = async (showAlert: boolean = false) => {
  // TODO: fix to not do anything else when update fail
  if (
    (await vm?.$refs.title.validate().length) ||
    pageInfo.value?.title?.length > 100
  ) {
    window.alert("Invalid title");
    return;
  }
  // else if(await vm?.$refs.tags.validate().length){
  //     window.alert('Invalid tags')
  //     return
  // }
  updating.value = true;
  const updateFields = changeTracker.getChange(pageInfo.value);
  // TODO: check object empty using lodash
  if (
    Object.keys(updateFields).length === 0 &&
    updateFields.constructor === Object
  )
    return;
  try {
    await fetchWithAuth(`${fetchLink}/admin/crawlers/${link.value}`, {
      method: "PATCH",
      body: JSON.stringify(updateFields),
    });
    if (showAlert) window.alert("Update success");
  } catch {
    window.alert("UPDATE FAIL");
  } finally {
    updating.value = false;
  }
};

const onCreatePost = async () => {
  if (!pageInfo.value) return;

  created.value = true;
  await onSaveDraft();
  updating.value = true;
  const body: PostCrawlersDataPayload = {
    origin: OriginCrawlPagesEnum.IVOLUNTEER_VN,
    post_name: link.value.toString(),
  };
  try {
    const result = await fetchWithAuth(`${fetchLink}/admin/crawlers`, {
      method: "POST",
      body: JSON.stringify(body),
    });
    const response_data = (await result.json()) as PostCrawlersResponse;
    pageInfo.value.id = response_data["id"];
    snackbar.value = true;
  } catch {
    created.value = false;
    window.alert("CREATE FAIL");
  } finally {
    updating.value = false;
  }
};

const onAIPromptGenerate = async (
  context: string,
  promtType: AIPromtTypeEnum,
) => {
  const body: PostAIPromtPayload = {
    context,
    prompt_type: promtType,
  };
  try {
    aiPrompt.value.loading = true;
    const response = await fetchWithAuth(`${fetchLink}/admin/ai/post_prompts`, {
      method: "POST",
      body: JSON.stringify(body),
    });
    aiPrompt.value[promtType] = (await response.json()).data;
  } catch {
  } finally {
    aiPrompt.value.loading = false;
  }
};

const onDiscordPreview = async () => {
  await onSaveDraft();
  updating.value = true;
  const body: PostCrawlersPreviewDiscordDataPayload = {
    origin: OriginCrawlPagesEnum.IVOLUNTEER_VN,
    preview_source: [CrawlerDataResponseTypeEnum.DISCORD],
  };
  await fetchWithAuth(`${fetchLink}/admin/crawlers/${link.value}/_preview`, {
    method: "POST",
    body: JSON.stringify(body),
  });
  isDiscordPreviewed.value = true;
  updating.value = false;
};
const onHtmlPreview = () => {
  updating.value = true;
  //
  isHtmlPreviewed.value = true;
  updating.value = false;
};
const onFacebookPreview = () => {
  updating.value = true;
  //
  isFacebookPreviewed.value = true;
  updating.value = false;
};

watch(
  () => [
    pageInfo.value?.description,
    pageInfo.value?.keywords,
    pageInfo.value?.tags,
  ],
  () => {
    isDiscordPreviewed.value = false;
    isHtmlPreviewed.value = false;
    isFacebookPreviewed.value = false;
  },
  { deep: true },
);

onMounted(async () => {
  await getPageInfo();
});
</script>

<style style lang="sass"></style>
