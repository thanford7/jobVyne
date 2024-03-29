<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Job Scrapers"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12">
          <q-table
            :rows="jobScrapers"
            :columns="scraperColumns"
            row-key="employer_name"
            selection="multiple"
            v-model:selected="selectedScrapers"
            :rows-per-page-options="[15, 25, 50]"
          >
            <template v-slot:top>
              <q-btn
                class="q-mr-sm"
                ripple color="primary" label="Run all" @click="runJobScrapers({ isAll: true })"
              />
              <q-btn
                class="q-mr-sm"
                ripple color="primary" label="Run Workable" @click="runJobScrapers({ isWorkable: true })"
              />
              <q-btn
                v-if="selectedScrapers.length"
                class="q-mr-sm"
                ripple color="primary" :label="`Run selected (${selectedScrapers.length})`" @click="runJobScrapers({ isAll: false })"
              />
            </template>
          </q-table>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta } from 'quasar'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAdminStore } from 'stores/admin-store.js'
import { useGlobalStore } from 'stores/global-store.js'

const scraperColumns = [
  { name: 'employerName', field: 'employer_name', align: 'left', label: 'Name', sortable: true },
  { name: 'ats', field: 'ats', align: 'left', label: 'ATS', sortable: true, format: (val) => val || 'Unknown' },
  {
    name: 'scrapeDate',
    field: 'last_job_scrape_success_dt',
    align: 'left',
    label: 'Last Success Date',
    sortable: true,
    sort: dateTimeUtil.sortDatesFn.bind(dateTimeUtil),
    format: (val) => dateTimeUtil.getDateTime(val)
  },
  { name: 'hasScrapeFailure', field: 'has_job_scrape_failure', align: 'left', label: 'Is Failing', sortable: true, format: (val) => dataUtil.capitalize(String(val)) }
]

export default {
  name: 'EmployersPage',
  components: { PageHeader },
  data () {
    return {
      scraperColumns,
      selectedScrapers: [],
      dataUtil
    }
  },
  methods: {
    async runJobScrapers ({ isAll = false, isWorkable = false }) {
      await this.$api.post('admin/job-scraper/', getAjaxFormData({
        is_run_all: isAll,
        is_run_workable: isWorkable,
        employer_names: this.selectedScrapers.map((employerScraper) => employerScraper.employer_name)
      }))
      await this.adminStore.setJobScrapers(true)
      this.selectedScrapers = []
    }
  },
  preFetch () {
    const adminStore = useAdminStore()
    Loading.show()

    return adminStore.setJobScrapers().finally(() => Loading.hide())
  },
  setup () {
    const globalStore = useGlobalStore()
    const adminStore = useAdminStore()
    const { jobScrapers } = storeToRefs(adminStore)

    const pageTitle = 'Admin Job Scraper Page'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      adminStore,
      jobScrapers
    }
  }
}
</script>
