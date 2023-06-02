<template>
  <KarmaContainer v-if="isLoaded">
    <div class="row">
      <div class="col-12 col-md-6">
        <p>
          Hi {{ userRequest.connection_first_name }},
        </p>
        <p>
          Thanks for considering meeting with me 😃 I'm trying to learn more about the HR and Talent Acquisition
          industry and am connecting with experts like you!
        </p>
        <p>
          I'd love to make a donation of $10 to charity since you are doing me a favor by meeting with me. Please
          choose one of the charities I support or pick your own.
        </p>
        <div class="q-pl-md">
          <q-list separator>
            <q-item tag="label" v-ripple v-for="org in donationOrganizations">
              <q-item-section avatar top>
                <q-radio v-model="selectedDonationOrg" :val="org.ein"/>
              </q-item-section>
              <q-item-section avatar>
                <q-img :src="org.logo_url" width="40px" alt="Organization logo"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>
                  {{ org.name }}
                  <a :href="org.url_main" target="_blank" @click.stop>
                    <q-icon name="open_in_new"/>
                  </a>
                </q-item-label>
                <q-item-label caption>{{ org.description }}</q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar top>
                <q-radio ref="customDonationRadio" v-model="selectedDonationOrg" :val="customDonationSelectionKey"/>
              </q-item-section>
              <q-item-section avatar>
                <q-img v-if="customDonationOrg" :src="customDonationOrg.logoUrl || customDonationOrg.logo_url" width="40px" alt="Organization logo"/>
              </q-item-section>
              <q-item-section>
                <SelectDonationOrganization
                  v-model="customDonationOrg"
                  :is-multi="false"
                  label="Select your own"
                />
              </q-item-section>
            </q-item>
          </q-list>
        </div>
        <p>
          I will make the donation after we meet.
        </p>
        <p>
          {{ user.first_name }}
        </p>
      </div>
    </div>
  </KarmaContainer>
</template>

<script>
import SelectDonationOrganization from 'components/inputs/SelectDonationOrganization.vue'
import KarmaContainer from 'pages/karma/KarmaContainer.vue'
import { Loading, useMeta } from 'quasar'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useKarmaStore } from 'stores/karma-store.js'

export default {
  name: 'ConnectionRequestPage',
  components: { SelectDonationOrganization, KarmaContainer },
  data () {
    return {
      isLoaded: false,
      requestId: null,
      userRequest: null,
      user: null,
      donationOrganizations: null,
      selectedDonationOrg: null,
      customDonationOrg: null,
      customDonationSelectionKey: 'custom'
    }
  },
  watch: {
    selectedDonationOrg: {
      async handler () {
        await this.updateSelectedDonationOrg()
      }
    },
    customDonationOrg: {
      async handler () {
        this.$refs.customDonationRadio?.set()
        await this.updateSelectedDonationOrg()
      }
    }
  },
  methods: {
    getSelectedDonationOrgEin () {
      if (this.selectedDonationOrg === this.customDonationSelectionKey) {
        return this.customDonationOrg?.ein
      } else {
        return this.selectedDonationOrg
      }
    },
    async updateSelectedDonationOrg () {
      const ein = this.getSelectedDonationOrgEin()
      if (!ein || (ein === this.userRequest.connection_donation_org.ein)) {
        return
      }
      await this.saveSelectedDonationOrg(ein)
    },
    async saveSelectedDonationOrg (ein) {
      await this.$api.put('karma/connection-donation-organization/', getAjaxFormData({
        request_id: this.requestId,
        ein
      }))
      await this.karmaStore.setUserRequest(this.requestId, true)
      const userRequestData = this.karmaStore.getUserRequest(this.requestId)
      this.userRequest = userRequestData.user_request
    }
  },
  async mounted () {
    this.requestId = this.$route.params.requestId
    await this.karmaStore.setUserRequest(this.requestId)
    const userRequestData = this.karmaStore.getUserRequest(this.requestId)
    this.userRequest = userRequestData.user_request
    this.user = userRequestData.user
    this.donationOrganizations = userRequestData.donation_organizations
    if (this.donationOrganizations.map((org) => org.id).includes(this.userRequest.connection_donation_org.id)) {
      this.selectedDonationOrg = this.userRequest.connection_donation_org.ein
    } else {
      this.customDonationOrg = this.userRequest.connection_donation_org
      this.selectedDonationOrg = this.customDonationSelectionKey
    }
    this.isLoaded = true
  },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()

    useMeta(globalStore.getMetaCfg({
      pageTitle: 'JobVyne Connection',
      description: 'Making connections while doing good'
    }))

    return {
      authStore,
      karmaStore: useKarmaStore()
    }
  }
}
</script>
