import dataUtil from 'src/utils/data.js'

class ApplicantFeedbackUtil {
  constructor () {
    this.NULL_DEFAULT_VAL = 'No response'
    this.KNOW_APPLICANT_NO = 0
    this.KNOW_APPLICANT_PROFESSIONAL = 1
    this.KNOW_APPLICANT_SOCIAL = 2
    this.FEEDBACK_KNOW_APPLICANT_OPTS = {
      [this.KNOW_APPLICANT_NO]: { label: 'No', val: this.KNOW_APPLICANT_NO },
      [this.KNOW_APPLICANT_PROFESSIONAL]: { label: 'Professionally', val: this.KNOW_APPLICANT_PROFESSIONAL },
      [this.KNOW_APPLICANT_SOCIAL]: { label: 'Socially', val: this.KNOW_APPLICANT_SOCIAL }
    }

    this.RECOMMEND_NO = 0
    this.RECOMMEND_YES = 1
    this.RECOMMEND_UNSURE = 2
    this.RECOMMEND_NA = 3
    this.RECOMMEND_APPLICANT_OPTS = {
      [this.RECOMMEND_NO]: { label: 'No', val: this.RECOMMEND_NO },
      [this.RECOMMEND_YES]: { label: 'Yes', val: this.RECOMMEND_YES },
      [this.RECOMMEND_UNSURE]: { label: 'Not sure', val: this.RECOMMEND_UNSURE },
      [this.RECOMMEND_NA]: { label: 'Not applicable', val: this.RECOMMEND_NA }
    }
  }

  getKnowApplicantOpts () {
    return [...Object.values(this.FEEDBACK_KNOW_APPLICANT_OPTS), { label: this.NULL_DEFAULT_VAL, val: null }]
  }

  getRecommendApplicantOpts () {
    return [...Object.values(this.RECOMMEND_APPLICANT_OPTS), { label: this.NULL_DEFAULT_VAL, val: null }]
  }

  getKnowApplicantLabel (val) {
    if (dataUtil.isNil(val)) {
      return this.NULL_DEFAULT_VAL
    }
    return this.FEEDBACK_KNOW_APPLICANT_OPTS[val].label
  }

  getRecommendApplicantLabel (val) {
    if (dataUtil.isNil(val)) {
      return this.NULL_DEFAULT_VAL
    }
    return this.RECOMMEND_APPLICANT_OPTS[val].label
  }
}

const applicantFeedbackUtil = new ApplicantFeedbackUtil()

export default applicantFeedbackUtil
