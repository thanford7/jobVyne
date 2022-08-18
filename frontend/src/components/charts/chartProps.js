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
  seriesCfgs: Array
}
