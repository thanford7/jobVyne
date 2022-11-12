<template>
  <div v-if="isLoaded" class="row">
    <div v-if="file && filePlacement === 'left'" class="col-4 q-pr-md">
      <video v-if="fileUtil.isVideo(file.url)" controls>
        <source :src="file.url">
      </video>
      <q-img v-if="fileUtil.isImage(file.url)" :src="file.url"/>
    </div>
    <div :class="(file) ? 'col-8' : 'col-12'">
      <div v-html="section.item_parts[0].html_content" :style="bodyStyle"/>
    </div>
    <div v-if="file && filePlacement === 'right'" class="col-4 q-pl-md">
      <video v-if="fileUtil.isVideo(file.url)" controls>
        <source :src="file.url">
      </video>
      <q-img v-if="fileUtil.isImage(file.url)" :src="file.url"/>
    </div>
  </div>
</template>

<script>
import sectionUtil from 'components/sections/sectionTypes.js'
import fileUtil from 'src/utils/file.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'TextSection',
  props: {
    section: Object,
    employerId: Number
  },
  data () {
    return {
      isLoaded: false,
      fileUtil
    }
  },
  computed: {
    bodyStyle () {
      return sectionUtil.getTextStyle(this.section)
    },
    file () {
      const files = this.employerStore.getEmployerFiles(this.employerId)
      const fileId = this.section.item_parts[0].file_id
      if (!fileId) {
        return null
      }
      return files.find((file) => file.id === fileId)
    },
    filePlacement () {
      return this.section.item_parts[0].file_placement
    }
  },
  async mounted () {
    await this.employerStore.setEmployerFiles(this.employerId)
    this.isLoaded = true
  },
  setup () {
    return {
      employerStore: useEmployerStore()
    }
  }
}
</script>
