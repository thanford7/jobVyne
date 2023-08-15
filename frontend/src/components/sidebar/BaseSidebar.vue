<template>
  <q-drawer
    :side="side" bordered persistent
    :width="300"
    :breakpoint="500"
    :mini="isDrawerMini"
    @mouseover="isDrawerMini = false"
    @mouseout="isDrawerMini = true"
  >
    <q-scroll-area class="fit text-gray-500">
      <q-list>
        <q-item class="bg-gray-100">
          <q-item-section avatar>
            <img
              v-if="isDrawerMini"
              src="../../assets/jobVyneLogoOnly.png" alt="Logo"
              style="height: 30px; object-fit: scale-down"
            >
            <img
              v-else
              src="../../assets/jobVyneLogo.png" alt="Logo"
              style="height: 30px; object-fit: scale-down"
            >
          </q-item-section>
        </q-item>
        <slot name="menuItems"/>
        <q-separator />
        <SidebarMenuItem
          icon-name="feedback" menu-label="Get help"
          @click="openFeedbackModal()"
        />
        <SidebarMenuItem
          v-if="user && !dataUtil.isEmpty(user)"
          icon-name="logout" menu-label="Logout"
          @click.prevent="logout()"
        />
        <SidebarMenuItem
          v-else
          icon-name="login" menu-label="Login or Sign Up"
          @click="openLoginModal()"
        />

      </q-list>
    </q-scroll-area>
  </q-drawer>
</template>
<script>
import DialogFeedback from 'components/dialogs/DialogFeedback.vue'
import DialogLogin from 'components/dialogs/DialogLogin.vue'
import SidebarMenuItem from 'components/sidebar/SidebarMenuItem.vue'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { USER_TYPE_CANDIDATE, USER_TYPES } from 'src/utils/user-types.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useUtilStore } from 'stores/utility-store.js'

export default {
  name: 'BaseSidebar',
  components: { SidebarMenuItem },
  props: {
    side: String,
    isRedirectOnLogout: {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      isDrawerMini: true,
      user: null,
      dataUtil,
      authStore: useAuthStore(),
      utilStore: useUtilStore(),
      q: useQuasar()
    }
  },
  methods: {
    openFeedbackModal () {
      return this.q.dialog({
        component: DialogFeedback
      })
    },
    openLoginModal () {
      this.q.dialog({
        component: DialogLogin,
        componentProps: {
          redirectPageUrl: window.location.pathname,
          redirectParams: dataUtil.getQueryParams(),
          userTypeBit: USER_TYPES[USER_TYPE_CANDIDATE]
        }
      }).onOk(async () => {
        await this.authStore.setUser(true)
        this.user = this.authStore.propUser
        this.$emit('login')
      })
    },
    async logout () {
      await this.authStore.logout(null)
      await this.authStore.setUser(true)
      this.user = this.authStore.propUser
      this.$emit('logout')
    }
  },
  async mounted () {
    await this.authStore.setUser()
    this.user = this.authStore.propUser
  }
}
</script>
