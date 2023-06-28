<template>
  <div>
    <KarmaSidebar v-model="isLeftDrawerOpen" :user="user"/>
    <q-page-container>
      <q-page padding class="q-pa-md-lg q-pa-md">
        <KarmaHeader @toggleLeftDrawer="isLeftDrawerOpen = !isLeftDrawerOpen"/>
        <slot/>
      </q-page>
    </q-page-container>
  </div>
</template>

<script>
import KarmaHeader from 'pages/karma/KarmaHeader.vue'
import KarmaSidebar from 'pages/karma/KarmaSidebar.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { useMeta } from 'quasar'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'KarmaContainer',
  components: { KarmaHeader, KarmaSidebar },
  data () {
    return {
      isLeftDrawerOpen: true
    }
  },
  methods: {
    //
  },
  setup () {
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)

    useMeta(globalStore.getMetaCfg({
      pageTitle: 'Karma Connect',
      description: 'Do good while doing good'
    }))

    return {
      user,
      authStore
    }
  }
}
</script>
