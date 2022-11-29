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
          v-model="formData.link_filter"
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
      <FormAutoPost ref="autoPost" :post="post" class="col-12 q-mt-md"/>
      <div class="col-12">
        <PostLiveView
          :content="post.content"
          :file="(post.files) ? post.files[0] : null"
          :job-link="formData.link_filter"
          :max-char-count="platformCfg.characterLimit"
          @content-update="formData.formatted_content = $event"
        />
      </div>
    </div>
  </DialogBase>
</template>

<script>
import FormAutoPost from 'components/dialogs/dialog-social-content/FormAutoPost.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'
import SelectJobLink from 'components/inputs/SelectJobLink.vue'
import PostLiveView from 'pages/content-page/PostLiveView.vue'
import { getAjaxFormData } from 'src/utils/requests.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useSocialAuthStore } from 'stores/social-auth-store.js'

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
  components: { FormAutoPost, DialogBase, SelectJobLink, PostLiveView },
  props: {
    post: Object
  },
  data () {
    return {
      formData: {
        link_filter: this.post.link_filter_id,
        post_accounts: {},
        is_post_now: true
      },
      isAjaxActive: false,
      authStore: null,
      socialAuthStore: null
    }
  },
  computed: {
    isValidForm () {
      return Boolean((!this.post.employer_id || this.formData.link_filter) && this.postAccountIds.length)
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
      if (!await this.$refs.autoPost.isValidForm()) {
        return
      }

      await this.$api.post('social-post/share/', getAjaxFormData(Object.assign(
        {
          post_id: this.post.id,
          link_filter_id: this.formData.link_filter?.id,
          post_account_ids: this.postAccountIds,
          owner_id: (this.post.employer_id) ? this.authStore.propUser.id : null, // If this post is owned by an employer, we need to copy it for the owner
          formatted_content: this.formData.formatted_content,
          is_post_now: this.formData.is_post_now
        }, this.$refs.autoPost.getFormData()
      ))).finally(() => {
        this.isAjaxActive = false
        this.$emit('ok')
      })
    },
    goToSocialAccountsPage () {
      this.$emit('hide')
      this.$router.push({ name: 'employee-social-accounts' })
    }
  },
  mounted () {
    this.authStore = useAuthStore()
    this.socialAuthStore = useSocialAuthStore()
  }
}
</script>
