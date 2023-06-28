<template>
  <q-select
    filled emit-value map-options
    label="Organization type"
    option-label="name"
    option-value="val"
    :options="orgOptions"
  >
    <template v-slot:after>
      <CustomTooltip>
        <ul>
          <li>
            <span class="text-bold">Employer:</span>
            Only hiring directly for jobs at their company
          </li>
          <li>
            <span class="text-bold">Group:</span>
            Professional group that subscribes to jobs from multiple employers
          </li>
          <li>
            <span class="text-bold">Agency:</span>
            Staffing agency that may have direct jobs and/or subscribe to jobs from
            other employers
          </li>
        </ul>
      </CustomTooltip>
    </template>
  </q-select>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import dataUtil from 'src/utils/data.js'
import employerTypeUtil from 'src/utils/employer-types.js'

export default {
  name: 'SelectOrganizationType',
  components: { CustomTooltip },
  data () {
    return {
      orgOptions: Object.entries(employerTypeUtil.ORG_TYPES).map(([orgTypeName, orgTypeValue]) => {
        return { name: dataUtil.capitalize(orgTypeName), val: orgTypeValue }
      })
    }
  }
}
</script>
