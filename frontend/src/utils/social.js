import dataUtil from 'src/utils/data.js'
import { FILE_TYPES } from 'src/utils/file.js'
import locationUtil from 'src/utils/location.js'

class SocialUtil {
  constructor () {
    this.platformCfgs = {
      LinkedIn: {
        allowedMedia: [FILE_TYPES.IMAGE.key],
        isMultiMedia: false,
        characterLimit: 3000
      },
      Facebook: {},
      Twitter: {},
      Instagram: {},
      TikTok: {},
      YouTube: {}
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

  getJobLinkUrl (jobLink) {
    return `${window.location.origin}/jobs-link/${jobLink.id}`
  }

  getSocialLinks (platforms, jobLink) {
    return platforms.reduce((socialLinks, platform) => {
      const socialLink = dataUtil.getUrlWithParams({
        isExcludeExistingParams: true,
        path: this.getJobLinkUrl(jobLink),
        addParams: [{ key: 'platform', val: platform.name }]
      })
      socialLinks.push(Object.assign(
        dataUtil.pick(platform, ['name', 'logo']),
        { socialLink }
      ))
      return socialLinks
    }, [])
  }
}

const socialUtil = new SocialUtil()
export default socialUtil
