<template>
  <div v-if="isLoaded" class="row q-gutter-y-md" style="min-width: 500px;">
    <div class="col-12">
      <q-table
        :rows="jobApplicationRequirements"
        :columns="jobApplicationRequirmentColumns"
        :rows-per-page-options="[25, 50]"
      >
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th auto-width>Action</q-th>
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
                v-if="!props.row.is_locked"
                icon="edit" size="sm" color="gray-500" round dense
                @click="openJobApplicationRequirementDialog(props.row)"
              />
            </q-td>
            <q-td
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
            >
              <template v-if="col.name === 'application_field'">
                <CustomTooltip v-if="props.row.is_locked" :is_include_icon="false">
                  <template v-slot:content><q-icon name="lock"/></template>
                  This application field cannot be modified
                </CustomTooltip>
                {{ col.value }}
              </template>
              <template v-else-if="col.name === 'overrides'">
                <div v-if="props.row.required">
                  <div class="text-bold text-small">Required</div>
                  <DepartmentChip v-if="props.row.required.departments" :departments="props.row.required.departments" :is-dense="true"/>
                  <JobChip v-if="props.row.required.jobs" :jobs="props.row.required.jobs" :is-dense="true"/>
                </div>
                <div v-if="props.row.optional">
                  <div class="text-bold text-small">Optional</div>
                  <DepartmentChip v-if="props.row.optional.departments" :departments="props.row.optional.departments" :is-dense="true"/>
                  <JobChip v-if="props.row.optional.jobs" :jobs="props.row.optional.jobs" :is-dense="true"/>
                </div>
                <div v-if="props.row.hidden">
                  <div class="text-bold text-small">Hidden</div>
                  <DepartmentChip v-if="props.row.hidden.departments" :departments="props.row.hidden.departments" :is-dense="true"/>
                  <JobChip v-if="props.row.hidden.jobs" :jobs="props.row.hidden.jobs" :is-dense="true"/>
                </div>
              </template>
              <span v-else>{{ col.value }}</span>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DepartmentChip from 'components/DepartmentChip.vue'
import DialogJobApplicationRequirement from 'components/dialogs/DialogJobApplicationRequirement.vue'
import JobChip from 'components/JobChip.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

const jobApplicationRequirmentColumns = [
  {
    name: 'application_field',
    field: 'application_field',
    label: 'Field',
    align: 'left',
    format: (val) => dataUtil.capitalize(val.split('_').join(' '), false),
    sortable: true
  },
  {
    name: 'default',
    field: 'default',
    label: 'Default',
    align: 'left',
    format: (val) => (val.is_required) ? 'Required' : (val.is_optional) ? 'Optional' : 'Hidden',
    sortable: true
  },
  {
    name: 'overrides',
    field: 'required',
    label: 'Overrides',
    align: 'left'
  }
]

export default {
  name: 'ApplicationQuestionsSection',
  components: { CustomTooltip, DepartmentChip, JobChip },
  data () {
    return {
      isLoaded: false,
      jobApplicationRequirements: [],
      jobApplicationRequirmentColumns
    }
  },
  methods: {
    openJobApplicationRequirementDialog (applicationRequirement) {
      this.q.dialog({
        component: DialogJobApplicationRequirement,
        componentProps: {
          applicationRequirement,
          employerId: this.user.employer_id
        }
      }).onOk(async () => {
        await this.loadApplicationRequirements(true)
      })
    },
    async loadApplicationRequirements (isForceRefresh) {
      await this.employerStore.setEmployerJobApplicationRequirements(
        { employerId: this.user.employer_id, isForceRefresh }
      )
      this.jobApplicationRequirements = this.employerStore.getEmployerJobApplicationRequirements({
        employerId: this.user.employer_id
      })
    }
  },
  async mounted () {
    await this.loadApplicationRequirements(false)
    this.isLoaded = true
  },
  setup () {
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    const q = useQuasar()

    return { employerStore, authStore, q, user }
  }
}
</script>
