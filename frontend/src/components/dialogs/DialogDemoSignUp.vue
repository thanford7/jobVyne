<template>
  <DialogBase
      base-title-text="Schedule 30-minute demo"
      primary-button-text="Pick time"
      primary-button-icon-right="arrow_forward"
      :is-valid-form-fn="getIsValid"
      @ok="save()"
  >
    <q-form ref="form">
      <q-input
        v-model="formData.first_name"
        label="First name" filled autofocus
        lazy-rules
        :rules="[
          (val) => val && val.length || 'First name is required'
        ]"
      />
      <q-input
        v-model="formData.last_name"
        label="Last name" filled
        lazy-rules
        :rules="[
          (val) => val && val.length || 'Last name is required'
        ]"
      />
      <q-input
        v-model="formData.company_name"
        label="Company name" filled
        lazy-rules
        :rules="[
          (val) => val && val.length || 'Company name is required'
        ]"
      />
      <EmailInput
        v-model="formData.email"
        label="Company email"
        :additional-rules="[
          (val) => (val && val.match(/^.+?@(?!(gmail.com)|(aol.com)|(hotmail.com)|(yahoo.com))/)) || 'Email must be a company email'
        ]"
      />
    </q-form>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import DialogDemoCalendar from 'components/dialogs/DialogDemoCalendar.vue'
import EmailInput from 'components/inputs/EmailInput.vue'
import { useQuasar } from 'quasar'
import { getAjaxFormData } from 'src/utils/requests.js'

export default {
  name: 'DialogDemoSignUp',
  extends: DialogBase,
  inheritAttrs: false,
  components: { EmailInput, DialogBase },
  data () {
    return {
      formData: {
        first_name: null,
        last_name: null,
        company_name: null,
        email: null
      }
    }
  },
  methods: {
    async getIsValid () {
      return await this.$refs.form.validate()
    },
    save () {
      // No need to wait on this post
      this.$api.post('sales/inquiry/', getAjaxFormData(this.formData))
      this.q.dialog({
        component: DialogDemoCalendar,
        componentProps: {
          firstName: this.formData.first_name,
          lastName: this.formData.last_name,
          email: this.formData.email
        }
      })
    }
  },
  setup () {
    return {
      q: useQuasar()
    }
  }
}
</script>
