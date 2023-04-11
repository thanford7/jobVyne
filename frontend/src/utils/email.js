
class EmailUtil {
  constructor () {
    // Keep in sync with ContentPlaceholders on SocialPost backend
    this.PLACEHOLDER_JOB_LINK = {
      name: 'Jobs page link',
      placeholder: '{{link}}',
      example: 'www.app.jobvyne.com/jobs-link/ad8audafdi'
    }
    this.PLACEHOLDER_JOBS_LIST = {
      name: 'Open jobs list',
      placeholder: '{{jobs-list}}',
      example: '- Software engineer\n- Product manager\n- Market analyst'
    }
    this.PLACEHOLDER_EMPLOYEE_FIRST_NAME = {
      name: 'Employee first name',
      placeholder: '{{employee.first_name}}',
      example: 'Jake'
    }
    this.PLACEHOLDER_EMPLOYEE_LAST_NAME = {
      name: 'Employee last name',
      placeholder: '{{employee.last_name}}',
      example: 'Smith'
    }
    this.PLACEHOLDER_EMPLOYER_NAME = {
      name: 'Employer',
      placeholder: '{{employer.name}}',
      example: 'Google'
    }
    this.PLACEHOLDER_APPLICANT_FIRST_NAME = {
      name: 'Applicant first name',
      placeholder: '{{applicant.first_name}}',
      example: 'Emilia'
    }
    this.PLACEHOLDER_APPLICANT_LAST_NAME = {
      name: 'Applicant last name',
      placeholder: '{{applicant.last_name}}',
      example: 'Fairbank'
    }
    this.PLACEHOLDER_JOB_TITLE = {
      name: 'Job title',
      placeholder: '{{job.job_title}}',
      example: 'Product Analyst'
    }
  }
}

const emailUtil = new EmailUtil()
export default emailUtil
