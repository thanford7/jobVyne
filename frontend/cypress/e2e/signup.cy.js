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
  })
})
