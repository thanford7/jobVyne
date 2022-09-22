<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Payments configuration"/>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="products" label="Products"/>
        <q-tab name="accounts" label="Accounts"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="products">
          <div class="row q-mt-md q-gutter-y-md">
            <div class="col-12"></div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="accounts">
          <div class="row q-mt-md q-gutter-y-md">
            <div class="col-12">Coming soon</div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'

export default {
  name: 'PaymentsPage',
  components: { PageHeader },
  data () {
    return {
      tab: 'products'
    }
  }
}
</script>
