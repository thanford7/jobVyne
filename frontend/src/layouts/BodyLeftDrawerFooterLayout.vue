<template>
  <q-layout view="hHh lpR fFf">
<!--    Drawer is dynamic so we put it inside the page view-->
    <router-view />
    <CustomFooter/>
  </q-layout>
</template>

<script>
import CustomFooter from 'components/CustomFooter.vue'
import { Loading } from 'quasar'
import { useAuthStore } from 'stores/auth-store.js'

export default {
  name: 'BodyLeftDrawerFooterLayout',
  components: { CustomFooter },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()
    return authStore.setUser().finally(() => Loading.hide())
  }
}
</script>
