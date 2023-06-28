<template>
  <div style="display: inline-block">
    <template v-if="departments.length > condenseDepartmentLimit">
      <CustomTooltip>
        <template v-slot:icon>
          <q-chip
            color="grey-7" text-color="white" size="md" :icon="icon" :dense="isDense"
          >
            Multiple departments&nbsp;
            <span v-if="utilStore.isUnderBreakPoint('md')">(press to view)</span>
            <span v-else>(hover to view)</span>
          </q-chip>
        </template>
        <ul>
          <li v-for="department in departments">
            {{ department.name }}
          </li>
        </ul>
      </CustomTooltip>
    </template>
    <template v-else-if="departments.length">
      <q-chip
        v-for="department in departments"
        color="grey-7" text-color="white" size="md" :icon="icon"
        :dense="isDense"
      >
        {{ department.name }}
      </q-chip>
    </template>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import { useUtilStore } from 'stores/utility-store.js'

export default {
  name: 'DepartmentChip',
  components: { CustomTooltip },
  props: {
    departments: Array,
    isDense: {
      type: Boolean,
      default: false
    },
    icon: {
      type: [String, null]
    },
    // The max departments to show before showing one chip with "Multiple departments"
    condenseDepartmentLimit: {
      type: Number,
      default: 1
    }
  },
  data () {
    return {
      utilStore: useUtilStore()
    }
  }
}
</script>
