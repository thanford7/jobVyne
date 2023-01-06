<template>
  <DialogBase
    base-title-text="Schedule 30-minute demo"
    :is-include-buttons="false"
  >
    <CalendlyEmbed :first-name="firstName" :last-name="lastName" :email="email"/>
  </DialogBase>
</template>

<script>
import CalendlyEmbed from 'components/CalendlyEmbed.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'

export default {
  name: 'DialogDemoCalendar',
  extends: DialogBase,
  inheritAttrs: false,
  props: {
    firstName: [String, null],
    lastName: [String, null],
    email: [String, null]
  },
  components: { CalendlyEmbed, DialogBase }
}
</script>
