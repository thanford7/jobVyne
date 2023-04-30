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

  getJobLinkUrl (jobLink, { platform, filters, employerId } = {}) {
    let url = `${window.location.origin}/jobs-link/`
    if (!jobLink) {
      url = `${url}example/${employerId}`
    } else {
      url = `${url}${jobLink.id}`
    }
    const params = []
    if (platform) {
      params.push({ key: 'platform', val: platform })
    }
    if (filters) {
      Object.entries(filters).forEach(([filterKey, filterVal]) => {
        if (filterVal && filterVal.length) {
          if (Array.isArray(filterVal)) {
            filterVal.forEach((val) => {
              params.push({ key: filterKey, val })
            })
          } else {
            params.push({ key: filterKey, val: filterVal })
          }
        }
      })
    }
    if (params.length) {
      url = dataUtil.getUrlWithParams({
        isExcludeExistingParams: true,
        path: url,
        addParams: params
      })
    }
    return url
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
}

const socialUtil = new SocialUtil()
export default socialUtil
