<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Dashboard"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div v-if="defaultReferralLink" class="col-12">
          <BaseExpansionItem v-if="!hasCompletedChecklist" :is-include-separator="false">
            <template v-slot:header>
              <div class="text-h6">
                Get started
              </div>
            </template>
            <div class="q-mb-sm">
              <i>
                Referral bonuses can be worth thousands of dollars. Complete your profile setup in minutes.
              </i>
            </div>
            <q-list dense>
              <q-item class="bg-hover-gray-100">
                <q-item-section>
                  <div class="text-bold">
                    <q-icon v-if="userEmployeeChecklist.is_email_verified" name="check_circle" color="positive"/>
                    <q-icon v-else name="assignment" color="negative"/>
                    Validate your email address
                  </div>
                  <ul v-if="!userEmployeeChecklist.is_email_verified" class="q-mb-none">
                    <li>Go to your
                      <a href="#"
                         @click.prevent="$router.push({ name: 'profile', params: { key: 'profile' }, query: { tab: 'security' } })">
                        account page
                      </a>
                    </li>
                    <li>Click the "Send verification email" button for your primary email</li>
                    <li>
                      Open the email sent to your email address and click the button to "verify email".
                      If you don't see the email, check your junk mail folder.
                    </li>
                  </ul>
                </q-item-section>
              </q-item>
              <q-item v-if="!userEmployeeChecklist.is_email_employer_permitted" class="bg-hover-gray-100">
                <q-item-section>
                  <div class="text-bold">
                    <q-icon v-if="userEmployeeChecklist.has_secondary_email" name="check_circle" color="positive"/>
                    <q-icon v-else name="assignment" color="negative"/>
                    Add your business email address
                  </div>
                  <ul v-if="!userEmployeeChecklist.has_secondary_email" class="q-mb-none">
                    <li>Go to your
                      <a href="#"
                         @click.prevent="$router.push({ name: 'profile', params: { key: 'profile' } })">
                        account page
                      </a>
                    </li>
                    <li>Enter your business email</li>
                    <li>
                      Click the "Save" button.
                    </li>
                  </ul>
                </q-item-section>
              </q-item>
              <q-item v-if="userEmployeeChecklist.has_secondary_email" class="bg-hover-gray-100">
                <q-item-section>
                  <div class="text-bold">
                    <q-icon v-if="userEmployeeChecklist.is_business_email_verified" name="check_circle"
                            color="positive"/>
                    <q-icon v-else name="assignment" color="negative"/>
                    Validate your business email address
                  </div>
                  <ul v-if="!userEmployeeChecklist.is_business_email_verified" class="q-mb-none">
                    <li>Go to your
                      <a href="#"
                         @click.prevent="$router.push({ name: 'profile', params: { key: 'profile' }, query: { tab: 'security' } })">
                        account page
                      </a>
                    </li>
                    <li>Click the "Send verification email" button for your business email</li>
                    <li>
                      Open the email sent to your email address and click the button to "verify email".
                      If you don't see the email, check your junk mail folder.
                    </li>
                  </ul>
                </q-item-section>
              </q-item>
              <q-item class="bg-hover-gray-100">
                <q-item-section>
                  <div class="text-bold">
                    <q-icon name="assignment" color="grey-7"/>
                    Add your personal link to your LinkedIn profile
                  </div>
                  <ul class="q-mb-none">
                    <li>Click the LinkedIn image in the "Quick links" section below to copy your unique link</li>
                    <li>Navigate to your profile on <a href="https://www.linkedin.com" target="_blank">LinkedIn</a></li>
                    <li>Add your unique link in one or more of the following places:</li>
                    <ul>
                      <li>
                        Website link at the top of profile |
                        <a href="#" @click.prevent="openImageExplainer([
                          '/images/employee-get-started/websiteLink1.png',
                          '/images/employee-get-started/websiteLink2.png'
                        ])"
                        >
                          show how to
                        </a>
                      </li>
                      <li>
                        Link in Experience section |
                        <a href="#" @click.prevent="openImageExplainer([
                          '/images/employee-get-started/Experience1.png',
                          '/images/employee-get-started/Experience2.png',
                          '/images/employee-get-started/Experience3.png',
                          '/images/employee-get-started/Experience4.png',
                          '/images/employee-get-started/Experience5.png',
                          '/images/employee-get-started/Experience6.png'
                        ])"
                        >
                          show how to
                        </a>
                      </li>
                      <li>
                        Link in your Featured section |
                        <a href="#" @click.prevent="openImageExplainer([
                          '/images/employee-get-started/Featured1.png',
                          '/images/employee-get-started/Featured2.png',
                          '/images/employee-get-started/Featured3.png',
                          '/images/employee-get-started/Featured4.png'
                        ])"
                        >
                          show how to
                        </a>
                      </li>
                    </ul>
                  </ul>
                </q-item-section>
              </q-item>
              <q-item class="bg-hover-gray-100">
                <q-item-section>
                  <div class="text-bold">
                    <q-icon v-if="userEmployeeChecklist.has_connected_linkedin" name="check_circle" color="positive"/>
                    <q-icon v-else name="assignment" color="negative"/>
                    Connect your LinkedIn account
                  </div>
                  <ul v-if="!userEmployeeChecklist.has_connected_linkedin" class="q-mb-none">
                    <li>Go to your
                      <a href="#"
                         @click.prevent="$router.push({ name: 'employee-social-accounts', params: { key: 'employee-social-accounts' } })">
                        account page
                      </a>
                    </li>
                    <li>Click the "Connect LinkedIn" button</li>
                    <li>Follow the instructions from the LinkedIn page</li>
                  </ul>
                </q-item-section>
              </q-item>
              <q-item class="bg-hover-gray-100">
                <q-item-section>
                  <div class="text-bold">
                    <q-icon v-if="userEmployeeChecklist.has_scheduled_auto_post" name="check_circle" color="positive"/>
                    <q-icon v-else name="assignment" color="negative"/>
                    Send your first LinkedIn post and schedule auto-post
                  </div>
                  <ul v-if="!userEmployeeChecklist.has_scheduled_auto_post" class="q-mb-none">
                    <li>Go to your
                      <a href="#"
                         @click.prevent="$router.push({ name: 'employee-content', params: { key: 'employee-content' } })">
                        Posts and Content page
                      </a>
                    </li>
                    <li>Post using an employer template</li>
                    <ul>
                      <li>Click the "Employer Post Templates" tab to check if there are any post templates you can share</li>
                      <li>
                        If there is at least one template, click the
                        <q-icon name="share"/>
                        icon and complete the form. Make sure "auto-post" is turned on
                      </li>
                    </ul>
                    <li>Or create your own post</li>
                    <ul>
                      <li>Click the "Posts" tab</li>
                      <li>Click the "Create post" button and select "LinkedIn"</li>
                      <li>Complete the form and make sure "auto-post" is turned on</li>
                    </ul>
                  </ul>
                </q-item-section>
              </q-item>
              <q-item class="bg-hover-gray-100">
                <q-item-section>
                  <div class="text-bold">
                    <q-icon v-if="userEmployeeChecklist.has_updated_profile" name="check_circle" color="positive"/>
                    <q-icon v-else name="assignment" color="negative"/>
                    Update your profile
                  </div>
                  <ul v-if="!userEmployeeChecklist.has_updated_profile" class="q-mb-none">
                    <li>Go to your
                      <a href="#"
                         @click.prevent="$router.push({ name: 'employee-profile-page', params: { key: 'employee-profile-page' } })">
                        profile page
                      </a>
                    </li>
                    <li>Fill in the basic information</li>
                    <li>Answer at least one profile question</li>
                  </ul>
                </q-item-section>
              </q-item>
            </q-list>
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
import DialogImgCarousel from 'components/dialogs/DialogImgCarousel.vue'
import PageHeader from 'components/PageHeader.vue'
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
        socialStore.setPlatforms(),
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
    const { platforms } = storeToRefs(socialStore)
    const { userEmployeeChecklist } = storeToRefs(userStore)

    const pageTitle = 'Dashboard'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      socialStore,
      platforms,
      user,
      userEmployeeChecklist,
      userStore,
      q: useQuasar()
    }
  }
}
</script>
