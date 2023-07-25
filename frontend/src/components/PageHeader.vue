<template>
  <div>
    <div class="q-pb-sm border-bottom-2-gray-300">
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
      <div>
        <div class="header" :class="(isIncludeJobVyneLogo) ? 'header-jv-logo' : ''" style="position: relative">
          <div v-if="isIncludeJobVyneLogo" class="flex flex-center q-py-sm">
            <img src="~assets/jobVyneLogo.png" alt="Logo" style="height: 40px; object-fit: scale-down">
          </div>
          <slot name="title">
            <div>
              <h5 class="text-gray-900">{{ title }}</h5>
            </div>
          </slot>
          <q-img
            v-if="!isIncludeJobVyneLogo && employer?.logo_square_88_url"
            :src="employer.logo_square_88_url"
            alt="Logo" width="50px"
            style="position: absolute; top: 10px; right: 10px;"
          />
          <div
            v-if="isIncludeSidebarToggle"
            class="flex items-center justify-end q-mr-md"
            :class="(utilStore.isUnderBreakPoint('md')) ? 'flex-center' : 'items-center justify-end'"
          >
            <q-btn @click="$emit('toggleLeftDrawer')" unelevated round dense icon="menu" color="primary"/>
          </div>
        </div>
      </div>
      <div>
        <p class="text-gray-500 q-mt-none">
          <slot/>
        </p>
      </div>
      <div>
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
    isIncludeJobVyneLogo: {
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
      employer: null,
      billingBannerMsg: null,
      utilStore: useUtilStore()
    }
  },
  async mounted () {
    const { namespace } = this.$route.params
    if (['employer', 'employee'].includes(namespace)) {
      const employerStore = useEmployerStore()
      const authStore = useAuthStore()
      await authStore.setUser()
      const employerId = authStore.propUser.employer_id
      await employerStore.setEmployer(employerId)
      this.employer = employerStore.getEmployer(employerId)
      if (namespace === 'employer') {
        await employerStore.setEmployerSubscription(employerId)
        const {
          is_active: isEmployerActive,
          has_seats: hasSeats
        } = employerStore.getEmployerSubscription(employerId)
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
}
</script>

<style lang="scss" scoped>
.header {
  display: grid;
  grid-template-columns: 75% 25%;
  grid-column-gap: 5px;

  &.header-jv-logo {
    grid-template-columns: 25% 50% 25%;
    @media (max-width: 767px) {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 767px) {
    grid-template-columns: 1fr;
  }
}
</style>
