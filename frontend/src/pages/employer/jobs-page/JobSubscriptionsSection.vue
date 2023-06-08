<template>
  <div v-if="isLoaded" class="row q-gutter-y-md" style="min-width: 500px;">
    <div class="col-12">
      <q-btn
        v-if="!isAddSubscription"
        label="Add job subscription" icon="add" color="primary"
        @click="isAddSubscription = true"
      />
    </div>
    <div v-if="isAddSubscription" class="col-12">
      <CollapsableCard title="Job subscription" :can-collapse="false">
        <template v-slot:header>
          <q-btn
            flat unelevated ripple
            icon="close" text-color="grey-5" class="q-pr-sm"
            @click="isAddSubscription = false"
          />
        </template>
        <template v-slot:body>
          <div class="col-12">
            <q-input
              v-model="subscriptionFilter.title"
              filled label="Subscription title"
            >
              <template v-slot:after>
                <CustomTooltip>
                  Used to summarize what this job subscription is for (e.g. "Remote Product Managers")
                </CustomTooltip>
              </template>
            </q-input>
          </div>
          <div class="col-md-6 col-12 q-pr-md-sm">
            <q-input
              v-model="subscriptionFilter.job_title_regex"
              filled label="Include job titles"
            >
              <template v-slot:after>
                <CustomTooltip>
                  Use partial or full job titles. You can include multiple titles using a "|" separator
                </CustomTooltip>
              </template>
            </q-input>
          </div>
          <div class="col-md-6 col-12 q-pl-md-sm">
            <q-input
              v-model="subscriptionFilter.exclude_job_title_regex"
              filled label="Exclude job titles"
            >
              <template v-slot:after>
                <CustomTooltip>
                  Use partial or full job titles. You can include multiple titles using a "|" separator
                </CustomTooltip>
              </template>
            </q-input>
          </div>
          <div class="col-12 q-pr-md-sm">
            <InputLocation
              v-model:location="subscriptionFilter.locations"
              v-model:range_miles="subscriptionFilter.range_miles"
              :is-include-range="true" :is-multi="true"
            />
          </div>
          <div class="col-md-4 col-12 q-pr-md-sm">
            <SelectRemote v-model="subscriptionFilter.remote_type_bit"/>
          </div>
          <div class="col-md-8 col-12 q-pl-md-sm">
            <SelectEmployer v-model="subscriptionFilter.employers" :is-multi="true"/>
          </div>
          <div class="col-12">
            <q-btn label="Save job subscription" color="primary" class="w-100" @click="saveJobSubscription"/>
          </div>
        </template>
      </CollapsableCard>
    </div>
    <div class="col-12">
      <q-table
        :rows="jobSubscriptions"
        :columns="jobSubscriptionColumns"
      >
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th auto-width class="text-left">
              Actions
            </q-th>
            <q-th
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
            >
              <span>{{ col.label }}</span>
            </q-th>
          </q-tr>
        </template>

        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td auto-width>
              <template v-if="!props.row.is_single_employer">
                <q-btn
                  outline round dense icon="edit" color="primary"
                  class="q-mr-xs"
                  @click="openEditJobSubscription(props.row)"
                />
                <q-btn
                  outline round dense icon="delete" color="negative"
                  class="q-mr-xs"
                  @click="deleteJobSubscription(props.row)"
                />
              </template>
              <CustomTooltip v-else :is_include_icon="false">
                <template v-slot:content>
                  <q-chip icon="lock">Employee referral</q-chip>
                </template>
                This is your employer's jobs. You may be eligible for a referral bonus by posting these jobs.
              </CustomTooltip>
            </q-td>
            <q-td
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
            >
              <template v-if="col.name === 'filters'">
                <JobSubscriptionInfo :job-subscription="props.row"/>
              </template>
              <template v-else-if="col.name === 'job_count'">
                {{ col.value }}
              </template>
              <span v-else>{{ col.value }}</span>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script>
import CollapsableCard from 'components/CollapsableCard.vue'
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogJobSubscription from 'components/dialogs/DialogJobSubscription.vue'
import InputLocation from 'components/inputs/InputLocation.vue'
import JobSubscriptionInfo from 'pages/employer/jobs-page/JobSubscriptionInfo.vue'
import { useQuasar } from 'quasar'
import locationUtil from 'src/utils/location.js'
import SelectEmployer from 'components/inputs/SelectEmployer.vue'
import SelectRemote from 'components/inputs/SelectRemote.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useJobSubscriptionStore } from 'stores/job-subscription-store.js'

const subscriptionFilterTemplate = {
  job_title_regex: null,
  exclude_job_title_regex: null,
  locations: null,
  range_miles: 25,
  jobs: [],
  employers: [],
  remote_type_bit: null
}

const jobSubscriptionColumns = [
  { name: 'title', field: 'title', align: 'left', label: 'Title', sortable: true },
  { name: 'filters', field: 'filters', align: 'left', label: 'Filters' },
  { name: 'job_count', field: 'job_count', align: 'left', label: 'Job count', sortable: true }
]

export default {
  name: 'JobSubscriptionsSection',
  components: {
    InputLocation,
    CustomTooltip,
    JobSubscriptionInfo,
    SelectRemote,
    SelectEmployer,
    CollapsableCard
  },
  props: {
    isEmployer: Boolean
  },
  data () {
    return {
      isLoaded: false,
      isAddSubscription: false,
      subscriptionFilter: { ...subscriptionFilterTemplate },
      jobSubscriptions: [],
      jobSubscriptionColumns,
      locationUtil
    }
  },
  methods: {
    async updateJobSubscriptions (isForceRefresh) {
      const params = (this.isEmployer) ? { employerId: this.user.employer_id } : { userId: this.user.id }
      await this.jobSubscriptionStore.setJobSubscription({ ...params, isForceRefresh })
      this.jobSubscriptions = this.jobSubscriptionStore.getJobSubscription(params)
    },
    openEditJobSubscription (jobSubscription) {
      return this.q.dialog({
        component: DialogJobSubscription,
        componentProps: { jobSubscription }
      }).onOk(async () => {
        await this.updateJobSubscriptions(true)
      })
    },
    async deleteJobSubscription (jobSubscription) {
      openConfirmDialog(
        this.q,
        'Are you sure you want to delete this job subscription?',
        {
          okFn: async () => {
            await this.$api.delete(`job-subscription/${jobSubscription.id}`)
            await this.updateJobSubscriptions(true)
          }
        }
      )
    },
    async saveJobSubscription () {
      await this.$api.post('job-subscription/', getAjaxFormData({
        employer_id: this.user.employer_id,
        user_id: this.user.id,
        ...this.subscriptionFilter
      }))
      this.subscriptionFilter = { ...subscriptionFilterTemplate }
      await this.updateJobSubscriptions(true)
    }
  },
  async mounted () {
    await this.updateJobSubscriptions(false)
    this.isLoaded = true
  },
  setup () {
    const jobSubscriptionStore = useJobSubscriptionStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)

    return { jobSubscriptionStore, authStore, user, q: useQuasar() }
  }
}
</script>
