<template>
  <DialogBase
    primary-button-text="Login"
    title-text="Login"
  >
    <AuthAll/>
  </DialogBase>
</template>

<script>
import AuthAll from 'components/AuthAll.vue'
import DialogBase from 'components/DialogBase.vue'

export default {
  name: 'DialogLogin',
  extends: DialogBase,
  inheritAttrs: false,
  components: { AuthAll, DialogBase }
}
</script>
