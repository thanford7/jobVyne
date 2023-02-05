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
      this.$global.$on(AJAX_EVENTS.ERROR, ({ error, message }) => {
        if (error) {
          messagesUtil.parseAndAddErrorMsg(error)
        } else {
          messagesUtil.addErrorMsg(message)
        }
      })
      this.$global.$on(AJAX_EVENTS.WARNING, ({ message }) => {
        messagesUtil.addWarningMsg(message)
      })
      this.$global.$on(AJAX_EVENTS.SUCCESS, ({ message }) => {
        messagesUtil.addSuccessMsg(message)
      })
      this.hasEventsLoaded = true
    }
  }
})
</script>
