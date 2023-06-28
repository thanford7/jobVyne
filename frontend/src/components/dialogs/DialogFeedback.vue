<template>
  <DialogBase
    base-title-text="Feedback"
    :is-include-buttons="false"
  >
    <FeedbackForm @feedback="closeDialog()"/>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import FeedbackForm from 'pages/feedback-page/FeedbackForm.vue'

export default {
  name: 'DialogFeedback',
  extends: DialogBase,
  inheritAttrs: false,
  components: { FeedbackForm, DialogBase },
  methods: {
    closeDialog () {
      this.$emit('ok')
      this.$emit('hide')
    }
  }
}
</script>
