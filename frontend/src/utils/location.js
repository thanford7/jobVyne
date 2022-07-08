
class LocationUtil {
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
