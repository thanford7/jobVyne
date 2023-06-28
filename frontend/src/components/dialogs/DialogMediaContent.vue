<template>
  <DialogBase
    :base-title-text="titleText"
    :primary-button-text="(!this.item.id) ? 'Create' : 'Update'"
    @ok="saveMedia"
  >
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'

export default {
  name: 'DialogMediaContent',
  extends: DialogBase,
  inheritAttrs: false,
  components: { DialogBase },
  props: {
    isVideo: {
      type: Boolean,
      default: false
    },
    item: {
      type: [Object, null],
      default: () => ({})
    }
  },
  computed: {
    titleText () {
      const action = (this.item.id) ? 'Edit' : 'Create'
      const item = (this.isVideo) ? 'video' : 'image'
      return `${action} ${item}`
    }
  },
  methods: {
    saveMedia () {
      this.$emit('ok')
    }
  }
}
</script>
