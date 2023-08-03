// Keep in sync with JobVyneUser member types
export const MEMBER_TYPE_ALL = 0
export const MEMBER_TYPE_JOB_SEEKER = 1
export const MEMBER_TYPE_HIRING_MGR = 2
export const MEMBER_TYPES = {
  // The value for member type "ALL" has to be truthy for quasar filters to work properly so we can't use 0
  [MEMBER_TYPE_ALL]: { filter_label: 'All members', name: 'Community member', value: 'all' },
  [MEMBER_TYPE_JOB_SEEKER]: { filter_label: 'Job seekers', name: 'Job seeker', value: MEMBER_TYPE_JOB_SEEKER },
  [MEMBER_TYPE_HIRING_MGR]: { filter_label: 'Hiring managers', name: 'Hiring manager', value: MEMBER_TYPE_HIRING_MGR }
}

export const CONNECTION_TYPE_HIRING_MEMBER = 1
export const CONNECTION_TYPE_CURRENT_EMPLOYEE = 2
export const CONNECTION_TYPE_FORMER_EMPLOYEE = 4
export const CONNECTION_TYPE_KNOW_EMPLOYEE = 8
export const CONNECTION_TYPE_NO_CONNECTION = 16

// Keep in sync with ConnectionTypeBit
export const CONNECTION_TYPES = {
  [CONNECTION_TYPE_HIRING_MEMBER]: { name: 'Hiring team', value: CONNECTION_TYPE_HIRING_MEMBER },
  [CONNECTION_TYPE_CURRENT_EMPLOYEE]: { name: 'Current employee', value: CONNECTION_TYPE_CURRENT_EMPLOYEE },
  [CONNECTION_TYPE_FORMER_EMPLOYEE]: { name: 'Former employee', value: CONNECTION_TYPE_FORMER_EMPLOYEE },
  [CONNECTION_TYPE_KNOW_EMPLOYEE]: { name: 'Knows company employee', value: CONNECTION_TYPE_KNOW_EMPLOYEE },
  [CONNECTION_TYPE_NO_CONNECTION]: { name: 'No company connection', value: CONNECTION_TYPE_NO_CONNECTION }
}

class CommunityUtil {
  get_member_type_label (memberTypeBits) {
    return Object.entries(MEMBER_TYPES).reduce((labels, [memberTypeBit, memberType]) => {
      if (memberTypeBit & memberTypeBits) {
        labels.push(memberType.name)
      }
      return labels
    }, []).join(', ')
  }

  isJobSeeker (memberTypeBits) {
    return Boolean(memberTypeBits & MEMBER_TYPE_JOB_SEEKER)
  }

  isHiringManager (memberTypeBits) {
    return Boolean(memberTypeBits & MEMBER_TYPE_HIRING_MGR)
  }

  isConnectionHiringMember (connectionTypeBit) {
    return Boolean(connectionTypeBit & CONNECTION_TYPE_HIRING_MEMBER)
  }

  isConnectionCurrentEmployee (connectionTypeBit) {
    return Boolean(connectionTypeBit & CONNECTION_TYPE_CURRENT_EMPLOYEE)
  }

  isConnectionFormerEmployee (connectionTypeBit) {
    return Boolean(connectionTypeBit & CONNECTION_TYPE_FORMER_EMPLOYEE)
  }

  isConnectionKnowEmployee (connectionTypeBit) {
    return Boolean(connectionTypeBit & CONNECTION_TYPE_KNOW_EMPLOYEE)
  }

  isConnectionNone (connectionTypeBit) {
    return Boolean(connectionTypeBit & CONNECTION_TYPE_NO_CONNECTION)
  }
}

const communityUtil = new CommunityUtil()
export default communityUtil
