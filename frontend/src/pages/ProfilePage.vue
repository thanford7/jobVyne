<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Profile"/>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="general" label="General"/>
        <q-tab name="security" label="Security"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="general">
          <div class="row q-gutter-y-sm">
            <div class="col-12 q-gutter-x-sm q-mb-sm">
              <q-btn
                v-if="hasUserDataChanged"
                ripple label="Undo" color="grey-6" icon="undo"
                @click="undoUserChanges"
              />
              <q-btn
                v-if="hasUserDataChanged"
                ripple label="Save" color="accent" icon="save"
                @click="saveUserChanges"
              />
            </div>
            <div class="col-12">
              <FileDisplayOrUpload
                ref="profileUpload"
                label="profile picture"
                :file-url="userData.profile_picture_url"
                :new-file="userData[newProfilePictureKey]"
                :new-file-key="newProfilePictureKey"
                file-url-key="profile_picture_url"
              >
                <template v-slot:fileInput>
                  <q-file
                    ref="newProfileUpload"
                    filled bottom-slots clearable
                    v-model="userData[newProfilePictureKey]"
                    label="Profile picture"
                    class="q-mb-none"
                    :accept="fileUtil.getAllowedFileExtensionsStr([FILE_TYPES.IMAGE.key])"
                    max-file-size="1000000"
                  />
                </template>
              </FileDisplayOrUpload>
            </div>
            <div class="col-12 col-md-6 q-pr-md-sm">
              <q-input
                filled
                v-model="userData.first_name"
                label="First name"
                lazy-rules
                :rules="[
                  val => val && val.length > 0 || 'First name is required'
                ]"
              />
            </div>
            <div class="col-12 col-md-6 q-pl-md-sm">
              <q-input
                filled
                v-model="userData.last_name"
                label="Last name"
                lazy-rules
                :rules="[
                  val => val && val.length > 0 || 'Last name is required'
                ]"
              />
            </div>
            <div class="col-12 col-md-6 q-pr-md-sm">
              <q-input
                filled
                v-model="userData.email"
                label="Email (Read only)"
                readonly
                class="q-pb-md"
              />
            </div>
            <div class="col-12 col-md-6 q-pl-md-sm">
              <EmailInput v-model="userData.business_email" label="Business email"/>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import EmailInput from 'components/inputs/EmailInput.vue'
import PageHeader from 'components/PageHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta } from 'quasar'
import dataUtil from 'src/utils/data.js'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import FileDisplayOrUpload from 'components/inputs/FileDisplayOrUpload.vue'

export default {
  name: 'ProfilePage',
  components: { EmailInput, FileDisplayOrUpload, PageHeader },
  data () {
    return {
      tab: 'general',
      currentUserData: dataUtil.deepCopy(this.user),
      userData: dataUtil.deepCopy(this.user),
      newProfilePictureKey: 'profile_picture',
      fileUtil,
      FILE_TYPES
    }
  },
  computed: {
    hasUserDataChanged () {
      return !dataUtil.isDeepEqual(this.currentUserData, this.userData)
    }
  },
  methods: {
    async saveUserChanges () {
      const data = Object.assign({},
        this.userData,
        (this.$refs.profileUpload) ? this.$refs.profileUpload.getValues() : {}
      )
      await this.$api.put(`user/${this.user.id}/`, getAjaxFormData(data, [this.newProfilePictureKey]))
      await this.authStore.setUser(true)
      this.userData = dataUtil.deepCopy(this.authStore.propUser)
      this.currentUserData = dataUtil.deepCopy(this.authStore.propUser)
    },
    undoUserChanges () {
      this.userData = dataUtil.deepCopy(this.user)
    }
  },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)

    const globalStore = useGlobalStore()
    const pageTitle = 'Profile Page'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      authStore,
      user
    }
  }
}
</script>
