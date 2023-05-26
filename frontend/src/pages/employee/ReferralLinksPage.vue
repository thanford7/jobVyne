<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Referral links">
        Add one or more referral links to your social media accounts. Anyone that visits your page can click on the
        link
        and will be directed to a webpage with all open jobs at your company. If they apply and work at your company,
        you can collect a referral bonus!
      </PageHeader>
      <div>
        <div class="row">
          <div class="col-12 q-mt-sm q-py-md">
            <q-btn ripple color="primary" label="Create link" @click="openJobLinkDialog"/>
          </div>
          <div v-if="!socialLinkFilters.length" class="col-12">
            No referral links. Create your first link.
          </div>
          <div
            v-for="socialLinkFilter in socialLinkFilters"
            class="col-12 col-md-4 q-pa-sm"
          >
            <q-card class="h-100" style="position: relative">
              <CustomTooltip
                v-if="socialLinkFilter.is_default"
                :is_include_icon="false"
                style="position: absolute; top: 0; left: 0; transform: translateX(-5%) translateY(-60%);"
              >
                <template v-slot:content>
                  <q-chip
                    v-if="socialLinkFilter.is_default"
                    square dense color="secondary" text-color="white"
                  >
                    <q-icon name="star"/>&nbsp;
                    Default
                  </q-chip>
                </template>
                The default referral link will be used to auto-populate links for posts you create.
              </CustomTooltip>
              <div class="row q-pt-sm q-px-xs border-bottom-1-gray-100">
                <template v-if="hasSocialLinkJobs(socialLinkFilter)">
                  <q-chip
                    v-if="socialLinkFilter.jobs.length === 1"
                    color="lime-9" text-color="white" dense size="13px"
                  >
                    {{ socialLinkFilter.jobs[0].title }}
                  </q-chip>
                  <CustomTooltip v-else>
                    <template v-slot:content>Multiple jobs</template>
                    <ul>
                      <li v-for="job in socialLinkFilter.jobs">{{ job.title }}</li>
                    </ul>
                  </CustomTooltip>
                </template>
                <q-space/>
                <q-chip
                  dense clickable
                  @click="utilStore.redirectUrl(socialUtil.getJobLinkUrl(socialLinkFilter), true)"
                  icon-right="launch"
                  size="13px"
                >
                  <q-avatar color="primary" text-color="white" size="20px">{{
                      socialLinkFilter.jobs_count
                    }}
                  </q-avatar>
                  &nbsp;View jobs
                </q-chip>
              </div>
              <div class="q-px-md q-pb-sm">
                <div>
                  <div class="q-mb-sm">
                    <span class="text-bold">Social Links</span> <span class="text-small">(Click to copy)</span>
                  </div>
                  <ReferralLinkButtons :social-link-filter="socialLinkFilter"/>
                </div>
                <div class="q-mt-sm">
                  <div class="text-bold">Performance</div>
                  <div class="q-mx-sm q-my-xs" style="display: inline-block;">
                    <div>{{ socialLinkFilter.performance.views.total }}</div>
                    <div class="text-small">Total views</div>
                  </div>
                  <div class="q-mx-sm q-my-xs" style="display: inline-block;">
                    <div>{{ socialLinkFilter.performance.views.unique }}</div>
                    <div class="text-small">Unique views</div>
                  </div>
                  <div class="q-mx-sm q-my-xs" style="display: inline-block;">
                    <div>
                      <span v-if="socialLinkFilter.performance.applications.length">
                        <a href="#" @click.prevent="openDataDialog(socialLinkFilter)">
                          {{ socialLinkFilter.performance.applications.length }}
                        </a>
                      </span>
                      <span v-else>
                        {{ socialLinkFilter.performance.applications.length }}
                      </span>
                    </div>
                    <div class="text-small">Applications</div>
                  </div>
                </div>
              </div>
              <q-card-actions class="border-top-1-gray-100">
                <q-btn
                  v-if="!socialLinkFilter.is_default"
                  icon="star" label="Set default" dense ripple color="grey-6"
                  @click="setDefaultLink(socialLinkFilter)"
                />
              </q-card-actions>
            </q-card>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import DialogJobLink from 'components/dialogs/DialogJobLink.vue'
