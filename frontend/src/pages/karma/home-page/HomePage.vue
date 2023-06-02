<template>
  <div class="q-pl-sm">
    <KarmaSidebar v-model="isLeftDrawerOpen" :user="user"/>
    <q-page-container>
      <q-page padding>
        <PageHeader
          title="Karma Connect"
          :is-include-sidebar-toggle="true"
          @toggleLeftDrawer="isLeftDrawerOpen = !isLeftDrawerOpen"
        />
        <div class="row q-gutter-y-lg q-mt-md">
          <div class="col-12">
            <q-table
              ref="userRequestTable"
              :loading="isUserRequestTableLoading"
              :rows="userRequests"
              :columns="userRequestColumns"
              no-data-label="No requests"
            >
              <template v-slot:top>
                <div class="flex w-100">
                  <div class="text-h6">Requests</div>
                  <q-space/>
                  <q-btn
                    label="Create request"
                    icon="volunteer_activism"
                    color="primary"
                    ripple dense
                    @click="openUserRequestDialog()"
                  />
                </div>
              </template>
              <template v-slot:body-cell-pages="props">
                <q-td key="pages" :props="props">
                  <div v-for="page in getUserRequestPages(props.row)">
                    <a :href="`/karma/${page.key}/${props.row.id}`" target="_blank">
                      {{ page.name }}
                    </a>
                  </div>
                </q-td>
              </template>
            </q-table>
          </div>
          <div class="col-12">
            <q-table
              ref="userDonationOrgTable"
              :loading="isUserDonationOrgTableLoading"
              :rows="userDonationOrganizations"
              :columns="userDonationOrganizationColumns"
              no-data-label="No donation organizations"
            >
              <template v-slot:top>
                <div class="flex w-100">
                  <div class="text-h6">My Donation Organizations</div>
                  <q-space/>
                  <q-btn
                    label="Add organization"
                    icon="add_business"
                    color="primary"
                    ripple
                    @click="openUserDonationOrganizationDialog()"
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
                    <template v-if="col.name === 'name'">
                      <div class="flex items-center">
                        <q-img :src="props.row.logo_url" width="50px" class="q-mr-sm"/>
                        <div>{{ props.row.name }}</div>
                      </div>
                    </template>
                    <template v-if="col.name === 'url_main'">
                      <a :href="props.row.url_main" target="_blank">{{ props.row.name }}</a>
                    </template>
                    <template v-if="col.name === 'url_donation'">
                      <a :href="karmaUtil.getEveryOrgDonationLink(props.row, user)" target="_blank">Donate to
                        {{ props.row.name }}</a>
                    </template>
                  </q-td>
                </q-tr>
              </template>
            </q-table>
          </div>
          <div class="col-12">
            <q-table
              ref="userDonationTable"
              :loading="isUserDonationTableLoading"
              :rows="userDonations"
              :columns="userDonationColumns"
              no-data-label="No donations"
            >
              <template v-slot:top>
                <div class="flex w-100">
                  <div class="text-h6">Donations</div>
                  <q-space/>
                  <q-btn
                    label="Add donation"
                    icon="price_check"
                    color="primary"
                    ripple
                    @click="openUserDonationDialog()"
                  />
                </div>
              </template>
              <template v-slot:body-cell-isVerified="props">
                <q-td key="isVerified" :props="props">
                  <div v-if="props.row.is_verified">
                    <q-icon name="check_circle" color="positive"/> Verified
                  </div>
                  <div v-else>
                    <q-icon name="highlight_off" color="negative"/>
                    <a :href="karmaUtil.getEveryOrgDonationLink(props.row.donation_organization, user, props.row.id, props.row.donation_amount)" target="_blank">
                      Complete donation
                    </a>
                  </div>
                </q-td>
              </template>
            </q-table>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </div>
</template>

<script>
import DialogUserDonation from 'components/dialogs/DialogUserDonation.vue'
import DialogUserDonationOrganization from 'components/dialogs/DialogUserDonationOrganization.vue'
import DialogUserRequest from 'components/dialogs/DialogUserRequest.vue'
import PageHeader from 'components/PageHeader.vue'
import KarmaSidebar from 'pages/karma/KarmaSidebar.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import dateTimeUtil from 'src/utils/datetime.js'
import karmaUtil, { USER_REQUEST_TYPES } from 'src/utils/karma.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useKarmaStore } from 'stores/karma-store.js'

const userDonationOrganizationColumns = [
  {
    name: 'name',
    field: 'name',
    align: 'left',
    label: 'Organization',
    sortable: true
  },
  {
    name: 'url_main',
    field: 'url_main',
    align: 'left',
    label: 'Home Page'
  },
  {
    name: 'url_donation',
    field: 'id',
    align: 'left',
    label: 'Donation Page'
  }
]

