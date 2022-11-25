<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Dashboard"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div v-if="defaultReferralLink" class="col-12">
          <BaseExpansionItem :is-include-separator="false">
            <template v-slot:header>
              <div class="text-h6">
                Get started
              </div>
            </template>
            <q-card>
              <q-card-section>
                <div>
                  <q-icon name="check_circle" color="positive"/>
                  Validate email address
                </div>
                <div>Add your personal link to your LinkedIn profile</div>
                <div>Connect your LinkedIn account</div>
                <div>Update your profile</div>
              </q-card-section>
            </q-card>
          </BaseExpansionItem>
          <BaseExpansionItem :is-include-separator="false">
            <template v-slot:header>
              <div class="text-h6">
                Quick links for
                <CustomTooltip :is_include_icon="false" color_class="bg-white">
                  <template v-slot:content>
                    <span style="text-decoration: underline">default referral</span>
                  </template>
                  <div class="border-bottom-1-gray-300 text-bold text-primary q-mb-sm">
                    {{ dataUtil.pluralize('Open job', defaultReferralLink.jobs_count) }}
                  </div>
                  <div>
                    <q-chip
                      v-for="dept in defaultReferralLink.departments"
                      dense color="blue-grey-7" text-color="white" size="13px"
                    >
                      {{ dept.name }}
                    </q-chip>
                    <q-chip v-if="!defaultReferralLink.departments.length" dense size="13px">
                      Any department
                    </q-chip>
                    <q-chip
                      v-for="loc in locationUtil.getFormattedLocations(defaultReferralLink)"
                      dense :color="loc.color" text-color="white" size="13px"
                    >
                      {{ loc.name }}
                    </q-chip>
                    <q-chip v-if="!locationUtil.getFormattedLocations(defaultReferralLink).length" dense size="13px">
                      Any location
                    </q-chip>
                  </div>
                </CustomTooltip>
              </div>
            </template>
            <div>
              <div class="text-small q-mb-sm">Click icon to copy link</div>
              <div v-for="socialLink in socialUtil.getSocialLinks(platforms, defaultReferralLink)"
                   style="display: inline-block">
                <q-chip clickable @click="dataUtil.copyText" size="16px">
                  <div class="flex items-center">
                    <img :src="socialLink.logo" :alt="socialLink.name" style="height: 20px;">
                    <span class="copy-target" style="display: none;">{{ socialLink.socialLink }}</span>
                  </div>
                </q-chip>
              </div>
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
import CustomTooltip from 'components/CustomTooltip.vue'
import PageHeader from 'components/PageHeader.vue'
import EmployeeLeaderBoard from 'pages/employer/dashboard-page/EmployeeLeaderBoard.vue'
import LinkPerformanceChart from 'pages/employer/dashboard-page/LinkPerformanceChart.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta } from 'quasar'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil, { GROUPINGS } from 'src/utils/datetime.js'
import locationUtil from 'src/utils/location.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'DashboardPage',
  components: { BaseExpansionItem, CustomTooltip, LinkPerformanceChart, EmployeeLeaderBoard, PageHeader },
  data () {
    return {
      GROUPINGS,
      dateRange: {
        from: dateTimeUtil.getStartOfMonthDate(new Date(), { monthOffset: -2 }),
        to: new Date()
      },
      dataUtil,
      locationUtil,
      socialUtil
    }
  },
  computed: {
    defaultReferralLink () {
      const referralLinks = this.socialStore.getSocialLinkFilters(this.user.id)
      return referralLinks.find((link) => link.is_default)
    }
  },
  preFetch () {
    const authStore = useAuthStore()
    const socialStore = useSocialStore()

    Loading.show()
    return authStore.setUser().then(() => {
      return Promise.all([
        socialStore.setPlatforms(),
        socialStore.setSocialLinkFilters(authStore.propUser.id)
      ])
    }).finally(() => Loading.hide())
  },
  setup () {
    const authStore = useAuthStore()
    const globalStore = useGlobalStore()
    const socialStore = useSocialStore()
    const { user } = storeToRefs(authStore)
    const { platforms } = storeToRefs(socialStore)

    const pageTitle = 'Dashboard'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      socialStore,
      platforms,
      user
    }
  }
}
</script>
