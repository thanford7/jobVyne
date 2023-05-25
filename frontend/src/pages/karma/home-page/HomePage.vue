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
              :rows="userRequests"
              :columns="userRequestColumns"
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
              :rows="userDonationOrganizations"
              :columns="userDonationOrganizationColumns"
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
                        <div>{{props.row.name}}</div>
                      </div>
                    </template>
                    <template v-if="col.name === 'url_main'">
                      <a :href="props.row.url_main">{{ props.row.name }}</a>
                    </template>
                    <template v-if="col.name === 'url_donation'">
                      <a :href="props.row.url_donation">Donate to {{ props.row.name }}</a>
                    </template>
                  </q-td>
                </q-tr>
              </template>
            </q-table>
          </div>
          <div class="col-12">
            <CollapsableCard
              title="Donations"
              :can-collapse="false"
            >
              <template v-slot:header>
                <div>
                  <q-btn
                    label="Add donation"
                    icon="price_check"
                    color="primary"
                    ripple
                    @click="openUserDonationDialog()"
                  />
                </div>
              </template>
            </CollapsableCard>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </div>
</template>

<script>
import CollapsableCard from 'components/CollapsableCard.vue'
import DialogUserDonation from 'components/dialogs/DialogUserDonation.vue'
import DialogUserDonationOrganization from 'components/dialogs/DialogUserDonationOrganization.vue'
import DialogUserRequest from 'components/dialogs/DialogUserRequest.vue'
import PageHeader from 'components/PageHeader.vue'
import KarmaSidebar from 'pages/karma/KarmaSidebar.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import { USER_REQUEST_TYPES } from 'src/utils/karma.js'
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
    field: 'url_donation',
    align: 'left',
    label: 'Donation Page'
  }
]

const userRequestColumns = [
  { name: 'request_type', field: (ur) => USER_REQUEST_TYPES[ur.request_type].label, align: 'left', label: 'Request type', sortable: true },
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

export default {
  name: 'HomePage',
  components: { CollapsableCard, KarmaSidebar, PageHeader },
  data () {
    return {
      isLeftDrawerOpen: true,
      userDonationOrganizationColumns,
      userRequestColumns,
      q: useQuasar()
    }
  },
  methods: {
    getUserRequestPages (userRequest) {
      return USER_REQUEST_TYPES[userRequest.request_type].pages
    },
    openUserDonationDialog () {
      return this.q.dialog({
        component: DialogUserDonation
      })
    },
    openUserDonationOrganizationDialog () {
      return this.q.dialog({
        component: DialogUserDonationOrganization
      })
    },
    openUserRequestDialog () {
      return this.q.dialog({
        component: DialogUserRequest
      }).onOk(async () => {
        await this.karmaStore.setUserRequests(this.user.id, true)
        this.userRequests = this.karmaStore.getUserRequests()
      })
    }
  },
  preFetch () {
    const authStore = useAuthStore()
    const karmaStore = useKarmaStore()
    Loading.show()

    return Promise.all([
      karmaStore.setUserRequests(authStore.propUser.id),
      karmaStore.setUserDonationOrganizations(authStore.propUser.id)
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
      userDonationOrganizations: karmaStore.getUserDonationOrganizations(),
      userRequests: karmaStore.getUserRequests(),
      karmaStore
    }
  }
}
</script>
