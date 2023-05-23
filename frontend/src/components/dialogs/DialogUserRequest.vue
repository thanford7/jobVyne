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
          <q-select
            v-model="formData.request_type"
            autofocus filled
            :options="[
              { label: 'Introduction', val: 'introduction' }
            ]"
            autocomplete="name"
            option-value="val"
            option-label="label"
            label="Request type"
            :rules="[
              (val) => val || 'Request type is required'
            ]"
          />
        </div>
        <div class="col-12">
          <q-input
            v-model="formData.connector_first_name"
            label="Connector first name" filled
            lazy-rules
            :rules="[
              (val) => val && val.length || 'First name is required'
            ]"
          >
            <template v-slot:after>
              <CustomTooltip>
                This is the person that will be making the introduction
              </CustomTooltip>
            </template>
          </q-input>
        </div>
        <div class="col-12">
          <q-input
            v-model="formData.connector_last_name"
            label="Connector last name" filled
          >
            <template v-slot:after>
              <CustomTooltip>
                This is the person that will be making the introduction
              </CustomTooltip>
            </template>
          </q-input>
        </div>
        <div class="col-12">
          <q-input
            v-model="formData.connection_first_name"
            label="Connection first name" filled
            lazy-rules
            :rules="[
              (val) => val && val.length || 'First name is required'
            ]"
          >
            <template v-slot:after>
              <CustomTooltip>
                This is the person you want to be introduced to
              </CustomTooltip>
            </template>
          </q-input>
        </div>
        <div class="col-12">
          <q-input
            v-model="formData.connection_last_name"
            label="Connection last name" filled
          >
            <template v-slot:after>
              <CustomTooltip>
                This is the person you want to be introduced to
              </CustomTooltip>
            </template>
          </q-input>
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
import DialogBase from 'components/dialogs/DialogBase.vue'
import InputLinkedIn from 'components/inputs/InputLinkedIn.vue'

export default {
  name: 'DialogUserRequest',
  components: { InputLinkedIn, CustomTooltip, DialogBase },
  data () {
    return {
      formData: {}
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async saveRequest () {
      //
    }
  }
}
</script>
