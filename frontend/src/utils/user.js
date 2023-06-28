import dataUtil from 'src/utils/data.js'

class UserUtil {
  getUserInitials (user, firstNameAttr = 'first_name', lastNameAttr = 'last_name') {
    const firstName = user[firstNameAttr]
    const lastName = user[lastNameAttr]
    const firstInitial = (firstName) ? dataUtil.capitalize(firstName[0]) : ''
    const lastInital = (lastName) ? dataUtil.capitalize(lastName[0]) : ''
    return firstInitial + lastInital
  }
}

const userUtil = new UserUtil()
export default userUtil
