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
          <ConnectionsTable :is-owner="true"/>
        </div>
      </div>
    </div>
  </q-page>
</template>
<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import PageHeader from 'components/PageHeader.vue'
import ConnectionsTable from 'pages/candidate/connections-page/ConnectionsTable.vue'
import ShareConnectionsTooltip from 'pages/candidate/ShareConnectionsTooltip.vue'
import { useMeta } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'ConnectionsPage',
  components: { ConnectionsTable, ShareConnectionsTooltip, CustomTooltip, PageHeader },
  data () {
    return {
      user: null,
      isShareConnections: null,
      dataUtil,
      authStore: useAuthStore()
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
    }
  },
  async mounted () {
    await this.authStore.setUser()
    this.user = this.authStore.propUser
    this.isShareConnections = this.user.is_share_connections
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