const userRequestColumns = [
  {
    name: 'request_type',
    field: (ur) => USER_REQUEST_TYPES[ur.request_type].label,
    align: 'left',
    label: 'Request type',
    sortable: true
  },
  {
    name: 'connector_first_name',
    field: 'connector_first_name',
    align: 'left',
    label: 'Connector first name',
    sortable: true
  },
  {
    name: 'connector_last_name',
    field: 'connector_last_name',
    align: 'left',
    label: 'Connector last name',
    sortable: true
  },
  {
    name: 'connection_first_name',
    field: 'connection_first_name',
    align: 'left',
    label: 'Connection first name',
    sortable: true
  },
  {
    name: 'connection_last_name',
    field: 'connection_last_name',
    align: 'left',
    label: 'Connection last name',
    sortable: true
  },
  { name: 'pages', field: 'id', align: 'left', label: 'Pages' }
]

const userDonationColumns = [
  {
    name: 'donationDate',
    field: 'donate_dt',
    align: 'left',
    label: 'Donation Date',
    format: (val) => dateTimeUtil.getShortDate(val),
    sortable: true
  },
  {
    name: 'donationOrganization',
    field: (donation) => donation.donation_organization.name,
    align: 'left',
    label: 'Organization',
    sortable: true
  },
  {
    name: 'donationAmount',
    field: (donation) => `${donation.donation_amount_currency.symbol}${donation.donation_amount}`,
    align: 'left',
    label: 'Amount',
    sortable: true
  },
  {
    name: 'isVerified',
    field: 'is_verified',
    align: 'left',
    label: 'Completed',
    sortable: true
  }
]

export default {
  name: 'HomePage',
  components: { KarmaSidebar, PageHeader },
  data () {
    return {
      isUserRequestTableLoading: false,
      isUserDonationOrgTableLoading: false,
      isUserDonationTableLoading: false,
      isLeftDrawerOpen: true,
      userRequestColumns,
      userDonationOrganizationColumns,
      userDonationColumns,
      userDonationOrganizations: [],
      userRequests: [],
      userDonations: [],
      q: useQuasar(),
      karmaUtil
    }
  },
  methods: {
    getUserRequestPages (userRequest) {
      return USER_REQUEST_TYPES[userRequest.request_type].pages
    },
    openUserDonationDialog () {
      return this.q.dialog({
        component: DialogUserDonation
      }).onOk(async () => {
        await this.refreshUserDonationTable(true)
      })
    },
    openUserDonationOrganizationDialog () {
      return this.q.dialog({
        component: DialogUserDonationOrganization
      }).onOk(async () => {
        await this.refreshUserDonationOrgTable(true)
      })
    },
    openUserRequestDialog () {
      return this.q.dialog({
        component: DialogUserRequest
      }).onOk(async () => {
        await this.refreshUserRequestsTable(true)
      })
    },
    async refreshUserDonationTable (isForce) {
      this.isUserDonationTableLoading = true
      await this.karmaStore.setUserDonations(this.user.id, isForce)
      this.userDonations = this.karmaStore.getUserDonations(this.user.id)
      this.isUserDonationTableLoading = false
    },
    async refreshUserDonationOrgTable (isForce) {
      this.isUserDonationOrgTableLoading = true
      await this.karmaStore.setUserDonationOrganizations(this.user.id, isForce)
      this.userDonationOrganizations = this.karmaStore.getUserDonationOrganizations(this.user.id)
      this.isUserDonationOrgTableLoading = false
    },
    async refreshUserRequestsTable (isForce) {
      this.isUserRequestTableLoading = true
      await this.karmaStore.setUserRequests(this.user.id, isForce)
      this.userRequests = this.karmaStore.getUserRequests(this.user.id)
      this.isUserRequestTableLoading = false
    }
  },
  preFetch () {
    const authStore = useAuthStore()
    const karmaStore = useKarmaStore()
    Loading.show()

    return Promise.all([
      karmaStore.setUserRequests(authStore.propUser.id),
      karmaStore.setUserDonationOrganizations(authStore.propUser.id),
      karmaStore.setUserDonations(authStore.propUser.id)
    ]).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const karmaStore = useKarmaStore()
    const { user } = storeToRefs(authStore)

    useMeta(globalStore.getMetaCfg({
      pageTitle: 'Karma Connect',
      description: 'Do good while doing good'
    }))

    return {
      user,
      karmaStore
    }
  },
  mounted () {
    this.refreshUserDonationOrgTable(false)
    this.refreshUserDonationTable(false)
    this.refreshUserRequestsTable(false)
  }
}
</script>
