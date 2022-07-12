<template>
  <div>
    <div v-if="isUpload">
      <slot name="fileInput"/>
    </div>
    <div v-else-if="fileUrl">
      <q-input
        filled
        readonly
        :model-value="dataUtil.getFileNameFromUrl(fileUrl)"
        :label="`Current ${label}`"
      />
      <span class="text-small">
        <span class="text-gray-3">
          <q-icon name="file_download"/>&nbsp;
        </span>
        <a :href="fileUrl" class="no-decoration" target="_blank">
          {{ dataUtil.getFileNameFromUrl(fileUrl) }}
        </a>
      </span>
    </div>
    <div v-if="fileUrl">
      <div class="q-gutter-sm">
        <q-radio v-model="isUpload" :val="true" :label="`Upload new ${label}`"/>
        <q-radio v-model="isUpload" :val="false" :label="`Use current ${label}`"/>
      </div>
    </div>
  </div>
</template>

<script>
import dataUtil from 'src/utils/data'

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
    }
  },
  data () {
    return {
      isUpload: true,
      dataUtil
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
