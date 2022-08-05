<template>
  <q-layout view="hHh lpR fFf">

    <q-drawer
      v-if="!utilStore.isMobile"
      :breakpoint="0"
      :width="250"
      side="left"
      show-if-above
      :mini="!isLeftDrawerOpen"
      bordered
    >
      <q-scroll-area class="fit text-gray-500">
        <q-list>
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
          <template v-if="isLeftDrawerOpen && userViewOptions.length > 1">
            <q-btn-dropdown
              flat unelevated
              :label="`View mode: ${userCfgMap[viewerModeBit].viewLabel}`"
              align="around"
              class="w-100 text-bold"
            >
              <q-list>
                <q-item v-for="viewOption in userViewOptions" clickable @click="changeViewMode(viewOption.userBit)">
                  <q-item-section avatar>
                    <q-icon :name="viewOption.icon"/>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>{{ viewOption.label }}</q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-btn-dropdown>
            <q-separator/>
          </template>
          <template v-for="(menuItem, index) in menuList">
            <q-item
              clickable
              :active="menuItem.key === pageKey"
              :class="(menuItem.key === pageKey) ? 'border-left-4-primary' : ''"
              @click="$router.push(pagePermissionsUtil.getRouterPageCfg(menuItem.key))"
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
          dense round unelevated
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

    <q-footer v-if="utilStore.isMobile" bordered reveal class="bg-gray-500 row scroll-x scrollbar-narrow">
      <q-btn-dropdown
        v-if="userViewOptions.length > 1"
        flat unelevated stack
        icon="fas fa-caret-up"
        dropdown-icon="none"
        class="border-right-1-white"
        style="margin-bottom: -20px;"
      >
        <template v-slot:label>
          <div class="text-small">View mode</div>
          <div class="text-bold">{{ userCfgMap[viewerModeBit].viewLabel }}</div>
        </template>
        <q-list>
          <q-item v-for="viewOption in userViewOptions" clickable @click="changeViewMode(viewOption.userBit)">
            <q-item-section avatar>
              <q-icon :name="viewOption.icon"/>
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ viewOption.label }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
      <div
        v-for="menuItem in menuList"
        class="col-3 q-py-sm"
        :class="getMobileMenuItemClasses(menuItem)"
        @click="$router.push(pagePermissionsUtil.getRouterPageCfg(menuItem.key))"
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
import { storeToRefs } from 'pinia/dist/pinia'
import { useUtilStore } from 'stores/utility-store'
import { useAuthStore } from 'stores/auth-store'
import { Loading } from 'quasar'
import pagePermissionsUtil from 'src/utils/permissions.js'
import { USER_TYPES } from 'src/utils/user-types'

const generalMenuList = [
  {
    icon: 'badge',
    key: 'profile',
    label: 'Profile',
    separator: false
  },
  {
    icon: 'message',
    key: 'messages',
    label: 'Messages',
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
      pagePermissionsUtil,
      userCfgMap: pagePermissionsUtil.userCfgMap
    }
  },
  computed: {
    menuList () {
      if (!this.viewerModeBit) {
        return generalMenuList
      }
      const userMenuList = pagePermissionsUtil.filterViewablePages(this.user, this.viewerModeBit)

      // Add a separator between user type specific items and general items
      if (userMenuList.length) {
        userMenuList[userMenuList.length - 1].separator = true
      }
      return [...userMenuList, ...generalMenuList]
    },
    pageKey () {
      return this.$route.name
    },
    viewerModeBit () {
      const viewerModeBit = Object.entries(this.userCfgMap).reduce((matchedUserBit, [userBit, cfg]) => {
        if (cfg.namespace === this.$route.params.namespace) {
          return userBit
        }
        return matchedUserBit
      }, 0)
      return viewerModeBit || this.getDefaultUserModeBit()
    },
    userViewOptions () {
      return this.authStore.propUserTypeBitsList.map((userBit) => {
        return {
          label: this.userCfgMap[userBit].viewLabel,
          icon: this.userCfgMap[userBit].viewIcon,
          userBit
        }
      })
    }
  },
  methods: {
    changeViewMode (viewModeBit) {
      this.$router.push(pagePermissionsUtil.getDefaultLandingPage(this.user, viewModeBit))
    },
    getDefaultUserModeBit () {
      const viewModePrioritized = [
        USER_TYPES.Admin,
        USER_TYPES.Employer,
        USER_TYPES.Influencer,
        USER_TYPES.Employee,
        USER_TYPES.Candidate
      ]
      for (const userBit of viewModePrioritized) {
        if (userBit & this.authStore.propUserTypeBits) {
          return userBit
        }
      }
    },
    getMobileMenuItemClasses (menuItem) {
      let classTxt = ''
      if (menuItem.key === this.pageKey) {
        classTxt += 'text-primary q-active'
      }
      if (menuItem.separator) {
        classTxt += ' border-right-1-white'
      }
      return classTxt
    }
  },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()
    return authStore.setUser().finally(() => Loading.hide())
  },
  setup () {
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return {
      authStore: useAuthStore(),
      utilStore: useUtilStore(),
      user
    }
  }
}
</script>

<style lang="scss" scoped>
.scroll-x {
  overflow-x: scroll;
  flex-wrap: nowrap;
}
</style>
