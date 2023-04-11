<template>
  <DialogBase
    :base-title-text="`Send email to ${dataUtil.pluralize('applicant', applicationIds.length)}`"
    primary-button-text="Send"
    :is-valid-form-fn="isValidForm"
    width="800px"
    @ok="sendEmail"
  >
    <q-form ref="form">
      <div class="row q-pt-md q-gutter-y-md">
        <div class="col-12">
          <q-select
            v-if="isLoaded"
            v-model="fromEmail"
            label="From address"
            filled emit-value map-options
            :options="emailOptions"
            option-value="val"
            option-label="val"
            :rules="[
              val => val && val.length > 0 || 'Email address is required'
            ]"
          />
          <q-input
            v-model="emailSubject"
            filled label="Email subject"
            :rules="[
              val => val && val.length > 0 || 'Email subject is required'
            ]"
          />
          <WysiwygEditor2 ref="editor" v-model="emailBody" placeholder="Email body"/>
        </div>
        <div class="col-12">
          <BaseExpansionItem
            title="Placeholder content" class="content-expansion q-mt-md"
            :is-include-separator="false"
          >
            <template v-slot:header>
              <CustomTooltip :is_include_space="true">
                This content will be filled in dynamically based on each applicant. Placeholders
                can be used in both the email subject and body.
              </CustomTooltip>
            </template>
            <EmailPlaceholderTable
            :placeholders="[
              emailUtil.PLACEHOLDER_APPLICANT_FIRST_NAME,
              emailUtil.PLACEHOLDER_APPLICANT_LAST_NAME,
              emailUtil.PLACEHOLDER_JOB_TITLE
            ]"
            @addContent="addContent($event)"
          />
          </BaseExpansionItem>
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import BaseExpansionItem from 'components/BaseExpansionItem.vue'
import EmailPlaceholderTable from 'components/EmailPlaceholderTable.vue'
import dataUtil from 'src/utils/data.js'
import DialogBase from 'components/dialogs/DialogBase.vue'
import WysiwygEditor2 from 'components/inputs/WysiwygEditor2.vue'
import emailUtil from 'src/utils/email.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'

export default {
  name: 'DialogEmployerApplicantEmail',
  extends: DialogBase,
  inheritAttrs: false,
  components: { BaseExpansionItem, EmailPlaceholderTable, DialogBase, WysiwygEditor2 },
  props: {
    applicationIds: Array,
    employerId: [Number, String]
  },
  data () {
    return {
      isLoaded: false,
      user: null,
      fromEmail: null,
      emailOptions: [],
      emailSubject: `Application update for ${emailUtil.PLACEHOLDER_JOB_TITLE.placeholder}`,
      emailBody: '',
      dataUtil,
      emailUtil
    }
  },
  methods: {
    addContent (content) {
      this.$refs.editor.insertContent(content)
    },
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async sendEmail () {
      await this.$api.post('email/employer/applicant/', getAjaxFormData({
        emailSubject: this.emailSubject,
        emailBody: this.emailBody,
        from_email: this.fromEmail,
        application_ids: this.applicationIds,
        employer_id: this.employerId
      }))
      this.$emit('ok')
    }
  },
  mounted () {
    const authStore = useAuthStore()
    this.user = authStore.propUser
    if (this.user.connected_emails?.length) {
      this.fromEmail = this.user.connected_emails[0]
      this.emailOptions = this.user.connected_emails.map((email) => ({ val: email }))
    }
    this.isLoaded = true
  }
}
</script>
