<template>
  <q-layout view="hHr lpR fFf">

    <q-header v-if="isLoaded" ref="header" elevated class="bg-white text-primary">
      <div class="justify-center row" style="position: relative">
        <q-toolbar class="col-12 col-md-11 col-lg-8 q-pt-md q-px-none justify-center">
          <q-toolbar-title shrink>
            <img v-if="employer?.logo_url" :src="employer.logo_url" alt="Logo"
                 style="height: 40px; max-width: 120px; object-fit: scale-down">
            <img v-else src="~assets/jobVyneLogo.png" alt="Logo"
                 style="height: 40px; max-width: 120px; object-fit: scale-down">
          </q-toolbar-title>
        </q-toolbar>
        <div class="q-pt-md flex" style="position: absolute; top: 0; right: 10px;">
          <div class="q-mr-md clickable" :style="employerStyleUtil.getTabStyle(employer)" @click="openFeedbackModal()">
            <div class="flex flex-center">
              <q-icon name="feedback" size="24px"/>
            </div>
            <div>Get help</div>
          </div>
          <div v-if="user && !dataUtil.isEmpty(user)">
            <div class="row flex-center">
              <q-avatar v-if="user.profile_picture_url" size="24px">
                <img :src="user.profile_picture_url">
              </q-avatar>
              <q-avatar v-else color="primary" text-color="white" size="24px">
                {{ userUtil.getUserInitials(user) }}
              </q-avatar>
            </div>
            <div>
              <a href="#" @click.prevent="logoutUser()" id="jv-logout" style="color: gray">Logout</a>
            </div>
          </div>
        </div>
        <ResponsiveWidth class="justify-center">
          <q-tabs align="center" v-model="tab" :style="employerStyleUtil.getTabStyle(employer)">
            <q-tab id="jv-tab-jobs" name="jobs" label="Jobs"/>
            <q-tab v-if="isShowEmployeeProfile" id="jv-tab-me" name="me"
                   :label="`About ${profile?.first_name}`"/>
          </q-tabs>
        </ResponsiveWidth>
      </div>
    </q-header>

    <q-drawer
      v-if="jobApplication"
      v-model="isRightDrawerOpen"
      side="right"
      :breakpoint="600"
      :width="400"
      overlay bordered persistent
    >
      <FormJobApplication
        ref="jobApplicationForm"
        :job-application="jobApplication"
        :employer="employer"
        @login="this.authStore.setApplications(this.authStore.propUser)"
        @closeApplication="closeJobApplication()"
      />
      <div v-if="isRightDrawerOpen" class="absolute" style="top: 10px; left: -16px">
        <q-btn
          dense round unelevated
          color="grey-5"
          icon="chevron_right"
          @click="closeJobApplication()"
        />
      </div>
    </q-drawer>

    <q-page-container class="q-pt-none">
      <q-page v-if="isLoaded">
        <q-tab-panels v-model="tab" animated keep-alive class="no-overflow">
          <q-tab-panel name="jobs" style="position: relative;">
            <JobsSection
              ref="jobs"
              :user="user"
              :employer="employer"
              :headerHeight="headerHeight"
              @openAppSideBar="openJobApplication"
              @closeAppSideBar="isRightDrawerOpen = false"
            />
          </q-tab-panel>
          <q-tab-panel name="me" v-if="isShowEmployeeProfile" class="q-pa-none">
            <div class="row justify-center q-px-xl q-pt-xl bg-grey-3">
              <div class="col-12 col-md-3 q-pr-md-md q-mb-md q-mb-md-none">
                <div class="flex items-center">
                  <img
                    v-if="profile.profile_picture_url"
                    :src="profile.profile_picture_url"
                    alt="Profile picture"
                    class="q-mr-md"
                    style="height: 150px; object-fit: scale-down; border-radius: 10px; float: left;"
                  >
                  <div class="q-gutter-y-sm">
                    <div class="text-h6 text-bold">{{ profile.first_name }} {{ profile.last_name }}</div>
                    <div>{{ profile.job_title }}</div>
                    <div v-if="profile.home_location">{{ locationUtil.getFullLocation(profile.home_location) }}</div>
                    <div v-if="profile.employment_start_date">
                      {{ dataUtil.pluralize('year', employmentYears) }} at {{ employer.name }}
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-12 col-md-4 q-pl-md-md">
                <div v-for="response in profile.profile_responses">
                  <div class="text-h6">{{ response.question }}</div>
                  <div class="q-mt-sm q-mb-md">{{ response.response }}</div>
                </div>
              </div>
            </div>
          </q-tab-panel>
        </q-tab-panels>
        <q-page-scroller position="bottom-right" :scroll-offset="100" :offset="[40, 40]">
          <q-btn round color="primary" icon="arrow_upward"/>
        </q-page-scroller>
      </q-page>
    </q-page-container>

    <CustomFooter/>
  </q-layout>
