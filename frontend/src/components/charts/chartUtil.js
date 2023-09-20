import colorUtil from 'src/utils/color.js'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil, { GROUPINGS } from 'src/utils/datetime.js'

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

class ChartUtil {
  getDateSeries (data, dateLabels, dateGroup, { yAxisKey, xAxisKey }) {
    data = dataUtil.deepCopy(data)
    data.forEach((point) => {
      point[xAxisKey] = GROUPINGS[dateGroup.toUpperCase()].formatter(point[xAxisKey])
    })

    // Add dates that don't have any data
    dateLabels.forEach((date) => {
      if (!data.find((point) => point[xAxisKey] === date)) {
        data.push({ [xAxisKey]: date, [yAxisKey]: 0 })
      }
    })

    // Remove data points that aren't in the date range
    data = data.reduce((validDates, dataPoint) => {
      if (dateLabels.includes(dataPoint[xAxisKey])) {
        validDates.push(dataPoint)
      }
      return validDates
    }, [])

    // Make sure series data is in order chart.js relies on this
    data.sort((a, b) => new Date(a[xAxisKey]) - new Date(b[xAxisKey]))
    return data
  }

  getDateLabels (dateGroup, { to, from }) {
    let datesInRange = dateTimeUtil.getDatesInRange(new Date(from), new Date(to))
    datesInRange = dataUtil.uniqArray(datesInRange.map((date) => GROUPINGS[dateGroup.toUpperCase()].formatter(date)))
    datesInRange.sort((a, b) => new Date(a) - new Date(b))
    return datesInRange
  }
}

const chartUtil = new ChartUtil()

export default chartUtil
