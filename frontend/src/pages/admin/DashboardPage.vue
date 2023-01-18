<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Admin Dashboard"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12 q-gutter-sm">
          <div class="text-h6">Support</div>
          <q-btn label="Product announcement email" color="primary" @click="openAnnouncementEmailDialog"/>
          <template v-if="failedAtsApplications.length">
            <q-btn label="Push failed ATS job applications" color="primary" @click="pushFailedAtsApps"/>
            <q-btn label="Show failed ATS job applications" color="primary" @click="openFailedAtsAppsDialog"/>
          </template>
        </div>
        <div class="col-12 q-gutter-sm">
          <div class="text-h6">Testing</div>
          <q-btn label="Test error message" color="primary" @click="getTestMsg"/>
          <q-btn label="Test email" color="primary" @click="sendTestEmail"/>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import DialogAnnouncementEmail from 'components/dialogs/DialogAnnouncementEmail.vue'
import DialogShowDataTable from 'components/dialogs/DialogShowDataTable.vue'
import PageHeader from 'components/PageHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import { useAdminStore } from 'stores/admin-store.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'DashboardPage',
  components: { PageHeader },
  methods: {
    getTestMsg () {
      this.$api.get('test/error-msg/')
    },
    openAnnouncementEmailDialog () {
      this.q.dialog({
        component: DialogAnnouncementEmail,
        componentProps: { employerId: null }
      })
    },
    openFailedAtsAppsDialog () {
      this.q.dialog({
        component: DialogShowDataTable,
        componentProps: {
          data: this.failedAtsApplications
        }
      })
    },
    pushFailedAtsApps () {
      this.$api.post('admin/ats-failure/')
    },
    sendTestEmail () {
      this.$api.post('test/email/')
    }
  },
  preFetch () {
    const authStore = useAuthStore()
    const adminStore = useAdminStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return adminStore.setFailedAtsApplications()
    }).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const globalStore = useGlobalStore()
    const adminStore = useAdminStore()
    const { failedAtsApplications } = storeToRefs(adminStore)

    const pageTitle = 'Admin Dashboard'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      failedAtsApplications,
      q: useQuasar()
    }
  }
}
</script>
