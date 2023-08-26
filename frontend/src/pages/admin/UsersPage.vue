<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Users"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12">
          <UserTable :is-admin-mode="true"/>
        </div>
      </div>
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
