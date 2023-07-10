<template>
  <div v-if="employer">
    <template v-if="!isApplicationSaved">
      <div class="q-pa-sm" :style="getHeaderStyle()">
        <div class="text-h6 text-center">Apply to {{ jobApplication.job_title }}</div>
      </div>
      <div v-if="!authStore.propIsAuthenticated" class="q-pa-sm">
        <a id="jv-form-job-app-login" href="#" @click="openLoginModal">Have an account? Login to auto-populate the
          form</a>
      </div>
      <div class="q-pa-sm q-mt-sm">
        <q-form
          ref="form"
          @submit="saveApplication"
          class="q-gutter-xs"
        >
          <q-input
            v-if="isFieldShown('first_name')"
            filled autofocus
            v-model="formData.first_name"
            class="jv-form-job-app-fname"
            :label="(isFieldOptional('first_name')) ? 'First name*' : 'First name'"
            lazy-rules
            :rules="[ val => isFieldOptional('first_name') || (val && val.length > 0) || 'First name is required']"
          />
          <q-input
            v-if="isFieldShown('last_name')"
            filled
            v-model="formData.last_name"
            class="jv-form-job-app-lname"
            :label="(isFieldOptional('last_name')) ? 'Last name*' : 'Last name'"
            lazy-rules
            :rules="[ val => isFieldOptional('last_name') || (val && val.length > 0) || 'Last name is required']"
          />
          <q-input
            v-if="isFieldShown('email')"
            filled
            v-model="formData.email"
            class="jv-form-job-app-email"
            type="email"
            :label="(isFieldOptional('email')) ? 'Email*' : 'Email'"
            lazy-rules
            :rules="[ val => {
              if (isFieldOptional('email') && (!val?.length || formUtil.isGoodEmail(val))) {
                return true
              } else if (!isFieldOptional('email') && val?.length && formUtil.isGoodEmail(val)) {
                return true
              }
              return 'A valid email is required'
            }]"
          />
          <PhoneInput
            v-if="isFieldShown('phone_number')"
            v-model="formData.phone_number"
            :label="(isFieldOptional('phone_number')) ? 'Phone number*' : 'Phone number'"
            :is-required="!isFieldOptional('phone_number')"
          />
          <InputLinkedIn
            v-if="isFieldShown('linkedin_url')"
            v-model="formData.linkedin_url"
            class="jv-form-job-app-linkedin"
            :label-override="(isFieldOptional('linkedin_url')) ? 'LinkedIn URL*' : 'LinkedIn URL'"
            :is-required="!isFieldOptional('linkedin_url')"
          />
          <FileDisplayOrUpload
            v-if="isFieldShown('resume')"
            ref="resumeUpload"
            :label="(isFieldOptional('resume')) ? 'Resume*' : 'Resume'"
            :file-url="formData.resume_url"
            :new-file="formData.resume"
            :new-file-key="newResumeKey"
            file-url-key="resume_url"
          >
            <template v-slot:fileInput>
              <q-file
                ref="newResumeUpload"
                filled bottom-slots clearable
                v-model="formData.resume"
                :label="(isFieldOptional('resume')) ? 'Resume*' : 'Resume'"
                class="q-mb-none jv-form-job-app-resume"
                :accept="allowedFileExtensionsStr"
                max-file-size="1000000"
                lazy-rules="ondemand"
                :rules="[ val => {
                  if (!this.$refs.resumeUpload.isUpload) {
                    return true
                  }
                  return isFieldOptional('resume') || val || 'A resume is required'
                }]"
              >
                <template v-slot:append>
                  <q-icon name="cloud_upload"/>
                </template>
              </q-file>
            </template>
          </FileDisplayOrUpload>
          <FileDisplayOrUpload
            v-if="isFieldShown('academic_transcript')"
            ref="transcriptUpload"
            :label="(isFieldOptional('academic_transcript')) ? 'Academic transcript*' : 'Academic transcript'"
            :file-url="formData.academic_transcript_url"
            :new-file="formData.academic_transcript"
            :new-file-key="newAcademicTranscriptKey"
            file-url-key="academic_transcript_url"
          >
            <template v-slot:fileInput>
              <q-file
                ref="newTranscriptUpload"
                filled bottom-slots clearable
                v-model="formData.academic_transcript"
                :label="(isFieldOptional('academic_transcript')) ? 'Academic transcript*' : 'Academic transcript'"
                class="q-mb-none jv-form-job-app-resume"
                :accept="allowedFileExtensionsStr"
                max-file-size="1000000"
                lazy-rules="ondemand"
                :rules="[ val => {
                  if (!this.$refs.transcriptUpload.isUpload) {
                    return true
                  }
                  return isFieldOptional('academic_transcript') || val || 'A transcript is required'
                }]"
              >
                <template v-slot:append>
                  <q-icon name="cloud_upload"/>
                </template>
              </q-file>
            </template>
          </FileDisplayOrUpload>
          <div class="text-small text-gray-3">
            *Optional
          </div>

          <div>
            <q-btn
              class="jv-form-job-app-submit"
              ripple label="Submit application"
              :style="getButtonStyle()"
              :loading="isSaving"
              type="submit"
            />
          </div>
        </q-form>
      </div>
    </template>
    <template v-else-if="!authStore.propIsAuthenticated">
      <div class="q-pa-sm" :style="getHeaderStyle()">
        <div class="text-h6 text-center jv-form-job-app-create">Create an account</div>
      </div>
      <div class="q-pa-sm q-mt-sm" :style="getTextStyle()">
        <div class="text-bold">Create an account and save time</div>
        <ListIcon
          icon-name="thumb_up"
          :items="[
              'One click application submission',
              'Message with employees and employers',
              'Track the jobs you\'ve already applied to'
            ]"
        />
        <q-separator/>
        <AuthAll
          class="q-mt-md"
          :is-create="true"
          :style-override="getButtonStyle()"
          :user-type-bit="USER_TYPES[USER_TYPE_CANDIDATE]"
          :user-props="{
            first_name: formData.first_name,
            last_name: formData.last_name
          }"
          :default-email="formData.email"
        />
      </div>
    </template>
    <template v-else-if="isVerifyEmail">
      <div class="q-pa-sm" :style="getHeaderStyle()">
        <div class="text-h6 text-center jv-form-job-app-confirm">Last step</div>
      </div>
      <div class="q-pa-sm q-mt-sm" :style="getTextStyle()">
        <q-icon name="celebration" size="64px"/>
        <div class="text-bold q-mt-md">
          Thanks for creating an account. We just sent you an email to verify your email address. Once you
          verify your email, you will be able to track all of your job applications. Please reload this page
          once you have completed this step.
        </div>
        <q-btn
          class="jv-form-job-app-verify q-mt-md"
          ripple label="Got it"
          :style="getButtonStyle()"
          @click="acknowledgeAndClose()"
        />
      </div>
    </template>
  </div>
