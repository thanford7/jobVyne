<template>
  <q-select
    v-if="isLoaded"
    ref="select"
    :model-value="selectedFiles"
    @update:model-value="emitFiles"
    filled use-chips
    :multiple="isMultiSelect"
    :options="fileOptions"
    autocomplete="title"
    use-input
    @filter="filterFiles"
    option-value="compositeId"
    option-label="title"
    :label="label"
  >
    <template v-slot:option="{ itemProps, opt, selected, toggleOption }">
      <q-expansion-item
        expand-separator
        :default-opened="true"
        header-class="text-bold"
        :label="opt.fileGroup"
      >
        <q-item
          v-for="file in opt.files"
          v-bind="getOptionProps(itemProps)"
          :active="selected"
          class="bg-hover"
          @click="toggleOption(file)"
        >
          <q-item-section>
            <div class="flex w-100 items-center">
              <div
                v-if="fileUtil.isImage(file.url)"
                style="width: 80px;"
                class="q-mr-sm"
              >
                <img
                  :src="file.url" :alt="file.title"
                  style="max-height: 32px;"
                >
              </div>
              <div
                v-if="fileUtil.isVideo(file.url)"
                style="width: 80px;"
                class="q-mr-sm"
              >
                <video
                  height="32"
                >
                  <source :src="file.url">
                </video>
              </div>
              {{ file.title }}
            </div>
          </q-item-section>
        </q-item>
      </q-expansion-item>
    </template>
    <template v-slot:selected-item="{ opt, removeAtIndex, tabindex, index }">
      <q-chip
        removable
        @remove="removeAtIndex(index)"
        :tabindex="tabindex"
      >{{ opt.title }}
      </q-chip>
    </template>
    <template v-slot:after>
      <slot name="after"/>
    </template>
  </q-select>
</template>

<script>
import dataUtil from 'src/utils/data.js'
import { useContentStore } from 'stores/content-store.js'
import { useEmployerStore } from 'stores/employer-store'
import { useAuthStore } from 'stores/auth-store'
import fileUtil, { FILE_TYPES } from 'src/utils/file'

