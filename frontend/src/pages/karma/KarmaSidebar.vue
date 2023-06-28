<template>
  <q-drawer
    v-if="user && !dataUtil.isEmpty(user)"
    side="left" show-if-above bordered
    :mini="isLeftDrawerMini"
  >
    <q-scroll-area class="fit text-gray-500">
      <q-list>
        <q-item class="bg-gray-100">
          <q-item-section avatar>
            <img src="~assets/jobVyneLogoOnly.png" alt="Logo" style="height: 30px; object-fit: scale-down">
          </q-item-section>
        </q-item>
        <q-item
          clickable
          @click="authStore.logout()"
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
    <div v-if="!utilStore.isUnderBreakPoint('md')" class="absolute" style="top: 10px; right: -16px">
      <q-btn
        dense round unelevated
        color="accent"
        :icon="(isLeftDrawerMini) ? 'chevron_left' : 'chevron_right'"
        @click="isLeftDrawerMini = !isLeftDrawerMini"
      />
    </div>
  </q-drawer>
</template>

<script>
import dataUtil from 'src/utils/data.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useUtilStore } from 'stores/utility-store.js'

export default {
  name: 'KarmaSidebar',
  props: {
    user: [Object, null]
  },
  data () {
    return {
      isLeftDrawerMini: false,
      dataUtil,
      authStore: useAuthStore(),
      utilStore: useUtilStore()
    }
  }
}
</script>
