<template>
  <q-table
    :loading="isLoading"
    :rows="connections"
    :columns="connectionColumns"
    :rows-per-page-options="[10, 25, 50]"
    v-model:pagination="pagination"
    :filter="connectionFilter"
    @request="updateConnections"
  >
    <template v-slot:top>
      <div class="col-12 q-mb-sm">
        <div class="row items-center">
          <div class="flex-inline">
            <div class="col-12 text-small text-center border-bottom-1-gray-100 q-mb-xs">Group by</div>
            <q-btn-group rounded unelevated>
              <q-btn
                v-for="option in GROUP_OPTIONS"
                :color="(groupBy.includes(option.key)) ? 'grey-8' : 'grey-4'"
                :text-color="(groupBy.includes(option.key)) ? 'white' : 'black'"
                rounded size="12px" :label="option.label"
                @click="toggleGroup(option.key)"
              />
            </q-btn-group>
          </div>
          <q-space/>
          <div v-if="isOwner">
            <q-btn
              ripple color="primary" label="Upload LinkedIn Contacts" class="q-mr-sm"
              @click="openDialogBulkUploadLinkedInContacts()"
            />
            <q-btn
              v-if="connections?.length"
              ripple color="negative" label="Delete All Contacts"
              @click="deleteContacts()"
            />
          </div>
        </div>
      </div>
    </template>
    <template v-slot:header="props">
      <q-tr :props="props">
        <q-th
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          <template v-if="col.name === 'fullName'">
            {{ col.label }}
            <TableFilter filter-name="Name"
                         :has-filter="dataUtil.getBoolean(connectionFilter?.name?.length)">
              <q-input filled borderless debounce="300" v-model="connectionFilter.name"
                       placeholder="Name">
                <template v-slot:append>
                  <q-icon name="search"/>
                </template>
              </q-input>
            </TableFilter>
          </template>
          <template v-else-if="col.name === 'employer'">
            {{ col.label }}
            <TableFilter filter-name="Employer"
                         :has-filter="dataUtil.getBoolean(connectionFilter?.employer_name?.length)">
              <q-input filled borderless debounce="300" v-model="connectionFilter.employer_name"
                       placeholder="Employer">
                <template v-slot:append>
                  <q-icon name="search"/>
                </template>
              </q-input>
            </TableFilter>
          </template>
          <template v-else-if="col.name === 'jobTitle'">
            {{ col.label }}
            <TableFilter filter-name="Job title"
                         :has-filter="dataUtil.getBoolean(connectionFilter?.job_title?.length)">
              <q-input filled borderless debounce="300" v-model="connectionFilter.job_title" placeholder="Job title">
                <template v-slot:append>
                  <q-icon name="search"/>
                </template>
              </q-input>
            </TableFilter>
          </template>
          <template v-else-if="col.name === 'profession'">
            {{ col.label }}
            <TableFilter filter-name="Professions"
                         :has-filter="dataUtil.getBoolean(connectionFilter?.profession_ids?.length)">
              <SelectJobProfession v-model="connectionFilter.profession_ids" :is-multi="true"/>
            </TableFilter>
          </template>
          <span v-else>{{ col.label }}</span>
        </q-th>
      </q-tr>
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
</template>
<script>

import DialogBulkUploadLinkedInContacts from 'components/dialogs/DialogBulkUploadLinkedInContacts.vue'
import SelectJobProfession from 'components/inputs/SelectJobProfession.vue'
import TableFilter from 'components/tables/TableFilter.vue'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useCommunityStore } from 'stores/community-store.js'

const GROUP_OPTIONS = [
  { label: 'Employer', key: 'employer' },
  { label: 'Profession', key: 'profession' }
]

const connectionFilterTemplate = {
  name: null,
  employer_name: null,
  job_title: null,
  profession_ids: null
}

const pagination = {
  sortBy: 'fullName',
  descending: false,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: null
}

export default {
  name: 'ConnectionsTable',
  components: { SelectJobProfession, TableFilter },
  props: {
    isOwner: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoading: true,
      connections: [],
      connectionFilter: { ...connectionFilterTemplate },
      pagination,
      user: null,
      groupBy: [],
      GROUP_OPTIONS,
      dataUtil,
      authStore: useAuthStore(),
      communityStore: useCommunityStore(),
      q: useQuasar()
    }
  },
  computed: {
    connectionColumns () {
      if (!this.groupBy?.length) {
        return [
          { name: 'fullName', field: 'full_name', align: 'left', label: 'Name', sortable: true },
          { name: 'linkedin', field: 'linkedin_url', align: 'left', label: 'LinkedIn' },
          { name: 'employer', field: 'employer', align: 'left', label: 'Employer', sortable: true },
          { name: 'jobTitle', field: 'job_title', align: 'left', label: 'Job Title', sortable: true },
          { name: 'profession', field: 'profession', align: 'left', label: 'Profession', sortable: true }
        ]
      }
      const connectionColumns = []
      if (this.groupBy.includes('employer')) {
        connectionColumns.push({ name: 'employer', field: 'employer', align: 'left', label: 'Employer', sortable: true })
      }
      if (this.groupBy.includes('profession')) {
        connectionColumns.push({ name: 'profession', field: 'profession', align: 'left', label: 'Profession', sortable: true })
      }
      connectionColumns.push({ name: 'connectionCount', field: 'connection_count', align: 'center', label: 'Connections', sortable: true })
      return connectionColumns
    }
  },
  methods: {
    async deleteContacts () {
      openConfirmDialog(this.q, 'Are you sure you want to delete all of your contacts? This is irreversible.', {
        okFn: async () => {
          await this.$api.delete('community/job-connections/', {
            data: getAjaxFormData({ userId: this.user.id })
          })
          await this.updateConnections({ isForceRefresh: true })
        }
      })
    },
    async updateConnections (
      {
        pagination = this.pagination,
        filters = this.connectionFilter,
        isForceRefresh = false
      } = {}
    ) {
      this.isLoading = true
      const params = {
        userId: this.user.id,
        rowsPerPage: pagination.rowsPerPage,
        pageCount: pagination.page,
        sortBy: pagination.sortBy,
        isDescending: pagination.descending,
        filters,
        groupBy: (this.groupBy?.length) ? this.groupBy : null
      }
      await this.communityStore.setJobConnections(
        { ...params, isForceRefresh }
      )
      const data = this.communityStore.getJobConnections(params)
      this.connections = data.user_connections
      Object.assign(this.pagination, pagination)
      this.pagination.rowsNumber = data.total_connection_count
      this.isLoading = false
    },
    async toggleGroup (groupKey) {
      if (this.groupBy.includes(groupKey)) {
        dataUtil.removeItemFromList(this.groupBy, { itemFindFn: (item) => item === groupKey })
      } else {
        this.groupBy.push(groupKey)
      }
      await this.updateConnections()
    },
    clearConnectionFilter () {
      this.connectionFilter = { ...connectionFilterTemplate }
    },
    openDialogBulkUploadLinkedInContacts () {
      this.q.dialog({
        component: DialogBulkUploadLinkedInContacts
      }).onOk(async () => {
        await this.updateConnections({ isForceRefresh: true })
      })
    }
  },
  async mounted () {
    this.user = this.authStore.propUser
    await this.updateConnections()
  }
}
</script>
