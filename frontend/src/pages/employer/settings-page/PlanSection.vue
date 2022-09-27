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
    <div class="row q-pa-md q-mt-md">
      <div v-for="plan in getPriceTiersForInterval()" class="col-12 col-md-6 q-px-xs q-py-sm q-px-md-sm q-my-md-md">
        <q-card class="h-100">
          <div class="text-h6 q-px-md q-py-sm">{{ plan.name }}</div>
          <q-separator/>
          <q-card-section class="q-mb-lg">
            <div>
              <table class="table">
                <tbody>
                <tr>
                  <td class="text-bold">Price per seat</td>
                  <td>{{ getPlanPriceText(plan) }}</td>
                </tr>
                <tr>
                  <td class="text-bold">
                    Employee seats
                    <CustomTooltip icon_size="16px">
                      Only users with the "Employee" type are counted towards these seats.
                      Users with only the "Employer" type (e.g. Admin, HR) are not included.
                    </CustomTooltip>
                  </td>
                  <td>{{ getSeatsRange(plan) }}</td>
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
          <q-btn
            color="grey-6" unelevated square
            class="w-100 border-bottom-rounded jv-plans__select-btn"
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
    employeeCount: [Number, null]
  },
  data () {
    return {
      isLoaded: false,
      PLAN_PERIODS,
      planData: null,
      formData: {
        plan_period: PLAN_PERIODS.year
      },
      dataUtil
    }
  },
  methods: {
    getPriceTiersForInterval () {
      const priceSchedule = this.planData.prices.find((price) => {
        return price.interval === this.formData.plan_period
      })
      return priceSchedule.tiers
    },
    getPlanPriceText (plan) {
      const price = plan.unit_amount
      if (Number.isFinite(price)) {
        return dataUtil.formatCurrency(price, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
      }
      return price
    },
    getSeatsRange (plan) {
      if (!plan.lower_count || !plan.upper_count) {
        return plan.lower_count || plan.upper_count
      }
      return `${plan.lower_count}-${plan.upper_count}`
    },
    getTotalPlanPrice (plan) {
      let price = plan.unit_amount
      if (Number.isFinite(price)) {
        price = price * plan.selected_seats
        price = dataUtil.formatCurrency(
          price,
          { minimumFractionDigits: 2, maximumFractionDigits: 2 }
        )
        return `${price} per ${this.formData.plan_period}`
      }
      return price
    },
    updateSelectedSeats (plan) {
      plan.selected_seats = dataUtil.roundTo(parseInt(plan.selected_seats), plan.seat_step)
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
        if (idx === 0) {
          tier.selected_seats = tier.upper_count
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
}
</style>
