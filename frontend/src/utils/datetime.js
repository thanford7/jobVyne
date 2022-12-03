import { date } from 'quasar'
import dataUtil from 'src/utils/data.js'

// Keys are based on the values returned by Python's datetime.weekday()
// This helps stay in sync with backend
// jsDayOfWeek corresponds with JS getDay() method
export const DAYS_OF_WEEK = {
  0: { jsDayOfWeek: 1, name: 'Monday' },
  1: { jsDayOfWeek: 2, name: 'Tuesday' },
  2: { jsDayOfWeek: 3, name: 'Wednesday' },
  3: { jsDayOfWeek: 4, name: 'Thursday' },
  4: { jsDayOfWeek: 5, name: 'Friday' },
  5: { jsDayOfWeek: 6, name: 'Saturday' },
  6: { jsDayOfWeek: 0, name: 'Sunday' }
}

class DateTimeUtil {
  constructor () {
    this.shortDateFormat = 'MMM D, YYYY'
    this.longDateFormat = 'MMMM D, YYYY'
    this.dateTimeFormat = 'MM/DD/YYYY HH:mm:ss'
    this.dateTimeFormatNoSeconds = 'MM/DD/YYYY HH:mm'
    this.serializeDateFormat = 'MM/DD/YYYY'
    this.serializeDateTimeFormat = 'MM/DD/YYYY HH:mm:ssZZ'

    this.time12HRegex = /^(?<hour>1[0-2]|0?[1-9]):(?<minute>[0-5][0-9])(:(?<second>[0-5][0-9]))? ?(?<ampm>[AaPp][Mm])/
    this.time24HRegex = /^(?<hour>0[0-9]|1[0-9]|2[0-3]):(?<minute>[0-5][0-9])(:(?<second>[0-5][0-9]))?$/
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
    // Dates without a time component are converted to local time which can throw off the date by a day
    // UTC time will always cause the date to be the same
    if (dateStr && dataUtil.isString(dateStr) && dateStr.length <= 10) {
      dateStr = this.forceToDate(dateStr).toUTCString()
      dateStr = dateStr.slice(0, dateStr.length - 4) // Remove the timezone to assume it is local time
    }
    return date.formatDate(dateStr, this.shortDateFormat)
  }

  getDateTime (dateTimeStr, { isIncludeSeconds = true } = {}) {
    const format = (isIncludeSeconds) ? this.dateTimeFormat : this.dateTimeFormatNoSeconds
    return date.formatDate(dateTimeStr, format)
  }

  getStartOfMonthDate (targetDate, { asString = true, monthOffset = 0 } = {}) {
    targetDate = this.forceToDate(targetDate)
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

  getTimeStrFromDate (targetDate, { isIncludeSeconds = true } = {}) {
    let format = 'HH:mm'
    if (isIncludeSeconds) {
      format += ':ss'
    }
    return date.formatDate(targetDate, format)
  }

  getDateDifference (firstDate, secondDate, unit) {
    firstDate = this.forceToDate(firstDate)
    secondDate = this.forceToDate(secondDate)
    const daysDiff = date.getDateDiff(secondDate, firstDate, 'days')
    if (unit === 'months') {
      return (daysDiff / 30).toFixed(1)
    } else if (unit === 'years') {
      return (daysDiff / 365).toFixed(1)
    } else {
      return daysDiff
    }
  }

  /**
   * @returns {string}: The region of the offset - e.g. America/Denver
   */
  getCurrentTimeZone () {
    return Intl.DateTimeFormat().resolvedOptions().timeZone
  }

  getCurrentTimeZoneHourOffset () {
    const minuteOffset = new Date().getTimezoneOffset()
    let hourOffset = Math.abs(minuteOffset / 60).toString()
    // 0 pad the hour offset
    hourOffset = (hourOffset.length === 1) ? `0${hourOffset}` : hourOffset
    // A negative offset means the timezone is ahead of UTC so the operator is "+"
    const operator = (minuteOffset <= 0) ? '+' : '-'
    return `${operator}${hourOffset}00`
  }

  parseTimeStr (timeStr) {
    const time12HMatch = timeStr.match(this.time12HRegex)
    const time24HMatch = timeStr.match(this.time24HRegex)
    let hour, minute, second, ampm
    if (time12HMatch) {
      ({ hour, minute, second, ampm } = time12HMatch.groups)
    } else if (time24HMatch) {
      ({ hour, minute, second } = time24HMatch.groups)
    } else {
      return null
    }
    const hourInc = (ampm) ? ((ampm.toLowerCase() === 'pm') ? 12 : 0) : 0
    return {
      hour: parseInt(hour) + hourInc,
      minute: parseInt(minute),
      second: parseInt(second || '0')
    }
  }

  forceToDate (dateVal) {
    if (dataUtil.isString(dateVal)) {
      return new Date(dateVal)
    }
    return dateVal
  }

  now () {
    return new Date()
  }

  getCurrentYear () {
    return this.today().getFullYear()
  }

  copyDate (date) {
    try {
      return new Date(date.getTime())
    } catch (error) {
      return new Date(date)
    }
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
   * @returns {boolean}
   */
  isBefore (targetDate, referenceDate, { isInclusive = false, isIncludeTime = true } = {}) {
    const normTargetDate = new Date(targetDate)
    const normReferenceDate = new Date(referenceDate)
    if (!isIncludeTime) {
      normTargetDate.setHours(0, 0, 0, 0)
      normReferenceDate.setHours(0, 0, 0, 0)
    }
    if (isInclusive) {
      return normTargetDate <= normReferenceDate
    }
    return normTargetDate < normReferenceDate
  }

  /**
   * Check whether the targetDate is after the referenceDate
   * @returns {boolean}
   */
  isAfter (targetDate, referenceDate, { isInclusive = false, isIncludeTime = true } = {}) {
    const normTargetDate = new Date(targetDate)
    const normReferenceDate = new Date(referenceDate)
    if (!isIncludeTime) {
      normTargetDate.setHours(0, 0, 0, 0)
      normReferenceDate.setHours(0, 0, 0, 0)
    }
    if (isInclusive) {
      return normTargetDate >= normReferenceDate
    }
    return normTargetDate > normReferenceDate
  }

  isBetween (targetDate, startDate, endDate, { isStartInclusive = true, isEndInclusive = true, isIncludeTime = true } = {}) {
    return (
      !this.isAfter(targetDate, endDate, { isIncludeTime, isInclusive: !isEndInclusive }) &&
      !this.isBefore(targetDate, startDate, { isIncludeTime, isInclusive: !isStartInclusive })
    )
  }
}

const dateTimeUtil = new DateTimeUtil()

export const GROUPINGS = {
  DATE: { key: 'date', formatter: dateTimeUtil.getShortDate.bind(dateTimeUtil) },
  WEEK: { key: 'week', formatter: dateTimeUtil.getStartOfWeekDate.bind(dateTimeUtil) },
  MONTH: { key: 'month', formatter: dateTimeUtil.getMonthYearFromDate.bind(dateTimeUtil) },
  YEAR: { key: 'year', formatter: dateTimeUtil.getYearFromDate.bind(dateTimeUtil) }
}

export default dateTimeUtil
