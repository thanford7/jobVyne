import { useUtilStore } from 'stores/utility-store'
import clone from 'just-clone'
import pluralize from 'pluralize'

class DataUtil {
  formatCurrency (val, currencyCfg = {}) {
    const formatCfg = Object.assign({
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0, // (this suffices for whole numbers, but will print 2500.10 as $2,500.1)
      maximumFractionDigits: 0 // (causes 2500.99 to be printed as $2,501)
    }, currencyCfg)

    if (!formatCfg.currency) {
      formatCfg.currency = 'USD'
    }

    const formatter = new Intl.NumberFormat('en-US', formatCfg)

    return formatter.format(val)
  }

  getSalaryRange (salaryFloor, salaryCeiling) {
    if (!salaryFloor && !salaryCeiling) {
      return null
    }
    if (salaryFloor && salaryCeiling) {
      return `${this.formatCurrency(salaryFloor)}-${this.formatCurrency(salaryCeiling)}`
    }
    if (salaryFloor) {
      return this.formatCurrency(salaryFloor)
    }
    return this.formatCurrency(salaryCeiling)
  }

  getBitsFromList (bitList) {
    if (!Array.isArray(bitList)) {
      return bitList
    }
    return bitList.reduce((allBits, bit) => {
      allBits |= bit
      return allBits
    }, 0)
  }

  getBoolean (val) {
    return Boolean(val)
  }

  getFullName (firstName, lastName) {
    if (!firstName && !lastName) {
      return null
    } else if (firstName && !lastName) {
      return firstName
    } else if (!firstName && lastName) {
      return lastName
    } else {
      return `${firstName} ${lastName}`
    }
  }

  roundTo (number, roundNumber) {
    return Math.ceil(number / roundNumber) * roundNumber
  }

