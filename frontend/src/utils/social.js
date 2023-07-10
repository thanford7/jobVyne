import dataUtil from 'src/utils/data.js'
import { FILE_TYPES } from 'src/utils/file.js'
import locationUtil from 'src/utils/location.js'

class SocialUtil {
  constructor () {
    this.SOCIAL_KEY_LINKED_IN = 'LinkedIn'
    this.SOCIAL_KEY_FACEBOOK = 'Facebook'
    this.SOCIAL_KEY_GOOGLE = 'Google'
    this.SOCIAL_KEY_TWITTER = 'Twitter'
    this.SOCIAL_KEY_INSTAGRAM = 'Instagram'
    this.SOCIAL_KEY_TIKTOK = 'TikTok'
    this.SOCIAL_KEY_YOUTUBE = 'YouTube'
    this.SOCIAL_KEY_SLACK = 'Slack'

    // Keep in sync with PostChannel
    this.SOCIAL_CHANNEL_SLACK_JOB = 'slack-job'
    this.SOCIAL_CHANNEL_SLACK_EMPLOYEE_REFERRAL = 'slack-employee-referral'
    this.SOCIAL_CHANNEL_LINKEDIN_JOB = 'linkedin-job'

    this.platformCfgs = {
      [this.SOCIAL_KEY_LINKED_IN]: {
        name: this.SOCIAL_KEY_LINKED_IN,
        allowedMedia: [FILE_TYPES.IMAGE.key],
        isMultiMedia: false,
        characterLimit: 3000,
        icon: 'fa-linkedin-in',
        logo: '/logos/linkedIn_logo.png',
        redirectProvider: 'linkedin-oauth2'
      },
      [this.SOCIAL_KEY_FACEBOOK]: {
        name: this.SOCIAL_KEY_FACEBOOK,
        icon: 'fa-facebook-f',
        redirectProvider: 'facebook'
      },
      [this.SOCIAL_KEY_TWITTER]: {
        name: this.SOCIAL_KEY_TWITTER
      },
      [this.SOCIAL_KEY_INSTAGRAM]: {
        name: this.SOCIAL_KEY_INSTAGRAM
      },
      [this.SOCIAL_KEY_TIKTOK]: {
        name: this.SOCIAL_KEY_TIKTOK
      },
      [this.SOCIAL_KEY_YOUTUBE]: {
        name: this.SOCIAL_KEY_YOUTUBE
      },
      [this.SOCIAL_KEY_GOOGLE]: {
        name: this.SOCIAL_KEY_GOOGLE,
        icon: 'fa-google',
        logo: '/logos/google_logo.png',
        redirectProvider: 'google-oauth2'
      },
      [this.SOCIAL_KEY_SLACK]: {
        name: this.SOCIAL_KEY_SLACK,
        icon: 'fa-slack',
        logo: '/logos/slack_logo.png',
        redirectProvider: 'slack'
      }
    }
  }

  getLinkTextDescription (jobsLink) {
    let text = ''
    if (jobsLink.departments.length) {
      text += `${jobsLink.departments.map((d) => d.name).join(', ')}`
    } else {
      text += '[Any department]'
    }
    const locations = locationUtil.getFormattedLocations(jobsLink)
    if (locations.length) {
      text += `|${locations.map((l) => l.name).join(', ')}`
    } else {
      text += '|[Any location]'
    }
    return text
  }

  getJobLinkUrl (jobLink, platform) {
    if (!platform) {
      return jobLink.url
    }
    return dataUtil.getUrlWithParams({
      isExcludeExistingParams: false,
      path: jobLink.url,
      addParams: [{ key: 'platform', val: platform }]
    })
  }

  getSocialLinks (platforms, jobLink) {
    return platforms.reduce((socialLinks, platform) => {
      const socialLink = this.getJobLinkUrl(jobLink, { platform: platform.name })
      socialLinks.push(Object.assign(
        dataUtil.pick(platform, ['name', 'logo', 'is_displayed']),
        { socialLink }
      ))
      return socialLinks
    }, [])
  }

  getPlatformLogo ({ platformName = null, provider = null }) {
    if (platformName) {
      return this.platformCfgs[platformName].logo
    }
    return Object.values(this.platformCfgs).find((cfg) => cfg.redirectProvider === provider).logo
  }
}

const socialUtil = new SocialUtil()
export default socialUtil
