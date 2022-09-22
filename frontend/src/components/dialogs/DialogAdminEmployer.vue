<template>
  <DialogBase
    base-title-text="Create new employer"
    primary-button-text="Create"
    :is-valid-form-fn="isValidForm"
    @ok="saveEmployer($event)"
  >
    <q-form ref="form" class="q-gutter-y-sm">
      <q-input
        v-model="formData.name"
        filled
        label="Employer name"
        lazy-rules
        :rules="[ val => val && val.length > 0 || 'Employer name is required']"
      />
      <q-file
        v-model="formData.logo"
        label="Logo"
        class="q-mb-lg"
        :accept="allowedFileExtensionsStr"
        filled
        max-file-size="5000000"
        lazy-rules
      >
        <template v-slot:append>
          <CustomTooltip>
            <ul>
              <li>Supported file types: {{ allowedFileExtensionsStr }}</li>
              <li>Maximum allowable file size is 5MB for a single file</li>
            </ul>
          </CustomTooltip>
        </template>
      </q-file>
      <InputPermittedEmailDomains :employer-data="formData"/>
      <div class="text-bold">
        Account owner
        <CustomTooltip :is_include_space="false">
          This will be the person that will be in charge of setting up the system on the employer's end. They will receive
          employer admin priveleges.
        </CustomTooltip>
      </div>
      <q-input
        filled
        v-model="formData.owner_first_name"
        label="First name"
        lazy-rules
        :rules="[ val => val && val.length > 0 || 'First name is required']"
      />
      <q-input
        filled
        v-model="formData.owner_last_name"
        label="Last name"
        lazy-rules
        :rules="[ val => val && val.length > 0 || 'Last name is required']"
      />
      <q-input
        filled
        v-model="formData.owner_email"
        label="Email"
        lazy-rules
        :rules="[
          val => val && val.length > 0 && formUtil.isGoodEmail(val) || 'Please enter a valid email',
          val => hasPermittedEmail(val) || 'Email address does not have a permitted domain'
        ]"
      />
    </q-form>
  </DialogBase>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'
import InputPermittedEmailDomains from 'pages/employer/settings-page/InputPermittedEmailDomains.vue'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import formUtil from 'src/utils/form.js'
import { getAjaxFormData } from 'src/utils/requests.js'

export default {
  name: 'DialogAdminEmployer',
  extends: DialogBase,
  inheritAttrs: false,
  components: { CustomTooltip, InputPermittedEmailDomains, DialogBase },
  data () {
    return {
      formData: {},
      formUtil
    }
  },
  computed: {
    allowedFileExtensionsStr () {
      return fileUtil.getAllowedFileExtensionsStr([FILE_TYPES.IMAGE.key])
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async saveEmployer () {
      await this.$api.post('admin/employer/', getAjaxFormData(this.formData, ['logo']))
      this.$emit('ok')
    },
    hasPermittedEmail () {
      if (!this.formData.email_domains || !this.formData.owner_email) {
        return false
      }
      const ownerEmailDomain = this.formData.owner_email.split('@').slice(-1)[0]
      const permittedDomains = this.formData.email_domains.split(',')
      for (const permittedDomain of permittedDomains) {
        if (permittedDomain === ownerEmailDomain) {
          return true
        }
      }
      return false
    }
  }
}
</script>
