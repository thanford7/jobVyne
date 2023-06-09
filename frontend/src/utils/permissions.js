import employerTypeUtil from 'src/utils/employer-types.js'
import { USER_TYPE_EMPLOYER, USER_TYPES } from 'src/utils/user-types.js'
import dataUtil from 'src/utils/data.js'

const EMAIL_VALIDATION_KEYS = {
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

class PagePermissionsUtil {
  constructor () {
    // Keep in sync with backend user model
    this.PERMISSION_NAMES = {
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

    this.userCfgMap = {
      [USER_TYPES.Admin]: {
        viewLabel: 'Admin',
        viewIcon: 'admin_panel_settings',
        namespace: 'admin',
        menuItems: [
          {
            icon: 'home',
            key: 'admin-dashboard',
            label: 'Dashboard',
            emailValidationKey: EMAIL_VALIDATION_KEYS.PERSONAL
          },
          {
            icon: 'business',
            key: 'admin-employers',
            label: 'Employers',
            emailValidationKey: EMAIL_VALIDATION_KEYS.PERSONAL
          },
          {
            icon: 'screenshot_monitor',
            key: 'admin-scrapers',
            label: 'Job Scrapers',
            emailValidationKey: EMAIL_VALIDATION_KEYS.PERSONAL
          },
          {
            icon: 'people',
            key: 'admin-users',
            label: 'Users',
            emailValidationKey: EMAIL_VALIDATION_KEYS.PERSONAL
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
            label: 'Dashboard'
          }
        ]
      },
      [USER_TYPES.Employee]: {
        viewLabel: 'Employee',
        viewIcon: 'badge',
        namespace: 'employee',
        menuItems: [
          {
            icon: 'home',
            key: 'employee-dashboard',
            label: 'Dashboard',
            emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER
          },
          {
            icon: 'work',
            key: 'employee-jobs',
            label: 'Jobs',
            emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER
          },
          {
            icon: 'contact_page',
            key: 'employee-applications',
            label: 'Job Referrals',
            emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER
          },
          {
            icon: 'web',
            key: 'employee-profile-page',
            label: 'Profile Settings',
            emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
            isPermittedFn: (permissionGroups, permissions) => {
              return permissions && permissions.includes(this.PERMISSION_NAMES.ADD_EMPLOYEE_CONTENT)
            }
          },
          {
            icon: 'share',
            key: 'employee-social-accounts',
            label: 'Social Accounts'
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
            emailValidationKey: EMAIL_VALIDATION_KEYS.PERSONAL
          },
          {
            icon: 'dvr',
            key: 'influencer-jobs',
            label: 'Job boards',
            emailValidationKey: EMAIL_VALIDATION_KEYS.PERSONAL
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
            isPermittedFn: isUserEmployerFn
          },
          {
            icon: 'work',
            key: 'employer-jobs',
            label: 'Jobs',
            emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
            isPermittedViewFn: (permissionGroups, permissions, orgTypeBit) => {
              return isUserEmployerFn(permissionGroups, permissions) && employerTypeUtil.isTypeEmployer(orgTypeBit)
            },
            isPermittedFn: (permissionGroups, permissions, orgTypeBit) => {
              return (
                isUserEmployerFn(permissionGroups, permissions) &&
                permissions.includes(this.PERMISSION_NAMES.MANAGE_REFERRAL_BONUSES) &&
                employerTypeUtil.isTypeEmployer(orgTypeBit)
              )
            }
          },
          {
            icon: 'person_add',
            key: 'employer-referrals',
            label: 'Employee Referrals',
            emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
            isPermittedViewFn: (permissionGroups, permissions, orgTypeBit) => {
              return isUserEmployerFn(permissionGroups, permissions) && employerTypeUtil.isTypeEmployer(orgTypeBit)
            },
            isPermittedFn: (permissionGroups, permissions, orgTypeBit) => {
              return (
                isUserEmployerFn(permissionGroups, permissions) &&
                permissions.includes(this.PERMISSION_NAMES.MANAGE_REFERRAL_BONUSES) &&
                employerTypeUtil.isTypeEmployer(orgTypeBit)
              )
            }
          },
          // TODO: Still in development
          // {
          //   icon: 'add_business',
          //   key: 'employer-job-adds',
          //   label: 'Job Adds',
          //   emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
          //   // isPermittedViewFn: isUserEmployerFn, TODO: Need to check org type of employer. If group, don't show this tab
          //   isPermittedFn: isUserEmployerFn
          // },
          {
            icon: 'dvr',
            key: 'employer-job-boards',
            label: 'Job Boards',
            emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
            isPermittedFn: isUserEmployerFn
          },
          {
            icon: 'contact_page',
            key: 'employer-applications',
            label: 'Job Applications',
            emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
            isPermittedFn: isUserEmployerFn
          },
          {
            icon: 'groups',
            key: 'employer-user-management',
            label: 'Users',
            emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
            isPermittedViewFn: isUserEmployerFn,
            isPermittedFn: (permissionGroups, permissions) => {
              const allowedPermissions = [this.PERMISSION_NAMES.MANAGE_PERMISSION_GROUPS, this.PERMISSION_NAMES.MANAGE_USER]
              return isUserEmployerFn(permissionGroups, permissions) && dataUtil.getArrayIntersection(allowedPermissions, permissions).length
            }
          },
          // TODO: Hide until messaging is supported
          // {
          //   icon: 'message',
          //   key: 'employer-messages',
          //   label: 'Employer Messages',
          //   emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
          //   isPermittedViewFn: isUserEmployerFn,
          //   isPermittedFn: (permissionGroups, permissions) => {
          //     return isUserEmployerFn(permissionGroups, permissions) && permissions.includes(this.PERMISSION_NAMES.MANAGE_EMPLOYER_CONTENT)
          //   }
          // },
          {
            icon: 'settings',
            key: 'employer-settings',
            label: 'Settings',
            emailValidationKey: EMAIL_VALIDATION_KEYS.EMPLOYER,
            isPermittedFn: (permissionGroups, permissions) => {
              const allowedPermissions = [this.PERMISSION_NAMES.MANAGE_EMPLOYER_SETTINGS, this.PERMISSION_NAMES.MANAGE_BILLING_SETTINGS]
              return isUserEmployerFn(permissionGroups, permissions) && dataUtil.getArrayIntersection(allowedPermissions, permissions).length
            }
          }
        ]
      }
    }

    this.userPagePermissionCfgs = Object.entries(this.userCfgMap).reduce((userPermissionCfgs, [userTypeBit, cfg]) => {
      cfg.menuItems.forEach((item) => {
        userPermissionCfgs[item.key] = Object.assign(
          { userTypeBit, namespace: cfg.namespace },
          dataUtil.pick(item, ['emailValidationKey', 'isPermittedFn', 'isPermittedViewFn'])
        )
      })
      return userPermissionCfgs
    }, {})
  }

  getUserPagePermissions (user, pageKey) {
    const pagePermissionCfg = this.userPagePermissionCfgs[pageKey]
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

    const userPermissions = this.getAllUserPermissions(user)
    const userPermissionGroups = this.getAllApprovedUserPermissionGroups(user)
    const canEdit = !isPermittedFn || isPermittedFn(userPermissionGroups, userPermissions, user.employer_org_type)
    const canView = (
      canEdit ||
      (!isPermittedFn && !isPermittedViewFn) ||
      (isPermittedViewFn && isPermittedViewFn(userPermissionGroups, userPermissions, user.employer_org_type))
    )
    return { canView, canEdit }
  }

  filterViewablePages (user, userTypeBit) {
    const menuItems = this.userCfgMap[userTypeBit].menuItems
    return menuItems.filter((item) => {
      return this.getUserPagePermissions(user, item.key).canView
    })
  }

  getAllUserPermissions (user) {
    const allPermissions = Object.values(user.permissions_by_employer).reduce((allPermissions, permissions) => {
      return [...allPermissions, ...permissions]
    }, [])
    return dataUtil.uniqArray(allPermissions)
  }

  getAllApprovedUserPermissionGroups (user) {
    return Object.values(user.permission_groups_by_employer).reduce((allGroups, groups) => {
      const approvedGroups = groups.filter((g) => g.is_approved)
      return [...allGroups, ...approvedGroups]
    }, [])
  }

  hasPermission (user, permission) {
    return this.getAllUserPermissions(user).includes(permission)
  }

  /**
   * Look for a dashboard that the user can view. If no dashboards are viewable,
   * revert to the user's profile page
   * @param user
   * @param userTypeBit {null | int}: If included, the dashboard for this userType will be used
   * @returns {Object}
   */
  getDefaultLandingPage (user, userTypeBit = null) {
    for (const [pageKey, permissionCfg] of Object.entries(this.userPagePermissionCfgs)) {
      if (pageKey.includes('dashboard') && (!userTypeBit || (userTypeBit & permissionCfg.userTypeBit))) {
        const { canView } = this.getUserPagePermissions(user, pageKey)
        if (canView) {
          return this.getRouterPageCfg(pageKey)
        }
      }
    }
    return this.getRouterPageCfg('profile')
  }

  getRouterPageCfg (pageKey, userTypeBit = null) {
    const routerCfg = { name: pageKey, params: { key: pageKey } }
    const pageCfg = this.userPagePermissionCfgs[pageKey]

    if (!pageCfg) {
      routerCfg.params.namespace = 'user'
      // Use the existing user type bit if this is a generic user page
      routerCfg.params.userTypeBit = userTypeBit
    } else {
      routerCfg.params.namespace = pageCfg.namespace
    }
    return routerCfg
  }
}

const pagePermissionsUtil = new PagePermissionsUtil()
export default pagePermissionsUtil
