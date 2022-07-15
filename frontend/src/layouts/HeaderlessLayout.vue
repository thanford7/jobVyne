<template>
  <q-layout view="hHh lpR fFf">

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script>

import { useAuthStore } from 'stores/auth-store'
import { Loading } from 'quasar'

export default {
  name: 'HeaderlessLayout',
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()
    return authStore.setUser().finally(() => Loading.hide())
  }
}
</script>
