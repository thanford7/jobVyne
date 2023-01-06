function createTag (src) {
  const script = document.createElement('script')
  script.type = 'application/javascript'
  script.async = true
  script.src = src
  return script
}

function addListeners (script, callback, resolve, reject) {
  script.addEventListener('error', reject)
  script.addEventListener('abort', reject)
  script.addEventListener('load', function loadScriptHandler () {
    if (callback) {
      callback()
    }
    script.setAttribute('data-loaded', '')
    resolve(removeScript.bind(null, script))
  })
}

export function removeScript (scriptOrSrc) {
  let script
  if (typeof scriptOrSrc === 'string') {
    script = document.querySelector(`script[src="${scriptOrSrc}"]`)
  } else {
    script = scriptOrSrc
  }

  if (script) script.parentNode.removeChild(script)
}

export function loadScript (src, callback = null) {
  return new Promise((resolve, reject) => {
    let script = document.querySelector(`script[src="${src}"]`)

    if (script && script.hasAttribute('data-loaded')) {
      resolve(removeScript.bind(null, script))
      return
    }

    script = createTag(src)
    addListeners(script, callback, resolve, reject)
    document.head.appendChild(script)
  })
}
