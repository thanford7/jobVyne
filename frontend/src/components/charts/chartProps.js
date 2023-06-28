import colorUtil from 'src/utils/color.js'

export const chartProps = {
  chartType: String,
  chartTitle: [String, null],
  chartOptions: {
    type: Object,
    default: () => ({})
  },
  dateRange: {
    type: Object
  },
  isIncludeDateRange: {
    type: Boolean,
    default: true
  },
  isLoading: Boolean,
  seriesCfgs: Array,
  labels: [Array, null]
}

export const chartColors = {
  primary: colorUtil.getPaletteColor('primary'),
  secondary: colorUtil.getPaletteColor('secondary'),
  accent: colorUtil.getPaletteColor('accent'),
  colors: [
    '#ABDEE6',
    '#CBAACB',
    '#FFCCB6',
    '#F3B0C3',
    '#C6DBDA',
    '#FEE1E8',
    '#FED7C3',
    '#F6EAC2',
    '#ECD5E3',
    '#FFC5BF',
    '#FF968A',
    '#FFAEA5',
    '#FFDBBE',
    '#FFC8A2',
    '#04F0F0',
    '#8FCACA',
    '#CCE2CB',
    '#B6CFB6',
    '#97C1A9',
    '#FCB9AA',
    '#FFDBCC',
    '#ECEAE4',
    '#A2E1DB',
    '#55CBCD'
  ]
}
