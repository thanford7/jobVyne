<template>
  <DialogBase
    base-title-text="Create user instructions"
    :is-include-buttons="false"
  >
    <div class="q-gutter-y-md">
      All candidates submitted from JobVyne to Greenhouse must have a "referrer" user. You
      must create a "Site Admin" user in Greenhouse which JobVyne can use as the referrer for candidates. The Site Admin role
      is required because it is the only role allowed to create new candidates.
      To create a new user:
      <ol>
        <li>Navigate to your Greenhouse admin website</li>
        <li>Click the "Configure" link (gear icon at the top right of the page)</li>
        <li>Click the "Users" link</li>
        <li>Click the "Add Users" button</li>
        <li>Enter "jobvyne-partner@jobvyne.com" for the user email</li>
        <li>
          Click the "Assign" button for the "Site Admin" permission
        </li>
        <li>Leave all boxes unchecked for "User-Specific Permissions" and "Developer Permissions"</li>
        <li>Click the "Save" button</li>
        <li>Enter the user email you used into this form field ("Greenhouse User Email")</li>
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
