
const EMAIL_REGEX = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
const WEB_LINK_REGEX = /(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_+.~#?&//=]*)/gi

// TODO: Test this
const PHONE_REGEX = /^[0-9.+\-()\s]+$/
const LINKED_IN_REGEX = /^(https:\/\/)?(www\.)?linkedin.com\/in\/\S+$/i

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
}

const formUtil = new FormUtil()

export default formUtil
