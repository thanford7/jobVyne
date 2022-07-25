<template>
  <DialogBase
    :title-text="titleText"
    :primary-button-text="(!this.file) ? 'Create' : 'Update'"
    @ok="confirmAndSaveFile"
  >
    <div class="q-gutter-y-md">
      <FileDisplayOrUpload
        ref="fileUpload"
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
            @rejected="onFileRejected"
            filled
          >
            <template v-slot:append>
              <CustomTooltip>
                Supported file types: {{ allowedFileExtensionsStr }}
              </CustomTooltip>
            </template>
          </q-file>
        </template>
      </FileDisplayOrUpload>
      <q-input filled borderless v-model="formData.title" label="File title (optional)">
        <template v-slot:append>
          <CustomTooltip>
            If empty, the uploaded file name will be used
          </CustomTooltip>
        </template>
      </q-input>
      <EmployerFileTagsSelector v-model="formData.tags"/>
    </div>
  </DialogBase>
</template>

<script>
import { FILE_TYPES } from 'src/utils/form'
import DialogBase from 'components/dialogs/DialogBase.vue'
import FileDisplayOrUpload from 'components/inputs/FileDisplayOrUpload.vue'
import { Loading, useQuasar } from 'quasar'
import CustomTooltip from 'components/CustomTooltip.vue'
import { useEmployerStore } from 'stores/employer-store'
import { useAuthStore } from 'stores/auth-store'
import EmployerFileTagsSelector from 'components/inputs/EmployerFileTagsSelector.vue'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests'
import dataUtil from 'src/utils/data'

export default {
  name: 'DialogEmployerFile',
  extends: DialogBase,
  inheritAttrs: false,
  components: { EmployerFileTagsSelector, CustomTooltip, FileDisplayOrUpload, DialogBase },
  props: {
    file: {
      type: [Object, null]
    },
    fileTypeKeys: {
      type: [Array, null],
      default: () => [FILE_TYPES.FILE.key, FILE_TYPES.VIDEO.key, FILE_TYPES.IMAGE.key]
    }
  },
  computed: {
    fileLabel () {
      if (this.fileTypeKeys.length > 1) {
        return 'file'
      }
      return FILE_TYPES[this.fileTypeKeys[0]].title
    },
    titleText () {
      if (!this.file) {
        return `Create new ${this.fileLabel}`
      }
      return `Update ${this.fileLabel}`
    },
    allowedFileExtensions () {
      return this.fileTypeKeys.reduce((allExtensions, fileTypeKey) => {
        allExtensions = [...allExtensions, ...FILE_TYPES[fileTypeKey].allowedExtensions]
        return allExtensions
      }, [])
    },
    allowedFileExtensionsStr () {
      return this.allowedFileExtensions.map((ext) => `.${ext}`).join(', ')
    },
    currentFileNames () {
      const employerFiles = this.employerStore.getEmployerFiles(this.authStore.propUser.employer_id)
      return employerFiles.map((f) => dataUtil.getFileNameFromUrl(f.url))
    }
  },
  data () {
    return {
      formData: {
        title: null,
        tags: null,
        file: null,
        file_url: null
      },
      newFileKey: 'file'
    }
  },
  methods: {
    onFileRejected (rejectedFile) {
      this.$q.notify({
        type: 'negative',
        message: 'This file extension type is not supported'
      })
    },
    async confirmAndSaveFile () {
      const newFile = this.$refs.fileUpload.getValues()[this.newFileKey]
      if (newFile && this.currentFileNames.includes(newFile.name)) {
        openConfirmDialog(
          this.$q,
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
      const employerId = this.authStore.propUser.employer_id
      const data = Object.assign(
        {},
        this.formData,
        this.$refs.fileUpload.getValues(),
        { employer_id: employerId }
      )
      const ajaxData = getAjaxFormData(data, [this.newFileKey])
      if (!this.file) {
        await this.$api.post('employer/file/', ajaxData)
      } else {
        await this.$api.put(`employer/file/${this.file.id}`, ajaxData)
      }
      await Promise.all([
        this.employerStore.setEmployerFiles(employerId, true),
        this.employerStore.setEmployerFileTags(employerId, true)
      ])
    }
  },
  preFetch () {
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployerFiles(authStore.propUser.employer_id),
        employerStore.setEmployerFileTags(authStore.propUser.employer_id)
      ])
    }).finally(() => Loading.hide())
  },
  setup () {
    return {
      authStore: useAuthStore(),
      employerStore: useEmployerStore(),
      $q: useQuasar()
    }
  }
}
</script>
