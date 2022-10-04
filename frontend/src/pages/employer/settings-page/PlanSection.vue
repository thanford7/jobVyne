<template>
  <div v-if="isLoaded" class="jv-plans border-1-gray-300 border-rounded q-mt-lg">
    <q-btn-toggle
      v-model="formData.plan_period"
      :options="[
        {label: 'Monthly', value: PLAN_PERIODS.month},
        {label: 'Yearly (30% discount)', value: PLAN_PERIODS.year},
      ]"
      class="jv-plans__cycle"
      unelevated
      toggle-color="primary" color="grey-3" text-color="grey-7"
    />
    <q-btn
      v-if="canClose"
      dense flat icon="close"
      class="jv-plans__close"
      @click="$emit('close')"
    />
    <div class="row q-px-md q-pt-md q-mt-md">
      <div v-if="subscription" class="col-12 text-center">
        Update your plan. You will be charged a prorated amount based on the length
        of time remaining in your existing subscription term. If you change from a monthly
        plan to a yearly plan or vice versa, the billing period will be updated.
      </div>
      <div v-else class="col-12 text-center">
        Select a plan
      </div>
      <div v-for="plan in getPricesForInterval().tiers" class="col-12 col-md-6 q-px-xs q-py-sm q-px-md-sm q-my-md-md">
        <q-card class="h-100 jv-plans__price" :class="isNotEnoughSeats(plan) ? 'bg-grey-3' : ''">
          <h6 class="q-px-md q-py-sm q-my-none" :class="(plan.is_selected) ? 'jv-plans__price--selected' : ''">
            {{ plan.name }}
          </h6>
          <q-separator/>
          <q-card-section class="q-mb-lg">
            <div>
              <table class="table">
                <tbody>
                <tr>
                  <td class="text-bold">Price per seat</td>
                  <td>{{ subscriptionUtil.getPlanPriceText(plan) }}</td>
                </tr>
                <tr>
                  <td class="text-bold">
                    Employee seats
                    <CustomTooltip icon_size="16px">
                      Only users with the "Employee" type are counted towards these seats.
                      Users with only the "Employer" type (e.g. Admin, HR) are not included.
                    </CustomTooltip>
                  </td>
                  <td>{{ subscriptionUtil.getSeatsRange(plan) }}</td>
                </tr>
                <tr v-if="plan.seat_step">
                  <td>
                    <span class="text-bold">Selected seats</span>
                    <div class="text-small">({{ plan.seat_step }} seat increment)</div>
                  </td>
                  <td>
                    <q-input
                      :model-value="plan.selected_seats"
                      @update:model-value="plan.selected_seats = $event"
                      @blur.prevent="updateSelectedSeats(plan)"
                      type="number"
                      flat hide-bottom-space dense outlined
                      :step="plan.seat_step"
                      :min="dataUtil.roundTo(plan.lower_count, plan.seat_step)"
                      :max="plan.upper_count"
                    />
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </q-card-section>
          <CustomTooltip v-if="isNotEnoughSeats(plan)" :is_include_icon="false">
            <template v-slot:content>
              <q-btn
                disabled
                color="grey-6" unelevated square
                class="w-100 border-bottom-rounded jv-plans__select-btn"
                @click="createSubscription(plan)"
              >
                Select plan ({{ getTotalPlanPrice(plan) }})
              </q-btn>
            </template>
            There are currently too many active employees for this plan. If you wish to choose this plan,
            deactivate some employees from the Users page
          </CustomTooltip>
          <q-btn
            v-else
            color="grey-6" unelevated square
            class="w-100 border-bottom-rounded jv-plans__select-btn"
            @click="createSubscription(plan)"
          >
            Select plan ({{ getTotalPlanPrice(plan) }})
          </q-btn>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import { Loading } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import subscriptionUtil from 'src/utils/subscription.js'
import { useBillingStore } from 'stores/billing-store.js'

