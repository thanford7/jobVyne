import dataUtil from 'src/utils/data.js'

class LocationUtil {
  constructor () {
    // Keep in sync with backend REMOTE_TYPES
    this.REMOTE_TYPE_FALSE = 1
    this.REMOTE_TYPE_TRUE = 2
  }

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

  updateFullLocations (locations) {
    return (locations || []).reduce((formattedLocations, location) => {
      location.fullLocationText = this.getFullLocation(location)
      formattedLocations.push(location)
      return formattedLocations
    }, [])
  }

  getFullLocation ({ is_remote: isRemote, city, state, country, text }) {
    if (!city && !state && !country) {
      return text
    }
    let location = [city, state, country].reduce((location, locPart) => {
      if (!locPart) {
        return location
      }
      if (!location.length) {
        return locPart
      }
      return location + ', ' + locPart
    }, '')
    if (isRemote) {
      const remoteText = (location.length) ? 'Remote: ' : 'Remote'
      location = `${remoteText}${location}`
    }
    return location
  }
}

const locationUtil = new LocationUtil()

export default locationUtil
