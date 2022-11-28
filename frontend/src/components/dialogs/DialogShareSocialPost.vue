<template>
  <DialogBase
    :base-title-text="`Share ${post.platform.name} post`"
    :primary-button-text="btnText"
    :is-loading="isAjaxActive"
    :is-o-k-btn-enabled="isValidForm"
    :ok-btn-help-text="validationHelpText"
    :ok-fn="sharePost"
  >
    <div class="row">
      <div class="col-12">
        <SelectJobLink
          v-model="formData.jobLink"
          :is-required="true"
          :platform-name="post.platform.name"
        />
      </div>
      <div class="col-12">
        <div class="text-bold">{{ this.post.platform.name }} account</div>
        <q-checkbox v-for="cred in socialCredentials" v-model="formData.post_accounts[cred.email]" :label="cred.email"/>
        <div v-if="!socialCredentials || !socialCredentials.length">
          <q-icon name="warning" color="warning" size="24px"/>
          No {{ this.post.platform.name }} account connected. Connect your account in the
          <a href="#" @click.prevent="goToSocialAccountsPage()">Social Accounts page</a>.
        </div>
      </div>
      <div class="col-12 q-mt-md">
        <div>
          <span class="text-bold">Post now </span>
          <CustomTooltip icon_size="24px">
            When on, this post will be sent immediately, in addition to any auto-posts in the future.
          </CustomTooltip>
        </div>
        <q-toggle
          v-model="formData.is_post_now"
          :label="(formData.is_post_now) ? 'On' : 'Off'"
        />
      </div>
      <div class="col-12 q-mt-md">
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
        <q-form v-if="formData.is_auto_post" ref="autoPost">
          <div class="row q-gutter-y-xs">
            <div class="col-12 col-md-6 q-pr-md-sm q-mb-md q-mb-md-none">
              <DateSelector v-model="formData.auto_start_date" label="Start date"/>
            </div>
            <div class="col-12 col-md-6">
              <q-input filled v-model="formData.auto_time" mask="time" :rules="['time']"
                       :label="`Time of day (${dateTimeUtil.getCurrentTimeZone()})`">
                <template v-slot:append>
                  <q-icon name="access_time" class="cursor-pointer">
                    <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                      <q-time v-model="formData.auto_time" :minute-options="[0, 15, 30, 45]">
                        <div class="row items-center justify-end">
                          <q-btn v-close-popup label="Close" color="primary" flat/>
                        </div>
                      </q-time>
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
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
      <div class="col-12">
        <PostLiveView
          :content="post.content"
          :file="(post.files) ? post.files[0] : null"
          :job-link="formData.jobLink"
          :max-char-count="platformCfg.characterLimit"
          @content-update="formData.formatted_content = $event"
        />
      </div>
    </div>
  </DialogBase>
</template>

<script>
/* eslint-disable camelcase */
import DialogBase from 'components/dialogs/DialogBase.vue'
import DateSelector from 'components/inputs/DateSelector.vue'
import SelectDayOfWeek from 'components/inputs/SelectDayOfWeek.vue'
import SelectJobLink from 'components/inputs/SelectJobLink.vue'
import PostLiveView from 'pages/content-page/PostLiveView.vue'
import dateTimeUtil, { DAYS_OF_WEEK } from 'src/utils/datetime.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useSocialAuthStore } from 'stores/social-auth-store.js'
import dataUtil from 'src/utils/data.js'

export const loadDialogShareSocialPostFn = () => {
  const socialAuthStore = useSocialAuthStore()
  const authStore = useAuthStore()
  return authStore.setUser().then(() => {
    return Promise.all([
      socialAuthStore.setUserSocialCredentials()
    ])
  })
}

