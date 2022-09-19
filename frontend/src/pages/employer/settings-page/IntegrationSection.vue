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
      <template v-if="atsData && atsData.id">
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
        <div class="col-12">
          <SelectAtsJobStage v-model="atsFormData.job_stage_name" :ats_id="atsData.id"/>
        </div>
        <div class="col-12">
          <q-btn label="Test connection" color="primary" @click="updateJobs"/>
          <span v-if="isGoodConnection" class="text-positive">
          &nbsp;<q-icon name="check_circle"/> Connection successful
        </span>
        </div>
      </template>
    </template>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import SelectAtsCustomField from 'components/inputs/greenhouse/SelectAtsCustomField.vue'
import SelectAtsJobStage from 'components/inputs/greenhouse/SelectAtsJobStage.vue'
import DialogGreenhouseApiKey from 'pages/employer/settings-page/DialogGreenhouseApiKey.vue'
import DialogGreenhouseUser from 'pages/employer/settings-page/DialogGreenhouseUser.vue'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
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
      employerStore: useEmployerStore(),
      q: useQuasar(),
      isGoodConnection: false
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
    },
    atsFormData: {
      handler () {
        if (!this.atsData) {
          return
        }
        if (this.atsFormData.name !== this.atsData.name) {
          this.atsFormData.id = null
        } else {
          this.atsFormData.id = this.atsData.id
        }
      },
      deep: true
    }
  },
  methods: {
    resetAtsFormData () {
      this.atsFormData = (this.atsData) ? { ...this.atsData } : {}
    },
    async saveAts () {
      if (this?.atsData?.id && !this.atsFormData.id) {
        openConfirmDialog(
          this.q,
          'Are you sure you want to delete the ATS configuration? The configuration will not be retrievable once deleted.',
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
      const resp = await this.$api.put('ats/jobs/', getAjaxFormData({ ats_id: this.atsData.id }))
      if (resp.status === 200) {
        this.isGoodConnection = true
      }
    },
    showGreenhouseUserDialog () {
      return this.q.dialog({
        component: DialogGreenhouseUser
      })
    },
    showGreenhouseApiKeyDialog () {
      return this.q.dialog({
        component: DialogGreenhouseApiKey
      })
    }
  },
  mounted () {
    this.resetAtsFormData()
  }
}
</script>
