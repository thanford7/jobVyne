<template>
  <div class="row q-gutter-y-md">
    <div class="col-12">
      <div class="text-h6">Slack</div>
      <a href="#" @click.prevent="showSlackIntegrationDialog">Show integration instructions</a>
    </div>
    <div v-if="hasChanged" class="col-12">
      <q-btn ripple label="Save" icon="save" color="primary" @click="saveSlackCfg"/>
      <q-btn ripple label="Undo" icon="undo" color="grey-6" class="q-ml-sm" @click="resetSlackFormData()"/>
    </div>
    <div class="col-12">
      <div v-if="slackData.oauth_key">
        <q-toggle
          v-model="slackFormData.is_enabled"
          :color="(slackFormData.is_enabled) ? 'positive' : 'negative'"
          :label="(slackFormData.is_enabled) ? 'Enabled' : 'Disabled'"
          keep-color
        />
      </div>
      <q-input
        v-model="slackFormData.oauth_key"
        filled label="OAuth Token (xoxb-...)"
      />
    </div>
    <div v-if="slackData.oauth_key" class="col-12">
      <q-form ref="slackForm" class="q-gutter-y-sm">
        <q-card flat bordered>
          <q-card-section>
            <div class="row">
              <div class="col-12">
                <div class="text-bold q-mb-md">
                  Send automated posts about the most recent jobs to a Slack channel
                </div>
                <SelectSlackChannel v-model="slackFormData.jobs_post_channel" label="Jobs slack channel">
                  <template v-slot:after>
                    <CustomTooltip>
                      This is the Slack channel where information about new jobs will be posted
                    </CustomTooltip>
                  </template>
                </SelectSlackChannel>
              </div>
              <template v-if="slackData.jobs_post_channel">
                <div class="col-12 q-my-md">
                  <q-btn label="Send test Slack message" color="primary" @click="postSlackMessage()"/>
                </div>
                <div class="col-12 q-mb-md">
                  <div class="text-bold">
                    Set a schedule for when new jobs will be posted to Slack
                  </div>
                  <div>
                    <em>{{ jobPostText }}</em>
                  </div>
                </div>
                <div class="col-12 col-md-6 q-pr-md-sm q-mb-sm">
                  <SelectDayOfWeek
                    ref="jobPostDows"
                    :model-value="slackFormData.jobs_post_dows"
                    @update:modelValue="updateJobPostDow($event)"
                    :is-multi="true"
                  >
                    <template v-slot:after>
                      <CustomTooltip>
                        If unspecified, Slack messages will be posted on Monday through Friday.
                      </CustomTooltip>
                    </template>
                  </SelectDayOfWeek>
                </div>
                <div class="col-12 col-md-6 q-pl-md-sm">
                  <InputTime
                    :model-value="slackFormData.jobs_post_tod"
                    @update:modelValue="updateJobPostTod($event)"
                    :is-required="false"
                  >
                    <template v-slot:after>
                      <CustomTooltip>
                        If unspecified, Slack messages will be posted at 7:00 am UTC.
                      </CustomTooltip>
                    </template>
                  </InputTime>
                </div>
                <div class="col-12">
                  <q-input
                    v-model.number="slackFormData.jobs_post_max_jobs"
                    type="number"
                    label="Max number of jobs to post"
                    filled
                    lazy-rules
                    :rules="[
                      (val) => !val || (val > 0 && val <= 5) || 'Value must be between 1 and 5 or unspecified'
                    ]"
                  >
                    <template v-slot:after>
                      <CustomTooltip>
                        Can be between 1 to 5 jobs. If blank, up to 5 jobs will be included.
                      </CustomTooltip>
                    </template>
                  </q-input>
                </div>
              </template>
            </div>
          </q-card-section>
        </q-card>
        <q-card flat bordered>
          <q-card-section>
            <div class="row">
              <div class="col-12">
                <div class="text-bold q-mb-md">
                  Send employee referral requests about the most recent jobs to a Slack channel
                </div>
                <SelectSlackChannel v-model="slackFormData.referrals_post_channel"
                                    label="Employee referrals slack channel">
                  <template v-slot:after>
                    <CustomTooltip>
                      This is the Slack channel where employee referral requests will be posted
                    </CustomTooltip>
                  </template>
                </SelectSlackChannel>
              </div>
            </div>
            <div v-if="slackData.referrals_post_channel" class="col-12 q-my-md">
              <q-btn label="Send test Slack message" color="primary" @click="postSlackReferralMessage()"/>
            </div>
          </q-card-section>
        </q-card>
      </q-form>
    </div>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import InputTime from 'components/inputs/InputTime.vue'
