<template>
  <DialogBase
    base-title-text="Create request"
    primary-button-text="Create"
    :is-valid-form-fn="isValidForm"
    @ok="saveRequest"
  >
    <q-form ref="form">
      <div class="row">
        <div class="col-12">
          <SelectUserRequestType
            v-model="formData.request_type"
          />
        </div>
        <div class="col-12 q-my-sm">
          <span class="text-bold">
            Connector
          </span>
          <CustomTooltip icon_size="22px">
            This is the person that will be making the introduction
          </CustomTooltip>
        </div>
        <div class="col-12">
          <q-input
            v-model="formData.connector_first_name"
            label="First name" filled
            lazy-rules
            :rules="[
              (val) => val && val.length || 'First name is required'
            ]"
          />
        </div>
        <div class="col-12">
          <q-input
            v-model="formData.connector_last_name"
            label="Last name" filled
          />
        </div>
        <div class="col-12 q-my-sm">
          <span class="text-bold">
            Connection
          </span>
          <CustomTooltip icon_size="22px">
            This is the person you want to be introduced to
          </CustomTooltip>
        </div>
        <div class="col-12">
          <q-input
            v-model="formData.connection_first_name"
            label="First name" filled
            lazy-rules
            :rules="[
              (val) => val && val.length || 'First name is required'
            ]"
          />
        </div>
        <div class="col-12 q-mb-sm">
          <q-input
            v-model="formData.connection_last_name"
            label="Last name" filled
          />
        </div>
        <div class="col-12">
          <InputLinkedIn
            v-model="formData.connection_linkedin_url"
            :is-required="false"
          />
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import SelectUserRequestType from 'components/inputs/SelectUserRequestType.vue'
import dataUtil from 'src/utils/data.js'
import DialogBase from 'components/dialogs/DialogBase.vue'
import InputLinkedIn from 'components/inputs/InputLinkedIn.vue'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'

export default {
  name: 'DialogUserRequest',
  components: { SelectUserRequestType, InputLinkedIn, CustomTooltip, DialogBase },
  props: {
    userRequest: [Object, null]
  },
  data () {
    return {
      formData: {},
      user: null,
      dataUtil
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async saveRequest () {
      const method = (this.userRequest?.id) ? this.$api.put : this.$api.post
      await method('karma/user-request/', getAjaxFormData(Object.assign(
        { user_id: this.user.id },
        this.formData
      )))
      this.$emit('ok')
    }
  },
  mounted () {
    const authStore = useAuthStore()
    this.user = authStore.propUser
  }
}
</script>
