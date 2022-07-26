<template>
  <q-select
    v-if="isLoaded"
    ref="select"
    filled use-chips multiple
    v-model="files"
    @update:model-value="$emit('update:model-value', $event)"
    :options="fileOptions"
    autocomplete="title"
    use-input
    @filter="filterFiles"
    option-value="id"
    option-label="title"
    :label="label"
  >
    <template v-slot:after>
      <slot name="after"/>
    </template>
  </q-select>
</template>

<script>
import { useEmployerStore } from 'stores/employer-store'
import { useAuthStore } from 'stores/auth-store'
import fileUtil, { FILE_TYPES } from 'src/utils/file'

export default {
  name: 'EmployerFilesSelector',
  props: {
    modelValue: {
      type: [Array, null]
    },
    fileTypeKeys: {
      type: [Array, null],
      default: () => Object.keys(FILE_TYPES)
    }
  },
  data () {
    return {
      isLoaded: false,
      files: [],
      filterTxt: null
    }
  },
  computed: {
    label () {
      return `Select ${fileUtil.getFileLabel(this.fileTypeKeys)}s`
    },
    fileOptions () {
      const allowedFiles = fileUtil.filterFilesByTypes(
        this.employerStore.getEmployerFiles(this.authStore.propUser.employer_id),
        this.fileTypeKeys
      )
      if (!this.filterTxt || this.filterTxt === '') {
        return allowedFiles
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return allowedFiles.filter((file) => {
        return (
          file.title.match(filterRegex) ||
          file.tags.some((tag) => tag.name.match(filterRegex))
        )
      })
    }
  },
  methods: {
    addFile (file) {
      this.$refs.select.add(file)
    },
    filterFiles (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    }
  },
  async mounted () {
    this.isLoaded = false
    await this.authStore.setUser().then(() => {
      return Promise.all([
        this.employerStore.setEmployerFiles(this.authStore.propUser.employer_id)
      ])
    })
    this.isLoaded = true
  },
  setup () {
    return {
      authStore: useAuthStore(),
      employerStore: useEmployerStore()
    }
  }
}
</script>
