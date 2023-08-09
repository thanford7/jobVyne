<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Employers"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12">
          <q-table
            :loading="isLoading"
            :rows="employers"
            :columns="employerColumns"
            row-key="id"
            v-model:pagination="pagination"
            :filter="employerFilter"
            @request="updatePagination"
            :rows-per-page-options="[20]"
          >
            <template v-slot:top>
              <q-btn
                ripple color="primary" label="Create new employer"
                class="q-mr-sm" debounce="800"
                @click="openDialogAdminEmployer()"
              />
              <q-input
                v-model="employerFilter.employer_name_text"
                filled label="Employer search"
              />
            </template>
            <template v-slot:header="props">
              <q-tr :props="props">
                <q-th auto-width/>
                <q-th
                  v-for="col in props.cols"
                  :key="col.name"
                  :props="props"
                >
                  {{ col.label }}
                </q-th>
              </q-tr>
            </template>
            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td auto-width>
                  <q-btn
                    class="q-mr-sm"
                    size="sm" color="gray-500" round dense icon="edit"
                    @click="openDialogAdminEmployer(props.row)"
                  />
                  <q-btn
                    size="sm" color="negative" round dense icon="delete"
                    @click="deleteEmployer(props.row)"
                  />
                </q-td>
                <q-td
                  v-for="col in props.cols"
                  :key="col.name"
                  :props="props"
                >
                  <template v-if="col.name === 'employerName'">
                    <q-img
                      :src="props.row.logo_url" class="q-mr-sm"
                      alt="Employer logo" height="30px" width="30px" style="display: inline-block"
                    />
                    <a :href="props.row.job_board_url" target="_blank">{{ props.row.name }}</a>
                  </template>
                  <template v-else-if="col.name === 'subscriptionStatus'">
                    <q-chip
                      dense
                      :label="(props.row.subscription_status) ? dataUtil.capitalize(props.row.subscription_status) : 'No subscription'"
                      :color="(props.row.subscription_status === SUBSCRIPTION_STATUS.ACTIVE) ? 'positive' : 'negative'"
                    />
                  </template>
                  <span v-else>{{ col.value }}</span>
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
import DialogAdminEmployer from 'components/dialogs/DialogAdminEmployer.vue'
import PageHeader from 'components/PageHeader.vue'
import { Loading, useMeta, useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import { openConfirmDialog } from 'src/utils/requests.js'
import { SUBSCRIPTION_STATUS } from 'src/utils/subscription.js'
import { useAdminStore } from 'stores/admin-store.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'

const employerColumns = [
  { name: 'employerName', field: 'name', align: 'left', label: 'Name', sortable: true },
  {
    name: 'joinedDate',
    field: 'joined_date',
    align: 'left',
    label: 'Joined Date',
    sortable: true,
    sort: dateTimeUtil.sortDatesFn.bind(dateTimeUtil),
    format: (val) => dateTimeUtil.getShortDate(val)
  },
  {
    name: 'useJobUrl',
    field: 'is_use_job_url',
    align: 'left',
    label: 'Use Job URL',
    sortable: true,
    format: (val) => dataUtil.capitalize(val.toString())
  },
  { name: 'employeeSeats', field: 'employee_seats', align: 'center', label: 'Employee Seats', sortable: true },
  { name: 'employeeCount', field: 'employee_count', align: 'center', label: 'Employee Count', sortable: true },
  { name: 'subscriptionStatus', field: 'subscription_status', align: 'left', label: 'Account Status', sortable: true },
  {
    name: 'accountOwnerName',
    field: (employer) => dataUtil.getFullName(employer.owner_first_name, employer.owner_last_name),
    align: 'left',
    label: 'Account Owner Name',
    sortable: true
  },
  {
    name: 'accountOwnerEmail',
    field: 'owner_email',
    align: 'left',
    label: 'Account Owner Email',
    sortable: true
  }
]

const employerFilterTemplate = {
  employer_name_text: null
}

export default {
  name: 'EmployersPage',
  components: { PageHeader },
  data () {
    return {
      isLoading: true,
      employers: [],
      pagination: {
        sortBy: 'none',
        descending: true,
        page: 1,
        rowsPerPage: 20,
        rowsNumber: null,
        totalPageCount: 1
      },
      employerFilter: { ...employerFilterTemplate },
      employerColumns,
      dataUtil,
      SUBSCRIPTION_STATUS,
      adminStore: useAdminStore(),
      q: useQuasar()
    }
  },
  watch: {
    employerFilter: {
      handler () {
        // This will cause a refresh since we are watching the pagination object
        this.pagination.page = 1
      },
      deep: true
    },
    pagination: {
      async handler () {
        await this.updateEmployerData(false)
      },
      deep: true
    }
  },
  methods: {
    clearEmployerFilter () {
      this.employerFilter = { ...employerFilterTemplate }
    },
    updatePagination (props) {
      this.pagination = props.pagination
    },
    async updateEmployerData (isForce) {
      this.isLoading = true
      const requestCfg = {
        pageCount: this.pagination.page,
        filterBy: JSON.stringify(this.employerFilter)
      }
      await this.adminStore.setPaginatedEmployers({ ...requestCfg, isForce })
      const {
        total_page_count: totalPageCount,
        total_employer_count: totalEmployerCount,
        employers
      } = this.adminStore.getPaginatedEmployers(requestCfg)
      this.pagination.totalPageCount = totalPageCount
      this.pagination.rowsNumber = totalEmployerCount
      this.employers = employers
      this.isLoading = false
    },
    async deleteEmployer (employer) {
      openConfirmDialog(
        this.q,
        `Are you sure you want to delete ${employer.name}? This will delete all associated data including job applications.`,
        {
          okFn: async () => {
            await this.$api.delete(`admin/employer/${employer.id}`)
            await this.updateEmployerData(true)
          }
        }
      )
    },
    openDialogAdminEmployer (employer) {
      return this.q.dialog({
        component: DialogAdminEmployer,
        componentProps: { employer }
      }).onOk(async () => {
        await this.updateEmployerData(true)
      })
    }
  },
  async mounted () {
    await this.updateEmployerData(false)
  },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()
    return authStore.setUser().finally(() => Loading.hide())
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Admin Employer Page'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>
