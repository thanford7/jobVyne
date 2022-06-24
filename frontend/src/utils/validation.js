const EMAIL_REGEX = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
const WEB_LINK_REGEX = /(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_+.~#?&//=]*)/gi

class Validation {
  isGoodEmail (rawVal) {
    return EMAIL_REGEX.test(String(rawVal).toLowerCase())
  }

  isGoodWebLink (rawVal) {
    return WEB_LINK_REGEX.test(String(rawVal))
  }
}

const validation = new Validation()

export default validation
