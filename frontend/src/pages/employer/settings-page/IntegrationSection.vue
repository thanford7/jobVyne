<template>
  <div class="row q-gutter-y-md">
    <div class="text-h6">Applicant Tracking System</div>
    <div v-if="hasChanged" class="col-12">
      <q-btn ripple label="Save" icon="save" color="primary" @click="saveAts"/>
      <q-btn ripple label="Undo" icon="undo" color="grey-6" class="q-ml-sm" @click="resetAtsFormData()"/>
    </div>
    <div class="col-12">
      <q-select
        filled clearable emit-value map-options
        label="ATS Name"
        v-model="atsFormData.name"
        :options="atsOptions"
        option-value="val"
        option-label="label"
        @update:model-value="resetAtsFormData($event, !$event)"
      />
    </div>
    <template v-if="atsFormData.name === ATS_CFGS.greenhouse.key">
      <div class="col-12">
        <q-input filled label="Greenhouse User Email" v-model="atsFormData.email">
          <template v-slot:after>
            <span class="text-small">
              <a href="#" @click.prevent="showGreenhouseUserDialog">Show instructions</a>
            </span>
          </template>
        </q-input>
      </div>
      <div class="col-12">
        <q-input filled label="Harvest API Key" v-model="atsFormData.api_key">
          <template v-slot:after>
            <span class="text-small">
              <a href="#" @click.prevent="showGreenhouseApiKeyDialog">Show instructions</a>
            </span>
          </template>
        </q-input>
      </div>
      <template v-if="atsData && atsData.id && atsData.name === ATS_CFGS.greenhouse.key">
        <div class="col-12">
          <SelectAtsCustomField
            label="Employment Type Field"
            :ats_id="atsData.id"
            v-model="atsFormData.employment_type_field_key"
          >
            <template v-slot:after>
              <CustomTooltip :is_include_space="true">
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
              <CustomTooltip :is_include_space="true">
                The salary range (e.g. $50,000-$60,000) is a custom field so it is necessary to provide the name
                of the field
              </CustomTooltip>
            </template>
          </SelectAtsCustomField>
        </div>
        <div class="col-12">
          <SelectAtsJobStage v-model="atsFormData.job_stage_name" :ats_id="atsData.id"
                             :ats_name="ATS_CFGS.greenhouse.key"/>
        </div>
        <div class="col-12">
          <q-btn label="Test connection" color="primary" @click="updateJobs" :loading="isFetchingJobs"/>
          <span v-if="isGoodConnection" class="text-positive">
          &nbsp;<q-icon name="check_circle"/> Connection successful
        </span>
        </div>
      </template>
    </template>
    <template v-if="atsFormData.name === ATS_CFGS.lever.key">
      <div
        v-if="!atsData || !atsData.has_access_token || atsData.is_token_expired"
        class="col-12"
      >
        <q-btn
          label="Connect Lever" color="primary" @click="connectLeverAccount"
        />
      </div>
      <template v-else>
        <div class="col-12">
          <div class="border-rounded bg-positive q-pa-xs">
            <q-icon name="check_circle" color="white"/>
            <span class="text-white">Connected</span>
          </div>
        </div>
        <div class="col-12">
          <q-input filled label="Lever User Email" v-model="atsFormData.email">
            <template v-slot:after>
              <q-btn
                label="Fill suggested email" color="primary"
                class="h-100"
                @click="atsFormData.email = suggestedEmployerEmail"
              />
              <CustomTooltip>
                <p>
                  A Lever user account is required to submit applications to Lever.
                  JobVyne will create a Lever user with this email address.
                  The user will have "Team Member" privileges.
                  The email address must use one of your company's domains.
                </p>
                <p>
                  Suggested email: <span class="text-bold">{{ suggestedEmployerEmail }}</span>
                </p>
              </CustomTooltip>
            </template>
          </q-input>
        </div>
        <div class="col-12">
          <SelectAtsJobStage v-model="atsFormData.job_stage_name" :ats_id="atsData.id" :ats_name="ATS_CFGS.lever.key"/>
        </div>
        <div class="col-12">
          <SelectYesNo v-model="atsFormData.is_webhook_enabled" label="Confirm webhooks enabled" :is-multi="false">
            <template v-slot:after>
            <span class="text-small">
              <a href="#" @click.prevent="showLeverWebhookDialog">Show instructions</a>
            </span>
            </template>
          </SelectYesNo>
        </div>
      </template>
    </template>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import SelectAtsCustomField from 'components/inputs/greenhouse/SelectAtsCustomField.vue'
