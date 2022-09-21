<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Profile settings">
        Your profile will be displayed on all jobs pages which job seekers are directed to when they click on one of
        your referral links. Adding profile information helps job seekers understand your company better and increases
        the likelihood that they will apply to a job.
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
import { useEmployerStore } from 'stores/employer-store.js'
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
  preFetch () {
    const authStore = useAuthStore()
    const employerStore = useEmployerStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployer(authStore.propUser.employer_id)
      ])
    }).finally(() => {
      Loading.hide()
    })
  },
  methods: {
    async saveUserChanges () {
      const data = Object.assign({},
        this.userData,
        (this.$refs.profileUpload) ? this.$refs.profileUpload.getValues() : {}
      )
      await this.$api.put(`user/${this.user.id}/`, getAjaxFormData(data, [this.$refs.profileUpload.newProfilePictureKey]))
      await this.authStore.setUser(true)
      this.userData = this.getUserData()
      this.currentUserData = this.getUserData()
    },
    getUserData () {
      const userData = dataUtil.deepCopy(this.user)
      if (userData.home_location) {
        userData.home_location_text = locationUtil.getFullLocation(userData.home_location)
      }
      return userData
    },
    undoUserChanges () {
      this.userData = this.getUserData()
    }
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
      user
    }
  }
}
</script>

<style scoped>

</style>