import DialogShowDataTable from 'components/dialogs/DialogShowDataTable.vue'
import ReferralLinkButtons from 'components/ReferralLinkButtons.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import jobsUtil from 'src/utils/jobs.js'
import locationUtil from 'src/utils/location.js'
import { getAjaxFormData } from 'src/utils/requests'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store'
import { useEmployerStore } from 'stores/employer-store'
import { useSocialStore } from 'stores/social-store'
import { useUtilStore } from 'stores/utility-store'
import dataUtil from 'src/utils/data'
import dateTimeUtil from 'src/utils/datetime'
import CustomTooltip from 'components/CustomTooltip.vue'
import { useGlobalStore } from 'stores/global-store'
import { Loading, useMeta, useQuasar } from 'quasar'
import PageHeader from 'components/PageHeader.vue'

const jobColumns = [
  { name: 'job_title', field: 'job_title', align: 'left', label: 'Title', sortable: true },
  { name: 'job_department', field: 'job_department', align: 'left', label: 'Department', sortable: true },
  { name: 'locations', field: 'locations', align: 'left', label: 'Location' },
  {
    name: 'open_date',
    field: 'open_date',
    align: 'left',
    label: 'Posted Date',
    sortable: true,
    format: (val) => dateTimeUtil.getShortDate(val)
  },
  {
    name: 'bonus',
    field: row => row.bonus.amount,
    label: 'Referral Bonus',
    sortable: true,
    sort: (a, b) => parseInt(a) - parseInt(b),
    format: dataUtil.formatCurrency
  }
]

const formDataTemplate = {
  departments: null,
  cities: null,
  states: null,
  countries: null
}

export default {
  components: {
    ReferralLinkButtons,
    PageHeader,
    CustomTooltip
  },
  data () {
    return {
      formData: { ...formDataTemplate },
      linkId: null,
      selectedLinkId: null, // Used to drill into application details
      tab: 'current',
      jobColumns,
      dataUtil,
      socialUtil
    }
  },
  methods: {
    getFullLocation: locationUtil.getFullLocation,
    getLocations: locationUtil.getFormattedLocations.bind(locationUtil),
    hasSocialLinkJobs (socialLinkFilter) {
      return socialLinkFilter.jobs && socialLinkFilter.jobs.length
    },
    openDataDialog (socialLinkFilter) {
      return this.q.dialog({
        component: DialogShowDataTable,
        componentProps: { data: socialLinkFilter.performance.applications, ignoreColumns: ['id'] }
      })
    },
    openJobLinkDialog () {
      return this.q.dialog({
        component: DialogJobLink,
        componentProps: { employerId: this.user.employer_id }
      })
    },
    jobDataFilter (rows) {
      return jobsUtil.filterJobs(this.formData, rows)
    },
    async setDefaultLink (jobLink) {
      await this.$api.put('social-link-filter/', getAjaxFormData({
        link_filter_id: jobLink.id,
        is_default: true
      }))
      await this.socialStore.setSocialLinkFilters(this.user.id, true)
    }
  },
  preFetch () {
    const socialStore = useSocialStore()
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        socialStore.setSocialLinkFilters(authStore.propUser.id),
        employerStore.setEmployer(authStore.propUser.employer_id),
        employerStore.setEmployerJobs(authStore.propUser.employer_id)
      ])
    }).finally(() => Loading.hide())
  },
  setup () {
    const socialStore = useSocialStore()
    const employerStore = useEmployerStore()
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const utilStore = useUtilStore()
    const { user } = storeToRefs(authStore)
    const { socialLinkFilters } = storeToRefs(socialStore)

    const pageTitle = 'Referral Links'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      socialStore,
      employerStore,
      authStore,
      globalStore,
      utilStore,
      socialLinkFilters,
      user,
      q: useQuasar()
    }
  }
}
</script>

<style lang="scss" scoped>
.row {
  margin-bottom: 8px;
}

.col-12 {
  margin-bottom: 8px;
}
</style>
