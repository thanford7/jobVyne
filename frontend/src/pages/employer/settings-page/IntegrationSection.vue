<template>
  <div class="row q-gutter-y-md">
    <div class="text-h6">Application Tracking System</div>
    <div class="col-12">
      <q-select
        filled clearable emit-value map-options
        label="ATS name"
        v-model="atsFormData.atsName"
        :options="[
          {val: 'greenhouse', label: 'Greenhouse'}
        ]"
        option-value="val"
        option-label="label"
      />
    </div>
    <template v-if="atsFormData.atsName === 'greenhouse'">
      <div class="col-12">
        <q-input filled label="Admin User Email" v-model="atsFormData.atsUserEmail">
          <template v-slot:after>
            <CustomTooltip>
              All candidates submitted from JobVyne to Greenhouse must have a "referrer" user. You
              must create a "Site Admin" user in Greenhouse which JobVyne can use as the referrer for candidates.
              To do so:
              <ol>
                <li>Navigate to your Greenhouse admin website</li>
                <li>Click the "Configure" link (gear icon at the top right of the page)</li>
                <li>Click the "Users" link</li>
                <li>Click the "Add Users" button</li>
                <li>Enter "jobvyne-partner@jobvyne.com" for the user email</li>
                <li>
                  Click the "Assign" button for the "Site Admin" permission. This permission is required because
                  all other permission types can only access jobs that the user has been directly assigned to.
                </li>
                <li>Leave all boxes unchecked for "User-Specific Permissions" and "Developer Permissions"</li>
                <li>Click the "Save" button</li>
                <li>Enter the user email you used into this form field ("Admin User Email")</li>
              </ol>
            </CustomTooltip>
          </template>
        </q-input>
      </div>
      <div class="col-12">
        <q-input filled label="Harvest API Key" v-model="atsFormData.atsApiKey">
          <template v-slot:after>
            <CustomTooltip>
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
                <li>Click the "Create" button</li>
                <li>Copy the API Key and paste it into this form field ("Harvest API Key")</li>
              </ol>
            </CustomTooltip>
          </template>
        </q-input>
      </div>
    </template>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
export default {
  name: 'IntegrationSection',
  components: { CustomTooltip },
  data () {
    return {
      atsFormData: {
        atsName: null
      }
    }
  }
}
</script>
