import { defineStore } from 'pinia'

export const msgClassCfgs = {
  SUCCESS: 'bg-positive',
  WARNING: 'bg-warning',
  ERROR: 'bg-negative text-white',
  INFO: 'bg-info text-white'
}

const isString = (val) => val && typeof val.valueOf() === 'string'

export const useAjaxStore = defineStore('ajax', {
  state: () => ({
    messages: [],
    msgIdx: 0
  }),

  actions: {
    addErrorMsg (error) {
      let msg
      if (error.response) {
        const { data, status, statusText } = error.response
        msg = `${status} ${statusText}`
        if (data && data.detail) {
          msg += `: ${data.detail}`
        } else if (isString(data) && data.includes('<!doctype html>')) {
          msg += `: ${this.parseHtmlMessage(data)}`
        } else if (isString(data)) {
          msg += `: ${data}`
        }
      } else {
        msg = error.message
      }
      this.addMsg(msg, msgClassCfgs.ERROR)
    },
    addSuccessMsg (msg) {
      const msgIdx = this.addMsg(msg, msgClassCfgs.SUCCESS)
      setTimeout(() => {
        this.removeMsg(msgIdx)
      }, 10000)
    },
    addMsg (msg, severity) {
      this.msgIdx++
      this.messages.push({
        msg,
        classStr: severity,
        idx: this.msgIdx
      })
      return this.msgIdx
    },
    removeMsg (msgIdx) {
      this.messages = this.messages.filter((msg) => msg.idx !== msgIdx)
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
