<template>
  <DialogBase
    :base-title-text="titleText"
    :is-include-buttons="false"
  >
    <q-table
      flat
      :columns="connectionColumns"
      :rows="jobConnections"
      :rows-per-page-options="[15]"
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            <template v-if="col.name === 'connectionName'">
              <a v-if="props.row.user_key" :href="`/jv/${props.row.user_key}`" target="_blank">{{ col.value }}</a>
              <span v-else>{{ col.value }}</span>
              <div v-if="props.row.linkedin_url" class="text-small">
                <a :href="props.row.linkedin_url" target="_blank">LinkedIn</a>
              </div>
            </template>
            <template v-else-if="col.name === 'connectionType'">
              {{ CONNECTION_TYPES[col.value].name }}
              <div v-if="props.row.owner" class="text-small">
                <a v-if="props.row.owner.user_key" :href="`/jv/${props.row.owner.user_key}`" target="_blank">
                  {{ props.row.owner.full_name }}
                </a>
                knows this person
              </div>
            </template>
            <template v-else>
              <span>{{ col.value }}</span>
            </template>
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import { CONNECTION_TYPES } from 'src/utils/community.js'
import { useCommunityStore } from 'stores/community-store.js'

export default {
  name: 'DialogShowEmployerConnections',
  extends: DialogBase,
  inheritAttrs: false,
  components: { DialogBase },
  data () {
    return {
      jobConnections: [],
      CONNECTION_TYPES
    }
  },
  props: {
    job: Object
  },
  computed: {
    titleText () {
      return `Connections for ${this.job.job_title}`
    },
    connectionColumns () {
      return [
        { name: 'connectionName', field: 'full_name', align: 'left', label: 'Name', sortable: true },
        {
          name: 'connectionType',
          field: 'connection_type',
          align: 'left',
          label: 'Connection',
          sortable: true,
          format: (val) => val || 'Unknown'
        },
        {
          name: 'profession',
          field: (conn) => conn.profession?.name || 'Unknown',
          align: 'left',
          label: 'Profession',
          sortable: true
        },
        {
          name: 'jobTitle',
          field: 'job_title',
          align: 'left',
          label: 'Job Title',
          sortable: true
        }
      ]
    }
  },
  methods: {},
  async mounted () {
    const communityStore = useCommunityStore()
    await communityStore.setJobConnections({ jobId: this.job.id })
    this.jobConnections = communityStore.getJobConnections({ jobId: this.job.id })
  }
}
</script>
