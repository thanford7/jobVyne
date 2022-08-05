<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Profile">
        <template v-slot:bottom>
          <q-banner v-if="(!user.is_employer_verified && isCompanyUser) || !user.is_email_verified" rounded
                    class="bg-warning">
            <template v-slot:avatar>
              <q-icon name="warning"/>
            </template>
            <template v-if="isCompanyUser">
              You must verify an email that is covered under your company's email domains.
              Use the "Send verification email" button in the
              <a href="/user/profile/?tab=security">"Security" profile section</a>
              to complete this action. The following domains
              are covered:
              <ul>
                <li v-for="domain in supportedEmailDomains">{{ domain }}</li>
              </ul>
              If your primary email is not covered under any of these domains, go to the <a
              href="/user/profile/?tab=general">"General" profile section</a>
              to add your business email.
            </template>
            <template v-else>
              You must verify your email before getting access to most JobVyne features. Use the "Send verification
              email" below to complete this action.
            </template>
          </q-banner>
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
          <div class="row q-gutter-y-lg">
            <div class="col-12">
              <q-table
                :rows="userEmailRows"
                :columns="userEmailColumns"
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
                <template v-slot:header-cell-isEmployerEmail="props">
                  <q-th key="isEmployerEmail">
                    {{ props.col.label }}
                    <CustomTooltip>
                      <template v-slot:icon>
                        <q-icon class="text-gray-500" tag="span" name="help_outline" size="16px"/>
                      </template>
                      You must have a verified email that belongs to an email domain supported
                      by {{ employer.name }}. The following domains are supported:
                      <ul>
                        <li v-for="domain in supportedEmailDomains">{{ domain }}</li>
                      </ul>
                    </CustomTooltip>
                  </q-th>
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
                <template v-slot:body-cell-isEmployerEmail="props">
                  <q-td key="isEmployerEmail" class="text-center">
                    <q-icon v-if="props.row.isEmployerEmail" name="check_circle" color="positive"/>
                    <q-icon v-else name="cancel" color="negative"/>
                  </q-td>
                </template>
              </q-table>
            </div>
            <div class="col-12">
              <q-table
                :rows="userPermissionGroupRows"
                :columns="userPermissionGroupColumns"
                :hide-bottom="true"
              >
                <template v-slot:top>
                  <div class="text-h6">
                    Employer Permission Groups
                    <CustomTooltip :is_include_space="false">
                      Permission groups determine what content you can view for each employer and
                      what you are allowed to do for each employer (e.g. manage other users). Some
                      permissions are automatically approved, but others require the approval of
                      an administrative user from the specified employer.
                    </CustomTooltip>
                  </div>
                </template>
                <template v-slot:header-cell-unapprovedGroups="props">
                  <q-th key="unapprovedGroups">
                    {{ props.col.label }}
                    <CustomTooltip>
                      <template v-slot:icon>
                        <q-icon class="text-gray-500" tag="span" name="help_outline" size="16px"/>
                      </template>
                      Administrative users from the employer are automatically notified when a user
                      has an unapproved permission that requires their review.
                    </CustomTooltip>
                  </q-th>
                </template>
                <template v-slot:body-cell-approvedGroups="props">
                  <q-td key="approvedGroups" class="text-center">
                    <q-chip
                      v-for="group in props.row.approvedGroups"
                      color="grey-7" text-color="white" size="md"
                    >{{ group.name }}</q-chip>
                    <span v-if="!props.row.approvedGroups">{{globalStore.nullValueStr}}</span>
                  </q-td>
                </template>
                <template v-slot:body-cell-unapprovedGroups="props">
                  <q-td key="unapprovedGroups" class="text-center">
                    <q-chip
                      v-for="group in props.row.unapprovedGroups"
                      color="grey-7" text-color="white" size="md"
                    >{{ group.name }}</q-chip>
                    <span v-if="!props.row.unapprovedGroups">{{globalStore.nullValueStr}}</span>
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
import { COMPANY_USER_TYPE_BITS } from 'src/utils/user-types.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import FileDisplayOrUpload from 'components/inputs/FileDisplayOrUpload.vue'

const userPermissionGroupColumns = [
  { name: 'employerName', field: 'employerName', align: 'left', label: 'Employer Name' },
  { name: 'approvedGroups', field: 'approvedGroups', align: 'center', label: 'Approved Groups' },
  { name: 'unapprovedGroups', field: 'unapprovedGroups', align: 'center', label: 'Unapproved Groups' }
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
      userPermissionGroupColumns,
      fileUtil,
      FILE_TYPES
    }
  },
  computed: {
    employer () {
      if (!this.user.employer_id) {
        return {}
      }
      return this.employerStore.getEmployer(this.user.employer_id)
    },
    supportedEmailDomains () {
      if (!this.employer.email_domains) {
        return []
      }
      return this.employer.email_domains.split(',')
    },
    hasUserDataChanged () {
      return !dataUtil.isDeepEqual(this.currentUserData, this.userData)
    },
    userPermissionGroupRows () {
      return Object.entries(this.user.permission_groups_by_employer).map(([employerId, permissionGroups]) => {
        const employer = this.employerStore.getEmployer(employerId)
        const employerName = (employer) ? employer.name : null
        const approvedGroups = permissionGroups.filter((pg) => pg.is_approved)
        const unapprovedGroups = permissionGroups.filter((pg) => !pg.is_approved)
        return { employerName, approvedGroups, unapprovedGroups }
      })
    },
    userEmailColumns () {
      const cols = [
        { name: 'type', field: 'type', align: 'left', label: 'Email type' },
        { name: 'email', field: 'email', align: 'left', label: 'Email' },
        { name: 'isVerified', field: 'isVerified', align: 'center', label: 'Verified' },
        { name: 'action', field: 'action', align: 'center', label: 'Action' }
      ]
      if (this.user.employer_id) {
        cols.splice(2, 0, {
          name: 'isEmployerEmail', field: 'isEmployerEmail', align: 'center', label: 'Employer email'
        })
      }
      return cols
    },
    userEmailRows () {
      const rows = [{
        type: 'Primary',
        email: this.user.email,
        isVerified: this.user.is_email_verified,
        isEmployerEmail: this.user.is_email_employer_permitted,
        action: !this.user.is_email_verified
      }]

      if (this.user.business_email) {
        rows.push({
          type: 'Business',
          email: this.user.business_email,
          isVerified: this.user.is_business_email_verified,
          isEmployerEmail: this.user.is_business_email_employer_permitted,
          action: !this.user.is_business_email_verified
        })
      }

      return rows
    },
    isCompanyUser () {
      return this.user.user_type_bits & COMPANY_USER_TYPE_BITS
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
    const employerStore = useEmployerStore()
    Loading.show()

    return authStore.setUser().then(() => {
      if (authStore.propUser.employer_id) {
        return Promise.all([
          employerStore.setEmployer(authStore.propUser.employer_id)
        ])
      }
    }).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const authStore = useAuthStore()
    const employerStore = useEmployerStore()
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
      employerStore,
      globalStore: useGlobalStore(),
      user
    }
  }
}
</script>
