<template>
  <DialogBase
    :base-title-text="`${(isEdit) ? 'Update' : 'Add'} review for ${application.first_name} ${application.last_name}`"
    :primary-button-text="`${(isEdit) ? 'Update' : 'Add'}`"
    width="700px"
    @ok="saveReview()"
  >
    <template v-slot:subTitle>
      Your applicant review is only visible to you and your company's HR department. The applicant will never
      see this information.
    </template>
    <div class="text-bold q-mb-md">Application for {{ application.job_title }} position</div>
    <q-form>
      <div class="row q-gutter-y-md">
        <div class="col-12">
          <q-select
            v-model="feedback_know_applicant"
            autofocus
            filled emit-value map-options
            :options="knowApplicantOpts"
            option-value="val"
            option-label="label"
            :label="`Do you know ${application.first_name}?`"
          />
        </div>
        <div class="col-12">
          <q-select
            ref="recommendThis"
            v-model="feedback_recommend_this_job"
            filled emit-value map-options label-slot
            :options="recommendApplicantOpts"
            option-value="val"
            option-label="label"
          >
            <template v-slot:label>
              Would you recommend {{ application.first_name }} for
              <span style="text-decoration: underline">this</span> job?
            </template>
          </q-select>
        </div>
        <div class="col-12">
          <q-select
            ref="recommendAny"
            v-model="feedback_recommend_any_job"
            filled emit-value map-options label-slot
            :options="recommendApplicantOpts"
            option-value="val"
            option-label="label"
          >
            <template v-slot:label>
              Would you recommend {{ application.first_name }} for
              <span style="text-decoration: underline">any</span> job?
            </template>
          </q-select>
        </div>
        <div class="col-12">
          <q-input
            v-model="feedback_note"
            filled autogrow
            :label="`Is there any other information you want to share about ${application.first_name}?`"
            type="textarea"
          />
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import applicantFeedbackUtil from 'src/utils/applicant-feedback.js'
import dataUtil from 'src/utils/data.js'
import DialogBase from 'components/dialogs/DialogBase.vue'
import { getAjaxFormData } from 'src/utils/requests.js'

export default {
  name: 'DialogApplicantReview',
  extends: DialogBase,
  inheritAttrs: false,
  components: { DialogBase },
  props: {
    application: Object,
    isEdit: Boolean
  },
  data () {
    return {
      feedback_know_applicant: null,
      feedback_recommend_any_job: null,
      feedback_recommend_this_job: null,
      feedback_note: null,
      knowApplicantOpts: applicantFeedbackUtil.getKnowApplicantOpts(),
      recommendApplicantOpts: applicantFeedbackUtil.getRecommendApplicantOpts(),
      dataUtil
    }
  },
  watch: {
    feedback_know_applicant (newVal, oldVal) {
      if (newVal !== oldVal && newVal === applicantFeedbackUtil.KNOW_APPLICANT_NO) {
        if (dataUtil.isNil(this.feedback_recommend_any_job)) {
          this.$refs.recommendAny.toggleOption(applicantFeedbackUtil.RECOMMEND_NA, false)
        }
        if (dataUtil.isNil(this.feedback_recommend_this_job)) {
          this.$refs.recommendThis.toggleOption(applicantFeedbackUtil.RECOMMEND_NA, false)
        }
      }
      if (newVal !== oldVal && newVal !== applicantFeedbackUtil.KNOW_APPLICANT_NO) {
        if (this.feedback_recommend_any_job === applicantFeedbackUtil.RECOMMEND_NA) {
          this.$refs.recommendAny.toggleOption(null, false)
        }
        if (this.feedback_recommend_this_job === applicantFeedbackUtil.RECOMMEND_NA) {
          this.$refs.recommendThis.toggleOption(null, false)
        }
      }
    }
  },
  methods: {
    async saveReview () {
      const formData = {
        feedback_know_applicant: this.feedback_know_applicant,
        feedback_recommend_any_job: this.feedback_recommend_any_job,
        feedback_recommend_this_job: this.feedback_recommend_this_job,
        feedback_note: this.feedback_note
      }
      await this.$api.put(`job-application/${this.application.id}`, getAjaxFormData(formData))
      this.$emit('ok')
    }
  },
  mounted () {
    Object.assign(this, this.application.feedback)
  }
}
</script>
