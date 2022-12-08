<template>
  <div>
    <div v-if="isUpload">
      <slot name="fileInput"/>
    </div>
    <div v-else-if="fileUrl">
      <q-input
        filled
        readonly
        class="jv-existing-file"
        :model-value="fileUtil.getFileNameFromUrl(fileUrl)"
        :label="`Current ${label}`"
      >
        <template v-if="fileUtil.isImage(fileUrl)" v-slot:after>
          <img :src="fileUrl" alt="Sample view of image" style="max-height: 56px">
        </template>
      </q-input>
      <span class="text-small">
        <span class="text-gray-3">
          <q-icon name="file_download"/>&nbsp;
        </span>
        <a :href="fileUrl" class="no-decoration" target="_blank">
          {{ fileUtil.getFileNameFromUrl(fileUrl) }}
        </a>
      </span>
    </div>
    <div v-if="fileUrl && isAllowFileUpdate">
      <div class="q-gutter-sm">
        <q-radio v-model="isUpload" :val="true" :label="`Upload new ${label}`"/>
        <q-radio v-model="isUpload" :val="false" :label="`Use current ${label}`"/>
      </div>
    </div>
  </div>
</template>

<script>
import fileUtil from 'src/utils/file'

export default {
  name: 'FileDisplayOrUpload',
  props: {
    newFile: { // This should point to the value of the file input field in the fileInput slot
      type: [Object, null]
    },
    fileUrl: {
      type: [String, null]
    },
    newFileKey: {
      type: String
    },
    fileUrlKey: {
      type: String
    },
    label: {
      type: String
    },
    isAllowFileUpdate: {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      isUpload: true,
      fileUtil
    }
  },
  watch: {
    fileUrl () {
      this.isUpload = !this.fileUrl
    }
  },
  methods: {
    getValues () {
      return {
        [this.newFileKey]: (this.isUpload) ? this.newFile : null,
        [this.fileUrlKey]: (this.isUpload) ? null : this.fileUrl
      }
    }
  },
  mounted () {
    this.isUpload = !this.fileUrl
  }
}
</script>
