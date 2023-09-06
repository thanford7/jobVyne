<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Admin Dashboard"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12">
          <div class="row">
            <div class="col-12 col-md-4 q-px-sm">
              <div class="text-bold">Jobs With Description</div>
              <div>
                {{ processedJobsData.jobs_with_description_count }} / {{ processedJobsData.open_jobs_count }}
                ({{
                  mathUtil.getPercentage(processedJobsData.jobs_with_description_count, processedJobsData.open_jobs_count)
                }})
              </div>
            </div>
            <div class="col-12 col-md-4 q-px-sm">
              <div class="text-bold">Jobs With Profession</div>
              <div>
                {{ processedJobsData.jobs_with_profession_count }} / {{ processedJobsData.open_jobs_count }}
                ({{
                  mathUtil.getPercentage(processedJobsData.jobs_with_profession_count, processedJobsData.open_jobs_count)
                }})
              </div>
            </div>
            <div class="col-12 col-md-4 q-px-sm">
              <div class="text-bold">Employers With Description</div>
              <div>
                {{ processedJobsData.employers_with_description_count }} / {{ processedJobsData.employers_count }}
                ({{
                  mathUtil.getPercentage(processedJobsData.employers_with_description_count, processedJobsData.employers_count)
                }})
              </div>
            </div>
          </div>
        </div>
        <div class="col-12 q-gutter-sm">
          <div class="text-h6">Support</div>
          <q-btn label="Product announcement email" color="primary" @click="openAnnouncementEmailDialog"/>
          <q-btn label="Update user connections" color="primary" @click="updateUserConnections"/>
        </div>
        <div class="col-12 q-gutter-sm">
          <div class="text-h6">Testing</div>
          <q-btn label="Test error message" color="primary" @click="getTestMsg"/>
          <q-btn label="Test email" color="primary" @click="sendTestEmail"/>
        </div>
        <div class="col-12 q-gutter-sm">
          <div class="text-h6">ATS</div>
          <q-btn label="Update jobs" color="primary" @click="updateAtsJobs"/>
          <template v-if="failedAtsApplications.length">
            <q-btn label="Push failed job applications" color="primary" @click="pushFailedAtsApps"/>
            <q-btn label="Show failed job applications" color="primary" @click="openFailedAtsAppsDialog"/>
          </template>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import DialogAnnouncementEmail from 'components/dialogs/DialogAnnouncementEmail.vue'
import DialogShowDataTable from 'components/dialogs/DialogShowDataTable.vue'
import PageHeader from 'components/PageHeader.vue'
import { Loading, useMeta, useQuasar } from 'quasar'
import mathUtil from 'src/utils/math.js'
import { useAdminStore } from 'stores/admin-store.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'DashboardPage',
  components: { PageHeader },
  data () {
    return {
      failedAtsApplications: [],
      processedJobsData: {},
      adminStore: useAdminStore(),
      q: useQuasar(),
      mathUtil
    }
  },
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
          data: this.failedAtsApplications,
          ignoreColumns: ['linkedin_url', 'resume_url']
        }
      })
    },
    pushFailedAtsApps () {
      this.$api.post('admin/ats-failure/')
    },
    sendTestEmail () {
      this.$api.post('test/email/')
    },
    updateAtsJobs () {
      this.$api.post('admin/ats-jobs/')
    },
    updateUserConnections () {
      this.$api.post('admin/user-connections/')
    }
  },
  async mounted () {
    Loading.show()
    const authStore = useAuthStore()

    await authStore.setUser().then(() => {
      return Promise.all([
        this.adminStore.setFailedAtsApplications(),
        this.adminStore.setProcessedJobsData()
      ])
    }).finally(() => {
      Loading.hide()
    })

    this.failedAtsApplications = this.adminStore.failedAtsApplications
    this.processedJobsData = this.adminStore.processedJobsData
  },
  setup () {
    const globalStore = useGlobalStore()
    const pageTitle = 'Admin Dashboard'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>
