<template>
  <q-input
    label="Days after hire payout"
    type="number"
    filled
  >
    <template v-slot:after>
      <CustomTooltip>
        The number of days required for a new hire to work after which time
        the referring employee will be eligible to receive the referral bonus.
      </CustomTooltip>
    </template>
  </q-input>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'

export default {
  name: 'InputDaysAfterHire',
  components: { CustomTooltip }
}
</script>
