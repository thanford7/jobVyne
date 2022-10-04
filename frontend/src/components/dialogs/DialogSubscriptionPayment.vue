<template>
  <DialogBase
    :base-title-text="`Submit subscription payment (${subscriptionUtil.getFormattedSubscriptionPrice(subscription)})`"
    primary-button-text="Submit payment"
    @ok="submitPayment"
  >
    <div class="row q-gutter-y-sm">
      <BillingInformationFields :billing-data="billingData" :is-dialog="true"/>
    </div>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import BillingInformationFields from 'pages/employer/settings-page/BillingInformationFields.vue'
import subscriptionUtil from 'src/utils/subscription.js'

export default {
  name: 'DialogSubscriptionPayment',
  extends: DialogBase,
  inheritAttrs: false,
  props: {
    billingData: Object,
    subscription: Object
  },
  components: { BillingInformationFields, DialogBase },
  data () {
    return {
      subscriptionUtil
    }
  },
  methods: {
    submitPayment () {
      //
    }
  }
}
</script>
