<template>
  <q-page padding v-if="isLoaded">
    <div class="q-ml-sm">
      <PageHeader title="Social posts and content">
        <template v-slot:default>
          <slot name="subheader"/>
        </template>
      </PageHeader>
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
        <q-tab v-if="!isEmployer" name="employer_post_template" label="Employer Post Templates"/>
        <q-tab name="content" label="Content"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated :keep-alive="true">
        <q-tab-panel name="post">
          <div class="row q-gutter-y-sm">
            <div class="col-12 q-gutter-x-sm q-gutter-y-md q-mb-sm">
              <q-btn-dropdown color="primary">
                <template v-slot:label>
                  <CustomTooltip v-if="isEmployer" :is_include_icon="false">
                    <template v-slot:content>
                      <q-icon name="add"/>
                      Create post template
                    </template>
                    Post templates are used by employees to easily post to their
                    social profiles
                  </CustomTooltip>
                  <template v-else>
                    <q-icon name="add"/>
                    Create post
                  </template>
                </template>
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
              <SocialPostsSection
                ref="socialPosts"
                :is-employer="isEmployer"
                :is-user-view="!isEmployer"
                :is-editable="true"
                @update-posts="updateSocialPosts()"
              />
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel v-if="!isEmployer" name="employer_post_template">
          <div class="row q-gutter-y-sm q-mt-md">
            <div class="col-12 q-gutter-x-sm q-gutter-y-md q-mb-sm">
              <SocialPostsSection
                ref="socialPostsTemplate"
                :is-employer="true"
                :is-user-view="true"
                :is-editable="false"
                @update-posts="updateSocialPosts()"
              />
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="content">
          <div class="row q-gutter-y-sm">
            <div class="col-12 q-gutter-y-lg q-mb-sm q-mt-xs">
              <CollapsableCard title="Post template text">
                <template v-slot:header>
                  <q-btn
                    unelevated dense
                    label="Add post template text" icon="add" color="primary"
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
                          <q-chip
                            v-if="!isEmployer && !getIsPostContentOwner(item)"
                            dense
                            title="This content was created by your employer"
                            color="grey-4"
                          >
                            Employer
                          </q-chip>
                          <template v-if="getIsPostContentOwner(item)">
                            <q-btn flat dense icon="edit" text-color="grey-6"
                                   @click="openEditContentDialog(item, true)"/>
                            <q-btn flat dense icon="delete" text-color="negative" @click="deleteContentItem(item)"/>
                          </template>
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
                    @click="openFileDialog(null, false)"
                  />
                </template>
                <template v-slot:body>
                  <div class="col-12">
                    <q-list v-if="isImageDisplayList" separator class="q-px-sm">
                      <q-item v-for="image in images" class="bg-hover">
                        <div class="flex items-center w-100">
                          <img
                            class="q-mr-sm"
                            :src="image.url" :alt="image.title"
                            style="max-height: 32px;"
                          >
                          {{ image.title }}
                          <q-space/>
                          <q-btn flat dense icon="edit" text-color="grey-6" @click="openFileDialog(image, false)"/>
                          <q-btn flat dense icon="delete" text-color="negative" @click="deleteFile(image)"/>
                        </div>
                      </q-item>
                    </q-list>
                    <div v-else class="row q-ma-md">
                      <div v-for="image in images" class="col-12 col-sm-6 col-md-4 q-pa-sm">
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
                                     @click="openFileDialog(image, false)"/>
                              <q-btn flat dense icon="delete" text-color="negative" @click="deleteFile(image)"/>
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
                    @click="openFileDialog(null, true)"
                  />
                </template>
                <template v-slot:body>
                  <div class="col-12">
                    <q-list v-if="isVideoDisplayList" separator class="q-px-sm">
                      <q-item v-for="video in videos" class="bg-hover">
                        <div class="flex items-center w-100">
                          <video height="32" class="q-mr-sm">
                            <source :src="video.url">
                          </video>
                          {{ video.title }}
                          <q-space/>
                          <q-btn flat dense icon="edit" text-color="grey-6" @click="openFileDialog(video, true)"/>
                          <q-btn flat dense icon="delete" text-color="negative" @click="deleteFile(video)"/>
                        </div>
                      </q-item>
                    </q-list>
                    <div v-else class="row q-ma-md">
                      <div v-for="video in videos" class="col-12 col-sm-6 col-md-4 q-pa-sm">
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
                                     @click="openFileDialog(video, true)"/>
                              <q-btn flat dense icon="delete" text-color="negative" @click="deleteFile(video)"/>
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
import DialogEmployerFile, { loadDialogEmployerFileDataFn } from 'components/dialogs/DialogEmployerFile.vue'
import DialogSocialContent, { loadDialogSocialContentFn } from 'components/dialogs/DialogSocialContent.vue'
import DialogUserFile, { loadDialogUserFileDataFn } from 'components/dialogs/DialogUserFile.vue'
import PageHeader from 'components/PageHeader.vue'
import SocialPostsSection from 'pages/content-page/SocialPostsSection.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useContentStore } from 'stores/content-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'BaseContentPage',
  components: { SocialPostsSection, CustomTooltip, CollapsableCard, PageHeader },
  props: {
    isEmployer: Boolean
  },
  data () {
    return {
      isLoaded: false,
      tab: 'post',
      isImageDisplayList: true,
      isVideoDisplayList: true,
      dataUtil
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
      return this.contentStore.getSocialContent(
        this.user.employer_id,
        (this.isEmployer) ? null : this.user.id
      )
    },
    files () {
      if (this.isEmployer) {
        return this.employerStore.getEmployerFiles(this.user.employer_id)
      }
      return this.contentStore.getUserFiles(this.user.id) || []
    },
    images () {
      return this.files.filter((f) => fileUtil.isImage(f.url))
    },
    videos () {
      return this.files.filter((f) => fileUtil.isVideo(f.url))
    }
  },
  methods: {
    async deleteContentItem (contentItem) {
      await this.$api.delete(`social-content-item/${contentItem.id}`)
      await this.contentStore.setSocialContent(
        this.user.employer_id,
        (this.isEmployer) ? null : this.user.id,
        true
      )
    },
    async deleteFile (file) {
      if (this.isEmployer) {
        await this.$api.delete(`employer/file/${file.id}`)
        await this.employerStore.setEmployerFiles(this.user.employer_id, true)
      } else {
        await this.$api.delete(`user/file/${file.id}`)
        await this.contentStore.setUserFiles(this.user.id, true)
      }
    },
    async openEditContentDialog (contentItem, isTemplate, platform = null) {
      await loadDialogSocialContentFn()
      return this.q.dialog({
        component: DialogSocialContent,
        componentProps: {
          contentItem: contentItem || {},
          user: this.user,
          isEmployer: this.isEmployer,
          isTemplate,
          platform
        }
      })
    },
    async openFileDialog (mediaItem, isVideo) {
      const componentProps = {
        file: mediaItem,
        fileTypeKeys: (isVideo) ? [FILE_TYPES.VIDEO.key] : [FILE_TYPES.IMAGE.key]
      }

      if (this.isEmployer) {
        await loadDialogEmployerFileDataFn()
        return this.q.dialog({
          component: DialogEmployerFile,
          componentProps
        })
      } else {
        await loadDialogUserFileDataFn()
        return this.q.dialog({
          component: DialogUserFile,
          componentProps
        })
      }
    },
    getIsPostContentOwner (postContentItem) {
      if (this.isEmployer) {
        return Boolean(postContentItem.employer_id)
      }
      return Boolean(postContentItem.user_id)
    },
    getSocialPostFilterParams () {
      const filterParams = {}
      const startDate = this.postFilter?.dateRange?.from
      if (startDate) {
        filterParams.start_date = dateTimeUtil.serializeDate(startDate, true)
      }
      const endDate = this.postFilter?.dateRange?.to
      if (endDate) {
        filterParams.end_date = dateTimeUtil.serializeDate(endDate, true, true)
      }
      if (this.postFilter?.platforms?.length) {
        filterParams.platform_ids = this.postFilter.platforms.map((p) => p.id)
      }
      return filterParams
    },
    async setSocialPosts () {
      const filterParams = this.getSocialPostFilterParams()
      return await this.contentStore.setSocialPosts(
        (this.isEmployer) ? this.user.employer_id : null,
        (this.isEmployer) ? null : this.user.id,
        this.pageNumber, { filterParams }
      )
    },
    updateSocialPosts () {
      this.$refs.socialPosts.setSocialPosts(true)
      const templateSocialPosts = this.$refs.socialPostsTemplate
      if (templateSocialPosts) {
        templateSocialPosts.setSocialPosts(true)
      }
    }
  },
  setup () {
    const authStore = useAuthStore()
    const globalStore = useGlobalStore()
    const { user } = storeToRefs(authStore)

    const pageTitle = 'Social Posts and Content'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      authStore,
      contentStore: useContentStore(),
      employerStore: useEmployerStore(),
      socialStore: useSocialStore(),
      q: useQuasar(),
      user
    }
  },
  async mounted () {
    Loading.show()

    await this.authStore.setUser().then(() => {
      return Promise.all([
        this.contentStore.setSocialContent(
          this.user.employer_id,
          this.user.id
        ),
        this.contentStore.setUserFiles(this.user.id),
        this.setSocialPosts(),
        this.employerStore.setEmployerFiles(this.user.employer_id, true),
        this.socialStore.setPlatforms()
      ])
    }).finally(() => Loading.hide())

    this.isLoaded = true
  }
}
</script>
