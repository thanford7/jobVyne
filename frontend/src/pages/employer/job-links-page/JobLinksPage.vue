<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Job links"/>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="employee" label="Employee referrals"/>
        <q-tab name="job" label="Job webpages"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="employee">
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
        </q-tab-panel>
        <q-tab-panel name="job">
          <div>
            <div class="row">
              <div class="col-12 callout-card">
                Generate links that will direct to a job board page. This can be used as a company jobs website
                or posted on other areas of employer owned sites (such as a LinkedIn employer page).
              </div>
              <div class="col-12 q-pt-md">
                <q-table
                  :rows="jobLinks"
                  :columns="jobLinkColumns"
                  :rows-per-page-options="[10, 25, 50]"
                >
                  <template v-slot:top>
                    <div>
                      <q-btn
                        label="Create new job board"
                        color="primary" ripple unelevated
                        @click="openJobLinkDialog()"
                      />
                    </div>
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
                          color="primary" outline round dense
                          title="Edit job board" class="q-mr-xs"
                          @click="openJobLinkDialog(props.row)" icon="edit"
                        />
                        <q-btn
                          color="negative" outline round dense title="Delete job board"
                          @click="deleteJobLink(props.row.id)" icon="delete"
                        />
                      </q-td>
                      <q-td
                        v-for="col in props.cols"
                        :key="col.name"
                        :props="props"
                      >
                        <template v-if="col.name === 'link'">
                          <a :href="socialUtil.getJobLinkUrl(props.row)" target="_blank">
                            Job board link
                          </a>
                          <q-btn
                            flat round dense icon="content_copy"
                            size="sm" @click="dataUtil.copyText(socialUtil.getJobLinkUrl(props.row))"
                          />
                        </template>
                        <template v-else-if="col.name === 'tags'">
                          <q-chip
                            v-for="tag in props.row.tags"
                            dense color="grey-7" text-color="white" size="13px"
                          >
                            {{ tag.name }}
                          </q-chip>
                        </template>
                        <span v-else>{{ col.value }}</span>
                      </q-td>
                    </q-tr>
                  </template>
                </q-table>
              </div>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import dataUtil from 'src/utils/data.js'
import DialogJobLink from 'components/dialogs/DialogJobLink.vue'
import DialogShareJobLink from 'components/dialogs/DialogShareJobLink.vue'
import PageHeader from 'components/PageHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import dateTimeUtil from 'src/utils/datetime.js'
import locationUtil from 'src/utils/location.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import socialUtil from 'src/utils/social.js'
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

const jobLinkColumns = [
  { name: 'link_name', field: 'link_name', align: 'left', label: 'Name', sortable: true },
  { name: 'link', field: 'id', align: 'left', label: 'Link' },
  { name: 'tags', field: 'tags', align: 'left', label: 'Tags' }
]

export default {
  name: 'JobLinksPage',
  components: { PageHeader },
  data () {
    return {
      tab: 'employee',
      referralRequests: [],
      jobLinks: [],
      referralRequestColumns,
      jobLinkColumns,
      dataUtil,
      locationUtil,
      socialUtil
    }
  },
  methods: {
    async deleteJobLink (jobLinkId) {
      openConfirmDialog(this.q, 'Are you sure you want to delete this job board? The link will still continue to work, but it will no longer be displayed in reports', {
        okFn: async () => {
          await this.$api.delete('social-link-filter/', {
            data: getAjaxFormData({ link_filter_id: jobLinkId })
          })
          await this.employerStore.setEmployerSocialLinks(this.user.employer_id, true)
          this.jobLinks = this.employerStore.getEmployerSocialLinks(this.user.employer_id)
        }
      })
    },
    openJobLinkDialog (jobLink) {
      return this.q.dialog({
        component: DialogJobLink,
        componentProps: { employerId: this.user.employer_id, isJobBoard: true, jobLink }
      }).onOk(() => {
        this.jobLinks = this.employerStore.getEmployerSocialLinks(this.user.employer_id)
      })
    },
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
    this.jobLinks = this.employerStore.getEmployerSocialLinks(this.user.employer_id)
  },
  preFetch () {
    const authStore = useAuthStore()
    const employerStore = useEmployerStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployerReferralRequests(authStore.propUser.employer_id),
        employerStore.setEmployerSocialLinks(authStore.propUser.employer_id)
      ])
    }).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)

    const pageTitle = 'Job links'
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
