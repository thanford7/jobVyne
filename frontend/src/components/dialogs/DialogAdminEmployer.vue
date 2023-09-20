<template>
  <DialogBase
    :base-title-text="(employer) ? 'Edit employer' : 'Create new employer'"
    :primary-button-text="(employer) ? 'Update' : 'Create'"
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
      <q-input
        v-model="formData.name_aliases"
        filled
        label="Alternate employer names"
        hint="Pipe (|) separated list of names"
        lazy-rules
      />
      <SelectOrganizationType v-model="formData.organization_type"/>
      <FileDisplayOrUpload
        ref="logoUpload"
        label="logo"
        :file-url="formData.logo_url"
        :new-file="formData[newLogoKey]"
        :new-file-key="newLogoKey"
        file-url-key="logo_url"
      >
        <template v-slot:fileInput>
          <q-file
            ref="newLogoUpload"
            filled bottom-slots clearable
            v-model="formData[newLogoKey]"
            label="Logo"
            class="q-mb-none"
            :accept="allowedFileExtensionsStr"
            lazy-rules
            max-file-size="5000000"
          >
            <template v-slot:append>
              <q-icon name="cloud_upload"/>
            </template>
            <template v-slot:after>
              <CustomTooltip :is_include_space="true">
                <ul>
                  <li>Supported file types: {{ allowedFileExtensionsStr }}</li>
                  <li>Maximum allowable file size is 5MB for a single file</li>
                </ul>
              </CustomTooltip>
            </template>
          </q-file>
        </template>
      </FileDisplayOrUpload>
      <InputPermittedEmailDomains :employer-data="formData"/>
      <SelectYesNo v-model="formData.is_use_job_url" label="Use job url" :is-multi="false">
        <template v-slot:after>
          <CustomTooltip>
            If this employer doesn't have a direct account with JobVyne, set this to "Yes". This
            allows job seekers to apply to jobs that have been scraped, but the employer doesn't
            have a JobVyne account or integration.
          </CustomTooltip>
        </template>
      </SelectYesNo>
      <template v-if="canUpdateSubscription">
        <div class="text-bold">
          Subscription
          <CustomTooltip>
            Set the number of free employee seats the employer will receive. Once an employer signs up for a paid
            subscription,
            the free employee seats will be overriden.
          </CustomTooltip>
        </div>
        <q-input
          v-model.number="formData.employee_seats"
          label="Employee seats"
          type="number" filled
          :rules="[
          val => !val || (val > 0 && val <= 100) || 'Value must be between 0 and 100'
        ]"
          hint="Enter a value between 0 and 100"
        />
        <q-btn-toggle
          v-if="employer"
          v-model="formData.subscription_status"
          toggle-color="primary"
          :options="[
          {label: 'Active', value: SUBSCRIPTION_STATUS.ACTIVE},
          {label: 'Canceled', value: SUBSCRIPTION_STATUS.CANCELED}
        ]"
        />
      </template>
    </q-form>
  </DialogBase>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'
import FileDisplayOrUpload from 'components/inputs/FileDisplayOrUpload.vue'
import SelectOrganizationType from 'components/inputs/SelectOrganizationType.vue'
import SelectYesNo from 'components/inputs/SelectYesNo.vue'
import InputPermittedEmailDomains from 'pages/employer/settings-page/InputPermittedEmailDomains.vue'
import dataUtil from 'src/utils/data.js'
import employerTypeUtil from 'src/utils/employer-types.js'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import formUtil from 'src/utils/form.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { SUBSCRIPTION_STATUS } from 'src/utils/subscription.js'

export default {
  name: 'DialogAdminEmployer',
  extends: DialogBase,
  inheritAttrs: false,
  components: { SelectOrganizationType, SelectYesNo, CustomTooltip, InputPermittedEmailDomains, DialogBase, FileDisplayOrUpload },
  props: {
    employer: [Object, null]
  },
  data () {
    return {
      formData: {},
      newLogoKey: 'logo',
      employerTypeUtil,
      formUtil,
      SUBSCRIPTION_STATUS
    }
  },
  watch: {
    employer () {
      this.setFormData()
    }
  },
  computed: {
    canUpdateSubscription () {
      return !this.employer || this.employer.is_manual_subscription
    },
    allowedFileExtensionsStr () {
      return fileUtil.getAllowedFileExtensionsStr([FILE_TYPES.IMAGE.key])
    }
  },
  methods: {
    setFormData () {
      this.formData = (this.employer) ? dataUtil.deepCopy(this.employer) : {}
    },
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async saveEmployer () {
      const data = Object.assign(
        { employer_id: this?.employer?.id },
        (this.canUpdateSubscription) ? this.formData : dataUtil.omit(this.formData, ['employee_seats', 'subscription_status']),
        (this.$refs.logoUpload) ? this.$refs.logoUpload.getValues() : {}
      )
      const apiMethod = (this.employer) ? this.$api.put : this.$api.post
      await apiMethod('admin/employer/', getAjaxFormData(data, [this.newLogoKey]))
      this.$emit('ok')
    }
  },
  mounted () {
    this.setFormData()
  }
}
</script>
