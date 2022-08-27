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
        <q-tab name="new" label="New post"/>
        <q-tab name="content" label="Content"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated :keep-alive="true">
        <q-tab-panel name="new">
          <div class="row q-gutter-y-sm">
            <div class="col-12 q-gutter-x-sm q-mb-sm"></div>
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
                    @click="openEditContentDialog"
                  />
                </template>
                <template v-slot:body>
                  <div class="col-12">
                    <q-list separator class="q-px-sm">
                      <q-item v-for="item in socialContent" class="bg-hover">
                        <div class="flex items-center w-100">
                          {{ dataUtil.truncateText(item.content, 50) }}
                          <q-space/>
                          <q-btn flat dense icon="edit" text-color="grey-6" @click="openEditContentDialog(item)"/>
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
import DialogSocialContent from 'components/dialogs/DialogSocialContent.vue'
import DialogUserFile, { loadDialogUserFileDataFn } from 'components/dialogs/DialogUserFile.vue'
import PageHeader from 'components/PageHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useContentStore } from 'stores/content-store.js'

export default {
  name: 'ContentPage',
  components: { CollapsableCard, PageHeader },
  data () {
    return {
      tab: 'new',
      isImageDisplayList: true,
      isVideoDisplayList: true,
      dataUtil
    }
  },
  computed: {
    socialContent () {
      return this.contentStore.getSocialContent(this.user.employer_id, this.user.id)
    },
    userImages () {
      return this.contentStore.getUserFiles(this.user.id).filter((f) => fileUtil.isImage(f.url))
    },
    userVideos () {
      return this.contentStore.getUserFiles(this.user.id).filter((f) => fileUtil.isVideo(f.url))
    }
  },
  methods: {
    async deleteContentItem (contentItem) {
      await this.$api.delete(`social-content-item/${contentItem.id}`)
      await this.contentStore.setSocialContent(this.user.employer_id, this.user.id)
    },
    async deleteUserFile (file) {
      await this.$api.delete(`user/file/${file.id}`)
      await this.contentStore.setUserFiles(this.user.id, true)
    },
    openEditContentDialog (contentItem) {
      return this.q.dialog({
        component: DialogSocialContent,
        componentProps: {
          contentItem,
          user: this.user,
          isEmployer: false
        }
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
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        contentStore.setSocialContent(
          authStore.propUser.employer_id,
          authStore.propUser.id
        ),
        contentStore.setUserFiles(authStore.propUser.id)
      ])
    }).finally(() => Loading.hide())
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return {
      contentStore: useContentStore(),
      q: useQuasar(),
      user
    }
  }
}
</script>
