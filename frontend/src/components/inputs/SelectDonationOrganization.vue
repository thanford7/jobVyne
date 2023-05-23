<template>
  <q-select
    v-if="isLoaded"
    filled map-options emit-value
    :options="donationOrganizations"
    option-value="id"
    option-label="name"
    label="Donation organization"
    lazy-rules
    :rules="rules"
  />
</template>

<script>
import { useKarmaStore } from 'stores/karma-store.js'

export default {
  name: 'SelectDonationOrganization',
  props: {
    isMulti: Boolean,
    isRequired: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    rules () {
      if (!this.isRequired) {
        return []
      } else if (this.isMulti) {
        return [
          (val) => (val && val.length) || 'This field is required'
        ]
      } else {
        return [
          (val) => val || 'This field is required'
        ]
      }
    }
  },
  data () {
    return {
      isLoaded: false,
      donationOrganizations: null
    }
  },
  async mounted () {
    const karmaStore = useKarmaStore()
    await karmaStore.setDonationOrganizations()
    this.donationOrganizations = karmaStore.getDonationOrganizations()
    this.isLoaded = true
  }
}
</script>
