<template>
  <q-table
    :loading="isLoading"
    :rows="userJobs"
    row-key="id"
    :columns="jobColumns"
    v-model:pagination="pagination"
    no-data-label="No jobs match the filter"
    :rows-per-page-options="[25]"
  >
    <template v-slot:top>
      <div class="col-12">
        <div class="row q-gutter-sm">
          <q-btn-toggle
            v-model="formData.isClosedJobs"
            unelevated
            class="border-1-primary"
            toggle-color="primary"
            :options="[
                {label: 'Open Jobs', value: false},
                {label: 'Closed Jobs', value: true}
              ]"
          />
          <q-select
            v-model="formData.isApprovedJobs"
            label="Approval Status"
            style="min-width: 200px"
            filled emit-value map-options
            :options="[
              { label: 'Approved', value: true },
              { label: 'Not Approved', value: false }
            ]"
          />
        </div>
      </div>
    </template>

    <template v-slot:header="props">
      <q-tr :props="props">
        <q-th auto-width>
          Actions
        </q-th>
        <q-th
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          <span>{{ col.label }}</span>
        </q-th>
      </q-tr>
    </template>

    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td auto-width>
          <template v-if="props.row.can_edit">
            <CustomTooltip v-if="isAdmin" :is_include_icon="false">
              <template v-slot:content>
                <q-btn
                  outline round dense
                  :icon="(props.row.is_approved) ? 'thumb_down_alt' : 'thumb_up_alt'"
                  :color="(props.row.is_approved) ? 'negative' : 'positive'"
                  class="q-mr-xs"
                  @click="changeJobApproval(props.row)"
                />
              </template>
              {{ (props.row.is_approved) ? 'Un-approve' : 'Approve' }} job
            </CustomTooltip>
            <CustomTooltip :is_include_icon="false">
              <template v-slot:content>
                <q-btn
                  outline round dense icon="edit" color="primary" class="q-mr-xs"
                  @click="openEditJobDialog(props.row)"
                />
              </template>
              Edit job
            </CustomTooltip>
            <CustomTooltip :is_include_icon="false">
              <template v-slot:content>
                <q-btn
                  outline round dense icon="delete" color="negative"
                  @click="deleteJob(props.row)"
                />
              </template>
              Delete job
            </CustomTooltip>
          </template>
        </q-td>
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          <template v-if="col.name === 'locations'">
            <LocationsCell :locations="props.row.locations"/>
          </template>
          <template v-else-if="col.name === 'is_approved'">
            <q-icon v-if="props.row.is_approved" name="check_circle" color="positive" size="24px" title="Approved"/>
            <CustomTooltip v-else :is_include_icon="false">
              <template v-slot:content>
                <q-icon name="do_not_disturb" color="negative" size="24px" title="Un-approved"/>
              </template>
              A JobVyne Administrator will review the job and approve within 24 hours of posting
            </CustomTooltip>
          </template>
          <template v-else-if="col.name === 'created_by'">
            <a :href="`mailto: ${props.row.created_by_email}`">{{ props.row.created_by }}</a>
          </template>
          <span v-else>{{ col.value }}</span>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogJob from 'components/dialogs/DialogJob.vue'
import LocationsCell from 'pages/employer/jobs-page/jobs-table/LocationsCell.vue'
import { useQuasar } from 'quasar'
import dateTimeUtil from 'src/utils/datetime.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import { useUserStore } from 'stores/user-store.js'

export default {
  name: 'UserJobsTable',
  components: {
    LocationsCell,
    CustomTooltip
  },
  props: {
    isAdmin: {
      type: Boolean,
      default: false
    },
    userId: [Number, null]
  },
  data () {
    return {
      isLoading: false,
      formData: {
        isClosedJobs: false,
        isApprovedJobs: null
      },
      pagination: {
        sortBy: null,
        descending: true,
        page: 1,
        rowsPerPage: 25,
        rowsNumber: null,
        totalPageCount: 1
      },
      userJobs: [],
      userStore: useUserStore(),
      q: useQuasar()
    }
  },
  watch: {
    formData: {
      async handler () {
        await this.loadJobs()
      },
      deep: true
    },
    pagination: {
      async handler () {
        await this.loadJobs()
      },
      deep: true
    }
  },
  computed: {
    jobColumns () {
      const columns = [
        { name: 'is_approved', field: 'is_approved', align: 'center', label: 'Approval' },
        { name: 'job_title', field: 'job_title', align: 'left', label: 'Title' },
        { name: 'employer', field: 'employer_name', align: 'left', label: 'Employer' },
        { name: 'locations', field: 'locations', align: 'left', label: 'Location' },
        { name: 'employment_type', field: 'employment_type', align: 'left', label: 'Employment Type' },
        { name: 'salary', field: 'salary_text', align: 'left', label: 'Salary' },
        {
          name: 'open_date',
          field: 'open_date',
          align: 'left',
          label: 'Posted Date',
          sortable: true,
          sort: dateTimeUtil.sortDatesFn.bind(dateTimeUtil),
          format: (val) => dateTimeUtil.getShortDate(val)
        }
      ]

      if (this.isClosedJobs) {
        columns.push({
          name: 'close_date',
          field: 'close_date',
          align: 'left',
          label: 'Closed Date',
          sortable: true,
          sort: dateTimeUtil.sortDatesFn.bind(dateTimeUtil),
          format: (val) => dateTimeUtil.getShortDate(val)
        })
      }

      if (this.isAdmin) {
        columns.push({ name: 'created_by', field: 'created_by', align: 'left', label: 'Created By' })
      }

      return columns
    }
  },
  methods: {
    async loadJobs (isForceRefresh = false, pagination = this.pagination) {
      this.isLoading = true
      const queryParams = {
        pageCount: pagination.page,
        userId: this.userId,
        isApproved: this.formData.isApprovedJobs,
        isClosed: this.formData.isClosedJobs,
        rows_per_page: pagination.rowsPerPage,
        sort_order: pagination.sortBy,
        is_descending: pagination.descending
      }
      await this.userStore.setPaginatedUserCreatedJobs({ ...queryParams, isForceRefresh })
      const { total_page_count: totalPageCount, total_job_count: totalJobCount, jobs } = this.userStore.getPaginatedUserCreatedJobs(queryParams)
      this.userJobs = jobs
      this.pagination.rowsNumber = totalJobCount
      this.pagination.totalPageCount = totalPageCount
      this.isLoading = false
    },
    async deleteJob (job) {
      openConfirmDialog(this.q, 'Are you sure you want to delete this job?', {
        okFn: async () => {
          await this.$api.delete('user/created-jobs/', {
            data: getAjaxFormData({ job_id: job.id })
          })
          await this.loadJobs(true)
        }
      })
    },
    async changeJobApproval (job) {
      await this.$api.post(
        'admin/user-created-job/approval/',
        getAjaxFormData({ job_ids: [job.id], is_approved: !job.is_approved })
      )
      await this.loadJobs(true)
    },
    openEditJobDialog (job) {
      return this.q.dialog({
        component: DialogJob,
        componentProps: { job, employerId: job.employer_id }
      }).onOk(async () => {
        await this.loadJobs(true)
      })
    }
  },
  async mounted () {
    await this.loadJobs()
  }
}
</script>
