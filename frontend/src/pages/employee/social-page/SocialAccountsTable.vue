<template>
  <div class="row q-gutter-y-md">
    <div class="col-12 q-gutter-sm">
      <AuthSocialButton
        v-for="platform in allowedPlatforms"
        :platform="platform"
        :button-text="`Connect with ${platform.name}`"
        @click="redirectAuthUrl(platform.redirectProvider)"
      />
    </div>
    <div class="col-12">
      <q-table
        :loading="isTableLoading"
        :rows="socialCredentialList"
        :columns="socialCredentialColumns"
        :rows-per-page-options="[100]"
        no-data-label="No current accounts"
      >
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
            >
              {{ col.label }}
            </q-th>
            <q-th auto-width>
              Actions
            </q-th>
          </q-tr>
        </template>

        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
            >
              <template v-if="col.name === 'expiration_dt'">
                <q-chip
                  v-if="props.row.daysToExpiration && props.row.daysToExpiration < 8"
                  dense
                  :color="getExpirationColor(props.row.daysToExpiration)"
                  title="Use the refresh button to extend the expiration date"
                >
                  {{ dataUtil.pluralize('day', props.row.daysToExpiration) }} left
                </q-chip>
                {{ col.value }}
              </template>
              <span v-else>{{ col.value }}</span>
            </q-td>
            <q-td auto-width>
              <AuthSocialButton
                :platform="socialUtil.platformCfgs[props.row.platform_name]"
                :button-text="`Refresh with ${props.row.platform_name}`"
                @click="redirectAuthUrl(props.row.provider)"
              />
            </q-td>
          </q-tr>
          <q-tr v-show="props.expand" :props="props">
            <q-td colspan="100%">
              <div class="text-left">This is expand slot for row above: {{ props.row.name }}.</div>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script>
import AuthSocialButton from 'components/AuthSocialButton.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import colorUtil from 'src/utils/color.js'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import socialUtil from 'src/utils/social.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useSocialAuthStore } from 'stores/social-auth-store.js'

export default {
  name: 'SocialAccountsTable',
  components: { AuthSocialButton },
  props: {
    excludePlatforms: {
      type: Array,
      default: () => ([])
    }
  },
  data () {
    return {
      isTableLoading: true,
      // Not all platforms are currently supported, only show the ones that are
      platforms: [
        socialUtil.platformCfgs[socialUtil.SOCIAL_KEY_LINKED_IN],
        socialUtil.platformCfgs[socialUtil.SOCIAL_KEY_GOOGLE]
      ],
      colorUtil,
      dataUtil,
      socialUtil
    }
  },
  computed: {
    socialCredentialList () {
      if (!this.socialCredentials) {
        return []
      }
      return Object.entries(this.socialCredentials).reduce((allVals, [platformName, platformVals]) => {
        if (this.excludePlatforms.includes(platformName)) {
          return allVals
        }
        platformVals.forEach((cred) => {
          if (!cred.expiration_dt) {
            cred.daysToExpiration = null
          } else {
            cred.daysToExpiration = dateTimeUtil.getDateDifference(dateTimeUtil.now(), cred.expiration_dt, 'days')
          }
        })
        return [...allVals, ...platformVals]
      }, [])
    },
    socialCredentialColumns () {
      return [
        { name: 'platform_name', field: 'platform_name', label: 'Platform', align: 'left', sortable: true },
        { name: 'email', field: 'email', label: 'Account', align: 'left', sortable: true },
        {
          name: 'expiration_dt',
          field: 'expiration_dt',
          label: 'Expiration',
          align: 'left',
          format: (val) => (val) ? dateTimeUtil.getShortDate(val) : 'Unknown',
          sortable: true,
          sort: dateTimeUtil.sortDatesFn.bind(dateTimeUtil)
        }
      ]
    },
    allowedPlatforms () {
      return this.platforms.filter((platform) => !this.excludePlatforms.includes(platform.name))
    }
  },
  methods: {
    getExpirationColor (daysToExpiration) {
      if (daysToExpiration > 7) {
        return 'positive'
      } else if (daysToExpiration > 2) {
        return 'warning'
      }
      return 'negative'
    },
    async redirectAuthUrl (provider) {
      const socialAuthUrl = await this.socialAuthStore.getOauthUrl(
        provider,
        {
          redirectPageUrl: window.location.pathname,
          redirectParams: dataUtil.getQueryParams(),
          isLogin: false
        }
      )
      window.location.href = socialAuthUrl
    }
  },
  async mounted () {
    await this.authStore.setUser()
    await this.socialAuthStore.setUserSocialCredentials()
    this.isTableLoading = false
  },
  setup () {
    const socialAuthStore = useSocialAuthStore()
    const { socialCredentials } = storeToRefs(socialAuthStore)

    return {
      authStore: useAuthStore(),
      socialAuthStore,
      socialCredentials
    }
  }
}
</script>
