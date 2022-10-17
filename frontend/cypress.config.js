const { defineConfig } = require('cypress')

module.exports = defineConfig({
  env: {
    apiUrl: 'https://localhost:3001'
  },
  e2e: {
    baseUrl: 'https://localhost',
    setupNodeEvents (on, config) {
      // implement node event listeners here
    }
  }
})
