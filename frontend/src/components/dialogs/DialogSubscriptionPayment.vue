<template>
  <DialogBase
    :base-title-text="`Submit subscription payment (${subscriptionUtil.getFormattedPrice(subscription.total_price)})`"
    primary-button-text="Submit payment"
    :ok-fn="submitPayment"
  >
    <q-form ref="billingForm">
      <div class="row q-gutter-y-sm">
        <BillingInformationFields :billing-data="billingData" :is-dialog="true"/>
      </div>
    </q-form>
    <StripePaymentFields
      v-if="!paymentMethod"
      ref="paymentMethod"
      :is-dialog="true"
      :billing-data="billingData"
      :employer-data="employerData"
      :invoice="subscription.latest_invoice"
    />
    <div v-else class="row">
      <div class="col-12 q-mb-sm">
        <span class="text-bold">Payment method</span>
        <CustomTooltip icon_size="16px" :is_include_space="true">
          If you wish to use a different payment method, change the default payment method in the billing settings
        </CustomTooltip>
      </div>
      <div class="col-12">
        <q-card flat bordered>
          <q-card-section class="q-pt-sm">
            <div class="text-h6 q-mb-sm">
              <StripeAccountType :payment-method="paymentMethod" :is-show-default="false"/>:
              {{ dataUtil.capitalize(paymentMethod.institution) }}
            </div>
            <q-separator/>
            <StripePaymentMethodDetails :payment-method="paymentMethod"/>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import BillingInformationFields from 'pages/employer/settings-page/BillingInformationFields.vue'
import StripeAccountType from 'pages/employer/settings-page/StripeAccountType.vue'
import StripePaymentFields from 'pages/employer/settings-page/StripePaymentFields.vue'
import StripePaymentMethodDetails from 'pages/employer/settings-page/StripePaymentMethodDetails.vue'
import { getAjaxFormData } from 'src/utils/requests.js'
import dataUtil from 'src/utils/data.js'
import subscriptionUtil from 'src/utils/subscription.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export const loadDialogSubscriptionPaymentFn = async () => {
  const authStore = useAuthStore()
  const employerStore = useEmployerStore()
  await authStore.setUser()
  await employerStore.setEmployerBilling(authStore.propUser.employer_id)
}

export default {
  name: 'DialogSubscriptionPayment',
  extends: DialogBase,
  inheritAttrs: false,
  props: {
    employerData: Object,
    subscription: Object,
    paymentMethod: [Object, null]
  },
  components: {
    StripePaymentMethodDetails,
    StripeAccountType,
    StripePaymentFields,
    BillingInformationFields,
    DialogBase
  },
  data () {
    const authStore = useAuthStore()
    const employerStore = useEmployerStore()
    return {
      dataUtil,
      subscriptionUtil,
      billingData: employerStore.getEmployerBilling(authStore.propUser.employer_id)
    }
  },
  methods: {
    async submitPayment () {
      // First save the billing data
      const isValidForm = await this.$refs.billingForm.validate()
      if (!isValidForm) {
        return
      }
      await this.$api.put(`employer/billing/${this.employerData.id}/`, getAjaxFormData(this.billingData))

      // Then submit the payment
      if (this.paymentMethod) {
        await this.$api.post('billing/invoice-pay/', getAjaxFormData({
          payment_method_id: this.paymentMethod.id,
          invoice_id: this.subscription.latest_invoice.id
        }))
      } else {
        // This will result in a page reload if successful
        await this.$refs.paymentMethod.submitPayment()
      }
    }
  }
}
</script>
