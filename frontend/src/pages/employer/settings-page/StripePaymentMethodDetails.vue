<template>
  <template v-if="paymentMethod.type === 'card'">
    <div>
      <span class="text-bold">Card number: </span>
      *********{{ paymentMethod.last4 }}
    </div>
    <div>
      <span class="text-bold">Expiration: </span>
      {{ paymentMethod.exp_month }}/{{ paymentMethod.exp_year }}
    </div>
  </template>
  <template v-else-if="paymentMethod.type === 'us_bank_account'">
    <div>
      <span class="text-bold">Account number: </span>
      *********{{ paymentMethod.last4 }}
    </div>
    <div>
      <span class="text-bold">Account type: </span>
      {{ dataUtil.capitalize(paymentMethod.account_type) }}
    </div>
  </template>
</template>

<script>
import dataUtil from 'src/utils/data.js'

export default {
  name: 'StripePaymentMethodDetails',
  props: {
    paymentMethod: Object
  },
  data () {
    return {
      dataUtil
    }
  }
}
</script>

<style scoped>

</style>
