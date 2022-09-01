<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Social content"/>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="post" label="Posts"/>
        <q-tab name="content" label="Content"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated :keep-alive="true">
        <q-tab-panel name="post">
          <div class="row q-gutter-y-sm">
            <div class="col-12 q-gutter-x-sm q-gutter-y-md q-mb-sm">
              <q-btn-dropdown icon="add" label="Create post" color="primary">
                <q-list>
                  <q-item
                    v-for="platform in availableSocialPlatforms"
                    clickable v-close-popup @click="openEditContentDialog(null, false, platform)"
                  >
                    <q-item-section avatar>
                      <img :src="platform.logo" alt="Logo" style="max-height: 20px">
                    </q-item-section>
                    <q-item-section>
                      {{ platform.name }}
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-btn-dropdown>
              <CollapsableCard v-for="post in socialPosts">
                <template v-slot:header-left>
                  <img :src="post.platform.logo" alt="Social platform logo" style="max-height: 32px">
                  <div class="text-h6 text-h6--mobile q-ml-md">
                    Post created at {{ dateTimeUtil.getDateTime(post.created_dt) }}
                  </div>
                </template>
                <template v-slot:header>
                  <q-btn flat dense icon="share" text-color="grey-6" @click="openSharePostDialog(post)"/>
                  <q-btn flat dense icon="delete" text-color="negative" @click="deletePost(post)"/>
                </template>
                <template v-slot:body>
                  <div class="w-100">
                    <div class="q-mb-xs border-bottom-1-gray-100">
                      <div class="q-pa-sm">
                        <div style="display: inline-block;">
                          <span class="copy-target" style="display: none">{{ post.formatted_content }}</span>
                          <q-btn
                            dense ripple unelevated icon="content_copy"
                            size="sm"
                            @click="dataUtil.copyText"
                          >
                            Copy post text
                          </q-btn>
                        </div>
                        <div class="q-ml-sm" style="display: inline-block;">
                          <span class="copy-target" style="display: none">{{ post.content }}</span>
                          <q-btn
                            dense ripple unelevated icon="content_copy"
                            size="sm"
                            @click="dataUtil.copyText"
                          >
                            Copy post template
                          </q-btn>
                        </div>
                        <q-btn
                          v-for="file in post.files"
                          dense ripple unelevated icon="file_download"
                          size="sm" type="a"
                          :href="file.url" target="_blank" download
                          class="q-ml-sm"
                        >
                          Download {{ fileUtil.getFileNameFromUrl(file.url) }}
                        </q-btn>
                      </div>
                    </div>
                    <div class="q-pa-md" style="white-space: pre-line;">
                      <div class="row">
                        <div class="col-12 col-md-8 q-pr-md-sm">
                          {{ post.formatted_content }}
                          <div v-for="file in post.files" class="q-mt-lg">
                            <img
                              v-if="fileUtil.isImage(file.url)"
                              :src="file.url" :alt="file.title"
                              style="max-height: 150px"
                            >
                            <video
                              v-if="fileUtil.isVideo(file.url)"
                              style="max-height: 150px"
                            >
                              <source :src="file.url">
                            </video>
                          </div>
                        </div>
                        <div class="col-12 col-md-4 q-pl-md-sm border-left-1-gray-100">
                          <div class="text-bold">
                            Post history
                            <CustomTooltip :is_include_space="false" icon_size="16px">
                              This shows which platforms you posted to and at what time
                            </CustomTooltip>
                          </div>
                          <ul v-if="post.posts.length">
                            <li v-for="postItem in post.posts" class="text-small">
                              Posted on {{ dateTimeUtil.getDateTime(postItem.posted_dt) }} from
                              {{ postItem.email }} account
                            </li>
                          </ul>
                          <div v-else class="text-small q-mt-sm">
                            Content has not been posted to any social platforms
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </template>
              </CollapsableCard>
            </div>
            <q-pagination
              v-if="socialPostPagesCount > 1"
              v-model="pageNumber"
              :max-pages="5"
              :max="socialPostPagesCount"
              direction-links
            />
          </div>
        </q-tab-panel>
        <q-tab-panel name="content">
          <div class="row q-gutter-y-sm">
            <div class="col-12 q-gutter-y-lg q-mb-sm q-mt-xs">
              <CollapsableCard title="Post template">
                <template v-slot:header>
                  <q-btn
                    unelevated dense
                    label="Add post template" icon="add" color="primary"
                    @click="openEditContentDialog(null, true)"
                  />
                </template>
                <template v-slot:body>
                  <div class="col-12">
                    <q-list separator class="q-px-sm">
                      <q-item v-for="item in socialContent" class="bg-hover">
                        <div class="flex items-center w-100">
                          {{ dataUtil.truncateText(item.content, 50) }}
                          <q-space/>
                          <q-btn flat dense icon="edit" text-color="grey-6" @click="openEditContentDialog(item, true)"/>
                          <q-btn flat dense icon="delete" text-color="negative" @click="deleteContentItem(item)"/>
                        </div>
                      </q-item>
                    </q-list>
                  </div>
                </template>
              </CollapsableCard>
              <CollapsableCard title="Images">
                <template v-slot:header>
                  <div class="q-mr-sm">
                    <q-btn
                      v-if="!isImageDisplayList"
                      title="View as list" flat dense
                      icon="list"
                      @click="isImageDisplayList = true"
                    />
                    <q-btn
                      v-if="isImageDisplayList"
                      title="View as cards" flat dense
                      icon="view_module"
                      @click="isImageDisplayList = false"
                    />
                  </div>
                  <q-btn
                    unelevated dense
                    label="Add image" icon="add" color="primary"
                    @click="openUserFileDialog(null, false)"
                  />
                </template>
                <template v-slot:body>
                  <div class="col-12">
                    <q-list v-if="isImageDisplayList" separator class="q-px-sm">
                      <q-item v-for="image in userImages" class="bg-hover">
                        <div class="flex items-center w-100">
                          <img
                            class="q-mr-sm"
                            :src="image.url" :alt="image.title"
                            style="max-height: 32px;"
                          >
                          {{ image.title }}
                          <q-space/>
                          <q-btn flat dense icon="edit" text-color="grey-6" @click="openUserFileDialog(image, false)"/>
                          <q-btn flat dense icon="delete" text-color="negative" @click="deleteUserFile(image)"/>
                        </div>
                      </q-item>
                    </q-list>
                    <div v-else class="row q-ma-md">
                      <div v-for="image in userImages" class="col-12 col-sm-6 col-md-4 q-pa-sm">
                        <q-card flat bordered class="bg-hover">
                          <div class="border-bottom-1-gray-300">
                            <img
                              class="q-pa-sm"
                              :src="image.url" :alt="image.title"
                              style="height: 100px; object-fit: contain"
                            >
                          </div>
                          <q-card-section>
                            <div class="flex items-center w-100">
                              {{ image.title }}
                              <q-space/>
                              <q-btn flat dense icon="edit" text-color="grey-6"
                                     @click="openUserFileDialog(image, false)"/>
                              <q-btn flat dense icon="delete" text-color="negative" @click="deleteUserFile(image)"/>
                            </div>
                          </q-card-section>
                        </q-card>
                      </div>
                    </div>
                  </div>
                </template>
              </CollapsableCard>
              <CollapsableCard title="Videos">
                <template v-slot:header>
                  <div class="q-mr-sm">
                    <q-btn
                      v-if="!isVideoDisplayList"
                      title="View as list" flat dense
                      icon="list"
                      @click="isVideoDisplayList = true"
                    />
                    <q-btn
                      v-if="isVideoDisplayList"
                      title="View as cards" flat dense
                      icon="view_module"
                      @click="isVideoDisplayList = false"
                    />
                  </div>
                  <q-btn
                    unelevated dense
                    label="Add video" icon="add" color="primary"
                    @click="openUserFileDialog(null, true)"
                  />
                </template>
                <template v-slot:body>
                  <div class="col-12">
                    <q-list v-if="isVideoDisplayList" separator class="q-px-sm">
                      <q-item v-for="video in userVideos" class="bg-hover">
                        <div class="flex items-center w-100">
                          <video height="32" class="q-mr-sm">
                            <source :src="video.url">
                          </video>
                          {{ video.title }}
                          <q-space/>
                          <q-btn flat dense icon="edit" text-color="grey-6" @click="openUserFileDialog(video, true)"/>
                          <q-btn flat dense icon="delete" text-color="negative" @click="deleteUserFile(video)"/>
                        </div>
                      </q-item>
                    </q-list>
                    <div v-else class="row q-ma-md">
                      <div v-for="video in userVideos" class="col-12 col-sm-6 col-md-4 q-pa-sm">
                        <q-card flat bordered class="bg-hover">
                          <div class="border-bottom-1-gray-300">
                            <video height="100" class="q-pa-sm" controls style="object-fit: contain">
                              <source :src="video.url">
                            </video>
                          </div>
                          <q-card-section>
                            <div class="flex items-center w-100">
                              {{ video.title }}
                              <q-space/>
                              <q-btn flat dense icon="edit" text-color="grey-6"
                                     @click="openUserFileDialog(video, true)"/>
                              <q-btn flat dense icon="delete" text-color="negative" @click="deleteUserFile(video)"/>
                            </div>
                          </q-card-section>
                        </q-card>
                      </div>
                    </div>
                  </div>
                </template>
              </CollapsableCard>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import CollapsableCard from 'components/CollapsableCard.vue'
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogShareSocialPost, { loadDialogShareSocialPostFn } from 'components/dialogs/DialogShareSocialPost.vue'
import DialogSocialContent, { loadDialogSocialContentFn } from 'components/dialogs/DialogSocialContent.vue'
import DialogUserFile, { loadDialogUserFileDataFn } from 'components/dialogs/DialogUserFile.vue'
import PageHeader from 'components/PageHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import { openConfirmDialog } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useContentStore } from 'stores/content-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'ContentPage',
  components: { CustomTooltip, CollapsableCard, PageHeader },
  data () {
    return {
      tab: 'post',
      isImageDisplayList: true,
      isVideoDisplayList: true,
      pageNumber: 1,
      dataUtil,
      dateTimeUtil,
      fileUtil
    }
  },
  computed: {
    availableSocialPlatforms () {
      // Limit social platforms to those where we have set up an API connection
      return this.socialStore.platforms.filter((platform) => {
        return ['LinkedIn'].includes(platform.name)
      })
    },
    socialContent () {
      return this.contentStore.getSocialContent(this.user.employer_id, this.user.id)
    },
    socialPosts () {
      const postContent = this.contentStore.getSocialPosts(null, this.user.id, this.pageNumber) || {}
      return postContent.posts
    },
    socialPostPagesCount () {
      const postContent = this.contentStore.getSocialPosts(null, this.user.id, this.pageNumber) || {}
      return postContent.total_page_count
    },
    userImages () {
      return this.contentStore.getUserFiles(this.user.id).filter((f) => fileUtil.isImage(f.url))
    },
    userVideos () {
      return this.contentStore.getUserFiles(this.user.id).filter((f) => fileUtil.isVideo(f.url))
    }
  },
  watch: {
    pageNumber: {
      async handler () {
        await this.contentStore.setSocialPosts(null, this.user.id, this.pageNumber)
      }
    }
  },
  methods: {
    async deleteContentItem (contentItem) {
      await this.$api.delete(`social-content-item/${contentItem.id}`)
      await this.contentStore.setSocialContent(this.user.employer_id, this.user.id, true)
    },
    async deletePost (post) {
      openConfirmDialog(this.q, 'Are you sure you want to delete this post? It will only be deleted from JobVyne. If it has been posted to any social media sites, it will continue to exist there.', {
        okFn: async () => {
          await this.$api.delete(`social-post/${post.id}`)
          await this.contentStore.setSocialPosts(null, this.user.id, 1, true)
        }
      })
    },
    async deleteUserFile (file) {
      await this.$api.delete(`user/file/${file.id}`)
      await this.contentStore.setUserFiles(this.user.id, true)
    },
    async openEditContentDialog (contentItem, isTemplate, platform = null) {
      await loadDialogSocialContentFn()
      return this.q.dialog({
        component: DialogSocialContent,
        componentProps: {
          contentItem: contentItem || {},
          user: this.user,
          isEmployer: false,
          isTemplate,
          platform
        }
      })
    },
    async openSharePostDialog (post) {
      await loadDialogShareSocialPostFn()
      return this.q.dialog({
        component: DialogShareSocialPost,
        componentProps: { post }
      })
    },
    async openUserFileDialog (mediaItem, isVideo) {
      await loadDialogUserFileDataFn()
      return this.q.dialog({
        component: DialogUserFile,
        componentProps: {
          file: mediaItem,
          fileTypeKeys: (isVideo) ? [FILE_TYPES.VIDEO.key] : [FILE_TYPES.IMAGE.key]
        }
      })
    }
  },
  preFetch () {
    const contentStore = useContentStore()
    const socialStore = useSocialStore()
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        contentStore.setSocialContent(
          authStore.propUser.employer_id,
          authStore.propUser.id
        ),
        contentStore.setUserFiles(authStore.propUser.id),
        contentStore.setSocialPosts(null, authStore.propUser.id, 1),
        socialStore.setPlatforms()
      ])
    }).finally(() => Loading.hide())
  },
  setup () {
    const authStore = useAuthStore()
    const globalStore = useGlobalStore()
    const { user } = storeToRefs(authStore)

    const pageTitle = 'User Content'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      contentStore: useContentStore(),
      socialStore: useSocialStore(),
      q: useQuasar(),
      user
    }
  }
}
</script>
