<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Social accounts">
        Connecting your social accounts allows you to save content and use "pre-packaged"
        content from your employer which can be pushed to your social accounts with one
        button click.
      </PageHeader>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12">
          <CollapsableCard title="LinkedIn">
            <template v-slot:header>
              <q-btn
                unelevated dense
                label="Connect account" icon="power" color="primary"
                @click="redirectAuthUrl(SOCIAL_KEY_LINKED_IN)"
              />
            </template>
            <template v-slot:body>
              <div class="q-px-md">
                <q-list>
                  <q-item
                    v-for="cred in (socialCredentials[SOCIAL_KEY_LINKED_IN] || [])"
                  >
                    <q-item-section>
                      <div class="flex items-center">
                        <q-icon name="check_circle" color="positive" class="q-mr-sm"/>
                        {{ cred.email }}
                      </div>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>
            </template>
          </CollapsableCard>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import CollapsableCard from 'components/CollapsableCard.vue'
import PageHeader from 'components/PageHeader.vue'
import { Loading, useMeta } from 'quasar'
import colorUtil from 'src/utils/color.js'
import dataUtil from 'src/utils/data.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useSocialAuthStore } from 'stores/social-auth-store.js'

export default {
  name: 'SocialAccountsPage',
  components: { CollapsableCard, PageHeader },
  data () {
    return {
      colorUtil,
      SOCIAL_KEY_LINKED_IN: 'LinkedIn',
      SOCIAL_KEY_FACEBOOK: 'Facebook'
    }
  },
  methods: {
    async redirectAuthUrl (provider) {
      window.location.href = await this.socialAuthStore.getOauthUrl(
        provider,
        {
          redirectPageUrl: window.location.pathname,
          redirectParams: dataUtil.getQueryParams(),
          isLogin: false
        }
      )
    }
  },
  computed: {
    socialCredentials () {
      return this.socialAuthStore.socialCredentials || {}
    }
  },
  preFetch () {
    const socialAuthStore = useSocialAuthStore()
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        socialAuthStore.setUserSocialCredentials()
      ])
    }).finally(() => Loading.hide())
  },
  setup () {
    const globalStore = useGlobalStore()
    const pageTitle = 'Social Accounts'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      socialAuthStore: useSocialAuthStore()
    }
  }
}
</script>

<style scoped>

</style>
