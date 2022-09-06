<template>
  <div class="row q-gutter-y-md">
    <div class="text-h6">Application Tracking System</div>
    <div v-if="hasChanged" class="col-12">
      <q-btn ripple label="Save" icon="save" color="primary" @click="saveAts"/>
      <q-btn ripple label="Undo" icon="undo" color="grey-6" class="q-ml-sm" @click="resetAtsFormData"/>
    </div>
    <div class="col-12">
      <q-select
        filled clearable emit-value map-options
        label="ATS Name"
        v-model="atsFormData.name"
        :options="[
          {val: 'greenhouse', label: 'Greenhouse'}
        ]"
        option-value="val"
        option-label="label"
      />
    </div>
    <template v-if="atsFormData.name === 'greenhouse'">
      <div class="col-12">
        <q-input filled label="Admin User Email" v-model="atsFormData.email">
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
                  allow JobVyne to send candidates for all open jobs.
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
        <q-input filled label="Harvest API Key" v-model="atsFormData.api_key">
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
      <div class="col-12">
        <SelectAtsCustomField
          label="Employment Type Field"
          :ats_id="atsData.id"
          v-model="atsFormData.employment_type_field_key"
        >
          <template v-slot:after>
            <CustomTooltip>
              The employment type (e.g. full time) is a custom field so it is necessary to provide the name
              of the field
            </CustomTooltip>
          </template>
        </SelectAtsCustomField>
      </div>
      <div class="col-12">
        <SelectAtsCustomField
          label="Salary Range Field"
          :ats_id="atsData.id"
          v-model="atsFormData.salary_range_field_key"
        >
          <template v-slot:after>
            <CustomTooltip>
              The salary range (e.g. $50,000-$60,000) is a custom field so it is necessary to provide the name
              of the field
            </CustomTooltip>
          </template>
        </SelectAtsCustomField>
      </div>
      <div v-if="atsData.id" class="col-12">
        <SelectAtsJobStage v-model="atsFormData.job_stage_name" :ats_id="atsData.id"/>
      </div>
    </template>
    <div class="col-12">
      <q-btn label="Test connection" color="primary" @click="updateJobs"/>
    </div>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import SelectAtsCustomField from 'components/inputs/greenhouse/SelectAtsCustomField.vue'
import SelectAtsJobStage from 'components/inputs/greenhouse/SelectAtsJobStage.vue'
import dataUtil from 'src/utils/data.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'IntegrationSection',
  components: { SelectAtsCustomField, SelectAtsJobStage, CustomTooltip },
  props: {
    atsData: [Object, null]
  },
  data () {
    return {
      atsFormData: {},
      authStore: useAuthStore(),
      employerStore: useEmployerStore()
    }
  },
  computed: {
    hasChanged () {
      return (!this.atsData && !dataUtil.isEmpty(this.atsFormData)) || !dataUtil.isDeepEqual(this.atsData, this.atsFormData)
    }
  },
  watch: {
    atsData () {
      this.resetAtsFormData()
    }
  },
  methods: {
    resetAtsFormData () {
      this.atsFormData = (this.atsData) ? { ...this.atsData } : {}
    },
    async saveAts () {
      const method = (this.atsData && this.atsData.id) ? this.$api.put : this.$api.post
      await method('employer/ats/', getAjaxFormData({
        ...this.atsFormData,
        employer_id: this.authStore.propUser.employer_id
      }))
      this.$emit('updateEmployer')
    },
    async updateJobs () {
      await this.$api.put('ats/jobs/', getAjaxFormData({ ats_id: this.atsData.id }))
    }
  },
  mounted () {
    this.resetAtsFormData()
  }
}
</script>
