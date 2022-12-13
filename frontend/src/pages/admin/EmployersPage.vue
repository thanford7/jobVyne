<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Employers"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12">
          <q-table
            :rows="employers"
            :columns="employerColumns"
            row-key="id"
            :rows-per-page-options="[15, 25, 50]"
          >
            <template v-slot:top>
              <q-btn ripple color="primary" label="Create new employer" @click="openDialogAdminEmployer()"/>
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
                  <q-btn size="sm" color="gray-500" round dense @click="openDialogAdminEmployer(props.row)"
                         icon="edit"/>
                </q-td>
                <q-td
                  v-for="col in props.cols"
                  :key="col.name"
                  :props="props"
                >
                  <template v-if="col.name === 'subscriptionStatus'">
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
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import { SUBSCRIPTION_STATUS } from 'src/utils/subscription.js'
import { useAdminStore } from 'stores/admin-store.js'
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
    format: dateTimeUtil.getShortDate.bind(dateTimeUtil)
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

export default {
  name: 'EmployersPage',
  components: { PageHeader },
  data () {
    return {
      employerColumns,
      dataUtil,
      SUBSCRIPTION_STATUS
    }
  },
  methods: {
    openDialogAdminEmployer (employer) {
      return this.q.dialog({
        component: DialogAdminEmployer,
        componentProps: { employer }
      }).onOk(async () => {
        Loading.show()
        await this.adminStore.setEmployers(true)
        Loading.hide()
      })
    }
  },
  preFetch () {
    const adminStore = useAdminStore()
    Loading.show()

    return adminStore.setEmployers().finally(() => Loading.hide())
  },
  setup () {
    const globalStore = useGlobalStore()
    const adminStore = useAdminStore()
    const { employers } = storeToRefs(adminStore)

    const pageTitle = 'Admin Employer Page'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      adminStore,
      employers,
      q: useQuasar()
    }
  }
}
</script>
