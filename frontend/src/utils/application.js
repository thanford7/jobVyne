import dataUtil from 'src/utils/data.js'

class ApplicationUtil {
  constructor () {
    // Keep in sync with JobApplication ApplicationStatus
    this.INTERESTED = 'interested'
    this.APPLIED = 'applied'
    this.APPROVED = 'application approved'
    this.INTERVIEWING = 'interviewing'
    this.HIRED = 'hired'
    this.DECLINED = 'declined'
    this.ARCHIVED = 'archived'

    this.APPLICATION_STATUSES = {
      [this.INTERESTED]: {
        label: dataUtil.capitalize(this.INTERESTED),
        val: this.INTERESTED,
        isEmployerValue: false,
        isCandidateValue: true
      },
      [this.APPLIED]: {
        label: dataUtil.capitalize(this.APPLIED),
        val: this.APPLIED,
        isEmployerValue: true,
        isCandidateValue: true
      },
      [this.APPROVED]: {
        label: dataUtil.capitalize(this.APPROVED),
        val: this.APPROVED,
        isEmployerValue: true,
        isCandidateValue: false
      },
      [this.INTERVIEWING]: {
        label: dataUtil.capitalize(this.INTERVIEWING),
        val: this.INTERVIEWING,
        isEmployerValue: true,
        isCandidateValue: false
      },
      [this.HIRED]: {
        label: dataUtil.capitalize(this.HIRED),
        val: this.HIRED,
        isEmployerValue: true,
        isCandidateValue: false
      },
      [this.DECLINED]: {
        label: dataUtil.capitalize(this.DECLINED),
        val: this.DECLINED,
        isEmployerValue: true,
        isCandidateValue: false
      },
      [this.ARCHIVED]: {
        label: dataUtil.capitalize(this.ARCHIVED),
        val: this.ARCHIVED,
        isEmployerValue: true,
        isCandidateValue: false
      }
    }

    // Keep in sync with UserApplicationReview Rating
    this.POSITIVE = 2
    this.NEUTRAL = 1
    this.NEGATIVE = 0

    this.RATINGS = {
      [this.POSITIVE]: { label: 'Positive', icon: 'thumb_up', val: this.POSITIVE, color: 'positive' },
      [this.NEUTRAL]: { label: 'Neutral', icon: 'sentiment_neutral', val: this.NEUTRAL, color: 'grey-7' },
      [this.NEGATIVE]: { label: 'Negative', icon: 'thumb_down', val: this.NEGATIVE, color: 'negative' }
    }
  }
}

const applicationUtil = new ApplicationUtil()

export default applicationUtil
