import { date } from 'quasar'

class DateTimeUtil {
  constructor () {
    this.shortDateFormat = 'MMM D, YYYY'
    this.longDateFormat = 'MMMM D, YYYY'
  }

  getShortDate (dateStr) {
    return date.formatDate(dateStr, this.shortDateFormat)
  }

  getLongDate (dateStr) {
    return date.formatDate(dateStr, this.longDateFormat)
  }

  today () {
    return new Date()
  }

  getCurrentYear () {
    return this.today().getFullYear()
  }

  /**
   * Check whether the targetDate is before the referenceDate
   * @param targetDate {String}
   * @param referenceDate {String}
   * @param isInclusive {Boolean}
   * @returns {boolean}
   */
  isBefore (targetDate, referenceDate, isInclusive = false) {
    const normTargetDate = new Date(targetDate)
    const normReferenceDate = new Date(referenceDate)
    normTargetDate.setHours(0, 0, 0, 0)
    normReferenceDate.setHours(0, 0, 0, 0)
    if (isInclusive) {
      return normTargetDate <= normReferenceDate
    }
    return normTargetDate < normReferenceDate
  }

  /**
   * Check whether the targetDate is after the referenceDate
   * @param targetDate {String}
   * @param referenceDate {String}
   * @param isInclusive {Boolean}
   * @returns {boolean}
   */
  isAfter (targetDate, referenceDate, isInclusive = false) {
    const normTargetDate = new Date(targetDate)
    const normReferenceDate = new Date(referenceDate)
    normTargetDate.setHours(0, 0, 0, 0)
    normReferenceDate.setHours(0, 0, 0, 0)
    if (isInclusive) {
      return normTargetDate >= normReferenceDate
    }
    return normTargetDate > normReferenceDate
  }
}

const dateTimeUtil = new DateTimeUtil()

export default dateTimeUtil
