import { date } from 'quasar'

class DateTimeUtil {
  getShortDate (dateStr) {
    return date.formatDate(dateStr, 'MMM D, YYYY')
  }

  getLongDate (dateStr) {
    return date.formatDate(dateStr, 'MMMM D, YYYY')
  }
}

const dateTimeUtil = new DateTimeUtil()

export default dateTimeUtil
