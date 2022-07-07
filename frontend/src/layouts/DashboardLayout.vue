<template>
  <q-layout view="hHh lpR fFf">

    <q-drawer
      v-if="!utilStore.isMobile"
      :breakpoint="0"
      :width="200"
      side="left"
      show-if-above
      :mini="!isLeftDrawerOpen"
      bordered
    >
      <q-scroll-area class="fit">
        <q-list class="text-gray-500">
          <q-item
            v-if="isLeftDrawerOpen"
            class="items-end bg-gray-100"
            title="Close menu"
          >
            <q-item-section class="items-start">
              <img src="../assets/jobVyneLogo.png" alt="Logo" style="height: 30px; object-fit: scale-down">
            </q-item-section>
          </q-item>
          <q-item v-else class="bg-gray-100">
            <q-item-section avatar>
              <img src="../assets/jobVyneLogoOnly.png" alt="Logo" style="height: 30px; object-fit: scale-down">
            </q-item-section>
          </q-item>
          <template v-for="(menuItem, index) in menuList" :key="index">
            <q-item
              clickable
              :active="menuItem.key === pageKey"
              :class="(menuItem.key === pageKey) ? 'border-left-4-primary' : ''"
              @click="redirectUrl(menuItem.key)"
              v-ripple
            >
              <q-item-section avatar>
                <q-icon :name="menuItem.icon"/>
              </q-item-section>
              <q-item-section>
                {{ menuItem.label }}
              </q-item-section>
            </q-item>
            <q-separator :key="'sep' + index" v-if="menuItem.separator"/>
          </template>
          <q-item
            clickable
            @click="authStore.logout"
            v-ripple
          >
            <q-item-section avatar>
              <q-icon name="logout"/>
            </q-item-section>
            <q-item-section>
              Logout
            </q-item-section>
          </q-item>

        </q-list>
      </q-scroll-area>
      <div class="absolute" style="top: 10px; right: -16px">
        <q-btn
          dense
          round
          unelevated
          color="accent"
          :icon="(isLeftDrawerOpen) ? 'chevron_left' : 'chevron_right'"
          @click="isLeftDrawerOpen=!isLeftDrawerOpen"
        />
      </div>
    </q-drawer>

    <q-drawer show-if-above v-if="isRightDrawerOpen" side="right" bordered>
      <!-- drawer content -->
    </q-drawer>

    <q-page-container>
      <BannerMessage/>
      <router-view/>
    </q-page-container>

    <q-footer v-if="utilStore.isMobile" bordered reveal class="bg-gray-500 row scroll-x scrollbar-narrow-x">
      <div
        v-for="menuItem in menuList"
        class="col-3 q-py-sm"
        :class="(menuItem.key === pageKey) ? 'text-primary q-active' : ''"
        @click="redirectUrl(menuItem.key)"
        v-ripple
      >
        <div class="text-center">
          <q-icon :name="menuItem.icon" size="24px"/>
        </div>
        <div class="text-center">{{ menuItem.label }}</div>
      </div>
      <div class="col-3 q-py-sm" v-ripple @click="authStore.logout">
        <div class="text-center">
          <q-icon name="logout" size="24px"/>
        </div>
        <div class="text-center">Logout</div>
      </div>
    </q-footer>

  </q-layout>
</template>

<script>
import BannerMessage from 'components/BannerMessage.vue'
import { useUtilStore } from 'stores/utility-store'
import { useAuthStore } from 'stores/auth-store'

const menuList = [
  {
    icon: 'home',
    key: 'dashboard',
    label: 'Dashboard',
    separator: false
  },
  {
    icon: 'link',
    key: 'links',
    label: 'Referral Links',
    separator: false
  },
  {
    icon: 'person',
    key: 'profile',
    label: 'Profile',
    separator: false
  },
  {
    icon: 'share',
    key: 'social-accounts',
    label: 'Social Accounts',
    separator: false
  },
  {
    icon: 'message',
    key: 'messages',
    label: 'Messages',
    separator: false
  },
  {
    icon: 'dynamic_feed',
    key: 'content',
    label: 'Content',
    separator: true
  },
  {
    icon: 'settings',
    key: 'settings',
    label: 'Settings',
    separator: false
  },
  {
    icon: 'feedback',
    key: 'feedback',
    label: 'Send Feedback',
    separator: false
  },
  {
    icon: 'help',
    key: 'help',
    label: 'Help',
    separator: false
  }
]

export default {
  components: { BannerMessage },
  data () {
    return {
      isLeftDrawerOpen: true,
      isRightDrawerOpen: false,
      pageKey: null,
      menuList
    }
  },
  methods: {
    getPageKey () {
      /**
       * Get the last part of the page path which will align with the page key
       * @type {string}
       */
      let path = window.location.pathname
      path = path.split('?')[0] // Remove any params
      const pathParts = path.split('/')
      const lastVal = pathParts[pathParts.length - 1]

      // The last part of the path could be a slash, so we need to protect against that
      if (lastVal) {
        return lastVal
      } else {
        return pathParts[pathParts.length - 2]
      }
    },
    toggleDrawerOpen () {
      this.isRightDrawerOpen = !this.isRightDrawerOpen
    },
    redirectUrl (key) {
      const url = (key === 'dashboard') ? `/${key}` : `/dashboard/${key}`
      this.pageKey = key
      this.$router.push(url)
    }
  },
  setup () {
    return {
      authStore: useAuthStore(),
      utilStore: useUtilStore()
    }
  },
  mounted () {
    this.pageKey = this.getPageKey()
  }
}
</script>

<style lang="scss" scoped>
.scroll-x {
  overflow-x: scroll;
  flex-wrap: nowrap;
}
</style>
