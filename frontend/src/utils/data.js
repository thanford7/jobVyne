import clone from 'just-clone'

class DataUtil {
  formatCurrency (val) {
    const formatter = new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0, // (this suffices for whole numbers, but will print 2500.10 as $2,500.1)
      maximumFractionDigits: 0 // (causes 2500.99 to be printed as $2,501)
    })

    return formatter.format(val)
  }

  copyText (e) {
    const targetEl = e.currentTarget
    const copyTargetEl = targetEl.closest('div').querySelector('.copy-target')
    const text = copyTargetEl.text() || copyTargetEl.val()
    const copyMsgId = this.getNewElUid()
    navigator.clipboard.writeText(text).then(
      () => {
        targetEl.parentNode.insertAdjacentHTML(
          'beforeend',
          `<span id="${copyMsgId}" class="-color-green-text -sub-text"> Copied successfully</span>`
        )
      }, () => {
        targetEl.parentNode.insertAdjacentHTML(
          'beforeend',
          `<span id="${copyMsgId}" class="-color-red-text -sub-text"> Copy failed. Please copy manually</span>`
        )
      }
    )
    setTimeout(() => {
      document.getElementById(copyMsgId).remove()
    }, 3000)
  }

  getFileNameFromUrl (fileUrl) {
    if (!fileUrl) {
      return null
    }
    const [fileName] = fileUrl.split('/').slice(-1)
    return fileName
  }

  getUrlWithoutQueryParams () {
    return window.location.origin + window.location.pathname
  }

  getQueryParams () {
    const searchParams = new URLSearchParams(window.location.search)
    const paramDict = {}
    for (const [key, val] of searchParams.entries()) {
      if (key in paramDict) {
        const currentVal = paramDict[key]
        if (Array.isArray(currentVal)) {
          currentVal.push(val)
        } else {
          paramDict[key] = [currentVal, val]
        }
      } else {
        paramDict[key] = val
      }
    }
    return paramDict
  }

  getUrlWithParams (params, path, isExcludeExistingParams = false) {
    if (!('URLSearchParams' in window)) {
      return
    }
    const searchParams = (isExcludeExistingParams) ? new URLSearchParams() : new URLSearchParams(window.location.search)
    params.forEach(({ key, val }) => {
      searchParams.delete(key) // Remove existing
      const vals = (Array.isArray(val)) ? val : [val]
      vals.forEach((v) => {
        if (!this.isNil(val)) {
          searchParams.append(key, v)
        }
      }) // Add new values
    })
    const targetPath = path || window.location.pathname
    return targetPath + '?' + searchParams.toString()
  }

  /**
   * Update query params and optionally redirect to a new page
   * @param params {Array}: Array of dicts with key: val: pairs. The key represents the name of the query param and
   * val represents the value. Val can be a single value or a list of values. Example: [{key: 'tab', val: 'settings'}]
   * @param path {null|string}: Optional path if directing to a new page
   */
  setQueryParams (params, path = null) {
    const newRelativePathQuery = this.getUrlWithParams(params, path)
    if (!newRelativePathQuery) {
      return
    }
    if (path) {
      window.location.href = newRelativePathQuery // Redirect to new page
    } else {
      history.pushState(null, '', newRelativePathQuery) // Add to view state
    }
  }

  handleAjaxError (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      const data = error.response.data
      if (!data.includes('DOCTYPE')) {
        console.log(error.response.data)
      }
      console.log(error.response.status)
      console.log(error.response.headers)
    } else if (error.request) {
      // The request was made but no response was received
      // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
      // http.ClientRequest in node.js
      console.log(error.request)
    } else {
      // Something happened in setting up the request that triggered an Error
      console.log('Error', error.message)
    }
    console.log(error.config)
  }

  /**
   * We can't add meta data directly onto file objects and order is not guaranteed when pairing files with
   * their respective meta data. To handle this, file objects and file meta data are processed into a dictionary
   * where the lookup value is based on the file object's name. This is the only "unique" key that the file object
   * possesses. It is possible for a file object to have the same name as another, so duplicate file names should
   * be guarded against when testing for good form data
   * @param files {Object|Array} Values are objects which contain meta data and a file
   * @param metaDataKey {string} The dictionary key which all meta data is assigned to
   * @param dataKey {string} The dictionary key which all file objects are assigned
   * @param fileKey {string} The dictionary key to get the file from each respective file object
   * @returns {Object}
   */
  getFileFormatForAjaxRequest (files, metaDataKey, dataKey, fileKey) {
    if (!Array.isArray(files)) {
      files = Object.values(files)
    }
    files = files.filter((file) => !this.isNil(file[fileKey]))
    return {
      [metaDataKey]: files.map((file) => {
        return Object.assign(
          this.omit(file, [fileKey]),
          { fileKey: this.isString(file[fileKey]) ? null : file[fileKey].name }
        )
      }),
      [dataKey]: files.map((file) => file[fileKey])
    }
  }

  getFileType (fileName) {
    if (!fileName) {
      return null
    }
    const [fileType] = fileName.split('.').slice(-1)
    return fileType
  }

  /**
   * This ensures Vue picks up changes (opposed to plain old assignment)
   * @param object: The object to be updated
   * @param newObjectData: The new object data. Any keys in the object that are not in newObjectData will be deleted
   */
  updateObjectInPlace (object, newObjectData) {
    Object.assign(object, newObjectData)

    // Make sure there aren't any keys that used to be present, but should be removed
    if (dataUtil.isObject(newObjectData) && dataUtil.isObject(object)) {
      const newKeys = Object.keys(newObjectData)
      Object.keys(object).forEach((key) => {
        if (!newKeys.includes(key)) {
          delete object[key]
        }
      })
    }
  }

  capitalize (string, isLowercaseRest = true) {
    if (!string) {
      return ''
    }
    const firstLetter = string.charAt(0).toUpperCase()
    let restOfString = string.slice(1)
    if (isLowercaseRest) {
      restOfString = restOfString.toLowerCase()
    }
    return firstLetter + restOfString
  }

  debounce (func, waitMS, immediate = false) {
    let timeout
    return () => {
      const args = arguments
      clearTimeout(timeout)
      timeout = setTimeout(function () {
        timeout = null
        if (!immediate) func.apply(this, args)
      }, waitMS)
      if (immediate && !timeout) func.apply(this, args)
    }
  }

  /**
   * Delete an item from an object using a relative path string
   * @param obj {Object}
   * @param path {String}: Use dot notation for nested variables
   */
  deleteFromPath (obj, path) {
    path = path.split('.')

    for (let i = 0; i < path.length - 1; i++) {
      obj = obj[path[i]]
      if (typeof obj === 'undefined') {
        return
      }
    }

    delete obj[path.pop()]
  }

  deepCopy (val) {
    return clone(val)
  }

  /**
   * Takes an array of objects and flattens them to an array of values based on the object key
   * @param objectArray: An array of objects
   * @param objectKey: The key to get the object value
   */
  flattenObjects (objectArray, objectKey) {
    if (!Array.isArray(objectArray)) {
      return objectArray
    }

    return objectArray.map((v) => this.get(v, objectKey))
  }

  get (obj, path, defaultValue = undefined) {
    const keyPath = path.split('.')
    let currentTarget = obj
    for (let i = 0; i < keyPath.length; i++) {
      currentTarget = currentTarget[keyPath[i]]
      if (this.isNil(currentTarget)) {
        return defaultValue
      }
    }
    return currentTarget
  }

  getFromArrayOrNone (array, idx) {
    if (!array) {
      return null
    }
    const val = array.slice(idx, idx + 1)
    return (val.length) ? val[0] : null
  }

  /**
   * Take a list of objects and return an object grouped by a key in each object
   * @param targetArray {Array}: Array of objects
   * @param key {String, Function}: Can be a key in each object or a function to compute a value from each object
   * @returns {*}
   */
  groupBy (targetArray, key) {
    return targetArray.reduce((groupedObj, obj) => {
      const keyVal = (this.isString(key)) ? obj[key] : key(obj)
      if (!groupedObj.get(keyVal)) {
        groupedObj[keyVal] = [obj]
      } else {
        groupedObj[keyVal].push(obj)
      }
      return groupedObj
    }, {})
  }

  isArraysEqual (a, b) {
    if (a === b) return true
    if (a === null || b === null) return false
    if (!Array.isArray(a) || !Array.isArray(b)) return false
    if (a.length !== b.length) return false

    // Copy before sorting so other elements aren't effected
    a = [...a]
    b = [...b]
    a.sort()
    a.sort()

    for (let i = 0; i < a.length; ++i) {
      if (a[i] !== b[i]) return false
    }
    return true
  }

  isEmpty (obj) {
    return [Object, Array].includes((obj || {}).constructor) && !Object.entries((obj || {})).length
  }

  isEmptyOrNil (val) {
    return this.isNil(val) || this.isEmpty(val)
  }

  isObject (val) {
    return (
      typeof val === 'object' &&
      !Array.isArray(val) &&
      val !== null
    )
  }

  isNil (val) {
    return val === undefined || val === null
  }

  isString (val) {
    return !this.isNil(val) && typeof val.valueOf() === 'string'
  }

  findTopVisibleElement (selector, pctTop = 0.7) {
    const viewportTop = window.scrollY
    const viewportBottom = viewportTop + window.innerHeight
    const viewportHeight = viewportBottom - viewportTop

    const visibleEls = document.querySelector(selector)
      .filter((idx, el) => {
        const elTop = el.scrollY
        const elBottom = elTop + document.getComputedStyle(el).height
        const isVisible = elBottom > viewportTop && elTop < viewportBottom
        if (!isVisible) {
          return false
        }

        const distFromTop = elTop - viewportTop
        return (distFromTop / viewportHeight) < pctTop
      })
      .map((idx, el) => {
        return { top: el.scrollY, el }
      })

    if (!visibleEls.length) {
      return null
    }
    this.sortBy(visibleEls, { key: 'top', direction: -1 }, true)
    return visibleEls[0].el
  }

  removeItemFromList (targetList, itemFindFn) {
    const listIdx = targetList.findIndex(itemFindFn)
    if (listIdx !== -1) {
      targetList.splice(listIdx, 1)
    }
  }

  /**
   * Returns a copied object with omitted properties removed. Does not mutate original object.
   * @param targetObject {Object}
   * @param omitList {Array}: Items in list can have relative paths using dot notation
   * @returns {*}
   */
  omit (targetObject, omitList) {
    const objCopy = this.deepCopy(targetObject)
    omitList.forEach((omission) => {
      this.deleteFromPath(objCopy, omission)
    })
    return objCopy
  }

  pick (object, keys) {
    return keys.reduce((obj, key) => {
      if (object && Object.prototype.hasOwnProperty.call(object, key)) {
        obj[key] = object[key]
      }
      return obj
    }, {})
  }

  sortBy (targetArray, sortKey, isInPlace = false) {
    const newArray = (isInPlace) ? targetArray : [...targetArray]
    const sortKeys = Array.isArray(sortKey) ? sortKey : [sortKey]
    sortKeys.reverse() // Reverse the order so the first item will be sorted last (making it primary)
    sortKeys.forEach((sortKey) => {
      // Deconstruct object if sort direction has been provided
      let direction = 1
      if (this.isObject(sortKey)) {
        direction = sortKey.direction
        sortKey = sortKey.key
      }
      let valGetter = (val) => this.get(val, sortKey)
      if (!this.isString(sortKey)) {
        valGetter = (val) => sortKey(val)
      }
      newArray.sort((a, b) => {
        if (valGetter(a) > valGetter(b)) {
          return direction
        }
        if (valGetter(b) > valGetter(a)) {
          return -direction
        }
        return 0
      })
    })
    return newArray
  }

  sum (vals) {
    if (!Array.isArray(vals)) {
      return vals
    }
    return vals.reduce((total, val) => {
      if (isNaN(val)) {
        if (val.includes('.')) {
          val = Number.parseFloat(val)
        } else {
          val = Number.parseInt(val)
        }
      }
      total += val
      return total
    }, 0)
  }

  truncateText (text, charCount, isWholeWord = true) {
    if (!text) {
      return ''
    }

    charCount = Math.min(charCount, text.length)
    let currentCharCount = 0
    let truncatedText = ''
    let endOfWord = false
    // eslint-disable-next-line no-unmodified-loop-condition
    while (currentCharCount < charCount && (!isWholeWord || endOfWord)) {
      truncatedText += text.slice(currentCharCount)
      endOfWord = (currentCharCount + 1 === charCount) || text.slice(currentCharCount + 1).match(/\s/)
      currentCharCount++
    }
    return truncatedText
  }

  uniqArray (array) {
    return array.filter((val, idx, arr) => {
      return arr.indexOf(val) === idx
    })
  }

  uniqWith (targetList, uniqFn) {
    return targetList.filter((el, idx) => targetList.findIndex((step) => uniqFn(el, step)) === idx)
  }

  uniqBy (targetList, uniqKey) {
    return this.uniqWith(targetList, (a, b) => this.get(a, uniqKey) === this.get(b, uniqKey))
  }
}

const dataUtil = new DataUtil()

export { dataUtil as default }
