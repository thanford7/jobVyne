<template>
  <q-form ref="form">
    <div class="row q-mt-md">
      <template v-if="!isLoggedIn">
        <div class="col-12 q-mb-md">
          <q-input
            filled
            v-model="formData.name"
            label="Name (optional)"
          />
        </div>
        <div class="col-12 q-mb-xs">
          <EmailInput v-model="formData.email"/>
        </div>
      </template>
      <div class="col-12 q-mb-xs">
        <q-input
          v-model="formData.message"
          filled
          autofocus
          type="textarea"
          label="Feedback"
          lazy-rules="ondemand"
          :rules="[
              val => val && val.length > 0 || 'Feedback is required'
            ]"
        />
      </div>
      <div class="col-12 q-mb-xs">
        <q-file
          v-model="formData.files"
          label="Supporting images (optional)"
          :accept="allowedFileExtensionsStr"
          filled multiple counter clearable
          max-file-size="5000000"
          max-total-size="50000000"
        >
          <template v-slot:append>
            <q-icon name="cloud_upload"/>
          </template>
          <template v-slot:after>
            <CustomTooltip :is_include_space="true">
              Screenshots of issues or product ideas are very helpful!
              <ul>
                <li>Supported file types: {{ allowedFileExtensionsStr }}</li>
                <li>Maximum allowable file size is 5MB for a single file</li>
                <li>Maximum allowable file size is 50MB for all files</li>
              </ul>
            </CustomTooltip>
          </template>
        </q-file>
      </div>
      <div v-if="formData?.message?.length" class="col-12">
        <q-btn label="Send feedback" icon="send" color="primary" @click="sendFeedback"/>
      </div>
    </div>
  </q-form>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import EmailInput from 'components/inputs/EmailInput.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import dataUtil from 'src/utils/data.js'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'

export default {
  name: 'FeedbackForm',
  components: { CustomTooltip, EmailInput },
  data () {
    return {
      formData: {}
    }
  },
  computed: {
    allowedFileExtensionsStr () {
      return fileUtil.getAllowedFileExtensionsStr([FILE_TYPES.IMAGE.key])
    },
    isLoggedIn () {
      return this.user && !dataUtil.isEmpty(this.user)
    }
  },
  methods: {
    async sendFeedback () {
      const isValidForm = await this.$refs.form.validate()
      if (!isValidForm) {
        return
      }
      await this.$api.post('feedback/', getAjaxFormData(this.formData, ['files']))
      this.formData = {}
      this.$emit('feedback')
    }
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return {
      user
    }
  }
}
</script>
