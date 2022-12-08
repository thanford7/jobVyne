<template>
  <DialogBase
    base-title-text="Login"
    :is-include-buttons="false"
  >
    <AuthAll :redirect-page-url="redirectPageUrl" :redirect-params="redirectParams"/>
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
    redirectPageUrl: {
      type: [String, null]
    },
    redirectParams: {
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
