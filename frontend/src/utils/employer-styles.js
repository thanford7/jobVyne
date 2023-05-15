import colorUtil from 'src/utils/color.js'

class EmployerStyleUtil {
  getTabStyle (employer) {
    const primaryColor = colorUtil.getEmployerPrimaryColor(employer)
    return { color: primaryColor }
  }

  getButtonStyle (employer) {
    const accentColor = colorUtil.getEmployerAccentColor(employer)
    return {
      backgroundColor: accentColor,
      color: colorUtil.getInvertedColor(accentColor)
    }
  }
}

const employerStyleUtil = new EmployerStyleUtil()
export default employerStyleUtil
