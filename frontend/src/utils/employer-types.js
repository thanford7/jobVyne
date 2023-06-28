class EmployerTypeUtil {
  constructor () {
    // Keep in sync with backend employer model
    this.ORG_TYPE_EMPLOYER = 'employer'
    this.ORG_TYPE_GROUP = 'group'
    this.ORG_TYPE_AGENCY = 'agency'
    this.ORG_TYPES = {
      [this.ORG_TYPE_EMPLOYER]: 0x1,
      [this.ORG_TYPE_GROUP]: 0x2,
      [this.ORG_TYPE_AGENCY]: 0x4
    }
  }

  getEmployerTypeByBit (employerTypeBit) {
    for (const [name, bit] of Object.entries(this.ORG_TYPES)) {
      if (bit === parseInt(employerTypeBit)) {
        return name
      }
    }
  }

  isTypeEmployer (employerTypeBit) {
    return this.ORG_TYPE_EMPLOYER === this.getEmployerTypeByBit(employerTypeBit)
  }

  isTypeGroup (employerTypeBit) {
    return this.ORG_TYPE_GROUP === this.getEmployerTypeByBit(employerTypeBit)
  }

  isTypeAgency (employerTypeBit) {
    return this.ORG_TYPE_AGENCY === this.getEmployerTypeByBit(employerTypeBit)
  }
}

const employerTypeUtil = new EmployerTypeUtil()
export default employerTypeUtil
