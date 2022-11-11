<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Candidate Dashboard"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12">
          <q-table
            title="Job applications"
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
            <template v-slot:body-cell-locations="props">
              <q-td key="locations" :props="props">
                <q-chip
                  v-for="loc in props.row.employer_job.locations"
                  dense color="grey-7" text-color="white" size="13px"
                >
                  {{ locationUtil.getFullLocation(loc) }}
                </q-chip>
                <span v-if="!props.row.employer_job.locations.length">
                  {{ globalStore.nullValueStr }}
                </span>
              </q-td>
            </template>
            <template v-slot:body-cell-jobStatus="props">
              <q-td key="jobStatus" :props="props">
                <q-chip
                  dense
                  :color="(props.row.employer_job.is_open) ? 'positive' : 'negative'"
                  :text-color="(props.row.employer_job.is_open) ? 'black' : 'white'"
                  size="13px"
                >
                  {{ (props.row.employer_job.is_open) ? 'Open' : 'Closed' }}
                </q-chip>
              </q-td>
            </template>
          </q-table>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import PageHeader from 'components/PageHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta } from 'quasar'
import dateTimeUtil from 'src/utils/datetime.js'
import locationUtil from 'src/utils/location.js'
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
  { name: 'locations', field: (app) => app.employer_job.locations, align: 'left', label: 'Locations' },
  { name: 'email', field: 'email', align: 'left', label: 'Email', sortable: true },
  {
    name: 'applicationDate',
    field: 'created_dt',
    align: 'center',
    label: 'Application date',
    format: dateTimeUtil.getShortDate.bind(dateTimeUtil),
    sortable: true
  },
  { name: 'jobStatus', field: (app) => app.employer_job.is_open, align: 'left', label: 'Job status', sortable: true }
]

export default {
  name: 'DashboardPage',
  components: { CustomTooltip, PageHeader },
  data () {
    return {
      applicationColumns,
      locationUtil
    }
  },
  computed: {
    applications () {
      return this.authStore.applications
    }
  },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        authStore.setApplications(authStore.propUser)
      ])
    }).finally(() => Loading.hide())
  },
  setup () {
    const authStore = useAuthStore()
    const globalStore = useGlobalStore()
    const { user } = storeToRefs(authStore)

    const pageTitle = 'Candidate Dashboard'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      authStore,
      globalStore,
      user
    }
  }
}
</script>
