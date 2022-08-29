import dataUtil from 'src/utils/data.js'

class LocationUtil {
  getFormattedLocations (record) {
    const locations = []
    dataUtil.getForceArray(record.cities).forEach((city) => {
      city.type = 'city'
      city.key = `city-${city.id}`
      city.color = 'blue-8'
      locations.push(city)
    })
    dataUtil.getForceArray(record.states).forEach((state) => {
      state.type = 'state'
      state.key = `state-${state.id}`
      state.color = 'teal-8'
      locations.push(state)
    })
    dataUtil.getForceArray(record.countries).forEach((country) => {
      country.type = 'country'
      country.key = `country-${country.id}`
      country.color = 'blue-grey-8'
      locations.push(country)
    })
    return locations
  }

  getFullLocation ({ city, state, country }) {
    return [city, state, country].reduce((location, locPart) => {
      if (!locPart) {
        return location
      }
      if (!location) {
        return locPart
      }
      return location + ', ' + locPart
    }, null)
  }
}

const locationUtil = new LocationUtil()

export default locationUtil
