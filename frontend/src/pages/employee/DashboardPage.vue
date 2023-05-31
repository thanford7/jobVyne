<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Dashboard"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div v-if="defaultReferralLink" class="col-12">
          <BaseExpansionItem :is-include-separator="false">
            <template v-slot:header>
              <div class="text-h6">
                Quick referral links
              </div>
            </template>
            <div>
              <div class="text-small q-mb-sm">Click icon to copy link</div>
              <ReferralLinkButtons :social-link-filter="defaultReferralLink"/>
            </div>
          </BaseExpansionItem>
        </div>
        <div class="col-12">
          <BaseExpansionItem :is-include-separator="false">
            <template v-slot:header>
              <div class="text-h6">
                Performance
              </div>
            </template>
            <div class="row">
              <div class="col-12 col-md-6 col-lg-4 q-pa-sm">
                <LinkPerformanceChart
                  :is-employer="false"
                  :default-date-group="GROUPINGS.MONTH.key"
                  :default-date-range="dateRange"
                />
              </div>
              <div class="col-12 col-md-6 col-lg-4 q-pa-sm">
                <EmployeeLeaderBoard :is-employer="false"/>
              </div>
            </div>
          </BaseExpansionItem>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import BaseExpansionItem from 'components/BaseExpansionItem.vue'
import DialogImgCarousel from 'components/dialogs/DialogImgCarousel.vue'
import PageHeader from 'components/PageHeader.vue'
import ReferralLinkButtons from 'components/ReferralLinkButtons.vue'
import EmployeeLeaderBoard from 'pages/employer/dashboard-page/EmployeeLeaderBoard.vue'
import LinkPerformanceChart from 'pages/employer/dashboard-page/LinkPerformanceChart.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil, { GROUPINGS } from 'src/utils/datetime.js'
import locationUtil from 'src/utils/location.js'
import { getAssetsPath } from 'src/utils/requests.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useSocialStore } from 'stores/social-store.js'
import { useUserStore } from 'stores/user-store.js'

export default {
  name: 'DashboardPage',
  components: { ReferralLinkButtons, BaseExpansionItem, LinkPerformanceChart, EmployeeLeaderBoard, PageHeader },
  data () {
    return {
      GROUPINGS,
      dateRange: {
        from: dateTimeUtil.getStartOfMonthDate(new Date(), { monthOffset: -2 }),
        to: new Date()
      },
      dataUtil,
      locationUtil,
      socialUtil,
      getAssetsPath
    }
  },
  computed: {
    defaultReferralLink () {
      const referralLinks = this.socialStore.getSocialLinkFilters(this.user.id)
      return referralLinks.find((link) => link.is_default)
    },
    hasCompletedChecklist () {
      return [
        this.userEmployeeChecklist.is_email_verified,
        this.userEmployeeChecklist.is_email_employer_permitted || this.userEmployeeChecklist.has_secondary_email,
        !this.userEmployeeChecklist.has_secondary_email || this.userEmployeeChecklist.is_business_email_verified,
        this.userEmployeeChecklist.has_updated_profile,
        this.userEmployeeChecklist.has_connected_linkedin,
        this.userEmployeeChecklist.has_scheduled_auto_post
      ].every((val) => val)
    }
  },
  watch: {
    user: {
      async handler () {
        await this.userStore.setUserEmployeeChecklist(this.user.id)
      },
      deep: true
    }
  },
  methods: {
    openImageExplainer (imageSrcs) {
      this.q.dialog({
        component: DialogImgCarousel,
        componentProps: {
          title: 'Instructions',
          imageSrcs
        }
      })
    }
  },
  preFetch () {
    const authStore = useAuthStore()
    const socialStore = useSocialStore()
    const userStore = useUserStore()

    Loading.show()
    return authStore.setUser().then(() => {
      return Promise.all([
        socialStore.setSocialLinkFilters(authStore.propUser.id),
        userStore.setUserEmployeeChecklist(authStore.propUser.id)
      ])
    }).finally(() => Loading.hide())
  },
  setup () {
    const authStore = useAuthStore()
    const globalStore = useGlobalStore()
    const socialStore = useSocialStore()
    const userStore = useUserStore()
    const { user } = storeToRefs(authStore)
    const { userEmployeeChecklist } = storeToRefs(userStore)

    const pageTitle = 'Dashboard'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      socialStore,
      user,
      userEmployeeChecklist,
      userStore,
      q: useQuasar()
    }
  }
}
</script>
