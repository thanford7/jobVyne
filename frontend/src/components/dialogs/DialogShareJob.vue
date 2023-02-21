<template>
  <DialogBase
    base-title-text="Share job"
    :primary-button-text="primaryBtnText"
    :is-include-buttons="hasButtons"
    width="700px"
    :is-valid-form-fn="isValidForm"
    @ok="shareJob"
  >
    <template v-slot:subTitle>
      {{ job.job_title }} - {{ jobLocation }}
    </template>
    <div class="q-mt-sm">
      <q-form v-if="isLoaded" ref="form">
        <div class="row q-gutter-y-sm">
          <template v-if="shareType === jobsUtil.shareTypes.EMAIL">
            <div class="col-12 col-md-6 q-pr-md-sm">
              <q-input
                v-model="formData.fromEmail"
                filled disable
                label="Sent from email"
              >
                <template v-slot:after>
                  <CustomTooltip>
                    Email must come from a JobVyne email address. If you want to send an email from your
                    own email address, copy the subject and message below and use your own email messenger (e.g. Gmail).
                  </CustomTooltip>
                </template>
              </q-input>
            </div>
            <div class="col-12 col-md-6 q-pl-md-sm">
              <EmailInput v-model="formData.toEmail" label="Send to email" autofocus/>
            </div>
            <div class="col-12">
              <q-input
                v-model="formData.emailSubject"
                filled label="Email subject"
                :rules="[(val) => val && val.length || 'An email subject is required']"
              />
            </div>
            <div class="col-12">
              <q-input
                v-model="formData.emailBody"
                filled autogrow label="Email message"
                type="textarea"
                :rules="[
                  (val) => val && val.length || 'An email message is required',
                  (val) => !val.includes('{name}') || 'Remember to update the {name} of your recipient'
                ]"
              />
            </div>
          </template>
          <template v-if="shareType === jobsUtil.shareTypes.SMS">
            <div class="col-12">
              <PhoneInput v-model="formData.phoneNumber" :is-auto-focus="true" :is-required="true"/>
            </div>
            <div class="col-12">
              <q-input
                v-model="formData.textBody"
                filled autogrow label="Text message"
                type="textarea"
                :rules="[
                    (val) => val && val.length || 'An text message is required',
                    (val) => !val.includes('{name}') || 'Remember to update the {name} of your recipient'
                  ]"
              />
            </div>
          </template>
          <template v-if="shareType === jobsUtil.shareTypes.QR">
            <div class="col-12 text-center">
              <QrCode :qr-value="socialLinkUrl"/>
            </div>
          </template>
          <template v-if="shareType === jobsUtil.shareTypes.LINK">
            <div class="col-12">
              <div>
                <q-input
                  v-model="socialLinkUrl"
                  filled disable
                  label="Job link"
                >
                  <template v-slot:after>
                    <q-btn flat stretch icon="content_copy" @click="dataUtil.copyText(socialLinkUrl)"/>
                  </template>
                </q-input>
              </div>
            </div>
            <div class="col-12">
              <q-input
                v-model="shortMessage"
                filled autogrow label="Message"
                type="textarea"
              >
                <template v-slot:after>
                  <q-btn flat stretch icon="content_copy" @click="dataUtil.copyText(shortMessage)"/>
                </template>
              </q-input>
            </div>
          </template>
        </div>
      </q-form>
    </div>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import EmailInput from 'components/inputs/EmailInput.vue'
import PhoneInput from 'components/inputs/PhoneInput.vue'
import QrCode from 'components/QrCode.vue'
import dataUtil from 'src/utils/data.js'
import jobsUtil from 'src/utils/jobs.js'
import locationUtil from 'src/utils/location.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'DialogShareJob',
  extends: DialogBase,
  inheritAttrs: false,
  components: { PhoneInput, QrCode, EmailInput, DialogBase },
  props: {
    job: Object,
    shareType: String
  },
  data () {
    return {
      isLoaded: false,
      formData: {
        fromEmail: null,
        toEmail: null,
        emailSubject: null,
        emailBody: null,
        phoneNumber: null,
        textBody: null
      },
      shortMessage: null,
      socialLink: null,
      socialLinkUrl: null,
      employerStore: useEmployerStore(),
      employer: null,
      user: null,
      dataUtil,
      jobsUtil
    }
  },
  computed: {
    hasButtons () {
      return [jobsUtil.shareTypes.EMAIL, jobsUtil.shareTypes.SMS].includes(this.shareType)
    },
    jobLocation () {
      if (this.job.locations.length > 1) {
        return 'Multiple locations'
      }
      return locationUtil.getFullLocation(this.job.locations[0])
    },
    primaryBtnText () {
      if (this.shareType === jobsUtil.shareTypes.EMAIL) {
        return 'Send email'
      } else {
        return 'Send text'
      }
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async shareJob () {
      await this.$api.post('social-link/share/', getAjaxFormData(Object.assign(
        {}, this.formData,
        { socialLinkId: this.socialLink.id, shareType: this.shareType }
      )))
    }
  },
  async mounted () {
    const authStore = useAuthStore()
    const globalStore = useGlobalStore()
    const socialStore = useSocialStore()
    await Promise.all([
      authStore.setUser(),
      this.employerStore.setEmployer(this.job.employer_id)
    ])
    this.socialLink = await socialStore.getOrCreateSocialLinkFilter({
      owner_id: authStore.propUser.id,
      employer_id: this.job.employer_id,
      job_ids: [this.job.id],
      is_get_or_create: true
    })
    this.socialLinkUrl = socialUtil.getJobLinkUrl(this.socialLink, { platform: this.shareType })
    this.employer = this.employerStore.getEmployer(this.job.employer_id)
    this.user = authStore.propUser
    this.shortMessage = `My company, ${this.employer.name}, is hiring for a ${this.job.job_title} position and I think you would be a great fit. If you're interested, you can use this link to view more details and apply:

${this.socialLinkUrl}`
    this.formData.textBody = `(Sent by ${this.user.first_name} ${this.user.last_name})
Hi {name},
${this.shortMessage}
    `
    this.formData.fromEmail = globalStore.emailReferral
    this.formData.emailSubject = `Job opportunity - ${this.job.job_title} - From ${this.user.first_name} ${this.user.last_name}`
    this.formData.emailBody = `Hi {name},
${this.shortMessage}

If you have any questions, feel free to email me at ${this.user.email}

Best,
${this.user.first_name} ${this.user.last_name}
`
    this.isLoaded = true
  }
}
</script>
