<template>
  <DialogBase
    :base-title-text="titleText"
    :primary-button-text="(applicationRequirement) ? 'Update' : 'Create'"
    @ok="saveApplicationRequirement"
  >
    <q-form class="q-mt-sm">
      <div class="row q-gutter-y-md">
        <div class="col-12">
          <q-input v-model="formData.application_field_name" label="Field" disable filled/>
        </div>
        <div class="col-12">
          <div class="text-bold">Default</div>
          <q-toggle
            label="Required"
            :model-value="formData.default.is_required"
            @update:model-value="updateDefaults('required', $event)"
          />
          <q-toggle
            label="Optional"
            :model-value="formData.default.is_optional"
            @update:model-value="updateDefaults('optional', $event)"
          />
          <q-toggle
            label="Hidden"
            :model-value="formData.default.is_hidden"
            @update:model-value="updateDefaults('hidden', $event)"
          />
        </div>
        <div class="col-12">
          <div class="text-bold">Overrides</div>
        </div>
        <div v-if="!formData.default.is_required" class="col-12">
          <SeparatorWithText text-position="left">
            <span class="text-bold text-small">
              Required
            </span>
          </SeparatorWithText>
          <div class="row q-gutter-y-md">
            <div class="col-12">
              <SelectJobDepartment v-model="formData.required.departments" :employer-id="employerId"/>
            </div>
            <div class="col-12">
              <SelectJob v-model="formData.required.jobs" :employer-id="employerId"/>
            </div>
          </div>
        </div>
        <div v-if="!formData.default.is_optional" class="col-12">
          <SeparatorWithText text-position="left">
            <span class="text-bold text-small">
              Optional
            </span>
          </SeparatorWithText>
          <div class="row q-gutter-y-md">
            <div class="col-12">
              <SelectJobDepartment v-model="formData.optional.departments" :employer-id="employerId"/>
            </div>
            <div class="col-12">
              <SelectJob v-model="formData.optional.jobs" :employer-id="employerId"/>
            </div>
          </div>
        </div>
        <div v-if="!formData.default.is_hidden" class="col-12">
          <SeparatorWithText text-position="left">
            <span class="text-bold text-small">
              Hidden
            </span>
          </SeparatorWithText>
          <div class="row q-gutter-y-md">
            <div class="col-12">
              <SelectJobDepartment v-model="formData.hidden.departments" :employer-id="employerId"/>
            </div>
            <div class="col-12">
              <SelectJob v-model="formData.hidden.jobs" :employer-id="employerId"/>
            </div>
          </div>
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import SelectJob from 'components/inputs/SelectJob.vue'
import SelectJobDepartment from 'components/inputs/SelectJobDepartment.vue'
import SeparatorWithText from 'components/SeparatorWithText.vue'
import dataUtil from 'src/utils/data.js'
import DialogBase from 'components/dialogs/DialogBase.vue'
import { getAjaxFormData } from 'src/utils/requests.js'

export default {
  name: 'DialogJobApplicationRequirement',
  extends: DialogBase,
  inheritAttrs: false,
  components: { SeparatorWithText, SelectJobDepartment, SelectJob, DialogBase },
  props: {
    applicationRequirement: [Object, null],
    employerId: Number
  },
  data () {
    return {
      formData: {}
    }
  },
  computed: {
    titleText () {
      let text = ''
      if (this.applicationRequirement) {
        text = 'Edit '
      } else {
        text = 'Create '
      }
      return text + 'application requirement'
    }
  },
  methods: {
    async saveApplicationRequirement () {
      const method = (this.applicationRequirement) ? this.$api.put : this.$api.post
      await method('employer/job-application-requirement/', getAjaxFormData({
        ...this.formData,
        employer_id: this.employerId
      }))
      this.$emit('ok')
    },
    updateDefaults (updateKey, val) {
      if (updateKey === 'required') {
        this.formData.default.is_required = val
        if (val) {
          this.formData.default.is_optional = false
          this.formData.default.is_hidden = false
        }
      }
      if (updateKey === 'optional') {
        this.formData.default.is_optional = val
        if (val) {
          this.formData.default.is_required = false
          this.formData.default.is_hidden = false
        }
      }
      if (updateKey === 'hidden') {
        this.formData.default.is_hidden = val
        if (val) {
          this.formData.default.is_optional = false
          this.formData.default.is_required = false
        }
      }
    }
  },
  mounted () {
    if (this.applicationRequirement) {
      this.formData = dataUtil.deepCopy(this.applicationRequirement)
      const formKeys = ['required', 'optional', 'hidden']
      formKeys.forEach((formKey) => {
        const field = this.formData[formKey]
        if (!field) {
          this.formData[formKey] = {
            departments: [],
            jobs: []
          }
        } else {
          field.departments = field.departments || []
          field.jobs = field.jobs || []
        }
      })
      this.formData.application_field_name = dataUtil.capitalize(
        this.applicationRequirement.application_field.split('_').join(' '),
        false
      )
    }
  }
}
</script>
