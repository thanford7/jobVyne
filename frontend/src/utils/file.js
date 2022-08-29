import dataUtil from 'src/utils/data'

export const FILE_TYPES = {
  VIDEO: {
    key: 'VIDEO',
    title: 'video',
    allowedExtensions: ['mp4', 'm4v', 'mov', 'wmv', 'avi', 'mpg', 'webm']
  },
  IMAGE: {
    key: 'IMAGE',
    title: 'image',
    allowedExtensions: ['png', 'jpeg', 'jpg', 'gif']
  },
  FILE: {
    key: 'FILE',
    title: 'file',
    allowedExtensions: ['doc', 'docx', 'pdf', 'txt', 'rtf']
  }
}

class FileUtil {
  getAllowedFileExtensions (fileTypeKeys) {
    return fileTypeKeys.reduce((allExtensions, fileTypeKey) => {
      allExtensions = [...allExtensions, ...FILE_TYPES[fileTypeKey].allowedExtensions]
      return allExtensions
    }, [])
  }

  getAllowedFileExtensionsStr (fileTypeKeys) {
    return this.getAllowedFileExtensions(fileTypeKeys).map((ext) => `.${ext}`).join(', ')
  }

  getFileNameFromUrl (fileUrl) {
    if (!fileUrl) {
      return null
    }
    const [fileName] = fileUrl.split('/').slice(-1)
    return fileName
  }

  getFileLabel (fileTypeKeys) {
    if (fileTypeKeys.length > 1) {
      return 'file'
    }
    return FILE_TYPES[fileTypeKeys[0]].title
  }

  getFileType (fileName) {
    if (!fileName) {
      return null
    }
    const [fileType] = fileName.split('.').slice(-1)
    return fileType
  }

  getFileGroup (fileName) {
    if (this.isImage(fileName)) {
      return FILE_TYPES.IMAGE.key
    } else if (this.isVideo(fileName)) {
      return FILE_TYPES.VIDEO.key
    }
    return FILE_TYPES.FILE.key
  }

  isImage (fileName) {
    const fileType = this.getFileType(fileName)
    return FILE_TYPES.IMAGE.allowedExtensions.includes(fileType)
  }

  isVideo (fileName) {
    const fileType = this.getFileType(fileName)
    return FILE_TYPES.VIDEO.allowedExtensions.includes(fileType)
  }

  isFile (fileName) {
    const fileType = this.getFileType(fileName)
    return FILE_TYPES.FILE.allowedExtensions.includes(fileType)
  }

  filterFilesByTypes (files, fileTypeKeys, isAddFileGroup = false) {
    // No need to filter if all file types are allowed
    if (dataUtil.isArraysEqual(fileTypeKeys, Object.keys(FILE_TYPES)) && !isAddFileGroup) {
      return files
    }
    const allowedExtensions = this.getAllowedFileExtensions(fileTypeKeys)
    return (files || []).filter((file) => {
      const fileExt = this.getFileType(file.url)
      if (isAddFileGroup) {
        file.group = this.getFileGroup(file.url)
      }
      return allowedExtensions.includes(fileExt)
    })
  }
}

const fileUtil = new FileUtil()

export default fileUtil
