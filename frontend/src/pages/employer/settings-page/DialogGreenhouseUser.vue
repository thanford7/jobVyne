<template>
  <DialogBase
    base-title-text="Create user instructions"
    :is-include-buttons="false"
  >
    <div class="q-gutter-y-md">
      All candidates submitted from JobVyne to Greenhouse must have a "referrer" user. You
      must create a "Basic" user in Greenhouse which JobVyne can use as the referrer for candidates.
      To do so:
      <ol>
        <li>Navigate to your Greenhouse admin website</li>
        <li>Click the "Configure" link (gear icon at the top right of the page)</li>
        <li>Click the "Users" link</li>
        <li>Click the "Add Users" button</li>
        <li>Enter "jobvyne-partner@jobvyne.com" for the user email</li>
        <li>
          Click the "Assign" button for the "Basic" permission
        </li>
        <li>Leave all boxes unchecked for "Developer Permissions"</li>
        <li>Click the "Save" button</li>
        <li>Enter the user email you used into this form field ("Admin User Email")</li>
      </ol>
    </div>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'

export default {
  name: 'DialogGreenhouseUser',
  components: { DialogBase }
}
</script>
