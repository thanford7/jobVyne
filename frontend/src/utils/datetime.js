import { date } from 'quasar'

class DateTimeUtil {
  getShortDate (dateStr) {
    return date.formatDate(dateStr, 'MMM D, YYYY')
  }

  getLongDate (dateStr) {
    return date.formatDate(dateStr, 'MMMM D, YYYY')
  }

  today () {
    return new Date()
  }

  getCurrentYear () {
    return this.today().getFullYear()
  }
}

const dateTimeUtil = new DateTimeUtil()

export default dateTimeUtil
