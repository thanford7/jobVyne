<template>
  <q-select
    v-if="channels"
    filled emit-value map-options
    :label="label"
    :options="channels"
    option-label="name"
    option-value="key"
  >
    <template v-slot:after>
      <slot name="after"/>
    </template>
  </q-select>
</template>

<script>
import { useAuthStore } from 'stores/auth-store.js'
import { useSlackStore } from 'stores/slack-store.js'

export default {
  name: 'SelectSlackChannel',
  props: {
    label: {
      type: [String, null],
      default: 'Slack channel'
    }
  },
  data () {
    return {
      channels: null
    }
  },
  async mounted () {
    const authStore = useAuthStore()
    const slackStore = useSlackStore()
    await authStore.setUser()
    await slackStore.setChannels(authStore.propUser.employer_id)
    this.channels = slackStore.getChannels(authStore.propUser.employer_id)
  }
}
</script>
