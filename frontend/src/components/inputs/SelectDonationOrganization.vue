<template>
  <q-select
    ref="select"
    filled use-input clearable
    :multiple="isMulti" :use-chips="isMulti"
    :options="donationOrganizations"
    :loading="isLoading"
    @input-value="getOrgsDebounceFn"
    new-value-mode="add-unique"
    option-value="ein"
    option-label="name"
    :label="label"
    hint="Search by name or category"
    lazy-rules
    :rules="rules"
  >
    <template v-slot:selected-item="scope">
      <q-chip v-if="isMulti" clickable removable>
        <span class="ellipsis" :title="scope.opt.name">{{ scope.opt.name }}</span>
      </q-chip>
      <span v-else class="ellipsis" :title="scope.opt.name">{{ scope.opt.name }}</span>
    </template>
    <template v-slot:no-option>
      <q-item>
        <q-item-section class="text-italic text-grey">
          Begin typing...
        </q-item-section>
      </q-item>
    </template>
    <template v-slot:option="scope">
      <q-item v-bind="scope.itemProps" class="border-bottom-1-gray-1">
        <q-item-section avatar>
          <q-img :src="scope.opt.logoUrl" alt="Organization logo"/>
        </q-item-section>
        <q-item-section>
          <q-item-label>
            {{ scope.opt.name }}
            <a :href="scope.opt.profileUrl" target="_blank" @click.stop>
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
import { debounce } from 'quasar'

export default {
  name: 'SelectDonationOrganization',
  props: {
    isMulti: Boolean,
    isRequired: {
      type: Boolean,
      default: false
    },
    label: {
      type: [String, null],
      default: 'Donation organization'
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
  data () {
    return {
      isLoading: false,
      donationOrganizations: null,
      getOrgsDebounceFn: null
    }
  },
  methods: {
    async getOrgOptions (searchText) {
      if (!searchText || !searchText.length) {
        return
      }
      this.isLoading = true
      const resp = await this.$api.get('search/donation-org/', {
        params: { search_text: searchText }
      })
      this.donationOrganizations = resp.data
      this.isLoading = false
      this.$refs.select.refresh()
      this.$refs.select.showPopup()
    }
  },
  async mounted () {
    this.getOrgsDebounceFn = debounce(this.getOrgOptions, 500)
  }
}
</script>
