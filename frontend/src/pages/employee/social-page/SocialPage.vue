<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Social sharing">
        Connect your social accounts to automatically post jobs.
      </PageHeader>
      <SocialAccountsTable :exclude-platforms="[socialUtil.SOCIAL_KEY_GOOGLE]"/>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import SocialAccountsTable from 'pages/employee/social-page/SocialAccountsTable.vue'
import { useMeta } from 'quasar'
import socialUtil from 'src/utils/social.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'SocialPage',
  components: { SocialAccountsTable, PageHeader },
  data () {
    return {
      socialUtil
    }
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Social Accounts'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>
