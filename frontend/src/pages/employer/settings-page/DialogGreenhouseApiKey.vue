<template>
  <DialogBase
    base-title-text="Create admin user instructions"
    :is-include-buttons="false"
  >
    <div class="q-gutter-y-md">
      You must create an API key for JobVyne to connect to your Greenhouse instance. To do so:
      <ol>
        <li>Navigate to your Greenhouse admin website</li>
        <li>Click the "Configure" link (gear icon at the top right of the page)</li>
        <li>Click the "Dev Center" navigation link</li>
        <li>Click the "API Credentials" navigations link</li>
        <li>Click the "Create New API Key" button</li>
        <li>Select "Harvest" for API Type</li>
        <li>Select "JobVyne" for Partner</li>
        <li>Enter a description (suggested: "JobVyne API")</li>
        <li>Click the "Manage Permissions" button</li>
        <li>Copy the API Key and paste it into this form field ("Harvest API Key")</li>
        <li>Click the "I have stored the API Key" button</li>
        <li>
          Add the following permissions:
        </li>
      </ol>
      <div class="q-table__container q-table--horizontal-separator q-table--dense">
        <table class="q-table q-table--bordered">
          <tbody>
          <tr>
            <td class="bg-grey-3 text-bold">Applications</td>
          </tr>
          <tr>
            <td>Get: Retrieve Application</td>
          </tr>
          <tr>
            <td>Get: List Applications</td>
          </tr>
          <tr>
            <td>Post: Add Attachment to Application</td>
          </tr>
          <tr>
            <td class="bg-grey-3 text-bold">Candidates</td>
          </tr>
          <tr>
            <td>Get: Retrieve Candidate</td>
          </tr>
          <tr>
            <td>Get: List Candidates</td>
          </tr>
          <tr>
            <td>Post: Add Candidate</td>
          </tr>
          <tr>
            <td>Post: Add Note</td>
          </tr>
          <tr>
            <td>Post: Add Attachment</td>
          </tr>
          <tr>
            <td>Post: Add Application</td>
          </tr>
          <tr>
            <td>Post: Add Prospect</td>
          </tr>
          <tr>
            <td class="bg-grey-3 text-bold">Users</td>
          </tr>
          <tr>
            <td>Get: Retrieve User</td>
          </tr>
          <tr>
            <td>Get: List Users</td>
          </tr>
          <tr>
            <td class="bg-grey-3 text-bold">Jobs</td>
          </tr>
          <tr>
            <td>Get: Retrieve Job</td>
          </tr>
          <tr>
            <td>Get: List Jobs</td>
          </tr>
          <tr>
            <td class="bg-grey-3 text-bold">Job Posts</td>
          </tr>
          <tr>
            <td>Get: List Job Posts</td>
          </tr>
          <tr>
            <td>Get: Retrieve Job Post for Job</td>
          </tr>
          <tr>
            <td>Get: List Job Posts for Job</td>
          </tr>
          <tr>
            <td class="bg-grey-3 text-bold">Job Stages</td>
          </tr>
          <tr>
            <td>Get: Retrieve Job Stage</td>
          </tr>
          <tr>
            <td>Get: List Job Stages</td>
          </tr>
          <tr>
            <td>Get: List Job Stages for Job</td>
          </tr>
          <tr>
            <td class="bg-grey-3 text-bold">Custom Fields</td>
          </tr>
          <tr>
            <td>Get: Get Custom Fields</td>
          </tr>
          </tbody>
        </table>
      </div>
      <ol start="13">
        <li>Click the "Save" button</li>
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
