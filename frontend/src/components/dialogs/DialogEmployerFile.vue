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
      <FileTagsSelector v-model="formData.tags"/>
    </div>
  </DialogBase>
</template>

<script>
import fileUtil, { FILE_TYPES } from 'src/utils/file'
import DialogBase from 'components/dialogs/DialogBase.vue'
import FileDisplayOrUpload from 'components/inputs/FileDisplayOrUpload.vue'
import { useQuasar } from 'quasar'
import CustomTooltip from 'components/CustomTooltip.vue'
import { useEmployerStore } from 'stores/employer-store'
import { useAuthStore } from 'stores/auth-store'
import FileTagsSelector from 'components/inputs/FileTagsSelector.vue'
import { getAjaxFormData, openConfirmDialog } from 'src/utils/requests'

export const loadDialogEmployerFileDataFn = () => {
  const employerStore = useEmployerStore()
  const authStore = useAuthStore()
  return authStore.setUser().then(() => {
    return Promise.all([
      employerStore.setEmployerFiles(authStore.propUser.employer_id),
      employerStore.setEmployerFileTags(authStore.propUser.employer_id)
    ])
  })
}

export default {
  name: 'DialogEmployerFile',
  extends: DialogBase,
  inheritAttrs: false,
  components: { FileTagsSelector, CustomTooltip, FileDisplayOrUpload, DialogBase },
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
      const employerFiles = this.employerStore.getEmployerFiles(this.authStore.propUser.employer_id)
      return employerFiles.map((f) => fileUtil.getFileNameFromUrl(f.url))
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
      const employerId = this.authStore.propUser.employer_id
      const data = Object.assign(
        {},
        this.formData,
        this.$refs.fileUpload.getValues(),
        { employer_id: employerId }
      )
      const ajaxData = getAjaxFormData(data, [this.newFileKey])
      let resp
      if (!this.file) {
        resp = await this.$api.post('employer/file/', ajaxData)
      } else {
        resp = await this.$api.put(`employer/file/${this.file.id}`, ajaxData)
      }
      await Promise.all([
        this.employerStore.setEmployerFiles(employerId, true),
        this.employerStore.setEmployerFileTags(employerId, true)
      ])
      this.$emit('ok', resp.data.id)
    }
  },
  setup () {
    return {
      authStore: useAuthStore(),
      employerStore: useEmployerStore(),
      q: useQuasar()
    }
  }
}
</script>
