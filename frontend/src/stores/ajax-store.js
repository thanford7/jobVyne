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
        } else if (isString(data)) {
          msg += `: ${data}`
        } else if (data.includes('<!doctype html>')) {
          msg += `: ${this.parseHtmlMessage(data)}`
        }
      } else {
        msg = error.message
      }

      this.msgIdx++
      this.messages.push({
        msg,
        classStr: msgClassCfgs.ERROR,
        idx: this.msgIdx
      })
    },
    addSuccessMsg (msg) {
      this.msgIdx++
      const idx = this.msgIdx
      this.messages.push({
        msg,
        classStr: msgClassCfgs.SUCCESS,
        idx
      })
      setTimeout(() => {
        this.removeMsg(idx)
      }, 10000)
    },
    removeMsg (msgIdx) {
      this.messages = this.messages.filter((msg) => msg.idx !== msgIdx)
    },
    parseHtmlMessage (htmlText) {
      const parser = new DOMParser()
      const htmlDoc = parser.parseFromString(htmlText, 'text/html')
      return htmlDoc.querySelector('.detail .errormsg').textContent
    }
  }
})
