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
          <q-btn
            class="btn-bordered"
            ripple color="primary"
            @click="redirectAuthUrl('linkedin-oauth2')"
          >
            <q-icon tag="div" name="fa-brands fa-linkedin-in" class="q-mr-sm"/>
            <div class="text-center">
              Connect LinkedIn
            </div>
          </q-btn>
        </div>
        <div class="col-12">
          <q-table
            :rows="socialCredentialList"
            :columns="socialCredentialColumns"
            :rows-per-page-options="[100]"
            :hide-bottom="true"
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
                  <q-btn
                    color="gray-500" no-wrap dense icon="sync" label="Refresh" class="q-pr-sm"
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
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta } from 'quasar'
import colorUtil from 'src/utils/color.js'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useSocialAuthStore } from 'stores/social-auth-store.js'

export default {
  name: 'SocialAccountsPage',
  components: { PageHeader },
  data () {
    return {
      colorUtil,
      dataUtil,
      SOCIAL_KEY_LINKED_IN: 'LinkedIn',
      SOCIAL_KEY_FACEBOOK: 'Facebook'
    }
  },
  computed: {
    socialCredentialList () {
      return Object.values(this.socialCredentials).reduce((allVals, platformVals) => {
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
    const socialAuthStore = useSocialAuthStore()
    const { socialCredentials } = storeToRefs(socialAuthStore)

    const pageTitle = 'Social Accounts'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      socialAuthStore,
      socialCredentials
    }
  }
}
</script>

<style scoped>

</style>
