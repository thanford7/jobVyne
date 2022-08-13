
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
}

const bonusUtil = new BonusUtil()
export default bonusUtil
