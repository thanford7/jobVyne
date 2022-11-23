<template>
  <q-layout view="hHh lpr fFf">

    <q-header elevated reveal class="bg-white text-primary justify-center row">
      <q-toolbar class="col-12 col-md-11 col-lg-8 q-py-md">
        <a href="/">
          <q-toolbar-title>
            <img src="~assets/jobVyneLogo.png" alt="Logo" style="height: 40px; object-fit: scale-down">
          </q-toolbar-title>
        </a>
        <q-space/>
        <q-tabs class="gt-sm" align="right" shrink>
          <template v-if="authStore.propIsAuthenticated">
            <q-route-tab :to="pagePermissionsUtil.getDefaultLandingPage(authStore.propUser)" label="Dashboard"/>
            <q-tab id="jv-logout-btn" label="Logout" @click="authStore.logout()"/>
          </template>
          <template v-else>
            <q-route-tab :to="{ name: 'login', query: { isNew: 0 } }" label="Login"/>
            <q-route-tab
              :to="{ name: 'login', query: { isNew: 1 } }"
              label="Sign up"
              class="bg-accent text-white"
            />
          </template>
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
              <template v-if="authStore.propIsAuthenticated">
                <q-item
                  exact clickable v-close-popup
                  v-ripple
                  label="Dashboard"
                  :to="pagePermissionsUtil.getDefaultLandingPage(authStore.propUser)"
                >
                  <q-item-section>
                    Dashboard
                  </q-item-section>
                </q-item>
                <q-item
                  exact clickable v-close-popup
                  v-ripple
                  label="Logout"
                  @click="authStore.logout()"
                >
                  <q-item-section>
                    Logout
                  </q-item-section>
                </q-item>
              </template>
              <template v-else>
                <q-item
                  exact clickable v-close-popup
                  v-ripple
                  :to="{ name: 'login', query: { isNew: 0 } }"
                >
                  <q-item-section>
                    Login
                  </q-item-section>
                </q-item>
                <q-item
                  exact clickable v-close-popup
                  v-ripple
                  :to="{ name: 'login', query: { isNew: 1 } }"
                >
                  <q-item-section>
                    Sign up
                  </q-item-section>
                </q-item>
              </template>
            </q-list>
          </q-btn-dropdown>
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view/>
    </q-page-container>

    <CustomFooter/>

  </q-layout>
</template>

<script>
import { loadScript } from 'src/utils/load-script.js'
import pagePermissionsUtil from 'src/utils/permissions.js'
import { useAuthStore } from 'stores/auth-store'
import CustomFooter from 'components/CustomFooter.vue'
import { Loading } from 'quasar'

export default {
  name: 'LandingLayout',
  components: { CustomFooter },
  data () {
    return {
      pagePermissionsUtil
    }
  },
  async created () {
    await loadScript(`https://www.google.com/recaptcha/enterprise.js?render=${process.env.GOOGLE_CAPTCHA_KEY}`)
  },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()
    return authStore.setUser().finally(() => Loading.hide())
  },
  setup () {
    const authStore = useAuthStore()
    return { authStore }
  }
}
</script>
