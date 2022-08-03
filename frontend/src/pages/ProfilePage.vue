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
        <q-tab-panel name="security">
          <div class="row q-gutter-y-sm">
            <div class="col-12">
              <q-table
                :rows="userEmailRows"
                :columns="emailVerificationColumns"
                :hide-bottom="true"
              >
                <template v-slot:top>
                  <div class="text-h6">
                    Email verification
                    <CustomTooltip :is_include_space="false">
                      Email verification helps us make sure it's actually you!
                      <q-icon name="fa-solid fa-user-secret"/>
                    </CustomTooltip>
                  </div>
                </template>
                <template v-slot:body-cell-isVerified="props">
                  <q-td key="isVerified" class="text-center">
                    <q-icon v-if="props.row.isVerified" name="check_circle" color="positive"/>
                    <q-icon v-else name="cancel" color="negative"/>
                  </q-td>
                </template>
                <template v-slot:body-cell-action="props">
                  <q-td key="action">
                    <div class="flex justify-center">
                      <q-btn
                        v-if="props.row.action"
                        color="primary"
                        label="Send verification email"
                        ripple dense
                        @click="sendVerificationEmail(props.row.email)"
                      />
                      <span v-else>None required</span>
                    </div>
                  </q-td>
                </template>
              </q-table>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
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

const emailVerificationColumns = [
  { name: 'type', field: 'type', align: 'left', label: 'Email type' },
  { name: 'email', field: 'email', align: 'left', label: 'Email' },
  { name: 'isVerified', field: 'isVerified', align: 'center', label: 'Verified' },
  { name: 'action', field: 'action', align: 'center', label: 'Action' }
]

export default {
  name: 'ProfilePage',
  components: { CustomTooltip, EmailInput, FileDisplayOrUpload, PageHeader },
  data () {
    return {
      tab: 'general',
      currentUserData: dataUtil.deepCopy(this.user),
      userData: dataUtil.deepCopy(this.user),
      newProfilePictureKey: 'profile_picture',
      emailVerificationColumns,
      fileUtil,
      FILE_TYPES
    }
  },
  computed: {
    hasUserDataChanged () {
      return !dataUtil.isDeepEqual(this.currentUserData, this.userData)
    },
    userEmailRows () {
      const rows = [{
        type: 'Primary',
        email: this.user.email,
        isVerified: this.user.is_email_verified,
        action: !this.user.is_email_verified
      }]

      if (this.user.business_email) {
        rows.push({
          type: 'Business',
          email: this.user.business_email,
          isVerified: this.user.is_business_email_verified,
          action: !this.user.is_business_email_verified
        })
      }

      return rows
    }
  },
  watch: {
    tab () {
      this.$router.replace({ name: this.$route.name, query: { tab: this.tab } })
    }
  },
  methods: {
    // General tab
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
    },
    // Security tab
    sendVerificationEmail (email) {
      this.$api.post('verify-email-generate/', getAjaxFormData({ email }))
    }
  },
  mounted () {
    const { tab } = this.$route.query
    if (tab) {
      this.tab = tab
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