import SelectAtsJobStage from 'components/inputs/greenhouse/SelectAtsJobStage.vue'
import SelectYesNo from 'components/inputs/SelectYesNo.vue'
import DialogGreenhouseApiKey from 'pages/employer/settings-page/DialogGreenhouseApiKey.vue'
import DialogGreenhouseUser from 'pages/employer/settings-page/DialogGreenhouseUser.vue'
import DialogLeverWebhook from 'pages/employer/settings-page/DialogLeverWebhook.vue'
import { useQuasar } from 'quasar'
import { ATS_CFGS } from 'src/utils/ats.js'
import dataUtil from 'src/utils/data.js'
import messagesUtil, { msgTypes } from 'src/utils/messages.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'IntegrationSection',
  components: { SelectYesNo, SelectAtsCustomField, SelectAtsJobStage, CustomTooltip },
  props: {
    atsData: [Object, null]
  },
  data () {
    return {
      ATS_CFGS,
      atsFormData: {},
      authStore: useAuthStore(),
      employerStore: useEmployerStore(),
      globalStore: useGlobalStore(),
      q: useQuasar(),
      isGoodConnection: false,
      isFetchingJobs: false
    }
  },
  computed: {
    atsOptions () {
      return Object.values(ATS_CFGS).map((cfg) => ({ val: cfg.key, label: cfg.name }))
    },
    hasChanged () {
      return (!this.atsData && !dataUtil.isEmpty(this.atsFormData)) || !dataUtil.isDeepEqual(this.atsData, this.atsFormData)
    },
    suggestedEmployerEmail () {
      const employer = this.employerStore.getEmployer(this.authStore.propUser.employer_id)
      const email = 'jobvyne_referral@'
      if (employer.email_domains && employer.email_domains.length) {
        return email + employer.email_domains.split(',')[0]
      }
      return email + '{your email domain}'
    }
  },
  watch: {
    atsData () {
      this.resetAtsFormData()
    }
  },
  methods: {
    resetAtsFormData (atsName = null, isClear = false) {
      const isCurrentAts = this.atsData && (!atsName || (this.atsData.name === atsName))
      this.atsFormData = (isCurrentAts && !isClear) ? { ...this.atsData } : { name: atsName }
    },
    async saveAts () {
      if (this?.atsData?.id && !this.atsFormData.id) {
        openConfirmDialog(
          this.q,
          'Are you sure you want to delete your current ATS configuration? The configuration will not be retrievable once deleted.',
          {
            okFn: async () => {
              await this.$api.delete(`employer/ats/${this.atsData.id}/`)
              this.$emit('updateEmployer')
            }
          }
        )
      } else {
        const method = (this.atsData && this.atsData.id) ? this.$api.put : this.$api.post
        await method('employer/ats/', getAjaxFormData({
          ...this.atsFormData,
          employer_id: this.authStore.propUser.employer_id
        }))
        this.$emit('updateEmployer')
      }
    },
    async updateJobs () {
      this.isFetchingJobs = true
      const resp = await this.$api.put('ats/jobs/', getAjaxFormData({ ats_id: this.atsData.id }))
      this.isFetchingJobs = false
      if (resp.status === 200) {
        this.isGoodConnection = true
      }
    },
    // Greenhouse
    showGreenhouseUserDialog () {
      return this.q.dialog({
        component: DialogGreenhouseUser,
        componentProps: { employer: this.employerStore.getEmployer(this.authStore.propUser.employer_id) }
      })
    },
    showGreenhouseApiKeyDialog () {
      return this.q.dialog({
        component: DialogGreenhouseApiKey
      })
    },
    // Lever
    showLeverWebhookDialog () {
      return this.q.dialog({
        component: DialogLeverWebhook
      })
    },
    async connectLeverAccount () {
      // Refresh existing connection
      if (this.atsData && this.atsData.has_access_token && !this.atsData.is_token_expired) {
        await this.$api.put('lever/oauth-token/', getAjaxFormData({
          name: this.ATS_CFGS.lever.key,
          employer_id: this.authStore.propUser.employer_id
        }))
        this.$emit('updateEmployer')
      } else {
        // Create new connection through Oauth
        window.location.replace(encodeURI(this.globalStore.leverOauthUrl))
      }
    }
  },
  async mounted () {
    this.resetAtsFormData()
    await this.globalStore.setLeverOauthUrl()

    // Handle redirect after user authenticates from Oauth
    const { code, state, error: errorType, error_description: errorDescription } = dataUtil.getQueryParams()
    if (errorType) {
      messagesUtil.addMsg(`${errorType}: ${errorDescription}`, msgTypes.ERROR)
    }
    if (code && state) {
      await this.$api.post('lever/oauth-token/', getAjaxFormData({
        code,
        state,
        name: this.ATS_CFGS.lever.key,
        employer_id: this.authStore.propUser.employer_id
      }))
      this.$emit('updateEmployer')
    }
  }
}
</script>
