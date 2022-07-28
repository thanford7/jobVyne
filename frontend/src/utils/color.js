import { colors } from 'quasar'

const { getPaletteColor } = colors

// https://quasar.dev/quasar-utils/color-utils
class ColorUtil {
  getPaletteColor (colorName) {
    return getPaletteColor(colorName)
  }
}

const colorUtil = new ColorUtil()

export default colorUtil
