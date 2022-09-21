<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Profile settings">
        Your profile will be displayed on all jobs pages which job seekers are directed to when they click on one of
        your referral links. Adding profile information helps job seekers understand your company better and increases
        the likelihood that they will apply to a job.
        <div class="col-12 q-mt-sm">
          <q-btn
            type="a"
            color="primary"
            :to="{
              name: 'jobs-link-example',
              params: { employerId: user.employer_id, ownerId: user.id, tab: 'me'}
            }"
            target="_blank"
          >
            <q-icon name="launch"/>
            &nbsp;Live site view
          </q-btn>
          <q-toggle
            v-model="userData.is_profile_viewable"
            color="primary"
            @update:model-value="saveUserChanges"
          >
            Is viewable
            <CustomTooltip :is_include_space="false">
              When off, your profile will not be shown on any job pages. It is recommended to turn on page viewing
              so job seekers can learn more about you and your company.
            </CustomTooltip>
          </q-toggle>
        </div>
      </PageHeader>
      <div class="row q-mt-md q-gutter-y-md">
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
          <div class="text-h6">Basic info</div>
        </div>
        <div class="col-12">
          <SelectOrDisplayProfilePic ref="profileUpload" :user-data="userData"/>
        </div>
        <div class="col-12 col-md-6 q-pr-md-sm">
          <q-input
            filled
            v-model="userData.job_title"
            label="Job title"
          />
        </div>
        <div class="col-12 col-md-6 q-pl-md-sm">
          <SelectMonthYear
            v-model="userData.employment_start_date"
            label="Employment start month"
          />
        </div>
        <div class="col-12">
          <q-input
            v-model="userData.home_location_text"
            filled
            label="Work location"
            hint="City, State, Country"
          >
            <template v-slot:after>
              <CustomTooltip :is_include_space="false">
                If you work remotely, use the city you currently live in
              </CustomTooltip>
            </template>
          </q-input>
        </div>
        <div class="col-12">
          <div class="text-h6">
            Profile questions
            <CustomTooltip :is_include_space="false">
              Fill out one or more questions to have your profile displayed on all
              of the jobs pages from your links.
            </CustomTooltip>
          </div>
        </div>
        <div v-for="question in userData.profile_questions" class="col-12">
          <q-input
            v-model="question.response"
            filled autogrow
            :label="question.question"
            type="textarea"
          />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import SelectMonthYear from 'components/inputs/SelectMonthYear.vue'
import SelectOrDisplayProfilePic from 'components/inputs/SelectOrDisplayProfilePic.vue'
import PageHeader from 'components/PageHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta } from 'quasar'
import dataUtil from 'src/utils/data.js'
import locationUtil from 'src/utils/location.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'ProfilePage',
  components: { CustomTooltip, SelectMonthYear, PageHeader, SelectOrDisplayProfilePic },
  data () {
    return {
      currentUserData: this.getUserData(),
      userData: this.getUserData()
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
      await this.$api.put(`user/${this.user.id}/`, getAjaxFormData(data, [this.$refs.profileUpload.newProfilePictureKey]))
      await this.authStore.setUser(true)
      await this.authStore.setUserEmployeeQuestions(this.user.employer_id)
      this.userData = this.getUserData()
      this.currentUserData = this.getUserData()
    },
    getUserData () {
      const userData = Object.assign(
        dataUtil.deepCopy(this.user),
        { profile_questions: dataUtil.deepCopy(this.authStore.getUserEmployeeQuestions(this.user.employer_id)) }
      )
      if (userData.home_location) {
        userData.home_location_text = locationUtil.getFullLocation(userData.home_location)
      }
      return userData
    },
    undoUserChanges () {
      this.userData = this.getUserData()
    }
  },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        authStore.setUserEmployeeQuestions(authStore.propUser.employer_id)
      ])
    }).finally(() => {
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

<style scoped>

</style>
