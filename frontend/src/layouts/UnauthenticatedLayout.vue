<template>
  <q-layout view="hHh lpr fFf">

    <q-header elevated reveal class="bg-white text-primary justify-center row">
      <q-toolbar class="col-12 col-md-11 col-lg-8 q-py-md">
        <a href="/">
          <q-toolbar-title>
            <img src="../assets/jobVyneLogo.png" alt="Logo" style="height: 40px; object-fit: scale-down">
          </q-toolbar-title>
        </a>
        <q-space/>
        <q-tabs class="gt-sm" align="right" shrink>
          <q-tab v-if="authStore.isAuthenticated" label="Logout" @click="authStore.logout"/>
          <q-route-tab v-else to="/login" label="Login"/>
        </q-tabs>
        <div class="lt-md q-pa-md" style="max-width: 250px">
          <q-btn-dropdown
            no-icon-animation
            flat dense rounded
            dropdown-icon="menu"
            aria-label="Menu"
          >
            <q-list
              bordered padding
              class="rounded-borders text-primary"
            >
              <q-item
                v-if="authStore.isAuthenticated"
                exact clickable v-close-popup
                v-ripple
                label="Logout"
                @click="authStore.logout"
              >
                <q-item-section>
                  Logout
                </q-item-section>
              </q-item>
              <q-item
                v-else
                exact clickable v-close-popup
                v-ripple
                to="/login"
                label="Login"
              >
                <q-item-section>
                  Login
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <BannerMessage/>
      <router-view/>
    </q-page-container>

    <q-footer elevated reveal class="bg-grey-8 text-white justify-center row">
      <q-toolbar class="col-12 col-md-11 col-lg-8 q-py-md">
        <q-toolbar-title>
          <img src="../assets/jobVyneLogoWhite.png" alt="Logo" style="height: 40px; object-fit: scale-down">
        </q-toolbar-title>
        <q-tabs align="right" shrink>
          <q-route-tab to="/privacy" label="Privacy"/>
          <q-route-tab to="/terms-of-service" label="Terms of Service"/>
        </q-tabs>
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

<script>
import { useAuthStore } from 'stores/auth-store'
import BannerMessage from 'components/BannerMessage.vue'

export default {
  name: 'UnauthenticatedLayout',
  components: { BannerMessage },
  setup () {
    const authStore = useAuthStore()
    return { authStore }
  }
}
</script>

<style scoped>

</style>
