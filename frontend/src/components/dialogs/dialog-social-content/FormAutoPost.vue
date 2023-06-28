<template>
  <div>
    <div>
      <span class="text-bold">Auto-post </span>
      <CustomTooltip icon_size="24px">
        It's tough to stay on top of all the new jobs at your company. Auto-post will post to your account(s) on the
        cadence you specify and will update the post with the most recent jobs. The post will only be sent if there
        is at least one open job.
      </CustomTooltip>
    </div>
    <q-toggle
      v-model="formData.is_auto_post"
      :label="(formData.is_auto_post) ? 'On' : 'Off'"
    />
    <q-form v-if="formData.is_auto_post" ref="form">
      <div class="row q-gutter-y-xs">
        <div class="col-12 col-md-6 q-pr-md-sm q-mb-md q-mb-md-none">
          <DateSelector v-model="formData.auto_start_date" label="Start date"/>
        </div>
        <div class="col-12 col-md-6">
          <InputTime v-model="formData.auto_time"/>
        </div>
        <div class="col-12 col-md-6 q-pr-md-sm">
          <q-input
            v-model.number="formData.auto_weeks_between"
            label="Weeks between post"
            type="number"
            filled
            :rules="[
                 val => val && val > 0 || 'Value is required and must be greater than 0'
              ]"
          />
        </div>
        <div class="col-12 col-md-6">
          <SelectDayOfWeek v-model="formData.auto_day_of_week"/>
        </div>
        <div class="col-12 text-small">
          <q-icon name="info"/>
          {{ nextPosts }}
        </div>
      </div>
    </q-form>
  </div>
</template>

<script>
/* eslint-disable camelcase */
import CustomTooltip from 'components/CustomTooltip.vue'
import DateSelector from 'components/inputs/DateSelector.vue'
import InputTime from 'components/inputs/InputTime.vue'
import SelectDayOfWeek from 'components/inputs/SelectDayOfWeek.vue'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil, { DAYS_OF_WEEK } from 'src/utils/datetime.js'

export default {
  name: 'FormAutoPost',
  components: { InputTime, DateSelector, SelectDayOfWeek, CustomTooltip },
  props: {
    post: {
      type: Object,
      default: () => ({})
    }
  },
  data () {
    return {
      formData: {
        is_auto_post: (!dataUtil.isNil(this.post.is_auto_post)) ? this.post.is_auto_post : true,
        auto_weeks_between: this.post.auto_weeks_between || 2,
        auto_start_date: dateTimeUtil.serializeDate((this.post.auto_start_dt) ? this.post.auto_start_dt : new Date(), { isUTC: false }),
        auto_time: (this.post.auto_start_dt) ? dateTimeUtil.getTimeStrFromDate(this.post.auto_start_dt, { isIncludeSeconds: false }) : '07:45',
        // q-select expects a string value instead of a number
        auto_day_of_week: (!dataUtil.isNil(this.post.auto_day_of_week)) ? this.post.auto_day_of_week : 0
      },
      dateTimeUtil
    }
  },
  computed: {
    nextPosts () {
      const { is_auto_post, auto_weeks_between, auto_time, auto_day_of_week } = this.formData
      if (!(is_auto_post && auto_weeks_between && auto_time && !dataUtil.isNil(auto_day_of_week))) {
        return 'Complete all auto post fields to see next post date'
      }
      const nextPostDt = this.calculatePostDate(0)
      const secondPostDt = this.calculatePostDate(1)
      return `Next post date is ${dateTimeUtil.getDateTime(nextPostDt, { isIncludeSeconds: false })}, followed by ${dateTimeUtil.getDateTime(secondPostDt, { isIncludeSeconds: false })}`
    }
  },
  methods: {
    async isValidForm () {
      if (!this.formData.is_auto_post) {
        return true
      }
      const isValid = await this.$refs.form.validate()
      return isValid
    },
    getFormData () {
      const data = dataUtil.pick(this.formData, [
        'is_auto_post', 'auto_weeks_between', 'auto_day_of_week'
      ])
      data.auto_start_dt = this.calculatePostDate(0)
      return data
    },
    getAutoStartDt () {
      const postDt = new Date(this.formData.auto_start_date)
      const parsedVal = dateTimeUtil.parseTimeStr(this.formData.auto_time)
      let hour, minute = 0
      if (parsedVal) {
        hour = parsedVal.hour
        minute = parsedVal.minute
      }
      postDt.setHours(hour, minute, 0, 0)
      return postDt
    },
    calculatePostDate (postIdx) {
      const { auto_weeks_between, auto_day_of_week } = this.formData
      const postDt = this.getAutoStartDt()

      // Set the postDt to the next date landing on the targetDow
      const targetDow = DAYS_OF_WEEK[auto_day_of_week].jsDayOfWeek
      const postDow = postDt.getDay()
      if (targetDow !== postDow) {
        const dayDistance = (targetDow + 7 - postDow) % 7
        postDt.setDate(postDt.getDate() + dayDistance)
      }

      // Find the first occurrence of the targetDate after the current date
      const currentDt = new Date()
      while (dateTimeUtil.isBefore(postDt, currentDt)) {
        postDt.setDate(postDt.getDate() + 7)
      }

      // Get the nth occurrence based on postIdx
      postDt.setDate(postDt.getDate() + (postIdx * 7 * auto_weeks_between))
      return postDt
    }
  }
}
</script>
