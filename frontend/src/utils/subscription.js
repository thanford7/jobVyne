import dataUtil from 'src/utils/data.js'

export const SUBSCRIPTION_STATUS = {
  ACTIVE: 'active',
  CANCELED: 'canceled',
  INCOMPLETE: 'incomplete',
  INCOMPLETE_EXPIRED: 'incomplete_expired',
  PAST_DUE: 'past_due',
  UNPAID: 'unpaid'
}

class SubscriptionUtil {
  getPlanPriceText (plan) {
    const price = plan.unit_amount
    if (Number.isFinite(price)) {
      return dataUtil.formatCurrency(price, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    }
    return price
  }

  getSeatsRange (plan) {
    if (!plan.lower_count || !plan.upper_count) {
      return plan.lower_count || plan.upper_count
    }
    return `${plan.lower_count}-${plan.upper_count}`
  }

  getTotalPlanPrice (plan, planPeriod) {
    let price = plan.unit_amount
    if (Number.isFinite(price)) {
      price = price * plan.selected_seats
      price = dataUtil.formatCurrency(
        price,
        { minimumFractionDigits: 2, maximumFractionDigits: 2 }
      )
      return `${price} per ${planPeriod}`
    }
    return price
  }

  getIsUnpaid (subscriptionStatus) {
    return [SUBSCRIPTION_STATUS.INCOMPLETE, SUBSCRIPTION_STATUS.UNPAID, SUBSCRIPTION_STATUS.PAST_DUE].includes(subscriptionStatus)
  }

  getFormattedSubscriptionPrice (subscription) {
    return dataUtil.formatCurrency(subscription.total_price, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    })
  }
}

const subscriptionUtil = new SubscriptionUtil()
export default subscriptionUtil
