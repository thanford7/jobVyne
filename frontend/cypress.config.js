const { defineConfig } = require('cypress')

module.exports = defineConfig({
  env: {
    apiUrl: '/api/v1',
    // New user that hasn't completed the onboarding process
    newUserEmail: 'cy-new-user@jobvyne.com',
    newUserPassword: 'Cypress1@34tpy',
    employeeUserEmail: 'cy-employee-user@jobvyne.com',
    employeeUserPassword: 'Cypress1@34tpy',
    employerUserEmail: 'cy-employer-user@jobvyne.com',
    employerUserPassword: 'Cypress1@34tpy',
    candidateUserEmail: 'cy-candidate-user@jobvyne.com',
    candidateUserPassword: 'Cypress1@34tpy'
  },
  e2e: {
    baseUrl: 'https://localhost',
    setupNodeEvents (on, config) {
      // implement node event listeners here
    }
  }
})
