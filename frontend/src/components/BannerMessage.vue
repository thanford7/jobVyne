<template>
  <div>
    <div v-for="msg in ajaxStore.messages" class="q-pa-md q-gutter-sm">
      <q-banner inline-actions rounded :class="msg.classStr">
        {{ msg.msg }}

        <template v-slot:action>
          <q-btn flat label="Dismiss" @click="ajaxStore.removeMsg(msg.idx)"/>
        </template>
      </q-banner>
    </div>
  </div>
</template>

<script>
import { useAjaxStore } from 'stores/ajax-store'

export default {
  name: 'BannerMessage',
  setup () {
    const ajaxStore = useAjaxStore()
    return { ajaxStore }
  }
}
</script>
