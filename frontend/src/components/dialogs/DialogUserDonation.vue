<template>
  <DialogBase
    base-title-text="Add donation"
    primary-button-text="Add"
    :is-valid-form-fn="isValidForm"
    @ok="saveDonation"
  >
    <q-form ref="form">
      <div class="row">
        <div class="col-12">
          <SelectUserDonationOrganization
            v-model="formData.donation_organization_id"
            :is-multi="false"
            :is-required="true"
          />
        </div>
        <div class="col-12 q-mb-md">
          <MoneyInput
            v-model:money-value="formData.donation_amount"
            v-model:currency-name="formData.donation_amount_currency"
            label="Donation amount"
          />
        </div>
        <div class="col-12">
          <q-input
            v-model="formData.donation_reason"
            filled autogrow
            label="Donation reason"
            lazy-rules
            :rules="[ val => !val || val.length <= 200 || 'Max character length is 200']"
          />
        </div>
        <div class="col-12">
          <FileDisplayOrUpload
            ref="logoUpload"
            label="donation receipt"
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
                label="Donation receipt"
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
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'
import FileDisplayOrUpload from 'components/inputs/FileDisplayOrUpload.vue'
import MoneyInput from 'components/inputs/MoneyInput.vue'
import SelectUserDonationOrganization from 'components/inputs/SelectUserDonationOrganization.vue'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import { getAjaxFormData } from 'src/utils/requests.js'

export default {
  name: 'DialogUserDonation',
  components: { SelectUserDonationOrganization, DialogBase, MoneyInput, FileDisplayOrUpload, CustomTooltip },
  computed: {
    allowedFileExtensionsStr () {
      return fileUtil.getAllowedFileExtensionsStr([FILE_TYPES.IMAGE.key, FILE_TYPES.FILE.key])
    }
  },
  data () {
    return {
      formData: {},
      newLogoKey: 'donation_receipt'
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async saveDonation () {
      await this.$api.post('karma/user-donation/', getAjaxFormData(this.formData, [this.newLogoKey]))
      this.$emit('ok')
    }
  }
}
</script>
