<template>
  <div class="row">
    <div class="col-12 text-bold q-my-sm">
      Payment method
    </div>
    <div class="col-12">
      <q-form ref="paymentForm" @submit.prevent="submitPayment()">
        <div :id="uniqueId">
          <!-- Stripe Elements will create form elements here -->
        </div>
        <div v-if="!isDialog" class="q-mt-sm">
          <q-btn
            label="Cancel" color="grey-6" @click="$emit('cancel')"
            class="q-mr-sm"
          />
          <q-btn
            label="Save payment details" color="accent" type="submit"
          />
        </div>
      </q-form>
    </div>
  </div>
</template>

<script>
import colorUtil from 'src/utils/color.js'
import { loadScript, removeScript } from 'src/utils/load-script.js'
import messagesUtil from 'src/utils/messages.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useBillingStore } from 'stores/billing-store.js'
import { onUnmounted } from 'vue'

const STRIPE_SCRIPT = 'https://js.stripe.com/v3/'
let uniqueCount = 0

export default {
  name: 'StripePaymentFields',
  props: {
    billingData: Object,
    employerData: Object,
    invoice: [Object, null], // If provided this is intended to pay an invoice. Otherwise this is to add a new payment method
    isDialog: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoaded: false,
      uniqueId: null,
      billingStore: null,
      stripe: null,
      stripeElements: null,
      isStripeLoaded: false,
      paymentSetupKey: null
    }
  },
  methods: {
    async submitPayment () {
      // Either submitting a payment or creating a new payment method
      const stripeFn = (this.invoice) ? this.stripe.confirmPayment : this.stripe.confirmSetup

      // This will redirect to the return url if successful
      const { error } = await stripeFn({
        elements: this.stripeElements,
        confirmParams: {
          return_url: window.location.href
        }
      })

      if (error) {
        messagesUtil.addErrorMsg(error)
      }
      this.$emit('submitted')
    },
    setupStripePaymentDom () {
      const paymentElement = document.getElementById(this.uniqueId)
      if (paymentElement && this.paymentSetupKey && !this.isStripeLoaded) {
        // Set up Stripe.js and Elements to use in checkout form
        this.stripeElements = this.stripe.elements({
          clientSecret: this.paymentSetupKey,
          appearance: {
            theme: 'stripe',
            variables: {
              colorPrimary: colorUtil.getPaletteColor('primary'),
              colorBackground: colorUtil.getPaletteColor('grey-2'),
              colorDanger: colorUtil.getPaletteColor('negative'),
              fontFamily: 'Open Sans, system-ui, sans-serif',
              borderRadius: '4px'
            }
          }
        })

        // Create and mount the Payment Element
        const paymentElement = this.stripeElements.create('payment', {
          defaultValues: {
            billingDetails: {
              name: this.employerData.name,
              email: this.billingData.billing_email,
              address: {
                line1: this.billingData.street_address,
                line2: this.billingData.street_address_2,
                city: this.billingData.city,
                state: this.billingData.state,
                country: this.billingData.country,
                postal_code: this.billingData.postal_code
              }
            }
          }
        })
        paymentElement.mount(`#${this.uniqueId}`)
        this.isStripeLoaded = true
      }
    }
  },
  setup () {
    onUnmounted(() => removeScript(STRIPE_SCRIPT))
  },
  async created () {
    this.uniqueId = `payment-element-${uniqueCount}`
    uniqueCount++
    this.billingStore = useBillingStore()
    const authStore = useAuthStore()
    await Promise.all([
      authStore.setUser(),
      this.billingStore.setIsPaymentLive()
    ])
    const employerId = authStore.propUser.employer_id
    if (!this.invoice) {
      await this.billingStore.setEmployerPaymentSetup(employerId)
      this.paymentSetupKey = this.billingStore.getEmployerPaymentSetup(employerId)
    } else {
      this.paymentSetupKey = this.invoice.payment_intent.client_secret
    }

    const stripeKey = (this.billingStore.isLive) ? process.env.STRIPE_LIVE_PUBLIC_KEY : process.env.STRIPE_PUBLIC_KEY
    await loadScript(STRIPE_SCRIPT).then(() => {
      this.stripe = window.Stripe(stripeKey)
      this.setupStripePaymentDom()
    })
  }
}
</script>
