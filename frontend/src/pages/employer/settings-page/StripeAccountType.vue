<template>
  <span v-if="paymentMethod.type === 'card'">Card</span>
  <span v-else-if="paymentMethod.type === 'us_bank_account'">Bank account</span>
  <q-chip v-if="paymentMethod.is_default && isShowDefault" label="Default" color="positive" dense/>
</template>

<script>
export default {
  name: 'StripeAccountType',
  props: {
    paymentMethod: Object,
    isShowDefault: {
      type: Boolean,
      default: true
    }
  }
}
</script>
