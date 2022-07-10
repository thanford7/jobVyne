<template>
  <router-view />
</template>

<script>
import { defineComponent } from 'vue'
import { useAjaxStore } from 'stores/ajax-store'
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
      const ajaxStore = useAjaxStore()
      ajaxStore.$on(AJAX_EVENTS.ERROR, (error) => {
        ajaxStore.addErrorMsg(error)
      })
      ajaxStore.$on(AJAX_EVENTS.SUCCESS, (msg) => {
        ajaxStore.addSuccessMsg(msg)
      })
      this.hasEventsLoaded = true
    }
  }
})
</script>
