<template>
  <DialogBase
    base-title-text="Upload connections"
    primary-button-text="Upload"
    :is-valid-form-fn="isValidForm"
    @ok="uploadConnections"
  >
    <template v-slot:subTitle>
      Go to <a href="https://www.linkedin.com/mypreferences/d/download-my-data" target="_blank">LinkedIn Data Download</a> to
      download a copy of your connections
    </template>
    <q-form ref="form">
      <q-file
        ref="connectionsUpload"
        filled bottom-slots clearable
        v-model="connectionsFile"
        label="Connections file" class="q-mb-none"
        accept=".csv"
        lazy-rules="ondemand"
        :rules="[val => val || 'A file is required']"
        max-file-size="1000000"
      >
        <template v-slot:append>
          <q-icon name="cloud_upload"/>
        </template>
      </q-file>
    </q-form>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'

export default {
  name: 'DialogBulkUploadLinkedInContacts',
  extends: DialogBase,
  inheritAttrs: false,
  components: { DialogBase },
  data () {
    return {
      connectionsFile: null,
      fileUtil,
      FILE_TYPES,
      authStore: null
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async uploadConnections () {
      await this.$api.post(
        'community/job-connections/',
        getAjaxFormData({
          connections_file: this.connectionsFile
        }, ['connections_file']))
      this.$emit('ok')
    }
  },
  mounted () {
    this.authStore = useAuthStore()
  }
}
</script>
