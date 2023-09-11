<template>
  <q-layout view="lHr LpR fFf">

    <q-header v-if="isLoaded" ref="header" elevated reveal class="bg-white text-primary">
      <div class="justify-center row" style="position: relative">
        <q-toolbar class="col-12 col-md-11 col-lg-8 q-pt-md q-px-none justify-center">
          <q-toolbar-title shrink>
            <img v-if="isUserPage" :src="profile.profile_picture_url" alt="Profile Picture"
                 style="height: 40px; max-width: 120px; object-fit: scale-down; border-radius: 50px;">
            <img v-else-if="employer?.logo_url" :src="employer.logo_url" alt="Logo"
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
            v-if="employer.description && !utilStore.isUnderBreakPoint('sm')"
            class="col-12 col-md-11 col-lg-8 q-px-lg q-mb-sm flex justify-center text-center"
          >
            {{ employer.description }}
          </div>
          <div
            class="col-12 col-md-11 col-lg-8 q-px-lg q-mb-sm flex justify-center items-center text-center text-small">
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
        <template v-else-if="isUserPage">
          <div
            class="col-12 col-md-11 col-lg-8 q-px-lg q-mb-md-sm flex justify-center text-h6 text-center"
          >
            {{ profile.first_name }} {{ profile.last_name }}
          </div>
          <div
            class="col-12 col-md-11 col-lg-8 q-px-lg q-mb-sm flex justify-center text-center"
          >
            <LocationChip v-if="profile.home_location" :locations="[profile.home_location]" icon="home"/>
            <q-chip
              v-if="profile.job_title"
              color="grey-7" text-color="white" size="md" icon="work"
            >
              {{ profile.job_title }}
            </q-chip>
            <q-chip
              v-if="profile.employer_name"
              color="grey-7" text-color="white" size="md" icon="business"
            >
              {{ profile.employer_name }}
            </q-chip>
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
        <template v-if="user?.id && userTypeUtil.isCandidate(user.user_type_bits)">
          <SidebarMenuItem
            menu-label="Job Applications" icon-name="contact_page"
            @click="openNewCandidatePage('candidate-dashboard')"
          />
          <SidebarMenuItem
            menu-label="Favorites" icon-name="star"
            @click="openNewCandidatePage('candidate-favorites')"
          />
          <SidebarMenuItem
            menu-label="Connections" icon-name="hub"
            @click="openNewCandidatePage('candidate-connections')"
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
        @updateApplications="$refs.jobs.loadJobs(true)"
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
        </q-tab-panels>
        <q-page-scroller position="bottom-right" :scroll-offset="100" :offset="[40, 40]">
          <q-btn round color="primary" icon="arrow_upward"/>
        </q-page-scroller>
        <q-page-sticky v-if="!user?.id" expand position="top">
          <q-toolbar class="items-center text-center border-y-1-primary bg-white">
            <div class="w-100 q-py-sm">
              🍇 Join The JobVyne Community | We Help Each Other Find Jobs 🍇
              <q-btn
                filled rounded color="accent" style="min-width: 100px;"
                @click="openSignUpDialog()"
              >
                Join
              </q-btn>
            </div>
          </q-toolbar>
        </q-page-sticky>
      </q-page>
    </q-page-container>

    <CustomFooter/>
  </q-layout>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import dialogLogin from 'components/dialogs/DialogLogin.vue'
import DialogUserProfile from 'components/dialogs/DialogUserProfile.vue'
import FormJobApplication from 'components/job-app-form/FormJobApplication.vue'
import LocationChip from 'components/LocationChip.vue'
import BaseSidebar from 'components/sidebar/BaseSidebar.vue'
import SidebarMenuItem from 'components/sidebar/SidebarMenuItem.vue'
import CommunitySection from 'pages/jobs-page/CommunitySection.vue'
import JobsSection from 'pages/jobs-page/JobsSection.vue'
import colorUtil from 'src/utils/color.js'
import employerStyleUtil from 'src/utils/employer-styles.js'
import employerTypeUtil from 'src/utils/employer-types.js'
import pagePermissionsUtil from 'src/utils/permissions.js'
import scrollUtil from 'src/utils/scroll.js'
import userTypeUtil, { USER_TYPE_CANDIDATE, USER_TYPES } from 'src/utils/user-types.js'
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
      colorUtil,
      dataUtil,
      dateTimeUtil,
      employerStyleUtil,
      employerTypeUtil,
      locationUtil,
      pagePermissionsUtil,
      scrollUtil,
      userUtil,
      userTypeUtil,
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
    LocationChip,
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
    isEmployerPage () {
      return ['company', 'group'].includes(this.$route.name)
    },
    isUserPage () {
      return this.$route.name === 'profile'
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
      const params = { userKey: this.$route.params.userKey }
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
    openSignUpDialog () {
      this.q.dialog({
        component: dialogLogin,
        componentProps: {
          isCreateDefault: true,
          redirectPageUrl: window.location.pathname,
          redirectParams: Object.assign(dataUtil.getQueryParams(), { isSignUp: true }),
          userTypeBit: USER_TYPES[USER_TYPE_CANDIDATE]
        }
      })
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
    },
    openUserProfile () {
      if (this.$route.query?.isSignUp) {
        if (this.user?.id) {
          this.q.dialog({
            component: DialogUserProfile
          })
        }
        const fullPath = dataUtil.getUrlWithParams({ deleteParams: ['isSignUp'] })
        window.history.replaceState({ path: fullPath }, '', fullPath)
      }
    }
  },
  updated () {
    this.openUserProfile()
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
    this.openUserProfile()
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
