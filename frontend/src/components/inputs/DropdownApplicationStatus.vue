<template>
  <q-btn-dropdown
    :label="statusLabel"
    color="blue-7" rounded split
    padding="2px 16px"
  >
    <q-list>
      <q-item
        v-for="status in statusOptions"
        clickable v-close-popup
        @click="$emit('update:model-value', status.val)"
      >
        <q-item-section>
          <q-item-label>{{ status.label }}</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-btn-dropdown>
</template>

<script>
import applicationUtil from 'src/utils/application.js'
import dataUtil from 'src/utils/data.js'

export default {
  name: 'DropdownApplicationStatus',
  props: {
    modelValue: String,
    isEmployer: Boolean
  },
  data () {
    return {
      applicationUtil
    }
  },
  computed: {
    statusLabel () {
      return applicationUtil.APPLICATION_STATUSES[this.modelValue]?.label || dataUtil.capitalize(this.modelValue)
    },
    statusOptions () {
      if (this.isEmployer) {
        return Object.values(applicationUtil.APPLICATION_STATUSES).filter((val) => val.isEmployerValue)
      }
      return Object.values(applicationUtil.APPLICATION_STATUSES).filter((val) => val.isCandidateValue)
    }
  }
}
</script>
