<template>
  <q-select
    v-if="isLoaded"
    ref="select"
    filled use-chips
    :multiple="isMultiSelect"
    v-model="files"
    @update:model-value="emitModelValue"
    :options="fileOptions"
    autocomplete="title"
    use-input
    @filter="filterFiles"
    option-value="id"
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
      >{{ opt.title }}</q-chip>
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
    modelValue: {
      type: [Object, Array, null]
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
      files: null,
      filterTxt: null,
      fileUtil
    }
  },
  computed: {
    label () {
      return `Select ${fileUtil.getFileLabel(this.fileTypeKeys)}s`
    },
    fileOptions () {
      let allowedFiles = fileUtil.filterFilesByTypes(
        this.employerStore.getEmployerFiles(this.authStore.propUser.employer_id),
        this.fileTypeKeys,
        true
      ).map((v) => {
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
            v.isEmployer = false
            return v
          })
        ]
      }
      const groupFn = (this.isEmployer) ? (f) => dataUtil.capitalize(f.group) : (f) => `${dataUtil.capitalize(f.group)} ${(f.isEmployer) ? '(Employer)' : '(Yours)'}`
      allowedFiles = Object.entries(dataUtil.groupBy(allowedFiles, groupFn)).map(([fileGroup, files]) => {
        return {
          fileGroup,
          files
        }
      })
      dataUtil.sortBy(allowedFiles, 'fileGroup', true)
      if (!this.filterTxt || this.filterTxt === '') {
        return allowedFiles
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      allowedFiles.forEach((fileGroup) => {
        fileGroup.files = fileGroup.files.filter((file) => {
          return (
            file.title.match(filterRegex) ||
            (file.tags && file.tags.some((tag) => tag.name.match(filterRegex)))
          )
        })
      })
      return allowedFiles
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
    emitModelValue (value) {
      if (this.isEmitIdOnly) {
        value = (value && value.length) ? value.map(v => v.id) : value
      }
      this.$emit('update:model-value', value)
    },
    getOptionProps (itemProps) {
      return dataUtil.omit(itemProps, ['id', 'onClick', 'onMousemove'])
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
