<template>
  <DialogBase
    base-title-text="Share post"
    :primary-button-text="btnText"
    :is-loading="isAjaxActive"
    :is-valid-form-fn="isValidForm"
    :ok-fn="sharePost"
  >
    <q-form ref="form">
      <div class="row">
        <div class="col-12">
          <SelectJobBoard
            v-model="formData.social_link"
            :is-required="true"
            :is-employer="false"
          >
            <template v-slot:after>
              <CustomTooltip>
                This is the job board where the latest jobs will be shown. The link in the post
                will direct to the job board web page.
              </CustomTooltip>
            </template>
          </SelectJobBoard>
        </div>
        <div class="col-12 q-mb-sm">
          <div class="text-bold">Accounts to post to:</div>
          <q-field
            ref="creds"
            :model-value="selectedPostAccounts"
            lazy-rules
            :rules="[
              (val) => val?.length || 'You must select at least one account to post to'
            ]"
            borderless dense
          >
            <template v-slot:control>
              <q-checkbox v-for="cred in socialCredentials" v-model="formData.post_account_ids[cred.id]">
                <q-img
                  v-if="socialUtil.getPlatformLogo({ platformName: cred.platform_name })"
                  :src="socialUtil.getPlatformLogo({ platformName: cred.platform_name})"
                  width="18px"
                />
                {{ cred.email }}
              </q-checkbox>
            </template>
          </q-field>
          <div v-if="!socialCredentials || !socialCredentials.length">
            <q-icon name="warning" color="warning" size="24px"/>
            No social accounts connected. Connect your account on the "Accounts" tab
          </div>
        </div>
        <div class="col-12">
          <q-input
            v-model="formData.content"
            filled autogrow
            label="Post text"
            type="textarea"
          >
            <template v-slot:after>
              <CustomTooltip>
                The live view box below will show the full text, including the open jobs.
              </CustomTooltip>
            </template>
          </q-input>
        </div>
        <div class="col-12">
          <PostLiveView
            :social-link="formData.social_link"
            :content="formData.content"
            :max-char-count="maxPostCharLength"
          />
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
        <FormAutoPost ref="autoPost" :post="post" class="col-12 q-mt-md"/>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import SelectJobBoard from 'components/inputs/SelectJobBoard.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import dataUtil from 'src/utils/data.js'
import FormAutoPost from 'components/dialogs/dialog-social-content/FormAutoPost.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'
import PostLiveView from 'pages/content-page/PostLiveView.vue'
import emailUtil from 'src/utils/email.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useSocialAuthStore } from 'stores/social-auth-store.js'

export default {
  name: 'DialogShareSocialPost',
  extends: DialogBase,
  inheritAttrs: false,
  components: { FormAutoPost, DialogBase, SelectJobBoard, PostLiveView },
  props: {
    isEmployer: {
      type: Boolean,
      default: false
    },
    post: [Object, null]
  },
  data () {
    return {
      socialCredentials: [],
      formData: {
        social_link: null,
        content: '',
        post_account_ids: {},
        is_post_now: true
      },
      isAjaxActive: false,
      user: null,
      socialAuthStore: null,
      socialUtil
    }
  },
  computed: {
    templatePostContent () {
      return `\n\n${emailUtil.PLACEHOLDER_JOBS_LIST.placeholder}\n\nView and apply for all jobs here: ${emailUtil.PLACEHOLDER_JOB_LINK.placeholder}`
    },
    maxPostCharLength () {
      // Get the minimum post length of all the selected social posts
      // For example if LinkedIn and Facebook are selected, we want to find the social with the lowest character count
      return this.selectedPostAccounts.reduce((totalMaxLength, acct) => {
        const maxLength = socialUtil.platformCfgs[acct.platform_name].characterLimit
        if (!totalMaxLength) {
          return maxLength
        }
        if (!dataUtil.isNil(maxLength)) {
          return Math.min(totalMaxLength, maxLength)
        }
        return totalMaxLength
      }, null)
    },
    selectedPostAccounts () {
      return Object.entries(this.formData.post_account_ids).reduce((data, [postAccountId, isShare]) => {
        if (!isShare) {
          return data
        }
        data.push(this.socialCredentials.find((cred) => cred.id === Number.parseInt(postAccountId)))
        return data
      }, [])
    },
    btnText () {
      const autoPostData = this.$refs?.autoPost?.getFormData() || {}
      if (this.formData.is_post_now && autoPostData.is_auto_post) {
        return 'Post & Save'
      } else if (this.formData.is_post_now) {
        return 'Post'
      }
      return 'Save'
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.isValidForm() && await this.$refs.autoPost.isValidForm()
    },
    async sharePost () {
      this.isAjaxActive = true
      await this.$api.put('social-post/', getAjaxFormData(Object.assign(
        {
          post_id: this.post?.id,
          social_link_id: this.formData.social_link.id,
          post_account_ids: this.selectedPostAccounts.map((acct) => acct.id),
          user_id: (this.isEmployer) ? null : this.user.id,
          employer_id: (this.isEmployer) ? this.user.employer_id : null,
          content: this.formData.content,
          is_post_now: this.formData.is_post_now
        }, this.$refs.autoPost.getFormData()
      ))).finally(() => {
        this.isAjaxActive = false
        this.$emit('ok')
      })
    }
  },
  async mounted () {
    const { user } = storeToRefs(useAuthStore())
    this.user = user
    this.socialAuthStore = useSocialAuthStore()
    await this.socialAuthStore.setUserSocialCredentials()
    this.socialCredentials = Object.entries(this.socialAuthStore.getUserSocialCredentials()).reduce((allCreds, [platformName, platformCreds]) => {
      if ([socialUtil.SOCIAL_KEY_LINKED_IN].includes(platformName)) {
        return [...allCreds, ...platformCreds]
      }
      return allCreds
    }, [])
    if (this.post) {
      Object.assign(this.formData, dataUtil.pick(this.post, Object.keys(this.formData)))
    }
    this.formData.post_account_ids = {}
    this.socialCredentials.forEach((cred) => {
      this.formData.post_account_ids[cred.id.toString()] = (this.post) ? this.post.post_account_ids.includes(cred.id) : true
    })
    if (!this.formData.content) {
      this.formData.content = this.templatePostContent
    }
  }
}
</script>
