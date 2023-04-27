<template>
  <div class="row">
    <div class="col-12 q-gutter-y-md">
      <IntegrationSectionAts
        :ats-data="employerData.ats_cfg"
        @update-employer="$emit('updateEmployer')"
      />
      <IntegrationSectionSlack
        class="border-top-1-gray-100"
        :slack-data="employerData.slack_cfg"
        @update-employer="$emit('updateEmployer')"
      />
    </div>
  </div>
</template>

<script>

import IntegrationSectionAts from 'pages/employer/settings-page/IntegrationSectionAts.vue'
import IntegrationSectionSlack from 'pages/employer/settings-page/IntegrationSectionSlack.vue'
export default {
  name: 'IntegrationSection',
  components: { IntegrationSectionSlack, IntegrationSectionAts },
  props: {
    employerData: Object
  }
}
</script>
