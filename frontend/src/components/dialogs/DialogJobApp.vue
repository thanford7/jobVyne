<template>
  <DialogBase
    :is-include-buttons="false"
  >
    <template v-slot:fullWidthBody>
      <FormJobApplication :job-application="jobApplication" @closeApplication="onDialogHide"/>
    </template>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import FormJobApplication from 'components/job-app-form/FormJobApplication.vue'

export default {
  name: 'DialogJobApp',
  extends: DialogBase,
  components: { FormJobApplication, DialogBase },
  props: {
    jobApplication: {
      type: [Object, null]
    }
  }
}
</script>
