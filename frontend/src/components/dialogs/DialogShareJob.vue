<template>
  <DialogBase
    base-title-text="Share job"
    :primary-button-text="primaryButtonText"
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
              <template v-if="this.user.business_email">
                <q-select
                  v-model="formData.fromEmail"
                  filled emit-value
                  :options="[
                { val: this.user.email },
                { val: this.user.business_email }
              ]"
                  option-value="val"
                  option-label="val"
                  label="Sent from email"
                />
              </template>
              <q-input
                v-else
                v-model="formData.fromEmail"
                filled disable
                label="Sent from email"
              />
            </div>
            <div class="col-12 col-md-6 q-pl-md-sm">
              <EmailInput v-model="formData.toEmail" label="Send to email"/>
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
        </div>
      </q-form>
    </div>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import EmailInput from 'components/inputs/EmailInput.vue'
import jobsUtil from 'src/utils/jobs.js'
import locationUtil from 'src/utils/location.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useSocialStore } from 'stores/social-store.js'

export default {
  name: 'DialogShareJob',
  extends: DialogBase,
  inheritAttrs: false,
  components: { EmailInput, DialogBase },
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
        emailBody: null
      },
      socialLink: null,
      employerStore: useEmployerStore(),
      employer: null,
      user: null,
      jobsUtil
    }
  },
  computed: {
    jobLocation () {
      if (this.job.locations.length > 1) {
        return 'Multiple locations'
      }
      return locationUtil.getFullLocation(this.job.locations[0])
    },
    primaryButtonText () {
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
    this.socialLinkUrl = socialUtil.getSocialLink(this.shareType, this.socialLink)
    this.employer = this.employerStore.getEmployer(this.job.employer_id)
    this.user = authStore.propUser
    this.formData.fromEmail = this.user.email
    this.formData.emailSubject = `Job opportunity - ${this.job.job_title}`
    this.formData.emailBody = `Hi {name},
My company, ${this.employer.name}, is hiring for a ${this.job.job_title} position and I think you
would be a great fit. If you're interested, you can use this link to view more details and apply:

${this.socialLinkUrl}

If you have any questions, feel free to email me.

Best,
${this.user.first_name}
`
    this.isLoaded = true
  }
}
</script>
