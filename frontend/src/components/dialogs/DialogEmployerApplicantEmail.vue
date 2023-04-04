<template>
  <DialogBase
    :base-title-text="`Send email to ${dataUtil.pluralize('applicant', applicationIds.length)}`"
    primary-button-text="Send"
    :is-valid-form-fn="isValidForm"
    width="800px"
    @ok="sendEmail"
  >
    <q-form ref="form">
      <div class="row q-mt-md">
        <div class="col-12">
          <q-input
            v-model="emailSubject"
            filled label="Email subject"
            :rules="[
              val => val && val.length > 0 || 'Email subject is required'
            ]"
          />
          <WysiwygEditor2 v-model="emailBody"/>
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import dataUtil from 'src/utils/data.js'
import DialogBase from 'components/dialogs/DialogBase.vue'
import WysiwygEditor2 from 'components/inputs/WysiwygEditor2.vue'
import { getAjaxFormData } from 'src/utils/requests.js'

export default {
  name: 'DialogEmployerApplicantEmail',
  extends: DialogBase,
  inheritAttrs: false,
  components: { DialogBase, WysiwygEditor2 },
  props: {
    applicationIds: Array,
    employerId: [Number, String]
  },
  data () {
    return {
      emailSubject: '',
      emailBody: '',
      dataUtil
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async sendEmail () {
      await this.$api.post('email/employer/applicant/', getAjaxFormData({
        emailSubject: this.emailSubject,
        emailBody: this.emailBody,
        application_ids: this.applicationIds,
        employer_id: this.employerId
      }))
    }
  }
}
</script>
