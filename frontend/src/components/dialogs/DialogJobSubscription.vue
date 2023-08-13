<template>
  <DialogBase
    :base-title-text="(jobSubscription) ? 'Edit job subscription' : 'Create job subscription'"
    :primary-button-text="(jobSubscription) ? 'Update' : 'Create'"
    @ok="saveJobSubscription"
  >
    <q-form ref="form">
      <div class="row q-gutter-y-md q-mt-sm">
        <div class="col-12">
          <q-input
            v-model="formData.title"
            autofocus filled label="Subscription title"
          >
            <template v-slot:after>
              <CustomTooltip>
                Used to summarize what this job subscription is for (e.g. "Remote Product Managers")
              </CustomTooltip>
            </template>
          </q-input>
        </div>
        <div class="col-12">
          <SelectJobProfession v-model="formData.job_professions" :is-multi="true" :is-required="true"/>
        </div>
        <div class="col-12">
          <SelectEmployer v-model="formData.employers" :is-multi="true"/>
        </div>
        <div class="col-12">
          <InputLocation
            v-model:location="formData.locations"
            v-model:range_miles="formData.range_miles"
            :is-include-range="true" :is-multi="true"
          />
        </div>
        <div class="col-12">
          <SelectRemote v-model="formData.remote_type_bit"/>
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import InputLocation from 'components/inputs/InputLocation.vue'
import SelectEmployer from 'components/inputs/SelectEmployer.vue'
import SelectJobProfession from 'components/inputs/SelectJobProfession.vue'
import SelectRemote from 'components/inputs/SelectRemote.vue'
import { getAjaxFormData } from 'src/utils/requests.js'

export default {
  name: 'DialogJobSubscription',
  extends: DialogBase,
  inheritAttrs: false,
  components: {
    SelectJobProfession,
    DialogBase,
    InputLocation,
    SelectEmployer,
    SelectRemote
  },
  props: {
    jobSubscription: [Object, null],
    employerId: [Number, null],
    userId: [Number, null]
  },
  data () {
    return {
      formData: {}
    }
  },
  methods: {
    async saveJobSubscription () {
      if (this.jobSubscription) {
        await this.$api.put(`job-subscription/${this.jobSubscription.id}`, getAjaxFormData(this.formData))
      } else {
        await this.$api.post('job-subscription/', getAjaxFormData({
          employer_id: this.employerId,
          user_id: this.userId,
          ...this.formData
        }))
      }
      this.$emit('ok')
    }
  },
  mounted () {
    if (this.jobSubscription) {
      this.formData = Object.assign({ title: this.jobSubscription.title }, this.jobSubscription.filters)

      // Turn filter objects into flat IDs
      const flattenFilterItems = ['jobs', 'employers', 'job_professions']
      flattenFilterItems.forEach((filterKey) => {
        this.formData[filterKey] = this.formData[filterKey].map((item) => item.id)
      })
    }
  }
}
</script>
