<template>
  <DialogBase
    base-title-text="Add donation organization"
    primary-button-text="Add"
    :is-valid-form-fn="isValidForm"
    @ok="saveOrganization"
  >
    <q-form ref="form">
      <div class="row">
        <div class="col-12">
          <SelectDonationOrganization
            v-model="formData.donation_organization_id"
            :is-multi="false"
            :is-required="true"
          />
        </div>
      </div>
    </q-form>
</DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import SelectDonationOrganization from 'components/inputs/SelectDonationOrganization.vue'
import { getAjaxFormData } from 'src/utils/requests.js'

export default {
  name: 'DialogUserDonationOrganization',
  components: { SelectDonationOrganization, DialogBase },
  data () {
    return {
      formData: {}
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async saveOrganization () {
      await this.$api.post('karma/user-donation-organization/', getAjaxFormData(this.formData))
      this.$emit('ok')
    }
  }
}
</script>
