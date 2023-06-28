const
  express = require('express'),
  serveStatic = require('serve-static'),
  history = require('connect-history-api-fallback'),
  port = process.env.PORT || 9000

const app = express()

app.use(history())
app.use(serveStatic('dist/spa', {
  maxAge: '1d',
  setHeaders: setCustomCacheControl
}))

function setCustomCacheControl (res, path) {
  if (serveStatic.mime.lookup(path) === 'text/html') {
    // Custom Cache-Control for HTML files
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate')
  }
}

const listener = app.listen(port, function () {
  console.log('Your server is running on port ' + listener.address().port)
})
