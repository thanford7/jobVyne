<template>
  <DialogBase
    base-title-text="Share post"
    primary-button-text="Share"
    :is-loading="isAjaxActive"
    :ok-fn="sharePost"
  >
    <div class="row">
      <div class="col-12 col-md-6 q-pr-md-sm">
        <template v-for="(creds, platform) in socialAuthStore.socialCredentials">
          <div class="text-bold">{{ platform }}</div>
          <q-checkbox v-for="cred in creds" v-model="formData[`${platform}|${cred.email}`]" :label="cred.email"/>
        </template>
      </div>
    </div>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import { getAjaxFormData } from 'src/utils/requests.js'
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
  components: { DialogBase },
  props: {
    post: Object
  },
  data () {
    return {
      formData: {},
      isAjaxActive: false,
      authStore: null,
      socialAuthStore: null
    }
  },
  computed: {
    socialCredentials () {
      if (!this.socialAuthStore) {
        return null
      }
      return this.socialAuthStore.socialCredentials
    }
  },
  watch: {
    socialCredentials () {
      if (!this.socialCredentials) {
        return
      }
      Object.values(this.socialCredentials).forEach((creds) => {
        creds.forEach((cred) => {
          this.formData[`${cred.platform_name}|${cred.email}`] = false
        })
      })
    }
  },
  methods: {
    async sharePost () {
      this.isAjaxActive = true
      const postAccounts = Object.entries(this.formData).reduce((data, [key, isShare]) => {
        if (!isShare) {
          return data
        }
        const [platform, email] = key.split('|')
        const cred = this.socialCredentials[platform].find((c) => c.email === email)
        data.push(cred)
        return data
      }, [])
      if (!postAccounts.length) {
        return
      }
      await this.$api.post('social-post/share/', getAjaxFormData({
        post_id: this.post.id,
        post_accounts: postAccounts
      })).finally(() => {
        this.isAjaxActive = false
      })
    }
  },
  mounted () {
    this.authStore = useAuthStore()
    this.socialAuthStore = useSocialAuthStore()
  }
}
</script>
