<template>
  <q-layout view="lHr LpR fFf">

    <q-header v-if="isLoaded" ref="header" elevated reveal class="bg-white text-primary">
      <div class="justify-center row" style="position: relative">
        <q-toolbar class="col-12 col-md-11 col-lg-8 q-pt-md q-px-none justify-center">
          <q-toolbar-title shrink>
            <img v-if="employer?.logo_url" :src="employer.logo_url" alt="Logo"
                 style="height: 40px; max-width: 120px; object-fit: scale-down">
            <img v-else src="~assets/jobVyneLogo.png" alt="Logo"
                 style="height: 40px; max-width: 120px; object-fit: scale-down">
          </q-toolbar-title>
        </q-toolbar>
        <template v-if="isEmployerPage">
          <div
            class="col-12 col-md-11 col-lg-8 q-px-lg q-mb-md-sm flex justify-center text-h6 text-center"
          >
            {{ employer.name }}
          </div>
          <div
            v-if="employer.description"
            class="col-12 col-md-11 col-lg-8 q-px-lg q-mb-sm flex justify-center text-center"
          >
            {{ employer.description }}
          </div>
          <div class="col-12 col-md-11 col-lg-8 q-px-lg q-mb-sm flex justify-center items-center text-center text-small">
            <a v-if="employer.website" :href="`https://www.${employer.website}`" target="_blank">Website</a>
            <template v-if="employer.ats_name">
              &nbsp;
              <CustomTooltip :is_include_icon="false">
                <template v-slot:icon>
                  <q-chip size="12px" color="gray-8" dense outline>{{ employer.ats_name }}</q-chip>
                </template>
                This is the Applicant Tracking System (ATS) that {{ employer.name }} uses. Some ATSs are easier to use
                compared with others. If you've been job searching for a bit of time, you'll know which ones 😆
              </CustomTooltip>
            </template>
          </div>
        </template>
        <div class="q-pt-md flex" style="position: absolute; top: 0; right: 10px;">
          <q-btn
            unelevated round dense color="grey-8"
            :icon="(isLeftDrawerOpen) ? 'close' : 'menu'"
            @click="isLeftDrawerOpen = !isLeftDrawerOpen"
          />
        </div>
        <ResponsiveWidth class="justify-center">
          <q-tabs align="center" v-model="tab" :style="employerStyleUtil.getTabStyle(employer)">
            <q-tab id="jv-tab-jobs" name="jobs" label="Jobs"/>
            <q-tab
              v-if="employerTypeUtil.isTypeGroup(employer?.organization_type)"
              id="jv-tab-community" name="community" label="Community"
            />
            <q-tab v-if="isShowEmployeeProfile" id="jv-tab-me" name="me"
                   :label="`About ${profile?.first_name}`"/>
          </q-tabs>
        </ResponsiveWidth>
      </div>
    </q-header>

    <BaseSidebar
      v-model="isLeftDrawerOpen" side="left"
      @login="loadUserData()"
      @logout="loadUserData()"
    >
      <template v-slot:menuItems>
        <template v-if="user?.id">
          <SidebarMenuItem
            menu-label="Job Applications" icon-name="contact_page"
            @click="openNewCandidatePage('candidate-dashboard')"
          />
          <SidebarMenuItem
            menu-label="Favorites" icon-name="star"
            @click="openNewCandidatePage('candidate-favorites')"
          />
        </template>
      </template>
    </BaseSidebar>

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
        @login="loadUserData()"
        @updateApplications="$refs.jobs.loadApplications()"
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
              v-if="tab === 'jobs'"
              ref="jobs"
              :user="user"
              :employer="employer"
              :user-favorites="userFavorites"
              :headerHeight="headerHeight"
              @openAppSideBar="openJobApplication"
              @closeAppSideBar="isRightDrawerOpen = false"
              @updateUserFavorites="loadUserFavorites(true)"
            />
          </q-tab-panel>
          <q-tab-panel name="community">
            <CommunitySection
              v-if="tab === 'community'"
              :user="user"
              :employer="employer"
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
import CustomTooltip from 'components/CustomTooltip.vue'
import FormJobApplication from 'components/job-app-form/FormJobApplication.vue'
import BaseSidebar from 'components/sidebar/BaseSidebar.vue'
import SidebarMenuItem from 'components/sidebar/SidebarMenuItem.vue'
import CommunitySection from 'pages/jobs-page/CommunitySection.vue'
import JobsSection from 'pages/jobs-page/JobsSection.vue'
import employerStyleUtil from 'src/utils/employer-styles.js'
import employerTypeUtil from 'src/utils/employer-types.js'
import pagePermissionsUtil from 'src/utils/permissions.js'
import scrollUtil from 'src/utils/scroll.js'
import { USER_TYPE_CANDIDATE, USER_TYPES } from 'src/utils/user-types.js'
import userUtil from 'src/utils/user.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useSocialStore } from 'stores/social-store.js'
import { useUserStore } from 'stores/user-store.js'
import { useUtilStore } from 'stores/utility-store.js'
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
      isRightDrawerOpen: false,
      isLeftDrawerOpen: false,
      user: null,
      userFavorites: {},
      employer: null,
      profile: null,
      isLoaded: false,
      jobApplication: null,
      headerHeight: 0,
      anchorPositions: {},
      dataUtil,
      dateTimeUtil,
      employerStyleUtil,
      employerTypeUtil,
      locationUtil,
      pagePermissionsUtil,
      scrollUtil,
      userUtil,
      authStore: useAuthStore(),
      employerStore: useEmployerStore(),
      socialStore: useSocialStore(),
      userStore: useUserStore(),
      utilStore: useUtilStore(),
      q: useQuasar(),
      USER_TYPES,
      USER_TYPE_CANDIDATE
    }
  },
  components: {
    CustomTooltip,
    SidebarMenuItem,
    BaseSidebar,
    CommunitySection,
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
    },
    isEmployerPage () {
      return ['company', 'group'].includes(this.$route.name)
    }
  },
  watch: {
    tab () {
      this.$router.replace({
        name: this.$route.name,
        params: this.$route.params,
        query: { ...this.$route.query, tab: this.tab }
      })
    }
  },
  methods: {
    getFullLocation: locationUtil.getFullLocation,
    async loadUserData () {
      if (!this.user.id) {
        return
      }
      await Promise.all([
        this.loadUserFavorites()
      ])
    },
    async loadUserFavorites (isForceRefresh = true) {
      if (!this.user?.id) {
        this.userFavorites = {}
        return
      }
      await this.userStore.setUserFavorites(this.user.id, { isForceRefresh })
      this.userFavorites = this.userStore.getUserFavorites(this.user.id)
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
    openNewCandidatePage (pageKey) {
      const newPage = this.$router.resolve(
        this.pagePermissionsUtil.getRouterPageCfg(pageKey, USER_TYPES[USER_TYPE_CANDIDATE])
      )
      window.open(newPage.href, '_blank')
    },
    openJobApplication (jobApplication) {
      this.jobApplication = jobApplication
      this.isRightDrawerOpen = true
    },
    async closeJobApplication () {
      this.jobApplication = null
      await this.$refs.jobs.closeApplication()
    }
  },
  async mounted () {
    Loading.show()
    await this.authStore.setUser()
    const { user } = storeToRefs(this.authStore)
    this.user = user
    Loading.hide()
    await Promise.all([
      this.loadData(),
      this.loadUserFavorites(false)
    ])
    this.headerHeight = this.$refs.header.$el.clientHeight
    const { tab } = this.$route.query
    if (tab) {
      this.tab = tab
    }
    this.isLoaded = true
  },
  setup () {
    const globalStore = useGlobalStore()

    useMeta(globalStore.getMetaCfg({
      pageTitle: 'Jobs',
      description: 'Apply to jobs on JobVyne'
    }))
  }
}
</script>

<style lang="scss" scoped>
.application-date {
  padding: 8px;
}
</style>
