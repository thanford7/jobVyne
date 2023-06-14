// Keep in sync with backend user model
export const USER_TYPE_ADMIN = 'Admin'
export const USER_TYPE_CANDIDATE = 'Candidate'
export const USER_TYPE_EMPLOYEE = 'Employee'
export const USER_TYPE_INFLUENCER = 'Influencer'
export const USER_TYPE_EMPLOYER = 'Employer'

export const USER_TYPES = {
  [USER_TYPE_ADMIN]: 0x1,
  [USER_TYPE_CANDIDATE]: 0x2,
  [USER_TYPE_EMPLOYEE]: 0x4,
  [USER_TYPE_INFLUENCER]: 0x8,
  [USER_TYPE_EMPLOYER]: 0x10
}

export const COMPANY_USER_TYPES = [USER_TYPE_EMPLOYEE, USER_TYPE_EMPLOYER]
export const COMPANY_USER_TYPE_BITS = COMPANY_USER_TYPES.reduce((bits, userType) => {
  bits |= USER_TYPES[userType]
  return bits
}, 0)

class UserTypeUtil {
  getUserTypeNameFromBit (userTypeBit) {
    for (const [name, bit] of Object.entries(USER_TYPES)) {
      if (bit === parseInt(userTypeBit)) {
        return name
      }
    }
  }

  getUserTypeList (userTypeBits, isInBits, { excludeBits = USER_TYPES.Admin | USER_TYPES.Candidate, includeBits } = {}) {
    return Object.entries(USER_TYPES).reduce((typeList, [userTypeName, userTypeBit]) => {
      const isExcluded = (userTypeBit & excludeBits) || (includeBits && !(userTypeBit & includeBits))
      if (!isExcluded && (userTypeBits & userTypeBit)) {
        typeList.push((isInBits) ? userTypeBit : userTypeName)
      }
      return typeList
    }, [])
  }
}

const userTypeUtil = new UserTypeUtil()
export default userTypeUtil
