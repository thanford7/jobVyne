<template>
  <div>
    <div v-for="msg in messages" class="q-pa-md q-gutter-sm">
      <q-banner inline-actions rounded :class="msg.classStr">
        {{ msg.msg }}

        <template v-slot:action>
          <q-btn flat label="Dismiss" @click="removeMsg(msg.idx)"/>
        </template>
      </q-banner>
    </div>
  </div>
</template>

<script>

export default {
  name: 'BannerMessage',
  data () {
    return {
      messages: []
    }
  },
  methods: {
    removeMsg (msgIdx) {
      this.messages.splice(msgIdx, 1)
    }
  }
}
</script>
