<template>
  <DialogBase
    :base-title-text="`${(job) ? 'Edit' : 'Add'} job for ${employer.name}`"
    :primary-button-text="`${(job) ? 'Update' : 'Add'}`"
    :is-full-screen="true"
    :is-valid-form-fn="isValidForm"
    @ok="saveJob"
  >
    <q-form ref="form">
      <div class="row q-gutter-y-md q-mt-sm">
        <div class="col-12 col-md-6 q-pr-md-sm">
          <q-input
            v-model="formData.job_title"
            filled label="Job title" lazy-rules
            :rules="[ val => val && val.length > 0 || 'Job title is required']"
          />
        </div>
        <div class="col-12 col-md-6 q-pl-md-sm">
          <SelectJobDepartment
            v-model="formData.job_department"
            :is-multi="false" :is-allow-create="true" :is-required="true"
          />
        </div>
        <div class="col-12 col-md-6 q-pr-md-sm">
          <DateSelector v-model="formData.open_date" label="Open date" :is-required="true"/>
        </div>
        <div class="col-12 col-md-6 q-pl-md-sm">
          <DateSelector
            v-model="formData.close_date"
            label="Close date"
            :additional-rules="[
              (val) => (!val || dateTimeUtil.isAfter(val, formData.open_date, { isIncludeTime: false })) || 'Close date must be after open date'
            ]"
          />
        </div>
        <div class="col-12">
          <q-toggle v-model="isAddSalary" label="Add salary range"/>
          <CustomTooltip :is_include_space="true">
            Salary can mean salary, remuneration, compensation, or stipend
          </CustomTooltip>
        </div>
        <template v-if="isAddSalary">
          <div class="col-12 col-md-4 q-pr-md-sm">
            <MoneyInput
              v-model:money-value="formData.salary_floor"
              v-model:currency-name="formData.salary_currency"
              :precision="2"
              label="Min salary"
              :is-required="isAddSalary"
            />
          </div>
          <div class="col-12 col-md-4 q-px-md-sm">
            <MoneyInput
              v-model:money-value="formData.salary_ceiling"
              v-model:currency-name="formData.salary_currency"
              :precision="2"
              label="Max salary" :is-include-currency-selection="false"
              :is-required="isAddSalary"
            />
          </div>
          <div class="col-12 col-md-4 q-pl-md-sm">
            <q-select
              v-model="formData.salary_interval"
              filled label="Salary interval"
              option-label="label" option-value="val" map-options emit-value
              :options="[
                { val: 'year', label: 'Yearly' },
                { val: 'month', label: 'Monthly' },
                { val: 'week', label: 'Weekly' },
                { val: 'hour', label: 'Hourly' },
                { val: 'once', label: 'One time'}
              ]"
              lazy-rules
              :rules="(isAddSalary) ? [
                (val) => dataUtil.getBoolean(val) || 'Salary interval is required'
              ] : null"
            />
          </div>
        </template>
        <div class="col-12 col-md-6 q-pr-md-sm">
          <q-select
            v-model="formData.employment_type"
            filled label="Employment type"
            option-label="val" option-value="val" map-options emit-value
            :options="[
              { val: 'Full Time' },
              { val: 'Part Time' },
              { val: 'Internship' },
              { val: 'Contract' }
            ]"
            lazy-rules
            :rules="[
              (val) => dataUtil.getBoolean(val) || 'Employment type is required'
            ]"
          />
        </div>
        <div class="col-12 col-md-6 q-pl-md-sm">
          <SelectLocation
            v-model="formData.locations" :locations="locations || []"
            :is-multi="true" :is-allow-create="true"
          />
        </div>
        <div class="col-12">
          <WysiwygEditor2 v-model="formData.job_description" placeholder="Job description"/>
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import DateSelector from 'components/inputs/DateSelector.vue'
import MoneyInput from 'components/inputs/MoneyInput.vue'
import SelectJobDepartment from 'components/inputs/SelectJobDepartment.vue'
import SelectLocation from 'components/inputs/SelectLocation.vue'
import WysiwygEditor2 from 'components/inputs/WysiwygEditor2.vue'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import locationUtil from 'src/utils/location.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'DialogJob',
  extends: DialogBase,
  inheritAttrs: false,
  components: { SelectLocation, MoneyInput, DateSelector, SelectJobDepartment, WysiwygEditor2, DialogBase },
  props: {
    employerId: Number,
    job: [Object, null]
  },
  data () {
    return {
      formData: {
        open_date: dateTimeUtil.serializeDate(dateTimeUtil.now()),
        job_description: '',
        salary_currency: 'USD'
      },
      isAddSalary: false,
      employer: {},
      locations: null,
      employerStore: useEmployerStore(),
      dataUtil,
      dateTimeUtil
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async saveJob () {
      const data = Object.assign(
        { employer_id: this.employerId },
        dataUtil.omit(
          this.formData,
          (!this.isAddSalary) ? ['salary_floor', 'salary_ceiling', 'salary_interval', 'salary_currency'] : []
        )
      )
      data.open_date = dateTimeUtil.serializeDate(data.open_date, { isUTC: false })
      data.close_date = (data.close_date) ? dateTimeUtil.serializeDate(data.close_date, { isUTC: false }) : null
      const method = (this.job) ? this.$api.put : this.$api.post
      await method('employer/job/', getAjaxFormData(data))
      this.$emit('ok')
    }
  },
  async mounted () {
    await Promise.all([
      this.employerStore.setEmployer(this.employerId),
      this.employerStore.setEmployerJobs(this.employerId)
    ])
    this.employer = this.employerStore.getEmployer(this.employerId)
    this.locations = this.employerStore.getJobLocations(this.employerId)
    if (this.job) {
      this.formData = Object.assign(this.formData, this.job)
      this.formData.locations = (this.formData.locations || []).map((loc) => locationUtil.getFullLocation(loc))
      this.formData.salary_currency = this.job?.salary_currency?.name
      this.formData.open_date = dateTimeUtil.getShortDate(this.formData.open_date, dateTimeUtil.serializeDateFormat)
      if (this.formData.close_date?.length) {
        this.formData.close_date = dateTimeUtil.getShortDate(this.formData.close_date, dateTimeUtil.serializeDateFormat)
      }
      this.formData.job_department = {
        id: this.job.job_department_id,
        name: this.job.job_department
      }
      if (this.formData.salary_floor) {
        this.isAddSalary = true
      }
    }
  }
}
</script>
