<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Users"/>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="users" label="Users"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="users">
          <div class="row q-mt-md q-gutter-y-md">
            <div class="col-12">
              <UserTable :is-admin-mode="true"/>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import UserTable from 'pages/employer/user-management-page/UserTable.vue'
import { useMeta } from 'quasar'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'UsersPage',
  components: { UserTable, PageHeader },
  data () {
    return {
      tab: 'users'
    }
  },
  setup () {
    const globalStore = useGlobalStore()
    const pageTitle = 'Users Admin'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>
