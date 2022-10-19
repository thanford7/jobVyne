const { defineConfig } = require('cypress')

module.exports = defineConfig({
  env: {
    apiUrl: '/api/v1',
    // New user that hasn't completed the onboarding process
    newUserEmail: 'cy-new-user@jobvyne.com',
    newUserPassword: 'cy-NewUser123',
    employeeUserEmail: 'cy-employee-user@jobvyne.com',
    employeeUserPassword: 'cy-EmployeeUser123',
    employerUserEmail: 'cy-employer-user@jobvyne.com',
    employerUserPassword: 'cy-EmployerUser123',
    candidateUserEmail: 'cy-candidate-user@jobvyne.com',
    candidateUserPassword: 'cy-CandidateUser123'
  },
  e2e: {
    baseUrl: 'https://localhost',
    setupNodeEvents (on, config) {
      // implement node event listeners here
    }
  }
})
