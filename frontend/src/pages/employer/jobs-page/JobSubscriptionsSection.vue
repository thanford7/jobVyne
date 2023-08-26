<template>
  <div v-if="isLoaded" class="row q-gutter-y-md" style="min-width: 500px;">
    <div class="col-12">
      <q-table
        :rows="jobSubscriptions"
        :columns="jobSubscriptionColumns"
      >
        <template v-slot:top>
          <q-btn
            label="Add job subscription" icon="add" color="primary"
            @click="openEditJobSubscription()"
          />
        </template>
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
              <template v-if="!props.row.is_single_employer || userTypeUtil.isAdmin(user.user_type_bits)">
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
              <CustomTooltip v-if="props.row.is_single_employer" :is_include_icon="false">
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
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogJobSubscription from 'components/dialogs/DialogJobSubscription.vue'
import JobSubscriptionInfo from 'pages/employer/jobs-page/JobSubscriptionInfo.vue'
import { useQuasar } from 'quasar'
import locationUtil from 'src/utils/location.js'
import { storeToRefs } from 'pinia/dist/pinia'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import userTypeUtil from 'src/utils/user-types.js'
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
    CustomTooltip,
    JobSubscriptionInfo
  },
  props: {
    isEmployer: Boolean
  },
  data () {
    return {
      isLoaded: false,
      subscriptionFilter: { ...subscriptionFilterTemplate },
      jobSubscriptions: [],
      jobSubscriptionColumns,
      locationUtil,
      userTypeUtil
    }
  },
  methods: {
    getEditParams () {
      return (this.isEmployer) ? { employerId: this.user.employer_id } : { userId: this.user.id }
    },
    async updateJobSubscriptions (isForceRefresh) {
      const params = this.getEditParams()
      await this.jobSubscriptionStore.setJobSubscription({ ...params, isForceRefresh })
      this.jobSubscriptions = this.jobSubscriptionStore.getJobSubscription(params)
    },
    openEditJobSubscription (jobSubscription) {
      return this.q.dialog({
        component: DialogJobSubscription,
        componentProps: { ...this.getEditParams(), jobSubscription }
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
        employer_id: (this.isEmployer) ? this.user.employer_id : null,
        user_id: (this.isEmployer) ? null : this.user.id,
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
