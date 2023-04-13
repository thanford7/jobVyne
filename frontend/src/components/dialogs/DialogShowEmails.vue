<template>
  <DialogBase
    base-title-text="Messages"
    :is-include-buttons="false"
    width="700px"
  >
    <div class="q-gutter-y-sm">
      <EmailThread v-for="emailThread in emailThreads" :email-thread="emailThread"/>
    </div>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import EmailThread from 'components/email/EmailThread.vue'

export default {
  name: 'DialogShowEmails',
  components: { EmailThread, DialogBase },
  props: {
    emailThreads: Array
  }
}
</script>