</template>

<script>
import DialogFeedback from 'components/dialogs/DialogFeedback.vue'
import FormJobApplication from 'components/job-app-form/FormJobApplication.vue'
import JobsSection from 'pages/jobs-page/JobsSection.vue'
import employerStyleUtil from 'src/utils/employer-styles.js'
import scrollUtil from 'src/utils/scroll.js'
import userUtil from 'src/utils/user.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useSocialStore } from 'stores/social-store.js'
import { useUserStore } from 'stores/user-store.js'
import { useUtilStore } from 'stores/utility-store.js'
import { ref } from 'vue'
import CustomFooter from 'components/CustomFooter.vue'
import locationUtil from 'src/utils/location'
import dataUtil from 'src/utils/data'
import { useAuthStore } from 'stores/auth-store'
import { Loading, useMeta, useQuasar } from 'quasar'
import { useGlobalStore } from 'stores/global-store'
import dateTimeUtil from 'src/utils/datetime'
import { storeToRefs } from 'pinia/dist/pinia'
import ResponsiveWidth from 'components/ResponsiveWidth.vue'

export default {
  data () {
    return {
      tab: this.$route?.params?.tab || 'jobs',
      pageNumber: 1,
      employer: null,
      profile: null,
      isLoaded: false,
      jobApplication: null,
      headerHeight: 0,
      anchorPositions: {},
      dataUtil,
      dateTimeUtil,
      employerStyleUtil,
      locationUtil,
      scrollUtil,
      userUtil
    }
  },
  components: {
    JobsSection,
    ResponsiveWidth,
    CustomFooter,
    FormJobApplication
  },
  computed: {
    employmentYears () {
      if (!this.profile.employment_start_date) {
        return null
      }
      return dateTimeUtil.getDateDifference(this.profile.employment_start_date, dateTimeUtil.now(), 'years')
    },
    isShowEmployeeProfile () {
      return Boolean(this.profile && this.profile.is_profile_viewable && this.profile.profile_responses.length)
    }
  },
  methods: {
    log (val) {
      console.log(val)
    },
    getFullLocation: locationUtil.getFullLocation,
    async logoutUser () {
      await this.authStore.logout(false)
      await this.authStore.setApplications()
    },
    async setLinkOwnerProfile () {
      const params = { socialLinkId: this.$route.params.filterId }
      await this.userStore.setUserProfile(params)
      this.profile = this.userStore.getUserProfile(params)
    },
    async setEmployer () {
      const params = {
        socialLinkId: this.$route.params.filterId,
        employerKey: this.$route.params.employerKey
      }
      await this.socialStore.setSocialLinkEmployer(params)
      this.employer = this.socialStore.getSocialLinkEmployer(params)
    },
    async loadData () {
      this.isLoaded = false
      Loading.show()
      await Promise.all([
        this.setLinkOwnerProfile(),
        this.setEmployer()
      ])
      this.isLoaded = true
      Loading.hide()
    },
    openJobApplication (jobApplication) {
      this.jobApplication = jobApplication
      this.isRightDrawerOpen = true
    },
    async closeJobApplication () {
      this.jobApplication = null
      await this.$refs.jobs.closeApplication()
    },
    openFeedbackModal () {
      return this.q.dialog({
        component: DialogFeedback
      })
    }
  },
  async mounted () {
    await this.loadData()
    this.headerHeight = this.$refs.header.$el.clientHeight
    this.isLoaded = true
  },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const isRightDrawerOpen = ref(false)
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const { user, applications } = storeToRefs(authStore)

    useMeta(globalStore.getMetaCfg({
      pageTitle: 'Jobs',
      description: 'Apply to jobs on JobVyne'
    }))

    return {
      user,
      applications,
      isRightDrawerOpen,
      authStore,
      employerStore: useEmployerStore(),
      socialStore: useSocialStore(),
      userStore: useUserStore(),
      utilStore: useUtilStore(),
      q: useQuasar()
    }
  }
}
</script>

<style lang="scss" scoped>
.application-date {
  padding: 8px;
}
</style>