export default {
  name: 'SelectFiles',
  props: {
    employerFileIds: {
      type: [Array, Object, Number, null]
    },
    userFileIds: {
      type: [Array, Object, Number, null]
    },
    isEmitIdOnly: {
      type: Boolean,
      default: false
    },
    fileTypeKeys: {
      type: [Array, null],
      default: () => Object.keys(FILE_TYPES)
    },
    isMultiSelect: {
      type: Boolean,
      default: false
    },
    isEmployer: Boolean
  },
  data () {
    return {
      isLoaded: false,
      filterTxt: null,
      fileUtil
    }
  },
  computed: {
    label () {
      return `Select ${fileUtil.getFileLabel(this.fileTypeKeys)}s`
    },
    selectedFiles () {
      const normalizedEmployerFileIds = this.normalizeFileIds(this.employerFileIds)
      const normalizedUserFileIds = this.normalizeFileIds(this.userFileIds)
      if (!this.isMultiSelect) {
        if (normalizedEmployerFileIds) {
          return this.getFileFromId(normalizedEmployerFileIds, true)
        } else if (normalizedUserFileIds) {
          return this.getFileFromId(normalizedUserFileIds, false)
        } else {
          return null
        }
      }
      const files = []
      dataUtil.getForceArray(normalizedEmployerFileIds).forEach((id) => {
        files.push(this.getFileFromId(id, true))
      })
      dataUtil.getForceArray(normalizedUserFileIds).forEach((id) => {
        files.push(this.getFileFromId(id, false))
      })
      return files
    },
    allowedFiles () {
      let allowedFiles = fileUtil.filterFilesByTypes(
        this.employerStore.getEmployerFiles(this.authStore.propUser.employer_id),
        this.fileTypeKeys,
        true
      ).map((v) => {
        v.compositeId = this.getCompositeId(v.id, true)
        v.isEmployer = true
        return v
      })
      if (!this.isEmployer) {
        allowedFiles = [
          ...allowedFiles,
          ...fileUtil.filterFilesByTypes(
            this.contentStore.getUserFiles(this.authStore.propUser.id),
            this.fileTypeKeys,
            true
          ).map((v) => {
            v.compositeId = this.getCompositeId(v.id, false)
            v.isEmployer = false
            return v
          })
        ]
      }
      return allowedFiles
    },
    groupedFiles () {
      const groupFn = (this.isEmployer) ? (f) => dataUtil.capitalize(f.group) : (f) => `${dataUtil.capitalize(f.group)} ${(f.isEmployer) ? '(Employer)' : '(Yours)'}`
      const groupedFiles = Object.entries(dataUtil.groupBy(this.allowedFiles, groupFn)).map(([fileGroup, files]) => {
        return {
          fileGroup,
          files
        }
      })
      dataUtil.sortBy(groupedFiles, 'fileGroup', true)
      return groupedFiles
    },
    fileOptions () {
      const files = dataUtil.deepCopy(this.groupedFiles)
      if (!this.filterTxt || this.filterTxt === '') {
        return files
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      files.forEach((fileGroup) => {
        fileGroup.files = fileGroup.files.filter((file) => {
          return (
            file.title.match(filterRegex) ||
            (file.tags && file.tags.some((tag) => tag.name.match(filterRegex)))
          )
        })
      })
      return files
    }
  },
  methods: {
    async updateFiles () {
      await Promise.all([
        this.employerStore.setEmployerFiles(this.authStore.propUser.employer_id),
        this.contentStore.setUserFiles(this.authStore.propUser.id)
      ])
    },
    filterFiles (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    },
    getCompositeId (id, isEmployerFile) {
      return (isEmployerFile) ? `employer-${id}` : `user-${id}`
    },
    getFileFromId (id, isEmployerFile) {
      const compositeId = this.getCompositeId(id, isEmployerFile)
      return this.allowedFiles.find((f) => f.compositeId === compositeId)
    },
    getOptionProps (itemProps) {
      return dataUtil.omit(itemProps, ['id', 'onClick', 'onMousemove'])
    },
    emitFiles (files) {
      if (!files) {
        this.$emit('update:employer-file-ids', null)
        this.$emit('update:user-file-ids', null)
        return
      }
      if (!this.isMultiSelect) {
        if (files.isEmployer) {
          this.$emit('update:employer-file-ids', (this.isEmitIdOnly) ? files.id : files)
          this.$emit('update:user-file-ids', null)
        } else {
          this.$emit('update:employer-file-ids', null)
          this.$emit('update:user-file-ids', (this.isEmitIdOnly) ? files.id : files)
        }
        return
      }
      const employerFiles = files.filter((f) => f.isEmployer).map((f) => (this.isEmitIdOnly) ? f.id : f)
      const userFiles = files.filter((f) => !f.isEmployer).map((f) => (this.isEmitIdOnly) ? f.id : f)
      this.$emit('update:employer-file-ids', employerFiles)
      this.$emit('update:user-file-ids', userFiles)
    },
    normalizeFileIds (fileIds) {
      if (!fileIds || Number.isInteger(fileIds)) {
        return fileIds
      } else if (Array.isArray(fileIds)) {
        return fileIds.map((f) => (dataUtil.isObject(f)) ? f.id : f)
      } else {
        return fileIds.id
      }
    }
  },
  async mounted () {
    this.isLoaded = false
    await this.authStore.setUser().then(() => {
      return Promise.all([
        this.employerStore.setEmployerFiles(this.authStore.propUser.employer_id),
        this.contentStore.setUserFiles(this.authStore.propUser.id)
      ])
    })
    this.isLoaded = true
  },
  setup () {
    return {
      authStore: useAuthStore(),
      contentStore: useContentStore(),
      employerStore: useEmployerStore()
    }
  }
}
</script>