</template>

<script>
import InputLinkedIn from 'components/inputs/InputLinkedIn.vue'
import PhoneInput from 'components/inputs/PhoneInput.vue'
import colorUtil from 'src/utils/color.js'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import { getAjaxFormData } from 'src/utils/requests'
import { USER_TYPE_CANDIDATE, USER_TYPES } from 'src/utils/user-types.js'
import { useAuthStore } from 'stores/auth-store'
import { useQuasar } from 'quasar'
import AuthAll from 'components/AuthAll.vue'
import DialogLogin from 'components/dialogs/DialogLogin.vue'
import dataUtil from 'src/utils/data.js'
import formUtil from 'src/utils/form.js'
import ListIcon from 'components/ListIcon.vue'
import FileDisplayOrUpload from 'components/inputs/FileDisplayOrUpload.vue'
import { storeToRefs } from 'pinia/dist/pinia'

const formDataTemplate = {
  first_name: null,
  last_name: null,
  email: null,
  phone_number: '',
  linkedin_url: null,
  resume: null,
  resume_url: null,
  academic_transcript: null,
  academic_transcript_url: null
}

export default {
  name: 'FormJobApplication',
  components: { InputLinkedIn, PhoneInput, FileDisplayOrUpload, AuthAll, ListIcon },
  data () {
    return {
      formData: this.resetFormData(),
      newResumeKey: 'resume',
      newAcademicTranscriptKey: 'academic_transcript',
      isApplicationSaved: false,
      isSaving: false,
      isVerifyEmail: false,
      formUtil,
      USER_TYPES,
      USER_TYPE_CANDIDATE
    }
  },
  props: {
    jobApplication: {
      type: [Object, null]
    },
    employer: Object
  },
  computed: {
    allowedFileExtensionsStr () {
      return fileUtil.getAllowedFileExtensionsStr([FILE_TYPES.FILE.key])
    }
  },
  watch: {
    jobApplication () {
      this.isApplicationSaved = false
    },
    user: {
      handler () {
        this.formData = this.resetFormData()
      },
      deep: true
    }
  },
  methods: {
    openLoginModal () {
      this.q.dialog({
        component: DialogLogin,
        componentProps: {
          redirectPageUrl: window.location.pathname,
          redirectParams: dataUtil.getQueryParams()
        }
      }).onOk(async () => {
        await this.authStore.setUser(true)
        this.$emit('login')
      })
    },
    isFieldShown (fieldKey) {
      return Boolean(this.jobApplication.application_fields[fieldKey]?.is_required) || this.isFieldOptional(fieldKey)
    },
    isFieldOptional (fieldKey) {
      return Boolean(this.jobApplication.application_fields[fieldKey]?.is_optional)
    },
    resetFormData () {
      return Object.assign(
        {},
        formDataTemplate,
        (this.user) ? dataUtil.pick(this.user, ['first_name', 'last_name', 'email']) : {},
        this?.user?.application_template || {}
      )
    },
    getHeaderStyle () {
      const primaryColor = colorUtil.getEmployerPrimaryColor(this.employer)
      return {
        backgroundColor: primaryColor,
        color: colorUtil.getInvertedColor(primaryColor)
      }
    },
    getTextStyle () {
      const primaryColor = colorUtil.getEmployerPrimaryColor(this.employer)
      return { color: primaryColor }
    },
    getButtonStyle () {
      const accentColor = colorUtil.getEmployerAccentColor(this.employer)
      return {
        backgroundColor: accentColor,
        color: colorUtil.getInvertedColor(accentColor)
      }
    },
    acknowledgeAndClose () {
      this.isVerifyEmail = false
      this.$emit('closeApplication')
    },
    async saveApplication () {
      this.isSaving = true

      const isValidForm = await this.$refs.form.validate()
      if (!isValidForm) {
        this.isSaving = false
        return
      }

      const data = Object.assign(
        {
          platform_name: this.$route?.query?.platform,
          referrer_user_id: this.$route?.query?.connect,
          referrer_employer_key: this.$route?.params?.employerKey
        },
        this.formData,
        (this.$refs.resumeUpload) ? this.$refs.resumeUpload.getValues() : {},
        (this.$refs.transcriptUpload) ? this.$refs.transcriptUpload.getValues() : {},
        { job_id: this.jobApplication.id, filter_id: this.$route.params.filterId }
      )

      await this.$api.post('job-application/', getAjaxFormData(data, [this.newResumeKey, this.newAcademicTranscriptKey]))
      await this.authStore.setApplications(this.authStore.propUser, true) // Update user applications and application template
      this.isApplicationSaved = true
      // Leave the drawer open to allow user to create an account if they don't have one
      if (this.authStore.propIsAuthenticated) {
        this.$emit('closeApplication')
      }
      this.isSaving = false
    }
  },
  mounted () {
    this.$global.$on('login', () => {
      this.isVerifyEmail = true
    })
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return {
      authStore,
      user,
      q: useQuasar()
    }
  }
}
</script>
