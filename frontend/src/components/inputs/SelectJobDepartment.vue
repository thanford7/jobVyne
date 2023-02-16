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
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

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
      type: [String, Number, null]
    }
  },
  data () {
    return {
      isLoaded: false,
      filterTxt: null
    }
  },
  computed: {
    departments () {
      if (!this.isLoaded) {
        return
      }
      const departments = this.employerStore.getEmployerJobDepartments(this.employerId || this.authStore.propUser.employer_id)
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
      const newDept = { id: departmentName, name: departmentName }
      this.filterTxt = null
      this.$refs.select.updateInputValue('')
      this.$refs.select.$emit('update:modelValue', newDept)
      this.$refs.select.blur()
    }
  },
  async mounted () {
    this.authStore = useAuthStore()
    this.employerStore = useEmployerStore()
    await this.authStore.setUser()
    const employerId = this.employerId || this.authStore.propUser.employer_id
    await Promise.all([
      this.employerStore.setEmployerJobs(employerId),
      this.employerStore.setEmployerJobDepartments(employerId)
    ])
    this.isLoaded = true
  },
  beforeUnmount () {
    this.$emit('before-unmount')
  }
}
</script>
