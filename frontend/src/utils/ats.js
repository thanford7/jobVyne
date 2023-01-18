import dataUtil from 'src/utils/data.js'

export const ATS_CFGS = {
  greenhouse: {
    key: 'greenhouse',
    name: 'Greenhouse'
  },
  lever: {
    key: 'lever',
    name: 'Lever'
  }
}

class AtsUtil {
  getFormattedStageOptions (stageData, atsKey) {
    if (atsKey === ATS_CFGS.greenhouse.key) {
      return dataUtil.sortBy(
        dataUtil.uniqBy(stageData.map((s) => ({ name: s.name, key: s.name, priority: s.priority })), 'name'),
        'priority',
        true)
    } else if (atsKey === ATS_CFGS.lever.key) {
      return stageData.map((s) => ({ name: s.text, key: s.id }))
    }
  }
}

const atsUtil = new AtsUtil()

export default atsUtil