  copyText (e) {
    const utilStore = useUtilStore()
    const targetEl = e.currentTarget
    const copyTargetEl = targetEl.closest('div').querySelector('.copy-target')
    const text = copyTargetEl.innerText || copyTargetEl.value
    const copyMsgId = utilStore.getNewElId()
    navigator.clipboard.writeText(text).then(
      () => {
        targetEl.parentNode.insertAdjacentHTML(
          'beforeend',
          `<span id="${copyMsgId}" class="text-positive text-small"> Copied successfully</span>`
        )
      }, () => {
        targetEl.parentNode.insertAdjacentHTML(
          'beforeend',
          `<span id="${copyMsgId}" class="text-negative text-small"> Copy failed. Please copy manually</span>`
        )
      }
    )
    setTimeout(() => {
      document.getElementById(copyMsgId).remove()
    }, 3000)
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

  /**
   * Get a modified URL string
   * @param isExcludeExistingParams {Boolean}: If true, remove all existing params
   * @param addParams {Array}: Params to add [{key: <param key>, val: <param val> || [<param val>...]},...]
   * @param deleteParams {Array|null}: Param keys to remove
   * @param path {String|null}: redirect path
   * @returns {string}
   */
  getUrlWithParams ({ isExcludeExistingParams = false, addParams = null, deleteParams = null, path = null }) {
    if (!('URLSearchParams' in window)) {
      return
    }
    const searchParams = (isExcludeExistingParams) ? new URLSearchParams() : new URLSearchParams(window.location.search)

    this.getForceArray(deleteParams).forEach((paramKey) => searchParams.delete(paramKey))
    this.getForceArray(addParams).forEach(({ key, val }) => {
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
   * Removes query params in place to avoid rearranging the params
   * @param url {String}: Full url including base and query params
   * @param paramsToRemove {Array}: List of param keys to remove
   * @returns {string|*}
   */
  removeQueryParams (url, paramsToRemove) {
    const urlParts = url.split('?')
    // No query params
    if (urlParts.length === 1) {
      return url
    }
    const queryStr = urlParts[1].split('&').reduce((totalQueryStr, queryParam) => {
      const [queryKey, queryValue] = queryParam.split('=')
      if (paramsToRemove.includes(queryKey)) {
        return totalQueryStr
      }
      const queryStr = queryKey + '=' + queryValue
      if (!totalQueryStr.length) {
        totalQueryStr = queryStr
      } else {
        totalQueryStr += '&' + queryStr
      }
      return totalQueryStr
    }, '')

    return (queryStr.length) ? urlParts[0] + '?' + queryStr : urlParts[0]
  }

  /**
   * Update query params and optionally redirect to a new page
   * See getUrlWithParams for argument definitions
   */
  setQueryParams ({ isExcludeExistingParams = false, addParams = null, deleteParams = null, path = null }) {
    const newRelativePathQuery = this.getUrlWithParams(
      { isExcludeExistingParams, addParams, deleteParams, path }
    )
    if (!newRelativePathQuery) {
      return
    }
    if (path) {
      window.location.href = newRelativePathQuery // Redirect to new page
    } else {
      history.pushState(null, '', newRelativePathQuery) // Add to view state
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

  concatWithAnd (list) {
    if (!list || !list.length) {
      return null
    }
    if (list.length === 1) {
      return list[0]
    }
    if (list.length === 2) {
      return list[0] + ' and ' + list[1]
    }

    return list.reduce((text, item, idx) => {
      if (idx === 0) {
        text = item
      } else if (idx !== list.length - 1) {
        text += ', ' + item
      } else {
        text += ', and ' + item
      }
      return text
    }, '')
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

  getForceArray (val) {
    if (Array.isArray(val)) {
      return val
    }
    return []
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

  getArrayIntersection (array1, array2) {
    if (!array1 || !array2) {
      return []
    }
    return array1.filter(value => array2.includes(value))
  }

  getArrayWithValuesOrNone (array) {
    if (!array || !array.length) {
      return null
    }
    return array
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
      if (!groupedObj[keyVal]) {
        groupedObj[keyVal] = [obj]
      } else {
        groupedObj[keyVal].push(obj)
      }
      return groupedObj
    }, {})
  }

  isBetween (number, lowerBound, upperBound) {
    return number >= lowerBound && number <= upperBound
  }

  isArraysEqual (a, b, isCheckOrder = false) {
    if (a === b) return true
    if (a === null || b === null) return false
    if (!Array.isArray(a) || !Array.isArray(b)) return false
    if (a.length !== b.length) return false

    // Copy before sorting so other elements aren't effected
    a = [...a]
    b = [...b]

    if (!isCheckOrder) {
      a.sort()
      b.sort()
    }

    for (let i = 0; i < a.length; ++i) {
      if (a[i] !== b[i]) return false
    }
    return true
  }

  isDeepEqual (a, b) {
    return JSON.stringify(a) === JSON.stringify(b)
  }

  isEmpty (obj) {
    return [Object, Array].includes((obj || {}).constructor) && !Object.entries((obj || {})).length
  }

  isEmptyOrNil (val) {
    return this.isNil(val) || this.isEmpty(val) || (val instanceof String && !val.length)
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

  mergeDeep (target, ...sources) {
    if (!sources.length) return target
    const source = sources.shift()

    if (this.isObject(target) && this.isObject(source)) {
      for (const key in source) {
        if (this.isObject(source[key])) {
          if (!target[key]) Object.assign(target, { [key]: {} })
          this.mergeDeep(target[key], source[key])
        } else {
          Object.assign(target, { [key]: source[key] })
        }
      }
    }

    return this.mergeDeep(target, ...sources)
  }

  /**
   * @param targetList: The list that the item should be removed from
   * @param itemFindFn: (Optional) The function to find the item.
   * @param listIdx: (Optional) The index of the item to be removed.
   */
  removeItemFromList (targetList, { itemFindFn, listIdx }) {
    listIdx = this.isNil(listIdx) ? targetList.findIndex(itemFindFn) : listIdx
    let item = null
    if (listIdx !== -1) {
      item = targetList[listIdx]
      targetList.splice(listIdx, 1)
    }
    return item
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

  pluralize (word, count, includeWord = true) {
    return pluralize(word, count, includeWord)
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

  truncateText (text, charCount, { isWholeWord = true, truncateChar = '...' } = {}) {
    if (!text) {
      return ''
    }

    charCount = Math.min(charCount, text.length)
    let currentCharCount = 0
    let truncatedText = ''
    let endOfWord = false
    // eslint-disable-next-line no-unmodified-loop-condition
    while (currentCharCount < charCount || (isWholeWord && !endOfWord)) {
      truncatedText = text.slice(0, currentCharCount + 1)
      endOfWord = currentCharCount === text.length || text.slice(currentCharCount + 1, currentCharCount + 2).match(/\s/)
      currentCharCount++
    }
    if (truncatedText.length < text.length) {
      truncatedText = truncatedText + truncateChar
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
