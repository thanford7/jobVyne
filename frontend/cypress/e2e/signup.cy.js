const TEST_USER_EMAIL = 'cy-test@jobvyne.com'
const TEST_USER_PWD = 'CyCy!12Me1'

describe('Sign up process', () => {
  beforeEach(function () {
    cy.intercept('POST', `${Cypress.env('apiUrl')}/user/`).as('signup')
    cy.intercept('POST', `${Cypress.env('apiUrl')}/auth/login/`).as('login')
  })

  it('Unauthenticated user should be redirected to login page', () => {
    cy.visit('/employee')
    cy.location('pathname').should('equal', '/login')
  })

  it('User should not be able to create a new account with a bad password', () => {
    cy.visit('/login?isNew=1')
    cy.get('.jv-email input').type(TEST_USER_EMAIL)
    cy.get('.jv-password input').type('cycycy101') // This password doesn't meet the requirements
    cy.get('.jv-login-btn').click() // Try to submit the new user
    cy.get('.jv-password .q-icon.fa-circle-exclamation').should('be.visible') // The exclamation icon indicates that the password was flagged
  })

  it('User should able to create a new account with a good password', () => {
    cy.visit('/login?isNew=1')
    cy.get('.jv-email input').type(TEST_USER_EMAIL)
    cy.get('.jv-password input').type(TEST_USER_PWD)
    cy.get('.jv-login-btn').click()
    cy.wait('@signup').its('response.statusCode').should('eq', 200)
    cy.wait('@login').its('response.statusCode').should('eq', 200)
    cy.location('pathname').should('equal', '/onboard')

    // Logout user so other tests aren't impacted
    cy.visit('/')
    cy.location('pathname').should('equal', '/')
    cy.get('#jv-logout-btn').click({ force: true })
  })

  it('New user should be directed to onboarding page', () => {
    cy.login(Cypress.env('newUserEmail'), Cypress.env('newUserPassword'))
    cy.location('pathname').should('equal', '/onboard')
  })

  it('Job seeker should advance to name and then have option to finalize', () => {
    cy.get('#jv-job-seeker').click({ force: true })
    cy.get('#jv-forward').click()
    cy.get('.jv-fname input').type('Cypress')
    cy.get('.jv-lname input').type('New')
    cy.get('#jv-forward .q-btn__content > span').should('have.text', 'Finish')
  })

  it('Employee should advance to name, business email, select an employer, and then have option to finalize', () => {
    cy.login(Cypress.env('newUserEmail'), Cypress.env('newUserPassword'))
    cy.location('pathname').should('equal', '/onboard')

    // First step (user type)
    cy.get('#jv-employee').click({ force: true })
    cy.get('#jv-forward').click()

    // Second step (name)
    cy.get('.jv-fname input').type('Cypress')
    cy.get('.jv-lname input').type('New')
    cy.get('#jv-forward').click()

    // Third step (business email) - gmail domain is allowable by two employers
    cy.get('.jv-email input').type('cypress-new@gmail.com').blur()
    cy.get('#jv-forward').click()

    // Fourth step (select employer)
    cy.get('#jv-employer-sel').should('be.visible')

    // Enter an email address not connected to an employer
    cy.get('#jv-back').click()
    cy.get('.jv-email input').clear().type('cypress-new@bogus.com').blur()
    cy.get('#jv-forward').click()
    cy.get('.jv-employer-unknown').should('be.visible')
  })
})
