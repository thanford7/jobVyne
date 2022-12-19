import { Notify } from 'quasar'

export const msgTypes = {
  SUCCESS: {
    color: 'positive',
    textColor: 'black',
    timeout: 6000
  },
  WARNING: {
    color: 'warning',
    textColor: 'black',
    icon: 'warning',
    timeout: 1000 * 60 // One minute
  },
  ERROR: {
    color: 'negative',
    textColor: 'white',
    icon: 'dangerous',
    timeout: 1000 * 60 * 60 * 24 // One day
  },
  INFO: {
    color: 'info',
    textColor: 'white',
    timeout: 10000
  }
}

const DEFAULT_ERROR_MSG = 'Something went wrong. The JobVyne team has been notified and will work on a fix as soon as possible.'

const isString = (val) => val && typeof val.valueOf() === 'string'

class MessagesUtil {
  addErrorMsg (error) {
    let msg
    if (error.response) {
      const { data, status, statusText } = error.response
      msg = `${status} ${statusText}`
      if (data && data.detail) {
        msg += `: ${data.detail}`
      } else if (isString(data) && data.toLowerCase().includes('<!doctype html>')) {
        let parsedMessage = this.parseHtmlMessage(data)
        if (!parsedMessage || !parsedMessage.length) {
          parsedMessage = DEFAULT_ERROR_MSG
        }
        msg += `: ${parsedMessage}`
      } else if (isString(data)) {
        msg += `: ${data}`
      }
    } else {
      msg = error.message
    }
    this.addMsg(msg, msgTypes.ERROR)
  }

  addSuccessMsg (msg) {
    this.addMsg(msg, msgTypes.SUCCESS)
  }

  addMsg (msg, { color, textColor, icon, timeout }) {
    Notify.create({
      color,
      textColor,
      message: msg,
      timeout,
      icon,
      actions: [
        {
          label: 'Dismiss',
          color: textColor,
          handler: () => { /* ... */ }
        }
      ]
    })
  }

  parseHtmlMessage (htmlText) {
    const parser = new DOMParser()
    const htmlDoc = parser.parseFromString(htmlText, 'text/html')
    const errorMsg = htmlDoc.querySelector('.detail .errormsg')
    if (errorMsg) {
      return errorMsg.textContent
    } else if (htmlDoc) {
      return htmlDoc.textContent
    }
    return htmlText
  }
}

const messagesUtil = new MessagesUtil()

export default messagesUtil
