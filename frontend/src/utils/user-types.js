// TODO: Importing dataUtil causes pinia to error out
// I've checked circular dependencies and can't find any
// Copying the required functions to this file for now
const getArrayIntersection = (array1, array2) => {
  if (!array1 || !array2) {
    return []
  }
  return array1.filter(value => array2.includes(value))
}

const pick = (object, keys) => {
  return keys.reduce((obj, key) => {
    if (object && Object.prototype.hasOwnProperty.call(object, key)) {
      obj[key] = object[key]
    }
    return obj
  }, {})
}

const uniqArray = (array) => {
  return array.filter((val, idx, arr) => {
    return arr.indexOf(val) === idx
  })
}

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

// Keep in sync with backend user model
export const PERMISSION_NAMES = {
  MANAGE_USER: 'Manage users',
  CHANGE_PERMISSIONS: 'Change user permissions',
  MANAGE_PERMISSION_GROUPS: 'Manage custom permission groups',
  MANAGE_EMPLOYER_CONTENT: 'Manage employer content',
  MANAGE_EMPLOYER_JOBS: 'Manage employer jobs',
  MANAGE_REFERRAL_BONUSES: 'Manage employee referral bonuses',
  ADD_EMPLOYEE_CONTENT: 'Add personal employee content',
  MANAGE_BILLING_SETTINGS: 'Manage billing settings',
  MANAGE_EMPLOYER_SETTINGS: 'Manage employer settings'
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

export const EMAIL_VALIDATION_KEYS = {
  PERSONAL: 'is_email_verified',
  EMPLOYER: 'is_employer_verified'
}
const isUserEmployerFn = (permissionGroups, permissions) => {
  // User has the employer type
  return permissionGroups && permissionGroups.reduce((allUserBits, authGroup) => {
    allUserBits |= authGroup.user_type_bit
    return allUserBits
  }, 0) & USER_TYPES[USER_TYPE_EMPLOYER]
}

export const userCfgMap = {
  [USER_TYPES.Admin]: {
    viewLabel: 'Admin',
    viewIcon: 'admin_panel_settings',
    namespace: 'admin',
    menuItems: [
      {
        icon: 'home',
        key: 'admin-dashboard',
        label: 'Dashboard',
        emailValidationKey: EMAIL_VALIDATION_KEYS.PERSONAL,
        separator: false
      }
    ]
  },
  [USER_TYPES.Candidate]: {
    viewLabel: 'Job seeker',
    viewIcon: 'fa-solid fa-binoculars',
    namespace: 'candidate',
    menuItems: [
      {
        icon: 'home',
        key: 'candidate-dashboard',
        label: 'Dashboard',
        separator: false
      }
    ]
  },
  [USER_TYPES.Employee]: {
    viewLabel: 'Employee',
    viewIcon: 'work',
    namespace: 'employee',
    menuItems: [
      {
        icon: 'home',
        key: 'employee-dashboard',
        label: 'Dashboard',
        emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
        separator: false
      },
      {
        icon: 'link',
        key: 'employee-links',
        label: 'Referral Links',
        emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
        separator: false
      },
      {
        icon: 'web',
        key: 'employee-profile-page',
        label: 'Profile Page',
        emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
        isPermittedFn: (permissionGroups, permissions) => {
          return permissions && permissions.includes(PERMISSION_NAMES.ADD_EMPLOYEE_CONTENT)
        },
        separator: false
      },
      {
        icon: 'share',
        key: 'employee-social-accounts',
        label: 'Social Accounts',
        separator: false
      },
      {
        icon: 'dynamic_feed',
        key: 'employee-content',
        label: 'Content',
        emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
        separator: true
      }
    ]
  },
  [USER_TYPES.Influencer]: {
    viewLabel: 'Influencer',
    viewIcon: 'groups_3',
    namespace: 'influencer',
    menuItems: [
      {
        icon: 'home',
        key: 'influencer-dashboard',
        label: 'Dashboard',
        emailValidationKey: EMAIL_VALIDATION_KEYS.PERSONAL,
        separator: false
      }
    ]
  },
  [USER_TYPES.Employer]: {
    viewLabel: 'Employer',
    viewIcon: 'business',
    namespace: 'employer',
    menuItems: [
      {
        icon: 'home',
        key: 'employer-dashboard',
        label: 'Dashboard',
        emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
        isPermittedFn: isUserEmployerFn,
        separator: false
      },
      {
        icon: 'web',
        key: 'employer-profile-page',
        label: 'Profile Page',
        emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
        isPermittedViewFn: isUserEmployerFn,
        isPermittedFn: (permissionGroups, permissions) => {
          return isUserEmployerFn(permissionGroups, permissions) && permissions.includes(PERMISSION_NAMES.MANAGE_EMPLOYER_CONTENT)
        },
        separator: false
      },
      {
        icon: 'groups',
        key: 'employer-user-management',
        label: 'Users',
        emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
        isPermittedViewFn: isUserEmployerFn,
        isPermittedFn: (permissionGroups, permissions) => {
          const allowedPermissions = [PERMISSION_NAMES.MANAGE_PERMISSION_GROUPS, PERMISSION_NAMES.MANAGE_USER]
          return isUserEmployerFn(permissionGroups, permissions) && getArrayIntersection(allowedPermissions, permissions).length
        },
        separator: false
      },
      {
        icon: 'message',
        key: 'employer-messages',
        label: 'Employer Messages',
        emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
        isPermittedViewFn: isUserEmployerFn,
        isPermittedFn: (permissionGroups, permissions) => {
          return isUserEmployerFn(permissionGroups, permissions) && permissions.includes(PERMISSION_NAMES.MANAGE_EMPLOYER_CONTENT)
        },
        separator: false
      },
      {
        icon: 'dynamic_feed',
        key: 'employer-content',
        label: 'Content',
        emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
        isPermittedViewFn: isUserEmployerFn,
        isPermittedFn: (permissionGroups, permissions) => {
          return isUserEmployerFn(permissionGroups, permissions) && permissions.includes(PERMISSION_NAMES.MANAGE_EMPLOYER_CONTENT)
        },
        separator: false
      },
      {
        icon: 'settings',
        key: 'employer-settings',
        label: 'Settings',
        emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
        isPermittedFn: (permissionGroups, permissions) => {
          const allowedPermissions = [PERMISSION_NAMES.MANAGE_EMPLOYER_SETTINGS, PERMISSION_NAMES.MANAGE_BILLING_SETTINGS]
          return isUserEmployerFn(permissionGroups, permissions) && getArrayIntersection(allowedPermissions, permissions).length
        },
        separator: true
      }
    ]
  }
}

const userPagePermissionCfgs = Object.entries(userCfgMap).reduce((userPermissionCfgs, [userTypeBit, cfg]) => {
  cfg.menuItems.forEach((item) => {
    userPermissionCfgs[item.key] = Object.assign(
      { userTypeBit },
      pick(item, ['emailValidationKey', 'isPermittedFn', 'isPermittedViewFn'])
    )
  })
  return userPermissionCfgs
}, {})

export const getUserPagePermissions = (user, pageKey) => {
  const pagePermissionCfg = userPagePermissionCfgs[pageKey]
  // Only certain pages require permission checks
  if (!pagePermissionCfg) {
    return { canView: true, canEdit: true }
  }
  const { userTypeBit, emailValidationKey, isPermittedFn, isPermittedViewFn } = pagePermissionCfg

  // User doesn't have the appropriate user type (e.g. user is not an employee)
  if (!(userTypeBit & user.user_type_bits)) {
    return { canView: false, canEdit: false }
  }

  // User has not validated their email and it is required to view the page
  if (emailValidationKey && !user[emailValidationKey]) {
    return { canView: false, canEdit: false }
  }

  const userPermissions = getAllUserPermissions(user)
  const userPermissionGroups = getAllUserPermissionGroups(user)
  const canEdit = !isPermittedFn || isPermittedFn(userPermissionGroups, userPermissions)
  const canView = canEdit || !isPermittedViewFn || isPermittedViewFn(userPermissionGroups, userPermissions)
  return { canView, canEdit }
}

const getAllUserPermissions = (user) => {
  const allPermissions = Object.values(user.permissions_by_employer).reduce((allPermissions, permissions) => {
    return [...allPermissions, ...permissions]
  }, [])
  return uniqArray(allPermissions)
}

const getAllUserPermissionGroups = (user) => {
  return Object.values(user.permission_groups_by_employer).reduce((allGroups, groups) => {
    return [...allGroups, ...groups]
  }, [])
}

/**
 * Look for a dashboard that the user can view. If no dashboards are viewable,
 * revert to the user's profile page
 * @param user
 * @param userTypeBit {null | int}: If included, the dashboard for this userType will be used
 * @returns {string}
 */
export const getDefaultLandingPageKey = (user, userTypeBit = null) => {
  for (const [pageKey, permissionCfg] of Object.entries(userPagePermissionCfgs)) {
    if (pageKey.includes('dashboard') && (!userTypeBit || (userTypeBit & permissionCfg.userTypeBit))) {
      const { canView } = getUserPagePermissions(user, pageKey)
      if (canView) {
        return pageKey
      }
    }
  }
  return 'profile'
}
