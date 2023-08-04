<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="User Created Jobs"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12 q-gutter-sm">
          <UserJobsTable :is-admin="true"/>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import UserJobsTable from 'pages/admin/user-jobs-page/UserJobsTable.vue'

export default {
  name: 'UserJobsPage',
  components: { UserJobsTable, PageHeader }
}
</script>
