<template>
  <DialogBase
      base-title-text="Schedule 30-minute demo"
      primary-button-text="Schedule"
      @ok="save()"
  >
    <q-form>
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
      <EmailInput v-model="formData.email"/>
    </q-form>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import DialogDemoCalendar from 'components/dialogs/DialogDemoCalendar.vue'
import EmailInput from 'components/inputs/EmailInput.vue'
import { useQuasar } from 'quasar'

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
        email: null
      }
    }
  },
  methods: {
    save () {
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
