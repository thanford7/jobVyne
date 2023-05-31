<template>
  <DialogBase
    base-title-text="Send referral request"
    primary-button-text="Send"
    :is-full-screen="true"
    :is-valid-form-fn="isValidForm"
    @ok="sendRequest"
  >
    <q-form ref="form">
      <div class="row q-mt-md">
        <div class="col-md-8 col-12 q-pr-md-sm">
          <q-input
            v-model="emailSubject"
            filled label="Email subject"
            :rules="[
              val => val && val.length > 0 || 'Email subject is required'
            ]"
          />
          <WysiwygEditor2 v-model="emailBody" ref="editor"/>
          <ErrorCallout ref="emailBodyError" :error-text="emailBodyErrorText"/>
          <BaseExpansionItem
            title="Placeholder content" class="content-expansion q-mt-md"
            :is-include-separator="false"
          >
            <template v-slot:header>
              <CustomTooltip :is_include_space="true">
                This content will be filled in dynamically based on the employee's unique
                link and the job filters.
              </CustomTooltip>
            </template>
            <EmailPlaceholderTable
              :placeholders="[
                emailUtil.PLACEHOLDER_EMPLOYEE_FIRST_NAME,
                emailUtil.PLACEHOLDER_EMPLOYEE_LAST_NAME,
                emailUtil.PLACEHOLDER_JOB_LINK,
                emailUtil.PLACEHOLDER_JOBS_LIST
              ]"
              @addContent="addContent($event)"
            />
          </BaseExpansionItem>
        </div>
        <div class="col-md-4 col-12 q-pl-md-sm q-mt-md q-mt-md-none">
          <BaseExpansionItem
            :is-include-separator="false"
            title="Email filters" class="content-expansion"
          >
            <template v-slot:header>
              <CustomTooltip :is_include_space="true">
                Select the employees you want to send the referral request to.
                If you want to send to all employees, leave the filter empty.
              </CustomTooltip>
            </template>
            <div>
              <q-icon name="info" color="gray-300" size="16px"/>
              Send to {{ dataUtil.pluralize('employee', sendEmployeeCount) }}
            </div>
            <SelectEmployee
              v-model="userFilters.user_ids"
              class="q-mb-md q-mt-sm"
              :employer-id="employerId" :is-multi="true"
            />
          </BaseExpansionItem>
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import BaseExpansionItem from 'components/BaseExpansionItem.vue'
import CustomTooltip from 'components/CustomTooltip.vue'
import EmailPlaceholderTable from 'components/EmailPlaceholderTable.vue'
import ErrorCallout from 'components/ErrorCallout.vue'
import dataUtil from 'src/utils/data.js'
import DialogBase from 'components/dialogs/DialogBase.vue'
import SelectEmployee from 'components/inputs/SelectEmployee.vue'
import WysiwygEditor2 from 'components/inputs/WysiwygEditor2.vue'
import emailUtil from 'src/utils/email.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'DialogShareJobLink',
  extends: DialogBase,
  inheritAttrs: false,
  components: {
    EmailPlaceholderTable,
    BaseExpansionItem,
    ErrorCallout,
    DialogBase,
    WysiwygEditor2,
    CustomTooltip,
    SelectEmployee
  },
  props: {
    employerId: [Number, String]
  },
  data () {
    return {
      employer: null,
      emailSubject: '',
      emailBody: '',
      emailBodyErrorText: null,
      userFilters: {
        user_ids: null
      },
      employerStore: null,
      dataUtil,
      emailUtil
    }
  },
  computed: {
    sendEmployeeCount () {
      if (this.userFilters.user_ids) {
        return this.userFilters.user_ids.length
      }
      const employees = this.employerStore.getEmployees(this.employerId)
      return employees?.length
    }
  },
  watch: {
    emailBody () {
      if (!this.emailBody.includes(emailUtil.PLACEHOLDER_JOB_LINK.placeholder)) {
        this.emailBodyErrorText = 'The email message must include the jobs page link placeholder'
      } else if (!this.emailBody?.length) {
        this.emailBodyErrorText = 'An email message is required'
      } else {
        this.emailBodyErrorText = null
      }
    }
  },
  methods: {
    addContent (content) {
      this.$refs.editor.insertContent(content)
    },
    async isValidForm () {
      const isValid = await this.$refs.form.validate()
      if (!isValid) {
        return false
      }
      if (this.emailBodyErrorText) {
        this.$refs.emailBodyError.shake()
        return false
      }
      return true
    },
    async sendRequest () {
      const formData = {
        employer_id: this.employerId,
        email_subject: this.emailSubject,
        email_body: this.emailBody,
        ...this.userFilters
      }
      await this.$api.post('employer/referral/request/', getAjaxFormData(formData))
      await this.employerStore.setEmployerReferralRequests(this.employerId, true)
      this.$emit('ok')
    }
  },
  async mounted () {
    this.employerStore = useEmployerStore()
    await Promise.all([
      this.employerStore.setEmployer(this.employerId),
      this.employerStore.setEmployees(this.employerId)
    ])
    this.employer = this.employerStore.getEmployer(this.employerId)
    this.emailSubject = `Help us hire at ${this.employer.name}! Share your personal referral link`
    this.emailBody = `
      <p>Hi ${emailUtil.PLACEHOLDER_EMPLOYEE_FIRST_NAME.placeholder},</p>
      <p>
        We are using JobVyne to help hire for ${this.employer.name}. The link below is personalized
        specifically for you and allows anyone to click the link to view and apply for open jobs at
        our company including:
      </p>
      <p>${emailUtil.PLACEHOLDER_JOBS_LIST.placeholder}</p>
      <p>
        Please help us hire by sharing your personal referral link directly with your professional network
        and also across professional social media sites like LinkedIn.
      </p>
      <p>
        Your referral link: ${emailUtil.PLACEHOLDER_JOB_LINK.placeholder}
      </p>
      <p>
        Thanks for helping us grow!
      </p>
    `
  }
}
</script>
