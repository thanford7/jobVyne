<template>
  <div class="row">
    <div class="col-12 q-gutter-y-md">
      <IntegrationSectionAts
        v-if="isEmployerOrgType"
        class="border-bottom-1-gray-100"
        :ats-data="employerData.ats_cfg"
        @update-employer="$emit('updateEmployer')"
      />
      <IntegrationSectionSlack
        :slack-data="employerData.slack_cfg"
        :is-employer-org-type="isEmployerOrgType"
        @update-employer="$emit('updateEmployer')"
      />
    </div>
  </div>
</template>

<script>
import IntegrationSectionAts from 'pages/employer/settings-page/IntegrationSectionAts.vue'
import IntegrationSectionSlack from 'pages/employer/settings-page/IntegrationSectionSlack.vue'
import employerTypeUtil from 'src/utils/employer-types.js'

export default {
  name: 'IntegrationSection',
  components: { IntegrationSectionSlack, IntegrationSectionAts },
  props: {
    employerData: Object
  },
  computed: {
    isEmployerOrgType () {
      return employerTypeUtil.isTypeEmployer(this.employerData.organization_type)
    }
  }
}
</script>
