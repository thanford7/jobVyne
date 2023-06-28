import colorUtil from 'src/utils/color.js'
import dataUtil from 'src/utils/data.js'

// Keep in sync with UserRequest backend
export const USER_REQUEST_TYPES = {
  introduction: {
    key: 'introduction',
    label: 'Introduction',
    pages: [
      { name: 'Intro Request', key: 'intro-request' },
      { name: 'Connection Request', key: 'connect-request' }
    ]
  },
  connect: {
    key: 'connect',
    label: 'Connection',
    pages: [
      { name: 'Connection Request', key: 'connect-request' }
    ]
  }
}

class KarmaUtil {
  getEveryOrgDonationLink (orgData, user, donationId, donationAmt = 0) {
    const successUrl = dataUtil.getUrlWithParams({
      path: `${window.location.origin}/karma/donation-confirm`,
      addParams: [
        { key: 'donationId', val: donationId }
      ]
    })
    const givingUrl = dataUtil.getUrlWithParams({
      path: `${process.env.EVERY_ORG_API_URL}${orgData.ein}`,
      addParams: [
        { key: 'frequency', val: 'ONCE' },
        { key: 'email', val: user.email },
        { key: 'first_name', val: user.first_name },
        { key: 'last_name', val: user.last_name },
        { key: 'success_url', val: successUrl },
        { key: 'exit_url', val: window.location.href },
        { key: 'description', val: 'JobVyne Karma Connect donation' },
        { key: 'theme_color', val: colorUtil.getPaletteColor('primary') },
        { key: 'min_value', val: donationAmt },
        { key: 'amount', val: donationAmt },
        { key: 'method', val: 'card,bank,paypal,venmo,pay' }
      ]
    })
    return `${givingUrl}#donate`
  }
}

const karmaUtil = new KarmaUtil()

export default karmaUtil
