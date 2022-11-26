<template>
  <q-input
    filled
    :label="label"
    mask="##/####"
    hint="Month/Year e.g. 02/2018"
    :model-value="monthYearText"
    @update:model-value="emitUpdate($event)"
  />
</template>

<script>
import dateTimeUtil from 'src/utils/datetime.js'

export default {
  name: 'SelectMonthYear',
  props: {
    label: String,
    modelValue: [null, String]
  },
  data () {
    return {
      monthYearText: null
    }
  },
  methods: {
    emitUpdate (val) {
      if (!val || val.length !== 7) {
        this.monthYearText = val
        this.$emit('update:model-value', null)
      } else {
        const [monthText, yearText] = val.split('/')
        const month = parseInt(monthText)
        const year = parseInt(yearText)
        if (month > 12 || month < 1) {
          this.monthYearText = null
          this.$emit('update:model-value', null)
        } else if (year > dateTimeUtil.getCurrentYear() || year < 1900) {
          this.monthYearText = null
          this.$emit('update:model-value', null)
        }
        this.$emit('update:model-value', `${yearText}-${monthText}-01`)
      }
    }
  },
  mounted () {
    if (this.modelValue) {
      // eslint-disable-next-line no-unused-vars
      const [year, month, day] = this.modelValue.split('-')
      this.monthYearText = `${month}/${year}`
    } else {
      this.monthYearText = null
    }
  }
}
</script>