const PLAN_PERIODS = {
  month: 'month',
  year: 'year'
}

const PLAN_TIER_NAMES = ['Starter', 'Growing', 'Mature', 'Enterprise']
const PLAN_SEAT_STEP = [null, 10, 25, null]

export default {
  name: 'PlanSection',
  components: { CustomTooltip },
  props: {
    employeeCount: [Number, null],
    employerId: [Number, null],
    subscription: [Object, null],
    canClose: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoaded: false,
      PLAN_PERIODS,
      planData: null,
      formData: {
        plan_period: PLAN_PERIODS.year
      },
      dataUtil,
      subscriptionUtil
    }
  },
  methods: {
    getPricesForInterval () {
      const priceSchedule = this.planData.prices.find((price) => {
        return price.interval === this.formData.plan_period
      })
      return priceSchedule
    },
    getTotalPlanPrice (plan) {
      return this.subscriptionUtil.getTotalPlanPrice(plan, this.formData.plan_period)
    },
    isNotEnoughSeats (plan) {
      return plan.upper_count && this.employeeCount && this.employeeCount > plan.upper_count
    },
    updateSelectedSeats (plan) {
      plan.selected_seats = dataUtil.roundTo(parseInt(plan.selected_seats), plan.seat_step)
    },
    async createSubscription (plan) {
      const prices = this.getPricesForInterval()
      const data = {
        employer_id: this.employerId,
        price_id: prices.id,
        quantity: plan.selected_seats
      }
      await this.$api.post('billing/subscription/', getAjaxFormData(data))
      this.$emit('updateSubscription')
    }
  },
  setup () {
    return {
      billingStore: useBillingStore()
    }
  },
  async mounted () {
    Loading.show()
    await this.billingStore.setProducts()
    const plans = this.billingStore.getProducts()
    this.planData = plans.find((plan) => plan.name === 'Normal plan')
    this.planData.prices.forEach((priceSchedule) => {
      priceSchedule.tiers.push({
        unit_amount: 'Contact sales',
        lower_count: '> 1,000'
      })
      priceSchedule.tiers.forEach((tier, idx) => {
        tier.name = PLAN_TIER_NAMES[idx]
        tier.seat_step = PLAN_SEAT_STEP[idx]
        tier.is_selected = false
        if (
          this.subscription &&
          this.subscription.quantity >= tier.lower_count &&
          this.subscription.quantity <= tier.upper_count
        ) {
          tier.is_selected = true
        }
        if (tier.is_selected) {
          tier.selected_seats = this.subscription.quantity
        } else if (idx === 0) {
          tier.selected_seats = tier.upper_count
        } else if (tier.lower_count && tier.upper_count && dataUtil.isBetween(this.employeeCount, tier.lower_count, tier.upper_count)) {
          tier.selected_seats = this.employeeCount
        } else {
          tier.selected_seats = tier.lower_count
        }
        if (tier.seat_step) {
          tier.selected_seats = dataUtil.roundTo(tier.selected_seats, tier.seat_step)
        }
      })
    })
    Loading.hide()
    this.isLoaded = true
  }
}
</script>

<style lang="scss" scoped>
.jv-plans {
  position: relative;

  &__cycle {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateY(-50%) translateX(-50%);
  }

  &__select-btn {
    position: absolute;
    bottom: 0;

    &:hover {
      background-color: $accent !important;
    }
  }

  &__price {
    position: relative;

    &--selected {
      background-color: $secondary;
      color: $white;
      border-top-right-radius: 4px;
      border-top-left-radius: 4px;
    }

    &__selected {
      position: absolute;
      top: 0;
      left: 50%;
      transform: translateY(-75%) translateX(-50%);
      background-color: $gray-100;
      padding: 4px 8px;
      border-radius: 4px;
    }
  }

  &__close {
    position: absolute;
    top: 0;
    right: 0;
  }
}
</style>
