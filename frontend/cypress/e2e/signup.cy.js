describe('Sign up process', () => {
  it('Unauthenticated user should be redirected to login page', () => {
    cy.visit('/employee')
    cy.location('pathname').should('equal', '/login')
  })
})
