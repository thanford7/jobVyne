
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

// Keep in sync with backend user model
export const PERMISSION_NAMES = {
  MANAGE_USER: 'Manage users',
  CHANGE_PERMISSIONS: 'Change user permissions',
  MANAGE_PERMISSION_GROUPS: 'Manage custom permission groups',
  MANAGE_EMPLOYER_CONTENT: 'Manage employer content',
  MANAGE_EMPLOYER_JOBS: 'Manage employer jobs',
  MANAGE_REFERRAL_BONUSES: 'Manage employee referral bonuses',
  ADD_EMPLOYEE_CONTENT: 'Add personal employee content',
  MANAGE_BILLING_SETTINGS: 'Add personal employee content'
}

class UserTypeUtil {
  getUserTypeNameFromBit (userTypeBit) {
    for (const [name, bit] of Object.entries(USER_TYPES)) {
      if (bit === parseInt(userTypeBit)) {
        return name
      }
    }
  }

  getUserTypeList (userTypeBits, isInBits, excludeBits = USER_TYPES.Admin | USER_TYPES.Candidate) {
    return Object.entries(USER_TYPES).reduce((typeList, [userTypeName, userTypeBit]) => {
      const isExcluded = userTypeBit & excludeBits
      if (!isExcluded && (userTypeBits & userTypeBit)) {
        typeList.push((isInBits) ? userTypeBit : userTypeName)
      }
      return typeList
    }, [])
  }
}

const userTypeUtil = new UserTypeUtil()
export default userTypeUtil
