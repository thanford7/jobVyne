<template>
  <div>
    <q-drawer
      v-model="isLeftDrawerOpen"
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
            v-ripple
            @click="openUserRequestDialog()"
          >
            <q-item-section avatar>
              <q-icon name="volunteer_activism"/>
            </q-item-section>
            <q-item-section>
              Create request
            </q-item-section>
          </q-item>
          <q-item
            clickable
            v-ripple
            @click="openUserDonationOrganizationDialog()"
          >
            <q-item-section avatar>
              <q-icon name="add_business"/>
            </q-item-section>
            <q-item-section>
              Add donation organization
            </q-item-section>
          </q-item>
          <q-item
            clickable
            v-ripple
            @click="openUserDonationDialog()"
          >
            <q-item-section avatar>
              <q-icon name="price_check"/>
            </q-item-section>
            <q-item-section>
              Add donation
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

    <q-page-container>
      <q-page padding>
        <div class="q-pb-sm header border-bottom-2-gray-300">
          <div class="flex flex-center q-py-sm">
            <img src="~assets/jobVyneLogo.png" alt="Logo" style="height: 40px; object-fit: scale-down">
          </div>
          <div class="self-center title">
            <h4 class="q-mb-none text-center">KARMA CONNECT</h4>
            <div class="text-center">Do Good While Doing Good</div>
          </div>
          <div class="flex items-center justify-end q-pa-md q-mr-md"
               :class="(utilStore.isUnderBreakPoint('md')) ? 'flex-center' : 'items-center justify-end'">
            <q-btn @click="isLeftDrawerOpen = !isLeftDrawerOpen" unelevated round dense icon="menu" color="primary"/>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </div>
</template>

<script>
import DialogUserDonation from 'components/dialogs/DialogUserDonation.vue'
import DialogUserDonationOrganization from 'components/dialogs/DialogUserDonationOrganization.vue'
import DialogUserRequest from 'components/dialogs/DialogUserRequest.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { useMeta, useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useUtilStore } from 'stores/utility-store.js'

export default {
  name: 'ConnectionRequestPage',
  data () {
    return {
      isLeftDrawerMini: false,
      isLeftDrawerOpen: true,
      dataUtil
    }
  },
  methods: {
    openUserDonationDialog () {
      return this.q.dialog({
        component: DialogUserDonation
      })
    },
    openUserDonationOrganizationDialog () {
      return this.q.dialog({
        component: DialogUserDonationOrganization
      })
    },
    openUserRequestDialog () {
      return this.q.dialog({
        component: DialogUserRequest
      })
    }
  },
  setup () {
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)

    useMeta(globalStore.getMetaCfg({
      pageTitle: 'Karma Connect',
      description: 'Do good while doing good'
    }))

    return {
      user,
      authStore,
      utilStore: useUtilStore(),
      q: useQuasar()
    }
  }
}
</script>

<style lang="scss" scoped>
.header {
  display: grid;
  grid-template-columns: 25% 50% 25%;
  grid-column-gap: 5px;

  @media (max-width: 767px) {
    grid-template-columns: 1fr;
  }
}
</style>