export default {
  name: 'DialogShareSocialPost',
  extends: DialogBase,
  inheritAttrs: false,
  components: { DateSelector, SelectDayOfWeek, DialogBase, SelectJobLink, PostLiveView },
  props: {
    post: Object
  },
  data () {
    return {
      formData: {
        post_accounts: {},
        is_post_now: true,
        is_auto_post: (!dataUtil.isNil(this.post.is_auto_post)) ? this.post.is_auto_post : true,
        auto_weeks_between: this.post.auto_weeks_between || 2,
        auto_start_date: dateTimeUtil.serializeDate((this.post.auto_start_dt) ? this.post.auto_start_dt : new Date()),
        auto_time: (this.post.auto_start_dt) ? dateTimeUtil.getTimeStrFromDate(this.post.auto_start_dt, { isIncludeSeconds: false }) : '07:45',
        // q-select expects a string value instead of a number
        auto_day_of_week: (!dataUtil.isNil(this.post.auto_day_of_week)) ? this.post.auto_day_of_week.toString() : '0'
      },
      isAjaxActive: false,
      authStore: null,
      socialAuthStore: null,
      dateTimeUtil
    }
  },
  computed: {
    isValidForm () {
      return Boolean((!this.post.employer_id || this.formData.jobLink) && this.postAccountIds.length)
    },
    validationHelpText () {
      if (this.isValidForm) {
        return null
      }
      let text = 'You must select at least one social account to post to'
      if (this.post.employer_id) {
        text += ' and select a job link'
      }
      return text
    },
    platformCfg () {
      return socialUtil.platformCfgs[this.post.platform.name]
    },
    postAccountIds () {
      return Object.entries(this.formData.post_accounts).reduce((data, [email, isShare]) => {
        if (!isShare) {
          return data
        }
        const cred = this.socialCredentials.find((c) => c.email === email)
        data.push(cred.id)
        return data
      }, [])
    },
    socialCredentials () {
      if (!this.socialAuthStore) {
        return null
      }
      return this.socialAuthStore.socialCredentials[this.post.platform.name]
    },
    nextPosts () {
      const { is_auto_post, auto_weeks_between, auto_time, auto_day_of_week } = this.formData
      if (!(is_auto_post && auto_weeks_between && auto_time && !dataUtil.isNil(auto_day_of_week))) {
        return 'Complete all auto post fields to see next post date'
      }
      const nextPostDt = this.calculatePostDate(0)
      const secondPostDt = this.calculatePostDate(1)
      return `Next post date is ${dateTimeUtil.getDateTime(nextPostDt, { isIncludeSeconds: false })}, followed by ${dateTimeUtil.getDateTime(secondPostDt, { isIncludeSeconds: false })}`
    },
    btnText () {
      const { is_post_now, is_auto_post } = this.formData
      if (is_post_now && is_auto_post) {
        return 'Post & Save'
      } else if (is_post_now) {
        return 'Post'
      }
      return 'Save'
    }
  },
  watch: {
    socialCredentials () {
      if (!this.socialCredentials) {
        return
      }
      Object.values(this.socialCredentials).forEach((cred) => {
        this.formData.post_accounts[cred.email] = !this.post.post_account_ids.length || this.post.post_account_ids.includes(cred.id)
      })
    }
  },
  methods: {
    async sharePost () {
      this.isAjaxActive = true

      // Make sure auto post fields are good
      if (this.formData.is_auto_post) {
        const isValid = await this.$refs.autoPost.validate()
        if (!isValid) {
          return
        }
      }

      await this.$api.post('social-post/share/', getAjaxFormData(Object.assign(
        {
          post_id: this.post.id,
          post_account_ids: this.postAccountIds,
          owner_id: (this.post.employer_id) ? this.authStore.propUser.id : null, // If this post is owned by an employer, we need to copy it for the owner
          auto_start_dt: this.getAutoStartDt()
        }, dataUtil.pick(this.formData, [
          'formatted_content', 'is_post_now', 'is_auto_post', 'auto_weeks_between', 'auto_day_of_week'
        ])
      ))).finally(() => {
        this.isAjaxActive = false
        this.$emit('ok')
      })
    },
    goToSocialAccountsPage () {
      this.$emit('hide')
      this.$router.push({ name: 'employee-social-accounts' })
    },
    getAutoStartDt () {
      const postDt = new Date(this.formData.auto_start_date)
      const { hour, minute } = dateTimeUtil.parseTimeStr(this.formData.auto_time)
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
  },
  mounted () {
    this.authStore = useAuthStore()
    this.socialAuthStore = useSocialAuthStore()
  }
}
</script>
