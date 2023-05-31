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
            <q-th auto-width>
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
            </q-td>
            <q-td
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
            >
              <template v-if="col.name === 'filters'">
                <q-chip
                  v-if="props.row.filters.job_title_regex"
                  dense size="13px"
                >
                  <b>Include: </b>&nbsp;{{ props.row.filters.job_title_regex }}
                </q-chip>
                <q-chip
                  v-if="props.row.filters.exclude_job_title_regex"
                  dense size="13px"
                >
                  <b>Exclude: </b>&nbsp;{{ props.row.filters.exclude_job_title_regex }}
                </q-chip>
                <LocationChip :locations="props.row.filters.locations" :is-dense="true"/>
                <template v-if="props.row.filters.jobs?.length && props.row.filters.jobs?.length > 2">
                  <CustomTooltip :is_include_icon="false">
                    <template v-slot:content>
                      <q-chip dense color="grey-8" text-color="white" size="13px">
                        Multiple jobs
                      </q-chip>
                    </template>
                    <ul>
                      <li v-for="job in props.row.filters.jobs">
                        {{ job.title }}
                      </li>
                    </ul>
                  </CustomTooltip>
                </template>
                <template v-else>
                  <q-chip
                    v-for="job in props.row.filters.jobs"
                    dense color="grey-8" text-color="white" size="13px"
                  >
                    {{ job.title }}
                  </q-chip>
                </template>
                <template v-if="props.row.filters.employers?.length && props.row.filters.employers?.length > 2">
                  <CustomTooltip :is_include_icon="false">
                    <template v-slot:content>
                      <q-chip dense color="grey-8" text-color="white" size="13px">
                        Multiple employers
                      </q-chip>
                    </template>
                    <ul>
                      <li v-for="employer in props.row.filters.employers">
                        {{ employer.name }}
                      </li>
                    </ul>
                  </CustomTooltip>
                </template>
                <template v-else>
                  <q-chip
                    v-for="employer in props.row.filters.employers"
                    dense color="grey-8" text-color="white" size="13px"
                  >
                    {{ employer.name }}
                  </q-chip>
                </template>
                <template v-if="props.row.filters.remote_type_bit">
                  <q-chip
                    v-if="props.row.filters.remote_type_bit === locationUtil.REMOTE_TYPE_TRUE"
                    dense color="grey-8" text-color="white" size="13px"
                  >
                    Remote only
                  </q-chip>
                  <q-chip
                    v-else
                    dense color="grey-8" text-color="white" size="13px"
                  >
                    On-site only
                  </q-chip>
                </template>
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
import LocationChip from 'components/LocationChip.vue'
import { useQuasar } from 'quasar'
import locationUtil from 'src/utils/location.js'
import SelectEmployer from 'components/inputs/SelectEmployer.vue'
import SelectRemote from 'components/inputs/SelectRemote.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

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
  { name: 'filters', field: 'filters', align: 'left', label: 'Filters' },
  { name: 'job_count', field: 'job_count', align: 'left', label: 'Job count', sortable: true }
]

export default {
  name: 'JobSubscriptionsSection',
  components: {
    LocationChip,
    InputLocation,
    CustomTooltip,
    SelectRemote,
    SelectEmployer,
    CollapsableCard
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
    async updateJobSubscriptions (isForce) {
      await this.employerStore.setEmployerJobSubscription(this.user.employer_id, isForce)
      this.jobSubscriptions = this.employerStore.getEmployerJobSubscription(this.user.employer_id)
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
            await this.$api.delete(`employer/job-subscription/${jobSubscription.id}`)
            await this.updateJobSubscriptions(true)
          }
        }
      )
    },
    async saveJobSubscription () {
      await this.$api.post('employer/job-subscription/', getAjaxFormData({
        employer_id: this.user.employer_id,
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
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)

    return { employerStore, authStore, user, q: useQuasar() }
  }
}
</script>
