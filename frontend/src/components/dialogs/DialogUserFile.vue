<template>
  <DialogBase
    :base-title-text="titleText"
    :primary-button-text="(!this.file) ? 'Create' : 'Update'"
    @ok="confirmAndSaveFile"
  >
    <div class="q-gutter-y-md">
      <FileDisplayOrUpload
        ref="fileUpload"
        :is-allow-file-update="false"
        :label="fileLabel"
        :new-file="formData.file"
        :file-url="file?.url"
        :new-file-key="newFileKey"
        file-url-key="file_url"
      >
        <template v-slot:fileInput>
          <q-file
            v-model="formData.file"
            label="Pick file"
            :accept="allowedFileExtensionsStr"
            filled
          >
            <template v-slot:append>
              <CustomTooltip :is_include_space="true">
                Supported file types: {{ allowedFileExtensionsStr }}
              </CustomTooltip>
            </template>
          </q-file>
        </template>
      </FileDisplayOrUpload>
      <q-input filled borderless v-model="formData.title" label="File title (optional)">
        <template v-slot:append>
          <CustomTooltip :is_include_space="true">
            If empty, the uploaded file name will be used
          </CustomTooltip>
        </template>
      </q-input>
    </div>
  </DialogBase>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'
import FileDisplayOrUpload from 'components/inputs/FileDisplayOrUpload.vue'
import { useQuasar } from 'quasar'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useContentStore } from 'stores/content-store.js'

export const loadDialogUserFileDataFn = () => {
  const contentStore = useContentStore()
  const authStore = useAuthStore()
  return authStore.setUser().then(() => {
    return Promise.all([
      contentStore.setUserFiles(authStore.propUser.id)
    ])
  })
}

export default {
  name: 'DialogUserFile',
  extends: DialogBase,
  inheritAttrs: false,
  components: { CustomTooltip, FileDisplayOrUpload, DialogBase },
  props: {
    file: {
      type: [Object, null]
    },
    fileTypeKeys: {
      type: [Array, null],
      default: () => Object.keys(FILE_TYPES)
    }
  },
  computed: {
    fileLabel () {
      return fileUtil.getFileLabel(this.fileTypeKeys)
    },
    titleText () {
      if (!this.file) {
        return `Create new ${this.fileLabel}`
      }
      return `Update ${this.fileLabel}`
    },
    allowedFileExtensions () {
      return fileUtil.getAllowedFileExtensions(this.fileTypeKeys)
    },
    allowedFileExtensionsStr () {
      return fileUtil.getAllowedFileExtensionsStr(this.fileTypeKeys)
    },
    currentFileNames () {
      const userFiles = this.contentStore.getUserFiles(this.authStore.propUser.id)
      return userFiles.map((f) => fileUtil.getFileNameFromUrl(f.url))
    }
  },
  data () {
    return {
      formData: {
        title: null,
        file: null,
        file_url: null
      },
      newFileKey: 'file'
    }
  },
  methods: {
    async confirmAndSaveFile () {
      const newFile = this.$refs.fileUpload.getValues()[this.newFileKey]
      if (newFile && this.currentFileNames.includes(newFile.name)) {
        openConfirmDialog(
          this.q,
          `A file named ${newFile.name} already exists. Do you want to proceed and overwrite the existing file?`,
          {
            okFn: async () => {
              await this.saveFile()
            }
          }
        )
      } else {
        await this.saveFile()
      }
    },
    async saveFile () {
      const userId = this.authStore.propUser.id
      const data = Object.assign(
        {},
        this.formData,
        this.$refs.fileUpload.getValues(),
        { user_id: userId }
      )
      const ajaxData = getAjaxFormData(data, [this.newFileKey])
      if (!this.file) {
        await this.$api.post('user/file/', ajaxData)
      } else {
        await this.$api.put(`user/file/${this.file.id}`, ajaxData)
      }
      await Promise.all([
        this.contentStore.setUserFiles(userId, true)
      ])
      this.$emit('ok')
    }
  },
  setup () {
    return {
      authStore: useAuthStore(),
      contentStore: useContentStore(),
      q: useQuasar()
    }
  }
}
</script>
