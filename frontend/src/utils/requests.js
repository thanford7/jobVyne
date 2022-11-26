import dataUtil from 'src/utils/data'

/**
 * Transforms an object into form data. Splits media data (files, images, videos) into separate fields so they
 * can be processed differently
 * @param data {Object}
 * @param mediaFields {Array}
 * @returns {FormData}
 */
export const getAjaxFormData = (data, mediaFields = null) => {
  const ajaxData = new FormData()
  mediaFields = mediaFields || []
  ajaxData.append('data', JSON.stringify(dataUtil.omit(data, mediaFields)))
  mediaFields.forEach((field) => {
    const val = dataUtil.get(data, field)
    if (!val) {
      return
    }
    const finalField = field.split('.').reduce((finalField, fieldPart, idx) => {
      if (idx !== 0) {
        fieldPart = dataUtil.capitalize(fieldPart, false)
      }
      return finalField + fieldPart
    }, '') // If field uses dot notation, we need to use the last subfield
    if (Array.isArray(val)) {
      val.forEach((file) => {
        ajaxData.append(finalField, file)
      })
    } else {
      ajaxData.append(finalField, val)
    }
  })
  return ajaxData
}

export const openDialog = ($q, title, message, { isCancel = false, okFn, cancelFn, dismissFn } = {}) => {
  return $q.dialog({
    title,
    message,
    cancel: isCancel,
    persistent: true
  }).onOk(() => {
    if (okFn) {
      okFn()
    }
  }).onCancel(() => {
    if (cancelFn) {
      cancelFn()
    }
  }).onDismiss(() => {
    // triggered on both OK and Cancel
    if (dismissFn) {
      dismissFn()
    }
  })
}

export const openConfirmDialog = ($q, message, { okFn, cancelFn, dismissFn }) => {
  return openDialog($q, 'Confirm', message,
    { isCancel: true, okFn, cancelFn, dismissFn }
  )
}

/**
 * ~assets doesn't work when assigned to a variable so this function can be used to get the appropriate path
 * @param relativePath {String}: The path from the assets folder, starting with the forward slash
 * @returns {string}
 */
export const getAssetsPath = (relativePath) => {
  return process.env.ASSETS_PATH + relativePath
}
