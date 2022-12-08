describe('Job application', () => {
  beforeEach(function () {
    cy.intercept('POST', `${Cypress.env('apiUrl')}/job-application/`).as('jobApplication')
    cy.intercept('POST', `${Cypress.env('apiUrl')}/user/`).as('createUser')
  })

  it('Jobs page loads correctly', () => {
    cy.visit('/jobs-link/3089c5b6-477a-4dbf-acff-a28d4ed69f89?platform=LinkedIn')

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
    cy.visit('/jobs-link/3089c5b6-477a-4dbf-acff-a28d4ed69f89?platform=LinkedIn')
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

    cy.wait('@jobApplication').its('response.statusCode').should('eq', 200)

    // Anonymous user should be prompted to create an account
    cy.get('.jv-form-job-app-create').should('have.text', 'Create an account')
    cy.get('.jv-password input').type('Cypress2@34tpy')
    cy.get('.jv-login-btn').click()
    cy.wait('@createUser').its('response.statusCode').should('eq', 200)

    // User should now be prompted to confirm their email
    cy.get('.jv-form-job-app-confirm').should('have.text', 'Last step')

    // TODO: Figure out how to update user's email_confirmation
    // // Job that was just applied to should no longer have the option to apply
    // cy.get('.jv-apply-btn').should('have.length', 4)
    //
    // // New application should have fields populated with user's content
    // cy.get('.jv-apply-btn').first().click()
    // cy.get('.jv-form-job-app-fname').should('have.text', firstName)
    // cy.get('.jv-form-job-app-lname').should('have.text', lastName)
    // cy.get('.jv-form-job-app-email').should('have.text', email)
    // cy.get('.jv-form-job-app-linkedin').should('have.text', linkedIn)
    // cy.get('.jv-existing-file input').should('have.text', 'TestResume.pdf')
    //
    // // New submission should work with all fields already filled in
    // cy.get('.jv-form-job-app-submit').click()
    // cy.wait('@jobApplication').its('response.statusCode').should('eq', 200)
  })

  it('Authenticated user should be able to submit an application', () => {
    cy.login(Cypress.env('candidateUserEmail'), Cypress.env('candidateUserPassword'))
    cy.visit('/jobs-link/3089c5b6-477a-4dbf-acff-a28d4ed69f89?platform=LinkedIn')

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
    cy.wait('@jobApplication').its('response.statusCode').should('eq', 200)
  })
})
