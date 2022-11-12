import { defineStore } from 'pinia'
import { Notify } from 'quasar'

export const msgTypes = {
  SUCCESS: {
    color: 'positive',
    textColor: 'black',
    timeout: 10000
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

const isString = (val) => val && typeof val.valueOf() === 'string'

export const useAjaxStore = defineStore('ajax', {
  state: () => ({
    messages: []
  }),

  actions: {
    addErrorMsg (error) {
      let msg
      if (error.response) {
        const { data, status, statusText } = error.response
        msg = `${status} ${statusText}`
        if (data && data.detail) {
          msg += `: ${data.detail}`
        } else if (isString(data) && data.toLowerCase().includes('<!doctype html>')) {
          msg += `: ${this.parseHtmlMessage(data)}`
        } else if (isString(data)) {
          msg += `: ${data}`
        }
      } else {
        msg = error.message
      }
      this.addMsg(msg, msgTypes.ERROR)
    },
    addSuccessMsg (msg) {
      this.addMsg(msg, msgTypes.SUCCESS)
    },
    addMsg (msg, { color, textColor, icon, timeout }) {
      Notify.create({
        color,
        textColor,
        message: msg,
        timeout,
        icon,
        actions: [
          { label: 'Dismiss', handler: () => { /* ... */ } }
        ]
      })
    },
    parseHtmlMessage (htmlText) {
      const parser = new DOMParser()
      const htmlDoc = parser.parseFromString(htmlText, 'text/html')
      const errorMsg = htmlDoc.querySelector('.detail .errormsg')
      if (errorMsg) {
        return errorMsg.textContent
      }
      return htmlDoc.textContent
    }
  }
})
