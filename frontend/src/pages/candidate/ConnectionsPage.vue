<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Connections"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12">
          <q-table
            :loading="isLoading"
            :rows="connections"
            :columns="connectionColumns"
            :rows-per-page-options="[25]"
          >
            <template v-slot:top>
              <q-btn
                ripple color="primary" label="Upload LinkedIn Contacts"
                @click="openDialogBulkUploadLinkedInContacts()"
              />
            </template>
            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td
                  v-for="col in props.cols"
                  :key="col.name"
                  :props="props"
                >
                  <template v-if="col.name === 'fullName'">
                    <a v-if="props.row.connection_user_key" :href="`/jv/${props.row.connection_user_key}/`">{{ col.value }}</a>
                    <span v-else>{{ col.value }}</span>
                  </template>
                  <template v-else-if="col.name === 'linkedin'">
                    <a :href="col.value">LinkedIn</a>
                  </template>
                  <template v-else-if="col.name === 'employer'">
                    <a v-if="props.row.employer" :href="`/co/${props.row.employer.key}`">{{ props.row.employer.name }}</a>
                    <span v-else>{{ props.row.employer_raw }}</span>
                  </template>
                  <template v-else-if="col.name === 'profession'">
                    {{ props.row.profession?.name || 'Unknown' }}
                  </template>
                  <template v-else>
                    {{ col.value }}
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
import DialogBulkUploadLinkedInContacts from 'components/dialogs/DialogBulkUploadLinkedInContacts.vue'
import PageHeader from 'components/PageHeader.vue'
import { useMeta, useQuasar } from 'quasar'
import { useAuthStore } from 'stores/auth-store.js'
import { useCommunityStore } from 'stores/community-store.js'
import { useGlobalStore } from 'stores/global-store.js'

const connectionColumns = [
  { name: 'fullName', field: 'full_name', align: 'left', label: 'Name', sortable: true },
  { name: 'linkedin', field: 'linkedin_url', align: 'left', label: 'LinkedIn' },
  { name: 'employer', field: 'employer', align: 'left', label: 'Employer', sortable: true },
  { name: 'jobTitle', field: 'job_title', align: 'left', label: 'Job Title', sortable: true },
  { name: 'profession', field: 'profession', align: 'left', label: 'Profession', sortable: true }
]

export default {
  name: 'ConnectionsPage',
  components: { PageHeader },
  data () {
    return {
      isLoading: true,
      connections: [],
      connectionColumns,
      authStore: useAuthStore(),
      communityStore: useCommunityStore(),
      q: useQuasar()
    }
  },
  methods: {
    async updateConnections (isForceRefresh) {
      this.isLoading = true
      await this.communityStore.setJobConnections({ userId: this.user.id, isForceRefresh })
      this.connections = this.communityStore.getJobConnections({ userId: this.user.id, isForceRefresh })
      this.isLoading = false
    },
    openDialogBulkUploadLinkedInContacts () {
      this.q.dialog({
        component: DialogBulkUploadLinkedInContacts
      }).onOk(async () => {
        await this.updateConnections(true)
      })
    }
  },
  async mounted () {
    await this.authStore.setUser().then(() => {
      this.user = this.authStore.propUser
      return Promise.all([
        this.updateConnections(false)
      ])
    })
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Connections'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>
