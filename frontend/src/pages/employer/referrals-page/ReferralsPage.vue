<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Employee referrals"/>
      <div>
        <div class="row q-gutter-y-md">
          <div class="col-12 callout-card">
            Send referral requests to employees. Each employee will receive a unique tracking link.
          </div>
          <div class="col-12 q-pt-md">
            <q-table
              :rows="referralRequests"
              :columns="referralRequestColumns"
            >
              <template v-slot:top>
                <div>
                  <q-btn
                    label="Send referral request"
                    color="primary" ripple unelevated
                    @click="openReferralRequestDialog"
                  />
                </div>
              </template>
              <template v-slot:body="props">
                <q-tr :props="props">
                  <q-td
                    v-for="col in props.cols"
                    :key="col.name"
                    :props="props"
                  >
                    <template v-if="col.name === 'departments'">
                      <template v-if="props.row?.departments?.length">
                        <q-chip
                          v-for="dept in props.row.departments"
                          dense color="blue-grey-7" text-color="white" size="13px"
                        >
                          {{ dept.name }}
                        </q-chip>
                      </template>
                      <span v-else>Any department</span>
                    </template>
                    <template v-else-if="col.name === 'locations'">
                      <template v-if="locationUtil.getFormattedLocations(props.row).length">
                        <q-chip
                          v-for="location in locationUtil.getFormattedLocations(props.row)"
                          dense :color="location.color" text-color="white" size="13px"
                        >
                          {{ location.name }}
                        </q-chip>
                      </template>
                      <span v-else>Any location</span>
                    </template>
                    <template v-else-if="col.name === 'jobs'">
                      <template v-if="props.row?.jobs?.length">
                        <q-chip
                          v-for="job in props.row.jobs"
                          dense color="blue-grey-7" text-color="white" size="13px"
                        >
                          {{ job.title }}
                        </q-chip>
                      </template>
                      <span v-else>Any job</span>
                    </template>
                    <span v-else>{{ col.value }}</span>
                  </q-td>
                </q-tr>
              </template>
            </q-table>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import DialogShareJobLink from 'components/dialogs/DialogShareJobLink.vue'
import PageHeader from 'components/PageHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import dateTimeUtil from 'src/utils/datetime.js'
import locationUtil from 'src/utils/location.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'

const referralRequestColumns = [
  {
    name: 'modified_dt',
    field: 'modified_dt',
    align: 'left',
    label: 'Last sent',
    sortable: true,
    sort: dateTimeUtil.sortDatesFn.bind(dateTimeUtil),
    format: (val) => dateTimeUtil.getShortDate(val)
  },
  { name: 'departments', field: 'departments', align: 'left', label: 'Job departments' },
  { name: 'locations', field: 'cities', align: 'left', label: 'Locations' },
  { name: 'jobs', field: 'jobs', align: 'left', label: 'Jobs' }
]

export default {
  name: 'ReferralsPage',
  components: {
    PageHeader
  },
  data () {
    return {
      tab: 'employee',
      referralRequests: [],
      referralRequestColumns,
      locationUtil
    }
  },
  methods: {
    openReferralRequestDialog () {
      return this.q.dialog({
        component: DialogShareJobLink,
        componentProps: { employerId: this.user.employer_id }
      }).onOk(() => {
        this.referralRequests = this.employerStore.getEmployerReferralRequests(this.user.employer_id)
      })
    }
  },
  mounted () {
    this.referralRequests = this.employerStore.getEmployerReferralRequests(this.user.employer_id)
  },
  preFetch () {
    const authStore = useAuthStore()
    const employerStore = useEmployerStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployerReferralRequests(authStore.propUser.employer_id)
      ])
    }).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)

    const pageTitle = 'Employee Referrals'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      user,
      employerStore: useEmployerStore(),
      q: useQuasar()
    }
  }
}
</script>
