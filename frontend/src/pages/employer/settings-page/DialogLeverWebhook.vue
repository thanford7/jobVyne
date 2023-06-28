<template>
  <DialogBase
    base-title-text="Enable Lever webhooks"
    :is-include-buttons="false"
  >
    <div class="q-gutter-y-md q-mt-md">
      <p>
        Webhooks are required to update job applications when there is a stage change in Lever.
        By default, this information is only viewable by JobVyne users at your company with employer permissions.
      </p>
      <p class="text-bold">Note: You will need "Super admin" priveleges to complete the actions below.</p>
      <ol>
        <li>
          Navigate to your
          <a href="https://hire.lever.co/settings/integrations?tab=webhooks" target="_blank">
            Lever admin website
          </a>
        </li>
        <li>If not already enabled, turn on webhooks for:</li>
        <ul>
          <li>Candidate stage change</li>
          <li>Candidate archive state change</li>
          <li>Candidate hired</li>
          <li>Candidate deleted</li>
        </ul>
        <li>
          Once you confirm that webhooks are enabled, on this JobVyne page, select "Yes" in the "Confirm webhooks enabled" field
        </li>
      </ol>
    </div>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'

export default {
  name: 'DialogLeverWebhook',
  components: { DialogBase }
}
</script>
