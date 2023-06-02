<template>
  <q-select
    filled clearable map-options emit-value
    :multiple="isMulti" :use-chips="isMulti"
    :options="userDonationOrgs"
    option-label="name"
    option-value="id"
    label="Donation organization"
    lazy-rules
    :rules="rules"
  >
    <template v-slot:option="scope">
      <q-item v-bind="scope.itemProps" class="border-bottom-1-gray-1">
        <q-item-section avatar>
          <q-img :src="scope.opt.logo_url" alt="Organization logo"/>
        </q-item-section>
        <q-item-section>
          <q-item-label>
            {{ scope.opt.name }}
            <a :href="scope.opt.url_main" target="_blank" @click.stop>
              <q-icon name="open_in_new"/>
            </a>
          </q-item-label>
          <q-item-label caption>{{ scope.opt.description || 'No description' }}</q-item-label>
        </q-item-section>
      </q-item>
    </template>
  </q-select>
</template>

<script>
import { useAuthStore } from 'stores/auth-store.js'
import { useKarmaStore } from 'stores/karma-store.js'

export default {
  name: 'SelectUserDonationOrganization',
  props: {
    isMulti: {
      type: Boolean,
      default: false
    },
    isRequired: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoading: false,
      userDonationOrgs: []
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
          (val) => Boolean(val) || 'This field is required'
        ]
      }
    }
  },
  async mounted () {
    const authStore = useAuthStore()
    const karmaStore = useKarmaStore()
    this.isLoading = true
    await karmaStore.setUserDonationOrganizations(authStore.propUser.id)
    this.userDonationOrgs = karmaStore.getUserDonationOrganizations(authStore.propUser.id)
    this.isLoading = false
  }
}
</script>
