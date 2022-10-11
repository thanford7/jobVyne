<template>
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
      <h5 class="text-gray-900">{{ title }}</h5>
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
</template>

<script>
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'PageHeader',
  props: {
    title: {
      type: String
    }
  },
  data () {
    return {
      billingBannerMsg: null
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
