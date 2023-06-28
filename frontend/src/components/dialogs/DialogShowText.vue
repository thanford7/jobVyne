<template>
  <DialogBase
    :base-title-text="title"
    :is-include-buttons="false"
    width="700px"
  >
    <div v-if="isHtml" v-html="text"/>
    <div v-else>
      {{ text }}
    </div>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'

export default {
  name: 'DialogShowText',
  components: { DialogBase },
  props: {
    isHtml: {
      type: Boolean,
      default: false
    },
    text: String,
    title: String
  }
}
</script>
