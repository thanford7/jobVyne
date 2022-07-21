<template>
  <div>
    <template v-if="!isApplicationSaved">
      <div class="q-pa-sm bg-primary text-white">
        <div class="text-h6 text-center">Apply to {{ jobApplication.job_title }}</div>
      </div>
      <div v-if="!authStore.propIsAuthenticated" class="q-pa-sm">
        <a href="#" @click="openLoginModal">Have an account? Login to auto-populate the form</a>
      </div>
      <div class="q-pa-sm q-mt-sm">
        <q-form
          @submit="saveApplication"
          class="q-gutter-xs"
        >
          <q-input
            filled
            v-model="formData.first_name"
            label="First name"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'First name is required']"
          />
          <q-input
            filled
            v-model="formData.last_name"
            label="Last name"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Last name is required']"
          />
          <q-input
            filled
            v-model="formData.email"
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
            type="url"
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
            new-file-key="resume"
            file-url-key="resume_url"
          >
            <template v-slot:fileInput>
              <q-file
                filled bottom-slots clearable
                v-model="formData.resume"
                label="Resume"
                class="q-mb-none"
                accept=".pdf,.doc,.docx,.pages,.gdoc"
                max-file-size="1000000"
                :rules="[ val => val || 'A resume is required']"
              />
            </template>
          </FileDisplayOrUpload>
          <div class="text-small text-gray-3">
            *Optional
          </div>

          <div>
            <q-btn ripple label="Submit application" type="submit" color="accent"/>
          </div>
        </q-form>
      </div>
    </template>
    <template v-else-if="!authStore.propIsAuthenticated">
      <div class="q-pa-sm bg-primary text-white">
        <div class="text-h6 text-center">Create an account</div>
      </div>
      <div class="q-pa-sm q-mt-sm">
        <div class="text-bold">Create an account and save time</div>
        <ListIcon
          color="primary"
          icon-name="thumb_up"
          :items="[
              'One click application submission',
              'Message with employees and employers',
              'Track the jobs you\'ve already applied to'
            ]"
        />
        <q-separator/>
        <AuthAll class="q-mt-md" :is-create="true"/>
      </div>
    </template>
  </div>
</template>

<script>
import { getAjaxFormData } from 'src/utils/requests'
import { useAuthStore } from 'stores/auth-store'
import { useQuasar } from 'quasar'
import AuthAll from 'components/AuthAll.vue'
import DialogLogin from 'components/dialogs/DialogLogin.vue'
import dataUtil from 'src/utils/data'
import formUtil from 'src/utils/form'
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
      formData: Object.assign(
        formDataTemplate,
        (this.user) ? dataUtil.pick(this.user, ['first_name', 'last_name', 'email']) : {},
        this?.user?.application_template || {}
      ),
      isApplicationSaved: false,
      formUtil
    }
  },
  props: {
    jobApplication: {
      type: [Object, null]
    }
  },
  watch: {
    jobApplication () {
      this.isApplicationSaved = false
    }
  },
  methods: {
    async saveApplication () {
      const data = Object.assign(
        {},
        this.formData,
        this.$refs.resumeUpload.getValues(),
        { job_id: this.jobApplication.id, filter_id: this.$route.params.filterId }
      )
      await this.$api.post('job-application/', getAjaxFormData(data, ['resume']))
      await this.authStore.setUser(true) // Update user applications and application template
      this.isApplicationSaved = true
      // Leave the drawer open to allow user to create an account if they don't have one
      if (this.authStore.propIsAuthenticated) {
        this.$emit('closeApplication')
      }
    }
  },
  setup () {
    const $q = useQuasar()
    const openLoginModal = () => {
      $q.dialog({
        component: DialogLogin,
        componentProps: {
          redirectPageUrl: window.location.pathname,
          redirectParams: dataUtil.getQueryParams()
        }
      })
    }
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return {
      authStore,
      user,
      openLoginModal
    }
  }
}
</script>