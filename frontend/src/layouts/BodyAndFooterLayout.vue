<template>
  <q-layout view="hHh lpR fFf">

    <q-page-container>
      <router-view />
    </q-page-container>

    <CustomFooter/>
  </q-layout>
</template>

<script>
import CustomFooter from 'components/CustomFooter.vue'
import { Loading } from 'quasar'
import { useAuthStore } from 'stores/auth-store.js'
export default {
  name: 'BodyAndFooterLayout',
  components: { CustomFooter },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()
    return authStore.setUser().finally(() => Loading.hide())
  }
}
</script>
