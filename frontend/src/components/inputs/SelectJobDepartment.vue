<template>
  <q-select
    v-if="isLoaded"
    ref="select"
    :multiple="isMulti" :clearable="isMulti" :use-chips="isMulti"
    filled use-input
    :map-options="isEmitId" :emit-value="isEmitId"
    :new-value-mode="(isAllowCreate) ? 'add-unique' : null"
    :options="departments"
    @filter="filter"
    option-value="id" option-label="name"
    label="Department"
    input-debounce="0"
    @new-value="createDepartment"
    lazy-rules
    :rules="(isRequired) ? [
      (val) => val || 'Job department is required'
    ] : null"
  >
    <template v-if="isAllowCreate" v-slot:no-option="{ inputValue }">
      <q-item clickable @click="createDepartment(inputValue)">
        <q-item-section>
          Create "{{ inputValue }}" department
        </q-item-section>
      </q-item>
    </template>
    <template v-if="isAllowCreate" v-slot:after>
      <CustomTooltip>
        Start typing to filter and/or create a new job department
      </CustomTooltip>
    </template>
  </q-select>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import dataUtil from 'src/utils/data.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useJobStore } from 'stores/job-store.js'

export default {
  name: 'SelectJobDepartment',
  components: { CustomTooltip },
  props: {
    isMulti: {
      type: Boolean,
      default: true
    },
    isAllowCreate: {
      type: Boolean,
      default: false
    },
    isRequired: {
      type: Boolean,
      default: false
    },
    isEmitId: {
      type: Boolean,
      default: false
    },
    employerId: {
      type: [Number, String, null]
    },
    isAll: { // Ignore employer and get all job departments
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoaded: false,
      filterTxt: null,
      authStore: null,
      employerStore: null,
      jobStore: null
    }
  },
  computed: {
    departments () {
      if (!this.isLoaded) {
        return
      }
      let departments = []
      if (this.isAll) {
        departments = this.jobStore.getJobDepartments()
      } else {
        departments = this.employerStore.getEmployerJobDepartments(this.employerId || this.authStore.propUser.employer_id)
      }
      if (!this.filterTxt || this.filterTxt === '') {
        return departments
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return departments.filter((d) => d.name.match(filterRegex))
    }
  },
  methods: {
    filter (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    },
    createDepartment (departmentName) {
      if (!this.isAllowCreate) {
        return
      }
      const newDept = (this.isEmitId) ? departmentName : { id: departmentName, name: departmentName }
      this.filterTxt = null
      this.$refs.select.updateInputValue('')
      let emitValue = newDept
      if (this.isMulti) {
        emitValue = [...dataUtil.getForceArray(this.$refs.select.modelValue), newDept]
      }
      this.$refs.select.$emit('update:modelValue', emitValue)
      this.$refs.select.blur()
    }
  },
  async mounted () {
    this.authStore = useAuthStore()
    this.employerStore = useEmployerStore()
    this.jobStore = useJobStore()
    await this.authStore.setUser()
    const employerId = this.employerId || this.authStore.propUser.employer_id
    if (this.isAll) {
      await this.jobStore.setJobDepartments()
    } else {
      await this.employerStore.setEmployerJobDepartments(employerId)
    }
    this.isLoaded = true
  },
  beforeUnmount () {
    this.$emit('before-unmount')
  }
}
</script>
