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
              <CollapsableCard title="Text content">
                <template v-slot:header>
                  <q-btn
                    unelevated dense
                    label="Add post content" icon="add" color="primary"
                    @click="openEditContentDialog"
                  />
                </template>
                <template v-slot:body>
                  <div class="col-12">
                    <q-list separator class="q-px-sm">
                      <q-item v-for="item in socialContent">
                        <div class="flex items-center w-100">
                          {{ dataUtil.truncateText(item.content, 100) }}
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
                  <q-btn
                    unelevated dense
                    label="Add image" icon="add" color="primary"
                    @click="openEditMediaDialog"
                  />
                </template>
                <template v-slot:body>
                  <div class="q-px-md q-py-sm">
                    xxx
                  </div>
                </template>
              </CollapsableCard>
              <CollapsableCard title="Videos">
                <template v-slot:header>
                  <q-btn
                    unelevated dense
                    label="Add video" icon="add" color="primary"
                  />
                </template>
                <template v-slot:body>
                  <div class="q-px-md q-py-sm">
                    xxx
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
import DialogMediaContent from 'components/dialogs/DialogMediaContent.vue'
import DialogSocialContent from 'components/dialogs/DialogSocialContent.vue'
import PageHeader from 'components/PageHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useContentStore } from 'stores/content-store.js'

export default {
  name: 'ContentPage',
  components: { CollapsableCard, PageHeader },
  data () {
    return {
      tab: 'new',
      dataUtil
    }
  },
  computed: {
    socialContent () {
      return this.contentStore.getSocialContent(this.user.employer_id, this.user.id)
    }
  },
  methods: {
    async deleteContentItem (contentItem) {
      await this.$api.delete(`social-content-item/${contentItem.id}`)
      await this.contentStore.setSocialContent(this.user.employer_id, this.user.id)
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
    openEditMediaDialog (mediaItem) {
      return this.q.dialog({
        component: DialogMediaContent
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
        )
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
