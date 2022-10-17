<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Account">
        <template v-slot:bottom>
          <q-banner v-if="(!user.is_employer_verified && isCompanyUser) || !user.is_email_verified" rounded
                    class="bg-warning">
            <template v-slot:avatar>
              <q-icon name="warning"/>
            </template>
            <template v-if="isCompanyUser && user.employer_id">
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
            <template v-else-if="isCompanyUser && !user.employer_id && potentialEmployers.length">
              As an employee or employer user, you must first select your employer. You can select
              your employer in the <a href="/user/profile/?tab=general">"General" profile section</a>.
            </template>
            <template v-else-if="isCompanyUser && !user.employer_id && !potentialEmployers.length">
              As an employee or employer user, you must first select your employer. Your current email
              address does not match with any employers on the JobVyne platform. If you have not yet
              added your business email, add it in the <a href="/user/profile/?tab=general">"General" profile section</a>.
              If your employer is still not found, you can use the help menu to receive assistance from the JobVyne team.
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
      <q-tab-panels v-model="tab" animated :keep-alive="true">
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
              <SelectOrDisplayProfilePic ref="profileUpload" :user-data="userData"/>
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
              <EmailInput
                v-model="userData.business_email"
                label="Business email"
                :is-required="false"
                :additional-rules="[
                  val => val !== userData.email || 'Business email must be different than personal email'
                ]"
              />
            </div>
            <div class="col-12 col-md-6 q-pr-md-sm">
              <q-select
                filled emit-value map-options
                v-model="userData.employer_id"
                :options="potentialEmployers"
                autocomplete="name"
                option-value="id"
                option-label="name"
                label="Employer"
                lazy-rules
                :rules="[val => val || 'Please select an option']"
              />
            </div>
            <div class="col-12 col-md-6 q-pl-md-sm">
              <SelectUserType v-model="userData.user_type_bits" :is-multi="true"/>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="security">
          <div class="row q-gutter-y-lg">
            <div class="col-12 border-bottom-1-gray-300">
              <div class="text-h6">Password update</div>
              <div class="row q-mt-md">
                <div class="col-12">
                  <q-btn
                    ripple color="primary"
                    label="Send password reset email"
                    @click="sendPasswordReset()"
                  />
                </div>
                <div class="col-12">
                  <SeparatorWithText>or</SeparatorWithText>
                </div>
                <q-form
                  @submit="savePassword"
                  class="q-gutter-xs q-mb-md"
                >
                  <div class="row">
                    <div class="col-12">
                      <PasswordInput label="Current password" v-model="passwordData.current_password"/>
                    </div>
                    <div class="col-12 col-md-6 q-pr-md-sm">
                      <PasswordInput label="New password" v-model="passwordData.new_password" :is-validate="true"/>
                    </div>
                    <div class="col-12 col-md-6">
                      <PasswordInput
                        label="Re-enter new password"
                        v-model="passwordData.new_password_confirm"
                        :custom-rules="[
                        (val) => val === passwordData.new_password || 'Password must match'
                      ]"
                      />
                    </div>
                    <div class="col-12 q-mt-sm">
                      <q-btn
                        label="Update password"
                        type="submit" ripple
                        color="primary"
                      />
                    </div>
                  </div>
                </q-form>
              </div>
            </div>
            <div class="col-12">
              <q-table
                :rows="userEmailRows"
                :columns="userEmailColumns"
                :hide-bottom="true"
              >
                <template v-slot:top>
                  <div class="text-h6">
                    Email verification
                    <CustomTooltip>
                      Email verification helps us make sure it's actually you!
                      <q-icon name="fa-solid fa-user-secret"/>
                    </CustomTooltip>
                  </div>
                </template>
                <template v-slot:header-cell-isEmployerEmail="props">
                  <q-th key="isEmployerEmail">
                    {{ props.col.label }}
                    <CustomTooltip :is_include_space="true">
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
                    <CustomTooltip>
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
                    <CustomTooltip :is_include_space="true">
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
                    >{{ group.name }}
                    </q-chip>
                    <span v-if="!props.row.approvedGroups">{{ globalStore.nullValueStr }}</span>
                  </q-td>
                </template>
                <template v-slot:body-cell-unapprovedGroups="props">
                  <q-td key="unapprovedGroups" class="text-center">
                    <q-chip
                      v-for="group in props.row.unapprovedGroups"
                      color="grey-7" text-color="white" size="md"
                    >{{ group.name }}
                    </q-chip>
                    <span v-if="!props.row.unapprovedGroups">{{ globalStore.nullValueStr }}</span>
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
import PasswordInput from 'components/inputs/PasswordInput.vue'
import SelectOrDisplayProfilePic from 'components/inputs/SelectOrDisplayProfilePic.vue'
import SelectUserType from 'components/inputs/SelectUserType.vue'
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
import SeparatorWithText from 'components/SeparatorWithText.vue'

const userPermissionGroupColumns = [
  { name: 'employerName', field: 'employerName', align: 'left', label: 'Employer Name' },
  { name: 'approvedGroups', field: 'approvedGroups', align: 'center', label: 'Approved Groups' },
  { name: 'unapprovedGroups', field: 'unapprovedGroups', align: 'center', label: 'Unapproved Groups' }
]

export default {
  name: 'ProfilePage',
  components: { SelectOrDisplayProfilePic, SelectUserType, PasswordInput, CustomTooltip, EmailInput, PageHeader, SeparatorWithText },
  data () {
    return {
      tab: 'general',
      currentUserData: dataUtil.deepCopy(this.user),
      userData: dataUtil.deepCopy(this.user),
      passwordData: {
        current_password: null,
        new_password: null,
        new_password_confirm: null
      },
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
    potentialEmployers () {
      const personal = this.employerStore.getEmployersFromDomain(this.authStore.propUser.email) || []
      const business = this.employerStore.getEmployersFromDomain(this.authStore.propUser.business_email) || []
      return dataUtil.uniqArray([...personal, ...business])
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
      this.$router.replace({ name: this.$route.name, params: this.$route.params, query: { tab: this.tab } })
    }
  },
  methods: {
    // General tab
    async saveUserChanges () {
      const data = Object.assign({},
        this.userData,
        (this.$refs.profileUpload) ? this.$refs.profileUpload.getValues() : {}
      )
      await this.$api.put(`user/${this.user.id}/`, getAjaxFormData(data, [this.$refs.profileUpload.newProfilePictureKey]))
      await this.authStore.setUser(true).then(() => {
        // Need to update employer in case user's employer changed
        return Promise.all([
          this.employerStore.setEmployer(this.authStore.propUser.employer_id, true),
          this.employerStore.setEmployersFromDomain(this.authStore.propUser.business_email, true)
        ])
      })
      this.userData = dataUtil.deepCopy(this.authStore.propUser)
      this.currentUserData = dataUtil.deepCopy(this.authStore.propUser)
    },
    undoUserChanges () {
      this.userData = dataUtil.deepCopy(this.user)
    },
    // Security tab
    savePassword () {
      this.$api.put('password-reset/', getAjaxFormData(this.passwordData))
    },
    sendPasswordReset () {
      this.$api.post('password-reset-generate/', getAjaxFormData({ email: this.user.email }))
    },
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
      return Promise.all([
        employerStore.setEmployer(authStore.propUser.employer_id),
        employerStore.setEmployersFromDomain(authStore.propUser.email),
        employerStore.setEmployersFromDomain(authStore.propUser.business_email)
      ])
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
      globalStore,
      user
    }
  }
}
</script>
