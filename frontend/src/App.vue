<template>
  <router-view />
</template>

<script>
import messagesUtil from 'src/utils/messages.js'
import { defineComponent } from 'vue'
import { AJAX_EVENTS } from 'boot/axios'

export default defineComponent({
  name: 'App',
  data () {
    return {
      hasEventsLoaded: false
    }
  },
  mounted () {
    if (!this.hasEventsLoaded) {
      this.$global.$on(AJAX_EVENTS.ERROR, (error) => {
        messagesUtil.addErrorMsg(error)
      })
      this.$global.$on(AJAX_EVENTS.SUCCESS, (msg) => {
        messagesUtil.addSuccessMsg(msg)
      })
      this.hasEventsLoaded = true
    }
  }
})
</script>
