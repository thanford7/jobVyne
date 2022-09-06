import sanitizeHtml from 'sanitize-html'

const EMAIL_REGEX = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
const WEB_LINK_REGEX = /(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_+.~#?&//=]*)/gi
const PHONE_REGEX = /^[0-9.+\-()\s]+$/
const LINKED_IN_REGEX = /^(https:\/\/)?(www\.)?linkedin.com\/in\/\S+$/i

// Needs to align with backend sanitization cfg (sanitize.py)
const colorMatch = [/^#(0x)?[0-9a-f]+$/i, /^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$/] // Match HEX and RGB
const sizeMatch = [/^-?\d+(?:px|em|%)$/, /0/] // Match any positive/negative number with px, em, or %
const sanitizeCfg = {
  allowedAttributes: {
    '*': ['class', 'style'],
    a: ['href', 'name', 'target', 'title', 'id', 'rel']
  },
  allowedStyles: {
    '*': {
      'background-color': colorMatch,
      'border-bottom-color': colorMatch,
      'border-collapse': [/^collapse$/, /^separate$/],
      'border-color': colorMatch,
      'border-left-color': colorMatch,
      'border-right-color': colorMatch,
      'border-top-color': colorMatch,
      color: colorMatch,
      float: [/^left$/, /^right$/, /^none$/, /^inline-start$/, /^inline-end$/],
      'font-size': sizeMatch,
      'font-weight': [/^normal$/, /^bold$/, /^lighter$/, /^bolder$/],
      height: sizeMatch,
      'text-align': [/^left$/, /^right$/, /^center$/],
      'text-decoration': [/^underline$/, /^overline$/, /^none$/],
      'text-indent': sizeMatch,
      'vertical-align': [/^baseline$/, /^sub$/, /^super$/, /^text-top$/, /^text-bottom$/, /^middle$/, /^top$/, /^bottom$/],
      'white-space': [/^normal$/, /^nowrap$/, /^pre$/, /^pre-wrap$/, /^pre-line$/, /^break-spaces$/],
      width: sizeMatch
    }
  }
}

class FormUtil {
  isGoodEmail (rawVal) {
    return EMAIL_REGEX.test(String(rawVal).toLowerCase())
  }

  isGoodPhoneNumber (rawVal) {
    return PHONE_REGEX.test(String(rawVal))
  }

  isGoodLinkedInUrl (rawVal) {
    return LINKED_IN_REGEX.test(String(rawVal))
  }

  isGoodWebLink (rawVal) {
    return WEB_LINK_REGEX.test(String(rawVal))
  }

  sanitizeHtml (htmlText) {
    return sanitizeHtml(htmlText, sanitizeCfg)
  }
}

const formUtil = new FormUtil()

export default formUtil
