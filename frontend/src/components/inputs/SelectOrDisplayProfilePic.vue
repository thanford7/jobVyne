<template>
  <!-- eslint-disable vue/no-mutating-props */ -->
  <FileDisplayOrUpload
    ref="profileUpload"
    label="profile picture"
    :file-url="userData.profile_picture_url"
    :new-file="userData[newProfilePictureKey]"
    :new-file-key="newProfilePictureKey"
    file-url-key="profile_picture_url"
  >
    <template v-slot:fileInput>
      <q-file
        ref="newProfileUpload"
        filled bottom-slots clearable
        v-model="userData[newProfilePictureKey]"
        label="Profile picture"
        class="q-mb-none"
        :accept="fileUtil.getAllowedFileExtensionsStr([FILE_TYPES.IMAGE.key])"
        max-file-size="1000000"
      >
        <template v-slot:append>
          <q-icon name="cloud_upload"/>
        </template>
      </q-file>
    </template>
  </FileDisplayOrUpload>
</template>

<script>
import FileDisplayOrUpload from 'components/inputs/FileDisplayOrUpload.vue'
import fileUtil, { FILE_TYPES } from 'src/utils/file.js'

export default {
  name: 'SelectOrDisplayProfilePic',
  props: {
    userData: Object
  },
  components: { FileDisplayOrUpload },
  data () {
    return {
      newProfilePictureKey: 'profile_picture',
      fileUtil,
      FILE_TYPES
    }
  },
  methods: {
    getValues () {
      return this.$refs.profileUpload.getValues()
    }
  }
}
</script>
