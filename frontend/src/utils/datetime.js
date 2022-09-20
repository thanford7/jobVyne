import { date } from 'quasar'
import dataUtil from 'src/utils/data.js'

class DateTimeUtil {
  constructor () {
    this.shortDateFormat = 'MMM D, YYYY'
    this.longDateFormat = 'MMMM D, YYYY'
    this.dateTimeFormat = 'MM/DD/YYYY HH:mm:ss'
    this.serializeDateFormat = 'MM/DD/YYYY'
    this.serializeDateTimeFormat = 'MM/DD/YYYY HH:mm:ssZZ'
  }

  serializeDate (targetDate, isIncludeTime = false, isEndOfDay = false) {
    const format = (isIncludeTime) ? this.serializeDateTimeFormat : this.serializeDateFormat
    if (isEndOfDay) {
      targetDate = date.adjustDate(targetDate, { hours: 23, minutes: 59, seconds: 59, millisecond: 0 })
    } else {
      targetDate = date.adjustDate(targetDate, { hours: 0, minutes: 0, seconds: 0, millisecond: 0 })
    }
    return date.formatDate(targetDate, format)
  }

  getShortDate (dateStr) {
    return date.formatDate(dateStr, this.shortDateFormat)
  }

  getLongDate (dateStr) {
    return date.formatDate(dateStr, this.longDateFormat)
  }

  getDateTime (dateTimeStr) {
    return date.formatDate(dateTimeStr, this.dateTimeFormat)
  }

  getStartOfMonthDate (targetDate, { asString = true, monthOffset = 0 } = {}) {
    if (dataUtil.isString(targetDate)) {
      targetDate = new Date(targetDate)
    }
    const year = targetDate.getFullYear()
    const month = targetDate.getMonth()
    let firstDayOfMonth = new Date(year, month, 1)
    firstDayOfMonth = date.addToDate(firstDayOfMonth, { months: monthOffset })
    if (asString) {
      return this.getShortDate(firstDayOfMonth)
    }
    return firstDayOfMonth
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

  getLongMonthYearFromDate (targetDate) {
    return date.formatDate(targetDate, 'MMMM YYYY')
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

  sortDatesFn (firstDate, secondDate) {
    const a = new Date(firstDate)
    const b = new Date(secondDate)
    return b - a
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
