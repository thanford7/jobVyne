<template>
  <DialogBase
    :base-title-text="`Share ${post.platform.name} post`"
    primary-button-text="Share"
    :is-loading="isAjaxActive"
    :is-o-k-btn-enabled="isValidForm"
    :ok-btn-help-text="validationHelpText"
    :ok-fn="sharePost"
  >
    <div class="row">
      <div class="col-12">
        <SelectJobLink
          v-if="post.employer_id"
          v-model="formData.jobLink"
          :is-required="true"
          :platform-filter="[post.platform.name]"
        />
      </div>
      <div class="col-12">
        <div class="text-bold">{{ this.post.platform.name }} account</div>
        <q-checkbox v-for="cred in socialCredentials" v-model="formData.post_accounts[cred.email]" :label="cred.email"/>
      </div>
      <div class="col-12">
        <PostLiveView
          v-if="post.employer_id"
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
  components: { DialogBase, SelectJobLink, PostLiveView },
  props: {
    post: Object
  },
  data () {
    return {
      formData: {
        post_accounts: {}
      },
      isAjaxActive: false,
      authStore: null,
      socialAuthStore: null
    }
  },
  computed: {
    isValidForm () {
      return Boolean((!this.post.employer_id || this.formData.jobLink) && this.postAccounts.length)
    },
    validationHelpText () {
      let text = 'You must select at least one social account to post to'
      if (this.post.employer_id) {
        text += ' and select a job link'
      }
      return text
    },
    platformCfg () {
      return socialUtil.platformCfgs[this.post.platform.name]
    },
    postAccounts () {
      return Object.entries(this.formData.post_accounts).reduce((data, [email, isShare]) => {
        if (!isShare) {
          return data
        }
        const cred = this.socialCredentials.find((c) => c.email === email)
        data.push(cred)
        return data
      }, [])
    },
    socialCredentials () {
      if (!this.socialAuthStore) {
        return null
      }
      return this.socialAuthStore.socialCredentials[this.post.platform.name]
    }
  },
  watch: {
    socialCredentials () {
      if (!this.socialCredentials) {
        return
      }
      Object.values(this.socialCredentials).forEach((cred) => {
        this.formData.post_accounts[cred.email] = false
      })
    }
  },
  methods: {
    async sharePost () {
      this.isAjaxActive = true
      await this.$api.post('social-post/share/', getAjaxFormData({
        post_id: this.post.id,
        post_accounts: this.postAccounts,
        formatted_content: this.formData.formatted_content,
        owner_id: (this.post.employer_id) ? this.authStore.propUser.id : null // If this post is owned by an employer, we need to copy it for the owner
      })).finally(() => {
        this.isAjaxActive = false
        this.$emit('ok')
      })
    }
  },
  mounted () {
    this.authStore = useAuthStore()
    this.socialAuthStore = useSocialAuthStore()
  }
}
</script>
