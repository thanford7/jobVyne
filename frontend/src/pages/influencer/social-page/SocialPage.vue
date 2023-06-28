<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Social sharing"/>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="accounts" label="Accounts"/>
        <q-tab name="posts" label="Posts"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="accounts">
          <div class="row q-gutter-y-sm">
            <div class="col-12 callout-card">
              Connect your social accounts to automatically post jobs
            </div>
            <div class="col-12">
              <SocialAccountsTable :exclude-platforms="[socialUtil.SOCIAL_KEY_GOOGLE]"/>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="posts">
          <div class="row q-gutter-y-sm">
            <div class="col-12">
              <SocialPostSection :is-employer="false" :is-editable="true"/>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import SocialAccountsTable from 'pages/employee/social-page/SocialAccountsTable.vue'
import SocialPostSection from 'pages/influencer/social-page/SocialPostSection.vue'
import { useMeta } from 'quasar'
import socialUtil from 'src/utils/social.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'SocialPage',
  components: { SocialPostSection, SocialAccountsTable, PageHeader },
  data () {
    return {
      tab: 'accounts',
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