import SelectDayOfWeek from 'components/inputs/SelectDayOfWeek.vue'
import SelectSlackChannel from 'components/inputs/SelectSlackChannel.vue'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import DialogSlackIntegration from 'pages/employer/settings-page/DialogSlackIntegration.vue'
import dateTimeUtil, { DAYS_OF_WEEK } from 'src/utils/datetime.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'

export default {
  name: 'IntegrationSectionSlack',
  components: { InputTime, CustomTooltip, SelectDayOfWeek, SelectSlackChannel },
  props: {
    slackData: [Object, null]
  },
  data () {
    return {
      slackFormData: {},
      q: useQuasar(),
      authStore: useAuthStore()
    }
  },
  computed: {
    hasChanged () {
      if (!this.slackData) {
        return !dataUtil.isEmpty(this.slackFormData)
      }
      return !dataUtil.isDeepEqual(this.slackData, this.slackFormData)
    },
    jobPostText () {
      let text = 'A post will be sent every'
      if (this.slackFormData.jobs_post_dows?.length) {
        text += ` ${this.slackFormData.jobs_post_dows.map((dowNum) => {
          return DAYS_OF_WEEK[dowNum].name
        }).join(', ')}`
      } else {
        text += ' Monday-Friday'
      }
      if (this.slackFormData.jobs_post_tod_minutes) {
        text += ` at ${dateTimeUtil.getTimeStrFromMinutes(this.slackFormData.jobs_post_tod_minutes)}`
        text += ` ${dateTimeUtil.getCurrentTimeZone()}`
      } else {
        text += ' at 12:00 PM UTC'
      }
      text += ' if at least one new job has been posted in the last 14 days.'
      text += ' Up to '
      text += `${dataUtil.pluralize('new job', this.slackFormData.jobs_post_max_jobs || 5)}`
      text += ' will be included in the post.'
      return text
    }
  },
  methods: {
    resetSlackFormData () {
      this.slackFormData = (this.slackData) ? { ...this.slackData } : {}
      if (this.slackFormData.jobs_post_dow_bits) {
        this.slackFormData.jobs_post_dows = dateTimeUtil.getDaysOfWeekFromBits(this.slackFormData.jobs_post_dow_bits)
      } else {
        this.slackFormData.jobs_post_dows = []
      }
      if (this.slackFormData.jobs_post_tod_minutes) {
        this.slackFormData.jobs_post_tod = dateTimeUtil.getTimeStrFromMinutes(this.slackFormData.jobs_post_tod_minutes)
      }
    },
    showSlackIntegrationDialog () {
      this.q.dialog({ component: DialogSlackIntegration })
    },
    updateJobPostDow (val) {
      this.slackFormData.jobs_post_dows = val
      this.slackFormData.jobs_post_dow_bits = this.$refs.jobPostDows.getDowBitsFromSelection()
    },
    updateJobPostTod (val) {
      this.slackFormData.jobs_post_tod = val
      const parsedTimeStr = dateTimeUtil.parseTimeStr(val)
      if (parsedTimeStr) {
        this.slackFormData.jobs_post_tod_minutes = parsedTimeStr.hour * 60 + parsedTimeStr.minute
      } else {
        this.slackFormData.jobs_post_tod_minutes = null
      }
    },
    async postSlackMessage () {
      await this.$api.post('slack/message/job/', getAjaxFormData({
        employer_id: this.authStore.propUser.employer_id,
        is_test: true
      }))
    },
    async postSlackReferralMessage () {
      await this.$api.post('slack/message/referral/', getAjaxFormData({
        employer_id: this.authStore.propUser.employer_id,
        is_test: true
      }))
    },
    async saveSlackCfg () {
      if (!this.slackFormData.id && this.slackData?.id) {
        await this.deleteSlackCfg()
      } else {
        const isGoodForm = await this.$refs.slackForm.validate()
        if (!isGoodForm) {
          return
        }
        await this.$api.post('employer/slack/', getAjaxFormData({
          ...this.slackFormData,
          employer_id: this.authStore.propUser.employer_id
        }))
      }
      this.$emit('updateEmployer')
    },
    async deleteSlackCfg () {
      openConfirmDialog(
        this.q,
        'Are you sure you want to delete your Slack integration? The configuration will not be retrievable once deleted.',
        {
          okFn: async () => {
            await this.$api.delete(`employer/slack/${this.slackData.id}/`)
            this.$emit('updateEmployer')
          }
        }
      )
    }
  },
  mounted () {
    this.resetSlackFormData()
  }
}
</script>
