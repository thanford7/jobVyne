import dataUtil from 'src/utils/data.js'

export const MODIFIER_TYPES = {
  PERCENT: 'PERCENT',
  NOMINAL: 'NOMINAL'
}

class BonusUtil {
  hasCriteria (criteriaVal) {
    return criteriaVal && criteriaVal.length
  }

  hasAnyCriteria (criteriaObject) {
    for (const criteriaVal of Object.values(criteriaObject)) {
      if (this.hasCriteria(criteriaVal)) {
        return true
      }
    }
    return false
  }

  getFilteredJobsFromRule (jobs, bonusRule) {
    return jobs.filter((job) => job.bonus_rule && job.bonus_rule.id === bonusRule.id)
  }

  getModifierSummaryHtml (modifier, baseAmount, currencyName) {
    let totalAmount, amountTxt
    if (modifier.type === MODIFIER_TYPES.PERCENT) {
      amountTxt = `${modifier.amount}%`
      totalAmount = baseAmount * (1 + modifier.amount / 100)
    } else {
      amountTxt = dataUtil.formatCurrency(modifier.amount, { currency: currencyName })
      totalAmount = baseAmount + modifier.amount
    }
    totalAmount = dataUtil.formatCurrency(totalAmount, { currency: currencyName })
    return `<span>After <span class="text-bold">${dataUtil.pluralize('day', modifier.start_days_after_post)}</span>
      from the post date of the job, increase the employee referral bonus amount by
      <span class="text-bold">${amountTxt}</span> to <span class="text-bold">${totalAmount}</span></span>
      `
  }
}

const bonusUtil = new BonusUtil()
export default bonusUtil
