<template>
  <DialogBase
    base-title-text="Login"
    :is-include-buttons="false"
  >
    <AuthAll
      :is-create="isCreate"
      :redirect-page-url="redirectPageUrl"
      :redirect-params="redirectParams"
      :user-type-bit="userTypeBit"
      :style-override="styleOverride"
    />
  </DialogBase>
</template>

<script>
import AuthAll from 'components/AuthAll.vue'
import DialogBase from 'components/dialogs/DialogBase.vue'

export default {
  name: 'DialogLogin',
  extends: DialogBase,
  inheritAttrs: false,
  components: { AuthAll, DialogBase },
  props: {
    isCreate: {
      type: Boolean,
      default: false
    },
    redirectPageUrl: {
      type: [String, null]
    },
    redirectParams: {
      type: [Object, null]
    },
    userTypeBit: {
      type: [Number, null]
    },
    styleOverride: {
      type: [Object, null]
    }
  },
  methods: {
    closeDialog () {
      this.$emit('ok')
      this.$emit('hide')
    }
  },
  mounted () {
    this.$global.$on('login', this.closeDialog.bind(this))
  }
}
</script>
