<template>
  <div v-if="employer">
    <template v-if="!isApplicationSaved">
      <div class="q-pa-sm" :style="getHeaderStyle()">
        <div class="text-h6 text-center">Apply to {{ jobApplication.job_title }}</div>
      </div>
      <div v-if="!authStore.propIsAuthenticated" class="q-pa-sm">
        <a id="jv-form-job-app-login" href="#" @click="openLoginModal">Have an account? Login to auto-populate the form</a>
      </div>
      <div class="q-pa-sm q-mt-sm">
        <q-form
          @submit="saveApplication"
          class="q-gutter-xs"
        >
          <q-input
            filled
            v-model="formData.first_name"
            class="jv-form-job-app-fname"
            label="First name"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'First name is required']"
          />
          <q-input
            filled
            v-model="formData.last_name"
            class="jv-form-job-app-lname"
            label="Last name"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Last name is required']"
          />
          <q-input
            filled
            v-model="formData.email"
            class="jv-form-job-app-email"
            type="email"
            label="Email"
            lazy-rules
            :rules="[ val => val && val.length > 0 && formUtil.isGoodEmail(val) || 'A valid email is required']"
          />
          <q-input
            filled
            v-model="formData.phone_number"
            type="tel"
            label="Phone number*"
            lazy-rules
            :rules="[ val => !val || !val.length || formUtil.isGoodPhoneNumber(val) || 'The phone number must be valid']"
          />
          <q-input
            filled
            v-model="formData.linkedin_url"
            class="jv-form-job-app-linkedin"
            label="LinkedIn URL*"
            hint="www.linkedin.com/in/{your profile id}"
            lazy-rules
            :rules="[ val => !val || !val.length || formUtil.isGoodLinkedInUrl(val)  || 'The LinkedIn URL must be valid']"
          />
          <FileDisplayOrUpload
            ref="resumeUpload"
            label="resume"
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
                label="Resume"
                class="q-mb-none jv-form-job-app-resume"
                :accept="allowedResumeExtensionsStr"
                max-file-size="1000000"
                lazy-rules="ondemand"
                :rules="[ val => val || 'A resume is required']"
              />
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
  phone_number: null,
  linkedin_url: null,
  resume: null,
  resume_url: null
}

export default {
  name: 'FormJobApplication',
  components: { FileDisplayOrUpload, AuthAll, ListIcon },
  data () {
    return {
      formData: this.resetFormData(),
      newResumeKey: 'resume',
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
    allowedResumeExtensionsStr () {
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
      const data = Object.assign(
        {},
        this.formData,
        this.$refs.resumeUpload.getValues(),
        { job_id: this.jobApplication.id, filter_id: this.$route.params.filterId }
      )

      // Make sure a resume is uploaded if existing resume is not being used
      if (this.$refs.resumeUpload.isUpload && !this.$refs.newResumeUpload.validate()) {
        this.isSaving = false
        return
      }

      await this.$api.post('job-application/', getAjaxFormData(data, [this.newResumeKey]))
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
