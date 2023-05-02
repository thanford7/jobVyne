<template>
  <DialogBase
    base-title-text="Upload users"
    primary-button-text="Bulk upload"
    :is-valid-form-fn="isValidForm"
    @ok="uploadUsers"
  >
    <template v-slot:subTitle>
      File must be a CSV and use the headers in the specification (below)
    </template>
    <q-form ref="form">
      <q-file
        ref="userUpload"
        filled bottom-slots clearable
        v-model="userFile"
        label="Users file" class="q-mb-none"
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
    <CollapsableCard flat bordered>
      <template v-slot:header-left>
        User file specification
      </template>
      <template v-slot:body>
        <q-table
          class="w-100"
          flat hide-bottom dense
          :columns="[
            { name: 'name', field: 'name', align: 'left', label: 'Description', sortable: true },
            { name: 'field', field: 'field', align: 'left', label: 'CSV header', sortable: true },
            { name: 'isRequired', field: 'isRequired', align: 'left', label: 'Required', sortable: true },
          ]"
          :rows="[
            { name: 'Email', field: 'email', isRequired: 'Yes' },
            { name: 'First name', field: 'first_name', isRequired: 'Yes' },
            { name: 'Last name', field: 'last_name', isRequired: 'Yes' },
            { name: 'Phone number', field: 'phone_number', isRequired: 'No' },
          ]"
        />
      </template>
    </CollapsableCard>
  </DialogBase>
</template>

<script>
import CollapsableCard from 'components/CollapsableCard.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'

export default {
  name: 'DialogBulkUploadUsers',
  extends: DialogBase,
  inheritAttrs: false,
  components: { CollapsableCard, DialogBase },
  data () {
    return {
      userFile: null,
      fileUtil,
      FILE_TYPES,
      authStore: null
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async uploadUsers () {
      await this.$api.post(
        'employer/user/upload/',
        getAjaxFormData({
          user_file: this.userFile,
          employer_id: this.authStore.propUser.employer_id
        }, ['user_file']))
      this.$emit('ok')
    }
  },
  mounted () {
    this.authStore = useAuthStore()
  }
}
</script>
