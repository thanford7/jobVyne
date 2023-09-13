<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Connections"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12">
          <a :href="`/jv/${user?.user_key}`" target="_blank">
            View your job connections
          </a>
          <CustomTooltip :is_include_icon="false">
            <template v-slot:content>
              <q-btn
                icon="content_copy"
                flat round size="sm"
                @click="dataUtil.copyText(jobConnectionsUrl)"
              />
            </template>
            Copy job connections URL
          </CustomTooltip>
        </div>
        <div class="col-12">
          <q-toggle :model-value="isShareConnections" @update:model-value="updateShareConnections">
            Share connections
            <ShareConnectionsTooltip/>
          </q-toggle>
        </div>
        <div class="col-12">
          <q-table
            :loading="isLoading"
            :rows="connections"
            :columns="connectionColumns"
            :rows-per-page-options="[25]"
          >
            <template v-slot:top>
              <q-btn
                ripple color="primary" label="Upload LinkedIn Contacts" class="q-mr-sm"
                @click="openDialogBulkUploadLinkedInContacts()"
              />
              <q-btn
                v-if="connections?.length"
                ripple color="negative" label="Delete All Contacts"
                @click="deleteContacts()"
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
                    <a v-if="props.row.connection_user_key" :href="`/jv/${props.row.connection_user_key}/`"
                       target="_blank">{{ col.value }}</a>
                    <span v-else>{{ col.value }}</span>
                  </template>
                  <template v-else-if="col.name === 'linkedin'">
                    <a :href="col.value" target="_blank">LinkedIn</a>
                  </template>
                  <template v-else-if="col.name === 'employer'">
                    <a v-if="props.row.employer" :href="`/co/${props.row.employer.key}`"
                       target="_blank">{{ props.row.employer.name }}</a>
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
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogBulkUploadLinkedInContacts from 'components/dialogs/DialogBulkUploadLinkedInContacts.vue'
import PageHeader from 'components/PageHeader.vue'
import ShareConnectionsTooltip from 'pages/candidate/ShareConnectionsTooltip.vue'
import { useMeta, useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
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
  components: { ShareConnectionsTooltip, CustomTooltip, PageHeader },
  data () {
    return {
      isLoading: true,
      isShareConnections: null,
      connections: [],
      connectionColumns,
      dataUtil,
      authStore: useAuthStore(),
      communityStore: useCommunityStore(),
      q: useQuasar()
    }
  },
  computed: {
    jobConnectionsUrl () {
      return `${window.location.origin}/jv/${this.user?.user_key}`
    }
  },
  methods: {
    async updateShareConnections (isShareConnections) {
      await this.$api.put('community/job-connections/share/', getAjaxFormData({
        user_id: this.user.id,
        is_share_connections: isShareConnections
      }))
      await this.authStore.setUser(true)
      this.user = this.authStore.propUser
      this.isShareConnections = this.user.is_share_connections
    },
    async deleteContacts () {
      openConfirmDialog(this.q, 'Are you sure you want to delete all of your contacts? This is irreversible.', {
        okFn: async () => {
          await this.$api.delete('community/job-connections/', {
            data: getAjaxFormData({ userId: this.user.id })
          })
          await this.updateConnections(true)
        }
      })
    },
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
      this.isShareConnections = this.user.is_share_connections
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
