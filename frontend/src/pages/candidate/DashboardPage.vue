<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Job Applications"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12">
          <q-table
            :loading="isLoading"
            :rows="applications"
            :columns="applicationColumns"
            :rows-per-page-options="[25,50,100]"
          >
            <template v-slot:header-cell-jobStatus="props">
              <q-th :props="props">
                {{ props.col.label }}
                <CustomTooltip icon_size="16px">
                  Whether the job is still open or has been filled/closed
                </CustomTooltip>
              </q-th>
            </template>
            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td
                  v-for="col in props.cols"
                  :key="col.name"
                  :props="props"
                >
                  <template v-if="col.name === 'employerName'">
                    <a :href="`/co/${props.row.employer_job.employer_key}`" target="_blank" :title="col.value">
                      {{ dataUtil.truncateText(col.value, 20, { isWholeWord: false }) }}
                    </a>
                  </template>
                  <template v-else-if="col.name === 'jobTitle'">
                    <a :href="`${props.row.employer_job.url}`" target="_blank" :title="col.value">
                      {{ dataUtil.truncateText(col.value, 30, { isWholeWord: false }) }}
                    </a>
                  </template>
                  <template v-else-if="col.name === 'applicationStatus'">
                    <DropdownApplicationStatus
                      :model-value="col.value"
                      @update:model-value="updateApplicationStatus(props.row.id, $event)"
                      :is-editable="props.row.is_external_application"
                      :is-employer="false"
                      style="width: 280px;"
                    />
                  </template>
                  <template v-else-if="col.name === 'locations'">
                    <LocationChip :locations="props.row.employer_job.locations"/>
                  </template>
                  <template v-else-if="col.name === 'jobStatus'">
                    <q-chip
                      dense
                      :color="(props.row.employer_job.is_open) ? 'positive' : 'negative'"
                      :text-color="(props.row.employer_job.is_open) ? 'black' : 'white'"
                      size="13px"
                    >
                      {{ (props.row.employer_job.is_open) ? 'Open' : 'Closed' }}
                    </q-chip>
                  </template>
                  <template v-else>
                    <span>{{ col.value }}</span>
                  </template>
                </q-td>
              </q-tr>
            </template>
          </q-table>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DropdownApplicationStatus from 'components/inputs/DropdownApplicationStatus.vue'
import LocationChip from 'components/LocationChip.vue'
import PageHeader from 'components/PageHeader.vue'
import { useMeta } from 'quasar'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import locationUtil from 'src/utils/location.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'

const applicationColumns = [
  {
    name: 'employerName',
    field: (app) => app.employer_job.employer_name,
    align: 'left',
    label: 'Company',
    sortable: true
  },
  { name: 'jobTitle', field: (app) => app.employer_job.title, align: 'left', label: 'Job title', sortable: true },
  {
    name: 'applicationStatus',
    field: (app) => app.application_status,
    align: 'left',
    label: 'Application status',
    sortable: true
  },
  { name: 'locations', field: (app) => app.employer_job.locations, align: 'left', label: 'Locations' },
  {
    name: 'applicationDate',
    field: 'created_dt',
    align: 'center',
    label: 'Application date',
    format: (val) => dateTimeUtil.getShortDate(val),
    sortable: true
  },
  { name: 'jobStatus', field: (app) => app.employer_job.is_open, align: 'left', label: 'Job status', sortable: true }
]

export default {
  name: 'DashboardPage',
  components: { DropdownApplicationStatus, LocationChip, CustomTooltip, PageHeader },
  data () {
    return {
      isLoading: false,
      applications: [],
      applicationColumns,
      dataUtil,
      locationUtil,
      authStore: useAuthStore(),
      user: null
    }
  },
  methods: {
    async updateData (isForceRefresh = true) {
      this.isLoading = true
      await this.authStore.setUserApplications(this.user, isForceRefresh)
      this.applications = this.authStore.applications
      this.isLoading = false
    },
    async updateApplicationStatus (applicationId, applicationStatus) {
      await this.$api.post('job-application/status/', getAjaxFormData({
        application_id: applicationId,
        application_status: applicationStatus
      }))
      await this.updateData()
    }
  },
  async mounted () {
    await this.authStore.setUser().then(() => {
      this.user = this.authStore.propUser
      return Promise.all([
        this.updateData(false)
      ])
    })
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Job Applications'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      globalStore
    }
  }
}
</script>
