const jobsUrl = '/jobs-link/3089c5b6-477a-4dbf-acff-a28d4ed69f89?platform=LinkedIn'

describe('Job application', () => {
  beforeEach(function () {
    cy.intercept('POST', `${Cypress.env('apiUrl')}/job-application/`).as('postJobApplication')
    cy.intercept('POST', `${Cypress.env('apiUrl')}/user/`).as('createUser')
    cy.intercept('POST', `${Cypress.env('apiUrl')}/auth/login/`).as('login')
    cy.intercept('POST', `${Cypress.env('apiUrl')}/auth/logout/`).as('logout')
  })

  it('Jobs page loads correctly', () => {
    cy.visit(jobsUrl)

    // Check the jobs tab
    cy.get('#jv-tab-jobs').should('exist')
    cy.get('.jv-job-card').should('have.length', 5)

    // Check the company tab
    cy.get('#jv-tab-company').click()
    cy.get('#employer-0').should('have.text', 'About us')

    // Check the me tab
    cy.get('#jv-tab-me').click()
    cy.contains('Chief Exporter').should('exist')
  })

  it('Anonymous user should be able to submit an application', () => {
    cy.visit(jobsUrl)
    const firstName = 'Becky'
    const lastName = 'Beckham'
    const email = 'b.beckham@cypress.com'
    const linkedIn = 'www.linkedin.com/in/bbeckham'

    // Fill in and submit application
    cy.get('.jv-apply-btn').first().click()
    cy.get('.jv-form-job-app-fname').type(firstName)
    cy.get('.jv-form-job-app-lname').type(lastName)
    cy.get('.jv-form-job-app-email').type(email)
    cy.get('.jv-form-job-app-linkedin').type(linkedIn)
    cy.get('.jv-form-job-app-resume').selectFile('cypress/fixtures/TestResume.pdf')
    cy.get('.jv-form-job-app-submit').click()

    cy.wait('@postJobApplication').its('response.statusCode').should('eq', 200)

    // Anonymous user should be prompted to create an account
    cy.get('.jv-form-job-app-create').should('have.text', 'Create an account')
    cy.get('.jv-password input').type('Cypress2@34tpy')
    cy.get('.jv-login-btn').click()
    cy.wait('@createUser').its('response.statusCode').should('eq', 200)

    // User should now be prompted to confirm their email
    cy.get('.jv-form-job-app-confirm').should('have.text', 'Last step')
  })

  it('Authenticated user should be able to submit an application', () => {
    cy.login(Cypress.env('candidateUserEmail'), Cypress.env('candidateUserPassword'))
    cy.visit(jobsUrl)

    // User has already applied to one job so that apply button should be hidden
    cy.get('.jv-apply-btn').should('have.length', 4)

    // New application should have fields populated with user's content
    cy.get('.jv-apply-btn').first().click()
    cy.get('.jv-form-job-app-fname input').should('have.value', 'Cypress')
    cy.get('.jv-form-job-app-lname input').should('have.value', 'Candidate')
    cy.get('.jv-form-job-app-email input').should('have.value', 'cy-candidate-user@jobvyne.com')
    cy.get('.jv-form-job-app-linkedin input').should('have.value', 'www.linkedin.com/in/cypresscan')
    cy.get('.jv-existing-file input').should('have.value', 'TestResume.pdf')

    // New submission should work with all fields already filled in
    cy.get('.jv-form-job-app-submit').click()
    cy.wait('@postJobApplication').its('response.statusCode').should('eq', 200)

    // Make sure sidebar closed
    cy.get('.jv-form-job-app-submit').should('not.exist')

    // When user logs out, all submission buttons should be shown
    cy.get('#jv-logout').click({force: true})
    cy.wait('@logout').its('response.statusCode').should('eq', 200)
    cy.get('.jv-apply-btn').should('have.length', 5)
  })

  it('User should be able to sign in from the sidebar', () => {
    cy.visit(jobsUrl)

    // Open login dialog
    cy.get('.jv-apply-btn').first().click()
    cy.get('#jv-form-job-app-login').click()

    // Login
    cy.get('.jv-email input').type(Cypress.env('candidateUserEmail'))
    cy.get('.jv-password input').type(Cypress.env('candidateUserPassword'))
    cy.get('.jv-login-btn').click()
    cy.wait('@login').its('response.statusCode').should('eq', 200)

    // Login dialog should close
    cy.get('.jv-email').should('not.exist')

    // Form field should fill in
    cy.get('.jv-form-job-app-fname input').should('have.value', 'Cypress')
    cy.get('.jv-form-job-app-lname input').should('have.value', 'Candidate')
    cy.get('.jv-form-job-app-email input').should('have.value', 'cy-candidate-user@jobvyne.com')
    cy.get('.jv-form-job-app-linkedin input').should('have.value', 'www.linkedin.com/in/cypresscan')
    cy.get('.jv-existing-file input').should('have.value', 'TestResume.pdf')
  })
})
