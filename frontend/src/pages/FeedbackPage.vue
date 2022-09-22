<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Feedback">
        We want to hear from you! If there is an issue, we will work to fix it as quickly as possible. If you have a
        feature request or product idea, we will consider it for our roadmap.
      </PageHeader>
      <div class="row q-mt-md">
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
              <CustomTooltip>
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
    </div>
  </q-page>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import PageHeader from 'components/PageHeader.vue'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import { getAjaxFormData } from 'src/utils/requests.js'

export default {
  name: 'FeedbackPage',
  components: { CustomTooltip, PageHeader },
  data () {
    return {
      formData: {}
    }
  },
  computed: {
    allowedFileExtensionsStr () {
      return fileUtil.getAllowedFileExtensionsStr([FILE_TYPES.IMAGE.key])
    }
  },
  methods: {
    async sendFeedback () {
      await this.$api.post('feedback/', getAjaxFormData(this.formData, ['files']))
      this.formData = {}
    }
  }
}
</script>
