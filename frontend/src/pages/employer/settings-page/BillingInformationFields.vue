<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <div class="col-12 q-my-sm">
    <span class="text-bold">Corporate address</span>
    <CustomTooltip icon_size="16px" :is_include_space="true">
      A corporate address is required for tax purposes
    </CustomTooltip>
    <div class="text-small">* indicates optional field</div>
  </div>
  <div class="col-12">
    <div class="row q-gutter-y-md">
      <div class="col-12" :class="(isDialog) ? '' : 'col-md-8 q-pr-md-sm'">
        <q-input
          v-model="billingData.street_address"
          filled
          label="Street address*"
        />
      </div>
      <div class="col-12" :class="(isDialog) ? '' : 'col-md-4 q-pl-md-sm'">
        <q-input
          v-model="billingData.street_address_2"
          filled
          label="Apt, suite, unit, or building*"
        />
      </div>
      <div class="col-6 q-pr-sm" :class="(isDialog) ? '' : 'col-md-3'">
        <q-input
          v-model="billingData.city"
          filled
          label="City"
          lazy-rules
          :rules="[val => val && val.length || 'City is required']"
        />
      </div>
      <div class="col-6 q-pl-sm" :class="(isDialog) ? '' : 'col-md-3 q-px-md-sm'">
        <q-input
          v-model="billingData.state"
          filled
          label="State"
          lazy-rules
          :rules="[val => val && val.length || 'State is required']"
        />
      </div>
      <div class="col-6 q-pr-sm" :class="(isDialog) ? '' : 'col-md-3 q-px-md-sm'">
        <q-input
          v-model="billingData.country"
          filled
          label="Country"
          lazy-rules
          :rules="[val => val && val.length || 'Country is required']"
        />
      </div>
      <div class="col-6 q-pl-sm" :class="(isDialog) ? '' : 'col-md-3'">
        <q-input
          v-model="billingData.postal_code"
          filled
          label="Postal code"
          lazy-rules
          :rules="[val => val && val.length || 'Postal code is required']"
        />
      </div>
    </div>
  </div>
  <div class="col-12 text-bold q-my-sm">
    Account email
    <CustomTooltip icon_size="16px">
      This is the email that will receive all communications regarding billing. It can be a group or
      individual
      corporate email address
    </CustomTooltip>
  </div>
  <div class="col-12">
    <EmailInput v-model="billingData.billing_email"/>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import EmailInput from 'components/inputs/EmailInput.vue'

export default {
  name: 'BillingInformationFields',
  props: {
    billingData: Object,
    isDialog: {
      type: Boolean,
      default: false
    }
  },
  components: { CustomTooltip, EmailInput }
}
</script>
