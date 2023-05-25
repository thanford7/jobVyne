<template>
  <div>
    <div class="row q-pb-sm border-bottom-2-gray-300">
      <div v-if="billingBannerMsg" class="col-12">
        <q-banner rounded class="bg-warning">
          <q-icon name="warning" size="32px"/>
          &nbsp;{{ billingBannerMsg }}
          Please go to your
          <router-link
            :to="{ name: 'employer-settings', params: { key: 'employer-settings' }, query: { tab: 'billing' } }">
            billing page
          </router-link>
          to update your subscription.
        </q-banner>
      </div>
      <div class="col-12">
        <div class="header" :class="(isIncludeLogo) ? 'header-logo' : ''">
          <div v-if="isIncludeLogo" class="flex flex-center q-py-sm">
            <img src="~assets/jobVyneLogo.png" alt="Logo" style="height: 40px; object-fit: scale-down">
          </div>
          <slot name="title">
            <div>
              <h5 class="text-gray-900">{{ title }}</h5>
            </div>
          </slot>
          <div
            v-if="isIncludeSidebarToggle"
            class="flex items-center justify-end q-mr-md"
            :class="(utilStore.isUnderBreakPoint('md')) ? 'flex-center' : 'items-center justify-end'"
          >
            <q-btn @click="$emit('toggleLeftDrawer')" unelevated round dense icon="menu" color="primary"/>
          </div>
        </div>
      </div>
      <div class="col-12">
        <p class="text-gray-500 q-mt-none">
          <slot/>
        </p>
      </div>
      <div class="col-12">
        <slot name="bottom"/>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useUtilStore } from 'stores/utility-store.js'

export default {
  name: 'PageHeader',
  props: {
    title: {
      type: String
    },
    isIncludeLogo: {
      type: Boolean,
      default: false
    },
    isIncludeSidebarToggle: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      billingBannerMsg: null,
      utilStore: useUtilStore()
    }
  },
  async mounted () {
    const { namespace } = this.$route.params
    if (namespace === 'employer') {
      const employerStore = useEmployerStore()
      const authStore = useAuthStore()
      await authStore.setUser()
      await employerStore.setEmployerSubscription(authStore.propUser.employer_id)
      const {
        is_active: isEmployerActive,
        has_seats: hasSeats
      } = employerStore.getEmployerSubscription(authStore.propUser.employer_id)
      if (!isEmployerActive || !hasSeats) {
        if (!isEmployerActive) {
          this.billingBannerMsg = 'Your subscription is currently not active.'
        }
        if (!hasSeats) {
          this.billingBannerMsg = 'You have reached the number of allowable active employees based on your subscription.'
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.header {
  display: grid;
  grid-template-columns: 75% 25%;
  grid-column-gap: 5px;

  &.header-logo {
    grid-template-columns: 25% 50% 25%;
  }

  @media (max-width: 767px) {
    grid-template-columns: 1fr;
  }
}
</style>
