import locationUtil from 'src/utils/location.js'

class SocialUtil {
  getLinkTextDescription (jobsLink) {
    let text = jobsLink.platform_name || '[No platform]'
    if (jobsLink.departments.length) {
      text += `|${jobsLink.departments.map((d) => d.name).join(', ')}`
    } else {
      text += '|[Any department]'
    }
    const locations = locationUtil.getFormattedLocations(jobsLink)
    if (locations.length) {
      text += `|${locations.map((l) => l.name).join(', ')}`
    } else {
      text += '|[Any location]'
    }
    return text
  }
}

const socialUtil = new SocialUtil()
export default socialUtil
