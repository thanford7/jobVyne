<template>
  <q-drawer :mini="!isLeftDrawerOpen" side="left" overlay bordered persistent show-if-above>
    <q-scroll-area class="fit text-gray-500">
      <q-list>
        <q-item v-if="user && !dataUtil.isEmpty(user)">
          <q-item-section avatar>
            <q-avatar color="primary" text-color="white">
              <img v-if="user.profile_picture_url" :src="user.profile_picture_url">
              <span v-else>{{ userUtil.getUserInitials(user) }}</span>
            </q-avatar>
          </q-item-section>
        </q-item>
        <q-item v-if="user && !dataUtil.isEmpty(user)">
          <q-item-section>
            <q-btn
              id="jv-logout"
              dense round unelevated color="grey" icon="logout" title="Logout"
              @click="$emit('logoutUser')"
            />
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
</template>

<script>
import dataUtil from 'src/utils/data.js'
import userUtil from 'src/utils/user.js'

export default {
  name: 'UserSidebar',
  props: {
    user: [Object, null]
  },
  data () {
    return {
      isLeftDrawerOpen: true,
      dataUtil,
      userUtil
    }
  }
}
</script>
