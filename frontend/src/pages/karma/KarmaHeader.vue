<template>
  <PageHeader :is-include-logo="true" :is-include-sidebar-toggle="isLoggedIn">
    <template v-slot:title>
      <div class="self-center title">
        <h4 class="q-mb-none text-center">KARMA CONNECT</h4>
        <div class="text-center">Do Good While Doing Good</div>
      </div>
    </template>
  </PageHeader>
</template>

<script>
import dataUtil from 'src/utils/data.js'
import PageHeader from 'components/PageHeader.vue'
import { useAuthStore } from 'stores/auth-store.js'

export default {
  name: 'KarmaHeader',
  components: { PageHeader },
  data () {
    return {
      user: null
    }
  },
  computed: {
    isLoggedIn () {
      console.log(this.user)
      return Boolean(this.user || !dataUtil.isEmpty(this.user))
    }
  },
  async mounted () {
    const authStore = useAuthStore()
    await authStore.setUser()
    this.user = authStore.propUser
  }
}
</script>
