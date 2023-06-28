import { colors } from 'quasar'

const { getPaletteColor } = colors

const padZero = (str, len) => {
  len = len || 2
  const zeros = new Array(len).join('0')
  return (zeros + str).slice(-len)
}

// https://quasar.dev/quasar-utils/color-utils
class ColorUtil {
  getPaletteColor (colorName) {
    return getPaletteColor(colorName)
  }

  getRandomPastelColor () {
    const hue = parseInt(360 * Math.random())
    const saturation = parseInt(40 + 20 * Math.random())
    const lightness = parseInt(65 + 20 * Math.random())
    return this.hslToHex(hue, saturation, lightness)
  }

  hslToHex (h, s, l) {
    l /= 100
    const a = s * Math.min(l, 1 - l) / 100
    const f = n => {
      const k = (n + h / 30) % 12
      const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1)
      return Math.round(255 * color).toString(16).padStart(2, '0')
    }
    return `#${f(0)}${f(8)}${f(4)}`
  }

  getInvertedColor (hex, isBlackWhite = true) {
    if (hex.indexOf('#') === 0) {
      hex = hex.slice(1)
    }
    // convert 3-digit hex to 6-digits.
    if (hex.length === 3) {
      hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2]
    }
    if (hex.length !== 6) {
      throw new Error('Invalid hex color')
    }
    let r = parseInt(hex.slice(0, 2), 16),
      g = parseInt(hex.slice(2, 4), 16),
      b = parseInt(hex.slice(4, 6), 16)
    if (isBlackWhite) {
      // https://stackoverflow.com/a/3943023/112731
      return (r * 0.299 + g * 0.587 + b * 0.114) > 186
        ? '#000000'
        : '#FFFFFF'
    }
    // invert color components
    r = (255 - r).toString(16)
    g = (255 - g).toString(16)
    b = (255 - b).toString(16)
    // pad each with zeros and return
    return '#' + padZero(r) + padZero(g) + padZero(b)
  }

  getEmployerPrimaryColor (employer) {
    return employer?.color_primary || this.getPaletteColor('primary')
  }

  getEmployerSecondaryColor (employer) {
    return employer?.color_secondary || employer?.color_primary || this.getPaletteColor('secondary')
  }

  getEmployerAccentColor (employer) {
    return employer?.color_accent || employer?.color_secondary || this.getPaletteColor('accent')
  }

  changeAlpha (color, offset) {
    return colors.changeAlpha(color, offset)
  }
}

const colorUtil = new ColorUtil()

export default colorUtil
