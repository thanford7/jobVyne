<template>
  <DialogBase
    base-title-text="Send announcement email"
    primary-button-text="Send"
    :is-full-screen="true"
    @ok="sendEmail"
  >
    <q-form ref="form">
      <div class="row q-mt-md">
        <div class="col-md-8 col-12 q-pr-md-sm">
          <q-input
            v-model="emailSubject"
            filled label="Email subject"
            :rules="[
              val => val && val.length > 0 || 'Email subject is required'
            ]"
          />
          <WysiwygEditor v-model="emailBody"/>
        </div>
        <div class="col-md-4 col-12 q-pl-md-sm q-gutter-y-md">
          <div class="text-bold">
            Email filters
            <CustomTooltip>
              Only users with these properties will receive the email announcement. Any fields left blank will
              allow all users.
            </CustomTooltip>
          </div>
          <SelectUserType v-model="userFilters.userTypes" :is-multi="true" :is-required="false"/>
          <SelectEmployer v-if="!employerId" v-model="userFilters.userEmployers" :is-multi="true"/>
          <SelectEmployee v-if="employerId" v-model="userFilters.userIds" :employer-id="employerId" :is-multi="true"/>
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import SelectEmployee from 'components/inputs/SelectEmployee.vue'
import SelectEmployer from 'components/inputs/SelectEmployer.vue'
import SelectUserType from 'components/inputs/SelectUserType.vue'
import WysiwygEditor from 'components/inputs/WysiwygEditor.vue'
import { getAjaxFormData } from 'src/utils/requests.js'

export default {
  name: 'DialogAnnouncementEmail',
  extends: DialogBase,
  inheritAttrs: false,
  components: { SelectEmployee, SelectEmployer, DialogBase, SelectUserType, WysiwygEditor },
  props: {
    employerId: [Number, String, null] // If no employerId, we are in admin mode
  },
  data () {
    return {
      emailSubject: '',
      emailBody: '',
      userFilters: {
        userTypes: null,
        userEmployers: null,
        userIds: null
      }
    }
  },
  methods: {
    async sendEmail () {
      const isValidForm = await this.$refs.form.validate()
      if (!isValidForm) {
        return
      }
      await this.$api.post('email/notification/', getAjaxFormData({
        emailSubject: this.emailSubject,
        emailBody: this.emailBody,
        userFilters: this.userFilters
      }))
    }
  }
}
</script>
