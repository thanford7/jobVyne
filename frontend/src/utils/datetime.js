import { date } from 'quasar'
import dataUtil from 'src/utils/data.js'

class DateTimeUtil {
  constructor () {
    this.shortDateFormat = 'MMM D, YYYY'
    this.longDateFormat = 'MMMM D, YYYY'
  }

  serializeDate (targetDate) {
    return date.formatDate(targetDate, 'MM/DD/YYYY')
  }

  getShortDate (dateStr) {
    return date.formatDate(dateStr, this.shortDateFormat)
  }

  getLongDate (dateStr) {
    return date.formatDate(dateStr, this.longDateFormat)
  }

  getStartOfWeekDate (targetDate, { asString = true } = {}) {
    if (dataUtil.isString(targetDate)) {
      targetDate = new Date(targetDate)
    }
    const newDate = this.copyDate(targetDate)
    const day = newDate.getDay()
    const diff = newDate.getDate() - day + ((day === 0) ? -6 : 1) // adjust when day is sunday
    newDate.setDate(diff)
    if (asString) {
      return this.getShortDate(newDate)
    }
    return newDate
  }

  getMonthYearFromDate (targetDate) {
    return date.formatDate(targetDate, 'MMM YY')
  }

  getYearFromDate (targetDate, { asString = true } = {}) {
    const yearStr = date.formatDate(targetDate, 'YYYY')
    if (asString) {
      return yearStr
    }
    return parseInt(yearStr)
  }

  today () {
    return new Date()
  }

  getCurrentYear () {
    return this.today().getFullYear()
  }

  copyDate (date) {
    return new Date(date.getTime())
  }

  addDays (date, days, isInPlace = false) {
    if (!isInPlace) {
      date = this.copyDate(date)
    }

    date.setDate(date.getDate() + days)
    return date
  }

  getDatesInRange (startDate, endDate) {
    const date = this.copyDate(startDate)

    const dates = []

    // eslint-disable-next-line no-unmodified-loop-condition
    while (date <= endDate) {
      dates.push(this.copyDate(date))
      date.setDate(date.getDate() + 1)
    }

    return dates
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

  isBetween (targetDate, startDate, endDate, { isStartInclusive = true, isEndInclusive = true } = {}) {
    return (
      !this.isAfter(targetDate, endDate, !isEndInclusive) &&
      !this.isBefore(targetDate, startDate, !isStartInclusive)
    )
  }
}

const dateTimeUtil = new DateTimeUtil()

export const GROUPINGS = {
  DAY: { key: 'DAY', formatter: dateTimeUtil.getShortDate.bind(dateTimeUtil) },
  WEEK: { key: 'WEEK', formatter: dateTimeUtil.getStartOfWeekDate.bind(dateTimeUtil) },
  MONTH: { key: 'MONTH', formatter: dateTimeUtil.getMonthYearFromDate.bind(dateTimeUtil) },
  YEAR: { key: 'YEAR', formatter: dateTimeUtil.getYearFromDate.bind(dateTimeUtil) }
}

export default dateTimeUtil
