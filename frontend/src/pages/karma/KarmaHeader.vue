<template>
  <PageHeader :is-include-logo="true" :is-include-sidebar-toggle="true">
    <template v-slot:title>
      <div class="self-center title">
        <h4 class="q-mb-none text-center">KARMA CONNECT</h4>
        <div class="text-center">Do Good While Doing Good</div>
      </div>
    </template>
  </PageHeader>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'

export default {
  name: 'KarmaHeader',
  components: { PageHeader }
}
</script>
